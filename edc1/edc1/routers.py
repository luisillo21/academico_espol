from rest_framework import routers
from apps_academico.planTrabajo.viewsets import *
from apps_academico.docente.viewsets import *
from apps_academico.participante.viewsets import *


"""
    Here are listed CRUD APIS, using Django Rest Viewsets.
    Each api is build from:
        - A model
        - A serializer class (How the model should be serialized)
        - A viewset (a generic Class to provide standard CRUD functionality through API REST for a given model )
        - A router (only a signature to expose the api)
"""

"""
    Custom APIS.
    If used for testing, the models used must have all fields with 
    null=True.
    If that is not the case. They will be used only for GET requests to retrieve 
    the fields especified. These fields are required in Plan de Trabajo flow.
"""

plan_trabajo_router = routers.DefaultRouter()
plan_trabajo_router.register(r'evento', EventoViewSet)
plan_trabajo_router.register(r'disenoEvento', DisenoEventoViewSet)
plan_trabajo_router.register(r'unidad', UnidadViewSet)
plan_trabajo_router.register(r'subUnidad', SubUnidadViewSet)
plan_trabajo_router.register(r'sesion', SesionViewSet)

"""
 APIS in Plan trabajo flow
"""
plan_trabajo_router.register(r'planTrabajo', PlanTrabajoViewSet)
plan_trabajo_router.register(r'actividadPlan',  ActividadPlanViewSet)
plan_trabajo_router.register(r'recursoSesion',RecursoSesionViewSet)
plan_trabajo_router.register(r'anexoPlan', AnexoPlanViewSet)
plan_trabajo_router.register(r'recursoPlan', RecursoPlanViewSet)
plan_trabajo_router.register(r'lecturaRecomendadaPlan', LecturaRecomendadaPlanViewSet)
plan_trabajo_router.register(r'referenciaBibliograficaPlan',ReferenciaBibliograficaPlanViewSet)
plan_trabajo_router.register(r'sesionItem',SesionItemViewSet)

"""
 APIS in Formulario de Hoja de vida de Docente flow
"""

docente_router = routers.DefaultRouter()
docente_router.register(r'docente',DocenteViewSet)
docente_router.register(r'educacionSuperior',EducacionSuperiorViewSet)
docente_router.register(r'actualizacionAcademica',ActualizacionAcademicaViewSet)
docente_router.register(r'formacionDocente',FormacionDocenteViewSet)
docente_router.register(r'experienciaProfesional',ExperienciaProfesionalViewSet)
docente_router.register(r'experienciaDocente',ExperienciaDocenteViewSet)
docente_router.register(r'perfil',PerfilViewSet)
docente_router.register(r'publicacion',PublicacionViewSet)
docente_router.register(r'anexoDocente',AnexoDocenteViewSet)

"""
 APIS in Participante flow
"""
participante_router = routers.DefaultRouter()
participante_router.register(r'participante',ParticipanteViewSet)
participante_router.register(r'asistencia',AsistenciaViewSet)
