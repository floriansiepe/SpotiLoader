import spotipy


class Album:
    def __init__(self, pSpotifyUri):
        self.sp = spotipy.Spotify()
        self.uri = pSpotifyUri

    def getUri(self):
        return self.uri

    def getAlbumName(self):
        return self.sp.album(self.uri)['name'].replace("/", "")

    def getLabel(self):
        return self.sp.album(self.uri)['label'].replace("/", "")

    def getReleaseDate(self):
        return self.sp.album(self.uri)['release_date']

    def getAlbumArtUrl(self):
        return self.sp.album(self.uri)['images'][0]['url']

    def getType(self):
        return self.sp.album(self.uri)['type']