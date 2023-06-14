from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        # (DB에 들어갈 value, admin페이지에서 보게되는 label)
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        # max_langth=20으로 해놨으므로 DB에 들어갈 값은 그보다 작아야함
        KR = ("kr", "Korean")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        # Tuple 을 꼭 써줄 필요 없다. 이것과 위에 ()를 쓴것과 같다
        WON = "won", "korean Won"
        USD = "usd", "Dollar"

    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )

    name = models.CharField(
        max_length=150,
        default="",
    )
    
    is_host = models.BooleanField(default=False)
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
    language = models.CharField(
        max_length=20,
        choices=LanguageChoices.choices,
    )

    currency = models.CharField(
        max_length=5,
        choices=CurrencyChoices.choices,
    )
    #form에서 필드를 비어둘 수 있게 해주는것 (null =True)랑은 다르다
    #form에서 필수적이지 않게 하는것(반드시 입력하시오가 아니게 하는것)
    profile_photo = models.URLField(blank=True)
