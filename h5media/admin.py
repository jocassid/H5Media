
from django.contrib.admin import ModelAdmin, register

from h5media.models import (
    Podcast,
    PodcastEpisode,
)


@register(Podcast)
class PodcastAdmin(ModelAdmin):
    list_display = (
        'title',
        'website',
        'rss',
    )


@register(PodcastEpisode)
class PodcastEpisodeAdmin(ModelAdmin):
    list_display = (
        'title',
        'podcast',
        'url',
    )
