from django.urls import path,include
from django.contrib import admin

from quiz import views

app_name = 'quiz'

urlpatterns = [
    path('', views.first_page, name='firstpage'),
    path('login', views.index, name='index'),
    path('home', views.home, name = 'home'),
    path('quiz_page', views.quiz_page, name = 'quiz_page'),
    path('result', views.result , name = 'result'),
]