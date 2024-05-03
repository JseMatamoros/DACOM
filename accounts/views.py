# importamos las bibliotecas necesarias
from django.contrib.auth.views import LoginView as AuthLoginView # para iniciar la sesion
from django.contrib.auth import logout # para cerrar la sesion
from django.contrib.auth.mixins import LoginRequiredMixin # para proteger las rutas
from django.views.generic import ListView, TemplateView # para las vistas visualizaciones
from django.views.generic.edit import DeleteView # para eliminar un usuario
from django.views import generic, View # para las visualizaciones
from django.http import HttpResponseRedirect # para redireccionar
from django.urls import reverse, reverse_lazy # para redireccionar
from django.shortcuts import get_object_or_404 # para redireccionar
from datetime import datetime, timedelta # para las fechas
from .forms import CustomUserCreationForm, CustomAuthenticationForm # para los formularios
from django.db.models import Count # para las visualizaciones
from encuestas.models import Respuesta,Prospecto # para las encuestas
from .models import CustomUser # para los usuarios
from django.templatetags.static import static # para las imagenes
import os # para las imagenes
import io # para las imagenes
import base64 # para las imagenes
import matplotlib.pyplot as plt # para las visualizaciones
plt.switch_backend('Agg') # para las visualizaciones
import pandas as pd # para las visualizaciones
import numpy as np # para las visualizaciones

#################################################################################################
# encargado de iniciar la sesion
class LoginView(AuthLoginView):
    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm
    def get_success_url(self):
        return reverse('home')
# encargado de cerrar la sesión
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('lista_encuestas'))
# encargado de visualizar el perfil del usuario y las visualizaciones de datos
class VerPerfil(LoginRequiredMixin, TemplateView):
    template_name = 'registration/perfil.html' 
    def get_context_data(self, **kwargs): 
        # obtenemos el contexto de la vista, que es un diccionario de variables que se pasará a la plantilla
        context = super().get_context_data(**kwargs)
        # obtenemos el usuario actualmente autenticado
        user = self.request.user
        # obtener las fechas de los ultimos 7 dias
        today = datetime.now().date()
        last_seven_days = [today - timedelta(days=i) for i in range(6, -2, -1)]
        last_seven_days_str = [date.strftime('%Y-%m-%d') for date in last_seven_days]
        # obtener la cantidad de encuestas respondidas por dia en los ultimos 7 dias
        respuestas_por_dia = Respuesta.objects.filter(prospecto__asistente=user, fecha__date__in=last_seven_days) \
            .values('fecha__date').annotate(cantidad=Count('id')).order_by('fecha__date')
        cantidad_encuestas_por_dia = {resp['fecha__date'].strftime('%Y-%m-%d'): resp['cantidad'] for resp in respuestas_por_dia}
        # crear la visualizacion con matplotlib
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(last_seven_days_str, [cantidad_encuestas_por_dia.get(date, 0) for date in last_seven_days_str], width=0.8)
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Cantidad de preguntas respondidas')
        ax.set_title('Observa tus últimos 8 días')
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        # guardar la visualizacion en memoria como un objeto BytesIO
        buffer = io.BytesIO()
        plt.savefig(buffer, format='jpg')
        buffer.seek(0)
        # convertir la imagen en base64 para incrustarla en la plantilla HTML
        encoded_image = base64.b64encode(buffer.read()).decode('utf-8')
        imagen_base64 = f'data:image/jpeg;base64,{encoded_image}'
        # obtener la cantidad de prospectos asociados al perfil del usuario autenticado
        cantidad_prospectos = Prospecto.objects.filter(asistente=user).count()
        cantidad_respuestas = Respuesta.objects.filter(prospecto__asistente=user).count()
        nombres_prospectos_relacionados = Prospecto.objects.filter(asistente=user).values_list('nombre', flat=True).distinct()
        # agregar los datos al contexto
        context['encuestas_respondidas_chart'] = imagen_base64
        context['cantidad_respuestas'] = cantidad_respuestas
        context['cantidad_prospectos'] = cantidad_prospectos
        context['nombres_prospectos_relacionados'] = nombres_prospectos_relacionados
        return context
# encargado de visualizar la lista de usuarios
class UserListView(ListView):
    # definimos la vista basada en clase ListView para mostrar una lista de usuarios
    model = CustomUser # especificamos el modelo de usuario a utilizar
    template_name = 'registration/user_list.html' # establecemos la plantilla para renderizar la vista
    context_object_name = 'users' # establecemos el nombre del objeto de contexto para los usuarios
# encargado de crear un nuevo usuario
class CreateUserView(generic.CreateView): # definimos la vista basada en clase CreateView para crear un nuevo usuario
    form_class = CustomUserCreationForm # establecemos el formulario de creacion de usuario
    success_url = reverse_lazy('login') # establecemos la URL de exito
    template_name = 'registration/create_user.html' # establecemos la plantilla para renderizar la vista
# encargado de eliminar un usuario
class UserDeleteView(DeleteView):
    model = CustomUser  
    template_name = 'registration/user_confirm_delete.html'
    success_url = reverse_lazy('user_list') # establecemos la URL de exito
    # definiendo la vista basada en clase DeleteView para eliminar un usuario
    def get_object(self, queryset=None): # definimos el objeto
        # obtenemos el objeto que se va a eliminar
        return get_object_or_404(CustomUser, pk=self.kwargs['pk'])
    # definiendo la vista basada en clase DeleteView para eliminar un usuario
    def delete(self, request, *args, **kwargs):
        # retornamos la vista basada en clase DeleteView para eliminar un usuario
        return super().delete(request, *args, **kwargs)
    # definiendo la vista basada en clase DeleteView para eliminar un usuario
    def get_context_data(self, **kwargs): # definimos el contexto
        context = super().get_context_data(**kwargs) # obtenemos el contexto
        context['user'] = self.object # establecemos el usuario
        return context # retornamos el contexto