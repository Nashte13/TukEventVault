#django built in admin interface
from django.contrib import admin
from .models import Event, EventData, Blog, UserProfile,Gallery, GalleryItem

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'event_type')
    search_fields = ('title', 'description')

@admin.register(EventData)
class EventDataAdmin(admin.ModelAdmin):
    list_display = ('event', 'file_type')
    list_filter = ('file_type',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content')

admin.site.register(Gallery)
admin.site.register(GalleryItem)

admin.site.register(UserProfile)