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
## OMITIR ACENTOS
from unicodedata import lookup, name
# MENSAJES
from django.contrib import messages
# FUNCION MAX
from django.db.models import Max
#VALIDACIONES
from inverboy.validaciones.validaciones import *

#---------------------------------CLASIFICACION DE SUMINISTROS------------------------------------------------------------------------

#Crear categoria suministro
def categoria_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_categoria' in user.get_all_permissions():
            form = CategoriaForm()
            if request.method == 'POST':
                form = CategoriaForm(request.POST)
                if form.is_valid():
                    categoria_existente = None
                    nombre = form.cleaned_data['nombre'].strip()
                    try:
                        categoria_existente = Categoria.objects.get(nombre=nombre, tipo=1)
                    except :
                        pass
                    if categoria_existente == None:
                        categoria = Categoria()
                        categoria.nombre = nombre
                        categoria.tipo = 1
                        categoria.estado = 1
                        categoria.save()
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, u"Registro nueva categoria suministros, nombre: "+ unicode(categoria.nombre))
                        return HttpResponseRedirect('/inverboy/home/categoriassearch/')
                    else:
                        msg = u"La categoria ya existe en el sistema."
                        form._errors["nombre"] = form.error_class([msg])
            return render_to_response('categoriaadd.html', {'user': user, 'form': form})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Reporte categorias de suministro
def categorias_search(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_categoria' in user.get_all_permissions():
            criterio = ''
            categorias = Categoria.objects.filter(tipo=1)
            if request.method == 'POST':
                criterio = request.POST['criterio'].strip()
                categorias = categorias.filter(Q(nombre__icontains=criterio))
            pag = Paginador(request, categorias, 20, 1)
            return render_to_response('reportecategorias.html', {'user': user, 'categorias': pag, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar categoria de suministro
def categoria_change(request, categoria_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_categoria' in user.get_all_permissions():
            categoria = Categoria.objects.get(id=categoria_id)
            form = CategoriaForm(initial={'nombre': categoria.nombre, 'estado': categoria.estado})
            if request.method == 'POST':
                form = CategoriaForm(request.POST)
                if form.is_valid():
                    categoria_existente = None
                    nombre = form.cleaned_data['nombre'].strip()
                    if normaliza(categoria.nombre.lower()) != normaliza(nombre.lower()):
                        try:
                            categoria_existente = Categoria.objects.get(nombre=nombre, tipo=1)
                        except :
                            pass
                    if categoria_existente == None:
                        categoria.nombre = nombre
                        categoria.estado = form.cleaned_data['estado']
                        categoria.save()
                        especificaciones = Categoria.objects.filter(tipo=2, categoria_asociada=categoria)
                        especificaciones.update(estado=categoria.estado)
                        for especificacion in especificaciones:
                            Suministro.objects.filter(categoria=especificacion).update(estado_suministro=categoria.estado)
                            tipos = Categoria.objects.filter(tipo=3, categoria_asociada=especificacion)
                            tipos.update(estado=categoria.estado)
                            for tipo in tipos:
                                Suministro.objects.filter(categoria=tipo).update(estado_suministro=categoria.estado)
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, u"Modifico categoria suministros, nombre: "+ unicode(categoria.nombre))
                        return HttpResponseRedirect('/inverboy/home/categoriassearch/')
                    else:
                        msg = u"La categoria ya existe en el sistema."
                        form._errors["nombre"] = form.error_class([msg])
            return render_to_response('categoriaadd.html', {'user': user, 'form': form, 'change': True})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Crear especificación de suministro
def especificacion_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_categoria' in user.get_all_permissions():
            form = EspecificacionForm()
            if request.method == 'POST':
                form = EspecificacionForm(request.POST)
                if form.is_valid():
                    especificacion_existente = None
                    categoria = form.cleaned_data['categoria_asociada']
                    nombre = form.cleaned_data['nombre'].strip()
                    try:
                        especificacion_existente = Categoria.objects.get(categoria_asociada=categoria, nombre=nombre, tipo=2)
                    except:
                        pass
                    if especificacion_existente == None:
                        especificacion = Categoria()
                        especificacion.nombre = nombre
                        especificacion.tipo = 2
                        especificacion.estado = 1
                        especificacion.categoria_asociada = categoria
                        especificacion.save()
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, u"Registro nueva especificacion suministros, nombre: "+ unicode(especificacion.nombre)+u", en la categoria: "+ unicode(especificacion.categoria_asociada.nombre))
                        return HttpResponseRedirect('/inverboy/home/especificacionessearch/'+str(especificacion.categoria_asociada_id)+'/')
                    else:
                        msg = u"La especificación ya existe en el sistema."
                        form._errors["nombre"] = form.error_class([msg])
            return render_to_response('especificacionadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Crear especificación de suministro
def especificacion_add_categoria(request, categoria_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_categoria' in user.get_all_permissions():
            form = EspecificacionForm(initial={'categoria_asociada': categoria_id})
            if request.method == 'POST':
                form = EspecificacionForm(request.POST)
                if form.is_valid():
                    especificacion_existente = None
                    categoria = form.cleaned_data['categoria_asociada']
                    nombre = form.cleaned_data['nombre'].strip()
                    try:
                        especificacion_existente = Categoria.objects.get(categoria_asociada=categoria, nombre=nombre, tipo=2)
                    except:
                        pass
                    if especificacion_existente == None:
                        especificacion = Categoria()
                        especificacion.nombre = nombre
                        especificacion.tipo = 2
                        especificacion.estado = 1
                        especificacion.categoria_asociada = categoria
                        especificacion.save()
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, u"Registro nueva especificacion suministros, nombre: "+ unicode(especificacion.nombre)+u", en la categoria: "+ unicode(especificacion.categoria_asociada.nombre))
                        return HttpResponseRedirect('/inverboy/home/especificacionessearch/'+str(especificacion.categoria_asociada_id)+'/')
                    else:
                        msg = u"La especificacion ya existe en el sistema."
                        form._errors["nombre"] = form.error_class([msg])
            return render_to_response('especificacionadd.html', {'user': user, 'form': form})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Busqueda especificaciones de suministro
def especificaciones_search(request, categoria_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_categoria' in user.get_all_permissions():
            criterio = ''
            categoria = Categoria.objects.get(id=categoria_id, tipo=1)
            especificaciones = Categoria.objects.filter(tipo=2, categoria_asociada=categoria)
            if request.method == 'POST':
                criterio = request.POST['criterio'].strip()
                especificaciones = especificaciones.filter(Q(nombre__icontains=criterio))
            pag = Paginador(request, especificaciones, 20, 1)
            return render_to_response('reporteespecificaciones.html', {'user': user, 'especificaciones': pag, 'categoria': categoria, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar especificación de suministro
def especificacion_change(request, especificacion_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_categoria' in user.get_all_permissions():
            especificacion = Categoria.objects.get(id=especificacion_id)
            form = EspecificacionForm(initial={'categoria_asociada': especificacion.categoria_asociada, 'nombre': especificacion.nombre, 'estado': especificacion.estado})
            if request.method == 'POST':
                form = EspecificacionForm(request.POST)
                if form.is_valid():
                    especificacion_existente = None
                    categoria = form.cleaned_data['categoria_asociada']
                    nombre = form.cleaned_data['nombre'].strip()
                    if normaliza(especificacion.nombre.lower()) != normaliza(nombre.lower()) or especificacion.categoria_asociada != categoria:
                        try:
                            especificacion_existente = Categoria.objects.get(categoria_asociada=categoria, nombre=nombre, tipo=2)
                        except:
                            pass
                    if especificacion_existente == None:
                        especificacion.nombre = nombre
                        especificacion.estado = form.cleaned_data['estado']
                        especificacion.categoria_asociada = categoria
                        especificacion.save()
                        Suministro.objects.filter(categoria=especificacion).update(estado_suministro=especificacion.estado)
                        tipos = Categoria.objects.filter(tipo=3, categoria_asociada=especificacion)
                        tipos.update(estado=especificacion.estado)
                        for tipo in tipos:
                            Suministro.objects.filter(categoria=tipo).update(estado_suministro=especificacion.estado)
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, u"Modifico especificacion suministros, nombre: "+ unicode(especificacion.nombre)+u", en la categoria: "+ unicode(especificacion.categoria_asociada.nombre))
                        return HttpResponseRedirect('/inverboy/home/especificacionessearch/'+str(especificacion.categoria_asociada_id)+'/')
                    else:
                        msg = u"La especificacion ya existe en el sistema."
                        form._errors["nombre"] = form.error_class([msg])
            return render_to_response('especificacionadd.html', {'user': user, 'form': form, 'change': True})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Crear tipo de suministro
def tipo_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_categoria' in user.get_all_permissions():
            categorias = Categoria.objects.filter(tipo=1, estado=True)
            lista_categorias = []
            lista_especificaciones = []
            item_nulo = Categoria()
            item_nulo.id = 0
            item_nulo.nombre = '----'
            lista_categorias.append(item_nulo)
            for categoria in categorias:
                lista_categorias.append(categoria)
            categoria_actual = Categoria()
            especificacion_actual = Categoria()
            form = TipoForm()
            if request.method == 'POST':
                form = TipoForm(request.POST)
                if request.POST['categoria'] != '0':
                    categoria_actual = Categoria.objects.get(id=request.POST['categoria'], tipo=1)
                    especificaciones = Categoria.objects.filter(tipo=2, estado=True, categoria_asociada=categoria_actual)
                    lista_especificaciones.append(item_nulo)
                    for especificacion in especificaciones:
                        lista_especificaciones.append(especificacion)
                    if request.POST['especificacion'] != '0':
                        especificacion_actual = Categoria.objects.get(id=request.POST['especificacion'], tipo=2)
                if form.is_valid():
                    tipo = Categoria()
                    tipo.nombre = form.cleaned_data['nombre'].strip()
                    tipo.tipo = 3
                    tipo.estado = 1
                    tipo.categoria_asociada = especificacion_actual
                    tipo.save()
                    usuario_actual = Usuario.objects.get(id=user.id)
                    direccion_ip = request.META['REMOTE_ADDR']
                    registro_historial(direccion_ip, usuario_actual, u"Registro nuevo tipo suministros, nombre: "+ unicode(tipo.nombre)+u", en la categoria: "+ unicode(tipo.categoria_asociada.categoria_asociada.nombre)+u", en la especificacion: "+ unicode(tipo.categoria_asociada.nombre))
                    return HttpResponseRedirect('/inverboy/home/tipossearch/'+str(especificacion_actual.id)+'/')
            return render_to_response('tipoadd.html', {'user': user, 'form': form, 'categorias': lista_categorias, 'especificaciones': lista_especificaciones, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Crear tipo de suministro
def tipo_add_especificacion(request, especificacion_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_categoria' in user.get_all_permissions():
            especificacion_actual = Categoria.objects.get(id=especificacion_id, tipo=2)
            categoria_actual = especificacion_actual.categoria_asociada
            categorias = Categoria.objects.filter(tipo=1, estado=True)
            especificaciones = Categoria.objects.filter(categoria_asociada=especificacion_actual.categoria_asociada, tipo=2, estado=True)
            lista_categorias = []
            lista_especificaciones = []
            item_nulo = Categoria()
            item_nulo.id = 0
            item_nulo.nombre = '----'
            lista_categorias.append(item_nulo)
            for categoria in categorias:
                lista_categorias.append(categoria)
            lista_especificaciones.append(item_nulo)
            for especificacion in especificaciones:
                lista_especificaciones.append(especificacion)
            form = TipoForm()
            if request.method == 'POST':
                form = TipoForm(request.POST)
                categoria_actual = Categoria()
                especificacion_actual = Categoria()
                lista_especificaciones = []
                if request.POST['categoria'] != '0':
                    categoria_actual = Categoria.objects.get(id=request.POST['categoria'], tipo=1)
                    especificaciones = Categoria.objects.filter(tipo=2, estado=True, categoria_asociada=categoria_actual)
                    lista_especificaciones = []
                    lista_especificaciones.append(item_nulo)
                    for especificacion in especificaciones:
                        lista_especificaciones.append(especificacion)
                    if request.POST['especificacion'] != '0':
                        especificacion_actual = Categoria.objects.get(id=request.POST['especificacion'], tipo=2)
                if form.is_valid():
                    tipo_existente = None
                    try:
                        nombre = form.cleaned_data['nombre'].strip()
                        tipo_existente = Categoria.objects.get(categoria_asociada=especificacion_actual, nombre=nombre, tipo=3)
                    except:
                        pass
                    if tipo_existente == None:
                        tipo = Categoria()
                        tipo.nombre = nombre
                        tipo.tipo = 3
                        tipo.estado = 1
                        tipo.categoria_asociada = especificacion_actual
                        tipo.save()
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, u"Registro nuevo tipo suministros, nombre: "+ unicode(tipo.nombre)+u", en la categoria: "+ unicode(tipo.categoria_asociada.categoria_asociada.nombre)+u", en la especificacion: "+ unicode(tipo.categoria_asociada.nombre))
                        return HttpResponseRedirect('/inverboy/home/tipossearch/'+str(especificacion_actual.id)+'/')
                    else:
                        msg = u"El tipo ya existe en el sistema."
                        form._errors["nombre"] = form.error_class([msg])
            return render_to_response('tipoadd.html', {'user': user, 'form': form, 'categorias': lista_categorias, 'especificaciones': lista_especificaciones, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar tipo suministro
def tipo_change(request, tipo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_categoria' in user.get_all_permissions():
            tipo = Categoria.objects.get(id=tipo_id)
            especificacion_actual = tipo.categoria_asociada
            categoria_actual = especificacion_actual.categoria_asociada
            categorias = Categoria.objects.filter(tipo=1, estado=True)
            especificaciones = Categoria.objects.filter(tipo=2, estado=True, categoria_asociada=categoria_actual)
            lista_especificaciones = []
            item_nulo = Categoria()
            item_nulo.id = 0
            item_nulo.nombre = '----'
            lista_especificaciones.append(item_nulo)
            for especificacion in especificaciones:
                lista_especificaciones.append(especificacion)
            form = TipoForm(initial={'nombre': tipo.nombre, 'estado': tipo.estado})
            if request.method == 'POST':
                form = TipoForm(request.POST)
                categoria_actual = Categoria()
                especificacion_actual = Categoria()
                lista_especificaciones = []
                if request.POST['categoria'] != '0':
                    categoria_actual = Categoria.objects.get(id=request.POST['categoria'], tipo=1)
                    especificaciones = Categoria.objects.filter(tipo=2, estado=True, categoria_asociada=categoria_actual)
                    lista_especificaciones = []
                    lista_especificaciones.append(item_nulo)
                    for especificacion in especificaciones:
                        lista_especificaciones.append(especificacion)
                    if request.POST['especificacion'] != '0':
                        especificacion_actual = Categoria.objects.get(id=request.POST['especificacion'], tipo=2)
                if form.is_valid():
                    tipo_existente = None
                    nombre = form.cleaned_data['nombre'].strip()
                    if normaliza(tipo.nombre.lower()) != normaliza(nombre.lower()) or tipo.categoria_asociada != especificacion_actual:
                        try:
                            tipo_existente = Categoria.objects.get(categoria_asociada=especificacion_actual, nombre=nombre, tipo=3)
                        except:
                            pass
                    if tipo_existente == None:
                        tipo.nombre = nombre
                        tipo.tipo = 3
                        tipo.estado = form.cleaned_data['estado']
                        tipo.categoria_asociada = especificacion_actual
                        tipo.save()
                        Suministro.objects.filter(categoria=tipo).update(estado_suministro=tipo.estado)
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, u"Modifico tipo suministros, nombre: "+ unicode(tipo.nombre)+ unicode(tipo.nombre)+u", en la categoria: "+ unicode(tipo.categoria_asociada.categoria_asociada.nombre)+u", en la especificacion: "+ unicode(tipo.categoria_asociada.nombre))
                        return HttpResponseRedirect('/inverboy/home/tipossearch/'+str(especificacion_actual.id)+'/')
            return render_to_response('tipoadd.html', {'user': user, 'form': form, 'categorias': categorias, 'especificaciones': lista_especificaciones, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'change': True})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Busqueda tipo suministro
def tipos_search(request, especificacion_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_categoria' in user.get_all_permissions():
            criterio = ''
            especificacion = Categoria.objects.get(id=especificacion_id, tipo=2)
            categoria = especificacion.categoria_asociada
            tipos = Categoria.objects.filter(tipo=3, categoria_asociada=especificacion)
            if request.method == 'POST':
                criterio = request.POST['criterio'].strip()
                tipos = tipos.filter(Q(nombre__icontains=criterio))
            pag = Paginador(request, tipos, 20, 1)
            return render_to_response('reportetipos.html', {'user': user, 'tipos': pag, 'categoria': categoria, 'especificacion': especificacion, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#--------------------------------------------SUMINISTROS-------------------------------------------------------------------------

#Crear suministro
def suministro_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_suministro' in user.get_all_permissions():
            categorias = Categoria.objects.filter(tipo=1, estado=1)
            lista_categorias = []
            lista_especificaciones = []
            lista_tipos = []
            categoria_actual = Categoria()
            especificacion_actual = Categoria()
            tipo_actual = Categoria()
            item_nulo = Categoria()
            item_nulo.id = 0
            item_nulo.nombre = '----'
            lista_categorias.append(item_nulo)
            for categoria in categorias:
                lista_categorias.append(categoria)
            form = SuministroForm()
            error = ''
            if request.method == 'POST':
                proveedores = None
                try:
                    proveedores = request.session['proveedores']
                except :
                    pass
                if proveedores != None:
                    form = SuministroForm(request.POST)
                    suministros_existentes = []
                    try:
                        if request.POST['categoria'] != '0':
                            categoria_actual = Categoria.objects.get(id=request.POST['categoria'], tipo=1)
                            especificaciones = Categoria.objects.filter(categoria_asociada=categoria_actual, estado=1)
                            if request.POST['especificacion'] != '0':
                                especificacion_actual = Categoria.objects.get(id=request.POST['especificacion'], tipo=2)
                                categoria_suministro = especificacion_actual
                                tipos = Categoria.objects.filter(categoria_asociada=especificacion_actual, tipo=3, estado=1)
                                suministros_existentes = Suministro.objects.filter(categoria=especificacion_actual)
                                if request.POST['tipo'] != '0':
                                    tipo_actual = Categoria.objects.get(id=request.POST['tipo'], tipo=3)
                                    categoria_suministro = tipo_actual
                                    suministros_existentes = Suministro.objects.filter(categoria=tipo_actual)
                                lista_tipos = []
                                lista_tipos.append(item_nulo)
                                for tipo in tipos:
                                    lista_tipos.append(tipo)
                            lista_especificaciones.append(item_nulo)
                            for especificacion in especificaciones:
                                lista_especificaciones.append(especificacion)
                    except :
                        pass
                    pag = Paginador(request, proveedores, 20, 1)
                    if len(proveedores) == 0:
                        error = 'Debe ingresar por lo menos un proveedor'
                        return render_to_response ('suministroadd.html',{'user': user, 'form':form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': pag, 'error': error} )
                    if form.is_valid():
                        nombre_nuevo_suministro = form.cleaned_data['nombre'].strip()
                        nombre_nuevo_suministro = normaliza(nombre_nuevo_suministro.lower())
                        for suministro_existente in suministros_existentes:
                            if normaliza(suministro_existente.nombre.lower()) == nombre_nuevo_suministro:
                                form._errors["nombre"] = ErrorList([u"El nombre del suministro ya existe en el sistema."])
                                return render_to_response ('suministroadd.html',{'user': user, 'form': form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': pag } )
                            sinonimos_suministro_existente = suministro_existente.sinonimos
                            sinonimos_suministro_existente = sinonimos_suministro_existente.split(',')
                            for sinonimo_suministro_existente in sinonimos_suministro_existente:
                                if normaliza(sinonimo_suministro_existente.lower().strip()) == nombre_nuevo_suministro:
                                    form._errors["nombre"] = ErrorList([u"El nombre del suministro ya existe en algunos suministros registrados en el sistema."])
                                    return render_to_response ('suministroadd.html',{'user': user, 'form': form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': pag } )
                        suministro = Suministro()
                        suministro.clasificacion_general = form.cleaned_data['clasificacion_general']
                        suministro.nombre = form.cleaned_data['nombre'].strip()
                        suministro.sinonimos = form.cleaned_data['sinonimos'].strip()
                        suministro.representativo = form.cleaned_data['representativo']
                        if form.cleaned_data['clasificacion_general'] == 'Material':
                            suministro.unidad_embalaje = form.cleaned_data['unidad_embalaje']
                        suministro.unidad_medida = form.cleaned_data['unidad_medida']
                        suministro.dias_compra = form.cleaned_data['dias_compra']
                        suministro.requiere_cartilla = form.cleaned_data['requiere_cartilla']
                        #suministro.promedio_precio_suministro = 0
                        suministro.peso = form.cleaned_data['peso']
                        suministro.largo = form.cleaned_data['largo']
                        suministro.alto = form.cleaned_data['alto']
                        suministro.ancho = form.cleaned_data['ancho']
                        #fecha = str(datetime.today().year) + '-' + str(datetime.today().month) + '-' + str(datetime.today().day)
                        #suministro.fecha_creacion = fecha
                        #suministro.fecha_actualizacion = fecha
                        suministro.estado_suministro = 1
                        usuario = Usuario.objects.get(id=user.id)
                        suministro.usuario = usuario
                        suministro.categoria = categoria_suministro
                        max_codigo = suministros_existentes.aggregate(Max('codigo'))
                        codigo_suministro = 1
                        if max_codigo['codigo__max'] is not None:
                            codigo_suministro = int(max_codigo['codigo__max'])+1
                        suministro.codigo = codigo_suministro
                        #try:
                        suministro.validate_unique()
                        suministro.save()
                        for proveedor in proveedores:
                            suministro_proveedor = SuministroProveedor()
                            suministro_proveedor.suministro = suministro
                            suministro_proveedor.proveedor = proveedor['proveedor']
                            suministro_proveedor.precio_suministro = proveedor['precio']
                            suministro_proveedor.iva_suministro = proveedor['iva']
                            suministro_proveedor.save()
                        del request.session['proveedores']
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, u"Registro nuevo suministro, nombre: "+ unicode(suministro.nombre))
                        return HttpResponseRedirect('/inverboy/home/suministrossearch/')
                        #except:
                        #    print 'error en campos unicos de suministro'
                else:
                    return HttpResponseRedirect('/inverboy/home/')
            else:
                request.session['proveedores'] = []
                pag = []
            request.session['proveedores_agregar'] = []
            return render_to_response ('suministroadd.html',{'user': user, 'form':form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': pag, 'error': error } )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar suministro
def suministro_change(request, suministro_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_suministro' in user.get_all_permissions():
            suministro = Suministro.objects.get(id=suministro_id)
            categoria_suministro = suministro.categoria
            categorias = Categoria.objects.filter(tipo=1, estado=1)
            especificaciones = []
            tipos = []
            especificacion_actual = Categoria()
            tipo_actual = Categoria()
            lista_categorias = []
            lista_especificaciones = []
            lista_tipos = []
            proveedores_suministro = SuministroProveedor.objects.filter(suministro=suministro)
            proveedores = []
            for proveedor_suministro in proveedores_suministro:
                proveedores.append({'proveedor': proveedor_suministro.proveedor, 'precio': proveedor_suministro.precio_suministro, 'iva': proveedor_suministro.iva_suministro })
            pag = Paginador(request, proveedores, 20, 1)
            if categoria_suministro.tipo == 2:
                especificacion_actual = categoria_suministro
                especificaciones = Categoria.objects.filter(categoria_asociada=especificacion_actual.categoria_asociada, tipo=2, estado=1)
                tipos = Categoria.objects.filter(categoria_asociada=especificacion_actual, tipo=3, estado=1)
            elif categoria_suministro.tipo == 3:
                tipo_actual = categoria_suministro
                especificacion_actual = tipo_actual.categoria_asociada
                tipos = Categoria.objects.filter(categoria_asociada=especificacion_actual, tipo=3, estado=1)
                especificaciones = Categoria.objects.filter(categoria_asociada=especificacion_actual.categoria_asociada, tipo=2, estado=1)
            categoria_actual = especificacion_actual.categoria_asociada
            item_nulo = Categoria()
            item_nulo.id = 0
            item_nulo.nombre = '----'
            lista_categorias.append(item_nulo)
            lista_especificaciones.append(item_nulo)
            lista_tipos.append(item_nulo)
            for categoria in categorias:
                lista_categorias.append(categoria)
            for especificacion in especificaciones:
                lista_especificaciones.append(especificacion)
            for tipo in tipos:
                lista_tipos.append(tipo)
            form = SuministroForm(initial={'clasificacion_general': suministro.clasificacion_general, 'nombre': suministro.nombre, 'sinonimos': suministro.sinonimos, 'representativo': suministro.representativo, 'unidad_embalaje': suministro.unidad_embalaje, 'unidad_medida': suministro.unidad_medida, 'dias_compra': suministro.dias_compra, 'requiere_cartilla': suministro.requiere_cartilla, 'peso': suministro.peso, 'largo': suministro.largo, 'alto': suministro.alto, 'ancho': suministro.ancho, 'estado': suministro.estado_suministro})
            error = ''
            if request.method == 'POST':
                proveedores = None
                try:
                    proveedores = request.session['proveedores']
                except :
                    pass
                if proveedores != None:
                    form = SuministroForm(request.POST)
                    suministros_existentes = []
                    lista_especificaciones = []
                    lista_tipos = []
                    categoria_actual = Categoria()
                    especificacion_actual = Categoria()
                    tipo_actual = Categoria()
                    if request.POST['categoria'] != '0':
                        categoria_actual = Categoria.objects.get(id=request.POST['categoria'], tipo=1)
                        especificaciones = Categoria.objects.filter(categoria_asociada=categoria_actual, tipo=2, estado=1)
                        try:
                            if request.POST['especificacion'] != '0':
                                especificacion_actual = Categoria.objects.get(id=request.POST['especificacion'], tipo=2)
                                categoria_suministro = especificacion_actual
                                tipos = Categoria.objects.filter(categoria_asociada=especificacion_actual, tipo=3, estado=1)
                                suministros_existentes = Suministro.objects.filter(categoria=especificacion_actual)
                                if request.POST['tipo'] != '0':
                                    tipo_actual = Categoria.objects.get(id=request.POST['tipo'], tipo=3)
                                    categoria_suministro = tipo_actual
                                    suministros_existentes = Suministro.objects.filter(categoria=tipo_actual)
                                lista_tipos.append(item_nulo)
                                for tipo in tipos:
                                    lista_tipos.append(tipo)
                        except :
                            pass
                        lista_especificaciones.append(item_nulo)
                        for especificacion in especificaciones:
                            lista_especificaciones.append(especificacion)

                    pag = Paginador(request, proveedores, 20, 1)
                    if len(proveedores) == 0:
                        error = 'Debe ingresar por lo menos un proveedor'
                        return render_to_response ('suministroadd.html',{'user': user, 'form':form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': pag, 'error': error, 'change': True } )
                    if form.is_valid():
                        nuevo_nombre_suministro = form.cleaned_data['nombre'].strip()
                        nuevo_nombre_suministro = normaliza(nuevo_nombre_suministro.lower())
                        if categoria_suministro == suministro.categoria and normaliza(suministro.nombre.lower()) == nuevo_nombre_suministro:
                            suministros_existentes = suministros_existentes.exclude(id=suministro.id)
                        for suministro_existente in suministros_existentes:
                            if normaliza(suministro_existente.nombre.lower()) == nuevo_nombre_suministro:
                                form._errors["nombre"] = ErrorList([u"El nombre del suministro ya existe en el sistema."])
                                return render_to_response ('suministroadd.html',{'user': user, 'form': form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': pag, 'change': True} )
                            sinonimos_suministro_existente = suministro_existente.sinonimos
                            sinonimos_suministro_existente = sinonimos_suministro_existente.split(',')
                            for sinonimo_suministro_existente in sinonimos_suministro_existente:
                                if normaliza(sinonimo_suministro_existente.lower().strip()) == nuevo_nombre_suministro:
                                    form._errors["nombre"] = ErrorList([u"El nombre del suministro ya existe en algunos suministros registrados en el sistema."])
                                    return render_to_response ('suministroadd.html',{'user': user, 'form': form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': pag, 'change': True} )
                        suministro.clasificacion_general = form.cleaned_data['clasificacion_general']
                        suministro.nombre = form.cleaned_data['nombre'].strip()
                        suministro.sinonimos = form.cleaned_data['sinonimos'].strip()
                        suministro.representativo = form.cleaned_data['representativo']
                        if form.cleaned_data['clasificacion_general'] == 'Material':
                            suministro.unidad_embalaje = form.cleaned_data['unidad_embalaje']
                        suministro.unidad_medida = form.cleaned_data['unidad_medida']
                        suministro.dias_compra = form.cleaned_data['dias_compra']
                        suministro.requiere_cartilla = form.cleaned_data['requiere_cartilla']
                        suministro.peso = form.cleaned_data['peso']
                        suministro.largo = form.cleaned_data['largo']
                        suministro.alto = form.cleaned_data['alto']
                        suministro.ancho = form.cleaned_data['ancho']
                        suministro.estado_suministro = form.cleaned_data['estado']
                        usuario = Usuario.objects.get(id=user.id)
                        suministro.usuario = usuario
                        if suministro.categoria != categoria_suministro:
                            suministro.categoria = categoria_suministro
                            max_codigo = suministros_existentes.aggregate(Max('codigo'))
                            codigo_suministro = 1
                            if max_codigo['codigo__max'] is not None:
                                codigo_suministro = int(max_codigo['codigo__max'])+1
                            suministro.codigo = codigo_suministro
                        try:
                            suministro.validate_unique()
                            suministro.save()
                            suministro.suministroproveedor_set.all().delete()
                            for proveedor in proveedores:
                                suministro_proveedor = SuministroProveedor()
                                suministro_proveedor.suministro = suministro
                                suministro_proveedor.proveedor = proveedor['proveedor']
                                suministro_proveedor.precio_suministro = proveedor['precio']
                                suministro_proveedor.iva_suministro = proveedor['iva']
                                suministro_proveedor.save()
                            del request.session['proveedores']
                            usuario_actual = Usuario.objects.get(id=user.id)
                            direccion_ip = request.META['REMOTE_ADDR']
                            registro_historial(direccion_ip, usuario_actual, u"Modifico suministro, nombre: "+ unicode(suministro.nombre))
                            return HttpResponseRedirect('/inverboy/home/suministrossearch')
                        except:
                            print 'error en campos unicos de suministro'
                else:
                    return HttpResponseRedirect('/inverboy/home/')
            request.session['proveedores'] = proveedores
            request.session['proveedores_agregar'] = []
            return render_to_response ('suministroadd.html',{'user': user, 'form':form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': pag, 'error': error, 'change': True} )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Busqueda suministros
def suministros_search(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_suministro' in user.get_all_permissions():
            criterio = ''
            suministros = Suministro.objects.all()
            if request.method == 'POST':
                criterio = request.POST['criterio'].strip()
                partes_criterio = criterio.split('.')
                if len(partes_criterio) == 4:
                    try:
                        categoria = Categoria.objects.get(id=int(partes_criterio[2]))
                        if categoria.categoria_asociada.id == int(partes_criterio[1]):
                            if categoria.categoria_asociada.categoria_asociada.id == int(partes_criterio[0]):
                                suministros = suministros.filter(categoria=categoria)
                                suministros = suministros.filter(codigo=int(partes_criterio[3]))
                            else:
                                suministros = []
                        else:
                            suministros = []
                    except :
                        suministros = []
                elif len(partes_criterio) == 3:
                    try:
                        categoria = Categoria.objects.get(id=int(partes_criterio[1]))
                        if categoria.categoria_asociada.id == int(partes_criterio[0]):
                            suministros = suministros.filter(categoria=categoria)
                            suministros = suministros.filter(codigo=int(partes_criterio[2]))
                        else:
                            suministros = []
                    except :
                        suministros = []
                else:
                    suministros = suministros.filter(Q(nombre__icontains=criterio) | Q(sinonimos__icontains=criterio))
            pag = Paginador(request, suministros, 20, 1)
            return render_to_response('reportesuministros.html', {'user': user, 'suministros': pag, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Crear suministro - Especificación
def suministro_add_especificacion(request, especificacion_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_suministro' in user.get_all_permissions():
            categorias = Categoria.objects.filter(tipo=1, estado=1)
            lista_categorias = []
            lista_especificaciones = []
            lista_tipos = []
            lista_proveedores = []
            especificacion_actual = Categoria.objects.get(id=especificacion_id)
            categoria_actual = especificacion_actual.categoria_asociada
            especificaciones = Categoria.objects.filter(categoria_asociada=categoria_actual)
            tipos = Categoria.objects.filter(categoria_asociada=especificacion_actual)
            tipo_actual = Categoria()
            item_nulo = Categoria()
            item_nulo.id = 0
            item_nulo.nombre = '----'
            lista_categorias.append(item_nulo)
            lista_especificaciones.append(item_nulo)
            lista_tipos.append(item_nulo)
            for categoria in categorias:
                lista_categorias.append(categoria)
            for especificacion in especificaciones:
                lista_especificaciones.append(especificacion)
            for tipo in tipos:
                lista_tipos.append(especificacion)
            form = SuministroForm()
            if request.method == 'POST':
                form = SuministroForm(request.POST)
                suministros_existentes = []
                if request.POST['categoria'] != '0':
                    categoria_actual = Categoria.objects.get(id=request.POST['categoria'], tipo=1)
                    especificaciones = Categoria.objects.filter(categoria_asociada=categoria_actual)
                    if request.POST['especificacion'] != '0':
                        especificacion_actual = Categoria.objects.get(id=request.POST['especificacion'], tipo=2)
                        categoria_suministro = especificacion_actual
                        tipos = Categoria.objects.filter(categoria_asociada=especificacion_actual, tipo=3)
                        suministros_existentes = Suministro.objects.filter(categoria=especificacion_actual)
                        if request.POST['tipo'] != '0':
                            tipo_actual = Categoria.objects.get(id=request.POST['tipo'], tipo=3)
                            categoria_suministro = tipo_actual
                            suministros_existentes = Suministro.objects.filter(categoria=tipo_actual)
                        lista_tipos = []
                        lista_tipos.append(item_nulo)
                        for tipo in tipos:
                            lista_tipos.append(tipo)
                    lista_especificaciones.append(item_nulo)
                    for especificacion in especificaciones:
                        lista_especificaciones.append(especificacion)
                proveedores = str(request.COOKIES["proveedores"])
                if proveedores == "":
                    error = 'Debe ingresar por lo menos un proveedor'
                    return render_to_response ('suministroadd.html',{'user': user, 'form':form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'error': error} )
                partes = proveedores.split('--')
                contador = 0
                while contador < len(partes)-1:
                    items = partes[contador]
                    item = items.split('-')
                    proveedor = Proveedor.objects.get(id=int(item[0]))
                    #proveedor.suministro_set.add(suministro)
                    suministro_proveedor = SuministroProveedor()
                    suministro_proveedor.precio_suministro = item[1]
                    if item[2] == 'true':
                        suministro_proveedor.iva_suministro = 0.16
                    else:
                        suministro_proveedor.iva_suministro = 0
                    #suministro_proveedor.suministro = suministro
                    suministro_proveedor.proveedor = proveedor
                    #suministro_proveedor.save()
                    lista_proveedores.append(suministro_proveedor)
                    contador = contador+1
                if form.is_valid():
                    nombre_nuevo_suministro = form.cleaned_data['nombre'].strip()
                    nombre_nuevo_suministro = normaliza(nombre_nuevo_suministro.lower())
                    for suministro_existente in suministros_existentes:
                        if normaliza(suministro_existente.nombre.lower()) == nombre_nuevo_suministro:
                            form._errors["nombre"] = ErrorList([u"El nombre del suministro ya existe en el sistema."])
                            return render_to_response ('suministroadd.html',{'user': user, 'form': form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': lista_proveedores} )
                        sinonimos_suministro_existente = suministro_existente.sinonimos
                        sinonimos_suministro_existente = sinonimos_suministro_existente.split(',')
                        for sinonimo_suministro_existente in sinonimos_suministro_existente:
                            if normaliza(sinonimo_suministro_existente.lower().strip()) == nombre_nuevo_suministro:
                                form._errors["nombre"] = ErrorList([u"El nombre del suministro ya existe en algunos suministros registrados en el sistema."])
                                return render_to_response ('suministroadd.html',{'user': user, 'form': form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': lista_proveedores} )
                    suministro = Suministro()
                    suministro.clasificacion_general = form.cleaned_data['clasificacion_general']
                    suministro.nombre = form.cleaned_data['nombre'].strip()
                    suministro.sinonimos = form.cleaned_data['sinonimos'].strip()
                    suministro.representativo = form.cleaned_data['representativo']
                    suministro.unidad_embalaje = form.cleaned_data['unidad_embalaje']
                    suministro.unidad_medida = form.cleaned_data['unidad_medida']
                    #suministro.promedio_precio_suministro = 0
                    suministro.peso = form.cleaned_data['peso']
                    suministro.largo = form.cleaned_data['largo']
                    suministro.alto = form.cleaned_data['alto']
                    suministro.ancho = form.cleaned_data['ancho']
                    #fecha = str(datetime.today().year) + '-' + str(datetime.today().month) + '-' + str(datetime.today().day)
                    #suministro.fecha_creacion = fecha
                    #suministro.fecha_actualizacion = fecha
                    suministro.estado_suministro = 1
                    usuario = Usuario.objects.get(id=user.id)
                    suministro.usuario = usuario
                    suministro.categoria = categoria_suministro

                    max_codigo = suministros_existentes.aggregate(Max('codigo'))
                    codigo_suministro = 1
                    if max_codigo['codigo__max'] is not None:
                        codigo_suministro = int(max_codigo['codigo__max'])+1
                    suministro.codigo = codigo_suministro
                    try:
                        suministro.validate_unique()
                        suministro.save()
                        for actual_suministro_proveedor in lista_proveedores:
                            actual_suministro_proveedor.suministro = suministro
                            actual_suministro_proveedor.save()
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, u"Registro nuevo suministro, nombre: "+ unicode(suministro.nombre))
                        return HttpResponseRedirect('/inverboy/home/suministrossearch/')
                    except:
                        print 'error en campos unicos de suministro'
            return render_to_response ('suministroadd.html',{'user': user, 'form':form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': lista_proveedores} )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Reporte suministros espcificación
def suministros_view_especificacion(request, especificacion_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_suministro' in user.get_all_permissions():
            especificacion = Categoria.objects.filter(id=especificacion_id, tipo=2)
            suministros = Suministro.objects.filter(categoria=especificacion)
            pag = Paginador(request, suministros, 20, 1)
            return render_to_response('reportesuministros.html', {'user': user, 'suministros': pag})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')