# music/admin.py (Final Corrected Version)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Creator, Song, SongHistory

# This class customizes how your CustomUser model is displayed in the admin
class CustomUserAdmin(UserAdmin):
    # This extends the default UserAdmin to include your custom fields
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('mobile_number', 'age', 'profile_avatar')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('mobile_number', 'age', 'profile_avatar')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'mobile_number')


class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'author_name', 'uploaded_by', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('name', 'author_name')
    actions = ['approve_songs']

    def approve_songs(self, request, queryset):
        queryset.update(is_approved=True)
    approve_songs.short_description = "Approve selected songs"


class SongHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'song', 'listened_at')
    list_filter = ('user', 'song')


# Register all your models with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Creator)
admin.site.register(Song, SongAdmin)
admin.site.register(SongHistory, SongHistoryAdmin)