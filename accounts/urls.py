from django.urls import path
from . import views
# accounts/urls.py
# mis URLs de autenticación de Django
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'), 
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.VerPerfil.as_view(), name='ver_perfil'), # aqui se muestran los graficos del perfil de usuario
    path('usuarios/', views.UserListView.as_view(), name='user_list'),
    path('create_user/', views.CreateUserView.as_view(), name='create_user'),
    path('user_delete/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'),
]

