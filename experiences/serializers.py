from rest_framework.serializers import ModelSerializer
from .models import Perk,Experiences
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer

class PerkSerializer(ModelSerializer):

    class Meta:
        model = Perk
        fields = "__all__"

class ExperiencesListSerializer(ModelSerializer):

    class Meta:
        model = Experiences
        fields = (
            "country",
            "city",
            "name",
            "price",
        )

class ExperiencesDetailSerializer(ModelSerializer):
    #난 새로운 호스트를 만드는게 아니라 있는 user를 가지고 오는것=>read_only
    host = TinyUserSerializer(read_only=True,)
    category = CategorySerializer(read_only=True,)
    perks = PerkSerializer(read_only=True,)

    class Meta:
        model = Experiences
        fields = "__all__"