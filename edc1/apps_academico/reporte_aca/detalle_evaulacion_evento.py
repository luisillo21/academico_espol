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

class Detalle_evaulacion_evento(View):
    def cabecera(self,pdf):
        archivo_imagen = settings.MEDIA_ROOT+'/image_event/espol.png'
        pdf.drawImage(archivo_imagen, 40, 740, 190, 90,preserveAspectRatio=True)
        pdf.line(260,740,35,740)
        pdf.setFont("Times-Roman", 10)
        pdf.drawString(325, 790, b"DETALLE DE EVAULACION DEL EVENTO")
        pdf.drawString(426, 774, u"CÓDIGO EVENTO ")
        pdf.drawString(466, 761, u"########") ; pdf.drawString(260,720,"Aula") ; pdf.drawString(400, 720, u"Horario:") 
        pdf.drawString(35, 720, u"Programa:") ; pdf.drawString(260, 705, u"Duración:")
        pdf.drawString(35, 705, u"Promoción:") ; pdf.drawString(260, 690, u"Fecha Inicio:")
        pdf.drawString(35, 690, u"Curso:") ; pdf.drawString(260, 675, u"Fecha Final:")
        pdf.drawString(35, 675, u"Tipo de Capacitación:")


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
        styles = getSampleStyleSheet()
        styleN = styles["BodyText"]
        styleN.alignment = TA_LEFT
        styleBH = styles["Normal"]
        styleBH.fontSize = 8
        styleBH.alignment = TA_CENTER

        va1 = Paragraph('''<b></b>''', styleBH)
        va2 = Paragraph('''<b>Participante</b>''', styleBH)
        va3 = Paragraph('''<b>Evaulación Dianostica (/100)</b>''', styleBH)
        va4 = Paragraph('''<b>*(Nombre y peso de la actividad 1)(/100)</b>''', styleBH)
        va5 = Paragraph('''<b>*(Nombre y peso de la actividad 2)(/100)</b>''', styleBH)
        va6 = Paragraph('''<b>*(Nombre y peso de la actividad 3)(/100)</b>''', styleBH)
        va7 = Paragraph('''<b>Promedio de Actividades(/100)</b>''', styleBH)
        va8 = Paragraph('''<b>Prueba final (/100)</b>''', styleBH)
        va9 = Paragraph('''<b>Nota final (/100)</b>''', styleBH)
        va10 = Paragraph('''<b>**Observación</b>''', styleBH)
        enc= Paragraph('''Representante el 40% de la nota final''',styleBH)
        encabezados = (va1,va2,va3,va4,va5,va6,va7,va8,va9,va10)
        encabezados2=(' ',' ',' ','Representa el 60% de la nota final','','','','',enc)
        #Creamos una lista de tuplas que van a contener a las personas
        detalles = [('0'),('1')]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados2,encabezados,] + detalles, colWidths=[0.5 * cm,2.2*cm, 2* cm, 2 * cm, 2 * cm,2*cm,2*cm,2*cm,2*cm,3*cm])
        #Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(2,0),'CENTER'),
                ('ALIGN',(0,0),(3,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (9,0), (-1, -1), 0.5, colors.black),
                ('GRID', (10,1), (-1, -1), 0.5, colors.black),
                ('GRID', (0, 1), (-1, -1), 0.5, colors.black),
                ('GRID',(3,0), (-1, -1), 0.5, colors.black),
                #('BACKGROUND',(3,0),(-1,-1),colors.green),
                #('BACKGROUND',(3,1),(-1,-1),colors.green),
                ('SPAN',(0,0),(2,0)),
                ('SPAN',(3,0),(7,0)),
                ('BOTTOMPADDING',(3,0),(0,1)),
                
                #El tamaño de las letras de cada una de las celdas será de 10
                #('FONTSIZE', (0, 0), (-1, -1), 10),
                #('BOTTOMPADDING', (6, 0), (-1, 0), 40),

            ]
        ))
        detalle_orden.wrapOn(pdf, 850, 650)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 15,y-80)
    def get(self, request, ):
            
            response = HttpResponse(content_type='application/pdf')
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer)
            y = 590 
            self.cabecera(pdf)
            self.pie_pagina(pdf)
            self.tabla(pdf,y)
            pdf.showPage()
            pdf.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            return response