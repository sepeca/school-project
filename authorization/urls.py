from django.urls import path, re_path
from authorization import views


urlpatterns = [
    path('login/', views.loginPage, name='login'),
    # path('register/', views.registerPage, name='register'),
    path('logout/', views.doLogout, name='logout'),
    path('profile/', views.profile, name='profile'),
]
