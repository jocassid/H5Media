
from django.contrib.auth.models import User
from django.db.models import (
    Model,
    CASCADE,
    CharField,
    ForeignKey,
)


class MediaFile(Model):
    """Audio or visual file"""
    title = CharField(max_length=250)
    file_path = CharField(max_length=250)
    owner = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='media_files',
    )


class PlayList(Model):
    owner = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='playlists',
    )
    name = CharField(max_length=200)


class Podcast(Model):
    name = CharField(max_length=200)












