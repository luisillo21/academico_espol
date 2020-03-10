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
class EventosPorGenero2(View):
    style = getSampleStyleSheet()
    def cabecera(self, pdf):
        width, height = A4
        archivo_imagen = settings.MEDIA_ROOT+'/image_event/espol.png'
        pdf.drawImage(archivo_imagen, 10, 760, 230,
                      90, preserveAspectRatio=True)
        pdf.setFont("Helvetica-Bold",14)
        pdf.drawString(380,810, b"Reporte de eventos por genero")
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
        F_ini = Paragraph('<b>F. Inicio</b>', styleN)
        F_fin =Paragraph('<b>F. Final</b>', styleN)
        t_capac =Paragraph('<b>Tipo de capacitación</b>', styleN)
        Publico = Paragraph('<b>Publico</b>', styleN)
        Hombre =  Paragraph('<b>Hombre</b>', styleN)
        Mujer =  Paragraph('<b>Mujer</b>', styleN)
        Participantes = Paragraph('<b>Participantes</b>', styleN)
        encabezado1 = [
                        ['','','','','','','',Participantes,''],
                        [Numero,Codigo,N_evento,F_ini,F_fin,t_capac,Publico,Hombre,Mujer],
                        ['1','','','','','','',''],
                        ['2','','','','','','',''],
                        ['3','','','','','','',''],
                        ['4','','','','','','','']
                      ]
        t = Table(encabezado1, colWidths=[0.9*cm,2*cm,4.6*cm,2*cm,2*cm,3*cm,2*cm,2*cm,2*cm])
        t.setStyle(TableStyle([
            ('BOX', (7, 0), (-1,0), 0.30, colors.black),
            ('INNERGRID', (7, 0), (-1, 0),0.10,colors.black),
            ('BOX', (0, 1), (-1,-1), 0.20, colors.black),
            ('INNERGRID', (0, 1), (-1, -1),0.10,colors.black),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('SPAN',(7,0),(8,0)),
            ('BOTTOMPADDING',(0,0),(-1,0),3),
        ]))
        t.wrapOn(pdf,width,height)
        t.drawOn(pdf,8,620)

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



class Eventos_Ejecutados(View):
    style = getSampleStyleSheet()
    styleN = style["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 8
    width,height =A4
    styleB = style["BodyText"]
    styleB.alignment = TA_LEFT
    styleB.fontSize = 10




    def cabecera(self, pdf):
        archivo_imagen = settings.MEDIA_ROOT+'/image_event/espol.png'
        pdf.drawImage(archivo_imagen, 10, 500, 230,
                      90, preserveAspectRatio=True)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(640, 565,"Eventos ejecutados por diseño")
        pdf.setFillColor(yellow)
        pdf.rect(750, 548, 67, 13, fill=True, stroke=False)
        pdf.setFillColor(black)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(750, 550, u"POEC0502 V7")

    def pie_pagina(self, pdf):
        pdf.setFont("Helvetica", 10)
        now = datetime.now()
        pdf.drawString(
            10, 45, 'CEC ESPOL, Campus Gustavo Galindo Velasco | Teléf:042269763 | 0960507588 ')
        pdf.drawString(10, 30, u"Fecha impresión:"+str(now.day) +
                       '/'+str(now.month)+'/'+str(now.year))
        page_num = pdf.getPageNumber()
        text = "Pág. %s|1" % page_num
        pdf.drawString(790, 30, text)
        pdf.drawString(200, 30, u'Usuario: ')
        pdf.drawString(240, 30, u'Luis Eduardo Ardila Macias')
        pdf.setFillColor(HexColor('#3c5634'))
        pdf.drawString(10, 60, "///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")

    def contenido(self, pdf, y):
        width, height = A4
        #disenios = DesignEvento.objects.filter()
        contenido = self.body_data()
        encabezado1 = [
            self.head_data(),
            self.body_data()[0],
            ['2','','','','','','','','','','','',''],
            ['3','','','','','','','','','','','',''],
            ['4','','','','','','','','','','','','']
        ]
        t = Table(encabezado1, colWidths=[
                  0.9*cm,2*cm,2*cm,5*cm,2*cm,2.5*cm,2.2*cm,2.2*cm,2*cm,2.2*cm,2*cm,1.8*cm, 2*cm])
        t.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.10, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.10, colors.black),
            ('BOTTOMPADDING', (2, 0), (7, 0), 9),
            ]))
        t.wrapOn(pdf,self.width,self.height)
        t.drawOn(pdf, 8, 380)
        #Formulario Inferior
        
        var_1 = Paragraph('<b>Total diseños</b>', self.styleB)
        var_2 = Paragraph('<b>Total por modalidad</b>', self.styleB)
        var_3 = Paragraph('<b>Total Diseño por área</b>', self.styleB)
        var_4 = Paragraph('<b>Total tipo certificado</b>',self.styleB)
        var_5=Paragraph('<b>Total tipo evento</b>',self.styleB)

        form_inferior = [
            [var_1, 'Σ total', '', var_2, 'Σ total'],
            [var_3, 'Σ total', '', var_4, 'Σ total'],
            [var_5, '', '', '', '']
        ]

        t_form = Table(form_inferior, colWidths=[
            5*cm, 2*cm, 4.5*cm, 4*cm, 4*cm])
        t_form.setStyle(TableStyle([
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            #('BOX', (0, 0), (-1, -1), 0.10, colors.black),
            #('INNERGRID', (0, 0), (-1, -1), 0.10, colors.black),
        ]))
        t_form.wrapOn(pdf, self.width,self.height)
        t_form.drawOn(pdf, 8, 90)

    def head_data(self):
        data =[
               Paragraph('<b>N.-</b>',self.styleN),
               Paragraph('<b>Codigo diseño</b>',self.styleN),
               Paragraph('<b>Version</b>',self.styleN),
               Paragraph('<b>Nombre del Evento</b>',self.styleN),
               Paragraph('<b>Area</b>',self.styleN),
               Paragraph('<b>Especialidad</b>',self.styleN),
               Paragraph('<b>Tipo Evento</b>',self.styleN),
               Paragraph('<b>Modalidad</b>',self.styleN),
               Paragraph('<b>Tipo certificado</b>',self.styleN),
               Paragraph('<b>Horas presenciales</b>',self.styleN),
               Paragraph('<b>Nº Horas autonomas</b>',self.styleN),
               Paragraph('<b>Total horas</b>',self.styleN),
               Paragraph('<b>Fecha Creacion</b>',self.styleN),
               ]
        return data
    
    def estilos(self,valor):
        styleD = self.style["BodyText"]
        styleD.alignment = TA_LEFT
        styleD.fontSize = 10
        value = Paragraph(valor,styleD)
        return value


    def body_data(self):
        lista_disenio = DesignEvento.objects.all()
            
        data = []
        for ist in lista_disenio:
            data = [
            [
               self.estilos(ist.codigo),
               self.estilos(ist.nombre),
               self.estilos(ist.area),
               self.estilos(ist.especialidad),
               self.estilos(ist.tipo_evento),
               self.estilos(ist.modalidad),
               self.estilos(ist.tipo_certificado),
               self.estilos(ist.horas_presenciales),
               self.estilos(ist.horas_autonomas),
               self.estilos(ist.horas_totales),
               self.estilos(ist.fecha),
              ]
            ]
        return data
        
    

    def get(self, request, ):
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        pdf.setPageSize(landscape(A4))
        y = 590
        self.cabecera(pdf)
        self.pie_pagina(pdf)
        self.contenido(pdf, y)
        self.body_data()
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
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


