from django.db import models
from common.models import CommonModel

#채팅방
class ChattingRoom(CommonModel):

    """ChattingRoom model Definition"""

    users = models.ManyToManyField(
        "users.User",
        related_name="chattingrooms",

    )
    def __str__(self) -> str:
        return "Chatting Room. (100)"

class Message(CommonModel):

   """Message model Definition""" 

   text= models.TextField()
   #유저를 지워도 남는다.
   user = models.ForeignKey(
       "users.User",
       null = True,
       blank =True,
       on_delete= models.SET_NULL,
       related_name="messages",

   )
   #채팅방이 사라진다면 메시지도 사라져야함
   room = models.ForeignKey(
       "direct_messages.ChattingRoom",
       on_delete=models.CASCADE,
       related_name="messages",

   )

   def __str__(self) -> str:
       return f"{self.user} says : {self.text}"

