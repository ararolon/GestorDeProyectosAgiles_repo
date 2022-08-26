from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Usuario(User):
    """
        Modelo utilizado para obtener los usuarios del sistema
        el modelo extiende del modelo User de Django
        modelo proxy
        Modelo padre : django.contrib.auth.models User
    """

    class Meta:
        proxy = True

    def __str__(self):
        return self.first_name + ' ' + self.last_name