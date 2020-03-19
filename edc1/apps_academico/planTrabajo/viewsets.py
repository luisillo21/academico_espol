from rest_framework import viewsets,generics
from rest_framework.response import Response
from .models import *
from .serializers import *

from apps_academico.diseñoEvento.models import Unidad
from apps_academico.diseñoEvento.models import SubUnidad
from apps_academico.diseñoEvento.models import DesignEvento as DisenoEvento
from apps_academico.crearEvento.models import CalendarioEvento as Sesion
from apps_academico.crearEvento.models import Evento

"""
    Custom APIS.
    If used for testing, the models used must have all fields with 
    null=True.
    If that is not the case. They will be used only for GET requests to retrieve 
    the fields especified. These fields are required in Plan de Trabajo flow.
"""

#Only used for testing for creation of Sesion(Calendario_Evento)
class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

#Only used for testing for creation of Unidad, SubUnidad
class DisenoEventoViewSet(viewsets.ModelViewSet):
    queryset = DisenoEvento.objects.all()
    serializer_class = DisenoEventoSerializer

class UnidadViewSet(viewsets.ModelViewSet):
    queryset = Unidad.objects.all()
    serializer_class = UnidadSerializer

    def list(self , request, *args, **kwargs):
        queryset = Unidad.objects.all()

        pk = request.query_params.get('disenoEvento_id',None)
        if pk is not None:
            queryset = Unidad.objects.filter(design_id=pk)
        serializer = UnidadSerializer(queryset, many=True)
        return Response(serializer.data)
     
class SubUnidadViewSet(viewsets.ModelViewSet):
    queryset = SubUnidad.objects.all()
    serializer_class = SubUnidadSerializer
    
    def list(self , request, *args, **kwargs):
        queryset = SubUnidad.objects.all()

        pk = request.query_params.get('disenoEvento_id',None)
        if pk is not None:
            queryset = SubUnidad.objects.filter(design_id=pk)
        serializer = SubUnidadSerializer(queryset, many=True)
        return Response(serializer.data)

class SesionViewSet(viewsets.ModelViewSet):
    queryset = Sesion.objects.all()
    serializer_class = SesionSerializer

    def list(self , request, *args, **kwargs):
        queryset = Sesion.objects.all()

        pk = request.query_params.get('evento_id',None)
        if pk is not None:
            queryset = Sesion.objects.filter(evento_id=pk)
        serializer = SesionSerializer(queryset, many=True)
        return Response(serializer.data)

"""
 Models in Plan trabajo flow
"""

class PlanTrabajoViewSet(viewsets.ModelViewSet):
    queryset = PlanTrabajo.objects.all()
    serializer_class = PlanTrabajoSerializer

class ActividadPlanViewSet(viewsets.ModelViewSet):
    queryset = ActividadPlan.objects.all()
    serializer_class = ActividadPlanSerializer

    def list(self , request, *args, **kwargs):
        queryset = ActividadPlan.objects.all()

        pk = request.query_params.get('planTrabajo_id',None)
        if pk is not None:
            queryset = ActividadPlan.objects.filter(plan_trabajo_id=pk)
        serializer = ActividadPlanSerializer(queryset, many=True)
        return Response(serializer.data)

class RecursoSesionViewSet(viewsets.ModelViewSet):
    queryset = RecursoSesion.objects.all()
    serializer_class = RecursoSesionSerializer

    def list(self , request, *args, **kwargs):
        queryset = RecursoSesion.objects.all()

        pk = request.query_params.get('planTrabajo_id',None)
        if pk is not None:
            queryset =RecursoSesion.objects.filter(plan_trabajo_id=pk)
        serializer =RecursoSesionSerializer(queryset, many=True)
        return Response(serializer.data)

class AnexoPlanViewSet(viewsets.ModelViewSet):
    queryset = AnexoPlan.objects.all()
    serializer_class = AnexoPlanSerializer

    def list(self , request, *args, **kwargs):
        queryset = AnexoPlan.objects.all()

        pk = request.query_params.get('planTrabajo_id',None)
        if pk is not None:
            queryset = AnexoPlan.objects.filter(plan_trabajo_id=pk)
        serializer = AnexoPlanSerializer(queryset, many=True)
        return Response(serializer.data)


class RecursoPlanViewSet(viewsets.ModelViewSet):
    queryset = RecursoPlan.objects.all()
    serializer_class = RecursoPlanSerializer

    def list(self , request, *args, **kwargs):
        queryset = RecursoPlan.objects.all()

        pk = request.query_params.get('planTrabajo_id',None)
        if pk is not None:
            queryset = RecursoPlan.objects.filter(plan_trabajo_id=pk)
        serializer = RecursoPlanSerializer(queryset, many=True)
        return Response(serializer.data)

class LecturaRecomendadaPlanViewSet(viewsets.ModelViewSet):
    queryset = LecturaRecomendadaPlan.objects.all()
    serializer_class = LecturaRecomendadaPlanSerializer

    def list(self , request, *args, **kwargs):
        queryset = LecturaRecomendadaPlan.objects.all()

        pk = request.query_params.get('planTrabajo_id',None)
        if pk is not None:
            queryset =LecturaRecomendadaPlan.objects.filter(plan_trabajo_id=pk)
        serializer = LecturaRecomendadaPlanSerializer(queryset, many=True)
        return Response(serializer.data)

class ReferenciaBibliograficaPlanViewSet(viewsets.ModelViewSet):
    queryset = ReferenciaBibliograficaPlan.objects.all()
    serializer_class =ReferenciaBibliograficaPlanSerializer

    def list(self , request, *args, **kwargs):
        queryset = ReferenciaBibliograficaPlan.objects.all()

        pk = request.query_params.get('planTrabajo_id',None)
        if pk is not None:
            queryset =ReferenciaBibliograficaPlan.objects.filter(plan_trabajo_id=pk)
        serializer = ReferenciaBibliograficaPlanSerializer(queryset, many=True)
        return Response(serializer.data)

class SesionItemViewSet(viewsets.ModelViewSet):
    queryset = SesionItem.objects.all()
    serializer_class = SesionItemSerializer

    def list(self , request, *args, **kwargs):
        queryset = SesionItem.objects.all()

        pk = request.query_params.get('planTrabajo_id',None)
        if pk is not None:
            queryset =SesionItem.objects.filter(plan_trabajo_id=pk)
        serializer =SesionItemSerializer(queryset, many=True)
        return Response(serializer.data)