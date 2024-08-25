
from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from h5media.models import Podcast, PodcastEpisode, Profile


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
    pass


class BaseDetailView(LoginRequiredMixin, DetailView):
    """Abstract class"""
    pass


class BasePostView(LoginRequiredMixin, View):

    template_name = 'SUBCLASSES SHOULD RE-DEFINE THIS'

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
        return {}


class PageView(BaseView):
    page_title_suffix = ''

    def get_context_data(self, **kwargs):
        return {
            'page_title_suffix': self.page_title_suffix
        }


class HomeView(PageView):
    template_name = 'home.html'
    page_title_suffix = 'Home'


class PodcastsView(PageView):
    template_name = 'podcasts.html'
    page_title_suffix = 'Podcasts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile: Profile = self.request.user.profile
        context['subscribed_podcasts'] = Podcast.objects.filter(
            subscribers=profile
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
        pk = kwargs.get('pk') or 0
        if not pk:
            raise ApiError("missing pk", 400)

        if not PodcastEpisode.objects.filter(pk=pk).exists():
            raise ApiError("No podcast episode found", 404)

        print(f"{kwargs=}")
        return {}






