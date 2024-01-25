import datetime
import os

import isodate
from googleapiclient.discovery import build

from src.video import Video


class PlayList:
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, id_playlist):
        self.id_playlist = id_playlist
        self.get_info_playlist()

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def get_info_playlist(self):
        playlists = self.get_service().playlists().list(id=self.id_playlist,
                                                        part='contentDetails,snippet',
                                                        maxResults=50,).execute()
        self.title = playlists['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.id_playlist}'

        playlist_videos = self.get_service().playlistItems().list(playlistId=self.id_playlist,
                                                                  part='contentDetails',
                                                                  maxResults=50,).execute()

        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(self.video_ids)).execute()

        total_time = datetime.timedelta()

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_time += duration
        self.__total_duration = total_time

    @property
    def total_duration(self):
        return self.__total_duration

    def show_best_video(self):
        like_max = 0
        for video in self.video_ids:
            info_video = Video(video)
            if info_video.like_count > like_max:
                like_max = info_video.like_count
                best_video = info_video.url
        return best_video
