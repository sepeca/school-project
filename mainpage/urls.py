from django.urls import path
from django.views.generic import RedirectView

from mainpage import views



urlpatterns = [
    path('', RedirectView.as_view(url='/news/', permanent=False)),
    path('news/', views.news, name='news'),
    path('article/<int:article_id>/', views.show_article, name='article'),
    path('publish_news/', views.publish_news, name='publish_news'),
    path('classes-list/', views.classes_list, name='classes_list'),
    path('class-journal/<int:subject_id>/<int:class_id>/', views.class_journal, name='class_journal'),
    path('my-journal/<int:class_id>/', views.my_journal, name='my_journal'),
    path('study_plan/<int:subject_id>/<int:class_id>/', views.study_plan, name='study_plan'),
    path('publish_plan/<int:subject_id>/<int:class_id>/', views.publish_plan, name='publish_plan'),
    path('contacts/', views.contacts, name='contacts'),
]
