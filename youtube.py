from pytube import YouTube
from pytube import Playlist
import os

p = Playlist(
    'https://www.youtube.com/playlist?list=PL9gnSGHSqcnr_DxHsP7AW9ftq0AtAyYqJ')


def download(link, playlist_count):
    try:
        youtubeObject = YouTube(link)
        resolution = youtubeObject.streams.get_highest_resolution()
        print("Downloading: " + youtubeObject.title)
        filepath = 'C:/Users/Vishnu/Desktop/Videos/'
        resolution.download(filepath)

        # filename = resolution.default_filename
        # updated_filename = str(playlist_count)+"_"+filename
        # os.rename(os.path.join(filepath, filename),
        #           os.path.join(filepath, updated_filename))

    except:
        print("Error")

    print("Download complete!")


download("https://www.youtube.com/watch?v=BSVKUk58K6U&list=PL9gnSGHSqcnr_DxHsP7AW9ftq0AtAyYqJ&index=37", 37)


# playlist_count = 37
# for url in p.video_urls[36:len(p.video_urls)]:
#     # print(url)
#     download(url, playlist_count)
#     playlist_count += 1
