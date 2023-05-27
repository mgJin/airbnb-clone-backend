from django.contrib import admin
from .models import Room, Amenity

#Room class 의 admin 이 될 거다
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    
    list_display = (
        "name",
        "price",
        "kind",
        "owner",
        "created_at",
        "updated_at",
    )

    list_filter =(
        "country",
        "city",
        "pet_freindly",
        "kind",
        "amenities",
    )
@admin.register(Amenity)
class Amenity(admin.ModelAdmin):
    list_display=(
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    
    readonly_fields=(
        "created_at",
        "updated_at",
    )
    list_filter=(
        "created_at",
        "updated_at",
    )
