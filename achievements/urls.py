from django.urls import path
from . import views

app_name = 'achievements'

urlpatterns = [
    path('', views.achievements_home, name='achievements_home'),
]