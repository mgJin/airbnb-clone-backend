from django.db import models


"""다른 앱들에서 공통적으로 쓰일 것들"""
#이것은 데이터베이스로 가지 않을 것이다. 왜냐? 추상클래스니께

class CommonModel(models.Model):
    
    """Common model Definition"""

     #방 생성 날짜 
    # property)
    # 1)auto_now_add : 필드의 값을 해당 object가 처음 생성 되었을 때 시간으로 설정
    created_at = models.DateTimeField(auto_now_add=True,)
    #방 업데이트 날짜
    #property)
    #1)auto_now : object가 저장될 때마다 해당 필드를 현재 date로 설정
    updated_at = models.DateTimeField(auto_now=True)

    #Django에서 model을 configure 할 때 사용
    #abstract = True 로 해놓으면 Django가 이 model을 봐도 DB에 저장안함
    #DB에서 실제 데이터로 사용되지 않을 것이다.
    class Meta:
        abstract = True
    
