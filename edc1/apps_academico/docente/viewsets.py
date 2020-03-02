from rest_framework import viewsets,generics
from rest_framework.response import Response
from .models import *
from .serializers import *

"""
    Models in Formulario de Hoja de vida de Docente flow
"""
class DocenteViewSet(viewsets.ModelViewSet):
    queryset = Docente.objects.all()
    serializer_class = DocenteSerializer

class EducacionSuperiorViewSet(viewsets.ModelViewSet):
    queryset = EducacionSuperior.objects.all()
    serializer_class = EducacionSuperiorSerializer
    
    def list(self , request, *args, **kwargs):
        queryset = EducacionSuperior.objects.all()

        pk = request.query_params.get('docente_id',None)
        if pk is not None:
            queryset = EducacionSuperior.objects.filter(docente_id=pk)
        serializer = EducacionSuperiorSerializer(queryset, many=True)
        return Response(serializer.data)

class ActualizacionAcademicaViewSet(viewsets.ModelViewSet):
    queryset = ActualizacionAcademica.objects.all()
    serializer_class = ActualizacionAcademicaSerializer

    def list(self , request, *args, **kwargs):
        queryset = ActualizacionAcademica.objects.all()

        pk = request.query_params.get('docente_id',None)
        if pk is not None:
            queryset = ActualizacionAcademica.objects.filter(docente_id=pk)
        serializer = ActualizacionAcademicaSerializer(queryset, many=True)
        return Response(serializer.data)

class FormacionDocenteViewSet(viewsets.ModelViewSet):
    queryset = FormacionDocente.objects.all()
    serializer_class = FormacionDocenteSerializer

    def list(self , request, *args, **kwargs):
        queryset = FormacionDocente.objects.all()

        pk = request.query_params.get('docente_id',None)
        if pk is not None:
            queryset = FormacionDocente.objects.filter(docente_id=pk)
        serializer = FormacionDocenteSerializer(queryset, many=True)
        return Response(serializer.data)

class ExperienciaProfesionalViewSet(viewsets.ModelViewSet):
    queryset = ExperienciaProfesional.objects.all()
    serializer_class = ExperienciaProfesionalSerializer

    def list(self , request, *args, **kwargs):
        queryset = ExperienciaProfesional.objects.all()

        pk = request.query_params.get('docente_id',None)
        if pk is not None:
            queryset = ExperienciaProfesional.objects.filter(docente_id=pk)
        serializer = ExperienciaProfesionalSerializer(queryset, many=True)
        return Response(serializer.data)

class ExperienciaDocenteViewSet(viewsets.ModelViewSet):
    queryset = ExperienciaDocente.objects.all()
    serializer_class = ExperienciaDocenteSerializer

    def list(self , request, *args, **kwargs):
        queryset = ExperienciaDocente.objects.all()

        pk = request.query_params.get('docente_id',None)
        if pk is not None:
            queryset = ExperienciaDocente.objects.filter(docente_id=pk)
        serializer = ExperienciaDocenteSerializer(queryset, many=True)
        return Response(serializer.data)


class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    
    def list(self , request, *args, **kwargs):
        queryset = Perfil.objects.all()

        pk = request.query_params.get('docente_id',None)
        if pk is not None:
            queryset = Perfil.objects.filter(docente_id=pk)
        serializer = PerfilSerializer(queryset, many=True)
        return Response(serializer.data)

class PublicacionViewSet(viewsets.ModelViewSet):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionSerializer

    def list(self , request, *args, **kwargs):
        queryset = Publicacion.objects.all()

        pk = request.query_params.get('docente_id',None)
        if pk is not None:
            queryset = Publicacion.objects.filter(docente_id=pk)
        serializer = PublicacionSerializer(queryset, many=True)
        return Response(serializer.data)

class AnexoDocenteViewSet(viewsets.ModelViewSet):
    queryset = AnexoDocente.objects.all()
    serializer_class = AnexoDocenteSerializer

    def list(self , request, *args, **kwargs):
        queryset = AnexoDocente.objects.all()

        pk = request.query_params.get('docente_id',None)
        if pk is not None:
            queryset = AnexoDocente.objects.filter(docente_id=pk)
        serializer = AnexoDocenteSerializer(queryset, many=True)
        return Response(serializer.data)