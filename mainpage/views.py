from django.shortcuts import render, get_object_or_404, redirect
from mainpage. models import Article, Class, Schedule, Student, Journal, Lesson
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json
from itertools import groupby
from django.contrib.auth import authenticate, login, logout
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def journal(request): #ф чтобы все отображалось(классы и предметы)
    if not request.user.is_authenticated:
        return redirect("/")
    classes = Class.objects.all()
    class_ids = [class_obj.id for class_obj in classes]
    #обработка данных
    tmp = []
    d = []
    for i in class_ids:
        tmp.append(Schedule.objects.filter(class_field_id=i).values_list('class_field_id', 'lesson_1', 'lesson_2', 'lesson_3', 'lesson_4', 'lesson_5', 'lesson_6', 'lesson_7').distinct())
    c = 0
    for i in tmp:
        c += 1
        el = []
        temp = int
        for j in i:
            for z in j:
                if z not in el and type(z) is not int:
                    el.append(z)
                elif z not in el and type(z) is int:
                    temp = z
        el.pop(el.index("-"))
        el.sort(key=len)
        el.append(temp)
        d.append(el)
    return render(request, 'journal.html', {'classes': classes, 'unique_subjects': d})


def class_journal(request):
    classes = Class.objects.all()
    class_ids = [class_obj.id for class_obj in classes]
    tmp = []
    d = []
    for i in class_ids:
        tmp.append(Schedule.objects.filter(class_field_id=i).values_list('class_field_id', 'lesson_1', 'lesson_2', 'lesson_3', 'lesson_4', 'lesson_5', 'lesson_6', 'lesson_7').distinct())
    c = 0
    for i in tmp:
        c += 1
        el = []
        temp = int
        for j in i:
            for z in j:
                if z not in el and type(z) is not int:
                    el.append(z)
                elif z not in el and type(z) is int:
                    temp = z
        el.pop(el.index("-"))
        el.sort(key=len)
        el.append(temp)
        d.append(el)
    id = request.GET.get('class_id')
    dates = list(Lesson.objects.all().values_list('date'))
    st = list(Student.objects.filter(class_name_id=id).values_list('first_name', 'id', 'last_name'))
    if request.method == "POST":
        save_data = []
        for i in range(len(list(st))):
            student_data = {}
            for j in range(len(dates)):
                student_data[f'{list(st)[i][1]}-{dates[j][0]}'] = request.POST.get(f"{list(st)[i][1]}-{dates[j][0]}")
            save_data.append(student_data)
        for i in save_data:
            keys = list(i.keys())
            for j in range(len(i)):
                if i[keys[j]] != '':
                    grades, created = Journal.objects.update_or_create(student_id=keys[j][:keys[j].index("-")], lesson_date=keys[j][keys[j].index("-")+1:], subject=request.GET.get('subject_name'),
                                                   defaults={"grade": i[keys[j]]})
    gds = list()
    for i in list(st):
        qwe = list(Journal.objects.filter(student_id=i[1], subject=request.GET.get('subject_name')).values_list('lesson_date', 'student_id','grade').order_by('lesson_date'))
        if qwe:
            gds.append(qwe)

    for data in dates:
        c = 0
        for j in gds:
            for i in range(len(j)):
                if data[0] == j[i][0]:
                    c += 1
            if c == 0:
                j.append((data[0], j[0][1], 0))
    if gds:
        return render(request, 'ready_journal.html', {'classes': classes, 'unique_subjects': d, 'dates': dates, 'students': st, 'grades': gds})
    else:
        return render(request, 'ready_journal.html', {'classes': classes, 'unique_subjects': d, 'dates': dates, 'students': st, 'grades': 1})


def schedule(request):
    if not request.user.is_authenticated:
        return redirect("/")
    classes = Class.objects.all()
    sched = Schedule.objects.all()
    return render(request, 'schedule.html', {'classes': classes, 'schedule': sched})


def news(request):
    article = Article.objects.all()
    context = {
        'articles': article
    }
    return render(request, 'news.html', context)


def show_article(request, article_id):
    article = get_object_or_404(Article, id=article_id) #Получаем статью или 404 ошибку
    return render(request, 'article.html', {'article': article})


def formivent(request):
    if request.method == "POST":
        sender_email = "g88005553535g@bk.ru"
        receiver_email = f"{request.POST.get('email')}"
        name = request.POST.get('first_name') + ' ' + request.POST.get('last_name')
        password = "LMtvnHXnpZ02Ajt6PLUc"
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = "Ваша заявка на участие в конкурс принята в обработку"
        body = f"Здравствуйте, {name}. Ваша заявка на участие в конкурсе была принята. Ожидайте обратной связи."
        message.attach(MIMEText(body, 'plain'))
        # Подключение к серверу Gmail
        server = smtplib.SMTP('smtp.mail.ru', 587)
        server.starttls()
        # Авторизация
        server.login(sender_email, password)
        # Отправка письма
        server.send_message(message)
        # Закрытие подключения
        server.quit()
        return render(request, 'completed.html')
    return render(request, 'Iventform.html')


def add_lesson_date(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        lesson = Lesson(date=date)
        lesson.save()  # Сохранение даты урока в базе данных

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})

