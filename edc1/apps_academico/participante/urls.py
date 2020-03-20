from django.urls import path, include
from django.shortcuts import *
from apps_academico.participante.views import *
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('asistencia/', TemplateView.as_view(template_name='asistencia.html'), name="participante_asistencia"),
    path('asistencia/by_evento_and_fecha', asistencia_by_evento_and_fecha, name="asistencia_by_evento_and_fecha"),
    #---------Reporte----------
    path('ParticipantesReprobados/', part_reprobados,name='Part_Reprobados'),
    path('Perfil_participante/',Perfil_participante.as_view(),name='Perfil_participante'),
    path('Conctacto_participante/',Conctacto_participante.as_view(),name='Conctacto_participante'),
    path('historico_participante/', historico_participante, name='historico_participante'),
    #--------
    path('contacto_participante',contacto_participante,name='contacto_participante'),
    path('registro_asistencia_evento/',registro_asistencia_evento,name='registro_asistencia_evento'),
    path('reporte_asistencia',reporte_asistencia,name='reporte_asistencia'),
    path('perfil_participante',perfil_participante,name='perfil_participante'),
    #-----
    path('acta_nota_evento',acta_nota_evento,name='acta_nota_evento'),
    #-----
    path('acta_entrega_certificado',acta_entrega_certificado,name='acta_entrega_certificado'),
    #-----
    path('acta_emision_certificados_evento',acta_emision_certificados_evento,name='acta_emision_certificados_evento'),
    path('detalle_evaulacion_evento',detalle_evaulacion_evento,name='detalle_evaulacion_evento'),
]
