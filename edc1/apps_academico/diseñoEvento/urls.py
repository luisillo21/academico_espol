from django.urls import include, path
from rest_framework import routers
from .views import *
from django.views.generic import TemplateView

router = routers.DefaultRouter()
router.register(r'area', AreaViewSet)
router.register(r'especialidad', EspecialidadViewSet)
router.register(r'tipoEvento', TipoEventoViewSet)
router.register(r'design', DesignEventoViewSet)
router.register(r'objetivoEspecifico', ObjetivoEspecificoViewSet)
router.register(r'unidad', UnidadViewSet)
router.register(r'subUnidad', SubUnidadViewSet)
router.register(r'recurso', RecursoViewSet)
router.register(r'lectura', LecturaViewSet)
router.register(r'referencia', ReferenciaViewSet)

urlpatterns = [
    path('api/',include(router.urls)),
    path('area/listar/',ListarAreaEspecialidad,name='listarGeneral'),
    #Area
    path('area/crear/',CrearArea.as_view(),name='crearArea'),
    path('area/<int:pk>/update/',UpdateArea.as_view(),name='updateArea'),
    #Especialidad
    path('especialidad/crear/',CrearEspecialidad.as_view(),name='crearEspecialidad'),
    path('especialidad/<int:pk>/update/',UpdateEspecialidad.as_view(),name='updateEspecialidad'),
    #Design Evento
    path('design/listar/',ListarDesign.as_view(),name='listarDesign'),
    path('design/crear/',CrearDesign.as_view(),name='crearDesign'),
    #-----Seccion de reportes
    path('EventosPorGenero/',EventosPorGenero.as_view(),name='Evento_por_genero'),
    path('EvetosPorGenero2/', EventosPorGenero2.as_view(), name='Evento_por_genero2'),

]
