import requests
import asyncio

from pytube import Playlist, YouTube
from youtubesearchpython import VideosSearch
import youtube_dl

import pyfiglet
from colorama import Fore, Back, Style


print(Fore.BLUE+pyfiglet.figlet_format("Playlist Downloader"))
print(Style.RESET_ALL)
print(Fore.BLUE+"-By Mr Papava \n\n\n")
print(Style.RESET_ALL)


def main(head):

    URL = input(Fore.CYAN + "input the url: ")
    print(Style.RESET_ALL)

    if "open.spotify" in URL:
        for name in asyncio.run(spotify_playlist(head, URL)):
            youtube_download(file_namer(name), youtube_search(name)['result'][0]['link'])
        input(Back.GREEN+Fore.BLACK+"Download Complete...")
        print(Style.RESET_ALL)

    elif "youtube" in URL:
        for link in youtube_playlist(URL):
            youtube_download(file_namer(file_namer2(link)), link)
        input(Back.GREEN+Fore.BLACK+"Download Complete...")
        print(Style.RESET_ALL)

    else:
        print(Back.RED+"enter the valid url")
        print(Style.RESET_ALL)


def file_namer(name):
    return {
        'outtmpl': 'downloaded/'+name+'.mp4',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }], }

def file_namer2(link):
    yt = YouTube(link)
    return yt.streams[0].title

async def spotify_playlist(headers, link):
    ID = link[34:link.index("?")]
    response = requests.get(
        f'https://api.spotify.com/v1/playlists/{ID}/tracks', headers=headers)
    return [x['track']['artists'][0]['name']+" "+x['track']["name"] for x in response.json()["items"]]


def youtube_search(name):
    videosSearch = VideosSearch(name, limit=0)

    return videosSearch.result()


def youtube_playlist(playlist_link):
    playlist = Playlist(playlist_link)
    return playlist.video_urls


def youtube_download(opts, link):

    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download([link])


if __name__ == "__main__":
    head = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer [SPOTIFY_API_KEY_HERE]',
    }
    main(head)
