from django.urls import path
from django.shortcuts import *
from django.views.generic import TemplateView
from .views import *



urlpatterns = [
    path('list/to_create/', TemplateView.as_view(template_name='plan_trabajo/list_to_create.html'), name="plan_trabajo_list_to_create"),
    path('list/to_approve/', TemplateView.as_view(template_name='plan_trabajo/list_to_approve.html'), name="plan_trabajo_list_to_approve"),
    path('<int:planTrabajo_pk>/fill/', PlanTrabajoCreate.as_view()),
    path('<int:planTrabajo_pk>/check/', PlanTrabajoCheck.as_view()),
    path('<int:basePlanTrabajo_pk>/<int:newPlanTrabajo_pk>/copy/', plan_trabajo_copy, name="plan_trabajo_copy"),
]
