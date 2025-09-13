from django.contrib import admin
from .models import CustomUser, Creator, Song, SongHistory

# ---------------------------
# CustomUser Admin
# ---------------------------
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'mobile_number', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'mobile_number']

# ---------------------------
# Creator Admin
# ---------------------------
@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ['user', 'youtube_channel_link']
    search_fields = ['user__username', 'youtube_channel_link']

# ---------------------------
# Song Admin
# ---------------------------
@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['name', 'author_name', 'uploaded_by', 'status', 'uploaded_at']
    list_filter = ['is_approved', 'uploaded_at']
    search_fields = ['name', 'author_name', 'uploaded_by__user__username']

    def status(self, obj):
        return "Approved" if obj.is_approved else "Awaiting Approval"
    status.short_description = "Status"
# ---------------------------
# SongHistory Admin
# ---------------------------
@admin.register(SongHistory)
class SongHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'song', 'listened_at']
    search_fields = ['user__username', 'song__name']
    list_filter = ['listened_at']
