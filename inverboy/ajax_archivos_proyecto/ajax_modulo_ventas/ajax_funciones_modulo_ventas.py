# -*- encoding: utf-8 -*-
__author__ = 'Diego Reyes'

from inverboy.models import *
from dajaxice.core import dajaxice_functions
from dajax.core import Dajax
from django.template.loader import render_to_string

from inverboy.models import Usuario, Proyecto, SeccionProyecto, PreguntaEncuesta, RespuestaPreguntaEncuesta, Cliente, NotificacionVenta, Municipio, ContactoCliente, TipoInmueble, Inmueble, AdicionalAgrupacion, EstadoContratoVenta, PagoEntidadContratoVenta, PagoEfectivoContratoVenta, AbonoPagoEfectivoContratoVenta,EntidadBancaria,NumeroCuenta

#from validator.core import Validator, Field
#from validator.rules import *
from inverboy.validaciones.validaciones import *

from django.template import RequestContext

from inverboy.forms import ContactoClienteForm, PreguntaEncuestaForm, NotificacionVentaForm, RespuestaNotificacionVentaForm, ContratoVentaForm, PagoEntidadContratoVentaForm, PagoEfectivoContratoVentaForm, AbonoPagoEntidadContratoVentaForm, AbonoPagoEfectivoContratoVentaForm

#CONSULTAS ANIDADAS
from django.db.models import Q

from django.contrib.humanize.templatetags.humanize import intcomma

# PAGINACION
from inverboy.paginator import *


def agregar_pregunta_nueva_encuesta2(request, datos):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        preguntas_encuesta = None
        try:
            preguntas_encuesta = request.session['preguntas_encuesta']
        except :
            pass
        if preguntas_encuesta != None:
            if request.is_ajax():
                request.POST = deserialize_form(datos)
                form = PreguntaEncuestaForm(request.POST)
                if form.is_valid():
                    nueva_pregunta = PreguntaEncuesta()
                    nueva_pregunta.texto = form.cleaned_data['texto_pregunta']
                    nueva_pregunta.respuestas = []

                    # Campos de respuestas
                    numero_respuestas = len(form.fields)
                    for consecutivo_respuestas in range(1, numero_respuestas):
                        nueva_pregunta.respuestas.append(form.cleaned_data['texto_respuesta_' + str(consecutivo_respuestas)])
                    preguntas_encuesta.append(nueva_pregunta)
                    render = render_to_string('ajax/ventas/preguntasencuesta.html', {'preguntas': preguntas_encuesta}, context_instance=RequestContext(request))
                    dajax.assign('#reporte_preguntas', 'innerHTML', render)
                    dajax.script("nueva_pregunta = false;")
                else:
                    render = render_to_string('ajax/ventas/nuevapreguntaencuesta.html', {'form': form}, context_instance=RequestContext(request))
                    dajax.assign('#id_panel_pregunta', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

def eliminar_pregunta_nueva_encuesta2(request, indice):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        preguntas_encuesta = None
        try:
            preguntas_encuesta = request.session['preguntas_encuesta']
        except :
            pass
        if preguntas_encuesta != None:
            if request.is_ajax():
                if request.method == 'POST':
                    preguntas_encuesta.pop(int(indice))
                    request.session['preguntas_encuesta'] = preguntas_encuesta
                    render = render_to_string('ajax/ventas/preguntasencuesta.html', {'preguntas': preguntas_encuesta}, context_instance=RequestContext(request))
                    dajax.assign('#reporte_preguntas', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def validar_identificacion_nuevo_cliente2(request, identificacion, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        contactos_cliente = None
        try:
            contactos_cliente = request.session['contactos_cliente']
        except :
            pass
        if contactos_cliente != None:
            identificacion = identificacion.strip()
            error_identificacion = ''
            validaciones = Validator().append([
                Field('identificacion', identificacion).append([
                    IsRequired('Este campo es obligatorio.'), Regex("^[1-9]{1}[0-9]{6,9}$", error='Este campo no cumple con el formato requerido.'),
                ]),
            ]).run(True).pop()

            if validaciones['passed'] == True:
                cliente = None
                try:
                    cliente = Cliente.objects.get(identificacion=identificacion)
                except :
                    pass
                if cliente == None:
                    pass
                else:
                    if 'inverboy.view_cliente' in user.get_all_permissions():
                        cliente = Cliente.objects.get(identificacion=identificacion)
                        dajax.redirect('/inverboy/home/detallescliente/' + str(cliente.id) + '/' + str(proyecto_id) + '/')
                    else:
                        error_identificacion = 'La identificación ya se encuentra registrada en el sistema.'
            else:
                for error in validaciones['errors']:
                    error_identificacion = error
                error_identificacion = 'Error campo identificacion ' + error_identificacion
            dajax.script("document.getElementById('id_label_error').innerHTML = '" + error_identificacion + "';")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def ventana_contacto_cliente2(request, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        contactos = None
        try:
            contactos = request.session['contactos_cliente']
        except :
            pass
        if contactos != None:
            form2 = ContactoClienteForm()
            form2.fields['municipio_contacto'].queryset = Municipio.objects.filter(id=0)
            render = render_to_string('ajax/ventas/nuevocontactocliente.html', {'user': user, 'form2': form2, 'change': 0}, context_instance=RequestContext(request))
            dajax.assign('#light', 'innerHTML', render)
            dajax.script("document.getElementById('light').style.display='block';")
            dajax.script("document.getElementById('fade').style.display='block';")
            dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_contacto_cliente2(request, datos):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        contactos = None
        try:
            contactos = request.session['contactos_cliente']
        except :
            pass
        if contactos != None:
            if request.is_ajax():
                if request.method == 'POST':
                    request.POST = deserialize_form(datos)
                    form2 = ContactoClienteForm(request.POST)
                    if form2.is_valid():
                        contacto = ContactoCliente()
                        contacto.nombre = form2.cleaned_data['nombre_contacto'].strip()
                        contacto.telefono = form2.cleaned_data['telefono_contacto'].strip()
                        contacto.municipio = form2.cleaned_data['municipio_contacto']
                        contacto.email = form2.cleaned_data['email_contacto']
                        contactos.append(contacto)
                        request.session['contactos_cliente'] = contactos
                        render = render_to_string('ajax/ventas/contactoscliente.html', {'user': user, 'contactos': contactos})
                        dajax.assign('#reporte_contactos', 'innerHTML', render)
                        dajax.script("document.getElementById('light').style.display='none';")
                        dajax.script("document.getElementById('fade').style.display='none';")
                        dajax.alert('Contacto agregado correctamente')
                        
                    else:
                        render = render_to_string('ajax/ventas/nuevocontactocliente.html', {'user': user, 'form2': form2, 'change': 0}, context_instance=RequestContext(request))
                        dajax.assign('#light', 'innerHTML', render)
                        dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def deserialize_form(data):
    """
    Create a new QueryDict from a serialized form.
    """
    from django.http import QueryDict
    data = QueryDict(query_string=unicode(data).encode('utf-8'))
    return data


def ventana_modificar_contacto_cliente2(request, indice):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        contactos = None
        try:
            contactos = request.session['contactos_cliente']
        except :
            pass
        if contactos != None:
            contacto = contactos[int(indice)]
            form2 = ContactoClienteForm(initial={'nombre_contacto': contacto.nombre, 'telefono_contacto': contacto.telefono, 'departamento_contacto': contacto.municipio.departamento, 'municipio_contacto': contacto.municipio, 'email_contacto': contacto.email})
            render = render_to_string('ajax/ventas/nuevocontactocliente.html', {'user': user, 'form2': form2, 'indice': indice, 'change': 1})
            dajax.assign('#light', 'innerHTML', render)
            dajax.script("document.getElementById('light').style.display='block';")
            dajax.script("document.getElementById('fade').style.display='block';")
            dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_contacto_cliente2(request, datos):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        contactos = None
        try:
            contactos = request.session['contactos_cliente']
        except :
            pass
        if contactos != None:
            if request.is_ajax():
                if request.method == 'POST':
                    request.POST = deserialize_form(datos)
                    form2 = ContactoClienteForm(request.POST)
                    if form2.is_valid():
                        contacto = contactos[int(request.POST['indice_contacto'])]
                        contacto.nombre = form2.cleaned_data['nombre_contacto'].strip()
                        contacto.telefono = form2.cleaned_data['telefono_contacto'].strip()
                        contacto.municipio = form2.cleaned_data['municipio_contacto']
                        contacto.email = form2.cleaned_data['email_contacto']
                        request.session['contactos_cliente'] = contactos
                        render = render_to_string('ajax/ventas/contactoscliente.html', {'user': user, 'contactos': contactos})
                        dajax.assign('#reporte_contactos', 'innerHTML', render)
                        dajax.script("document.getElementById('light').style.display='none';")
                        dajax.script("document.getElementById('fade').style.display='none';")
                        dajax.alert('Contacto modificado correctamente')
                    else:
                        departamento_contacto = request.POST['departamento_contacto']
                        if departamento_contacto == '':
                            departamento_contacto = 0
                        form2.fields['municipio_contacto'].queryset = Municipio.objects.filter(departamento=departamento_contacto)
                        render = render_to_string('ajax/ventas/nuevocontactocliente.html', {'user': user, 'form2': form2, 'change': 1}, context_instance=RequestContext(request))
                        dajax.assign('#light', 'innerHTML', render)
                        dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_contacto_cliente2(request, indice):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        contactos = None
        try:
            contactos = request.session['contactos_cliente']
        except :
            pass
        if contactos != None:
            contactos.pop(int(indice))
            request.session['contactos_cliente'] = contactos
            render = render_to_string('ajax/ventas/contactoscliente.html', {'user': user, 'contactos': contactos})
            dajax.assign('#reporte_contactos', 'innerHTML', render)
            dajax.script("document.getElementById('light').style.display='none';")
            dajax.script("document.getElementById('fade').style.display='none';")
            dajax.alert('Contacto eliminado correctamente')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def asignar_modificacion_inmueble_proyecto2(request, permiso, inmueble_id, pagina, tipo_inmueble_id, seccion_proyecto_id, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.assignchangepermission_inmueble' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            inmueble = proyecto.inmueble_set.get(id=inmueble_id)
            if permiso == 1:
                inmueble.permiso_modificar = True
            elif permiso == 0:
                inmueble.permiso_modificar = False
            inmueble.save()

            tipo_inmueble = TipoInmueble(id='')
            seccion_proyecto = SeccionProyecto(id='')
            tipo_inmueble_id = tipo_inmueble_id.strip()
            seccion_proyecto_id = seccion_proyecto_id.strip()
            criterio = criterio.strip()
            inmuebles = proyecto.inmueble_set.all()
            if tipo_inmueble_id != '':
                tipo_inmueble = TipoInmueble.objects.get(id=tipo_inmueble_id)
                inmuebles = inmuebles.filter(tipo_inmueble=tipo_inmueble)
            if seccion_proyecto_id != '':
                seccion_proyecto = proyecto.seccionproyecto_set.get(id=seccion_proyecto_id)
                inmuebles = inmuebles.filter(seccion_proyecto=seccion_proyecto)
            if criterio != '':
                inmuebles = inmuebles.filter(identificacion=criterio)

            tipo_inmuebles = TipoInmueble.objects.all()
            secciones_proyecto = proyecto.seccionproyecto_set.all()
            pag = Paginador(request, inmuebles, 20, pagina)
            user = request.user
            render = render_to_string('ajax/ventas/busquedainmueble.html', {'user': user, 'inmuebles': pag, 'tipo_inmuebles': tipo_inmuebles, 'actual_tipo_inmueble': tipo_inmueble, 'secciones_proyecto': secciones_proyecto, 'actual_seccion_proyecto': seccion_proyecto, 'criterio': criterio, 'proyecto': proyecto})
            dajax.assign('#id_reporte_inmuebles', 'innerHTML', render)
            dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def informacion_cliente2(request, cliente_id, indice):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        cliente = Cliente.objects.get(id=cliente_id)
        render = render_to_string('ajax/ventas/informacioncliente.html', {'user': user, 'cliente': cliente})
        dajax.script("document.getElementById('flotanteClientes').style.top=((document.getElementById('id_fila_cliente_"+str(indice)+"').offsetTop) + 62) + 'px';")
        dajax.script("document.getElementById('flotanteClientes').style.display='block';")
        dajax.assign('#flotanteClientes','innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def validar_identificacion_inmueble2(request, identificacion, identificacion_actual, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        identificacion = identificacion.strip()
        error_identificacion = ''
        validaciones = Validator().append([
            Field('identificacion', identificacion).append([
                IsRequired('Este campo es obligatorio.'), Regex("^[ A-Za-z0-9_-]+$", error='Este campo no cumple con el formato requerido.'),
            ]),
        ]).run(True).pop()

        if validaciones['passed'] == True:
            if identificacion_actual == None:
                validar_identificacion, form = validate_unique_field(Inmueble, {'identificacion': identificacion, 'proyecto': proyecto})
            else:
                identificacion_actual = identificacion_actual.strip()
                validar_identificacion, form = validate_unique_field(Inmueble, {'identificacion': identificacion, 'proyecto': proyecto}, exclude_initials_values={'identificacion': identificacion_actual, 'proyecto': proyecto})
            if validar_identificacion:
                error_identificacion = 'La identificación ya se encuentra registrada en el sistema'
        else:
            for error in validaciones['errors']:
                error_identificacion = error
            error_identificacion = 'Error campo identificacion ' + error_identificacion
        dajax.script("document.getElementById('id_label_error').innerHTML = '" + error_identificacion + "';")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_input_precio_asignacion_individual_precios2(request, inmueble_id, tipo_inmueble_id, seccion_proyecto_id, criterio, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_inmueble' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            inmueble = proyecto.lista_inmuebles().get(id=inmueble_id)

            # Actualiza la interfaz
            tipo_inmueble = TipoInmueble()
            seccion_proyecto = SeccionProyecto()
            error = {'id': int(inmueble_id), 'value_precio': str(inmueble.valor), 'value_lista_precios': str(inmueble.str_lista_precios()), 'error': ''}

            criterio = criterio.strip()

            # Solo los inmuebles que no se encuentran comprometidos
            inmuebles = proyecto.lista_inmuebles().filter(item_agrupacion_inmueble__agrupacion_inmueble__agrupacion_contrato_venta=None)

            if tipo_inmueble_id != '':
                tipo_inmueble = TipoInmueble.objects.get(id=tipo_inmueble_id)
                inmuebles = inmuebles.filter(tipo_inmueble=tipo_inmueble)
            if seccion_proyecto_id != '':
                seccion_proyecto = proyecto.seccionproyecto_set.get(id=seccion_proyecto_id)
                inmuebles = inmuebles.filter(seccion_proyecto=seccion_proyecto)
            if criterio != '':
                inmuebles = inmuebles.filter(identificacion__icontains=criterio)

            pag = Paginador(request, inmuebles, len(inmuebles), 1)

            tipo_inmuebles = TipoInmueble.objects.all()
            secciones_proyecto = proyecto.lista_secciones()
            render = render_to_string('ajax/ventas/busquedainmuebleasignacionindividualprecios.html', {'user': user, 'inmuebles': pag, 'tipo_inmuebles': tipo_inmuebles, 'actual_tipo_inmueble': tipo_inmueble, 'secciones_proyecto': secciones_proyecto, 'actual_seccion_proyecto': seccion_proyecto, 'criterio': criterio, 'proyecto': proyecto, 'error': error})
            dajax.assign('#id_reporte_inmuebles','innerHTML', render)
            dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
            dajax.script("document.getElementById('id_text_precio_" + str(inmueble_id) + "').select();")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def asignar_precio_asignacion_individual_precios2(request, inmueble_id, precio, lista_precios, tipo_inmueble_id, seccion_proyecto_id, criterio, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_inmueble' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)

            precio = precio.strip()
            lista_precios = lista_precios.strip()

            error_precio = ''
            validaciones_precio = Validator().append([
                Field('precio', precio).append([
                    IsRequired('Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
                ]),
            ]).run(True).pop()

            error_lista_precios = ''
            validaciones_lista_precios = Validator().append([
                Field('lista_precios', lista_precios).append([
                    IsRequired('Este campo es obligatorio.'), Regex("^[0-9]{1,6}?$", error='La cantidad no tiene el formato correcto'),
                ]),
            ]).run(True).pop()

            if validaciones_precio['passed'] == True and validaciones_lista_precios['passed'] == True:
                inmueble = proyecto.lista_inmuebles().get(id=inmueble_id)
                inmueble.valor = precio
                inmueble.lista_precios = lista_precios
                inmueble.save()
            else:
                if validaciones_precio['passed'] == False:
                    for error in validaciones_precio['errors']:
                        error_precio = error

                if validaciones_lista_precios['passed'] == False:
                    for error in validaciones_lista_precios['errors']:
                        error_lista_precios = error

            error = {}
            if error_precio != '' or error_lista_precios != '':
                error = {'id': int(inmueble_id), 'value_precio': precio, 'error_precio': error_precio, 'value_lista_precios': lista_precios, 'error_lista_precios': error_lista_precios}

            # Actualiza la interfaz
            tipo_inmueble = TipoInmueble()
            seccion_proyecto = SeccionProyecto()
            
            criterio = criterio.strip()

            # Solo los inmuebles que no se encuentran comprometidos
            inmuebles = proyecto.lista_inmuebles().filter(item_agrupacion_inmueble__agrupacion_inmueble__agrupacion_contrato_venta=None)

            if tipo_inmueble_id != '':
                tipo_inmueble = TipoInmueble.objects.get(id=tipo_inmueble_id)
                inmuebles = inmuebles.filter(tipo_inmueble=tipo_inmueble)
            if seccion_proyecto_id != '':
                seccion_proyecto = proyecto.seccionproyecto_set.get(id=seccion_proyecto_id)
                inmuebles = inmuebles.filter(seccion_proyecto=seccion_proyecto)
            if criterio != '':
                inmuebles = inmuebles.filter(identificacion__icontains=criterio)

            pag = Paginador(request, inmuebles, len(inmuebles), 1)

            tipo_inmuebles = TipoInmueble.objects.all()
            secciones_proyecto = proyecto.lista_secciones()
            render = render_to_string('ajax/ventas/busquedainmuebleasignacionindividualprecios.html', {'user': user, 'inmuebles': pag, 'tipo_inmuebles': tipo_inmuebles, 'actual_tipo_inmueble': tipo_inmueble, 'secciones_proyecto': secciones_proyecto, 'actual_seccion_proyecto': seccion_proyecto, 'criterio': criterio, 'proyecto': proyecto, 'error': error})
            dajax.assign('#id_reporte_inmuebles','innerHTML', render)
            dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
            if error_precio != '':
                dajax.script("document.getElementById('id_text_precio_" + str(inmueble_id) + "').select();")
            elif error_lista_precios != '':
                dajax.script("document.getElementById('id_text_lista_precios_" + str(inmueble_id) + "').select();")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def busqueda_inmuebles_modificacion_masiva2(request, inmueble_id, seccion_proyecto_id, criterio, proyecto_id):
    from django.template.loader import render_to_string
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_inmueble' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)

            inmueble = proyecto.lista_inmuebles().get(id=inmueble_id)

            # Actualiza la interfaz
            seccion_proyecto = SeccionProyecto(id='')

            criterio = criterio.strip()

            # Solo se aplica la modificación masiva a inmuebles que no esten comprometidos
            inmuebles = proyecto.lista_inmuebles().filter(tipo_inmueble=inmueble.tipo_inmueble).exclude(id=inmueble_id)

            if seccion_proyecto_id != '':
                seccion_proyecto = proyecto.seccionproyecto_set.get(id=seccion_proyecto_id)
                inmuebles = inmuebles.filter(seccion_proyecto=seccion_proyecto)
            if criterio != '':
                inmuebles = inmuebles.filter(identificacion__icontains=criterio)

            items = len(inmuebles)
            if items == 0:
                items = 1
            pag = Paginador(request, inmuebles, items, 1)

            secciones_proyecto = proyecto.lista_secciones()
            render = render_to_string('ajax/ventas/busquedainmueblesmodificacionmasiva.html', {'user': user, 'inmuebles': pag, 'secciones_proyecto': secciones_proyecto, 'actual_seccion_proyecto': seccion_proyecto, 'criterio': criterio, 'proyecto': proyecto})
            dajax.assign('#id_reporte_inmuebles','innerHTML', render)
            dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def busqueda_inmuebles_agrupacion_inmueble_add2(request, datos):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        inmuebles_agrupacion = None
        try:
            inmuebles_agrupacion = request.session['inmuebles_agrupacion']
        except :
            pass
        if inmuebles_agrupacion != None:
            if request.is_ajax():
                if request.method == 'POST':
                    request.POST = deserialize_form(datos)
                    proyecto_id = request.POST['proyecto']
                    proyecto = Proyecto.objects.get(id=proyecto_id)
                    tipo_inmueble = request.POST['tipo_inmueble'].strip()
                    criterio = request.POST['criterio'].strip()
                    # Elimina de la lista los inmuebles que ya se ecuentran el variable de session
                    ids_inmuebles =[]
                    for inmueble_agrupacion in inmuebles_agrupacion:
                        ids_inmuebles.append(inmueble_agrupacion.id)
                    # Solo inmuebles que contengan la información basica (area_contruida, area_privada, fecha_entrega_obra)
                    inmuebles = proyecto.lista_inmuebles().filter(item_agrupacion_inmueble=None).exclude(Q(id__in=ids_inmuebles) | Q(area_construida=None) | Q(area_privada=None) | Q(fecha_entrega_obra=None))
                    
                    tipo_inmueble_actual = TipoInmueble()
                    if tipo_inmueble != '':
                        tipo_inmueble_actual = TipoInmueble.objects.get(id=tipo_inmueble)
                        inmuebles = inmuebles.filter(tipo_inmueble=tipo_inmueble_actual)
                    if criterio != '':
                        inmuebles = inmuebles.filter(identificacion__icontains=criterio)
                    tipos_inmueble = TipoInmueble.objects.all()
                    render = render_to_string('ajax/ventas/busquedainmueblesnuevaagrupacioninmueble.html', {'inmuebles': inmuebles, 'tipos_inmueble': tipos_inmueble, 'tipo_inmueble_actual': tipo_inmueble_actual, 'criterio': criterio, 'proyecto': proyecto})
                    dajax.assign('#id_busqueda_inmuebles', 'innerHTML', render)
                    dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_inmueble_agrupacion_inmueble_add2(request, inmueble_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        inmuebles_agrupacion = None
        try:
            inmuebles_agrupacion = request.session['inmuebles_agrupacion']
        except :
            pass
        if inmuebles_agrupacion != None:
            if request.is_ajax():
                if request.method == 'POST':
                    error = ''
                    proyecto = Proyecto.objects.get(id=proyecto_id)
                    dajax.script("document.getElementById('error_inmueble').style.display='none';")
                    if inmueble_id != None:
                        inmueble = proyecto.inmueble_set.get(id=inmueble_id)
                        # Valida que el inmueble no este agregado
                        agregar_inmueble = True
                        for inmueble_actual in inmuebles_agrupacion:
                            if inmueble_actual.id == inmueble.id:
                                agregar_inmueble = False
                        if agregar_inmueble:
                            inmuebles_agrupacion.append(inmueble)
                            # Actualiza el valor total de la agrupación
                            valor_total = 0
                            for inmueble_actual in inmuebles_agrupacion:
                                valor_total = round(valor_total + inmueble_actual.valor, 2)
                                
                            render = render_to_string('ajax/ventas/inmueblesagrupacion.html', {'user': user, 'inmuebles_agrupacion': inmuebles_agrupacion, 'valor_total': valor_total, 'proyecto': proyecto})
                            dajax.assign('#reporte_inmuebles', 'innerHTML', render)

                            tipos_inmueble = TipoInmueble.objects.all()
                            render = render_to_string('ajax/ventas/busquedainmueblesnuevaagrupacioninmueble.html', {'user': user, 'tipos_inmueble': tipos_inmueble, 'proyecto': proyecto})
                            dajax.assign('#id_busqueda_inmuebles', 'innerHTML', render)

                            dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
                    else:
                        error = 'Debe seleccionar un inmueble'
                    if error != '':
                        dajax.assign('#error_inmueble','innerHTML', error)
                        dajax.script("document.getElementById('error_inmueble').style.display='block';")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_inmueble_agrupacion_inmueble_add2(request, inmueble_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        inmuebles_agrupacion = None
        try:
            inmuebles_agrupacion = request.session['inmuebles_agrupacion']
        except :
            pass
        if inmuebles_agrupacion != None:
            if request.is_ajax():
                if request.method == 'POST':
                    proyecto = Proyecto.objects.get(id=proyecto_id)
                    # Actualiza el valor total de la agrupación
                    valor_total = 0
                    for inmueble_actual in inmuebles_agrupacion:
                        if inmueble_actual.id == int(inmueble_id):
                            inmuebles_agrupacion.remove(inmueble_actual)
                        else:
                            valor_total = round(valor_total + inmueble_actual.valor, 2)

                    render = render_to_string('ajax/ventas/inmueblesagrupacion.html', {'user': user, 'inmuebles_agrupacion': inmuebles_agrupacion, 'valor_total': valor_total, 'proyecto': proyecto})
                    dajax.assign('#reporte_inmuebles', 'innerHTML', render)

                    tipos_inmueble = TipoInmueble.objects.all()
                    render = render_to_string('ajax/ventas/busquedainmueblesnuevaagrupacioninmueble.html', {'tipos_inmueble': tipos_inmueble, 'proyecto': proyecto})
                    dajax.assign('#id_busqueda_inmuebles', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def busqueda_inmuebles_nuevo_prospecto_venta2(request, proyecto_id, datos):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        inmuebles_interes = None
        notificaciones_prospecto = None
        try:
            inmuebles_interes = request.session['inmuebles_interes']
            notificaciones_prospecto = request.session['notificaciones_prospecto']
        except :
            pass
        if inmuebles_interes != None and notificaciones_prospecto != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                criterio = ''

                if datos != None:
                    request.POST = deserialize_form(datos)
                    criterio = request.POST['criterio'].strip()
                    inmuebles_agregar = None
                    try:
                        inmuebles_agregar = request.session['inmuebles_agregar']
                    except :
                        pass
                else:
                    inmuebles_agregar = []
                    request.session['inmuebles_agregar'] = inmuebles_agregar

                # Filtra las agrupaciones de inmuebles que no esten comprometidas
                inmuebles = proyecto.lista_agrupaciones_inmueble(criterio=criterio).filter(agrupacion_contrato_venta=None)

                # Excluye las agruapciones que ya se encuentran en el prospecto
                ids_inmuebles_interes_prospecto = []
                for inmueble_interes in inmuebles_interes:
                    ids_inmuebles_interes_prospecto.append(inmueble_interes.id)
                inmuebles = inmuebles.exclude(id__in=ids_inmuebles_interes_prospecto)
                pag = Paginador(request, inmuebles, 20, 1)
                render = render_to_string('ajax/ventas/busquedainmueblesnuevoprospectoventa.html', {'user': user, 'agrupaciones': pag, 'agrupaciones_seleccionadas': inmuebles_agregar, 'criterio': criterio, 'proyecto': proyecto})
                dajax.assign('#light', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='block';")
                dajax.script("document.getElementById('fade').style.display='block';")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def seleccionar_agrupacion_inmuebles_nuevo_prospecto_venta2(request, agrupacion_inmueble_id, parametro, criterio, pagina, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        inmuebles_interes = None
        notificaciones_prospecto = None
        inmuebles_agregar = None
        try:
            inmuebles_interes = request.session['inmuebles_interes']
            notificaciones_prospecto = request.session['notificaciones_prospecto']
            inmuebles_agregar = request.session['inmuebles_agregar']
        except :
            pass
        if inmuebles_interes != None and inmuebles_agregar != None and notificaciones_prospecto != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                criterio = criterio.strip()
                # Filtra las agrupaciones de inmuebles que no esten comprometidas
                inmuebles = proyecto.lista_agrupaciones_inmueble(criterio=criterio).filter(agrupacion_contrato_venta=None)

                if parametro:
                    inmuebles_agregar.append(inmuebles.get(id=agrupacion_inmueble_id))
                else:
                    for inmueble_agregar in inmuebles_agregar:
                        if inmueble_agregar.id == int(agrupacion_inmueble_id):
                            inmuebles_agregar.remove(inmueble_agregar)

                # Excluye las agrupaciones que ya se encuentran en el prospecto
                ids_inmuebles_interes_prospecto = []
                for inmueble_interes in inmuebles_interes:
                    ids_inmuebles_interes_prospecto.append(inmueble_interes.id)
                inmuebles = inmuebles.exclude(id__in=ids_inmuebles_interes_prospecto)

                pag = Paginador(request, inmuebles, 20, int(pagina))
                render = render_to_string('ajax/ventas/busquedainmueblesnuevoprospectoventa.html', {'user': user, 'agrupaciones': pag, 'agrupaciones_seleccionadas': inmuebles_agregar, 'criterio': criterio, 'proyecto': proyecto})
                dajax.assign('#light', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_agrupaciones_inmuebles_nuevo_prospecto_venta2(request, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        inmuebles_interes = None
        notificaciones_prospecto = None
        inmuebles_agregar = None
        try:
            inmuebles_interes = request.session['inmuebles_interes']
            notificaciones_prospecto = request.session['notificaciones_prospecto']
            inmuebles_agregar = request.session['inmuebles_agregar']
        except :
            pass
        if inmuebles_interes != None and inmuebles_agregar != None and notificaciones_prospecto != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)

                for inmueble_agregar in inmuebles_agregar:
                    inmuebles_interes.append(inmueble_agregar)

                del request.session['inmuebles_agregar']

                render = render_to_string('ajax/ventas/inmueblesnuevoprospectoventa.html', {'user': user, 'agrupaciones': inmuebles_interes, 'proyecto': proyecto})
                dajax.assign('#id_inmuebles_interes', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='none';")
                dajax.script("document.getElementById('fade').style.display='none';")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_agrupacion_inmuebles_nuevo_prospecto_venta2(request, agrupacion_inmuebles_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        inmuebles_interes = None
        notificaciones_prospecto = None
        try:
            inmuebles_interes = request.session['inmuebles_interes']
            notificaciones_prospecto = request.session['notificaciones_prospecto']
        except :
            pass
        if inmuebles_interes != None and notificaciones_prospecto != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)

                for inmueble_interes in inmuebles_interes:
                    if inmueble_interes.id == int(agrupacion_inmuebles_id):
                        inmuebles_interes.remove(inmueble_interes)

                render = render_to_string('ajax/ventas/inmueblesnuevoprospectoventa.html', {'user': user, 'agrupaciones': inmuebles_interes, 'proyecto': proyecto})
                dajax.assign('#id_inmuebles_interes', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def nueva_notificacion_nuevo_prospecto_venta2(request, proyecto_id, datos):
    from datetime import datetime
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        inmuebles_interes = None
        notificaciones_prospecto = None
        try:
            inmuebles_interes = request.session['inmuebles_interes']
            notificaciones_prospecto = request.session['notificaciones_prospecto']
        except :
            pass
        if inmuebles_interes != None and notificaciones_prospecto != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                
                if datos != None:
                    request.POST = deserialize_form(datos)
                    form = NotificacionVentaForm(request.POST)
                    if form.is_valid():
                        notificacion_prospecto = NotificacionVenta()
                        notificacion_prospecto.tipo_notificacion = form.cleaned_data['tipo_notificacion']
                        notificacion_prospecto.fecha_limite_notificacion = datetime.combine(form.cleaned_data['fecha_limite_notificacion'], form.cleaned_data['hora_limite_notificacion'])
                        notificacion_prospecto.observaciones = form.cleaned_data['descripcion']
                        notificaciones_prospecto.append(notificacion_prospecto)
                        render = render_to_string('ajax/ventas/notificacionesnuevoprospectoventa.html', {'user': user, 'notificaciones_prospecto': notificaciones_prospecto, 'proyecto': proyecto})
                        dajax.assign('#id_notificaciones', 'innerHTML', render)
                        dajax.script("document.getElementById('light').style.display='none';")
                        dajax.script("document.getElementById('fade').style.display='none';")
                        return dajax.json()
                else:
                    form = NotificacionVentaForm()
                render = render_to_string('ajax/ventas/nuevanotificacionprospectoventa.html', {'user': user, 'form': form, 'change': False, 'proyecto': proyecto})
                dajax.assign('#light', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='block';")
                dajax.script("document.getElementById('fade').style.display='block';")
                dajax.script("Calendar.setup({inputField:'id_fecha_limite_notificacion',ifFormat:'%Y-%m-%d',button:'lanzador'});")
                #dajax.script("$('#clockpick').clockpick({ valuefield: 'id_hora_limite_notificacion' });")
                dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_notificacion_nuevo_prospecto_venta2(request, proyecto_id, datos, indice):
    from datetime import datetime
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        inmuebles_interes = None
        notificaciones_prospecto = None
        try:
            inmuebles_interes = request.session['inmuebles_interes']
            notificaciones_prospecto = request.session['notificaciones_prospecto']
        except :
            pass
        if inmuebles_interes != None and notificaciones_prospecto != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                if datos != None:
                    request.POST = deserialize_form(datos)
                    indice = request.POST['indice_notificacion']
                    form = NotificacionVentaForm(request.POST)
                    if form.is_valid():
                        notificacion_prospecto = NotificacionVenta()
                        notificacion_prospecto.tipo_notificacion = form.cleaned_data['tipo_notificacion']
                        notificacion_prospecto.fecha_limite_notificacion = datetime.combine(form.cleaned_data['fecha_limite_notificacion'], form.cleaned_data['hora_limite_notificacion'])
                        notificacion_prospecto.observaciones = form.cleaned_data['observaciones']
                        notificaciones_prospecto[int(indice)] = notificacion_prospecto
                        render = render_to_string('ajax/ventas/notificacionesnuevoprospectoventa.html', {'user': user, 'notificaciones_prospecto': notificaciones_prospecto, 'proyecto': proyecto})
                        dajax.assign('#id_notificaciones', 'innerHTML', render)
                        dajax.script("document.getElementById('light').style.display='none';")
                        dajax.script("document.getElementById('fade').style.display='none';")
                        return dajax.json()
                else:
                    notificacion_prospecto = notificaciones_prospecto[int(indice)]
                    form = NotificacionVentaForm(initial={'tipo_notificacion': notificacion_prospecto.tipo_notificacion, 'fecha_limite_notificacion': notificacion_prospecto.fecha_limite_notificacion.strftime('%Y-%m-%d'), 'hora_limite_notificacion': notificacion_prospecto.fecha_limite_notificacion.strftime('%H:%M'), 'observaciones': notificacion_prospecto.observaciones})
                render = render_to_string('ajax/ventas/nuevanotificacionprospectoventa.html', {'user': user, 'form': form, 'change': True, 'indice': indice, 'proyecto': proyecto})
                dajax.assign('#light', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='block';")
                dajax.script("document.getElementById('fade').style.display='block';")
                dajax.script("Calendar.setup({inputField:'id_fecha_limite_notificacion',ifFormat:'%Y-%m-%d',button:'lanzador'});")
                #dajax.script("$('#clockpick').clockpick({ valuefield: 'id_hora_limite_notificacion' });")
                dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_notificacion_nuevo_prospecto_venta2(request, indice, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        inmuebles_interes = None
        notificaciones_prospecto = None
        try:
            inmuebles_interes = request.session['inmuebles_interes']
            notificaciones_prospecto = request.session['notificaciones_prospecto']
        except :
            pass
        if inmuebles_interes != None and notificaciones_prospecto != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                notificaciones_prospecto.pop(int(indice))
                render = render_to_string('ajax/ventas/notificacionesnuevoprospectoventa.html', {'user': user, 'notificaciones_prospecto': notificaciones_prospecto, 'proyecto': proyecto})
                dajax.assign('#id_notificaciones', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def busqueda_inmuebles_detalles_prospecto_venta2(request, prospecto_venta_id, proyecto_id, datos):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if request.is_ajax():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            criterio = ''

            if datos != None:
                request.POST = deserialize_form(datos)
                criterio = request.POST['criterio'].strip()
                inmuebles_agregar = None
                try:
                    inmuebles_agregar = request.session['inmuebles_agregar']
                except :
                    pass
            else:
                inmuebles_agregar = []
                request.session['inmuebles_agregar'] = inmuebles_agregar

            # Filtra las agrupaciones de inmuebles que no esten comprometidas
            inmuebles = proyecto.lista_agrupaciones_inmueble(criterio=criterio).filter(agrupacion_contrato_venta=None)

            # Excluye las agruapciones que ya se encuentran en el prospecto
            prospecto_venta = proyecto.prospectoventa_set.get(id=prospecto_venta_id)
            ids_inmuebles_prospecto = []
            for agrupacion_prospecto in prospecto_venta.agrupacionesinmuebleprospectoventa_set.all():
                ids_inmuebles_prospecto.append(agrupacion_prospecto.agrupacion_inmueble.id)
            inmuebles = inmuebles.exclude(id__in=ids_inmuebles_prospecto)

            pag = Paginador(request, inmuebles, 20, 1)
            render = render_to_string('ajax/ventas/busquedainmueblesnuevoprospectoventa.html', {'user': user, 'agrupaciones': pag, 'agrupaciones_seleccionadas': inmuebles_agregar, 'criterio': criterio, 'proyecto': proyecto})
            dajax.assign('#light', 'innerHTML', render)
            dajax.script("document.getElementById('light').style.display='block';")
            dajax.script("document.getElementById('fade').style.display='block';")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def seleccionar_agrupacion_inmuebles_detalles_prospecto_venta2(request, prospecto_venta_id, agrupacion_inmueble_id, parametro, criterio, pagina, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        inmuebles_agregar = None
        try:
            inmuebles_agregar = request.session['inmuebles_agregar']
        except :
            pass
        if inmuebles_agregar != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                criterio = criterio.strip()
                # Filtra las agrupaciones de inmuebles que no esten comprometidas
                inmuebles = proyecto.lista_agrupaciones_inmueble(criterio=criterio).filter(agrupacion_contrato_venta=None)

                if parametro:
                    inmuebles_agregar.append(inmuebles.get(id=agrupacion_inmueble_id))
                else:
                    for inmueble_agregar in inmuebles_agregar:
                        if inmueble_agregar.id == int(agrupacion_inmueble_id):
                            inmuebles_agregar.remove(inmueble_agregar)

                # Excluye las agruapciones que ya se encuentran en el prospecto
                prospecto_venta = proyecto.prospectoventa_set.get(id=prospecto_venta_id)
                ids_inmuebles_prospecto = []
                for agrupacion_prospecto in prospecto_venta.agrupacionesinmuebleprospectoventa_set.all():
                    ids_inmuebles_prospecto.append(agrupacion_prospecto.agrupacion_inmueble.id)
                inmuebles = inmuebles.exclude(id__in=ids_inmuebles_prospecto)

                pag = Paginador(request, inmuebles, 20, int(pagina))
                render = render_to_string('ajax/ventas/busquedainmueblesnuevoprospectoventa.html', {'user': user, 'agrupaciones': pag, 'agrupaciones_seleccionadas': inmuebles_agregar, 'prospecto_venta': prospecto_venta, 'criterio': criterio, 'proyecto': proyecto})
                dajax.assign('#light', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_agrupaciones_inmuebles_detalles_prospecto_venta2(request, prospecto_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        inmuebles_agregar = None
        try:
            inmuebles_agregar = request.session['inmuebles_agregar']
        except :
            pass
        if inmuebles_agregar != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                prospecto_venta = proyecto.prospectoventa_set.get(id=prospecto_venta_id)

                for inmueble_agregar in inmuebles_agregar:
                    prospecto_venta.agrupacionesinmuebleprospectoventa_set.get_or_create(agrupacion_inmueble=inmueble_agregar)

                del request.session['inmuebles_agregar']

                render = render_to_string('ajax/ventas/inmueblesprospectoventa.html', {'user': user, 'prospecto_venta': prospecto_venta, 'proyecto': proyecto})
                dajax.assign('#id_inmuebles_interes', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='none';")
                dajax.script("document.getElementById('fade').style.display='none';")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def nueva_notificacion_detalles_prospecto_venta2(request, prospecto_venta_id, proyecto_id, datos):
    from datetime import datetime
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if request.is_ajax():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            prospecto_venta = proyecto.prospectoventa_set.get(id=prospecto_venta_id)

            if datos != None:
                request.POST = deserialize_form(datos)
                form = NotificacionVentaForm(request.POST)
                if form.is_valid():
                    usuario = Usuario.objects.get(id=user.id)
                    notificacion_prospecto = NotificacionVenta()
                    notificacion_prospecto.tipo_notificacion = form.cleaned_data['tipo_notificacion']
                    notificacion_prospecto.fecha_limite_notificacion = datetime.combine(form.cleaned_data['fecha_limite_notificacion'], form.cleaned_data['hora_limite_notificacion'])
                    notificacion_prospecto.descripcion = form.cleaned_data['descripcion']
                    notificacion_prospecto.prospecto_venta = prospecto_venta
                    notificacion_prospecto.usuario_registro = usuario
                    notificacion_prospecto.usuario_responsable = usuario
                    notificacion_prospecto.save()

                    render = render_to_string('ajax/ventas/notificacionesprospectoventa.html', {'user': user, 'prospecto_venta': prospecto_venta, 'proyecto': proyecto})
                    dajax.assign('#id_notificaciones', 'innerHTML', render)
                    dajax.script("document.getElementById('light').style.display='none';")
                    dajax.script("document.getElementById('fade').style.display='none';")
                    return dajax.json()
            else:
                form = NotificacionVentaForm()
            render = render_to_string('ajax/ventas/nuevanotificacionprospectoventa.html', {'user': user, 'form': form, 'change': False, 'proyecto': proyecto})
            dajax.assign('#light', 'innerHTML', render)
            dajax.script("document.getElementById('light').style.display='block';")
            dajax.script("document.getElementById('fade').style.display='block';")
            dajax.script("Calendar.setup({inputField:'id_fecha_limite_notificacion',ifFormat:'%Y-%m-%d',button:'lanzador'});")
            #dajax.script("$('#clockpick').clockpick({ valuefield: 'id_hora_limite_notificacion' });")
            dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def contestar_notificacion_prospecto_venta2(request, proyecto_id, datos, notificacion_id):
    from datetime import datetime
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if request.is_ajax():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            if datos != None:
                request.POST = deserialize_form(datos)
                notificacion_id = request.POST['notificacion_id']
                notificacion_prospecto = NotificacionVenta.objects.get(id=notificacion_id)
                form = RespuestaNotificacionVentaForm(request.POST)
                if form.is_valid():
                    notificacion_prospecto.respuesta_notificacion = form.cleaned_data['observaciones']
                    notificacion_prospecto.fecha_registro_respuesta = datetime.today()
                    # Verifica que la respuesta haya sido registrada antes de la fecha limite (Respuesta oportuna)
                    if datetime.today() <= notificacion_prospecto.fecha_limite_notificacion:
                        notificacion_prospecto.respuesta_oportuna = True
                    notificacion_prospecto.save()
                    render = render_to_string('ajax/ventas/notificacionesprospectoventa.html', {'user': user, 'prospecto_venta': notificacion_prospecto.prospecto_venta, 'proyecto': proyecto})
                    dajax.assign('#id_notificaciones', 'innerHTML', render)
                    dajax.script("document.getElementById('light').style.display='none';")
                    dajax.script("document.getElementById('fade').style.display='none';")
                    return dajax.json()
            else:
                notificacion_prospecto = NotificacionVenta.objects.get(id=notificacion_id)
                form = RespuestaNotificacionVentaForm()
            render = render_to_string('ajax/ventas/respuestanotificacionprospectoventa.html', {'user': user, 'form': form, 'notificacion_prospecto': notificacion_prospecto, 'proyecto': proyecto})
            dajax.assign('#light', 'innerHTML', render)
            dajax.script("document.getElementById('light').style.display='block';")
            dajax.script("document.getElementById('fade').style.display='block';")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_convenio_prospecto_venta2(request, prospecto_venta_id, proyecto_id, datos):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if request.is_ajax():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            prospecto_venta = proyecto.prospectoventa_set.get(id=prospecto_venta_id)
            # Filtra las agrupaciones de interes que se registraron en el prospecto (Excluyendo las que se encuentre comprometidas)
            criterio = ''
            if datos != None:
                request.POST = deserialize_form(datos)
                criterio = request.POST['criterio'].strip()
            agrupaciones_inmueble = prospecto_venta.lista_agrupaciones_inmuebles_disponibles_venta(criterio=criterio)
            if not agrupaciones_inmueble and criterio == '':
                return busqueda_agrupaciones_inmueble_agregar_convenio_prospecto_venta2(request, prospecto_venta_id, proyecto_id, None)
            else:
                render = render_to_string('ajax/ventas/inmueblesnuevoconvenioprospectoventa.html', {'user': user, 'prospecto_venta': prospecto_venta, 'agrupaciones_inmueble': agrupaciones_inmueble, 'criterio': criterio, 'proyecto': proyecto})
                dajax.assign('#light', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='block';")
                dajax.script("document.getElementById('fade').style.display='block';")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def busqueda_agrupaciones_inmueble_agregar_convenio_prospecto_venta2(request, prospecto_venta_id, proyecto_id, datos):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if request.is_ajax():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            prospecto_venta = proyecto.prospectoventa_set.get(id=prospecto_venta_id)
            criterio = ''
            # Lista solo las agrupaciones que no esten comprometidas
            if datos != None:
                request.POST = deserialize_form(datos)
                criterio = request.POST['criterio'].strip()
            agrupacion_inmuebles = proyecto.lista_agrupaciones_inmueble(criterio=criterio).filter(agrupacion_contrato_venta=None)
            pag = Paginador(request, agrupacion_inmuebles, 20, 1)
            render = render_to_string('ajax/ventas/busquedainmueblesproyectonuevoconvenioprospectoventa.html', {'user': user, 'prospecto_venta': prospecto_venta, 'agrupaciones_inmueble': pag, 'criterio': criterio, 'proyecto': proyecto})
            dajax.assign('#light', 'innerHTML', render)
            dajax.script("document.getElementById('light').style.display='block';")
            dajax.script("document.getElementById('fade').style.display='block';")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def busqueda_clientes_nuevo_contrato_venta2(request, prospecto_venta_id, proyecto_id, datos):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        # Validacion de variables de session
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                prospecto_venta = proyecto.prospectoventa_set.get(id=prospecto_venta_id)
                criterio = ''

                if datos != None:
                    request.POST = deserialize_form(datos)
                    criterio = request.POST['criterio'].strip()
                    clientes_agregar = None
                    try:
                        clientes_agregar = request.session['clientes_agregar']
                    except :
                        pass
                else:
                    clientes_agregar = []
                    request.session['clientes_agregar'] = clientes_agregar

                # Filtra los clientes que se encuentren activos
                clientes = Cliente.objects.filter(estado=True)
                if criterio != '':
                    try:
                        criterio = int(criterio)
                        clientes = clientes.filter(identificacion=criterio)
                    except :
                        clientes = clientes.filter(Q(nombre_1__icontains=criterio) | Q(nombre_2__icontains=criterio) | Q(apellido_1__icontains=criterio) | Q(apellido_2__icontains=criterio))

                # Excluye los clientes que ya se encuentran en el contrato
                clientes = clientes.exclude(id=prospecto_venta.cliente.id)
                ids_clientes_contrato = []
                for cliente_contrato in clientes_contrato:
                    ids_clientes_contrato.append(cliente_contrato.id)
                clientes = clientes.exclude(id__in=ids_clientes_contrato)
                pag = Paginador(request, clientes, 20, 1)
                render = render_to_string('ajax/ventas/busquedaclientesnuevocontratoventa.html', {'user': user, 'clientes': pag, 'clientes_seleccionados': clientes_agregar, 'criterio': criterio, 'prospecto_venta': prospecto_venta, 'proyecto': proyecto})
                dajax.assign('#light', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='block';")
                dajax.script("document.getElementById('fade').style.display='block';")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def seleccionar_cliente_nuevo_contrato_venta2(request, cliente_id, parametro, criterio, pagina, prospecto_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        # Validacion de variables de session
        clientes_contrato = None
        clientes_agregar = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            clientes_agregar = request.session['clientes_agregar']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and clientes_agregar != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                prospecto_venta = proyecto.prospectoventa_set.get(id=prospecto_venta_id)
                
                criterio = criterio.strip()
                # Filtra los clientes que se encuentren activos
                clientes = Cliente.objects.filter(estado=True)

                if parametro:
                    clientes_agregar.append(clientes.get(id=cliente_id))
                else:
                    for cliente_agregar in clientes_agregar:
                        if cliente_agregar.id == int(cliente_id):
                            clientes_agregar.remove(cliente_agregar)

                if criterio != '':
                    try:
                        criterio = int(criterio)
                        clientes = clientes.filter(identificacion=criterio)
                    except :
                        clientes = clientes.filter(Q(nombre_1__icontains=criterio) | Q(nombre_2__icontains=criterio) | Q(apellido_1__icontains=criterio) | Q(apellido_2__icontains=criterio))

                # Excluye los clientes que ya se encuentran en el contrato
                clientes = clientes.exclude(id=prospecto_venta.cliente.id)
                ids_clientes_contrato = []
                for cliente_contrato in clientes_contrato:
                    ids_clientes_contrato.append(cliente_contrato.id)
                clientes = clientes.exclude(id__in=ids_clientes_contrato)
                pag = Paginador(request, clientes, 20, int(pagina))
                render = render_to_string('ajax/ventas/busquedaclientesnuevocontratoventa.html', {'user': user, 'clientes': pag, 'clientes_seleccionados': clientes_agregar, 'criterio': criterio, 'prospecto_venta': prospecto_venta, 'proyecto': proyecto})
                dajax.assign('#light', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_clientes_nuevo_contrato_venta2(request, prospecto_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        # Validacion de variables de session
        clientes_contrato = None
        clientes_agregar = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            clientes_agregar = request.session['clientes_agregar']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and clientes_agregar != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                prospecto_venta = proyecto.prospectoventa_set.get(id=prospecto_venta_id)

                for cliente_agregar in clientes_agregar:
                    clientes_contrato.append(cliente_agregar)

                del request.session['clientes_agregar']

                render = render_to_string('ajax/ventas/clientesnuevocontratoventa.html', {'user': user, 'clientes': clientes_contrato, 'prospecto_venta': prospecto_venta, 'proyecto': proyecto})
                dajax.assign('#id_clientes', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='none';")
                dajax.script("document.getElementById('fade').style.display='none';")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_cliente_nuevo_contrato_venta2(request, cliente_id, prospecto_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                prospecto_venta = proyecto.prospectoventa_set.get(id=prospecto_venta_id)

                for cliente_contrato in clientes_contrato:
                    if cliente_contrato.id == int(cliente_id) and prospecto_venta.cliente.id != int(cliente_id):
                        clientes_contrato.remove(cliente_contrato)

                render = render_to_string('ajax/ventas/clientesnuevocontratoventa.html', {'user': user, 'clientes': clientes_contrato, 'prospecto_venta': prospecto_venta, 'proyecto': proyecto})
                dajax.assign('#id_clientes', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def busqueda_adicionales_agrupacion_nuevo_contrato_venta2(request, prospecto_venta_id, proyecto_id, datos):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and adicionales_agrupacion_inmueble_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                prospecto_venta = proyecto.prospectoventa_set.get(id=prospecto_venta_id)
                tipo_adicional = ''
                criterio = ''

                if datos != None:
                    request.POST = deserialize_form(datos)
                    tipo_adicional = request.POST['tipo_adicional']
                    criterio = request.POST['criterio'].strip()
                    adicionales_agregar = None
                    try:
                        adicionales_agregar = request.session['adicionales_agregar']
                    except :
                        pass
                else:
                    adicionales_agregar = []
                    request.session['adicionales_agregar'] = adicionales_agregar

                # Filtra los adicionales del proyecto
                if tipo_adicional != '':
                    tipo_adicional = AdicionalAgrupacion.objects.get(id=tipo_adicional)
                else:
                    tipo_adicional = None
                adicionales_agrupacion_inmueble = proyecto.lista_adicionales_agrupaciones_inmueble(tipo_adicional=tipo_adicional, criterio=criterio)

                # Excluye los adicionales que ya se encuentran en el contrato
                ids_adicionales_contrato = []
                for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                    ids_adicionales_contrato.append(adicional_agrupacion_inmueble_contrato.id)
                adicionales_agrupacion_inmueble = adicionales_agrupacion_inmueble.exclude(id__in=ids_adicionales_contrato)
                pag = Paginador(request, adicionales_agrupacion_inmueble, 20, 1)
                tipos_adicional = proyecto.lista_tipos_adicionales_agrupaciones_inmueble()
                render = render_to_string('ajax/ventas/busquedaadicionalesagrupacioninmueblenuevocontratoventa.html', {'user': user, 'adicionales_agrupacion_inmueble': pag, 'adicionales_agrupacion_inmueble_seleccionados': adicionales_agregar, 'tipos_adicional': tipos_adicional, 'tipo_adicional_actual': tipo_adicional, 'criterio': criterio, 'prospecto_venta': prospecto_venta, 'proyecto': proyecto})
                dajax.assign('#light', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='block';")
                dajax.script("document.getElementById('fade').style.display='block';")
                dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def seleccionar_adicional_agrupacion_inmueble_nuevo_contrato_venta2(request, adicional_agrupacion_inmueble_id, parametro, pagina, tipo_adicional_id, criterio, prospecto_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        # Validacion de variables de session
        clientes_contrato = None
        adicionales_agregar = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            adicionales_agregar = request.session['adicionales_agregar']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and adicionales_agregar != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                prospecto_venta = proyecto.prospectoventa_set.get(id=prospecto_venta_id)

                if parametro:
                    adicionales_agregar.append(proyecto.lista_adicionales_agrupaciones_inmueble().get(id=adicional_agrupacion_inmueble_id))
                else:
                    for adicional_agregar in adicionales_agregar:
                        if adicional_agregar.id == int(adicional_agrupacion_inmueble_id):
                            adicionales_agregar.remove(adicional_agregar)

                criterio = criterio.strip()

                # Filtra los adicionales del proyecto
                if tipo_adicional_id != None and tipo_adicional_id != '':
                    tipo_adicional = AdicionalAgrupacion.objects.get(id=tipo_adicional_id)
                else:
                    tipo_adicional = None

                adicionales_agrupacion_inmueble = proyecto.lista_adicionales_agrupaciones_inmueble(tipo_adicional=tipo_adicional, criterio=criterio)

                # Excluye los adicionales que ya se encuentran en el contrato
                ids_adicionales_contrato = []
                for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                    ids_adicionales_contrato.append(adicional_agrupacion_inmueble_contrato.id)
                adicionales_agrupacion_inmueble = adicionales_agrupacion_inmueble.exclude(id__in=ids_adicionales_contrato)
                pag = Paginador(request, adicionales_agrupacion_inmueble, 20, int(pagina))
                tipos_adicional = proyecto.lista_tipos_adicionales_agrupaciones_inmueble()
                render = render_to_string('ajax/ventas/busquedaadicionalesagrupacioninmueblenuevocontratoventa.html', {'user': user, 'adicionales_agrupacion_inmueble': pag, 'adicionales_agrupacion_inmueble_seleccionados': adicionales_agregar, 'tipos_adicional': tipos_adicional, 'tipo_adicional_actual': tipo_adicional, 'criterio': criterio, 'prospecto_venta': prospecto_venta, 'proyecto': proyecto})
                dajax.assign('#light', 'innerHTML', render)
                dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_adicionales_agrupacion_inmueble_nuevo_contrato_venta2(request, agrupacion_inmueble_id, prospecto_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        # Validacion de variables de session
        clientes_contrato = None
        adicionales_agregar = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            adicionales_agregar = request.session['adicionales_agregar']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and adicionales_agregar != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                prospecto_venta = proyecto.prospectoventa_set.get(id=prospecto_venta_id)

                for adicional_agregar in adicionales_agregar:
                    adicionales_agrupacion_inmueble_contrato.append(adicional_agregar)

                del request.session['adicionales_agregar']

                render = render_to_string('ajax/ventas/adicionalesnuevocontratoventa.html', {'user': user, 'adicionales_agrupacion_inmueble_contrato': adicionales_agrupacion_inmueble_contrato, 'prospecto_venta': prospecto_venta, 'proyecto': proyecto})
                dajax.assign('#id_adicionales', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='none';")
                dajax.script("document.getElementById('fade').style.display='none';")

                agrupacion_inmueble = proyecto.agrupacioninmueble_set.get(id=agrupacion_inmueble_id)
                valor_total_agrupacion = agrupacion_inmueble.str_valor()

                for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                    valor_total_agrupacion = round(valor_total_agrupacion + adicional_agrupacion_inmueble_contrato.valor, 2)

                dajax.assign('#id_valor_inmueble', 'innerHTML', 'VALOR INMUEBLE $' + str(intcomma(valor_total_agrupacion)))
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_adicional_agrupacion_inmueble_nuevo_contrato_venta2(request, adicional_agrupacion_inmueble_id, agrupacion_inmueble_id, prospecto_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        # Validacion de variables de session
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                prospecto_venta = proyecto.prospectoventa_set.get(id=prospecto_venta_id)

                for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                    if adicional_agrupacion_inmueble_contrato.id == int(adicional_agrupacion_inmueble_id):
                        adicionales_agrupacion_inmueble_contrato.remove(adicional_agrupacion_inmueble_contrato)

                request.session['adicionales_agrupacion_inmueble_contrato'] = adicionales_agrupacion_inmueble_contrato

                render = render_to_string('ajax/ventas/adicionalesnuevocontratoventa.html', {'user': user, 'adicionales_agrupacion_inmueble_contrato': adicionales_agrupacion_inmueble_contrato, 'prospecto_venta': prospecto_venta, 'proyecto': proyecto})
                dajax.assign('#id_adicionales', 'innerHTML', render)

                agrupacion_inmueble = proyecto.agrupacioninmueble_set.get(id=agrupacion_inmueble_id)
                valor_total_agrupacion = agrupacion_inmueble.str_valor()

                for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                    valor_total_agrupacion = round(valor_total_agrupacion + adicional_agrupacion_inmueble_contrato.valor, 2)

                dajax.assign('#id_valor_inmueble', 'innerHTML', 'VALOR INMUEBLE $' + str(intcomma(valor_total_agrupacion)))
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def seleccionar_forma_pago_nuevo_contrato_venta2(request, forma_pago, prospecto_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                prospecto_venta = proyecto.prospectoventa_set.get(id=prospecto_venta_id)
                render = ''
                if forma_pago != '':
                    aplica_adicionales = False
                    if len(proyecto.lista_adicionales_agrupaciones_inmueble()) > 0:
                        aplica_adicionales = True
                    if (aplica_adicionales == True and len(adicionales_agrupacion_inmueble_contrato) > 0) or aplica_adicionales == False :
                        forma_pago = int(forma_pago)
                        request.session['forma_pago'] = forma_pago
                        if forma_pago == 2:
                            try:
                                del request.session['monto_credito']
                            except :
                                pass
                        form = ContratoVentaForm(initial={'forma_pago': forma_pago})
                        render = render_to_string('ajax/ventas/formapagonuevocontratoventa.html', {'user': user, 'form': form, 'prospecto_venta': prospecto_venta, 'proyecto': proyecto},context_instance=RequestContext(request))
                    else:
                        dajax.assign('#id_error_adicionales', 'innerHTML', 'Debe seleccionar por lo menos 1 adicional')
                        dajax.alert('Debe seleccionar por lo menos 1 adicional')
                        dajax.script("$('#id_forma_pago').val('-----');")
                        dajax.script("$('#id_forma_pago').trigger('chosen:updated');")
                else:
                    try:
                        del request.session['forma_pago']
                        del request.session['monto_credito']
                    except :
                        pass
                request.session['pagos_entidades_contrato'] = []
                request.session['cuotas_efectivo_contrato'] = []
                dajax.assign('#id_panel_forma_pago', 'innerHTML', render)
                dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $' + str(intcomma(0.0)))
                dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
                if forma_pago and ((aplica_adicionales and adicionales_agrupacion_inmueble_contrato) or not aplica_adicionales):
                    dajax.script("Calendar.setup({inputField:'id_fecha_registro_desembolso_credito',ifFormat:'%Y-%m-%d',button:'lanzador_fecha_desembolso'});")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_pago_entidad_nuevo_contrato_venta2(request, agrupacion_inmueble_id, datos, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                if datos:
                    request.POST = deserialize_form(datos)
                    form = PagoEntidadContratoVentaForm(data=request.POST)
                    if form.is_valid():
                        pago_entidad_contrato_venta = PagoEntidadContratoVenta()
                        pago_entidad_contrato_venta.tipo_cuenta = form.cleaned_data['tipo_cuenta']
                        pago_entidad_contrato_venta.entidad = form.cleaned_data['entidad']
                        if form.cleaned_data['numero_cuenta'].strip() != '':
                            pago_entidad_contrato_venta.numero_cuenta = form.cleaned_data['numero_cuenta'].strip()
                        pago_entidad_contrato_venta.fecha_desembolso = form.cleaned_data['fecha_desembolso']
                        pago_entidad_contrato_venta.valor = float(form.cleaned_data['valor'])
                        pagos_entidades_contrato.append(pago_entidad_contrato_venta)
                        request.session['pagos_entidades_contrato'] = pagos_entidades_contrato
                        # Actualiza el valor a pagar por parte de entidades
                        valor_pagar_entidad_contrato = 0
                        for pago_entidad_contrato in pagos_entidades_contrato:
                            valor_pagar_entidad_contrato = round(valor_pagar_entidad_contrato + pago_entidad_contrato.valor, 2)
                        render = render_to_string('ajax/ventas/pagosentidadcontratoventa.html', {'user': user, 'pagos_entidades_contrato': pagos_entidades_contrato, 'valor_pagar_entidad_contrato': valor_pagar_entidad_contrato})
                        dajax.assign('#id_reporte_pagos_entidad', 'innerHTML', render)
                        dajax.script("document.getElementById('light').style.display='none';")
                        dajax.script("document.getElementById('fade').style.display='none';")

                        # Actualiza el valor a pagar por el cliente
                        try:
                            monto_credito = request.session['monto_credito']
                        except :
                            monto_credito = 0
                        valor_pagar = round(monto_credito + valor_pagar_entidad_contrato, 2)

                        for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                            valor_pagar = round(valor_pagar + cuota_efectivo_contrato.valor, 2)

                        dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $' + str(intcomma(valor_pagar)))

                        # Actualiza el valor en efectivo excedente a pagar por el cliente
                        agrupacion_inmueble = proyecto.lista_agrupaciones_inmueble().get(id=agrupacion_inmueble_id)

                        valor_total_inmueble = agrupacion_inmueble.str_valor()
                        for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                            valor_total_inmueble = round(valor_total_inmueble + adicional_agrupacion_inmueble_contrato.valor, 2)

                        valor_excedente_pagar_efectivo = round(valor_total_inmueble - monto_credito - valor_pagar_entidad_contrato, 2)
                        dajax.assign('#id_valor_excedente_pagar_efectivo', 'innerHTML', 'Pagos en efectivo $' + str(intcomma(valor_excedente_pagar_efectivo)))

                        dajax.alert('Nuevo pago agregado correctamente')
                        return dajax.json()
                else:
                    form = PagoEntidadContratoVentaForm()
                render = render_to_string('ajax/ventas/nuevopagoentidadcontratoventa.html', {'user': user, 'form': form, 'change': 0}, context_instance=RequestContext(request))
                dajax.assign('#light', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='block';")
                dajax.script("document.getElementById('fade').style.display='block';")
                dajax.script("Calendar.setup({inputField:'id_fecha_desembolso',ifFormat:'%Y-%m-%d',button:'lanzador_fecha_desembolso'});")
                dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_pago_entidad_nuevo_contrato_venta2(request, agrupacion_inmueble_id, indice, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                pagos_entidades_contrato.pop(int(indice))
                request.session['pagos_entidades_contrato'] = pagos_entidades_contrato
                # Actualiza el valor a pagar por parte de entidades
                valor_pagar_entidad_contrato = 0
                for pago_entidad_contrato in pagos_entidades_contrato:
                    valor_pagar_entidad_contrato = round(valor_pagar_entidad_contrato + pago_entidad_contrato.valor, 2)

                render = render_to_string('ajax/ventas/pagosentidadcontratoventa.html', {'user': user, 'pagos_entidades_contrato': pagos_entidades_contrato, 'valor_pagar_entidad_contrato': valor_pagar_entidad_contrato})
                dajax.assign('#id_reporte_pagos_entidad', 'innerHTML', render)
                dajax.alert('Pago entidad eliminado correctamente')

                # Actualiza el valor a pagar por el cliente
                try:
                    monto_credito = request.session['monto_credito']
                except :
                    monto_credito = 0
                valor_pagar = round(monto_credito + valor_pagar_entidad_contrato, 2)

                for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                    valor_pagar = round(valor_pagar + cuota_efectivo_contrato.valor, 2)

                dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $' + str(intcomma(valor_pagar)))

                # Actualiza el valor en efectivo excedente a pagar por el cliente
                agrupacion_inmueble = proyecto.lista_agrupaciones_inmueble().get(id=agrupacion_inmueble_id)

                valor_total_inmueble = agrupacion_inmueble.str_valor()
                for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                    valor_total_inmueble = round(valor_total_inmueble + adicional_agrupacion_inmueble_contrato.valor, 2)

                valor_excedente_pagar_efectivo = round(valor_total_inmueble - monto_credito - valor_pagar_entidad_contrato, 2)
                dajax.assign('#id_valor_excedente_pagar_efectivo', 'innerHTML', 'Pagos en efectivo $' + str(intcomma(valor_excedente_pagar_efectivo)))
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_pago_entidad_nuevo_contrato_venta2(request, agrupacion_inmueble_id, datos, indice, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                if datos:
                    request.POST = deserialize_form(datos)
                    indice = int(request.POST['indice'])
                    pago_entidad_contrato_venta = pagos_entidades_contrato[indice]
                    form = PagoEntidadContratoVentaForm(instance=pago_entidad_contrato_venta, data=request.POST)
                    if form.is_valid():
                        pago_entidad_contrato_venta.tipo_cuenta = form.cleaned_data['tipo_cuenta']
                        pago_entidad_contrato_venta.entidad = form.cleaned_data['entidad']
                        if form.cleaned_data['numero_cuenta'].strip() != '':
                            pago_entidad_contrato_venta.numero_cuenta = form.cleaned_data['numero_cuenta'].strip()
                        pago_entidad_contrato_venta.fecha_desembolso = form.cleaned_data['fecha_desembolso']
                        pago_entidad_contrato_venta.valor = float(form.cleaned_data['valor'])
                        # Actualiza el valor a pagar por parte de entidades
                        valor_pagar_entidad_contrato = 0
                        for pago_entidad_contrato in pagos_entidades_contrato:
                            valor_pagar_entidad_contrato = round(valor_pagar_entidad_contrato + pago_entidad_contrato.valor, 2)
                        request.session['pagos_entidades_contrato'] = pagos_entidades_contrato
                        render = render_to_string('ajax/ventas/pagosentidadcontratoventa.html', {'user': user, 'pagos_entidades_contrato': pagos_entidades_contrato, 'valor_pagar_entidad_contrato': valor_pagar_entidad_contrato})
                        dajax.assign('#id_reporte_pagos_entidad', 'innerHTML', render)
                        dajax.script("document.getElementById('light').style.display='none';")
                        dajax.script("document.getElementById('fade').style.display='none';")

                        # Actualiza el valor a pagar por el cliente
                        try:
                            monto_credito = request.session['monto_credito']
                        except :
                            monto_credito = 0
                        valor_pagar = round(monto_credito + valor_pagar_entidad_contrato, 2)

                        for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                            valor_pagar = round(valor_pagar + cuota_efectivo_contrato.valor, 2)

                        dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $' + str(intcomma(valor_pagar)))

                        # Actualiza el valor en efectivo excedente a pagar por el cliente
                        agrupacion_inmueble = proyecto.lista_agrupaciones_inmueble().get(id=agrupacion_inmueble_id)

                        valor_total_inmueble = agrupacion_inmueble.str_valor()
                        for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                            valor_total_inmueble = round(valor_total_inmueble + adicional_agrupacion_inmueble_contrato.valor, 2)

                        valor_excedente_pagar_efectivo = round(valor_total_inmueble - monto_credito - valor_pagar_entidad_contrato, 2)
                        dajax.assign('#id_valor_excedente_pagar_efectivo', 'innerHTML', 'Pagos en efectivo $' + str(intcomma(valor_excedente_pagar_efectivo)))

                        dajax.alert('Nuevo pago modificado correctamente')
                        return dajax.json()
                else:
                    pago_entidad_contrato_venta = pagos_entidades_contrato[int(indice)]
                    entidad = ''
                    if pago_entidad_contrato_venta.entidad != None:
                        entidad = pago_entidad_contrato_venta.entidad
                    numero_cuenta = ''
                    if pago_entidad_contrato_venta.numero_cuenta != None:
                        numero_cuenta = pago_entidad_contrato_venta.numero_cuenta
                    fecha_desembolso = ''
                    if pago_entidad_contrato_venta.fecha_desembolso != None:
                        fecha_desembolso = pago_entidad_contrato_venta.fecha_desembolso.strftime('%Y-%m-%d')
                    form = PagoEntidadContratoVentaForm(initial={'tipo_cuenta': pago_entidad_contrato_venta.tipo_cuenta, 'entidad': entidad, 'numero_cuenta': numero_cuenta, 'fecha_desembolso': fecha_desembolso, 'valor': pago_entidad_contrato_venta.valor})
                render = render_to_string('ajax/ventas/nuevopagoentidadcontratoventa.html', {'user': user, 'form': form, 'indice': indice, 'change': 1}, context_instance=RequestContext(request))
                dajax.assign('#light', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='block';")
                dajax.script("document.getElementById('fade').style.display='block';")
                dajax.script("Calendar.setup({inputField:'id_fecha_desembolso',ifFormat:'%Y-%m-%d',button:'lanzador_fecha_desembolso'});")
                dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def asignar_monto_credito_nuevo_contrato_venta2(request, agrupacion_inmueble_id, monto_credito, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            proyecto = Proyecto.objects.get(id=proyecto_id)
            error_monto_credito = ''
            validaciones_monto_credito = Validator().append([
                Field('monto_credito', monto_credito).append([
                    IsRequired('Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
                ]),
            ]).run(True).pop()

            if validaciones_monto_credito['passed'] == True:
                monto_credito = float(monto_credito)
                request.session['monto_credito'] = monto_credito

                # Actualiza el valor a pagar por el cliente
                valor_pagar = 0
                valor_pagar_entidad_contrato = 0
                for pago_entidad_contrato in pagos_entidades_contrato:
                    valor_pagar = round(valor_pagar + pago_entidad_contrato.valor, 2)
                    valor_pagar_entidad_contrato = round(valor_pagar_entidad_contrato + pago_entidad_contrato.valor, 2)

                valor_pagar_efectivo_contrato = 0
                for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                    valor_pagar = round(valor_pagar + cuota_efectivo_contrato.valor, 2)
                    valor_pagar_efectivo_contrato = round(valor_pagar_efectivo_contrato + cuota_efectivo_contrato.valor, 2)

                valor_pagar= round(valor_pagar + monto_credito, 2)
                dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $' + str(intcomma(valor_pagar)))

                # Actualiza el valor en efectivo excedente a pagar por el cliente
                agrupacion_inmueble = proyecto.lista_agrupaciones_inmueble().get(id=agrupacion_inmueble_id)

                valor_total_inmueble = agrupacion_inmueble.str_valor()
                for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                    valor_total_inmueble = round(valor_total_inmueble + adicional_agrupacion_inmueble_contrato.valor, 2)

                valor_excedente_pagar_efectivo = round(valor_total_inmueble - monto_credito - valor_pagar_entidad_contrato, 2)
                dajax.assign('#id_valor_excedente_pagar_efectivo', 'innerHTML', 'Pagos en efectivo $' + str(intcomma(valor_excedente_pagar_efectivo)))
                dajax.script("document.getElementById('id_monto_credito').value = '" + str(monto_credito) + "';")
                dajax.script("document.getElementById('id_monto_credito_0').value = '" + str(intcomma(monto_credito)) + "';")
                dajax.script("document.getElementById('id_monto_credito_0').readOnly = true;")
                dajax.script("document.getElementById('id_btn_asignar_monto_credito').style.display = 'none';")
                dajax.script("document.getElementById('id_btn_modificar_monto_credito').style.display = 'block';")
            else:
                for error in validaciones_monto_credito['errors']:
                    error_monto_credito = error
                dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $ -')
            dajax.assign('#id_error_monto_credito', 'innerHTML', error_monto_credito)
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def activar_asignar_monto_credito_nuevo_contrato_venta2(request):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        monto_credito = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
            monto_credito = request.session['monto_credito']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None and monto_credito != None:
            del request.session['monto_credito']
            dajax.script("$('#id_monto_credito').val('');")
            dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $ -')
            dajax.script("$('#id_monto_credito').val('');")
            dajax.script("$('#id_monto_credito_0').val('" + str(monto_credito) + "');")
            dajax.script("document.getElementById('id_monto_credito_0').readOnly = false;")
            dajax.script("document.getElementById('id_monto_credito_0').focus();")
            dajax.script("document.getElementById('id_monto_credito_0').select();")
            dajax.script("document.getElementById('id_btn_asignar_monto_credito').style.display = 'block';")
            dajax.script("document.getElementById('id_btn_modificar_monto_credito').style.display = 'none';")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def seleccionar_numero_cuotas_efectivo_nuevo_contrato_venta2(request, agrupacion_inmueble_id, numero_cuotas, prospecto_venta_id, proyecto_id):
    import datetime
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        forma_pago = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
            forma_pago = request.session['forma_pago']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                prospecto_venta = proyecto.prospectoventa_set.get(id=prospecto_venta_id)
                monto_credito = 0
                if forma_pago == 1:
                    try:
                        monto_credito = request.session['monto_credito']
                    except :
                        monto_credito = None
                # Veridica que se haya registrado un monto para el credito
                if monto_credito != None:
                    cuotas_efectivo_contrato = []
                    request.session['cuotas_efectivo_contrato'] = cuotas_efectivo_contrato
                    render = ''
                    if numero_cuotas != '':
                        agrupacion_inmueble = proyecto.agrupacioninmueble_set.get(id=agrupacion_inmueble_id)
                        # Calcula el valor de la agrupación
                        valor_total_agrupacion = agrupacion_inmueble.str_valor()

                        for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                            valor_total_agrupacion = round(valor_total_agrupacion + adicional_agrupacion_inmueble_contrato.valor, 2)

                        # Calcula el valor a pagar por el cliente
                        valor_pagar = monto_credito
                        for pago_entidad_contrato in pagos_entidades_contrato:
                            valor_pagar = round(valor_pagar + pago_entidad_contrato.valor, 2)

                        valor_pendiente_pagar = round(valor_total_agrupacion - valor_pagar, 2)

                        numero_cuotas = int(numero_cuotas)
                        valor_cuota = round(valor_pendiente_pagar / numero_cuotas, 2)

                        anio_actual = datetime.date.today().year
                        mes_actual = datetime.date.today().month
                        dia_actual = datetime.date.today().day

                        for cuota in range(mes_actual + 1, numero_cuotas + mes_actual + 1):
                            cuota_efectivo_contrato = PagoEfectivoContratoVenta()
                            coeficiente = int(round(cuota / 12, 0))
                            if cuota % 12 == 0:
                                coeficiente -= 1
                            anio = anio_actual + coeficiente
                            mes = cuota
                            if cuota > 12:
                                mes = (cuota - (coeficiente * 12))
                            cuota_adicionada = False
                            dia = dia_actual
                            while cuota_adicionada == False:
                                try:
                                    cuota_efectivo_contrato.fecha_desembolso = datetime.date(anio, mes, dia)
                                    cuota_adicionada = True
                                except :
                                    dia = dia - 1                                    
                            cuota_efectivo_contrato.valor = valor_cuota
                            cuotas_efectivo_contrato.append(cuota_efectivo_contrato)
                        render = render_to_string('ajax/ventas/pagosefectivocontratoventa.html', {'user': user, 'cuotas_efectivo_contrato': cuotas_efectivo_contrato, 'valor_efectivo_pagar': valor_pendiente_pagar, 'prospecto_venta': prospecto_venta, 'proyecto': proyecto})

                    dajax.assign('#id_panel_numero_cuotas', 'innerHTML', render)
                    # Actualiza el valor a pagar por el cliente
                    valor_pagar = monto_credito or 0
                    for pago_entidad_contrato in pagos_entidades_contrato:
                        valor_pagar = round(valor_pagar + pago_entidad_contrato.valor, 2)

                    for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                        valor_pagar = round(valor_pagar + cuota_efectivo_contrato.valor, 2)

                    dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $' + str(intcomma(valor_pagar)))
                else:
                    dajax.assign('#id_error_monto_credito', 'innerHTML', 'Debe ingresar un monto para credito')
                    dajax.script("$('#id_numero_cuotas').val('');")
                    dajax.script("$('#id_numero_cuotas').trigger('chosen:updated');")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_pago_efectivo_nuevo_contrato_venta2(request, agrupacion_inmueble_id, datos, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        forma_pago = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
            forma_pago = request.session['forma_pago']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                monto_credito = 0
                if forma_pago == 1:
                    try:
                        monto_credito = request.session['monto_credito']
                    except :
                        monto_credito = None
                # Veridica que se haya registrado un monto para el credito
                if monto_credito != None:
                    if datos != None:
                        proyecto = Proyecto.objects.get(id=proyecto_id)
                        request.POST = deserialize_form(datos)
                        form = PagoEfectivoContratoVentaForm(request.POST)
                        if form.is_valid():
                            nueva_cuota_efectivo_contrato = PagoEfectivoContratoVenta()
                            nueva_cuota_efectivo_contrato.fecha_desembolso = form.cleaned_data['fecha_desembolso']
                            nueva_cuota_efectivo_contrato.valor = float(form.cleaned_data['valor'])
                            cuotas_efectivo_contrato.append(nueva_cuota_efectivo_contrato)

                            # Ordena las cuotas por fecha de desembolso
                            cuotas_efectivo_contrato.sort(compara_fechas_cuotas_efectivo)

                            # Calcula el valor de la agrupación
                            agrupacion_inmueble = proyecto.lista_agrupaciones_inmueble().get(id=agrupacion_inmueble_id)
                            valor_total_agrupacion = agrupacion_inmueble.str_valor()

                            for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                                valor_total_agrupacion = round(valor_total_agrupacion + adicional_agrupacion_inmueble_contrato.valor, 2)

                            valor_pagar = monto_credito
                            valor_pagar_entidad_contrato = 0
                            for pago_entidad_contrato in pagos_entidades_contrato:
                                valor_pagar = round(valor_pagar + pago_entidad_contrato.valor, 2)
                                valor_pagar_entidad_contrato = round(valor_pagar_entidad_contrato + pago_entidad_contrato.valor, 2)

                            valor_pagar_efectivo_contrato = 0
                            for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                                valor_pagar_efectivo_contrato = round(valor_pagar_efectivo_contrato + cuota_efectivo_contrato.valor, 2)

                            valor_pagar = round(valor_pagar + valor_pagar_efectivo_contrato, 2)

                            # Se recalcula el valor de las cuotas a partir de la nueva cuota agregada
                            if not(valor_pagar < round(valor_total_agrupacion + 100, 2) and valor_pagar > round(valor_total_agrupacion - 100, 2)):
                                suma_cuotas_confirmadas = 0
                                cuota_encontrada = False
                                indice = 0
                                valor_cuota_predeterminada = 0
                                for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                                    indice += 1
                                    if cuota_efectivo_contrato.fecha_desembolso == nueva_cuota_efectivo_contrato.fecha_desembolso:
                                        if len(cuotas_efectivo_contrato) - indice > 0:
                                            suma_cuotas_confirmadas = round(suma_cuotas_confirmadas + cuota_efectivo_contrato.valor, 2)
                                            valor_cuota_predeterminada = round((valor_total_agrupacion - (monto_credito + valor_pagar_entidad_contrato + suma_cuotas_confirmadas)) / (len(cuotas_efectivo_contrato) - indice), 2)
                                            cuota_encontrada = True
                                    elif cuota_encontrada == False:
                                        suma_cuotas_confirmadas = round(suma_cuotas_confirmadas + cuota_efectivo_contrato.valor, 2)
                                    else:
                                        cuota_efectivo_contrato.valor = valor_cuota_predeterminada

                            request.session['cuotas_efectivo_contrato'] = cuotas_efectivo_contrato
                            valor_pagar_efectivo_contrato = 0
                            for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                                valor_pagar_efectivo_contrato = round(valor_pagar_efectivo_contrato + cuota_efectivo_contrato.valor, 2)

                            render = render_to_string('ajax/ventas/pagosefectivocontratoventa.html', {'user': user, 'cuotas_efectivo_contrato': cuotas_efectivo_contrato, 'valor_efectivo_pagar': valor_pagar_efectivo_contrato})
                            dajax.assign('#id_panel_numero_cuotas', 'innerHTML', render)
                            dajax.alert('Pago efectivo agregado correctamente')

                            # Actualiza el valor a pagar por el cliente
                            valor_pagar = monto_credito
                            for pago_entidad_contrato in pagos_entidades_contrato:
                                valor_pagar = round(valor_pagar + pago_entidad_contrato.valor, 2)

                            valor_pagar = round(valor_pagar + valor_pagar_efectivo_contrato, 2)

                            dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $' + str(intcomma(valor_pagar)))
                            dajax.assign('#id_valor_excedente_pagar_efectivo', 'innerHTML', 'Pagos en efectivo $' + str(intcomma(valor_pagar_efectivo_contrato)))
                            dajax.script("$('#id_numero_cuotas').val('"+ str(len(cuotas_efectivo_contrato)) + "');")
                            dajax.script("document.getElementById('light').style.display='none';")
                            dajax.script("document.getElementById('fade').style.display='none';")
                            dajax.script("$('#id_numero_cuotas').trigger('chosen:updated');")
                            return dajax.json()
                    else:
                        form = PagoEfectivoContratoVentaForm()
                    render = render_to_string('ajax/ventas/nuevopagoefectivocontratoventa.html', {'user': user, 'form': form, 'change': 0}, context_instance=RequestContext(request))
                    dajax.assign('#light', 'innerHTML', render)
                    dajax.script("document.getElementById('light').style.display='block';")
                    dajax.script("document.getElementById('fade').style.display='block';")
                    dajax.script("Calendar.setup({inputField:'id_fecha_desembolso',ifFormat:'%Y-%m-%d',button:'lanzador_fecha_desembolso'});")
                else:
                    dajax.assign('#id_error_monto_credito', 'innerHTML', 'Debe ingresar un monto para credito')
                    dajax.script("$('#id_numero_cuotas').val('');")
                    dajax.script("$('#id_numero_cuotas').trigger('chosen:updated');")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def compara_fechas_cuotas_efectivo( x, y ) :
    # x e y son objetos de los que se desea ordenar
    if x.fecha_desembolso < y.fecha_desembolso :
      rst = -1
    elif x.fecha_desembolso > y.fecha_desembolso :
      rst = 1
    else :
      rst = 0

    return rst


def modificar_pago_efectivo_nuevo_contrato_venta2(request, agrupacion_inmueble_id, datos, indice, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        forma_pago = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
            forma_pago = request.session['forma_pago']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                if datos != None:
                    proyecto = Proyecto.objects.get(id=proyecto_id)
                    monto_credito = 0
                    if forma_pago == 1:
                        try:
                            monto_credito = request.session['monto_credito']
                        except :
                            monto_credito = None
                    # Veridica que se haya registrado un monto para el credito
                    if monto_credito != None:
                        request.POST = deserialize_form(datos)
                        indice = int(request.POST['indice'])
                        form = PagoEfectivoContratoVentaForm(request.POST)
                        if form.is_valid():
                            cuota_efectivo_contrato_modificar = cuotas_efectivo_contrato[indice]
                            cuota_efectivo_contrato_modificar.fecha_desembolso = form.cleaned_data['fecha_desembolso']
                            cuota_efectivo_contrato_modificar.valor = float(form.cleaned_data['valor'])
                            
                            # Ordena las cuotas por fecha de desembolso
                            cuotas_efectivo_contrato.sort(compara_fechas_cuotas_efectivo)

                            # Calcula el valor de la agrupación
                            agrupacion_inmueble = proyecto.lista_agrupaciones_inmueble().get(id=agrupacion_inmueble_id)
                            valor_total_agrupacion = agrupacion_inmueble.str_valor()

                            for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                                valor_total_agrupacion = round(valor_total_agrupacion + adicional_agrupacion_inmueble_contrato.valor, 2)

                            valor_pagar = monto_credito
                            valor_pagar_entidad_contrato = 0
                            for pago_entidad_contrato in pagos_entidades_contrato:
                                valor_pagar = round(valor_pagar + pago_entidad_contrato.valor, 2)
                                valor_pagar_entidad_contrato = round(valor_pagar_entidad_contrato + pago_entidad_contrato.valor, 2)

                            valor_pagar_efectivo_contrato = 0
                            for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                                valor_pagar_efectivo_contrato = round(valor_pagar_efectivo_contrato + cuota_efectivo_contrato.valor, 2)

                            valor_pagar = round(valor_pagar + valor_pagar_efectivo_contrato, 2)

                            # Se recalcula el valor de las cuotas a partir de la nueva cuota agregada
                            if not(valor_pagar < round(valor_total_agrupacion + 100, 2) and valor_pagar > round(valor_total_agrupacion - 100, 2)):
                                suma_cuotas_confirmadas = 0
                                cuota_encontrada = False
                                indice = 0
                                valor_cuota_predeterminada = 0
                                for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                                    indice += 1
                                    if cuota_efectivo_contrato.fecha_desembolso == cuota_efectivo_contrato_modificar.fecha_desembolso:
                                        if len(cuotas_efectivo_contrato) - indice > 0:
                                            suma_cuotas_confirmadas = round(suma_cuotas_confirmadas + cuota_efectivo_contrato.valor, 2)
                                            valor_cuota_predeterminada = round((valor_total_agrupacion - (monto_credito + valor_pagar_entidad_contrato + suma_cuotas_confirmadas)) / (len(cuotas_efectivo_contrato) - indice), 2)
                                            cuota_encontrada = True
                                    elif cuota_encontrada == False:
                                        suma_cuotas_confirmadas = round(suma_cuotas_confirmadas + cuota_efectivo_contrato.valor, 2)
                                    else:
                                        cuota_efectivo_contrato.valor = valor_cuota_predeterminada

                            request.session['cuotas_efectivo_contrato'] = cuotas_efectivo_contrato
                            valor_pagar_efectivo_contrato = 0
                            for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                                valor_pagar_efectivo_contrato = round(valor_pagar_efectivo_contrato + cuota_efectivo_contrato.valor, 2)

                            render = render_to_string('ajax/ventas/pagosefectivocontratoventa.html', {'user': user, 'cuotas_efectivo_contrato': cuotas_efectivo_contrato, 'valor_efectivo_pagar': valor_pagar_efectivo_contrato})
                            dajax.assign('#id_panel_numero_cuotas', 'innerHTML', render)
                            dajax.alert('Pago efectivo modificado correctamente')

                            # Actualiza el valor a pagar por el cliente
                            valor_pagar = monto_credito
                            for pago_entidad_contrato in pagos_entidades_contrato:
                                valor_pagar = round(valor_pagar + pago_entidad_contrato.valor, 2)

                            valor_pagar = round(valor_pagar + valor_pagar_efectivo_contrato, 2)

                            dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $' + str(intcomma(valor_pagar)))
                            dajax.assign('#id_valor_excedente_pagar_efectivo', 'innerHTML', 'Pagos en efectivo $' + str(intcomma(valor_pagar_efectivo_contrato)))
                            dajax.script("$('#id_numero_cuotas').val('"+ str(len(cuotas_efectivo_contrato)) + "');")
                            dajax.script("document.getElementById('light').style.display='none';")
                            dajax.script("document.getElementById('fade').style.display='none';")
                            dajax.script("$('#id_numero_cuotas').trigger('chosen:updated');")
                            return dajax.json()
                    else:
                        dajax.redirect('/inverboy/home/')
                else:
                    cuota_efectivo_contrato_modificar = cuotas_efectivo_contrato[int(indice)]
                    form = PagoEfectivoContratoVentaForm(initial={'fecha_desembolso': cuota_efectivo_contrato_modificar.fecha_desembolso.strftime('%Y-%m-%d'), 'valor': cuota_efectivo_contrato_modificar.valor})
                render = render_to_string('ajax/ventas/nuevopagoefectivocontratoventa.html', {'user': user, 'form': form, 'indice': indice, 'change': 1}, context_instance=RequestContext(request))
                dajax.assign('#light', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='block';")
                dajax.script("document.getElementById('fade').style.display='block';")
                dajax.script("Calendar.setup({inputField:'id_fecha_desembolso',ifFormat:'%Y-%m-%d',button:'lanzador_fecha_desembolso'});")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_pago_efectivo_nuevo_contrato_venta2(request, agrupacion_inmueble_id, indice, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        forma_pago = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
            forma_pago = request.session['forma_pago']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                monto_credito = 0
                if forma_pago == 1:
                    try:
                        monto_credito = request.session['monto_credito']
                    except :
                        monto_credito = None
                # Veridica que se haya registrado un monto para el credito
                if monto_credito != None:
                    cuotas_efectivo_contrato.pop(int(indice))

                    # Calcula el valor de la agrupación
                    agrupacion_inmueble = proyecto.lista_agrupaciones_inmueble().get(id=agrupacion_inmueble_id)
                    valor_total_agrupacion = agrupacion_inmueble.str_valor()

                    for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                        valor_total_agrupacion = round(valor_total_agrupacion + adicional_agrupacion_inmueble_contrato.valor, 2)

                    valor_pagar = monto_credito
                    valor_pagar_entidad_contrato = 0
                    for pago_entidad_contrato in pagos_entidades_contrato:
                        valor_pagar = round(valor_pagar + pago_entidad_contrato.valor, 2)
                        valor_pagar_entidad_contrato = round(valor_pagar_entidad_contrato + pago_entidad_contrato.valor, 2)

                    valor_pagar_efectivo_contrato = 0
                    for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                        valor_pagar_efectivo_contrato = round(valor_pagar_efectivo_contrato + cuota_efectivo_contrato.valor, 2)

                    valor_pagar = round(valor_pagar + valor_pagar_efectivo_contrato, 2)

                    # Se recalcula el valor de las cuotas a partir de la cuota eliminada
                    indice = int(indice)
                    if not(valor_pagar < round(valor_total_agrupacion + 100, 2) and valor_pagar > round(valor_total_agrupacion - 100, 2)):
                        suma_cuotas_confirmadas = 0
                        indice_referencia = 0
                        valor_cuota_predeterminada = 0
                        for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                            if indice_referencia < indice:
                                suma_cuotas_confirmadas = round(suma_cuotas_confirmadas + cuota_efectivo_contrato.valor, 2)
                            elif indice == indice_referencia:
                                valor_cuota_predeterminada = round((valor_total_agrupacion - (monto_credito + valor_pagar_entidad_contrato + suma_cuotas_confirmadas)) / (len(cuotas_efectivo_contrato) - indice), 2)
                                cuota_efectivo_contrato.valor = valor_cuota_predeterminada
                            else:
                                cuota_efectivo_contrato.valor = valor_cuota_predeterminada
                            indice_referencia += 1

                    request.session['cuotas_efectivo_contrato'] = cuotas_efectivo_contrato
                    valor_pagar_efectivo_contrato = 0
                    for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                        valor_pagar_efectivo_contrato = round(valor_pagar_efectivo_contrato + cuota_efectivo_contrato.valor, 2)
                    render = render_to_string('ajax/ventas/pagosefectivocontratoventa.html', {'user': user, 'cuotas_efectivo_contrato': cuotas_efectivo_contrato, 'valor_efectivo_pagar': valor_pagar_efectivo_contrato})
                    dajax.assign('#id_panel_numero_cuotas', 'innerHTML', render)
                    dajax.alert('Pago efectivo eliminado correctamente')

                    # Actualiza el valor a pagar por el cliente
                    try:
                        monto_credito = request.session['monto_credito']
                    except :
                        monto_credito = 0
                    valor_pagar = monto_credito
                    for pago_entidad_contrato in pagos_entidades_contrato:
                        valor_pagar = round(valor_pagar + pago_entidad_contrato.valor, 2)

                    for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                        valor_pagar = round(valor_pagar + cuota_efectivo_contrato.valor, 2)

                    dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $' + str(intcomma(valor_pagar)))
                    dajax.assign('#id_valor_excedente_pagar_efectivo', 'innerHTML', 'Pagos en efectivo $' + str(intcomma(valor_pagar_efectivo_contrato)))
                    dajax.script("$('#id_numero_cuotas').val('"+ str(len(cuotas_efectivo_contrato)) + "');")
                    dajax.script("$('#id_numero_cuotas').trigger('chosen:updated');")
                else:
                    dajax.redirect('/inverboy/home/')
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def busqueda_adicionales_agrupacion_modificar_contrato_venta2(request, contrato_venta_id, proyecto_id, datos):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and adicionales_agrupacion_inmueble_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                tipo_adicional = ''
                criterio = ''

                if datos != None:
                    request.POST = deserialize_form(datos)
                    tipo_adicional = request.POST['tipo_adicional']
                    criterio = request.POST['criterio'].strip()
                    adicionales_agregar = None
                    try:
                        adicionales_agregar = request.session['adicionales_agregar']
                    except :
                        pass
                else:
                    adicionales_agregar = []
                    request.session['adicionales_agregar'] = adicionales_agregar

                # Filtra los adicionales del proyecto
                if tipo_adicional != '':
                    tipo_adicional = AdicionalAgrupacion.objects.get(id=tipo_adicional)
                else:
                    tipo_adicional = None
                adicionales_agrupacion_inmueble = proyecto.lista_adicionales_agrupaciones_inmueble(tipo_adicional=tipo_adicional, criterio=criterio)

                # Excluye los adicionales que ya se encuentran en el contrato
                ids_adicionales_contrato = []
                for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                    if type(adicional_agrupacion_inmueble_contrato) == type(AdicionalAgrupacion()):
                        ids_adicionales_contrato.append(adicional_agrupacion_inmueble_contrato.id)
                adicionales_agrupacion_inmueble = adicionales_agrupacion_inmueble.exclude(id__in=ids_adicionales_contrato)
                pag = Paginador(request, adicionales_agrupacion_inmueble, 20, 1)
                tipos_adicional = proyecto.lista_tipos_adicionales_agrupaciones_inmueble()
                render = render_to_string('ajax/ventas/busquedaadicionalesagrupacioninmueblemodificarcontratoventa.html', {'user': user, 'adicionales_agrupacion_inmueble': pag, 'adicionales_agrupacion_inmueble_seleccionados': adicionales_agregar, 'tipos_adicional': tipos_adicional, 'tipo_adicional_actual': tipo_adicional, 'criterio': criterio, 'contrato_venta': contrato_venta, 'proyecto': proyecto})
                dajax.assign('#light', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='block';")
                dajax.script("document.getElementById('fade').style.display='block';")
                dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def busqueda_clientes_modificar_contrato_venta2(request, contrato_venta_id, proyecto_id, datos):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        # Validacion de variables de session
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                criterio = ''

                if datos != None:
                    request.POST = deserialize_form(datos)
                    criterio = request.POST['criterio'].strip()
                    clientes_agregar = None
                    try:
                        clientes_agregar = request.session['clientes_agregar']
                    except :
                        pass
                else:
                    clientes_agregar = []
                    request.session['clientes_agregar'] = clientes_agregar

                # Filtra los clientes que se encuentren activos
                clientes = Cliente.objects.filter(estado=True)
                if criterio != '':
                    try:
                        criterio = int(criterio)
                        clientes = clientes.filter(identificacion=criterio)
                    except :
                        clientes = clientes.filter(Q(nombre_1__icontains=criterio) | Q(nombre_2__icontains=criterio) | Q(apellido_1__icontains=criterio) | Q(apellido_2__icontains=criterio))

                # Excluye los clientes que ya se encuentran en el contrato
                clientes = clientes.exclude(id=contrato_venta.cliente_principal_id)
                ids_clientes_contrato = []
                for cliente_contrato in clientes_contrato:
                    ids_clientes_contrato.append(cliente_contrato.id)
                clientes = clientes.exclude(id__in=ids_clientes_contrato)
                pag = Paginador(request, clientes, 20, 1)
                render = render_to_string('ajax/ventas/busquedaclientesmodificarcontratoventa.html', {'user': user, 'clientes': pag, 'clientes_seleccionados': clientes_agregar, 'criterio': criterio, 'contrato_venta': contrato_venta, 'proyecto': proyecto})
                dajax.assign('#light', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='block';")
                dajax.script("document.getElementById('fade').style.display='block';")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def seleccionar_cliente_modificar_contrato_venta2(request, cliente_id, parametro, criterio, pagina, contrato_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        # Validacion de variables de session
        clientes_contrato = None
        clientes_agregar = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            clientes_agregar = request.session['clientes_agregar']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and clientes_agregar != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)

                criterio = criterio.strip()
                # Filtra los clientes que se encuentren activos
                clientes = Cliente.objects.filter(estado=True)

                if parametro:
                    clientes_agregar.append(clientes.get(id=cliente_id))
                else:
                    for cliente_agregar in clientes_agregar:
                        if cliente_agregar.id == int(cliente_id):
                            clientes_agregar.remove(cliente_agregar)

                if criterio != '':
                    try:
                        criterio = int(criterio)
                        clientes = clientes.filter(identificacion=criterio)
                    except :
                        clientes = clientes.filter(Q(nombre_1__icontains=criterio) | Q(nombre_2__icontains=criterio) | Q(apellido_1__icontains=criterio) | Q(apellido_2__icontains=criterio))

                # Excluye los clientes que ya se encuentran en el contrato
                clientes = clientes.exclude(id=contrato_venta.cliente_principal_id)
                ids_clientes_contrato = []
                for cliente_contrato in clientes_contrato:
                    ids_clientes_contrato.append(cliente_contrato.id)
                clientes = clientes.exclude(id__in=ids_clientes_contrato)
                pag = Paginador(request, clientes, 20, int(pagina))
                render = render_to_string('ajax/ventas/busquedaclientesnuevocontratoventa.html', {'user': user, 'clientes': pag, 'clientes_seleccionados': clientes_agregar, 'criterio': criterio, 'contrato_venta': contrato_venta, 'proyecto': proyecto})
                dajax.assign('#light', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_clientes_modificar_contrato_venta2(request, contrato_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        # Validacion de variables de session
        clientes_contrato = None
        clientes_agregar = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            clientes_agregar = request.session['clientes_agregar']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and clientes_agregar != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)

                for cliente_agregar in clientes_agregar:
                    clientes_contrato.append(cliente_agregar)

                del request.session['clientes_agregar']

                render = render_to_string('ajax/ventas/clientesnuevocontratoventa.html', {'user': user, 'clientes': clientes_contrato, 'contrato_venta': contrato_venta, 'proyecto': proyecto})
                dajax.assign('#id_clientes', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='none';")
                dajax.script("document.getElementById('fade').style.display='none';")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_cliente_modificar_contrato_venta2(request, cliente_id, contrato_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta= proyecto.contratoventa_set.get(id=contrato_venta_id)

                for cliente_contrato in clientes_contrato:
                    if cliente_contrato.id == int(cliente_id) and contrato_venta.cliente_principal.cliente_id != int(cliente_id):
                        clientes_contrato.remove(cliente_contrato)

                render = render_to_string('ajax/ventas/clientesnuevocontratoventa.html', {'user': user, 'clientes': clientes_contrato, 'contrato_venta': contrato_venta, 'proyecto': proyecto})
                dajax.assign('#id_clientes', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def seleccionar_forma_pago_modificar_contrato_venta2(request, forma_pago, contrato_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                render = ''
                if forma_pago != '':
                    aplica_adicionales = False
                    if len(proyecto.lista_adicionales_agrupaciones_inmueble()) > 0:
                        aplica_adicionales = True
                    if (aplica_adicionales == True and len(adicionales_agrupacion_inmueble_contrato) > 0) or aplica_adicionales == False :
                        forma_pago = int(forma_pago)
                        request.session['forma_pago'] = forma_pago
                        if forma_pago == 2:
                            try:
                                del request.session['monto_credito']
                            except :
                                pass
                        form = ContratoVentaForm(initial={'forma_pago': forma_pago})
                        render = render_to_string('ajax/ventas/formapagonuevocontratoventa.html', {'user': user, 'forma_pago': forma_pago, 'form': form, 'contrato_venta': contrato_venta, 'proyecto': proyecto})
                    else:
                        dajax.assign('#id_error_adicionales', 'innerHTML', 'Debe seleccionar por lo menos 1 adicional')
                        dajax.script("$('#id_forma_pago').val('-----');")
                        dajax.script("$('#id_forma_pago').trigger('chosen:updated');")
                else:
                    try:
                        del request.session['forma_pago']
                        del request.session['monto_credito']
                    except :
                        pass
                request.session['pagos_entidades_contrato'] = []
                request.session['cuotas_efectivo_contrato'] = []
                dajax.assign('#id_panel_forma_pago', 'innerHTML', render)
                dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $' + str(intcomma(0.0)))
                dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def asignar_monto_credito_modificar_contrato_venta2(request, contrato_venta_id, monto_credito, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            proyecto = Proyecto.objects.get(id=proyecto_id)
            contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
            error_monto_credito = ''
            validaciones_monto_credito = Validator().append([
                Field('monto_credito', monto_credito).append([
                    IsRequired('Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
                ]),
            ]).run(True).pop()

            if validaciones_monto_credito['passed'] == True:
                monto_credito = float(monto_credito)
                request.session['monto_credito'] = monto_credito

                # Actualiza el valor a pagar por el cliente
                valor_pagar = 0
                valor_pagar_entidad_contrato = 0
                for pago_entidad_contrato in pagos_entidades_contrato:
                    valor_pagar = round(valor_pagar + pago_entidad_contrato.valor, 2)
                    valor_pagar_entidad_contrato = round(valor_pagar_entidad_contrato + pago_entidad_contrato.valor, 2)

                valor_pagar_efectivo_contrato = 0
                for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                    valor_pagar = round(valor_pagar + cuota_efectivo_contrato.valor, 2)
                    valor_pagar_efectivo_contrato = round(valor_pagar_efectivo_contrato + cuota_efectivo_contrato.valor, 2)

                valor_pagar= round(valor_pagar + monto_credito, 2)
                dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $' + str(intcomma(valor_pagar)))

                # Actualiza el valor en efectivo excedente a pagar por el cliente
                valor_total_inmueble = contrato_venta.agrupacion_contrato_venta().str_valor()
                for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                    valor_total_inmueble = round(valor_total_inmueble + adicional_agrupacion_inmueble_contrato.valor, 2)

                valor_excedente_pagar_efectivo = round(valor_total_inmueble - monto_credito - valor_pagar_entidad_contrato, 2)
                dajax.assign('#id_valor_excedente_pagar_efectivo', 'innerHTML', 'Pagos en efectivo $' + str(intcomma(valor_excedente_pagar_efectivo)))

                dajax.script("document.getElementById('id_monto_credito').value = '" + str(monto_credito) + "';")
                dajax.script("document.getElementById('id_monto_credito_0').value = '" + str(intcomma(monto_credito)) + "';")
                dajax.script("document.getElementById('id_monto_credito_0').readOnly = true;")
                dajax.script("document.getElementById('id_btn_asignar_monto_credito').style.display = 'none';")
                dajax.script("document.getElementById('id_btn_modificar_monto_credito').style.display = 'block';")
            else:
                for error in validaciones_monto_credito['errors']:
                    error_monto_credito = error
                dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $ -')
            dajax.assign('#id_error_monto_credito', 'innerHTML', error_monto_credito)
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def seleccionar_adicional_agrupacion_inmueble_modificar_contrato_venta2(request, adicional_agrupacion_inmueble_id, parametro, pagina, tipo_adicional_id, criterio, contrato_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        # Validacion de variables de session
        clientes_contrato = None
        adicionales_agregar = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            adicionales_agregar = request.session['adicionales_agregar']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and adicionales_agregar != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)

                if parametro:
                    adicionales_agregar.append(proyecto.lista_adicionales_agrupaciones_inmueble().get(id=adicional_agrupacion_inmueble_id))
                else:
                    for adicional_agregar in adicionales_agregar:
                        if adicional_agregar.id == int(adicional_agrupacion_inmueble_id):
                            adicionales_agregar.remove(adicional_agregar)

                criterio = criterio.strip()

                # Filtra los adicionales del proyecto
                if tipo_adicional_id != None and tipo_adicional_id != '':
                    tipo_adicional = AdicionalAgrupacion.objects.get(id=tipo_adicional_id)
                else:
                    tipo_adicional = None

                adicionales_agrupacion_inmueble = proyecto.lista_adicionales_agrupaciones_inmueble(tipo_adicional=tipo_adicional, criterio=criterio)

                # Excluye los adicionales que ya se encuentran en el contrato
                ids_adicionales_contrato = []
                for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                    if type(adicional_agrupacion_inmueble_contrato) == type(AdicionalAgrupacion()):
                        ids_adicionales_contrato.append(adicional_agrupacion_inmueble_contrato.id)
                adicionales_agrupacion_inmueble = adicionales_agrupacion_inmueble.exclude(id__in=ids_adicionales_contrato)
                pag = Paginador(request, adicionales_agrupacion_inmueble, 20, int(pagina))
                tipos_adicional = proyecto.lista_tipos_adicionales_agrupaciones_inmueble()
                render = render_to_string('ajax/ventas/busquedaadicionalesagrupacioninmueblenuevocontratoventa.html', {'user': user, 'adicionales_agrupacion_inmueble': pag, 'adicionales_agrupacion_inmueble_seleccionados': adicionales_agregar, 'tipos_adicional': tipos_adicional, 'tipo_adicional_actual': tipo_adicional, 'criterio': criterio, 'contrato_venta': contrato_venta, 'proyecto': proyecto})
                dajax.assign('#light', 'innerHTML', render)
                dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_adicionales_agrupacion_inmueble_modificar_contrato_venta2(request, contrato_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        # Validacion de variables de session
        clientes_contrato = None
        adicionales_agregar = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            adicionales_agregar = request.session['adicionales_agregar']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and adicionales_agregar != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)

                for adicional_agregar in adicionales_agregar:
                    adicionales_agrupacion_inmueble_contrato.append(adicional_agregar)

                del request.session['adicionales_agregar']

                render = render_to_string('ajax/ventas/adicionalesnuevocontratoventa.html', {'user': user, 'adicionales_agrupacion_inmueble_contrato': adicionales_agrupacion_inmueble_contrato, 'contrato_venta': contrato_venta, 'proyecto': proyecto})
                dajax.assign('#id_adicionales', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='none';")
                dajax.script("document.getElementById('fade').style.display='none';")

                valor_total_agrupacion = contrato_venta.agrupacion_contrato_venta().str_valor()

                for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                    valor_total_agrupacion = round(valor_total_agrupacion + adicional_agrupacion_inmueble_contrato.valor, 2)

                dajax.assign('#id_valor_inmueble', 'innerHTML', 'VALOR INMUEBLE $' + str(intcomma(valor_total_agrupacion)))
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_adicional_agrupacion_inmueble_modificar_contrato_venta2(request, indice, contrato_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        # Validacion de variables de session
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)

                adicionales_agrupacion_inmueble_contrato.pop(int(indice))
                
                request.session['adicionales_agrupacion_inmueble_contrato'] = adicionales_agrupacion_inmueble_contrato

                render = render_to_string('ajax/ventas/adicionalesnuevocontratoventa.html', {'user': user, 'adicionales_agrupacion_inmueble_contrato': adicionales_agrupacion_inmueble_contrato, 'contrato_venta': contrato_venta, 'proyecto': proyecto})
                dajax.assign('#id_adicionales', 'innerHTML', render)

                valor_total_agrupacion = contrato_venta.agrupacion_contrato_venta().str_valor()

                for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                    valor_total_agrupacion = round(valor_total_agrupacion + adicional_agrupacion_inmueble_contrato.valor, 2)

                dajax.assign('#id_valor_inmueble', 'innerHTML', 'VALOR INMUEBLE $' + str(intcomma(valor_total_agrupacion)))
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_pago_entidad_modificar_contrato_venta2(request, contrato_venta_id, datos, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                if datos:
                    request.POST = deserialize_form(datos)
                    form = PagoEntidadContratoVentaForm(contrato_venta=contrato_venta, data=request.POST)
                    if form.is_valid():
                        pago_entidad_contrato_venta = PagoEntidadContratoVenta()
                        pago_entidad_contrato_venta.tipo_cuenta = form.cleaned_data['tipo_cuenta']
                        pago_entidad_contrato_venta.entidad = form.cleaned_data['entidad']
                        if form.cleaned_data['numero_cuenta'].strip() != '':
                            pago_entidad_contrato_venta.numero_cuenta = form.cleaned_data['numero_cuenta'].strip()
                        pago_entidad_contrato_venta.fecha_desembolso = form.cleaned_data['fecha_desembolso']
                        pago_entidad_contrato_venta.valor = float(form.cleaned_data['valor'])
                        pagos_entidades_contrato.append(pago_entidad_contrato_venta)
                        request.session['pagos_entidades_contrato'] = pagos_entidades_contrato
                        # Actualiza el valor a pagar por parte de entidades
                        valor_pagar_entidad_contrato = 0
                        for pago_entidad_contrato in pagos_entidades_contrato:
                            valor_pagar_entidad_contrato = round(valor_pagar_entidad_contrato + pago_entidad_contrato.valor, 2)
                        render = render_to_string('ajax/ventas/pagosentidadcontratoventa.html', {'user': user, 'pagos_entidades_contrato': pagos_entidades_contrato, 'valor_pagar_entidad_contrato': valor_pagar_entidad_contrato})
                        dajax.assign('#id_reporte_pagos_entidad', 'innerHTML', render)
                        dajax.script("document.getElementById('light').style.display='none';")
                        dajax.script("document.getElementById('fade').style.display='none';")

                        # Actualiza el valor a pagar por el cliente
                        try:
                            monto_credito = request.session['monto_credito']
                        except :
                            monto_credito = 0
                        valor_pagar = round(monto_credito + valor_pagar_entidad_contrato, 2)

                        for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                            valor_pagar = round(valor_pagar + cuota_efectivo_contrato.valor, 2)

                        dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $' + str(intcomma(valor_pagar)))

                        # Actualiza el valor en efectivo excedente a pagar por el cliente
                        valor_total_inmueble = contrato_venta.agrupacion_contrato_venta().str_valor()
                        for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                            valor_total_inmueble = round(valor_total_inmueble + adicional_agrupacion_inmueble_contrato.valor, 2)

                        valor_excedente_pagar_efectivo = round(valor_total_inmueble - monto_credito - valor_pagar_entidad_contrato, 2)
                        dajax.assign('#id_valor_excedente_pagar_efectivo', 'innerHTML', 'Pagos en efectivo $' + str(intcomma(valor_excedente_pagar_efectivo)))

                        dajax.alert('Nuevo pago agregado correctamente')
                        return dajax.json()
                else:
                    form = PagoEntidadContratoVentaForm()
                render = render_to_string('ajax/ventas/nuevopagoentidadcontratoventa.html', {'user': user, 'form': form, 'change': 0}, context_instance=RequestContext(request))
                dajax.assign('#light', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='block';")
                dajax.script("document.getElementById('fade').style.display='block';")
                dajax.script("Calendar.setup({inputField:'id_fecha_desembolso',ifFormat:'%Y-%m-%d',button:'lanzador_fecha_desembolso'});")
                dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_pago_entidad_modificar_contrato_venta2(request, contrato_venta_id, indice, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                # Verifica que el pago de la entidad no se encuentre checkiado (Pagado)
                pago_entidad_contrato = pagos_entidades_contrato[int(indice)]
                if pago_entidad_contrato.permite_modificacion():
                    pagos_entidades_contrato.pop(int(indice))
                    request.session['pagos_entidades_contrato'] = pagos_entidades_contrato
                    # Actualiza el valor a pagar por parte de entidades
                    valor_pagar_entidad_contrato = 0
                    for pago_entidad_contrato in pagos_entidades_contrato:
                        valor_pagar_entidad_contrato = round(valor_pagar_entidad_contrato + pago_entidad_contrato.valor, 2)

                    render = render_to_string('ajax/ventas/pagosentidadcontratoventa.html', {'user': user, 'pagos_entidades_contrato': pagos_entidades_contrato, 'valor_pagar_entidad_contrato': valor_pagar_entidad_contrato})
                    dajax.assign('#id_reporte_pagos_entidad', 'innerHTML', render)
                    dajax.alert('Pago entidad eliminado correctamente')

                    # Actualiza el valor a pagar por el cliente
                    try:
                        monto_credito = request.session['monto_credito']
                    except :
                        monto_credito = 0
                    valor_pagar = round(monto_credito + valor_pagar_entidad_contrato, 2)

                    for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                        valor_pagar = round(valor_pagar + cuota_efectivo_contrato.valor, 2)

                    dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $' + str(intcomma(valor_pagar)))

                    # Actualiza el valor en efectivo excedente a pagar por el cliente
                    valor_total_inmueble = contrato_venta.agrupacion_contrato_venta().str_valor()
                    for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                        valor_total_inmueble = round(valor_total_inmueble + adicional_agrupacion_inmueble_contrato.valor, 2)

                    valor_excedente_pagar_efectivo = round(valor_total_inmueble - monto_credito - valor_pagar_entidad_contrato, 2)
                    dajax.assign('#id_valor_excedente_pagar_efectivo', 'innerHTML', 'Pagos en efectivo $' + str(intcomma(valor_excedente_pagar_efectivo)))
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_pago_entidad_modificar_contrato_venta2(request, contrato_venta_id, datos, indice, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                if datos:
                    request.POST = deserialize_form(datos)
                    indice = int(request.POST['indice'])
                    pago_entidad_contrato_venta = pagos_entidades_contrato[indice]
                    form = PagoEntidadContratoVentaForm(contrato_venta=contrato_venta, instance=pago_entidad_contrato_venta, data=request.POST)
                    # Verifica que el pago de la entidad no se encuentre checkiado (Pagado)
                    if pago_entidad_contrato_venta.id != None:
                        if not pago_entidad_contrato_venta.permite_modificacion():
                            form.fields.pop('valor')
                    if form.is_valid():
                        pago_entidad_contrato_venta.tipo_cuenta = form.cleaned_data['tipo_cuenta']
                        pago_entidad_contrato_venta.entidad = form.cleaned_data['entidad']
                        if form.cleaned_data['numero_cuenta'].strip() != '':
                            pago_entidad_contrato_venta.numero_cuenta = form.cleaned_data['numero_cuenta'].strip()
                        pago_entidad_contrato_venta.fecha_desembolso = form.cleaned_data['fecha_desembolso']
                        if pago_entidad_contrato_venta.id != None:
                            if pago_entidad_contrato_venta.permite_modificacion():
                                pago_entidad_contrato_venta.valor = float(form.cleaned_data['valor'])
                        # Actualiza el valor a pagar por parte de entidades
                        valor_pagar_entidad_contrato = 0
                        for pago_entidad_contrato in pagos_entidades_contrato:
                            valor_pagar_entidad_contrato = round(valor_pagar_entidad_contrato + pago_entidad_contrato.valor, 2)
                        request.session['pagos_entidades_contrato'] = pagos_entidades_contrato
                        render = render_to_string('ajax/ventas/pagosentidadcontratoventa.html', {'user': user, 'pagos_entidades_contrato': pagos_entidades_contrato, 'valor_pagar_entidad_contrato': valor_pagar_entidad_contrato})
                        dajax.assign('#id_reporte_pagos_entidad', 'innerHTML', render)
                        dajax.script("document.getElementById('light').style.display='none';")
                        dajax.script("document.getElementById('fade').style.display='none';")

                        # Actualiza el valor a pagar por el cliente
                        try:
                            monto_credito = request.session['monto_credito']
                        except :
                            monto_credito = 0
                        valor_pagar = round(monto_credito + valor_pagar_entidad_contrato, 2)

                        for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                            valor_pagar = round(valor_pagar + cuota_efectivo_contrato.valor, 2)

                        dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $' + str(intcomma(valor_pagar)))

                        # Actualiza el valor en efectivo excedente a pagar por el cliente
                        valor_total_inmueble = contrato_venta.agrupacion_contrato_venta().str_valor()
                        for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                            valor_total_inmueble = round(valor_total_inmueble + adicional_agrupacion_inmueble_contrato.valor, 2)

                        valor_excedente_pagar_efectivo = round(valor_total_inmueble - monto_credito - valor_pagar_entidad_contrato, 2)
                        dajax.assign('#id_valor_excedente_pagar_efectivo', 'innerHTML', 'Pagos en efectivo $' + str(intcomma(valor_excedente_pagar_efectivo)))

                        dajax.alert('Nuevo pago modificado correctamente')
                        return dajax.json()
                else:
                    pago_entidad_contrato_venta = pagos_entidades_contrato[int(indice)]
                    entidad = ''
                    if pago_entidad_contrato_venta.entidad != None:
                        entidad = pago_entidad_contrato_venta.entidad
                    numero_cuenta = ''
                    if pago_entidad_contrato_venta.numero_cuenta != None:
                        numero_cuenta = pago_entidad_contrato_venta.numero_cuenta
                    fecha_desembolso = ''
                    if pago_entidad_contrato_venta.fecha_desembolso != None:
                        fecha_desembolso = pago_entidad_contrato_venta.fecha_desembolso.strftime('%Y-%m-%d')
                    form = PagoEntidadContratoVentaForm(initial={'tipo_cuenta': pago_entidad_contrato_venta.tipo_cuenta, 'entidad': entidad, 'numero_cuenta': numero_cuenta, 'fecha_desembolso': fecha_desembolso, 'valor': pago_entidad_contrato_venta.valor})
                    # Verifica que el pago de la entidad no se encuentre checkiado (Pagado)
                    if pago_entidad_contrato_venta.id != None:
                        if not pago_entidad_contrato_venta.permite_modificacion():
                            form.fields.pop('valor')
                render = render_to_string('ajax/ventas/nuevopagoentidadcontratoventa.html', {'user': user, 'form': form, 'indice': indice, 'change': 1}, context_instance=RequestContext(request))
                dajax.assign('#light', 'innerHTML', render)
                dajax.script("document.getElementById('light').style.display='block';")
                dajax.script("document.getElementById('fade').style.display='block';")
                dajax.script("Calendar.setup({inputField:'id_fecha_desembolso',ifFormat:'%Y-%m-%d',button:'lanzador_fecha_desembolso'});")
                dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def seleccionar_numero_cuotas_efectivo_modificar_contrato_venta2(request, numero_cuotas, contrato_venta_id, proyecto_id):
    import datetime
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        forma_pago = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
            forma_pago = request.session['forma_pago']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                monto_credito = 0
                if forma_pago == 1:
                    try:
                        monto_credito = request.session['monto_credito']
                    except :
                        monto_credito = None
                # Veridica que se haya registrado un monto para el credito
                if monto_credito != None:
                    cuotas_efectivo_contrato = []
                    request.session['cuotas_efectivo_contrato'] = cuotas_efectivo_contrato
                    render = ''
                    if numero_cuotas != '':
                        # Calcula el valor de la agrupación
                        valor_total_agrupacion = contrato_venta.agrupacion_contrato_venta().str_valor()

                        for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                            valor_total_agrupacion = round(valor_total_agrupacion + adicional_agrupacion_inmueble_contrato.valor, 2)

                        # Calcula el valor a pagar por el cliente
                        valor_pagar = monto_credito
                        for pago_entidad_contrato in pagos_entidades_contrato:
                            valor_pagar = round(valor_pagar + pago_entidad_contrato.valor, 2)

                        valor_pendiente_pagar = round(valor_total_agrupacion - valor_pagar, 2)

                        numero_cuotas = int(numero_cuotas)
                        valor_cuota = round(valor_pendiente_pagar / numero_cuotas, 2)

                        anio_actual = datetime.date.today().year
                        mes_actual = datetime.date.today().month
                        dia_actual = datetime.date.today().day

                        for cuota in range(mes_actual + 1, numero_cuotas + mes_actual + 1):
                            cuota_efectivo_contrato = PagoEfectivoContratoVenta()
                            coeficiente = int(round(cuota / 12, 0))
                            if cuota % 12 == 0:
                                coeficiente -= 1
                            anio = anio_actual + coeficiente
                            mes = cuota
                            if cuota > 12:
                                mes = (cuota - (coeficiente * 12))
                            cuota_adicionada = False
                            dia = dia_actual
                            while cuota_adicionada == False:
                                try:
                                    cuota_efectivo_contrato.fecha_desembolso = datetime.date(anio, mes, dia)
                                    cuota_adicionada = True
                                except :
                                    dia = dia - 1
                            cuota_efectivo_contrato.valor = valor_cuota
                            cuotas_efectivo_contrato.append(cuota_efectivo_contrato)
                        render = render_to_string('ajax/ventas/pagosefectivocontratoventa.html', {'user': user, 'cuotas_efectivo_contrato': cuotas_efectivo_contrato, 'valor_efectivo_pagar': valor_pendiente_pagar, 'contrato_venta': contrato_venta, 'proyecto': proyecto})

                    dajax.assign('#id_panel_numero_cuotas', 'innerHTML', render)
                    # Actualiza el valor a pagar por el cliente
                    valor_pagar = monto_credito or 0
                    for pago_entidad_contrato in pagos_entidades_contrato:
                        valor_pagar = round(valor_pagar + pago_entidad_contrato.valor, 2)

                    for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                        valor_pagar = round(valor_pagar + cuota_efectivo_contrato.valor, 2)

                    dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $' + str(intcomma(valor_pagar)))
                else:
                    dajax.assign('#id_error_monto_credito', 'innerHTML', 'Debe ingresar un monto para credito')
                    dajax.script("$('#id_numero_cuotas').val('');")
                    dajax.script("$('#id_numero_cuotas').trigger('chosen:updated');")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def agregar_pago_efectivo_modificar_contrato_venta2(request, contrato_venta_id, datos, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        forma_pago = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
            forma_pago = request.session['forma_pago']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                monto_credito = 0
                if forma_pago == 1:
                    try:
                        monto_credito = request.session['monto_credito']
                    except :
                        monto_credito = None
                # Veridica que se haya registrado un monto para el credito
                if monto_credito != None:
                    form = PagoEfectivoContratoVentaForm()
                    if datos != None:
                        request.POST = deserialize_form(datos)
                        form = PagoEfectivoContratoVentaForm(request.POST)
                        if form.is_valid():
                            nueva_cuota_efectivo_contrato = PagoEfectivoContratoVenta()
                            nueva_cuota_efectivo_contrato.fecha_desembolso = form.cleaned_data['fecha_desembolso']
                            nueva_cuota_efectivo_contrato.valor = float(form.cleaned_data['valor'])
                            cuotas_efectivo_contrato.append(nueva_cuota_efectivo_contrato)

                            # Ordena las cuotas por fecha de desembolso
                            cuotas_efectivo_contrato.sort(compara_fechas_cuotas_efectivo)

                            # Calcula el valor de la agrupación
                            valor_total_agrupacion = contrato_venta.agrupacion_contrato_venta().str_valor()

                            for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                                valor_total_agrupacion = round(valor_total_agrupacion + adicional_agrupacion_inmueble_contrato.valor, 2)

                            valor_pagar = monto_credito
                            valor_pagar_entidad_contrato = 0
                            for pago_entidad_contrato in pagos_entidades_contrato:
                                valor_pagar = round(valor_pagar + pago_entidad_contrato.valor, 2)
                                valor_pagar_entidad_contrato = round(valor_pagar_entidad_contrato + pago_entidad_contrato.valor, 2)

                            valor_pagar_efectivo_contrato = 0
                            for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                                valor_pagar_efectivo_contrato = round(valor_pagar_efectivo_contrato + cuota_efectivo_contrato.valor, 2)

                            valor_pagar = round(valor_pagar + valor_pagar_efectivo_contrato, 2)

                            # Se recalcula el valor de las cuotas a partir de la nueva cuota agregada
                            if not(valor_pagar < round(valor_total_agrupacion + 100, 2) and valor_pagar > round(valor_total_agrupacion - 100, 2)):
                                suma_cuotas_confirmadas = 0
                                cuota_encontrada = False
                                indice = 0
                                valor_cuota_predeterminada = 0
                                for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                                    indice += 1
                                    if cuota_efectivo_contrato.fecha_desembolso == nueva_cuota_efectivo_contrato.fecha_desembolso:
                                        if len(cuotas_efectivo_contrato) - indice > 0:
                                            suma_cuotas_confirmadas = round(suma_cuotas_confirmadas + cuota_efectivo_contrato.valor, 2)
                                            valor_cuota_predeterminada = round((valor_total_agrupacion - (monto_credito + valor_pagar_entidad_contrato + suma_cuotas_confirmadas)) / (len(cuotas_efectivo_contrato) - indice), 2)
                                            cuota_encontrada = True
                                    elif cuota_encontrada == False:
                                        suma_cuotas_confirmadas = round(suma_cuotas_confirmadas + cuota_efectivo_contrato.valor, 2)
                                    else:
                                        cuota_efectivo_contrato.valor = valor_cuota_predeterminada

                            request.session['cuotas_efectivo_contrato'] = cuotas_efectivo_contrato
                            valor_pagar_efectivo_contrato = 0
                            for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                                valor_pagar_efectivo_contrato = round(valor_pagar_efectivo_contrato + cuota_efectivo_contrato.valor, 2)

                            render = render_to_string('ajax/ventas/pagosefectivocontratoventa.html', {'user': user, 'cuotas_efectivo_contrato': cuotas_efectivo_contrato, 'valor_efectivo_pagar': valor_pagar_efectivo_contrato})
                            dajax.assign('#id_panel_numero_cuotas', 'innerHTML', render)
                            dajax.alert('Pago efectivo agregado correctamente')

                            # Actualiza el valor a pagar por el cliente
                            valor_pagar = monto_credito
                            for pago_entidad_contrato in pagos_entidades_contrato:
                                valor_pagar = round(valor_pagar + pago_entidad_contrato.valor, 2)

                            valor_pagar = round(valor_pagar + valor_pagar_efectivo_contrato, 2)

                            dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $' + str(intcomma(valor_pagar)))
                            dajax.assign('#id_valor_excedente_pagar_efectivo', 'innerHTML', 'Pagos en efectivo $' + str(intcomma(valor_pagar_efectivo_contrato)))
                            dajax.script("$('#id_numero_cuotas').val('"+ str(len(cuotas_efectivo_contrato)) + "');")
                            dajax.script("document.getElementById('light').style.display='none';")
                            dajax.script("document.getElementById('fade').style.display='none';")
                            dajax.script("$('#id_numero_cuotas').trigger('chosen:updated');")
                            return dajax.json()
                    render = render_to_string('ajax/ventas/nuevopagoefectivocontratoventa.html', {'user': user, 'form': form, 'change': 0}, context_instance=RequestContext(request))
                    dajax.assign('#light', 'innerHTML', render)
                    dajax.script("document.getElementById('light').style.display='block';")
                    dajax.script("document.getElementById('fade').style.display='block';")
                    dajax.script("Calendar.setup({inputField:'id_fecha_desembolso',ifFormat:'%Y-%m-%d',button:'lanzador_fecha_desembolso'});")
                else:
                    dajax.assign('#id_error_monto_credito', 'innerHTML', 'Debe ingresar un monto para credito')
                    dajax.script("$('#id_numero_cuotas').val('');")
                    dajax.script("$('#id_numero_cuotas').trigger('chosen:updated');")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_pago_efectivo_modificar_contrato_venta2(request, contrato_venta_id, indice, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        forma_pago = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
            forma_pago = request.session['forma_pago']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                monto_credito = 0
                if forma_pago == 1:
                    try:
                        monto_credito = request.session['monto_credito']
                    except :
                        monto_credito = None
                # Veridica que se haya registrado un monto para el credito
                if monto_credito != None:
                    cuotas_efectivo_contrato.pop(int(indice))

                    # Calcula el valor de la agrupación
                    valor_total_agrupacion = contrato_venta.agrupacion_contrato_venta().str_valor()

                    for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                        valor_total_agrupacion = round(valor_total_agrupacion + adicional_agrupacion_inmueble_contrato.valor, 2)

                    valor_pagar = monto_credito
                    valor_pagar_entidad_contrato = 0
                    for pago_entidad_contrato in pagos_entidades_contrato:
                        valor_pagar = round(valor_pagar + pago_entidad_contrato.valor, 2)
                        valor_pagar_entidad_contrato = round(valor_pagar_entidad_contrato + pago_entidad_contrato.valor, 2)

                    valor_pagar_efectivo_contrato = 0
                    for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                        valor_pagar_efectivo_contrato = round(valor_pagar_efectivo_contrato + cuota_efectivo_contrato.valor, 2)

                    valor_pagar = round(valor_pagar + valor_pagar_efectivo_contrato, 2)

                    # Se recalcula el valor de las cuotas a partir de la cuota eliminada
                    indice = int(indice)
                    if not(valor_pagar < round(valor_total_agrupacion + 100, 2) and valor_pagar > round(valor_total_agrupacion - 100, 2)):
                        suma_cuotas_confirmadas = 0
                        indice_referencia = 0
                        valor_cuota_predeterminada = 0
                        for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                            if indice_referencia < indice:
                                suma_cuotas_confirmadas = round(suma_cuotas_confirmadas + cuota_efectivo_contrato.valor, 2)
                            elif indice == indice_referencia:
                                valor_cuota_predeterminada = round((valor_total_agrupacion - (monto_credito + valor_pagar_entidad_contrato + suma_cuotas_confirmadas)) / (len(cuotas_efectivo_contrato) - indice), 2)
                                cuota_efectivo_contrato.valor = valor_cuota_predeterminada
                            else:
                                cuota_efectivo_contrato.valor = valor_cuota_predeterminada
                            indice_referencia += 1

                    request.session['cuotas_efectivo_contrato'] = cuotas_efectivo_contrato
                    valor_pagar_efectivo_contrato = 0
                    for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                        valor_pagar_efectivo_contrato = round(valor_pagar_efectivo_contrato + cuota_efectivo_contrato.valor, 2)
                    render = render_to_string('ajax/ventas/pagosefectivocontratoventa.html', {'user': user, 'cuotas_efectivo_contrato': cuotas_efectivo_contrato, 'valor_efectivo_pagar': valor_pagar_efectivo_contrato})
                    dajax.assign('#id_panel_numero_cuotas', 'innerHTML', render)
                    dajax.alert('Pago efectivo eliminado correctamente')

                    # Actualiza el valor a pagar por el cliente
                    try:
                        monto_credito = request.session['monto_credito']
                    except :
                        monto_credito = 0
                    valor_pagar = monto_credito
                    for pago_entidad_contrato in pagos_entidades_contrato:
                        valor_pagar = round(valor_pagar + pago_entidad_contrato.valor, 2)

                    for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                        valor_pagar = round(valor_pagar + cuota_efectivo_contrato.valor, 2)

                    dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $' + str(intcomma(valor_pagar)))
                    dajax.assign('#id_valor_excedente_pagar_efectivo', 'innerHTML', 'Pagos en efectivo $' + str(intcomma(valor_pagar_efectivo_contrato)))
                    dajax.script("$('#id_numero_cuotas').val('"+ str(len(cuotas_efectivo_contrato)) + "');")
                    dajax.script("$('#id_numero_cuotas').trigger('chosen:updated');")
                else:
                    dajax.assign('#id_error_monto_credito', 'innerHTML', 'Debe ingresar un monto para credito')
                    dajax.script("$('#id_numero_cuotas').val('');")
                    dajax.script("$('#id_numero_cuotas').trigger('chosen:updated');")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def modificar_pago_efectivo_modificar_contrato_venta2(request, contrato_venta_id, datos, indice, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        forma_pago = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
            forma_pago = request.session['forma_pago']
        except :
            pass
        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                monto_credito = 0
                if forma_pago == 1:
                    try:
                        monto_credito = request.session['monto_credito']
                    except :
                        monto_credito = None
                # Veridica que se haya registrado un monto para el credito
                if monto_credito != None:
                    if datos != None:
                        request.POST = deserialize_form(datos)
                        indice = int(request.POST['indice'])
                        form = PagoEfectivoContratoVentaForm(request.POST)
                        if form.is_valid():
                            cuota_efectivo_contrato_modificar = cuotas_efectivo_contrato[indice]
                            cuota_efectivo_contrato_modificar.fecha_desembolso = form.cleaned_data['fecha_desembolso']
                            cuota_efectivo_contrato_modificar.valor = float(form.cleaned_data['valor'])

                            # Ordena las cuotas por fecha de desembolso
                            cuotas_efectivo_contrato.sort(compara_fechas_cuotas_efectivo)

                            # Calcula el valor de la agrupación
                            valor_total_agrupacion = contrato_venta.agrupacion_contrato_venta().str_valor()

                            for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                                valor_total_agrupacion = round(valor_total_agrupacion + adicional_agrupacion_inmueble_contrato.valor, 2)

                            valor_pagar = monto_credito
                            valor_pagar_entidad_contrato = 0
                            for pago_entidad_contrato in pagos_entidades_contrato:
                                valor_pagar = round(valor_pagar + pago_entidad_contrato.valor, 2)
                                valor_pagar_entidad_contrato = round(valor_pagar_entidad_contrato + pago_entidad_contrato.valor, 2)

                            valor_pagar_efectivo_contrato = 0
                            for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                                valor_pagar_efectivo_contrato = round(valor_pagar_efectivo_contrato + cuota_efectivo_contrato.valor, 2)

                            valor_pagar = round(valor_pagar + valor_pagar_efectivo_contrato, 2)

                            # Se recalcula el valor de las cuotas a partir de la nueva cuota agregada
                            if not(valor_pagar < round(valor_total_agrupacion + 100, 2) and valor_pagar > round(valor_total_agrupacion - 100, 2)):
                                suma_cuotas_confirmadas = 0
                                cuota_encontrada = False
                                indice = 0
                                valor_cuota_predeterminada = 0
                                for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                                    indice += 1
                                    if cuota_efectivo_contrato.fecha_desembolso == cuota_efectivo_contrato_modificar.fecha_desembolso:
                                        if len(cuotas_efectivo_contrato) - indice > 0:
                                            suma_cuotas_confirmadas = round(suma_cuotas_confirmadas + cuota_efectivo_contrato.valor, 2)
                                            valor_cuota_predeterminada = round((valor_total_agrupacion - (monto_credito + valor_pagar_entidad_contrato + suma_cuotas_confirmadas)) / (len(cuotas_efectivo_contrato) - indice), 2)
                                            cuota_encontrada = True
                                    elif cuota_encontrada == False:
                                        suma_cuotas_confirmadas = round(suma_cuotas_confirmadas + cuota_efectivo_contrato.valor, 2)
                                    else:
                                        cuota_efectivo_contrato.valor = valor_cuota_predeterminada

                            request.session['cuotas_efectivo_contrato'] = cuotas_efectivo_contrato
                            valor_pagar_efectivo_contrato = 0
                            for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                                valor_pagar_efectivo_contrato = round(valor_pagar_efectivo_contrato + cuota_efectivo_contrato.valor, 2)

                            render = render_to_string('ajax/ventas/pagosefectivocontratoventa.html', {'user': user, 'cuotas_efectivo_contrato': cuotas_efectivo_contrato, 'valor_efectivo_pagar': valor_pagar_efectivo_contrato})
                            dajax.assign('#id_panel_numero_cuotas', 'innerHTML', render)
                            dajax.alert('Pago efectivo modificado correctamente')

                            # Actualiza el valor a pagar por el cliente
                            valor_pagar = monto_credito
                            for pago_entidad_contrato in pagos_entidades_contrato:
                                valor_pagar = round(valor_pagar + pago_entidad_contrato.valor, 2)

                            valor_pagar = round(valor_pagar + valor_pagar_efectivo_contrato, 2)

                            dajax.assign('#id_valor_pagar', 'innerHTML', 'VALOR A PAGAR $' + str(intcomma(valor_pagar)))
                            dajax.assign('#id_valor_excedente_pagar_efectivo', 'innerHTML', 'Pagos en efectivo $' + str(intcomma(valor_pagar_efectivo_contrato)))
                            dajax.script("$('#id_numero_cuotas').val('"+ str(len(cuotas_efectivo_contrato)) + "');")
                            dajax.script("document.getElementById('light').style.display='none';")
                            dajax.script("document.getElementById('fade').style.display='none';")
                            dajax.script("$('#id_numero_cuotas').trigger('chosen:updated');")
                            return dajax.json()
                    else:
                        cuota_efectivo_contrato_modificar = cuotas_efectivo_contrato[int(indice)]
                        form = PagoEfectivoContratoVentaForm(initial={'fecha_desembolso': cuota_efectivo_contrato_modificar.fecha_desembolso.strftime('%Y-%m-%d'), 'valor': cuota_efectivo_contrato_modificar.valor})
                    render = render_to_string('ajax/ventas/nuevopagoefectivocontratoventa.html', {'user': user, 'form': form, 'indice': indice, 'change': 1}, context_instance=RequestContext(request))
                    dajax.assign('#light', 'innerHTML', render)
                    dajax.script("document.getElementById('light').style.display='block';")
                    dajax.script("document.getElementById('fade').style.display='block';")
                    dajax.script("Calendar.setup({inputField:'id_fecha_desembolso',ifFormat:'%Y-%m-%d',button:'lanzador_fecha_desembolso'});")
                else:
                    dajax.assign('#id_error_monto_credito', 'innerHTML', 'Debe ingresar un monto para credito')
                    dajax.script("$('#id_numero_cuotas').val('');")
                    dajax.script("$('#id_numero_cuotas').trigger('chosen:updated');")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def registrar_abono_entidad_contrato_venta2(request, contrato_venta_id, proyecto_id, pago_entidad_contrato_venta_id, datos):
    from datetime import datetime
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if request.is_ajax():
            if 'inverboy.add_contratoventa' in user.get_all_permissions():
                usuario = Usuario.objects.get(id=user.id)
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                if datos:
                    request.POST = deserialize_form(datos)
                    pago_entidad_contrato_venta = contrato_venta.pagoentidadcontratoventa_set.get(id=request.POST['pago_entidad_contrato_venta'])
                    if pago_entidad_contrato_venta.permite_modificacion():
                        form = AbonoPagoEntidadContratoVentaForm(data=request.POST)
                        if form.is_valid():
                            valor = form.cleaned_data['valor']
                            if valor >= pago_entidad_contrato_venta.valor:
                                pago_entidad_contrato_venta.valor_desembolsado = form.cleaned_data['valor']
                                pago_entidad_contrato_venta.fecha_registro_desembolso = datetime.today()
                                pago_entidad_contrato_venta.usuario_registro_desembolso = usuario
                                pago_entidad_contrato_venta.save()
                                dajax.alert('Nuevo pago registrado correctamente')
                                dajax.redirect('/inverboy/home/detallescontratoventa/' + str(contrato_venta_id) + '/' + str(proyecto_id) + '/')
                            else:
                                form._errors["valor"] = ErrorList([u"El valor no puede ser menor al valor de desembolso registrado."])
                    else:
                        dajax.redirect('/inverboy/home/')
                else:
                    pago_entidad_contrato_venta = contrato_venta.pagoentidadcontratoventa_set.get(id=pago_entidad_contrato_venta_id)
                    if pago_entidad_contrato_venta.existe_abono():
                        form = AbonoPagoEntidadContratoVentaForm(initial={'valor': pago_entidad_contrato_venta.valor_desembolsado})
                    else:
                        form = AbonoPagoEntidadContratoVentaForm()
                if pago_entidad_contrato_venta.permite_modificacion():
                    render = render_to_string('ajax/ventas/nuevoabonopagoentidadcontratoventa.html', {'user': user, 'form': form, 'pago_entidad_contrato_venta': pago_entidad_contrato_venta, 'fecha_actual': datetime.today()}, context_instance=RequestContext(request))
                    dajax.assign('#light', 'innerHTML', render)
                    dajax.script("document.getElementById('light').style.display='block';")
                    dajax.script("document.getElementById('fade').style.display='block';")
                else:
                    dajax.redirect('/inverboy/home/')
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_abono_entidad_contrato_venta2(request, pago_entidad_contrato_venta_id, contrato_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if request.is_ajax():
            if 'inverboy.add_contratoventa' in user.get_all_permissions():
                usuario = Usuario.objects.get(id=user.id)
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                pago_entidad_contrato_venta = contrato_venta.pagoentidadcontratoventa_set.get(id=pago_entidad_contrato_venta_id)
                if not pago_entidad_contrato_venta.verificado:
                    pago_entidad_contrato_venta.fecha_registro_desembolso = None
                    pago_entidad_contrato_venta.valor_desembolsado = 0
                    pago_entidad_contrato_venta.usuario_registro_desembolso = None
                    pago_entidad_contrato_venta.save()
                    dajax.alert('Pago eliminado correctamente')
                    dajax.redirect('/inverboy/home/detallescontratoventa/' + str(contrato_venta_id) + '/' + str(proyecto_id) + '/')
                else:
                    dajax.redirect('/inverboy/home/')
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def validar_abono_entidad_contrato_venta2(request, pago_entidad_contrato_venta_id, contrato_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if request.is_ajax():
            if 'inverboy.validate_paymentcontratoventa' in user.get_all_permissions():
                usuario = Usuario.objects.get(id=user.id)
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                pago_entidad_contrato_venta = contrato_venta.pagoentidadcontratoventa_set.get(id=pago_entidad_contrato_venta_id)
                if pago_entidad_contrato_venta.existe_abono():
                    pago_entidad_contrato_venta.verificado = True
                    pago_entidad_contrato_venta.save()
                    dajax.alert('Pago validado correctamente')
                    dajax.redirect('/inverboy/home/detallescontratoventa/' + str(contrato_venta_id) + '/' + str(proyecto_id) + '/')
                else:
                    dajax.redirect('/inverboy/home/')
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def registrar_abono_efectivo_contrato_venta2(request, contrato_venta_id, proyecto_id, datos):
    from datetime import datetime
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if request.is_ajax():
            if 'inverboy.add_contratoventa' in user.get_all_permissions():
                usuario = Usuario.objects.get(id=user.id)
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                if datos:
                    request.POST = deserialize_form(datos)
                    form = AbonoPagoEfectivoContratoVentaForm(data=request.POST)
                    if form.is_valid():
                        valor_abono_efectivo_contrato_venta = form.cleaned_data['valor']
                        error_pago_efectivo_cuota_inicial = ''
                        if len(contrato_venta.abonopagoefectivocontratoventa_set.all()) == 0:
                            pago_efectivo_cuota_inicial = contrato_venta.pagoefectivocontratoventa_set.all().order_by('fecha_desembolso', 'id')[0]
                            if valor_abono_efectivo_contrato_venta < pago_efectivo_cuota_inicial.valor:
                                error_pago_efectivo_cuota_inicial = 'El pago de la cuota inicial no debe ser menor al valor pactado.'
                        if not error_pago_efectivo_cuota_inicial:
                            abono_pago_efectivo_contrato_venta = AbonoPagoEfectivoContratoVenta()
                            abono_pago_efectivo_contrato_venta.fecha_consignacion = form.cleaned_data['fecha_consignacion']
                            abono_pago_efectivo_contrato_venta.numero_consignacion = form.cleaned_data['numero_consignacion']
                            abono_pago_efectivo_contrato_venta.valor = form.cleaned_data['valor']
                            abono_pago_efectivo_contrato_venta.entidad_bancaria = EntidadBancaria.objects.get(pk=request.POST['entidad_bancaria'])
                            if 'cuenta' in request.POST:
                                abono_pago_efectivo_contrato_venta.cuenta = NumeroCuenta.objects.get(pk=request.POST['cuenta'])
                            abono_pago_efectivo_contrato_venta.contrato_venta = contrato_venta
                            abono_pago_efectivo_contrato_venta.usuario_registro = usuario

                            abono_pago_efectivo_contrato_venta.save()
                            # Si el cliente cancela la cuota inicial (primer cuota) se actualiza el estado del contrato a (2-Separado)
                            if contrato_venta.estado_contrato_venta().estado_contrato == 1 and len(contrato_venta.abonopagoefectivocontratoventa_set.all()) == 1:
                                estado_contrato_venta = contrato_venta.estado_contrato_venta()
                                estado_contrato_venta.estado_registro = False
                                estado_contrato_venta.save()
                                estado_contrato_venta, registro_creado = contrato_venta.estadocontratoventa_set.get_or_create(estado_contrato=2)
                                if not registro_creado:
                                    estado_contrato_venta.estado_registro = True
                                    estado_contrato_venta.save()
                            dajax.alert('Nuevo pago registrado correctamente')
                            dajax.redirect('/inverboy/home/detallescontratoventa/' + str(contrato_venta_id) + '/' + str(proyecto_id) + '/')
                        else:
                            dajax.alert('El pago inicial debe ser mayor o igual al valor de la primera cuota.')
                            form._errors["valor"] = ErrorList([error_pago_efectivo_cuota_inicial])
                else:
                    form = AbonoPagoEfectivoContratoVentaForm()
                render = render_to_string('ajax/ventas/nuevoabonopagoefectivocontratoventa.html', {'user': user, 'form': form, 'fecha_actual': datetime.today()}, context_instance=RequestContext(request))
                # dajax.assign('#light', 'innerHTML', render)
                # dajax.script("document.getElementById('light').style.display='block';")
                # dajax.script("document.getElementById('fade').style.display='block';")
                # dajax.script("Calendar.setup({inputField:'id_fecha_consignacion',ifFormat:'%Y-%m-%d',button:'lanzador_fecha_consignacion'});")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def eliminar_abono_efectivo_contrato_venta2(request, abono_pago_efectivo_contrato_venta_id, contrato_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if request.is_ajax():
            if 'inverboy.add_contratoventa' in user.get_all_permissions():
                usuario = Usuario.objects.get(id=user.id)
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                abono_pago_efectivo_contrato_venta = contrato_venta.abonopagoefectivocontratoventa_set.get(id=abono_pago_efectivo_contrato_venta_id)
                if not abono_pago_efectivo_contrato_venta.verificado:
                    abono_pago_efectivo_contrato_venta.delete()
                    # Si el cliente cancela la cuota inicial (primer cuota) se actualiza el estado del contrato a (2-Separado)
                    if contrato_venta.estado_contrato_venta().estado_contrato == 2 and len(contrato_venta.abonopagoefectivocontratoventa_set.all()) == 0:
                        estado_contrato_venta = contrato_venta.estado_contrato_venta()
                        estado_contrato_venta.estado_registro = False
                        estado_contrato_venta.save()
                        estado_contrato_venta, registro_creado = contrato_venta.estadocontratoventa_set.get_or_create(estado_contrato=1)
                        if not registro_creado:
                            estado_contrato_venta.estado_registro = True
                            estado_contrato_venta.save()
                    dajax.alert('Pago eliminado correctamente')
                    dajax.redirect('/inverboy/home/detallescontratoventa/' + str(contrato_venta_id) + '/' + str(proyecto_id) + '/')
                else:
                    dajax.redirect('/inverboy/home/')
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def validar_abono_efectivo_contrato_venta2(request, abono_pago_efectivo_contrato_venta_id, contrato_venta_id, proyecto_id, datos):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if request.is_ajax():
            if 'inverboy.validate_paymentcontratoventa' in user.get_all_permissions():
                usuario = Usuario.objects.get(id=user.id)
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                abono_pago_efectivo_contrato_venta = contrato_venta.abonopagoefectivocontratoventa_set.get(id=abono_pago_efectivo_contrato_venta_id)
                if not abono_pago_efectivo_contrato_venta.verificado:
                    abono_pago_efectivo_contrato_venta.verificado = True
                    abono_pago_efectivo_contrato_venta.save()
                    dajax.alert('Pago validado correctamente')
                    dajax.redirect('/inverboy/home/detallescontratoventa/' + str(contrato_venta_id) + '/' + str(proyecto_id) + '/')
                else:
                    dajax.redirect('/inverboy/home/')
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def asignar_numero_cuenta_fiducia_contrato_venta2(request, contrato_venta_id, proyecto_id, numero_fiducuenta):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if request.is_ajax():
            if 'inverboy.add_contratoventa' in user.get_all_permissions():
                usuario = Usuario.objects.get(id=user.id)
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                error_numero_fiducuenta = ''
                if numero_fiducuenta:
                    numero_fiducuenta = numero_fiducuenta.strip()
                    validaciones = Validator().append([
                        Field('numero_fiducuenta', numero_fiducuenta).append([
                            IsRequired('Este campo es obligatorio.'), Regex("^[ A-Za-z0-9_-]{1,40}$", error='Este campo no cumple con el formato requerido.'),
                        ]),
                    ]).run(True).pop()

                    if validaciones['passed'] == True:
                        contrato_venta.numero_cuenta_fiducia = numero_fiducuenta
                        contrato_venta.save()
                        dajax.redirect('/inverboy/home/detallescontratoventa/' + str(contrato_venta_id) + '/' + str(proyecto_id) +  '/')
                    else:
                        for error in validaciones['errors']:
                            error_numero_fiducuenta = error
                        dajax.script("document.getElementById('id_numero_cuenta_fiducia').readOnly=false;")
                        dajax.script("document.getElementById('id_numero_cuenta_fiducia').select();")
                else:
                    if contrato_venta.numero_cuenta_fiducia:
                        dajax.script("$('#id_numero_cuenta_fiducia').val('" + contrato_venta.numero_cuenta_fiducia + "');")
                    dajax.script("document.getElementById('id_numero_cuenta_fiducia').readOnly=false;")
                    dajax.script("document.getElementById('id_numero_cuenta_fiducia').select();")
                    dajax.script("document.getElementById('id_btn_modificar_numero_fiducuenta').style.display='none';")
                    dajax.script("document.getElementById('id_btn_asignar_numero_fiducuenta').style.display='block';")
                dajax.script("$('#id_error_numero_cuenta_fiducia').html('" + error_numero_fiducuenta + "');")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def asignar_fecha_escritura_contrato_venta2(request, contrato_venta_id, proyecto_id, fecha_escritura):
    from datetime import date
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if request.is_ajax():
            if 'inverboy.add_contratoventa' in user.get_all_permissions():
                usuario = Usuario.objects.get(id=user.id)
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                error_fecha_escritura = ''
                if fecha_escritura:
                    fecha_escritura = fecha_escritura.strip()
                    validaciones = Validator().append([
                        Field('fecha_escritura', fecha_escritura).append([
                            IsRequired('Este campo es obligatorio.'), Regex("^\d{4}\-\d{1,2}\-\d{1,2}$", error='Este campo no cumple con el formato requerido.'),
                        ]),
                    ]).run(True).pop()

                    if validaciones['passed'] == True:
                        partes_fecha_escritura = fecha_escritura.split('-')
                        str_fecha_escritura = date(int(partes_fecha_escritura[0]), int(partes_fecha_escritura[1]), int(partes_fecha_escritura[2]))
                        fecha_actual = date.today()
                        if str_fecha_escritura >= fecha_actual:
                            inmueble_principal = contrato_venta.agrupacion_contrato_venta().inmueble_principal.inmueble
                            inmueble_principal.fecha_escritura = fecha_escritura
                            inmueble_principal.save()
                            dajax.redirect('/inverboy/home/detallescontratoventa/' + str(contrato_venta_id) + '/' + str(proyecto_id) +  '/')
                        else:
                            error_fecha_escritura = 'La fecha no debe ser menor a la fecha actual.'
                    else:
                        for error in validaciones['errors']:
                            error_fecha_escritura = error
                        dajax.script("document.getElementById('id_fecha_escritura').readOnly=false;")
                        dajax.script("document.getElementById('id_fecha_escritura').select();")
                else:
                    inmueble_principal = contrato_venta.agrupacion_contrato_venta().inmueble_principal.inmueble
                    if inmueble_principal.fecha_escritura:
                        dajax.script("$('#id_fecha_escritura').val('" + inmueble_principal.fecha_escritura.strftime('%Y-%m-%d') + "');")
                    dajax.script("document.getElementById('id_fecha_escritura').readOnly=false;")
                    dajax.script("document.getElementById('id_fecha_escritura').select();")
                    dajax.script("document.getElementById('id_btn_modificar_fecha_escritura').style.display='none';")
                    dajax.script("document.getElementById('id_btn_asignar_fecha_escritura').style.display='block';")
                    dajax.script("document.getElementById('lanzador_fecha_escritura').style.display='block';")
                    dajax.script("Calendar.setup({inputField:'id_fecha_escritura',ifFormat:'%Y-%m-%d',button:'lanzador_fecha_escritura'});")
                dajax.script("$('#id_error_fecha_escritura').html('" + error_fecha_escritura + "');")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

#referencia inmueble
def asignar_referencia_inmueble_contrato_venta2(request, contrato_venta_id, proyecto_id, referencia_inmueble):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if request.is_ajax():
            if 'inverboy.add_contratoventa' in user.get_all_permissions():
                usuario = Usuario.objects.get(id=user.id)
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                error_referencia_inmueble = ''
                if referencia_inmueble:
                    referencia_inmueble = referencia_inmueble.strip()
                    validaciones = Validator().append([
                        Field('referencia_inmueble', referencia_inmueble).append([
                            IsRequired('Este campo es obligatorio.'), Regex("^[ A-Za-z0-9_-]{1,40}$", error='Este campo no cumple con el formato requerido.'),
                        ]),
                    ]).run(True).pop()

                    if validaciones['passed'] == True:
                        contrato_venta.referencia_inmueble = referencia_inmueble
                        contrato_venta.save()
                        dajax.redirect('/inverboy/home/detallescontratoventa/' + str(contrato_venta_id) + '/' + str(proyecto_id) +  '/')
                    else:
                        for error in validaciones['errors']:
                            error_referencia_inmueble = error
                        dajax.script("document.getElementById('id_referencia_inmueble').readOnly=false;")
                        dajax.script("document.getElementById('id_referencia_inmueble').select();")
                else:
                    if contrato_venta.referencia_inmueble:
                        dajax.script("$('#id_referencia_inmueble').val('" + contrato_venta.referencia_inmueble + "');")
                    dajax.script("document.getElementById('id_referencia_inmueble').readOnly=false;")
                    dajax.script("document.getElementById('id_referencia_inmueble').select();")
                    dajax.script("document.getElementById('id_btn_modificar_referencia_inmueble').style.display='none';")
                    dajax.script("document.getElementById('id_btn_asignar_referencia_inmueble').style.display='block';")
                dajax.script("$('#id_error_referencia_inmueble').html('" + error_referencia_inmueble + "');")
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()