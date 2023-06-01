from rest_framework.serializers import ModelSerializer
from .models import User
class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "profile_photo",
            "username",
        )