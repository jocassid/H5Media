"""
URL configuration for h5media project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
)
from django.urls import path

from h5media.views import (
    HomeView,
    PodcastEpisodeAddToQueueView,
    PodcastEpisodeListView,
    PodcastView,
    PodcastsView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'login/',
        LoginView.as_view(template_name='login.html'),
        name='login',
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout',
    ),
    path(
        'password-reset/',
        PasswordResetView.as_view(template_name="password_reset.html"),
        name='password_reset',
    ),
    path(
        'podcasts/',
        PodcastsView.as_view(),
        name='podcasts',
    ),
    path(
        'podcasts/<int:pk>/',
        PodcastView.as_view(),
        name='podcast',
    ),
    path(
        'podcasts/<int:pk>/episodes/',
        PodcastEpisodeListView.as_view(),
        name='podcast_episode_list',
    ),
    path(
        'podcasts/episodes/<int:pk>/queue-add/',
        PodcastEpisodeAddToQueueView.as_view(),
        name='podcast_episode_add_to_queue',
    ),
    path(
        '',
        HomeView.as_view(),
        name='home',
    )
]
