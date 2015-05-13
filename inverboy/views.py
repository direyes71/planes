# -*- encoding: utf-8 -*-

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

# Create your views here.

import socket


def logear(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user']
            password = form.cleaned_data['clave']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    request.session.set_expiry(600)
                    login(request, user)
                    direccion_ip = request.META['REMOTE_ADDR']
                    usuario_actual = Usuario.objects.get(id=user.id)
                    registro_historial(direccion_ip, usuario_actual, u"Inicio sesión")
                    return HttpResponseRedirect('/inverboy/home/')
                else:
                    error = 'El usuario no se encuentra activo'
            else:
                error = 'Datos no validos'
            return render_to_response('index.html', {'form': form, 'error': error})
    return render_to_response('index.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated():
        user = request.user
        direccion_ip = request.META['REMOTE_ADDR']
        usuario_actual = Usuario.objects.get(id=user.id)
        registro_historial(direccion_ip, usuario_actual, u"Cerró sesion")
        logout(request)
    return HttpResponseRedirect('/inverboy/')


def home(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        permisos_usuario = user.get_all_permissions()
        return render_to_response('home.html', {'user': user, 'permisos': permisos_usuario})
    return HttpResponseRedirect('/inverboy/')


def change_usuario(request, usuario_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        permisos_usuario = user.get_all_permissions()
        if user.id == int(usuario_id):
            usuario = Usuario.objects.get(id=usuario_id)
            form = ModificarUsuarioForm()
            if request.method == 'POST':
                form = ModificarUsuarioForm(request.POST)
                if form.is_valid():
                    if usuario.check_password(form.cleaned_data['contrasena_anterior'])==False:
                        form._errors["contrasena_anterior"] = ErrorList([u"La contraseña anterior no coincide."])
                    else:
                        usuario.set_password(form.cleaned_data['contrasena'])
                        usuario.save()
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario, u"Cambió su contraseña de usuario")
                        return HttpResponseRedirect('/inverboy/home/')
            return render_to_response('usuariochange.html', {'user': user, 'permisos': permisos_usuario, 'form': form, 'usuario': usuario})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def validar_permiso_usuario(id_usuario, codename_permiso):
    usuario = Usuario.objects.get(id=id_usuario)
    permisos_usuario = usuario.get_all_permissions()
    #for permiso in permisos_usuario:
    #    print permiso
    #print permisos_usuario
    #print codename_permiso in permisos_usuario
    return codename_permiso in permisos_usuario


def usuario_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.add_usuario'):
            permisos_usuario = user.get_all_permissions()
            form = UsuarioForm()
            departamentos = Departamento.objects.all()
            lista_municipios = []
            departamento_actual = Departamento()
            municipio_actual = Municipio()
            fecha_nacimiento = ''
            if request.method == 'POST':
                if request.POST['departamento'] != '0':
                    departamento_actual = Departamento.objects.get(id=request.POST['departamento'])
                    municipios = Municipio.objects.filter(departamento=departamento_actual)
                    if request.POST['municipio'] != '0':
                        municipio_actual = Municipio.objects.get(id=request.POST['municipio'])
                    item_nulo = Municipio()
                    item_nulo.id = 0
                    item_nulo.nombre = '---'
                    lista_municipios.append(item_nulo)
                    for municipio in municipios:
                        lista_municipios.append(municipio)
                form = UsuarioForm(request.POST)
                fecha_nacimiento = request.POST['fecha_nacimiento']
                if form.is_valid():
                    usuario = Usuario()
                    usuario.identificacion = form.cleaned_data['identificacion']
                    try:
                        usuario.validate_unique(exclude='username')
                    except:
                        form._errors["identificacion"] = ErrorList([u"La identificacion ya existe en el sistema."])
                    usuario.username = form.cleaned_data['nombre_usuario']
                    try:
                        usuario.validate_unique(exclude='identificacion')
                    except:
                        form._errors["nombre_usuario"] = ErrorList([u"El nombre de usuario ya existe en el sistema."])
                    usuario.first_name = form.cleaned_data['nombres']
                    usuario.last_name = form.cleaned_data['apellidos']
                    usuario.municipio = form.cleaned_data['municipio']
                    usuario.fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
                    usuario.direccion = form.cleaned_data['direccion']
                    usuario.cargo = form.cleaned_data['cargo']
                    usuario.celular = form.cleaned_data['celular']
                    usuario.telefono = form.cleaned_data['telefono']
                    usuario.is_active = form.cleaned_data['estado']
                    usuario.set_password(form.cleaned_data['contrasena'])
                    try:
                        usuario.validate_unique()
                        usuario.save()
                        grupo_usuario = form.cleaned_data['grupo_usuario']
                        usuario.groups.add(grupo_usuario)
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, u"Registro nuevo usuario, identificación: "+str(usuario.identificacion))
                        return HttpResponseRedirect('/inverboy/home/usuariosview/')
                    except:
                        print 'error en campos unicos de usuario'
            return render_to_response('usuarioadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form, 'departamentos': departamentos, 'municipios': lista_municipios, 'departamento_actual': departamento_actual, 'municipio_actual': municipio_actual, 'fecha_nacimiento': fecha_nacimiento})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def usuarios_view(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.view_usuario'):
            usuarios = Usuario.objects.all()
            permisos_usuario = user.get_all_permissions()
            pag = Paginador(request, usuarios, 20, 1)
            return render_to_response('reporteusuarios.html', {'user': user, 'permisos': permisos_usuario, 'usuarios': pag, 'titulo':'Usuarios'})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def usuarios_search(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.view_usuario'):
            permisos_usuario = user.get_all_permissions()
            criterio = request.GET['criterio']

            #usuarios = Usuario.objects.all()
            if criterio == "":
                return HttpResponseRedirect('/inverboy/home/usuariosview/')
            qry = "SELECT * FROM inverboy_usuario, auth_user WHERE user_ptr_id=id"
            try:
                criterio = int(criterio)
                #usuarios = usuarios.filter(identificacion=criterio)
                qry = qry + " AND identificacion="+str(criterio)
            except:
                #us = Usuario()
                #us.get_full_name()
                #usuarios = usuarios.filter(Q(full_name__icontains=criterio) | Q(nombre_comercial=criterio))
                #usuarios = usuarios.filter(Q(fullName__icontains=criterio))
                #usuarios.filter(fullname__icontains=criterio)
                qry = qry + " AND (CONCAT(first_name, ' ', last_name) LIKE '%%" + criterio + "%%' OR username LIKE '%%"+ criterio+"%%')"
            usuarios = Usuario.objects.raw(qry)
            lista_usuarios = []
            for usuario in usuarios:
                lista_usuarios.append(usuario)
            pag = Paginador(request, lista_usuarios, 20, 1)
            return render_to_response('reporteusuarios.html', {'user': user, 'permisos': permisos_usuario, 'usuarios': pag, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def usuario_change(request, usuario_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.change_usuario'):
            permisos_usuario = user.get_all_permissions()
            usuario = Usuario.objects.get(id = usuario_id)
            grupos = usuario.groups.all()
            grupo_usuario = grupos[0]
            form = UsuarioForm(initial={'user': user, 'identificacion': usuario.identificacion, 'nombre_usuario': usuario.username, 'nombres': usuario.first_name, 'apellidos': usuario.last_name, 'municipio': usuario.municipio, 'fecha_nacimiento': usuario.fecha_nacimiento, 'direccion': usuario.direccion, 'cargo': usuario.cargo, 'celular': usuario.celular, 'telefono':usuario.telefono, 'grupo_usuario':grupo_usuario, 'estado': usuario.is_active})
            departamentos = Departamento.objects.all()
            lista_municipios = []
            municipio_actual = usuario.municipio
            departamento_actual = municipio_actual.departamento
            municipios = Municipio.objects.filter(departamento=municipio_actual.departamento)
            item_nulo = Municipio()
            item_nulo.id = 0
            item_nulo.nombre = '---'
            lista_municipios.append(item_nulo)
            for municipio in municipios:
                lista_municipios.append(municipio)
            fecha_nacimiento = usuario.fecha_nacimiento.strftime("%Y-%m-%d")
            if request.method == 'POST':
                if request.POST['departamento'] != '0':
                    departamento_actual = Departamento.objects.get(id=request.POST['departamento'])
                    municipios = Municipio.objects.filter(departamento=departamento_actual)
                    lista_municipios = []
                    if request.POST['municipio'] != '0':
                        municipio_actual = Municipio.objects.get(id=request.POST['municipio'])
                    lista_municipios.append(item_nulo)
                    for municipio in municipios:
                        lista_municipios.append(municipio)
                form = UsuarioForm(request.POST)
                fecha_nacimiento = request.POST['fecha_nacimiento']
                if form.is_valid():
                    #print usuario.identificacion
                    #print usuario.username
                    if usuario.identificacion != form.cleaned_data['identificacion']:
                        usuario.identificacion = form.cleaned_data['identificacion']
                        try:
                            usuario.validate_unique(exclude='username')
                        except:
                            form._errors["identificacion"] = ErrorList([u"La identificacion ya existe en el sistema."])
                    if usuario.username != form.cleaned_data['nombre_usuario']:
                        usuario.username = form.cleaned_data['nombre_usuario']
                        try:
                            usuario.validate_unique(exclude='identificacion')
                        except:
                            form._errors["nombre_usuario"] = ErrorList([u"El nombre de usuario ya existe en el sistema."])
                    usuario.first_name = form.cleaned_data['nombres']
                    usuario.last_name = form.cleaned_data['apellidos']
                    usuario.municipio = form.cleaned_data['municipio']
                    usuario.fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
                    usuario.direccion = form.cleaned_data['direccion']
                    usuario.cargo = form.cleaned_data['cargo']
                    usuario.celular = form.cleaned_data['celular']
                    usuario.telefono = form.cleaned_data['telefono']
                    usuario.is_active = form.cleaned_data['estado']
                    usuario.set_password(form.cleaned_data['contrasena'])
                    try:
                        usuario.validate_unique()
                        usuario.save()
                        usuario.groups.clear()
                        grupo_usuario = form.cleaned_data['grupo_usuario']
                        usuario.groups.add(grupo_usuario)
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, "Modifico usuario, identificacion: "+str(usuario.identificacion))
                        return HttpResponseRedirect('/inverboy/home/usuariosview/')
                    except:
                        print 'error campos unicos usuario'
            return render_to_response('usuarioadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form, 'departamentos': departamentos, 'municipios': lista_municipios, 'departamento_actual': departamento_actual, 'municipio_actual': municipio_actual, 'fecha_nacimiento': fecha_nacimiento})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def grupo_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'auth.add_group'):
            permisos_usuario = user.get_all_permissions()
            form = GrupoForm()
            #print form
            if request.method == 'POST':
                form = GrupoForm(request.POST)
                if form.is_valid():
                    #grupo, created = Group.objects.get_or_create(name=form.cleaned_data['nombre_grupo'])
                    grupo = Group()
                    grupo.name = form.cleaned_data['nombre_grupo']
                    try:
                        grupo.validate_unique()
                        grupo.save()
                        modulo_usuarios = form.cleaned_data['modulo_usuarios']
                        modulo_grupos = form.cleaned_data['modulo_grupos']
                        modulo_proveedores = form.cleaned_data['modulo_proveedores']
                        modulo_categorias = form.cleaned_data['modulo_categorias']
                        modulo_suministros = form.cleaned_data['modulo_suministros']
                        modulo_capitulos = form.cleaned_data['modulo_capitulos']
                        modulo_apu = form.cleaned_data['modulo_apu']
                        modulo_proyectos = form.cleaned_data['modulo_proyectos']
                        for item in modulo_usuarios:
                            # obtenemos el id del permiso, el que es creado de forma automtica cuando usamos syncdb
                            permiso = Permission.objects.get(codename=item)
                            # agregamos el permiso
                            grupo.permissions.add(permiso)
                        for item in modulo_grupos:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_proveedores:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_categorias:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_suministros:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_capitulos:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_apu:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_proyectos:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, "Registro nuevo grupo de usuarios, nombre: "+grupo.name)
                        return HttpResponseRedirect('/inverboy/home/gruposview/')
                    except:
                        form._errors["nombre_grupo"] = ErrorList([u"El grupo ya existe en el sistema."])
            return render_to_response('grupoadd.html', { 'user': user, 'permisos': permisos_usuario, 'form': form})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def grupos_view(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'auth.view_group'):
            permisos_usuario = user.get_all_permissions()
            grupos = Group.objects.all()
            pag = Paginador(request, grupos, 20, 1)
            return render_to_response('reportegrupos.html', {'user': user, 'permisos': permisos_usuario, 'grupos': pag})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def grupos_search(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'auth.view_group'):
            permisos_usuario = user.get_all_permissions()
            criterio = request.GET['criterio']
            if criterio == "":
                return HttpResponseRedirect('/inverboy/home/gruposview/')
            grupos = Group.objects.all()
            grupos = grupos.filter(name__icontains=criterio)
            pag = Paginador(request, grupos, 20, 1)
            return render_to_response('reportegrupos.html', {'user': user, 'permisos': permisos_usuario, 'grupos': pag, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def grupo_details(request, grupo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'auth.view_group'):
            permisos_usuario = user.get_all_permissions()
            grupo = Group.objects.get(id = grupo_id)
            permisos = grupo.permissions.all()
            return render_to_response('grupodetails.html', {'user': user, 'permisos': permisos_usuario, 'grupo': grupo, 'permisos_grupo': permisos})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def grupo_change(request, grupo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'auth.change_group'):
            permisos_usuario = user.get_all_permissions()
            grupo = Group.objects.get(id = grupo_id)
            permisos = grupo.permissions.all()
            modulo_usuarios = []
            modulo_grupos = []
            modulo_proveedores = []
            modulo_categorias = []
            modulo_suministros = []
            modulo_capitulos = []
            modulo_apu = []
            modulo_proyectos = []
            for permiso in permisos:
                if permiso.codename == 'add_usuario':
                    modulo_usuarios.append(permiso.codename)
                elif permiso.codename == 'change_usuario':
                    modulo_usuarios.append(permiso.codename)
                elif permiso.codename == 'view_usuario':
                    modulo_usuarios.append(permiso.codename)
                elif permiso.codename == 'add_group':
                    modulo_grupos.append(permiso.codename)
                elif permiso.codename == 'change_group':
                    modulo_grupos.append(permiso.codename)
                elif permiso.codename == 'view_group':
                    modulo_grupos.append(permiso.codename)
                elif permiso.codename == 'add_proveedor':
                    modulo_proveedores.append(permiso.codename)
                elif permiso.codename == 'change_proveedor':
                    modulo_proveedores.append(permiso.codename)
                elif permiso.codename == 'view_proveedor':
                    modulo_proveedores.append(permiso.codename)
                elif permiso.codename == 'add_categoria':
                    modulo_categorias.append(permiso.codename)
                elif permiso.codename == 'change_categoria':
                    modulo_categorias.append(permiso.codename)
                elif permiso.codename == 'view_categoria':
                    modulo_categorias.append(permiso.codename)
                elif permiso.codename == 'add_suministro':
                    modulo_suministros.append(permiso.codename)
                elif permiso.codename == 'change_suministro':
                    modulo_suministros.append(permiso.codename)
                elif permiso.codename == 'view_suministro':
                    modulo_suministros.append(permiso.codename)
                elif permiso.codename == 'add_capitulo':
                    modulo_capitulos.append(permiso.codename)
                elif permiso.codename == 'change_capitulo':
                    modulo_capitulos.append(permiso.codename)
                elif permiso.codename == 'view_capitulo':
                    modulo_capitulos.append(permiso.codename)
                elif permiso.codename == 'add_apu':
                    modulo_apu.append(permiso.codename)
                elif permiso.codename == 'change_apu':
                    modulo_apu.append(permiso.codename)
                elif permiso.codename == 'view_apu':
                    modulo_apu.append(permiso.codename)
                elif permiso.codename == 'add_proyecto':
                    modulo_proyectos.append(permiso.codename)
                elif permiso.codename == 'change_proyecto':
                    modulo_proyectos.append(permiso.codename)
                elif permiso.codename == 'view_proyecto':
                    modulo_proyectos.append(permiso.codename)
            form = GrupoForm(initial={'nombre_grupo': grupo.name, 'modulo_usuarios': modulo_usuarios, 'modulo_grupos': modulo_grupos,'modulo_proveedores': modulo_proveedores, 'modulo_categorias': modulo_categorias, 'modulo_suministros': modulo_suministros, 'modulo_capitulos': modulo_capitulos, 'modulo_apu': modulo_apu, 'modulo_proyectos': modulo_proyectos})
            if request.method == 'POST':
                form = GrupoForm(request.POST)
                if form.is_valid():
                    #grupo.name = form.cleaned_data['nombre_grupo']
                    try:
                        if grupo.name != form.cleaned_data['nombre_grupo']:
                            grupo.name = form.cleaned_data['nombre_grupo']
                            grupo.validate_unique()
                            grupo.save()
                        modulo_usuarios = form.cleaned_data['modulo_usuarios']
                        modulo_grupos = form.cleaned_data['modulo_grupos']
                        modulo_proveedores = form.cleaned_data['modulo_proveedores']
                        modulo_categorias = form.cleaned_data['modulo_categorias']
                        modulo_suministros = form.cleaned_data['modulo_suministros']
                        modulo_capitulos = form.cleaned_data['modulo_capitulos']
                        modulo_apu = form.cleaned_data['modulo_apu']
                        modulo_proyectos = form.cleaned_data['modulo_proyectos']
                        grupo.permissions.clear()
                        for item in modulo_usuarios:
                            # obtenemos el id del permiso, el que es creado de forma automtica cuando usamos syncdb
                            permiso = Permission.objects.get(codename=item)
                            # agregamos el permiso
                            grupo.permissions.add(permiso)
                        for item in modulo_grupos:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_proveedores:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_categorias:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_suministros:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_capitulos:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_apu:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_proyectos:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, "Modifico grupo de usuario, nombre: "+grupo.name)
                        return HttpResponseRedirect('/inverboy/home/gruposview/')
                    except:
                        form._errors["nombre_grupo"] = ErrorList([u"El grupo ya existe en el sistema."])
            return render_to_response('grupoadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def proveedor_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.add_proveedor'):
            permisos_usuario = user.get_all_permissions()
            form1 = ProveedorForm()
            form2 = ContactoForm()
            departamentos = Departamento.objects.all()
            lista_municipios = []
            departamento_actual = Departamento()
            municipio_actual = Municipio()
            lista_contactos = []
            if request.method == 'POST':
                if request.POST['departamento'] != '0':
                    departamento_actual = Departamento.objects.get(id=request.POST['departamento'])
                    municipios = Municipio.objects.filter(departamento=departamento_actual)
                    if request.POST['municipio'] != '0':
                        municipio_actual = Municipio.objects.get(id=request.POST['municipio'])
                    item_nulo = Municipio()
                    item_nulo.id = 0
                    item_nulo.nombre = '---'
                    lista_municipios.append(item_nulo)
                    for municipio in municipios:
                        lista_municipios.append(municipio)
                form1 = ProveedorForm(request.POST)
                contactos = str(request.COOKIES["contactos"])
                if contactos == "":
                    error = 'Debe ingresar por lo menos un contacto'
                    return render_to_response('proveedor.html',{'user': user, 'permisos': permisos_usuario, 'form1': form1, 'form2': form2, 'departamentos': departamentos, 'municipios': lista_municipios, 'departamento_actual': departamento_actual, 'municipio_actual': municipio_actual, 'error': error})
                partes = contactos.split('..')
                contador_contactos = 0
                while contador_contactos < len(partes)-1:
                    parte = partes[contador_contactos]
                    items = parte.split('.')
                    contacto = Contacto()
                    conta = 0
                    for item in items:
                        item_decodificado = decodeFromHex(item)
                        if conta == 0:
                            contacto.nombre_contacto = item_decodificado
                        if conta == 1:
                            contacto.cargo_contacto = int(item_decodificado)
                        if conta == 2:
                            contacto.telefono_contacto = item_decodificado
                        if conta == 3:
                            contacto.ext_contacto = item_decodificado
                        if conta == 4:
                            contacto.celular_contacto = item_decodificado
                        if conta == 5:
                            contacto.email_contacto = item_decodificado
                        conta = conta+1
                    lista_contactos.append(contacto)
                    contador_contactos = contador_contactos+1
                if form1.is_valid():
                    proveedor = Proveedor()
                    proveedor.identificacion = form1.cleaned_data['identificacion']
                    try:
                        proveedor.validate_unique()
                    except:
                        form1._errors["identificacion"] = ErrorList([u"La identificacion ya existe en el sistema."])
                    proveedor.razon_social = form1.cleaned_data['razon_social']
                    proveedor.nombre_comercial = form1.cleaned_data['nombre_comercial']
                    proveedor.direccion = form1.cleaned_data['direccion']
                    proveedor.tipo = form1.cleaned_data['tipo']
                    proveedor.regimen_tributario = form1.cleaned_data['regimen_tributario']
                    proveedor.telefono_1 = form1.cleaned_data['telefono_1']
                    proveedor.telefono_2 = form1.cleaned_data['telefono_2']
                    proveedor.fax = form1.cleaned_data['fax']
                    proveedor.web_site = form1.cleaned_data['web_site']
                    proveedor.email = form1.cleaned_data['email']
                    proveedor.estado_proveedor = True
                    proveedor.observaciones = form1.cleaned_data['observaciones']
                    proveedor.municipio = form1.cleaned_data['municipio']
                    try:
                        proveedor.validate_unique()
                        proveedor.save()
                        for contacto in lista_contactos:
                            contacto.proveedor = proveedor
                            contacto.save()
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, "Registro nuevo proveedor, identificacion: "+str(proveedor.identificacion))
                        return HttpResponseRedirect('/inverboy/home/proveedoresview/')
                    except:
                        print 'error en campos unicos de proveedor'
            return render_to_response('proveedor.html',{'user': user, 'permisos': permisos_usuario, 'form1': form1, 'form2': form2, 'departamentos': departamentos, 'municipios': lista_municipios, 'departamento_actual': departamento_actual, 'municipio_actual': municipio_actual, 'contactos': lista_contactos})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def proveedores_view(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.view_proveedor'):
            permisos_usuario = user.get_all_permissions()
            proveedores = Proveedor.objects.all()
            pag = Paginador(request, proveedores, 20, 1)
            return render_to_response('reporteproveedores.html', {'user': user, 'permisos': permisos_usuario, 'proveedores': pag})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def proveedores_search(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.view_proveedor'):
            permisos_usuario = user.get_all_permissions()
            criterio = request.GET['criterio']
            if criterio == "":
                return HttpResponseRedirect('/inverboy/home/proveedoresview/')
            proveedores = Proveedor.objects.all()
            try:
                criterio = int(criterio)
                proveedores = proveedores.filter(identificacion=criterio)
            except:
                proveedores = proveedores.filter(Q(razon_social__icontains=criterio) | Q(nombre_comercial=criterio))
            pag = Paginador(request, proveedores, 20, 1)
            return render_to_response('reporteproveedores.html', {'user': user, 'permisos': permisos_usuario, 'proveedores': pag, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def proveedor_change(request, proveedor_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.change_proveedor'):
            permisos_usuario = user.get_all_permissions()
            proveedor = Proveedor.objects.get(id=proveedor_id)
            form1 = ProveedorForm(initial={'identificacion': proveedor.identificacion, 'razon_social': proveedor.razon_social, 'nombre_comercial': proveedor.nombre_comercial, 'direccion': proveedor.direccion, 'tipo': proveedor.tipo, 'regimen_tributario': proveedor.regimen_tributario, 'telefono_1': proveedor.telefono_1, 'telefono_2': proveedor.telefono_2, 'fax': proveedor.fax, 'web_site': proveedor.web_site, 'email': proveedor.email, 'observaciones': proveedor.observaciones, 'estado': proveedor.estado_proveedor})
            form2 = ContactoForm()
            departamentos = Departamento.objects.all()
            lista_municipios = []
            municipio_actual = proveedor.municipio
            departamento_actual = municipio_actual.departamento
            lista_contactos = Contacto.objects.filter(proveedor=proveedor)
            municipios = Municipio.objects.filter(departamento = municipio_actual.departamento)
            item_nulo = Municipio()
            item_nulo.id = 0
            item_nulo.nombre = '---'
            lista_municipios.append(item_nulo)
            for municipio in municipios:
                lista_municipios.append(municipio)
            if request.method == 'POST':
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
                contactos = str(request.COOKIES["contactos"])
                if contactos == "":
                    error = 'Debe ingresar por lo menos un contacto'
                    return render_to_response('proveedor.html',{'user': user, 'permisos': permisos_usuario, 'form1': form1, 'form2': form2, 'departamentos': departamentos, 'municipios': lista_municipios, 'departamento_actual': departamento_actual, 'municipio_actual': municipio_actual, 'error': error, 'change': True})
                lista_contactos = []
                partes = contactos.split('..')
                contador_contactos = 0
                while contador_contactos < len(partes)-1:
                    parte = partes[contador_contactos]
                    items = parte.split('.')
                    contacto = Contacto()
                    conta = 0
                    for item in items:
                        item_decodificado = decodeFromHex(item)
                        if conta == 0:
                            contacto.nombre_contacto = item_decodificado
                        if conta == 1:
                            contacto.cargo_contacto = int(item_decodificado)
                        if conta == 2:
                            contacto.telefono_contacto = item_decodificado
                        if conta == 3:
                            contacto.ext_contacto = item_decodificado
                        if conta == 4:
                            contacto.celular_contacto = item_decodificado
                        if conta == 5:
                            contacto.email_contacto = item_decodificado
                        conta = conta+1
                    lista_contactos.append(contacto)
                    contador_contactos = contador_contactos+1
                if form1.is_valid():
                    if proveedor.identificacion != form1.cleaned_data['identificacion']:
                        proveedor.identificacion = form1.cleaned_data['identificacion']
                        try:
                            proveedor.validate_unique()
                        except:
                            form1._errors["identificacion"] = ErrorList([u"La identificación ya existe en el sistema."])
                    proveedor.razon_social = form1.cleaned_data['razon_social']
                    proveedor.nombre_comercial = form1.cleaned_data['nombre_comercial']
                    proveedor.direccion = form1.cleaned_data['direccion']
                    proveedor.tipo = form1.cleaned_data['tipo']
                    proveedor.regimen_tributario = form1.cleaned_data['regimen_tributario']
                    proveedor.telefono_1 = form1.cleaned_data['telefono_1']
                    proveedor.telefono_2 = form1.cleaned_data['telefono_2']
                    proveedor.fax = form1.cleaned_data['fax']
                    proveedor.web_site = form1.cleaned_data['web_site']
                    proveedor.email = form1.cleaned_data['email']
                    proveedor.estado_proveedor = form1.cleaned_data['estado']
                    proveedor.observaciones = form1.cleaned_data['observaciones']
                    proveedor.municipio = form1.cleaned_data['municipio']
                    try:
                        proveedor.validate_unique()
                        proveedor.save()
                        Contacto.objects.filter(proveedor=proveedor).delete()
                        for contacto in lista_contactos:
                            contacto.proveedor = proveedor
                            contacto.save()
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, "Modifico proveedor, identificacion: "+str(proveedor.identificacion))
                        return HttpResponseRedirect('/inverboy/home/proveedoresview/')
                    except:
                        print 'error en campos unicos de proveedor'
            return render_to_response('proveedor.html', {'user': user, 'permisos': permisos_usuario, 'form1': form1, 'form2': form2, 'contactos': lista_contactos, 'departamentos': departamentos, 'municipios': lista_municipios, 'departamento_actual': departamento_actual, 'municipio_actual':municipio_actual, 'change': True})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def categoria_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.add_categoria'):
            permisos_usuario = user.get_all_permissions()
            form = CategoriaForm()
            if request.method == 'POST':
                form = CategoriaForm(request.POST)
                if form.is_valid():
                    categoria = Categoria()
                    categoria.nombre = form.cleaned_data['nombre']
                    categoria.tipo = 1
                    categoria.estado = 1
                    categoria.save()
                    usuario_actual = Usuario.objects.get(id=user.id)
                    direccion_ip = request.META['REMOTE_ADDR']
                    registro_historial(direccion_ip, usuario_actual, u"Registró nueva categoria suministros, nombre: "+unicode(categoria.nombre))
                    return HttpResponseRedirect('/inverboy/home/categoriasview/')
            return render_to_response('categoriaadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def categorias_view(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.view_categoria'):
            permisos_usuario = user.get_all_permissions()
            categorias = Categoria.objects.filter(tipo=1)
            pag = Paginador(request, categorias, 20, 1)
            return render_to_response('reportecategorias.html', {'user': user, 'permisos': permisos_usuario, 'categorias': pag})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def categorias_search(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.view_categoria'):
            permisos_usuario = user.get_all_permissions()
            criterio = request.GET['criterio']
            if criterio == "":
                return HttpResponseRedirect('/inverboy/home/categoriasview/')
            categorias = Categoria.objects.filter(tipo=1)
            categorias = categorias.filter(Q(nombre__icontains=criterio))
            pag = Paginador(request, categorias, 20, 1)
            return render_to_response('reportecategorias.html', {'user': user, 'permisos': permisos_usuario, 'categorias': pag, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def categoria_change(request, categoria_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.change_categoria'):
            permisos_usuario = user.get_all_permissions()
            categoria = Categoria.objects.get(id=categoria_id)
            form = CategoriaForm(initial={'nombre': categoria.nombre, 'estado': categoria.estado})
            if request.method == 'POST':
                form = CategoriaForm(request.POST)
                if form.is_valid():
                    categoria.nombre = form.cleaned_data['nombre']
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
                    registro_historial(direccion_ip, usuario_actual, u"Modificó categoria suministros, nombre: "+unicode(categoria.nombre))
                    return HttpResponseRedirect('/inverboy/home/categoriasview/')
            return render_to_response('categoriaadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form, 'change': True})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def especificacion_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.add_categoria'):
            permisos_usuario = user.get_all_permissions()
            form = EspecificacionForm()
            if request.method == 'POST':
                form = EspecificacionForm(request.POST)
                if form.is_valid():
                    especificacion = Categoria()
                    especificacion.nombre = form.cleaned_data['nombre']
                    especificacion.tipo = 2
                    especificacion.estado = 1
                    especificacion.categoria_asociada = form.cleaned_data['categoria_asociada']
                    especificacion.save()
                    usuario_actual = Usuario.objects.get(id=user.id)
                    direccion_ip = request.META['REMOTE_ADDR']
                    registro_historial(direccion_ip, usuario_actual, u"Registro nueva especificación suministros, nombre: "+unicode(especificacion.nombre)+u", en la categoria: "+unicode(especificacion.categoria_asociada.nombre))
                    return HttpResponseRedirect('/inverboy/home/especificacionesview/'+str(especificacion.categoria_asociada_id)+'/')
            return render_to_response('especificacionadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def especificacion_add_categoria(request, categoria_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.add_categoria'):
            permisos_usuario = user.get_all_permissions()
            form = EspecificacionForm(initial={'categoria_asociada': categoria_id})
            if request.method == 'POST':
                form = EspecificacionForm(request.POST)
                if form.is_valid():
                    especificacion = Categoria()
                    especificacion.nombre = form.cleaned_data['nombre']
                    especificacion.tipo = 2
                    especificacion.estado = 1
                    especificacion.categoria_asociada = form.cleaned_data['categoria_asociada']
                    especificacion.save()
                    usuario_actual = Usuario.objects.get(id=user.id)
                    direccion_ip = request.META['REMOTE_ADDR']
                    registro_historial(direccion_ip, usuario_actual, u"Registro nueva especificación suministros, nombre: "+unicode(especificacion.nombre)+u", en la categoria: "+unicode(especificacion.categoria_asociada.nombre))
                    return HttpResponseRedirect('/inverboy/home/especificacionesview/'+str(especificacion.categoria_asociada_id)+'/')
            return render_to_response('especificacionadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def especificaciones_view(request, categoria_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.view_categoria'):
            permisos_usuario = user.get_all_permissions()
            categoria = Categoria.objects.get(id=categoria_id, tipo=1)
            especificaciones = Categoria.objects.filter(tipo=2, categoria_asociada=categoria)
            pag = Paginador(request, especificaciones, 20, 1)
            return render_to_response('reporteespecificaciones.html', {'user': user, 'permisos': permisos_usuario, 'especificaciones': pag, 'categoria': categoria})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def especificaciones_search(request, categoria_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.view_categoria'):
            permisos_usuario = user.get_all_permissions()
            criterio = request.GET['criterio']
            if criterio == "":
                return HttpResponseRedirect('/inverboy/home/especificacionesview/'+categoria_id+'/')
            categoria = Categoria.objects.get(id=categoria_id, tipo=1)
            especificaciones = Categoria.objects.filter(tipo=2, categoria_asociada=categoria)
            especificaciones = especificaciones.filter(Q(nombre__icontains=criterio))
            pag = Paginador(request, especificaciones, 20, 1)
            return render_to_response('reporteespecificaciones.html', {'user': user, 'permisos': permisos_usuario, 'especificaciones': pag, 'categoria': categoria, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')



def especificacion_change(request, especificacion_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.change_categoria'):
            permisos_usuario = user.get_all_permissions()
            especificacion = Categoria.objects.get(id=especificacion_id)
            form = EspecificacionForm(initial={'categoria_asociada': especificacion.categoria_asociada, 'nombre': especificacion.nombre, 'estado': especificacion.estado})
            if request.method == 'POST':
                form = EspecificacionForm(request.POST)
                if form.is_valid():
                    especificacion.nombre = form.cleaned_data['nombre']
                    especificacion.estado = form.cleaned_data['estado']
                    especificacion.categoria_asociada = form.cleaned_data['categoria_asociada']
                    especificacion.save()
                    Suministro.objects.filter(categoria=especificacion).update(estado_suministro=especificacion.estado)
                    tipos = Categoria.objects.filter(tipo=3, categoria_asociada=especificacion)
                    tipos.update(estado=especificacion.estado)
                    for tipo in tipos:
                        Suministro.objects.filter(categoria=tipo).update(estado_suministro=especificacion.estado)
                    usuario_actual = Usuario.objects.get(id=user.id)
                    direccion_ip = request.META['REMOTE_ADDR']
                    registro_historial(direccion_ip, usuario_actual, u"Modifico especificación suministros, nombre: "+unicode(especificacion.nombre)+u", en la categoria: "+unicode(especificacion.categoria_asociada.nombre))
                    return HttpResponseRedirect('/inverboy/home/especificacionesview/'+str(especificacion.categoria_asociada_id)+'/')
            return render_to_response('especificacionadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form, 'change': True})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def tipo_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.add_categoria'):
            permisos_usuario = user.get_all_permissions()
            categorias = Categoria.objects.filter(tipo=1, estado=1)
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
                    especificaciones = Categoria.objects.filter(tipo=2, categoria_asociada=categoria_actual)
                    lista_especificaciones.append(item_nulo)
                    for especificacion in especificaciones:
                        lista_especificaciones.append(especificacion)
                    if request.POST['especificacion'] != '0':
                        especificacion_actual = Categoria.objects.get(id=request.POST['especificacion'], tipo=2)
                if form.is_valid():
                    tipo = Categoria()
                    tipo.nombre = form.cleaned_data['nombre']
                    tipo.tipo = 3
                    tipo.estado = 1
                    tipo.categoria_asociada = especificacion_actual
                    tipo.save()
                    usuario_actual = Usuario.objects.get(id=user.id)
                    direccion_ip = request.META['REMOTE_ADDR']
                    registro_historial(direccion_ip, usuario_actual, u"Registró nuevo tipo suministros, nombre: "+unicode(tipo.nombre)+u", en la categoria: "+unicode(tipo.categoria_asociada.categoria_asociada.nombre)+u", en la especificación: "+unicode(tipo.categoria_asociada.nombre))
                    return HttpResponseRedirect('/inverboy/home/tiposview/'+str(especificacion_actual.id)+'/')
            return render_to_response('tipoadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form, 'categorias': lista_categorias, 'especificaciones': lista_especificaciones, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def tipo_add_especificacion(request, especificacion_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.add_categoria'):
            permisos_usuario = user.get_all_permissions()
            especificacion_actual = Categoria.objects.get(id=especificacion_id, tipo=2)
            categoria_actual = especificacion_actual.categoria_asociada
            categorias = Categoria.objects.filter(tipo=1, estado=1)
            especificaciones = Categoria.objects.filter(categoria_asociada=especificacion_actual.categoria_asociada, tipo=2, estado=1)
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
                if request.POST['categoria'] != '0':
                    categoria_actual = Categoria.objects.get(id=request.POST['categoria'], tipo=1)
                    especificaciones = Categoria.objects.filter(tipo=2, categoria_asociada=categoria_actual)
                    lista_especificaciones.append(item_nulo)
                    for especificacion in especificaciones:
                        lista_especificaciones.append(especificacion)
                    if request.POST['especificacion'] != '0':
                        especificacion_actual = Categoria.objects.get(id=request.POST['especificacion'], tipo=2)
                if form.is_valid():
                    tipo = Categoria()
                    tipo.nombre = form.cleaned_data['nombre']
                    tipo.tipo = 3
                    tipo.estado = 1
                    tipo.categoria_asociada = especificacion_actual
                    tipo.save()
                    usuario_actual = Usuario.objects.get(id=user.id)
                    direccion_ip = request.META['REMOTE_ADDR']
                    registro_historial(direccion_ip, usuario_actual, u"Registró nuevo tipo suministros, nombre: "+unicode(tipo.nombre)+u", en la categoria: "+unicode(tipo.categoria_asociada.categoria_asociada.nombre)+u", en la especificación: "+unicode(tipo.categoria_asociada.nombre))
                    return HttpResponseRedirect('/inverboy/home/tiposview/'+str(especificacion_actual.id)+'/')
            return render_to_response('tipoadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form, 'categorias': lista_categorias, 'especificaciones': lista_especificaciones, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')



def tipos_view(request, especificacion_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.view_categoria'):
            permisos_usuario = user.get_all_permissions()
            tipos = Categoria.objects.filter(tipo=3, categoria_asociada=especificacion_id)
            especificacion = Categoria.objects.get(id=especificacion_id, tipo=2)
            categoria = Categoria.objects.get(id = especificacion.categoria_asociada_id, tipo=1)
            pag = Paginador(request, tipos, 20, 1)
            return render_to_response('reportetipos.html', {'user': user, 'permisos': permisos_usuario, 'tipos': pag, 'categoria': categoria, 'especificacion': especificacion})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def tipos_search(request, especificacion_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.view_categoria'):
            permisos_usuario = user.get_all_permissions()
            criterio = request.GET['criterio']
            if criterio == "":
                return HttpResponseRedirect('/inverboy/home/tiposview/'+especificacion_id+'/')
            especificacion = Categoria.objects.get(id=especificacion_id, tipo=2)
            categoria = especificacion.categoria_asociada
            tipos = Categoria.objects.filter(tipo=3, categoria_asociada=especificacion)
            tipos = tipos.filter(Q(nombre__icontains=criterio))
            pag = Paginador(request, tipos, 20, 1)
            return render_to_response('reportetipos.html', {'user': user, 'permisos': permisos_usuario, 'tipos': pag, 'categoria': categoria, 'especificacion': especificacion, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def tipo_change(request, tipo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.change_categoria'):
            permisos_usuario = user.get_all_permissions()
            tipo = Categoria.objects.get(id=tipo_id)
            especificacion_actual = tipo.categoria_asociada
            categoria_actual = especificacion_actual.categoria_asociada
            categorias = Categoria.objects.filter(tipo=1, estado=1)
            especificaciones = Categoria.objects.filter(tipo=2, categoria_asociada=categoria_actual)
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
                if request.POST['categoria'] != '0':
                    categoria_actual = Categoria.objects.get(id=request.POST['categoria'], tipo=1)
                    especificaciones = Categoria.objects.filter(tipo=2, categoria_asociada=categoria_actual)
                    lista_especificaciones = []
                    lista_especificaciones.append(item_nulo)
                    for especificacion in especificaciones:
                        lista_especificaciones.append(especificacion)
                    if request.POST['especificacion'] != '0':
                        especificacion_actual = Categoria.objects.get(id=request.POST['especificacion'], tipo=2)
                if form.is_valid():
                    tipo.nombre = form.cleaned_data['nombre']
                    tipo.tipo = 3
                    tipo.estado = form.cleaned_data['estado']
                    tipo.categoria_asociada = especificacion_actual
                    tipo.save()
                    Suministro.objects.filter(categoria=tipo).update(estado_suministro=tipo.estado)
                    usuario_actual = Usuario.objects.get(id=user.id)
                    direccion_ip = request.META['REMOTE_ADDR']
                    registro_historial(direccion_ip, usuario_actual, u"Modificó tipo suministros, nombre: "+unicode(tipo.nombre)+unicode(tipo.nombre)+u", en la categoria: "+unicode(tipo.categoria_asociada.categoria_asociada.nombre)+u", en la especificación: "+unicode(tipo.categoria_asociada.nombre))
                    return HttpResponseRedirect('/inverboy/home/tiposview/'+str(especificacion_actual.id)+'/')
            return render_to_response('tipoadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form, 'categorias': categorias, 'especificaciones': lista_especificaciones, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'change': True})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def suministro_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.add_suministro'):
            permisos_usuario = user.get_all_permissions()
            categorias = Categoria.objects.filter(tipo=1, estado=1)
            lista_categorias = []
            lista_especificaciones = []
            lista_tipos = []
            lista_proveedores = []
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
                    return render_to_response ('suministroadd.html',{'user': user, 'permisos': permisos_usuario, 'form':form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'error': error} )
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
                    nombre_nuevo_suministro = form.cleaned_data['nombre']
                    nombre_nuevo_suministro = normaliza(nombre_nuevo_suministro.lower())
                    for suministro_existente in suministros_existentes:
                        if normaliza(suministro_existente.nombre.lower()) == nombre_nuevo_suministro:
                            form._errors["nombre"] = ErrorList([u"El nombre del suministro ya existe en el sistema."])
                            return render_to_response ('suministroadd.html',{'user': user, 'permisos': permisos_usuario, 'form': form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': lista_proveedores} )
                        sinonimos_suministro_existente = suministro_existente.sinonimos
                        sinonimos_suministro_existente = sinonimos_suministro_existente.split(',')
                        for sinonimo_suministro_existente in sinonimos_suministro_existente:
                            if normaliza(sinonimo_suministro_existente.lower().strip()) == nombre_nuevo_suministro:
                                form._errors["nombre"] = ErrorList([u"El nombre del suministro ya existe en algunos suministros registrados en el sistema."])
                                return render_to_response ('suministroadd.html',{'user': user, 'permisos': permisos_usuario, 'form': form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': lista_proveedores} )
                    suministro = Suministro()
                    suministro.clasificacion_general = form.cleaned_data['clasificacion_general']
                    suministro.nombre = form.cleaned_data['nombre']
                    suministro.sinonimos = form.cleaned_data['sinonimos']
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
                        registro_historial(direccion_ip, usuario_actual, u"Registró nuevo suministro, nombre: "+unicode(suministro.nombre))
                        return HttpResponseRedirect('/inverboy/home/suministrosview/')
                    except:
                        print 'error en campos unicos de suministro'
            return render_to_response ('suministroadd.html',{'user': user, 'permisos': permisos_usuario, 'form':form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': lista_proveedores} )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def suministro_add_especificacion(request, especificacion_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.add_suministro'):
            permisos_usuario = user.get_all_permissions()
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
                    return render_to_response ('suministroadd.html',{'user': user, 'permisos': permisos_usuario, 'form':form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'error': error} )
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
                    nombre_nuevo_suministro = form.cleaned_data['nombre']
                    nombre_nuevo_suministro = normaliza(nombre_nuevo_suministro.lower())
                    for suministro_existente in suministros_existentes:
                        if normaliza(suministro_existente.nombre.lower()) == nombre_nuevo_suministro:
                            form._errors["nombre"] = ErrorList([u"El nombre del suministro ya existe en el sistema."])
                            return render_to_response ('suministroadd.html',{'user': user, 'permisos': permisos_usuario, 'form': form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': lista_proveedores} )
                        sinonimos_suministro_existente = suministro_existente.sinonimos
                        sinonimos_suministro_existente = sinonimos_suministro_existente.split(',')
                        for sinonimo_suministro_existente in sinonimos_suministro_existente:
                            if normaliza(sinonimo_suministro_existente.lower().strip()) == nombre_nuevo_suministro:
                                form._errors["nombre"] = ErrorList([u"El nombre del suministro ya existe en algunos suministros registrados en el sistema."])
                                return render_to_response ('suministroadd.html',{'user': user, 'permisos': permisos_usuario, 'form': form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': lista_proveedores} )
                    suministro = Suministro()
                    suministro.clasificacion_general = form.cleaned_data['clasificacion_general']
                    suministro.nombre = form.cleaned_data['nombre']
                    suministro.sinonimos = form.cleaned_data['sinonimos']
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
                        registro_historial(direccion_ip, usuario_actual, u"Registró nuevo suministro, nombre: "+unicode(suministro.nombre))
                        return HttpResponseRedirect('/inverboy/home/suministrosview/')
                    except:
                        print 'error en campos unicos de suministro'
            return render_to_response ('suministroadd.html',{'user': user, 'permisos': permisos_usuario, 'form':form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': lista_proveedores} )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')



def suministros_view(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.view_suministro'):
            permisos_usuario = user.get_all_permissions()
            suministros = Suministro.objects.all()
            pag = Paginador(request, suministros, 20, 1)
            return render_to_response('reportesuministros.html', {'user': user, 'permisos': permisos_usuario, 'suministros': pag})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def suministros_view_especificacion(request, especificacion_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.view_suministro'):
            permisos_usuario = user.get_all_permissions()
            especificacion = Categoria.objects.filter(id=especificacion_id, tipo=2)
            suministros = Suministro.objects.filter(categoria=especificacion)
            pag = Paginador(request, suministros, 20, 1)
            return render_to_response('reportesuministros.html', {'user': user, 'permisos': permisos_usuario, 'suministros': pag})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def suministros_search(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.view_suministro'):
            permisos_usuario = user.get_all_permissions()
            criterio = request.GET['criterio']
            if criterio == "":
                return HttpResponseRedirect('/inverboy/home/suministrosview/')
            suministros = Suministro.objects.all()
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
            return render_to_response('reportesuministros.html', {'user': user, 'permisos': permisos_usuario, 'suministros': pag, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')



""" SUMINISTROS DE UNA CATEGORIA ESPECIFICA
def suministros_view(request, categoria_id):
    if request.user.is_authenticated():
        user = request.user
        suministros = Suministro.objects.filter(categoria_asociada=categoria_id)
        categoria_actual = Categoria.objects.get(id=categoria_id)
        return render_to_response('reportesuministros.html', {'user': user, 'suministros': suministros, 'categoria_actual': categoria_actual})
    return HttpResponseRedirect('/support/')
"""


def suministro_change(request, suministro_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.change_suministro'):
            permisos_usuario = user.get_all_permissions()
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
            lista_proveedores = SuministroProveedor.objects.filter(suministro=suministro)
            if categoria_suministro.tipo == 2:
                especificacion_actual = categoria_suministro
                especificaciones = Categoria.objects.filter(categoria_asociada=especificacion_actual.categoria_asociada, tipo=2)
                tipos = Categoria.objects.filter(categoria_asociada=especificacion_actual, tipo=3)
            elif categoria_suministro.tipo == 3:
                tipo_actual = categoria_suministro
                especificacion_actual = tipo_actual.categoria_asociada
                tipos = Categoria.objects.filter(categoria_asociada=especificacion_actual, tipo=3)
                especificaciones = Categoria.objects.filter(categoria_asociada=especificacion_actual.categoria_asociada, tipo=2)
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
            form = SuministroForm(initial={'clasificacion_general': suministro.clasificacion_general, 'nombre': suministro.nombre, 'sinonimos': suministro.sinonimos, 'representativo': suministro.representativo, 'unidad_embalaje': suministro.unidad_embalaje, 'unidad_medida': suministro.unidad_medida, 'peso': suministro.peso, 'largo': suministro.largo, 'alto': suministro.alto, 'ancho': suministro.ancho, 'estado': suministro.estado_suministro})
            if request.method == 'POST':
                form = SuministroForm(request.POST)
                suministros_existentes = []
                lista_especificaciones = []
                lista_tipos = []
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
                        lista_tipos.append(item_nulo)
                        for tipo in tipos:
                            lista_tipos.append(tipo)
                    lista_especificaciones.append(item_nulo)
                    for especificacion in especificaciones:
                        lista_especificaciones.append(especificacion)
                proveedores = str(request.COOKIES["proveedores"])
                if proveedores == "":
                    error = 'Debe ingresar por lo menos un proveedor'
                    return render_to_response ('suministroadd.html',{'user': user, 'permisos': permisos_usuario, 'form': form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'error': error, 'change': True} )
                #print proveedores
                partes = proveedores.split('--')
                contador = 0
                lista_proveedores = []
                while contador < len(partes)-1:
                    items = partes[contador]
                    item = items.split('-')
                    proveedor = Proveedor.objects.get(id=int(item[0]))
                    suministro_proveedor = SuministroProveedor()
                    suministro_proveedor.precio_suministro = item[1]
                    if item[2] == 'true':
                        suministro_proveedor.iva_suministro = 0.16
                    else:
                        suministro_proveedor.iva_suministro = 0
                    suministro_proveedor.proveedor = proveedor
                    lista_proveedores.append(suministro_proveedor)
                    contador = contador+1
                if form.is_valid():
                    nuevo_nombre_suministro = form.cleaned_data['nombre']
                    nuevo_nombre_suministro = normaliza(nuevo_nombre_suministro.lower())
                    if categoria_suministro == suministro.categoria and normaliza(suministro.nombre.lower()) == nuevo_nombre_suministro:
                        suministros_existentes = suministros_existentes.exclude(id=suministro.id)
                    for suministro_existente in suministros_existentes:
                        if normaliza(suministro_existente.nombre.lower()) == nuevo_nombre_suministro:
                            form._errors["nombre"] = ErrorList([u"El nombre del suministro ya existe en el sistema."])
                            return render_to_response ('suministroadd.html',{'user': user, 'permisos': permisos_usuario, 'form': form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': lista_proveedores, 'change': True} )
                        sinonimos_suministro_existente = suministro_existente.sinonimos
                        sinonimos_suministro_existente = sinonimos_suministro_existente.split(',')
                        for sinonimo_suministro_existente in sinonimos_suministro_existente:
                            if normaliza(sinonimo_suministro_existente.lower().strip()) == nuevo_nombre_suministro:
                                form._errors["nombre"] = ErrorList([u"El nombre del suministro ya existe en algunos suministros registrados en el sistema."])
                                return render_to_response ('suministroadd.html',{'user': user, 'permisos': permisos_usuario, 'form': form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': lista_proveedores, 'change': True} )
                    suministro.clasificacion_general = form.cleaned_data['clasificacion_general']
                    suministro.nombre = form.cleaned_data['nombre']
                    suministro.sinonimos = form.cleaned_data['sinonimos']
                    suministro.representativo = form.cleaned_data['representativo']
                    suministro.unidad_embalaje = form.cleaned_data['unidad_embalaje']
                    suministro.unidad_medida = form.cleaned_data['unidad_medida']
                    suministro.peso = form.cleaned_data['peso']
                    suministro.largo = form.cleaned_data['largo']
                    suministro.alto = form.cleaned_data['alto']
                    suministro.ancho = form.cleaned_data['ancho']
                    #fecha = str(datetime.today().year) + '-' + str(datetime.today().month) + '-' + str(datetime.today().day)
                    #suministro.fecha_actualizacion = fecha
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
                        SuministroProveedor.objects.filter(suministro=suministro).delete()
                        for actual_suministro_proveedor in lista_proveedores:
                            actual_suministro_proveedor.suministro = suministro
                            actual_suministro_proveedor.save()
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, u"Modificó suministro, nombre: "+unicode(suministro.nombre))
                        return HttpResponseRedirect('/inverboy/home/suministrosview')
                    except:
                        print 'error en campos unicos de suministro'
            return render_to_response ('suministroadd.html',{'user': user, 'permisos': permisos_usuario, 'form':form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': lista_proveedores, 'change': True} )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def capitulo_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.add_capitulo'):
            permisos_usuario = user.get_all_permissions()
            form = CapituloForm()
            if request.method == 'POST':
                form = CapituloForm(request.POST)
                if form.is_valid():
                    capitulo = Capitulo()
                    capitulo.nombre_capitulo = form.cleaned_data['nombre']
                    capitulo.tipo_capitulo = 1
                    capitulo.estado_capitulo = 1
                    capitulo.save()
                    usuario_actual = Usuario.objects.get(id=user.id)
                    direccion_ip = request.META['REMOTE_ADDR']
                    registro_historial(direccion_ip, usuario_actual, u"Registró capitulo APU, nombre: "+unicode(capitulo.nombre))
                    return HttpResponseRedirect('/inverboy/home/capitulosview/')
            return render_to_response('capituloadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def capitulos_view(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.view_capitulo'):
            permisos_usuario = user.get_all_permissions()
            capitulos = Capitulo.objects.filter(tipo_capitulo=1)
            pag = Paginador(request, capitulos, 20, 1)
            return render_to_response('reportecapitulos.html', {'user': user, 'permisos': permisos_usuario, 'capitulos': pag})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def capitulos_search(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.view_capitulo'):
            permisos_usuario = user.get_all_permissions()
            criterio = request.GET['criterio']
            if criterio == "":
                return HttpResponseRedirect('/inverboy/home/capitulosview/')
            capitulos = Capitulo.objects.filter(tipo_capitulo=1)
            capitulos = capitulos.filter(Q(nombre_capitulo__icontains=criterio))
            pag = Paginador(request, capitulos, 20, 1)
            return render_to_response('reportecapitulos.html', {'user': user, 'permisos': permisos_usuario, 'capitulos': pag, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def capitulo_change(request, capitulo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.change_capitulo'):
            permisos_usuario = user.get_all_permissions()
            capitulo = Capitulo.objects.get(id=capitulo_id)
            form = CapituloForm(initial={'nombre': capitulo.nombre_capitulo, 'estado': capitulo.estado_capitulo})
            if request.method == 'POST':
                form = CapituloForm(request.POST)
                if form.is_valid():
                    capitulo.nombre_capitulo = form.cleaned_data['nombre']
                    capitulo.estado_capitulo = form.cleaned_data['estado']
                    capitulo.save()
                    ## PARA MODIFICAR EL ESTADO DE SUBCAPITULOS Y APUS
                    """especificaciones = Categoria.objects.filter(tipo=2, categoria_asociada=categoria)
                    especificaciones.update(estado=categoria.estado)
                    for especificacion in especificaciones:
                        Suministro.objects.filter(categoria=especificacion).update(estado_suministro=categoria.estado)
                        tipos = Categoria.objects.filter(tipo=3, categoria_asociada=especificacion)
                        tipos.update(estado=categoria.estado)
                        for tipo in tipos:
                            Suministro.objects.filter(categoria=tipo).update(estado_suministro=categoria.estado)"""
                    usuario_actual = Usuario.objects.get(id=user.id)
                    direccion_ip = request.META['REMOTE_ADDR']
                    registro_historial(direccion_ip, usuario_actual, "Modifico capitulo APU, nombre: "+capitulo.nombre)
                    return HttpResponseRedirect('/inverboy/home/capitulosview/')
            return render_to_response('capituloadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form, 'change': True})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def subcapitulo_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.add_capitulo'):
            permisos_usuario = user.get_all_permissions()
            form = SubCapituloForm()
            if request.method == 'POST':
                form = SubCapituloForm(request.POST)
                if form.is_valid():
                    subCapitulo = Capitulo()
                    subCapitulo.nombre_capitulo = form.cleaned_data['nombre']
                    subCapitulo.tipo_capitulo = 2
                    subCapitulo.estado_capitulo = 1
                    subCapitulo.capitulo_asociado = form.cleaned_data['capitulo_asociado']
                    subCapitulo.save()
                    usuario_actual = Usuario.objects.get(id=user.id)
                    direccion_ip = request.META['REMOTE_ADDR']
                    registro_historial(direccion_ip, usuario_actual, "Registro subcapitulo APU, nombre: "+subCapitulo.nombre)
                    return HttpResponseRedirect('/inverboy/home/subcapitulosview/'+str(subCapitulo.capitulo_asociado_id)+'/')
            return render_to_response('subcapituloadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def subcapitulos_view(request, capitulo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.view_capitulo'):
            permisos_usuario = user.get_all_permissions()
            capitulo = Capitulo.objects.get(id=capitulo_id, tipo_capitulo=1)
            subcapitulos = Capitulo.objects.filter(tipo_capitulo=2, capitulo_asociado=capitulo)
            pag = Paginador(request, subcapitulos, 20, 1)
            return render_to_response('reportesubcapitulos.html', {'user': user, 'permisos': permisos_usuario, 'subcapitulos': pag, 'capitulo': capitulo})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def subcapitulos_search(request, capitulo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.view_capitulo'):
            permisos_usuario = user.get_all_permissions()
            criterio = request.GET['criterio']
            if criterio == "":
                return HttpResponseRedirect('/inverboy/home/subcapitulosview/'+capitulo_id+'/')
            capitulo = Capitulo.objects.get(id=capitulo_id, tipo_capitulo=1)
            subcapitulos = Capitulo.objects.filter(tipo_capitulo=2, capitulo_asociado=capitulo)
            subcapitulos = subcapitulos.filter(Q(nombre_capitulo__icontains=criterio))
            pag = Paginador(request, subcapitulos, 20, 1)
            return render_to_response('reportesubcapitulos.html', {'user': user, 'permisos': permisos_usuario, 'subcapitulos': pag, 'capitulo': capitulo, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def subcapitulos_change(request, subcapitulo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.change_capitulo'):
            permisos_usuario = user.get_all_permissions()
            subcapitulo = Capitulo.objects.get(id=subcapitulo_id, tipo_capitulo=2)
            form = SubCapituloForm(initial={'capitulo_asociado': subcapitulo.capitulo_asociado, 'nombre': subcapitulo.nombre_capitulo, 'estado': subcapitulo.estado_capitulo})
            if request.method == 'POST':
                form = SubCapituloForm(request.POST)
                if form.is_valid():
                    subcapitulo.nombre_capitulo = form.cleaned_data['nombre']
                    subcapitulo.estado_capitulo = form.cleaned_data['estado']
                    subcapitulo.capitulo_asociado = form.cleaned_data['capitulo_asociado']
                    subcapitulo.save()
                    ####### Modificar estado APU's relacionados con subcapitulo ####################################
                    """Suministro.objects.filter(categoria=especificacion).update(estado_suministro=especificacion.estado)
                    tipos = Categoria.objects.filter(tipo=3, categoria_asociada=especificacion)
                    tipos.update(estado=especificacion.estado)
                    for tipo in tipos:
                        Suministro.objects.filter(categoria=tipo).update(estado_suministro=especificacion.estado)"""
                    usuario_actual = Usuario.objects.get(id=user.id)
                    direccion_ip = request.META['REMOTE_ADDR']
                    registro_historial(direccion_ip, usuario_actual, "Modifico subcapitulo APU, nombre: "+subcapitulo.nombre)
                    return HttpResponseRedirect('/inverboy/home/subcapitulosview/'+str(subcapitulo.capitulo_asociado_id)+'/')
            return render_to_response('subcapituloadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form, 'change': True})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def apu_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.add_apu'):
            permisos_usuario = user.get_all_permissions()
            capitulos = Capitulo.objects.filter(tipo_capitulo=1, estado_capitulo=1)
            lista_capitulos = []
            lista_subcapitulos = []
            lista_suministros = []
            capitulo_actual = Capitulo()
            subcapitulo_actual = Capitulo()
            item_nulo = Capitulo()
            item_nulo.id = 0
            item_nulo.nombre_capitulo = '----'
            lista_capitulos.append(item_nulo)
            for capitulo in capitulos:
                lista_capitulos.append(capitulo)
            form = ApuForm()
            if request.method == 'POST':
                form = ApuForm(request.POST)
                apus_existentes = []
                if request.POST['capitulo'] != '0':
                    capitulo_actual = Capitulo.objects.get(id=request.POST['capitulo'], tipo_capitulo=1)
                    subcapitulos = Capitulo.objects.filter(capitulo_asociado=capitulo_actual, estado_capitulo=1)
                    if request.POST['subcapitulo'] != '0':
                        subcapitulo_actual = Capitulo.objects.get(id=request.POST['subcapitulo'], tipo_capitulo=2)
                        capitulo_apu = subcapitulo_actual
                        apus_existentes = Apu.objects.filter(capitulo=subcapitulo_actual)
                    lista_subcapitulos.append(item_nulo)
                    for subcapitulo in subcapitulos:
                        lista_subcapitulos.append(subcapitulo)
                suministros = str(request.COOKIES["suministros"])
                if suministros == "":
                    error = 'Debe ingresar por lo menos un suministro'
                    return render_to_response ('apuadd.html',{'user': user, 'permisos': permisos_usuario, 'form':form, 'capitulos':  lista_capitulos, 'subcapitulos': lista_subcapitulos, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'error': error} )
                partes = suministros.split('--')
                contador = 0
                while contador < len(partes)-1:
                    items = partes[contador]
                    item = items.split('-')
                    suministro = Suministro.objects.get(id=int(item[0]))
                    #print suministro.id
                    suministro_apu = SuministroApu()
                    suministro_apu.precio_suministro = item[1]
                    suministro_apu.cantidad_suministro = item[2]
                    suministro_apu.suministro = suministro
                    lista_suministros.append(suministro_apu)
                    contador = contador+1
                if form.is_valid():
                    nombre_nuevo_apu = form.cleaned_data['nombre']
                    nombre_nuevo_apu = normaliza(nombre_nuevo_apu.lower())
                    for apu_existente in apus_existentes:
                        if normaliza(apu_existente.nombre_apu.lower()) == nombre_nuevo_apu:
                            form._errors["nombre"] = ErrorList([u"El nombre del apu ya existe en el sistema."])
                            return render_to_response ('apuadd.html',{'user': user, 'permisos': permisos_usuario, 'form': form, 'capitulos':  lista_capitulos, 'subcapitulos': lista_subcapitulos, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'suministros_apu': lista_suministros} )
                        """sinonimos_suministro_existente = suministro_existente.sinonimos
                        sinonimos_suministro_existente = sinonimos_suministro_existente.split(',')
                        for sinonimo_suministro_existente in sinonimos_suministro_existente:
                            if normaliza(sinonimo_suministro_existente.lower().strip()) == nombre_nuevo_suministro:
                                form._errors["nombre"] = ErrorList([u"El nombre del suministro ya existe en algunos suministros registrados en el sistema."])
                                return render_to_response ('suministroadd.html',{'user': user, 'permisos': permisos_usuario, 'form': form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': lista_proveedores} )"""
                    apu = Apu()
                    apu.nombre_apu = form.cleaned_data['nombre']
                    apu.unidad_medida_apu = form.cleaned_data['unidad_medida']
                    apu.estado_apu = 1
                    usuario = Usuario.objects.get(id=user.id)
                    apu.usuario = usuario
                    apu.capitulo = capitulo_apu
                    try:
                        apu.validate_unique()
                        apu.save()
                        for actual_suministro_apu in lista_suministros:
                            actual_suministro_apu.apu = apu
                            actual_suministro_apu.save()
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, "Registro APU, nombre: "+apu.nombre)
                        return HttpResponseRedirect('/inverboy/home/apusview/')
                    except:
                        print 'error en campos unicos de apu'
            return render_to_response ('apuadd.html',{'user': user, 'permisos': permisos_usuario, 'form':form, 'capitulos':  lista_capitulos, 'subcapitulos': lista_subcapitulos, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'suministros_apu': lista_suministros} )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def apus_search(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.view_apu'):
            permisos_usuario = user.get_all_permissions()
            apus = Apu.objects.all()
            capitulos = Capitulo.objects.filter(tipo_capitulo=1, estado_capitulo=1)
            lista_subcapitulos = []
            criterio = ""
            capitulo_actual = Capitulo()
            subcapitulo_actual = Capitulo()
            item_nulo = Capitulo()
            item_nulo.id = 0
            item_nulo.nombre_capitulo = '----'
            form = BusquedaApuform()
            if request.method == 'POST':
                if request.POST['capitulo'] != '0':
                    capitulo_actual = Capitulo.objects.get(tipo_capitulo=1, id=request.POST['capitulo'])
                    subcapitulos = Capitulo.objects.filter(tipo_capitulo=2, capitulo_asociado=capitulo_actual)
                    lista_subcapitulos.append(item_nulo)
                    for subcapitulo in subcapitulos:
                        lista_subcapitulos.append(subcapitulo)
                    if request.POST['subcapitulo'] != '0':
                        subcapitulo_actual = Capitulo.objects.get(tipo_capitulo=2, id=request.POST['subcapitulo'])
                form = BusquedaApuform(request.POST)
                if form.is_valid():
                    if subcapitulo_actual != Capitulo():
                        apus = apus.filter(Q(capitulo=subcapitulo_actual))
                    if form.cleaned_data['criterio'] != '':
                        criterio = form.cleaned_data['criterio']
                        apus = apus.filter(Q(nombre_apu__icontains=criterio))
            pag = Paginador(request, apus, 1, 1)
            return render_to_response('reporteapus.html', {'user': user, 'permisos': permisos_usuario, 'form': form, 'capitulos': capitulos, 'subcapitulos': lista_subcapitulos, 'apus': pag, 'criterio': criterio, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def apu_change(request, apu_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if validar_permiso_usuario(user.id, 'inverboy.change_apu'):
            permisos_usuario = user.get_all_permissions()
            apu = Apu.objects.get(id=apu_id)
            lista_capitulos = []
            lista_subcapitulos = []
            lista_suministros = SuministroApu.objects.filter(apu=apu)
            subcapitulo_actual = apu.capitulo
            capitulo_actual = subcapitulo_actual.capitulo_asociado
            capitulos = Capitulo.objects.filter(tipo_capitulo=1, estado_capitulo=1)
            subcapitulos = Capitulo.objects.filter(tipo_capitulo=2, estado_capitulo=1, capitulo_asociado=capitulo_actual)
            item_nulo = Capitulo()
            item_nulo.id = 0
            item_nulo.nombre_capitulo = '----'
            lista_capitulos.append(item_nulo)
            for capitulo in capitulos:
                lista_capitulos.append(capitulo)
            lista_subcapitulos.append(item_nulo)
            for subcapitulo in subcapitulos:
                lista_subcapitulos.append(subcapitulo)

            form = ApuForm(initial={'nombre': apu.nombre_apu, 'unidad_medida': apu.unidad_medida_apu, 'estado': apu.estado_apu})
            if request.method == 'POST':
                form = ApuForm(request.POST)
                apus_existentes = []
                lista_subcapitulos = []
                if request.POST['capitulo'] != '0':
                    capitulo_actual = Capitulo.objects.get(id=request.POST['capitulo'], tipo_capitulo=1)
                    subcapitulos = Capitulo.objects.filter(capitulo_asociado=capitulo_actual, estado_capitulo=1)
                    if request.POST['subcapitulo'] != '0':
                        subcapitulo_actual = Capitulo.objects.get(id=request.POST['subcapitulo'], tipo_capitulo=2)
                        capitulo_apu = subcapitulo_actual
                        apus_existentes = Apu.objects.filter(capitulo=subcapitulo_actual)
                    lista_subcapitulos.append(item_nulo)
                    for subcapitulo in subcapitulos:
                        lista_subcapitulos.append(subcapitulo)
                suministros = str(request.COOKIES["suministros"])
                if suministros == "":
                    error = 'Debe ingresar por lo menos un suministro'
                    return render_to_response ('apuadd.html',{'user': user, 'permisos': permisos_usuario, 'form':form, 'capitulos':  lista_capitulos, 'subcapitulos': lista_subcapitulos, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'error': error} )
                partes = suministros.split('--')
                contador = 0
                lista_suministros = []
                while contador < len(partes)-1:
                    items = partes[contador]
                    item = items.split('-')
                    suministro = Suministro.objects.get(id=int(item[0]))
                    #print suministro.id
                    suministro_apu = SuministroApu()
                    suministro_apu.precio_suministro = item[1]
                    suministro_apu.cantidad_suministro = item[2]
                    suministro_apu.suministro = suministro
                    lista_suministros.append(suministro_apu)
                    contador = contador+1
                if form.is_valid():
                    nuevo_nombre_apu = form.cleaned_data['nombre']
                    nuevo_nombre_apu = normaliza(nuevo_nombre_apu.lower())
                    if capitulo_apu == apu.capitulo and normaliza(apu.nombre_apu.lower()) == nuevo_nombre_apu:
                        apus_existentes = apus_existentes.exclude(id=apu.id)
                    for apu_existente in apus_existentes:
                        if normaliza(apu_existente.nombre_apu.lower()) == nuevo_nombre_apu:
                            form._errors["nombre"] = ErrorList([u"El nombre del apu ya existe en el sistema."])
                            return render_to_response ('apuadd.html',{'user': user, 'permisos': permisos_usuario, 'form': form, 'capitulos':  lista_capitulos, 'subcapitulos': lista_subcapitulos, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'suministros_apu': lista_suministros} )
                        """sinonimos_suministro_existente = suministro_existente.sinonimos
                        sinonimos_suministro_existente = sinonimos_suministro_existente.split(',')
                        for sinonimo_suministro_existente in sinonimos_suministro_existente:
                            if normaliza(sinonimo_suministro_existente.lower().strip()) == nombre_nuevo_suministro:
                                form._errors["nombre"] = ErrorList([u"El nombre del suministro ya existe en algunos suministros registrados en el sistema."])
                                return render_to_response ('suministroadd.html',{'user': user, 'permisos': permisos_usuario, 'form': form, 'categorias':  lista_categorias, 'especificaciones': lista_especificaciones, 'tipos': lista_tipos, 'categoria_actual': categoria_actual, 'especificacion_actual': especificacion_actual, 'tipo_actual': tipo_actual, 'suministro_proveedores': lista_proveedores} )"""
                    apu.nombre_apu = form.cleaned_data['nombre']
                    apu.unidad_medida_apu = form.cleaned_data['unidad_medida']
                    apu.estado_apu = 1
                    usuario = Usuario.objects.get(id=user.id)
                    apu.usuario = usuario
                    apu.capitulo = capitulo_apu
                    SuministroApu.objects.filter(apu=apu).delete()
                    try:
                        apu.validate_unique()
                        apu.save()
                        for actual_suministro_apu in lista_suministros:
                            actual_suministro_apu.apu = apu
                            actual_suministro_apu.save()
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, "Modifico APU, nombre: "+apu.nombre)
                        return HttpResponseRedirect('/inverboy/home/apusview/')
                    except:
                        print 'error en campos unicos de apu'
            return render_to_response ('apuadd.html',{'user': user, 'permisos': permisos_usuario, 'form':form, 'capitulos':  lista_capitulos, 'subcapitulos': lista_subcapitulos, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'suministros_apu': lista_suministros} )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def capitulo_apu_proyecto_add(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'inverboy.add_capitulo'):
        permisos_usuario = user.get_all_permissions()
        try:
            proyecto = Proyecto.objects.get(id=proyecto_id)
        except:
            return HttpResponseRedirect('/inverboy/home/')
        form = CapituloApuProyectoForm()
        titulo = "Nuevo capitulo APU's"
        if request.method == 'POST':
            form = CapituloApuProyectoForm(request.POST)
            if form.is_valid():
                capitulos_apu_proyecto = CapituloApuProyecto.objects.filter(tipo_capitulo=1, proyecto=proyecto)
                capitulo_apu_existe = False
                if capitulos_apu_proyecto.filter(Q(codigo=form.cleaned_data['codigo'])):
                    form._errors["codigo"] = ErrorList([u"El codigo ya se encuentra asignado a un capitulo del proyecto."])
                    capitulo_apu_existe = True
                if capitulos_apu_proyecto.filter(Q(nombre_capitulo=form.cleaned_data['nombre'])):
                    form._errors["nombre"] = ErrorList([u"El nombre ya se encuentra asignado a un capitulo del proyecto."])
                    capitulo_apu_existe = True
                if capitulo_apu_existe == False:
                    capitulo = CapituloApuProyecto()
                    capitulo.codigo = form.cleaned_data['codigo']
                    capitulo.nombre_capitulo = form.cleaned_data['nombre']
                    capitulo.tipo_capitulo = 1
                    capitulo.estado_capitulo = 1
                    capitulo.proyecto = proyecto
                    capitulo.save()
                    usuario_actual = Usuario.objects.get(id=user.id)
                    direccion_ip = request.META['REMOTE_ADDR']
                    registro_historial(direccion_ip, usuario_actual, "registro capitulo apu proyecto, codigo: "+capitulo.codigo+", nombre: "+capitulo.nombre+", proyecto: "+proyecto.nombre)
                    return HttpResponseRedirect('/inverboy/home/capitulosapuproyectoview/'+str(proyecto.id)+'/')
        return render_to_response('capituloapuproyectoadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form, 'proyecto': proyecto, 'titulo': titulo})
        #return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def capitulos_apu_proyecto_view(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'auth.view_group'):
        permisos_usuario = user.get_all_permissions()
        try:
            proyecto = Proyecto.objects.get(id = proyecto_id)
        except:
            return HttpResponseRedirect('/inverboy/home/')
        capitulos_apu_proyecto = CapituloApuProyecto.objects.filter(tipo_capitulo=1, proyecto=proyecto)
        pag = Paginador(request, capitulos_apu_proyecto, 20, 1)
        return render_to_response('reportecapitulosapuproyecto.html', {'user': user, 'permisos': permisos_usuario, 'proyecto': proyecto, 'capitulos': pag})
        #return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def capitulos_apu_proyecto_search(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'inverboy.view_capitulo'):
        permisos_usuario = user.get_all_permissions()
        try:
            proyecto = Proyecto.objects.get(id=proyecto_id)
        except:
            return HttpResponseRedirect('/inverboy/home/')
        criterio = request.GET['criterio']
        if criterio == "":
            return HttpResponseRedirect('/inverboy/home/capitulosapuproyectoview/'+proyecto_id+'/')
        capitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=1, proyecto=proyecto)
        try:
            criterio = int(criterio)
            capitulos = capitulos.filter(Q(codigo=criterio))
        except:
            capitulos = capitulos.filter(Q(nombre_capitulo__icontains=criterio))
        pag = Paginador(request, capitulos, 20, 1)
        return render_to_response('reportecapitulosapuproyecto.html', {'user': user, 'permisos': permisos_usuario, 'proyecto': proyecto, 'capitulos': pag, 'criterio': criterio})
        #return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def apu_proyecto_change(request, apu_proyecto_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'inverboy.change_apu'):
        permisos_usuario = user.get_all_permissions()
        try:
            proyecto = Proyecto.objects.get(id=proyecto_id)
            apu_proyecto = ApuProyecto.objects.get(id=apu_proyecto_id, proyecto=proyecto)
        except:
            return HttpResponseRedirect('/inverboy/home/')
        lista_capitulos = []
        lista_subcapitulos = []
        lista_suministros = SuministroApuProyecto.objects.filter(apu_proyecto=apu_proyecto)
        capitulo_actual = apu_proyecto.capitulo
        subcapitulo_actual = CapituloApuProyecto()
        if capitulo_actual.tipo_capitulo == 2:
            subcapitulo_actual = capitulo_actual
            capitulo_actual = capitulo_actual.capitulo_asociado
        capitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=1, estado_capitulo=1)
        subcapitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=2, estado_capitulo=1, capitulo_asociado=capitulo_actual)
        item_nulo = Capitulo()
        item_nulo.id = 0
        item_nulo.nombre_capitulo = '----'
        lista_capitulos.append(item_nulo)
        for capitulo in capitulos:
            lista_capitulos.append(capitulo)
        lista_subcapitulos.append(item_nulo)
        for subcapitulo in subcapitulos:
            lista_subcapitulos.append(subcapitulo)
        form = ApuProyectoForm(initial={'nombre': apu_proyecto.nombre_apu, 'cantidad_proyecto': apu_proyecto.cantidad_proyecto, 'cantidad_apu': apu_proyecto.cantidad_apu, 'cantidad_total': apu_proyecto.cantidad_total, 'valor_unitario': apu_proyecto.valor_unitario, 'valor_total': apu_proyecto.valor_total })
        if request.method == 'POST':
            form = ApuProyectoForm(request.POST)
            apus_existentes = []
            lista_subcapitulos = []
            if request.POST['capitulo'] != '0':
                capitulo_actual = CapituloApuProyecto.objects.get(id=request.POST['capitulo'], tipo_capitulo=1, proyecto=proyecto)
                apus_existentes = ApuProyecto.objects.filter(capitulo=capitulo_actual, proyecto=proyecto)
                subcapitulos = CapituloApuProyecto.objects.filter(capitulo_asociado=capitulo_actual, estado_capitulo=1, proyecto=proyecto)
                capitulo_apu = capitulo_actual
                if request.POST['subcapitulo'] != '0':
                    subcapitulo_actual = CapituloApuProyecto.objects.get(id=request.POST['subcapitulo'], tipo_capitulo=2, proyecto=proyecto)
                    capitulo_apu = subcapitulo_actual
                    apus_existentes = ApuProyecto.objects.filter(capitulo=subcapitulo_actual, proyecto=proyecto)
                lista_subcapitulos.append(item_nulo)
                for subcapitulo in subcapitulos:
                    lista_subcapitulos.append(subcapitulo)
            suministros = str(request.COOKIES["suministros"])
            if suministros == "":
                error = 'Debe ingresar por lo menos un suministro'
                return render_to_response ('apuadd.html',{'user': user, 'permisos': permisos_usuario, 'form':form, 'capitulos':  lista_capitulos, 'subcapitulos': lista_subcapitulos, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'error': error} )
            partes = suministros.split('--')
            contador = 0
            lista_suministros = []
            valor_unitario = 0
            while contador < len(partes)-1:
                items = partes[contador]
                item = items.split('-')
                suministro = Suministro.objects.get(id=int(item[0]))
                suministro_apu = SuministroApuProyecto()
                suministro_apu.precio_suministro = item[1]
                suministro_apu.cantidad_suministro = item[2]
                suministro_apu.cantidad_adicion = 0
                suministro_apu.precio_total = float(suministro_apu.precio_suministro) * float(suministro_apu.cantidad_suministro)
                suministro_apu.suministro = suministro
                valor_unitario = valor_unitario + float(suministro_apu.precio_suministro) * float(suministro_apu.cantidad_suministro)
                lista_suministros.append(suministro_apu)
                contador = contador+1
            if form.is_valid():
                nombre_nuevo_apu = form.cleaned_data['nombre']
                nombre_nuevo_apu = normaliza(nombre_nuevo_apu.lower())
                if normaliza(apu_proyecto.nombre_apu.lower()) != nombre_nuevo_apu:
                    for apu_existente in apus_existentes:
                        if normaliza(apu_existente.nombre_apu.lower()) == nombre_nuevo_apu:
                            form._errors["nombre"] = ErrorList([u"El nombre del apu ya existe en el sistema."])
                            return render_to_response ('apuadd.html',{'user': user, 'permisos': permisos_usuario, 'form': form, 'capitulos':  lista_capitulos, 'subcapitulos': lista_subcapitulos, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'suministros_apu': lista_suministros} )
                apu_proyecto.nombre_apu = form.cleaned_data['nombre']
                apu_proyecto.cantidad_proyecto = form.cleaned_data['cantidad_proyecto']
                apu_proyecto.cantidad_apu = form.cleaned_data['cantidad_apu']
                apu_proyecto.cantidad_total = apu_proyecto.cantidad_proyecto * apu_proyecto.cantidad_apu
                apu_proyecto.valor_unitario = valor_unitario
                apu_proyecto.valor_total = valor_unitario * apu_proyecto.cantidad_total
                apu_proyecto.proyecto = proyecto
                apu_proyecto.capitulo = capitulo_apu
                #try:
                    #apu_proyecto.validate_unique()
                apu_proyecto.save()
                SuministroApuProyecto.objects.filter(apu_proyecto=apu_proyecto).delete()
                for actual_suministro_apu in lista_suministros:
                    actual_suministro_apu.apu_proyecto = apu_proyecto
                    actual_suministro_apu.save()
                usuario_actual = Usuario.objects.get(id=user.id)
                direccion_ip = request.META['REMOTE_ADDR']
                registro_historial(direccion_ip, usuario_actual, u"Modificó APU proyecto, nombre: "+apu_proyecto.nombre_apu+", en proyecto: "+proyecto.nombre)
                return HttpResponseRedirect('/inverboy/home/apusproyectosearch/'+str(proyecto.id)+'/')
                #except:
                #    print 'error en campos unicos de apu'
        return render_to_response ('apumaestrodetails.html',{'user': user, 'permisos': permisos_usuario, 'form':form, 'apu': apu_proyecto, 'capitulos':  lista_capitulos, 'subcapitulos': lista_subcapitulos, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'suministros_apu': lista_suministros, 'proyecto': proyecto } )
        #return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def capitulo_apu_proyecto_change(request, proyecto_id, capitulo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'inverboy.change_capitulo'):
        permisos_usuario = user.get_all_permissions()
        try:
            proyecto = Proyecto.objects.get(id=proyecto_id)
            capitulo = CapituloApuProyecto.objects.get(tipo_capitulo=1, id=capitulo_id)
            if proyecto != capitulo.proyecto:
                return HttpResponseRedirect('/inverboy/home/')
        except:
            return HttpResponseRedirect('/inverboy/home/')
        form = CapituloApuProyectoForm(initial={'codigo': capitulo.codigo, 'nombre': capitulo.nombre_capitulo, 'estado': capitulo.estado_capitulo})
        titulo = "Modificar capitulo APU's"
        if request.method == 'POST':
            form = CapituloApuProyectoForm(request.POST)
            if form.is_valid():
                capitulos_apu_proyecto = CapituloApuProyecto.objects.filter(tipo_capitulo=1, proyecto=proyecto)
                capitulo_apu_existe = False
                if capitulo.codigo != form.cleaned_data['codigo']:
                    if capitulos_apu_proyecto.filter(Q(codigo=form.cleaned_data['codigo'])):
                        form._errors["codigo"] = ErrorList([u"El codigo ya se encuentra asignado a un capitulo del proyecto."])
                        capitulo_apu_existe = True
                nuevo_nombre = form.cleaned_data['nombre']
                nuevo_nombre = normaliza(nuevo_nombre.lower())
                if normaliza(capitulo.nombre_capitulo.lower()) != nuevo_nombre:
                    if capitulos_apu_proyecto.filter(Q(nombre_capitulo=form.cleaned_data['nombre'])):
                        form._errors["nombre"] = ErrorList([u"El nombre ya se encuentra asignado a un capitulo del proyecto."])
                        capitulo_apu_existe = True
                if capitulo_apu_existe == False:
                    capitulo.codigo = form.cleaned_data['codigo']
                    capitulo.nombre_capitulo = form.cleaned_data['nombre']
                    capitulo.estado_capitulo = form.cleaned_data['estado']
                    capitulo.save()
                    return HttpResponseRedirect('/inverboy/home/capitulosapuproyectoview/'+str(proyecto.id)+'/')
        return render_to_response('capituloapuproyectoadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form, 'titulo': titulo, 'proyecto': proyecto, 'change': True})
        #return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def subcapitulo_apu_proyecto_add(request, proyecto_id, capitulo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'inverboy.add_capitulo'):
        permisos_usuario = user.get_all_permissions()
        try:
            proyecto = Proyecto.objects.get(id=proyecto_id)
            capitulo = CapituloApuProyecto.objects.get(tipo_capitulo=1, id=capitulo_id)
            if proyecto != capitulo.proyecto:
                return HttpResponseRedirect('/inverboy/home/')
        except:
            return HttpResponseRedirect('/inverboy/home/')
        form = CapituloApuProyectoForm()
        titulo = "Nuevo capitulo APU's"
        if request.method == 'POST':
            form = CapituloApuProyectoForm(request.POST)
            if form.is_valid():
                subcapitulos_apu_proyecto = CapituloApuProyecto.objects.filter(tipo_capitulo=2, proyecto=proyecto, capitulo_asociado=capitulo)
                capitulo_apu_existe = False
                if subcapitulos_apu_proyecto.filter(Q(codigo=form.cleaned_data['codigo'])):
                    form._errors["codigo"] = ErrorList([u"El codigo ya se encuentra asignado a un subcapitulo del proyecto."])
                    capitulo_apu_existe = True
                if subcapitulos_apu_proyecto.filter(Q(nombre_capitulo=form.cleaned_data['nombre'])):
                    form._errors["nombre"] = ErrorList([u"El nombre ya se encuentra asignado a un subcapitulo del proyecto."])
                    capitulo_apu_existe = True
                if capitulo_apu_existe == False:
                    subCapitulo = CapituloApuProyecto()
                    subCapitulo.codigo = form.cleaned_data['codigo']
                    subCapitulo.nombre_capitulo = form.cleaned_data['nombre']
                    subCapitulo.tipo_capitulo = 2
                    subCapitulo.estado_capitulo = 1
                    subCapitulo.capitulo_asociado = capitulo
                    subCapitulo.proyecto = proyecto
                    subCapitulo.save()
                    return HttpResponseRedirect('/inverboy/home/subcapitulosapuproyectoview/'+str(proyecto.id)+'/'+str(capitulo.id)+'/')
        return render_to_response('subcapituloapuproyectoadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form, 'proyecto': proyecto, 'capitulo': capitulo, 'titulo': titulo })
        #return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def subcapitulos_apu_proyecto_view(request, proyecto_id, capitulo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'inverboy.view_capitulo'):
        permisos_usuario = user.get_all_permissions()
        try:
            proyecto = Proyecto.objects.get(id=proyecto_id)
            capitulo = CapituloApuProyecto.objects.get(id=capitulo_id, tipo_capitulo=1)
        except:
            return HttpResponseRedirect('/inverboy/home/')
        subcapitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=2, capitulo_asociado=capitulo, proyecto=proyecto)
        pag = Paginador(request, subcapitulos, 20, 1)
        return render_to_response('reportesubcapitulosapuproyecto.html', {'user': user, 'permisos': permisos_usuario, 'subcapitulos': pag, 'capitulo': capitulo, 'proyecto': proyecto})
        #return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def subcapitulos_apu_proyecto_search(request, proyecto_id, capitulo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'inverboy.view_capitulo'):
        permisos_usuario = user.get_all_permissions()
        try:
            proyecto = Proyecto.objects.get(id=proyecto_id)
            capitulo = CapituloApuProyecto.objects.get(id=capitulo_id)
            if proyecto != capitulo.proyecto:
                return HttpResponseRedirect('/inverboy/home/')
        except:
            return HttpResponseRedirect('/inverboy/home/')
        criterio = request.GET['criterio']
        if criterio == "":
            return HttpResponseRedirect('/inverboy/home/subcapitulosapuproyectoview/'+proyecto_id+'/'+capitulo_id+'/')
        subcapitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=2, capitulo_asociado=capitulo, proyecto=proyecto)
        try:
            criterio = int(criterio)
            subcapitulos = subcapitulos.filter(Q(codigo=criterio))
        except:
            subcapitulos = subcapitulos.filter(Q(nombre_capitulo__icontains=criterio))
        pag = Paginador(request, subcapitulos, 20, 1)
        return render_to_response('reportesubcapitulosapuproyecto.html', {'user': user, 'permisos': permisos_usuario, 'proyecto': proyecto, 'subcapitulos': pag, 'criterio': criterio, 'proyecto': proyecto, 'capitulo': capitulo })
        #return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def subcapitulo_apu_proyecto_change(request, proyecto_id, capitulo_id, subcapitulo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'inverboy.change_capitulo'):
        permisos_usuario = user.get_all_permissions()
        try:
            proyecto = Proyecto.objects.get(id=proyecto_id)
            capitulo = CapituloApuProyecto.objects.get(tipo_capitulo=1, id=capitulo_id)
            subcapitulo = CapituloApuProyecto.objects.get(tipo_capitulo=2, id=subcapitulo_id)
            if proyecto != capitulo.proyecto or proyecto != subcapitulo.proyecto or capitulo != subcapitulo.capitulo_asociado:
                return HttpResponseRedirect('/inverboy/home/')
        except:
            return HttpResponseRedirect('/inverboy/home/')
        form = CapituloApuProyectoForm(initial={'codigo': subcapitulo.codigo, 'nombre': subcapitulo.nombre_capitulo, 'estado': subcapitulo.estado_capitulo})
        titulo = "Modificar subcapitulo APU's"
        if request.method == 'POST':
            form = CapituloApuProyectoForm(request.POST)
            if form.is_valid():
                subcapitulos_apu_proyecto = CapituloApuProyecto.objects.filter(tipo_capitulo=2, proyecto=proyecto, capitulo_asociado=capitulo)
                subcapitulo_apu_existe = False
                if subcapitulo.codigo != form.cleaned_data['codigo']:
                    if subcapitulos_apu_proyecto.filter(Q(codigo=form.cleaned_data['codigo'])):
                        form._errors["codigo"] = ErrorList([u"El codigo ya se encuentra asignado a un capitulo del proyecto."])
                        subcapitulo_apu_existe = True
                nuevo_nombre = form.cleaned_data['nombre']
                nuevo_nombre = normaliza(nuevo_nombre.lower())
                if normaliza(subcapitulo.nombre_capitulo.lower()) != nuevo_nombre:
                    if subcapitulos_apu_proyecto.filter(Q(nombre_capitulo=form.cleaned_data['nombre'])):
                        form._errors["nombre"] = ErrorList([u"El nombre ya se encuentra asignado a un capitulo del proyecto."])
                        subcapitulo_apu_existe = True
                if subcapitulo_apu_existe == False:
                    subcapitulo.codigo = form.cleaned_data['codigo']
                    subcapitulo.nombre_capitulo = form.cleaned_data['nombre']
                    subcapitulo.estado_capitulo = form.cleaned_data['estado']
                    subcapitulo.save()
                    return HttpResponseRedirect('/inverboy/home/subcapitulosapuproyectoview/'+str(proyecto.id)+'/'+str(capitulo.id)+'/')
        return render_to_response('subcapituloapuproyectoadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form, 'titulo': titulo, 'proyecto': proyecto, 'capitulo': capitulo, 'change': True})
        #return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def apus_proyecto_search(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'inverboy.view_apu'):
        permisos_usuario = user.get_all_permissions()
        try:
            proyecto = Proyecto.objects.get(id = proyecto_id)
        except:
            return HttpResponseRedirect('/inverboy/home/')
        apus = ApuProyecto.objects.filter(proyecto=proyecto)
        capitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=1, estado_capitulo=1)
        lista_subcapitulos = []
        criterio = ""
        capitulo_actual = CapituloApuProyecto()
        subcapitulo_actual = CapituloApuProyecto()
        item_nulo = CapituloApuProyecto()
        item_nulo.id = 0
        item_nulo.nombre_capitulo = '----'
        form = BusquedaApuProyectoform()
        if request.method == 'POST':
            if request.POST['capitulo'] != '0':
                capitulo_actual = CapituloApuProyecto.objects.get(tipo_capitulo=1, id=request.POST['capitulo'])
                subcapitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=2, capitulo_asociado=capitulo_actual)
                lista_subcapitulos.append(item_nulo)
                for subcapitulo in subcapitulos:
                    lista_subcapitulos.append(subcapitulo)
                if request.POST['subcapitulo'] != '0':
                    subcapitulo_actual = CapituloApuProyecto.objects.get(tipo_capitulo=2, id=request.POST['subcapitulo'])
            form = BusquedaApuProyectoform(request.POST)
            if form.is_valid():
                if capitulo_actual != CapituloApuProyecto() and subcapitulo_actual == CapituloApuProyecto():
                    apus = apus.filter(Q(capitulo=capitulo_actual))
                if subcapitulo_actual != CapituloApuProyecto():
                    apus = apus.filter(Q(capitulo=subcapitulo_actual))
                if form.cleaned_data['criterio'] != '':
                    criterio = form.cleaned_data['criterio']
                    apus = apus.filter(Q(nombre_apu__icontains=criterio))
        pag = Paginador(request, apus, 1, 1)
        return render_to_response('reporteapusproyecto.html', {'user': user, 'permisos': permisos_usuario, 'form': form, 'capitulos': capitulos, 'subcapitulos': lista_subcapitulos, 'apus': pag, 'criterio': criterio, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'proyecto': proyecto })
        #return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def apus_maestro_search(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'inverboy.view_apu'):
        permisos_usuario = user.get_all_permissions()
        try:
            proyecto = Proyecto.objects.get(id=proyecto_id)
        except :
            return HttpResponseRedirect('/inverboy/home/')
        apus = Apu.objects.filter(estado_apu=1)
        capitulos = Capitulo.objects.filter(tipo_capitulo=1, estado_capitulo=1)
        lista_subcapitulos = []
        criterio = ""
        capitulo_actual = Capitulo()
        subcapitulo_actual = Capitulo()
        item_nulo = Capitulo()
        item_nulo.id = 0
        item_nulo.nombre_capitulo = '----'
        form = BusquedaApuform()
        if request.method == 'POST':
            if request.POST['capitulo'] != '0':
                capitulo_actual = Capitulo.objects.get(tipo_capitulo=1, id=request.POST['capitulo'])
                subcapitulos = Capitulo.objects.filter(tipo_capitulo=2, capitulo_asociado=capitulo_actual)
                lista_subcapitulos.append(item_nulo)
                for subcapitulo in subcapitulos:
                    lista_subcapitulos.append(subcapitulo)
                if request.POST['subcapitulo'] != '0':
                    subcapitulo_actual = Capitulo.objects.get(tipo_capitulo=2, id=request.POST['subcapitulo'])
            form = BusquedaApuform(request.POST)
            if form.is_valid():
                if subcapitulo_actual != Capitulo():
                    apus = apus.filter(Q(capitulo=subcapitulo_actual))
                if form.cleaned_data['criterio'] != '':
                    criterio = form.cleaned_data['criterio']
                    apus = apus.filter(Q(nombre_apu__icontains=criterio))
        pag = Paginador(request, apus, 1, 1)
        return render_to_response('busquedaapus.html', {'user': user, 'permisos': permisos_usuario, 'form': form, 'capitulos': capitulos, 'subcapitulos': lista_subcapitulos, 'apus': pag, 'criterio': criterio, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'proyecto': proyecto })
        #return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def apu_maestro_details(request, proyecto_id, apu_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'inverboy.change_apu'):
        permisos_usuario = user.get_all_permissions()
        try:
            proyecto = Proyecto.objects.get(id=proyecto_id)
            apu = Apu.objects.get(id=apu_id)
        except :
            return HttpResponseRedirect('/inverboy/home/')
        lista_capitulos = []
        lista_subcapitulos = []
        lista_suministros = SuministroApu.objects.filter(apu=apu)
        subcapitulo_actual = apu.capitulo
        capitulo_actual = subcapitulo_actual.capitulo_asociado
        capitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=1, estado_capitulo=1, proyecto=proyecto)
        #subcapitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=2, estado_capitulo=1, capitulo_asociado=capitulo_actual, proyecto=proyecto)
        item_nulo = Capitulo()
        item_nulo.id = 0
        item_nulo.nombre_capitulo = '----'
        lista_capitulos.append(item_nulo)
        for capitulo in capitulos:
            lista_capitulos.append(capitulo)
        #lista_subcapitulos.append(item_nulo)
        #for subcapitulo in subcapitulos:
        #    lista_subcapitulos.append(subcapitulo)
        form = ApuProyectoForm(initial={'nombre': apu.nombre_apu})
        if request.method == 'POST':
            form = ApuProyectoForm(request.POST)
            apus_existentes = []
            lista_subcapitulos = []
            if request.POST['capitulo'] != '0':
                capitulo_actual = CapituloApuProyecto.objects.get(id=request.POST['capitulo'], tipo_capitulo=1, proyecto=proyecto)
                apus_existentes = ApuProyecto.objects.filter(capitulo=capitulo_actual, proyecto=proyecto)
                subcapitulos = CapituloApuProyecto.objects.filter(capitulo_asociado=capitulo_actual, estado_capitulo=1, proyecto=proyecto)
                capitulo_apu = capitulo_actual
                if request.POST['subcapitulo'] != '0':
                    subcapitulo_actual = CapituloApuProyecto.objects.get(id=request.POST['subcapitulo'], tipo_capitulo=2, proyecto=proyecto)
                    capitulo_apu = subcapitulo_actual
                    apus_existentes = ApuProyecto.objects.filter(capitulo=subcapitulo_actual, proyecto=proyecto)
                lista_subcapitulos.append(item_nulo)
                for subcapitulo in subcapitulos:
                    lista_subcapitulos.append(subcapitulo)
            suministros = str(request.COOKIES["suministros"])
            if suministros == "":
                error = 'Debe ingresar por lo menos un suministro'
                return render_to_response ('apuadd.html',{'user': user, 'permisos': permisos_usuario, 'form':form, 'capitulos':  lista_capitulos, 'subcapitulos': lista_subcapitulos, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'error': error} )
            partes = suministros.split('--')
            contador = 0
            lista_suministros = []
            valor_unitario = 0
            while contador < len(partes)-1:
                items = partes[contador]
                item = items.split('-')
                suministro = Suministro.objects.get(id=int(item[0]))
                suministro_apu = SuministroApuProyecto()
                suministro_apu.precio_suministro = item[1]
                suministro_apu.cantidad_suministro = item[2]
                suministro_apu.cantidad_adicion = 0
                suministro_apu.precio_total = float(suministro_apu.precio_suministro) * float(suministro_apu.cantidad_suministro)
                suministro_apu.suministro = suministro
                valor_unitario = valor_unitario + float(suministro_apu.precio_suministro) * float(suministro_apu.cantidad_suministro)

                lista_suministros.append(suministro_apu)
                contador = contador+1
            if form.is_valid():
                nombre_nuevo_apu = form.cleaned_data['nombre']
                nombre_nuevo_apu = normaliza(nombre_nuevo_apu.lower())
                for apu_existente in apus_existentes:
                    if normaliza(apu_existente.nombre_apu.lower()) == nombre_nuevo_apu:
                        form._errors["nombre"] = ErrorList([u"El nombre del apu ya existe en el sistema."])
                        return rendr_to_response ('apuadd.html',{'user': user, 'permisos': permisos_usuario, 'form': form, 'capitulos':  lista_capitulos, 'subcapitulos': lista_subcapitulos, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'suministros_apu': lista_suministros} )
                apu_proyecto = ApuProyecto()
                apu_proyecto.nombre_apu = form.cleaned_data['nombre']
                apu_proyecto.unidad_medida_apu = apu.unidad_medida_apu
                apu_proyecto.cantidad_proyecto = form.cleaned_data['cantidad_proyecto']
                apu_proyecto.cantidad_apu = form.cleaned_data['cantidad_apu']
                apu_proyecto.cantidad_total = apu_proyecto.cantidad_proyecto * apu_proyecto.cantidad_apu
                apu_proyecto.valor_unitario = valor_unitario
                apu_proyecto.valor_total = valor_unitario * apu_proyecto.cantidad_total
                apu_proyecto.proyecto = proyecto
                apu_proyecto.capitulo = capitulo_apu
                #try:
                    #apu_proyecto.validate_unique()
                apu_proyecto.save()
                for actual_suministro_apu in lista_suministros:
                    actual_suministro_apu.apu_proyecto = apu_proyecto
                    #actual_suministro_apu.valor_promedio
                    actual_suministro_apu.save()
                usuario_actual = Usuario.objects.get(id=user.id)
                direccion_ip = request.META['REMOTE_ADDR']
                registro_historial(direccion_ip, usuario_actual, "Registro APU proyecto, nombre: "+apu_proyecto.nombre_apu+", en proyecto: "+proyecto.nombre)
                return HttpResponseRedirect('/inverboy/home/apusproyectosearch/'+str(proyecto.id)+'/')
                #except:
                #    print 'error en campos unicos de apu'
        return render_to_response ('apumaestrodetails.html',{'user': user, 'permisos': permisos_usuario, 'form':form, 'apu': apu, 'capitulos':  lista_capitulos, 'subcapitulos': lista_subcapitulos, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'suministros_apu': lista_suministros, 'proyecto': proyecto } )
        #return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# PETICION NUEVA REQUISICIÓN A PROYECTO
def nueva_requisicion(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        permisos_usuario = user.get_all_permissions()
        try:
            proyecto = Proyecto.objects.get(id = proyecto_id)
        except:
            return HttpResponseRedirect('/inverboy/home/')
        apus = ApuProyecto.objects.filter(proyecto=proyecto)
        capitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=1, estado_capitulo=1)
        lista_subcapitulos = []
        criterio = ""
        capitulo_actual = CapituloApuProyecto()
        subcapitulo_actual = CapituloApuProyecto()
        item_nulo = CapituloApuProyecto()
        item_nulo.id = 0
        item_nulo.nombre_capitulo = '----'
        form = BusquedaApuProyectoform()
        apus_proyecto = ApuProyecto.objects.filter(proyecto=proyecto)
        pag = Paginador(request, apus_proyecto, 20, 1)
        carrito = Carro()
        request.session['carrito'] = carrito
        return render_to_response('prueba.html', {'user': user, 'permisos': permisos_usuario, 'form': form, 'capitulos': capitulos, 'subcapitulos': lista_subcapitulos, 'apus': pag, 'criterio': criterio, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'proyecto': proyecto })
    return HttpResponseRedirect('/inverboy/')


def proyecto_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'inverboy.add_proyecto'):
        permisos_usuario = user.get_all_permissions()
        form = ProyectoForm()
        departamentos = Departamento.objects.all()
        lista_municipios = []
        departamento_actual = Departamento()
        municipio_actual = Municipio()
        if request.method == 'POST':
            form = ProyectoForm(request.POST)
            if request.POST['departamento'] != '0':
                departamento_actual = Departamento.objects.get(id=request.POST['departamento'])
                municipios = Municipio.objects.filter(departamento=departamento_actual)
                if request.POST['municipio'] != '0':
                    municipio_actual = Municipio.objects.get(id=request.POST['municipio'])
                item_nulo = Municipio()
                item_nulo.id = 0
                item_nulo.nombre = '---'
                lista_municipios.append(item_nulo)
                for municipio in municipios:
                    lista_municipios.append(municipio)

                """ PERSONAS ANEXAS
                personas_anexas = str(request.COOKIES["personas"])
                #request.set_cookie('personas','')
                print 'personas anexas :' +personas_anexas+':'
                if personas_anexas == "":
                    error = 'Debe ingresar por lo menos una persona anexa al proyecto'
                    return render_to_response ('proyectoadd.html',{'user': user, 'permisos': permisos_usuario, 'form':form, 'error': error} )
                partes = personas_anexas.split('--')
                contador = 0
                lista_personas = []
                while contador < len(partes)-1:
                    items = partes[contador]
                    item = items.split('-')
                    suministro = Suministro.objects.get(id=int(item[0]))
                    #print suministro.id
                    suministro_apu = SuministroApu()
                    suministro_apu.precio_suministro = item[1]
                    suministro_apu.cantidad_suministro = item[2]
                    suministro_apu.suministro = suministro
                    lista_suministros.append(suministro_apu)
                    contador = contador+1
            """
            if form.is_valid():
                
                proyecto = Proyecto()
                proyecto.nombre = form.cleaned_data['nombre']
                proyecto.tipo_proyecto = form.cleaned_data['tipo_proyecto']
                proyecto.direccion = form.cleaned_data['direccion']
                proyecto.municipio = form.cleaned_data['municipio']
                proyecto.ext = form.cleaned_data['ext']
                proyecto.save()
                #proyecto.director_obra = form.cleaned_data['director_obra']
                #proyecto.save()
                
                return HttpResponseRedirect('/inverboy/home/usuariosview/')
        return render_to_response('proyectoadd.html', {'user': user, 'permisos': permisos_usuario, 'form': form, 'departamentos': departamentos, 'municipios': lista_municipios, 'departamento_actual': departamento_actual, 'municipio_actual': municipio_actual,})
        #return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def proyectos_view(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'inverboy.view_apu'):
        permisos_usuario = user.get_all_permissions()
        proyectos = Proyecto.objects.all()
        pag = Paginador(request, proyectos, 20, 1)
        return render_to_response('proyectosview.html', {'user': user, 'permisos': permisos_usuario, 'proyectos': pag})
        #return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def proyecto_details(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'auth.view_group'):
        permisos_usuario = user.get_all_permissions()
        proyecto = Proyecto.objects.get(id = proyecto_id)
        return render_to_response('proyectodetails.html', {'user': user, 'permisos': permisos_usuario, 'proyecto': proyecto})
        #return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def reports(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #if validar_permiso_usuario(user.id, 'inverboy.add_proyecto'):
        permisos_usuario = user.get_all_permissions()
        return render_to_response('reports.html', {'user': user, 'permisos': permisos_usuario})
        #return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


################## FUNCIONES ##########################################

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


## FUNCION QUE DEVUELVE UNA CADENA OMITIENDO SUS ACENTOS
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


# FUNCION PARA GUARDAR EL HISTRIAL DE UN USUARIO
def registro_historial(direccion_ip, usuario, actividad):
    historial = Historial()
    historial.usuario = usuario
    historial.direccion_ip = direccion_ip
    historial.actividad = actividad
    historial.save()



# FUNCION DE PAGINACION

def get_pagination_page(page=1):
	from django.core.paginator import Paginator, InvalidPage, EmptyPage
	items = range(0,100)
	paginator = Paginator(items, 10)
	try:
		page = int(page)
	except ValueError:
		page = 1

	try:
		items = paginator.page(page)
	except (EmptyPage, InvalidPage):
		items = paginator.page(paginator.num_pages)

	return items