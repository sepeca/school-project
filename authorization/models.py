
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from mainpage.models import Class


class CustomUserManager(BaseUserManager):
    def create_user(self,email, first_name, last_name, third_name, role, password=None):

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            third_name=third_name,
            role=role,
        )
        if password:
            user.set_password(password)
        else:
            raise ValueError("Users must have a password")

        user.save(using=self._db)
        return user

    def create_superuser(self,email, first_name, last_name, third_name, role, password=None):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            third_name=third_name,
            role=role,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('pupil', "Ученик"),
        ('teacher', "Учитель"),
        ('deputy director', "Завуч"),
        ('director', "Директор"),
    )
    email = models.EmailField(unique=True, null=False)  # Уникальный email
    # 5 первых букв фамилии + 2 первые буквы имени + 1, 2, 3 и тд при повторениях


    first_name = models.CharField(max_length=50, null=False) #Имя
    last_name = models.CharField(max_length=50, null=False) #фамилия
    third_name = models.CharField(max_length=50, null=True,blank=True)# Отчество
    birthdate = models.DateField(null=True, blank=True)
    tel = models.CharField(max_length=15, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)

    class_name = models.ForeignKey(Class, null=True, blank=True, on_delete=models.SET_NULL)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


    is_active = models.BooleanField(default=True)  # Включен ли аккаунт
    is_staff = models.BooleanField(default=False)  # Может ли входить в админку

    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # Поле для входа
    REQUIRED_FIELDS = ["first_name", "last_name","third_name", "role"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

    def get_full_name_with_initials(self):
        initials = ''
        if self.first_name:
            initials += f"{self.first_name[0]}."
        if self.third_name:
            initials += f" {self.third_name[0]}."
        return f"{self.last_name} {initials.strip()}"
