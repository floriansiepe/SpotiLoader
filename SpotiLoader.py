import getopt
import os
import sys

import spotipy

from M3UWriter import M3UWriter
from MetaTag import MetaTag
from YTDownloader import YTDownloader


class SpotiLoader:
    def __init__(self, list=None, track=None, album=None, interactive=False):
        os.chdir(sys.path[0])
        if not os.path.exists("Music"):
            os.makedirs("Music")
        self.playlistWriter = M3UWriter()
        if list != None:
            self.startList(list)
        elif track != None:
            self.startTrack(track)
        elif album != None:
            self.startAlbum(album)
        elif interactive:
            self.startInteractive()

    def startTrack(self, pTrack):
        try:
            spotipy.Spotify().track(pTrack)
        except spotipy.client.SpotifyException:
            print ('Unknow track ID. Exiting')
            sys.exit()
        metatag = MetaTag(pTrack, byID=True)
        if os.path.isfile("Music/" + metatag.getArtist().getArtistName() + ' - ' + metatag.getAlbum().getAlbumName() + ' - ' + metatag.getTrack().getTrackName() +".mp3"):
            print ("Found: " + metatag.getArtist().getArtistName() + ' - ' + metatag.getAlbum().getAlbumName() + ' - ' + metatag.getTrack().getTrackName() + "\n Skiping")
        else:
            downloader = YTDownloader(metatag)
            path = downloader.download()
            self.playlistWriter.addItem(path)

    def startAlbum(self, pAlbum):
        try:
            re = spotipy.Spotify().album(pAlbum)['tracks']['items']
        except spotipy.client.SpotifyException:
            print ('Unknow album ID. Exiting')
            sys.exit()
        print ("")
        print ('Downloading: ' + spotipy.Spotify().album(pAlbum)['name'])
        for i in range(len(re)):
            print ("")
            print (str(i + 1) + " of " + str(len(re)))
            self.startTrack(re[i]['uri'])
        self.playlistWriter.writeM3U()

    def startInteractive(self):
        print ('Enter exit to quit the program.')
        while True:
            a = raw_input('Enter a search term: ')
            if a == 'exit':
                break
            downloader = YTDownloader(MetaTag(a, byID=False))
            path = downloader.download()
            self.playlistWriter.addItem(path)
        self.playlistWriter.writeM3U()

    def startList(self, pList):
        data = self.getDownloadList(pList)
        print("Loaded " + str(len(data)) + " items from list")
        for i in range(len(data)):
            print ("")
            print (str(i + 1) + " of " + str(len(data)))
            self.startTrack(data[i])
        self.playlistWriter.writeM3U()

    def getDownloadList(self, pList):
        try:
            with open(pList, 'r') as fin:
                data = fin.read().splitlines(True)
        except IOError:
            print ("Can't open " + pList + ". Exiting.")
            sys.exit()
        for i in range(len(data)):
            data[i] = data[i].strip()
        return data


def printhelp():
    print ("Usage:")
    print("%s -l, --list inputfile          Downloads tracks by Spotify Track IDs from an inputfile" % sys.argv[0])
    print("%s -t, --track spotifyTrackID    Downloads an track" % sys.argv[0])
    print("%s -a, --album spotifyAlbumID    Downloads an album" % sys.argv[0])
    print("%s -i, --interactive             Starts in interactiveMode" % sys.argv[0])
    print("%s -h, --help                    Print this help" % sys.argv[0])
    print ("")
    print ("")


if __name__ == "__main__":
    print ("")
    print ("Author: Florian Siepe")
    print ("")
    print ("Disclaimer: \n"
           "I'm not responsible for thermonuclear war or the cancellation\n"
           " of your internetprovider because you downloaded something from YouTube.\n"
           " All you do with this programm is your responsibility! \n"
           "\n"
           "But neverless: Happy loading :)")
    print ("")
    try:
        myopts, args = getopt.getopt(sys.argv[1:], 'l:t:a:i', ['list=', 'track=', 'album=', 'interactive'])
    except getopt.GetoptError as e:
        print (str(e))
        printhelp()
        sys.exit()

    for o, a in myopts:
        if o in ('-l', '--list'):
            sp = SpotiLoader(list=a)
        elif o in ('-t', '--track'):
            sp = SpotiLoader(track=a)
        elif o in ('-a', '--album'):
            sp = SpotiLoader(album=a)
        elif o in ('-i', '--interactive'):
            sp = SpotiLoader(interactive=True)
        elif o in ('-h', '--help'):
            printhelp()
        else:
            printhelp()
    print ("")
    print ("All done.")
