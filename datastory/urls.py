from django.urls import path
from . import views

urlpatterns = [
    path('<int:encuesta_id>/', views.panel_encuesta_respuestas, name='panel_encuesta_respuestas'),
]