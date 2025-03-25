from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from authorization.models import User
from mainpage.models import Schedule, ClassTeacher


from django.shortcuts import get_object_or_404

@login_required(login_url='login')
def schedule(request, teacher_id=None):
    user = request.user
    role = user.role

    # Дни недели в нужном порядке (Пн-Сб)
    week_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    week_days_display = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

    schedule_data = []

    if role == 'teacher':
        teacher = user
    elif teacher_id:
        # Получаем пользователя-учителя по ID
        teacher = get_object_or_404(User, id=teacher_id, role='teacher')
    elif role == 'pupil':
        class_field = user.class_name
        if not class_field:
            return render(request, 'no_info.html', {'message': "Класс не найден"})

        # Получаем расписание для класса
        schedule_entries = Schedule.objects.filter(class_field=class_field)

        for lesson_number in range(1, 8):
            row = {"lesson_number": lesson_number, "lessons": []}
            for day in week_days:
                entry = schedule_entries.filter(day=day).first()
                if entry:
                    subject_name = getattr(entry, f'lesson_{lesson_number}', '')
                    # Определяем учителя для предмета
                    teacher_entry = ClassTeacher.objects.filter(class_name=class_field, subject__name=subject_name).first()
                    teacher_name = teacher_entry.teacher.get_full_name_with_initials() if teacher_entry else ''
                    lesson_display = f"{subject_name} <br> <small>{teacher_name}</small>" if subject_name else '-'
                else:
                    lesson_display = '-'
                row["lessons"].append(lesson_display)
            schedule_data.append(row)

        return render(request, 'schedule.html', {
            'week_days_display': week_days_display,
            'schedule_data': schedule_data,
        })

    else:
        return render(request, 'no_info.html', {'message': "Выберите учителя для просмотра расписания."})

    # Для учителя или через ID
    teacher_classes = ClassTeacher.objects.filter(teacher=teacher)
    schedule_entries = Schedule.objects.filter(class_field__in=teacher_classes.values("class_name"))

    for lesson_number in range(1, 8):
        row = {"lesson_number": lesson_number, "lessons": []}
        for day in week_days:
            lessons_for_day = []
            entries = schedule_entries.filter(day=day)
            for entry in entries:
                subject = getattr(entry, f'lesson_{lesson_number}', None)
                if subject:
                    class_number = entry.class_field.number
                    lessons_for_day.append(f"{subject} <br> {class_number} класс")
            row["lessons"].append(", ".join(lessons_for_day) if lessons_for_day else "-")
        schedule_data.append(row)

    return render(request, 'schedule.html', {
        'week_days_display': week_days_display,
        'schedule_data': schedule_data,
        'teacher_name': teacher.get_full_name_with_initials()
    })



def schedule_list(request):
    teachers = User.objects.filter(role='teacher')
    return render(request, 'navigation_classes/schedule_list.html', {'teachers': teachers})

