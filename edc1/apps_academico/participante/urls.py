from django.urls import path, include
from django.shortcuts import *
from apps_academico.participante.views import *
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('asistencia/', TemplateView.as_view(template_name='asistencia.html'), name="participante_asistencia"),
    path('asistencia/by_evento_and_fecha', asistencia_by_evento_and_fecha, name="asistencia_by_evento_and_fecha"),
    path('ParticipantesReprobados/', ParticipantesReprobados.as_view(),name='Part_Reprobados'),
]
