
from django.contrib.admin import ModelAdmin, register

from h5media.models import (
    Album,
    AlbumTrack,
    Audiobook,
    AudiobookChapter,
    PlayList,
    Podcast,
    PodcastEpisode,
    Profile,
)


@register(Album)
class AlbumAdmin(ModelAdmin):
    list_display = (
        'pk',
        'title',
    )


@register(AlbumTrack)
class AlbumTrackAdmin(ModelAdmin):
    list_display = (
        'pk',
        'album',
        'title',
    )


@register(Audiobook)
class AudiobookAdmin(ModelAdmin):
    list_display = (
        'pk',
        'title',
    )


@register(AudiobookChapter)
class AudiobookChapterAdmin(ModelAdmin):
    list_display = (
        'pk',
        'audiobook',
        'chapter',
        'title',
    )


@register(PlayList)
class PlayListAdmin(ModelAdmin):
    list_display = (
        'pk',
        'owner',
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


@register(Profile)
class Profile(ModelAdmin):
    list_display = (
        'pk',
        'user',
    )
