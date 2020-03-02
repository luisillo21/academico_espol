from django.shortcuts import render
from django.views.generic import *
from django.shortcuts import *
from .models import *
from django.http import *
from functools import reduce
from operator import add
from django.conf import settings
from io import BytesIO
from django.shortcuts import render, HttpResponse
from django.views.generic import View
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

# Create your views here.
class DocenteFill(TemplateView):
    template_name='docente/fill.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        docente_id = self.kwargs['docente_pk']
        context['docente_id'] = docente_id
        return context

class DocenteCheck(TemplateView):
    template_name='docente/check.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        docente_id = self.kwargs['docente_pk']
        context['docente_id'] = docente_id
        return context

def docente_score(request,docente_pk):
    ms = {
        'actualizacionAcademica' : ActualizacionAcademica,
        'formacionDocente' : FormacionDocente,
        'experienciaDocente' : ExperienciaDocente,
        'perfil' : Perfil
    }
    score = {}
    for key, model in ms.items():
        try:
            queryset = get_list_or_404(model,docente_id = docente_pk)
            hours = list(map(lambda x: x.duracion_en_horas, queryset))
            total_hours = reduce(add, hours)            
            score[key] = total_hours
        except Http404:
            score[key] = 0
    return JsonResponse(score)

#-------Seccion de reportes------------------
# ---------Registro de asistencias del docente------------ 
class AsistenciasDocentePDF(View):
    style = getSampleStyleSheet()
    def cabecera(self, pdf):
        width, height = A4
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = settings.MEDIA_ROOT+'/image_event/espol.png'
        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 10, 760, 230,
                      90, preserveAspectRatio=True)
        #Se dibuja una linea horizontal
        #pdf.line(260, 740, 35, 740)
        # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Helvetica-Bold", 10)
        # Dibujamos una cadena en la ubicación X,Y especificada
        pdf.drawString(373,810, b"REGISTRO DE ASISTENCIAS DEL DOCENTE")
        pdf.setFillColor(yellow)
        pdf.rect(520,791, 67, 12, fill=True, stroke=False)
        pdf.setFillColor(black)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(520,793, u"POEC0502 V7")
        #pdf.drawString(466, 761, u"########")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(10, 740, u"Evento: ")
        pdf.drawString(260,740,u"Aula:")
        pdf.drawString(430,740,u"Horario:")
        pdf.drawString(10, 720, u"Promoción:")
        pdf.drawString(260,720,u"Fecha de Inicio: ")
        pdf.drawString(10, 700, u"Módulo: ")
        pdf.drawString(260,700,u"Fecha Fin: ")
        pdf.drawString(10, 680, u"Docente: ")
        pdf.drawString(260,680,u"Duración: ")

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
        #Creamos una tupla de encabezados para neustra tabla
        width, height = A4
        styles = getSampleStyleSheet()
        styleN = styles["BodyText"]
        styleN.alignment = TA_CENTER
        Numero= Paragraph('<b>N.-</b>',styleN)
        Sesion =Paragraph('<b>Sesión</b>', styleN)
        Fecha  =Paragraph('<b>Fecha</b>', styleN)
        Firma = Paragraph('<b>Firma</b>', styleN)
        Hora_de_entrada_planificada=Paragraph('<b>H.Entrada</b>', styleN)
        Hora_de_salida_planificada =Paragraph('<b>H.Salida</b>', styleN)
        Hora_de_entrada_ejecutada = Paragraph('<b>H.Entrada</b>', styleN)
        Hora_de_salida_ejecutada =  Paragraph('<b>H.Entrada</b>', styleN)
        Planificada = Paragraph('<b>Planificada</b>', styleN)
        Ejecutada =   Paragraph('<b>Ejecutada</b>', styleN)
        encabezado1 = [
                        ['','','','',Planificada,'',Ejecutada,''],
                        [Numero,Sesion,Fecha,Firma,Hora_de_entrada_planificada,Hora_de_salida_planificada,Hora_de_entrada_ejecutada,Hora_de_salida_ejecutada],
                        ['1','','','','','','',''],
                        ['2','','','','','','',''],
                        ['3','','','','','','',''],
                        ['4','','','','','','','']
                      ]
        #encabezado2 = [[Numero,Sesion,Fecha,Firma,Hora_de_entrada_planificada,Hora_de_salida_planificada,Hora_de_entrada_ejecutada,Hora_de_salida_ejecutada]]
        t = Table(encabezado1, colWidths=[1*cm,2*cm,3*cm,5*cm,2.3*cm,2.3*cm,2.3*cm,2.3*cm])
        t.setStyle(TableStyle([
            ('BOX', (4, 0), (-1,0), 0.30, colors.black),
            ('INNERGRID', (4, 0), (-1, 0),0.10,colors.black),
            ('BOX', (0, 1), (-1,-1), 0.20, colors.black),
            ('INNERGRID', (0, 1), (-1, -1),0.10,colors.black),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('SPAN',(4,0),(5,0)),
            ('SPAN',(6,0),(7,0)),
            ('BOTTOMPADDING',(0,0),(-1,-1),3),
        ]))
        t.wrapOn(pdf,width,height)
        t.drawOn(pdf,10,550)

    def get(self, request, ):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer, pagesize=A4)
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


class DocentePorCriterio(View):
    style = getSampleStyleSheet()

    def cabecera(self, pdf):
        width, height = A4
        archivo_imagen = settings.MEDIA_ROOT+'/image_event/espol.png'
        pdf.drawImage(archivo_imagen, 10, 500, 230,
                      90, preserveAspectRatio=True)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(650, 550, b"Reporte de eventos por genero")
        pdf.setFillColor(yellow)
        pdf.rect(760, 526, 67, 14, fill=True, stroke=False)
        pdf.setFillColor(black)
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(760, 530, u"POEC0502 V7")
        pdf.drawString(10,480,'Ruc:')
        pdf.drawString(180,480,'Empresa:')

    def pie_pagina(self, pdf):
        pdf.setFont("Helvetica", 10)
        now = datetime.now()
        pdf.drawString(
            10, 45, 'CEC ESPOL, Campus Gustavo Galindo Velasco | Teléf:042269763 | 0960507588 ')
        pdf.drawString(10, 30, u"Fecha impresión:"+str(now.day) +
                       '/'+str(now.month)+'/'+str(now.year))
        page_num = pdf.getPageNumber()
        text = "Pág. %s|1" % page_num
        pdf.drawString(500, 30, text)
        pdf.drawString(200, 30, u'Usuario: ')
        pdf.drawString(240, 30, u'Luis Eduardo Ardila Macias')
        pdf.setFillColor(HexColor('#3c5634'))
        pdf.drawString(10, 60, "//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")

    def contenido(self, pdf, y):
        width, height = A4
        styles = getSampleStyleSheet()
        styleN = styles["BodyText"]
        
        styleN.fontSize = 9
       
        styleN.alignment = TA_CENTER
       
        var_1 = Paragraph('<b>N.-</b>', styleN)
        var_2 = Paragraph('<b>Cedula</b>', styleN)
        var_3 = Paragraph('<b>Estados</b>', styleN)
        var_4 = Paragraph('<b>Apellidos</b>', styleN)
        var_5 = Paragraph('<b>Nombres</b>',styleN)
        var_6 = Paragraph('<b>Genero</b>', styleN)
        var_7 = Paragraph('<b>Correo</b>', styleN)
        var_8 = Paragraph('<b>Telefono fijo</b>', styleN)
        var_9 = Paragraph('<b>Celular</b>', styleN)
        var_10 = Paragraph('<b>Título</b>', styleN)
        var_11 = Paragraph('<b>Cursos dictados en CEC</b>', styleN)
        var_12 = Paragraph('<b>Último costo hora</b>', styleN)
        var_13 = Paragraph('<b>Promedio de Evaluaciones</b>', styleN)
        var_14 = Paragraph('<b>Áreas especialidad ( SETEC )</b>', styleN)
        var_15 = Paragraph('<b>Estado</b>', styleN)

        styleC = styles["BodyText"]
        styleC.fontSize = 9
        styleC.alignment = TA_LEFT
        #var_16 = Paragraph('<b>Zambrano Zambrano</b>', styleC)

        


        encabezado1 = [
            [var_1,var_2,var_3,var_4,var_5,var_6,var_7,var_8,var_9,var_10,var_11,var_12,var_13,var_14,var_15],
            ['1', '', '','','', '','','','','','','','','',''],
            ['2', '', '', '','', '','','','','','','','','',''],
            ['3', '', '', '','', '','','','','','','','','',''],
            ['4', '', '', '','', '','','','','','','','','','']
        ]

        t = Table(encabezado1, colWidths=[
                  1*cm, 2*cm, 2*cm, 2*cm,2*cm, 2*cm,2*cm,2*cm,2*cm,2*cm,2*cm,2*cm,2*cm,2.5*cm,1.5*cm])
        t.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.20, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.10, colors.black),

        ]))

        t.wrapOn(pdf, width, height)
        t.drawOn(pdf, 8, 360)
        
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
