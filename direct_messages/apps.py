from django.apps import AppConfig


class DirectMessagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "direct_messages"
    #앱의 이름을 바꾸고 싶다면 이렇게(클래스의 이름은 모델에)
    verbose_name = "Direct Messages"

