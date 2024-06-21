import yt_dlp


def download_media(url, output_path, audio_only=False, playlist=False):
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'bestaudio/best' if audio_only else 'best',
        'noplaylist': not playlist,  # Download single video if False
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if audio_only else [],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
url = 'https://www.youtube.com/watch?v=zig6qByF9bg'
output_path = 'Output/MediaDownloader/%(title)s.%(ext)s'
download_media(url, output_path, audio_only=False, playlist=False)
