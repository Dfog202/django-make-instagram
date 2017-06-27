import requests
from oauth2client.tools import argparser

DEVELOPER_KEY = 'REPLACE_ME'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def search_original(q):
    url_api_search = 'https://www.googleapis.com/youtube/v3/search'
    search_params = {
        'part': 'snippet',
        'key': 'AIzaSyCfNVvone9F96-ExRmi9zR05lQKvt8Tals',
        'maxResults': '10',
        'type': 'video',
        'q': q,
    }
    response = requests.get(url_api_search, params=search_params)
    data = response.json()
    return data

def search(q):
    # google api client를 사용
    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY,
    )

    search_response = youtube.search().list(
        q=q.q,
        part='id.snippet',
        maxResults='q.max_results'
    ).execute()