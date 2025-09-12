# music/context_processors.py (Create this new file)

from .models import Creator

def is_creator_context(request):
    is_creator = False
    if request.user.is_authenticated:
        try:
            # Check if a Creator object exists for the logged-in user
            is_creator = Creator.objects.filter(user=request.user).exists()
        except Creator.DoesNotExist:
            is_creator = False
    return {'is_creator': is_creator}