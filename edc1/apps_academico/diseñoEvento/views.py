from rest_framework import viewsets, filters
from .models import *
from .forms import *
from .serializers import *
from django.views.generic import ListView,TemplateView
from django.shortcuts import render,reverse
from django.urls import reverse_lazy
from filters.mixins import FiltersMixin
from bootstrap_modal_forms.generic import BSModalCreateView,BSModalUpdateView,BSModalDeleteView
from django.views.generic import View
#-------import para reportes----
from django.conf import settings
from io import BytesIO
from django.shortcuts import render, HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, yellow, black
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, TA_CENTER
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch, mm, cm
from reportlab.platypus import (
    Paragraph,
    Table,
    SimpleDocTemplate,
    Spacer,
    TableStyle,
    Paragraph,
    Image)

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from apps_academico.reporte_aca.utils import link_callback

#----------------------------------
# API
class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer

class TipoEventoViewSet(viewsets.ModelViewSet):
    queryset = TipoEvento.objects.all()
    serializer_class = TipoEventoSerializer

class DesignEventoViewSet(FiltersMixin,viewsets.ModelViewSet):
    queryset = DesignEvento.objects.prefetch_related().all()
    serializer_class = DesignEventoSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id', 'codigo',)
    ordering = ('id',)
    filter_mappings = {
        'id':'id',
        'cod':'codigo',
    }
    

class ObjetivoEspecificoViewSet(FiltersMixin,viewsets.ModelViewSet):
    queryset = ObjetivoEpecifico.objects.all()
    serializer_class = ObjetivoEspecificoSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id', 'descripcion',)
    ordering = ('id',)
    filter_mappings = {
        'id':'id',
        'desc':'descripcion',
    }

class UnidadViewSet(FiltersMixin,viewsets.ModelViewSet):
    queryset = Unidad.objects.all()
    serializer_class = UnidadSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id', 'nombre_unidad',)
    ordering = ('id',)
    filter_mappings = {
        'id':'id',
        'nom':'nombre_unidad',
    }

class SubUnidadViewSet(viewsets.ModelViewSet):
    queryset = SubUnidad.objects.all()
    serializer_class = SubUnidadSerializer

class RecursoViewSet(viewsets.ModelViewSet):
    queryset = Recurso.objects.all()
    serializer_class =RecursoSerializer

class LecturaViewSet(viewsets.ModelViewSet):
    queryset = Lectura.objects.all()
    serializer_class = LecturaSerializer

class ReferenciaViewSet(viewsets.ModelViewSet):
    queryset = Referencia.objects.all()
    serializer_class = ReferenciaSerializer

#Design

class ListarDesign(ListView):
    model=DesignEvento
    context_object_name =  'designs'
    template_name="design/listaDiseño.html"

class CrearDesign(TemplateView):
    template_name='design/crearDiseño.html'

    def get_success_url(self):
        return reverse_lazy('listarDesign')

#Lista General Area/Especialidad

def ListarAreaEspecialidad(request):
    area=Area.objects.all()
    especialidad=Especialidad.objects.all()
    contexto={'areas':area,'especialidades':especialidad}
    return render(request,'area/listarGeneralArea.html',contexto)

#Area
class CrearArea(BSModalCreateView):
    model=Area
    form_class=AreaForm
    template_name='area/crearArea.html'
    success_message = 'El área se creo con exito'
    success_url = reverse_lazy('listarGeneral')

class UpdateArea(BSModalUpdateView):
    model=Area
    form_class=AreaForm
    template_name='area/crearArea.html'
    success_message = 'El área se actualizó con exito'
    success_url = reverse_lazy('listarGeneral')
#Especialidad
class CrearEspecialidad(BSModalCreateView):
    model=Especialidad
    form_class=EspecialidadForm
    template_name='especialidades/crearEspecialidad.html'
    success_message = 'La especicalidad se creo con exito'
    success_url = reverse_lazy('listarGeneral')

class UpdateEspecialidad(BSModalUpdateView):
    model=Especialidad
    form_class=EspecialidadForm
    template_name='especialidades/crearEspecialidad.html'
    success_message = 'La especicalidad se actualizó con exito'
    success_url = reverse_lazy('listarGeneral')

#--------Seccion de Reportes---------------------   

class EventosPorGenero(View):
    style = getSampleStyleSheet()
    def cabecera(self, pdf):
        width, height = A4
        archivo_imagen = settings.MEDIA_ROOT+'/image_event/espol.png'
        pdf.drawImage(archivo_imagen, 10, 760, 230,
                      90, preserveAspectRatio=True)
        pdf.setFont("Helvetica-Bold",12 )
        pdf.drawString(410,810, b"Reporte de eventos por genero")
        pdf.setFillColor(yellow)
        pdf.rect(520,791, 67, 12, fill=True, stroke=False)
        pdf.setFillColor(black)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(520, 793, u"POEC0502 V7")


    def pie_pagina(self, pdf):
        pdf.setFont("Helvetica", 10)
        now = datetime.now()
        pdf.drawString(10,45,'CEC ESPOL, Campus Gustavo Galindo Velasco | Teléf:042269763 | 0960507588 ')
        pdf.drawString(10, 30, u"Fecha impresión:"+str(now.day) +
                       '/'+str(now.month)+'/'+str(now.year))
        page_num = pdf.getPageNumber()
        text = "Pág. %s|1" % page_num
        pdf.drawString(500, 30, text)
        pdf.drawString(200, 30, u'Usuario: ')
        pdf.drawString(240, 30, u'Luis Eduardo Ardila Macias')
        pdf.setFillColor(HexColor('#3c5634'))
        pdf.drawString(10, 60,"//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")


    def contenido(self, pdf, y):
        width, height = A4
        styles = getSampleStyleSheet()
        styleN = styles["BodyText"]
        styleN.alignment = TA_CENTER
        Numero= Paragraph('<b>N.-</b>',styleN)
        Codigo =Paragraph('<b>Codigo</b>', styleN)
        N_evento  =Paragraph('<b>Nombre del evento</b>', styleN)
        Precio  =Paragraph('<b>Precio</b>', styleN)
        Participantes = Paragraph('<b>Participantes</b>', styleN)
        P_sat =Paragraph('<b>Porcentaje de satisfacción sobre el uso del servicio</b>', styleN)
        encabezado1 = [
                        [Numero,Codigo,N_evento,Precio,Participantes,P_sat],
                        ['1','','','','',''],
                        ['2','','','','',''],
                        ['3','','','','',''],
                        ['4','','','','','']
                      ]
                
        t = Table(encabezado1, colWidths=[1*cm,2*cm,7*cm,2.5*cm,3.5*cm,4*cm])
        t.setStyle(TableStyle([
            ('BOX', (0, 0), (-1,-1), 0.20, colors.black),
            ('INNERGRID', (0, 0), (-1, -1),0.10,colors.black),
            ('BOTTOMPADDING',(0,0),(4,0),15),
        ]))
        t.wrapOn(pdf,width,height)
        t.drawOn(pdf,12,620)

    def get(self, request, ):
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        y = 590
        self.cabecera(pdf)
        self.pie_pagina(pdf)
        self.contenido(pdf, y)
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


def eventos_ejecutados(request):
    template_path = 'reportes/eventos_ejecutados.html'
    design = DesignEvento.objects.filter()
    context = {'design':design}
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


