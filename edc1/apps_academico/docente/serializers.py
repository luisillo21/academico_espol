from rest_framework import serializers
from .models import *


"""
 Models in Formulario de Hoja de vida de Docente flow
"""

class DocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docente
        fields = '__all__'

class EducacionSuperiorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducacionSuperior
        fields = '__all__'

class ActualizacionAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActualizacionAcademica
        fields = '__all__'


class FormacionDocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormacionDocente
        fields = '__all__'

class ExperienciaProfesionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienciaProfesional
        fields = '__all__'

class ExperienciaDocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienciaDocente
        fields = '__all__'

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = '__all__'

class PublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicacion
        fields = '__all__'


class AnexoDocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnexoDocente
        fields = '__all__'
