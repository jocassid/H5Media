
from django_init import django_init
django_init()

if True:
    from random import choice

    from django.contrib.auth.models import User

    from h5media.actions.podcast_actions import download_rss, load_episodes


def main():
    rss_file_urls = (
        # 'https://talkpython.fm/subscribe/rss',
        # 'https://feeds.megaphone.fm/revisionisthistory',
        # 'http://feeds.feedburner.com/HolosuiteMedia',
        # 'https://feeds.twit.tv/podcasts/sn.xml',

        'https://thehistoryofengland.co.uk/feed',
    )

    rss_file_url = choice(rss_file_urls)

    with open('history_of_england.rss', 'rb') as in_file:
        rss_bytes = in_file.read()

    load_episodes(
        rss_file_url,
        rss_bytes,
        # download_rss(rss_file_url),
        User.objects.get(username='john'),
    )


if __name__ == '__main__':
    main()
