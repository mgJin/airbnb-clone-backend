from django.db import models
from common.models import CommonModel


class Room(CommonModel):

    """Room model Definition"""

    class RoomKindChoice(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_PLACE = ("private_place", "Private Place")
        SHARED_PLACE = ("shared_place", "Shared Place")
    #방이름
    name = models.CharField(max_length=180,default="",)

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
    # 가격
    price = models.PositiveIntegerField()
    # 방 개수
    rooms = models.PositiveIntegerField()
    # 화장실 갯수
    toilet = models.PositiveIntegerField(null=True)
    # 설명
    description = models.TextField()
    # 주소
    address = models.CharField(max_length=250)
    # 애완동물
    pet_freindly = models.BooleanField(
        default=True,
    )
    # 방의 종류  choice로 선택
    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoice.choices,
    )
    # 방의 주인
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    #카테고리
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    #어떤 모델을 가지고 싶은지 적어줘야함 Room 클래스에서 amenity지정
    amenities = models.ManyToManyField("rooms.Amenity")
   
    def __str__(self)->str:
        return self.name


# amenity: 쾌적함,살아가는데 필요한 종합적인것들
# 다대다 관계(many to many)
class Amenity(CommonModel):

    """Amenity Definition"""

    name = models.CharField(
        max_length=150,
    )
    description = models.CharField(
        max_length=150,
        null=True, #이 필드가 데이터베이스에서 null일 수 있다
        blank=True,# black=True 면 DjangoForm에서 공백을 의미
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Amenities"
