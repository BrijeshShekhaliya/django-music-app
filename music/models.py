from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# User Model: The base for everyone
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("listener", "Listener"),
        ("creator", "Creator"),
    ]

    mobile_number = models.CharField(max_length=15, unique=True, blank=False, null=False)
    age = models.PositiveIntegerField(blank=True, null=True)
    profile_avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="listener")

    def is_creator(self):
        return self.role == "creator"

    def is_listener(self):
        return self.role == "listener"

# Creator Profile: Linked to a User, with specific fields
class Creator(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    youtube_channel_link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Song Model: The core of the platform
class Song(models.Model):
    name = models.CharField(max_length=200)
    theme_image = models.ImageField(upload_to='song_themes/')
    author_name = models.CharField(max_length=200)
    song_file = models.FileField(upload_to='songs/')
    duration_in_seconds = models.PositiveIntegerField()
    uploaded_by = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='songs')
    is_approved = models.BooleanField(default=False)  # Admin controls this!
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'author_name')

    def __str__(self):
        return f'"{self.name}" by {self.author_name}'

# History Model: Powers the AI song suggestions
class SongHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    listened_at = models.DateTimeField(auto_now_add=True)
