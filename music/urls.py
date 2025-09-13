from django.urls import path
from . import views
from .views import CustomConfirmEmailView

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_song, name='upload_song'),
    path('profile/', views.profile, name='profile'),
    path('log_play/<int:song_id>/', views.log_song_play, name='log_song_play'),
    path('search/', views.search_results, name='search_results'),
    path('like_song/<int:song_id>/', views.like_song, name='like_song'),
    path('creator-dashboard/', views.creator_dashboard, name='creator_dashboard'),
    path('listener-dashboard/', views.listener_dashboard, name='listener_dashboard'),
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),
    path('custom-logout/', views.custom_logout, name='custom_logout'),

    # Email confirmation
    path('accounts/confirm-email/<key>/', CustomConfirmEmailView.as_view(), name='account_confirm_email'),

    # Logout success
    path('logout-success/', lambda request: render(request, "account/logout_success.html"), name='logout_success'),
]
