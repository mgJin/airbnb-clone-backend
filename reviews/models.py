from django.db import models
from common.models import CommonModel

class Review(CommonModel):

    """ Review from a User to a Room or Experience"""

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="reviews",
        )

    #리뷰는 room의 것일 수도 experience의 것일 수도 있다.
    #따라서 null 이 될 수 있어야한다.
    room = models.ForeignKey(
        "rooms.Room",
        null = True,
        blank = True,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    experience = models.ForeignKey(
        "experiences.Experiences",
        null = True,
        blank = True,
        on_delete=models.CASCADE,
        related_name="reviews",

    )
    #유저가 남긴 리뷰
    payload = models.TextField()
    #유저가 남긴 평점
    rating = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.user} / {self.rating}"