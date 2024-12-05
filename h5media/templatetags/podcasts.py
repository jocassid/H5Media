
from urllib.parse import urlencode

from django import template

register = template.Library()


@register.simple_tag
def podcast_index_url(search: str) -> str:
    return "https://podcastindex.org/search?{}".format(
        urlencode({'q': search, 'type': 'all'})
    )
