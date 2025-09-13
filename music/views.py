# music/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Song, Creator, SongHistory
from .forms import SongForm, UserUpdateForm
from mutagen.mp3 import MP3
from django.contrib import messages
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from allauth.account.views import ConfirmEmailView

@login_required
def search_results(request):
    query = request.GET.get('q', '')
    songs = Song.objects.filter(name__icontains=query, is_approved=True) if query else []
    return render(request, "music/search_results.html", {"songs": songs})


@never_cache
def home(request):
    if request.user.is_authenticated:
        if request.user.is_creator():
            return redirect("creator_dashboard")
        else:
            return redirect("listener_dashboard")
    return render(request, "music/home.html")


@login_required
def redirect_after_login(request):
    user = request.user
    if user.is_superuser:
        return redirect('/admin/')
    elif user.is_creator():
        return redirect('creator_dashboard')
    else:
        return redirect('listener_dashboard')


@login_required
def upload_song(request):
    if not request.user.is_creator():
        messages.warning(request, "You must be a Creator to upload songs.")
        return redirect("listener_dashboard")

    creator_profile, created = Creator.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.uploaded_by = creator_profile

            song_file = request.FILES.get('song_file')
            if song_file:
                audio = MP3(song_file)
                song.duration_in_seconds = int(audio.info.length)

            song.status = "pending"
            song.save()
            messages.success(request, "Your song has been uploaded successfully and is awaiting approval.")
            return redirect("creator_dashboard")
    else:
        form = SongForm()

    return render(request, "music/upload_song.html", {"form": form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})


@login_required
def listener_dashboard(request):
    if request.user.is_creator():
        messages.warning(request, "You are a Creator, not a Listener!")
        return redirect("creator_dashboard")

    # Use uploaded_at to order newest first
    songs = Song.objects.filter(is_approved=True).order_by('-uploaded_at')
    return render(request, "music/listener_dashboard.html", {"songs": songs})


@login_required
def creator_dashboard(request):
    if not request.user.is_creator():
        messages.warning(request, "You must be a Creator to access this page.")
        return redirect("listener_dashboard")

    creator_profile = getattr(request.user, "creator", None)
    if not creator_profile:
        messages.error(request, "Creator profile not found.")
        return redirect("home")

    songs = creator_profile.songs.all().order_by('-uploaded_at')
    return render(request, "music/creator_dashboard.html", {"songs": songs})


@login_required
def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("account_login")


@login_required
def log_song_play(request, song_id):
    if request.method == 'POST':
        song = get_object_or_404(Song, id=song_id)
        SongHistory.objects.create(user=request.user, song=song)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        self.object = self.get_object()
        email_address = self.object.email_address
        email_address.verified = True
        email_address.save()

        user = email_address.user
        user.is_active = True
        user.save()

        messages.success(self.request, "Your email has been confirmed successfully.")
        return render(self.request, "account/email_confirm_success.html")
    

@login_required
def like_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    if song in request.user.liked_songs.all():
        request.user.liked_songs.remove(song)
        liked = False
    else:
        request.user.liked_songs.add(song)
        liked = True
    return JsonResponse({'liked': liked})
