# SpotiLoader
A simple Python programm for Linux to fetch track information from spotify to download them from YouTube

All downloaded files will be tagged and saved to a seperate folder called Music.

Dependencies:

    A Linux machine
    python 2.7
    pafy
    BeautifulSoup
    urllib2
    os
    sys
    eyed3
    requests
    shutil
    subprocess
    spotipy
    getopt

Usage:

    SpotiLoader.py -l, --list inputfile          Downloads tracks by Spotify Track IDs from an inputfile
    SpotiLoader.py -t, --track spotifyTrackID    Downloads an track
    SpotiLoader.py -a, --album spotifyAlbumID    Downloads an album
    SpotiLoader.py -i, --interactive             Starts in interactiveMode
    SpotiLoader.py -h, --help                    Print this help

How to get the Spotify ID:

  Tracks:
    
