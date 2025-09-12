from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Creator, Song, SongHistory

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'mobile_number', 'age', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('mobile_number', 'age', 'profile_avatar')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('mobile_number', 'age', 'profile_avatar')}),
    )

class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'author_name', 'uploaded_by', 'is_approved')

class SongHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'song', 'listened_at')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Creator)
admin.site.register(Song, SongAdmin)
admin.site.register(SongHistory, SongHistoryAdmin)