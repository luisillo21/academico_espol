from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator,MinLengthValidator,MaxLengthValidator

# Create your models here.
class Area(models.Model):
    codigo=models.TextField()
    area=models.TextField()

    def __str__(self):
        return "{}".format(self.codigo+" : "+self.area)

    def getNameArea(self):
        return "{}".format(self.area)

class Especialidad(models.Model):
     codigo=models.TextField()
     especialidades=models.TextField()
     area=models.ForeignKey(Area,null=False,blank=False,on_delete=models.CASCADE)

     def __str__(self):
          return "{}".format(self.codigo+" : "+self.especialidades)

class TipoEvento(models.Model):
    nombre=models.TextField()

    def __str__(self):
        return "{}".format(self.nombre)
    
class DesignEvento(models.Model):
    codigo=models.TextField()
    nombre=models.TextField()
    fecha=models.DateField(auto_now=True)
    version=models.IntegerField()
    cod_programa=models.TextField()
    area=models.ForeignKey(Area,null=False,blank=False,on_delete=models.CASCADE)
    especialidad=models.ForeignKey(Especialidad,null=False,blank=False,on_delete=models.CASCADE)
    tipo_evento=models.ForeignKey(TipoEvento,null=False,blank=False,on_delete=models.CASCADE)
    modalidad=models.TextField()
    tipo_certificado=models.TextField()
    estado=models.TextField()
    requisitos_facilitador=models.TextField()   
    horas_presenciales=models.IntegerField()
    horas_autonomas=models.IntegerField()
    horas_totales=models.IntegerField()
    justificacion=models.TextField()
    objetivo=models.TextField()
    dirigido_participante=models.TextField()
    indispensable_participante=models.TextField()
    recomendables_participante=models.TextField()
    metodologia1=models.BooleanField()
    metodologia2=models.BooleanField()
    metodologia3=models.BooleanField()
    metodologia4=models.BooleanField()
    metodologia5=models.BooleanField()
    metodologia6=models.BooleanField()
    metodologia7=models.BooleanField()
    metodologia8=models.BooleanField()

    def getUnidades(self):
        unidades = Unidad.objects.filter(design=self.id)
        return unidades

    def cantidad_diseños(self):
        pass


    def __str__(self):
        return "{}".format(self.nombre)



class ObjetivoEpecifico(models.Model):
    descripcion=models.TextField()
    design=models.ForeignKey(DesignEvento,null=False,blank=False,on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.descripcion)

class Unidad(models.Model):
    numero=models.IntegerField()
    nombre_unidad=models.TextField()
    horas_presenciales_unidad=models.IntegerField()
    horas_autonomas_unidad=models.IntegerField()
    horas_totales=models.IntegerField()
    objetivo=models.ForeignKey(ObjetivoEpecifico,null=False,blank=False,on_delete=models.CASCADE)
    design=models.ForeignKey(DesignEvento,null=False,blank=False,on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.nombre_unidad)

class SubUnidad(models.Model):
    numero_sub=models.TextField()
    nombre_sub=models.TextField()
    horas_presenciales_sub=models.IntegerField()
    horas_autonomas_sub=models.IntegerField()
    horas_totales_sub=models.IntegerField()
    unidad=models.ForeignKey(Unidad,null=False,blank=False,on_delete=models.CASCADE)
    design=models.ForeignKey(DesignEvento,null=False,blank=False,on_delete=models.CASCADE)
    def __str__(self):
        return "{}".format(self.nombre_sub)


class Recurso(models.Model):
    tipo=models.TextField()
    descripcion=models.TextField()
    design=models.ForeignKey(DesignEvento,null=False,blank=False,on_delete=models.CASCADE)

class Lectura(models.Model):
    tipo=models.TextField()
    titulo=models.TextField()
    autor=models.TextField()
    sitio_web=models.TextField(null=True,blank=True)
    enlace=models.TextField(null=True,blank=True)
    publicacion=models.IntegerField(null=True,blank=True)
    editorial=models.TextField(null=True,blank=True)
    pais=models.TextField(null=True,blank=True)
    fecha=models.DateField(null=True,blank=True)
    descripcion=models.TextField()
    design=models.ForeignKey(DesignEvento,null=False,blank=True,on_delete=models.CASCADE)

class Referencia(models.Model):
    tipo=models.TextField()
    titulo=models.TextField()
    autor=models.TextField()
    sitio_web=models.TextField(null=True,blank=True)
    enlace=models.TextField(null=True,blank=True)
    publicacion=models.IntegerField(null=True,blank=True)
    editorial=models.TextField(null=True,blank=True)
    pais=models.TextField(null=True,blank=True)
    fecha=models.DateField(null=True,blank=True)
    descripcion=models.TextField()
    design=models.ForeignKey(DesignEvento,null=False,blank=True,on_delete=models.CASCADE)

