from django.db import transaction
from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound,ParseError,PermissionDenied
from rest_framework.status import HTTP_202_ACCEPTED,HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from .serializers import PerkSerializer,ExperiencesListSerializer,ExperiencesDetailSerializer
from .models import Perk,Experiences
from categories.models import Category
from bookings import models as bk_models, serializers as bk_serializers

class Perks(APIView):

    def get(self,request):
        perks = Perk.objects.all()
        serializer = PerkSerializer(perks,many=True,)
        return Response(
            serializer.data
        )

    def post(self,request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            new = serializer.save()
            return Response(
                PerkSerializer(new).data
            )
        else:
            return Response(
                serializer.errors
            )

class PerkDetail(APIView):

    def get_object(self,pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self,request,pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(
            serializer.data
        )

    def put(self,request,pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk,data=request.data,partial=True,)
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(
                PerkSerializer(updated_perk).data
            )
        else:
            return Response(
                serializer.errors
            )

    def delete(self,request,pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(
            status = HTTP_204_NO_CONTENT
        )
    

class ExperiencesList(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self,request):
        try:
            experiences = Experiences.objects.all()
        except Experiences.DoesNotExist:
            raise NotFound

        serializer = ExperiencesListSerializer(
            experiences,
            many=True,
        )
        return Response(
            serializer.data
        )
        

    def post(self,request):

        serializer = ExperiencesDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("need correct category_pk")
            try:
                category = Category.objects.get(pk = category_pk)
            
                if category.kind != Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("choose corretly category kind")
            except Category.DoesNotExist:
                raise NotFound("Can't find category")
            
            try:
                with transaction.atomic():
                    experience = serializer.save(
                        host = request.user,
                        category = category
                    )
                    perks_pk_list = request.data.get("perks")
                    for perk_pk in perks_pk_list:
                        perk = Perk.objects.get(pk = perk_pk)
                        experience.perks.add(perk)
                    serializer = ExperiencesDetailSerializer(experience)
                    return Response(
                        serializer.data
                    )
            except:
                raise ParseError("with wrong perks")
        else:
            return Response(
                serializer.errors
            )
        
class ExperienceDetail(APIView):

    def get_object(self,pk):
        try:
            return Experiences.objects.get(pk = pk)
        except:
            raise NotFound

    def get(self,request,pk):
        exp = self.get_object(pk)
        serializer = ExperiencesDetailSerializer(exp)
        return Response(
            serializer.data
        )
    
    def put(self,request,pk):

        exp = self.get_object(pk)
        if request.user != exp.host:
            raise PermissionDenied
        serializer= ExperiencesDetailSerializer(
            exp,
            data = request.data,
            partial =True,
        )
        if serializer.is_valid():
            
            if request.data.get('category'):
                try:
                    category_pk = request.data.get('category')
                    category = Category.objects.get(pk = category_pk)
                except Category.DoesNotExist:
                    raise NotFound("can't find category")
                    
                if category.kind != Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("wrong category choice")
                exp= serializer.save(
                    category=category
                )
            else:
                exp = serializer.save()
            if request.data.get('perks'):

                perks_pk = request.data.get('perks')
                
                exp.perks.clear()
                try:
                    for perk_pk in perks_pk:
                        perk = Perk.objects.get(pk = perk_pk)
                        exp.perks.add(perk)
                except Perk.DoesNotExist:
                    raise NotFound("Can't find Perks")
                serializer = ExperiencesDetailSerializer(exp)
            return Response(
                serializer.data                
            )
        else:
            return Response(
                serializer.errors
            )

    def delete(self,request,pk):
        
        exp = self.get_object(pk)
        if exp.host != request.user:
            raise PermissionDenied
        exp.delete()
        return Response(
            HTTP_202_ACCEPTED
        )


class ExperiencePerks(APIView):

    def get_object(self,pk):
        try:
            return Experiences.objects.get(pk=pk)
        except Experiences.DoesNotExist:
            raise NotFound("Can't find Exp")
    
    def get(self,request,pk):
        try:
            page = request.query_params.get('page')
            page = int(page)
        except (TypeError,ValueError):
            page = 1
        page_size= settings.PAGE_SIZE
        start = (page-1)*page_size
        end = start + page_size

        exp = self.get_object(pk)
        perks = exp.perks.all()[start:end]

        return Response(
            PerkSerializer(
            perks,
            many=True,
            ).data
        )
    
class ExperienceBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self,pk):
        try:
            return Experiences.objects.get(pk=pk)
        except Experiences.DoesNotExist:
            raise NotFound
    
    def get(self,request,pk):
        # try:
        #     page = request.query_params.get('page')
        #     page= int(page)
        # except(ValueError,TypeError):
        #     page =1
        # start = (page-1)*settings.PAGE_SIZE
        # end = start + settings.PAGE_SIZE
        now_time = timezone.localtime(timezone.now()).date()
        exp = self.get_object(pk)
       
        bookings = bk_models.Booking.objects.filter(
            experience = exp,
            kind = bk_models.Booking.BookingKindChoices.Experience,
            experience_time__gt = now_time
        )

        return Response(
            bk_serializers.PublicBookingSerializer(
                bookings,
                many=True,
            ).data
        )

    def post(self,request,pk):
        exp = self.get_object(pk)
        serializer= bk_serializers.CreateExperienceBookingSerializer(data = request.data)
        if serializer.is_valid():
            booking = serializer.save(
                experience = exp,
                user= request.user,
                kind = bk_models.Booking.BookingKindChoices.Experience,
            )
            serializer= bk_serializers.CreateExperienceBookingSerializer(booking)
            return Response(
                serializer.data
            )
        else:
            return Response(
                serializer.errors
            )
        

class ExperienceBookingDetail(APIView):

    permission_classes = [IsAuthenticated]
   
    def get_object(self,pk,booking_pk):
        try:
            exp = Experiences.objects.get(pk=pk)
            booking = exp.bookings.get(pk = booking_pk)
            return booking
        except:
            raise NotFound

    def get(self,request,pk,booking_pk):
        booking = self.get_object(pk,booking_pk)
        
        serializer= bk_serializers.PublicBookingSerializer(booking)
        return Response(
            serializer.data
        )
    def put(self,request,pk,booking_pk):
        booking = self.get_object(pk,booking_pk)
        if request.user != booking.user:
            raise PermissionDenied
        serializer = bk_serializers.CreateExperienceBookingSerializer(
            booking,
            data= request.data,
            partial=True
        )
        if serializer.is_valid():
            booking = serializer.save()
            serializer= bk_serializers.PublicBookingSerializer(booking)
            return Response(
                serializer.data
            )
        else:
            return Response(
                serializer.errors
            )


    def delete(self,request,pk,booking_pk):
        booking = self.get_object(pk,booking_pk)
        if request.user != booking.user:
            raise PermissionDenied
        booking.delete()
        return Response(
            HTTP_202_ACCEPTED
        )
        
