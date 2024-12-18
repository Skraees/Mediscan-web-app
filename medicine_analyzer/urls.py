from django.urls import path
from . import views

urlpatterns = [
    path('', views.analyze_medicine, name='analyze_medicine'),  # Root path for the app
]
