# -*- encoding: utf-8 -*-
from dajaxice.core import dajaxice_functions
from dajax.core import Dajax
from django.template.loader import render_to_string
from inverboy.models import *
# PAGINACION
from inverboy.paginator import *
## CONSULTAS ANIDADAS
from django.db.models import Q
#from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse
#VALIDACIONES
from inverboy.validaciones.validaciones import *

#from validator.core import Validator, Field
#from validator.rules import *


from django.db.models import Sum, Max

#---------------------------- USUARIOS ---------------------------------------------


#---------------------------- PROVEEDORES ---------------------------------------------

def ventana_contacto_proveedor2(request):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        lista_contactos = None
        try:
            lista_contactos = request.session['lista_contactos']
        except :
            pass
        if lista_contactos != None:
            render = render_to_string('ajax/contactoadd.html', {'user': user, 'change': 0 } )
            dajax.assign('#light', 'innerHTML', render)
            dajax.script("document.getElementById('light').style.display='block';")
            dajax.script("document.getElementById('fade').style.display='block';")
        else:
            dajax.redirect('/inverboy/home/') 
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_contacto_proveedor2(request, nombre, cargo, telefono, ext, celular, email):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        lista_contactos = None
        try:
            lista_contactos = request.session['lista_contactos']
        except :
            pass
        if lista_contactos != None:
            error_nombre = validar_cadena(nombre)
            if error_nombre == '':
                error_nombre = validar_cadena_caracteres_especiales(nombre)
            error_cargo = validar_select(cargo)
            error_telefono = validar_cadena(telefono)
            if error_telefono == '':
                error_telefono = validar_telefono(telefono)
            error_ext = ''
            if ext != '':
                error_ext = validar_ext(ext)
            error_celular = ''
            if celular != '':
                error_celular = validar_celular(celular)
            error_email = ''
            if email != '':
                error_email = validar_email(email)
            if error_nombre == '' and error_cargo == '' and error_telefono == '' and error_ext == '' and error_celular == '' and error_email == '':
                contacto = Contacto()
                contacto.nombre_contacto = nombre.strip()
                contacto.cargo_contacto = int(cargo)
                contacto.telefono_contacto = telefono.strip()
                contacto.ext_contacto = ext.strip()
                contacto.celular_contacto = celular.strip()
                contacto.email_contacto = email.strip()
                lista_contactos.append(contacto)
                request.session['lista_contactos'] = lista_contactos
                render = render_to_string('ajax/contactosproveedor.html', {'user': user, 'contactos': lista_contactos } )
                dajax.assign('#reporte_contactos', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='none';")
                dajax.script("document.getElementById('fade').style.display='none';")
                dajax.alert('Contacto agregado correctamente')
            else:
                print 'error en campos de contacto'
                render = render_to_string('ajax/contactoadd.html', {'user': user, 'nombre': nombre, 'cargo': int(cargo), 'telefono': telefono, 'ext': ext, 'celular': celular, 'email': email, 'error_nombre': error_nombre, 'error_cargo': error_cargo, 'error_telefono': error_telefono, 'error_ext': error_ext, 'error_celular': error_celular, 'error_email': error_email, 'change': 0 } )
                dajax.assign('#light', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

def ventana_modificar_contacto_proveedor2(request, indice):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        lista_contactos = None
        try:
            lista_contactos = request.session['lista_contactos']
        except :
            pass
        if lista_contactos != None:
            contacto = lista_contactos.__getitem__(indice)
            render = render_to_string('ajax/contactoadd.html', {'user': user, 'nombre': contacto.nombre_contacto, 'cargo': contacto.cargo_contacto, 'telefono': contacto.telefono_contacto, 'ext': contacto.ext_contacto, 'celular': contacto.celular_contacto, 'email': contacto.email_contacto , 'indice': indice, 'change': 1 } )
            dajax.assign('#light', 'innerHTML', render)
            dajax.script("document.getElementById('light').style.display='block';")
            dajax.script("document.getElementById('fade').style.display='block';")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

def modificar_contacto_proveedor2(request, indice, nombre, cargo, telefono, ext, celular, email):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        lista_contactos = None
        try:
            lista_contactos = request.session['lista_contactos']
        except :
            pass
        if lista_contactos != None:
            error_nombre = validar_cadena(nombre)
            if error_nombre == '':
                error_nombre = validar_cadena_caracteres_especiales(nombre)
            error_cargo = validar_select(cargo)
            error_telefono = validar_cadena(telefono)
            if error_telefono == '':
                error_telefono = validar_telefono(telefono)
            error_ext = ''
            if ext != '':
                error_ext = validar_ext(ext)
            error_celular = ''
            if celular != '':
                error_celular = validar_celular(celular)
            error_email = ''
            if email != '':
                error_email = validar_email(email)
            if error_nombre == '' and error_cargo == '' and error_telefono == '' and error_ext == '' and error_celular == '' and error_email == '':
                lista_contactos.__getitem__(indice).nombre_contacto = nombre.strip()
                lista_contactos.__getitem__(indice).cargo_contacto = int(cargo)
                lista_contactos.__getitem__(indice).telefono_contacto = telefono.strip()
                lista_contactos.__getitem__(indice).ext_contacto = ext.strip()
                lista_contactos.__getitem__(indice).celular_contacto = celular.strip()
                lista_contactos.__getitem__(indice).email_contacto = email.strip()
                request.session['lista_contactos'] = lista_contactos
                render = render_to_string('ajax/contactosproveedor.html', {'user': user, 'contactos': lista_contactos } )
                dajax.assign('#reporte_contactos', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='none';")
                dajax.script("document.getElementById('fade').style.display='none';")
                dajax.alert('Contacto modificado correctamente')
            else:
                print 'error en campos de contacto'
                render = render_to_string('ajax/contactoadd.html', {'user': user, 'indice': indice, 'nombre': nombre, 'cargo': int(cargo), 'telefono': telefono, 'ext': ext, 'celular': celular, 'email': email, 'error_nombre': error_nombre, 'error_cargo': error_cargo, 'error_telefono': error_telefono, 'error_ext': error_ext, 'error_celular': error_celular, 'error_email': error_email, 'change': 1 } )
                dajax.assign('#light', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_contacto_proveedor2(request, indice):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        lista_contactos = None
        try:
            lista_contactos = request.session['lista_contactos']
        except :
            pass
        if lista_contactos != None:
            lista_contactos = request.session['lista_contactos']
            lista_contactos.__delitem__(indice)
            request.session['lista_contactos'] = lista_contactos
            render = render_to_string('ajax/contactosproveedor.html', {'user': user, 'contactos': lista_contactos } )
            dajax.assign('#reporte_contactos', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------------------------- SUMINISTROS ---------------------------------------------

def ventana_proveedor_suministro2(request):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        permisos_usuario = user.get_all_permissions()
        render = render_to_string('ajax/contactoadd.html', {'user': user, 'permisos': permisos_usuario, 'change': 0 } )
        dajax.assign('#light', 'innerHTML', render)
        dajax.script("document.getElementById('light').style.display='block';")
        dajax.script("document.getElementById('fade').style.display='block';")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

def seleccionar_proveedor_lista_proveedores_suministro_add2(request, parametro, proveedor_id, pagina, criterio):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        lista_proveedores = None
        try:
            lista_proveedores = request.session['proveedores']
        except :
            pass
        if lista_proveedores != None:
            proveedores_agregar = request.session['proveedores_agregar']
            proveedor_id = int(proveedor_id)
            for proveedor in proveedores_agregar:
                if proveedor['proveedor'].id == proveedor_id:
                    proveedores_agregar.remove(proveedor)
            request.session['proveedores_agregar'] = proveedores_agregar
            proveedores = Proveedor.objects.filter(estado_proveedor=True)
            criterio = criterio.strip()
            if criterio != "":
                try:
                    int(criterio)
                    proveedores = proveedores.filter(identificacion=criterio)
                except :
                    proveedores = proveedores.filter(Q(razon_social__icontains=criterio) | Q(nombre_comercial__icontains=criterio))
            for proveedor in lista_proveedores:
                proveedores = proveedores.exclude(id=proveedor['proveedor'].id)
            pag = Paginador(request, proveedores, 20, pagina)
            render = render_to_string('ajax/tabla_busqueda_proveedores.html', {'user': user, 'lista_proveedores': pag, 'criterio': criterio, 'proveedores_agregar': proveedores_agregar})
            dajax.assign('#light','innerHTML', render)
            if parametro == True:
                dajax.script("document.getElementById('id_option_" + str(proveedor_id) + "').checked=true;")
                dajax.script("document.getElementById('id_precio_" + str(proveedor_id) + "').disabled=false;")
                dajax.script("document.getElementById('id_option_iva_" + str(proveedor_id) + "').disabled=false;")
                dajax.script("document.getElementById('ahref_agregar_" + str(proveedor_id) + "').style.display = 'block';")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_proveedor_suministro_add2(request, proveedor_id, precio, iva, criterio, pagina):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        precio = precio.strip()
        lista_proveedores = None
        try:
            lista_proveedores = request.session['proveedores']
        except :
            pass
        if lista_proveedores != None:
            error_precio = validar_cadena(precio)
            if error_precio == '':
                error_precio = validar_cantidad_float_digitos(str(precio))
                if error_precio == '':
                    error_precio = validar_cantidad_float(precio)
                    if error_precio == '':
                        precio = float(precio)
                        proveedores_agregar = request.session['proveedores_agregar']
                        error_precio = validar_cantidad_float_0(precio)
                        if error_precio == '':
                            proveedor = Proveedor.objects.get(id=proveedor_id)
                            if iva == True:
                                iva = 0.16
                            else:
                                iva = 0
                            proveedores_agregar.append({'proveedor': proveedor, 'precio': precio, 'iva': iva})
                            request.session['proveedores_agregar'] = proveedores_agregar
                            proveedores = Proveedor.objects.filter(estado_proveedor=True)
                            criterio = criterio.strip()
                            if criterio != "":
                                try:
                                    int(criterio)
                                    proveedores = proveedores.filter(identificacion=criterio)
                                except :
                                    proveedores = proveedores.filter(Q(razon_social__icontains=criterio) | Q(nombre_comercial__icontains=criterio))

                            for proveedor in lista_proveedores:
                                proveedores = proveedores.exclude(id=proveedor['proveedor'].id)
                            pag = Paginador(request, proveedores, 20, pagina)
                            render = render_to_string('ajax/tabla_busqueda_proveedores.html', {'user': user, 'lista_proveedores': pag, 'criterio': criterio, 'proveedores_agregar': proveedores_agregar})
                            dajax.assign('#light','innerHTML', render)
                            dajax.script("document.getElementById('id_cargando_" + str(proveedor_id) + "').style.visibility = 'none';")
            if error_precio != '':
                dajax.script("document.getElementById('id_label_error_precio_"+str(proveedor_id)+"').innerHTML='"+error_precio+"';")
                dajax.script("document.getElementById('id_precio_"+str(proveedor_id)+"').disabled=false;")
                dajax.script("document.getElementById('id_precio_"+str(proveedor_id)+"').focus();")
                dajax.script("document.getElementById('id_precio_"+str(proveedor_id)+"').select();")
                dajax.script("document.getElementById('id_option_"+str(proveedor_id)+"').checked=true;")
                dajax.script("document.getElementById('ahref_agregar_" + str(proveedor_id) + "').style.display = 'block';")
                dajax.script("document.getElementById('id_cargando_" + str(proveedor_id) + "').style.display = 'none';")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_proveedores_suministro_add2(request):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proveedores = None
        try:
            proveedores = request.session['proveedores']
        except :
            pass
        if proveedores != None:
            proveedores_agregar = request.session['proveedores_agregar']
            if len(proveedores_agregar) > 0:
                for proveedor_agregar in proveedores_agregar:
                    proveedores.append({'proveedor': proveedor_agregar['proveedor'], 'precio': proveedor_agregar['precio'], 'iva': proveedor_agregar['iva']})
            request.session['proveedores_agregar'] = []
            pag = Paginador(request, proveedores, 20, 1)
            render = render_to_string('ajax/proveedoressuministro.html', {'user': user, 'suministro_proveedores': pag })
            dajax.assign('#id_reporte_proveedores','innerHTML', render)
            dajax.script("document.getElementById('id_criterio_busqueda').value='';")
            dajax.script("document.getElementById('light').style.display='none';")
            dajax.script("document.getElementById('fade').style.display='none';")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def cancelar_agregar_proveedores_suministro_add2(request):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proveedores = None
        try:
            proveedores = request.session['proveedores']
        except :
            pass
        if proveedores != None:
            request.session['proveedores_agregar'] = []
            dajax.script("document.getElementById('id_criterio_busqueda').value='';")
            dajax.script("document.getElementById('light').style.display='none';")
            dajax.script("document.getElementById('fade').style.display='none';")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_proveedor_suministro_add2(request, proveedor_id, pagina):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proveedores = None
        try:
            proveedores = request.session['proveedores']
        except :
            pass
        if proveedores != None:
            proveedor_id = int(proveedor_id)
            indice_eliminar = 0
            indice = 0
            for proveedor in proveedores:
                if proveedor['proveedor'].id == proveedor_id:
                    indice_eliminar = indice
                indice = indice + 1
            del proveedores[indice_eliminar]
            request.session['proveedores'] = proveedores
            pag = Paginador(request, proveedores, 20, 1)
            render = render_to_string('ajax/proveedoressuministro.html', {'user': user, 'suministro_proveedores': pag })
            dajax.assign('#id_reporte_proveedores','innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_precio_proveedor_suministro_add2(request, proveedor_id, pagina):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proveedores = None
        try:
            proveedores = request.session['proveedores']
        except :
            pass
        if proveedores != None:
            for proveedor in proveedores:
                if proveedor['proveedor'].id == proveedor_id:
                    error = {'id': proveedor_id, 'value': str(proveedor['precio']), 'error': ''}
            pag = Paginador(request, proveedores, 20, pagina)
            render = render_to_string('ajax/proveedoressuministro.html', {'user': user, 'suministro_proveedores': pag, 'error': error })
            dajax.assign('#id_reporte_proveedores','innerHTML', render)
            dajax.script("document.getElementById('id_text_precio_" + str(proveedor_id) + "').disabled =false;")
            dajax.script("document.getElementById('id_text_precio_" + str(proveedor_id) + "').select();")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_precio_proveedor_suministro_add2(request, proveedor_id, precio, pagina):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proveedores = None
        try:
            proveedores = request.session['proveedores']
        except :
            pass
        if proveedores != None:
            error = {'elemento': '', 'error': ''}
            error_precio = validar_cadena(precio)
            if error_precio == '':
                error_precio = validar_cantidad_float_digitos(str(precio))
            if error_precio == '':
                error_precio = validar_cantidad_float(precio)
            if error_precio == '':
                error_precio = validar_cantidad_float_0(precio)
            if error_precio == '':
                precio = float(precio)
                for proveedor in proveedores:
                    if proveedor['proveedor'].id == proveedor_id:
                        proveedor['precio'] = precio
                request.session['proveedores'] = proveedores
            if error_precio != '':
                error = {'id': proveedor_id, 'value': precio, 'error': error_precio}
            pag = Paginador(request, proveedores, 20, pagina)
            render = render_to_string('ajax/proveedoressuministro.html', {'user': user, 'suministro_proveedores': pag, 'error': error })
            dajax.assign('#id_reporte_proveedores','innerHTML', render)
            if error_precio != '':
                dajax.script("document.getElementById('id_text_precio_" + str(proveedor_id) + "').select();")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_iva_proveedor_suministro_add2(request, proveedor_id, pagina):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proveedores = None
        try:
            proveedores = request.session['proveedores']
        except :
            pass
        if proveedores != None:
            pag = Paginador(request, proveedores, 20, pagina)
            render = render_to_string('ajax/proveedoressuministro.html', {'user': user, 'suministro_proveedores': pag })
            dajax.assign('#id_reporte_proveedores','innerHTML', render)
            dajax.script("document.getElementById('id_ima_3_"+ str(proveedor_id) + "').style.display='none';")
            dajax.script("document.getElementById('id_ima_4_" + str(proveedor_id) + "').style.display='block';")
            dajax.script("document.getElementById('id_opcion_iva_" + str(proveedor_id) + "').disabled =false;")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_iva_proveedor_suministro_add2(request, proveedor_id, iva, pagina):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proveedores = None
        try:
            proveedores = request.session['proveedores']
        except :
            pass
        if proveedores != None:
            for proveedor in proveedores:
                if proveedor['proveedor'].id == proveedor_id:
                    if iva == '1':
                        proveedor['iva'] = 0.16
                    elif iva == '0':
                        proveedor['iva'] = 0
            request.session['proveedores'] = proveedores
            pag = Paginador(request, proveedores, 20, pagina)
            render = render_to_string('ajax/proveedoressuministro.html', {'user': user, 'suministro_proveedores': pag })
            dajax.assign('#id_reporte_proveedores','innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------------------------- APUS ---------------------------------------------
def seleccionar_suministro_lista_suministros_apu_add2(request, parametro, suministro_id, pagina, clasificacion_general, criterio):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        lista_suministros = None
        try:
            lista_suministros = request.session['suministros']
        except :
            pass
        if lista_suministros != None:
            suministros_agregar = request.session['suministros_agregar']
            suministro_id = int(suministro_id)
            for suministro in suministros_agregar:
                if suministro['suministro'].id == suministro_id:
                    suministros_agregar.remove(suministro)
            request.session['suministros_agregar'] = suministros_agregar

            suministros = Suministro.objects.filter(estado_suministro=True)
            if clasificacion_general != '0':
                suministros = suministros.filter(clasificacion_general=clasificacion_general)
            if criterio != "":
                suministros = suministros.filter(Q(nombre__icontains=criterio) | Q(sinonimos__icontains=criterio))

            for suministro in lista_suministros:
                suministros = suministros.exclude(id=suministro['suministro'].id)

            for suministro in suministros:
                suministro_proveedores = SuministroProveedor.objects.filter(suministro=suministro)
                promedio_precio_suministro = 0
                contador_proveedores = 0
                for suministro_proveedor in suministro_proveedores:
                    promedio_precio_suministro = round(promedio_precio_suministro + (round(suministro_proveedor.precio_suministro+(round(suministro_proveedor.precio_suministro*suministro_proveedor.iva_suministro, 2)), 2)), 2)
                    contador_proveedores = contador_proveedores+1
                if contador_proveedores == 0:
                    contador_proveedores=1
                promedio_precio_suministro = round(promedio_precio_suministro/contador_proveedores, 2)
                suministro.promedio_precio_suministro = promedio_precio_suministro
            pag = Paginador(request, suministros, 20, pagina)
            render = render_to_string('ajax/busquedasuministrosapuadd.html', {'user': user, 'lista_suministros': pag, 'clasificacion_general': clasificacion_general, 'criterio': criterio, 'suministros_agregar': suministros_agregar })
            dajax.assign('#light','innerHTML', render)
            if parametro == True:
                dajax.script("document.getElementById('id_option_" + str(suministro_id) + "').checked=true")
                dajax.script("document.getElementById('id_cantidad_" + str(suministro_id) + "').disabled=false")
                dajax.script("document.getElementById('ahref_agregar_" + str(suministro_id) + "').style.display = 'block';")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_suministro_apu_add2(request, suministro_id, cantidad, clasificacion_general, criterio, pagina):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        lista_suministros = None
        try:
            lista_suministros = request.session['suministros']
        except :
            pass
        if lista_suministros != None:
            error_cantidad = validar_cadena(cantidad)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float_digitos(str(cantidad), decimales=4)
                if error_cantidad == '':
                    error_cantidad = validar_cantidad_float(cantidad)
                    if error_cantidad == '':
                        cantidad = float(cantidad)
                        suministros_agregar = request.session['suministros_agregar']
                        error_cantidad = validar_cantidad_float_0(cantidad)
                        if error_cantidad == '':
                            suministro = Suministro.objects.get(id=suministro_id)
                            suministro_proveedores = SuministroProveedor.objects.filter(suministro=suministro)
                            promedio_precio_suministro = 0
                            contador_proveedores = 0
                            for suministro_proveedor in suministro_proveedores:
                                promedio_precio_suministro = round(promedio_precio_suministro + (round(suministro_proveedor.precio_suministro + (round(suministro_proveedor.precio_suministro * suministro_proveedor.iva_suministro, 2)), 2)), 2)
                                contador_proveedores = contador_proveedores+1
                            if contador_proveedores == 0:
                                contador_proveedores=1
                            promedio_precio_suministro = round(promedio_precio_suministro / contador_proveedores, 2)
                            suministro.promedio_precio_suministro = promedio_precio_suministro
                            suministros_agregar.append({'suministro': suministro, 'precio': suministro.promedio_precio_suministro, 'cantidad': cantidad})
                            request.session['suministros_agregar'] = suministros_agregar

                            suministros = Suministro.objects.filter(estado_suministro=True)
                            if clasificacion_general != '0':
                                suministros = suministros.filter(clasificacion_general=clasificacion_general)
                            if criterio != "":
                                suministros = suministros.filter(Q(nombre__icontains=criterio) | Q(sinonimos__icontains=criterio))

                            for suministro in lista_suministros:
                                suministros = suministros.exclude(id=suministro['suministro'].id)

                            for suministro in suministros:
                                suministro_proveedores = SuministroProveedor.objects.filter(suministro=suministro)
                                promedio_precio_suministro = 0
                                contador_proveedores = 0
                                for suministro_proveedor in suministro_proveedores:
                                    promedio_precio_suministro = round(promedio_precio_suministro + (round(suministro_proveedor.precio_suministro + (round(suministro_proveedor.precio_suministro * suministro_proveedor.iva_suministro, 2)), 2)), 2)
                                    contador_proveedores = contador_proveedores + 1
                                if contador_proveedores == 0:
                                    contador_proveedores=1
                                promedio_precio_suministro = round(promedio_precio_suministro/contador_proveedores, 2)
                                suministro.promedio_precio_suministro = promedio_precio_suministro
                            pag = Paginador(request, suministros, 20, pagina)
                            render = render_to_string('ajax/busquedasuministrosapuadd.html', {'user': user, 'lista_suministros': pag, 'clasificacion_general': clasificacion_general, 'criterio': criterio, 'suministros_agregar': suministros_agregar })
                            dajax.assign('#light','innerHTML', render)
                            dajax.script("document.getElementById('id_cargando_" + str(suministro_id) + "').style.visibility = 'none';")
            if error_cantidad != '':
                dajax.script("document.getElementById('id_label_error_cantidad_"+str(suministro_id)+"').innerHTML='"+error_cantidad+"';")
                dajax.script("document.getElementById('id_cantidad_"+str(suministro_id)+"').disabled=false;")
                dajax.script("document.getElementById('id_cantidad_"+str(suministro_id)+"').focus();")
                dajax.script("document.getElementById('id_cantidad_"+str(suministro_id)+"').select();")
                dajax.script("document.getElementById('id_option_"+str(suministro_id)+"').checked=true;")
                dajax.script("document.getElementById('ahref_agregar_" + str(suministro_id) + "').style.display = 'block';")
                dajax.script("document.getElementById('id_cargando_" + str(suministro_id) + "').style.display = 'none';")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_suministros_apu_add2(request):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            suministros_agregar = request.session['suministros_agregar']
            if len(suministros_agregar) > 0:
                for suministro_agregar in suministros_agregar:
                    suministros.append({'suministro': suministro_agregar['suministro'], 'precio': suministro_agregar['precio'], 'cantidad': suministro_agregar['cantidad']})
            request.session['suministros_agregar'] = []
            pag = Paginador(request, suministros, 20, 1)
            render = render_to_string('ajax/suministrosapuadd.html', {'user': user, 'suministros_apu': pag })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
            pag = Paginador(request, [], 20, 1)
            render = render_to_string('ajax/busquedasuministrosapuadd.html', {'user': user, 'lista_suministros': pag, 'clasificacion_general': '0', 'criterio': '' })
            dajax.assign('#light','innerHTML', render)
            dajax.script("document.getElementById('light').style.display='none';")
            dajax.script("document.getElementById('fade').style.display='none';")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def cancelar_agregar_suministros_apu_add2(request):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        lista_suministros = None
        try:
            lista_suministros = request.session['suministros']
        except :
            pass
        if lista_suministros != None:
            request.session['suministros_agregar'] = []
            pag = Paginador(request, [], 20, 1)
            render = render_to_string('ajax/busquedasuministrosapuadd.html', {'user': user, 'lista_suministros': pag, 'clasificacion_general': '0', 'criterio': '' })
            dajax.assign('#light','innerHTML', render)
            dajax.script("document.getElementById('light').style.display='none';")
            dajax.script("document.getElementById('fade').style.display='none';")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_suministro_apu_add2(request, suministro_id, pagina):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            suministro_id = int(suministro_id)
            indice_eliminar = 0
            indice = 0
            for suministro in suministros:
                if suministro['suministro'].id == suministro_id:
                    indice_eliminar = indice
                indice = indice + 1
            del suministros[indice_eliminar]
            request.session['suministros'] = suministros
            pag = Paginador(request, suministros, 20, 1)
            render = render_to_string('ajax/suministrosapuadd.html', {'user': user, 'suministros_apu': pag })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_precio_suministro_apu_add2(request, suministro_id, pagina):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            for suministro in suministros:
                if suministro['suministro'].id == suministro_id:
                    error = {'id': suministro_id, 'item': 'precio', 'value': str(suministro['precio']), 'error': ''}
            pag = Paginador(request, suministros, 20, pagina)
            render = render_to_string('ajax/suministrosapuadd.html', {'user': user, 'suministros_apu': pag, 'error': error })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
            dajax.script("document.getElementById('id_text_precio_" + str(suministro_id) + "').select();")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_precio_suministro_apu_add2(request, suministro_id, precio, pagina):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            error = {}
            error_precio = validar_cadena(precio)
            if error_precio == '':
                error_precio = validar_cantidad_float_digitos(str(precio))
            if error_precio == '':
                error_precio = validar_cantidad_float(precio)
            if error_precio == '':
                error_precio = validar_cantidad_float_0(precio)
            if error_precio == '':
                precio = float(precio)
                for suministro in suministros:
                    if suministro['suministro'].id == suministro_id:
                        suministro['precio'] = precio
                request.session['suministros'] = suministros
            if error_precio != '':
                error = {'id': suministro_id, 'item': 'precio', 'value': precio, 'error': error_precio}
            pag = Paginador(request, suministros, 20, pagina)
            render = render_to_string('ajax/suministrosapuadd.html', {'user': user, 'suministros_apu': pag, 'error': error })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
            if error_precio != '':
                dajax.script("document.getElementById('id_text_precio_" + str(suministro_id) + "').select();")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_cantidad_suministro_apu_add2(request, suministro_id, pagina):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            for suministro in suministros:
                if suministro['suministro'].id == suministro_id:
                    error = {'id': suministro_id, 'item': 'cantidad', 'value': str(suministro['cantidad']), 'error': ''}
            pag = Paginador(request, suministros, 20, pagina)
            render = render_to_string('ajax/suministrosapuadd.html', {'user': user, 'suministros_apu': pag, 'error': error })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_" + str(suministro_id) + "').select();")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_cantidad_suministro_apu_add2(request, suministro_id, cantidad, pagina):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            error = {}
            error_cantidad = validar_cadena(cantidad)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float_digitos(str(cantidad), decimales=4)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float(cantidad)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float_0(cantidad)
            if error_cantidad == '':
                cantidad = float(cantidad)
                for suministro in suministros:
                    if suministro['suministro'].id == suministro_id:
                        suministro['cantidad'] = cantidad
                request.session['suministros'] = suministros
            if error_cantidad != '':
                error = {'id': suministro_id, 'item': 'cantidad', 'value': cantidad, 'error': error_cantidad}
            pag = Paginador(request, suministros, 20, pagina)
            render = render_to_string('ajax/suministrosapuadd.html', {'user': user, 'suministros_apu': pag, 'error': error })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
            if error_cantidad != '':
                dajax.script("document.getElementById('id_text_cantidad_" + str(suministro_id) + "').select();")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------------------------- APUS PROYECTO ---------------------------------------------

def ventana_anadir_persona_administrativo_proyecto2(request, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        #Se crea una lista en la session para las personas a adicionar
        request.session['personas_seleccionadas'] = []
        qry = "SELECT * FROM inverboy_usuario u, auth_user au WHERE u.user_ptr_id=au.id AND au.is_active=1"
        usuarios = Usuario.objects.raw(qry)
        lista_usuarios = []
        for usuario in usuarios:
            lista_usuarios.append(usuario)
        pag = Paginador(request, lista_usuarios, 20, 1)
        user = request.user
        render =  render_to_string('ajax/personassearchproyecto.html', {'user': user, 'lista_usuarios': pag, 'criterio': '', 'cargo_usuario': '0', 'personas_seleccionadas': [], 'proyecto': proyecto })
        dajax.assign('#light','innerHTML', render)
        dajax.script("document.getElementById('light').style.display='block';")
        dajax.script("document.getElementById('fade').style.display='block';")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def seleccionar_usuario_persona_administrativo_proyecto_add2(request, usuario_id, pagina, criterio, cargo_usuario, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        personas_seleccionadas = request.session['personas_seleccionadas']
        error_usuario = ''
        #Verifica que el usuario no se encuentre en la lista de personas seleccionadas que se quieren agregar al proyecto (personal Administrativo)
        if usuario_id not in personas_seleccionadas:
            #Se verifica si el usuario ya se encuentra vinculado al proyecto y que este activo
            usuario = None
            try:
                usuario = proyecto.personaadministrativoproyecto_set.get(persona__id=usuario_id)
            except :
                pass
            if usuario != None:
                if usuario.estado_registro == True:
                    error_usuario = 'El usuario ya se encuentra vinculado al proyecto'

            usuario_agregar = Usuario.objects.get(id=usuario_id)

            #Si el usuario no se ecuentra vinculado al proyecto, se verifica que si el usuario tiene como cargo 'Director de obra' solo exista uno en el proyecto
            if usuario_agregar.cargo == 'DIRECTOR DE OBRA':
                if error_usuario == '':
                    usuario = None
                    try:
                        usuarios_cargo = proyecto.personaadministrativoproyecto_set.filter(persona__cargo='DIRECTOR DE OBRA')
                        for usuario_cargo in usuarios_cargo:
                            if usuario_cargo.estado_registro == True:
                                usuario = usuario_cargo
                    except :
                        pass
                    if usuario != None:
                        error_usuario = 'Ya se encuentra asignado un usuario como DIRECTOR DE OBRA en el proyecto'

            #Si el usuario no se ecuentra vinculado al proyecto, se verifica que si el usuario tiene como cargo 'Almacenista' solo exista uno en el proyecto
            if usuario_agregar.cargo == 'ALMACENISTA':
                if error_usuario == '':
                    usuario = None
                    try:
                        usuarios_cargo = proyecto.personaadministrativoproyecto_set.filter(persona__cargo='ALMACENISTA')
                        for usuario_cargo in usuarios_cargo:
                            if usuario_cargo.estado_registro == True:
                                usuario = usuario_cargo
                    except :
                        pass
                    if usuario != None:
                        error_usuario = 'Ya se encuentra asignado un usuario como ALMACENISTA en el proyecto'

            #Si el usuario no se ecuentra vinculado al proyecto, se verifica que no se hayan seleccionado usuarios con cargos de 'Director de obra' ó 'Almacenista'
            if error_usuario == '':
                usuarios_seleccionados = Usuario.objects.filter(id__in=personas_seleccionadas)
                for usuario_cargo in usuarios_seleccionados:
                    if usuario_agregar.cargo == 'DIRECTOR DE OBRA':
                        if usuario_cargo.cargo == 'DIRECTOR DE OBRA':
                            error_usuario = 'Ya se ha seleccionado un usuario como DIRECTOR DE OBRA'
                    if usuario_agregar.cargo == 'ALMACENISTA':
                        if usuario_cargo.cargo == 'ALMACENISTA':
                            error_usuario = 'Ya se ha seleccionado un usuario como ALMACENISTA'

            #Si no se encontro ningún error para adicionar el usuario a la lista  de personas seleccionadas que se quieren agregar al proyecto (personal Administrativo)
            if error_usuario == '':
                personas_seleccionadas.append(usuario_id)
        else:
            personas_seleccionadas.remove(usuario_id)

        #Se actualiza la variable de la session
        request.session['personas_seleccionadas'] = personas_seleccionadas
        #Se inicializa la variable de error
        error = {}
        if error_usuario != '':
            error = {'id': usuario_id, 'error': error_usuario}
        #Se actualiza la interfaz
        qry = "SELECT * FROM inverboy_usuario u, auth_user au WHERE u.user_ptr_id=au.id AND au.is_active=1"
        if criterio != "":
            if criterio != '':
                criterio = criterio.replace("'",'"')
                try:
                    criterio = int(criterio)
                    qry = qry + " AND identificacion="+str(criterio)
                except:
                    qry = qry + " AND (CONCAT(first_name, ' ', last_name) LIKE '%%" + criterio + "%%' OR username LIKE '%%"+criterio+"%%')"
        if(cargo_usuario!="0"):
            qry = qry + " AND cargo='"+cargo_usuario+"'"
        usuarios = Usuario.objects.raw(qry)
        lista_usuarios = []
        for usuario in usuarios:
            lista_usuarios.append(usuario)
        pag = Paginador(request, lista_usuarios, 20, pagina)
        user = request.user
        render =  render_to_string('ajax/personassearchproyecto.html', {'user': user, 'lista_usuarios': pag, 'criterio': criterio, 'cargo_usuario': cargo_usuario, 'personas_seleccionadas': personas_seleccionadas, 'proyecto': proyecto, 'error': error })
        dajax.assign('#light','innerHTML', render)
        dajax.script("document.getElementById('light').style.display='block';")
        dajax.script("document.getElementById('fade').style.display='block';")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def anadir_personas_administrativo_proyecto_add2(request, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        personas_seleccionadas = request.session['personas_seleccionadas']
        for persona_seleccionada in personas_seleccionadas:
            usuario = Usuario.objects.get(id=persona_seleccionada)
            if usuario.is_active:
                persona_proyecto, creado = proyecto.personaadministrativoproyecto_set.get_or_create(persona=usuario)
                if creado == False:
                    persona_proyecto.estado_registro = True
                    persona_proyecto.save()
        #Actualiza la interfaz
        ids_usuarios_administracion_proyecto = proyecto.personaadministrativoproyecto_set.filter(estado_registro=True).values('persona_id')
        usuarios_administracion_proyecto = Usuario.objects.filter(id__in=ids_usuarios_administracion_proyecto)

        render =  render_to_string('ajax/personaladministrativoproyecto.html', {'user': user, 'usuarios_administracion_proyecto': usuarios_administracion_proyecto, 'proyecto': proyecto})
        dajax.assign('#personal_administrativo_proyecto','innerHTML', render)

        dajax.script("document.getElementById('light').style.display='none';")
        dajax.script("document.getElementById('fade').style.display='none';")
        dajax.alert("Las personas se han relacionado con el proyecto")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def cancelar_anadir_persona_administrativo_proyecto_add2(request, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        del request.session['personas_seleccionadas']
        render =  render_to_string('ajax/personassearchproyecto.html', {'user': user, 'lista_usuarios': [], 'criterio': '', 'cargo_usuario': '0', 'personas_seleccionadas': [], 'proyecto': proyecto, 'error': {} })
        dajax.assign('#light','innerHTML', render)
        dajax.script("document.getElementById('light').style.display='none';")
        dajax.script("document.getElementById('fade').style.display='none';")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_persona_administrativo_proyecto2(request, usuario_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        persona_proyecto = proyecto.personaadministrativoproyecto_set.get(persona__id=usuario_id)
        persona_proyecto.estado_registro = False
        persona_proyecto.save()

        #Actualiza la interfaz
        ids_usuarios_administracion_proyecto = proyecto.personaadministrativoproyecto_set.filter(estado_registro=True).values('persona_id')
        usuarios_administracion_proyecto = Usuario.objects.filter(id__in=ids_usuarios_administracion_proyecto)

        render =  render_to_string('ajax/personaladministrativoproyecto.html', {'user': user, 'usuarios_administracion_proyecto': usuarios_administracion_proyecto, 'proyecto': proyecto})
        dajax.assign('#personal_administrativo_proyecto','innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def ventana_persona_proyecto_add2(request, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_personaproyecto' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            qry = "SELECT p.* FROM inverboy_ordenservicio os, inverboy_proveedor p WHERE os.proveedor_id = p.id AND os.proyecto_id = " + str(proyecto_id) + " AND os.estado=1 GROUP BY p.id"
            proveedores = Proveedor.objects.raw(qry)
            render = render_to_string('ajax/personaproyectoadd.html', {'user': user, 'proveedores': proveedores, 'change': 0, 'proyecto': proyecto, 'error_identificacion': '', 'error_nombre': '', 'error_cargo': '', 'error_telefono': '', 'error_proveedor': '' } )
            dajax.assign('#light2', 'innerHTML', render)
            dajax.script("document.getElementById('light2').style.display='block';")
            dajax.script("document.getElementById('fade').style.display='block';")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def anadir_persona_anexa_proyecto2(request, identificacion, nombre, cargo, telefono, proveedor, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_personaproyecto' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            error_identificacion = validar_identificacion(identificacion)
            error_nombre = validar_cadena(nombre)
            if error_nombre == '':
                error_nombre = validar_cadena_caracteres_especiales(nombre)
            error_cargo = validar_cadena(cargo)
            error_telefono = validar_telefono(telefono)
            error_proveedor = validar_select(proveedor)
            if error_identificacion == '' and error_nombre == '' and error_cargo == '' and error_telefono == '' and error_proveedor == '':
                #Verifica si la persona ya esta registrada en el proyecto
                persona_existente = None
                try:
                    persona_existente = proyecto.personaproyecto_set.get(identificacion=identificacion)
                except :
                    pass
                #Si la nueva persona no esta registrada en el proyecto
                if persona_existente == None:
                    persona = PersonaProyecto()
                    persona.identificacion = identificacion
                    persona.nombre = nombre
                    persona.cargo = cargo
                    persona.telefono = telefono
                    proveedor = Proveedor.objects.get(id=proveedor)
                    persona.proveedor = proveedor
                    persona.proyecto = proyecto
                    usuario = Usuario.objects.get(id=request.user.id)
                    persona.persona = usuario
                    persona.save()
                    personas = proyecto.personaproyecto_set.filter(estado=True)
                    render = render_to_string('ajax/personasproyecto.html', {'user': user, 'proyecto': proyecto, 'personas': personas } )
                    dajax.assign('#personas_proyecto', 'innerHTML', render)
                    dajax.script("document.getElementById('light2').style.display='none';")
                    dajax.script("document.getElementById('fade').style.display='none';")
                #Si la nueva persona esta registrada en el proyecto
                else:
                    #Si la persona esta habilitada
                    if persona_existente.estado == True:
                        dajax.alert(u'Esta persona (identificación) ya se encuntra registrada en el proyecto.')
                    #Si la persona se encuentra inhabilitada (Eliminada)
                    else :
                        persona_existente.estado = True
                        persona_existente.save()
                        personas = proyecto.personaproyecto_set.filter(estado=True)
                        render = render_to_string('ajax/personasproyecto.html', {'user': user, 'proyecto': proyecto, 'personas': personas } )
                        dajax.assign('#personas_proyecto', 'innerHTML', render)
                        dajax.script("document.getElementById('light2').style.display='none';")
                        dajax.script("document.getElementById('fade').style.display='none';")
                        dajax.alert(u'Esta persona (identificación) ya se encontraba registrada anteriormente en el proyecto, se ha reactivado de nuevo con los datos anteriormente guardados.')
            else:
                qry = "SELECT p.* FROM inverboy_ordenservicio os, inverboy_proveedor p WHERE os.proveedor_id = p.id AND os.proyecto_id = " + str(proyecto_id) + " AND os.estado=1 GROUP BY p.id"
                proveedores = Proveedor.objects.raw(qry)
                if error_proveedor == '':
                    proveedor = Proveedor.objects.get(id=proveedor)
                render = render_to_string('ajax/personaproyectoadd.html', {'user': user, 'proveedores': proveedores, 'change': 0, 'proyecto': proyecto, 'identificacion': identificacion, 'nombre': nombre, 'cargo': cargo, 'telefono': telefono, 'actual_proveedor': proveedor, 'error_identificacion': error_identificacion, 'error_nombre': error_nombre, 'error_cargo': error_cargo, 'error_telefono': error_telefono, 'error_proveedor': error_proveedor } )
                dajax.assign('#light2', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def ventana_modificar_persona_anexa_proyecto2(request, persona_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_personaproyecto' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            persona = proyecto.personaproyecto_set.get(id=persona_id)
            qry = "SELECT p.* FROM inverboy_ordenservicio os, inverboy_proveedor p WHERE os.proveedor_id = p.id AND os.proyecto_id = " + str(proyecto_id) + " AND os.estado=1 GROUP BY p.id"
            proveedores = Proveedor.objects.raw(qry)
            render = render_to_string('ajax/personaproyectoadd.html', {'user': user, 'proveedores': proveedores, 'change': 1, 'proyecto': proyecto, 'persona': persona, 'identificacion': persona.identificacion, 'nombre': persona.nombre, 'cargo': persona.cargo, 'telefono': persona.telefono, 'actual_proveedor': persona.proveedor } )
            dajax.assign('#light2', 'innerHTML', render)
            dajax.script("document.getElementById('light2').style.display='block';")
            dajax.script("document.getElementById('fade').style.display='block';")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_persona_anexa_proyecto2(request, persona_id, identificacion, nombre, cargo, telefono, proveedor, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_personaproyecto' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            persona = proyecto.personaproyecto_set.get(id=persona_id)
            error_identificacion = validar_identificacion(identificacion)
            error_nombre = validar_cadena(nombre)
            error_cargo = validar_cadena(cargo)
            error_telefono = validar_telefono(telefono)
            error_proveedor = validar_select(proveedor)
            if error_identificacion == '' and error_nombre == '' and error_cargo == '' and error_telefono == '' and error_proveedor == '':
                persona_existente = None
                if persona.identificacion != int(identificacion):
                    try:
                        persona_existente = PersonaProyecto.objects.get(identificacion=identificacion, estado=True)
                    except :
                        persona_existente = None
                if persona_existente == None:
                    persona.identificacion = identificacion
                    persona.nombre = nombre
                    persona.cargo = cargo
                    persona.telefono = telefono
                    proveedor = Proveedor.objects.get(id=proveedor)
                    persona.proveedor = proveedor
                    persona.proyecto = proyecto
                    usuario = Usuario.objects.get(id=request.user.id)
                    persona.persona = usuario
                    persona.save()
                    personas = PersonaProyecto.objects.filter(estado=True, proyecto=proyecto)
                    render = render_to_string('ajax/personasproyecto.html', {'user': user, 'proyecto': proyecto, 'personas': personas } )
                    dajax.assign('#personas_proyecto', 'innerHTML', render)
                    dajax.script("document.getElementById('light2').style.display='none';")
                    dajax.script("document.getElementById('fade').style.display='none';")
                else:
                    dajax.alert(u'Esta identificación se enuentra asignada a una persona al proyecto actualmente')
            else:
                qry = "SELECT p.* FROM inverboy_ordenservicio os, inverboy_proveedor p WHERE os.proveedor_id = p.id AND os.proyecto_id = " + str(proyecto_id) + " AND os.estado=1 GROUP BY p.id"
                proveedores = Proveedor.objects.raw(qry)
                if error_proveedor == '':
                    proveedor = Proveedor.objects.get(id=proveedor)
                render = render_to_string('ajax/personaproyectoadd.html', {'user': user, 'proveedores': proveedores, 'change': 0, 'proyecto': proyecto, 'identificacion': identificacion, 'nombre': nombre, 'cargo': cargo, 'telefono': telefono, 'actual_proveedor': proveedor, 'error_identificacion': error_identificacion, 'error_nombre': error_nombre, 'error_cargo': error_cargo, 'error_telefono': error_telefono, 'error_proveedor': error_proveedor } )
                dajax.assign('#light2', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_persona_proyecto2(request, persona_id, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user#Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_personaproyecto' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            persona = PersonaProyecto.objects.get(id=persona_id)
            persona.estado = False
            persona.save()
            personas = PersonaProyecto.objects.filter(estado=True, proyecto=proyecto)
            render = render_to_string('ajax/personasproyecto.html', {'user': user, 'proyecto': proyecto, 'personas': personas } )
            dajax.assign('#personas_proyecto', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_suministro_apu_proyecto_add2(request, suministro_id, cantidad, clasificacion_general, criterio, pagina, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        lista_suministros = None
        try:
            lista_suministros = request.session['suministros']
        except :
            pass
        if lista_suministros != None:
            error_cantidad = validar_cadena(cantidad)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float_digitos(str(cantidad), decimales=4)
                if error_cantidad == '':
                    error_cantidad = validar_cantidad_float(cantidad)
                    if error_cantidad == '':
                        cantidad = float(cantidad)
                        suministros_agregar = request.session['suministros_agregar']
                        error_cantidad = validar_cantidad_float_0(cantidad)
                        if error_cantidad == '':
                            suministro = Suministro.objects.get(id=suministro_id)
                            suministro_proveedores = SuministroProveedor.objects.filter(suministro=suministro)
                            promedio_precio_suministro = 0
                            contador_proveedores = 0
                            for suministro_proveedor in suministro_proveedores:
                                promedio_precio_suministro = round(promedio_precio_suministro + (round(suministro_proveedor.precio_suministro+(round(suministro_proveedor.precio_suministro*suministro_proveedor.iva_suministro, 2)), 2)), 2)
                                contador_proveedores = contador_proveedores+1
                            if contador_proveedores == 0:
                                contador_proveedores=1
                            promedio_precio_suministro = round(promedio_precio_suministro/contador_proveedores, 2)
                            suministro.promedio_precio_suministro = promedio_precio_suministro
                            suministros_agregar.append({'suministro': suministro, 'precio': suministro.promedio_precio_suministro, 'cantidad': cantidad})
                            request.session['suministros_agregar'] = suministros_agregar

                            suministros = Suministro.objects.filter(estado_suministro=True)
                            if clasificacion_general != '0':
                                suministros = suministros.filter(clasificacion_general=clasificacion_general)
                            if criterio != "":
                                suministros = suministros.filter(Q(nombre__icontains=criterio) | Q(sinonimos__icontains=criterio))

                            for suministro in lista_suministros:
                                suministros = suministros.exclude(id=suministro['suministro'].id)

                            for suministro in suministros:
                                suministro_proveedores = SuministroProveedor.objects.filter(suministro=suministro)
                                promedio_precio_suministro = 0
                                contador_proveedores = 0
                                for suministro_proveedor in suministro_proveedores:
                                    promedio_precio_suministro = round(promedio_precio_suministro + (round(suministro_proveedor.precio_suministro+(round(suministro_proveedor.precio_suministro*suministro_proveedor.iva_suministro, 2)), 2)), 2)
                                    contador_proveedores = contador_proveedores+1
                                if contador_proveedores == 0:
                                    contador_proveedores=1
                                promedio_precio_suministro = round(promedio_precio_suministro/contador_proveedores, 2)
                                suministro.promedio_precio_suministro = promedio_precio_suministro

                            pag = Paginador(request, suministros, 20, pagina)
                            render = render_to_string('ajax/tabla_busqueda_suministros.html', {'user': user, 'lista_suministros': pag, 'clasificacion_general': clasificacion_general, 'criterio': criterio, 'suministros_agregar': suministros_agregar, 'proyecto': proyecto })
                            dajax.assign('#light','innerHTML', render)
            if error_cantidad != '':
                dajax.script("document.getElementById('id_label_error_cantidad_"+str(suministro_id)+"').innerHTML='"+error_cantidad+"';")
                dajax.script("document.getElementById('id_cantidad_"+str(suministro_id)+"').disabled=false;")
                dajax.script("document.getElementById('id_cantidad_"+str(suministro_id)+"').select();")
                dajax.script("document.getElementById('id_option_"+str(suministro_id)+"').checked=true;")
                dajax.script("document.getElementById('ahref_agregar_" + str(suministro_id) + "').style.display = 'block';")
                dajax.script("document.getElementById('id_cargando_" + str(suministro_id) + "').style.display = 'none';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/' + str(proyecto.id) + '/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_suministros_apu_proyecto_add2(request, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            suministros_agregar = request.session['suministros_agregar']
            if len(suministros_agregar) > 0:
                for suministro_agregar in suministros_agregar:
                    suministros.append({'suministro': suministro_agregar['suministro'], 'precio': suministro_agregar['precio'], 'cantidad': suministro_agregar['cantidad']})
            request.session['suministros_agregar'] = []
            pag = Paginador(request, suministros, 20, 1)
            apu_manejo_estandar = request.session['apu_manejo_estandar']
            suministro_estandar = request.session['id_suministro_estandar']
            render = render_to_string('ajax/suministrosapuproyectoadd.html', {'user': user, 'suministros_apu': pag, 'apu_manejo_estandar': apu_manejo_estandar, 'suministro_estandar': suministro_estandar, 'proyecto': proyecto })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
            dajax.script("document.getElementById('id_criterio_busqueda').value = '';")
            dajax.script("document.getElementById('id_clasificacion_general_suministro').value = 0;")
            dajax.script("document.getElementById('light').style.display='none';")
            dajax.script("document.getElementById('fade').style.display='none';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/' + str(proyecto.id) + '/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def cancelar_agregar_suministros_apu_proyecto_add2(request, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            request.session['suministros_agregar'] = []
            dajax.script("document.getElementById('id_criterio_busqueda').value = '';")
            dajax.script("document.getElementById('id_clasificacion_general_suministro').value = 0;")
            dajax.script("document.getElementById('light').style.display='none';")
            dajax.script("document.getElementById('fade').style.display='none';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/' + str(proyecto.id) + '/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_suministro_apu_proyecto_add2(request, suministro_id, pagina, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            suministro_id = int(suministro_id)
            apu_manejo_estandar = request.session['apu_manejo_estandar']
            suministro_estandar = request.session['id_suministro_estandar']
            if apu_manejo_estandar:
                if suministro_estandar == suministro_id:
                    request.session['apu_manejo_estandar'] = apu_manejo_estandar = False
                    request.session['id_suministro_estandar'] = suministro_estandar = None
                    dajax.script("document.getElementById('id_apu_manejo_estandar').checked=false")
            indice_eliminar = 0
            indice = 0
            for suministro in suministros:
                if suministro['suministro'].id == suministro_id:
                    indice_eliminar = indice
                indice = indice + 1
            del suministros[indice_eliminar]
            request.session['suministros'] = suministros
            pag = Paginador(request, suministros, 20, 1)
            render = render_to_string('ajax/suministrosapuproyectoadd.html', {'user': user, 'suministros_apu': pag, 'apu_manejo_estandar': apu_manejo_estandar, 'suministro_estandar': suministro_estandar, 'proyecto': proyecto })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/' + str(proyecto.id) + '/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def seleccionar_suministro_lista_suministros_apu_proyecto_add2(request, parametro, suministro_id, pagina, clasificacion_general, criterio, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        lista_suministros = None
        try:
            lista_suministros = request.session['suministros']
        except :
            pass
        if lista_suministros != None:
            suministros_agregar = request.session['suministros_agregar']
            suministro_id = int(suministro_id)
            for suministro in suministros_agregar:
                if suministro['suministro'].id == suministro_id:
                    suministros_agregar.remove(suministro)
            request.session['suministros_agregar'] = suministros_agregar

            suministros = Suministro.objects.filter(estado_suministro=True)
            if clasificacion_general != '0':
                suministros = suministros.filter(clasificacion_general=clasificacion_general)
            if criterio != "":
                suministros = suministros.filter(Q(nombre__icontains=criterio) | Q(sinonimos__icontains=criterio))

            for suministro in lista_suministros:
                suministros = suministros.exclude(id=suministro['suministro'].id)

            for suministro in suministros:
                suministro_proveedores = SuministroProveedor.objects.filter(suministro=suministro)
                promedio_precio_suministro = 0
                contador_proveedores = 0
                for suministro_proveedor in suministro_proveedores:
                    promedio_precio_suministro = round(promedio_precio_suministro + (round(suministro_proveedor.precio_suministro+(round(suministro_proveedor.precio_suministro*suministro_proveedor.iva_suministro, 2)), 2)), 2)
                    contador_proveedores = contador_proveedores+1
                if contador_proveedores == 0:
                    contador_proveedores=1
                promedio_precio_suministro = round(promedio_precio_suministro/contador_proveedores, 2)
                suministro.promedio_precio_suministro = promedio_precio_suministro

            pag = Paginador(request, suministros, 20, pagina)
            render = render_to_string('ajax/tabla_busqueda_suministros.html', {'user': user, 'lista_suministros': pag, 'clasificacion_general': clasificacion_general, 'criterio': criterio, 'suministros_agregar': suministros_agregar, 'proyecto': proyecto })
            dajax.assign('#light','innerHTML', render)
            if parametro == True:
                dajax.script("document.getElementById('id_option_" + str(suministro_id) + "').checked=true;")
                dajax.script("document.getElementById('id_cantidad_" + str(suministro_id) + "').disabled=false;")
                dajax.script("document.getElementById('ahref_agregar_" + str(suministro_id) + "').style.display = 'block';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/' + str(proyecto.id) + '/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def calcular_valor_apu_proyecto_add2(request, cantidad_proyecto, cantidad_apu, proyecto_id):
    from decimal import *
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            error_cantidad_proyecto = validar_cadena(cantidad_proyecto)
            if error_cantidad_proyecto == '':
                error_cantidad_proyecto = validar_cantidad_float(cantidad_proyecto)
            if error_cantidad_proyecto == '':
                error_cantidad_proyecto = validar_cantidad_float_0(cantidad_proyecto)
            if error_cantidad_proyecto == '':
                error_cantidad_proyecto = validar_cantidad_float_digitos(cantidad_proyecto)
            error_cantidad_apu = validar_cadena(cantidad_apu)
            if error_cantidad_apu == '':
                error_cantidad_apu = validar_cantidad_float(cantidad_apu)
            if error_cantidad_apu == '':
                error_cantidad_apu = validar_cantidad_float_0(cantidad_apu)
            if error_cantidad_apu == '':
                error_cantidad_apu = validar_cantidad_float_digitos(cantidad_apu)
            if error_cantidad_proyecto == '' and error_cantidad_apu == '':
                cantidad_proyecto = float(cantidad_proyecto)
                cantidad_apu = float(cantidad_apu)

                valor = 0.0
                for suministro in suministros:
                    valor = valor + round(suministro['cantidad'] * suministro['precio'], 2)

                valor_unitario = Decimal(round(valor, 2))
                cantidad_total = Decimal(round(Decimal(cantidad_proyecto) * Decimal(cantidad_apu), 2))
                valor_total = Decimal(round(valor_unitario * cantidad_total, 2))

                # Función de redondeo con round()
                valor_unitario = round(valor_unitario, 2)
                cantidad_total = round(cantidad_total, 2)
                valor_total = round(valor_total, 2)

                # Valida si se esta modificando un APU
                apu_proyecto_id = None
                try:
                    apu_proyecto_id = request.session['apu_proyecto_id']
                except :
                    pass

                if apu_proyecto_id != None:
                    apu_proyecto = proyecto.apuproyecto_set.get(id=apu_proyecto_id)
                    suministros_apu = apu_proyecto.suministroapuproyecto_set.all()
                    for suministro in suministros:
                        for suministro_apu in suministros_apu:
                            if suministro['suministro'].id == suministro_apu.suministro.id:
                                nueva_cantidad_total_suministro = round(float(suministro['cantidad']) * cantidad_total, 2)
                                if nueva_cantidad_total_suministro < suministro_apu.suministrorequisicion_set.all().aggregate(Sum('cantidad_requerida'))['cantidad_requerida__sum']:
                                    error_cantidad_proyecto = 'La cantidad proyecto debe ser proporcional a la cantidad apu y las cantidades de cada suministro, (Según las cantidades requeridas)'
                                    error_cantidad_apu = 'La cantidad apu debe ser proporcional a la cantidad proyecto y las cantidades de cada suministro, (Según las cantidades requeridas)'

                dajax.script("document.getElementById('id_cantidad_total').value='';")
                dajax.script("document.getElementById('id_valor_unitario').value='';")
                dajax.script("document.getElementById('id_valor_total').value='';")

                if error_cantidad_proyecto == '' and error_cantidad_apu == '':
                    dajax.script("document.getElementById('id_cantidad_total').value='" + str(cantidad_total)+"';")
                    dajax.script("document.getElementById('id_valor_unitario').value='" + str(valor_unitario)+"';")
                    dajax.script("document.getElementById('id_valor_total').value='" + str(valor_total)+"';")
                    
            dajax.script("document.getElementById('id_label_error_cantidad_proyecto').innerHTML='" + error_cantidad_proyecto+"';")
            dajax.script("document.getElementById('id_label_error_cantidad_apu').innerHTML='" + error_cantidad_apu+"';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/' + str(proyecto.id) + '/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def redondeo(cifra, digitos=0):
  """Rutina par redondeo de cifras decimales como para uso en contabilidad"""
  # Symmetric Arithmetic Rounding for decimal numbers
  if type(cifra) != decimal.Decimal:
    cifra = decimal.Decimal(str(cifra))
  return cifra.quantize(decimal.Decimal("1") / (decimal.Decimal('10') ** digitos), decimal.ROUND_HALF_UP)


def activar_input_precio_suministro_apu_proyecto_add2(request, suministro_id, pagina, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            apu_manejo_estandar = request.session['apu_manejo_estandar']
            suministro_estandar = request.session['id_suministro_estandar']

            for suministro in suministros:
                if suministro['suministro'].id == suministro_id:
                    error = {'id': suministro_id, 'item': 'precio', 'value': str(suministro['precio']), 'error': ''}
            pag = Paginador(request, suministros, 20, pagina)
            render = render_to_string('ajax/suministrosapuproyectoadd.html', {'user': user, 'suministros_apu': pag, 'apu_manejo_estandar': apu_manejo_estandar, 'suministro_estandar': suministro_estandar, 'error': error, 'proyecto': proyecto })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
            dajax.script("document.getElementById('id_text_precio_" + str(suministro_id) + "').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/' + str(proyecto.id) + '/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_precio_suministro_apu_proyecto_add2(request, suministro_id, precio, pagina, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            error = {}
            error_precio = validar_cadena(precio)
            if error_precio == '':
                error_precio = validar_cantidad_float_digitos(precio)
            if error_precio == '':
                error_precio = validar_cantidad_float(precio)
            if error_precio == '':
                error_precio = validar_cantidad_float_0(precio)
            if error_precio == '':
                precio = float(precio)
                for suministro in suministros:
                    if suministro['suministro'].id == suministro_id:
                        suministro['precio'] = precio
                request.session['suministros'] = suministros
            if error_precio != '':
                error = {'id': suministro_id, 'item': 'precio', 'value': precio, 'error': error_precio}
            pag = Paginador(request, suministros, 20, pagina)
            apu_manejo_estandar = request.session['apu_manejo_estandar']
            suministro_estandar = request.session['id_suministro_estandar']
            render = render_to_string('ajax/suministrosapuproyectoadd.html', {'user': user, 'suministros_apu': pag, 'apu_manejo_estandar': apu_manejo_estandar, 'suministro_estandar': suministro_estandar, 'error': error, 'proyecto': proyecto })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
            if error_precio != '':
                dajax.script("document.getElementById('id_text_precio_" + str(suministro_id) + "').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/' + str(proyecto.id) + '/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_cantidad_suministro_apu_proyecto_add2(request, suministro_id, pagina, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            apu_manejo_estandar = request.session['apu_manejo_estandar']
            suministro_estandar = request.session['id_suministro_estandar']

            for suministro in suministros:
                if suministro['suministro'].id == suministro_id:
                    error = {'id': suministro_id, 'item': 'cantidad', 'value': str(suministro['cantidad']), 'error': ''}
            pag = Paginador(request, suministros, 20, pagina)
            render = render_to_string('ajax/suministrosapuproyectoadd.html', {'user': user, 'suministros_apu': pag, 'apu_manejo_estandar': apu_manejo_estandar, 'suministro_estandar': suministro_estandar, 'error': error, 'proyecto': proyecto })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_" + str(suministro_id) + "').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/' + str(proyecto.id) + '/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_cantidad_suministro_apu_proyecto_add2(request, suministro_id, cantidad, cantidad_proyecto, cantidad_apu, pagina, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            error = {}
            error_cantidad = validar_cadena(cantidad)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float_digitos(cantidad, decimales=4)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float(cantidad)
            if error_cantidad == '':
                #Verifica si el proyecto se encuentra en presupuesto
                if proyecto.proceso_proyecto == 1:
                    #Si se encuentra en presupuesto no se permiten cantidades en 0
                    error_cantidad = validar_cantidad_float_0(cantidad)
                elif proyecto.proceso_proyecto == 2:
                    #Si no se encuentra en presupuesto se permiten cantidades en 0 (Como si se eliminara el suministro)
                    error_cantidad = validar_cantidad_float_negativo(cantidad)
            if error_cantidad == '':
                cantidad = float(cantidad)
                for suministro in suministros:
                    if suministro['suministro'].id == suministro_id:
                        # Valida si se esta modificando un APU
                        apu_proyecto_id = None
                        try:
                            apu_proyecto_id = request.session['apu_proyecto_id']
                        except :
                            pass
                        if apu_proyecto_id != None:
                            apu_proyecto = proyecto.apuproyecto_set.get(id=apu_proyecto_id)
                            if cantidad_proyecto != None and cantidad_apu != None:
                                if cantidad_proyecto != '' and cantidad_apu != '':
                                    cantidad_total = round(float(cantidad_proyecto) * float(cantidad_apu), 2)
                                    nueva_cantidad_total_suministro = round(cantidad * cantidad_total, 2)
                                    suministro_apu = None
                                    try:
                                        suministro_apu = apu_proyecto.suministroapuproyecto_set.get(suministro__id=suministro_id)
                                    except :
                                        pass
                                    if suministro_apu != None:
                                        if nueva_cantidad_total_suministro < suministro_apu.suministrorequisicion_set.aggregate(Sum('cantidad_requerida'))['cantidad_requerida__sum']:
                                            error_cantidad = 'La nueva cantidad debe ser proporcional a la cantidad proyecto y la cantidad apu (Según la cantidad requerida)'
                                        else:
                                            suministro['cantidad'] = cantidad
                                    else:
                                        suministro['cantidad'] = cantidad
                                else:
                                    cantidad_total = round(apu_proyecto.cantidad_proyecto * apu_proyecto.cantidad_apu, 2)
                                    nueva_cantidad_total_suministro = round(cantidad * cantidad_total, 2)
                                    if nueva_cantidad_total_suministro < apu_proyecto.suministroapuproyecto_set.get(suministro__id=suministro_id).suministrorequisicion_set.aggregate(Sum('cantidad_requerida'))['cantidad_requerida__sum']:
                                        error_cantidad = 'La nueva cantidad debe ser proporcional a la cantidad proyecto y la cantidad apu (Según la cantidad requerida)'
                                    else:
                                        suministro['cantidad'] = cantidad
                            else:
                                 suministro['cantidad'] = cantidad
                        else:
                            suministro['cantidad'] = cantidad
                request.session['suministros'] = suministros
            if error_cantidad != '':
                error = {'id': suministro_id, 'item': 'cantidad', 'value': cantidad, 'error': error_cantidad}
            pag = Paginador(request, suministros, 20, pagina)
            apu_manejo_estandar = request.session['apu_manejo_estandar']
            suministro_estandar = request.session['id_suministro_estandar']
            render = render_to_string('ajax/suministrosapuproyectoadd.html', {'user': user, 'suministros_apu': pag, 'apu_manejo_estandar': apu_manejo_estandar, 'suministro_estandar': suministro_estandar, 'error': error, 'proyecto': proyecto })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
            if error_cantidad != '':
                dajax.script("document.getElementById('id_text_cantidad_" + str(suministro_id) + "').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/' + str(proyecto.id) + '/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def cambiar_manejo_estandar_apu_proyecto_add2(request, parametro, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            if parametro == True:
                request.session['apu_manejo_estandar'] = True
            else:
                request.session['apu_manejo_estandar'] = False
            request.session['id_suministro_estandar'] = None
            pag = Paginador(request, suministros, 20, 1)
            render = render_to_string('ajax/suministrosapuproyectoadd.html', {'user': user, 'suministros_apu': pag, 'proyecto': proyecto, 'apu_manejo_estandar': request.session['apu_manejo_estandar'] })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/' + str(proyecto.id) + '/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def asignar_suministro_estandar_apu_proyecto_add2(request, suministro_id, parametro, pagina, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            apu_manejo_estandar = request.session['apu_manejo_estandar']
            suministro_estandar = None
            if parametro == True:
                suministro_estandar = suministro_id
            request.session['id_suministro_estandar'] = suministro_estandar
            pag = Paginador(request, suministros, 20, pagina)
            render = render_to_string('ajax/suministrosapuproyectoadd.html', {'user': user, 'suministros_apu': pag, 'apu_manejo_estandar': apu_manejo_estandar, 'suministro_estandar': suministro_estandar, 'proyecto': proyecto })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/' + str(proyecto.id) + '/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------------------------- REQUISICIONES ---------------------------------------------

def anadir_suministro_carrito2(request, suministro_id, cantidad_requerir, observaciones, pagina, criterio, apu_id, proyecto_id):
    from django.contrib.humanize.templatetags.humanize import intcomma
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        carrito = None
        try:
            carrito = request.session['carrito']
        except :
            pass
        if carrito != None:
            apu = ApuProyecto.objects.get(id=apu_id, proyecto=proyecto)
            suministros = apu.suministroapuproyecto_set.all()
            criterio = criterio.strip()
            if criterio != '':
                suministros = suministros.filter(Q(suministro__nombre__icontains=criterio) | Q(suministro__sinonimos__icontains=criterio))
            error = {}
            error_cantidad = validar_cadena(cantidad_requerir)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float_digitos(cantidad_requerir)
                if error_cantidad == '':
                    error_cantidad = validar_cantidad_float(cantidad_requerir)
                    if error_cantidad == '':
                        error_cantidad = validar_cantidad_float_0(cantidad_requerir)
                        if error_cantidad == '':
                            cantidad_requerir = float(cantidad_requerir)
                            suministro_apu_proyecto = SuministroApuProyecto.objects.get(id=suministro_id, apu_proyecto__proyecto=proyecto)
                            cantidad_disponible = suministro_apu_proyecto.cantidadDisponibleRequerir()
                            if float(cantidad_requerir) <= float(str(cantidad_disponible)):
                                #Verifica si el suministro a requerir necesita cartilla
                                if ((suministro_apu_proyecto.suministro.requiere_cartilla == True and observaciones.strip() != '') or (suministro_apu_proyecto.suministro.requiere_cartilla == False)):
                                    carrito.set_articulo( { 'id': suministro_apu_proyecto.id, 'cantidad': cantidad_requerir, 'observaciones': observaciones.strip() } )
                                    request.session['carrito'] = carrito
                                else:
                                    error_cantidad = 'Este suministro requiere especificar una cartilla'
                            else :
                                error_cantidad = 'La cantidad requerida no esta disponible para este APU'
                        else:
                            if float(cantidad_requerir) == 0:
                                error_cantidad = ''
                                carrito.del_articulo(suministro_id)
                                request.session['carrito'] = carrito
            if error_cantidad != '':
                error = {'id': suministro_id, 'value': cantidad_requerir, 'value_observaciones': observaciones, 'error': error_cantidad}
            suministros_apu = []
            for suministro in suministros:
                suministro_apu = {'suministro': suministro, 'cantidad_nueva_requisicion': '', 'observaciones': ''}
                if carrito.existe_articulo(suministro.id):
                    articulo = carrito.get_articulo(suministro.id)
                    suministro_apu['cantidad_nueva_requisicion'] = articulo['cantidad']
                    suministro_apu['observaciones'] = articulo['observaciones']
                suministros_apu.append(suministro_apu)
            pag = Paginador(request, suministros_apu, 20, pagina)
            render = render_to_string('ajax/contenidoapuproyectodetails.html', {'user': user, 'suministros_apu': pag, 'criterio': criterio, 'apu': apu, 'error': error, 'proyecto': proyecto} )
            dajax.assign('#id_contenido_suministros_apu', 'innerHTML', render)
            if error_cantidad != '':
                dajax.script("document.getElementById('id_text_cantidad_" + str(suministro_id) + "').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_modificar_suministro_carrito2(request, suministro_id, apu_id, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        carrito = None
        try:
            carrito = request.session['carrito']
        except :
            pass
        if carrito != None:
            apu = ApuProyecto.objects.get(id=apu_id, proyecto=proyecto)
            suministros = apu.suministroapuproyecto_set.all()
            criterio = criterio.strip()
            if criterio != '':
                suministros = suministros.filter(Q(suministro__nombre__icontains=criterio) | Q(suministro__sinonimos__icontains=criterio))
            suministros_apu = []
            error = {}
            for suministro in suministros:
                suministro_apu = {'suministro': suministro, 'cantidad_nueva_requisicion': '', 'observaciones': ''}
                if carrito.existe_articulo(suministro.id):
                    articulo = carrito.get_articulo(suministro.id)
                    suministro_apu['cantidad_nueva_requisicion'] = articulo['cantidad']
                    suministro_apu['observaciones'] = articulo['observaciones']
                    if suministro.id == suministro_id:
                        error = {'id': suministro_id, 'value': str(articulo['cantidad']), 'value_observaciones': articulo['observaciones'], 'error': ''}
                suministros_apu.append(suministro_apu)
            pag = Paginador(request, suministros_apu, 20, pagina)
            render = render_to_string('ajax/contenidoapuproyectodetails.html', {'user': user, 'suministros_apu': pag, 'criterio': criterio, 'apu': apu, 'error': error, 'proyecto': proyecto} )
            dajax.assign('#id_contenido_suministros_apu', 'innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_cantidad_suministro_carrito2(request, suministro_id, pagina, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        carrito = None
        try:
            carrito = request.session['carrito']
        except :
            pass
        if carrito != None:
            articulos = carrito.items()
            suministros_requisicion = []
            for articulo in articulos:
                suministro_apu_proyecto = SuministroApuProyecto.objects.get(id=articulo['id'])
                suministro_requisicion = SuministroRequisicion()
                suministro_requisicion.suministro = suministro_apu_proyecto
                suministro_requisicion.cantidad_requerida = articulo['cantidad']
                suministro_requisicion.observaciones = articulo['observaciones']
                suministros_requisicion.append(suministro_requisicion)
                if suministro_apu_proyecto.id == suministro_id:
                    error = {'id': suministro_id, 'value': str(articulo['cantidad']), 'value_observaciones': articulo['observaciones'], 'error': ''}
            pag = Paginador(request, suministros_requisicion, 20, pagina)
            render = render_to_string('ajax/nuevarequisiciondetails.html', {'user': user, 'suministros_requisicion': pag, 'error': error, 'proyecto': proyecto} )
            dajax.assign('#id_contenido', 'innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_" + str(suministro_id) + "').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_suministro_carrito2(request, suministro_id, cantidad_requerir, observaciones, pagina, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        carrito = None
        try:
            carrito = request.session['carrito']
        except :
            pass
        if carrito != None:
            error = {}
            error_cantidad = validar_cadena(cantidad_requerir)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float_digitos(cantidad_requerir)
                if error_cantidad == '':
                    error_cantidad = validar_cantidad_float(cantidad_requerir)
                    if error_cantidad == '':
                        error_cantidad = validar_cantidad_float_0(cantidad_requerir)
                        if error_cantidad == '':
                            cantidad_requerir = float(cantidad_requerir)
                            suministro_apu_proyecto = SuministroApuProyecto.objects.get(id=suministro_id, apu_proyecto__proyecto=proyecto)
                            cantidad_disponible = suministro_apu_proyecto.cantidadDisponibleRequerir()
                            if float(cantidad_requerir) <= cantidad_disponible:
                                #Verifica si el suministro a requerir necesita cartilla
                                if ((suministro_apu_proyecto.suministro.requiere_cartilla and observaciones.strip() != '') or (suministro_apu_proyecto.suministro.requiere_cartilla == False)):
                                    carrito.set_articulo( { 'id': suministro_apu_proyecto.id, 'cantidad': cantidad_requerir, 'observaciones': observaciones.strip() } )
                                    request.session['carrito'] = carrito
                                else:
                                    error_cantidad = 'Este suministro requiere especificar una cartilla'
                            else :
                                error_cantidad = 'La cantidad requerida no esta disponible para este APU'
            if error_cantidad != '':
                error = {'id': suministro_id, 'value': cantidad_requerir, 'value_observaciones': observaciones, 'error': error_cantidad}
            articulos = carrito.items()
            suministros_requisicion = []
            for articulo in articulos:
                suministro_apu_proyecto = SuministroApuProyecto.objects.get(id=articulo['id'])
                suministro_requisicion = SuministroRequisicion()
                suministro_requisicion.suministro = suministro_apu_proyecto
                suministro_requisicion.cantidad_requerida = articulo['cantidad']
                suministro_requisicion.observaciones = articulo['observaciones']
                suministros_requisicion.append(suministro_requisicion)
            pag = Paginador(request, suministros_requisicion, 20, pagina)
            render = render_to_string('ajax/nuevarequisiciondetails.html', {'user': user, 'suministros_requisicion': pag, 'error': error, 'proyecto': proyecto} )
            dajax.assign('#id_contenido', 'innerHTML', render)
            if error_cantidad != '':
                dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def del_suministro_carrito2(request, suministro_id, pagina, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        carrito = None
        try:
            carrito = request.session['carrito']
        except :
            pass
        if carrito != None:
            carrito.del_articulo(suministro_id)
            request.session['carrito'] = carrito
            articulos = carrito.items()
            suministros_requisicion = []
            for articulo in articulos:
                suministro_apu_proyecto = SuministroApuProyecto.objects.get(id=articulo['id'])
                suministro_requisicion = SuministroRequisicion()
                suministro_requisicion.suministro = suministro_apu_proyecto
                suministro_requisicion.cantidad_requerida = articulo['cantidad']
                suministro_requisicion.observaciones = articulo['observaciones']
                suministros_requisicion.append(suministro_requisicion)
            try:
                pag = Paginador(request, suministros_requisicion, 20, pagina)
            except :
                pag = Paginador(request, suministros_requisicion, 20, pagina-1)
            user = request.user
            render = render_to_string('ajax/nuevarequisiciondetails.html', {'user': user, 'suministros_requisicion': pag, 'proyecto': proyecto} )
            dajax.assign('#id_contenido', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def anadir_suministro_carrito_requisicion_indirectos_add2(request, suministro_id, cantidad_requerir, observaciones, pagina, criterio, apu_id, proyecto_id):
    from django.contrib.humanize.templatetags.humanize import intcomma
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        carrito = None
        try:
            carrito = request.session['carrito']
        except :
            pass
        if carrito != None:
            apu = proyecto.apuproyecto_set.get(id=apu_id)
            suministros = apu.suministroapuproyecto_set.all()
            criterio = criterio.strip()
            if criterio != '':
                suministros = suministros.filter(Q(suministro__nombre__icontains=criterio) | Q(suministro__sinonimos__icontains=criterio))
            error = {}
            error_cantidad = validar_cadena(cantidad_requerir)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float_digitos(cantidad_requerir)
                if error_cantidad == '':
                    error_cantidad = validar_cantidad_float(cantidad_requerir)
                    if error_cantidad == '':
                        error_cantidad = validar_cantidad_float_0(cantidad_requerir)
                        if error_cantidad == '':
                            cantidad_requerir = float(cantidad_requerir)
                            suministro_apu_proyecto = SuministroApuProyecto.objects.get(id=suministro_id, apu_proyecto__proyecto=proyecto)
                            cantidad_disponible = suministro_apu_proyecto.cantidadDisponibleRequerir()
                            if float(cantidad_requerir) <= float(str(cantidad_disponible)):
                                #Verifica si el suministro a requerir necesita cartilla
                                if ((suministro_apu_proyecto.suministro.requiere_cartilla == True and observaciones.strip() != '') or (suministro_apu_proyecto.suministro.requiere_cartilla == False)):
                                    carrito.set_articulo( { 'id': suministro_apu_proyecto.id, 'cantidad': cantidad_requerir, 'observaciones': observaciones.strip() } )
                                    request.session['carrito'] = carrito
                                else:
                                    error_cantidad = 'Este suministro requiere especificar una cartilla'
                            else :
                                error_cantidad = 'La cantidad requerida no esta disponible para este APU'
                        else:
                            if float(cantidad_requerir) == 0:
                                error_cantidad = ''
                                carrito.del_articulo(suministro_id)
                                request.session['carrito'] = carrito
            if error_cantidad != '':
                error = {'id': suministro_id, 'value': cantidad_requerir, 'value_observaciones': observaciones, 'error': error_cantidad}
            suministros_apu = []
            for suministro in suministros:
                suministro_apu = {'suministro': suministro, 'cantidad_nueva_requisicion': '', 'observaciones': ''}
                if carrito.existe_articulo(suministro.id):
                    articulo = carrito.get_articulo(suministro.id)
                    suministro_apu['cantidad_nueva_requisicion'] = articulo['cantidad']
                    suministro_apu['observaciones'] = articulo['observaciones']
                suministros_apu.append(suministro_apu)
            pag = Paginador(request, suministros_apu, 20, pagina)
            render = render_to_string('ajax/contenidoapuproyectodetailsrequisicionindirectosadd.html', {'user': user, 'suministros_apu': pag, 'criterio': criterio, 'apu': apu, 'error': error, 'proyecto': proyecto} )
            dajax.assign('#id_contenido_suministros_apu', 'innerHTML', render)
            if error_cantidad != '':
                dajax.script("document.getElementById('id_text_cantidad_" + str(suministro_id) + "').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_modificar_suministro_carrito_requisicion_indirectos_add2(request, suministro_id, apu_id, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        carrito = None
        try:
            carrito = request.session['carrito']
        except :
            pass
        if carrito != None:
            apu = proyecto.apuproyecto_set.get(id=apu_id)
            suministros = apu.suministroapuproyecto_set.all()
            criterio = criterio.strip()
            if criterio != '':
                suministros = suministros.filter(Q(suministro__nombre__icontains=criterio) | Q(suministro__sinonimos__icontains=criterio))
            suministros_apu = []
            error = {}
            for suministro in suministros:
                suministro_apu = {'suministro': suministro, 'cantidad_nueva_requisicion': '', 'observaciones': ''}
                if carrito.existe_articulo(suministro.id):
                    articulo = carrito.get_articulo(suministro.id)
                    suministro_apu['cantidad_nueva_requisicion'] = articulo['cantidad']
                    suministro_apu['observaciones'] = articulo['observaciones']
                    if suministro.id == suministro_id:
                        error = {'id': suministro_id, 'value': str(articulo['cantidad']), 'value_observaciones': articulo['observaciones'], 'error': ''}
                suministros_apu.append(suministro_apu)
            pag = Paginador(request, suministros_apu, 20, pagina)
            render = render_to_string('ajax/contenidoapuproyectodetailsrequisicionindirectosadd.html', {'user': user, 'suministros_apu': pag, 'criterio': criterio, 'apu': apu, 'error': error, 'proyecto': proyecto} )
            dajax.assign('#id_contenido_suministros_apu', 'innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_cantidad_suministro_carrito_requisicion_indirectos_add2(request, suministro_id, pagina, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        carrito = None
        try:
            carrito = request.session['carrito']
        except :
            pass
        if carrito != None:
            articulos = carrito.items()
            suministros_requisicion = []
            for articulo in articulos:
                suministro_apu_proyecto = SuministroApuProyecto.objects.get(id=articulo['id'])
                suministro_requisicion = SuministroRequisicion()
                suministro_requisicion.suministro = suministro_apu_proyecto
                suministro_requisicion.cantidad_requerida = articulo['cantidad']
                suministro_requisicion.observaciones = articulo['observaciones']
                suministros_requisicion.append(suministro_requisicion)
                if suministro_apu_proyecto.id == suministro_id:
                    error = {'id': suministro_id, 'value': str(articulo['cantidad']), 'value_observaciones': articulo['observaciones'], 'error': ''}
            pag = Paginador(request, suministros_requisicion, 20, pagina)
            render = render_to_string('ajax/nuevarequisicionindirectosdetails.html', {'user': user, 'suministros_requisicion': pag, 'error': error, 'proyecto': proyecto} )
            dajax.assign('#id_contenido', 'innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_" + str(suministro_id) + "').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_suministro_carrito_requisicion_indirectos_add2(request, suministro_id, cantidad_requerir, observaciones, pagina, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        carrito = None
        try:
            carrito = request.session['carrito']
        except :
            pass
        if carrito != None:
            error = {}
            error_cantidad = validar_cadena(cantidad_requerir)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float_digitos(cantidad_requerir)
                if error_cantidad == '':
                    error_cantidad = validar_cantidad_float(cantidad_requerir)
                    if error_cantidad == '':
                        error_cantidad = validar_cantidad_float_0(cantidad_requerir)
                        if error_cantidad == '':
                            cantidad_requerir = float(cantidad_requerir)
                            suministro_apu_proyecto = SuministroApuProyecto.objects.get(id=suministro_id, apu_proyecto__proyecto=proyecto)
                            cantidad_disponible = suministro_apu_proyecto.cantidadDisponibleRequerir()
                            if float(cantidad_requerir) <= cantidad_disponible:
                                #Verifica si el suministro a requerir necesita cartilla
                                if ((suministro_apu_proyecto.suministro.requiere_cartilla and observaciones.strip() != '') or (suministro_apu_proyecto.suministro.requiere_cartilla == False)):
                                    carrito.set_articulo( { 'id': suministro_apu_proyecto.id, 'cantidad': cantidad_requerir, 'observaciones': observaciones.strip() } )
                                    request.session['carrito'] = carrito
                                else:
                                    error_cantidad = 'Este suministro requiere especificar una cartilla'
                            else :
                                error_cantidad = 'La cantidad requerida no esta disponible para este APU'
            if error_cantidad != '':
                error = {'id': suministro_id, 'value': cantidad_requerir, 'value_observaciones': observaciones, 'error': error_cantidad}
            articulos = carrito.items()
            suministros_requisicion = []
            for articulo in articulos:
                suministro_apu_proyecto = SuministroApuProyecto.objects.get(id=articulo['id'])
                suministro_requisicion = SuministroRequisicion()
                suministro_requisicion.suministro = suministro_apu_proyecto
                suministro_requisicion.cantidad_requerida = articulo['cantidad']
                suministro_requisicion.observaciones = articulo['observaciones']
                suministros_requisicion.append(suministro_requisicion)
            pag = Paginador(request, suministros_requisicion, 20, pagina)
            render = render_to_string('ajax/nuevarequisicionindirectosdetails.html', {'user': user, 'suministros_requisicion': pag, 'error': error, 'proyecto': proyecto} )
            dajax.assign('#id_contenido', 'innerHTML', render)
            if error_cantidad != '':
                dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

def del_suministro_carrito_requisicion_indirectos_add2(request, suministro_id, pagina, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        carrito = None
        try:
            carrito = request.session['carrito']
        except :
            pass
        if carrito != None:
            carrito.del_articulo(suministro_id)
            request.session['carrito'] = carrito
            articulos = carrito.items()
            suministros_requisicion = []
            for articulo in articulos:
                suministro_apu_proyecto = SuministroApuProyecto.objects.get(id=articulo['id'])
                suministro_requisicion = SuministroRequisicion()
                suministro_requisicion.suministro = suministro_apu_proyecto
                suministro_requisicion.cantidad_requerida = articulo['cantidad']
                suministro_requisicion.observaciones = articulo['observaciones']
                suministros_requisicion.append(suministro_requisicion)
            try:
                pag = Paginador(request, suministros_requisicion, 20, pagina)
            except :
                pag = Paginador(request, suministros_requisicion, 20, pagina-1)
            user = request.user
            render = render_to_string('ajax/nuevarequisicionindirectosdetails.html', {'user': user, 'suministros_requisicion': pag, 'proyecto': proyecto} )
            dajax.assign('#id_contenido', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def apus_proyecto2(request, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        apus = ApuProyecto.objects.filter(proyecto=proyecto)
        pag = Paginador(request, apus, 20, 1)
        capitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=1, estado_capitulo=1)
        lista_subcapitulos = []
        criterio = ""
        capitulo_actual = CapituloApuProyecto()
        subcapitulo_actual = CapituloApuProyecto()
        user = request.user
        permisos_usuario = user.get_all_permissions()
        render = render_to_string('ajax/contenidoapusproyectosearch.html', {'user': user, 'permisos': permisos_usuario, 'apus': pag, 'proyecto': proyecto, 'capitulos': capitulos, 'subcapitulos': lista_subcapitulos, 'apus': pag, 'criterio': criterio, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'proyecto': proyecto, 'apus_proyecto_search': True, } )
        dajax.assign('#id_contenido', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def nueva_requisicion_details2(request, proyecto_id):
    import datetime
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        permisos_usuario = user.get_all_permissions()
        proyecto = Proyecto.objects.get(id=proyecto_id)
        carrito = None
        try:
            carrito = request.session['carrito']
        except :
            pass
        if carrito != None:
            articulos = carrito.items()
            suministros_requisicion = []
            for articulo in articulos:
                suministro_apu_proyecto = SuministroApuProyecto.objects.get(id=articulo['id'])
                suministro_requisicion = SuministroRequisicion()
                suministro_requisicion.suministro = suministro_apu_proyecto
                suministro_requisicion.cantidad_requerida = articulo['cantidad']
                suministro_requisicion.observaciones = articulo['observaciones']
                suministros_requisicion.append(suministro_requisicion)
            now = datetime.datetime.now()
            fecha_actual = now.strftime("%Y-%m-%d")
            render = render_to_string('ajax/nuevarequisiciondetails.html', {'user': user, 'permisos': permisos_usuario, 'suministros_requisicion': suministros_requisicion, 'proyecto': proyecto, 'fecha_actual': fecha_actual, 'nueva_requisicion_details': True } )
            dajax.assign('#id_contenido', 'innerHTML', render)
            dajax.script("Calendar.setup({inputField:'id_fecha_arribo',ifFormat:'%Y-%m-%d',button:'lanzador'});")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def suministro_cotizar2(request, suministro_id, proyecto_id):
    import datetime
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        #if validar_permiso_usuario(user.id, 'auth.view_group'):
                
        suministro_comprar = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(suministro_id=suministro_id)[0]
        pag = Paginador(request, suministro_comprar.suministro.suministro.get_proveedores_activos_suministro(), 20, 1)

        now = datetime.datetime.now()
        fecha_actual = now.strftime("%Y-%m-%d")
        render = render_to_string('ajax/suministrocotizarproveedoressearch.html', {'user': user, 'suministro_proveedores': pag, 'suministro_comprar': suministro_comprar, 'proyecto': proyecto, 'fecha_actual': fecha_actual, } )
        dajax.assign('#light', 'innerHTML', render)
        dajax.script("document.getElementById('light').style.display='block';")
        dajax.script("document.getElementById('fade').style.display='block';")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def seleccionar_proveedor_lista_proveedores_suministro_cotizacion_add2(request, parametro, suministro_id, proveedor_id, pagina, criterio, proyecto_id):
    import datetime
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)

        criterio = criterio.strip()
        suministro_comprar = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(suministro_id=suministro_id).pop()
        pag = Paginador(request, suministro_comprar.suministro.suministro.get_proveedores_activos_suministro(criterio=criterio), 20, pagina)

        now = datetime.datetime.now()
        fecha_actual = now.strftime("%Y-%m-%d")
        error = {}
        if parametro == True:
            error = { 'id': proveedor_id, 'value': '', 'error': '', 'value_observaciones': suministro_comprar.observaciones }
        render = render_to_string('ajax/suministrocotizarproveedoressearch.html', {'user': user, 'suministro_proveedores': pag, 'suministro_comprar': suministro_comprar, 'fecha_actual': fecha_actual, 'criterio_proveedor': criterio, 'proyecto': proyecto, 'error': error } )
        dajax.assign('#light', 'innerHTML', render)
        if parametro == True:
            dajax.script("document.getElementById('id_text_cantidad_" + str(proveedor_id) + "').focus();")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def cotizar_suministro_proveedor2(request, suministro_id, proveedor_id, cantidad, observaciones, pagina, criterio, proyecto_id):
    from django.db.models import Sum
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'auth.view_group'):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        cantidad = cantidad.strip()
        observaciones = observaciones.strip()

        error_cantidad = ''
        validaciones = Validator().append([
            Field('cantidad', cantidad).append([
                IsRequired('Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto.'),
            ]),
        ]).run(True).pop()

        if validaciones['passed'] == True:
            cantidad = float(cantidad)
            if cantidad > 0:
                suministro_cotizar = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(suministro_id=suministro_id).pop()
                if cantidad <= suministro_cotizar.cantidad_requerida:
                    suministro = suministro_cotizar.suministro.suministro
                    if is_residuo_0(cantidad, suministro.unidad_embalaje):
                        persona = Usuario.objects.get(id=user.id)
                        cotizacion = Cotizacion()
                        cotizacion.tipo = 1
                        cotizacion.proyecto = proyecto
                        cotizacion.persona = persona
                        proveedor = Proveedor.objects.get(id=proveedor_id)
                        cotizacion.proveedor = proveedor
                        request.session['cotizacion'] = cotizacion
                        #Variable de la sesion
                        suministros_cotizacion = []
                        observaciones = observaciones.strip()
                        if observaciones == '':
                            observaciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(suministro_id=suministro_id)[0].observaciones
                        suministros_cotizacion.append({'suministro_id': suministro_id, 'cantidad': cantidad, 'observaciones': observaciones })
                        request.session['suministros_cotizacion'] = suministros_cotizacion

                        #Visualiza los suministros requeridos con la cantidad a cotizar
                        suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(proveedor_id=proveedor_id)
                        suministros_comprar = []
                        for suministro_requisiciones in suministros_requisiciones:
                            suministro_comprar = {'suministro': suministro_requisiciones, 'cantidad_nueva_cotizacion': '', 'observaciones': suministro_requisiciones.observaciones}
                            if suministro_requisiciones.suministro.suministro.id == suministro_id:
                                suministro_comprar['cantidad_nueva_cotizacion'] = cantidad
                                suministro_comprar['observaciones'] = observaciones
                            suministros_comprar.append(suministro_comprar)

                        pag = Paginador(request, suministros_comprar, 20, 1)

                        render = render_to_string('ajax/suministrosrequisicionesproveedorsearch.html', {'user': user, 'suministros_requisiciones': pag, 'proveedor': proveedor, 'proyecto': proyecto } )
                        dajax.assign('#light', 'innerHTML', render)
                    else:
                        error_cantidad = 'La cantidad de este suministro que puede cotizar es: '+str(cantidad-(cantidad % suministro.unidad_embalaje))
                else:
                    error_cantidad = 'La cantidad no debe ser mayor al total requerido'
            else:
                error_cantidad = 'La cantidad debe ser mayor a 0 (cero)'
        else:
            for error in validaciones['errors']:
                error_cantidad = error
        if error_cantidad != '':
            import datetime
            error = { 'id': proveedor_id, 'value': cantidad, 'error': error_cantidad, 'value_observaciones': observaciones }
            criterio = criterio.strip()
            suministro_comprar = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(suministro_id=suministro_id)[0]
            pag = Paginador(request, suministro_comprar.suministro.suministro.get_proveedores_activos_suministro(criterio=criterio), 20, pagina)
            now = datetime.datetime.now()
            fecha_actual = now.strftime("%Y-%m-%d")
            render = render_to_string('ajax/suministrocotizarproveedoressearch.html', {'user': user, 'suministro_proveedores': pag, 'criterio_proveedor': criterio, 'suministro_comprar': suministro_comprar, 'proyecto': proyecto, 'fecha_actual': fecha_actual, 'error': error } )
            dajax.assign('#light', 'innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_"+str(proveedor_id)+"').select();")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def cotizar_todos_suministros_proveedor2(request, proveedor_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)

        suministros_cotizacion = None
        try:
            suministros_cotizacion = request.session['suministros_cotizacion']
        except :
            pass

        if suministros_cotizacion != None:
            proveedor = Proveedor.objects.get(id=proveedor_id)

            #Visualiza los suministros requeridos con la cantidad a cotizar
            suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(proveedor_id=proveedor_id)
            suministros_comprar = []
            for suministro_requisiciones in suministros_requisiciones:
                suministro_comprar = { 'suministro': suministro_requisiciones, 'cantidad_nueva_cotizacion': '', 'observaciones': suministro_requisiciones.observaciones }
                for suministro_cotizacion in suministros_cotizacion:
                    if suministro_requisiciones.suministro.suministro.id == suministro_cotizacion['suministro_id']:
                        suministro_comprar['cantidad_nueva_cotizacion'] = suministro_cotizacion['cantidad']
                        suministro_comprar['observaciones'] = suministro_cotizacion['observaciones']
                suministros_comprar.append(suministro_comprar)

            for suministro_comprar in suministros_comprar:
                if suministro_comprar['cantidad_nueva_cotizacion'] == '':
                    suministro_actual = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(suministro_id=suministro_comprar['suministro'].suministro.suministro.id).pop()
                    if suministro_actual.cantidad_requerida >= suministro_comprar['suministro'].suministro.suministro.unidad_embalaje:
                        cantidad_comprar = round(suministro_actual.cantidad_requerida - round(round(round(suministro_actual.cantidad_requerida * 100, 2) % (round(suministro_comprar['suministro'].suministro.suministro.unidad_embalaje * 100, 2)), 2) / 100, 2), 2)
                        suministro_comprar['cantidad_nueva_cotizacion'] = cantidad_comprar
                        suministro_comprar['observaciones'] = suministro_actual.observaciones
                        suministros_cotizacion.append({ 'suministro_id': suministro_comprar['suministro'].suministro.suministro.id, 'cantidad': cantidad_comprar, 'observaciones': suministro_actual.observaciones })
            pag = Paginador(request, suministros_comprar, 20, 1)
            render = render_to_string('ajax/suministrosrequisicionesproveedorsearch.html', {'user': user, 'suministros_requisiciones': pag, 'proveedor': proveedor, 'proyecto': proyecto})
            dajax.assign('#light', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


## PROVISIONAL
def validar_cantidad_suministros(request, dajax):
    suministros_cotizacion = request.session['suministros_cotizacion']
    cantidades_correctas = True
    for suministro_cotizacion in suministros_cotizacion:
        try:
            float(suministro_cotizacion['cantidad'])
        except :
            cantidades_correctas = False
    if cantidades_correctas == True:
        for suministro_cotizacion in suministros_cotizacion:
            suministro = Suministro.objects.get(id=suministro_cotizacion['suministro_id'])
            cantidad = float(suministro_cotizacion['cantidad'])
            cantidades_correctas = is_residuo_0(cantidad, suministro.unidad_embalaje)
        if cantidades_correctas == False:
            dajax.alert('Las cantidades deben ser un multiplo de la unidad de embalaje del suministro')
    else:
        dajax.alert('Las cantidades deben ser un valor numerico')
    return cantidades_correctas
## PROVISIONAL


def anadir_suministro_cotizacion2(request, pagina, suministro_id, cantidad, observaciones, proveedor_id, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros_cotizacion = None
        try:
            suministros_cotizacion = request.session['suministros_cotizacion']
        except :
            pass
        if suministros_cotizacion != None:
            cantidad = cantidad.strip()
            observaciones = observaciones.strip()

            error_cantidad = ''
            validaciones = Validator().append([
                Field('cantidad', cantidad).append([
                    IsRequired('Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto.'),
                ]),
            ]).run(True).pop()

            if validaciones['passed'] == True:
                cantidad = float(cantidad)
                if cantidad > 0:
                    suministro_cotizar = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(proveedor_id=proveedor_id, suministro_id=suministro_id).pop()
                    if cantidad <= suministro_cotizar.cantidad_requerida:
                        suministro = suministro_cotizar.suministro.suministro
                        if is_residuo_0(cantidad, suministro.unidad_embalaje):
                            existe_suministro = False
                            for suministro_cotizacion in suministros_cotizacion:
                                if suministro_cotizacion['suministro_id'] == suministro_id:
                                    suministro_cotizacion['cantidad'] = cantidad
                                    suministro_cotizacion['observaciones'] = observaciones
                                    existe_suministro = True
                            if existe_suministro == False:
                                suministros_cotizacion.append({ 'suministro_id': suministro_id, 'cantidad': cantidad, 'observaciones': observaciones })
                            request.session['suministros_cotizacion'] = suministros_cotizacion
                        else:
                            error_cantidad = 'La cantidad de este suministro que puede cotizar es: '+str(round(cantidad-(round(cantidad % suministro.unidad_embalaje, 2)), 2))
                    else:
                        error_cantidad = 'La cantidad no debe ser mayor al total requerido'
                else:
                    if cantidad == 0:
                        error_cantidad = ''
                        for suministro_cotizacion in suministros_cotizacion:
                            if suministro_cotizacion['suministro_id'] == suministro_id:
                                suministros_cotizacion.remove(suministro_cotizacion)
                        request.session['suministros_cotizacion'] = suministros_cotizacion
            else:
                for error in validaciones['errors']:
                    error_cantidad = error

            error = {}
            if error_cantidad != '':
                error = { 'id': suministro_id, 'value': cantidad, 'error': error_cantidad, 'value_observaciones': observaciones }
            proveedor = Proveedor.objects.get(id=proveedor_id)
            criterio = criterio.strip()

            #Visualiza los suministros requeridos con la cantidad a cotizar
            suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(criterio=criterio, proveedor_id=proveedor_id)
            suministros_comprar = []
            for suministro_requisiciones in suministros_requisiciones:
                suministro_comprar = { 'suministro': suministro_requisiciones, 'cantidad_nueva_cotizacion': '', 'observaciones': suministro_requisiciones.observaciones}
                for suministro_cotizacion in suministros_cotizacion:
                    if suministro_requisiciones.suministro.suministro.id == suministro_cotizacion['suministro_id']:
                        suministro_comprar['cantidad_nueva_cotizacion'] = suministro_cotizacion['cantidad']
                        suministro_comprar['observaciones'] = suministro_cotizacion['observaciones']
                suministros_comprar.append(suministro_comprar)

            pag = Paginador(request, suministros_comprar, 20, pagina)

            render = render_to_string('ajax/suministrosrequisicionesproveedorsearch.html', {'user': user, 'suministros_requisiciones': pag, 'criterio': criterio, 'proveedor': proveedor, 'proyecto': proyecto, 'error': error } )
            dajax.assign('#light', 'innerHTML', render)
            if error_cantidad != '':
                dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_cantidad_suministro_cotizacion_add2(request, pagina, suministro_id, proveedor_id, criterio, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros_cotizacion = None
        try:
            suministros_cotizacion = request.session['suministros_cotizacion']
        except :
            pass
        if suministros_cotizacion != None:
            proveedor = Proveedor.objects.get(id=proveedor_id)
            criterio = criterio.strip()

            #Visualiza los suministros requeridos con la cantidad a cotizar
            suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(criterio=criterio, proveedor_id=proveedor_id)
            suministros_comprar = []

            error = {}
            for suministro_requisiciones in suministros_requisiciones:
                suministro_comprar = { 'suministro': suministro_requisiciones, 'cantidad_nueva_cotizacion': '', 'observaciones': suministro_requisiciones.observaciones}
                for suministro_cotizacion in suministros_cotizacion:
                    if suministro_requisiciones.suministro.suministro.id == suministro_cotizacion['suministro_id']:
                        suministro_comprar['cantidad_nueva_cotizacion'] = suministro_cotizacion['cantidad']
                        suministro_comprar['observaciones'] = suministro_cotizacion['observaciones']
                        if suministro_cotizacion['suministro_id'] == suministro_id:
                            error = { 'id': suministro_id, 'value': suministro_cotizacion['cantidad'], 'error': '', 'value_observaciones': suministro_cotizacion['observaciones'] }
                suministros_comprar.append(suministro_comprar)
            pag = Paginador(request, suministros_comprar, 20, pagina)
            render = render_to_string('ajax/suministrosrequisicionesproveedorsearch.html', {'user': user, 'suministros_requisiciones': pag, 'criterio': criterio, 'proveedor': proveedor, 'proyecto': proyecto, 'error': error } )
            dajax.assign('#light', 'innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def realizar_cotizacion2(request, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros_cotizacion = None
        try:
            suministros_cotizacion = request.session['suministros_cotizacion']
        except :
            pass
        if suministros_cotizacion != None:
            cantidades_correctas = validar_cantidad_suministros(request, dajax)
            if cantidades_correctas == True:
                cotizacion = request.session['cotizacion']
                if len(suministros_cotizacion) > 0:
                    cantidades_correctas = True
                    for suministro_cotizacion in suministros_cotizacion:
                        suministros = SuministroRequisicion.objects.filter(suministro__suministro__id=suministro_cotizacion['suministro_id'], requisicion__proyecto=proyecto)
                        cantidad_total_requerida = suministros.__getitem__(0).cantidad_total_requerida_proyecto()
                        cantidad = float(suministro_cotizacion['cantidad'])
                        if cantidad > cantidad_total_requerida:
                            cantidades_correctas = False
                    if cantidades_correctas:
                        cotizacion.save()
                        for suministro_cotizacion in suministros_cotizacion:
                            suministro = Suministro.objects.get(id=suministro_cotizacion['suministro_id'])
                            nuevo_suministro_cotizacion = SuministroCotizacion()
                            nuevo_suministro_cotizacion.cantidad_cotizada = suministro_cotizacion['cantidad']
                            nuevo_suministro_cotizacion.observaciones = suministro_cotizacion['observaciones']
                            nuevo_suministro_cotizacion.suministro = suministro
                            nuevo_suministro_cotizacion.cotizacion = cotizacion
                            nuevo_suministro_cotizacion.save()
                        del request.session['cotizacion']
                        del request.session['suministros_cotizacion']
                        dajax.alert('Se ha realizado la cotizacion')
                        dajax.redirect('/inverboy/home/cotizacionesproyectodetails/'+str(cotizacion.id)+'/'+str(proyecto_id))
                    else:
                        dajax.alert(u'Verifique que las cantidades de la cotización no sean mayores que las cantidades requeridas')
                        dajax.script("document.getElementById('id_guardar').disabled = false;")
                else:
                    dajax.alert(u'No hay suministros en la cotización')
                    dajax.script("document.getElementById('id_guardar').disabled = false;")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_suministro_cotizacion2(request, suministro_id, cotizacion_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'auth.view_group'):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        cotizacion = None
        try:
            cotizacion = proyecto.cotizacion_set.get(id=cotizacion_id)
        except :
            pass
        if cotizacion != None:
            cotizacion.suministrocotizacion_set.get(suministro__id=suministro_id).delete()
            suministros = cotizacion.suministrocotizacion_set.all()
            pag = Paginador(request, suministros, 20, 1)
            if cotizacion.tipo == 1:
                render = render_to_string('ajax/suministroscotizacionsearch.html', {'user': user, 'cotizacion': cotizacion, 'proyecto': proyecto, 'suministros': pag })
            elif cotizacion.tipo == 2:
                render = render_to_string('ajax/suministroscotizacionordenserviciosearch.html', {'user': user, 'cotizacion': cotizacion, 'proyecto': proyecto, 'suministros': pag })
            dajax.assign('#id_reporte_suministros', 'innerHTML', render)
            dajax.script("Calendar.setup({inputField:'id_fecha_arribo',ifFormat:'%Y-%m-%d',button:'lanzador'});")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_cantidad_suministro_cotizacion_orden_compra_add2(request, pagina, suministro_id, cotizacion_id, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        cotizacion = None
        try:
            cotizacion = proyecto.cotizacion_set.get(id=cotizacion_id)
        except :
            pass
        if cotizacion != None:
            suministros = cotizacion.suministrocotizacion_set.all()
            pag = Paginador(request, suministros, 20, pagina)
            suministro = cotizacion.suministrocotizacion_set.get(id=suministro_id)
            error = { 'id': suministro_id, 'item': 'cantidad', 'value': suministro.cantidad_cotizada, 'error': '' }
            render = render_to_string('ajax/suministroscotizacionsearch.html', {'user': user, 'suministros': pag, 'cotizacion': cotizacion, 'proyecto': proyecto, 'error': error })
            dajax.assign('#id_reporte_suministros', 'innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_suministro_orden_compra2(request, suministro_id, orden_compra_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'auth.view_group'):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            subtotal = 0
            valor_iva = 0
            valor_total = 0
            orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
            # Verifica que se pueda modificar la orden de compra
            if len(orden_compra.informerecepcion_set.all()) == 0 and orden_compra.permiso_modificar:
                for suministro in suministros:
                    if suministro['suministro'].id == suministro_id:
                        suministro_eliminar = suministro
                    else:
                        subtotal = round(subtotal + (suministro['cantidad'] * suministro['precio']), 2)
                        valor_iva = round(valor_iva + (suministro['cantidad'] * suministro['precio'] * suministro['iva_suministro']), 2)
                suministros.remove(suministro_eliminar)
                valor_total = round(subtotal + valor_iva, 2)
                pag = Paginador(request, suministros, 20, 1)
                render = render_to_string('ajax/suministrosordencomprachange.html', {'user': user, 'orden_compra': orden_compra, 'suministros': pag, 'subtotal': subtotal, 'valor_iva': valor_iva, 'valor_total': valor_total, 'proyecto': proyecto})
                dajax.assign('#id_reporte_suministros', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_cantidad_suministro_orden_compra_change2(request, pagina, suministro_id, orden_compra_id, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
            # Verifica que se pueda modificar la orden de compra
            if len(orden_compra.informerecepcion_set.all()) == 0 and orden_compra.permiso_modificar:
                for suministro in suministros:
                    if suministro['suministro'].id == suministro_id:
                        error = {'id': suministro_id, 'item': 'cantidad', 'value': suministro['cantidad'], 'error': ''}
                pag = Paginador(request, suministros, 20, pagina)
                render = render_to_string('ajax/suministrosordencomprachange.html', {'user': user, 'suministros': pag, 'orden_compra': orden_compra, 'proyecto': proyecto, 'error': error})
                dajax.assign('#id_reporte_suministros', 'innerHTML', render)
                dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_cantidad_suministro_orden_compra_change2(request, suministro_id, cantidad, orden_compra_id, pagina, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
            # Verifica que se pueda modificar la orden de compra
            if len(orden_compra.informerecepcion_set.all()) == 0 and orden_compra.permiso_modificar:
                subtotal = 0
                valor_iva = 0
                valor_total = 0

                cantidad = cantidad.strip()
                error_cantidad = validar_cadena(cantidad)
                if error_cantidad == '':
                    error_cantidad = validar_cantidad_float_digitos(cantidad)
                    if error_cantidad == '':
                        error_cantidad = validar_cantidad_float(cantidad)
                        if error_cantidad == '':
                            cantidad = float(cantidad)
                            error_cantidad = validar_cantidad_float_0(cantidad)
                            if error_cantidad == '':
                                suministro = Suministro.objects.get(id=suministro_id)
                                if is_residuo_0(cantidad, suministro.unidad_embalaje):
                                    cantidad_requerida = None
                                    try:
                                        cantidad_requerida = SuministroRequisicion.objects.filter(requisicion__proyecto=proyecto, suministro__suministro__id=suministro_id, cantidad_comprada__lt=F('cantidad_requerida')).aggregate(Sum('cantidad_requerida'))['cantidad_requerida__sum'] - SuministroRequisicion.objects.filter(requisicion__proyecto=proyecto, suministro__suministro__id=suministro_id, cantidad_comprada__lt=F('cantidad_requerida')).aggregate(Sum('cantidad_comprada'))['cantidad_comprada__sum']
                                    except :
                                        pass
                                    if cantidad_requerida == None:
                                        cantidad_requerida = 0
                                    cantidad_comprada_orden_actual = None
                                    try:
                                        cantidad_comprada_orden_actual = orden_compra.suministroordencompraitem_set.get(suministro__id=suministro_id).suministroordencompra_set.aggregate(Sum('cantidad_comprada'))['cantidad_comprada__sum']
                                    except :
                                        pass
                                    if cantidad_comprada_orden_actual == None:
                                        cantidad_comprada_orden_actual = 0
                                    cantidad_disponible = round(cantidad_requerida + cantidad_comprada_orden_actual, 2)
                                    if cantidad <= cantidad_disponible:
                                        for suministro in suministros:
                                            if suministro['suministro'].id == suministro_id:
                                                suministro['cantidad'] = cantidad
                                            subtotal = round(subtotal + (suministro['cantidad'] * suministro['precio']), 2)
                                            valor_iva = round(valor_iva + (suministro['cantidad'] * suministro['precio'] * suministro['iva_suministro']), 2)
                                        valor_total = round(subtotal + valor_iva, 2)
                                        request.session['suministros'] = suministros
                                    else:
                                        error_cantidad = 'La cantidad no puede ser mayor a la cantidad requerida en el proyecto'
                                else:
                                    error_cantidad = 'La cantidad de este suministro que puede cotizar es: '+str(round(cantidad-(round(cantidad % suministro.unidad_embalaje, 2)), 2))
                error = {}
                if error_cantidad != '':
                    error = {'id': suministro_id, 'item': 'cantidad', 'value': cantidad, 'error': error_cantidad}
                pag = Paginador(request, suministros, 20, pagina)
                render = render_to_string('ajax/suministrosordencomprachange.html', {'user': user, 'orden_compra': orden_compra, 'suministros': pag, 'subtotal': subtotal, 'valor_iva': valor_iva, 'valor_total': valor_total, 'proyecto': proyecto, 'error': error})
                dajax.assign('#id_reporte_suministros', 'innerHTML', render)
                if error_cantidad != '':
                    dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_precio_suministro_orden_compra_change2(request, pagina, suministro_id, orden_compra_id, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
            # Verifica que se pueda modificar la orden de compra
            if len(orden_compra.informerecepcion_set.all()) == 0 and orden_compra.permiso_modificar:
                for suministro in suministros:
                    if suministro['suministro'].id == suministro_id:
                        error = {'id': suministro_id, 'item': 'precio', 'value': suministro['precio'], 'error': ''}
                pag = Paginador(request, suministros, 20, pagina)
                render = render_to_string('ajax/suministrosordencomprachange.html', {'user': user, 'suministros': pag, 'orden_compra': orden_compra, 'proyecto': proyecto, 'error': error})
                dajax.assign('#id_reporte_suministros', 'innerHTML', render)
                dajax.script("document.getElementById('id_text_precio_"+str(suministro_id)+"').select();")
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_precio_suministro_orden_compra_change2(request, suministro_id, precio, orden_compra_id, pagina, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
            # Verifica que se pueda modificar la orden de compra
            if len(orden_compra.informerecepcion_set.all()) == 0 and orden_compra.permiso_modificar:
                subtotal = 0
                valor_iva = 0
                valor_total = 0
                
                precio = precio.strip()
                error_precio = validar_cadena(precio)
                if error_precio == '':
                    error_precio = validar_cantidad_float_digitos(precio)
                    if error_precio == '':
                        error_precio = validar_cantidad_float(precio)
                        if error_precio == '':
                            precio = float(precio)
                            error_precio = validar_cantidad_float_0(precio)
                            if error_precio == '':
                                for suministro in suministros:
                                    if suministro['suministro'].id == suministro_id:
                                        suministro['precio'] = precio
                                    subtotal = round(subtotal + (suministro['cantidad'] * suministro['precio']), 2)
                                    valor_iva = round(valor_iva + (suministro['cantidad'] * suministro['precio'] * suministro['iva_suministro']), 2)
                                valor_total = round(subtotal + valor_iva, 2)
                                request.session['suministros'] = suministros
                error = {}
                if error_precio != '':
                    error = {'id': suministro_id, 'item': 'precio', 'value': precio, 'error': error_precio}
                pag = Paginador(request, suministros, 20, pagina)
                render = render_to_string('ajax/suministrosordencomprachange.html', {'user': user, 'orden_compra': orden_compra, 'suministros': pag, 'subtotal': subtotal, 'valor_iva': valor_iva, 'valor_total': valor_total, 'proyecto': proyecto, 'error': error})
                dajax.assign('#id_reporte_suministros', 'innerHTML', render)
                if error_precio != '':
                    dajax.script("document.getElementById('id_text_precio_"+str(suministro_id)+"').select();")
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_iva_suministro_orden_compra_change2(request, suministro_id, iva, orden_compra_id, pagina, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
            # Verifica que se pueda modificar la orden de compra
            if len(orden_compra.informerecepcion_set.all()) == 0 and orden_compra.permiso_modificar:
                subtotal = 0
                valor_iva = 0
                valor_total = 0

                for suministro in suministros:
                    if suministro['suministro'].id == suministro_id:
                        if iva:
                            suministro['iva_suministro'] = 0.16
                        else:
                            suministro['iva_suministro'] = 0
                    subtotal = round(subtotal + (suministro['cantidad'] * suministro['precio']), 2)
                    valor_iva = round(valor_iva + (suministro['cantidad'] * suministro['precio'] * suministro['iva_suministro']), 2)
                valor_total = round(subtotal + valor_iva, 2)
                request.session['suministros'] = suministros
                pag = Paginador(request, suministros, 20, pagina)
                render = render_to_string('ajax/suministrosordencomprachange.html', {'user': user, 'orden_compra': orden_compra, 'suministros': pag, 'subtotal': subtotal, 'valor_iva': valor_iva, 'valor_total': valor_total, 'proyecto': proyecto})
                dajax.assign('#id_reporte_suministros', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_observaciones_suministro_orden_compra_change2(request, pagina, suministro_id, orden_compra_id, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
            # Verifica que se pueda modificar la orden de compra
            if len(orden_compra.informerecepcion_set.all()) == 0 and orden_compra.permiso_modificar:
                subtotal = 0
                valor_iva = 0
                valor_total = 0
                error = {}
                for suministro in suministros:
                    if suministro['suministro'].id == suministro_id:
                        error = {'id': suministro_id, 'item': 'observaciones', 'value': suministro['observaciones'], 'error': ''}
                    subtotal = round(subtotal + (suministro['cantidad'] * suministro['precio']), 2)
                    valor_iva = round(valor_iva + (suministro['cantidad'] * suministro['precio'] * suministro['iva_suministro']), 2)
                valor_total = round(subtotal + valor_iva, 2)
                pag = Paginador(request, suministros, 20, pagina)
                render = render_to_string('ajax/suministrosordencomprachange.html', {'user': user, 'orden_compra': orden_compra, 'suministros': pag, 'subtotal': subtotal, 'valor_iva': valor_iva, 'valor_total': valor_total, 'proyecto': proyecto, 'error': error})
                dajax.assign('#id_reporte_suministros', 'innerHTML', render)
                dajax.script("document.getElementById('id_text_observaciones_"+str(suministro_id)+"').select();")
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_observaciones_suministro_orden_compra_change2(request, suministro_id, observaciones, orden_compra_id, pagina, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
            # Verifica que se pueda modificar la orden de compra
            if len(orden_compra.informerecepcion_set.all()) == 0 and orden_compra.permiso_modificar:
                subtotal = 0
                valor_iva = 0
                valor_total = 0

                observaciones = observaciones.strip()
                for suministro in suministros:
                    if suministro['suministro'].id == suministro_id:
                        suministro['observaciones'] = observaciones
                    subtotal = round(subtotal + (suministro['cantidad'] * suministro['precio']), 2)
                    valor_iva = round(valor_iva + (suministro['cantidad'] * suministro['precio'] * suministro['iva_suministro']), 2)
                valor_total = round(subtotal + valor_iva, 2)
                request.session['suministros'] = suministros
                error = {}
                pag = Paginador(request, suministros, 20, pagina)
                render = render_to_string('ajax/suministrosordencomprachange.html', {'user': user, 'orden_compra': orden_compra, 'suministros': pag, 'subtotal': subtotal, 'valor_iva': valor_iva, 'valor_total': valor_total, 'proyecto': proyecto, 'error': error})
                dajax.assign('#id_reporte_suministros', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def suministros_proveedor_orden_compra_change2(request, orden_compra_id, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
            # Verifica que se pueda modificar la orden de compra
            if len(orden_compra.informerecepcion_set.all()) == 0 and orden_compra.permiso_modificar:
                suministros_agregar = None
                try:
                    suministros_agregar = request.session['suministros_agregar']
                except :
                    suministros_agregar = []
                    request.session['suministros_agregar'] = suministros_agregar
                ids_suministros_excluir = []
                for suministro in suministros:
                    ids_suministros_excluir.append(suministro['suministro'].id)

                #Visualiza los suministros requeridos con la cantidad a cotizar
                if criterio != None:
                    criterio = criterio.strip()
                else:
                    criterio = ''
                suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(criterio=criterio, proveedor_id=orden_compra.proveedor.id, exclude_suministros_id=ids_suministros_excluir)
                suministros_comprar = []
                for suministro_requisiciones in suministros_requisiciones:
                    suministro_orden_compra_item = None
                    try:
                        suministro_orden_compra_item = orden_compra.suministroordencompraitem_set.get(suministro=suministro_requisiciones.suministro.suministro)
                    except :
                        pass
                    if suministro_orden_compra_item != None:
                        suministro_requisiciones.cantidad_requerida = round(suministro_requisiciones.cantidad_requerida + suministro_orden_compra_item.suministroordencompra_set.aggregate(Sum('cantidad_comprada'))['cantidad_comprada__sum'], 2)
                    suministro_comprar = {'suministro': suministro_requisiciones, 'cantidad': '', 'precio': '', 'iva_suministro': '', 'observaciones': suministro_requisiciones.observaciones}
                    for suministro_agregar in suministros_agregar:
                        if suministro_requisiciones.suministro.suministro.id == suministro_agregar['suministro'].id:
                            suministro_comprar['cantidad'] = suministro_agregar['cantidad']
                            suministro_comprar['precio'] = suministro_agregar['precio']
                            suministro_comprar['iva_suministro'] = suministro_agregar['iva_suministro']
                            suministro_comprar['observaciones'] = suministro_agregar['observaciones']
                    suministros_comprar.append(suministro_comprar)

                pag = Paginador(request, suministros_comprar, 20, 1)
                render = render_to_string('ajax/suministrosrequisicionesproveedorsearchordencomprachange.html', {'user': user, 'suministros_requisiciones': pag, 'orden_compra': orden_compra, 'criterio': criterio, 'proyecto': proyecto} )
                dajax.assign('#light', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='block';")
                dajax.script("document.getElementById('fade').style.display='block';")
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def anadir_suministro_orden_compra_change2(request, pagina, suministro_id, cantidad, precio, iva_suministro, observaciones, orden_compra_id, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        suministros_agregar = None
        try:
            suministros = request.session['suministros']
            suministros_agregar = request.session['suministros_agregar']
        except :
            pass
        if suministros != None and suministros_agregar != None:
            orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
            cantidad = cantidad.strip()
            precio = precio.strip()
            observaciones = observaciones.strip()

            error_cantidad = ''
            validaciones_cantidad = Validator().append([
                Field('cantidad', cantidad).append([
                    IsRequired('Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
                ]),
            ]).run(True).pop()

            error_precio = ''
            validaciones_precio = Validator().append([
                Field('precio', precio).append([
                    IsRequired('Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
                ]),
            ]).run(True).pop()

            if iva_suministro:
                iva_suministro = 0.16
            else:
                iva_suministro = 0

            if validaciones_cantidad['passed'] == True and validaciones_precio['passed'] == True:
                cantidad = float(cantidad)
                precio = float(precio)
                if cantidad > 0:
                    if precio > 0:
                        suministro_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(proveedor_id=orden_compra.proveedor_id, suministro_id=suministro_id).pop()
                        suministro_orden_compra_item = None
                        try:
                            suministro_orden_compra_item = orden_compra.suministroordencompraitem_set.get(suministro=suministro_requisiciones.suministro.suministro)
                        except :
                            pass
                        if suministro_orden_compra_item != None:
                            suministro_requisiciones.cantidad_requerida = round(suministro_requisiciones.cantidad_requerida + suministro_orden_compra_item.suministroordencompra_set.aggregate(Sum('cantidad_comprada'))['cantidad_comprada__sum'], 2)
                        if cantidad <= suministro_requisiciones.cantidad_requerida:
                            suministro = suministro_requisiciones.suministro.suministro
                            if is_residuo_0(cantidad, suministro.unidad_embalaje):
                                existe_suministro = False
                                for suministro_agregar in suministros_agregar:
                                    if suministro_agregar['suministro'].id == suministro_id:
                                        suministro_agregar['cantidad'] = cantidad
                                        suministro_agregar['precio'] = precio
                                        suministro_agregar['iva_suministro'] = iva_suministro
                                        suministro_agregar['observaciones'] = observaciones
                                        existe_suministro = True
                                if existe_suministro == False:
                                    suministros_agregar.append({'suministro': suministro, 'cantidad': cantidad, 'precio': precio, 'iva_suministro': iva_suministro, 'observaciones': observaciones})
                            else:
                                error_cantidad = 'La cantidad de este suministro que puede cotizar es: '+str(round(cantidad-(round(cantidad % suministro.unidad_embalaje, 2)), 2))
                        else:
                            error_cantidad = 'La cantidad no debe ser mayor al total requerido'
                    else:
                            error_precio = 'El cantidad debe ser mayor a 0 (cero).'
                else:
                    if cantidad == 0:
                        error_cantidad = ''
                        error_precio = ''
                        for suministro_agregar in suministros_agregar:
                            if suministro_agregar['suministro'].id == suministro_id:
                                suministros_agregar.remove(suministro_agregar)
                request.session['suministros_agregar'] = suministros_agregar
            else:
                if validaciones_cantidad['passed'] == False:
                    for error in validaciones_cantidad['errors']:
                        error_cantidad = error

                if validaciones_precio['passed'] == False:
                    for error in validaciones_precio['errors']:
                        error_precio = error

            error = {}
            if error_cantidad != '' or error_precio != '':
                error = {'id': suministro_id, 'value': cantidad, 'error': error_cantidad, 'value_precio': precio, 'error_precio': error_precio, 'iva_suministro': iva_suministro, 'value_observaciones': observaciones}

            criterio = criterio.strip()
            ids_suministros_excluir = []
            for suministro in suministros:
                ids_suministros_excluir.append(suministro['suministro'].id)

            #Visualiza los suministros requeridos con la cantidad a cotizar
            suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(criterio=criterio, proveedor_id=orden_compra.proveedor.id, exclude_suministros_id=ids_suministros_excluir)
            suministros_comprar = []
            for suministro_requisiciones in suministros_requisiciones:
                suministro_orden_compra_item = None
                try:
                    suministro_orden_compra_item = orden_compra.suministroordencompraitem_set.get(suministro=suministro_requisiciones.suministro.suministro)
                except :
                    pass
                if suministro_orden_compra_item != None:
                    suministro_requisiciones.cantidad_requerida = round(suministro_requisiciones.cantidad_requerida + suministro_orden_compra_item.suministroordencompra_set.aggregate(Sum('cantidad_comprada'))['cantidad_comprada__sum'], 2)
                suministro_comprar = {'suministro': suministro_requisiciones, 'cantidad': '', 'precio': '', 'observaciones': suministro_requisiciones.observaciones}
                for suministro_agregar in suministros_agregar:
                    if suministro_requisiciones.suministro.suministro.id == suministro_agregar['suministro'].id:
                        suministro_comprar['cantidad'] = suministro_agregar['cantidad']
                        suministro_comprar['precio'] = suministro_agregar['precio']
                        suministro_comprar['iva_suministro'] = suministro_agregar['iva_suministro']
                        suministro_comprar['observaciones'] = suministro_agregar['observaciones']
                suministros_comprar.append(suministro_comprar)

            pag = Paginador(request, suministros_comprar, 20, pagina)
            render = render_to_string('ajax/suministrosrequisicionesproveedorsearchordencomprachange.html', {'user': user, 'suministros_requisiciones': pag, 'orden_compra': orden_compra, 'criterio': criterio, 'error': error, 'proyecto': proyecto})
            dajax.assign('#light', 'innerHTML', render)
            if error_cantidad != '':
                dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
            elif error_precio != '':
                dajax.script("document.getElementById('id_text_precio_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_suministro_agregar_orden_compra_change2(request, pagina, suministro_id, orden_compra_id, criterio, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        suministros_agregar = None
        try:
            suministros = request.session['suministros']
            suministros_agregar = request.session['suministros_agregar']
        except :
            pass
        if suministros != None and suministros_agregar != None:
            orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)

            error = {}
            for suministro_agregar in suministros_agregar:
                if suministro_agregar['suministro'].id == suministro_id:
                    error = {'id': suministro_id, 'value': suministro_agregar['cantidad'], 'error': '', 'value_precio': suministro_agregar['precio'], 'error_precio': '', 'iva_suministro': suministro_agregar['iva_suministro'], 'value_observaciones': suministro_agregar['observaciones']}

            criterio = criterio.strip()

            ids_suministros_excluir = []
            for suministro in suministros:
                ids_suministros_excluir.append(suministro['suministro'].id)

            #Visualiza los suministros requeridos con la cantidad a cotizar
            suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(criterio=criterio, proveedor_id=orden_compra.proveedor.id, exclude_suministros_id=ids_suministros_excluir)
            suministros_comprar = []
            for suministro_requisiciones in suministros_requisiciones:
                suministro_orden_compra_item = None
                try:
                    suministro_orden_compra_item = orden_compra.suministroordencompraitem_set.get(suministro=suministro_requisiciones.suministro.suministro)
                except :
                    pass
                if suministro_orden_compra_item != None:
                    suministro_requisiciones.cantidad_requerida = round(suministro_requisiciones.cantidad_requerida + suministro_orden_compra_item.suministroordencompra_set.aggregate(Sum('cantidad_comprada'))['cantidad_comprada__sum'], 2)
                suministro_comprar = {'suministro': suministro_requisiciones, 'cantidad': '', 'precio': '', 'iva_suministro': 0, 'observaciones': suministro_requisiciones.observaciones}
                for suministro_agregar in suministros_agregar:
                    if suministro_requisiciones.suministro.suministro.id == suministro_agregar['suministro'].id:
                        suministro_comprar['cantidad'] = suministro_agregar['cantidad']
                        suministro_comprar['precio'] = suministro_agregar['precio']
                        suministro_comprar['iva_suministro'] = suministro_agregar['iva_suministro']
                        suministro_comprar['observaciones'] = suministro_agregar['observaciones']
                suministros_comprar.append(suministro_comprar)

            pag = Paginador(request, suministros_comprar, 20, pagina)
            render = render_to_string('ajax/suministrosrequisicionesproveedorsearchordencomprachange.html', {'user': user, 'suministros_requisiciones': pag, 'orden_compra': orden_compra, 'criterio': criterio, 'error': error, 'proyecto': proyecto})
            dajax.assign('#light', 'innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def anadir_todos_suministros_orden_compra_change2(request, orden_compra_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        suministros_agregar = None
        try:
            suministros = request.session['suministros']
            suministros_agregar = request.session['suministros_agregar']
        except :
            pass
        if suministros != None and suministros_agregar != None:
            orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)

            ids_suministros_excluir = []
            for suministro in suministros:
                ids_suministros_excluir.append(suministro['suministro'].id)

            #Visualiza los suministros requeridos con la cantidad a cotizar
            suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(proveedor_id=orden_compra.proveedor.id, exclude_suministros_id=ids_suministros_excluir)
            suministros_comprar = []
            for suministro_requisiciones in suministros_requisiciones:
                suministro_orden_compra_item = None
                try:
                    suministro_orden_compra_item = orden_compra.suministroordencompraitem_set.get(suministro=suministro_requisiciones.suministro.suministro)
                except :
                    pass
                if suministro_orden_compra_item != None:
                    suministro_requisiciones.cantidad_requerida = round(suministro_requisiciones.cantidad_requerida + suministro_orden_compra_item.suministroordencompra_set.aggregate(Sum('cantidad_comprada'))['cantidad_comprada__sum'], 2)
                suministro_comprar = {'suministro': suministro_requisiciones, 'cantidad': '', 'observaciones': suministro_requisiciones.observaciones}
                suministro_existe_lista_suministros_agregar = False
                for suministro_agregar in suministros_agregar:
                    if suministro_requisiciones.suministro.suministro.id == suministro_agregar['suministro'].id:
                        suministro_existe_lista_suministros_agregar = True
                if suministro_existe_lista_suministros_agregar == False:
                    if suministro_requisiciones.cantidad_requerida >= suministro_requisiciones.suministro.suministro.unidad_embalaje:
                        cantidad_comprar = round(suministro_requisiciones.cantidad_requerida - round(round(round(suministro_requisiciones.cantidad_requerida * 100, 2) % (round(suministro_requisiciones.suministro.suministro.unidad_embalaje * 100, 2)), 2) / 100, 2), 2)
                        suministro_comprar['cantidad'] = cantidad_comprar
                        suministro_comprar['observaciones'] = suministro_requisiciones.observaciones
                        suministros_agregar.append({'suministro': suministro_requisiciones.suministro.suministro, 'cantidad': cantidad_comprar, 'observaciones': suministro_requisiciones.observaciones })
                suministros_comprar.append(suministro_comprar)

            pag = Paginador(request, suministros_comprar, 20, 1)
            render = render_to_string('ajax/suministrosrequisicionesproveedorsearchordencomprachange.html', {'user': user, 'suministros_requisiciones': pag, 'orden_compra': orden_compra, 'proyecto': proyecto})
            dajax.assign('#light', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def anadir_suministros_orden_compra_change2(request, orden_compra_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        suministros_agregar = None
        try:
            suministros = request.session['suministros']
            suministros_agregar = request.session['suministros_agregar']
        except :
            pass
        if suministros != None and suministros_agregar != None:
            orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)

            cantidades_disponibles = True
            # Validar que esten disponibles las cantidades
            for suministro_agregar in suministros_agregar:
                suministro_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(proveedor_id=orden_compra.proveedor.id, suministro_id=suministro_agregar['suministro'].id).pop()
                suministro_orden_compra_item = None
                try:
                    suministro_orden_compra_item = orden_compra.suministroordencompraitem_set.get(suministro=suministro_requisiciones.suministro.suministro)
                except :
                    pass
                if suministro_orden_compra_item != None:
                    suministro_requisiciones.cantidad_requerida = round(suministro_requisiciones.cantidad_requerida + suministro_orden_compra_item.suministroordencompra_set.aggregate(Sum('cantidad_comprada'))['cantidad_comprada__sum'], 2)
                if suministro_agregar['cantidad'] <= suministro_requisiciones.cantidad_requerida:
                    suministros.append(suministro_agregar)
                else:
                    cantidades_disponibles = False

            # Elimina las variables de session
            del request.session['suministros_agregar']

            subtotal = 0
            valor_iva = 0
            valor_total = 0
            for suministro in suministros:
                subtotal = round(subtotal + (suministro['cantidad'] * suministro['precio']), 2)
                valor_iva = round(valor_iva + (suministro['cantidad'] * suministro['precio'] * suministro['iva_suministro']), 2)
            valor_total = round(subtotal + valor_iva, 2)

            pag = Paginador(request, suministros, 20, 1)
            render = render_to_string('ajax/suministrosordencomprachange.html', {'user': user, 'orden_compra': orden_compra, 'suministros': pag, 'subtotal': subtotal, 'valor_iva': valor_iva, 'valor_total': valor_total, 'proyecto': proyecto})
            dajax.assign('#id_reporte_suministros', 'innerHTML', render)
            if cantidades_disponibles == False:
                dajax.alert('No se han agregado algunos suministros por la disponibilidad en las cantidades en requisiciones')
            dajax.script("document.getElementById('light').style.display='none';")
            dajax.script("document.getElementById('fade').style.display='none';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def cancelar_anadir_suministros_orden_compra_change2(request, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        suministros_agregar = None
        try:
            suministros = request.session['suministros']
            suministros_agregar = request.session['suministros_agregar']
        except :
            pass
        if suministros != None and suministros_agregar != None:
            del request.session['suministros_agregar']
            dajax.script("document.getElementById('light').style.display='none';")
            dajax.script("document.getElementById('fade').style.display='none';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def asignar_modificacion_orden_compra2(request, permiso, orden_compra_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.assignchangepermission_ordencompra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
            if orden_compra.permite_modificar() == True:
                if permiso == 1:
                    orden_compra.permiso_modificar = True
                elif permiso == 0:
                    orden_compra.permiso_modificar = False
                orden_compra.save()
                dajax.redirect('/inverboy/home/ordenescompraproyectodetails/'+str(orden_compra_id)+'/'+str(proyecto_id)+'/')
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_precio_suministro_cotizacion_realizar_orden_servicio2(request, pagina, suministro_id, cotizacion_id, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        cotizacion = None
        try:
            cotizacion = proyecto.cotizacion_set.get(id=cotizacion_id)
        except :
            pass
        if cotizacion != None:
            suministros = cotizacion.suministrocotizacion_set.all()
            pag = Paginador(request, suministros, 20, pagina)
            suministro = cotizacion.suministrocotizacion_set.get(id=suministro_id)
            error = { 'id': suministro_id, 'item': 'precio', 'value': suministro.precio, 'error': '' }
            render = render_to_string('ajax/suministroscotizacionordenserviciosearch.html', {'user': user, 'suministros': pag, 'cotizacion': cotizacion, 'proyecto': proyecto, 'error': error })
            dajax.assign('#id_reporte_suministros', 'innerHTML', render)
            dajax.script("document.getElementById('id_text_precio_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def cambiar_tipo_iva_cotizacion_orden_servicio_add2(request, parametro, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        dajax.script("document.getElementById('id_parametros_iva_aiu').style.display='none';")
        dajax.script("document.getElementById('id_parametros_iva_utilidad').style.display='none';")
        out_aiu = '<label>Porcentaje aiu: </label><input type="text" id="id_a_i_u" name="a_i_u" value=""> %'
        out_utilidad = '<label>Utilidad: </label><input type="text" id="id_utilidad" name="utilidad" value=""> %'
        dajax.assign('#id_parametros_iva_aiu', 'innerHTML', out_aiu)
        dajax.assign('#id_parametros_iva_utilidad', 'innerHTML', out_utilidad)
        if parametro == '1':
            dajax.script("document.getElementById('id_parametros_iva_aiu').style.display='block';")
            dajax.script("document.getElementById('id_parametros_iva_utilidad').style.display='block';")
        elif parametro == '3':
            dajax.script("document.getElementById('id_parametros_iva_aiu').style.display='block';")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_suministro_cotizacion2(request, suministro_id, cantidad, cotizacion_id, pagina, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        cotizacion = None
        try:
            cotizacion = proyecto.cotizacion_set.get(id=cotizacion_id, proyecto=proyecto)
        except :
            pass
        if cotizacion != None:
            suministro_cotizacion = cotizacion.suministrocotizacion_set.get(id=suministro_id)
            cantidad_requerida = suministro_cotizacion.cantidad_total_requerida_suministro_proyecto().cantidad_requerida
            error_cantidad = validar_cantidad_float(cantidad)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float_digitos(cantidad)
                if error_cantidad == '':
                    cantidad = float(cantidad)
                    error_cantidad = validar_cantidad_float_0(cantidad)
                    if error_cantidad == '':
                        if cantidad <= cantidad_requerida:
                            if is_residuo_0(cantidad, suministro_cotizacion.suministro.unidad_embalaje):
                                suministro_cotizacion.cantidad_cotizada = cantidad
                                suministro_cotizacion.save()
                            else:
                                error_cantidad = u'La cantidad deben ser un multiplo de la unidad de embalaje del suministro'
                        else:
                            error_cantidad = u'La cantidad no debe ser mayor a la cantidad requerida en el proyecto'
            error = {}
            if error_cantidad != '':
                error = { 'id': suministro_id, 'item': 'cantidad', 'value': cantidad, 'error': error_cantidad }
            suministros = cotizacion.suministrocotizacion_set.all()
            pag = Paginador(request, suministros, 20, pagina)
            render = render_to_string('ajax/suministroscotizacionsearch.html', {'user': user, 'cotizacion': cotizacion, 'suministros': pag, 'proyecto': proyecto, 'error': error })
            dajax.assign('#id_reporte_suministros', 'innerHTML', render)
            if error_cantidad != '':
                dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_suministro_cotizacion_orden_servicio2(request, suministro_id, cantidad, cotizacion_id, pagina, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        cotizacion = None
        try:
            cotizacion = proyecto.cotizacion_set.get(id=cotizacion_id)
        except :
            pass
        if cotizacion != None:
            suministro_cotizacion = cotizacion.suministrocotizacion_set.get(id=suministro_id)
            cantidad_requerida = suministro_cotizacion.cantidad_total_requerida_suministro_proyecto().cantidad_requerida
            cantidad = cantidad.strip()
            error_cantidad = validar_cantidad_float(cantidad)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float_digitos(cantidad)
                if error_cantidad == '':
                    error_cantidad = validar_cantidad_float_0(cantidad)
                    if error_cantidad == '':
                        cantidad = float(cantidad)
                        if error_cantidad == '':
                            if cantidad <= cantidad_requerida:
                                suministro_cotizacion.cantidad_cotizada = cantidad
                                suministro_cotizacion.save()
                            else:
                                error_cantidad = 'La cantidad no debe ser mayor a la cantidad requerida en el proyecto'
            error = {}
            if error_cantidad != '':
                error = { 'id': suministro_id, 'item': 'cantidad', 'value': cantidad, 'error': error_cantidad }
            suministros = cotizacion.suministrocotizacion_set.all()
            pag = Paginador(request, suministros, 20, pagina)
            render = render_to_string('ajax/suministroscotizacionordenserviciosearch.html', {'user': user, 'cotizacion': cotizacion, 'proyecto': proyecto, 'suministros': pag, 'error': error })
            dajax.assign('#id_reporte_suministros', 'innerHTML', render)
            if error_cantidad != '':
                dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_precio_suministro_cotizacion_orden_compra_add2(request, pagina, suministro_id, cotizacion_id, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        cotizacion = None
        try:
            cotizacion = proyecto.cotizacion_set.get(id=cotizacion_id)
        except :
            pass
        if cotizacion != None:
            suministros = cotizacion.suministrocotizacion_set.all()
            pag = Paginador(request, suministros, 20, pagina)
            suministro = cotizacion.suministrocotizacion_set.get(id=suministro_id)
            error = { 'id': suministro_id, 'item': 'precio', 'value': suministro.precio, 'error': '' }
            render = render_to_string('ajax/suministroscotizacionsearch.html', {'user': user, 'suministros': pag, 'cotizacion': cotizacion, 'proyecto': proyecto, 'error': error })
            dajax.assign('#id_reporte_suministros', 'innerHTML', render)
            dajax.script("document.getElementById('id_text_precio_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_precio_suministro_cotizacion2(request, suministro_id, precio, cotizacion_id, pagina, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        cotizacion = None
        try:
            cotizacion = proyecto.cotizacion_set.get(id=cotizacion_id)
        except :
            pass
        if cotizacion != None:
            error_precio = validar_cantidad_float_digitos(precio)
            if error_precio == '':
                error_precio = validar_cantidad_float(precio)
            if error_precio == '':
                precio = float(precio)
                error_precio = validar_cantidad_float_0(precio)
            if error_precio == '':
                cotizacion.suministrocotizacion_set.filter(id=suministro_id).update(precio=precio)
                #dajax.script("Calendar.setup({inputField:'id_fecha_arribo',ifFormat:'%Y-%m-%d',button:'lanzador'});")
            error = {}
            if error_precio != '':
                error = { 'id': suministro_id, 'item': 'precio', 'value': precio, 'error': error_precio}
            suministros = cotizacion.suministrocotizacion_set.all()
            pag = Paginador(request, suministros, 20, pagina)
            if cotizacion.tipo == 1:
                render = render_to_string('ajax/suministroscotizacionsearch.html', {'user': user, 'cotizacion': cotizacion, 'suministros': pag, 'proyecto': proyecto, 'error': error })
            elif cotizacion.tipo == 2:
                render = render_to_string('ajax/suministroscotizacionordenserviciosearch.html', {'user': user, 'cotizacion': cotizacion, 'suministros': pag, 'proyecto': proyecto, 'error': error })
            dajax.assign('#id_reporte_suministros', 'innerHTML', render)
            if error_precio != '':
                dajax.script("document.getElementById('id_text_precio_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_iva_suministro_cotizacion2(request, suministro_id, cotizacion_id, iva, pagina, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        cotizacion = None
        try:
            cotizacion = proyecto.cotizacion_set.get(id=cotizacion_id)
        except :
            pass
        if cotizacion != None:
            suministro = cotizacion.suministrocotizacion_set.get(id=suministro_id)
            if iva == True:
                suministro.iva_suministro = 0.16
            elif iva == False:
                suministro.iva_suministro = 0
            suministro.save()
            suministros = cotizacion.suministrocotizacion_set.all()
            pag = Paginador(request, suministros, 20, pagina)
            if cotizacion.tipo == 1:
                render = render_to_string('ajax/suministroscotizacionsearch.html', {'user': user, 'cotizacion': cotizacion, 'suministros': pag, 'proyecto': proyecto })
            elif cotizacion.tipo == 2:
                render = render_to_string('ajax/suministroscotizacionordenserviciosearch.html', {'user': user, 'cotizacion': cotizacion, 'suministros': pag, 'proyecto': proyecto })
            dajax.assign('#id_reporte_suministros', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_observaciones_suministro_cotizacion_orden_compra_add2(request, pagina, suministro_id, cotizacion_id, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        cotizacion = None
        try:
            cotizacion = proyecto.cotizacion_set.get(id=cotizacion_id)
        except :
            pass
        if cotizacion != None:
            suministros = cotizacion.suministrocotizacion_set.all()
            pag = Paginador(request, suministros, 20, pagina)
            suministro = cotizacion.suministrocotizacion_set.get(id=suministro_id)
            error = { 'id': suministro_id, 'item': 'observaciones', 'value': suministro.observaciones, 'error': '' }
            render = render_to_string('ajax/suministroscotizacionsearch.html', {'user': user, 'suministros': pag, 'cotizacion': cotizacion, 'proyecto': proyecto, 'error': error })
            dajax.assign('#id_reporte_suministros', 'innerHTML', render)
            dajax.script("document.getElementById('id_text_observaciones_"+str(suministro_id)+"').focus();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_observaciones_suministro_cotizacion2(request, suministro_id, observaciones, cotizacion_id, pagina, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'auth.view_group'):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        cotizacion = None
        try:
            cotizacion = proyecto.cotizacion_set.get(id=cotizacion_id)
        except :
            pass
        if cotizacion != None:
            cotizacion.suministrocotizacion_set.filter(id=suministro_id).update(observaciones=observaciones.strip())
            error = {}
            suministros = cotizacion.suministrocotizacion_set.all()
            pag = Paginador(request, suministros, 20, pagina)
            if cotizacion.tipo == 1:
                render = render_to_string('ajax/suministroscotizacionsearch.html', {'user': user, 'cotizacion': cotizacion, 'suministros': pag, 'proyecto': proyecto, 'error': error })
            elif cotizacion.tipo == 2:
                render = render_to_string('ajax/suministroscotizacionordenserviciosearch.html', {'user': user, 'cotizacion': cotizacion, 'suministros': pag, 'proyecto': proyecto, 'error': error })
            dajax.assign('#id_reporte_suministros', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def compra_suministros_proveedor2(request, proveedor_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        usuario = Usuario.objects.get(id=user.id)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        proveedor = Proveedor.objects.get(id=proveedor_id)

        cotizacion = Cotizacion()
        cotizacion.tipo = 1
        cotizacion.proyecto = proyecto
        cotizacion.proveedor = proveedor
        cotizacion.persona = usuario
        request.session['cotizacion'] = cotizacion

        request.session['suministros_cotizacion'] = []

        #Visualiza los suministros requeridos con la cantidad a cotizar
        suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(proveedor_id=proveedor_id)
        suministros_comprar = []
        for suministro_requisiciones in suministros_requisiciones:
            suministro_comprar = {'suministro': suministro_requisiciones, 'cantidad_nueva_cotizacion': '', 'observaciones': suministro_requisiciones.observaciones}
            suministros_comprar.append(suministro_comprar)

        pag = Paginador(request, suministros_comprar, 20, 1)
        render = render_to_string('ajax/suministrosrequisicionesproveedorsearch.html', {'user': user, 'suministros_requisiciones': pag, 'proveedor': proveedor, 'proyecto': proyecto } )
        dajax.assign('#light', 'innerHTML', render)
        dajax.script("document.getElementById('light').style.display='block';")
        dajax.script("document.getElementById('fade').style.display='block';")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_suministro_informe_recepcion2(request, pagina, suministro_id, orden_compra_id, criterio, proyecto_id, cantidad):
    from django.db.models import Sum
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
        suministros_informe_recepcion = None
        try:
            suministros_informe_recepcion = request.session['suministros_informe_recepcion']
        except :
            pass
        if suministros_informe_recepcion != None:
            error_cantidad = validar_cadena(cantidad)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float_digitos(cantidad)
                if error_cantidad == '':
                    error_cantidad = validar_cantidad_float(cantidad)
                    if error_cantidad == '':
                        cantidad = float(cantidad)
                        error_cantidad = validar_cantidad_float_0(cantidad)
                        if error_cantidad == '':
                            suministro = Suministro.objects.get(id=suministro_id)
                            if is_residuo_0(cantidad, suministro.unidad_embalaje):
                                cantidad_total_recibida = SuministroOrdenCompra.objects.filter(suministro__suministro__suministro__id=suministro_id, orden_compra=orden_compra, orden_compra__proyecto=proyecto).aggregate(Sum('cantidad_almacen'))
                                cantidad_total_comprada = SuministroOrdenCompra.objects.filter(suministro__suministro__suministro__id=suministro_id, orden_compra=orden_compra, orden_compra__proyecto=proyecto).aggregate(Sum('cantidad_comprada'))
                                cantidad_total_recibir = round(cantidad_total_comprada['cantidad_comprada__sum'] - cantidad_total_recibida['cantidad_almacen__sum'], 2)
                                if cantidad <= float(str(cantidad_total_recibir)):
                                    existe_suministro = False
                                    for suministro_informe_recepcion in suministros_informe_recepcion:
                                        if suministro_informe_recepcion['id'] == suministro_id:
                                            suministro_informe_recepcion['cantidad'] = cantidad
                                            existe_suministro = True
                                    if existe_suministro == False:
                                        suministro = { 'id': suministro_id, 'cantidad': cantidad }
                                        suministros_informe_recepcion.append(suministro)
                                else:
                                    error_cantidad = 'La cantidad no debe ser mayor a la cantidad por recibir'
                            else:
                                error_cantidad = 'La cantidad debe ser multiplo de la unidad de embalaje del sumnistro'
                        else:
                            if cantidad == 0:
                                error_cantidad = ''
                                for suministro_informe_recepcion in suministros_informe_recepcion:
                                    if suministro_informe_recepcion['id'] == suministro_id:
                                        suministros_informe_recepcion.remove(suministro_informe_recepcion)
            request.session['suministros_informe_recepcion'] = suministros_informe_recepcion
            error = {}
            if error_cantidad != '':
                error = { 'id': suministro_id, 'value': cantidad, 'error': error_cantidad }
            suministros = orden_compra.suministroordencompra_set.all().order_by('suministro__suministro__suministro__nombre')
            criterio = criterio.strip()
            if criterio != '':
                suministros = suministros.filter(Q(suministro__suministro__suministro__nombre__icontains=criterio))
            suministros_orden_compra = []
            for suministro in suministros:
                suministro_tmp = suministro
                suministro_adicionado = False
                for suministro_tmp2 in suministros_orden_compra:
                    if suministro_tmp2['suministro'].suministro.suministro.suministro.id == suministro_tmp.suministro.suministro.suministro.id:
                        suministro_tmp2['suministro'].cantidad_comprada = round(suministro_tmp2['suministro'].cantidad_comprada + suministro_tmp.cantidad_comprada, 2)
                        suministro_tmp2['suministro'].cantidad_almacen = round(suministro_tmp2['suministro'].cantidad_almacen + suministro_tmp.cantidad_almacen, 2)
                        suministro_adicionado = True
                if suministro_adicionado == False:
                    suministros_orden_compra.append({'suministro': suministro_tmp, 'cantidad_nuevo_informe': ''})
            for suministro_informe_recepcion in suministros_informe_recepcion:
                for suministro_orden_compra in suministros_orden_compra:
                    if suministro_informe_recepcion['id'] == suministro_orden_compra['suministro'].suministro.suministro.suministro.id:
                        suministro_orden_compra['cantidad_nuevo_informe'] = suministro_informe_recepcion['cantidad']
            pag = Paginador(request, suministros_orden_compra, 20, pagina)
            render =  render_to_string('ajax/suministrosordencomprasearchinformerecepcion.html', {'user': user, 'suministros': pag, 'criterio': criterio, 'orden_compra': orden_compra, 'proyecto': proyecto, 'error': error })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
            if error_cantidad != '':
                dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_modificar_suministro_informe_recepcion2(request, pagina, suministro_id, orden_compra_id, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
        suministros_informe_recepcion = None
        try:
            suministros_informe_recepcion = request.session['suministros_informe_recepcion']
        except :
            pass
        if suministros_informe_recepcion != None:
            error = {}
            for suministro_informe_recepcion in suministros_informe_recepcion:
                if suministro_informe_recepcion['id'] == suministro_id:
                    error = { 'id': suministro_id, 'value': suministro_informe_recepcion['cantidad'], 'error': '' }
            suministros = orden_compra.suministroordencompra_set.all().order_by('suministro__suministro__suministro__nombre')
            criterio = criterio.strip()
            if criterio != '':
                suministros = suministros.filter(Q(suministro__suministro__suministro__nombre__icontains=criterio))
            suministros_orden_compra = []
            for suministro in suministros:
                suministro_tmp = suministro
                suministro_adicionado = False
                for suministro_tmp2 in suministros_orden_compra:
                    if suministro_tmp2['suministro'].suministro.suministro.suministro.id == suministro_tmp.suministro.suministro.suministro.id:
                        suministro_tmp2['suministro'].cantidad_comprada = round(suministro_tmp2['suministro'].cantidad_comprada + suministro_tmp.cantidad_comprada, 2)
                        suministro_tmp2['suministro'].cantidad_almacen = round(suministro_tmp2['suministro'].cantidad_almacen + suministro_tmp.cantidad_almacen, 2)
                        suministro_adicionado = True
                if suministro_adicionado == False:
                    suministros_orden_compra.append({'suministro': suministro_tmp, 'cantidad_nuevo_informe': ''})
            for suministro_informe_recepcion in suministros_informe_recepcion:
                for suministro_orden_compra in suministros_orden_compra:
                    if suministro_informe_recepcion['id'] == suministro_orden_compra['suministro'].suministro.suministro.suministro.id:
                        suministro_orden_compra['cantidad_nuevo_informe'] = suministro_informe_recepcion['cantidad']
            pag = Paginador(request, suministros_orden_compra, 20, pagina)
            render =  render_to_string('ajax/suministrosordencomprasearchinformerecepcion.html', {'user': user, 'suministros': pag, 'criterio': criterio, 'orden_compra': orden_compra, 'proyecto': proyecto, 'error': error })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#Ventana agregar suministro informe de salida (APU's de proyecto)
def ventana_agregar_suministro_informe_salida2(request, pagina, suministro_id, criterio_apu, criterio_suministro, pagina_suministro, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros_informe_salida = None
        try:
            suministros_informe_salida = request.session['suministros_informe_salida']
        except :
            pass
        if suministros_informe_salida != None:
            apus_informe_salida = None
            try:
                apus_informe_salida = request.session['apus_informe_salida']
            except :
                pass
            if apus_informe_salida == None:
                apus_informe_salida = []

            if len(apus_informe_salida) == 0:
                for suministro_informe_salida in suministros_informe_salida:
                    if suministro_informe_salida['id'] == suministro_id:
                        for apu_proyecto in suministro_informe_salida['apus_proyecto']:
                            apus_informe_salida.append({'id': apu_proyecto['id'], 'cantidad': apu_proyecto['cantidad']})

            #Se almacena la variable en la sesion
            request.session['apus_informe_salida'] = apus_informe_salida
            suministro_almacen = proyecto.suministroalmacen_set.get(id=suministro_id)
            criterio_apu = criterio_apu.strip()
            apus_proyecto = proyecto.lista_apus_contienen_suministro(suministro_id=suministro_almacen.suministro.id, criterio=criterio_apu)
            lista_apus_informe_salida = []
            for apu_proyecto in apus_proyecto:
                item_apu_informe_salida = {'apu': apu_proyecto, 'cantidad_suministro_apu_nuevo_informe': ''}
                for apu_informe_salida in apus_informe_salida:
                    if apu_informe_salida['id'] == apu_proyecto.id:
                        item_apu_informe_salida['cantidad_suministro_apu_nuevo_informe'] = apu_informe_salida['cantidad']
                lista_apus_informe_salida.append(item_apu_informe_salida)
            pag = Paginador(request, lista_apus_informe_salida, 20, pagina)
            render = render_to_string('ajax/apusproyectosearchinformesalidaadd.html', {'user': user, 'suministro_almacen': suministro_almacen, 'apus': pag, 'criterio_apu': criterio_apu, 'criterio_suministro': criterio_suministro, 'pagina_suministro': pagina_suministro, 'proyecto': proyecto})
            dajax.assign('#light','innerHTML', render)
            dajax.script("document.getElementById('fade').style.display='block';")
            dajax.script("document.getElementById('light').style.display='block';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_cantidad_apu_proyecto_informe_salida2(request, pagina, suministro_id, apu_proyecto_id, cantidad, criterio_apu, criterio_suministro, pagina_suministro, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros_informe_salida = None
        apus_informe_salida = None
        try:
            suministros_informe_salida = request.session['suministros_informe_salida']
            apus_informe_salida = request.session['apus_informe_salida']
        except :
            pass
        if suministros_informe_salida != None and apus_informe_salida != None:
            error_cantidad = validar_cadena(cantidad)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float_digitos(cantidad)
                if error_cantidad == '':
                    error_cantidad = validar_cantidad_float(cantidad)
                    if error_cantidad == '':
                        cantidad = float(cantidad)
                        error_cantidad = validar_cantidad_float_0(cantidad)
                        if error_cantidad == '':
                            suministro = SuministroAlmacen.objects.get(id=suministro_id)
                            #Verificar si la cantidad a registrar esta disponible
                            cantidad_disponible = suministro.cantidad_actual
                            for apu_informe_salida in apus_informe_salida:
                                if apu_informe_salida['id'] != apu_proyecto_id:
                                    cantidad_disponible = round(cantidad_disponible - apu_informe_salida['cantidad'], 2)
                            cantidad_disponible = round(cantidad_disponible - cantidad, 2)
                            if cantidad_disponible >= 0:
                                existe_apu_proyecto = False
                                for apu_informe_salida in apus_informe_salida:
                                    if apu_informe_salida['id'] == apu_proyecto_id:
                                        apu_informe_salida['cantidad'] = cantidad
                                        existe_apu_proyecto = True
                                if existe_apu_proyecto == False:
                                    apu_informe_salida = {'id': apu_proyecto_id, 'cantidad': cantidad}
                                    apus_informe_salida.append(apu_informe_salida)
                            else:
                                error_cantidad = 'La cantidad no debe ser mayor a la cantidad actual en almacen'
                        else:
                            if cantidad == 0:
                                error_cantidad = ''
                                for apu_informe_salida in apus_informe_salida:
                                    if apu_informe_salida['id'] == apu_proyecto_id:
                                        apus_informe_salida.remove(apu_informe_salida)
            request.session['apus_informe_salida'] = apus_informe_salida
            error = {}
            if error_cantidad != '':
                error = {'id': apu_proyecto_id, 'value': cantidad, 'error': error_cantidad}
            suministro_almacen = proyecto.suministroalmacen_set.get(id=suministro_id)
            criterio_apu = criterio_apu.strip()
            apus_proyecto = proyecto.lista_apus_contienen_suministro(suministro_id=suministro_almacen.suministro.id, criterio=criterio_apu)
            lista_apus_informe_salida = []
            for apu_proyecto in apus_proyecto:
                item_apu_informe_salida = {'apu': apu_proyecto, 'cantidad_suministro_apu_nuevo_informe': ''}
                for apu_informe_salida in apus_informe_salida:
                    if apu_informe_salida['id'] == apu_proyecto.id:
                        item_apu_informe_salida['cantidad_suministro_apu_nuevo_informe'] = apu_informe_salida['cantidad']
                lista_apus_informe_salida.append(item_apu_informe_salida)
            pag = Paginador(request, lista_apus_informe_salida, 20, pagina)
            render = render_to_string('ajax/apusproyectosearchinformesalidaadd.html', {'user': user, 'suministro_almacen': suministro_almacen, 'apus': pag, 'criterio_apu': criterio_apu, 'criterio_suministro': criterio_suministro, 'pagina_suministro': pagina_suministro, 'proyecto': proyecto, 'error': error})
            dajax.assign('#light','innerHTML', render)
            if error_cantidad != '':
                dajax.script("document.getElementById('id_text_cantidad_"+str(apu_proyecto_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_cantidad_apu_proyecto_informe_salida2(request, pagina, suministro_id, apu_proyecto_id, criterio_apu, criterio_suministro, pagina_suministro, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros_informe_salida = None
        apus_informe_salida = None
        try:
            suministros_informe_salida = request.session['suministros_informe_salida']
            apus_informe_salida = request.session['apus_informe_salida']
        except :
            pass
        if suministros_informe_salida != None and apus_informe_salida != None:
            for apu_informe_salida in apus_informe_salida:
                if apu_informe_salida['id'] == apu_proyecto_id:
                    error = {'id': apu_proyecto_id, 'value': apu_informe_salida['cantidad'], 'error': ''}
            suministro_almacen = proyecto.suministroalmacen_set.get(id=suministro_id)
            criterio_apu = criterio_apu.strip()
            apus_proyecto = proyecto.lista_apus_contienen_suministro(suministro_id=suministro_almacen.suministro.id, criterio=criterio_apu)
            lista_apus_informe_salida = []
            for apu_proyecto in apus_proyecto:
                item_apu_informe_salida = {'apu': apu_proyecto, 'cantidad_suministro_apu_nuevo_informe': ''}
                for apu_informe_salida in apus_informe_salida:
                    if apu_informe_salida['id'] == apu_proyecto.id:
                        item_apu_informe_salida['cantidad_suministro_apu_nuevo_informe'] = apu_informe_salida['cantidad']
                lista_apus_informe_salida.append(item_apu_informe_salida)
            pag = Paginador(request, lista_apus_informe_salida, 20, pagina)
            render = render_to_string('ajax/apusproyectosearchinformesalidaadd.html', {'user': user, 'suministro_almacen': suministro_almacen, 'apus': pag, 'criterio_apu': criterio_apu, 'criterio_suministro': criterio_suministro, 'pagina_suministro': pagina_suministro, 'proyecto': proyecto, 'error': error})
            dajax.assign('#light','innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_"+str(apu_proyecto_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_suministro_informe_salida2(request, pagina, suministro_id, criterio_suministro, pagina_suministro, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros_informe_salida = None
        try:
            suministros_informe_salida = request.session['suministros_informe_salida']
        except :
            pass
        if suministros_informe_salida != None:
            apus_informe_salida = request.session['apus_informe_salida']

            existe_suministro = False
            for suministro_informe_salida in suministros_informe_salida:
                if suministro_informe_salida['id'] == suministro_id:
                    existe_suministro = True
                    #Si no hay APU's registrados con cantidades se elimina el suministro del informe de salida
                    if len(apus_informe_salida) == 0:
                        suministros_informe_salida.remove(suministro_informe_salida)
                    else:
                        #Se actualiza el suministro existente
                        cantidad = 0
                        for apu_informe_salida in apus_informe_salida:
                            cantidad = cantidad + apu_informe_salida['cantidad']
                        suministro_informe_salida['apus_proyecto'] = apus_informe_salida
                        suministro_informe_salida['cantidad'] = cantidad
            if existe_suministro == False:
                if len(apus_informe_salida) > 0:
                    #Se actualiza la lista de suministros con el nuevo suministro
                    cantidad = 0
                    for apu_informe_salida in apus_informe_salida:
                        cantidad = cantidad + apu_informe_salida['cantidad']
                    suministros_informe_salida.append({'id': suministro_id, 'apus_proyecto': apus_informe_salida, 'cantidad': cantidad})

            del request.session['apus_informe_salida']
            request.session['suministros_informe_salida'] = suministros_informe_salida

            suministros = proyecto.suministroalmacen_set.all().order_by('suministro__nombre')

            criterio_suministro = criterio_suministro.strip()
            if criterio_suministro != '':
                suministros = suministros.filter(Q(suministro__nombre__icontains=criterio_suministro) | Q(suministro__sinonimos__icontains=criterio_suministro))
            suministros_almacen = []
            for suministro in suministros:
                suministro_almacen = {'suministro': suministro, 'cantidad_nuevo_informe': ''}
                for suministro_informe_salida in suministros_informe_salida:
                    if suministro_informe_salida['id'] == suministro.id:
                        suministro_almacen['cantidad_nuevo_informe'] = suministro_informe_salida['cantidad']
                suministros_almacen.append(suministro_almacen)
            pag = Paginador(request, suministros_almacen, 20, pagina_suministro)
            render = render_to_string('ajax/suministrosalmacensearchinformesalida.html', {'user': user, 'suministros': pag, 'criterio_suministro': criterio_suministro, 'pagina_suministro': pagina_suministro, 'proyecto': proyecto})
            dajax.assign('#id_reporte_suministros','innerHTML', render)
            dajax.script("document.getElementById('fade').style.display='none';")
            dajax.script("document.getElementById('light').style.display='none';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def cancelar_agregar_suministro_informe_salida2(request, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros_informe_salida = None
        try:
            suministros_informe_salida = request.session['suministros_informe_salida']
        except :
            pass
        if suministros_informe_salida != None:
            del request.session['apus_informe_salida']
            dajax.script("document.getElementById('fade').style.display='none';")
            dajax.script("document.getElementById('light').style.display='none';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()



#Ordenes de servicio
##Cotización orden de servicio por suministro
###Cotizar_1 (Elección del suministro)
def suministro_orden_servicio_cotizar2(request, suministro_id, proyecto_id):
    import datetime
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        #if validar_permiso_usuario(user.id, 'auth.view_group'):
        suministro_comprar = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(suministro_id=suministro_id, tipo_cotizacion=2)[0]
        pag = Paginador(request, suministro_comprar.suministro.suministro.get_proveedores_activos_suministro(), 20, 1)

        now = datetime.datetime.now()
        fecha_actual = now.strftime("%Y-%m-%d")
        render = render_to_string('ajax/suministrocotizarproveedoressearch.html', {'user': user, 'suministro_proveedores': pag, 'suministro_comprar': suministro_comprar, 'proyecto': proyecto, 'fecha_actual': fecha_actual, } )
        dajax.assign('#light', 'innerHTML', render)
        dajax.script("document.getElementById('light').style.display='block';")
        dajax.script("document.getElementById('fade').style.display='block';")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


###Seleccionar un proveedor de la lista que provee el suministro seleccionado
def seleccionar_proveedor_lista_proveedores_suministro_cotizacion_orden_serivicio_add2(request, parametro, suministro_id, proveedor_id, pagina, criterio, proyecto_id):
    import datetime
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)

        criterio = criterio.strip()
        suministro_comprar = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(suministro_id=suministro_id, tipo_cotizacion=2)[0]
        pag = Paginador(request, suministro_comprar.suministro.suministro.get_proveedores_activos_suministro(criterio=criterio), 20, pagina)

        now = datetime.datetime.now()
        fecha_actual = now.strftime("%Y-%m-%d")
        error = {}
        if parametro == True:
            error = { 'id': proveedor_id, 'value': '', 'error': '' }
        render = render_to_string('ajax/suministrocotizarproveedoressearch.html', {'user': user, 'suministro_proveedores': pag, 'suministro_comprar': suministro_comprar, 'fecha_actual': fecha_actual, 'criterio_proveedor': criterio, 'proyecto': proyecto, 'error': error } )
        dajax.assign('#light', 'innerHTML', render)
        if parametro == True:
            dajax.script("document.getElementById('id_text_cantidad_" + str(proveedor_id) + "').focus();")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


###Cotizar_2 (Cotizar suministro según el proveedor seleccionado)
def cotizar_suministro_orden_servicio_proveedor2(request, suministro_id, proveedor_id, cantidad, pagina, criterio, proyecto_id):
    from django.db.models import Sum
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        cantidad = cantidad.strip()
        error_cantidad = validar_cadena(cantidad)
        if error_cantidad == '':
            error_cantidad = validar_cantidad_float(cantidad)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float_0(cantidad)
                if error_cantidad == '':
                    error_cantidad = validar_cantidad_float_digitos(cantidad)
                    if error_cantidad == '':
                        cantidad = float(cantidad)
                        suministro = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(suministro_id=suministro_id, tipo_cotizacion=2).pop()
                        if cantidad <= suministro.cantidad_requerida:
                            #suministro = Suministro.objects.get(id=suministro_id)
                            #if is_residuo_0(cantidad, suministro.unidad_embalaje):
                            persona = Usuario.objects.get(id=user.id)
                            cotizacion = Cotizacion()
                            cotizacion.tipo = 2
                            cotizacion.proyecto = proyecto
                            cotizacion.persona = persona
                            proveedor = Proveedor.objects.get(id=proveedor_id)
                            cotizacion.proveedor = proveedor
                            #Variable de la sesion
                            request.session['cotizacion'] = cotizacion
                            suministros_cotizacion = []
                            suministros_cotizacion.append({'suministro_id': suministro_id, 'cantidad': cantidad})
                            request.session['suministros_cotizacion'] = suministros_cotizacion

                            #Visualiza los suministros requeridos con la cantidad a cotizar
                            suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(proveedor_id=proveedor_id, tipo_cotizacion=2)
                            suministros_comprar = []
                            for suministro_requisiciones in suministros_requisiciones:
                                suministro_comprar = {'suministro': suministro_requisiciones, 'cantidad_nueva_cotizacion': ''}
                                if suministro_requisiciones.suministro.suministro.id == suministro_id:
                                    suministro_comprar['cantidad_nueva_cotizacion'] = cantidad
                                suministros_comprar.append(suministro_comprar)

                            pag = Paginador(request, suministros_comprar, 20, 1)
                            render = render_to_string('ajax/suministrosrequisicionesproveedorsearchordenservicioadd.html', {'user': user, 'suministros_requisiciones': pag, 'proveedor': proveedor, 'proyecto': proyecto } )
                            dajax.assign('#light', 'innerHTML', render)
                            #else:
                            #    error = 'La cantidad de este suministro que puede cotizar es: '+str(cantidad-(cantidad % suministro.unidad_embalaje))
                        else:
                            error_cantidad = 'La cantidad no debe ser mayor al total requerido'
        if error_cantidad != '':
            import datetime
            error = {'id': proveedor_id, 'value': cantidad, 'error': error_cantidad}
            suministro_comprar = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(suministro_id=suministro_id, tipo_cotizacion=2)[0]
            pag = Paginador(request, suministro_comprar.suministro.suministro.get_proveedores_activos_suministro(criterio=criterio), 20, pagina)
            now = datetime.datetime.now()
            fecha_actual = now.strftime("%Y-%m-%d")
            render = render_to_string('ajax/suministrocotizarproveedoressearch.html', {'user': user, 'suministro_proveedores': pag, 'criterio_proveedor': criterio, 'suministro_comprar': suministro_comprar, 'proyecto': proyecto, 'fecha_actual': fecha_actual, 'error': error})
            dajax.assign('#light', 'innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_"+str(proveedor_id)+"').select();")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


###Cotizar_3 (Anadir un suministro a la cotización)
def anadir_suministro_cotizacion_orden_servicio2(request, pagina, suministro_id, proveedor_id, criterio, proyecto_id, cantidad):
    from django.db.models import Sum
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        #Validacion de variables de session
        suministros_cotizacion = None
        try:
            suministros_cotizacion = request.session['suministros_cotizacion']
        except :
            pass
        if suministros_cotizacion != None:
            cantidad = cantidad.strip()
            error_cantidad = validar_cadena(cantidad)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float_digitos(cantidad)
                if error_cantidad == '':
                    error_cantidad = validar_cantidad_float(cantidad)
                    if error_cantidad == '':
                        cantidad = float(cantidad)
                        error_cantidad = validar_cantidad_float_0(cantidad)
                        if error_cantidad == '':
                            suministro = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(suministro_id=suministro_id, tipo_cotizacion=2).pop()
                            if cantidad <= suministro.cantidad_requerida:
                                #suministro = Suministro.objects.get(id=suministro_id)
                                #if is_residuo_0(cantidad, suministro.unidad_embalaje):
                                existe_suministro = False
                                for suministro_cotizacion in suministros_cotizacion:
                                    if suministro_cotizacion['suministro_id'] == suministro_id:
                                        suministro_cotizacion['cantidad'] = cantidad
                                        existe_suministro = True
                                if existe_suministro == False:
                                    suministros_cotizacion.append({'suministro_id': suministro_id, 'cantidad': cantidad})
                                request.session['suministros_cotizacion'] = suministros_cotizacion
                            else:
                                error_cantidad = 'La cantidad no debe ser mayor al total requerido'
                        else:
                            if cantidad == 0:
                                error_cantidad = ''
                                for suministro_cotizacion in suministros_cotizacion:
                                    if suministro_cotizacion['suministro_id'] == suministro_id:
                                        suministros_cotizacion.remove(suministro_cotizacion)
                                request.session['suministros_cotizacion'] = suministros_cotizacion
            error = {}
            if error_cantidad != '':
                error = { 'id': suministro_id, 'value': cantidad, 'error': error_cantidad }
            proveedor = Proveedor.objects.get(id=proveedor_id)
            criterio = criterio.strip()

            #Visualiza los suministros requeridos con la cantidad a cotizar
            suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(criterio=criterio, proveedor_id=proveedor_id, tipo_cotizacion=2)
            suministros_comprar = []
            for suministro_requisiciones in suministros_requisiciones:
                suministro_comprar = {'suministro': suministro_requisiciones, 'cantidad_nueva_cotizacion': ''}
                for suministro_cotizacion in suministros_cotizacion:
                    if suministro_requisiciones.suministro.suministro.id == suministro_cotizacion['suministro_id']:
                        suministro_comprar['cantidad_nueva_cotizacion'] = suministro_cotizacion['cantidad']
                suministros_comprar.append(suministro_comprar)

            pag = Paginador(request, suministros_comprar, 20, pagina)

            render = render_to_string('ajax/suministrosrequisicionesproveedorsearchordenservicioadd.html', {'user': user, 'suministros_requisiciones': pag, 'criterio': criterio, 'proveedor': proveedor, 'proyecto': proyecto, 'error': error } )
            dajax.assign('#light', 'innerHTML', render)

            if error_cantidad != '':
                dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


###Cotizar todos los suministros
def cotizar_todos_suministros_proveedor_orden_servicio_add2(request, proveedor_id, proyecto_id):
    from django.db.models import Sum
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        #Validación de variables de session
        suministros_cotizacion = None
        try:
            suministros_cotizacion = request.session['suministros_cotizacion']
        except :
            pass

        if suministros_cotizacion != None:
            proveedor = Proveedor.objects.get(id=proveedor_id)

            #Visualiza los suministros requeridos con la cantidad a cotizar
            suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(proveedor_id=proveedor_id, tipo_cotizacion=2)
            suministros_comprar = []
            for suministro_requisiciones in suministros_requisiciones:
                suministro_comprar = {'suministro': suministro_requisiciones, 'cantidad_nueva_cotizacion': ''}
                for suministro_cotizacion in suministros_cotizacion:
                    if suministro_requisiciones.suministro.suministro.id == suministro_cotizacion['suministro_id']:
                        suministro_comprar['cantidad_nueva_cotizacion'] = suministro_cotizacion['cantidad']
                suministros_comprar.append(suministro_comprar)

            #Calcula las cantidades maximas a cotizar
            for suministro_comprar in suministros_comprar:
                if suministro_comprar['cantidad_nueva_cotizacion'] == '':
                    suministro = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(suministro_id=suministro_comprar['suministro'].suministro.suministro.id, tipo_cotizacion=2).pop()
                    if suministro.cantidad_requerida > 0:
                        cantidad_comprar = suministro.cantidad_requerida
                        suministro_comprar['cantidad_nueva_cotizacion'] = str(cantidad_comprar)
                        suministros_cotizacion.append({'suministro_id': suministro_comprar['suministro'].suministro.suministro.id, 'cantidad': cantidad_comprar})
            pag = Paginador(request, suministros_comprar, 20, 1)
            render = render_to_string('ajax/suministrosrequisicionesproveedorsearchordenservicioadd.html', {'user': user, 'suministros_requisiciones': pag, 'proveedor': proveedor, 'proyecto': proyecto } )
            dajax.assign('#light', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


###Activar input para modificar una cantidad de un suministro de la catización
def activar_input_cantidad_suministro_cotizacion_orden_servicio_add2(request, pagina, suministro_id, proveedor_id, criterio, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        #Validacion de variables de session
        suministros_cotizacion = None
        try:
            suministros_cotizacion = request.session['suministros_cotizacion']
        except :
            pass
        if suministros_cotizacion != None:
            proveedor = Proveedor.objects.get(id=proveedor_id)
            criterio = criterio.strip()

            #Visualiza los suministros requeridos con la cantidad a cotizar
            suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(criterio=criterio, proveedor_id=proveedor_id, tipo_cotizacion=2)
            suministros_comprar = []

            error = {}
            for suministro_requisiciones in suministros_requisiciones:
                suministro_comprar = {'suministro': suministro_requisiciones, 'cantidad_nueva_cotizacion': ''}
                for suministro_cotizacion in suministros_cotizacion:
                    if suministro_requisiciones.suministro.suministro.id == suministro_cotizacion['suministro_id']:
                        suministro_comprar['cantidad_nueva_cotizacion'] = suministro_cotizacion['cantidad']
                        if suministro_cotizacion['suministro_id'] == suministro_id:
                            error = { 'id': suministro_id, 'value': suministro_cotizacion['cantidad'], 'error': '' }
                suministros_comprar.append(suministro_comprar)
            pag = Paginador(request, suministros_comprar, 20, pagina)
            render = render_to_string('ajax/suministrosrequisicionesproveedorsearchordenservicioadd.html', {'user': user, 'suministros_requisiciones': pag, 'criterio': criterio, 'proveedor': proveedor, 'proyecto': proyecto, 'error': error } )
            dajax.assign('#light', 'innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_cantidad_suministro_cotizacion_realizar_orden_servicio2(request, pagina, suministro_id, cotizacion_id, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        cotizacion = None
        try:
            cotizacion = proyecto.cotizacion_set.get(id=cotizacion_id)
        except :
            pass
        if cotizacion != None:
            suministros = cotizacion.suministrocotizacion_set.all()
            pag = Paginador(request, suministros, 20, pagina)
            suministro = cotizacion.suministrocotizacion_set.get(id=suministro_id)
            error = { 'id': suministro_id, 'item': 'cantidad', 'value': suministro.cantidad_cotizada, 'error': '' }
            render = render_to_string('ajax/suministroscotizacionordenserviciosearch.html', {'user': user, 'suministros': pag, 'cotizacion': cotizacion, 'proyecto': proyecto, 'error': error })
            dajax.assign('#id_reporte_suministros', 'innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def orden_servicio_suministros_proveedor2(request, proveedor_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        usuario = Usuario.objects.get(id=user.id)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        proveedor = Proveedor.objects.get(id=proveedor_id)
        cotizacion = Cotizacion()
        cotizacion.tipo = 2
        cotizacion.proyecto = proyecto
        cotizacion.proveedor = proveedor
        cotizacion.persona = usuario
        #Variable de la sesion
        request.session['cotizacion'] = cotizacion
        request.session['suministros_cotizacion'] = []

        #Visualiza los suministros requeridos con la cantidad a cotizar
        suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(proveedor_id=proveedor_id, tipo_cotizacion=2)
        suministros_comprar = []
        for suministro_requisiciones in suministros_requisiciones:
            suministro_comprar = {'suministro': suministro_requisiciones, 'cantidad_nueva_cotizacion': ''}
            suministros_comprar.append(suministro_comprar)

        pag = Paginador(request, suministros_comprar, 20, 1)
        render = render_to_string('ajax/suministrosrequisicionesproveedorsearchordenservicioadd.html', {'user': user, 'suministros_requisiciones': pag, 'proveedor': proveedor, 'proyecto': proyecto } )
        dajax.assign('#light', 'innerHTML', render)
        dajax.script("document.getElementById('light').style.display='block';")
        dajax.script("document.getElementById('fade').style.display='block';")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def realizar_cotizacion_orden_servicio_add2(request, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        #Validacion de variables de session
        suministros_cotizacion = None
        try:
            suministros_cotizacion = request.session['suministros_cotizacion']
        except :
            pass
        if suministros_cotizacion != None:
            cotizacion = request.session['cotizacion']
            if len(suministros_cotizacion) > 0:
                cantidades_correctas = True
                for suministro_cotizacion in suministros_cotizacion:
                    suministros = SuministroRequisicion.objects.filter(suministro__suministro__id=suministro_cotizacion['suministro_id'], requisicion__proyecto=proyecto)
                    cantidad_total_requerida = suministros.__getitem__(0).cantidad_total_requerida_proyecto()
                    cantidad = float(suministro_cotizacion['cantidad'])
                    if cantidad > cantidad_total_requerida:
                        cantidades_correctas = False
                if cantidades_correctas:
                    cotizacion.save()
                    for suministro_cotizacion in suministros_cotizacion:
                        suministro = Suministro.objects.get(id=suministro_cotizacion['suministro_id'])
                        nuevo_suministro_cotizacion = SuministroCotizacion()
                        nuevo_suministro_cotizacion.cantidad_cotizada = suministro_cotizacion['cantidad']
                        nuevo_suministro_cotizacion.suministro = suministro
                        nuevo_suministro_cotizacion.cotizacion = cotizacion
                        nuevo_suministro_cotizacion.save()
                    del request.session['cotizacion']
                    del request.session['suministros_cotizacion']
                    dajax.alert('Se ha realizado la cotizacion')
                    dajax.redirect('/inverboy/home/cotizacionesproyectodetails/'+str(cotizacion.id)+'/'+str(proyecto_id))
                else:
                    dajax.alert(u'Verifique que las cantidades de la cotización no sean mayores que las cantidades requeridas')
                    dajax.script("document.getElementById('id_guardar').disabled = false;")
            else:
                dajax.alert(u'No hay suministros en la cotización')
                dajax.script("document.getElementById('id_guardar').disabled = false;")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def cancelar_cotizacion_orden_servicio_add2(request, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        #Validacion de variables de session
        suministros_cotizacion = None
        try:
            suministros_cotizacion = request.session['suministros_cotizacion']
        except :
            pass
        if suministros_cotizacion != None:
            del request.session['cotizacion']
            del request.session['suministros_cotizacion']
            dajax.script("document.getElementById('light').style.display='none';")
            dajax.script("document.getElementById('fade').style.display='none';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_cantidad_suministro_orden_servicio_change2(request, pagina, suministro_id, orden_servicio_id, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
            # Verifica que se pueda modificar la orden de servicio
            if orden_servicio.permite_modificaciones():
                for suministro in suministros:
                    if suministro['suministro'].id == suministro_id:
                        error = {'id': suministro_id, 'item': 'cantidad', 'value': suministro['cantidad'], 'error': ''}
                pag = Paginador(request, suministros, 20, pagina)
                render = render_to_string('ajax/suministrosordenserviciochange.html', {'user': user, 'suministros': pag, 'orden_servicio': orden_servicio, 'proyecto': proyecto, 'error': error})
                dajax.assign('#id_reporte_suministros', 'innerHTML', render)
                dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_cantidad_suministro_orden_servicio_change2(request, suministro_id, cantidad, orden_servicio_id, pagina, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
            # Verifica que se pueda modificar la orden de servicio
            if orden_servicio.permite_modificaciones():
                valores_discriminados = {'subtotal': 0, 'valor_iva': 0, 'valor_total': 0}
                cantidad = cantidad.strip()

                error_cantidad = ''
                validaciones = Validator().append([
                    Field('cantidad', cantidad).append([
                        IsRequired('Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
                    ]),
                ]).run(True).pop()

                if validaciones['passed'] == True:
                    cantidad = float(cantidad)
                    if cantidad > 0:
                        cantidad_requerida = None
                        try:
                            cantidad_requerida = SuministroRequisicion.objects.filter(requisicion__proyecto=proyecto, suministro__suministro__id=suministro_id, cantidad_comprada__lt=F('cantidad_requerida')).aggregate(Sum('cantidad_requerida'))['cantidad_requerida__sum'] - SuministroRequisicion.objects.filter(requisicion__proyecto=proyecto, suministro__suministro__id=suministro_id, cantidad_comprada__lt=F('cantidad_requerida')).aggregate(Sum('cantidad_comprada'))['cantidad_comprada__sum']
                        except :
                            pass
                        if cantidad_requerida == None:
                            cantidad_requerida = 0

                        cantidad_comprada_orden_actual = None
                        try:
                            cantidad_comprada_orden_actual = orden_servicio.suministroordenservicioitem_set.get(suministro__id=suministro_id).suministroordenservicio_set.aggregate(Sum('cantidad'))['cantidad__sum']
                        except :
                            pass
                        if cantidad_comprada_orden_actual == None:
                            cantidad_comprada_orden_actual = 0

                        cantidad_disponible = round(cantidad_requerida + cantidad_comprada_orden_actual, 2)
                        if cantidad <= cantidad_disponible:
                            cantidad_entregada_actual = None
                            try:
                                cantidad_entregada_actual = orden_servicio.suministroordenservicioitem_set.get(suministro__id=suministro_id).suministroordenservicio_set.aggregate(Sum('cantidad_entregada'))['cantidad_entregada__sum']
                            except :
                                pass
                            if cantidad_entregada_actual == None:
                                cantidad_entregada_actual
                            if cantidad >= cantidad_entregada_actual:
                                for suministro in suministros:
                                    if suministro['suministro'].id == suministro_id:
                                        suministro['cantidad'] = cantidad
                                    valores_discriminados['valor_total'] = round(valores_discriminados['valor_total'] + (suministro['cantidad'] * suministro['precio']), 2)
                                request.session['suministros'] = suministros
                            else:
                                error_cantidad = 'La cantidad no puede ser menor a la cantidad entregada del suministro'
                        else:
                            error_cantidad = 'La cantidad no puede ser mayor a la cantidad requerida en el proyecto'
                    else:
                        error_cantidad = 'La cantidad debe ser mayor a 0 (cero).'
                else:
                    for error in validaciones['errors']:
                        error_cantidad = error
                    
                error = {}
                if error_cantidad != '':
                    error = {'id': suministro_id, 'item': 'cantidad', 'value': cantidad, 'error': error_cantidad}
                pag = Paginador(request, suministros, 20, pagina)
                render = render_to_string('ajax/suministrosordenserviciochange.html', {'user': user, 'orden_servicio': orden_servicio, 'suministros': pag, 'valores_discriminados': valores_discriminados, 'proyecto': proyecto, 'error': error})
                dajax.assign('#id_reporte_suministros', 'innerHTML', render)
                if error_cantidad != '':
                    dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_precio_suministro_orden_servicio_change2(request, pagina, suministro_id, orden_servicio_id, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
            # Verifica que se pueda modificar la orden de servicio
            if orden_servicio.permite_modificaciones():
                for suministro in suministros:
                    if suministro['suministro'].id == suministro_id:
                        error = {'id': suministro_id, 'item': 'precio', 'value': suministro['precio'], 'error': ''}
                pag = Paginador(request, suministros, 20, pagina)
                render = render_to_string('ajax/suministrosordenserviciochange.html', {'user': user, 'suministros': pag, 'orden_servicio': orden_servicio, 'proyecto': proyecto, 'error': error})
                dajax.assign('#id_reporte_suministros', 'innerHTML', render)
                dajax.script("document.getElementById('id_text_precio_"+str(suministro_id)+"').select();")
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_precio_suministro_orden_servicio_change2(request, suministro_id, precio, orden_servicio_id, pagina, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
            # Verifica que se pueda modificar la orden de servicio
            if orden_servicio.permite_modificaciones():
                valores_discriminados = {'subtotal': 0, 'valor_iva': 0, 'valor_total': 0}
                precio = precio.strip()
                
                error_precio = ''
                validaciones = Validator().append([
                    Field('precio', precio).append([
                        IsRequired('Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
                    ]),
                ]).run(True).pop()

                if validaciones['passed'] == True:
                    precio = float(precio)
                    if precio > 0:
                        for suministro in suministros:
                            if suministro['suministro'].id == suministro_id:
                                suministro['precio'] = precio
                            valores_discriminados['valor_total'] = round(valores_discriminados['valor_total'] + (suministro['cantidad'] * suministro['precio']), 2)
                        request.session['suministros'] = suministros
                    else:
                        error_precio = 'La cantidad debe ser mayor a 0 (cero).'
                else:
                    for error in validaciones['errors']:
                        error_precio = error
                error = {}
                if error_precio != '':
                    error = {'id': suministro_id, 'item': 'precio', 'value': precio, 'error': error_precio}
                pag = Paginador(request, suministros, 20, pagina)
                render = render_to_string('ajax/suministrosordenserviciochange.html', {'user': user, 'orden_servicio': orden_servicio, 'suministros': pag, 'valores_discriminados': valores_discriminados, 'proyecto': proyecto, 'error': error})
                dajax.assign('#id_reporte_suministros', 'innerHTML', render)
                if error_precio != '':
                    dajax.script("document.getElementById('id_text_precio_"+str(suministro_id)+"').select();")
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_observaciones_suministro_orden_servicio_change2(request, pagina, suministro_id, orden_servicio_id, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
            # Verifica que se pueda modificar la orden de servicio
            if orden_servicio.permite_modificaciones():
                valores_discriminados = {'subtotal': 0, 'valor_iva': 0, 'valor_total': 0}

                error = {}
                for suministro in suministros:
                    if suministro['suministro'].id == suministro_id:
                        error = {'id': suministro_id, 'item': 'observaciones', 'value': suministro['observaciones'], 'error': ''}
                    valores_discriminados['valor_total'] = round(valores_discriminados['valor_total'] + (suministro['cantidad'] * suministro['precio']), 2)
                    
                pag = Paginador(request, suministros, 20, pagina)
                render = render_to_string('ajax/suministrosordenserviciochange.html', {'user': user, 'orden_servicio': orden_servicio, 'suministros': pag, 'valores_discriminados': valores_discriminados, 'proyecto': proyecto, 'error': error})
                dajax.assign('#id_reporte_suministros', 'innerHTML', render)
                dajax.script("document.getElementById('id_text_observaciones_"+str(suministro_id)+"').select();")
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_observaciones_suministro_orden_servicio_change2(request, suministro_id, observaciones, orden_servicio_id, pagina, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
            # Verifica que se pueda modificar la orden de servicio
            if orden_servicio.permite_modificaciones():
                valores_discriminados = {'subtotal': 0, 'valor_iva': 0, 'valor_total': 0}

                observaciones = observaciones.strip()
                for suministro in suministros:
                    if suministro['suministro'].id == suministro_id:
                        suministro['observaciones'] = observaciones
                    valores_discriminados['valor_total'] = round(valores_discriminados['valor_total'] + (suministro['cantidad'] * suministro['precio']), 2)
                request.session['suministros'] = suministros
                error = {}
                pag = Paginador(request, suministros, 20, pagina)
                render = render_to_string('ajax/suministrosordenserviciochange.html', {'user': user, 'orden_servicio': orden_servicio, 'suministros': pag, 'valores_discriminados': valores_discriminados, 'proyecto': proyecto, 'error': error})
                dajax.assign('#id_reporte_suministros', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def suministros_proveedor_orden_servicio_change2(request, orden_servicio_id, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
            # Verifica que se pueda modificar la orden de servicio
            if orden_servicio.permite_modificaciones():
                suministros_agregar = None
                try:
                    suministros_agregar = request.session['suministros_agregar']
                except :
                    suministros_agregar = []
                    request.session['suministros_agregar'] = suministros_agregar
                ids_suministros_excluir = []
                for suministro in suministros:
                    ids_suministros_excluir.append(suministro['suministro'].id)

                #Visualiza los suministros requeridos con la cantidad a cotizar
                if criterio != None:
                    criterio = criterio.strip()
                else:
                    criterio = ''
                suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(criterio=criterio, proveedor_id=orden_servicio.proveedor.id, tipo_cotizacion=2, exclude_suministros_id=ids_suministros_excluir)
                suministros_comprar = []
                for suministro_requisiciones in suministros_requisiciones:
                    suministro_orden_servicio_item = None
                    try:
                        suministro_orden_servicio_item = orden_servicio.suministroordenservicioitem_set.get(suministro=suministro_requisiciones.suministro.suministro)
                    except :
                        pass
                    if suministro_orden_servicio_item != None:
                        suministro_requisiciones.cantidad_requerida = round(suministro_requisiciones.cantidad_requerida + suministro_orden_servicio_item.suministroordenservicio_set.aggregate(Sum('cantidad'))['cantidad__sum'], 2)
                    suministro_comprar = {'suministro': suministro_requisiciones, 'cantidad': '', 'precio': '', 'iva_suministro': '', 'observaciones': suministro_requisiciones.observaciones}
                    for suministro_agregar in suministros_agregar:
                        if suministro_requisiciones.suministro.suministro.id == suministro_agregar['suministro'].id:
                            suministro_comprar['cantidad'] = suministro_agregar['cantidad']
                            suministro_comprar['precio'] = suministro_agregar['precio']
                            suministro_comprar['observaciones'] = suministro_agregar['observaciones']
                    suministros_comprar.append(suministro_comprar)

                pag = Paginador(request, suministros_comprar, 20, 1)
                render = render_to_string('ajax/suministrosrequisicionesproveedorsearchordenserviciochange.html', {'user': user, 'suministros_requisiciones': pag, 'orden_servicio': orden_servicio, 'criterio': criterio, 'proyecto': proyecto} )
                dajax.assign('#light', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='block';")
                dajax.script("document.getElementById('fade').style.display='block';")
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def anadir_suministro_orden_servicio_change2(request, pagina, suministro_id, cantidad, precio, observaciones, orden_servicio_id, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        suministros_agregar = None
        try:
            suministros = request.session['suministros']
            suministros_agregar = request.session['suministros_agregar']
        except :
            pass
        if suministros != None and suministros_agregar != None:
            orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
            cantidad = cantidad.strip()
            precio = precio.strip()
            observaciones = observaciones.strip()

            error_cantidad = ''
            validaciones_cantidad = Validator().append([
                Field('cantidad', cantidad).append([
                    IsRequired('Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
                ]),
            ]).run(True).pop()

            error_precio = ''
            validaciones_precio = Validator().append([
                Field('precio', precio).append([
                    IsRequired('Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
                ]),
            ]).run(True).pop()

            if validaciones_cantidad['passed'] == True and validaciones_precio['passed'] == True:
                cantidad = float(cantidad)
                precio = float(precio)
                if cantidad > 0:
                    suministro_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(proveedor_id=orden_servicio.proveedor_id, tipo_cotizacion=2, suministro_id=suministro_id).pop()
                    suministro_orden_servicio_item = None
                    try:
                        suministro_orden_servicio_item = orden_servicio.suministroordenservicioitem_set.get(suministro=suministro_requisiciones.suministro.suministro)
                    except :
                        pass
                    if suministro_orden_servicio_item != None:
                        suministro_requisiciones.cantidad_requerida = round(suministro_requisiciones.cantidad_requerida + suministro_orden_servicio_item.suministroordenservicio_set.aggregate(Sum('cantidad'))['cantidad__sum'], 2)

                    if cantidad <= suministro_requisiciones.cantidad_requerida:
                        existe_suministro = False
                        for suministro_agregar in suministros_agregar:
                            if suministro_agregar['suministro'].id == suministro_id:
                                suministro_agregar['cantidad'] = cantidad
                                suministro_agregar['precio'] = precio
                                suministro_agregar['observaciones'] = observaciones
                                existe_suministro = True
                        if existe_suministro == False:
                            suministros_agregar.append({'suministro': suministro_requisiciones.suministro.suministro, 'cantidad': cantidad, 'precio': precio, 'observaciones': observaciones})
                    else:
                        error_cantidad = 'La cantidad no debe ser mayor al total requerido'
                else:
                    error_cantidad = ''
                    error_precio = ''
                    for suministro_agregar in suministros_agregar:
                        if suministro_agregar['suministro'].id == suministro_id:
                            suministros_agregar.remove(suministro_agregar)

                request.session['suministros_agregar'] = suministros_agregar
            else:
                if validaciones_cantidad['passed'] == False:
                    for error in validaciones_cantidad['errors']:
                        error_cantidad = error

                if validaciones_precio['passed'] == False:
                    for error in validaciones_precio['errors']:
                        error_precio = error
            error = {}
            if error_cantidad != '' or error_precio != '':
                error = {'id': suministro_id, 'value': cantidad, 'error': error_cantidad, 'value_precio': precio, 'error_precio': error_precio, 'value_observaciones': observaciones}

            criterio = criterio.strip()
            ids_suministros_excluir = []
            for suministro in suministros:
                ids_suministros_excluir.append(suministro['suministro'].id)

            #Visualiza los suministros requeridos con la cantidad a cotizar
            suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(criterio=criterio, proveedor_id=orden_servicio.proveedor.id, tipo_cotizacion=2, exclude_suministros_id=ids_suministros_excluir)
            suministros_comprar = []
            for suministro_requisiciones in suministros_requisiciones:
                suministro_orden_servicio_item = None
                try:
                    suministro_orden_servicio_item = orden_servicio.suministroordenservicioitem_set.get(suministro=suministro_requisiciones.suministro.suministro)
                except :
                    pass
                if suministro_orden_servicio_item != None:
                    suministro_requisiciones.cantidad_requerida = round(suministro_requisiciones.cantidad_requerida + suministro_orden_servicio_item.suministroordenservicio_set.aggregate(Sum('cantidad'))['cantidad__sum'], 2)
                suministro_comprar = {'suministro': suministro_requisiciones, 'cantidad': '', 'precio': '', 'observaciones': suministro_requisiciones.observaciones}
                for suministro_agregar in suministros_agregar:
                    if suministro_requisiciones.suministro.suministro.id == suministro_agregar['suministro'].id:
                        suministro_comprar['cantidad'] = suministro_agregar['cantidad']
                        suministro_comprar['precio'] = suministro_agregar['precio']
                        suministro_comprar['observaciones'] = suministro_agregar['observaciones']
                suministros_comprar.append(suministro_comprar)

            pag = Paginador(request, suministros_comprar, 20, pagina)
            render = render_to_string('ajax/suministrosrequisicionesproveedorsearchordenserviciochange.html', {'user': user, 'suministros_requisiciones': pag, 'orden_servicio': orden_servicio, 'criterio': criterio, 'error': error, 'proyecto': proyecto})
            dajax.assign('#light', 'innerHTML', render)
            if error_cantidad != '':
                dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
            elif error_precio != '':
                dajax.script("document.getElementById('id_text_precio_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_suministro_agregar_orden_servicio_change2(request, pagina, suministro_id, orden_servicio_id, criterio, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        suministros_agregar = None
        try:
            suministros = request.session['suministros']
            suministros_agregar = request.session['suministros_agregar']
        except :
            pass
        if suministros != None and suministros_agregar != None:
            orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)

            error = {}
            for suministro_agregar in suministros_agregar:
                if suministro_agregar['suministro'].id == suministro_id:
                    error = {'id': suministro_id, 'value': suministro_agregar['cantidad'], 'error': '', 'value_precio': suministro_agregar['precio'], 'error_precio': '', 'value_observaciones': suministro_agregar['observaciones']}

            criterio = criterio.strip()

            ids_suministros_excluir = []
            for suministro in suministros:
                ids_suministros_excluir.append(suministro['suministro'].id)

            #Visualiza los suministros requeridos con la cantidad a cotizar
            suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(criterio=criterio, proveedor_id=orden_servicio.proveedor.id, tipo_cotizacion=2, exclude_suministros_id=ids_suministros_excluir)
            suministros_comprar = []
            for suministro_requisiciones in suministros_requisiciones:
                suministro_orden_servicio_item = None
                try:
                    suministro_orden_servicio_item = orden_servicio.suministroordenservicioitem_set.get(suministro=suministro_requisiciones.suministro.suministro)
                except :
                    pass
                if suministro_orden_servicio_item != None:
                    suministro_requisiciones.cantidad_requerida = round(suministro_requisiciones.cantidad_requerida + suministro_orden_servicio_item.suministroordenservicio_set.aggregate(Sum('cantidad'))['cantidad__sum'], 2)
                suministro_comprar = {'suministro': suministro_requisiciones, 'cantidad': '', 'precio': '', 'observaciones': suministro_requisiciones.observaciones}
                for suministro_agregar in suministros_agregar:
                    if suministro_requisiciones.suministro.suministro.id == suministro_agregar['suministro'].id:
                        suministro_comprar['cantidad'] = suministro_agregar['cantidad']
                        suministro_comprar['precio'] = suministro_agregar['precio']
                        suministro_comprar['observaciones'] = suministro_agregar['observaciones']
                suministros_comprar.append(suministro_comprar)

            pag = Paginador(request, suministros_comprar, 20, pagina)
            render = render_to_string('ajax/suministrosrequisicionesproveedorsearchordenserviciochange.html', {'user': user, 'suministros_requisiciones': pag, 'orden_servicio': orden_servicio, 'criterio': criterio, 'error': error, 'proyecto': proyecto})
            dajax.assign('#light', 'innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def anadir_suministros_orden_servicio_change2(request, orden_servicio_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        suministros_agregar = None
        try:
            suministros = request.session['suministros']
            suministros_agregar = request.session['suministros_agregar']
        except :
            pass
        if suministros != None and suministros_agregar != None:
            orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)

            cantidades_disponibles = True
            # Validar que esten disponibles las cantidades
            for suministro_agregar in suministros_agregar:
                suministro_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(proveedor_id=orden_servicio.proveedor.id, tipo_cotizacion=2, suministro_id=suministro_agregar['suministro'].id).pop()
                suministro_orden_servicio_item = None
                try:
                    suministro_orden_servicio_item = orden_servicio.suministroordenservicioitem_set.get(suministro=suministro_requisiciones.suministro.suministro)
                except :
                    pass
                if suministro_orden_servicio_item != None:
                    suministro_requisiciones.cantidad_requerida = round(suministro_requisiciones.cantidad_requerida + suministro_orden_servicio_item.suministroordenservicio_set.aggregate(Sum('cantidad'))['cantidad__sum'], 2)
                if suministro_agregar['cantidad'] <= suministro_requisiciones.cantidad_requerida:
                    suministros.append(suministro_agregar)
                else:
                    cantidades_disponibles = False

            # Elimina las variables de session
            del request.session['suministros_agregar']

            valores_discriminados = {'subtotal': 0, 'valor_iva': 0, 'valor_total': 0}
            for suministro in suministros:
                valores_discriminados['valor_total'] = round(valores_discriminados['valor_total'] + (suministro['cantidad'] * suministro['precio']), 2)
                
            pag = Paginador(request, suministros, 20, 1)
            render = render_to_string('ajax/suministrosordenserviciochange.html', {'user': user, 'orden_servicio': orden_servicio, 'suministros': pag, 'valores_discriminados': valores_discriminados, 'proyecto': proyecto})
            dajax.assign('#id_reporte_suministros', 'innerHTML', render)
            if cantidades_disponibles == False:
                dajax.alert('No se han agregado algunos suministros por la disponibilidad en las cantidades en requisiciones')
            dajax.script("document.getElementById('light').style.display='none';")
            dajax.script("document.getElementById('fade').style.display='none';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def cancelar_anadir_suministros_orden_servicio_change2(request, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        suministros_agregar = None
        try:
            suministros = request.session['suministros']
            suministros_agregar = request.session['suministros_agregar']
        except :
            pass
        if suministros != None and suministros_agregar != None:
            del request.session['suministros_agregar']
            dajax.script("document.getElementById('light').style.display='none';")
            dajax.script("document.getElementById('fade').style.display='none';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_suministro_orden_servicio2(request, suministro_id, orden_servicio_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'auth.view_group'):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
            # Verifica que se pueda modificar la orden de servicio
            if orden_servicio.permite_modificaciones():
                # Verifica que el suministro a eliminar no tenga cantidad en cortes diarios de obra
                item_orden_servicio = None
                error_eliminar_suministro = ''
                try:
                    item_orden_servicio = orden_servicio.suministroordenservicioitem_set.get(suministro__id=suministro_id)
                except :
                    pass
                if item_orden_servicio != None:
                    if item_orden_servicio.suministroordenservicio_set.all().aggregate(Sum('cantidad_entregada'))['cantidad_entregada__sum'] > 0:
                        error_eliminar_suministro = 'No es posible eliminar este suministro.'

                if error_eliminar_suministro == '':
                    valores_discriminados = {'subtotal': 0, 'valor_iva': 0, 'valor_total': 0}
                    for suministro in suministros:
                        if suministro['suministro'].id == suministro_id:
                            suministros.remove(suministro)
                        else:
                            valores_discriminados['valor_total'] = round(valores_discriminados['valor_total'] + (suministro['cantidad'] * suministro['precio']), 2)
                    pag = Paginador(request, suministros, 20, 1)
                    render = render_to_string('ajax/suministrosordenserviciochange.html', {'user': user, 'orden_servicio': orden_servicio, 'suministros': pag, 'valores_discriminados': valores_discriminados, 'proyecto': proyecto})
                    dajax.assign('#id_reporte_suministros', 'innerHTML', render)
                else:
                    dajax.alert(error_eliminar_suministro)
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def asignar_modificacion_orden_servicio2(request, permiso, orden_servicio_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.assignchangepermission_ordenservicio' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
            if orden_servicio.permite_modificar() == True:
                if permiso == 1:
                    orden_servicio.permiso_modificar = True
                elif permiso == 0:
                    orden_servicio.permiso_modificar = False
                orden_servicio.save()
                dajax.redirect('/inverboy/home/ordenesservicioproyectodetails/'+str(orden_servicio_id)+'/'+str(proyecto_id)+'/')
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def realizar_orden_servicio2(request, cotizacion_id, fecha_arribo, forma_pago, parametro_pago, amortizacion, retencion_garantia, rete_ica, rete_fuente, observaciones, a_i_u, utilidad, iva, proyecto_id):
    import datetime
    from datetime import date
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        usuario = Usuario.objects.get(id=user.id)
        permisos_usuario = user.get_all_permissions()
        #if validar_permiso_usuario(user.id, 'auth.view_group'):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        cotizacion = Cotizacion.objects.get(id=cotizacion_id, proyecto=proyecto)
        suministros_cotizacion = cotizacion.suministrocotizacion_set.all()
        if len(suministros_cotizacion) > 0:
            cantidades_correctas = True
            for suministro_cotizacion in suministros_cotizacion:
                cantidad_requerida = suministro_cotizacion.cantidad_total_requerida_proyecto()
                if (suministro_cotizacion.cantidad_cotizada <= 0) or (suministro_cotizacion.cantidad_cotizada > cantidad_requerida):
                    ##dajax.script("document.getElementById('id_label_error_cantidad_"+str(suministro_cotizacion.suministro.id)+"').innerHTML='Cantidad incorrecta';")
                    cantidades_correctas = False
            precios_correctos = True
            pagina = 0
            indice = 0
            for suministro_cotizacion in suministros_cotizacion:
                indice = indice + 1
                if suministro_cotizacion.precio <= 0:
                    precios_correctos = False
                    if pagina == 0:
                        pagina = indice // 20
                        if(indice % 20) > 0:
                            pagina = pagina + 1
            if cantidades_correctas == False:
                dajax.alert('Revise las cantidades deben ser mayores a 0, pero menores que la cantidad requerida')
            if precios_correctos == False:
                dajax.alert('Revise las precios, deben ser mayores a 0')

            error_fecha_arribo = ''
            if fecha_arribo == '':
                error_fecha_arribo = 'Campo obligatorio'
            if error_fecha_arribo == '':
                error_fecha_arribo = validar_fecha(fecha_arribo)
            if error_fecha_arribo == '':
                partes_fecha_arribo = fecha_arribo.split('-')
                now = datetime.datetime.now()
                fecha_actual = date(now.year, now.month, now.day)
                fecha_arribo = date(int(partes_fecha_arribo[0]), int(partes_fecha_arribo[1]), int(partes_fecha_arribo[2]),)
                diff = fecha_arribo - fecha_actual
                if diff.days < 0:
                    error_fecha_arribo = 'La fecha de arribo para la orden de compra no debe ser menor a la fecha actual'

            error_forma_pago = ''
            if forma_pago not in ['1', '2', '3', '4']:
                error_forma_pago = 'Campo obligatorio'

            error_parametro_pago = ''

            if error_forma_pago == '':
                forma_pago = int(forma_pago)
                if forma_pago == 4:
                    error_parametro_pago = validar_cadena(parametro_pago)
                elif forma_pago == 1 or forma_pago == 2 or forma_pago == 3:
                    pass

            error_amortizacion = validar_cadena(amortizacion)
            if error_amortizacion == '':
                error_amortizacion = validar_cantidad_float(amortizacion)
                if error_amortizacion == '':
                    error_amortizacion = validar_cantidad_float_negativo(amortizacion)

            error_retencion_garantia = validar_cadena(retencion_garantia)
            if error_retencion_garantia == '':
                error_retencion_garantia = validar_cantidad_float(retencion_garantia)
                if error_retencion_garantia == '':
                    error_retencion_garantia = validar_cantidad_float_negativo(retencion_garantia)

            error_rete_ica = validar_cadena(rete_ica)
            if error_rete_ica == '':
                error_rete_ica = validar_cantidad_float(rete_ica)
                if error_rete_ica == '':
                    error_rete_ica = validar_cantidad_float_negativo(rete_ica)

            error_rete_fuente = validar_cadena(rete_fuente)
            if error_rete_fuente == '':
                error_rete_fuente = validar_cantidad_float(rete_fuente)
                if error_rete_fuente == '':
                    error_rete_fuente = validar_cantidad_float_negativo(rete_fuente)

            error_a_i_u = ''
            error_utilidad = ''
            error_iva = ''
            if cotizacion.proveedor.regimen_tributario == 1:
                error_a_i_u = validar_cadena(a_i_u)
                if error_a_i_u == '':
                    error_a_i_u = validar_cantidad_float(a_i_u)
                    if error_a_i_u == '':
                        error_a_i_u = validar_cantidad_float_0(a_i_u)
                error_utilidad = validar_cadena(utilidad)
                if error_utilidad == '':
                    error_utilidad = validar_cantidad_float(utilidad)
                    if error_utilidad == '':
                        error_utilidad = validar_cantidad_float_0(utilidad)
                error_iva = validar_cadena(iva)
                if error_iva == '':
                    error_iva = validar_cantidad_float(iva)
                    if error_iva == '':
                        error_iva = validar_cantidad_float_0(iva)
            if cantidades_correctas == True and precios_correctos == True and error_fecha_arribo == '' and error_forma_pago == '' and error_parametro_pago == '' and error_amortizacion == '' and error_retencion_garantia == '' and error_rete_ica == '' and error_rete_fuente == '' and error_a_i_u == '' and error_utilidad == '' and error_iva == '':
                if fecha_arribo != '':
                    orden_servicio = OrdenServicio()
                    orden_servicio.fecha_entrega = fecha_arribo
                    orden_servicio.rete_ica = rete_ica
                    orden_servicio.rete_fuente = rete_fuente
                    orden_servicio.forma_pago = forma_pago
                    if forma_pago == 4:
                        orden_servicio.parametro_pago = parametro_pago
                    orden_servicio.amortizacion = amortizacion
                    orden_servicio.retencion_garantia = retencion_garantia
                    orden_servicio.observaciones = observaciones.strip()
                    orden_servicio.proyecto = proyecto
                    orden_servicio.proveedor = cotizacion.proveedor
                    orden_servicio.persona = usuario
                    orden_servicio.save()
                    costo_total_orden = 0
                    for suministro_cotizacion in suministros_cotizacion:
                        suministros = SuministroRequisicion.objects.filter(suministro__suministro__id=suministro_cotizacion.suministro.id, requisicion__estado=1, requisicion__proyecto=proyecto)
                        suministros = suministros.order_by('requisicion__fecha_arribo')
                        cantidad_comprada = 0.0

                        cantidad = suministro_cotizacion.cantidad_cotizada
                        for suministro in suministros:
                            cantidad_comprada_suministro_requicision = 0.0
                            if cantidad_comprada < cantidad:
                                if (round(cantidad-cantidad_comprada, 2)) <= (round(suministro.cantidad_requerida-suministro.cantidad_comprada, 2)):
                                    cantidad_comprada_suministro_requicision = round(cantidad - cantidad_comprada, 2)
                                elif (round(cantidad-cantidad_comprada, 2)) > (round(suministro.cantidad_requerida-suministro.cantidad_comprada, 2)):
                                    cantidad_comprada_suministro_requicision = round(suministro.cantidad_requerida-suministro.cantidad_comprada, 2)
                                cantidad_comprada = round(cantidad_comprada + cantidad_comprada_suministro_requicision, 2)
                                if cantidad_comprada_suministro_requicision > 0:
                                    # Actualiza la cantidad comprada en suministro apu proyecto
                                    suministro_apu_proyecto = suministro.suministro
                                    suministro_apu_proyecto.cantidad_comprada = round(suministro_apu_proyecto.cantidad_comprada + cantidad_comprada_suministro_requicision, 2)
                                    # Actualiza la cantidad requerida del suministro en el apu proyecto
                                    suministro_apu_proyecto.cantidad_requerida = round(suministro_apu_proyecto.cantidad_requerida - cantidad_comprada_suministro_requicision, 2)
                                    suministro_apu_proyecto.save()
                                    # Actualiza la cantidad comprada en suministro requicisión
                                    suministro.cantidad_comprada = round(suministro.cantidad_comprada + cantidad_comprada_suministro_requicision, 2)
                                    suministro.save()
                                    # Crea el nuevo suministro de la orden de compra
                                    suministro_orden_servicio = SuministroOrdenServicio()
                                    suministro_orden_servicio.suministro = suministro
                                    suministro_orden_servicio.cantidad = cantidad_comprada_suministro_requicision
                                    suministro_orden_servicio.precio = suministro_cotizacion.precio
                                    suministro_orden_servicio.iva_suministro = suministro_cotizacion.iva_suministro
                                    suministro_orden_servicio.orden_servicio = orden_servicio
                                    suministro_orden_servicio.save()
                        # Actualiza el precio del suministro correspondiente al proveedor
                        suministro_proveedor = SuministroProveedor.objects.get(suministro=suministro_cotizacion.suministro, proveedor=cotizacion.proveedor)
                        suministro_proveedor.precio_suministro = suministro_cotizacion.precio
                        suministro_proveedor.iva_suministro = suministro_cotizacion.iva_suministro
                        suministro_proveedor.save()
                        costo_total_orden = round(costo_total_orden + (round(suministro_cotizacion.cantidad_cotizada * (round(suministro_cotizacion.precio + round(suministro_cotizacion.precio * suministro_cotizacion.iva_suministro, 2), 2)), 2)), 2)
                        # Borra el suministro de las cotizaciones
                        SuministroCotizacion.objects.filter(suministro=suministro_cotizacion.suministro).delete()
                    if orden_servicio.proveedor.regimen_tributario == 1:
                        a_i_u = float(a_i_u)
                        iva = float(iva)
                        utilidad = float(utilidad)
                        porcentaje_costo_directo = 100 / (100+a_i_u+((iva/100)*utilidad))
                        costo_directo = costo_total_orden * porcentaje_costo_directo
                        orden_servicio.costo_directo = costo_directo
                        orden_servicio.porcentaje_a_i_u = a_i_u
                        orden_servicio.porcentaje_utilidad = utilidad
                        orden_servicio.porcentaje_iva = iva
                        orden_servicio.save()
                    actualizar_estado_requisiciones(proyecto)
                    actualizar_cotizaciones(proyecto)
                    actualizar_valor_suministro_apus(suministro_cotizacion.suministro)
                    dajax.alert('se ha realizado la orden de servicio')
                    dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id))
            dajax.script("document.getElementById('id_guardar').disabled = false;")
            if error_fecha_arribo != '' or error_forma_pago != '' or error_parametro_pago != '' or error_amortizacion != '' or error_retencion_garantia or error_rete_ica != '' or error_rete_fuente != '' or error_a_i_u != '' or error_utilidad != '' or error_iva != '':
                dajax.script("document.getElementById('id_label_error_fecha_arribo').innerHTML='"+ error_fecha_arribo +"';")
                dajax.script("document.getElementById('id_label_error_forma_pago').innerHTML='"+ error_forma_pago +"';")
                dajax.script("document.getElementById('id_label_error_parametro_forma_pago').innerHTML='"+ error_parametro_pago +"';")
                dajax.script("document.getElementById('id_label_error_amortizacion').innerHTML='"+ error_amortizacion +"';")
                dajax.script("document.getElementById('id_label_error_retencion_garantia').innerHTML='"+ error_retencion_garantia +"';")
                dajax.script("document.getElementById('id_label_error_rete_ica').innerHTML='"+ error_rete_ica +"';")
                dajax.script("document.getElementById('id_label_error_rete_fuente').innerHTML='"+ error_rete_fuente +"';")
                if cotizacion.proveedor.regimen_tributario == 1:
                    dajax.script("document.getElementById('id_label_error_a_i_u').innerHTML='"+ error_a_i_u +"';")
                    dajax.script("document.getElementById('id_label_error_utilidad').innerHTML='"+ error_utilidad +"';")
                    dajax.script("document.getElementById('id_label_error_iva').innerHTML='"+ error_iva +"';")
            if precios_correctos == False:
                pag = Paginador(request, suministros_cotizacion, 20, pagina)
                user = request.user
                permisos_usuario = user.get_all_permissions()
                render = render_to_string('ajax/suministroscotizacionordenserviciosearch.html', {'user': user, 'permisos': permisos_usuario, 'suministros': pag, 'cotizacion': cotizacion, 'proyecto': proyecto} )
                dajax.assign('#id_reporte_suministros', 'innerHTML', render)
                for suministro in pag['modelo']:
                    if suministro.precio <= 0:
                        dajax.script("document.getElementById('id_label_error_precio_" + str(suministro.id) + "').innerHTML='Precio incorrecto';")
        else:
            dajax.alert('No hay suministros en esta cotización')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_suministro_corte_diario_obra_add2(request, pagina, suministro_id, orden_servicio_id, criterio, proyecto_id, cantidad):
    from django.db.models import Sum
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
        suministros_corte_diario_obra = None
        try:
            suministros_corte_diario_obra = request.session['suministros_corte_diario_obra']
        except :
            pass
        if suministros_corte_diario_obra != None:
            cantidad = cantidad.strip()
            error_cantidad = validar_cadena(cantidad)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float_digitos(cantidad)
                if error_cantidad == '':
                    error_cantidad = validar_cantidad_float(cantidad)
                    if error_cantidad == '':
                        cantidad = float(cantidad)
                        error_cantidad = validar_cantidad_float_0(cantidad)
                        if error_cantidad == '':
                            suministro = Suministro.objects.get(id=suministro_id)
                            cantidad_total_recibida = SuministroOrdenServicio.objects.filter(suministro__suministro__suministro__id=suministro_id, orden_servicio=orden_servicio, orden_servicio__proyecto=proyecto).aggregate(Sum('cantidad_entregada'))
                            cantidad_total_comprada = SuministroOrdenServicio.objects.filter(suministro__suministro__suministro__id=suministro_id, orden_servicio=orden_servicio, orden_servicio__proyecto=proyecto).aggregate(Sum('cantidad'))
                            cantidad_total_recibida = cantidad_total_recibida['cantidad_entregada__sum']
                            cantidad_total_comprada = cantidad_total_comprada['cantidad__sum']
                            cantidad_total_recibir = round(cantidad_total_comprada - cantidad_total_recibida, 2)
                            if cantidad <= float(str(cantidad_total_recibir)):
                                existe_suministro = False
                                for suministro_corte_diario_obra in suministros_corte_diario_obra:
                                    if suministro_corte_diario_obra['id'] == suministro_id:
                                        suministro_corte_diario_obra['cantidad'] = cantidad
                                        suministro_corte_diario_obra['nuevo_porcentaje_entregado'] = round(round(100*(round(cantidad_total_recibida+cantidad, 2)),2)/cantidad_total_comprada, 2)
                                        existe_suministro = True
                                if existe_suministro == False:
                                    suministro = {'id': suministro_id, 'cantidad': cantidad, 'nuevo_porcentaje_entregado': round((round(100*(round(cantidad_total_recibida+cantidad, 2)), 2)/cantidad_total_comprada), 2)}
                                    suministros_corte_diario_obra.append(suministro)
                            else:
                                error_cantidad = 'La cantidad no debe ser mayor a la cantidad por recibir'
                        else:
                            if cantidad == 0:
                                error_cantidad = ''
                                suministros_corte_diario_obra = request.session['suministros_corte_diario_obra']
                                for suministro_corte_diario_obra in suministros_corte_diario_obra:
                                    if suministro_corte_diario_obra['id'] == suministro_id:
                                        suministros_corte_diario_obra.remove(suministro_corte_diario_obra)
                                request.session['suministros_corte_diario_obra'] = suministros_corte_diario_obra
            error = {}
            if error_cantidad != '':
                error = { 'id': suministro_id, 'value': cantidad, 'error': error_cantidad }
                
            suministros = orden_servicio.suministroordenservicio_set.all().order_by('suministro__suministro__suministro__nombre')
            criterio = criterio.strip()
            if criterio != '':
                suministros = suministros.filter(Q(suministro__suministro__suministro__nombre__icontains=criterio))
            suministros_orden_servicio = []
            for suministro in suministros:
                suministro_tmp = suministro
                suministro_adicionado = False
                for suministro_tmp2 in suministros_orden_servicio:
                    if suministro_tmp2['suministro'].suministro.suministro.suministro.id == suministro_tmp.suministro.suministro.suministro.id:
                        suministro_tmp2['suministro'].cantidad = round(suministro_tmp2['suministro'].cantidad + suministro_tmp.cantidad, 2)
                        suministro_tmp2['suministro'].cantidad_entregada = round(suministro_tmp2['suministro'].cantidad_entregada + suministro_tmp.cantidad_entregada, 2)
                        suministro_tmp2['porcentaje_entregado'] = round((round(round(100 * suministro_tmp2['suministro'].cantidad_entregada, 2), 2)/suministro_tmp2['suministro'].cantidad), 2)
                        suministro_adicionado = True
                if suministro_adicionado == False:
                    suministros_orden_servicio.append({'suministro': suministro_tmp, 'porcentaje_entregado': round(((round(100*suministro_tmp.cantidad_entregada, 2))/suministro_tmp.cantidad), 2), 'cantidad_nuevo_informe': '', 'nuevo_porcentaje_entregado': ''})

            for suministro_corte_diario_obra in suministros_corte_diario_obra:
                for suministro_orden_servicio in suministros_orden_servicio:
                    if suministro_corte_diario_obra['id'] == suministro_orden_servicio['suministro'].suministro.suministro.suministro.id:
                        suministro_orden_servicio['cantidad_nuevo_informe'] = suministro_corte_diario_obra['cantidad']
                        suministro_orden_servicio['nuevo_porcentaje_entregado'] = suministro_corte_diario_obra['nuevo_porcentaje_entregado']
            pag = Paginador(request, suministros_orden_servicio, 20, pagina)
            render =  render_to_string('ajax/suministrosordenserviciosearchcortediarioobra.html', {'user': user, 'suministros': pag, 'criterio': criterio, 'orden_servicio': orden_servicio, 'proyecto': proyecto, 'error': error })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
            if error_cantidad != '':
                dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_modificar_suministro_corte_diario_obra_add2(request, pagina, suministro_id, orden_servicio_id, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
        suministros_corte_diario_obra = None
        try:
            suministros_corte_diario_obra = request.session['suministros_corte_diario_obra']
        except :
            pass
        if suministros_corte_diario_obra != None:
            error = {}
            for suministro_corte_diario_obra in suministros_corte_diario_obra:
                if suministro_corte_diario_obra['id'] == suministro_id:
                    error = { 'id': suministro_id, 'value': suministro_corte_diario_obra['cantidad'], 'error': '' }
            suministros = orden_servicio.suministroordenservicio_set.all().order_by('suministro__suministro__suministro__nombre')
            criterio = criterio.strip()
            if criterio != '':
                suministros = suministros.filter(Q(suministro__suministro__suministro__nombre__icontains=criterio))
            suministros_orden_servicio = []
            for suministro in suministros:
                suministro_tmp = suministro
                suministro_adicionado = False
                for suministro_tmp2 in suministros_orden_servicio:
                    if suministro_tmp2['suministro'].suministro.suministro.suministro.id == suministro_tmp.suministro.suministro.suministro.id:
                        suministro_tmp2['suministro'].cantidad = round(suministro_tmp2['suministro'].cantidad + suministro_tmp.cantidad, 2)
                        suministro_tmp2['suministro'].cantidad_entregada = round(suministro_tmp2['suministro'].cantidad_entregada + suministro_tmp.cantidad_entregada, 2)
                        suministro_tmp2['porcentaje_entregado'] = round(((round(100 * suministro_tmp2['suministro'].cantidad_entregada, 2))/suministro_tmp2['suministro'].cantidad), 2)
                        suministro_adicionado = True
                if suministro_adicionado == False:
                    suministros_orden_servicio.append({'suministro': suministro_tmp, 'porcentaje_entregado': round(((round(100*suministro_tmp.cantidad_entregada, 2))/suministro_tmp.cantidad), 2), 'cantidad_nuevo_informe': '', 'nuevo_porcentaje_entregado': ''})
            
            for suministro_corte_diario_obra in suministros_corte_diario_obra:
                for suministro_orden_servicio in suministros_orden_servicio:
                    if suministro_corte_diario_obra['id'] == suministro_orden_servicio['suministro'].suministro.suministro.suministro.id:
                        suministro_orden_servicio['cantidad_nuevo_informe'] = suministro_corte_diario_obra['cantidad']
                        suministro_orden_servicio['nuevo_porcentaje_entregado'] = suministro_corte_diario_obra['nuevo_porcentaje_entregado']
            pag = Paginador(request, suministros_orden_servicio, 20, pagina)
            render =  render_to_string('ajax/suministrosordenserviciosearchcortediarioobra.html', {'user': user, 'suministros': pag, 'criterio': criterio, 'orden_servicio': orden_servicio, 'proyecto': proyecto, 'error': error })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#Acta de recibo de obra
#Detalles cantidad suministro acta_recibo_obra add
def detalles_cantidad_suministro_acta_recibo_obra_add2(request, suministro_id, fecha_especifica, orden_servicio_id, fecha_inicio, fecha_fin, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)

        fecha_especifica = fecha_especifica.strip()

        fecha_inicio_rango = fecha_especifica + ' 00:00:00'
        fecha_fin_rango = fecha_especifica + ' 23:59:59'

        suministro = Suministro.objects.get(id=suministro_id)

        suministros_cortes_diario_obra = SuministroCorteDiarioObra.objects.filter(corte_diario_obra__orden_servicio=orden_servicio, corte_diario_obra__estado=True, corte_diario_obra__fecha_corte__range=(fecha_inicio_rango, fecha_fin_rango), suministro__suministro_orden_servicio_item__suministro=suministro)

        suministros_cortes_diarios = []

        # Agrupación por suministro y corte diario
        for suministro_cortes_diario_obra in suministros_cortes_diario_obra:
            existe_suministro = False
            for suministro_cortes_diarios in suministros_cortes_diarios:
                if suministro_cortes_diario_obra.corte_diario_obra.id == suministro_cortes_diarios.corte_diario_obra.id:
                    suministro_cortes_diarios.cantidad = round(suministro_cortes_diarios.cantidad + suministro_cortes_diario_obra.cantidad, 2)
                    existe_suministro = True
            if existe_suministro == False:
                suministros_cortes_diarios.append(suministro_cortes_diario_obra)

        request.session['suministros_cortes_diarios'] = suministros_cortes_diarios

        render =  render_to_string('ajax/detallescantidadsuministroactareciboobraadd.html', {'user': user, 'orden_servicio': orden_servicio, 'suministros_cortes_diarios': suministros_cortes_diarios, 'suministro': suministro, 'fecha_especifica': fecha_especifica, 'fecha_inicio': fecha_inicio, 'fecha_fin':fecha_fin, 'proyecto': proyecto})
        dajax.assign('#light','innerHTML', render)
        dajax.script("document.getElementById('light').style.display='block';")
        dajax.script("document.getElementById('fade').style.display='block';")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#Activar input cantidad de suministro acta_recibo_obra_add
def activar_input_cantidad_suministro_acta_recibo_obra_add2(request, corte_diario_obra_id, suministro_id, fecha_especifica, orden_servicio_id, fecha_inicio, fecha_fin, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)

        fecha_especifica = fecha_especifica.strip()

        suministro = Suministro.objects.get(id=suministro_id)

        suministros_cortes_diarios = request.session['suministros_cortes_diarios']

        error = {}

        for suministro_cortes_diarios in suministros_cortes_diarios:
            if suministro_cortes_diarios.corte_diario_obra.id == corte_diario_obra_id:
                error = {'id': corte_diario_obra_id, 'value': suministro_cortes_diarios.cantidad, 'error': ''}

        render =  render_to_string('ajax/detallescantidadsuministroactareciboobraadd.html', {'user': user, 'orden_servicio': orden_servicio, 'suministros_cortes_diarios': suministros_cortes_diarios, 'suministro': suministro, 'fecha_especifica': fecha_especifica, 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin, 'error': error, 'proyecto': proyecto})
        dajax.assign('#light','innerHTML', render)
        dajax.script("document.getElementById('id_text_cantidad_"+str(corte_diario_obra_id)+"').select();")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#Modificar la cantidad de suministro de un corte de obra diario acta_recibo_obra_add
def modificar_cantidad_suministro_acta_recibo_obra_add2(request, corte_diario_obra_id, suministro_id, cantidad, fecha_especifica, orden_servicio_id, fecha_inicio, fecha_fin, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)

        suministros_cortes_diarios = None
        try:
            suministros_cortes_diarios = request.session['suministros_cortes_diarios']
        except :
            pass
        if suministros_cortes_diarios != None:
            suministro = Suministro.objects.get(id=suministro_id)
            cantidad = cantidad.strip()
            error_cantidad = validar_cadena(cantidad)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float_digitos(cantidad)
                if error_cantidad == '':
                    error_cantidad = validar_cantidad_float(cantidad)
                    if error_cantidad == '':
                        cantidad = float(cantidad)
                        error_cantidad = validar_cantidad_float_negativo(cantidad)
                        if error_cantidad == '':
                            for suministro_cortes_diarios in suministros_cortes_diarios:
                                if suministro_cortes_diarios.corte_diario_obra.id == corte_diario_obra_id and suministro_cortes_diarios.suministro.suministro_orden_servicio_item.suministro.id == suministro_id:
                                    if cantidad <= suministro_cortes_diarios.cantidad:
                                        suministro_cortes_diarios.cantidad = cantidad
                                    else:
                                        error_cantidad = 'La cantidad no puede ser mayor a la registrada en el corte diario de obra'
            error = {}
            if error_cantidad != '':
                error = {'id': corte_diario_obra_id, 'value': cantidad, 'error': error_cantidad}
            render =  render_to_string('ajax/detallescantidadsuministroactareciboobraadd.html', {'user': user, 'orden_servicio': orden_servicio, 'suministros_cortes_diarios': suministros_cortes_diarios, 'suministro': suministro, 'fecha_especifica': fecha_especifica, 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin, 'error': error, 'proyecto': proyecto})
            dajax.assign('#light','innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_"+str(corte_diario_obra_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#Registrar la cantidad de suministro de un corte de obra diario acta_recibo_obra_add
def registrar_cantidad_suministro_acta_recibo_obra_add2(request, orden_servicio_id, fecha_inicio, fecha_fin, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)

        suministros_cortes_diarios = None
        try:
            suministros_cortes_diarios = request.session['suministros_cortes_diarios']
        except :
            pass
        if suministros_cortes_diarios != None:
            for suministro_cortes_diarios in suministros_cortes_diarios:
                corte_diario_obra = CorteDiarioObra.objects.get(id=suministro_cortes_diarios.corte_diario_obra.id)
                corte_diario_obra.modificar_cantidad_suministro(suministro_cortes_diarios.suministro.suministro_orden_servicio_item.suministro.id, suministro_cortes_diarios.cantidad)

            fecha_inicio = fecha_inicio.strip()
            fecha_fin = fecha_fin.strip()
            fecha_inicio_rango = '2013-01-01'
            error_fecha_inicio = ''
            error_fecha_fin = ''
            if fecha_inicio != '':
                fecha_inicio_rango = fecha_inicio

            fecha_fin_rango = fecha_fin + ' 23:59:59'
            
            suministros_cortes_diario_obra = SuministroCorteDiarioObra.objects.filter(corte_diario_obra__orden_servicio=orden_servicio, corte_diario_obra__estado=True, corte_diario_obra__fecha_corte__range=(fecha_inicio_rango, fecha_fin_rango)).order_by('corte_diario_obra__fecha_corte', 'id', 'suministro__suministro_orden_servicio_item__suministro__nombre')

            etiquetas_suministros = suministros_cortes_diario_obra.values('suministro__suministro__suministro__suministro__id', 'suministro__suministro__suministro__suministro__nombre', 'suministro__suministro__suministro__suministro__unidad_medida').annotate(cantidad_total=Sum('cantidad'))

            qry_etiquetas_fechas = suministros_cortes_diario_obra.values('corte_diario_obra__fecha_corte')
            etiquetas_fechas = []
            for item in qry_etiquetas_fechas:
                item = {'corte_diario_obra__fecha_corte': item['corte_diario_obra__fecha_corte']}
                existe_item = False
                for etiqueta_fecha in etiquetas_fechas:
                    if item['corte_diario_obra__fecha_corte'].year == etiqueta_fecha['corte_diario_obra__fecha_corte'].year and item['corte_diario_obra__fecha_corte'].month == etiqueta_fecha['corte_diario_obra__fecha_corte'].month and item['corte_diario_obra__fecha_corte'].day == etiqueta_fecha['corte_diario_obra__fecha_corte'].day:
                        existe_item = True
                if existe_item == False:
                    etiquetas_fechas.append(item)

            matriz = [ [ 0 for i in range(len(etiquetas_fechas)+3) ] for j in range(len(etiquetas_suministros)+1) ]

            for d1 in range(1, len(etiquetas_suministros)+1):
                matriz[d1][0] = etiquetas_suministros[d1-1]
                matriz[d1][1] = etiquetas_suministros[d1-1]
                matriz[d1][2] = etiquetas_suministros[d1-1]

            for d1 in range(3, (len(etiquetas_fechas)+3)):
                matriz[0][d1] = etiquetas_fechas[d1-3]

            #Suministros de cortes de obra diarios agrupados por suministro y fecha de corte de obra diario
            suministros_cortes_diarios = suministros_cortes_diario_obra.values('suministro__suministro__suministro__suministro__id', 'corte_diario_obra__fecha_corte').annotate(cantidad_corte=Sum('cantidad'))

            suministros = []
            for suministro_cortes_diarios in suministros_cortes_diarios:
                existe_suministro = False
                for suministro in suministros:
                    #Verifica el id del suministro y si pertenece a la misma fecha de registro
                    if suministro_cortes_diarios['suministro__suministro__suministro__suministro__id'] == suministro['suministro__suministro__suministro__suministro__id']:
                        if suministro_cortes_diarios['corte_diario_obra__fecha_corte'].year == suministro['corte_diario_obra__fecha_corte'].year and suministro_cortes_diarios['corte_diario_obra__fecha_corte'].month == suministro['corte_diario_obra__fecha_corte'].month and suministro_cortes_diarios['corte_diario_obra__fecha_corte'].day == suministro['corte_diario_obra__fecha_corte'].day:
                            suministro['cantidad_corte'] = round(suministro['cantidad_corte'] + suministro_cortes_diarios['cantidad_corte'], 2)
                            existe_suministro = True
                if existe_suministro == False:
                    suministros.append(suministro_cortes_diarios)

            for d1 in range(1, len(etiquetas_suministros)+1):
                for d2 in range(3, len(etiquetas_fechas)+3):
                    for suministro in suministros:
                        if suministro['suministro__suministro__suministro__suministro__id'] == matriz[d1][0]['suministro__suministro__suministro__suministro__id'] and suministro['corte_diario_obra__fecha_corte'].year == matriz[0][d2]['corte_diario_obra__fecha_corte'].year and suministro['corte_diario_obra__fecha_corte'].month == matriz[0][d2]['corte_diario_obra__fecha_corte'].month and suministro['corte_diario_obra__fecha_corte'].day == matriz[0][d2]['corte_diario_obra__fecha_corte'].day:
                            matriz[d1][d2] = suministro

            render =  render_to_string('ajax/itemsordenserviciosearchactareciboobraadd.html', {'user': user, 'orden_servicio': orden_servicio, 'matriz': matriz, 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin, 'error_fecha_inicio': error_fecha_inicio, 'error_fecha_fin': error_fecha_fin, 'proyecto': proyecto})
            dajax.assign('#id_reporte_suministros','innerHTML', render)
            dajax.script("document.getElementById('light').style.display='none';")
            dajax.script("document.getElementById('fade').style.display='none';")
            # Elimina las variables de la session
            del request.session['suministros_cortes_diarios']
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#Asignar valor_cooperativa acta_recibo_obra
def asignar_valor_cooperativa_acta_recibo_obra2(request, acta_recibo_obra_id, valor_cooperativa, proyecto_id):
    from django.contrib.humanize.templatetags.humanize import intcomma
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_actareciboobra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                acta_recibo_obra = ActaReciboObra.objects.get(id=acta_recibo_obra_id, orden_servicio__proyecto=proyecto)
                if acta_recibo_obra.estado_acta == 1:
                    valor_cooperativa = valor_cooperativa.strip()
                    error_valor_cooperativa = validar_cadena(valor_cooperativa)
                    if error_valor_cooperativa == '':
                        error_valor_cooperativa = validar_cantidad_float_digitos(valor_cooperativa)
                        if error_valor_cooperativa == '':
                            error_valor_cooperativa = validar_cantidad_float(valor_cooperativa)
                            if error_valor_cooperativa == '':
                                valor_cooperativa = float(valor_cooperativa)
                                error_valor_cooperativa = validar_cantidad_float_0(valor_cooperativa)
                                if error_valor_cooperativa == '':
                                    if valor_cooperativa <= acta_recibo_obra.valor_maximo_cooperativa():
                                        acta_recibo_obra.valor_cooperativa = valor_cooperativa
                                        acta_recibo_obra.save()
                                        dajax.redirect('/inverboy/home/actasreciboobraproyectodetails/' + str(acta_recibo_obra_id) + '/' + str(proyecto_id)+'/')
                                        #dajax.script("document.getElementById('id_text_valor_cooperativa').value = '" + str(intcomma(valor_cooperativa)) + "';")
                                        #dajax.script("document.getElementById('id_asignar_valor_cooperativa').style.display = 'none';")
                                        #dajax.script("document.getElementById('id_text_valor_cooperativa').readOnly = true;")
                                    else:
                                        error_valor_cooperativa = 'El valor de la cooperativa no puede exceder a: ' + str(intcomma(acta_recibo_obra.valor_maximo_cooperativa()))
                    dajax.script("document.getElementById('id_label_error_cooperativa').innerHTML = '" + error_valor_cooperativa + "';")
                    if error_valor_cooperativa != '':
                        dajax.script("document.getElementById('id_text_valor_cooperativa').select();")
                else:
                    dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#Cerrar acta_recibo_obra (Estado = 2 - No se puede modificar valor_cooperativa)
def cerrar_acta_recibo_obra2(request, acta_recibo_obra_id, valor_cooperativa, proyecto_id):
    from django.contrib.humanize.templatetags.humanize import intcomma
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_actareciboobra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                acta_recibo_obra = ActaReciboObra.objects.get(id=acta_recibo_obra_id, orden_servicio__proyecto=proyecto)
                if acta_recibo_obra.estado_acta == 1:
                    valor_cooperativa = valor_cooperativa.strip()
                    error_valor_cooperativa = validar_cadena(valor_cooperativa)
                    if error_valor_cooperativa == '':
                        error_valor_cooperativa = validar_cantidad_float_digitos(valor_cooperativa)
                        if error_valor_cooperativa == '':
                            error_valor_cooperativa = validar_cantidad_float(valor_cooperativa)
                            if error_valor_cooperativa == '':
                                valor_cooperativa = float(valor_cooperativa)
                                error_valor_cooperativa = validar_cantidad_float_0(valor_cooperativa)
                                if error_valor_cooperativa == '':
                                    if valor_cooperativa <= acta_recibo_obra.valor_maximo_cooperativa():
                                        acta_recibo_obra.valor_cooperativa = valor_cooperativa
                                        acta_recibo_obra.estado_acta = 2
                                        acta_recibo_obra.save()
                                        dajax.redirect('/inverboy/home/actasreciboobraproyectodetails/' + str(acta_recibo_obra_id) + '/' + str(proyecto_id)+'/')
                                        #dajax.script("document.getElementById('id_text_valor_cooperativa').value = '" + str(intcomma(valor_cooperativa)) + "';")
                                        #dajax.script("document.getElementById('id_asignar_valor_cooperativa').style.display = 'none';")
                                        #dajax.script("document.getElementById('id_cerrar_acta_recibo_obra').style.display = 'none';")
                                        #dajax.script("document.getElementById('id_text_valor_cooperativa').readOnly = true;")
                                    else:
                                        error_valor_cooperativa = 'El valor de la cooperativa no puede exceder a: ' + str(intcomma(acta_recibo_obra.valor_maximo_cooperativa()))
                    dajax.script("document.getElementById('id_label_error_cooperativa').innerHTML = '" + error_valor_cooperativa + "';")
                    if error_valor_cooperativa != '':
                        dajax.script("document.getElementById('id_text_valor_cooperativa').select();")

                else:
                    dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def detalles_cantidad_suministro_modificar_acta_recibo_obra2(request, suministro_id, fecha_especifica, acta_recibo_obra_id, proyecto_id):
    """Detalles cantidad suministro modificar acta_recibo_obra
    """
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        items_acta_recibo_obra = None
        try:
            items_acta_recibo_obra = request.session['items_acta_recibo_obra']
        except :
            pass
        if items_acta_recibo_obra != None:
            proyecto = Proyecto.objects.get(id=proyecto_id)
            acta_recibo_obra = ActaReciboObra.objects.get(id=acta_recibo_obra_id, orden_servicio__proyecto=proyecto)
            suministro = {}
            for item_acta_recibo_obra in items_acta_recibo_obra['lista_items']:
                if item_acta_recibo_obra['suministro'].id == int(suministro_id):
                    for registro in item_acta_recibo_obra['registros']:
                        if registro['fecha_registro'] == fecha_especifica:
                            # Crea una nueva lista  en memoria con los registros a modificar
                            lista_registros = []
                            for item_registro in registro['registros']:
                                lista_registros.append({'id': item_registro['id'], 'consecutivo': item_registro['consecutivo'], 'usuario': item_registro['usuario'], 'cantidad': item_registro['cantidad']})
                            suministro = {'suministro': item_acta_recibo_obra['suministro'], 'fecha_especifica': fecha_especifica, 'cantidad': registro['cantidad'], 'registros': lista_registros}
                            request.session['suministro_modificar'] = suministro
            render =  render_to_string('ajax/detallescantidadsuministromodificaractareciboobra.html', {'user': user, 'acta_recibo_obra': acta_recibo_obra, 'suministro': suministro, 'proyecto': proyecto})
            dajax.assign('#light','innerHTML', render)
            dajax.script("document.getElementById('light').style.display='block';")
            dajax.script("document.getElementById('fade').style.display='block';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#Activa input la cantidad de suministro de un corte de obra diario acta_recibo_obra_add
def activar_input_modificar_cantidad_suministro_modificar_acta_recibo_obra2(request, registro_id, acta_recibo_obra_id, proyecto_id):
    """Activa caja de texto para modificación de cantidad
    """
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        items_acta_recibo_obra = None
        suministro_modificar = None
        try:
            items_acta_recibo_obra = request.session['items_acta_recibo_obra']
            suministro_modificar = request.session['suministro_modificar']
        except :
            pass
        if items_acta_recibo_obra and suministro_modificar:
            proyecto = Proyecto.objects.get(id=proyecto_id)
            acta_recibo_obra = ActaReciboObra.objects.get(id=acta_recibo_obra_id, orden_servicio__proyecto=proyecto)
            for registro in suministro_modificar['registros']:
                if registro['id'] == int(registro_id):
                    error = {'id': registro['id'], 'value': registro['cantidad'], 'error': ''}
                    break
            render =  render_to_string('ajax/detallescantidadsuministromodificaractareciboobra.html', {'user': user, 'acta_recibo_obra': acta_recibo_obra, 'suministro': suministro_modificar, 'error': error, 'proyecto': proyecto})
            dajax.assign('#light','innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_" + str(registro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#Modificar la cantidad de suministro de un corte de obra diario acta_recibo_obra_add
def modificar_cantidad_suministro_modificar_acta_recibo_obra2(request, registro_id, cantidad, acta_recibo_obra_id, proyecto_id):
    from django.contrib.humanize.templatetags.humanize import intcomma
    """Modificar cantidad de un registro
    """
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        items_acta_recibo_obra = None
        suministro_modificar = None
        try:
            items_acta_recibo_obra = request.session['items_acta_recibo_obra']
            suministro_modificar = request.session['suministro_modificar']
        except :
            pass
        if items_acta_recibo_obra and suministro_modificar:
            proyecto = Proyecto.objects.get(id=proyecto_id)
            acta_recibo_obra = ActaReciboObra.objects.get(id=acta_recibo_obra_id, orden_servicio__proyecto=proyecto)

            error_cantidad = ''
            validaciones = Validator().append([
                Field('cantidad', cantidad).append([
                    IsRequired('Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto.'),
                ]),
            ]).run(True).pop()

            if validaciones['passed'] == True:
                cantidad = float(cantidad)
                if cantidad > 0:
                    for registro in suministro_modificar['registros']:
                        if registro['id'] == int(registro_id):
                            suministro_corte_diario = SuministroCorteDiarioObra.objects.get(id=registro_id)
                            if cantidad <= suministro_corte_diario.cantidad:
                                if cantidad != registro['cantidad']:
                                    diferencia = round(registro['cantidad'] - cantidad, 2)
                                    registro['cantidad'] = cantidad
                                    suministro_modificar['cantidad'] = round(suministro_modificar['cantidad'] - diferencia, 2)
                                    break
                            else:
                                error_cantidad = 'La cantidad no puede ser mayor a la cantidad registrada (' + str(intcomma(suministro_corte_diario.cantidad)) + ')'
                else:
                    error_cantidad = 'La cantidad debe ser mayor a cero (0).'
            else:
                for error in validaciones['errors']:
                    error_cantidad = error
            error = {}
            if error_cantidad != '':
                error = {'id': int(registro_id), 'value': cantidad, 'error': error_cantidad}
            render =  render_to_string('ajax/detallescantidadsuministromodificaractareciboobra.html', {'user': user, 'acta_recibo_obra': acta_recibo_obra, 'suministro': suministro_modificar, 'error': error, 'proyecto': proyecto})
            dajax.assign('#light','innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_" + str(registro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/' + str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def registrar_cantidad_suministro_modificar_acta_recibo_obra2(request, acta_recibo_obra_id, proyecto_id):
    """Modificar cantidad de un registro
    """
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        items_acta_recibo_obra = None
        suministro_modificar = None
        try:
            items_acta_recibo_obra = request.session['items_acta_recibo_obra']
            suministro_modificar = request.session['suministro_modificar']
        except :
            pass
        if items_acta_recibo_obra and suministro_modificar:
            proyecto = Proyecto.objects.get(id=proyecto_id)
            acta_recibo_obra = ActaReciboObra.objects.get(id=acta_recibo_obra_id, orden_servicio__proyecto=proyecto)
            for item_acta_recibo_obra in items_acta_recibo_obra['lista_items']:
                if item_acta_recibo_obra['suministro'].id == suministro_modificar['suministro'].id:
                    for registro in item_acta_recibo_obra['registros']:
                        if registro['fecha_registro'] == suministro_modificar['fecha_especifica']:
                            registro['registros'] = suministro_modificar['registros']
                            if registro['cantidad'] != suministro_modificar['cantidad']:
                                diferencia = round(registro['cantidad'] - suministro_modificar['cantidad'], 2)
                                registro['cantidad'] = suministro_modificar['cantidad']
                                item_acta_recibo_obra['cantidad'] = round(item_acta_recibo_obra['cantidad'] - diferencia, 2)
                                break
            del request.session['suministro_modificar']
            render =  render_to_string('ajax/itemsactareciboobramodificar.html', {'user': user, 'acta_recibo_obra': acta_recibo_obra, 'items_acta_recibo_obra': items_acta_recibo_obra, 'proyecto': proyecto})
            dajax.assign('#id_reporte_suministros','innerHTML', render)
            dajax.script("document.getElementById('fade').style.display='none';")
            dajax.script("document.getElementById('light').style.display='none';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/' + str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def cancelar_registrar_cantidad_suministro_modificar_acta_recibo_obra2(request, acta_recibo_obra_id, proyecto_id):
    """Modificar cantidad de un registro
    """
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        items_acta_recibo_obra = None
        suministro_modificar = None
        try:
            items_acta_recibo_obra = request.session['items_acta_recibo_obra']
            suministro_modificar = request.session['suministro_modificar']
        except :
            pass
        if items_acta_recibo_obra and suministro_modificar:
            proyecto = Proyecto.objects.get(id=proyecto_id)
            acta_recibo_obra = ActaReciboObra.objects.get(id=acta_recibo_obra_id, orden_servicio__proyecto=proyecto)
            del request.session['suministro_modificar']
            dajax.script("document.getElementById('fade').style.display='none';")
            dajax.script("document.getElementById('light').style.display='none';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/' + str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def anadir_suministro_orden_giro2(request, pagina, suministro_id, cantidad, observaciones, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros_orden_giro = None
        try:
            suministros_orden_giro = request.session['suministros_orden_giro']
        except :
            pass
        if suministros_orden_giro != None:
            cantidad = cantidad.strip()
            observaciones = observaciones.strip()
            error_cantidad = validar_cadena(cantidad)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float_digitos(cantidad)
                if error_cantidad == '':
                    error_cantidad = validar_cantidad_float(cantidad)
                    if error_cantidad == '':
                        cantidad = float(cantidad)
                        error_cantidad = validar_cantidad_float_negativo(cantidad)
                        if error_cantidad == '':
                            if proyecto.validar_cantidad_suministro_pendientes_comprar(suministro_requisicion_id=suministro_id, cantidad_evaluar=cantidad, clasificacion_general=['Indirectos']) == False:
                                error_cantidad = 'La cantidad no debe ser mayor al total requerido'
            error_observaciones = validar_cadena(observaciones)
            if error_cantidad == '' and error_observaciones == '':
                if cantidad == 0:
                    error_cantidad = ''
                    for suministro_orden_giro in suministros_orden_giro:
                        if suministro_orden_giro['suministro_id'] == suministro_id:
                            suministros_orden_giro.remove(suministro_orden_giro)
                else:
                    existe_suministro = False
                    for suministro_orden_giro in suministros_orden_giro:
                        if suministro_orden_giro['suministro_id'] == suministro_id:
                            suministro_orden_giro['cantidad'] = cantidad
                            suministro_orden_giro['observaciones'] = observaciones
                            existe_suministro = True
                    if existe_suministro == False:
                        suministros_orden_giro.append({ 'suministro_id': suministro_id, 'cantidad': cantidad, 'observaciones': observaciones })
                request.session['suministros_orden_giro'] = suministros_orden_giro

            error = {}
            if error_cantidad != '' or error_observaciones != '':
                error = {'id': suministro_id, 'value': cantidad, 'error': error_cantidad, 'value_observaciones': observaciones, 'error_observaciones': error_observaciones}

            #Visualiza los suministros requeridos con la cantidad a cotizar
            criterio = criterio.strip()
            suministros_pendientes = proyecto.get_suministros_pendientes_comprar(criterio=criterio, clasificacion_general=['Indirectos'])
            suministros_requisiciones = []
            for suministro_pendientes in suministros_pendientes:
                suministro_requisicion = { 'suministro': suministro_pendientes, 'cantidad_nueva_orden_giro': '', 'observaciones': '' }
                for suministro_orden_giro in suministros_orden_giro:
                    if suministro_pendientes.id == suministro_orden_giro['suministro_id']:
                        suministro_requisicion['cantidad_nueva_orden_giro'] = suministro_orden_giro['cantidad']
                        suministro_requisicion['observaciones'] = suministro_orden_giro['observaciones']
                suministros_requisiciones.append(suministro_requisicion)

            pag = Paginador(request, suministros_requisiciones, 20, pagina)

            render = render_to_string('ajax/suministrosrequisicionessearchordengiroadd.html', {'user': user, 'suministros_requisiciones': pag, 'criterio': criterio, 'proyecto': proyecto, 'error': error } )
            dajax.assign('#id_reporte_suministros_requisiciones', 'innerHTML', render)

            if (error_cantidad != '' and error_observaciones != '') or (error_cantidad != ''):
                dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
            elif error_observaciones != '':
                dajax.script("document.getElementById('id_text_observaciones_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_modificar_suministro_orden_giro_add2(request, pagina, suministro_id, criterio, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros_orden_giro = None
        try:
            suministros_orden_giro = request.session['suministros_orden_giro']
        except :
            pass
        if suministros_orden_giro != None:
            #Visualiza los suministros requeridos
            suministros_pendientes = proyecto.get_suministros_pendientes_comprar(criterio=criterio, clasificacion_general=['Indirectos'])
            suministros_requisiciones = []
            error = {}
            for suministro_pendientes in suministros_pendientes:
                suministro_requisicion = { 'suministro': suministro_pendientes, 'cantidad_nueva_orden_giro': '', 'observaciones': '' }
                for suministro_orden_giro in suministros_orden_giro:
                    if suministro_pendientes.id == suministro_orden_giro['suministro_id']:
                        suministro_requisicion['cantidad_nueva_orden_giro'] = suministro_orden_giro['cantidad']
                        suministro_requisicion['observaciones'] = suministro_orden_giro['observaciones']
                        if suministro_orden_giro['suministro_id'] == suministro_id:
                            error = { 'id': suministro_id, 'value': suministro_orden_giro['cantidad'], 'error': '', 'value_observaciones': suministro_orden_giro['observaciones'], 'error_observaciones': '' }
                suministros_requisiciones.append(suministro_requisicion)

            pag = Paginador(request, suministros_requisiciones, 20, pagina)

            render = render_to_string('ajax/suministrosrequisicionessearchordengiroadd.html', {'user': user, 'suministros_requisiciones': pag, 'criterio': criterio, 'proyecto': proyecto, 'error': error} )
            dajax.assign('#id_reporte_suministros_requisiciones', 'innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def seleccionar_proveedor_orden_giro_proyecto_add2(request, proveedor_id, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros_orden_giro = None
        try:
            suministros_orden_giro = request.session['suministros_orden_giro']
        except :
            pass
        if suministros_orden_giro != None:
            proveedor = Proveedor.objects.get(id=proveedor_id)
            dajax.script("document.getElementById('id_proveedor').value='" + str(proveedor_id) + "';")
            render = render_to_string('ajax/informacionproveedorordengiroproyectoadd.html', {'user': user, 'proveedor': proveedor, 'proyecto': proyecto} )
            dajax.assign('#id_informacion_proveedor', 'innerHTML', render)
            dajax.script("document.getElementById('fade').style.display='none';")
            dajax.script("document.getElementById('light').style.display='none';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_item_acta_conformidad_add2(request, pagina, item_id, orden_giro_id, criterio, proyecto_id, valor):
    from django.db.models import Sum
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        orden_giro = proyecto.ordengiro_set.get(id=orden_giro_id)
        items_acta_conformidad = None
        try:
            items_acta_conformidad = request.session['items_acta_conformidad']
        except :
            pass
        if items_acta_conformidad != None:
            error_valor = validar_cadena(valor)
            if error_valor == '':
                error_valor = validar_cantidad_float_digitos(valor)
                if error_valor == '':
                    error_valor = validar_cantidad_float(valor)
                    if error_valor == '':
                        valor = float(valor)
                        error_valor = validar_cantidad_float_0(valor)
                        if error_valor == '':
                            item_orden_giro = orden_giro.itemordengiro_set.get(id=item_id)
                            if item_orden_giro.valor_disponible(valor) == True:
                                existe_item = False
                                for item_acta_conformidad in items_acta_conformidad:
                                    if item_acta_conformidad['id'] == item_id:
                                        item_acta_conformidad['valor'] = valor
                                        existe_item = True
                                if existe_item == False:
                                    item = {'id': item_id, 'valor': valor}
                                    items_acta_conformidad.append(item)
                            else:
                                error_valor = 'El valor no debe ser mayor a la cantidad disponible por girar'
                        else:
                            if valor == 0:
                                error_valor = ''
                                for item_acta_conformidad in items_acta_conformidad:
                                    if item_acta_conformidad['id'] == item_id:
                                        items_acta_conformidad.remove(item_acta_conformidad)
            request.session['items_acta_conformidad'] = items_acta_conformidad
            error = {}
            if error_valor != '':
                error = {'id': item_id, 'value': valor, 'error': error_valor}
            orden_giro = OrdenGiro.objects.get(id=orden_giro_id)
            items_orden_giro = orden_giro.itemordengiro_set.all().order_by('suministro__suministro__suministro__nombre')
            criterio = criterio.strip()
            if criterio != '':
                items_orden_giro = items_orden_giro.filter(Q(descripcion__icontains=criterio))
            lista_items_orden_giro = []
            for item_orden_giro in items_orden_giro:
                item = {'item': item_orden_giro, 'valor_nueva_acta': ''}
                for item_acta_conformidad in items_acta_conformidad:
                    if item_acta_conformidad['id'] == item_orden_giro.id:
                        item['valor_nueva_acta'] = item_acta_conformidad['valor']
                lista_items_orden_giro.append(item)
            pag = Paginador(request, lista_items_orden_giro, 20, pagina)
            render =  render_to_string('ajax/itemsordengirosearchactaconformidad.html', {'user': user, 'items': pag, 'criterio': criterio, 'orden_giro': orden_giro, 'proyecto': proyecto, 'error': error})
            dajax.assign('#id_reporte_items','innerHTML', render)
            if error_valor != '':
                dajax.script("document.getElementById('id_text_valor_"+str(item_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_modificar_item_acta_conformidad_add2(request, pagina, item_id, orden_giro_id, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        items_acta_conformidad = None
        try:
            items_acta_conformidad = request.session['items_acta_conformidad']
        except :
            pass
        if items_acta_conformidad != None:
            error = {}
            for item_acta_conformidad in items_acta_conformidad:
                if item_acta_conformidad['id'] == item_id:
                    error = {'id': item_id, 'value': item_acta_conformidad['valor'], 'error': ''}
            #Actualiza la interfaz
            orden_giro = proyecto.ordengiro_set.get(id=orden_giro_id)
            items_orden_giro = orden_giro.itemordengiro_set.all().order_by('suministro__suministro__suministro__nombre')
            criterio = criterio.strip()
            if criterio != '':
                items_orden_giro = items_orden_giro.filter(Q(descripcion__icontains=criterio))
            lista_items_orden_giro = []
            for item_orden_giro in items_orden_giro:
                item = {'item': item_orden_giro, 'valor_nueva_acta': ''}
                for item_acta_conformidad in items_acta_conformidad:
                    if item_acta_conformidad['id'] == item_orden_giro.id:
                        item['valor_nueva_acta'] = item_acta_conformidad['valor']
                    if item_acta_conformidad['id'] == item_id:
                        error = {'id': item_id, 'value': item_acta_conformidad['valor'], 'error': ''}
                lista_items_orden_giro.append(item)
            pag = Paginador(request, lista_items_orden_giro, 20, pagina)
            user = request.user
            render =  render_to_string('ajax/itemsordengirosearchactaconformidad.html', {'user': user, 'items': pag, 'criterio': criterio, 'orden_giro': orden_giro, 'proyecto': proyecto, 'error': error})
            dajax.assign('#id_reporte_items','innerHTML', render)
            dajax.script("document.getElementById('id_text_valor_" + str(item_id) + "').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#Ventana agregar suministro factura orden de compra (Suministros informe de recepción)
def ventana_agregar_suministro_factura_orden_compra2(request, pagina, informe_recepcion_id, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        items_factura = None
        try:
            items_factura = request.session['items_factura']
        except :
            pass
        if items_factura != None:
            items_factura_agregar = None
            try:
                items_factura_agregar = request.session['items_factura_agregar']
            except :
                pass
            if items_factura_agregar == None:
                items_factura_agregar = []

            if len(items_factura_agregar) == 0:
                for item_factura in items_factura:
                    if item_factura['informe_recepcion_id'] == informe_recepcion_id:
                        items_factura_agregar.append({'informe_recepcion_id': informe_recepcion_id, 'id': item_factura['id'], 'cantidad': item_factura['cantidad']})

            #Se almacena la variable en la sesion
            request.session['items_factura_agregar'] = items_factura_agregar

            #Actualización de la interfaz
            criterio = criterio.strip()
            informe_recepcion = InformeRecepcion.objects.get(id=informe_recepcion_id, orden_compra__proyecto=proyecto)
            suministros = informe_recepcion.get_suministros_agrupados_suministro(criterio=criterio)
            suministros_informe_recepcion = []
            for suministro in suministros:
                suministro_informe_recepcion = {'suministro': suministro, 'cantidad_suministro_nueva_factura': ''}
                for item_factura_agregar in items_factura_agregar:
                    if item_factura_agregar['id'] == suministro.suministro.suministro_orden_compra_item.suministro.id:
                        suministro_informe_recepcion['cantidad_suministro_nueva_factura'] = item_factura_agregar['cantidad']
                suministros_informe_recepcion.append(suministro_informe_recepcion)
            pag = Paginador(request, suministros_informe_recepcion, 20, pagina)
            render = render_to_string('ajax/suministrosinformerecepcionsearchfacturaordencompraadd.html', {'user': user, 'informe_recepcion': informe_recepcion, 'suministros_informe_recepcion': pag, 'criterio': criterio, 'proyecto': proyecto})
            dajax.assign('#light','innerHTML', render)
            dajax.script("document.getElementById('fade').style.display='block';")
            dajax.script("document.getElementById('light').style.display='block';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_item_factura_orden_compra2(request, pagina, suministro_id, informe_recepcion_id, cantidad, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        items_factura = None
        items_factura_agregar = None
        try:
            items_factura = request.session['items_factura']
            items_factura_agregar = request.session['items_factura_agregar']
        except :
            pass
        if items_factura != None and items_factura_agregar != None:
            informe_recepcion = InformeRecepcion.objects.get(id=informe_recepcion_id)
            suministro = informe_recepcion.get_suministro(suministro_id)
            error_cantidad = validar_cadena(cantidad)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float_digitos(cantidad)
                if error_cantidad == '':
                    error_cantidad = validar_cantidad_float(cantidad)
                    if error_cantidad == '':
                        cantidad = float(cantidad)
                        error_cantidad = validar_cantidad_float_0(cantidad)
                        if error_cantidad == '':
                            #Verificar si la cantidad a registrar esta disponible
                            if cantidad <= round(suministro.cantidad - suministro.cantidad_facturada, 2):
                                existe_item_factura = False
                                for item_factura_agregar in items_factura_agregar:
                                    if item_factura_agregar['informe_recepcion_id'] == informe_recepcion_id and item_factura_agregar['id'] == suministro_id:
                                        item_factura_agregar['cantidad'] = cantidad
                                        existe_item_factura = True
                                if existe_item_factura == False:
                                    item_factura = {'informe_recepcion_id': suministro.informe_recepcion.id, 'id': suministro_id, 'cantidad': cantidad}
                                    items_factura_agregar.append(item_factura)
                            else:
                                error_cantidad = 'La cantidad no debe ser mayor a la cantidad actual en el informe de recepcion'
                        else:
                            if cantidad == 0:
                                error_cantidad = ''
                                for item_factura_agregar in items_factura_agregar:
                                    if item_factura_agregar['informe_recepcion_id'] == informe_recepcion_id and item_factura_agregar['id'] == suministro_id:
                                        items_factura_agregar.remove(item_factura_agregar)
            request.session['items_factura_agregar'] = items_factura_agregar
            error = {}
            if error_cantidad != '':
                error = {'id': suministro_id, 'value': cantidad, 'error': error_cantidad}
            #Actualización de la interfaz
            criterio = criterio.strip()
            informe_recepcion = InformeRecepcion.objects.get(id=informe_recepcion_id, orden_compra__proyecto=proyecto)
            suministros = informe_recepcion.get_suministros_agrupados_suministro(criterio=criterio)
            suministros_informe_recepcion = []
            for suministro in suministros:
                suministro_informe_recepcion = {'suministro': suministro, 'cantidad_suministro_nueva_factura': ''}
                for item_factura_agregar in items_factura_agregar:
                    if item_factura_agregar['id'] == suministro.suministro.suministro_orden_compra_item.suministro.id:
                        suministro_informe_recepcion['cantidad_suministro_nueva_factura'] = item_factura_agregar['cantidad']
                suministros_informe_recepcion.append(suministro_informe_recepcion)
            pag = Paginador(request, suministros_informe_recepcion, 20, pagina)
            render = render_to_string('ajax/suministrosinformerecepcionsearchfacturaordencompraadd.html', {'user': user, 'informe_recepcion': informe_recepcion, 'suministros_informe_recepcion': pag, 'criterio': criterio, 'proyecto': proyecto, 'error': error})
            dajax.assign('#light','innerHTML', render)
            if error_cantidad != '':
                dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_cantidad_item_factura_orden_compra2(request, pagina, suministro_id, informe_recepcion_id, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        items_factura = None
        items_factura_agregar = None
        try:
            items_factura = request.session['items_factura']
            items_factura_agregar = request.session['items_factura_agregar']
        except :
            pass
        if items_factura != None and items_factura_agregar != None:
            for item_factura_agregar in items_factura_agregar:
                if item_factura_agregar['id'] == suministro_id:
                    error = {'id': suministro_id, 'value': item_factura_agregar['cantidad'], 'error': ''}
            #Actualización de la interfaz
            criterio = criterio.strip()
            informe_recepcion = InformeRecepcion.objects.get(id=informe_recepcion_id, orden_compra__proyecto=proyecto)
            suministros = informe_recepcion.get_suministros_agrupados_suministro(criterio=criterio)
            suministros_informe_recepcion = []
            for suministro in suministros:
                suministro_informe_recepcion = {'suministro': suministro, 'cantidad_suministro_nueva_factura': ''}
                for item_factura_agregar in items_factura_agregar:
                    if item_factura_agregar['id'] == suministro.suministro.suministro_orden_compra_item.suministro.id:
                        suministro_informe_recepcion['cantidad_suministro_nueva_factura'] = item_factura_agregar['cantidad']
                suministros_informe_recepcion.append(suministro_informe_recepcion)
            pag = Paginador(request, suministros_informe_recepcion, 20, pagina)
            render = render_to_string('ajax/suministrosinformerecepcionsearchfacturaordencompraadd.html', {'user': user, 'informe_recepcion': informe_recepcion, 'suministros_informe_recepcion': pag, 'criterio': criterio, 'proyecto': proyecto, 'error': error})
            dajax.assign('#light','innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_"+str(suministro_id)+"').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_items_factura_orden_compra2(request, informe_recepcion_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        items_factura = None
        items_factura_agregar = None
        try:
            items_factura = request.session['items_factura']
            items_factura_agregar = request.session['items_factura_agregar']
        except :
            pass
        if items_factura != None and items_factura_agregar != None:
            #Elimina los items que no se asigno valor
            items_eliminar = []
            for item_factura in items_factura:
                if int(item_factura['informe_recepcion_id']) == int(informe_recepcion_id):
                    eliminar_item = True
                    for item_factura_agregar in items_factura_agregar:
                        if int(item_factura['id']) == int(item_factura_agregar['id']):
                            eliminar_item = False
                    if eliminar_item == True:
                        items_eliminar.append(item_factura)

            for item_eliminar in items_eliminar:
                items_factura.remove(item_eliminar)

            #Actualiza la lista de items de la factura
            for item_factura_agregar in items_factura_agregar:
                agregar_nuevo_item = True
                for item_factura in items_factura:
                    if item_factura['informe_recepcion_id'] == informe_recepcion_id:
                        if item_factura['id'] == item_factura_agregar['id']:
                            item_factura['cantidad'] = item_factura_agregar['cantidad']
                            agregar_nuevo_item = False
                if agregar_nuevo_item == True:
                    items_factura.append(item_factura_agregar)

            request.session['items_factura'] = items_factura
            del request.session['items_factura_agregar']
            
            dajax.script("document.getElementById('fade').style.display='none';")
            dajax.script("document.getElementById('light').style.display='none';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def cancelar_agregar_items_factura_orden_compra2(request, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        items_factura = None
        items_factura_agregar = None
        try:
            items_factura = request.session['items_factura']
            items_factura_agregar = request.session['items_factura_agregar']
        except :
            pass
        if items_factura != None and items_factura_agregar != None:
            #Elimina la variable temporal de la session
            del request.session['items_factura_agregar']

            dajax.script("document.getElementById('fade').style.display='none';")
            dajax.script("document.getElementById('light').style.display='none';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_item_factura_orden_compra_add2(request, suministro_id, informe_recepcion_id, pagina, proveedor_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        items_factura = None
        try:
            items_factura = request.session['items_factura']
        except :
            pass
        if items_factura != None:
            #Actualiza la lista de items de la factura
            for item_factura in items_factura:
                if item_factura['informe_recepcion_id'] == informe_recepcion_id and item_factura['id'] == suministro_id:
                    items_factura.remove(item_factura)

            request.session['items_factura'] = items_factura

            proveedor = Proveedor.objects.get(id=proveedor_id)
            #Visualiza la interfaz
            discriminacion_valores = {'subtotal': 0, 'valor_iva': 0, 'valor_total': 0}
            lista_items_factura = []
            for item_factura in items_factura:
                informe_recepcion = InformeRecepcion.objects.get(id=item_factura['informe_recepcion_id'])
                suministro_informe_recepcion = informe_recepcion.get_suministro(item_factura['id'])
                precio_suministro = suministro_informe_recepcion.suministro.suministro_orden_compra_item.precio
                iva_suministro = suministro_informe_recepcion.suministro.suministro_orden_compra_item.iva_suministro
                subtotal_item = round(item_factura['cantidad'] * precio_suministro, 2)
                valor_iva_item = round(subtotal_item * iva_suministro, 2)
                valor_total_item = round(subtotal_item + valor_iva_item, 2)
                lista_items_factura.append({'suministro': suministro_informe_recepcion, 'cantidad_suministro_nueva_factura': item_factura['cantidad'], 'subtotal': subtotal_item, 'valor_iva': valor_iva_item, 'valor_total': valor_total_item})
                discriminacion_valores['subtotal'] = round(discriminacion_valores['subtotal'] + subtotal_item, 2)
                discriminacion_valores['valor_iva'] = round(discriminacion_valores['valor_iva'] + valor_iva_item, 2)
            discriminacion_valores['valor_total'] = round(discriminacion_valores['subtotal'] + discriminacion_valores['valor_iva'], 2)
                
            #Valida la paginacion
            if pagina > (len(lista_items_factura) // 20):
                pagina = pagina - 1
            if pagina <= 0:
                pagina = 1
            pag = Paginador(request, lista_items_factura, 20, pagina)
            render = render_to_string('ajax/itemsfacturaordencompraadd.html', {'user': user, 'proveedor': proveedor, 'items_factura': pag, 'discriminacion_valores': discriminacion_valores, 'proyecto': proyecto })
            dajax.assign('#id_reporte_items', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_cantidad_item_factura_orden_compra_add2(request, pagina, suministro_id, informe_recepcion_id, proveedor_id, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        items_factura = None
        try:
            items_factura = request.session['items_factura']
        except :
            pass
        if items_factura != None:
            proveedor = Proveedor.objects.get(id=proveedor_id)
            #Visualiza la interfaz
            discriminacion_valores = {'subtotal': 0, 'valor_iva': 0, 'valor_total': 0}
            lista_items_factura = []
            error = {}
            for item_factura in items_factura:
                informe_recepcion = InformeRecepcion.objects.get(id=item_factura['informe_recepcion_id'])
                suministro_informe_recepcion = informe_recepcion.get_suministro(item_factura['id'])
                precio_suministro = suministro_informe_recepcion.suministro.suministro_orden_compra_item.precio
                iva_suministro = suministro_informe_recepcion.suministro.suministro_orden_compra_item.iva_suministro
                subtotal_item = round(item_factura['cantidad'] * precio_suministro, 2)
                valor_iva_item = round(subtotal_item * iva_suministro, 2)
                valor_total_item = round(subtotal_item + valor_iva_item, 2)
                lista_items_factura.append({'suministro': suministro_informe_recepcion, 'cantidad_suministro_nueva_factura': item_factura['cantidad'], 'subtotal': subtotal_item, 'valor_iva': valor_iva_item, 'valor_total': valor_total_item})
                if item_factura['id'] == suministro_id and item_factura['informe_recepcion_id'] == informe_recepcion_id:
                    error = {'id': suministro_id, 'informe_recepcion_id': informe_recepcion_id, 'value': item_factura['cantidad'], 'error': ''}
                discriminacion_valores['subtotal'] = round(discriminacion_valores['subtotal'] + subtotal_item, 2)
                discriminacion_valores['valor_iva'] = round(discriminacion_valores['valor_iva'] + valor_iva_item, 2)
            discriminacion_valores['valor_total'] = round(discriminacion_valores['subtotal'] + discriminacion_valores['valor_iva'], 2)

            pag = Paginador(request, lista_items_factura, 20, pagina)
            render = render_to_string('ajax/itemsfacturaordencompraadd.html', {'user': user, 'proveedor': proveedor, 'items_factura': pag, 'discriminacion_valores': discriminacion_valores, 'proyecto': proyecto, 'error': error})
            dajax.assign('#id_reporte_items', 'innerHTML', render)
            dajax.script("document.getElementById('id_text_cantidad_" + str(suministro_id) + "_" + str(informe_recepcion_id) + "').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_cantidad_item_factura_orden_compra_add2(request, suministro_id, informe_recepcion_id, cantidad, pagina, proveedor_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        items_factura = None
        try:
            items_factura = request.session['items_factura']
        except :
            pass
        if items_factura != None:
            informe_recepcion = InformeRecepcion.objects.get(id=informe_recepcion_id)
            suministro = informe_recepcion.get_suministro(suministro_id)
            error_cantidad = validar_cantidad_float(cantidad)
            if error_cantidad == '':
                error_cantidad = validar_cantidad_float_digitos(cantidad)
                if error_cantidad == '':
                    cantidad = float(cantidad)
                    error_cantidad = validar_cantidad_float_0(cantidad)
                    if error_cantidad == '':
                        if cantidad <= round(suministro.cantidad - suministro.cantidad_facturada, 2):
                            for item_factura in items_factura:
                                if item_factura['id'] == suministro_id and item_factura['informe_recepcion_id'] == informe_recepcion_id:
                                    item_factura['cantidad'] = cantidad
                        else:
                            error_cantidad = u'La cantidad no debe ser mayor a la cantidad recibida en el informe de recepcion'
            error = {}
            if error_cantidad != '':
                error = { 'id': suministro_id, 'informe_recepcion_id': informe_recepcion_id, 'value': cantidad, 'error': error_cantidad }

            proveedor = Proveedor.objects.get(id=proveedor_id)
            #Visualiza la interfaz
            discriminacion_valores = {'subtotal': 0, 'valor_iva': 0, 'valor_total': 0}
            lista_items_factura = []
            for item_factura in items_factura:
                informe_recepcion = InformeRecepcion.objects.get(id=item_factura['informe_recepcion_id'])
                suministro_informe_recepcion = informe_recepcion.get_suministro(item_factura['id'])
                precio_suministro = suministro_informe_recepcion.suministro.suministro_orden_compra_item.precio
                iva_suministro = suministro_informe_recepcion.suministro.suministro_orden_compra_item.iva_suministro
                subtotal_item = round(item_factura['cantidad'] * precio_suministro, 2)
                valor_iva_item = round(subtotal_item * iva_suministro, 2)
                valor_total_item = round(subtotal_item + valor_iva_item, 2)
                lista_items_factura.append({'suministro': suministro_informe_recepcion, 'cantidad_suministro_nueva_factura': item_factura['cantidad'], 'subtotal': subtotal_item, 'valor_iva': valor_iva_item, 'valor_total': valor_total_item})
                discriminacion_valores['subtotal'] = round(discriminacion_valores['subtotal'] + subtotal_item, 2)
                discriminacion_valores['valor_iva'] = round(discriminacion_valores['valor_iva'] + valor_iva_item, 2)
            discriminacion_valores['valor_total'] = round(discriminacion_valores['subtotal'] + discriminacion_valores['valor_iva'], 2)
                
            pag = Paginador(request, lista_items_factura, 20, pagina)
            render = render_to_string('ajax/itemsfacturaordencompraadd.html', {'user': user, 'proveedor': proveedor, 'items_factura': pag, 'discriminacion_valores': discriminacion_valores, 'proyecto': proyecto, 'error': error})
            dajax.assign('#id_reporte_items', 'innerHTML', render)
            if error_cantidad != '':
                dajax.script("document.getElementById('id_text_cantidad_" + str(suministro_id) + "_" + str(informe_recepcion_id) + "').select();")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def facturar_todos_suministros_informe_recepcion_factura_orden_compra_add2(request, informe_recepcion_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        items_factura = None
        items_factura_agregar = None
        try:
            items_factura = request.session['items_factura']
            items_factura_agregar = request.session['items_factura_agregar']
        except :
            pass
        if items_factura != None and items_factura_agregar != None:
            #Actualización de la interfaz
            informe_recepcion = InformeRecepcion.objects.get(id=informe_recepcion_id, orden_compra__proyecto=proyecto)
            suministros = informe_recepcion.get_suministros_agrupados_suministro()
            suministros_informe_recepcion = []
            for suministro in suministros:
                suministro_informe_recepcion = {'suministro': suministro, 'cantidad_suministro_nueva_factura': ''}
                agregar_suministro = True
                for item_factura_agregar in items_factura_agregar:
                    if int(item_factura_agregar['id']) == suministro.suministro.suministro_orden_compra_item.suministro.id and int(item_factura_agregar['informe_recepcion_id']) == int(informe_recepcion_id):
                        suministro_informe_recepcion['cantidad_suministro_nueva_factura'] = item_factura_agregar['cantidad']
                        agregar_suministro = False
                if agregar_suministro == True:
                    if suministro.cantidad_facturada < suministro.cantidad:
                        cantidad_facturar = round(suministro.cantidad - suministro.cantidad_facturada, 2)
                        suministro_informe_recepcion['cantidad_suministro_nueva_factura'] = cantidad_facturar
                        item_factura = {'informe_recepcion_id': informe_recepcion_id, 'id': suministro.suministro.suministro_orden_compra_item.suministro.id, 'cantidad': cantidad_facturar}
                        items_factura_agregar.append(item_factura)

                suministros_informe_recepcion.append(suministro_informe_recepcion)
            request.session['items_factura_agregar'] = items_factura_agregar
            pag = Paginador(request, suministros_informe_recepcion, 20, 1)
            render = render_to_string('ajax/suministrosinformerecepcionsearchfacturaordencompraadd.html', {'user': user, 'informe_recepcion': informe_recepcion, 'suministros_informe_recepcion': pag, 'proyecto': proyecto})
            dajax.assign('#light','innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#Asignar numero de factura acta_recibo_obra
def asignar_numero_factura_acta_recibo_obra2(request, acta_recibo_obra_id, numero_factura, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_actareciboobra' in user.get_all_permissions() or 'inverboy.change_actareciboobra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                acta_recibo_obra = ActaReciboObra.objects.get(id=acta_recibo_obra_id, orden_servicio__proyecto=proyecto)
                numero_factura = numero_factura.strip()
                error_numero_factura = ''
                validaciones = Validator().append([
                    Field('numero_factura', numero_factura).append([
                        IsRequired('Este campo es obligatorio.'), Regex("^[ A-Za-z0-9]{1,40}$", error='El numero de factura no tiene el formato correcto.'),
                    ]),
                ]
                ).run(True).pop()
                if validaciones['passed'] == True:
                    acta_recibo_obra.numero_factura = numero_factura
                    acta_recibo_obra.save()
                    dajax.redirect('/inverboy/home/actasreciboobraproyectodetails/' + str(acta_recibo_obra_id) + '/' + str(proyecto_id)+'/')
                else:
                    for error in validaciones['errors']:
                        error_numero_factura = error
                dajax.script("document.getElementById('id_label_error_numero_factura').innerHTML = '" + error_numero_factura + "';")
                if error_numero_factura != '':
                    dajax.script("document.getElementById('id_text_numero_factura').select();")
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#Cerrar numero factura acta recibo de obra ( No se puede modificar numero de factura)
def cerrar_numero_factura_acta_recibo_obra2(request, acta_recibo_obra_id, numero_factura, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.assignchangepermission_ordenservicio' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                acta_recibo_obra = ActaReciboObra.objects.get(id=acta_recibo_obra_id, orden_servicio__proyecto=proyecto)
                numero_factura = numero_factura.strip()
                error_numero_factura = validar_cadena(numero_factura)
                if error_numero_factura == '':
                    acta_recibo_obra.numero_factura = numero_factura
                    acta_recibo_obra.cerrado_numero_factura = True
                    acta_recibo_obra.save()
                    dajax.redirect('/inverboy/home/actasreciboobraproyectodetails/' + str(acta_recibo_obra_id) + '/' + str(proyecto_id)+'/')

                dajax.script("document.getElementById('id_label_error_numero_factura').innerHTML = '" + error_numero_factura + "';")
                if error_numero_factura != '':
                    dajax.script("document.getElementById('id_text_numero_factura').select();")
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#asignar descuento
def asignar_descuento_acta_recibo_obra2(request, orden_servicio_id, proyecto_id, descuento):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if request.is_ajax():
            if 'inverboy.add_actareciboobra' in user.get_all_permissions():
                usuario = Usuario.objects.get(id=user.id)
                proyecto = Proyecto.objects.get(id=proyecto_id)
                orden_servicio = OrdenServicio.objects.get(id = orden_servicio_id)
                error_descuento = ''
                if descuento:
                    descuento = descuento.strip()
                    validaciones = Validator().append([
                        Field('descuento', descuento).append([
                            Regex("^[0-9]{1,40}$", error='Este campo no cumple con el formato requerido.'),
                        ]),
                    ]).run(True).pop()

                    if validaciones['passed'] == True:
                        dajax.script("$('#id_descuento').val('" + descuento + "');")
                        dajax.script("document.getElementById('id_descuento').readOnly=true;")
                        dajax.script("document.getElementById('id_btn_asignar_descuento').style.display='none';")
                        dajax.script("document.getElementById('id_btn_modificar_descuento').style.display='block';")

                    else:
                        for error in validaciones['errors']:
                            error_descuento = error
                        dajax.script("document.getElementById('id_descuento').readOnly=false;")
                        dajax.script("document.getElementById('id_descuento').select();")
                else:

                    dajax.script("document.getElementById('id_descuento').readOnly=false;")
                    dajax.script("document.getElementById('id_descuento').select();")
                    dajax.script("document.getElementById('id_btn_modificar_descuento').style.display='none';")
                    dajax.script("document.getElementById('id_btn_asignar_descuento').style.display='block';")
                dajax.script("$('#id_error_descuento').html('" + error_descuento + "');")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()












"""

** Funcion para mostrar en detalle las cantidades pendientes (por acta de recibo de obra), según los cortes de obra diarios
def detalles_cantidad_suministro_acta_recibo_obra_add2(request, suministro_id, fecha_inicio, fecha_fin, orden_servicio_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        permisos_usuario = user.get_all_permissions()
        #if validar_permiso_usuario(user.id, 'auth.view_group'):
        proyecto = Proyecto.objects.get(id=proyecto_id)
        orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
        fecha_inicio = fecha_inicio.strip()
        fecha_fin = fecha_fin.strip()
        error_fecha_inicio = ''
        if fecha_inicio != '':
            error_fecha_inicio = validar_fecha(fecha_inicio)
        error_fecha_fin = validar_fecha(fecha_fin)
        if error_fecha_inicio == '' and error_fecha_fin == '':
            if fecha_inicio == '':
                fecha_inicio_rango = '2013-01-01'
            else:
                fecha_inicio_rango = fecha_inicio
            if fecha_fin == '':
                fecha_fin = hoy
            suministros_cortes_diario_obra = SuministroCorteDiarioObra.objects.filter(corte_diario_obra__orden_servicio=orden_servicio, corte_diario_obra__estado=True, corte_diario_obra__fecha_corte__range=(fecha_inicio_rango, fecha_fin), suministro__suministro__suministro__suministro__id=suministro_id)

            qry_etiquetas_fechas = suministros_cortes_diario_obra.values('corte_diario_obra__fecha_corte')
            etiquetas_fechas = []
            for item in qry_etiquetas_fechas:
                item = item['corte_diario_obra__fecha_corte'].strftime("%Y-%m-%d")
                if not item in etiquetas_fechas:
                    etiquetas_fechas.append(item)

            qry_etiquetas_apus = suministros_cortes_diario_obra.values('suministro__suministro__suministro__apu_proyecto__id', 'suministro__suministro__suministro__apu_proyecto__nombre_apu')
            etiquetas_apus = []
            for item in qry_etiquetas_apus:
                if not item in etiquetas_apus:
                    etiquetas_apus.append(item)

            matriz = [ [ 0 for i in range(len(etiquetas_fechas)+1) ] for j in range(len(etiquetas_apus)+1) ]

            for d1 in range(1, len(etiquetas_apus)+1):
                matriz[d1][0] = etiquetas_apus[d1-1]

            for d1 in range(1, len(etiquetas_fechas)+1):
                matriz[0][d1] = etiquetas_fechas[d1-1]

            for d1 in range(1, len(etiquetas_apus)+1):
                for d2 in range(1, len(etiquetas_fechas)+1):
                    for suministro_cortes_diario_obra in suministros_cortes_diario_obra:
                        suministro_cortes_diario_obra.cantidad
                        print '-------------------------------------------------------------------------'
                        print 'str(suministro_cortes_diario_obra.corte_diario_obra.fecha_corte.date())'+str(suministro_cortes_diario_obra.corte_diario_obra.fecha_corte.date())
                        print 'etiquetas_fechas[d1-1]'+etiquetas_fechas[d2-1]
                        print 'suministro_cortes_diario_obra.suministro.suministro.suministro.apu_proyecto.id'+str(suministro_cortes_diario_obra.suministro.suministro.suministro.apu_proyecto.id)
                        print 'etiquetas_apus[d2-1][suministro__suministro__suministro__apu_proyecto__id]'+str(etiquetas_apus[d1-1]['suministro__suministro__suministro__apu_proyecto__id'])
                        print '-------------------------------------------------------------------------'
                        if str(suministro_cortes_diario_obra.corte_diario_obra.fecha_corte.date()) == etiquetas_fechas[d2-1] and suministro_cortes_diario_obra.suministro.suministro.suministro.apu_proyecto.id == etiquetas_apus[d1-1]['suministro__suministro__suministro__apu_proyecto__id']:
                            matriz[d1][d2] = suministro_cortes_diario_obra

            render =  render_to_string('ajax/detallescantidadsuministroactareciboobraadd.html', {'user': user, 'permisos': permisos_usuario, 'matriz': matriz })
            dajax.assign('#light','innerHTML', render)
            dajax.script("document.getElementById('fade').style.display = 'block';")
            dajax.script("document.getElementById('light').style.display = 'block';")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

"""