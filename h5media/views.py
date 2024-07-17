
from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from h5media.models import Podcast, PodcastEpisode, Profile


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
        return render(
            request,
            self.template_name,
            self.get_context_data(**kwargs),
            status=self.response_status
        )

    def get_context_data(self, **kwargs):
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

    template_name = ''

    # def post(self, *args, **kwargs):
    #     raise NotImplementedError("This should return a response")






