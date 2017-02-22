from spotipy import *

from Album import *
from Artist import *
from Track import *


class MetaTag:
    def __init__(self, pString, byID=False):
        self.artist = None
        self.album = None
        self.track = None
        self.sp = Spotify()
        if not byID:
            self.searchSpotify(pString)
        else:
            self.searchSpotifyById(pString)

    def searchSpotify(self, pString):
        results = self.sp.search(pString, limit=1)
        for i, t in enumerate(results['tracks']['items']):
            self.artist = Artist(t['artists'][0]['uri'])
            self.album = Album(t['album']['uri'])
            self.track = Track(t['uri'])

    def searchSpotifyById(self, pID):
        results = self.sp.track(pID)
        self.artist = Artist(results['artists'][0]['uri'])
        self.album = Album(results['album']['uri'])
        self.track = Track(results['uri'])

    def getArtist(self):
        return self.artist

    def getAlbum(self):
        return self.album

    def getTrack(self):
        return self.track
