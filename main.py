from dotenv import load_dotenv
from googleapiclient.discovery import build
import os
import json

load_dotenv()

API_KEY = os.getenv('API_KEY')
id_Chanel = os.getenv('id_Chanel')
youtube = build('youtube', 'v3', developerKey=API_KEY)
url = 'https://www.youtube.com/watch?v='


def get_data_playlists():
    request = youtube.playlists().list(part="snippet, id",
                                       channelId=id_Chanel,
                                       maxResults=50
                                       )
    response = request.execute()

    playlists_data = []
    for item in response['items']:
        playlist_id = item['id']
        playlist_title = item['snippet']['title']
        playlist_image = item['snippet']['thumbnails']['standard']['url']

        playlists_data.append({
            'playlist_id': playlist_id,
            'playlist_title': playlist_title,
            'playlist_image': playlist_image,
        })

    with open('playlists_data.json', 'w') as file:
        json.dump(playlists_data, file, indent=4, ensure_ascii=False)


def get_playlist_videos(playlist_id):
    request = youtube.playlistItems().list(part='contentDetails, snippet',
                                           playlistId=playlist_id)

    response = request.execute()
    playlist_videos = []
    for item in response['items']:
        video_title = item['snippet']['title']
        video_image = item['snippet']['thumbnails']['standard']['url']
        video_url = f"{url}{item['contentDetails']['videoId']}"
        video_description = item['snippet']['description'][0:100]
        playlist_videos.append({
            'video_title': video_title,
            'video_image': video_image,
            'video_url': video_url,
            'video_description': video_description,
        })

    with open('playlist_videos.json', 'w') as file:
        json.dump(playlist_videos, file, indent=4, ensure_ascii=False)
