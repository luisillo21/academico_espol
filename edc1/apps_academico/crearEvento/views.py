from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse, HttpResponseForbidden
from django.forms.models import inlineformset_factory, modelformset_factory
from django.core import serializers
from rest_framework import viewsets
from .serializers import *
import json
from .models import Evento, Aula, Aliado, CalendarioEvento, Docente, Co, PubEvento
from apps_academico.diseñoEvento.models import DesignEvento, TipoEvento
from django.views.generic import CreateView,ListView,UpdateView,DeleteView, DetailView, View
from django.views.generic.edit import FormMixin
from .forms import EventoForm, AulaForm, AliadoForm, CalendarioForm, CalendarioFormSet, CoForm, CoFormSet, PubForm
#-------import para reportes----
from django.conf import settings
from io import BytesIO
from django.shortcuts import render, HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,yellow,black
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
    Paragraph)
#----------------------------------
# Create your views here.

#Api event
class TipoConvenioAliadoViewSet(viewsets.ModelViewSet):
    serializer_class = TipoConvenioAliadoSerializer
    queryset = TipoConvenioAliado.objects.all()

class AliadoViewSet(viewsets.ModelViewSet):
    serializer_class = AliadoSerializer
    queryset = Aliado.objects.all()

class DocenteViewSet(viewsets.ModelViewSet):
    serializer_class = DocenteSerializer
    queryset = Docente.objects.all()

class UnidadAulaViewSet(viewsets.ModelViewSet):
    serializer_class = UnidadAulaSerializer
    queryset = UnidadAula.objects.all()

class TipoAulaViewSet(viewsets.ModelViewSet):
    serializer_class = TipoAulaSerializer
    queryset = TipoAula.objects.all()

class EstadoAulaViewSet(viewsets.ModelViewSet):
    serializer_class = EstadoAulaSerializer
    queryset = EstadoAula.objects.all()    

class AulaViewSet(viewsets.ModelViewSet):
    serializer_class = AulaSerializer
    queryset = Aula.objects.all()

class EventoViewSet(viewsets.ModelViewSet):
    serializer_class = EventoSerializer
    queryset = Evento.objects.all()

class CalendarioEventoViewSet(viewsets.ModelViewSet):
    serializer_class = CalendarioEventoSerializer
    queryset = CalendarioEvento.objects.all()

class CoViewSet(viewsets.ModelViewSet):
    serializer_class = CoSerializer
    queryset = Co.objects.all()

class PubEventoViewSet(viewsets.ModelViewSet):
    serializer_class = PubEventoSerializer
    queryset = PubEvento.objects.all()

#Eventos
class CrearEvento(CreateView):
    model = Evento
    template_name = 'eventos/crearEvento.html'
    form_class = EventoForm
    success_url = reverse_lazy('listarEvento')
    
    def get_context_data(self, **kwargs):
        context = super(CrearEvento, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = CalendarioFormSet(queryset=CalendarioEvento.objects.none(), prefix='calendario')
        if 'form3' not in context:
            context['form3'] = CoFormSet(queryset=Co.objects.none(), prefix='cofaci')
        context['docente'] = Docente.objects.all()
        context['diseno'] = DesignEvento.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = CalendarioFormSet(request.POST, prefix='calendario')
        form3 = CoFormSet(request.POST, prefix='cofaci')
        print(form2.errors)
        
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            
            eve = form.save(commit=False)
            eve.save()
            instancesdia = form2.save(commit=False)
            for instanced in instancesdia:
                instanced.evento = eve
                instanced.save()
            instancesco = form3.save(commit=False)
            for instance in instancesco:
                instance.evento = eve
                instance.save()
            
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form='form',form2='form2',form3='form3'))


class ListarEvento(ListView):
    model=Evento
    template_name='eventos/listarEvento.html'
    queryset = Evento.objects.all()


class EditarEvento(UpdateView):
    model = Evento
    template_name='eventos/crearEvento.html'
    form_class=EventoForm
    success_url = reverse_lazy('listarEvento')

    def get_context_data(self, **kwargs):
        context = super(EditarEvento, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        evento = self.model.objects.get(codigo_evento=pk)
        calendarios_days = CalendarioEvento.objects.filter(id=evento.codigo_evento)
        co = Co.objects.filter(id=evento.codigo_evento)
        if 'form' not in context:
            context['form'] = self.form_class()
        """if 'form2' not in context:
            context['form2'] = CalendarioFormSet(queryset=CalendarioEvento.objects.filter(evento_id=evento.codigo_evento))
        if 'form3' not in context:
            context['form3'] = CoFormSet(queryset=Co.objects.filter(evento_id=evento.codigo_evento))
        context['id'] = pk"""
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_evento = kwargs['pk']
        evento = self.model.objects.get(codigo_evento=id_evento)
        calendarios_days = CalendarioEvento.objects.filter(evento_id=evento.codigo_evento)
        co = Co.objects.filter(id=evento.codigo_evento)
        form = self.form_class(request.POST, instance=evento)
        print(form.is_valid())
        """form2 = CalendarioFormSet(request.POST, queryset=CalendarioEvento.objects.filter(evento_id=evento.codigo_evento))
        print(form2.errors)
        form3 = CoFormSet(request.POST, queryset=Co.objects.filter(evento_id=evento.codigo_evento))
        #print(form3.errors)"""

        if form.is_valid(): #and form2.is_valid() and form3.is_valid():
            #evento_modificado = form.save(commit=False)
            form.save()
            """instances = form2.save(commit=False)
            instances2 = form3.save(commit=False)
            print(evento.codigo_evento)
            for ce in instances:
                ce.evento = evento
                ce.save()

            for c in instances2:
                c.evento = evento
                c.save()"""
            
            return HttpResponseRedirect(self.get_success_url())
        else:
            """if not form3.is_valid():
                print('form 3 no valida')
            if not form2.is_valid():
                print('form 2 no valida')"""
            if not form.is_valid():
                print('form 1 no son valida')
            return HttpResponseRedirect(self.get_success_url())

class EliminarEvento(DeleteView):
    model=Evento
    template_name="eventos/eliminarEvento.html"
    success_url=reverse_lazy('listarEvento')

#Aliados
class CrearAliado(CreateView):
    model=Aliado
    template_name="aliados/crearAliado.html"
    #success_message= 'El aliado ha sido creado con exito'
    form_class=AliadoForm
    success_url=reverse_lazy('listarAliado')

class ListarAliado(ListView):
    model=Aliado
    template_name="aliados/listarAliado.html"

class EditarAliado(UpdateView):
    model=Aliado
    template_name="aliados/crearAliado.html"
    form_class=AliadoForm
    success_url=reverse_lazy('listarAliado')

class EliminarAliado(DeleteView):
    model=Aliado
    template_name="aliados/eliminarAliado.html"
    success_url=reverse_lazy('listarAliado')

#Aulas
class CrearAula(CreateView):
    model = Aula
    template_name = 'aulas/crearAula.html'
    #success_message= 'El aula ha sido creada con exito'
    form_class = AulaForm
    success_url=reverse_lazy('listarAula')

class ListarAula(ListView):
    model=Aula
    template_name="aulas/listarAula.html"

class EditarAula(UpdateView):
    model=Aula
    template_name="aulas/crearAula.html"
    form_class=AulaForm
    success_url=reverse_lazy('listarAula')

class EliminarAula(DeleteView):
    model=Aula
    template_name="aulas/eliminarAula.html"
    success_url=reverse_lazy('listarAula')

class DiaCrear(CreateView):
    model = CalendarioEvento
    template_name = 'dias/crearDia.html'
    form_class = CalendarioForm
    success_url = reverse_lazy('listarDia')

class EditarDia(UpdateView):
    model = CalendarioEvento
    template_name = 'dias/crearDia.html'
    form_class = CalendarioForm
    success_url=reverse_lazy('listarDia')

class ListarDia(ListView):
    model = CalendarioEvento
    template_name = 'dias/listarDia.html'

class EliminarDia(DeleteView):
    model = CalendarioEvento
    template_name="dias/eliminarDia.html"
    success_url=reverse_lazy('listarDia')

class CrearPub(CreateView):
    model = PubEvento
    template_name='pub/crearPub.html'
    form_class = PubForm
    success_url=reverse_lazy('listarPub')

class ListarPub(ListView):
    model = PubEvento
    template_name = 'pub/listarPub.html'

class DetalleEvento(FormMixin, DetailView):
    model = Evento
    form_class = PubForm
    template_name='pub/crearPub.html'

    def get_context_data(self, **kwargs):
        context = super(DetalleEvento, self).get_context_data(**kwargs)
        #self.object.web = 'Publicado'
        #self.object.save(update_fields=['web'])
        return context

    def get_success_url(self):
        return reverse('listarEvento')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)

class infoEvento(DetailView):
    model = PubEvento
    template_name='pub/infoPub.html'

#consultas
def loadEventoName(request):
    event = Evento.objects.all()
    json_event = serializers.serialize('json', event)
    return HttpResponse(json_event, content_type='application/json')

#--------------Seccion de reportes----------------
class EventoPorCriterio(View):
    
    def cabecera(self, pdf):
        width, height = A4
        archivo_imagen = settings.MEDIA_ROOT+'/image_event/espol.png'
        pdf.drawImage(archivo_imagen, 10, 515, 230,
                      90, preserveAspectRatio=True)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(690 ,560, b"REPORTE DE EVENTOS")
        pdf.setFillColor(yellow)
        pdf.rect(748,540,78, 12, fill=True, stroke=False)
        pdf.setFillColor(black)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(750,540, u"POEC0502 V7")


    def pie_pagina(self, pdf):

        pdf.setFont("Helvetica", 10)
        now = datetime.now()
        pdf.drawString(10,45,'CEC ESPOL, Campus Gustavo Galindo Velasco | Teléf:042269763 | 0960507588')
        pdf.drawString(10, 30, u"Fecha impresión:"+str(now.day) +
                       '/'+str(now.month)+'/'+str(now.year))
        page_num = pdf.getPageNumber()
        text = "Pág. %s|1" % page_num
        pdf.drawString(28*cm, 30, text)
        pdf.drawString(7.1*cm, 30, u'Usuario: ')
        pdf.drawString(8.5*cm, 30, u'Luis Eduardo Ardila Macias')
        
        pdf.setFillColor(HexColor('#3c5634'))
        pdf.drawString(10, 60,"//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")

    def contenido(self, pdf, y):
        #Creamos una tupla de encabezados para neustra tabla
        width, height = A4
        styles = getSampleStyleSheet()
        styleN = styles["BodyText"]
        styleN.alignment = TA_CENTER
        Numero= Paragraph('<b>N.-</b>',styleN)
        Áreas =Paragraph('<b>Áreas</b>', styleN)
        Estados  =Paragraph('<b>Estados</b>', styleN)
        Inicio_Fin = Paragraph('<b>Inicio/ Fin</b>', styleN)
        Periodos=Paragraph('<b>Periodos</b>', styleN)
        Secuencial = Paragraph('<b>Secuencial</b>', styleN)
        Tipo_capacitación = Paragraph('<b>Por sede</b>', styleN)
        sede = Paragraph('<b>Por sede</b>', styleN)
        Público = Paragraph('<b>Público</b>', styleN)
        Coordinador_a = Paragraph('<b>Coordinador/a</b>', styleN)
        Asesor_a = Paragraph('<b>Asesor/a</b>', styleN)
        Aula = Paragraph('<b>Aula</b>', styleN)
        encabezado1 = [
                        [Numero,Áreas,Estados,Inicio_Fin,Periodos,Secuencial,Tipo_capacitación,sede,Público,Coordinador_a,Asesor_a,Aula],
                        ['1','','','','','','','','','','',''],
                        ['2','','','','','','','','','','',''],
                        ['3','','','','','','','','','','',''],
                        ['4','','','','','','','','','','','']
                      ]
        #encabezado2 = [[Numero,Sesion,Fecha,Firma,Hora_de_entrada_planificada,Hora_de_salida_planificada,Hora_de_entrada_ejecutada,Hora_de_salida_ejecutada]]
        t = Table(encabezado1, colWidths=[1*cm,2.5*cm,2.5*cm,4*cm,3.5*cm,2.5*cm,2*cm,2*cm,2*cm,2.9*cm,2*cm,2*cm])
        t.setStyle(TableStyle([
            ('BOX', (0, 0), (-1,-1), 0.20, colors.black),
            ('INNERGRID', (0,0), (-1, -1),0.10,colors.black),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('BOTTOMPADDING',(0,0),(-1,-1),3),
        ]))
        t.wrapOn(pdf,width,height)
        t.drawOn(pdf,8,420)

    def get(self, request, ):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer, pagesize=A4)
        pdf.setPageSize(landscape(A4))
        #Llamo al método donde están definidos los datos que aparecen en el reporte.
        y = 590
        self.cabecera(pdf)
        self.pie_pagina(pdf)
        self.contenido(pdf, y)
        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


class Eventos_Ejecutados(View):
    style = getSampleStyleSheet()

    def cabecera(self, pdf):
        width, height = A4
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
        styles = getSampleStyleSheet()
        styleN = styles["BodyText"]
        styleN.alignment = TA_CENTER
        styleN.fontSize = 8
        col_1 = Paragraph('<b>N.-</b>', styleN)
        col_2 = Paragraph('<b>Codigo diseño</b>', styleN)
        col_3 = Paragraph('<b>Version</b>', styleN)
        col_4 = Paragraph('<b>Nombre del Evento</b>', styleN)
        col_5 = Paragraph('<b>Area</b>', styleN)
        col_6 = Paragraph('<b>Especialidad</b>', styleN)
        col_7 = Paragraph('<b>Tipo Evento</b>',styleN)
        col_8 = Paragraph('<b>Modalidad</b>',styleN)
        col_9 = Paragraph('<b>Tipo certificado</b>',styleN)
        col_10= Paragraph('<b>Horas presenciales</b>',styleN)
        col_11 = Paragraph('<b>Nº Horas autonomas</b>',styleN)
        col_12 = Paragraph('<b>Total horas</b>',styleN)
        col_13 = Paragraph('<b>Fecha Creacion</b>',styleN)
        encabezado1 = [
            [col_1,col_2,col_3,col_4,col_5,col_6,col_7,col_8,col_9,col_10,col_11,col_12,col_13],
            ['1','','','','','','','','','','','',''],
            ['2','','','','','','','','','','','',''],
            ['3','','','','','','','','','','','',''],
            ['4','','','','','','','','','','','','']
        ]

        t = Table(encabezado1, colWidths=[
                  0.9*cm,2*cm,2*cm,5*cm,2*cm,2.5*cm,2.2*cm,2.2*cm,2*cm,2.2*cm,2*cm,1.8*cm, 2*cm])
        t.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.10, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.10, colors.black),
            ('BOTTOMPADDING', (2, 0), (2, 0), 9),
            ('BOTTOMPADDING', (3, 0), (3, 0), 9),
            ('BOTTOMPADDING', (4, 0), (4, 0), 9),
            ('BOTTOMPADDING', (5, 0), (5, 0), 9),
            ('BOTTOMPADDING', (6, 0), (6, 0), 9),
            ('BOTTOMPADDING', (7, 0), (7, 0), 9),
        ]))

        t.wrapOn(pdf,width,height)
        t.drawOn(pdf, 8, 380)
        #Formulario Inferior
        styleB = styles["BodyText"]
        styleB.alignment = TA_LEFT
        styleB.fontSize = 10
        var_1 = Paragraph('<b>Total diseños</b>', styleB)
        var_2 = Paragraph('<b>Total por modalidad</b>', styleB)
        var_3 = Paragraph('<b>Total Diseño por área</b>', styleB)
        var_4 = Paragraph('<b>Total tipo certificado</b>', styleB)
        var_5 = Paragraph('<b>Total tipo evento</b>', styleB)
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

        t_form.wrapOn(pdf, width, height)
        t_form.drawOn(pdf, 8, 90)

    def get(self, request, ):
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        pdf.setPageSize(landscape(A4))
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

class Registro_asistencia_evento(View):
    def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = settings.MEDIA_ROOT+'/image_event/espol.png'
        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 740, 190, 90,preserveAspectRatio=True)
        #Se dibuja una linea horizontal
        pdf.line(260,740,35,740)
        # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Times-Roman", 10)
        # Dibujamos una cadena en la ubicación X,Y especificada
        pdf.drawString(315, 790, b" REGISTRO DE ASISTENCIA POR EVENTO")
        pdf.drawString(426, 774, u"CÓDIGO EVENTO ")
        pdf.drawString(466, 761, u"########")
        pdf.drawString(35, 720, u"Programa:") ; pdf.drawString(260, 720, u"Duración:")
        pdf.drawString(35, 705, u"Promoción:") ; pdf.drawString(260, 705, u"Fecha Inicio:")
        pdf.drawString(35, 690, u"Curso:") ; pdf.drawString(260, 690, u"Fecha Final:")
        pdf.drawString(35, 675, u"Instructor:") ; pdf.drawString(260, 675, u"Tipo de Capacitación:")
        pdf.drawString(415,660,"CONTROL DE ASISTENCIA")


    def pie_pagina(self,pdf):
        pdf.setFillColor(HexColor(308011))
        pdf.drawString(10, 60, u" /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
        pdf.setFillColor(HexColor(000000))
        page_num = pdf.getPageNumber()
        text = "Pag %s" % page_num
        pdf.drawString(500, 30, text)
        pdf.drawString(35,50 ,u'CEC ESPOL, Campus Gustavo Galindo Velasco | Teléf:042269763 | 0960507588 ')
        now = datetime.now()
        pdf.drawString(35,35, u"Fecha impresión:"+str(now.day)+'/'+str(now.month)+'/'+str(now.year))
        pdf.drawString(260, 35,u'Usuario')

    def tabla(self,pdf,y):
        #Creamos una tupla de encabezados para neustra tabla
        styles = getSampleStyleSheet()
        styleN = styles["BodyText"]
        styleN.alignment = TA_LEFT
        styleBH = styles["Normal"]
        styleBH.alignment = TA_CENTER
        hnum = Paragraph('''<b>N.-</b>''', styleBH)
        hcedula = Paragraph('''<b>Cedula</b>''', styleBH)
        hnombre = Paragraph('''<b>Nombre</b>''', styleBH)
        hfirma = Paragraph('''<b>Firma</b>''', styleBH)
        hentrada = Paragraph('''<b>H.Entrada</b>''', styleBH)
        hsalida = Paragraph('''<b>H.Salida</b>''', styleBH)
        #hcargo = Paragraph('''<b>Cargo</b>''', styleBH)
        #harea = Paragraph('''<b>Área</b>''', styleBH)
        
        encabezados = (hnum,hcedula,hnombre,hfirma,hentrada,hsalida,"","","","","","","","","","")#hprofesion,hcargo,harea)
        encabezados2=("","","","","")
        #Creamos una lista de tuplas que van a contener a las personas
        detalles = [('0'),('1')]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados2,encabezados] + detalles, colWidths=[1 * cm,2*cm, 2 * cm, 2 * cm, 2.5 * cm,2.5*cm,0.5*cm])
        #Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(2,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 1), (-1, -1), 0.5, colors.black), 
                ('GRID', (6, 0), (-1, -1), 0.5, colors.black),
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (6, 0), (-1, 0), 40),

            ]
        ))
        #Establecemos el tamaño de la hoja que ocupará la tabla 
        detalle_orden.wrapOn(pdf, 850, 650)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 65,y-50)
    def get(self, request, ):
            
            #Indicamos el tipo de contenido a devolver, en este caso un pdf
            response = HttpResponse(content_type='application/pdf')
            #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
            buffer = BytesIO()
            #Canvas nos permite hacer el reporte con coordenadas X y Y
            pdf = canvas.Canvas(buffer)
            #Llamo al método donde están definidos los datos que aparecen en el reporte.
            y = 590 
            self.cabecera(pdf)
            self.pie_pagina(pdf)
            self.tabla(pdf,y)
            #Con show page hacemos un corte de página para pasar a la siguiente
            pdf.showPage()
            pdf.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            return response