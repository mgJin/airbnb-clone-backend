from django.db import transaction
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        return Response(
            AmenitySerializer(self.get_object(pk)).data,
        )

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(
                AmenitySerializer(updated_amenity).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(
                data=request.data,
            )
            if serializer.is_valid():
                #request에서 category의 id를 받음
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required")
                try:
                    category = Category.objects.get(
                        pk=category_pk,
                    )
                    #카테고리의 kind가 room이 아니라면 에러
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("Category kind should be rooms")
                except Category.DoesNotExist:
                    raise ParseError("Category do not found")
                try:
                    with transaction.atomic():
                        room = serializer.save(
                            owner=request.user,
                            category=category,
                        )
                        #save한 후에 받음으로써 방을 만들 떄 꼭 필요하지는 않게 만듦
                        amenities= request.data.get("amenities")
                
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                        serializer = RoomDetailSerializer(room)
                        return Response(serializer.data)
                except Exception:
                    raise ParseError("Amennnniitttyy")
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if request.user != room.owner:
            raise PermissionDenied
        
        serializer = RoomDetailSerializer(
            room, 
            data = request.data,
            partial=True,
            )
        if serializer.is_valid():
            
            if request.data.get("category"):
                try:
                    category_pk = request.data.get("category")
                    if Category.objects.get(pk = category_pk):
                        category = Category.objects.get(pk = category_pk)
                        if category.kind != Category.CategoryKindChoices.ROOMS:
                            raise ParseError("Room category kind must be rooms")

                        room=serializer.save(category = category)
                except Category.DoesNotExist:
                    raise NotFound
            else:
                room = serializer.save()
            
            if request.data.get("amenities"):
                amenities_pk_list = request.data.get("amenities")
                room.amenities.clear()
                try:
                    for amenity_pk in amenities_pk_list:
                        amenity = Amenity.objects.get(pk = amenity_pk)
                        room.amenities.add(amenity)
                    
                except Amenity.DoesNotExist:
                    pass
            return Response(
                        RoomDetailSerializer(room).data
            )
        else:
            return Response(
                serializer.errors
            )
   
    #delete를 할때는 유저가 로그인 됐는지, 유저가 방주인이랑 같은지 확인해야함
    def delete(self,request,pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied

        room.delete()
        return Response(
            status= HTTP_204_NO_CONTENT
        )
