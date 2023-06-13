from rest_framework import serializers
from .models import Review
from users.serializers import TinyUserSerializer
class ReviewSerializer(serializers.ModelSerializer):
    
    #유저가 직접 유저 항목을 입력하지 않고 쓸 수 있게 read_only=True
    user = TinyUserSerializer(read_only = True,)
    
    class Meta:
        model = Review
        fields = (
            "user",
            "payload",
            "rating",
        )

