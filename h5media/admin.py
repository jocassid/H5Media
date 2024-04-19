
from django.contrib.admin import ModelAdmin, register

from h5media.models import Podcast


@register(Podcast)
class PodcastAdmin(ModelAdmin):
    list_display = (
        'name',
        'website',
        'rss',
    )
