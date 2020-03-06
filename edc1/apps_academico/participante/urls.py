from django.urls import path, include
from django.shortcuts import *
from apps_academico.participante.views import *
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('asistencia/', TemplateView.as_view(template_name='asistencia.html'), name="participante_asistencia"),
    path('asistencia/by_evento_and_fecha', asistencia_by_evento_and_fecha, name="asistencia_by_evento_and_fecha"),
    path('ParticipantesReprobados/', ParticipantesReprobados.as_view(),name='Part_Reprobados'),
    path('Perfil_participante/',Perfil_participante.as_view(),name='Perfil_participante'),
    path('Conctacto_participante/',Conctacto_participante.as_view(),name='Conctacto_participante'),
    path('historico_participante/', historico_participante, name='historico_participante'),
]
