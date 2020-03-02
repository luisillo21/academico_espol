from django.core.validators import ValidationError

def validar_entrada_nombre(value):
    if not len(value) > 10:
        raise ValidationError('Minimo 10 caracteres')

def validar_entrada_entero(value):
    if not len(str(value)) == 4:
        raise ValidationError('Minimo una cifra de 4 digitos')

def validar_entrada_textarea(value):
    if not len(value) > 10:
        raise ValidationError('Minimo 10 Caracteres')
