# -*- encoding: utf-8 -*-
__author__ = 'Diego Reyes'

import re
import decimal

##libreria para el manejo de errores
from django.forms.util import ErrorList

def validate_unique_field(model, fields_unique, fields_error=None, exclude_initials_values=None, form=None):
    """
        Retorna true si el registro ya existe en la BD, y form especificando el campo de error o duplicado
        Retorna False si el registro no existe en la BD

        Parametros:
        * model: Modelo
        * fields_unique: Campos a evaluar
        * fields_error: Campos referencia error
        * field_exclude: Campo a excluir, si la acción es de modificación de un registro
        * exclude_initial_value: Valor de field_exclude a excluir
        * form: formulario a especificar error
    """
    value = False
    qs = model._default_manager.filter(**fields_unique)
    if exclude_initials_values != None:
        qs = qs.exclude(**exclude_initials_values)
    if qs.count() > 0:
        value = True
        if fields_error != None and form != None:
            for field in fields_error:
                #form._errors[field] = ErrorList([u'%(field)s %(field_value)s ya existe en el sistema.' %{'field': field, 'field_value': fields_unique[field]} ])
                form._errors[field] = ErrorList([u'%(field_value)s ya existe en el sistema.' %{'field_value': fields_unique[field]} ])
    return value, form

def validar_cadena(cadena):
    mensaje = ''
    if cadena.strip() == '':
        mensaje = 'Campo obligatorio'
    return mensaje

def validar_long_max_cadena(cadena, long_max):
    mensaje = ''
    if len(cadena) > long_max:
        mensaje = 'Este campo no debe exceder ' + str(long_max) + ' caracteres'
    return mensaje

# Verifica que una cadena no contenga caracteres especiales
def validar_cadena_caracteres_especiales(cadena):
    mensaje = ''
    patron = u'^[&áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$'
    if re.match(patron, cadena) == None:
        mensaje = 'Campo incorrecto'
    return mensaje

# Verifica que una cadena no contenga caracteres especiales ni espacios
def validar_cadena_caracteres_especiales_acentos_espacios(cadena):
    mensaje = ''
    patron = u'^[ñÑA-Za-z0-9_-]+$'
    if re.match(patron, cadena) == None:
        mensaje = 'Campo incorrecto'
    return mensaje

def validar_identificacion(identificacion):
    mensaje = validar_cadena(identificacion)
    if len(identificacion) > 10 or len(identificacion) < 7:
        mensaje = 'Campo incorrecto'
    else :
        try:
            identificacion = int(identificacion)
        except :
            mensaje = 'Campo incorrecto'
        if mensaje == '':
            if identificacion <= 0:
                mensaje = 'Campo incorrecto'
    return mensaje

def validar_select(option):
    mensaje = ''
    if int(option) == 0:
        mensaje = 'Campo obligatorio'
    return mensaje

def validar_telefono(telefono):
    mensaje = ''
    if len(telefono) == 10:
        patron = '(^\({1}[0-9]{1}\){1}?[0-9]{7})|(\d{10})'
        if re.match(patron, telefono) == None:
            mensaje = 'Campo incorrecto'
    else:
        mensaje = 'Campo incorrecto'
    return mensaje

def validar_ext(ext):
    mensaje = ''
    patron = '^\d{3}$'
    if re.match(patron, ext) == None:
        mensaje = 'Campo incorrecto'
    return mensaje

def validar_celular(celular):
    mensaje = ''
    patron = '^\d{10}$'
    if re.match(patron, celular) == None:
        mensaje = 'Campo incorrecto'
    return mensaje

def validar_email(email):
    mensaje = ''
    patron = '^(.+\@.+\..+)$'
    if re.match(patron, email) == None:
        mensaje = 'Campo incorrecto'
    return mensaje

def validar_cantidad_float(numero):
    mensaje = ''
    try:
        float(numero)
    except :
        mensaje = 'Cantidad incorrecta'
    return mensaje

def validar_cantidad_float_0(numero):
    mensaje = ''
    numero = float(numero)
    if numero <= 0:
        mensaje = 'Cantidad incorrecta'
    return mensaje

def validar_cantidad_float_negativo(numero):
    mensaje = ''
    numero = float(numero)
    if numero < 0:
        mensaje = 'Cantidad incorrecta'
    return mensaje

def validar_cantidad_float_digitos(numero, decimales=2):
    mensaje = ''
    if numero.find('.') >= 0:
        partes_numero = numero.split('.')
        if len(partes_numero[0]) > 10:
            mensaje = 'Cantidad incorrecta'
        if len(partes_numero[1]) > decimales:
            mensaje = 'Cantidad incorrecta'
    else:
        if len(numero) > 10:
            mensaje = 'Cantidad incorrecta'
    return mensaje

def validar_cantidad_int(numero):
    mensaje = ''
    try:
        int(numero)
    except :
        mensaje = 'Cantidad incorrecta'
    return mensaje

def validar_cantidad_int_0(numero):
    mensaje = ''
    numero = int(numero)
    if numero <= 0:
        mensaje = 'Cantidad incorrecta'
    return mensaje

def validar_int_4digitos(numero):
    mensaje = ''
    if len(numero) > 4:
        mensaje = 'Cantidad incorrecta'
    return mensaje

def validar_int_digitos(numero, digitos):
    mensaje = ''
    numero = str(numero)
    if len(numero) > digitos:
        mensaje = 'Cantidad incorrecta'
    return mensaje

def validar_fecha(fecha):
    mensaje = ''
    patron = '^\d{4}\-\d{1,2}\-\d{1,2}$'
    if re.match(patron, fecha) == None:
        mensaje = 'Campo incorrecto'
    else:
        partes_fecha = fecha.split('-')
        if int(partes_fecha[0]) < 1900 or int(partes_fecha[0]) > 2100:
            mensaje = 'Campo incorrecto'
        if int(partes_fecha[1]) <= 0 or int(partes_fecha[1]) > 12:
            mensaje = 'Campo incorrecto'
        if int(partes_fecha[2]) <= 0 or int(partes_fecha[2]) > 31:
            mensaje = 'Campo incorrecto'
    return mensaje

#Verificar si hay residuo entre a % b
def is_residuo_0(a, b):
    rtdo = False

    division =  a / b
    cadena = str(division)
    partes_cadena = cadena.split('.')
    parte_decimal = float(partes_cadena[1])
    if parte_decimal == 0:
        rtdo = True
    return rtdo

## Complementarias ##
# Valida el nombre de un suministro
def validar_cadena_nombre_suministro(cadena):
    mensaje = ''
    patron = u'^[+/.°"#áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$'
    if re.match(patron, cadena) == None:
        mensaje = 'Campo incorrecto'
    return mensaje

# Valida el nombre de un APU
def validar_cadena_nombre_apu(cadena):
    mensaje = ''
    patron = u'^[./°"#áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$'
    if re.match(patron, cadena) == None:
        mensaje = 'Campo incorrecto'
    return mensaje

## Complementarias ##
## Función que devuelve una cadena omitiendo sus acentos
def normaliza(cadena):
    from unicodedata import normalize
    decomposed = normalize("NFKD", cadena)
    return ''.join(c for c in decomposed if ord(c)<0x7f)

class iStr(str):
    """Case insensitive strings class.
    Performs like str except comparisons are case insensitive."""

    def __init__(self, strMe):
        str.__init__(self, strMe)
        self.__lowerCaseMe = strMe.lower()

    def __repr__(self):
        return "iStr(%s)" % str.__repr__(self)

    def __eq__(self, other):
        return self.__lowerCaseMe == other.lower()

    def __lt__(self, other):
        return self.__lowerCaseMe < other.lower()

    def __le__(self, other):
        return self.__lowerCaseMe <= other.lower()

    def __gt__(self, other):
        return self.__lowerCaseMe > other.lower()

    def __ne__(self, other):
        return self.__lowerCaseMe != other.lower()

    def __ge__(self, other):
        return self.__lowerCaseMe >= other.lower()

    def __cmp__(self, other):
        return cmp(self.__lowerCaseMe, other.lower())

    def __hash__(self):
        return hash(self.__lowerCaseMe)

    def __contains__(self, other):
        return other.lower() in self.__lowerCaseMe

    def count(self, other, *args):
        return str.count(self.__lowerCaseMe, other.lower(), *args)

    def endswith(self, other, *args):
        return str.endswith(self.__lowerCaseMe, other.lower(), *args)

    def find(self, other, *args):
        return str.find(self.__lowerCaseMe, other.lower(), *args)

    def index(self, other, *args):
        return str.index(self.__lowerCaseMe, other.lower(), *args)

    def lower(self):   # Courtesy Duncan Booth
        return self.__lowerCaseMe

    def rfind(self, other, *args):
        return str.rfind(self.__lowerCaseMe, other.lower(), *args)

    def rindex(self, other, *args):
        return str.rindex(self.__lowerCaseMe, other.lower(), *args)

    def startswith(self, other, *args):
        return str.startswith(self.__lowerCaseMe, other.lower(), *args)