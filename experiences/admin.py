from django.contrib import admin
from .models import Experiences, Perk

@admin.register(Experiences)
class ExperiencAdmin(admin.ModelAdmin):
    
    list_display =(
        "name",
        "price",
        "start",
        "end",
    )

    list_filter = (
        "category",
    )

@admin.register(Perk)
class PerkAdmin(admin.ModelAdmin):
    
    list_display =(
        "name",
        "details",
        "explanation"
    )