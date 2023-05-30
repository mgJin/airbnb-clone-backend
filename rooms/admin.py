from django.contrib import admin
from .models import Room, Amenity

#관리자 페이지의 행동 정하기  액션은 3개의 arg를 가진다
#decription은 설명
@admin.action(description="Set all prices to zero")
def reset_prices(model_admin,request,rooms): 
    #첫 parameter : 이 액션을 호출하는 클래스
    #2번째 parameter : request =>누가 호출했는지에 대한 정보
    #3번째 parameter : queryset(내가 선택한 객체를 준다)
    for room in rooms:
        room.price = 0
        room.save()
    


#Room class 의 admin 이 될 거다
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    
    #class 에서 내가 행할 동작 지정
    actions = (reset_prices,)

    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities",
        "rating",
        "owner",
        "created_at",
        
        
    )

    list_filter =(
        "country",
        "city",
        "pet_freindly",
        "kind",
        "amenities",
        "bookings__kind",
    )

    search_fields = (
        "owner__username",
    )
    #self는 관리자를 뜻하기 때문에 room을 넣어준다(Django가 알아서 각각에 맞게
    # 넣어주는 듯) 두번째 메서드는 클래스를 의미하는듯?
    def total_amenities(self,room):
        return room.price
    
@admin.register(Amenity)
class Amenity(admin.ModelAdmin):
    list_display=(
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    
    readonly_fields=(
        "created_at",
        "updated_at",
    )
    list_filter=(
        "created_at",
        "updated_at",
    )
