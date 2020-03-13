from django.urls import path, include
from django.shortcuts import *
from apps_academico.docente.views import *
from django.views.generic import TemplateView


urlpatterns = [
    path('list/to_create/', TemplateView.as_view(template_name='docente/list_to_create.html'), name="docente_list_to_create"),
    path('list/to_enable/', TemplateView.as_view(template_name='docente/list_to_enable.html'), name="docente_list_to_enable"),
    path('<int:docente_pk>/fill/', DocenteFill.as_view()),
    path('<int:docente_pk>/check/', DocenteCheck.as_view()),
    path('<int:docente_pk>/score/', docente_score),
    #----------------Seccion de reportes
    path('DocentePorCriterio/',docentePorCriterio,name='DocentePorCriterio'),
    path('AsistenciaDocentes/',asistencia_docente,name='asistencia_docente'),
]
