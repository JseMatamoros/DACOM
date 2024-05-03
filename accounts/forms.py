# importamos las bibliotecas necesarias
from django import forms # para los formularios
from django.contrib.auth.forms import UserCreationForm # para los formularios
from django.contrib.auth.forms import AuthenticationForm # para los formularios
from .models import CustomUser # para los usuarios
from django.contrib.auth.models import Group # para los usuarios
# CustomAuthenticationForm extiende AuthenticationForm de Django.
# El campo username es un CharField con widget TextInput y una clase de CSS personalizada.
# El campo password es un CharField con widget PasswordInput y una clase de CSS personalizada.
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
# Esta definición de clase crea un formulario personalizado para la creación de usuarios con campos adicionales y un método de guardado personalizado.
# email: define un campo de email con una longitud máxima y un texto de ayuda.
# selected_group_id: define un campo de selección de modelo para elegir un grupo.
# Meta: asocia el formulario con el modelo CustomUser y especifica los campos a incluir.
# save: reemplaza el método de guardado predeterminado para guardar al usuario y manejar el grupo seleccionado si se proporciona.
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Requerido. Ingrese una dirección de correo electrónico válida.')
    selected_group_id = forms.ModelChoiceField(queryset=Group.objects.all(), label="Grupo", required=False, empty_label="Seleccionar grupo")
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'selected_group_id')
    def save(self, commit=True): # reemplaza el método de guardado predeterminado
        user = super().save(commit=False) # guardar al usuario
        if commit: # si se debe realizar el guardado
            user.save() # guardar al usuario
        selected_group = self.cleaned_data.get('selected_group_id') # obtener el grupo seleccionado
        if selected_group: # si se proporcionó un grupo
            user.selected_group = selected_group # asignar el grupo
            user.save() # guardar al usuario
            user.groups.add(selected_group) # agregar el usuario al grupo
        return user # devolver el usuario
# Esta clase define un formulario para 
# confirmar la eliminación de un usuario.
# El método confirm_delete crea un campo booleano 
# para confirmar la eliminación con una entrada de checkbox.
class UserDeletionConfirmationForm(forms.Form): # para los formularios
    confirm_delete = forms.BooleanField( # para los formularios
        required=True, # para los formularios
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), # para los formularios
    )
