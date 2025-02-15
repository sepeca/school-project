from django.contrib import admin
from mainpage.models import Article, Class, Schedule, Student, Journal, Lesson

#регистрация для того, чтобы в админке можно было что-то изменить
admin.site.register(Article)
admin.site.register(Class)
admin.site.register(Schedule)
admin.site.register(Student)
admin.site.register(Journal)
admin.site.register(Lesson)