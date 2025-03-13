from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from mainpage.models import Article, SubjectPlanCreator, Schedule, Subject, Event, Event_images


class PublishNewsForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        label='Заголовок',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    text = forms.CharField(
        required=True,
        label='Текст статьи',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )
    url = forms.ImageField(
        required=False,
        label='Изображение',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-url'})
    )

    class Meta:
        model = Article
        fields = ['title', 'text', 'url']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Получаем user из kwargs
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if not self.user:
            raise ValidationError("Пользователь не передан в форму.")

        if self.user.role not in ['teacher', 'deputy director', 'director']:
            raise ValidationError("У вас нет прав для публикации новостей.")

        return cleaned_data

    def save(self, commit=True):
        article = super().save(commit=False)
        article.user = self.user  # Устанавливаем пользователя
        if commit:
            article.save()
        return article


class PublishPlan(forms.ModelForm):
    plan = forms.CharField(
        required=True,
        label='Учебный план',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    class Meta:
        model = SubjectPlanCreator
        fields = ['plan']

    def __init__(self, *args, **kwargs):
        self.subject = kwargs.pop('subject', None)
        self.class_name = kwargs.pop('class_name', None)
        self.creator = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.subject:
            instance.subject_id = self.subject  # Присваиваем subject_id
        if self.class_name:
            instance.class_name_id = self.class_name  # Присваиваем class_name_id
        if self.creator:
            instance.creator = self.creator  # Присваиваем user

        if commit:
            instance.save()
        return instance

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Проверяем, существует ли уже объект расписания (при редактировании)
        class_instance = getattr(self.instance, 'class_field', None)

        if class_instance:  # Если у объекта уже есть класс, фильтруем предметы
            subjects = Subject.objects.filter(teacher_subject__class_name=class_instance).distinct()
        else:
            subjects = Subject.objects.none()  # При создании нового объекта нет доступных предметов

        for lesson in range(1, 8):  # Применяем фильтрацию для каждого урока
            field_name = f'lesson_{lesson}'
            self.fields[field_name].queryset = subjects

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result



class PublishEventForm(forms.ModelForm):
        class Meta:
            model = Event
            fields = ['title', 'text', 'date']

class EventImageForm(forms.ModelForm):
    img = MultipleFileField(label='Select files', required=False)

    class Meta:
        model = Event_images
        fields = ['img', ]


