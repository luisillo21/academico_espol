from bootstrap_modal_forms.forms import BSModalForm
from .models import Area,Especialidad
from django import forms
class AreaForm(BSModalForm):
    class Meta:
        model=Area
        fields = {
            'codigo',
            'area',
        }

        widgets = {
            'codigo':forms.TextInput(attrs={'class':'form-control'}),
            'area':forms.TextInput(attrs={'class':'form-control'}),
        }

class EspecialidadForm(BSModalForm):
    class Meta:
        model=Especialidad

        fields = {
            'codigo',
            'especialidades',
            'area',
        }

        widgets = {
            'codigo':forms.TextInput(attrs={'class':'form-control'}),
            'especialidades':forms.Textarea(attrs={'class':'form-control','rows':'10'}),
            'area':forms.Select(attrs={'class':'form-control'}),
        }
