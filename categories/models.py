from django.db import models
from common.models import CommonModel

class Category(CommonModel):
    
    """Room or Experience Category"""
    class CategoryKindChoices(models.TextChoices):
        ROOMS = "rooms", "Rooms"
        EXPERIENCES = "experiences" , "Experiences"

    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=15, choices=CategoryKindChoices.choices)

    #title() : 첫 글자 대문자(메서드든 뭐든)
    def __str__(self) -> str:
        return f"{self.kind.title()}: {self.name}"
    
    class Meta:
        verbose_name_plural = "Categories"
