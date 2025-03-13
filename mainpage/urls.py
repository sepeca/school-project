from django.urls import path
from django.views.generic import RedirectView

from mainpage import views



urlpatterns = [
    path('', RedirectView.as_view(url='/news/', permanent=False)),

    path('news/', views.news, name='news'),
    path('article/<int:article_id>/', views.show_article, name='article'),
    path('publish_news/', views.publish_news, name='publish_news'),

    path('events/', views.events, name='events'),
    path('event/<int:event_id>/', views.show_event, name='event'),
    path('publish_event/', views.publish_event, name='publish_event'),

    path('classes-list/', views.classes_list, name='classes_list'),
    path('class-journal/<int:subject_id>/<int:class_id>/', views.class_journal, name='class_journal'),
    path('my-journal/<int:class_id>/', views.my_journal, name='my_journal'),

    path('study_plan/<int:subject_id>/<int:class_id>/', views.study_plan, name='study_plan'),
    path('publish_plan/<int:subject_id>/<int:class_id>/', views.publish_plan, name='publish_plan'),

    path('contacts/', views.contacts, name='contacts'),
    path('about_us/', views.about_us, name='about_us'),

    path('schedule_list/', views.schedule_list, name='schedule_list'),
    path('schedule/', views.schedule, name='schedule'),
    path('schedule/<int:teacher_id>/', views.schedule, name='schedule_by_teacher'),
]
urlpatterns += [
    path('chat/<int:student_id>/', views.private_chat, name='private_chat'),
    path('send_message/<int:receiver_id>/', views.send_private_message, name='send_private_message'),
    path('get_messages/<int:student_id>/', views.get_private_messages, name='get_private_messages'),
]