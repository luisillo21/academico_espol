from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from ckeditor.fields import RichTextField
from .validator import validar_entrada_nombre, validar_entrada_entero, validar_entrada_textarea
from apps_academico.diseñoEvento.models import DesignEvento
from apps_academico.docente.models import Docente

# this class is temporaly, that's not the right table for Docente, only for test
"""
class Docente(models.Model):
    id_docente = models.CharField(max_length=10)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    
    def __str__(self):
        return '{} {}'.format(self.nombres, self.apellidos)
"""

# Create your models here.
class TipoConvenioAliado(models.Model):
    id_convenio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.nombre)


class Aliado(models.Model):
    codigo_aliado = models.IntegerField(primary_key=True, max_length=3)
    origen = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    tipo_de_covenio = models.ForeignKey(
        TipoConvenioAliado, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.nombre)


class UnidadAula(models.Model):
    id_unidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.nombre)


class TipoAula(models.Model):
    id_tipo_aula = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.nombre)


class EstadoAula(models.Model):
    id_estado_aula = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.estado)


class Aula(models.Model):
    codigo_aula = models.IntegerField(primary_key=True, max_length=3)
    unidad = models.ForeignKey(
        UnidadAula, null=False, blank=False, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=150)
    tipo = models.ForeignKey(TipoAula, null=False,
                             blank=False, on_delete=models.CASCADE)
    capacidad = models.IntegerField()
    observacion = models.TextField()
    estado = models.ForeignKey(
        EstadoAula, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.nombre)


class Evento(models.Model):
    diseno = models.ForeignKey(DesignEvento, on_delete=models.CASCADE)
    codigo_evento = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    tipo_evento = models.CharField(max_length=100)
    codigo_evento_padre = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='evento')
    nombre_evento_Padre = models.CharField(
        max_length=100, null=True, blank=True)
    modalidad = models.CharField(max_length=100)
    centro_costos = models.CharField(max_length=100)
    alcance = models.CharField(max_length=100)
    promocion = models.CharField(max_length=100)
    duracion = models.IntegerField()
    aliado = models.ForeignKey(
        Aliado, null=False, blank=False, on_delete=models.CASCADE)
    docente = models.ForeignKey(
        Docente, null=False, blank=False, on_delete=models.CASCADE)
    lugar = models.CharField(max_length=150)
    asesor_comercial_responsable = models.CharField(max_length=100)
    publico = models.CharField(max_length=100)
    servicios_incluidos = models.CharField(max_length=250)
    hora_break = models.TimeField(null=True, blank=True)
    hora_almuerzo = models.TimeField(null=True, blank=True)
    opciones_de_calendario = models.CharField(max_length=150)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=100)
    web = models.CharField(max_length=100)

    def get_aula(self):
        sesiones = CalendarioEvento.objects.filter(
            evento_id=self.codigo_evento)
        return sesiones[0]

    def format_servicios(self):
        s = self.servicios_incluidos
        s = s.replace('[', '')
        s = s.replace(']', '')
        s = s.replace("'", '')
        return s

    def horarios(self):
        horario = ""
        mes = ""
        anno = ""
        days = CalendarioEvento.objects.filter(evento_id=self.codigo_evento)
        for d in days:
            if horario == "":
                horario = horario + str(d.fecha.day)
                mes = d.fecha.strftime("%B").capitalize()
                anno = str(d.fecha.year)
            else:
                if mes != d.fecha.strftime("%B").capitalize():
                    horario = horario + ' de ' + mes + ' de ' + anno
                    horario = horario + ", " + str(d.fecha.day)
                    mes = d.fecha.strftime("%B").capitalize()
                    anno = str(d.fecha.year)
                else:
                    horario = horario + ", " + str(d.fecha.day)
                    mes = d.fecha.strftime("%B").capitalize()
                    anno = str(d.fecha.year)

        horario = horario + ' de ' + mes + ' de ' + anno
        return horario

    def publish(self):
        self.web = 'Publicado'
        self.save(update_fields=['web'])

    def __str__(self):
        return '{}'.format(self.codigo_evento)

    
class CalendarioEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    dia = models.CharField(max_length=100)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    facilitador = models.CharField(max_length=150)
    aula = models.ForeignKey(
        Aula, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.dia)


class Co(models.Model):
    co_facilitador = models.ForeignKey(
        Docente, null=True, blank=True, on_delete=models.CASCADE, related_name='docente')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.apellidos, self.nombres)


class PubEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to='image_event/')
