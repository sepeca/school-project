from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect

from authorization.forms import LoginForm
from mainpage.models import Article, ClassTeacher
from django.contrib.auth.decorators import login_required


def do_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/lk/login/')
def profile(request):
    user = request.user


    first_name = user.first_name
    last_name = user.last_name
    third_name = user.third_name
    user_role = user.role
    email = user.email
    tel = user.tel if user.tel else "Не указан"
    birthday = user.birthdate.strftime("%d.%m.%Y") if user.birthdate else "Не указана"  # Форматирование даты

    if user_role == 'pupil':
        class_name = f"Учится в: {user.class_name}е" if user.class_name else "Учится в: Не определен"
    else:
        # Если учитель, находим классы, где он преподаёт (убираем дубликаты)
        class_teaching = set(ClassTeacher.objects.filter(teacher=user).values_list("class_name__number", flat=True))

        if class_teaching:
            sorted_classes = sorted(class_teaching)  # Сортируем классы по номеру
            class_name = f"Преподает в: {', '.join(str(cls) for cls in sorted_classes)} класс(е/ах)"
        else:
            class_name = "Преподает в: Нет закрепленных классов"

    return render(request, 'lk.html', {
        'full_name': f"{last_name} {first_name} {third_name}",
        'user': user,
        'email': email,
        'class_info': class_name,
        'tel': tel,
        'birthday': birthday,
    })


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('profile')  # Если уже авторизован, перенаправляем на профиль

    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')  # Редирект после успешного входа
            else:
                form.add_error(None, 'Неверный email или пароль!')

    return render(request, 'login.html', {'form': form})
