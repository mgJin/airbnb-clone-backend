from django.urls import path
from . import views

#이미 rooms/로 들어온 상태
urlpatterns = [
    path("", views.see_all_rooms), #그래서 경로에 ""만 적어놓았다
    path("<int:room_pk>",views.see_one_room), #담아올 변수는 <>로 표시
]