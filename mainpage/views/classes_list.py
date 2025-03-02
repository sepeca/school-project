from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from mainpage.models import ClassTeacher


@login_required(login_url='/lk/login/')
def classes_list(request):
    page_type = request.GET.get('type')

    if request.user.role == 'pupil' and page_type == 'grades':
        class_id = request.user.class_name.id
        return redirect(f'/my-journal/{class_id}/')
    if request.user.role == 'teacher':
        teacher_classes = ClassTeacher.objects.filter(teacher=request.user).select_related('class_name', 'subject')
    elif request.user.role == 'pupil':
        message = 'У Вас недостаточно прав для просмотра'
        return render(request, 'no_info.html', {'message': message})
    else:
        teacher_classes = ClassTeacher.objects.all().select_related('class_name', 'subject')

    # Получаем GET-параметр type (какая кнопка была нажата)

    if page_type == 'grades' and teacher_classes:
        title = 'Журналы классов'
        url_name = 'class_journal'

    elif page_type == 'plans' and teacher_classes:
        title = 'Учебные планы'
        url_name = 'study_plan'

    else:
        message = 'У Вас нет своих классов'
        return render(request, 'no_info.html', {'message': message})

    subject_classes_map = {}

    for entry in teacher_classes:
        subject_id = entry.subject.id  # Получаем ID предмета
        subject_name = entry.subject.name  # Получаем название предмета

        # Если предмета еще нет в словаре, создаем запись
        if subject_id not in subject_classes_map:
            subject_classes_map[subject_id] = {
                "name": subject_name,  # Сохраняем название предмета
                "classes": []  # Создаем список классов
            }

        # Добавляем номер класса в список
        subject_classes_map[subject_id]["classes"].append(entry.class_name.number)

    # Сортируем номера классов от большего к меньшему
    for subject_id in subject_classes_map:
        subject_classes_map[subject_id]["classes"] = sorted(subject_classes_map[subject_id]["classes"], reverse=True)

    return render(request, 'classes_list.html',
                      {'subject_classes_map': subject_classes_map,
                       'title': title,
                       'url_name': url_name})