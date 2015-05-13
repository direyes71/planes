# -*- encoding: utf-8 -*-
__author__ = 'Diego Reyes'

from django.template.loader import render_to_string

from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse, render

from inverboy.models import Usuario, Departamento, Municipio, Proyecto, Cliente, ContactoCliente

from inverboy.forms import ClienteForm, ContactoClienteForm, DocumentoVentaForm

from funciones_views import *

# PAGINACION
from inverboy.paginator import *


from django.template import RequestContext

from django.utils import simplejson
from settings import TIEMPO_INACTIVIDAD
from django.utils.encoding import codecs

#Busqueda documentos ventas
def busqueda_documentos_ventas(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_documentoventa' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
                return render_to_response('ventas/busquedadocumentosventas.html', {'user': user, 'proyecto': proyecto})
    return HttpResponseRedirect('/inverboy/home/')


#Detalles documento ventas
def detalles_documento_ventas(request, documento, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_documentoventa' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
                texto = ''
                if documento == 'aperturafiducuenta':
                    if proyecto.apertura_fiducuenta:
                        texto = proyecto.str_apertura_fiducuenta()
                if documento == 'cartainstrucciones':
                    if proyecto.carta_instrucciones:
                        texto = proyecto.str_carta_instrucciones()
                if documento == 'promesacompraventa':
                    if proyecto.promesa_compraventa:
                        texto = proyecto.str_promesa_compraventa()
                return render_to_response('ventas/detallesdocumentoventa.html', {'user': user, 'texto': texto, 'documento': documento, 'proyecto': proyecto})
    return HttpResponseRedirect('/inverboy/home/')


#Registrar documento venta apertura fiducuenta
def registrar_documento_venta_apertura_fiducuenta(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_documentoventa' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
                if request.method == 'POST':
                    form = DocumentoVentaForm(request.POST)
                    if form.is_valid():
                        texto = form.cleaned_data['texto'].strip()
                        if texto != '':
                            proyecto.apertura_fiducuenta = texto
                        else:
                            proyecto.apertura_fiducuenta = None
                        proyecto.save()
                        return HttpResponseRedirect('/inverboy/home/detallesdocumentoventas/aperturafiducuenta/' + str(proyecto_id) + '/')
                else:
                    form = DocumentoVentaForm()
                    if proyecto.apertura_fiducuenta:
                        form.initial = {'texto': proyecto.apertura_fiducuenta}
                return render_to_response('ventas/registrardocumentoventa.html', {'user': user, 'form': form, 'titulo': 'Registrar apertura fiducuenta', 'proyecto': proyecto})
    return HttpResponseRedirect('/inverboy/home/')


#Registrar documento venta carta instrucciones
def registrar_documento_venta_carta_instrucciones(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_documentoventa' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
                if request.method == 'POST':
                    form = DocumentoVentaForm(request.POST)
                    if form.is_valid():
                        texto = form.cleaned_data['texto'].strip()
                        if texto != '':
                            proyecto.carta_instrucciones = texto
                        else:
                            proyecto.carta_instrucciones = None
                        proyecto.save()
                        return HttpResponseRedirect('/inverboy/home/detallesdocumentoventas/cartainstrucciones/' + str(proyecto_id) + '/')
                else:
                    form = DocumentoVentaForm()
                    if proyecto.carta_instrucciones:
                        form.initial = {'texto': proyecto.carta_instrucciones}
                return render_to_response('ventas/registrardocumentoventa.html', {'user': user, 'form': form, 'titulo': 'Registrar carta instrucciones', 'proyecto': proyecto})
    return HttpResponseRedirect('/inverboy/home/')


#Registrar documento venta promesa compraventa
def registrar_documento_venta_promesa_compraventa(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_documentoventa' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
                if request.method == 'POST':
                    form = DocumentoVentaForm(request.POST)
                    if form.is_valid():
                        texto = unicode(form.cleaned_data['texto'].strip())
                        if texto != '':
                            proyecto.promesa_compraventa = texto
                        else:
                            proyecto.promesa_compraventa = None
                        proyecto.save()
                        return HttpResponseRedirect('/inverboy/home/detallesdocumentoventas/promesacompraventa/' + str(proyecto_id) + '/')
                else:
                    form = DocumentoVentaForm()
                    if proyecto.promesa_compraventa:
                        form.initial = {'texto': proyecto.promesa_compraventa}
                return render_to_response('ventas/registrardocumentoventa.html', {'user': user, 'form': form, 'titulo': 'Registrar promesa compraventa', 'proyecto': proyecto})
    return HttpResponseRedirect('/inverboy/home/')

import os
import math
def imprimir_cotizacion_ventas(request,contrato_venta_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        usuario = Usuario.objects.get(pk=user.pk)
        contrato_venta = ContratoVenta.objects.get(pk=int(contrato_venta_id))
        fecha_reserva = EstadoContratoVenta.objects.get(contrato_venta=contrato_venta,estado_contrato=1).fecha_registro
        pagesize = 'letter'
        orientation= 'portrait'
        margin= '1cm'
        font_size= '11pt'
        contrato_venta.calcular_valores()
        datos_pagos = []
        cont = 0
        for cuota in contrato_venta.consolidado_pagos_efectivo():
            datos_pagos.append([cuota.fecha_desembolso,cuota.valor,'cuota',cont])
            cont+=1
        if datos_pagos:
            datos_pagos[0][2]=u'Separación'
        
        for pago_entidad in contrato_venta.pagoentidadcontratoventa_set.all():
            datos_pagos.append([pago_entidad.fecha_desembolso,pago_entidad.valor,pago_entidad.str_tipo_cuenta(),cont])
            cont+=1
        if contrato_venta.forma_pago == 1:
            datos_pagos.append(['',contrato_venta.monto_credito,'credito',cont])
        mitad = int(math.floor(len(datos_pagos)/2))
        datos_pagos_1 = datos_pagos[:mitad]
        datos_pagos_2 = datos_pagos[mitad:]
        imagen_fondo = os.path.dirname(os.path.realpath(__file__))+'/../../templates/ventas/pdfs/LOGO_IBL.png'
        html = render_to_string('ventas/pdfs/pdfcotizacionventa.html', locals(), context_instance=RequestContext(request))
        return generar_pdf(html, contrato_venta_id)
    return HttpResponseRedirect('/inverboy/home/')

def cuentas_por_banco(request):
    if request.is_ajax() and request.method == 'POST':
        cuentas = EntidadBancaria.objects.get(pk=request.POST['entidad_bancaria']).cuentas_asociadas()
        resultado = []
        for c in cuentas:
            resultado.append({'numero':c.numero,'id':c.pk})
        return HttpResponse(simplejson.dumps(resultado), mimetype='application/json;charset=utf-8')
    return HttpResponse()

def lista_entidades_bancarias(request):
    if request.is_ajax() and request.method == 'POST':
        entidades_bancarias = EntidadBancaria.objects.filter(estado_registro=True)
        resultado = []
        for e in entidades_bancarias:
            resultado.append({'nombre':e.nombre,'id':e.pk})
        return HttpResponse(simplejson.dumps(resultado), mimetype='application/json;charset=utf-8')
    return HttpResponse()

#Nueva entidad bancaria
def nueva_entidad_bancaria(request):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_entidadbancaria' in user.get_all_permissions():
            if request.method=='POST' and request.POST['nombre']:
                nueva_entidad = EntidadBancaria(nombre=request.POST['nombre'])
                try:
                    nueva_entidad.save()
                    cant = int(request.POST['cuentas'])
                    p = request.POST
                    for x in xrange(0,cant):
                        aux_cuenta = NumeroCuenta(entidad_bancaria=nueva_entidad,numero=p['nombre_%d' % x],descripcion=p['descripcion_%d' % x])
                        aux_cuenta.save()
                except Exception,e:
                    print e
                return HttpResponseRedirect('/inverboy/home/busquedaentidadesbancarias/')
            return render_to_response('ventas/nuevaentidadbancaria.html', locals())
    return HttpResponseRedirect('/inverboy/home/')


#Busqueda entidades bancarias
def busqueda_entidades_bancarias(request):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_entidadbancaria' in user.get_all_permissions():
            entidades_bancarias = EntidadBancaria.objects.all()
            criterio = ''
            if request.method == 'POST':
                criterio = request.POST['criterio'].strip()
                if criterio != '' :
                    entidades_bancarias = entidades_bancarias.filter(Q(nombre__icontains=criterio))
            return render_to_response('ventas/busquedaentidadesbancarias.html', locals())
    return HttpResponseRedirect('/inverboy/home/')


#Modificar entidad bancaria
def modificar_entidad_bancaria(request, entidad_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_entidadbancaria' in user.get_all_permissions():
            entidad_bancaria = EntidadBancaria.objects.get(id=entidad_id)
            #form = EntidadBancariaForm(initial={'nombre': entidad_bancaria.nombre, 'estado_registro': entidad_bancaria.estado_registro})
            form = EntidadBancariaForm(instance=entidad_bancaria)
            if request.method == 'POST':
                nueva_entidad = EntidadBancaria.objects.get(pk=request.POST['entidad_a_modificar'])
                nueva_entidad.nombre = request.POST['nombre']
                if 'activo' in request.POST:
                    nueva_entidad.estado_registro = True
                else:
                    nueva_entidad.estado_registro = False
                try:
                    nueva_entidad.save()
                    cant = int(request.POST['cuentas'])
                    p = request.POST
                    for x in xrange(0,cant):
                        if ('nombre_%d' % x) in p:
                            if ("cuenta_%d" % x) in p:
                                aux_cuenta = NumeroCuenta.objects.get(pk=int(p["cuenta_%d" % x]))
                                aux_cuenta.numero = p['nombre_%d' % x]
                                aux_cuenta.descripcion = p['descripcion_%d' % x]
                            else:
                                aux_cuenta = NumeroCuenta(entidad_bancaria=nueva_entidad,numero=p['nombre_%d' % x],descripcion=p['descripcion_%d' % x])
                            aux_cuenta.save()
                    eliminadas = p['eliminadas'].split(",")
                    for e in eliminadas:
                        a_eliminar = NumeroCuenta.objects.get(pk=int(e))
                        a_eliminar.delete()
                except Exception,e:
                    print e
                return HttpResponseRedirect('/inverboy/home/busquedaentidadesbancarias/')
            modificar = True
            return render_to_response('ventas/nuevaentidadbancaria.html', locals())
    return HttpResponseRedirect('/inverboy/home/')


#Nuevo tipo de adicional proyecto
def nuevo_tipo_adicional_agrupacion(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_adicionalagrupacion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                # Inicialización de formularios
                form = TipoAdicionalAgrupacionForm()
                if request.method == 'POST':
                    form = TipoAdicionalAgrupacionForm(request.POST)
                    if form.is_valid():
                        nombre = form.cleaned_data['nombre']
                        validar_nombre, form = validate_unique_field(AdicionalAgrupacion, {'nombre': nombre, 'proyecto': proyecto}, fields_error={'nombre': nombre}, form=form)
                        if validar_nombre == False:
                            tipo_adicional = AdicionalAgrupacion()
                            tipo_adicional.nombre = form.cleaned_data['nombre']
                            tipo_adicional.proyecto = proyecto
                            tipo_adicional.save()
                                                        
                            # Registro de la actividad del usuario
                            direccion_ip = request.META['REMOTE_ADDR']
                            registro_historial(direccion_ip, usuario, "Registro nuevo tipo adicional, nombre: " + unicode(tipo_adicional.nombre) + ", proyecto: " + unicode(proyecto.nombre))
                            return HttpResponseRedirect('/inverboy/home/busquedatipoadicionales/' + str(proyecto_id) + '/')
                return render_to_response('ventas/nuevotipoadicional.html',{'user': user, 'form': form, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Busqueda tipos adicional proyecto
def busqueda_tipos_adicional(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_adicionalagrupacion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                tipos_adicional = proyecto.lista_tipos_adicionales_agrupaciones_inmueble(criterio=criterio)
                pag = Paginador(request, tipos_adicional, 20, 1)
                return render_to_response('ventas/reportetiposadicional.html', {'user': user, 'tipos_adicional': pag, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar tipo adicional
def modificar_tipo_adicional(request, tipo_adicional_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_adicionalagrupacion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                tipo_adicional = proyecto.adicionalagrupacion_set.get(id=tipo_adicional_id)
                form = TipoAdicionalAgrupacionForm(initial={'nombre': tipo_adicional.nombre})
                if request.method == 'POST':
                    form = TipoAdicionalAgrupacionForm(request.POST)
                    if form.is_valid():
                        nombre = form.cleaned_data['nombre']
                        validar_nombre, form = validate_unique_field(AdicionalAgrupacion, {'nombre': nombre, 'proyecto': proyecto}, fields_error={'nombre': nombre}, exclude_initials_values={'nombre': tipo_adicional.nombre, 'proyecto': proyecto}, form=form)
                        if validar_nombre == False:
                            tipo_adicional.nombre = form.cleaned_data['nombre'].strip()
                            tipo_adicional.save()

                            # Registro de la actividad del usuario
                            direccion_ip = request.META['REMOTE_ADDR']
                            registro_historial(direccion_ip, usuario, "Modifico tipo adicional, nombre: " + unicode(tipo_adicional.nombre) + ", proyecto: " + unicode(proyecto.nombre))
                            return HttpResponseRedirect('/inverboy/home/busquedatipoadicionales/' + str(proyecto_id) + '/')
                return render_to_response('ventas/nuevotipoadicional.html', {'user': user, 'form': form, 'proyecto': proyecto, 'change': True})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Nuevo adicional proyecto
def nuevo_adicional_agrupacion(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_adicionalagrupacion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                # Inicialización de formularios
                form = AdicionalAgrupacionForm(proyecto.id)
                if request.method == 'POST':
                    form = AdicionalAgrupacionForm(proyecto.id, request.POST)
                    if form.is_valid():
                        nombre = form.cleaned_data['nombre']
                        tipo_adicional = None
                        try:
                            tipo_adicional = form.cleaned_data['tipo_adicional']
                        except :
                            pass
                        if tipo_adicional == None:
                            validar_nombre, form = validate_unique_field(AdicionalAgrupacion, {'nombre': nombre, 'proyecto': proyecto}, fields_error={'nombre': nombre}, form=form)
                        else:
                            validar_nombre, form = validate_unique_field(AdicionalAgrupacion, {'nombre': nombre, 'tipo_adicional': tipo_adicional}, fields_error={'nombre': nombre}, form=form)
                        if validar_nombre == False:
                            adicional = AdicionalAgrupacion()
                            adicional.nombre = form.cleaned_data['nombre']
                            adicional.descripcion = form.cleaned_data['descripcion']
                            adicional.valor = form.cleaned_data['valor']
                            adicional.item_adicional = True
                            if tipo_adicional == None:
                                adicional.proyecto = proyecto
                            else:
                                adicional.tipo_adicional = tipo_adicional
                            adicional.save()

                            # Registro de la actividad del usuario
                            direccion_ip = request.META['REMOTE_ADDR']
                            registro_historial(direccion_ip, usuario, "Registro nuevo adicional, nombre: " + unicode(adicional.nombre) + ", proyecto: " + unicode(proyecto.nombre))
                            return HttpResponseRedirect('/inverboy/home/busquedaadicionales/' + str(proyecto_id) + '/')
                return render_to_response('ventas/nuevoadicional.html',{'user': user, 'form': form, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Busqueda adicionales proyecto
def busqueda_adicionales(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_adicionalagrupacion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                tipo_adicional = ''
                criterio = ''
                if request.method == 'POST':
                    tipo_adicional = request.POST['tipo_adicional']
                    criterio = request.POST['criterio'].strip()
                if tipo_adicional != '':
                    tipo_adicional = proyecto.lista_tipos_adicionales_agrupaciones_inmueble().get(id=tipo_adicional)
                else:
                    tipo_adicional = None
                adicionales = proyecto.lista_adicionales_agrupaciones_inmueble(tipo_adicional=tipo_adicional, criterio=criterio)
                pag = Paginador(request, adicionales, 20, 1)
                tipos_adicional = proyecto.lista_tipos_adicionales_agrupaciones_inmueble()
                return render_to_response('ventas/reporteadicionales.html', {'user': user, 'adicionales': pag, 'tipos_adicional': tipos_adicional, 'tipo_adicional_actual': tipo_adicional, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar adicional
def modificar_adicional_agrupacion(request, adicional_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_adicionalagrupacion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                adicional = AdicionalAgrupacion.objects.get(item_adicional=True, id=adicional_id)
                # Inicialización de formularios
                form = AdicionalAgrupacionForm(proyecto.id, instance=adicional)
                if request.method == 'POST':
                    form = AdicionalAgrupacionForm(proyecto.id, request.POST, instance=adicional)
                    if form.is_valid():
                        nombre = form.cleaned_data['nombre']
                        tipo_adicional = None
                        try:
                            tipo_adicional = form.cleaned_data['tipo_adicional']
                        except :
                            pass
                        if tipo_adicional == None:
                            validar_nombre, form = validate_unique_field(AdicionalAgrupacion, {'nombre': nombre, 'proyecto': proyecto}, fields_error={'nombre': nombre}, exclude_initials_values={'nombre': adicional.nombre, 'proyecto': proyecto}, form=form)
                        else:
                            validar_nombre, form = validate_unique_field(AdicionalAgrupacion, {'nombre': nombre, 'tipo_adicional': tipo_adicional}, fields_error={'nombre': nombre}, exclude_initials_values={'nombre': adicional.nombre, 'tipo_adicional': adicional.tipo_adicional}, form=form)
                        if validar_nombre == False:
                            adicional.nombre = form.cleaned_data['nombre']
                            adicional.descripcion = form.cleaned_data['descripcion']
                            adicional.valor = form.cleaned_data['valor']
                            adicional.item_adicional = True
                            if tipo_adicional == None:
                                adicional.proyecto = proyecto
                                adicional.tipo_adicional = None
                            else:
                                adicional.tipo_adicional = tipo_adicional
                                adicional.proyecto = None
                            adicional.save()

                            # Registro de la actividad del usuario
                            direccion_ip = request.META['REMOTE_ADDR']
                            registro_historial(direccion_ip, usuario, "Modifico adicional, nombre: " + unicode(adicional.nombre) + ", proyecto: " + unicode(proyecto.nombre))
                            return HttpResponseRedirect('/inverboy/home/busquedaadicionales/' + str(proyecto_id) + '/')
                return render_to_response('ventas/nuevoadicional.html',{'user': user, 'form': form, 'proyecto': proyecto, 'change': True})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Nuevo cliente
def nuevo_cliente(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_cliente' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                # Inicialización de formularios
                form1 = ClienteForm()
                form2 = ContactoClienteForm()
                contactos = []
                if request.method == 'POST':
                    contactos = None
                    try:
                        contactos = request.session['contactos_cliente']
                    except :
                        pass
                    if contactos != None:
                        form1 = ClienteForm(request.POST)
                        if form1.is_valid():
                            identificacion = form1.cleaned_data['identificacion']
                            validar_identificacion, form1 = validate_unique_field(Cliente, {'identificacion': identificacion}, fields_error={'identificacion': identificacion}, form=form1)
                            if validar_identificacion == False:
                                cliente = Cliente()
                                cliente.tipo_identificacion = form1.cleaned_data['tipo_identificacion']
                                cliente.identificacion = form1.cleaned_data['identificacion']
                                cliente.nombre_1 = form1.cleaned_data['nombre_1'].strip().upper()
                                cliente.nombre_2 = form1.cleaned_data['nombre_2'].strip().upper()
                                cliente.apellido_1 = form1.cleaned_data['apellido_1'].strip().upper()
                                cliente.apellido_2 = form1.cleaned_data['apellido_2'].strip().upper()
                                cliente.municipio_documento = form1.cleaned_data['municipio_documento']
                                cliente.estado_civil = form1.cleaned_data['estado_civil']
                                cliente.municipio_residencia = form1.cleaned_data['municipio_residencia']
                                cliente.direccion_residencia = form1.cleaned_data['direccion_residencia'].strip()
                                cliente.telefono_1 = form1.cleaned_data['telefono_1']
                                cliente.telefono_2 = form1.cleaned_data['telefono_2']
                                cliente.email = form1.cleaned_data['email']
                                cliente.empresa = form1.cleaned_data['empresa'].strip()
                                cliente.telefono_empresa = form1.cleaned_data['telefono_empresa']
                                cliente.direccion_empresa = form1.cleaned_data['direccion_empresa'].strip()
                                cliente.ingresos_mensuales = form1.cleaned_data['ingresos_mensuales'].strip()
                                cliente.observaciones = form1.cleaned_data['observaciones'].strip()
                                cliente.estado = form1.cleaned_data['estado']

                                # Datos del usuario que registro
                                cliente.usuario_registro = usuario

                                cliente.save()

                                # Registro de los contactos del cliente
                                for contacto in contactos:
                                    contacto.cliente = cliente
                                    contacto.save()

                                # Elimina las variables de sesion
                                del request.session['contactos_cliente']
                                direccion_ip = request.META['REMOTE_ADDR']
                                registro_historial(direccion_ip, usuario, "Registro nuevo cliente, identificacion: "+ str(cliente.identificacion))
                                return HttpResponseRedirect('/inverboy/home/nuevoprospectoventa/' + str(cliente.id) + '/' + str(proyecto_id) + '/')
                    else:
                        return HttpResponseRedirect('/inverboy/home/')
                else:
                    request.session['contactos_cliente'] = contactos
                return render_to_response('ventas/nuevocliente.html',{'user': user, 'form1': form1, 'form2': form2, 'contactos': contactos, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Busqueda clientes
def busqueda_clientes(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_cliente' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                clientes = Cliente.objects.all()
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                    try:
                        criterio = int(criterio)
                        clientes = clientes.filter(identificacion=criterio)
                    except:
                        clientes = clientes.filter(Q(nombre_1__icontains=criterio) | Q(nombre_2__icontains=criterio) | Q(apellido_1__icontains=criterio) | Q(apellido_2__icontains=criterio))
                pag = Paginador(request, clientes, 20, 1)
                return render_to_response('ventas/reporteclientes.html', {'user': user, 'clientes': pag, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar cliente
def modificar_cliente(request, cliente_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_cliente' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                cliente = Cliente.objects.get(id=cliente_id)
                form1 = ClienteForm(initial={'tipo_identificacion': cliente.tipo_identificacion, 'identificacion': cliente.identificacion, 'nombre_1': cliente.nombre_1, 'nombre_2': cliente.nombre_2, 'apellido_1': cliente.apellido_1, 'apellido_2': cliente.apellido_2, 'departamento_documento': cliente.municipio_documento.departamento, 'municipio_documento': cliente.municipio_documento, 'estado_civil': cliente.estado_civil, 'departamento_residencia': cliente.municipio_residencia.departamento, 'municipio_residencia': cliente.municipio_residencia, 'direccion_residencia': cliente.direccion_residencia, 'telefono_1': cliente.telefono_1, 'telefono_2': cliente.telefono_2, 'email': cliente.email, 'empresa': cliente.empresa, 'telefono_empresa': cliente.telefono_empresa, 'direccion_empresa': cliente.direccion_empresa, 'ingresos_mensuales': cliente.ingresos_mensuales, 'observaciones': cliente.observaciones, 'estado': cliente.estado})
                form2 = ContactoForm()
                if request.method == 'POST':
                    contactos = None
                    try:
                        contactos = request.session['contactos_cliente']
                    except :
                        pass
                    if contactos != None:
                        form1 = ClienteForm(request.POST)
                        if form1.is_valid():
                            cliente.tipo_identificacion = form1.cleaned_data['tipo_identificacion']
                            cliente.nombre_1 = form1.cleaned_data['nombre_1'].strip().upper()
                            cliente.nombre_2 = form1.cleaned_data['nombre_2'].strip().upper()
                            cliente.apellido_1 = form1.cleaned_data['apellido_1'].strip().upper()
                            cliente.apellido_2 = form1.cleaned_data['apellido_2'].strip().upper()
                            cliente.municipio_documento = form1.cleaned_data['municipio_documento']
                            cliente.estado_civil = form1.cleaned_data['estado_civil']
                            cliente.municipio_residencia = form1.cleaned_data['municipio_residencia']
                            cliente.direccion_residencia = form1.cleaned_data['direccion_residencia'].strip()
                            cliente.telefono_1 = form1.cleaned_data['telefono_1']
                            cliente.telefono_2 = form1.cleaned_data['telefono_2']
                            cliente.email = form1.cleaned_data['email']
                            cliente.empresa = form1.cleaned_data['empresa'].strip()
                            cliente.telefono_empresa = form1.cleaned_data['telefono_empresa']
                            cliente.direccion_empresa = form1.cleaned_data['direccion_empresa'].strip()
                            cliente.ingresos_mensuales = form1.cleaned_data['ingresos_mensuales'].strip()
                            cliente.observaciones = form1.cleaned_data['observaciones'].strip()
                            cliente.estado = form1.cleaned_data['estado']

                            # Datos del usuario que registro
                            cliente.usuario_registro = usuario
                            cliente.save()

                            cliente.contactocliente_set.all().delete()
                            for contacto in contactos:
                                contacto.cliente = cliente
                                contacto.save()

                            # Elimina las variables de sesion
                            del request.session['contactos_cliente']
                            usuario_actual = Usuario.objects.get(id=user.id)
                            direccion_ip = request.META['REMOTE_ADDR']
                            registro_historial(direccion_ip, usuario_actual, "Modifico cliente, identificacion: " + str(cliente.identificacion))
                            return HttpResponseRedirect('/inverboy/home/busquedaclientes/' + str(proyecto_id))
                    else:
                        return HttpResponseRedirect('/inverboy/home/')
                else:
                    contactos = list(cliente.contactocliente_set.all())
                    request.session['contactos_cliente'] = contactos
                form1.fields['identificacion'].widget.attrs['readonly'] = 'readonly'
                return render_to_response('ventas/nuevocliente.html', {'user': user, 'form1': form1, 'form2': form2, 'contactos': contactos, 'proyecto': proyecto, 'change': True})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Detalles cliente
def detalles_cliente(request, cliente_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_cliente' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                cliente = Cliente.objects.get(id=cliente_id)
                cliente.existe_prospecto_venta_proyecto(proyecto)
                return render_to_response('ventas/detallescliente.html', {'user': user, 'cliente': cliente, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Nuevo prospecto de venta
def nuevo_prospecto_venta(request, cliente_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_contratoventa' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                cliente = Cliente.objects.get(id=cliente_id)
                cliente.existe_prospecto_venta_proyecto(proyecto=proyecto)
                #Valida que no exista prospecto
                if cliente.prospecto_venta_proyecto == None and cliente.estado:
                    encuesta = Encuesta.objects.get(titulo='Encuesta prospecto venta', estado_registro=True)
                    encuesta_form = EncuestaClienteForm(encuesta=encuesta)
                    if request.method == 'POST':
                        inmuebles_interes = None
                        notificaciones_prospecto = None
                        try:
                            inmuebles_interes = request.session['inmuebles_interes']
                            notificaciones_prospecto = request.session['notificaciones_prospecto']
                        except :
                            pass
                        if inmuebles_interes != None and notificaciones_prospecto != None:
                            encuesta_form = EncuestaClienteForm(encuesta, request.POST)
                            if encuesta_form.is_valid():
                                respuestas_cliente = []
                                for campo in encuesta_form.fields:
                                    pregunta_encuesta = encuesta.preguntaencuesta_set.get(id=campo)
                                    respuestas_cliente.append(encuesta_form.cleaned_data[campo])

                                #Registros en la BD
                                prospecto_venta = ProspectoVenta()
                                prospecto_venta.cliente = cliente
                                prospecto_venta.proyecto = proyecto
                                prospecto_venta.usuario_registro = usuario
                                prospecto_venta.usuario_responsable = usuario
                                prospecto_venta.save()

                                #Diligencia la encuesta
                                encuesta_cliente = EncuestaCliente()
                                encuesta_cliente.cliente = cliente
                                encuesta_cliente.encuesta = encuesta
                                encuesta_cliente.usuario_registro = usuario
                                encuesta_cliente.save()

                                for respuesta_cliente in respuestas_cliente:
                                    #Registro de la pregunta
                                    pregunta_encuesta_cliente = PreguntaEncuestaCliente()
                                    pregunta_encuesta_cliente.encuesta_cliente = encuesta_cliente
                                    pregunta_encuesta_cliente.pregunta_encuesta = respuesta_cliente.pregunta_encuesta
                                    pregunta_encuesta_cliente.save()

                                    #Registro de la respuesta
                                    respuesta_encuesta_cliente = RespuestaClientePreguntaEncuesta()
                                    respuesta_encuesta_cliente.encuesta_cliente = encuesta_cliente
                                    respuesta_encuesta_cliente.pregunta_encuesta_cliente = pregunta_encuesta_cliente
                                    respuesta_encuesta_cliente.respuesta_pregunta_encuesta = respuesta_cliente
                                    respuesta_encuesta_cliente.save()

                                for inmueble_interes in inmuebles_interes:
                                    agrupacion_inmueble_prospecto_venta = AgrupacionesInmuebleProspectoVenta()
                                    agrupacion_inmueble_prospecto_venta.prospecto_venta = prospecto_venta
                                    agrupacion_inmueble_prospecto_venta.agrupacion_inmueble_id = inmueble_interes.id
                                    agrupacion_inmueble_prospecto_venta.save()

                                for notificacion_prospecto in notificaciones_prospecto:
                                    notificacion_prospecto.prospecto_venta = prospecto_venta
                                    notificacion_prospecto.usuario_registro = usuario
                                    notificacion_prospecto.usuario_responsable = usuario
                                    notificacion_prospecto.save()

                                # Elimina las variables de session
                                del request.session['inmuebles_interes']
                                del request.session['notificaciones_prospecto']
                                return HttpResponseRedirect('/inverboy/home/detallesprospectoventa/' + str(cliente_id) + '/' + str(proyecto_id) + '/')
                        else:
                            return HttpResponseRedirect('/inverboy/home/')
                    else:
                        inmuebles_interes = []
                        request.session['inmuebles_interes'] = inmuebles_interes

                        notificaciones_prospecto = []
                        request.session['notificaciones_prospecto'] = notificaciones_prospecto

                    return render_to_response('ventas/nuevoprospectoventa.html', {'user': user, 'encuesta_form': encuesta_form, 'agrupaciones': inmuebles_interes, 'notificaciones_prospecto': notificaciones_prospecto, 'cliente': cliente, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Detalles prospecto de venta
def detalles_prospecto_venta(request, cliente_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_contratoventa' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                cliente = Cliente.objects.get(id=cliente_id)
                prospecto_venta = proyecto.prospectoventa_set.get(cliente=cliente)
                if prospecto_venta != None:
                    return render_to_response('ventas/detallesprospectoventa.html', {'user': user, 'prospecto_venta': prospecto_venta, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Nueva pregunta encuesta prospecto de venta
def nueva_encuesta(request):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_encuesta' in user.get_all_permissions():
            error = ''
            if request.method == 'POST':
                preguntas_encuesta = None
                try:
                    preguntas_encuesta = request.session['preguntas_encuesta']
                except :
                    pass
                if preguntas_encuesta != None:
                    form = EncuestaForm(request.POST)
                    if len(preguntas_encuesta) > 0:
                        if form.is_valid():
                            encuesta = Encuesta()
                            encuesta.titulo = form.cleaned_data['titulo'].strip()
                            encuesta.descripcion = form.cleaned_data['descripcion'].strip()
                            encuesta.save()

                            for pregunta_encuesta in preguntas_encuesta:
                                pregunta_encuesta.encuesta = encuesta
                                pregunta_encuesta.save()

                                for respuesta in pregunta_encuesta.respuestas:
                                    pregunta_encuesta.respuestapreguntaencuesta_set.create(texto=respuesta)
                            del request.session['preguntas_encuesta']
                            return HttpResponseRedirect('/inverboy/home/detallesencuesta/' + str(encuesta.id) + '/')
                    else:
                        error = 'Debe ingresar por lo menos una pregunta a la encuesta'
                else:
                    return HttpResponseRedirect('/inverboy/home/')
            else:
                preguntas_encuesta = []
                request.session['preguntas_encuesta'] = preguntas_encuesta
                form = EncuestaForm()
            return render_to_response('ventas/nuevaencuesta.html', {'user': user, 'form': form, 'preguntas': preguntas_encuesta, 'error': error})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Busqueda encuestas
def busqueda_encuestas(request):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_encuesta' in user.get_all_permissions():
            criterio = ''
            encuestas = Encuesta.objects.all()
            if request.method == 'POST':
                criterio = request.POST['criterio'].strip()
                if criterio != '':
                    encuestas = encuestas.filter(Q(titulo__icontains=criterio) | Q(descripcion__icontains=criterio))
            pag = Paginador(request, encuestas, 20, 1)
            return render_to_response('ventas/reporteencuestas.html', {'user': user, 'encuestas': pag, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Detalles encuesta
def detalles_encuesta(request, encuesta_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_encuesta' in user.get_all_permissions():
            encuesta = Encuesta.objects.get(id=encuesta_id)
            return render_to_response('ventas/detallesencuesta.html', {'user': user, 'encuesta': encuesta})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar encuesta
def modificar_encuesta(request, encuesta_id):
    request.session.set_expiry(TIEMPO_INACTIVIDAD)
    user = request.user
    #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
    if 'inverboy.add_encuesta' in user.get_all_permissions():
        error = ''
        encuesta = Encuesta.objects.get(id=encuesta_id)
        form = EncuestaForm(initial={'titulo': encuesta.titulo, 'descripcion': encuesta.descripcion, 'preguntas': encuesta.preguntaencuesta_set.all(), })
        preguntas_encuesta = encuesta.preguntaencuesta_set.all()
        if request.method == 'POST':
            if preguntas_encuesta != None:
                form = EncuestaForm(request.POST)
                if len(preguntas_encuesta) > 0:
                    if form.is_valid():
                        encuesta = Encuesta()
                        encuesta.titulo = form.cleaned_data['titulo'].strip()
                        encuesta.descripcion = form.cleaned_data['descripcion'].strip()
                        encuesta.save()
                        for pregunta_encuesta in preguntas_encuesta:
                            pregunta_encuesta.encuesta = encuesta
                            pregunta_encuesta.save()

                            for respuesta in pregunta_encuesta.respuestas:
                                pregunta_encuesta.respuestapreguntaencuesta_set.create(texto=respuesta)
                        del request.session['preguntas_encuesta']
                        return HttpResponseRedirect('/inverboy/home/detallesencuesta/' + str(encuesta.id) + '/')
                else:
                    error = 'Debe ingresar por lo menos una pregunta a la encuesta'

        return render_to_response('ventas/nuevaencuesta.html', {'user': user, 'form': form, 'preguntas': preguntas_encuesta, 'encuesta': encuesta, 'error': error, 'modificar': True})
        #return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Nueva sección de proyecto
def nueva_seccion_proyecto(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_seccionproyecto' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                # Inicialización de formularios
                form = SeccionProyectoForm()
                if request.method == 'POST':
                    form = SeccionProyectoForm(request.POST)
                    if form.is_valid():
                        nombre = form.cleaned_data['nombre'].strip()
                        iniciales = form.cleaned_data['iniciales'].strip()
                        validar_nombre_unico, form = validate_unique_field(SeccionProyecto, {'nombre': nombre, 'proyecto': proyecto}, fields_error=['nombre'], form=form)
                        validar_iniciales_unico, form = validate_unique_field(SeccionProyecto, {'iniciales': iniciales, 'proyecto': proyecto}, fields_error=['iniciales'], form=form)
                        if validar_nombre_unico == False and validar_iniciales_unico == False:
                            seccion_proyecto = SeccionProyecto(nombre=nombre, iniciales= iniciales, proyecto=proyecto)
                            seccion_proyecto.save()

                            # Registro de la accion del usuario
                            direccion_ip = request.META['REMOTE_ADDR']
                            registro_historial(direccion_ip, usuario, "Registro nueva seccion de proyecto: " + unicode(nombre) + ", proyecto: " + unicode(proyecto.nombre))
                            return HttpResponseRedirect('/inverboy/home/busquedaseccionesproyecto/' + str(proyecto_id)+ '/')
                return render_to_response('ventas/nuevaseccionproyecto.html',{'user': user, 'form': form, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Busqueda secciones proyecto
def busqueda_secciones_proyecto(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_seccionproyecto' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                secciones_proyecto = proyecto.seccionproyecto_set.filter(nombre__icontains=criterio)
                pag = Paginador(request, secciones_proyecto, 20, 1)
                return render_to_response('ventas/reporteseccionesproyecto.html', {'user': user, 'secciones_proyecto': pag, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar seccion proyecto
def modificar_seccion_proyecto(request, seccion_proyecto_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_seccionproyecto' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                seccion_proyecto = proyecto.seccionproyecto_set.get(id=seccion_proyecto_id)
                form = SeccionProyectoForm(instance=seccion_proyecto)
                if request.method == 'POST':
                    form = SeccionProyectoForm(request.POST)
                    if form.is_valid():
                        nombre = form.cleaned_data['nombre'].strip()
                        iniciales = form.cleaned_data['iniciales'].strip()
                        validar_nombre_unico, form = validate_unique_field(SeccionProyecto, {'nombre': nombre, 'proyecto': proyecto}, fields_error=['nombre'], exclude_initials_values={'nombre': seccion_proyecto.nombre, 'proyecto': proyecto}, form=form)
                        validar_iniciales_unico, form = validate_unique_field(SeccionProyecto, {'iniciales': iniciales, 'proyecto': proyecto}, fields_error=['iniciales'], exclude_initials_values={'iniciales': seccion_proyecto.iniciales, 'proyecto': proyecto}, form=form)
                        if validar_nombre_unico == False and validar_iniciales_unico == False:
                            seccion_proyecto.nombre = nombre
                            seccion_proyecto.iniciales = iniciales
                            seccion_proyecto.save()

                            # Registro de la accion del usuario
                            usuario_actual = Usuario.objects.get(id=user.id)
                            direccion_ip = request.META['REMOTE_ADDR']
                            registro_historial(direccion_ip, usuario_actual, "Modifico seccion proyecto, nombre: " + unicode(seccion_proyecto.nombre) + ', proyecto: ' + unicode(proyecto.nombre))
                            return HttpResponseRedirect('/inverboy/home/busquedaseccionesproyecto/' + str(proyecto_id))
                return render_to_response('ventas/nuevaseccionproyecto.html', {'user': user, 'form': form, 'proyecto': proyecto, 'change': True})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Nuevo tipoinmueble
def nuevo_tipo_inmueble(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_tipoinmueble' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                # Inicialización de formularios
                form = TipoInmuebleForm()
                if request.method == 'POST':
                    form = TipoInmuebleForm(request.POST)
                    if form.is_valid():
                        form.save()

                        # Registro de la accion del usuario
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario, "Registro nuevo tipo inmueble, id: "+str(form.instance.id))
                        return HttpResponseRedirect('/inverboy/home/busquedatipoinmuebles/' + str(proyecto_id)+ '/')
                return render_to_response('ventas/nuevotipoinmueble.html',{'user': user, 'form': form, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Busqueda tipo inmuebles
def busqueda_tipo_inmuebles(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_tipoinmueble' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                tipo_inmuebles = TipoInmueble.objects.all()
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()

                tipo_inmuebles = tipo_inmuebles.filter(nombre__icontains=criterio)
                pag = Paginador(request, tipo_inmuebles, 20, 1)
                return render_to_response('ventas/reportetipoinmuebles.html', {'user': user, 'tipo_inmuebles': pag, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar tipo inmueble
def modificar_tipo_inmueble(request, tipo_inmueble_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_tipoinmueble' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                tipo_inmueble = TipoInmueble.objects.get(id=tipo_inmueble_id)
                form = TipoInmuebleForm(instance=tipo_inmueble)
                if request.method == 'POST':
                    form = TipoInmuebleForm(request.POST, instance=tipo_inmueble)
                    if form.is_valid():
                        form.save()

                        # Registro de la accion del usuario
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, "Modifico tipo inmueble, id: " + str(form.instance.id))
                        return HttpResponseRedirect('/inverboy/home/busquedatipoinmuebles/' + str(proyecto_id))
                return render_to_response('ventas/nuevotipoinmueble.html', {'user': user, 'form': form, 'proyecto': proyecto, 'change': True})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Nuevo inmueble
def nuevo_inmueble(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_inmueble' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                # Inicialización de formularios
                form = InmuebleForm()
                if request.method == 'POST':
                    form = InmuebleForm(request.POST)
                    if form.is_valid():
                        identificacion = form.cleaned_data['identificacion']
                        seccion_proyecto = form.cleaned_data['seccion_proyecto']
                        validar_identificacion, form = validate_unique_field(Inmueble, {'identificacion': identificacion, 'seccion_proyecto': seccion_proyecto}, fields_error={'identificacion': identificacion}, form=form)
                        if validar_identificacion == False:
                            inmueble = Inmueble()
                            inmueble.identificacion = identificacion
                            inmueble.area_construida = form.cleaned_data['area_construida']
                            inmueble.area_privada = form.cleaned_data['area_privada']
                            inmueble.fecha_entrega_obra = form.cleaned_data['fecha_entrega_obra']
                            inmueble.valor = form.cleaned_data['valor']
                            inmueble.lista_precios = form.cleaned_data['lista_precios']
                            inmueble.tipo_inmueble = form.cleaned_data['tipo_inmueble']
                            inmueble.seccion_proyecto = seccion_proyecto
                            inmueble.proyecto = proyecto
                            inmueble.usuario_registro = usuario
                            inmueble.save()

                            # Registro de la accion del usuario
                            direccion_ip = request.META['REMOTE_ADDR']
                            registro_historial(direccion_ip, usuario, "Registro nuevo inmueble, identificacion: "+ unicode(inmueble.identificacion))
                            return HttpResponseRedirect('/inverboy/home/busquedainmuebles/' + str(proyecto_id) + '/')
                # Actualiza las secciones del proyecto actual
                form.fields['seccion_proyecto'].queryset = proyecto.seccionproyecto_set.all()
                # Remueve el campo de estado
                form.fields.pop('estado_registro')
                return render_to_response('ventas/nuevoinmueble.html',{'user': user, 'form': form, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Busqueda inmuebles
def busqueda_inmuebles(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_inmueble' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                tipo_inmueble = TipoInmueble(id='')
                seccion_proyecto = SeccionProyecto(id='')
                criterio = ''
                inmuebles = proyecto.inmueble_set.all()
                if request.method == 'POST':
                    tipo_inmueble = request.POST['tipo_inmueble'].strip()
                    seccion_proyecto = request.POST['seccion_proyecto'].strip()
                    criterio = request.POST['criterio'].strip()
                    if tipo_inmueble != '':
                        tipo_inmueble = TipoInmueble.objects.get(id=tipo_inmueble)
                        inmuebles = inmuebles.filter(tipo_inmueble=tipo_inmueble)
                    if seccion_proyecto != '':
                        seccion_proyecto = proyecto.seccionproyecto_set.get(id=seccion_proyecto)
                        inmuebles = inmuebles.filter(seccion_proyecto=seccion_proyecto)
                    if criterio != '':
                        inmuebles = inmuebles.filter(identificacion=criterio)
                pag = Paginador(request, inmuebles, 20, 1)
                tipo_inmuebles = TipoInmueble.objects.all()
                secciones_proyecto = proyecto.seccionproyecto_set.all()
                return render_to_response('ventas/reporteinmuebles.html', {'user': user, 'inmuebles': pag, 'tipo_inmuebles': tipo_inmuebles, 'actual_tipo_inmueble': tipo_inmueble, 'secciones_proyecto': secciones_proyecto, 'actual_seccion_proyecto': seccion_proyecto, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar inmueble
def modificar_inmueble(request, inmueble_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_inmueble' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                inmueble = proyecto.inmueble_set.get(id=inmueble_id)
                form = InmuebleForm(instance=inmueble)
                if request.method == 'POST':
                    form = InmuebleForm(instance=inmueble, data=request.POST)
                    if form.is_valid():
                        identificacion = form.cleaned_data['identificacion'].strip()
                        seccion_proyecto = form.cleaned_data['seccion_proyecto']
                        validar_identificacion = False
                        if inmueble.identificacion != identificacion:
                            validar_identificacion, form = validate_unique_field(Inmueble, {'identificacion': identificacion, 'seccion_proyecto': seccion_proyecto}, fields_error={'identificacion': identificacion}, exclude_initials_values={'identificacion': inmueble.identificacion, 'seccion_proyecto': inmueble.seccion_proyecto}, form=form)
                        if validar_identificacion == False:
                            inmueble.identificacion = identificacion
                            inmueble.seccion_proyecto = seccion_proyecto
                            inmueble.area_construida = form.cleaned_data['area_construida']
                            inmueble.area_privada = form.cleaned_data['area_privada']
                            inmueble.fecha_entrega_obra = form.cleaned_data['fecha_entrega_obra']
                            inmueble.tipo_inmueble = form.cleaned_data['tipo_inmueble']
                            # Valida si el inmueble no se encuentre comprometido
                            if inmueble.permiso_modificar == True:
                                inmueble.valor = form.cleaned_data['valor']
                                inmueble.lista_precios = form.cleaned_data['lista_precios']
                                #a = form.cleaned_data['estado_registro']
                                inmueble.estado_registro = True
                            inmueble.usuario_registro = usuario
                            inmueble.save()

                            # Registro de la accion del usuario
                            direccion_ip = request.META['REMOTE_ADDR']
                            registro_historial(direccion_ip, usuario, "Modifico inmueble, identificacion: " + unicode(inmueble.identificacion))
                            return HttpResponseRedirect('/inverboy/home/busquedainmuebles/' + str(proyecto_id) + '/')
                # Actualiza las secciones del proyecto actual
                form.fields['seccion_proyecto'].queryset = proyecto.seccionproyecto_set.all()
                return render_to_response('ventas/nuevoinmueble.html', {'user': user, 'form': form, 'proyecto': proyecto, 'change': True})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificacion masiva de inmuebles
# Solo se aplica la modificación masiva a inmuebles que no esten comprometidos
def modificacion_masiva_inmuebles(request, inmueble_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_inmueble' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                # Valida que el inmueble "maestro" este activo
                inmueble = None
                try:
                    inmueble = proyecto.lista_inmuebles().get(id=inmueble_id)
                except :
                    pass
                if inmueble != None:
                    seccion_proyecto_id = ''
                    seccion_proyecto = SeccionProyecto(id='')
                    criterio = ''
                    if request.method == 'POST':
                        seccion_proyecto_id = request.POST['seccion_proyecto'].strip()
                        criterio = request.POST['criterio'].strip()
                        propiedades_inmueble = None
                        try:
                            propiedades_inmueble = request.POST.getlist('propiedades_inmueble')
                        except :
                            pass
                        if propiedades_inmueble != None:
                            seleccion_modificacion_masiva = None
                            try:
                                seleccion_modificacion_masiva = request.POST.getlist('seleccion_modificacion_masiva')
                            except :
                                pass
                            if seleccion_modificacion_masiva != None:
                                inmuebles = proyecto.lista_inmuebles().filter(tipo_inmueble=inmueble.tipo_inmueble, id__in=seleccion_modificacion_masiva)
                                propiedades_inmueble_actualizar = {}
                                for propiedad_inmueble in propiedades_inmueble:
                                    propiedades_inmueble_actualizar.update({propiedad_inmueble: inmueble.__getattribute__(propiedad_inmueble)})
                                inmuebles.update(**propiedades_inmueble_actualizar)

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
                    secciones_proyecto = proyecto.seccionproyecto_set.all()
                    return render_to_response('ventas/modificacionmasivainmuebles.html', {'user': user, 'inmueble': inmueble, 'inmuebles': pag, 'secciones_proyecto': secciones_proyecto, 'actual_seccion_proyecto': seccion_proyecto, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Asignaciòn individual de precios
def asignacion_individual_precios_inmuebles(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_inmueble' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                tipo_inmueble = TipoInmueble()
                seccion_proyecto = SeccionProyecto()
                criterio = ''
                # Solo los inmuebles que no se encuentran comprometidos
                inmuebles = proyecto.lista_inmuebles().filter(item_agrupacion_inmueble__agrupacion_inmueble__agrupacion_contrato_venta=None)
                if request.method == 'POST':
                    tipo_inmueble = request.POST['tipo_inmueble'].strip()
                    seccion_proyecto = request.POST['seccion_proyecto'].strip()
                    criterio = request.POST['criterio'].strip()
                    if tipo_inmueble != '':
                        tipo_inmueble = TipoInmueble.objects.get(id=tipo_inmueble)
                        inmuebles = inmuebles.filter(tipo_inmueble=tipo_inmueble)
                    if seccion_proyecto != '':
                        seccion_proyecto = proyecto.seccionproyecto_set.get(id=seccion_proyecto)
                        inmuebles = inmuebles.filter(seccion_proyecto=seccion_proyecto)
                    if criterio != '':
                        inmuebles = inmuebles.filter(identificacion__icontains=criterio)
                items = len(inmuebles)
                if items == 0:
                    items = 1
                pag = Paginador(request, inmuebles, items, 1)
                tipo_inmuebles = TipoInmueble.objects.all()
                secciones_proyecto = proyecto.lista_secciones()
                return render_to_response('ventas/asignacionindividualpreciosinmuebles.html', {'user': user, 'inmuebles': pag, 'tipo_inmuebles': tipo_inmuebles, 'actual_tipo_inmueble': tipo_inmueble, 'secciones_proyecto': secciones_proyecto, 'actual_seccion_proyecto': seccion_proyecto, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Nueva agrupación inmueble
def nueva_agrupacion_inmueble(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_agrupacioninmueble' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                # Inicialización de formularios
                #form = AgrupacionInmuebleForm()
                error = ''
                # Actualiza el valor total de la agrupación
                valor_total = 0
                            
                if request.method == 'POST':
                    inmuebles_agrupacion = None
                    try:
                        inmuebles_agrupacion = request.session['inmuebles_agrupacion']
                    except :
                        pass
                    if inmuebles_agrupacion != None:
                        if len(inmuebles_agrupacion) > 0:
                            inmuebles_disponibles = True
                            inmuebles_sin_disponibilidad = []
                            for inmueble_agrupacion in inmuebles_agrupacion:
                                inmueble_actual = Inmueble.objects.get(id=inmueble_agrupacion.id)
                                if inmueble_actual.item_agrupacion_inmueble != None:
                                    inmuebles_disponibles = False
                                    inmuebles_sin_disponibilidad.append(inmueble_agrupacion)
                            for inmueble_sin_disponibilidad in inmuebles_sin_disponibilidad:
                                inmuebles_agrupacion.remove(inmueble_sin_disponibilidad)
                            if inmuebles_disponibles:
                                inmueble_principal = None
                                try:
                                    inmueble_principal = request.POST['inmueble_principal']
                                except :
                                    pass
                                if inmueble_principal != None:
                                    inmueble_principal_seleccionado = proyecto.lista_inmuebles().get(id=inmueble_principal)
                                    if inmueble_principal_seleccionado.valor > 0:
                                        # Creación de la agrupación
                                        agrupacion_inmueble = AgrupacionInmueble()
                                        agrupacion_inmueble.proyecto = proyecto
                                        agrupacion_inmueble.usuario_registro = usuario
                                        agrupacion_inmueble.save()

                                        # Inmueble principal
                                        inmueble_principal_agrupacion = ItemAgrupacionInmueble()

                                        # Registro de los inmuebles en la agrupación
                                        for inmueble in inmuebles_agrupacion:
                                            item_agrupacion = ItemAgrupacionInmueble()
                                            item_agrupacion.inmueble = inmueble
                                            item_agrupacion.agrupacion_inmueble = agrupacion_inmueble
                                            item_agrupacion.save()

                                            # Inmueble principal
                                            if inmueble.id == int(inmueble_principal):
                                                inmueble_principal_agrupacion = item_agrupacion

                                            # Actualización del inmueble
                                            inmueble.item_agrupacion_inmueble = item_agrupacion
                                            inmueble.save()

                                        # Inmueble principal
                                        agrupacion_inmueble.inmueble_principal = inmueble_principal_agrupacion
                                        agrupacion_inmueble.save()

                                        # Registro de la accion del usuario
                                        direccion_ip = request.META['REMOTE_ADDR']
                                        registro_historial(direccion_ip, usuario, "Registro nueva agrupacion inmueble, identificacion: " + unicode(agrupacion_inmueble.identificacion))
                                        return HttpResponseRedirect('/inverboy/home/busquedaagrupacioninmuebles/' + str(proyecto_id) + '/')
                                    else:
                                        error = 'El inmueble principal seleccionado debe tener un precio mayor a 0.'
                                else:
                                    error = 'Debe seleccionar un inmueble principal.'
                            else:
                                error = 'Algunos inmuebles seleccionados para la nueva agrupación no estan libres, estos se han eliminado de la lista de inmuebles de la agrupación.'
                        else:
                            error = 'La lista de inmuebles no debe estar vacia'
                    else:
                        return HttpResponseRedirect('/inverboy/home/')
                else:
                    # Genera las variables de la session
                    inmuebles_agrupacion = []
                    request.session['inmuebles_agrupacion'] = inmuebles_agrupacion
                tipos_inmueble = TipoInmueble.objects.all()

                # Actualiza el valor total de la agrupación
                for inmueble_actual in inmuebles_agrupacion:
                    valor_total = round(valor_total + inmueble_actual.valor, 2)
                    
                return render_to_response('ventas/nuevaagrupacioninmueble.html',{'user': user, 'inmuebles_agrupacion': inmuebles_agrupacion, 'tipos_inmueble': tipos_inmueble, 'valor_total': valor_total, 'proyecto': proyecto, 'error': error})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Busqueda agrupaciones
def busqueda_agrupacion_inmuebles_proyecto(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_agrupacioninmueble' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                agrupacion_inmuebles = proyecto.lista_agrupaciones_inmueble(criterio=criterio)
                pag = Paginador(request, agrupacion_inmuebles, 800, 1)
                return render_to_response('ventas/reporteagrupacioninmueblesproyecto.html', {'user': user, 'agrupacion_inmuebles': pag, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar agrupación inmueble
def modificar_agrupacion_inmueble(request, agrupacion_inmueble_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_agrupacioninmueble' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                # Inicialización de formularios
                agrupacion_inmueble = proyecto.agrupacioninmueble_set.get(id=agrupacion_inmueble_id)
                # Se modifica si y solo si la agrupación no se encuentra comprometida
                #if agrupacion_inmueble.agrupacion_contrato_venta == None:
                    #form = AgrupacionInmuebleForm(instance=agrupacion_inmueble)
		valor_total = agrupacion_inmueble.str_valor()
		inmueble_principal = None
		error = ''
		if request.method == 'POST':
		    inmuebles_agrupacion = None
		    try:
			inmuebles_agrupacion = request.session['inmuebles_agrupacion']
		    except :
			pass
		    if inmuebles_agrupacion != None:
			# Actualiza el valor total de la agrupación
			valor_total = 0
			if len(inmuebles_agrupacion) > 0:
			    inmuebles_disponibles = True
			    inmuebles_sin_disponibilidad = []
			    for inmueble_agrupacion in inmuebles_agrupacion:
				inmueble_actual = Inmueble.objects.get(id=inmueble_agrupacion.id)
				if inmueble_actual.item_agrupacion_inmueble != None:
				    if inmueble_actual.item_agrupacion_inmueble.agrupacion_inmueble != agrupacion_inmueble:
					inmuebles_disponibles = False
					inmuebles_sin_disponibilidad.append(inmueble_agrupacion)
			    for inmueble_sin_disponibilidad in inmuebles_sin_disponibilidad:
				inmuebles_agrupacion.remove(inmueble_sin_disponibilidad)
			    if inmuebles_disponibles:
				inmueble_principal = None
				try:
				    inmueble_principal = request.POST['inmueble_principal']
				except :
				    pass
				if inmueble_principal != None:
				    inmueble_principal_seleccionado = proyecto.lista_inmuebles().get(id=inmueble_principal)
				    if inmueble_principal_seleccionado.valor > 0:
					# Modificación de la agrupación
					agrupacion_inmueble.usuario_registro = usuario
					agrupacion_inmueble.fecha_actualizacion = date.today()
					# Actualiza el inmueble principal de la agrupación
					agrupacion_inmueble.inmueble_principal = None
					agrupacion_inmueble.save()

					# Inmueble principal
					inmueble_principal_agrupacion = ItemAgrupacionInmueble()

					# Lista de inmuebles a eliminar
					ids_inmuebles_agrupacion = []

					# Registro de los inmuebles en la agrupación
					for inmueble in inmuebles_agrupacion:
					    item_agrupacion = None
					    try:
						item_agrupacion = ItemAgrupacionInmueble.objects.get(inmueble=inmueble, agrupacion_inmueble=agrupacion_inmueble, agrupacion_inmueble__estado_registro=True)
					    except :
						pass
					    if item_agrupacion == None:
						item_agrupacion = ItemAgrupacionInmueble(inmueble=inmueble, agrupacion_inmueble=agrupacion_inmueble)
						item_agrupacion.save()

					    # Inmueble principal
					    if inmueble.id == int(inmueble_principal):
						inmueble_principal_agrupacion = item_agrupacion

					    # Actualización del inmueble
					    inmueble.item_agrupacion_inmueble = item_agrupacion
					    inmueble.save()

					    ids_inmuebles_agrupacion.append(inmueble.id)

					# Elimina los inmuebles que ya no pertenecen a la agrupación
					items_agrupacion_inmueble = agrupacion_inmueble.itemagrupacioninmueble_set.all().exclude(inmueble__id__in=ids_inmuebles_agrupacion)
					for item_agrupacion_inmueble in items_agrupacion_inmueble:
					    # Actualiza el item_agrupacion del inmueble
					    item_agrupacion_inmueble.inmueble.item_agrupacion_inmueble = None
					    item_agrupacion_inmueble.inmueble.save()
					    item_agrupacion_inmueble.delete()

					# Inmueble principal
					agrupacion_inmueble.inmueble_principal = inmueble_principal_agrupacion
					agrupacion_inmueble.save()

					# Registro de la accion del usuario
					direccion_ip = request.META['REMOTE_ADDR']
					registro_historial(direccion_ip, usuario, "Modifico agrupacion inmueble, identificacion: " + unicode(agrupacion_inmueble.identificacion))
					return HttpResponseRedirect('/inverboy/home/busquedaagrupacioninmuebles/' + str(proyecto_id) + '/')
				    else:
					error = 'El inmueble principal seleccionado debe tener un precio mayor a 0.'
				else:
				    error = 'Debe seleccionar un inmueble principal.'
			    else:
				error = 'Algunos inmuebles seleccionados para la nueva agrupación no estan libres, estos se han eliminado de la lista de inmuebles de la agrupación.'
			else:
			    error = 'La lista de inmuebles no debe estar vacia'
		    else:
			return HttpResponseRedirect('/inverboy/home/')
		else:
		    # Genera las variables de la session
		    inmuebles_agrupacion = []
		    for item_agrupacion_inmueble in agrupacion_inmueble.itemagrupacioninmueble_set.all():
			inmuebles_agrupacion.append(item_agrupacion_inmueble.inmueble)
		    request.session['inmuebles_agrupacion'] = inmuebles_agrupacion
		    inmueble_principal = agrupacion_inmueble.inmueble_principal.inmueble.id
		tipos_inmueble = TipoInmueble.objects.all()
		return render_to_response('ventas/nuevaagrupacioninmueble.html',{'user': user, 'agrupacion_inmueble': agrupacion_inmueble, 'inmuebles_agrupacion': inmuebles_agrupacion, 'inmueble_principal': inmueble_principal, 'valor_total': valor_total, 'tipos_inmueble': tipos_inmueble, 'proyecto': proyecto, 'change': True, 'error': error})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Eliminar agrupación inmueble
def eliminar_agrupacion_inmueble(request, agrupacion_inmueble_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_agrupacioninmueble' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                # Inicialización de formularios
                agrupacion_inmueble = proyecto.agrupacioninmueble_set.get(id=agrupacion_inmueble_id)
                # Se elimina si y solo si la agrupación no se encuentra comprometida
                if agrupacion_inmueble.agrupacion_contrato_venta == None:
                    # Actualiza los inmuebles que pertenecian a la agrupación
                    for item_agrupacion_inmueble in agrupacion_inmueble.itemagrupacioninmueble_set.all():
                        item_agrupacion_inmueble.inmueble.item_agrupacion_inmueble = None
                        item_agrupacion_inmueble.inmueble.save()

                    # Actualiza la agrupación de inmuebles
                    agrupacion_inmueble.estado_registro = False
                    agrupacion_inmueble.save()

                    # Registro de la accion del usuario
                    direccion_ip = request.META['REMOTE_ADDR']
                    registro_historial(direccion_ip, usuario, "Elimino agrupacion inmueble, identificacion: " + unicode(agrupacion_inmueble.identificacion))
                    return HttpResponseRedirect('/inverboy/home/busquedaagrupacioninmuebles/' + str(proyecto_id) + '/')
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Busqueda de agrupaciones disponibles para realizar contrato de venta
def busqueda_agrupacion_inmuebles_proyecto_nuevo_contrato_venta(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_contratoventa' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                # Lista solo las agrupaciones que no esten comprometidas
                agrupacion_inmuebles = proyecto.lista_agrupaciones_inmueble(criterio=criterio).filter(agrupacion_contrato_venta=None)
                pag = Paginador(request, agrupacion_inmuebles, 20, 1)
                return render_to_response('ventas/busquedaagrupacioninmueblesnuevocontratoventa.html', {'user': user, 'agrupacion_inmuebles': pag, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Nuevo contrato de venta
def nuevo_contrato_venta(request, agrupacion_inmueble_id, prospecto_venta_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_contratoventa' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                prospecto_venta = proyecto.prospectoventa_set.get(id=prospecto_venta_id)
                # Inicialización de formularios
                agrupacion_inmueble = proyecto.agrupacioninmueble_set.get(id=agrupacion_inmueble_id)
                valor_agrupacion_inmueble = agrupacion_inmueble.str_valor()
                # Se modifica si y solo si la agrupación no se encuentra comprometida
                if agrupacion_inmueble.agrupacion_contrato_venta == None:
                    valor_pagar = '-'
                    valor_pagar_entidad_contrato = 0
                    valor_efectivo_pagar = 0
                    error = ''
                    if request.method == 'POST':
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
                        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
                            if monto_credito == None:
                                monto_credito = 0
                            # Actualiza el valor total del inmueble
                            for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                                valor_agrupacion_inmueble = round(valor_agrupacion_inmueble + adicional_agrupacion_inmueble_contrato.valor, 2)
                            # Actualiza el valor a pagar por el cliente
                            valor_pagar = monto_credito
                            for pago_entidad_contrato in pagos_entidades_contrato:
                                valor_pagar_entidad_contrato = round(valor_pagar_entidad_contrato + pago_entidad_contrato.valor, 2)
                            for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                                valor_efectivo_pagar = round(valor_efectivo_pagar + cuota_efectivo_contrato.valor, 2)

                            valor_pagar = round(valor_pagar + valor_pagar_entidad_contrato + valor_efectivo_pagar, 2)

                            form = ContratoVentaForm(request.POST)
                            if form.is_valid():
                                if (len(proyecto.lista_adicionales_agrupaciones_inmueble()) > 0 and len(adicionales_agrupacion_inmueble_contrato) > 0) or len(proyecto.lista_adicionales_agrupaciones_inmueble()) == 0:
                                    forma_pago = form.cleaned_data['forma_pago']
                                    if forma_pago != '':
                                        if valor_pagar < round(valor_agrupacion_inmueble - 100, 2):
                                            error = 'El valor a pagar por el cliente no debe ser menor al valor total del inmueble.'
                                        if valor_pagar > round(valor_agrupacion_inmueble + 100, 2):
                                            error = 'El valor a pagar por el cliente no debe exceder al valor total del inmueble.'
                                    if error == '':
                                        # Valida que los valores de las cuotas en efectivo no sean negativos
                                        for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                                            if cuota_efectivo_contrato.valor <= 0:
                                                error = 'Los valores de las cuotas en efectivo deben ser mayores a 0 (cero).'
                                        if error == '':
                                            # Se registra el contrato de venta
                                            contrato_venta = ContratoVenta()
                                            contrato_venta.prospecto_venta = prospecto_venta
                                            contrato_venta.proyecto = proyecto
                                            if forma_pago != '':
                                                contrato_venta.forma_pago = int(forma_pago)
                                                if contrato_venta.forma_pago == 1:
                                                    contrato_venta.entidad_bancaria_credito = form.cleaned_data['entidad_bancaria_credito']
                                                    contrato_venta.monto_credito = monto_credito

                                            contrato_venta.usuario_registro = usuario
                                            contrato_venta.usuario_responsable = usuario
                                            if 'valor_desembolsado_credito' in request.POST and request.POST['valor_desembolsado_credito']:
                                                contrato_venta.valor_desembolsado_credito = float(request.POST['valor_desembolsado_credito'].replace(",","."))
                                            if 'fecha_registro_desembolso_credito' in request.POST and request.POST['fecha_registro_desembolso_credito']:
                                                contrato_venta.fecha_registro_desembolso_credito = datetime.datetime.strptime(request.POST['fecha_registro_desembolso_credito'],'%Y-%m-%d')
                                            contrato_venta.save()

                                            # Se registra el estado del contrato de venta
                                            estado_contrato_venta = EstadoContratoVenta()
                                            estado_contrato_venta.estado_contrato = 1
                                            estado_contrato_venta.fecha_limite_estado = form.cleaned_data['fecha_maxima_separacion']
                                            estado_contrato_venta.contrato_venta = contrato_venta
                                            estado_contrato_venta.save()

                                            # Se registra el inmueble del contrato
                                            agrupacion_inmueble_contrato_venta = AgrupacionInmuebleContratoVenta()
                                            agrupacion_inmueble_contrato_venta.agrupacion_inmueble = agrupacion_inmueble
                                            agrupacion_inmueble_contrato_venta.contrato_venta = contrato_venta
                                            agrupacion_inmueble_contrato_venta.save()

                                            # Se actualiza la agrupacion_inmueble_contrato de la agrupacion_inmueble
                                            agrupacion_inmueble.agrupacion_contrato_venta = agrupacion_inmueble_contrato_venta
                                            agrupacion_inmueble.save()

                                            # Se registran los adicionales del inmueble
                                            for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                                                adicional_agrupacion_contrato_venta = AdicionalAgrupacionContratoVenta()
                                                adicional_agrupacion_contrato_venta.nombre = adicional_agrupacion_inmueble_contrato.nombre
                                                adicional_agrupacion_contrato_venta.descripcion = adicional_agrupacion_inmueble_contrato.descripcion
                                                adicional_agrupacion_contrato_venta.valor = adicional_agrupacion_inmueble_contrato.valor
                                                adicional_agrupacion_contrato_venta.contrato_venta = contrato_venta
                                                adicional_agrupacion_contrato_venta.save()

                                            # Se registran los clientes del contrato
                                            for cliente_contrato in clientes_contrato:
                                                cliente_contrato_venta = ClienteContratoVenta()
                                                cliente_contrato_venta.cliente = cliente_contrato
                                                cliente_contrato_venta.contrato_venta = contrato_venta
                                                cliente_contrato_venta.save()
                                                if cliente_contrato.id == prospecto_venta.cliente.id:
                                                    contrato_venta.cliente_principal = cliente_contrato_venta

                                            # Se actualiza el contrato venta
                                            contrato_venta.save()

                                            # Se registran los pagos por entidades bancarias del contrato
                                            for pago_entidad_contrato in pagos_entidades_contrato:
                                                pago_entidad_contrato.contrato_venta = contrato_venta
                                                pago_entidad_contrato.save()

                                            # Se registran los pagos en efectivo del contrato
                                            for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                                                cuota_efectivo_contrato.contrato_venta = contrato_venta
                                                cuota_efectivo_contrato.save()

                                            # Se eliminan las variables de session
                                            del request.session['clientes_contrato']
                                            del request.session['pagos_entidades_contrato']
                                            del request.session['cuotas_efectivo_contrato']
                                            del request.session['adicionales_agrupacion_inmueble_contrato']
                                            return HttpResponseRedirect('/inverboy/home/detallescontratoventa/' + str(contrato_venta.id) + '/' + str(proyecto_id) + '/')
                                else:
                                    error = 'Debe seleccionar por lo menos un adicional.'
                    else:
                        clientes_contrato = []
                        clientes_contrato.append(prospecto_venta.cliente)
                        request.session['clientes_contrato'] = clientes_contrato
                        pagos_entidades_contrato = []
                        cuotas_efectivo_contrato = []
                        request.session['pagos_entidades_contrato'] = pagos_entidades_contrato
                        request.session['cuotas_efectivo_contrato'] = cuotas_efectivo_contrato
                        adicionales_agrupacion_inmueble_contrato = []
                        request.session['adicionales_agrupacion_inmueble_contrato'] = adicionales_agrupacion_inmueble_contrato
                        form = ContratoVentaForm()
                    return render_to_response('ventas/nuevocontratoventa.html',{'user': user, 'form': form, 'prospecto_venta': prospecto_venta, 'agrupacion_inmueble': agrupacion_inmueble, 'adicionales_agrupacion_inmueble_contrato': adicionales_agrupacion_inmueble_contrato, 'valor_agrupacion_inmueble': valor_agrupacion_inmueble, 'clientes': clientes_contrato, 'pagos_entidades_contrato': pagos_entidades_contrato, 'valor_pagar_entidad_contrato': valor_pagar_entidad_contrato, 'cuotas_efectivo_contrato': cuotas_efectivo_contrato, 'valor_efectivo_pagar': valor_efectivo_pagar, 'valor_pagar': valor_pagar, 'error': error, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Busqueda de contratos de venta
def busqueda_contrato_venta(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_contratoventa' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                # Lista los contratos
                contratos_venta = proyecto.lista_contratos(criterio=criterio)
                pag = Paginador(request, contratos_venta, 20, 1)
                return render_to_response('ventas/busquedacontratoventa.html', {'user': user, 'contratos_venta': pag, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Detalles contrato de venta
def detalles_contrato_venta(request, contrato_venta_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_contratoventa' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                contrato_venta.calcular_valores()
                hoy = datetime.datetime.today()
                entidades_bancarias = EntidadBancaria.objects.filter(estado_registro=True)
                otro_si = ModificacionContratoVenta.objects.filter(contrato_venta=contrato_venta)
                return render_to_response('ventas/detallescontratoventa.html', locals())
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Modificar contrato de venta
def modificar_contrato_venta(request, contrato_venta_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_contratoventa' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                # Inicialización de formularios
                agrupacion_inmueble = contrato_venta.agrupacion_contrato_venta()
                valor_agrupacion_inmueble = agrupacion_inmueble.str_valor()
                # Se modifica el contrato si y solo si el contrato tiene permiso modificar
                if contrato_venta.permiso_modificar:
                    valor_pagar = 0
                    valor_pagar_entidad_contrato = 0
                    valor_efectivo_pagar = 0
                    error = ''
                    if request.method == 'POST':
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
                        if clientes_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None:
                            if monto_credito == None:
                                monto_credito = 0
                            valor_pagar = monto_credito
                            # Actualiza el valor total del inmueble
                            for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                                valor_agrupacion_inmueble = round(valor_agrupacion_inmueble + adicional_agrupacion_inmueble_contrato.valor, 2)
                            # Actualiza el valor a pagar por el cliente
                            for pago_entidad_contrato in pagos_entidades_contrato:
                                valor_pagar_entidad_contrato = round(valor_pagar_entidad_contrato + pago_entidad_contrato.valor, 2)
                            for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                                valor_efectivo_pagar = round(valor_efectivo_pagar + cuota_efectivo_contrato.valor, 2)

                            valor_pagar = round(valor_pagar + valor_pagar_entidad_contrato + valor_efectivo_pagar, 2)

                            form = ContratoVentaForm(instance=contrato_venta, data=request.POST)
                            if contrato_venta.estado_contrato_venta().estado_contrato > 1:
                                form.fields.pop('fecha_maxima_separacion')
                            if request.POST['forma_pago'] == '2':
                                form.fields.pop('monto_credito')
                            if form.is_valid():
                                if (len(proyecto.lista_adicionales_agrupaciones_inmueble()) > 0 and len(adicionales_agrupacion_inmueble_contrato) > 0) or len(proyecto.lista_adicionales_agrupaciones_inmueble()) == 0:
                                    forma_pago = form.cleaned_data['forma_pago']
                                    if forma_pago != '':
                                        if valor_pagar < round(valor_agrupacion_inmueble - 100, 2):
                                            error = 'El valor a pagar por el cliente no debe ser menor al valor total del inmueble.'
                                        if valor_pagar > round(valor_agrupacion_inmueble + 100, 2):
                                            error = 'El valor a pagar por el cliente no debe exceder al valor total del inmueble.'
                                    if error == '':
                                        # Valida que los valores de las cuotas en efectivo no sean negativos
                                        for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                                            if cuota_efectivo_contrato.valor <= 0:
                                                error = 'Los valores de las cuotas en efectivo deben ser mayores a 0 (cero).'
                                        if error == '':
                                            # Se registra el contrato de venta
                                            contrato_venta.forma_pago = None
                                            contrato_venta.entidad_bancaria_credito = None
                                            contrato_venta.monto_credito = 0
                                            # Se valida la forma de pago del contrato
                                            if forma_pago != '':
                                                contrato_venta.forma_pago = int(forma_pago)
                                                if contrato_venta.forma_pago == 1:
                                                    contrato_venta.entidad_bancaria_credito = form.cleaned_data['entidad_bancaria_credito']
                                                    contrato_venta.monto_credito = form.cleaned_data['monto_credito']

                                            contrato_venta.usuario_registro = usuario
                                            contrato_venta.usuario_responsable = usuario
                                            if 'valor_desembolsado_credito' in request.POST:
                                                if request.POST['valor_desembolsado_credito']:
                                                    contrato_venta.valor_desembolsado_credito = float(request.POST['valor_desembolsado_credito'].replace(",","."))
                                                else:
                                                    contrato_venta.valor_desembolsado_credito = None
                                            if 'fecha_registro_desembolso_credito' in request.POST:
                                                if request.POST['fecha_registro_desembolso_credito']:
                                                    contrato_venta.fecha_registro_desembolso_credito = datetime.datetime.strptime(request.POST['fecha_registro_desembolso_credito'],'%Y-%m-%d')
                                                else:
                                                    contrato_venta.fecha_registro_desembolso_credito = None
                                            contrato_venta.save()

                                            # Si el contrato esta en estado (1-Reservado se registra la fecha maxima de separación)
                                            estado_contrato_venta = contrato_venta.estado_contrato_venta()
                                            if estado_contrato_venta.estado_contrato == 1:
                                                if estado_contrato_venta.fecha_limite_estado != form.cleaned_data['fecha_maxima_separacion']:
                                                    estado_contrato_venta.fecha_limite_estado = form.cleaned_data['fecha_maxima_separacion']
                                                    estado_contrato_venta.save()

                                            # Se eliminan los registros de los adicionales
                                            for actual_adicional_agrupacion_inmueble_contrato  in contrato_venta.adicionalagrupacioncontratoventa_set.all():
                                                eliminar_adicional_agrupacion_inmueble_contrato = True
                                                for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                                                    if type(adicional_agrupacion_inmueble_contrato) == type(AdicionalAgrupacionContratoVenta()):
                                                        if actual_adicional_agrupacion_inmueble_contrato.id == adicional_agrupacion_inmueble_contrato.id:
                                                            eliminar_adicional_agrupacion_inmueble_contrato = False
                                                if eliminar_adicional_agrupacion_inmueble_contrato:
                                                    actual_adicional_agrupacion_inmueble_contrato.delete()

                                            # Se registran los nuevos adicionales
                                            for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                                                if type(adicional_agrupacion_inmueble_contrato) == type(AdicionalAgrupacion()):
                                                    adicional_agrupacion_contrato_venta = AdicionalAgrupacionContratoVenta()
                                                    adicional_agrupacion_contrato_venta.nombre = adicional_agrupacion_inmueble_contrato.nombre
                                                    adicional_agrupacion_contrato_venta.descripcion = adicional_agrupacion_inmueble_contrato.descripcion
                                                    adicional_agrupacion_contrato_venta.valor = adicional_agrupacion_inmueble_contrato.valor
                                                    adicional_agrupacion_contrato_venta.contrato_venta = contrato_venta
                                                    adicional_agrupacion_contrato_venta.save()

                                            # Se eliminan los registros de los clientes
                                            for actual_cliente_contrato_venta in contrato_venta.clientecontratoventa_set.all():
                                                eliminar_cliente_contrato_venta = True
                                                for cliente_contrato in clientes_contrato:
                                                    if actual_cliente_contrato_venta.cliente.id == cliente_contrato.id:
                                                        eliminar_cliente_contrato_venta = False
                                                if eliminar_cliente_contrato_venta:
                                                    actual_cliente_contrato_venta.delete()

                                            # Se registran los nuevos clientes del contrato
                                            for cliente_contrato in clientes_contrato:
                                                contrato_venta.clientecontratoventa_set.get_or_create(cliente=cliente_contrato, contrato_venta=contrato_venta)

                                            # Se eliminan los registros de los pagos por entidades bancarias del contrato
                                            for pago_entidad_contrato_venta in contrato_venta.pagoentidadcontratoventa_set.all():
                                                eliminar_pago_entidad_contrato_venta = True
                                                for pago_entidad_contrato in pagos_entidades_contrato:
                                                    if pago_entidad_contrato.id != None:
                                                        if pago_entidad_contrato_venta.id == pago_entidad_contrato.id:
                                                            eliminar_pago_entidad_contrato_venta = False
                                                if eliminar_pago_entidad_contrato_venta:
                                                    pago_entidad_contrato_venta.delete()

                                            # Se registran los pagos por entidades bancarias del contrato
                                            for pago_entidad_contrato in pagos_entidades_contrato:
                                                pago_entidad_contrato.contrato_venta = contrato_venta
                                                pago_entidad_contrato.save()

                                            # Se eliminan los pagos en efectivo del contrato
                                            for pago_efectivo_contrato_venta in contrato_venta.pagoefectivocontratoventa_set.all():
                                                eliminar_pago_efectivo_contrato_venta = True
                                                for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                                                    if cuota_efectivo_contrato.id != None:
                                                        if pago_efectivo_contrato_venta.id == cuota_efectivo_contrato.id:
                                                            eliminar_pago_efectivo_contrato_venta = False
                                                if eliminar_pago_efectivo_contrato_venta:
                                                    pago_efectivo_contrato_venta.delete()

                                            # Se registran los pagos en efectivo del contrato
                                            for cuota_efectivo_contrato in cuotas_efectivo_contrato:
                                                cuota_efectivo_contrato.contrato_venta = contrato_venta
                                                cuota_efectivo_contrato.save()

                                            # Si el contrato ya esta en estado (3-Vendido)
                                            if contrato_venta.estado_contrato_venta().estado_contrato >= 3:
                                                modificacion_contrato_venta = ModificacionContratoVenta()
                                                modificacion_contrato_venta.texto_legal = form.cleaned_data['texto_legal'].strip()
                                                modificacion_contrato_venta.contrato_venta = contrato_venta
                                                modificacion_contrato_venta.usuario_registro = usuario
                                                modificacion_contrato_venta.save()

                                                ### Rutina a ejecutar para guardar una copia del estado actual del contrato solo aplica para estado del contrato despues de (3-Vendido) ###

                                            # Se actualiza del contrato
                                            contrato_venta.save()

                                            # Se eliminan las variables de session
                                            del request.session['clientes_contrato']
                                            del request.session['pagos_entidades_contrato']
                                            del request.session['cuotas_efectivo_contrato']
                                            del request.session['adicionales_agrupacion_inmueble_contrato']
                                            return HttpResponseRedirect('/inverboy/home/detallescontratoventa/' + str(contrato_venta.id) + '/' + str(proyecto_id) + '/')
                                else:
                                    error = 'Debe seleccionar por lo menos un adicional.'
                        else:
                            return HttpResponseRedirect('/inverboy/home/')
                    else:
                        contrato_venta.calcular_valores()
                        clientes_contrato = []
                        for cliente_contrato in contrato_venta.clientecontratoventa_set.all():
                            clientes_contrato.append(cliente_contrato.cliente)
                        request.session['clientes_contrato'] = clientes_contrato
                        pagos_entidades_contrato = list(contrato_venta.pagoentidadcontratoventa_set.all())
                        cuotas_efectivo_contrato = list(contrato_venta.pagoefectivocontratoventa_set.all().order_by('fecha_desembolso'))
                        request.session['pagos_entidades_contrato'] = pagos_entidades_contrato
                        request.session['cuotas_efectivo_contrato'] = cuotas_efectivo_contrato
                        adicionales_agrupacion_inmueble_contrato = list(contrato_venta.adicionalagrupacioncontratoventa_set.all())
                        request.session['adicionales_agrupacion_inmueble_contrato'] = adicionales_agrupacion_inmueble_contrato
                        for adicional_agrupacion_contrato_venta in adicionales_agrupacion_inmueble_contrato:
                            valor_agrupacion_inmueble = round(valor_agrupacion_inmueble + adicional_agrupacion_contrato_venta.valor, 2)
                        request.session['forma_pago'] = contrato_venta.forma_pago
                        if contrato_venta.forma_pago == 1:
                            request.session['monto_credito'] = contrato_venta.monto_credito
                        valor_pagar_entidad_contrato = contrato_venta.str_valor_pagar_entidades_bancarias
                        valor_efectivo_pagar = contrato_venta.str_valor_pagar_efectivo
                        valor_pagar = contrato_venta.str_valor_pagar_cliente
                        if contrato_venta.estado_contrato_venta().estado_contrato == 1:
                            form = ContratoVentaForm(instance=contrato_venta, initial={'fecha_maxima_separacion': contrato_venta.estado_contrato_venta().fecha_limite_estado.strftime('%Y-%m-%d'), 'numero_cuotas': contrato_venta.str_numero_pagos_efectivo})
                        else:
                            form = ContratoVentaForm(instance=contrato_venta, initial={'numero_cuotas': contrato_venta.str_numero_pagos_efectivo})
                            form.fields.pop('fecha_maxima_separacion')
                    return render_to_response('ventas/modificarcontratoventa.html',{'user': user, 'form': form, 'contrato_venta': contrato_venta, 'agrupacion_inmueble': agrupacion_inmueble, 'adicionales_agrupacion_inmueble_contrato': adicionales_agrupacion_inmueble_contrato, 'valor_agrupacion_inmueble': valor_agrupacion_inmueble, 'clientes': clientes_contrato, 'pagos_entidades_contrato': pagos_entidades_contrato, 'valor_pagar_entidad_contrato': valor_pagar_entidad_contrato, 'cuotas_efectivo_contrato': cuotas_efectivo_contrato, 'valor_efectivo_pagar': valor_efectivo_pagar, 'valor_pagar': valor_pagar, 'error': error, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')

def imprimir_otro_si(request,contrato_venta_id,proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        if 'inverboy.change_contratoventa' in user.get_all_permissions():
            usuario = Usuario.objects.get(pk=user.pk)
            contrato_venta = ContratoVenta.objects.get(pk=int(contrato_venta_id))
            fecha_actual = datetime.datetime.today()
            imagen_cabecera = 'pdfs/rotulootrosi.jpg'
            otro_si = ModificacionContratoVenta.objects.filter(contrato_venta=contrato_venta).order_by('-fecha_registro')
            if otro_si:
                otro_si = otro_si[0]
                pagesize = 'letter'
                orientation = 'portrait'
                margin = '1cm'
                font_size = '11pt' 
                informacion_inmueble = '<strong> Tipo: </strong>'
                agrupacion_contrato_venta = contrato_venta.agrupacion_contrato_venta()
                for inmueble in agrupacion_contrato_venta.itemagrupacioninmueble_set.all():
                    informacion_inmueble += inmueble.inmueble.tipo_inmueble.nombre + ' No.' + inmueble.inmueble.identificacion
                    if inmueble == agrupacion_contrato_venta.inmueble_principal:
                        informacion_inmueble += '<strong> Area: </strong>' + str(inmueble.inmueble.area_construida) + ', '
                informacion_inmueble += u'<strong> Localización: </strong>' + contrato_venta.proyecto.direccion
                informacion_inmueble += '<strong> Acabados: </strong>'
                for acabado in contrato_venta.adicionalagrupacioncontratoventa_set.all():
                    informacion_inmueble += acabado.nombre + ' '
                contrato_venta.calcular_valores()
                contrato_venta.calcular_valores()
                datos_pagos = []
                cont = 0
                for cuota in contrato_venta.consolidado_pagos_efectivo():
                    datos_pagos.append([cuota.fecha_desembolso,cuota.valor,'cuota',cont])
                    cont+=1
                if datos_pagos:
                    datos_pagos[0][2]=u'Separación'
                mitad = int(math.floor(len(datos_pagos)/2))+1
                datos_pagos_1 = datos_pagos[:mitad]
                datos_pagos_2 = datos_pagos[mitad:]
                html = render_to_string('ventas/pdfs/pdfotrosi.html', locals(), context_instance=RequestContext(request))
                return generar_pdf(html, proyecto_id)
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')

def imprimir_hoja_negociacion(request,contrato_venta_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        imagen_fondo = os.path.dirname(os.path.realpath(__file__))+'/../../templates/ventas/pdfs/LOGO_IBL.png'
        contrato_venta= ContratoVenta.objects.get(pk=contrato_venta_id)
        hoy = datetime.datetime.today()
        pagesize = 'letter'
        orientation = 'portrait'
        margin = '0.5cm'
        font_size = '11pt' 
        contrato_venta.calcular_valores()
        datos_pagos = []
        cont = 0
        total_recursos_propios = 0
        for cuota in contrato_venta.consolidado_pagos_efectivo():
            datos_pagos.append([cuota.fecha_desembolso,cuota.valor,'cuota',cont])
            total_recursos_propios+=cuota.valor
            cont+=1
        if datos_pagos:
            datos_pagos[0][2]=u'Separación'
        otros_pagos = []
        for pago_entidad in contrato_venta.pagoentidadcontratoventa_set.all():
            otros_pagos.append([pago_entidad.str_tipo_cuenta(),pago_entidad.valor])
            total_recursos_propios+=pago_entidad.valor
        porcentaje_recursos_propios = (100.0/float(contrato_venta.agrupacion_contrato_venta().str_valor()))*total_recursos_propios
        porcentaje_banco = 100.0 - porcentaje_recursos_propios
        if porcentaje_banco < 0:
            porcentaje_banco=0
        porcentaje_recursos_propios = '%.2f'%porcentaje_recursos_propios
        porcentaje_banco = '%.2f' % porcentaje_banco
        html = render_to_string('ventas/pdfs/pdfhojanegociacion.html', locals(), context_instance=RequestContext(request))
        return generar_pdf(html, contrato_venta_id)
    return HttpResponseRedirect('/inverboy/home/')



def pdf_documento_apertura_fiducuenta(request, contrato_venta_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_contratoventa' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                contrato_venta = proyecto.lista_contratos().get(id=contrato_venta_id)
                if proyecto.apertura_fiducuenta:
                    fecha_actual = datetime.datetime.today()
                    texto = contrato_venta.str_documento_apertura_fiducuenta(usuario=usuario)
                    html = render_to_string('ventas/pdfs/pdfdocumentoventa.html', {'pagesize': 'letter', 'orientation': 'portrait', 'margin': '1cm', 'font_size': '11pt', 'contrato_venta': contrato_venta, 'texto': texto, 'proyecto': proyecto}, context_instance=RequestContext(request))
                    return generar_pdf(html, proyecto_id)
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def pdf_documento_carta_instrucciones(request, contrato_venta_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_contratoventa' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                contrato_venta = proyecto.lista_contratos().get(id=contrato_venta_id)
                if proyecto.apertura_fiducuenta:
                    fecha_actual = datetime.datetime.today()
                    contrato_venta.calcular_valores()
                    texto = contrato_venta.str_documento_carta_instrucciones()
                    imagen_cabecera = 'pdfs/rotulocartainstrucciones.jpg'
                    html = render_to_string('ventas/pdfs/pdfdocumentoventacartainstrucciones.html', {'pagesize': 'letter', 'orientation': 'portrait', 'margin': '1cm', 'imagen_cabecera': imagen_cabecera, 'font_size': '11pt', 'fecha_actual': fecha_actual, 'contrato_venta': contrato_venta, 'texto': texto, 'proyecto': proyecto}, context_instance=RequestContext(request))
                    return generar_pdf(html, proyecto_id)
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def pdf_documento_promesa_compraventa(request, contrato_venta_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_contratoventa' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                if proyecto.promesa_compraventa:
                    contrato_venta = proyecto.lista_contratos().get(id=contrato_venta_id)
                    if contrato_venta.permite_imprimir_promesa_compraventa():
                        # Actualiza el estado del contrato
                        if contrato_venta.estado_contrato_venta().estado_contrato == 2:
                            estado_contrato_venta = contrato_venta.estado_contrato_venta()
                            estado_contrato_venta.estado_registro = False
                            estado_contrato_venta.save()
                            estado_contrato_venta, registro_creado = contrato_venta.estadocontratoventa_set.get_or_create(estado_contrato=3)
                            if not registro_creado:
                                estado_contrato_venta.estado_registro = True
                                estado_contrato_venta.save()

                        contrato_venta.permiso_imprimir_promesa_compraventa = False
                        contrato_venta.save()
                        
                        fecha_actual = datetime.datetime.today()
                        contrato_venta.calcular_valores()
                        texto = contrato_venta.str_documento_promesa_compraventa()
                        imagen_cabecera = 'pdfs/rotulopromesacompraventa.jpg'
                        html = render_to_string('ventas/pdfs/pdfdocumentoventapromesa.html', {'pagesize': 'letter', 'orientation': 'portrait', 'margin': '1cm', 'imagen_cabecera': imagen_cabecera, 'font_size': '11pt', 'fecha_actual': fecha_actual, 'contrato_venta': contrato_venta, 'texto': texto, 'proyecto': proyecto}, context_instance=RequestContext(request))
                        return generar_pdf(html, proyecto_id)
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')

#Principal reportes ventas
def principal_reportes_ventas(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_documentoventa' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
                return render_to_response('ventas/principalreportesventas.html', {'user': user, 'proyecto': proyecto})
    return HttpResponseRedirect('/inverboy/home/')

#Principal reportes ventas
def principal_reportes_ventas(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        clientes = Cliente.objects.all()
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_documentoventa' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                form = ReporteVentasForm()
                if request.method == 'POST':
                    print 'dasss'
                    form = ReporteVentasForm(request.POST)
                    if form.is_valid():
                        reporte_ventas_opciones = form.cleaned_data['reporte_ventas_opciones']
                        print reporte_ventas_opciones
                        return render_to_response('ventas/reporteventas.html', {'user': user, 'proyecto': proyecto, 'form': form, 'reporte_ventas_opciones': reporte_ventas_opciones, 'clientes': clientes})
                return render_to_response('ventas/principalreportesventas.html', {'user': user, 'proyecto': proyecto, 'form': form})
    return HttpResponseRedirect('/inverboy/home/')
