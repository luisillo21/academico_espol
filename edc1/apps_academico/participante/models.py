from django.db import models
from django.contrib.postgres.fields import JSONField

from apps_academico.crearEvento.models import Evento


# Create your models here.
class Participante(models.Model):
    """
        null fields are allowed for speed of development
        TODO:
            - add field 'foto'
    """
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    nombres = models.TextField()
    apellidos = models.TextField()


class Asistencia(models.Model):
    """
        In registro field I will save a value like :
        [
            { participante_id : 'PARTICIPANTE_ID1' , is_presente : true },
            { participante_id : 'PARTICIPANTE_ID2' , is_presente : false },
            ...
        ]
    """
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fecha = models.DateField(null=True)
    registro = JSONField(null=True)
