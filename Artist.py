import spotipy


class Artist:
    def __init__(self, pSpotifyUri):
        self.sp = spotipy.Spotify()
        self.uri = pSpotifyUri

    def getUri(self):
        return self.uri

    def getArtistName(self):
        return self.sp.artist(self.uri)['name'].replace("/", "")

    def getType(self):
        return self.sp.artist(self.uri)['type']

    def getArtUrl(self):
        return self.sp.artist(self.uri)['images'][0]['url']

    def getGenre(self):
        return self.sp.artist(self.uri)['genres'][0]

    def getFollower(self):
        return self.sp.artist(self.uri)['followers']['total']
