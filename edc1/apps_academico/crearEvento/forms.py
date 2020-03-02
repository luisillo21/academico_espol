from django import forms
from .models import Evento,Aliado,Aula, CalendarioEvento, Co, PubEvento
from ckeditor.widgets import CKEditorWidget
from django.forms.models import inlineformset_factory, modelformset_factory

OPTIONS_EVENTO = (
    ('Diplomado', 'Diplomado'),
    ('Programa', 'Programa'),
    ('Curso', 'Curso'),
    ('Conferencia', 'Conferencia'),
    ('Taller', 'Taller'),
    ('Webinario', 'Webinario'),
    ('Charla', 'Charla'),
    ('Modulo', 'Modulo'),
)

OPTIONS_MODALIDAD = (
    ('Presencial', 'Presencial'),
    ('Semi-virtual', 'Semi-Virtual'),
    ('Virtual', 'Virtual'),   
)

OPTIONS_SERVICIOS = (
    ('Break', 'Break'),
    ('Almuerzo', 'Almuerzo'),
    ('Computadora por participante', 'Computadora por participante'),   
)

OPTIONS_CALENDAR = (
    ('Lunes a Viernes', 'Lunes a Viernes'),
    ('Sabados y Domingos', 'Sabados y Domingos'),
    ('Personalizado', 'Personalizado'),   
)

OPTIONS_ORIGEN = {
    ('Nacional', 'Nacional'),
    ('Internacional', 'Internacional'),  
}

OPTIONS_ASESOR = {
    ('Asesor1', 'Asesor1'),
    ('Asesor2', 'Asesor2'),
    ('Asesor3', 'Asesor3'),
}

OPTIONS_PUBLICO = {
    ('Abierto', 'Abierto'),
    ('Corporativo', 'Corporativo'),  
}

class EventoForm(forms.ModelForm):

    class Meta:
        model = Evento

        fields = [
            'diseno',
            'codigo_evento',
            'nombre',
            'tipo_evento',
            'codigo_evento_padre',
            'nombre_evento_Padre',
            'modalidad',
            'centro_costos',
            'alcance',
            'promocion',
            'duracion',
            'aliado',
            'docente',
            #'co_facilitador',
            'lugar',
            'asesor_comercial_responsable',
            'publico',
            'servicios_incluidos',
            'hora_break',
            'hora_almuerzo',
            'opciones_de_calendario',
            'fecha_inicio',
            'fecha_fin',
            'estado',
            'web',
        ]

        labels = {
            'diseno': 'Diseño',
            'codigo_evento': 'Cód. evento',
            'nombre': 'Nombre del evento',
            'tipo_evento': 'Tipo evento',
            'codigo_evento_padre': 'Evento Padre',
            'nombre_evento_Padre': 'Nombre de evento padre',
            'modalidad': 'Modalidad',
            'centro_costos': 'Centro de costos',
            'alcance': 'Alcance',
            'promocion': 'Promocion',
            'duracion': 'Duración',
            'aliado': 'Aliado',
            'docente': 'Asignar Docente',
            #'co_facilitador': 'Asignar co-faciliatdor',
            'lugar': 'Lugar',
            'asesor_comercial_responsable': 'Asesor Comercial responsable',
            'publico': 'Publico',
            'servicios_incluidos': 'Servicios incluidos',
            'hora_break': 'Horario break',
            'hora_almuerzo': 'Horario almuerzo',
            'opciones_de_calendario': 'Opciones para generar calendario del evento',
            'fecha_inicio': 'Fecha inicio',
            'fecha_fin': 'Fecha fin',
            'estado': 'Estado',
            'web': 'Web',
        }
       
        widgets = {
            'diseno': forms.Select(attrs={'class':'form-control'}),
            'codigo_evento': forms.TextInput(attrs={'class':'form-control'}),
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'tipo_evento': forms.TextInput(attrs={'class':'form-control'}),
            'codigo_evento_padre': forms.Select(attrs={'class':'form-control'}),
            'nombre_evento_Padre': forms.TextInput(attrs={'class':'form-control'}),
            'modalidad': forms.TextInput(attrs={'class':'form-control'}),
            'centro_costos': forms.TextInput(attrs={'class':'form-control'}),
            'alcance': forms.Select(attrs={'class':'form-control'}, choices=OPTIONS_ORIGEN),
            'promocion': forms.TextInput(attrs={'class':'form-control'}),
            'duracion': forms.NumberInput(attrs={'class':'form-control'}),
            'aliado': forms.Select(attrs={'class':'form-control'}),
            'docente': forms.Select(attrs={'class':'form-control'}),
            #'co_facilitador': forms.Select(attrs={'class':'form-control'}),
            'lugar': forms.TextInput(attrs={'class':'form-control'}),
            'asesor_comercial_responsable': forms.Select(attrs={'class':'form-control'},choices=OPTIONS_ASESOR),
            'publico': forms.Select(attrs={'class':'form-control'}, choices=OPTIONS_PUBLICO),
            'servicios_incluidos': forms.CheckboxSelectMultiple(choices=OPTIONS_SERVICIOS),
            'hora_break': forms.TimeInput(attrs={'class':'form-control', 'type':'time'}),
            'hora_almuerzo': forms.TimeInput(attrs={'class':'form-control', 'type':'time'}),
            'opciones_de_calendario': forms.RadioSelect(choices=OPTIONS_CALENDAR),
            'fecha_inicio': forms.DateInput(attrs={'class':'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'class':'form-control'}),
            'estado': forms.TextInput(attrs={'class':'form-control'}),
            'web': forms.TextInput(attrs={'class':'form-control'}),
        }



class AliadoForm(forms.ModelForm):
    class Meta:
        model=Aliado

        fields = [
            'codigo_aliado',
            'origen',
            'nombre',
            'pais',
            'tipo_de_covenio',
        ]

        labels = {
            'codigo_aliado':'Código',
            'origen':'Origen',
            'nombre':'Nombre',
            'pais':'Pais',
            'tipo_de_covenio':'Tipo de convenio',
        }

        widgets = {
            'codigo_aliado':forms.TextInput(attrs={'class':'form-control'}),
            'origen':forms.RadioSelect(choices=OPTIONS_ORIGEN),
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'pais': forms.TextInput(attrs={'class':'form-control'}),
            'tipo_de_covenio': forms.Select(attrs={'class':'form-control'}),
        }


class AulaForm(forms.ModelForm):
    class Meta:
        model=Aula

        fields = [
            'codigo_aula',
            'unidad',
            'nombre',
            'ubicacion',
            'tipo',
            'capacidad',
            'observacion',
            'estado',

        ]

        labels = {
            'codigo_aula':'Código',
            'unidad':'Unidad',
            'nombre':'Nombre',
            'ubicacion':'Ubicación',
            'tipo':'Tipo',
            'capacidad':'Capacidad',
            'observacion':'Observación',
            'estado':'Estado',
        }

        widgets = {
            'codigo_aula':forms.TextInput(attrs={'class':'form-control'}),
            'unidad': forms.Select(attrs={'class':'form-control'}),
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class':'form-control'}),
            'tipo': forms.Select(attrs={'class':'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class':'form-control'}),
            'observacion':forms.Textarea(attrs={'class':'form-control'}),
            'estado': forms.Select(attrs={'class':'form-control'}),
        }


class CalendarioForm(forms.ModelForm):
    class Meta:
        model = CalendarioEvento

        fields = [
            'dia',
            'fecha',
            'hora_inicio',
            'hora_fin',
            'facilitador',
            'aula',
        ]

        labels = {
            'dia':'Dia',
            'fecha':'Fecha',
            'hora_inicio':'Hora inicio de Sesion',
            'hora_fin':'Hora fin de Sesion',
            'facilitador':'Facilitador',
            'aula':'Aula',
        }

        widgets = {
            'dia': forms.TextInput(attrs={'class':'form-control'}),
            'fecha': forms.DateInput(attrs={'class':'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'class':'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'class':'form-control'}),
            'facilitador': forms.Select(attrs={'class':'form-control'}),
            'aula': forms.Select(attrs={'class':'form-control'}),
        }


class CoForm(forms.ModelForm):
    class Meta:
        model = Co
        fields = [
            'co_facilitador',
        ]

        labels = {
            'co_facilitador':'Asignar co-facilitador', 
        }

        widgets = {
            'co_facilitador': forms.Select(attrs={'class':'form-control'}),
        }

class PubForm(forms.ModelForm):
    class Meta:
        model = PubEvento
        fields = [
            'evento',
            'precio',
            'picture',
        ]

        labels = {
            'evento':'Evento',
            'precio':'Precio',
            'picture':'Picture',
        }

        widgets = {
            'evento': forms.Select(attrs={'class':'form-control'}),
            'precio': forms.TextInput(attrs={'class':'form-control'}),
            'picture': forms.ClearableFileInput(),
        }


CoFormSet = modelformset_factory(Co, form=CoForm, extra=1, can_delete=True)
CalendarioFormSet = modelformset_factory(CalendarioEvento, form=CalendarioForm, extra=0, can_delete=True)
