
from django.conf import settings

from requests import codes, get
from requests.exceptions import Timeout



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


def load_episodes(content: bytes):

    content_mb = len(content) / 2**20
    if content_mb > settings.MAX_RSS_MB:
        raise DownloadException(f"rss file is {content_mb:.2f}MB max is {settings.MAX_RSS_MB}MB")
    # print(f"{content_mb = }")
    #
    # # print(response.content)
    # # print(type(response.content))
    pass








