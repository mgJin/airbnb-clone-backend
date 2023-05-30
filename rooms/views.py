from django.shortcuts import render
from django.http import HttpResponse
from .models import Room


# /room 으로 접근했을 때 실행되는 함수
def see_all_rooms(request):
    rooms = Room.objects.all()

    return render(request, "all_rooms.html", {"rooms": rooms, "title": "good"})


def see_one_room(request, room_pk):
    try:
        room = Room.objects.get(pk=room_pk)
        return render(
            request,
            "room_detail.html",
            {
                "room": room,
            },
        )
    except Room.DoesNotExist: #error 원인이 이것이라면 밑에 것을 실행
        return render(
            request,
            "room_detail.html",
            {
                "not_found": True
            }
        )
