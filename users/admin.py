from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 개개인 별 관리 시
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "profile_photo",
                    "username",
                    "password",
                    "name",
                    "email",
                    "is_host",
                    "gender",
                    "language",
                    "currency",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "important Dates",
            {"fields": ("last_login", "date_joined")},
        ),
    )

    # 여러명을 볼때 볼 항목들
    list_display = (
        "username",
        "email",
        "name",
        "is_host",
    )
