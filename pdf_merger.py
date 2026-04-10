#!/usr/bin/env python3
"""
PDF Merger GUI - Drag & drop PDFs, reorder them, then merge into one file.

Dependencies:
    pip install pypdf tkinterdnd2
"""

import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


def check_deps():
    missing = []
    try:
        import pypdf  # noqa: F401
    except ImportError:
        missing.append("pypdf")
    try:
        import tkinterdnd2  # noqa: F401
    except ImportError:
        missing.append("tkinterdnd2")
    if missing:
        print(
            f"Missing dependencies. Install with:\n  pip install {' '.join(missing)}")
        sys.exit(1)


check_deps()

from tkinterdnd2 import DND_FILES, TkinterDnD  # noqa: E402


# ── helpers ──────────────────────────────────────────────────────────────────

def parse_drop_data(data: str) -> list[Path]:
    """tkinterdnd2 returns a Tcl list; parse it into paths."""
    paths: list[Path] = []
    # Tcl lists use {} for items with spaces
    raw = data.strip()
    items: list[str] = []
    if raw.startswith("{"):
        i = 0
        while i < len(raw):
            if raw[i] == "{":
                end = raw.index("}", i)
                items.append(raw[i + 1: end])
                i = end + 2
            elif raw[i] == " ":
                i += 1
            else:
                end = raw.find(" ", i)
                if end == -1:
                    items.append(raw[i:])
                    break
                items.append(raw[i:end])
                i = end + 1
    else:
        items = raw.split()
    for item in items:
        p = Path(item)
        if p.suffix.lower() == ".pdf":
            paths.append(p)
    return paths


def merge_pdfs(files: list[Path], output: Path, progress_cb=None):
    from pypdf import PdfWriter

    writer = PdfWriter()
    for i, f in enumerate(files):
        writer.append(str(f))
        if progress_cb:
            progress_cb(i + 1, len(files))
    with open(output, "wb") as fh:
        writer.write(fh)
    return len(writer.pages)


# ── main window ──────────────────────────────────────────────────────────────

class PDFMergerApp(TkinterDnD.Tk):
    ACCENT = "#4A90D9"
    BG = "#1E1E2E"
    SURFACE = "#2A2A3E"
    SURFACE2 = "#313147"
    TEXT = "#CDD6F4"
    SUBTEXT = "#A6ADC8"
    RED = "#F38BA8"
    GREEN = "#A6E3A1"

    def __init__(self):
        super().__init__()
        self.title("PDF Merger")
        self.geometry("700x560")
        self.minsize(580, 480)
        self.configure(bg=self.BG)
        self._drag_index: int | None = None
        self._build_ui()

    # ── UI construction ──────────────────────────────────────────────────────

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # ── header
        hdr = tk.Frame(self, bg=self.BG, pady=12)
        hdr.grid(row=0, column=0, sticky="ew", padx=20)
        tk.Label(hdr, text="PDF Merger", font=("Segoe UI", 18, "bold"),
                 bg=self.BG, fg=self.TEXT).pack(side="left")
        tk.Label(hdr, text="drag, order, merge", font=("Segoe UI", 10),
                 bg=self.BG, fg=self.SUBTEXT).pack(side="left", padx=(10, 0), pady=(6, 0))

        # ── drop zone + list (left) and controls (right)
        body = tk.Frame(self, bg=self.BG)
        body.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 8))
        body.columnconfigure(0, weight=1)
        body.rowconfigure(0, weight=1)

        # drop zone (doubles as the file list)
        list_frame = tk.Frame(body, bg=self.SURFACE, bd=0, relief="flat")
        list_frame.grid(row=0, column=0, sticky="nsew")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)

        self.drop_label = tk.Label(
            list_frame,
            text="Drop PDF files here\nor click  +  to browse",
            font=("Segoe UI", 12), bg=self.SURFACE, fg=self.SUBTEXT,
            pady=30, cursor="hand2",
        )
        self.drop_label.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self.drop_label.bind("<Button-1>", lambda _: self._browse_files())

        # listbox with scrollbar
        lb_wrap = tk.Frame(list_frame, bg=self.SURFACE)
        lb_wrap.grid(row=1, column=0, sticky="nsew", padx=2, pady=(0, 2))
        lb_wrap.columnconfigure(0, weight=1)
        lb_wrap.rowconfigure(0, weight=1)

        self.listbox = tk.Listbox(
            lb_wrap,
            bg=self.SURFACE2, fg=self.TEXT,
            selectbackground=self.ACCENT, selectforeground="#FFFFFF",
            font=("Segoe UI", 10), bd=0, highlightthickness=0,
            activestyle="none", selectmode="extended",
        )
        self.listbox.grid(row=0, column=0, sticky="nsew")

        sb = tk.Scrollbar(lb_wrap, orient="vertical",
                          command=self.listbox.yview)
        sb.grid(row=0, column=1, sticky="ns")
        self.listbox.configure(yscrollcommand=sb.set)

        # drag-to-reorder within list
        self.listbox.bind("<ButtonPress-1>",   self._lb_drag_start)
        self.listbox.bind("<B1-Motion>",       self._lb_drag_motion)
        self.listbox.bind("<ButtonRelease-1>", self._lb_drag_end)

        # file-drop from OS
        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self._on_drop)
        list_frame.drop_target_register(DND_FILES)
        list_frame.dnd_bind("<<Drop>>", self._on_drop)
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind("<<Drop>>", self._on_drop)

        # ── right-side button column
        btn_col = tk.Frame(body, bg=self.BG, padx=8)
        btn_col.grid(row=0, column=1, sticky="ns")

        def icon_btn(parent, text, cmd, fg=None, width=8):
            return tk.Button(
                parent, text=text, command=cmd,
                bg=self.SURFACE2, fg=fg or self.TEXT,
                activebackground=self.ACCENT, activeforeground="#fff",
                font=("Segoe UI", 10), bd=0, padx=6, pady=6,
                relief="flat", cursor="hand2", width=width,
            )

        icon_btn(btn_col, "+ Add",
                 self._browse_files).pack(pady=(0, 4), fill="x")
        icon_btn(btn_col, "✕ Remove", self._remove_selected,
                 fg=self.RED).pack(pady=4, fill="x")
        tk.Frame(btn_col, bg=self.SURFACE2, height=1).pack(fill="x", pady=8)
        icon_btn(btn_col, "▲ Up",     self._move_up).pack(pady=4, fill="x")
        icon_btn(btn_col, "▼ Down",   self._move_down).pack(pady=4, fill="x")
        tk.Frame(btn_col, bg=self.SURFACE2, height=1).pack(fill="x", pady=8)
        icon_btn(btn_col, "⬆ Top",    self._move_top).pack(pady=4, fill="x")
        icon_btn(btn_col, "⬇ Bottom", self._move_bottom).pack(pady=4, fill="x")
        tk.Frame(btn_col, bg=self.SURFACE2, height=1).pack(fill="x", pady=8)
        icon_btn(btn_col, "🗑 Clear",  self._clear_all,
                 fg=self.RED).pack(pady=4, fill="x")

        # ── output row
        out_frame = tk.Frame(self, bg=self.BG)
        out_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(4, 4))
        out_frame.columnconfigure(1, weight=1)

        tk.Label(out_frame, text="Output:", font=("Segoe UI", 10),
                 bg=self.BG, fg=self.SUBTEXT, width=7, anchor="w").grid(row=0, column=0)

        self.out_var = tk.StringVar(value="merged.pdf")
        out_entry = tk.Entry(out_frame, textvariable=self.out_var,
                             bg=self.SURFACE2, fg=self.TEXT, insertbackground=self.TEXT,
                             font=("Segoe UI", 10), bd=0, relief="flat")
        out_entry.grid(row=0, column=1, sticky="ew", ipady=5, padx=(4, 4))

        tk.Button(out_frame, text="Browse", command=self._choose_output,
                  bg=self.SURFACE2, fg=self.TEXT,
                  activebackground=self.ACCENT, activeforeground="#fff",
                  font=("Segoe UI", 10), bd=0, padx=8, pady=4, relief="flat",
                  cursor="hand2").grid(row=0, column=2)

        # ── progress bar
        self.progress = ttk.Progressbar(self, mode="determinate", length=200)
        self.progress.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 4))
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TProgressbar", troughcolor=self.SURFACE2,
                        background=self.ACCENT, borderwidth=0, thickness=6)

        # ── status label
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(self, textvariable=self.status_var, font=("Segoe UI", 9),
                 bg=self.BG, fg=self.SUBTEXT).grid(row=4, column=0, sticky="w", padx=22)

        # ── merge button
        self.merge_btn = tk.Button(
            self, text="Merge PDFs", command=self._start_merge,
            bg=self.ACCENT, fg="#FFFFFF",
            activebackground="#357ABD", activeforeground="#fff",
            font=("Segoe UI", 12, "bold"), bd=0, pady=10,
            relief="flat", cursor="hand2",
        )
        self.merge_btn.grid(row=5, column=0, sticky="ew",
                            padx=20, pady=(4, 16))

        self._refresh_drop_label()

    # ── file management ───────────────────────────────────────────────────────

    def _files(self) -> list[str]:
        return list(self.listbox.get(0, "end"))

    def _add_files(self, paths: list[Path]):
        existing = set(self._files())
        added = 0
        for p in paths:
            s = str(p)
            if s not in existing:
                self.listbox.insert("end", s)
                existing.add(s)
                added += 1
        if added:
            self._refresh_drop_label()
            self.status_var.set(f"{self.listbox.size()} file(s) loaded")

    def _browse_files(self):
        paths = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )
        self._add_files([Path(p) for p in paths])

    def _choose_output(self):
        path = filedialog.asksaveasfilename(
            title="Save merged PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=self.out_var.get(),
        )
        if path:
            self.out_var.set(path)

    def _on_drop(self, event):
        self._add_files(parse_drop_data(event.data))

    def _remove_selected(self):
        for idx in reversed(self.listbox.curselection()):
            self.listbox.delete(idx)
        self._refresh_drop_label()
        self.status_var.set(f"{self.listbox.size()} file(s) loaded")

    def _clear_all(self):
        self.listbox.delete(0, "end")
        self._refresh_drop_label()
        self.status_var.set("Ready")

    def _refresh_drop_label(self):
        if self.listbox.size() == 0:
            self.drop_label.grid()
        else:
            self.drop_label.grid_remove()

    # ── reordering ────────────────────────────────────────────────────────────

    def _swap(self, i: int, j: int):
        items = self._files()
        items[i], items[j] = items[j], items[i]
        self.listbox.delete(0, "end")
        for item in items:
            self.listbox.insert("end", item)

    def _move_selection(self, delta: int):
        sel = list(self.listbox.curselection())
        if not sel:
            return
        if delta < 0 and sel[0] == 0:
            return
        if delta > 0 and sel[-1] == self.listbox.size() - 1:
            return
        for idx in (sel if delta > 0 else reversed(sel)):
            self._swap(idx, idx + delta)
        new_sel = [i + delta for i in sel]
        self.listbox.selection_clear(0, "end")
        for i in new_sel:
            self.listbox.selection_set(i)
        self.listbox.see(new_sel[0])

    def _move_up(self):     self._move_selection(-1)
    def _move_down(self):   self._move_selection(1)

    def _move_top(self):
        sel = list(self.listbox.curselection())
        if not sel or sel[0] == 0:
            return
        items = self._files()
        moved = [items[i] for i in sel]
        rest = [items[i] for i in range(len(items)) if i not in set(sel)]
        new_items = moved + rest
        self.listbox.delete(0, "end")
        for item in new_items:
            self.listbox.insert("end", item)
        self.listbox.selection_clear(0, "end")
        for i in range(len(moved)):
            self.listbox.selection_set(i)

    def _move_bottom(self):
        sel = list(self.listbox.curselection())
        if not sel or sel[-1] == self.listbox.size() - 1:
            return
        items = self._files()
        moved = [items[i] for i in sel]
        rest = [items[i] for i in range(len(items)) if i not in set(sel)]
        new_items = rest + moved
        self.listbox.delete(0, "end")
        for item in new_items:
            self.listbox.insert("end", item)
        self.listbox.selection_clear(0, "end")
        start = len(rest)
        for i in range(start, start + len(moved)):
            self.listbox.selection_set(i)

    # ── drag-to-reorder within listbox ────────────────────────────────────────

    def _lb_drag_start(self, event):
        self._drag_index = self.listbox.nearest(event.y)

    def _lb_drag_motion(self, event):
        if self._drag_index is None:
            return
        target = self.listbox.nearest(event.y)
        if target != self._drag_index:
            self._swap(self._drag_index, target)
            self.listbox.selection_clear(0, "end")
            self.listbox.selection_set(target)
            self._drag_index = target

    def _lb_drag_end(self, _event):
        self._drag_index = None

    # ── merge ─────────────────────────────────────────────────────────────────

    def _start_merge(self):
        files = [Path(f) for f in self._files()]
        if not files:
            messagebox.showwarning(
                "No files", "Add at least one PDF before merging.")
            return
        output = Path(self.out_var.get().strip() or "merged.pdf")
        if not output.suffix:
            output = output.with_suffix(".pdf")

        self.merge_btn.configure(state="disabled", text="Merging…")
        self.progress["value"] = 0
        self.progress["maximum"] = len(files)
        self.status_var.set("Merging…")

        def run():
            try:
                def on_progress(done, total):
                    self.progress["value"] = done
                    self.status_var.set(f"Adding file {done}/{total}…")

                pages = merge_pdfs(files, output, progress_cb=on_progress)
                self.after(0, self._merge_done, output, pages)
            except Exception as exc:
                self.after(0, self._merge_error, str(exc))

        threading.Thread(target=run, daemon=True).start()

    def _merge_done(self, output: Path, pages: int):
        self.merge_btn.configure(state="normal", text="Merge PDFs")
        self.progress["value"] = self.progress["maximum"]
        self.status_var.set(f"Done — {pages} pages saved to '{output.name}'")
        messagebox.showinfo(
            "Done", f"Merged {pages} pages.\n\nSaved to:\n{output}")

    def _merge_error(self, msg: str):
        self.merge_btn.configure(state="normal", text="Merge PDFs")
        self.status_var.set("Error — see dialog")
        messagebox.showerror("Merge failed", msg)


if __name__ == "__main__":
    app = PDFMergerApp()
    app.mainloop()
