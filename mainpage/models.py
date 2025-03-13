from django.db import models
from django.conf import settings
from datetime import date

from django.forms import ImageField
from django.utils import timezone


class Class(models.Model):
    number = models.PositiveSmallIntegerField(unique=True, default=1)  # Номер класса (1-11)

    def __str__(self):
        return f"{self.number} класс"  # Строковое представление для админки и вывода

    class Meta:
        ordering = ['number']  # Упорядочивание по возрастанию номера

class Subject(models.Model):
    """ Школьный предмет (Математика, Физика и т.д.) """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.name}'

class ClassTeacher(models.Model):
    """ Промежуточная таблица: учитель -> класс -> предмет """
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                limit_choices_to={'role': 'teacher'})

    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='teacher_subject')  # Учитель ведет конкретный предмет в классе

    def __str__(self):
        return f"{self.teacher} - {self.class_name} ({self.subject})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['class_name', 'subject'], name='unique_class_subject')
        ]
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
    lesson_1 = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name="lesson_1")
    lesson_2 = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name="lesson_2")
    lesson_3 = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name="lesson_3")
    lesson_4 = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name="lesson_4")
    lesson_5 = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name="lesson_5")
    lesson_6 = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name="lesson_6")
    lesson_7 = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name="lesson_7")


    def __str__(self):
        return f"{self.class_field} - {self.day}"
class SubjectPlanCreator(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                limit_choices_to={'role__in': ['teacher', 'deputy director', 'director']})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    plan = models.TextField(blank=True)

    def __str__(self):
        return f'Учебный план {self.subject} - {self.creator} ({self.class_name})'
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['class_name', 'subject'], name='unique_plan_subject')
        ]

class Mark(models.Model):
    """ Таблица для хранения оценок """
    MARK_CHOICES = [
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    TYPE_CHOICES = [
        ('HW', 'Домашнее задание'),
        ('ClW', 'Классная работа'),
        ('SW', 'Самостоятельная работа'),
        ('CW', 'Контрольная работа')
    ]

    mark = models.PositiveSmallIntegerField(choices=MARK_CHOICES)  # Оценка
    date = models.DateField(default=date.today)  # Дата выставления оценки
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)  # Тип работы

    pupil = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'pupil'},
        related_name="marks_pupil"
    )

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},
        related_name="marks_teacher"
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="marks_subject"
    )

    class_field = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name="marks_class"
    )

    def __str__(self):

        return f"{self.pupil.first_name} {self.pupil.last_name} - {self.subject.name}: {self.mark} ({self.type})"

    class Meta:
        ordering = ['date']



class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             limit_choices_to={'role__in': ['teacher', 'deputy director', 'director']})
    url = models.ImageField(upload_to='articles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_short_text(self):
        if len(self.text) > 300:
            return f'{self.text[:300]}...'
        else:
            return self.text


class Quarter(models.Model):
    QUARTER_CHOICES = [
        (1, "1 четверть"),
        (2, "2 четверть"),
        (3, "3 четверть"),
        (4, "4 четверть"),
    ]

    name = models.PositiveSmallIntegerField(choices=QUARTER_CHOICES)  # Выбор номера четверти
    begin = models.DateField()  # Дата начала
    end = models.DateField()  # Дата окончания
    year = models.PositiveSmallIntegerField()  # Учебный год

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(begin__lt=models.F('end')), name='begin_before_end'),
        ]
        ordering = ["year", "name"]  # Сортировка по году и номеру четверти

    def __str__(self):
        return f"{dict(self.QUARTER_CHOICES).get(self.name, 'Неизвестно')} ({self.begin} - {self.end}, {self.year})"



class Event(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateField(default=date.today)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                limit_choices_to={'role__in': ['teacher', 'deputy director', 'director']})
    def get_short_text(self):
        if len(self.text) > 300:
            return f'{self.text[:300]}...'
        else:
            return self.text
    def get_creator(self):
        if self.user:
            return self.user.get_full_name_with_initials()
        return ''

class Event_images(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='images'
    )
    img = models.ImageField(upload_to='events/')


class PrivateMessage(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_messages',
        on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.message[:20]}"