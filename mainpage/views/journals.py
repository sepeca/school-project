from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from authorization.models import User
from mainpage.models import Mark, Class, Subject, Quarter

from django.shortcuts import render, get_object_or_404
import locale

# Устанавливаем русскую локаль для сокращений дней недели
locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")


@login_required(login_url='/lk/login/')
def class_journal(request, subject_id, class_id):
    """Журнал оценок для выбранного предмета и класса"""

    class_obj = get_object_or_404(Class, id=class_id)
    subject_obj = get_object_or_404(Subject, id=subject_id)

    students = User.objects.filter(class_name=class_obj, role='pupil').order_by('last_name')
    marks = Mark.objects.filter(class_field=class_obj, subject=subject_obj).order_by('date')

    # Определяем текущую дату и корректируем, если сегодня воскресенье
    today = date.today()
    if today.weekday() == 6:  # Если воскресенье, берем субботу
        today -= timedelta(days=1)

    # Определяем текущую четверть
    current_quarter = Quarter.objects.filter(begin__lte=today, end__gte=today).first()

    # Получаем номер четверти из GET-запроса или берем текущую четверть
    selected_quarter_id = request.GET.get("quarter", current_quarter.name if current_quarter else 1)

    # Фильтруем даты по выбранной четверти
    quarter_obj = Quarter.objects.filter(name=selected_quarter_id).first()
    lesson_dates = []

    if quarter_obj:
        current_date = quarter_obj.begin
        while current_date <= min(quarter_obj.end, today):  # Ограничиваем будущие даты
            if current_date.weekday() != 6:  # Исключаем воскресенье
                lesson_dates.append(current_date)
            current_date += timedelta(days=1)

    # Создаем структуру оценок
    grades_dict = {
        student.id: {
            lesson_date: {'mark': None, 'type': None}
            for lesson_date in lesson_dates
        }
        for student in students
    }

    for mark in marks.filter(date__range=(quarter_obj.begin, quarter_obj.end)):
        if mark.date in lesson_dates:
            grades_dict[mark.pupil.id][mark.date] = {'mark': mark.mark if mark.mark is not None else 0, 'type': mark.type}

    if request.method == "POST":
        selected_type = request.POST.get("selected_type")  # Получаем выбранный тип работы

        if not selected_type:
            return redirect(request.path)  # Если не выбран тип работы, не сохраняем

        for student in students:
            for lesson_date in lesson_dates:
                lesson_date_str = lesson_date.strftime('%Y-%m-%d')  # Преобразуем в строку
                mark_key = f"mark_{student.id}_{lesson_date_str}"
                mark_value = request.POST.get(mark_key)

                if mark_value and mark_value.isdigit():
                    mark_value = int(mark_value)  # Приводим к int
                    old_mark = grades_dict[student.id][lesson_date]['mark']

                    if old_mark != mark_value:  # ✅ Обновляем только если оценка изменилась
                        Mark.objects.update_or_create(
                            pupil=student,
                            teacher=request.user,
                            subject=subject_obj,
                            class_field=class_obj,
                            date=lesson_date,
                            defaults={"mark": mark_value, "type": selected_type}
                        )

        return redirect(request.path)

    return render(request, 'journal.html', {
        'class_obj': class_obj,
        'subject_obj': subject_obj,
        'students': students,
        'lesson_dates': lesson_dates,  # Отображаем все даты до сегодняшнего дня
        'grades_dict': grades_dict,
        'type_choices': Mark.TYPE_CHOICES,
        'mark_choices': Mark.MARK_CHOICES,
        'quarters': Quarter.objects.all(),
        'selected_quarter_id': int(selected_quarter_id),
        'today': today,  # Передаем текущую дату в шаблон
    })



@login_required(login_url='/lk/login/')
def my_journal(request, class_id):
    """Журнал оценок для ученика по всем предметам в выбранной четверти"""

    # Проверяем, что пользователь — ученик
    if request.user.role != 'pupil':
        return render(request, 'no_info.html', {'message': 'Доступ запрещен'})

    # Получаем объект класса
    class_obj = get_object_or_404(Class, id=class_id)

    # Получаем все оценки ученика
    marks = Mark.objects.filter(class_field=class_obj, pupil=request.user).order_by('date')

    # Получаем список всех предметов, по которым есть оценки
    subjects = Subject.objects.filter(marks_subject__pupil=request.user).distinct()

    # Определяем текущую дату
    today = date.today()
    if today.weekday() == 6:  # Если воскресенье, то берем субботу
        today -= timedelta(days=1)

    # Определяем текущую четверть
    current_quarter = Quarter.objects.filter(begin__lte=today, end__gte=today).first()

    # Получаем выбранную четверть (из GET-запроса или используем текущую)
    selected_quarter_id = request.GET.get("quarter", current_quarter.name if current_quarter else 1)

    # Фильтруем четверти
    quarter_obj = Quarter.objects.filter(name=selected_quarter_id).first()

    # Создаем список всех дат текущей четверти, исключая воскресенья, но **не выходя за сегодняшний день**
    lesson_dates = []
    if quarter_obj:
        current_date = quarter_obj.begin
        while current_date <= min(quarter_obj.end, today):  # Ограничиваем будущие даты
            if current_date.weekday() != 6:  # Исключаем воскресенье
                lesson_dates.append(current_date)
            current_date += timedelta(days=1)

    # Структура {subject_id: {date: оценка}}
    grades_dict = {subject.id:
                       {lesson_date: {"mark": None, "type": None} for lesson_date in lesson_dates}
                   for subject in subjects}

    # Заполняем оценки только за выбранную четверть
    for mark in marks.filter(date__range=(quarter_obj.begin, quarter_obj.end)):
        grades_dict[mark.subject.id][mark.date] = {
            'mark': mark.mark,
            'type': mark.type
        }

    return render(request, 'my_journal.html', {
        'class_obj': class_obj,
        'subjects': subjects,
        'lesson_dates': lesson_dates,  # Все даты четверти до сегодняшнего дня включительно
        'grades_dict': grades_dict,
        'quarters': Quarter.objects.all(),
        'selected_quarter_id': int(selected_quarter_id),
    })
