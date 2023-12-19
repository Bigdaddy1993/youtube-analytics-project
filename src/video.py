import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()


class Video:
    """
    класс для видео
    """
    api_key = os.getenv("YT_API")
    youtube = build("youtube", "v3", developerKey=api_key)

    def __init__(self, id_video: str):
        try:
            self.id_video = id_video
            self.video_response = (
                self.youtube.videos()
                .list(part="snippet,statistics,contentDetails,topicDetails", id=self.id_video)
                .execute()
            )
            self.title = self.video_response["items"][0]["snippet"]["title"]
            self.video_url = f"https://youtu.be/{self.id_video}"
            self.video_view = self.video_response["items"][0]["statistics"]["viewCount"]
            self.like_count = self.video_response["items"][0]["statistics"]["likeCount"]
        except Exception:
            self.id_video = "Не существует такого id"
            self.video_response = None
            self.title = None
            self.video_url = None
            self.video_view = None
            self.like_count = None

    def __str__(self):
        """

        :return: название видео
        """
        return f"{self.title}"


class PLVideo(Video):
    """
    класс для плейлиста
    """

    def __init__(self, id_video: str, id_playlist: str):
        super().__init__(id_video)
        self.id_playlist = id_playlist
        self.playlist_videos = (
            self.youtube.playlistItems()
            .list(
                playlistId=self.id_playlist,
                part="contentDetails",
                maxResults=50,
            )
            .execute()
        )

    def __str__(self):
        """

        :return: название видео
        """
        return f"{self.title}"
