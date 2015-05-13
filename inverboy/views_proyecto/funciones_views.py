# -*- encoding: utf-8 -*-

from inverboy.forms import *
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse

#Función que retorna una cadena omitiendo sus acentos
def normaliza(cadena):
    #from unicodedata import normalize, category
    #return ''.join([x for x in normalize('NFD', cadena) if category(x) == 'Ll'])
    # return ''.join([x for x in normalize('NFD', cadena)])
    #return ''.join([x for x in normalize('NFD', cadena) if category(x) == 'Mn'])
    from unicodedata import normalize
    # import re
    decomposed = normalize("NFKD", cadena)
    #no_accent = ''.join(c for c in decomposed if ord(c)<0x7f)
    return ''.join(c for c in decomposed if ord(c)<0x7f)


#Función para registrar el historial de un usuario
def registro_historial(direccion_ip, usuario, actividad):
    historial = Historial()
    historial.usuario = usuario
    historial.direccion_ip = direccion_ip
    historial.actividad = actividad
    historial.save()


#Funciones para generar PDF

#Funcion para el manejo de archivos estaticos en los PDF's
def fetch_resources(uri, rel):
    import os, settings
    """
    Callback to allow pisa/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    `rel` gives a relative path, but it's not used here.

    """
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path

#Función para generar un rotulo
def generar_rotulo(fichero_imagen, width, height):
    import os
    import settings
    from reportlab.platypus import Image
    fichero_imagen = os.path.join(settings.MEDIA_ROOT, 'ima', 'pdfs', fichero_imagen)
    imagen_logo = Image(os.path.realpath(fichero_imagen), width=width, height=height)
    return imagen_logo


#Función para generar un estilo
def generar_estilo(especificaciones):
    from reportlab.lib.styles import ParagraphStyle
    return ParagraphStyle(**especificaciones)


import ho.pisa as pisa
from django.template import loader, Context
import StringIO
import cgi
def render_to_pdf(template_src, context_dict):
    template = loader.get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))


def generar_pdf(html, nro):
    # Función para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result, encoding="UTF-8", link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))



#### Libreria para convertir numeros a letras
from itertools import ifilter

UNIDADES = (
    '',
    'UN ',
    'DOS ',
    'TRES ',
    'CUATRO ',
    'CINCO ',
    'SEIS ',
    'SIETE ',
    'OCHO ',
    'NUEVE ',
    'DIEZ ',
    'ONCE ',
    'DOCE ',
    'TRECE ',
    'CATORCE ',
    'QUINCE ',
    'DIECISEIS ',
    'DIECISIETE ',
    'DIECIOCHO ',
    'DIECINUEVE ',
    'VEINTE '
)

DECENAS = (
    'VENTI',
    'TREINTA ',
    'CUARENTA ',
    'CINCUENTA ',
    'SESENTA ',
    'SETENTA ',
    'OCHENTA ',
    'NOVENTA ',
    'CIEN '
)

CENTENAS = (
    'CIENTO ',
    'DOSCIENTOS ',
    'TRESCIENTOS ',
    'CUATROCIENTOS ',
    'QUINIENTOS ',
    'SEISCIENTOS ',
    'SETECIENTOS ',
    'OCHOCIENTOS ',
    'NOVECIENTOS '
)

MONEDAS = (
    {'country': u'Colombia', 'currency': 'COP', 'singular': u'PESO COLOMBIANO', 'plural': u'PESOS COLOMBIANOS', 'symbol': u'$'},
    {'country': u'Estados Unidos', 'currency': 'USD', 'singular': u'DÓLAR', 'plural': u'DÓLARES', 'symbol': u'US$'},
    {'country': u'Europa', 'currency': 'EUR', 'singular': u'EURO', 'plural': u'EUROS', 'symbol': u'€'},
    {'country': u'México', 'currency': 'MXN', 'singular': u'PESO MEXICANO', 'plural': u'PESOS MEXICANOS', 'symbol': u'$'},
    {'country': u'Perú', 'currency': 'PEN', 'singular': u'NUEVO SOL', 'plural': u'NUEVOS SOLES', 'symbol': u'S/.'},
    {'country': u'Reino Unido', 'currency': 'GBP', 'singular': u'LIBRA', 'plural': u'LIBRAS', 'symbol': u'£'}
)
# Para definir la moneda me estoy basando en los código que establece el ISO 4217
# Decidí poner las variables en inglés, porque es más sencillo de ubicarlas sin importar el país
# Si, ya sé que Europa no es un país, pero no se me ocurrió un nombre mejor para la clave.


def to_word(number, mi_moneda=None):
    if mi_moneda != None:
        try:
            moneda = ifilter(lambda x: x['currency'] == mi_moneda, MONEDAS).next()
            if number < 2:
                moneda = moneda['singular']
            else:
                moneda = moneda['plural']
        except:
            return "Tipo de moneda inválida"
    else:
        moneda = ""
    """Converts a number into string representation"""
    converted = ''

    if not (0 < number < 999999999):
        return 'No es posible convertir el numero a letras'

    number_str = str(number).zfill(9)
    millones = number_str[:3]
    miles = number_str[3:6]
    cientos = number_str[6:]

    if(millones):
        if(millones == '001'):
            converted += 'UN MILLON '
        elif(int(millones) > 0):
            converted += '%sMILLONES ' % __convert_group(millones)

    if(miles):
        if(miles == '001'):
            converted += 'MIL '
        elif(int(miles) > 0):
            converted += '%sMIL ' % __convert_group(miles)

    if(cientos):
        if(cientos == '001'):
            converted += 'UN '
        elif(int(cientos) > 0):
            converted += '%s ' % __convert_group(cientos)

    converted += moneda

    return converted.title()


def __convert_group(n):
    """Turn each group of numbers into letters"""
    output = ''

    if(n == '100'):
        output = "CIEN "
    elif(n[0] != '0'):
        output = CENTENAS[int(n[0]) - 1]

    k = int(n[1:])
    if(k <= 20):
        output += UNIDADES[k]
    else:
        if((k > 30) & (n[2] != '0')):
            output += '%sY %s' % (DECENAS[int(n[1]) - 2], UNIDADES[int(n[2])])
        else:
            output += '%s%s' % (DECENAS[int(n[1]) - 2], UNIDADES[int(n[2])])

    return output


################## Funciones de codificación ##########################################
def decodeFromHex(arg):
    cont = len(arg)
    cadena = ""
    while cont>=0:
        cadena = cadena + arg[cont-3:cont]
        cont = cont-3

    arg = cadena
    e=len(arg)
    cadena = ""
    while(e>=0):
        s=e-3;
        tmpCadena = str(arg[s:e])
        decimal = hexaToDecimal(tmpCadena)
        caracter = encodeDecimalToCaracter(decimal)
        cadena = cadena + str(caracter)
        e=s;
    return cadena


def hexaToDecimal(hexa):
    hexa = str(hexa)
    suma = 0
    potencia = len(hexa)-1
    for digito in hexa:
        digito = str(digito)
        actualDigito = 0
        if digito == '0':
            actualDigito = 0
        if digito == '1':
            actualDigito = 1
        if digito == '2':
            actualDigito = 2
        if digito == '3':
            actualDigito = 3
        if digito == '4':
            actualDigito = 4
        if digito == '5':
            actualDigito = 5
        if digito == '6':
            actualDigito = 6
        if digito == '7':
            actualDigito = 7
        if digito == '8':
            actualDigito = 8
        if digito == '9':
            actualDigito = 9
        if digito == 'a':
            actualDigito = 10
        if digito == 'b':
            actualDigito = 11
        if digito == 'c':
            actualDigito = 12
        if digito == 'd':
            actualDigito = 13
        if digito == "e":
            actualDigito = 14
        if digito == 'f':
            actualDigito = 15
        suma = suma + (actualDigito*(pow(16, potencia)))
        potencia = potencia -1
    return suma

######################FUNCION DE CODIFICACION DECIMAL ASCII ISO LATIN1 (ISO-8859-1)################################
def encodeDecimalToCaracter(decimal):
    if decimal == 32:
        return str(' ')
    if decimal == 33:
        return "!"
    if decimal == 34:
        return '"'
    if decimal == 35:
        return "#"
    if decimal == 36:
        return "$"
    if decimal == 37:
        return "%"
    if decimal == 38:
        return "&"
    if decimal == 39:
        return "'"
    if decimal == 40:
        return "("
    if decimal == 41:
        return ")"
    if decimal == 42:
        return "*"
    if decimal == 43:
        return "+"
    if decimal == 44:
        return ","
    if decimal == 45:
        return "-"
    if decimal == 46:
        return "."
    if decimal == 47:
        return "/"
    if decimal == 48:
        return "0"
    if decimal == 49:
        return "1"
    if decimal == 50:
        return "2"
    if decimal == 51:
        return "3"
    if decimal == 52:
        return "4"
    if decimal == 53:
        return "5"
    if decimal == 54:
        return "6"
    if decimal == 55:
        return "7"
    if decimal == 56:
        return "8"
    if decimal == 57:
        return "9"
    if decimal == 58:
        return ":"
    if decimal == 59:
        return ";"
    if decimal == 60:
        return "<"
    if decimal == 61:
        return "="
    if decimal == 62:
        return ">"
    if decimal == 63:
        return "?"
    if decimal == 64:
        return "@"
    if decimal == 65:
        return "A"
    if decimal == 66:
        return "B"
    if decimal == 67:
        return "C"
    if decimal == 68:
        return "D"
    if decimal == 69:
        return "E"
    if decimal == 70:
        return "F"
    if decimal == 71:
        return "G"
    if decimal == 72:
        return "H"
    if decimal == 73:
        return "I"
    if decimal == 74:
        return str('J')
    if decimal == 75:
        return "K"
    if decimal == 76:
        return "L"
    if decimal == 77:
        return "M"
    if decimal == 78:
        return "N"
    if decimal == 79:
        return "O"
    if decimal == 80:
        return "P"
    if decimal == 81:
        return "Q"
    if decimal == 82:
        return "R"
    if decimal == 83:
        return "S"
    if decimal == 84:
        return "T"
    if decimal == 85:
        return "U"
    if decimal == 86:
        return "V"
    if decimal == 87:
        return "W"
    if decimal == 88:
        return "X"
    if decimal == 89:
        return "Y"
    if decimal == 90:
        return "Z"
    if decimal == 91:
        return "["
    if decimal == 92:
        return " " # 92 = '\'
    if decimal == 93:
        return "]"
    if decimal == 94:
        return "^"
    if decimal == 95:
        return "_"
    if decimal == 96:
        return "`"
    if decimal == 97:
        return "a"
    if decimal == 98:
        return "b"
    if decimal == 99:
        return "c"
    if decimal == 100:
        return "d"
    if decimal == 101:
        return "e"
    if decimal == 102:
        return "f"
    if decimal == 103:
        return "g"
    if decimal == 104:
        return "h"
    if decimal == 105:
        return "i"
    if decimal == 106:
        return 'j'
    if decimal == 107:
        return "k"
    if decimal == 108:
        return "l"
    if decimal == 109:
        return "m"
    if decimal == 110:
        return "n"
    if decimal == 111:
        return str('o')
    if decimal == 112:
        return "p"
    if decimal == 113:
        return "q"
    if decimal == 114:
        return "r"
    if decimal == 115:
        return "s"
    if decimal == 116:
        return "t"
    if decimal == 117:
        return "u"
    if decimal == 118:
        return 'v'
    if decimal == 119:
        return "w"
    if decimal == 120:
        return "x"
    if decimal == 121:
        return "y"
    if decimal == 122:
        return "z"
    if decimal == 123:
        return "{"
    if decimal == 124:
        return "|"
    if decimal == 125:
        return "}"
    if decimal == 126:
        return "~"
    if decimal == 127:
        return "⌂"
    if decimal == 160:
        return "&nbsp;" # No se sabe
    if decimal == 161:
        return "¡"
    if decimal == 162:
        return "¢"
    if decimal == 163:
        return "£"
    if decimal == 164:
        return "¤"
    if decimal == 165:
        return "¥"
    if decimal == 166:
        return "|"
    if decimal == 167:
        return "§"
    if decimal == 168:
        return "¨"
    if decimal == 169:
        return "©"
    if decimal == 170:
        return "ª"
    if decimal == 171:
        return "«"
    if decimal == 172:
        return "¬"
    if decimal == 173:
        return "-"
    if decimal == 174:
        return "®"
    if decimal == 175:
        return "¯"
    if decimal == 176:
        return "°"
    if decimal == 177:
        return "±"
    if decimal == 178:
        return "²"
    if decimal == 179:
        return "³"
    if decimal == 180:
        return "´"
    if decimal == 181:
        return "μ"
    if decimal == 182:
        return "¶"
    if decimal == 183:
        return "·"
    if decimal == 184:
        return "¸"
    if decimal == 185:
        return "¹"
    if decimal == 186:
        return "º"
    if decimal == 187:
        return "»"
    if decimal == 188:
        return "1/4"
    if decimal == 189:
        return "1/2"
    if decimal == 190:
        return "3/4"
    if decimal == 191:
        return "¿"
    if decimal == 192:
        return "À"
    if decimal == 193:
        return "Á"
    if decimal == 194:
        return "Â"
    if decimal == 195:
        return "Ã"
    if decimal == 196:
        return "Ä"
    if decimal == 197:
        return "Å"
    if decimal == 198:
        return "Æ"
    if decimal == 199:
        return "Ç"
    if decimal == 200:
        return "È"
    if decimal == 201:
        return "É"
    if decimal == 202:
        return "Ê"
    if decimal == 203:
        return "Ë"
    if decimal == 204:
        return "Ì"
    if decimal == 205:
        return "Í"
    if decimal == 206:
        return "Î"
    if decimal == 207:
        return "Ï"
    if decimal == 208:
        return "Ð"
    if decimal == 209:
        return "Ñ"
    if decimal == 210:
        return "Ò"
    if decimal == 211:
        return "Ó"
    if decimal == 212:
        return "Ô"
    if decimal == 213:
        return "Õ"
    if decimal == 214:
        return "Ö"
    if decimal == 215:
        return "×"
    if decimal == 216:
        return "Ø"
    if decimal == 217:
        return "Ù"
    if decimal == 218:
        return "Ú"
    if decimal == 219:
        return "Û"
    if decimal == 220:
        return "Ü"
    if decimal == 221:
        return "Ý"
    if decimal == 222:
        return "Þ"
    if decimal == 223:
        return "ß"
    if decimal == 224:
        return "à"
    if decimal == 225:
        return "á"
    if decimal == 226:
        return "â"
    if decimal == 227:
        return "ã"
    if decimal == 228:
        return "ä"
    if decimal == 229:
        return "å"
    if decimal == 230:
        return "æ"
    if decimal == 231:
        return "ç"
    if decimal == 232:
        return "è"
    if decimal == 233:
        return "é"
    if decimal == 234:
        return "ê"
    if decimal == 235:
        return "ë"
    if decimal == 236:
        return "ì"
    if decimal == 237:
        return "í"
    if decimal == 238:
        return "î"
    if decimal == 239:
        return "ï"
    if decimal == 240:
        return "ð"
    if decimal == 241:
        return "ñ"
    if decimal == 242:
        return "ò"
    if decimal == 243:
        return "ó"
    if decimal == 244:
        return "ô"
    if decimal == 245:
        return "õ"
    if decimal == 246:
        return "ö"
    if decimal == 247:
        return "÷"
    if decimal == 248:
        return "ø"
    if decimal == 249:
        return "ù"
    if decimal == 250:
        return "ú"
    if decimal == 251:
        return "û"
    if decimal == 252:
        return "ü"
    if decimal == 253:
        return "ý"
    if decimal == 254:
        return "þ"
    if decimal == 255:
        return "ÿ"

    return ""
#####################FUNCION DE CODIFICACION DECIMAL ASCII################################


