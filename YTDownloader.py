from bs4 import BeautifulSoup
import pafy
import urllib2
import os
import eyed3
import requests
import shutil
import subprocess
#import youtube_dl

class YTDownloader:
    def __init__(self, pMetatag):
        pUrl = self.getUrl(pMetatag)
        pPath = self.downloadTrackWithPafy(pUrl, pMetatag)
        self.convertSong(pPath, pMetatag)
        self.fixMetaTags(pPath, pMetatag)

    def getUrl(self, pMetaTag):
        print(pMetaTag.getArtist().getArtistName() + " - " + pMetaTag.getTrack().getTrackName() + ": Fetching YouTube URL")
        query = (pMetaTag.getArtist().getArtistName() + ' - ' + pMetaTag.getTrack().getTrackName()).replace(" ", "+").replace("&","%26")
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        download = []
        for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
            if vid['href'].find('channel') == -1 or vid['href'].find('googleads') == -1 or vid['href'].find('user') == -1:
                download.append('https://www.youtube.com' + vid['href'])
        return download[0]

#    def downloadTrackWithYoutubeDl(self, pUrl, pMetaTag):
#        print(pMetaTag.getArtist().getArtistName() + " - " + pMetaTag.getTrack().getTrackName() + ": Downloading from YouTube")
#        path = "Music/" + pMetaTag.getArtist().getArtistName() + ' - ' + pMetaTag.getAlbum().getAlbumName() + ' - ' + pMetaTag.getTrack().getTrackName() + ".mp3"
#        ydl_opts = {
#            'format': 'bestaudio/best', # choice of quality
#            'extractaudio' : True,      # only keep the audio
#            'audiofo>>> parser.add_argument('--sum', dest='accumulate', action='store_const',rmat' : "mp3",      # convert to mp3
#            'outtmpl': path,        # name the file the ID of the video
#            'noplaylist' : True,        # only download single song, not playlist
#        }
#        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#            cwd = os.getcwd()
#            os.chdir("Music")
#            ydl.download([pUrl])
#            os.chdir(cwd)
#        return path
#
    def fixMetaTags(self, path, pMetaTag):
        print(pMetaTag.getArtist().getArtistName() + " - " + pMetaTag.getTrack().getTrackName() + ": Fixing Metatags")
        audiofile = eyed3.load(path + '.mp3')
        audiofile.tag.artist = pMetaTag.getArtist().getArtistName()
        audiofile.tag.album = pMetaTag.getAlbum().getAlbumName()
        audiofile.tag.title = pMetaTag.getTrack().getTrackName()
        #audiofile.tag.genre = pMetaTag.getArtist().getGenre()
        audiofile.tag.track_num = pMetaTag.getTrack().getTrackNumber()
        albumart = (requests.get(pMetaTag.getAlbum().getAlbumArtUrl(), stream=True)).raw
        with open('last_albumart.jpg', 'wb') as out_file:
            shutil.copyfileobj(albumart, out_file)
        albumart = open("last_albumart.jpg", "rb").read()
        audiofile.tag.images.set(3, albumart, "image/jpeg")
        audiofile.tag.save(version=(2, 3, 0))
        os.remove("last_albumart.jpg")

    def convertSong(self, path, pMetaTag):
        print(pMetaTag.getArtist().getArtistName() + " - " + pMetaTag.getTrack().getTrackName() + ": Converting to mp3")
        subprocess.call(["ffmpeg", "-hide_banner", "-loglevel", "panic", "-i", path + '.m4a', "-acodec", "libmp3lame", "-ab", "256k", path + '.mp3'])
        os.remove(path + '.m4a')

    def downloadTrackWithPafy(self, pUrl, pMetaTag):
        print(pMetaTag.getArtist().getArtistName() + " - " + pMetaTag.getTrack().getTrackName() + ": Downloading from YouTube")
        path = pMetaTag.getArtist().getArtistName() + ' - ' + pMetaTag.getAlbum().getAlbumName() + ' - ' + pMetaTag.getTrack().getTrackName()
        video = pafy.new(pUrl)
        bestaudio = video.getbestaudio(preftype="m4a")
        bestaudio.download(filepath="Music/" + path + ".m4a")
        print ("")
        path = 'Music/' + path
        return (path)
