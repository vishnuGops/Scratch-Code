import os
import yt_dlp


def download_audio():
    # 1. Get the download folder from the user
    output_folder = "C://Users//vishv//Desktop//Code//Scratch-Code//Output//Music".strip()

    if not output_folder:
        output_folder = os.getcwd()

    # Create the folder if it doesn't exist
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
            print(f"Created folder: {output_folder}")
        except OSError as e:
            print(f"Error creating folder: {e}")
            return

    # 2. Configuration for yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        # Record downloaded IDs to skip duplicates
        'download_archive': os.path.join(output_folder, 'archive.txt'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': True,
    }

    print(f"\nSaving to: {output_folder}")
    print("Paste YouTube links below (separated by spaces or commas).")
    print("Type 'q' or 'done' to finish.")
    print("-" * 50)

    # 3. Loop to accept links
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        while True:
            user_input = input("Links: ").strip()

            if user_input.lower() in ['q', 'quit', 'exit', 'done']:
                break

            if not user_input:
                continue

            # Split input by commas or spaces to create a list of URLs
            urls = user_input.replace(',', ' ').split()

            try:
                print(f"Processing {len(urls)} link(s)...")
                ydl.download(urls)  # yt-dlp accepts a list of URLs directly
                print("✅ Batch complete!\n")
            except Exception as e:
                print(f"❌ Error: {e}\n")

    print("\nAll tasks finished!")


if __name__ == "__main__":
    download_audio()
