import os

from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, id_video):
        self.id_video = id_video
        self.info_video()

    def __str__(self):
        return self.title

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def info_video(self):
        video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=self.id_video).execute()
        self.id = self.id_video
        self.title = video_response['items'][0]['snippet']['title']
        self.url = f"https://youtu.be/{self.id_video}"
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']


class PLVideo(Video):
    def __init__(self, id_video, id_playlist):
        super().__init__(id_video)
        self.id_playlist = id_playlist
