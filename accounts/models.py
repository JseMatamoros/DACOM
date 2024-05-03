from django.contrib.auth.models import AbstractUser, Group
from django.db import models
# La clase CustomUser extiende AbstractUser, lo que probablemente 
# representa un modelo de usuario personalizado.
# selected_group: Un campo ForeignKey que se vincula al modelo Group, 
# permitiendo que los usuarios estén asociados con un grupo específico.
class CustomUser(AbstractUser): # La clase CustomUser extiende AbstractUser
    selected_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True) # selected_group: Un campo ForeignKey que se vincula al modelo Group, permitiendo que los usuarios estén asociados con un grupo específico.
