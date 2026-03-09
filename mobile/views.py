
from django.shortcuts import render
from django.views.generic import TemplateView

from h5media.views import PageView
from h5media.models import MediaFile

# Create your views here.

class HomeView(PageView):
    template_name = 'mobile/home.html'
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


class MenuView(TemplateView):

    template_name = 'mobile/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class CloseMenuView(TemplateView):

    template_name = 'mobile/close_menu.html'
