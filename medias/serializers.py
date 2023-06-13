from rest_framework.serializers import ModelSerializer
from .models import Photo,video


class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "pk",
            "file",
            "description",
        )