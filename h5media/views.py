
from http import HTTPStatus
from logging import getLogger
from typing import Optional, List, Set, Union

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.db.models import BooleanField, Count, Q
from django.db.models.functions import Cast
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from h5media.actions.podcast_actions import AddEpisodeToQueueAction
from h5media.models import (
    MediaFile,
    Podcast,
    PodcastEpisode,
    Profile,
)
from h5media.serializers import PodcastEpisodeSerializer


logger = getLogger('web')


class ApiError(RuntimeError):
    def __init__(
            self,
            message_or_messages: Union[str, List[str]],
            status: int = 400,
    ):
        if isinstance(message_or_messages, list):
            messages = message_or_messages
            super().__init__(messages[0])
            self.messages = messages
        else:
            message = str(message_or_messages)
            super().__init__(message)
            self.messages = [message]
        self.status = status

    @property
    def has_multiple_messages(self):
        return len(self.messages) > 1


def error_response(request: HttpRequest, api_error: ApiError):
    return render(
        request,
        'error.html',
        {'api_error': api_error},
        status=api_error.status,
    )


class GetProfileMixin:

    @staticmethod
    def get_profile(request: HttpRequest) -> Optional[Profile]:
        try:
            return Profile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return None


class BaseView(LoginRequiredMixin, GetProfileMixin, TemplateView):
    """Abstract class"""
    def get_context_data(self, **kwargs):
        request: HttpRequest = self.request
        message = f"user={request.user} path={request.path}"
        logger.info(message)
        return {}


class BaseDetailView(LoginRequiredMixin, GetProfileMixin, DetailView):
    """Abstract class"""
    pass


class BasePostView(BaseView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.response_status: int = HTTPStatus.OK.value

    def post(self, request, *args, **kwargs):

        try:
            return render(
                request,
                self.template_name,
                self.get_context_data(**kwargs),
                status=self.response_status
            )
        except ApiError as error:
            return error_response(request, error)

    def get_context_data(self, **kwargs):
        """Subclasses may override this to update records in the database and
        provide any data needed to render a response"""
        context = super().get_context_data(**kwargs)
        return context


class PageView(BaseView):
    page_title_suffix = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title_suffix'] = self.page_title_suffix
        return context


class HomeView(PageView):
    template_name = 'home.html'
    page_title_suffix = 'Home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MediaFile'] = MediaFile

        profile = self.get_profile(self.request)
        if profile:
            queue = profile.queue or []
        else:
            queue = []

        context['queue'] = queue
        return context


class PodcastsView(PageView):
    template_name = 'podcasts.html'
    page_title_suffix = 'Podcasts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['podcasts'] = Podcast.objects.prefetch_related(
            'episodes'
        ).order_by('title')
        return context


class PodcastSearchView(PageView):
    template_name = 'podcast_search.html'
    page_title_suffix = 'Podcast Search'

    def get_context_data(self, **kwargs):
        return self.get_context_data_inner(
            super().get_context_data(**kwargs),
            str(self.request.GET.get('search') or ''),
            self.request.user,
        )

    @staticmethod
    def get_context_data_inner(
            context: dict,
            search: str,
            user: User,
    ):
        if search:
            podcasts = Podcast.objects.annotate(
                subscribed=Cast(
                    Count(
                        'subscribers',
                        filter=Q(subscribers=user.id)
                    ),
                    output_field=BooleanField(),
                )
            ).filter(
                title__icontains=search,
            ).order_by('title')
        else:
            podcasts = Podcast.objects.none()

        context.update(
            search=search,
            podcasts=list(podcasts),
        )
        return context


class PodcastView(BaseDetailView):
    """Displays Podcast title, url, description along with a list of
    episodes"""

    template_name = 'podcast.html'
    page_title_suffix = 'Podcast'
    model = Podcast

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class PodcastEpisodeListView(BaseView):
    template_name = 'podcast_episode_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        podcast_pk = kwargs.get('pk') or 0
        if not podcast_pk:
            context['episodes'] = []
            return context

        profile = self.get_profile(self.request)
        context['in_queue_pks'] = self.get_in_queue_pks(profile)

        episodes = PodcastEpisode.objects.filter(
            podcast_id=podcast_pk,
        ).order_by(
            'pub_date'
        )

        paginator = Paginator(episodes, 25)
        episodes = paginator.page(1)

        context['episodes'] = episodes
        return context

    @staticmethod
    def get_in_queue_pks(profile: Optional[Profile]) -> Set[int]:
        """Returns a set of the primary keys for MediaFiles that are in
        Profile.now_playing or in Profile.queue"""
        if not profile:
            return set()

        pks = set()

        now_playing: dict = profile.now_playing
        if now_playing:
            pk = now_playing.get('pk') or 0
            if pk:
                pks.add(pk)

        queue: List[dict] = profile.queue
        if not queue:
            return pks

        for item in queue:
            pk = item.get('pk') or 0
            if pk:
                pks.add(pk)
        return pks


class PodcastEpisodeAddToQueueView(BasePostView):
    """Add Podcast to the user's queue.  return html for "in queue" button"""

    template_name = 'partial/in_queue_button.html'

    def get_context_data(self, **kwargs):
        return self.get_context_data_inner(
            episode_pk=kwargs.get('pk') or 0,
            user=self.request.user,
        )

    @staticmethod
    def get_context_data_inner(episode_pk: int, user: User):
        if not episode_pk:
            raise ApiError("missing pk", 400)

        try:
            episode = PodcastEpisode.objects.get(pk=episode_pk)
        except ObjectDoesNotExist:
            raise ApiError("No podcast episode found", 404)

        profile = user.profile
        if not profile:
            raise ApiError(f"User {user.username} missing profile")

        AddEpisodeToQueueAction().run(episode, profile)
        return {}

#
# class PodcastSearchView(PageView):
#
#     page_title_suffix = 'search podcasts'
#     template_name = 'podcast_search.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         return context


class PodcastToggleSubscription(BasePostView):
    """<input type='checkbox'/> can create a included template for using in
    podcast_search.html and to be used by this view."""
    template_name = 'partial/podcast_subscribe_checkbox.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        request = self.request

        errors = []
        status = HTTPStatus.OK

        user = getattr(request, 'user', None)
        if not user:
            errors.append("missing user")
            status = HTTPStatus.BAD_REQUEST

        podcast_pk = request.POST.get('podcast_pk') or 0
        if not podcast_pk:
            errors.append('missing podcast_pk')
            status = HTTPStatus.BAD_REQUEST

        if errors:
            raise ApiError(errors, status=status)

        try:
            podcast = Podcast.objects.get(pk=podcast_pk)
        except ObjectDoesNotExist:
            raise ApiError(
                f"Podcast (PK={podcast_pk}) not found",
                status=HTTPStatus.NOT_FOUND,
            )

        if podcast in user.podcasts_subscribed_to.all():
            user.podcasts_subscribed_to.remove(podcast)
            subscribed = False
        else:
            user.podcasts_subscribed_to.add(podcast)
            subscribed = True

        setattr(podcast, 'subscribed', subscribed)
        context['podcast'] = podcast
        return context


class DevelopmentView(BasePostView):

    template_name = 'partial/development.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        request = self.request
        method = request.method
        content_type = request.content_type

        context.update({
            'method': method,
            'content_type': content_type,
        })

        if method == 'POST':
            if request.POST:
                context['POST'] = request.POST
            else:
                context['body'] = request.body

        return context











