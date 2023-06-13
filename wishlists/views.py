from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_200_OK,HTTP_204_NO_CONTENT
from .models import Wishlist
from .serializers import WishlistSerializer
from rooms.models import Room

class Wishlists(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):
        all_wishlists = Wishlist.objects.filter(user = request.user)
        serializer= WishlistSerializer(
            all_wishlists,
            many=True,
            context = {"request" : request},
        )
        return Response(
            serializer.data
        )

    def post(self,request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            wishlist=serializer.save(
                user= request.user,
            )
            serializer = WishlistSerializer(wishlist)
            return Response(
                serializer.data
            )
        else:
            return Response(
                serializer.errors
            )
        
class WishlistDetail(APIView):

    permission_classes = [IsAuthenticated]
    #개인만 볼 수 있는 프라이빗 한거이라 user까지 필요
    def get_object(self,pk,user):
        try:
            return Wishlist.objects.get(pk=pk, user = user)
        except Wishlist.DoesNotExist:
            raise NotFound
        

    def get(self,request,pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            context={"request":request}
        )
        return Response(
            serializer.data
        )
    
    def delete(self,request,pk):
        wishlist = self.get_object(pk,request.user)
        wishlist.delete()
        return Response(
            HTTP_204_NO_CONTENT
        )
    
    def put(self,request,pk):
        wishlist = self.get_object(pk,request.user)
        serializer = WishlistSerializer(
            wishlist,
            data=request.data,
            partial = True
        )
        if serializer.is_valid():
            updated_wishlist = serializer.save()
            serializer = WishlistSerializer(updated_wishlist)
            return Response(
                serializer.data
            )
        else:
            return Response(
                serializer.errors
            )


class WishlistToggle(APIView):

    def get_list(self,pk,user):
        try:
            return Wishlist.objects.get(pk=pk, user = user)
        except Wishlist.DoesNotExist:
            raise NotFound
    def get_room(self,pk):
        try:
            return Room.objects.get(pk = pk)
        except Room.DoesNotExist:
            raise NotFound
        
    def put(self,request, pk, room_pk):
        wishlist = self.get_list(pk,request.user)
        room = self.get_room(room_pk) 
        #단지 있는지 확인만 하는 것이므로 filter뒤에 exist를 한다(아니면 list를 받으니깐)
        if wishlist.rooms.filter(pk = room.pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        return Response(
            status = HTTP_200_OK
        )