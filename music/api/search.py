#!/usr/bin/python

# Execute a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from music.api import apikey
import music
import heapq

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
MAX_RESULTS = 10

def get_next_song():
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=apikey.DEVELOPER_KEY)
                    
    next_song_title = heapq.heappop(music.SONG_QUEUE)
    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=next_song_title,
        part='id,snippet',
        maxResults=MAX_RESULTS
    ).execute()

    videos = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append(search_result['id']['videoId'])
                
    return "https://www.youtube.com/watch?v=" + videos[0]
