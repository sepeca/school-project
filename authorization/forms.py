from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.forms import PasswordInput, ModelForm
from django.core.validators import validate_email
from urllib3 import request

from mainpage.models import Article


# форма авторизации
class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label="email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Введите вашу почту"})
    )
    password = forms.CharField(
        required=True,
        label="password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль"})
    )

    def clean(self):
        """ Проверяем, существует ли пользователь и верен ли пароль """
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise ValidationError("Неверный email или пароль.")
        return cleaned_data

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User

class CustomUserCreationForm(forms.ModelForm):
    """Форма создания пользователя в админке"""
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "third_name", "role")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Хэшируем пароль
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    """Форма редактирования пользователя в админке"""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "third_name", "role", "password", "is_active", "is_staff")

    def clean_password(self):
        """Возвращает пароль в неизменном виде, чтобы Django не требовал его обновления"""
        return self.initial["password"]
