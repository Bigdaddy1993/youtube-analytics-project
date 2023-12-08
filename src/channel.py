import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()


class Channel:
    """Класс для ютуб-канала"""

    channel_id = os.getenv("YT_API")
    youtube = build("youtube", "v3", developerKey=channel_id)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = (
            self.youtube.channels()
            .list(id=self.channel_id, part="snippet,statistics")
            .execute()
        )

        self.title = self.channel["items"][0]["snippet"]["title"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.id = self.channel["items"][0]["id"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.subscriberCount = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.viewCount = self.channel["items"][0]["statistics"]["viewCount"]

    def __str__(self):
        return f"{self.title}({self.url})"

    def __add__(self, other):
        """

        :param other:
        :return: возвращает количество подписчиков двух каналов
        """
        return int(self.subscriberCount) + int(other.subscriberCount)

    def __sub__(self, other):
        """

        :param other:
        :return: возвращает разницу в кол-ве подписчиков двух каналов
        """
        return int(self.subscriberCount) - int(other.subscriberCount)

    def __gt__(self, other):
        """

        :param other:
        :return:  Возвращает False, если количество подписчиков
                    текущего канала больше, чем у другого
        """
        return self.subscriberCount > other.subscriberCount

    def __le__(self, other):
        """

        :param other:
        :return:  Возвращает True, если количество подписчиков
        текущего канала меньше или равно, чем у другого
        """
        return self.subscriberCount <= other.subscriberCount

    def __eq__(self, other):
        """

        :param other:
        :return: Возвращает True, если количество подписчиков
        у двух каналов одинаково
        """
        return self.subscriberCount == other.subscriberCount

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API')
        cls.youtube = build('youtube', 'v3', developerKey=api_key)
        return cls.youtube

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(self.channel)

    def to_json(self, filename):
        channel_info = {"title": self.title,
                        "channel_id": self.__channel_id,
                        "description": self.description,
                        "url": self.url,
                        "count_subscriberCount": self.subscriberCount,
                        "video_count": self.video_count,
                        "count_views": self.viewCount}
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(channel_info, file, indent=4, ensure_ascii=False)
