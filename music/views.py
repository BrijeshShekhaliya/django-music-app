# music/views.py (Updated)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required # Import this
from .models import Song, Creator, CustomUser, SongHistory
from .forms import SongForm, UserUpdateForm # Import your new form
from mutagen.mp3 import MP3 # Import mutagen
from django.contrib import messages # To show success/error messages
from .recommender import get_recommendations_for_user 
from django.db.models import Q 

def home(request):
    approved_songs = Song.objects.filter(is_approved=True)
    context = {'songs': approved_songs}
    return render(request, 'home.html', context)

# Add this new view function
@login_required
def upload_song(request):
    # First, check if the logged-in user has a Creator profile
    try:
        creator = request.user.creator
    except Creator.DoesNotExist:
        messages.error(request, 'You need to be a creator to upload songs.')
        return redirect('home') # Or redirect to a 'become a creator' page

    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            # Check song duration before saving
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

            # Save the form but don't commit to the database yet
            song = form.save(commit=False)
            song.uploaded_by = creator
            song.duration_in_seconds = duration
            song.is_approved = False # All songs must be approved by an admin
            song.save()
            
            messages.success(request, 'Your song has been uploaded and is pending approval!')
            return redirect('home')
    else:
        form = SongForm()
    
    return render(request, 'upload_song.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        # If a GET request, create the form pre-filled with the user's current info
        form = UserUpdateForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})

# Add this new view for logging history
@login_required
def log_song_play(request, song_id):
    if request.method == 'POST':
        # Find the song object, or return a 404 error if it doesn't exist
        song = get_object_or_404(Song, id=song_id)
        
        # Create a new entry in the SongHistory model
        SongHistory.objects.create(user=request.user, song=song)
        
        # Return a success response in JSON format
        return JsonResponse({'status': 'success', 'message': 'Play logged.'})
    
    # If it's not a POST request, return an error
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)

def home(request):
    approved_songs = Song.objects.filter(is_approved=True)
    
    recommendations = []
    # Check if the user is logged in
    if request.user.is_authenticated:
        # Get recommendations for the logged-in user
        recommendations = get_recommendations_for_user(request.user)

    context = {
        'songs': approved_songs,
        'recommendations': recommendations, # Add recommendations to the context
    }
    return render(request, 'home.html', context)

def search_results(request):
    # Get the search query from the URL (?q=...)
    query = request.GET.get('q')
    
    results = []
    if query:
        # Use a Q object to search in multiple fields (name OR author_name)
        # The 'icontains' makes the search case-insensitive
        results = Song.objects.filter(
            Q(name__icontains=query) | Q(author_name__icontains=query),
            is_approved=True
        ).distinct()

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'search_results.html', context)

@login_required
def like_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    if song in request.user.liked_songs.all():
        # User has already liked it, so unlike it
        request.user.liked_songs.remove(song)
        liked = False
    else:
        # User hasn't liked it yet, so like it
        request.user.liked_songs.add(song)
        liked = True
    return JsonResponse({'liked': liked})