from django.shortcuts import render
from authorization.models import User

def contacts(request):
    # Получаем всех заместителей директоров
    deputy_directors = User.objects.filter(role='deputy director')

    # Получаем директора (берем первого, если есть)
    director = User.objects.filter(role='director').first()

    # Создаем список заместителей с их данными
    deputies_data = [
        {
            "last_name": deputy.last_name,
            "first_name": deputy.first_name,
            "third_name": deputy.third_name,
            "telephone": deputy.tel if deputy.tel else ''
        }
        for deputy in deputy_directors
    ]

    # Данные директора (если он найден)
    director_data = {
        "last_name": director.last_name if director else "",
        "first_name": director.first_name if director else "",
        "third_name": director.third_name if director else "",
        "telephone": director.tel if director and director.tel else ""
    }

    # Передаем данные в шаблон
    return render(request, 'contacts.html', {
        'deputy_directors': deputies_data,
        'director': director_data
    })