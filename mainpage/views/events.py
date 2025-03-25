from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render, redirect

from mainpage.forms import PublishEventForm, EventImageForm
from mainpage.models import Event, Event_images


def events(request):
    # Оптимизация запросов: получаем события и связанные с ними изображения
    events = Event.objects.prefetch_related('images')

    context = {
        'events': events
    }
    return render(request, 'events/events.html', context)

def show_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)  # Получаем статью или 404 ошибку
    return render(request, 'events/event.html', {'event': event})


@login_required(login_url='/lk/login/')
def publish_event(request):
    if request.user.role == 'pupil':
        return render(request, 'no_info.html',
                      {'message': 'У вас нет прав публиковать отчеты по мероприятиям'})

    form = PublishEventForm()

    if request.method == "POST":
        form = PublishEventForm(request.POST)
        image_form = EventImageForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()

            uploaded_images = request.FILES.getlist('images')
            for img in uploaded_images:
                Event_images.objects.create(event=event, img=img)

            return redirect('events')

    else:
        form = PublishEventForm()
        image_form = EventImageForm()

    return render(request, 'events/publish_event.html', {
        'form': form,
        'image_form': image_form
    })