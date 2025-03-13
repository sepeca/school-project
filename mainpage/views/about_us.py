from django.shortcuts import render
from authorization.models import User


def about_us(request):
    # Получаем всех учителей
    teachers = User.objects.filter(role='teacher')
    # Получаем всех заместителей директоров
    deputy_directors = User.objects.filter(role='deputy director')

    # Получаем директора
    director = User.objects.filter(role='director').first()

    teacher_data = [
        {
            "last_name": teacher.last_name,
            "first_name": teacher.first_name,
            "third_name": teacher.third_name,
            "telephone": teacher.tel if teacher.tel else '',
            "about_me": teacher.about_me if teacher.about_me else '',
            "avatar": teacher.avatar.url if teacher.avatar else '',
            "email": teacher.email,
            "role": teacher.get_role_display()
        }
        for teacher in teachers
    ]
    # Создаем список заместителей с их данными
    deputies_data = [
        {
            "last_name": deputy.last_name,
            "first_name": deputy.first_name,
            "third_name": deputy.third_name,
            "telephone": deputy.tel if deputy.tel else '',
            "about_me": deputy.about_me if deputy.about_me else '',
            "avatar": deputy.avatar.url if deputy.avatar else '',
            "email": deputy.email,
            "role": deputy.get_role_display()
        }
        for deputy in deputy_directors
    ]

    # Данные директора (если он найден)
    director_data = {
        "last_name": director.last_name if director else "",
        "first_name": director.first_name if director else "",
        "third_name": director.third_name if director else "",
        "telephone": director.tel if director and director.tel else "",
        "about_me": director.about_me if director.about_me else '',
        "avatar": director.avatar.url if director.avatar else '',
        "email": director.email,
        "role": director.get_role_display()
    }

    return render(request, "public_info/about_us.html", {
        "teachers": teacher_data,
        "deputies": deputies_data,
        "director": director_data,
    })
