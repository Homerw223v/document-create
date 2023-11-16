from django.urls import path

from . import views

urlpatterns = [
    path('send-document/', views.DocumentView.as_view(), name='send-document'),
]
