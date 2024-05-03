from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_encuesta, name='crear_encuesta'), # crear una nueva encuesta
    path('editar_encuesta/<int:encuesta_id>/', views.editar_encuesta, name='editar_encuesta'), # editar una encuesta
    path('eliminar_encuesta/<int:encuesta_id>/', views.eliminar_encuesta, name='eliminar_encuesta'), # eliminar una encuesta
    path('confirmar_eliminacion/<int:encuesta_id>/', views.confirmar_eliminacion, name='confirmar_eliminacion'), # confirmar la eliminación de una encuesta
    path('crear_preguntas_encuesta/<int:encuesta_id>/', views.crear_preguntas_encuesta, name='crear_preguntas_encuesta'), # crear preguntas
    path('crear_opciones/<int:pregunta_id>/', views.crear_opciones, name='crear_opciones'), # crear opciones
    path('lista_encuestas/', views.lista_encuestas, name='lista_encuestas'), # lista de encuestas
    path('', views.encuestas_disponibles, name='encuestas_disponibles'), # encuestas disponibles
    path('responder_encuesta/<int:encuesta_id>/', views.responder_encuesta, name='responder_encuesta'), # responder encuesta
    path('gracias/', views.gracias_view, name='gracias'), # vista de agradecimiento
    path('agregar_opcion/<int:pregunta_id>/', views.agregar_opcion, name='agregar_opcion'), # agregar opcion de pregunta
    path('agregar_pregunta/<int:encuesta_id>/', views.agregar_pregunta, name='agregar_pregunta'), # agregar pregunta
    path('confirmar_eliminar_opcion/<int:encuesta_id>/', views.confirmar_eliminar_opcion, name='confirmar_eliminar_opcion'), # confirmar la eliminación de una encuesta
    path('confirmar_eliminacion_pregunta/<int:pregunta_id>/', views.confirmar_eliminacion_pregunta, name='confirmar_eliminacion_pregunta'), # confirmar la eliminación de una pregunta

]
