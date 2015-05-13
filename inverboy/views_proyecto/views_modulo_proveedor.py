# -*- encoding: utf-8 -*-
from views_modulo_usuario import *
from funciones_views import *
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission
from inverboy.models import *
from inverboy.forms import *
from datetime import *
## PAGINACION
from inverboy.paginator import *
## MANEJO DE ERRORES MANUALMENTE
from django.forms.util import ErrorList
## CONSULTAS ANIDADAS
from django.db.models import Q
from settings import TIEMPO_INACTIVIDAD
## OMITIR ACENTOS
from unicodedata import lookup, name
# MENSAJES
from django.contrib import messages
# FUNCION MAX
from django.db.models import Max


#Nuevo proveedor
def proveedor_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_proveedor' in user.get_all_permissions():
            form1 = ProveedorForm()
            form2 = ContactoForm()
            departamentos = Departamento.objects.all()
            lista_municipios = []
            departamento_actual = Departamento()
            municipio_actual = Municipio()
            contactos = []
            if request.method == 'POST':
                contactos = None
                try:
                    contactos = request.session['lista_contactos']
                except :
                    pass
                if contactos != None:
                    if request.POST['departamento'] != '0':
                        departamento_actual = Departamento.objects.get(id=request.POST['departamento'])
                        municipios = Municipio.objects.filter(departamento=departamento_actual)
                        try:
                            if request.POST['municipio'] != '0':
                                municipio_actual = Municipio.objects.get(id=request.POST['municipio'])
                        except :
                            pass
                        item_nulo = Municipio()
                        item_nulo.id = 0
                        item_nulo.nombre = '---'
                        lista_municipios.append(item_nulo)
                        for municipio in municipios:
                            lista_municipios.append(municipio)
                    form1 = ProveedorForm(request.POST)
                    if len(contactos) == 0:
                        error = 'Debe ingresar por lo menos un contacto'
                        return render_to_response('proveedor.html',{'user': user, 'form1': form1, 'form2': form2, 'departamentos': departamentos, 'municipios': lista_municipios, 'departamento_actual': departamento_actual, 'municipio_actual': municipio_actual, 'error': error})
                    if form1.is_valid():
                        proveedor = Proveedor()
                        proveedor.identificacion = form1.cleaned_data['identificacion']
                        try:
                            proveedor.validate_unique()
                        except:
                            form1._errors["identificacion"] = ErrorList([u"La identificacion ya existe en el sistema."])
                        proveedor.razon_social = form1.cleaned_data['razon_social'].strip()
                        proveedor.nombre_comercial = form1.cleaned_data['nombre_comercial'].strip()
                        proveedor.direccion = form1.cleaned_data['direccion'].strip()
                        proveedor.tipo = form1.cleaned_data['tipo']
                        proveedor.regimen_tributario = form1.cleaned_data['regimen_tributario']
                        proveedor.telefono_1 = form1.cleaned_data['telefono_1'].strip()
                        proveedor.telefono_2 = form1.cleaned_data['telefono_2'].strip()
                        proveedor.fax = form1.cleaned_data['fax']
                        proveedor.web_site = form1.cleaned_data['web_site'].strip()
                        proveedor.email = form1.cleaned_data['email'].strip()
                        proveedor.estado_proveedor = True
                        proveedor.observaciones = form1.cleaned_data['observaciones'].strip()
                        proveedor.municipio = form1.cleaned_data['municipio']
                        try:
                            proveedor.validate_unique()
                            proveedor.save()
                            for contacto in contactos:
                                contacto.proveedor = proveedor
                                contacto.save()
                            del request.session['lista_contactos']
                            usuario_actual = Usuario.objects.get(id=user.id)
                            direccion_ip = request.META['REMOTE_ADDR']
                            registro_historial(direccion_ip, usuario_actual, "Registro nuevo proveedor, identificacion: " + str(proveedor.identificacion))
                            return HttpResponseRedirect('/inverboy/home/proveedoressearch/')
                        except:
                            pass
                else:
                    return HttpResponseRedirect('/inverboy/home/')
            request.session['lista_contactos'] = contactos
            return render_to_response('proveedor.html',{'user': user, 'form1': form1, 'form2': form2, 'departamentos': departamentos, 'municipios': lista_municipios, 'departamento_actual': departamento_actual, 'municipio_actual': municipio_actual, 'contactos': contactos})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar proveedor
def proveedor_change(request, proveedor_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_proveedor' in user.get_all_permissions():
            proveedor = Proveedor.objects.get(id=proveedor_id)
            form1 = ProveedorForm(initial={'identificacion': proveedor.identificacion, 'razon_social': proveedor.razon_social, 'nombre_comercial': proveedor.nombre_comercial, 'direccion': proveedor.direccion, 'tipo': proveedor.tipo, 'regimen_tributario': proveedor.regimen_tributario, 'telefono_1': proveedor.telefono_1, 'telefono_2': proveedor.telefono_2, 'fax': proveedor.fax, 'web_site': proveedor.web_site, 'email': proveedor.email, 'observaciones': proveedor.observaciones, 'estado': proveedor.estado_proveedor})
            form2 = ContactoForm()
            departamentos = Departamento.objects.all()
            lista_municipios = []
            municipio_actual = proveedor.municipio
            departamento_actual = municipio_actual.departamento
            contactos = Contacto.objects.filter(proveedor=proveedor)
            lista_contactos = []
            for contacto in contactos:
                lista_contactos.append(contacto)
            municipios = Municipio.objects.filter(departamento = municipio_actual.departamento)
            item_nulo = Municipio()
            item_nulo.id = 0
            item_nulo.nombre = '---'
            lista_municipios.append(item_nulo)
            for municipio in municipios:
                lista_municipios.append(municipio)
            if request.method == 'POST':
                lista_contactos = None
                try:
                    lista_contactos = request.session['lista_contactos']
                except :
                    pass
                if lista_contactos != None:
                    departamento_actual = Departamento()
                    municipio_actual = Municipio()
                    if request.POST['departamento'] != '0':
                        departamento_actual = Departamento.objects.get(id=request.POST['departamento'])
                        municipios = Municipio.objects.filter(departamento=departamento_actual)
                        lista_municipios = []
                        if request.POST['municipio'] != '0':
                            municipio_actual = Municipio.objects.get(id=request.POST['municipio'])
                        lista_municipios.append(item_nulo)
                        for municipio in municipios:
                            lista_municipios.append(municipio)
                    form1 = ProveedorForm(request.POST)
                    if len(lista_contactos) == 0:
                        error = 'Debe ingresar por lo menos un contacto'
                        return render_to_response('proveedor.html',{'user': user, 'form1': form1, 'form2': form2, 'departamentos': departamentos, 'municipios': lista_municipios, 'departamento_actual': departamento_actual, 'municipio_actual': municipio_actual, 'error': error, 'change': True})
                    if form1.is_valid():
                        if proveedor.identificacion != form1.cleaned_data['identificacion']:
                            proveedor.identificacion = form1.cleaned_data['identificacion']
                            try:
                                proveedor.validate_unique()
                            except:
                                form1._errors["identificacion"] = ErrorList([u"La identificación ya existe en el sistema."])
                        proveedor.razon_social = form1.cleaned_data['razon_social'].strip()
                        proveedor.nombre_comercial = form1.cleaned_data['nombre_comercial'].strip()
                        proveedor.direccion = form1.cleaned_data['direccion'].strip()
                        proveedor.tipo = form1.cleaned_data['tipo']
                        proveedor.regimen_tributario = form1.cleaned_data['regimen_tributario']
                        proveedor.telefono_1 = form1.cleaned_data['telefono_1'].strip()
                        proveedor.telefono_2 = form1.cleaned_data['telefono_2'].strip()
                        proveedor.fax = form1.cleaned_data['fax']
                        proveedor.web_site = form1.cleaned_data['web_site'].strip()
                        proveedor.email = form1.cleaned_data['email'].strip()
                        proveedor.estado_proveedor = form1.cleaned_data['estado']
                        proveedor.observaciones = form1.cleaned_data['observaciones'].strip()
                        proveedor.municipio = form1.cleaned_data['municipio']
                        try:
                            proveedor.validate_unique()
                            proveedor.save()
                            Contacto.objects.filter(proveedor=proveedor).delete()
                            for contacto in lista_contactos:
                                contacto.proveedor = proveedor
                                contacto.save()
                            del request.session['lista_contactos']
                            usuario_actual = Usuario.objects.get(id=user.id)
                            direccion_ip = request.META['REMOTE_ADDR']
                            registro_historial(direccion_ip, usuario_actual, "Modifico proveedor, identificacion: "+str(proveedor.identificacion))
                            return HttpResponseRedirect('/inverboy/home/proveedoressearch/')
                        except:
                            print 'error en campos unicos de proveedor'
                else:
                    return HttpResponseRedirect('/inverboy/home/')
            request.session['lista_contactos'] = lista_contactos
            return render_to_response('proveedor.html', {'user': user, 'form1': form1, 'form2': form2, 'contactos': lista_contactos, 'departamentos': departamentos, 'municipios': lista_municipios, 'departamento_actual': departamento_actual, 'municipio_actual':municipio_actual, 'change': True})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#BUSQUEDA PROVEEDORES
def proveedores_search(request):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_proveedor' in user.get_all_permissions():
            criterio = ''
            proveedores = Proveedor.objects.all()
            if request.method == 'POST':
                criterio = request.POST['criterio'].strip()
                try:
                    criterio = int(criterio)
                    proveedores = proveedores.filter(identificacion=criterio)
                except:
                    proveedores = proveedores.filter(Q(razon_social__icontains=criterio) | Q(nombre_comercial__icontains=criterio))
            pag = Paginador(request, proveedores, 20, 1)
            return render_to_response('reporteproveedores.html', {'user': user, 'proveedores': pag, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')
