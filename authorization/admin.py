from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(BaseUserAdmin):
    """Кастомная админка для модели пользователя"""
    form = CustomUserChangeForm  # Форма редактирования
    add_form = CustomUserCreationForm  # Форма создания

    list_display = ("email", "first_name", "last_name", "role", "is_staff")
    list_filter = ("role", "last_name", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Личная информация", {"fields": ("first_name", "last_name", "third_name", "role","birthdate","tel","class_name", "avatar","about_me",)}),
        ("Разрешения", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "third_name",
                       "role", "birthdate", "tel","avatar","about_me", "password1", "password2"),
        }),
        ("Учится в:", {'fields': ("class_name",)})
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    filter_horizontal = ()


# Регистрируем кастомную модель в админке
admin.site.register(User, CustomUserAdmin)
