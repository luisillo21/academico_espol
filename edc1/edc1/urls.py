"""edc1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from .routers import *
from apps_academico.reporte_aca.Acta_entrega_certificados import Acta_entrega_certificados

urlpatterns = [
    path('', RedirectView.as_view(url='academico/designListar/')),
    path('admin/', admin.site.urls),
    path('academico/', include('apps_academico.diseñoEvento.urls')),
    path('academico/', include('apps_academico.crearEvento.urls')),
    path('academico/planTrabajo/', include('apps_academico.planTrabajo.urls')),
    path('academico/participante/', include('apps_academico.participante.urls')),
    path('academico/docente/', include('apps_academico.docente.urls')),
    path('api/', include(plan_trabajo_router.urls)),
    path('api/', include(docente_router.urls)),
    path('api/', include(participante_router.urls)),
    path('entrega_certificado/',Acta_entrega_certificados.as_view(),name='entrega_certificado')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""path('evento/', include(('apps_academico.crearEvento.urls', 'index'), namespace="index")),
    path('evento/', include(('apps_academico.crearEvento.urls', 'crearEvento'), namespace="crearEvento")),"""
