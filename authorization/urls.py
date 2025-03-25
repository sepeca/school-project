from django.urls import path
from authorization import views


urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.do_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]
