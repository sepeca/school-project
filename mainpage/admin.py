from django.contrib import admin

from mainpage.forms import ScheduleForm
from mainpage.models import Article, Class, Mark, Subject, ClassTeacher, SubjectPlanCreator, Quarter, Schedule, Event, \
    Event_images, PrivateMessage

#регистрация для того, чтобы в админке можно было что-то изменить
admin.site.register(Article)
admin.site.register(Class)
admin.site.register(Mark)
admin.site.register(Subject)
admin.site.register(ClassTeacher)
admin.site.register(SubjectPlanCreator)
admin.site.register(Quarter)
admin.site.register(Event)
admin.site.register(Event_images)
admin.site.register(PrivateMessage)


class ScheduleAdmin(admin.ModelAdmin):
    form = ScheduleForm
    list_display = ('class_field', 'day')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Фильтруем выбор предметов только для соответствующего класса.
        """
        if db_field.name.startswith('lesson_'):
            class_id = request.GET.get('class_field')
            if class_id:
                kwargs["queryset"] = Subject.objects.filter(teacher_subject__class_name=class_id).distinct()
            else:
                kwargs["queryset"] = Subject.objects.none()  # Чтобы не вызывать ошибку при создании нового объекта

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Schedule, ScheduleAdmin)