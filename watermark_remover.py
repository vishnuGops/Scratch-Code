"""
Watermark remover — exemplar-based (patch-matching) inpainting.
Dependencies: Pillow, numpy only — works on ARM Windows.
Install: pip install Pillow numpy
"""

import time
import numpy as np
import argparse
from pathlib import Path
from PIL import Image


# ── Watermark geometry defaults (tune per photographer) ──────────────────────
DEFAULT_HEIGHT_PCT = 10.0   # % of image height
DEFAULT_WIDTH_PCT  = 40.0   # % of image width, centred
DEFAULT_PAD_PCT    = 0.0    # % from bottom edge (0 = flush to bottom)

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp", ".webp"}


# ── Image helpers ─────────────────────────────────────────────────────────────

def load_image(path: str) -> np.ndarray:
    return np.array(Image.open(path).convert("RGB"))


def build_mask(h: int, w: int, height_pct: float, width_pct: float, pad_pct: float) -> tuple:
    wm_h = max(1, int(h * height_pct / 100))
    wm_w = max(1, int(w * width_pct / 100))
    pad  = int(h * pad_pct / 100)
    x0   = (w - wm_w) // 2
    y0   = h - wm_h - pad
    mask = np.zeros((h, w), dtype=np.uint8)
    mask[y0:y0 + wm_h, x0:x0 + wm_w] = 1
    return mask, y0, y0 + wm_h - 1, x0, x0 + wm_w - 1


# ── Exemplar inpainting ───────────────────────────────────────────────────────

def _collect_source_patches(img: np.ndarray, mask: np.ndarray,
                             y_wm_top: int, half: int,
                             max_patches: int) -> tuple:
    """
    Gather candidate patches from the unmasked region above the watermark.
    Returns (src_flat [N, patch_pixels], centers [(cy, cx), ...]).
    """
    h, w = mask.shape
    patch_size = 2 * half + 1

    # Search up to 3x watermark height above it, but at least 60px
    search_h = max(60, 3 * (mask.sum(axis=1) > 0).sum())
    sy_start = max(half, y_wm_top - search_h)
    sy_end   = y_wm_top - half - 1

    if sy_end < sy_start:
        return None, None

    area   = (sy_end - sy_start + 1) * (w - 2 * half)
    stride = max(1, int((area / max_patches) ** 0.5))

    flat_list, centers = [], []
    for cy in range(sy_start, sy_end + 1, stride):
        for cx in range(half, w - half, stride):
            if mask[cy - half:cy + half + 1, cx - half:cx + half + 1].sum() == 0:
                flat_list.append(
                    img[cy - half:cy + half + 1, cx - half:cx + half + 1].reshape(-1)
                )
                centers.append((cy, cx))

    if not flat_list:
        return None, None

    return np.array(flat_list, dtype=np.float32), centers


def inpaint_exemplar(img: np.ndarray, mask: np.ndarray,
                     patch_size: int = 9, max_patches: int = 3000,
                     verbose: bool = False) -> np.ndarray:
    """
    Two-pass exemplar inpainting — only touches pixels where mask == 1.

    Pass 1 — Mirror init: each masked row is seeded by mirroring the
              content from the same distance above the watermark top,
              so patch matching starts from a plausible initial state.

    Pass 2 — Patch replacement: each masked patch position is replaced
              by the best-matching (min SSD) patch from source patches
              collected above the watermark. Only masked pixels within
              each patch are overwritten, so unmasked pixels are never
              touched.
    """
    h, w = mask.shape
    half = patch_size // 2
    result = img.copy().astype(np.float32)

    ys, xs = np.where(mask)
    if len(ys) == 0:
        return img

    y0, y1 = int(ys.min()), int(ys.max())
    x0, x1 = int(xs.min()), int(xs.max())

    # ── Pass 1: mirror initialisation ────────────────────────────────────────
    for dy in range(y1 - y0 + 1):
        y     = y0 + dy
        src_y = max(0, y0 - dy - 1)
        cols  = np.where(mask[y, x0:x1 + 1])[0] + x0
        result[y, cols] = img[src_y, cols]

    # ── Pass 2: patch-based replacement ──────────────────────────────────────
    src_flat, centers = _collect_source_patches(result, mask, y0, half, max_patches)

    if src_flat is None:
        # Not enough unmasked area above — mirror-only result is the best we can do
        return np.clip(result, 0, 255).astype(np.uint8)

    stride_fill = max(1, patch_size // 2)
    positions = [
        (ty, tx)
        for ty in range(y0, y1 + 1, stride_fill)
        for tx in range(x0, x1 + 1, stride_fill)
        if half <= ty < h - half and half <= tx < w - half and mask[ty, tx]
    ]

    total = len(positions)
    report_every = max(1, total // 20)

    for i, (ty, tx) in enumerate(positions):
        if verbose and i % report_every == 0:
            pct = int(100 * i / total)
            print(f"    {pct:3d}%\r", end="", flush=True)

        # SSD against all source patches — vectorised over N patches at once
        target = result[ty - half:ty + half + 1, tx - half:tx + half + 1].reshape(-1)
        diff   = src_flat - target
        best   = int(np.argmin((diff * diff).sum(axis=1)))
        bcy, bcx = centers[best]
        best_patch = result[bcy - half:bcy + half + 1, bcx - half:bcx + half + 1]

        # Write ONLY to masked pixels so unmasked edges are never touched
        pm = mask[ty - half:ty + half + 1, tx - half:tx + half + 1].astype(bool)
        pm3 = np.stack([pm, pm, pm], axis=2)
        region = result[ty - half:ty + half + 1, tx - half:tx + half + 1]
        np.copyto(region, best_patch, where=pm3)

    if verbose:
        print("    100%")

    return np.clip(result, 0, 255).astype(np.uint8)


# ── Per-file driver ───────────────────────────────────────────────────────────

def process_image(src: Path, dst: Path, args, verbose: bool = False) -> float:
    img  = load_image(str(src))
    h, w = img.shape[:2]
    mask, *_ = build_mask(h, w, args.height, args.width, args.pad)

    t0     = time.time()
    result = inpaint_exemplar(img, mask,
                              patch_size=args.patch,
                              max_patches=args.max_patches,
                              verbose=verbose)
    elapsed = time.time() - t0

    dst.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(result).save(str(dst))
    return elapsed


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Remove centre-bottom watermarks via patch-matching inpainting (Pillow+numpy).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single image
  python watermark_remover.py photo.jpg -o clean.jpg

  # Whole folder → <folder>/watermark_removed/
  python watermark_remover.py --dir "C:/Photos/Haldi"

  # Tune geometry if the strip isn't covered precisely
  python watermark_remover.py --dir "C:/Photos" --height 12 --width 35
""",
    )

    src_grp = parser.add_mutually_exclusive_group(required=True)
    src_grp.add_argument("input",  nargs="?", help="Single input image path")
    src_grp.add_argument("--dir",  metavar="FOLDER",
                         help="Process all images in FOLDER, save to FOLDER/watermark_removed/")

    parser.add_argument("-o", "--output",
                        help="Output path for single-image mode")
    parser.add_argument("--height", type=float, default=DEFAULT_HEIGHT_PCT,
                        help=f"Watermark height as %% of image height (default: {DEFAULT_HEIGHT_PCT})")
    parser.add_argument("--width",  type=float, default=DEFAULT_WIDTH_PCT,
                        help=f"Watermark width as %% of image width, centred (default: {DEFAULT_WIDTH_PCT})")
    parser.add_argument("--pad",    type=float, default=DEFAULT_PAD_PCT,
                        help="Bottom padding as %% of image height (default: 0 = flush to bottom)")
    parser.add_argument("--patch",  type=int,   default=9,
                        help="Patch size in pixels (default: 9 — larger = smoother, slower)")
    parser.add_argument("--max-patches", type=int, default=3000,
                        help="Source patch pool size (default: 3000)")

    args = parser.parse_args()

    if args.dir:
        folder = Path(args.dir)
        if not folder.is_dir():
            parser.error(f"Not a directory: {args.dir}")
        images = sorted(p for p in folder.iterdir() if p.suffix.lower() in IMAGE_EXTS)
        if not images:
            print("No images found.")
            return
        out_dir = folder / "watermark_removed"
        print(f"Processing {len(images)} image(s)  →  {out_dir}")
        for i, src in enumerate(images, 1):
            print(f"  [{i}/{len(images)}] {src.name}")
            elapsed = process_image(src, out_dir / src.name, args, verbose=True)
            print(f"    done in {elapsed:.1f}s")
        print("All done.")

    else:
        src = Path(args.input)
        if not src.is_file():
            parser.error(f"File not found: {args.input}")
        dst = Path(args.output) if args.output else \
              src.parent / f"{src.stem}_no_watermark{src.suffix}"
        print(f"Processing: {src.name}")
        elapsed = process_image(src, dst, args, verbose=True)
        print(f"Saved: {dst}  ({elapsed:.1f}s)")


if __name__ == "__main__":
    main()
