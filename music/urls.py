# music/urls.py (Updated)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_song, name='upload_song'),
    path('profile/', views.profile, name='profile'),
    path('log_play/<int:song_id>/', views.log_song_play, name='log_song_play'),
    # Add this new URL for the search results page
    path('search/', views.search_results, name='search_results'),
    path('like_song/<int:song_id>/', views.like_song, name='like_song'),
]