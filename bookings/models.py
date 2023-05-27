from django.db import models
from common.models import CommonModel


class Booking(CommonModel):

    """Booking model Definition"""

    class BookingKindChoices(models.TextChoices):
        Room = "room", "Room"
        Experience = "experience", "Experience"

    kind = models.CharField(
        max_length=15,
        choices=BookingKindChoices.choices,
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    #예약은 하나의 방만 가질 수 있다.
    room = models.ForeignKey(
        "rooms.Room",
        null = True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    experience = models.ForeignKey(
        "experiences.Experiences",
        null = True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    #Room예약은 날짜만 신경쓰기
    check_in = models.DateField(null=True,blank=True,)
    check_out = models.DateField(null=True,blank=True,)

    #Expereinces 는 시간까지 신경써야함

    experience_time = models.DateTimeField(null=True,blank=True,)
    guests = models.PositiveIntegerField()
