from django.contrib import admin
from .models import Photo,video

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass

@admin.register(video)
class VideoAdmin(admin.ModelAdmin):
    pass
