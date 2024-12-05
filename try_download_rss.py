
from django_init import django_init
django_init()

if True:
    from logging import getLogger
    from pathlib import Path
    from typing import Iterator, Tuple
    from urllib.parse import urlparse

    from django.contrib.auth.models import User

    from h5media.actions.podcast_actions import (
        DownloadException,
        download_rss,
        load_episodes,
    )


logger = getLogger('web')

# Local rss files to load
# rss_file_paths = (
#     ('https://thehistoryofengland.co.uk/feed', 'history_of_england.rss'),
# )

rss_file_urls = (
    'https://talkpython.fm/subscribe/rss',
    # 'https://feeds.megaphone.fm/revisionisthistory',  # rss down
    'http://feeds.feedburner.com/HolosuiteMedia',
    'https://feeds.twit.tv/podcasts/sn.xml',
    'https://thehistoryofengland.co.uk/feed',
)


def get_url_and_rss_bytes() -> Iterator[Tuple[str, bytes]]:
    for url in rss_file_urls:
        url_parts = urlparse(url)

        cached_rss_path = Path('./rss_cache') / f"{url_parts.hostname}.rss"
        if not cached_rss_path.exists():
            try:
                rss_bytes = download_rss(url)
            except DownloadException as error:
                logger.error(str(error))
                continue
            else:
                with open(cached_rss_path, 'wb') as out_file:
                    out_file.write(rss_bytes)

        if not cached_rss_path.exists():
            logger.error(f"cached file not present for {url}")
            continue

        with open(cached_rss_path, 'rb') as in_file:
            yield url, in_file.read()


def main():
    user: User = User.objects.get(username='john')

    for url, rss_bytes in get_url_and_rss_bytes():
        logger.info(f"Loading rss for {url}")
        load_episodes(url, rss_bytes, user)


if __name__ == '__main__':
    main()
