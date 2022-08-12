from django.urls import path
from waveapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('output/', views.output, name='output'),
]
