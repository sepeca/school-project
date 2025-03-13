from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from mainpage.forms import PublishPlan
from mainpage.models import SubjectPlanCreator, Subject, Class


@login_required(login_url='/lk/login/')
def study_plan(request, subject_id, class_id):
    if request.user.role == 'pupil':
        return redirect('/news/')

    try:
        # Ищем учебный план по subject_id и class_id
        plan = (SubjectPlanCreator.objects.get(subject_id=subject_id, class_name_id=class_id))

        return render(request, 'study_plans/study_plan.html', {
            'subject_name': plan.subject.name,
            'class_name': plan.class_name.number,
            'plan': plan.plan,
            'last_name': plan.creator.last_name if plan.creator else "Неизвестный",
            'first_name': plan.creator.first_name if plan.creator else "",
            'third_name': plan.creator.third_name if plan.creator and plan.creator.third_name else "",
            'role': plan.creator.role if plan.creator else "Неизвестно"
        })

    except SubjectPlanCreator.DoesNotExist:
        # Если план не найден, показываем сообщение
        message = 'У предмета этого класса не записан учебный план в систему'
        redirect_button = (f'/publish_plan/{subject_id}/{class_id}')
        redirect_message = 'Создать план'
        return render(request, 'no_info.html', {
            'message': message,
            'redirect_button': redirect_button,
            'redirect_message': redirect_message
        })

@login_required(login_url='/lk/login/')
def publish_plan(request, subject_id, class_id):
    if request.user.role == 'pupil':
        return redirect('/news/')

    subject = get_object_or_404(Subject, id=subject_id)
    class_name = get_object_or_404(Class, id=class_id)

    # Проверяем, есть ли уже учебный план для этого предмета и класса
    plan_instance = SubjectPlanCreator.objects.filter(subject=subject, class_name=class_name).first()
    if plan_instance is not None:
        return redirect(f'/study_plan/{subject_id}/{class_id}')

    if request.method == "POST":
        form = PublishPlan(request.POST, user=request.user, subject=subject.id, class_name=class_name.id, instance=plan_instance)
        if form.is_valid():
            form.save()
            return redirect(f'/study_plan/{subject_id}/{class_id}')  # Перенаправление на страницу с учебным планом
    else:
        form = PublishPlan(user=request.user, subject=subject.id, class_name=class_name.id, instance=plan_instance)

    return render(request, 'study_plans/publish_plan.html', {'form': form, 'subject': subject, 'class_name': class_name})
