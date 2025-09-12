# music/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_song, name='upload_song'),
    path('profile/', views.profile, name='profile'),
    path('log_play/<int:song_id>/', views.log_song_play, name='log_song_play'),
    path('search/', views.search_results, name='search_results'),
    path('like_song/<int:song_id>/', views.like_song, name='like_song'),

    # New
    path('dashboard/listener/', views.listener_dashboard, name='listener_dashboard'),
    path('dashboard/creator/', views.creator_dashboard, name='creator_dashboard'),
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),
]
