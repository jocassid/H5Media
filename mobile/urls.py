from django.urls import path
from . import views

app_name = 'mobile'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('menu/close/', views.CloseMenuView.as_view(), name='close_menu'),
]
