from django.urls import path, re_path, include
from mainpage import views


urlpatterns = [
    path('', views.news, name='news'),
    path('form-ivent/', views.formivent, name='form-ivent'),
    path('article/<int:article_id>/', views.show_article, name='article'),
    path('schedule/', views.schedule, name='schedule'),
    path('journal/', views.journal, name='journal'),
    path('class-journal/', views.class_journal, name='class-journal'),
    path('add_lesson_date/', views.add_lesson_date, name='add_lesson_date'),
]
