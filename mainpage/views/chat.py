from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from mainpage.models import PrivateMessage
from authorization.models import User
from django.db import models
import time
from django.utils.dateparse import parse_datetime


@login_required
def private_chat(request, student_id):
    student = get_object_or_404(User, id=student_id, role='pupil')

    # Получаем входящие и исходящие сообщения
    messages_in = PrivateMessage.objects.filter(
        sender=student,
        receiver=request.user
    ).annotate(direction=models.Value('in', output_field=models.CharField()))

    messages_out = PrivateMessage.objects.filter(
        sender=request.user,
        receiver=student
    ).annotate(direction=models.Value('out', output_field=models.CharField()))

    # Объединяем и сортируем сообщения по времени
    messages = sorted(
        list(messages_in) + list(messages_out),
        key=lambda msg: msg.timestamp
    )



    return render(request, 'journals/chat.html', {
        'student': student,
        'student_id': student_id,
        'messages': messages,
    })

@login_required
def send_private_message(request, receiver_id):
    if request.method == "POST":
        receiver = get_object_or_404(User, id=receiver_id)
        message_text = request.POST.get('message')
        if message_text:
            PrivateMessage.objects.create(
                sender=request.user,
                receiver=receiver,
                message=message_text
            )
            return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'fail'})


@login_required
def get_private_messages(request, student_id):
    """Получение новых сообщений (Long Polling)"""
    last_timestamp = request.GET.get('last_timestamp')
    timeout = 30
    start_time = time.time()

    while time.time() - start_time < timeout:
        messages_query = PrivateMessage.objects.filter(
            models.Q(sender=request.user, receiver_id=student_id) |
            models.Q(sender_id=student_id, receiver=request.user)
        ).order_by('timestamp')

        # Фильтрация сообщений по timestamp
        if last_timestamp:
            parsed_timestamp = parse_datetime(last_timestamp)
            if parsed_timestamp:
                messages_query = messages_query.filter(timestamp__gt=parsed_timestamp)

        if messages_query.exists():
            data = [{
                'user': msg.sender.get_full_name_with_initials(),
                'message': msg.message,
                'timestamp': msg.timestamp.isoformat(),
                'direction': 'in' if msg.sender_id == student_id else 'out'
            } for msg in messages_query]

            return JsonResponse({'messages': data})

        time.sleep(1)

    return JsonResponse({'messages': []})


