from rest_framework import serializers
from .models import *

class TipoConvenioAliadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoConvenioAliado
        fields = '__all__'

class AliadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aliado
        fields = '__all__'

class DocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docente
        fields = '__all__'

class UnidadAulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadAula
        fields = '__all__'

class TipoAulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAula
        fields = '__all__'

class EstadoAulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoAula
        fields = '__all__'

class AulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aula
        fields = '__all__'

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

class CalendarioEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarioEvento
        fields = '__all__'

class CoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Co
        fields = '__all__'

class PubEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PubEvento
        fields = '__all__'

