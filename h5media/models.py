
from collections.abc import Iterable
from typing import Optional, Tuple

from django.contrib.auth.models import User
from django.core.exceptions import (
    MultipleObjectsReturned,
    ObjectDoesNotExist,
)
from django.db.models import (
    Model,
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    IntegerField,
    JSONField,
    Manager,
    ManyToManyField,
    Max,
    OneToOneField,
    PositiveIntegerField,
    TextField,
    UniqueConstraint,
    URLField,
)
from django.db.transaction import atomic


def build_title_field() -> CharField:
    return CharField(
        max_length=250,
        null=False,
        blank=False,
        default='',
    )


class DatabaseError(RuntimeError):
    pass





class BaseModel(Model):

    update_fields = tuple()

    class Meta:
        abstract = True

    def fetch(self) -> Optional[Model]:
        """When this method is invoked on an unsaved instance of BaseModel,
        an attempt will be made to find a matching record in the database.
        If a matching record is found, the record is returned otherwise None
        is returned.  Subclasses will override this method to match on
        whatever fields are appropriate for that Model"""
        return None

    def update(
            self,
            instance: Model,
            copy_nulls: bool = False,
            defer_save: bool = False,
    ):
        for field in self.update_fields:
            rhs_value = getattr(instance, field)
            if rhs_value or copy_nulls:
                setattr(self, field, rhs_value)
        if defer_save:
            return
        self.save()


def profile_queue_default():
    return []


class Profile(BaseModel):
    user = OneToOneField(
        User,
        on_delete=CASCADE,
        related_name='profile',
    )

    queue = ManyToManyField('MediaFile', through='ProfileQueue')

    def __str__(self):
        return self.user.username


class MediaFile(BaseModel):
    """Audio or visual file"""

    title = build_title_field()

    file_path = CharField(
        max_length=250,
        null=False,
        blank=True,
    )

    TYPE_PODCAST_EPISODE = 'e'
    TYPE_AUDIOBOOK_CHAPTER = 'c'
    TYPE_ALBUM_TRACK = 't'

    TYPE_CHOICES = (
        (TYPE_PODCAST_EPISODE, 'Podcast Episode'),
        (TYPE_AUDIOBOOK_CHAPTER, 'Audiobook Chapter'),
        (TYPE_ALBUM_TRACK, 'Album Track'),
    )

    type = CharField(
        max_length=1,
        null=False,
        blank=True,
        choices=TYPE_CHOICES,
    )

    def __str__(self):
        return self.title


class ProfileQueue(BaseModel):

    profile = ForeignKey(
        Profile,
        on_delete=CASCADE,
    )

    media_file = ForeignKey(
        MediaFile,
        on_delete=CASCADE,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['profile', 'media_file'],
                name='unique_profile_media_file',
            )
        ]


def playlist_contents_default():
    return []


class PlayList(BaseModel):

    title = build_title_field()

    owner = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='playlists',
    )


class PlayListItem(BaseModel):

    class Meta:
        unique_together = ('playlist', 'item_number')

    playlist = ForeignKey(
        PlayList,
        on_delete=CASCADE,
        related_name='items',
    )

    item_number = PositiveIntegerField(
        null=True,
        default=1
    )

    media_file = ForeignKey(
        MediaFile,
        on_delete=CASCADE,
        related_name='play_list_items',
    )


class Podcast(BaseModel):

    update_fields = ('title', 'website', 'rss', 'description')

    # This class doesn't inherit from TitledObjectMixin because of the
    # unique constraint on this field.
    title = CharField(max_length=200, unique=True)

    website = URLField(max_length=500, default='')
    
    rss = URLField(max_length=500, default='', unique=True)

    description = TextField(default='')

    def __str__(self):
        return self.title

    def fetch(self) -> Optional[Model]:
        try:
            podcast = Podcast.objects.get(rss__iexact=self.rss)
        except ObjectDoesNotExist:
            return None
        else:
            return podcast


class PodcastEpisode(MediaFile):

    update_fields = (
        'podcast', 'title', 'url',
        'pub_date', 'description',
    )

    podcast = ForeignKey(
        Podcast,
        related_name='episodes',
        on_delete=CASCADE
    )

    url = URLField(max_length=500, default='', unique=True)

    pub_date = DateTimeField(
        null=True,
        blank=True,
    )

    description = TextField(default='')

    def fetch(self) -> Optional[Model]:
        try:
            episode = PodcastEpisode.objects.get(url__iexact=self.url)
        except ObjectDoesNotExist:
            return None
        else:
            return episode


class Audiobook(BaseModel):

    title = build_title_field()


class AudiobookChapter(MediaFile):
    audiobook = ForeignKey(
        Audiobook,
        related_name='chapters',
        on_delete=CASCADE
    )

    chapter = IntegerField(
        null=False,
        blank=False,
        default=0,
    )

    class Meta:
        unique_together = [[
            'audiobook',
            'chapter'
        ]]


class Album(BaseModel):

    title = build_title_field()

    def __str__(self):
        return self.title


class AlbumTrackManager(Manager):

    def create(self, **kwargs):
        ...

class AlbumTrack(MediaFile):

    album = ForeignKey(
        Album,
        null=True,
        blank=True,
        related_name='tracks',
        on_delete=CASCADE,
    )

    disc = IntegerField(default=1)

    track = IntegerField(default=1)














