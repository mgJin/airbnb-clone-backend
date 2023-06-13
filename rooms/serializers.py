from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import Amenity ,Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist

class AmenitySerializer(ModelSerializer):

    class Meta:
        model = Amenity
        fields =(
            "name",
            "description",
        )


class RoomDetailSerializer(ModelSerializer):

    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(read_only=True,many=True)
    category = CategorySerializer(read_only=True,)
    rating= SerializerMethodField()
    is_owner = SerializerMethodField()
    is_liked = SerializerMethodField()
    #리뷰는 따로 뺴기
    # reviews = ReviewSerializer(many = True, read_only=True,)
    photos = PhotoSerializer(many = True, read_only=True,)
    
    class Meta:
        model = Room
        fields = "__all__"


    def get_rating(self,room):

        return room.rating()
    
    def get_is_owner(self,room):
        request = self.context['request']
        return request.user == room.owner
    
    def get_is_liked(self,room):
        request = self.context['request']
        #user가 만든 wishlist 중에 room id 가 있는 room list를 포함한 wishlist
        return Wishlist.objects.filter(
            user = request.user,
            rooms__pk = room.pk
        ).exists()

    

class RoomListSerializer(ModelSerializer):

    rating = SerializerMethodField()
    photos = PhotoSerializer(many = True, read_only=True,)
    is_owner = SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "id",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "photos",
            "is_owner",
        )
    
    def get_rating(self,room):
        # print(room)
        return room.rating()
    
    def get_is_owner(self,room):
        request = self.context['request']
        return request.user == room.owner
