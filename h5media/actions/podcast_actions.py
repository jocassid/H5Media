
from collections import Counter
from datetime import datetime
from enum import Enum
from re import compile as re_compile, IGNORECASE
from typing import List, Optional
from xml.sax import parseString
from xml.sax.handler import ContentHandler

from requests import codes, get
from requests.exceptions import Timeout

from django.conf import settings
from django.contrib.auth.models import User


from h5media.actions.actions import Action
from h5media.models import Podcast, PodcastEpisode


class DownloadException(RuntimeError):
    pass


def download_rss(rss_url) -> bytes:
    timeout_seconds = 30
    try:
        response = get(rss_url, timeout=timeout_seconds)
    except Timeout:
        raise DownloadException(
            f"Download of {rss_url} timed out after {timeout_seconds} seconds"
        )
    else:
        if not response.status_code == codes.ok:
            raise DownloadException(f"{rss_url} returned status {response.status_code}")
        return response.content


class RssHandler(ContentHandler):

    # These are elements which don't require a special startElement/endElement
    # handler
    regular_elements = {
        'rss',
        'title',
        'link',
        'description',
        'pubDate',
        'lastBuildDate',
    }

    special_start_elements = {

    }

    special_end_elements = {

    }

    special_elements = {
        'channel',
        'item',
        'enclosure',
    }

    elements_of_interest = regular_elements | special_elements

    DATE_FORMATS = [
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
    ]

    def __init__(self, rss_file_url: str, user: User):
        super().__init__()

        self.rss_file_url = rss_file_url
        self.user = user

        self.path_stack = []
        self.errors: List[str] = []

        self.podcast: Optional[Podcast] = None
        self.episode: Optional[PodcastEpisode] = None
        self.podcast_episodes: List[PodcastEpisode] = []

        # self.date_regex = re_compile(
        #     r"([a-z]{3}), (\d{2}) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{4})",
        #     IGNORECASE,
        # )

    def startElement(self, name, attrs):
        if len(self.path_stack) == 0 and name != 'rss':
            raise ValueError("Not an rss document")

        self.path_stack.append(name)
        if name not in self.elements_of_interest:
            return

        if name in self.regular_elements:
            return

        if name == 'channel':
            self.start_channel(attrs)
        elif name == 'item':
            self.start_item(attrs)
        elif name == 'enclosure':
            self.start_enclosure(attrs)
        else:
            self.errors.append(f"Unsupported start tag {name}")
        return

    def endElement(self, name):
        self.path_stack.pop()

        if name not in self.elements_of_interest:
            return
        if name in self.regular_elements:
            return

        if name == 'channel':
            self.end_channel()
        elif name == 'item':
            self.end_item()
        else:
            self.errors.append(f"Unsupported end tag {name}")

    def characters(self, content):

        if len(self.path_stack) < 2:
            return

        second_to_last_tag, last_tag = self.path_stack[-2:]
        if second_to_last_tag == 'channel':
            if last_tag == 'title':
                self.podcast.title = content
                return
            if last_tag == 'link':
                self.podcast.website = content
                return
            if last_tag == 'description':
                self.podcast.description = content
                return
            return

        if second_to_last_tag == 'item':
            if last_tag == 'title':
                self.episode.title = content
                return
            if last_tag == 'pubDate':
                for date_format in self.DATE_FORMATS:
                    try:
                        pub_date = datetime.strptime(content, date_format)
                    except ValueError:
                        pass
                    else:
                        self.episode.pub_date = pub_date
                return

    def start_channel(self, attrs) -> None:
        podcast = Podcast(rss=self.rss_file_url)
        podcast = podcast.fetch() or podcast
        self.podcast = podcast

    def end_channel(self) -> None:
        self.podcast.save()

    def start_item(self, attrs) -> None:
        if not self.podcast:
            self.errors.append("self.podcast not set")
            return

        if not self.podcast.pk:
            self.podcast.save()

        episode = PodcastEpisode(
            owner=self.user,
            podcast=self.podcast,
        )
        episode = episode.fetch() or episode
        self.episode = episode

    def end_item(self) -> None:
        db_episode: Optional[PodcastEpisode] = self.episode.fetch()
        if db_episode:
            db_episode.update(self.episode)
            return
        self.episode.save()
        self.episode = None

    def start_enclosure(self, attrs):
        self.episode.url = attrs.get('url')


class LoadEpisodesAction(Action):

    def __init__(self, rss_file_url: str, user: User):
        pass


def load_episodes(rss_file_url: str, content: bytes, user: User) -> None:

    content_mb = len(content) / 2**20
    if content_mb > settings.MAX_RSS_MB:
        raise DownloadException(
            f"rss file is {content_mb:.2f}MB max is {settings.MAX_RSS_MB}MB"
        )

    handler = RssHandler(rss_file_url, user)
    parseString(content, handler)
    for value in Counter(handler.errors).most_common():
        print(value)









