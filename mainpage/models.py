from django.db import models
from django.contrib.auth.models import User


class Lesson(models.Model):
    date = models.CharField(max_length=10)  # Новое поле с правильным форматом даты
    # Другие поля для урока

    def __str__(self):
        return str(self.date)

class Class(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class CustomUser(models.Model):  # Универсальная модель для учеников, учителей и высшего состава
    role_choices = (
        ('pupil', "ученик"),
        ('teacher', "учитель"),
        ('deputy director', "завуч"),
        ('director', "директор")
    )

    role = models.CharField(max_length=20, choices=role_choices)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    third_name = models.CharField(max_length=50)  # Отчество

    # Связь учеников с одним классом
    class_name = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        null=True,  # Чтобы поле было пустым для учителей
        blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_role_display()})"

class ClassTeacher(models.Model):
    """
    Промежуточная таблица для связи учителей и классов.
    Один учитель может преподавать в нескольких классах.
    В одном классе может быть несколько учителей.
    """
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.teacher} -> {self.class_field}"

class Journal(models.Model):
    student_id = models.IntegerField()  # Поле для хранения id студента
    lesson_date = models.CharField(max_length=12)  # Поле для хранения даты занятия
    subject = models.CharField(max_length=100)  # Поле для хранения предмета
    grade = models.PositiveSmallIntegerField(default=0) # Поле для хранения предмета

    def __str__(self):
        return f"{self.student_id} - {self.subject} - {self.lesson_date}"


class Schedule(models.Model):
    day_choices = (
        ('monday', 'Понедельник'),
        ('tuesday', 'Вторник'),
        ('wednesday', 'Среда'),
        ('thursday', 'Четверг'),
        ('friday', 'Пятница'),
        ('saturday', 'Суббота'),
    )

    class_field = models.ForeignKey(Class, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=day_choices)
    lesson_1 = models.CharField(max_length=50)
    lesson_2 = models.CharField(max_length=50)
    lesson_3 = models.CharField(max_length=50)
    lesson_4 = models.CharField(max_length=50)
    lesson_5 = models.CharField(max_length=50)
    lesson_6 = models.CharField(max_length=50)
    lesson_7 = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.class_field} - {self.day}"


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_short_text(self):
        if len(self.text) > 300:
            return self.text[:300]
        else:
            return self.text
