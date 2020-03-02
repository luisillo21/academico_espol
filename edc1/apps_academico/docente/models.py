from django.db import models

"""
 Models in Formulario Docente flow
"""
class Docente(models.Model):
    """
        null fields are allowed for speed of development
        TODO: 
            - add field 'foto'
    """
    nombres = models.TextField()
    apellidos = models.TextField()
    sintesis_cv = models.TextField(null=True)
    indice_dactilar = models.TextField(null=True)
    direccion_de_domicilio = models.TextField(null=True)
    telefono_movil = models.TextField(null=True)
    telefono_convencional = models.TextField(null=True)
    fecha_de_nacimiento = models.DateField(null=True)
    lugar_de_nacimiento = models.TextField(null=True)
    correo_principal = models.TextField(null=True)
    correo_secundario = models.TextField(null=True)
    numero_de_cedula = models.TextField(null=True)
    estado = models.TextField(null=True)
    observacion = models.TextField(null=True)

    def __str__(self):
        return '{} {}'.format(self.nombres, self.apellidos)

class EducacionSuperior(models.Model):
    """
        tipo = PREGRADO| POSTGRADO| TÉCNICO O TECNOLÓGICO|ARTESANAL|CERTIFICACIÓN POR COMPETENCIAS LABORALES
    """
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    tipo = models.TextField()
    nombre_de_institucion = models.TextField()
    pais = models.TextField()
    nombre_de_titulo = models.TextField()
    registro_senesyct = models.TextField()
    fecha_de_inicio = models.DateField()
    fecha_de_fin = models.DateField()

class ActualizacionAcademica(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    nombre_de_curso = models.TextField()
    nombre_de_institucion = models.TextField()
    nombre_de_certificado = models.TextField()
    duracion_en_horas = models.IntegerField()    
    fecha_de_inicio = models.DateField()
    fecha_de_fin = models.DateField()

class FormacionDocente(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    nombre_de_curso = models.TextField()
    nombre_de_institucion = models.TextField()
    nombre_de_certificado = models.TextField()
    duracion_en_horas = models.IntegerField()    
    fecha_de_inicio = models.DateField()
    fecha_de_fin = models.DateField()

class ExperienciaProfesional(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)    
    nombre_de_empresa = models.TextField()
    pais = models.TextField()
    nombre_de_cargo = models.TextField()
    descripcion_de_actividades = models.TextField()       
    fecha_de_inicio = models.DateField()
    fecha_de_fin = models.DateField()

class ExperienciaDocente(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)    
    nombre_de_empresa = models.TextField()    
    nombre_de_curso = models.TextField()    
    nombre_de_especialidad = models.TextField()
    pais = models.TextField()    
    duracion_en_horas = models.IntegerField()
    fecha_de_inicio = models.DateField()
    fecha_de_fin = models.DateField()

class Perfil(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)    
    nombre_de_empresa = models.TextField()    
    nombre = models.TextField()
    duracion_en_horas = models.IntegerField()
    fecha_de_inicio = models.DateField()
    fecha_de_fin = models.DateField()

class Publicacion(models.Model):
    """
        medio = Digital | Escrito
    """
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)     
    titulo = models.TextField()
    nombre_de_revista = models.TextField()    
    medio = models.TextField()    
    descripcion = models.TextField()
    enlace = models.TextField()    
    fecha_de_publicacion = models.DateField()

class AnexoDocente(models.Model):
    docente = models.ForeignKey(Docente,on_delete=models.CASCADE)
    nombre =  models.TextField()
    descripcion = models.TextField()
    """
        TODO: add archivo adjunto
    """