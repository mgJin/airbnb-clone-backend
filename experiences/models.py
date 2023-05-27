from django.db import models
from common.models import CommonModel


class Experiences(CommonModel):

    """Experiences model Definition"""

    # 나라
    country = models.CharField(
        max_length=50,
        default="한국",
    )
    # 도시
    city = models.CharField(
        max_length=80,
        default="서울",
    )

    name = models.CharField(
        max_length=250,
    )
    host = models.ForeignKey("users.User", on_delete=models.CASCADE,)

    price = models.PositiveIntegerField()

    address = models.CharField(max_length=250)
    # 시작 시간, timefield는 시,분,초만 기억한다
    start = models.TimeField()
    end = models.TimeField()

    description = models.TextField()

    perks = models.ManyToManyField(
        "experiences.Perk",
    )

    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self) -> str:
        return self.name


class Perk(CommonModel):
    "What is in experiences"

    name = models.CharField(
        max_length=100,
    )
    details = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        default="",
    )
    explanation = models.TextField(
        blank=True,
        null=True,
        default="",
    )

    def __str__(self) -> str:
        return self.name
