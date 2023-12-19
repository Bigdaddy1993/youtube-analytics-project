import os
from src.channel import Channel
from dotenv import load_dotenv
from googleapiclient.discovery import build
import datetime
import isodate
from src.video import Video

load_dotenv()


class PlayList:
    api_key = os.getenv("YT_API")
    youtube = build("youtube", "v3", developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = self.get_title_playlist()
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"

    def get_title_playlist(self):
        """Возвращает title плэйлиста для инициализации"""
        pl_info = (
            self.youtube
            .playlists()
            .list(id=self.playlist_id, part="snippet")
            .execute()
        )
        return pl_info["items"][0]["snippet"]["title"]

    def get_video_id(self):
        """
        Вовращает список видео по id из плейлиста
        """
        playlist_videos = (
            self.youtube
            .playlistItems()
            .list(playlistId=self.playlist_id, part="contentDetails")
            .execute()
        )
        return [video["contentDetails"]["videoId"] for video in playlist_videos["items"]]

    @property
    def total_duration(self):
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(self.get_video_id())
                                                    ).execute()
        total_duration_list = []
        for video in video_response["items"]:
            duration = video["contentDetails"]["duration"]
            all_duration = isodate.parse_duration(duration)
            total_duration_list.append(all_duration)
        td = datetime.timedelta(
            seconds=sum(td.total_seconds() for td in total_duration_list))
        return td

    def show_best_video(self):
        video_ids = self.get_video_id()
        list_with_video_info = []
        for video_id in video_ids:
            video_info_dict = {}
            video_obj = Video(video_id)  # инициализация через класс Video
            video_info_dict["likes"] = video_obj.like_count
            video_info_dict["url"] = video_obj.video_url
            list_with_video_info.append(video_info_dict)
        sorted_list = sorted(
            list_with_video_info, key=lambda x: x["likes"], reverse=True
        )
        return sorted_list[0]["url"]
