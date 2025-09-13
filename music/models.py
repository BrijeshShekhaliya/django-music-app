# music/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("listener", "Listener"),
        ("creator", "Creator"),
    ]

    mobile_number = models.CharField(max_length=15, unique=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    profile_avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="listener")
    liked_songs = models.ManyToManyField('Song', blank=True, related_name='liked_by')

    def is_creator(self):
        return self.role == "creator"

    def is_listener(self):
        return self.role == "listener"

    def __str__(self):
        return f"{self.username} ({self.role})"


class Creator(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="creator"
    )
    youtube_channel_link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Creator: {self.user.username}"


class Song(models.Model):
    name = models.CharField(max_length=200)
    author_name = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(Creator, related_name='songs', on_delete=models.CASCADE)
    song_file = models.FileField(upload_to='songs/')
    theme_image = models.ImageField(upload_to='song_images/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # ✅ Approval status
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SongHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="song_history"
    )
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name="play_history"
    )
    listened_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} listened to {self.song.name} on {self.listened_at}"


@receiver(post_save, sender=CustomUser)
def create_creator_profile(sender, instance, created, **kwargs):
    if created and instance.role == "creator":
        Creator.objects.get_or_create(user=instance)
