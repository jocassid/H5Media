
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class BaseView(LoginRequiredMixin, TemplateView):
    """Abstract class"""
    pass


class HomeView(BaseView):
    template_name = 'home.html'


