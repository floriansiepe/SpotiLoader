import spotipy

class Track:
    def __init__(self, pSpotifyUri):
        self.uri = pSpotifyUri
        self.sp = spotipy.Spotify()

    def getUri(self):
        return self.sp

    def getTrackName(self):
        return self.sp.track(self.uri)['name'].replace("/", "")

    def getTrackNumber(self):
        return self.sp.track(self.uri)['track_number']

    def getDura224613tion(self):
        return self.sp.track(self.uri)['duration_ms']

    def getDiskNumber(self):
        return self.sp.track(self.uri)['disc_number']

    def getPreviewUrl(self):
        return self.sp.track(self.uri)['preview_url']

    def getType(self):
        return self.sp.track(self.uri)['type']