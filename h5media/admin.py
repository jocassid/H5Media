
from django.contrib.admin import ModelAdmin, register

from h5media.models import (
    Album,
    AlbumTrack,
    Audiobook,
    AudiobookChapter,
    MediaFile,
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
    search_fields = ('title',)


@register(AlbumTrack)
class AlbumTrackAdmin(ModelAdmin):
    list_display = (
        'pk',
        'album',
        'title',
        'disc',
        'track',
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


@register(MediaFile)
class MediaFileAdmin(ModelAdmin):
    list_display = (
        'pk',
        'title',
        'type',
    )


@register(PlayList)
class PlayListAdmin(ModelAdmin):
    list_display = (
        'pk',
        'title',
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
