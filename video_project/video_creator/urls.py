from django.urls import path
from . import views

urlpatterns = [
    path('create-video', views.create_video, name='create_video'),
]