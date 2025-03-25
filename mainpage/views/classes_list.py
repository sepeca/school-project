from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from mainpage.models import ClassTeacher


@login_required(login_url='/lk/login/')
def classes_list(request):
    page_type = request.GET.get('type')
    director_factor = False

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
        director_factor = True  # Включаем плитки классов

    if page_type == 'grades' and teacher_classes:
        title = 'Журналы классов'
        url_name = 'class_journal'
    elif page_type == 'plans' and teacher_classes:
        title = 'Учебные планы'
        url_name = 'study_plan'
    else:
        message = 'У Вас нет своих классов'
        return render(request, 'no_info.html', {'message': message})

    # 🔹 Сортировка для директора (классы по возрастанию + предметы по алфавиту)
    if director_factor:
        class_subject_map = {}

        for entry in teacher_classes:
            class_number = entry.class_name.number  # Класс
            subject_id = entry.subject.id  # ID предмета
            subject_name = entry.subject.name  # Название предмета

            if class_number not in class_subject_map:
                class_subject_map[class_number] = []

            class_subject_map[class_number].append({"id": subject_id, "name": subject_name})

        # 1. Сортируем предметы по алфавиту внутри каждого класса
        for class_number in class_subject_map:
            class_subject_map[class_number].sort(key=lambda x: x["name"].lower())

        # 2. Сортируем классы по возрастанию (1, 2, 3, ...)
        class_subject_map = dict(sorted(class_subject_map.items(), key=lambda x: x[0]))

        return render(request, 'navigation_classes/classes_list.html', {
            'class_subject_map': class_subject_map,
            'title': title,
            'url_name': url_name,
            'director_factor': True
        })

    # 🔹 Сортировка для учителя (предметы по алфавиту)
    subject_classes_map = {}

    for entry in teacher_classes:
        subject_id = entry.subject.id
        subject_name = entry.subject.name

        if subject_id not in subject_classes_map:
            subject_classes_map[subject_id] = {
                "name": subject_name,
                "classes": []
            }

        subject_classes_map[subject_id]["classes"].append(entry.class_name.number)

    # 1. Сортируем классы внутри предмета (от большего к меньшему)
    for subject_id in subject_classes_map:
        subject_classes_map[subject_id]["classes"] = sorted(subject_classes_map[subject_id]["classes"], reverse=True)

    # 2. Сортируем предметы по алфавиту
    subject_classes_map = dict(sorted(subject_classes_map.items(), key=lambda x: x[1]['name'].lower()))

    return render(request, 'navigation_classes/classes_list.html', {
        'subject_classes_map': subject_classes_map,
        'title': title,
        'url_name': url_name,
        'director_factor': False
    })

