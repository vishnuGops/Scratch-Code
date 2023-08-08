from pytube import YouTube


def download(link):
    try:
        youtubeObject = YouTube(link)
        resolution = youtubeObject.streams.get_highest_resolution()
        resolution.download()

    except:
        print("Error")

    print("Download complete!")


download("https://www.youtube.com/watch?v=6UQZ5oQg8XA")
