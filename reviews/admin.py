from typing import Any, List, Optional, Tuple
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Review

class WordFilter(admin.SimpleListFilter):

    title = "Filter by words" #simplefilter에는 title속성이 필요

    parameter_name = "word"

    def lookups(self,request, model_admin): #3가지 parm  1.self, 2.호출한 유저정보 3.이것을 사용할 클래스에 대한 정보
        return [
            ("good","Good"),
            ("great","Great"),
            ("awesome","Awesome"),
        ]

    def queryset(self,request,queryset):
        word = self.value()
        if word:
            
            return queryset.filter(payload__contains=word)
        else:
            queryset

class GoodBadFilter(admin.SimpleListFilter):

    title = "Filter by Rating"

    parameter_name = "score"

    def lookups(self,request,model_admin):
        return [
            (3,"good"),
            (2,"bad"),
        ]
    
    def queryset(self,request,reviews):
        score = self.value()
        if score:
            if int(score)>=3:
                return reviews.filter(rating__gte=score)
            else:
                return reviews.filter(rating__lte=score)
        else:
            return reviews
            

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    
    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (
        WordFilter,
        GoodBadFilter,
        "rating",
        
    )