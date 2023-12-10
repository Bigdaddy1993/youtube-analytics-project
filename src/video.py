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
        self.id_video = id_video
        self.video_response = (
            self.youtube.videos()
            .list(part="snippet,statistics,contentDetails,topicDetails", id=self.id_video)
            .execute()
        )
        self.title = self.video_response["items"][0]["snippet"]["title"]
        self.video_url = f"https://www.youtube.com/channel/{self.id_video}"
        self.video_view = self.video_response["items"][0]["statistics"]["viewCount"]
        self.video_likes = self.video_response["items"][0]["statistics"]["likeCount"]

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
