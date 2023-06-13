from django.utils import timezone
from rest_framework.serializers import ModelSerializer,DateField,ValidationError
from .models import Booking

class CreateRoomBookingSerializer(ModelSerializer):
    
    check_in = DateField()
    check_out = DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self,value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise ValidationError("Can't book, go future")
        return value
    
    def validate_check_out(self,value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise ValidationError("Can't book, go future")
        return value

class PublicBookingSerializer(ModelSerializer):

    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )