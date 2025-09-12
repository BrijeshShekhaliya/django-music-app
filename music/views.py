# music/views.py (Corrected and Cleaned)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required
from .models import Song, Creator, CustomUser, SongHistory
from .forms import SongForm, UserUpdateForm
from mutagen.mp3 import MP3
from django.contrib import messages
from .recommender import get_recommendations_for_user 
from django.db.models import Q 

def home(request):
    return render(request, "music/home.html")

@login_required
def upload_song(request):
    try:
        creator = request.user.creator
    except Creator.DoesNotExist:
        messages.error(request, 'You need to be a creator to upload songs.')
        return redirect('home')

    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = request.FILES['song_file']
            try:
                audio = MP3(audio_file)
                duration = int(audio.info.length)
                if duration > 600: # 10 minutes limit
                    messages.error(request, 'Song duration cannot exceed 10 minutes.')
                    return render(request, 'upload_song.html', {'form': form})
            except Exception as e:
                messages.error(request, f'Could not read audio file: {e}')
                return render(request, 'upload_song.html', {'form': form})

            song = form.save(commit=False)
            song.uploaded_by = creator
            song.duration_in_seconds = duration
            song.is_approved = False
            song.save()
            
            messages.success(request, 'Your song has been uploaded and is pending approval!')
            return redirect('home')
    else:
        form = SongForm()
    
    return render(request, 'upload_song.html', {'form': form})

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
def log_song_play(request, song_id):
    if request.method == 'POST':
        song = get_object_or_404(Song, id=song_id)
        SongHistory.objects.create(user=request.user, song=song)
        return JsonResponse({'status': 'success', 'message': 'Play logged.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)

def search_results(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Song.objects.filter(
            Q(name__icontains=query) | Q(author_name__icontains=query),
            is_approved=True
        ).distinct()

    context = { 'query': query, 'results': results }
    return render(request, 'search_results.html', context)

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

@login_required
def listener_dashboard(request):
    if request.user.role != "listener":
        return redirect("creator_dashboard")
    return render(request, "music/listener_dashboard.html")

@login_required
def creator_dashboard(request):
    if request.user.role != "creator":
        return redirect("listener_dashboard")
    return render(request, "music/creator_dashboard.html")

def redirect_after_login(request):
    if request.user.role == "creator":
        return redirect("creator_dashboard")
    return redirect("listener_dashboard")