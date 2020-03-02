from rest_framework import serializers
from .models import *

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Area
        fields = '__all__'

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model=Especialidad
        fields = '__all__'

class TipoEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model=TipoEvento
        fields = '__all__'

class DesignEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model=DesignEvento
        fields = '__all__'

class ObjetivoEspecificoSerializer(serializers.ModelSerializer):
    class Meta:
        model=ObjetivoEpecifico
        fields = '__all__'

class UnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model=Unidad
        fields = '__all__'

class SubUnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubUnidad
        fields = '__all__'

class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Recurso
        fields = '__all__'

class LecturaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lectura
        fields = '__all__'

class ReferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Referencia
        fields = '__all__'

