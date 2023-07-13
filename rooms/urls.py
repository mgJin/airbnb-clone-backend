from django.urls import path
from . import views

# 이미 rooms/로 들어온 상태
# urlpatterns = [
#     path("", views.see_all_rooms), #그래서 경로에 ""만 적어놓았다
#     path("<int:room_pk>",views.see_one_room), #담아올 변수는 <>로 표시
# ]

urlpatterns = [
    path("", views.Rooms.as_view()),
    path("<int:pk>", views.RoomDetail.as_view()),
    path("<int:pk>/reviews", views.RoomReviews.as_view()),
    path("<int:pk>/amenities/", views.RoomAmenities.as_view()),
    path("<int:pk>/photos/", views.RoomPhotos.as_view()),
    path("<int:pk>/bookings/", views.RoomBookings.as_view()),
    path("<int:pk>/bookings/check", views.RoomBookingsCheck.as_view()),
    path("amenities/", views.Amenities.as_view()),
    path("amenities/<int:pk>", views.AmenityDetail.as_view()),
]
