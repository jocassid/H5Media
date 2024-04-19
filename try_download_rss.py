
from django_init import django_init
django_init()

from random import choice

from h5media.actions.podcast_actions import download_rss, load_episodes


rss_file_urls = (
    'https://talkpython.fm/subscribe/rss',
    'https://feeds.megaphone.fm/revisionisthistory',
    'http://feeds.feedburner.com/HolosuiteMedia',
)

load_episodes(
    download_rss(
        choice(rss_file_urls)
    )
)

