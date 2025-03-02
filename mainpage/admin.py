from django.contrib import admin
from mainpage.models import Article, Class, Mark, Subject, ClassTeacher, SubjectPlanCreator, Quarter


#регистрация для того, чтобы в админке можно было что-то изменить
admin.site.register(Article)
admin.site.register(Class)
admin.site.register(Mark)
admin.site.register(Subject)
admin.site.register(ClassTeacher)
admin.site.register(SubjectPlanCreator)
admin.site.register(Quarter)