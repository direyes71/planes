# -*- encoding: utf-8 -*-

from dajaxice.core import dajaxice_functions
from dajax.core import Dajax
from django.template.loader import render_to_string
from inverboy.models import *
# PAGINACION
from inverboy.paginator import *
## CONSULTAS ANIDADAS
from django.db.models import Q

#---------------------------- COMUNES EN MODULOS ----------------------------------

# FUNCION PARA CARGAR LOS MUNICIPIOS DE UN DEPARTAMENTO ESPECIFICO
def cargar_municipios2(request, option, elemento):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        municipios = []
        if option != '':
            municipios = Municipio.objects.filter(departamento = int(option))
        out = '<option value="0">----</option>'
        for municipio in municipios:
            out = out + '<option value="' + str(municipio.id)+'">' + municipio.nombre + '</option>'
        dajax.assign('#' + elemento,'innerHTML',out)
        dajax.script("$('#" + elemento + "').trigger('chosen:updated');")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

#---------------------------- USUARIOS ---------------------------------------------


#---------------------------- PROVEEDORES ---------------------------------------------

def informacion_proveedor2(request, id, indice):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proveedor = Proveedor.objects.get(id=id)
        contactos = Contacto.objects.filter(proveedor = proveedor)
        user = request.user
        render = render_to_string('ajax/informacionproveedor.html', {'user': user, 'proveedor': proveedor, 'contactos': contactos })
        dajax.script("document.getElementById('flotanteProveedores').style.top=((document.getElementById('fila_proveedor_"+str(indice)+"').offsetTop) + 62) + 'px';")
        dajax.script("document.getElementById('flotanteProveedores').style.display = 'block';")
        dajax.assign('#flotanteProveedores','innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

#---------------------------- SUMINISTROS ---------------------------------------------

def cargar_especificaciones2(request, option, html):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        especificaciones = Categoria.objects.filter(tipo=2, categoria_asociada = int(option), estado=1)
        out = '<option value="0">----</option>'
        dajax.assign('#id_tipo','innerHTML',out )
        for especificacion in especificaciones:
            out = out + '<option value="'+str(especificacion.id)+'">'+especificacion.nombre+'</option>'
        dajax.assign('#id_especificacion','innerHTML',out )
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

def cargar_tipos2(request, option, html):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        tipos = Categoria.objects.filter(tipo=3, categoria_asociada=int(option), estado=1)
        out = '<option value="0">----</option>'
        for tipo in tipos:
             out = out + '<option value="' + str(tipo.id)+'">' + tipo.nombre + '</option>'
        dajax.assign('#id_tipo', 'innerHTML', out)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def informacion_suministro2(request,id, indice):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        suministro = Suministro.objects.get(id= id)
        proveedores = suministro.suministroproveedor_set.all()
        user = request.user
        render = render_to_string('ajax/informacionsuministro.html', {'user': user, 'suministro': suministro, 'proveedores': proveedores })
        dajax.script("document.getElementById('flotanteSuministros').style.top=((document.getElementById('fila_suministro_"+str(indice)+"').offsetTop) + 62) + 'px';")
        dajax.script("document.getElementById('flotanteSuministros').style.display = 'block';")
        dajax.assign('#flotanteSuministros','innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

#---------------------------- APUS ---------------------------------------------

def cargar_subcapitulos2(request, option, html):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        out = ''
        if int(option) != 0:
            subcapitulos = Capitulo.objects.filter(tipo_capitulo=2, capitulo_asociado = int(option), estado_capitulo=1)
            # lista_subcapitulos = []
            out = '<option value="0">----</option>'
            for subcapitulo in subcapitulos:
                out = out + '<option value="'+str(subcapitulo.id)+'">'+subcapitulo.nombre_capitulo+'</option>'
        dajax.assign('#id_subcapitulo','innerHTML',out)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

#---------------------------- APUS PROYECTO ---------------------------------------------

# Función para cargar los subcapitulos de un capitulo de APU proyecto
def cargar_subcapitulos_apus_proyectos2(request, option, elemento):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        subcapitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=2, capitulo_asociado = int(option), estado_capitulo=True)
        out = '<option value="0">----</option>'
        for subcapitulo in subcapitulos:
            out = out + '<option value="'+str(subcapitulo.id)+'">'+subcapitulo.nombre_capitulo+'</option>'
        dajax.assign('#'+elemento,'innerHTML', out)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


# Función para cargar los subcapitulos de un capitulo de APU proyecto
def cargar_subcapitulos_apus_proyectos_busqueda2(request, option, elemento):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        subcapitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=2, capitulo_asociado = int(option), estado_capitulo=True)
        out = '<option value="0">----</option>'
        for subcapitulo in subcapitulos:
            out = out + '<option value="'+str(subcapitulo.id)+'">'+subcapitulo.nombre_capitulo+'</option>'
        dajax.assign('#'+elemento,'innerHTML', out)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def informacion_proyecto2(request,id, indice):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id= id)
        user = request.user
        render = render_to_string('ajax/informacionproyecto.html', {'user': user, 'proyecto': proyecto })
        dajax.script("document.getElementById('flotanteProyectos').style.top=((document.getElementById('fila_proyecto_"+str(indice)+"').offsetTop) + 62) + 'px';")
        dajax.script("document.getElementById('flotanteProyectos').style.display = 'block';")
        dajax.assign('#flotanteProyectos','innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


# Función para cargar los subcapitulos de un capitulo de APU proyecto
def cargar_terceros_orden_servicio_add2(request, proveedor_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        terceros = Proveedor.objects.filter(estado_proveedor=True).exclude(id=proveedor_id).order_by('razon_social')
        out = '<option value="0">----</option>'
        for tercero in terceros:
            out = out + '<option value="'+str(tercero.id)+'">' + tercero.razon_social + '</option>'
        dajax.assign('#id_tercero','innerHTML', out)
        dajax.script("document.getElementById('id_panel_aplica_tercero').style.display = 'block';")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()