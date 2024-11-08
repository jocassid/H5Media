
from django.contrib.admin import ModelAdmin, register

from h5media.models import (
    Podcast,
    PodcastEpisode,
    Profile,
)


@register(Profile)
class Profile(ModelAdmin):
    list_display = (
        'pk',
        'user',
    )


@register(Podcast)
class PodcastAdmin(ModelAdmin):
    list_display = (
        'pk',
        'title',
        'website',
        'rss',
    )


@register(PodcastEpisode)
class PodcastEpisodeAdmin(ModelAdmin):
    list_display = (
        'pk',
        'podcast',
        'title',
        'pub_date',
        'url',
    )
