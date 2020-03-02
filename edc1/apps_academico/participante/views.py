from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.decorators import *
from rest_framework.renderers import *
from django.http import JsonResponse
from .models import *
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist
import datetime
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
    Paragraph)
#----------------------------------
# Create your views here.

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def asistencia_by_evento_and_fecha(request):
    evento_id = request.GET.get('evento_id', None)
    fecha = request.GET.get('fecha', None)

    try:
        fecha_object = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
        asistencia = Asistencia.objects.get(
            evento_id=evento_id,
            fecha=fecha_object
        )
        serializer = AsistenciaSerializer(asistencia)
        return Response(serializer.data)
    except ValueError:
        return JsonResponse({
            'detail': 'Either evento or fecha is null'
        }, status=400)
    except TypeError:
        return JsonResponse({
            'detail': 'Fecha parameter was missing'
        }, status=400)
    except ObjectDoesNotExist:
        return JsonResponse({
            'detail': '. Not found'
        }, status=404)

#---------Seccion de reportes-------------------------


class ParticipantesReprobados(View):
    style = getSampleStyleSheet()

    def cabecera(self, pdf):
        width, height = A4
        archivo_imagen = settings.MEDIA_ROOT+'/image_event/espol.png'
        pdf.drawImage(archivo_imagen, 10, 760, 230,
                      90, preserveAspectRatio=True)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(410, 810, b"Reporte de eventos por genero")
        pdf.setFillColor(yellow)
        pdf.rect(520, 791, 67, 12, fill=True, stroke=False)
        pdf.setFillColor(black)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(520, 793, u"POEC0502 V7")

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
        styleN.alignment = TA_CENTER
        Numero = Paragraph('<b>N.-</b>', styleN)
        Codigo = Paragraph('<b>Codigo</b>', styleN)
        N_evento = Paragraph('<b>Nombre del evento</b>', styleN)
        Cedula = Paragraph('<b>Cedula</b>', styleN)
        N_part = Paragraph('<b>Nombre del Participante</b>',styleN)
        Asistencia = Paragraph('<b>Asistencia</b>', styleN)
        N_final = Paragraph('<b>Nota final</b>', styleN)
        encabezado1 = [
            [Numero, Codigo, N_evento, Cedula, N_part , Asistencia, N_final],
            ['1', '', '', '','', '%', ''],
            ['2', '', '', '','',  '', ''],
            ['3', '', '', '','',  '', ''],
            ['4', '', '', '','',  '', '']
        ]

        t = Table(encabezado1, colWidths=[
                  1*cm, 2*cm, 5*cm, 3.1*cm,5*cm, 2.3*cm,2*cm])
        t.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.20, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.10, colors.black),
            ('BOTTOMPADDING', (0, 0), (5,0), 10),
        ]))

        t.wrapOn(pdf, width, height)
        t.drawOn(pdf, 8, 650)
        #Formulario Inferior
        styleB = styles["BodyText"]
        styleB.alignment = TA_LEFT
        var_1 = Paragraph('<b>Total reprobados por asistencia</b>', styleB)
        var_2 = Paragraph('<b>Total por Evento</b>', styleB)
        var_3 = Paragraph('<b>Total reprobados por  calificación</b>', styleB)
        var_4 = Paragraph('<b>Total inscritos personalmente</b>',styleB)
        var_5 = Paragraph('<b>Total inscritos Auspiciados </b>', styleB)
        form_inferior = [
                          [var_1 ,'Σ total','Asistencia minina del 80%',var_2,'Σ total'],
                          [var_3,'Σ total','Nota mínima 70/100',var_4,'Σ total'],
                          ['', '', '', var_5, 'Σ total']
                        ]
        t_form = Table(form_inferior, colWidths=[
                  5*cm, 2*cm, 4.5*cm, 5*cm,4*cm])
        t_form.setStyle(TableStyle([
            ('BOTTOMPADDING', (3, 0), (3,0),15),
            ('BOTTOMPADDING', (1, 0), (1,0),15),
            ('BOTTOMPADDING', (1, 1), (1,1),15),
            ('BOTTOMPADDING', (2, 0), (2,0),15),
            ('BOTTOMPADDING', (2, 1), (2,1), 15),
            ('BOTTOMPADDING', (4, 0), (4, 0), 15),
            ('BOTTOMPADDING', (4, 1), (4, 1), 15),
            ('BOTTOMPADDING', (4, 2), (4, 2), 15),
        ]))

        t_form.wrapOn(pdf, width, height)
        t_form.drawOn(pdf, 8, 90)


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

#---------------------------------------
class Perfil_participante(View):
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
        pdf.drawString(390, 790, b" PERFIL DE PARTICIPANTES")
        pdf.drawString(426, 774, u"CÓDIGO EVENTO ")
        pdf.drawString(466, 761, u"########")
        pdf.drawString(35, 720, u"Programa:") ; pdf.drawString(260, 720, u"Duración:")
        pdf.drawString(35, 705, u"Promoción:") ; pdf.drawString(260, 705, u"Fecha Inicio:")
        pdf.drawString(35, 690, u"Curso:") ; pdf.drawString(260, 690, u"Fecha Final:")
        pdf.drawString(35, 675, u"Instructor:") ; pdf.drawString(260, 675, u"Tipo de Capacitación:")


    def pie_pagina(self,pdf):
        pdf.setFillColor(HexColor(308011))
        pdf.drawString(10, 60, u" /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
        pdf.setFillColor(HexColor(000000))
        page_num = pdf.getPageNumber()
        text = "Pag %s |1 " % page_num
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
        hnum = Paragraph('''<b>N°.-</b>''', styleBH)
        hcedula = Paragraph('''<b>Cedula</b>''', styleBH)
        hnombre = Paragraph('''<b>Nombre</b>''', styleBH)
        htitulo3 = Paragraph('''<b>Titulo tercer nivel</b>''', styleBH)
        htitulo4 = Paragraph('''<b>Titulo cuarto nivel</b>''', styleBH)
        hprofesion = Paragraph('''<b>Profesion</b>''', styleBH)
        hcargo = Paragraph('''<b>Cargo</b>''', styleBH)
        harea = Paragraph('''<b>Área</b>''', styleBH)
        encabezados = (hnum,hcedula,hnombre,htitulo3,htitulo4,hprofesion,hcargo,harea)
        #Creamos una lista de tuplas que van a contener a las personas
        detalles = [('0')]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados] + detalles, colWidths=[0.9 * cm, 2 * cm, 2 * cm, 2.5 * cm,2.5*cm,2.5*cm,2*cm])
        #Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(2,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black), 
                #('SPAN',(-1,-1),(-3-1)),
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))
        #Establecemos el tamaño de la hoja que ocupará la tabla 
        detalle_orden.wrapOn(pdf, 850, 650)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 60,y)
    def get(self, request, ):
            
            #Indicamos el tipo de contenido a devolver, en este caso un pdf
            response = HttpResponse(content_type='application/pdf')
            #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
            buffer = BytesIO()
            #Canvas nos permite hacer el reporte con coordenadas X y Y
            pdf = canvas.Canvas(buffer)
            #Llamo al método donde están definidos los datos que aparecen en el reporte.
            y = 600
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


#--------------------------------
class Conctacto_participante(View):
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
        pdf.drawString(365, 790, b"CONTACTO DE PARTICIPANTE")
        pdf.drawString(426, 774, u"CÓDIGO EVENTO ")
        pdf.drawString(466, 761, u"########")
        pdf.drawString(35, 720, u"Evento:") ; pdf.drawString(260, 720, u"Aula:"); pdf.drawString(410, 720, u"Horario:")
        pdf.drawString(35, 705, u"Promoción:") ; pdf.drawString(260, 705, u"Fecha Inicio:")
        pdf.drawString(35, 690, u"Módulo:") ; pdf.drawString(260, 690, u"Fecha Final:")
        pdf.drawString(35, 675, u"Tipo de capacitación:") ; pdf.drawString(260, 675, u"Duración:")


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
        width, height = A4
        styles = getSampleStyleSheet()
        styleN = styles["BodyText"]
        styleN.alignment = TA_LEFT
        styleBH = styles["Normal"]
        styleBH.alignment = TA_CENTER
        hparticipante = Paragraph('''<b>PARTICIPANTE</b>''', styleBH)
        hemail1 = Paragraph('''<b>Email1</b>''', styleBH)
        hemail2 = Paragraph('''<b>Email2</b>''', styleBH)
        hcelular = Paragraph('''<b>Celular</b>''', styleBH)
        htelf_domicilio = Paragraph('''<b>Telefono Domicilio</b>''', styleBH)
        htelf_trabajo = Paragraph('''<b>Telefono Trabajo</b>''', styleBH)
        hdireccion = Paragraph('''<b>Dirección</b>''', styleBH)
        nombre= Paragraph('''Steen''',styleBH)
        #harea = Paragraph('''<b>Área</b>''', styleBH)
        encabezados = ('',hparticipante,hemail1,hemail2,hcelular,htelf_domicilio,htelf_trabajo,hdireccion)
        #Creamos una lista de tuplas que van a contener a las personas
        detalles = [('1',nombre,'')]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados] + detalles, colWidths=[0.5*cm,3.5 * cm, 2 * cm, 2 * cm, 2.5 * cm,2.5*cm,2.5*cm,2.5*cm])
        #Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(2,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('BOX', (1, 0), (-1, -1), 0.20, colors.black),
                ('GRID', (1, 0), (-1,-1), 0.5, colors.black), 
                 ('GRID', (0, 1), (0,1), 0.5, colors.black), 
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))
        #Establecemos el tamaño de la hoja que ocupará la tabla 
        detalle_orden.wrapOn(pdf,width, height)
        
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf,60,y)
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