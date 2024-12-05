
from http import HTTPStatus
from logging import getLogger

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from h5media.models import Podcast, PodcastEpisode, Profile
from h5media.serializers import MediaFileSerializer


logger = getLogger('web')


class ApiError(RuntimeError):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.status = status


def error_response(request: HttpRequest, api_error: ApiError):
    return render(
        request,
        'error.html',
        {'error': str(api_error)},
        status=api_error.status,
    )


class BaseView(LoginRequiredMixin, TemplateView):
    """Abstract class"""
    def get_context_data(self, **kwargs):
        request: HttpRequest = self.request
        message = f"user={request.user} path={request.path}"
        print(message)
        logger.info(message)
        return {}


class BaseDetailView(LoginRequiredMixin, DetailView):
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
        return context


class PodcastsView(PageView):
    template_name = 'podcasts.html'
    page_title_suffix = 'Podcasts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user: User = self.request.user
        context['subscribed_podcasts'] = Podcast.objects.filter(
            subscribers=user,
        )
        return context


class PodcastSearchView(PageView):
    template_name = 'podcast_search.html'
    page_title_suffix = 'Podcast Search'

    def get_context_data(self, **kwargs):
        return self.get_context_data_inner(
            super().get_context_data(**kwargs),
            str(self.request.GET.get('search') or '')
        )

    @staticmethod
    def get_context_data_inner(
            context: dict,
            search: str,
            user: User,
    ):
        if search:
            podcasts = Podcast.objects.filter(
                title__icontains=search,
            ).order_by('title')
        else:
            podcasts = Podcast.objects.none()

        subscribed_to = set(
            user.podcasts_subscribed_to.values_list('pk', flat=True),
        )
        for


        context.update(
            search=search,
            podcasts=list(podcasts),
        )
        return context



class PodcastView(BaseDetailView):
    template_name = 'podcast.html'
    page_title_suffix = 'Podcast'
    model = Podcast

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PodcastEpisodeListView(BaseView):
    template_name = 'podcast_episode_list.html'

    def get_context_data(self, **kwargs):
        podcast_pk = kwargs.get('pk') or 0
        if not podcast_pk:
            return {'episodes': []}

        episodes = PodcastEpisode.objects.filter(
            podcast_id=podcast_pk,
        ).order_by(
            'pub_date'
        )

        paginator = Paginator(episodes, 25)
        episodes = paginator.page(1)

        return {'episodes': episodes}


class PodcastEpisodeAddToQueueView(BasePostView):
    """Add Podcast to the user's queue.  return html for "in queue" button"""

    template_name = 'partial/in_queue_button.html'

    def get_context_data(self, **kwargs):
        return self.get_context_data_inner(
            episode_pk=kwargs.get('pk') or 0,
            user=self.request.user
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

        data = MediaFileSerializer(episode).data

        profile.queue.append(data)
        profile.save()

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




