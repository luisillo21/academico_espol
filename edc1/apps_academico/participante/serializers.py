from rest_framework import serializers
from .models import *

class ParticipanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = '__all__'

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = '__all__'