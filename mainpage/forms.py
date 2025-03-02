from django import forms
from django.core.exceptions import ValidationError


from mainpage.models import Article, SubjectPlanCreator


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

    class Meta:
        model = Article
        fields = ['title', 'text']

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
