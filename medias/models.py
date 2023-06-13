from django.db import models
from common.models import CommonModel

class Photo(CommonModel):

    file = models.URLField()
    description = models.CharField(max_length=140,)
    room =models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        null=True,
        blank = True,
        related_name="photos",
    )

    experience = models.ForeignKey(
        "experiences.Experiences",
        on_delete=models.CASCADE,
        null=True,
        blank = True,
        related_name="photos",     
    )

    def __str__(self) -> str:
        return "Photo File"

class video(CommonModel):
    #동영상 파일은 imagefield처럼 따로 없다
    file = models.URLField()
    #지금 동영상은 하나의 활동에만 귀속되는 상태
    #따라서 onetoone이 된다
    #onetoone은 고유한 값이 된다 ==> 다른 곳에서 쓸 수 없게 된다(서로 하나만 된다)
    #foriegnkey는 다른곳에서 쓸 수가 있다.
    experience = models.OneToOneField(
        "experiences.Experiences",
        on_delete=models.CASCADE,
        related_name="videos",
    )

    def __str__(self) -> str:
        return "Video File"