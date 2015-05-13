# -*- encoding: utf-8 -*-
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


#PAGINA INICIO
def home(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        usuario = Usuario.objects.get(id=user.id)
        return render_to_response('home.html', {'user': user})
    return HttpResponseRedirect('/inverboy/')


#Login
def logear(request):
    u"""Función utilizada para logearse en la plataforma via ajax.
    """
    from django.utils import simplejson
    import httpagentparser
    from django.http import HttpResponse

    if httpagentparser.detect(request.META['HTTP_USER_AGENT'])['browser']['name'] == 'Firefox' or True:
        if request.method == 'POST':
            if not request.is_ajax() and False:
                return HttpResponseRedirect('/inverboy/home/')
            username = request.POST['user'].strip()
            password = request.POST['clave'].strip()
            user = authenticate(username=username, password=password)

            error = ''
            if user is None:
                error = u'Datos no validos.'

            if user and not user.is_active:
                error = u'Usuario no activo.'

            response_data = {}
            if not error:
                login(request, user)
                direccion_ip = request.META['REMOTE_ADDR']
                usuario_actual = Usuario.objects.get(id=user.id)
                registro_historial(direccion_ip, usuario_actual, u"Inicio sesion")
                response_data['data'] = {'url': '/inverboy/home/'}
                response_data['result'] = 0
            else:
                response_data['result'] = 1
            response_data['message'] = error
            return HttpResponse(simplejson.dumps(response_data))

        import settings
        db = str(settings.DATABASES)
        db = db.split(',')
        db = db[1]
        return render_to_response('index.html', {'db':db})
    else:
        html = "<html><body>Para usar esta aplicaci&oacute;n debe usar Mozilla Firefox V.18 o superior.</body></html>"
        return HttpResponse(html)


#Cerrar sesion
def logout_view(request):
    if request.user.is_authenticated():
        user = request.user
        direccion_ip = request.META['REMOTE_ADDR']
        usuario_actual = Usuario.objects.get(id=user.id)
        registro_historial(direccion_ip, usuario_actual, u"Cerro sesion")
        logout(request)
    return HttpResponseRedirect('/inverboy/')


#Crear usuario
def usuario_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_usuario' in user.get_all_permissions():
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
                    usuario.username = form.cleaned_data['nombre_usuario'].strip()
                    try:
                        usuario.validate_unique(exclude='identificacion')
                    except:
                        form._errors["nombre_usuario"] = ErrorList([u"El nombre de usuario ya existe en el sistema."])
                    usuario.first_name = form.cleaned_data['nombres'].strip()
                    usuario.last_name = form.cleaned_data['apellidos'].strip()
                    usuario.municipio = form.cleaned_data['municipio']
                    usuario.fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
                    usuario.direccion = form.cleaned_data['direccion'].strip()
                    usuario.cargo = form.cleaned_data['cargo']
                    usuario.celular = form.cleaned_data['celular']
                    usuario.telefono = form.cleaned_data['telefono']
                    usuario.is_active = form.cleaned_data['estado']
                    usuario.set_password(form.cleaned_data['contrasena'])
                    try:
                        usuario.validate_unique()
                        usuario.save()
                        #### HASTA AQUI PASA CUANDO SE GUARDA UN USUARIO CON IDENTIFICACION MAYOR A UN NUMERO ENTERO ---- BORRAR ESTE COMMENT CUANDO SE SOLUCIONE
                        grupo_usuario = form.cleaned_data['grupo_usuario']
                        usuario.groups.add(grupo_usuario)
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, u"Registro nuevo usuario, identificacion: "+str(usuario.identificacion))
                        return HttpResponseRedirect('/inverboy/home/usuariossearch/')
                    except:
                        print 'error en campos unicos de usuario'
            return render_to_response('usuarioadd.html', {'user': user, 'form': form, 'departamentos': departamentos, 'municipios': lista_municipios, 'departamento_actual': departamento_actual, 'municipio_actual': municipio_actual, 'fecha_nacimiento': fecha_nacimiento})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar usuario
def change_usuario(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        usuario = Usuario.objects.get(id=user.id)
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
                    registro_historial(direccion_ip, usuario, u"Cambio su contraseña de usuario")
                    return HttpResponseRedirect('/inverboy/home/')
        return render_to_response('usuariochange.html', {'user': user, 'form': form, 'usuario': usuario})
    return HttpResponseRedirect('/inverboy/')


#Busqueda de usuarios
def usuarios_search(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_usuario' in user.get_all_permissions():
            lista_usuarios = Usuario.objects.all().exclude(username='administrator')
            criterio = ''
            if request.method == 'POST':
                criterio = request.POST['criterio'].strip()
                criterio = criterio.replace("'",'"')
                qry = "SELECT * FROM inverboy_usuario, auth_user WHERE user_ptr_id=id"
                try:
                    criterio = int(criterio)
                    qry = qry + " AND identificacion="+str(criterio)
                except:
                    qry = qry + " AND (CONCAT(first_name, ' ', last_name) LIKE '%%" + criterio + "%%' OR username LIKE '%%"+ criterio+"%%')"
                qry = qry + " AND (CONCAT(first_name, ' ', last_name) NOT LIKE '%%administrator%%' OR username NOT LIKE '%%administrator%%')"
                lista_usuarios = list(Usuario.objects.raw(qry))
            pag = Paginador(request, lista_usuarios, 20, 1)
            return render_to_response('reporteusuarios.html', {'user': user, 'usuarios': pag, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar usuario
def usuario_change(request, usuario_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_usuario' in user.get_all_permissions():
            usuario = Usuario.objects.get(id=usuario_id)
            grupos = usuario.groups.all()
            grupo_usuario = Group()
            try:
                grupo_usuario = grupos[0]
            except :
                pass
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
                    if usuario.identificacion != form.cleaned_data['identificacion']:
                        usuario.identificacion = form.cleaned_data['identificacion']
                        try:
                            usuario.validate_unique(exclude='username')
                        except:
                            form._errors["identificacion"] = ErrorList([u"La identificacion ya existe en el sistema."])
                    if usuario.username != form.cleaned_data['nombre_usuario']:
                        usuario.username = form.cleaned_data['nombre_usuario'].strip()
                        try:
                            usuario.validate_unique(exclude='identificacion')
                        except:
                            form._errors["nombre_usuario"] = ErrorList([u"El nombre de usuario ya existe en el sistema."])
                    usuario.first_name = form.cleaned_data['nombres'].strip()
                    usuario.last_name = form.cleaned_data['apellidos'].strip()
                    usuario.municipio = form.cleaned_data['municipio']
                    usuario.fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
                    usuario.direccion = form.cleaned_data['direccion'].strip()
                    usuario.cargo = form.cleaned_data['cargo']
                    usuario.celular = form.cleaned_data['celular']
                    usuario.telefono = form.cleaned_data['telefono']
                    usuario.is_active = form.cleaned_data['estado']
                    conservar_contrasena = form.cleaned_data['conservar_contrasena']
                    if conservar_contrasena == False:
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
                        return HttpResponseRedirect('/inverboy/home/usuariossearch/')
                    except:
                        print 'error campos unicos usuario'
            return render_to_response('usuarioadd.html', {'user': user, 'form': form, 'departamentos': departamentos, 'municipios': lista_municipios, 'departamento_actual': departamento_actual, 'municipio_actual': municipio_actual, 'fecha_nacimiento': fecha_nacimiento, 'usuario': usuario })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Crear grupo de usuario
def grupo_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'auth.add_group' in user.get_all_permissions():
            form = GrupoForm()
            if request.method == 'POST':
                form = GrupoForm(request.POST)
                if form.is_valid():
                    #grupo, created = Group.objects.get_or_create(name=form.cleaned_data['nombre_grupo'])
                    grupo = Group()
                    grupo.name = form.cleaned_data['nombre_grupo'].strip()
                    #try:
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
                    modulo_personal_administrativo_proyecto = form.cleaned_data['modulo_personal_administrativo_proyecto']
                    modulo_personal_anexo_proyecto = form.cleaned_data['modulo_personal_anexo_proyecto']
                    modulo_capitulos_apu_proyecto = form.cleaned_data['modulo_capitulos_apu_proyecto']
                    modulo_apu_proyecto = form.cleaned_data['modulo_apu_proyecto']
                    modulo_requisiciones = form.cleaned_data['modulo_requisiciones']
                    modulo_cotizaciones = form.cleaned_data['modulo_cotizaciones']
                    modulo_orden_compra = form.cleaned_data['modulo_orden_compra']
                    modulo_informe_recepcion = form.cleaned_data['modulo_informe_recepcion']
                    modulo_almacen = form.cleaned_data['modulo_almacen']
                    modulo_informe_salida = form.cleaned_data['modulo_informe_salida']
                    modulo_orden_servicio = form.cleaned_data['modulo_orden_servicio']
                    modulo_corte_diario_obra = form.cleaned_data['modulo_corte_diario_obra']
                    modulo_acta_recibo_obra = form.cleaned_data['modulo_acta_recibo_obra']
                    modulo_requisiciones_indirectos = form.cleaned_data['modulo_requisiciones_indirectos']
                    modulo_orden_giro = form.cleaned_data['modulo_orden_giro']
                    modulo_acta_conformidad = form.cleaned_data['modulo_acta_conformidad']
                    modulo_factura_orden_compra = form.cleaned_data['modulo_factura_orden_compra']
                    modulo_encuestas = form.cleaned_data['modulo_encuestas']
                    modulo_entidad_bancaria = form.cleaned_data['modulo_entidad_bancaria']
                    modulo_seccion_proyecto = form.cleaned_data['modulo_seccion_proyecto']
                    modulo_tipo_inmueble = form.cleaned_data['modulo_tipo_inmueble']
                    modulo_inmuebles = form.cleaned_data['modulo_inmuebles']
                    modulo_agrupacion_inmuebles = form.cleaned_data['modulo_agrupacion_inmuebles']
                    modulo_adicionales_agrupacion_inmueble = form.cleaned_data['modulo_adicionales_agrupacion_inmueble']
                    modulo_clientes = form.cleaned_data['modulo_clientes']
                    modulo_contrato_venta = form.cleaned_data['modulo_contrato_venta']
                    modulo_documentos_venta = form.cleaned_data['modulo_documentos_venta']
                    modulo_reporte_fotografico = form.cleaned_data['modulo_reporte_fotografico']
                    #modulo juridico
                    modulo_juridico = form.cleaned_data['modulo_juridico']
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
                    for item in modulo_personal_administrativo_proyecto:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_personal_anexo_proyecto:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_capitulos_apu_proyecto:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_apu_proyecto:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_requisiciones:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_cotizaciones:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_orden_compra:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_informe_recepcion:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_almacen:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_informe_salida:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_orden_servicio:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_corte_diario_obra:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_acta_recibo_obra:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_requisiciones_indirectos:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_orden_giro:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_acta_conformidad:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_factura_orden_compra:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_encuestas:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_entidad_bancaria:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_seccion_proyecto:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_tipo_inmueble:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_inmuebles:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_agrupacion_inmuebles:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_adicionales_agrupacion_inmueble:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_clientes:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_contrato_venta:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_documentos_venta:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    for item in modulo_reporte_fotografico:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    #modulo juridico
                    for item in modulo_juridico:
                        permiso = Permission.objects.get(codename=item)
                        grupo.permissions.add(permiso)
                    usuario_actual = Usuario.objects.get(id=user.id)
                    direccion_ip = request.META['REMOTE_ADDR']
                    registro_historial(direccion_ip, usuario_actual, "Registro nuevo grupo de usuarios, nombre: " + grupo.name)
                    return HttpResponseRedirect('/inverboy/home/grupossearch/')
                    """except:
                        form._errors["nombre_grupo"] = ErrorList([u"El grupo ya existe en el sistema."])"""
            return render_to_response('grupoadd.html', { 'user': user, 'form': form})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#BUSQUEDA GRUPOS DE USUARIO
def grupos_search(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'auth.view_group' in user.get_all_permissions():
            criterio = ''
            grupos = Group.objects.all()
            if request.method == 'POST':
                criterio = request.POST['criterio'].strip()
                grupos = grupos.filter(name__icontains=criterio)
            pag = Paginador(request, grupos, 20, 1)
            return render_to_response('reportegrupos.html', {'user': user, 'grupos': pag, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#PERMISOS DE CADA GRUPO DE USUARIO
def grupo_details(request, grupo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'auth.view_group' in user.get_all_permissions():
            grupo = Group.objects.get(id = grupo_id)
            permisos = grupo.permissions.all()
            return render_to_response('grupodetails.html', {'user': user, 'grupo': grupo, 'permisos_grupo': permisos})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#MODIFICAR GRUPO DE USUARIO
def grupo_change(request, grupo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'auth.change_group' in user.get_all_permissions():
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
            modulo_personal_administrativo_proyecto = []
            modulo_personal_anexo_proyecto = []
            modulo_capitulos_apu_proyecto = []
            modulo_apu_proyecto = []
            modulo_requisiciones = []
            modulo_cotizaciones = []
            modulo_orden_compra = []
            modulo_informe_recepcion = []
            modulo_almacen = []
            modulo_informe_salida = []
            modulo_orden_servicio = []
            modulo_corte_diario_obra = []
            modulo_acta_recibo_obra = []
            modulo_requisiciones_indirectos = []
            modulo_orden_giro = []
            modulo_acta_conformidad = []
            modulo_factura_orden_compra = []
            modulo_encuestas = []
            modulo_entidad_bancaria = []
            modulo_seccion_proyecto = []
            modulo_tipo_inmueble = []
            modulo_inmuebles = []
            modulo_agrupacion_inmuebles = []
            modulo_adicionales_agrupacion_inmueble = []
            modulo_clientes = []
            modulo_contrato_venta = []
            modulo_documentos_venta = []
            modulo_reporte_fotografico = []
            #modulo juridico
            modulo_juridico = []
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
                elif permiso.codename == 'add_personaadministrativoproyecto':
                    modulo_personal_administrativo_proyecto.append(permiso.codename)
                elif permiso.codename == 'change_personaadministrativoproyecto':
                    modulo_personal_administrativo_proyecto.append(permiso.codename)
                elif permiso.codename == 'view_personaadministrativoproyecto':
                    modulo_personal_administrativo_proyecto.append(permiso.codename)
                elif permiso.codename == 'add_personaproyecto':
                    modulo_personal_anexo_proyecto.append(permiso.codename)
                elif permiso.codename == 'change_personaproyecto':
                    modulo_personal_anexo_proyecto.append(permiso.codename)
                elif permiso.codename == 'view_personaproyecto':
                    modulo_personal_anexo_proyecto.append(permiso.codename)
                elif permiso.codename == 'add_capituloapuproyecto':
                    modulo_capitulos_apu_proyecto.append(permiso.codename)
                elif permiso.codename == 'change_capituloapuproyecto':
                    modulo_capitulos_apu_proyecto.append(permiso.codename)
                elif permiso.codename == 'view_capituloapuproyecto':
                    modulo_capitulos_apu_proyecto.append(permiso.codename)
                elif permiso.codename == 'add_apuproyecto':
                    modulo_apu_proyecto.append(permiso.codename)
                elif permiso.codename == 'change_apuproyecto':
                    modulo_apu_proyecto.append(permiso.codename)
                elif permiso.codename == 'view_apuproyecto':
                    modulo_apu_proyecto.append(permiso.codename)
                elif permiso.codename == 'add_requisicion':
                    modulo_requisiciones.append(permiso.codename)
                elif permiso.codename == 'change_requisicion':
                    modulo_requisiciones.append(permiso.codename)
                elif permiso.codename == 'view_requisicion':
                    modulo_requisiciones.append(permiso.codename)
                elif permiso.codename == 'approve_requisicion':
                    modulo_requisiciones.append(permiso.codename)
                elif permiso.codename == 'add_cotizacion':
                    modulo_cotizaciones.append(permiso.codename)
                elif permiso.codename == 'change_cotizacion':
                    modulo_cotizaciones.append(permiso.codename)
                elif permiso.codename == 'view_cotizacion':
                    modulo_cotizaciones.append(permiso.codename)
                elif permiso.codename == 'add_ordencompra':
                    modulo_orden_compra.append(permiso.codename)
                elif permiso.codename == 'change_ordencompra':
                    modulo_orden_compra.append(permiso.codename)
                elif permiso.codename == 'assignchangepermission_ordencompra':
                    modulo_orden_compra.append(permiso.codename)
                elif permiso.codename == 'view_ordencompra':
                    modulo_orden_compra.append(permiso.codename)
                elif permiso.codename == 'add_informerecepcion':
                    modulo_informe_recepcion.append(permiso.codename)
                elif permiso.codename == 'view_informerecepcion':
                    modulo_informe_recepcion.append(permiso.codename)
                elif permiso.codename == 'view_suministroalmacen':
                    modulo_almacen.append(permiso.codename)
                elif permiso.codename == 'add_informesalida':
                    modulo_informe_salida.append(permiso.codename)
                elif permiso.codename == 'view_informesalida':
                    modulo_informe_salida.append(permiso.codename)
                elif permiso.codename == 'add_ordenservicio':
                    modulo_orden_servicio.append(permiso.codename)
                elif permiso.codename == 'change_ordenservicio':
                    modulo_orden_servicio.append(permiso.codename)
                elif permiso.codename == 'assignchangepermission_ordenservicio':
                    modulo_orden_servicio.append(permiso.codename)
                elif permiso.codename == 'view_ordenservicio':
                    modulo_orden_servicio.append(permiso.codename)
                elif permiso.codename == 'add_cortediarioobra':
                    modulo_corte_diario_obra.append(permiso.codename)
                elif permiso.codename == 'view_cortediarioobra':
                    modulo_corte_diario_obra.append(permiso.codename)
                elif permiso.codename == 'add_actareciboobra':
                    modulo_acta_recibo_obra.append(permiso.codename)
                elif permiso.codename == 'change_actareciboobra':
                    modulo_acta_recibo_obra.append(permiso.codename)
                elif permiso.codename == 'view_actareciboobra':
                    modulo_acta_recibo_obra.append(permiso.codename)
                elif permiso.codename == 'approve_actareciboobra':
                    modulo_acta_recibo_obra.append(permiso.codename)
                elif permiso.codename == 'approve_cooperativaactareciboobra':
                    modulo_acta_recibo_obra.append(permiso.codename)
                elif permiso.codename == 'add_requisicionindirectos':
                    modulo_requisiciones_indirectos.append(permiso.codename)
                elif permiso.codename == 'add_ordengiro':
                    modulo_orden_giro.append(permiso.codename)
                elif permiso.codename == 'view_ordengiro':
                    modulo_orden_giro.append(permiso.codename)
                elif permiso.codename == 'add_actaconformidad':
                    modulo_acta_conformidad.append(permiso.codename)
                elif permiso.codename == 'view_actaconformidad':
                    modulo_acta_conformidad.append(permiso.codename)
                elif permiso.codename == 'add_facturaordencompra':
                    modulo_factura_orden_compra.append(permiso.codename)
                elif permiso.codename == 'view_facturaordencompra':
                    modulo_factura_orden_compra.append(permiso.codename)
                elif permiso.codename == 'add_encuesta':
                    modulo_encuestas.append(permiso.codename)
                elif permiso.codename == 'change_encuesta':
                    modulo_encuestas.append(permiso.codename)
                elif permiso.codename == 'view_encuesta':
                    modulo_encuestas.append(permiso.codename)
                elif permiso.codename == 'add_entidadbancaria':
                    modulo_entidad_bancaria.append(permiso.codename)
                elif permiso.codename == 'change_entidadbancaria':
                    modulo_entidad_bancaria.append(permiso.codename)
                elif permiso.codename == 'view_entidadbancaria':
                    modulo_entidad_bancaria.append(permiso.codename)
                elif permiso.codename == 'add_seccionproyecto':
                    modulo_seccion_proyecto.append(permiso.codename)
                elif permiso.codename == 'change_seccionproyecto':
                    modulo_seccion_proyecto.append(permiso.codename)
                elif permiso.codename == 'view_seccionproyecto':
                    modulo_seccion_proyecto.append(permiso.codename)
                elif permiso.codename == 'add_tipoinmueble':
                    modulo_tipo_inmueble.append(permiso.codename)
                elif permiso.codename == 'change_tipoinmueble':
                    modulo_tipo_inmueble.append(permiso.codename)
                elif permiso.codename == 'view_tipoinmueble':
                    modulo_tipo_inmueble.append(permiso.codename)
                elif permiso.codename == 'add_inmueble':
                    modulo_inmuebles.append(permiso.codename)
                elif permiso.codename == 'change_inmueble':
                    modulo_inmuebles.append(permiso.codename)
                elif permiso.codename == 'view_inmueble':
                    modulo_inmuebles.append(permiso.codename)
                elif permiso.codename == 'add_agrupacioninmueble':
                    modulo_agrupacion_inmuebles.append(permiso.codename)
                elif permiso.codename == 'change_agrupacioninmueble':
                    modulo_agrupacion_inmuebles.append(permiso.codename)
                elif permiso.codename == 'view_agrupacioninmueble':
                    modulo_agrupacion_inmuebles.append(permiso.codename)
                elif permiso.codename == 'add_adicionalagrupacion':
                    modulo_adicionales_agrupacion_inmueble.append(permiso.codename)
                elif permiso.codename == 'change_adicionalagrupacion':
                    modulo_adicionales_agrupacion_inmueble.append(permiso.codename)
                elif permiso.codename == 'view_adicionalagrupacion':
                    modulo_adicionales_agrupacion_inmueble.append(permiso.codename)
                elif permiso.codename == 'add_cliente':
                    modulo_clientes.append(permiso.codename)
                elif permiso.codename == 'change_cliente':
                    modulo_clientes.append(permiso.codename)
                elif permiso.codename == 'view_cliente':
                    modulo_clientes.append(permiso.codename)
                elif permiso.codename == 'add_contratoventa':
                    modulo_contrato_venta.append(permiso.codename)
                elif permiso.codename == 'change_contratoventa':
                    modulo_contrato_venta.append(permiso.codename)
                elif permiso.codename == 'view_contratoventa':
                    modulo_contrato_venta.append(permiso.codename)
                elif permiso.codename == 'assignchangepermission_contratoventa':
                    modulo_contrato_venta.append(permiso.codename)
                elif permiso.codename == 'validate_paymentcontratoventa':
                    modulo_contrato_venta.append(permiso.codename)
                elif permiso.codename == 'add_documentoventa':
                    modulo_documentos_venta.append(permiso.codename)
                elif permiso.codename == 'view_documentoventa':
                    modulo_documentos_venta.append(permiso.codename)
                elif permiso.codename == 'create_setup':
                    modulo_reporte_fotografico.append(permiso.codename)
                elif permiso.codename == 'upload_chronologicalpicture':
                    modulo_reporte_fotografico.append(permiso.codename)
                elif permiso.codename == 'delete_chronologicalpicture':
                    modulo_reporte_fotografico.append(permiso.codename)
                elif permiso.codename == 'view_stage':
                    modulo_reporte_fotografico.append(permiso.codename)
                #modulo juridico
                elif permiso.codename == 'juridico':
                    modulo_juridico.append(permiso.codename)
                elif permiso.codename == 'modificar_juridico':
                    modulo_juridico.append(permiso.codename)
            form = GrupoForm(initial={'nombre_grupo': grupo.name, 'modulo_usuarios': modulo_usuarios, 'modulo_grupos': modulo_grupos,'modulo_proveedores': modulo_proveedores, 'modulo_categorias': modulo_categorias, 'modulo_suministros': modulo_suministros, 'modulo_capitulos': modulo_capitulos, 'modulo_apu': modulo_apu, 'modulo_proyectos': modulo_proyectos, 'modulo_personal_administrativo_proyecto': modulo_personal_administrativo_proyecto, 'modulo_personal_anexo_proyecto': modulo_personal_anexo_proyecto, 'modulo_capitulos_apu_proyecto': modulo_capitulos_apu_proyecto, 'modulo_apu_proyecto': modulo_apu_proyecto, 'modulo_requisiciones': modulo_requisiciones, 'modulo_cotizaciones': modulo_cotizaciones, 'modulo_orden_compra': modulo_orden_compra, 'modulo_informe_recepcion': modulo_informe_recepcion, 'modulo_almacen': modulo_almacen, 'modulo_informe_salida': modulo_informe_salida, 'modulo_orden_servicio': modulo_orden_servicio, 'modulo_corte_diario_obra': modulo_corte_diario_obra, 'modulo_acta_recibo_obra': modulo_acta_recibo_obra, 'modulo_requisiciones_indirectos': modulo_requisiciones_indirectos, 'modulo_orden_giro': modulo_orden_giro, 'modulo_acta_conformidad': modulo_acta_conformidad, 'modulo_factura_orden_compra': modulo_factura_orden_compra, 'modulo_encuestas': modulo_encuestas, 'modulo_entidad_bancaria': modulo_entidad_bancaria, 'modulo_seccion_proyecto': modulo_seccion_proyecto, 'modulo_tipo_inmueble': modulo_tipo_inmueble, 'modulo_inmuebles': modulo_inmuebles, 'modulo_agrupacion_inmuebles': modulo_agrupacion_inmuebles, 'modulo_adicionales_agrupacion_inmueble': modulo_adicionales_agrupacion_inmueble, 'modulo_clientes': modulo_clientes, 'modulo_contrato_venta': modulo_contrato_venta, 'modulo_documentos_venta': modulo_documentos_venta, 'modulo_reporte_fotografico': modulo_reporte_fotografico, 'modulo_juridico': modulo_juridico})
            if request.method == 'POST':
                form = GrupoForm(request.POST)
                if form.is_valid():
                    try:
                        if grupo.name != form.cleaned_data['nombre_grupo']:
                            grupo.name = form.cleaned_data['nombre_grupo'].strip()
                            grupo.validate_unique()
                            grupo.save()

                        grupo.permissions.clear()
                        
                        modulo_usuarios = form.cleaned_data['modulo_usuarios']
                        modulo_grupos = form.cleaned_data['modulo_grupos']
                        modulo_proveedores = form.cleaned_data['modulo_proveedores']
                        modulo_categorias = form.cleaned_data['modulo_categorias']
                        modulo_suministros = form.cleaned_data['modulo_suministros']
                        modulo_capitulos = form.cleaned_data['modulo_capitulos']
                        modulo_apu = form.cleaned_data['modulo_apu']
                        modulo_proyectos = form.cleaned_data['modulo_proyectos']
                        modulo_personal_administrativo_proyecto = form.cleaned_data['modulo_personal_administrativo_proyecto']
                        modulo_personal_anexo_proyecto = form.cleaned_data['modulo_personal_anexo_proyecto']
                        modulo_capitulos_apu_proyecto = form.cleaned_data['modulo_capitulos_apu_proyecto']
                        modulo_apu_proyecto = form.cleaned_data['modulo_apu_proyecto']
                        modulo_requisiciones = form.cleaned_data['modulo_requisiciones']
                        modulo_cotizaciones = form.cleaned_data['modulo_cotizaciones']
                        modulo_orden_compra = form.cleaned_data['modulo_orden_compra']
                        modulo_informe_recepcion = form.cleaned_data['modulo_informe_recepcion']
                        modulo_almacen = form.cleaned_data['modulo_almacen']
                        modulo_informe_salida = form.cleaned_data['modulo_informe_salida']
                        modulo_orden_servicio = form.cleaned_data['modulo_orden_servicio']
                        modulo_corte_diario_obra = form.cleaned_data['modulo_corte_diario_obra']
                        modulo_acta_recibo_obra = form.cleaned_data['modulo_acta_recibo_obra']
                        modulo_requisiciones_indirectos = form.cleaned_data['modulo_requisiciones_indirectos']
                        modulo_orden_giro = form.cleaned_data['modulo_orden_giro']
                        modulo_acta_conformidad = form.cleaned_data['modulo_acta_conformidad']
                        modulo_factura_orden_compra = form.cleaned_data['modulo_factura_orden_compra']
                        modulo_encuestas = form.cleaned_data['modulo_encuestas']
                        modulo_entidad_bancaria = form.cleaned_data['modulo_entidad_bancaria']
                        modulo_seccion_proyecto = form.cleaned_data['modulo_seccion_proyecto']
                        modulo_tipo_inmueble = form.cleaned_data['modulo_tipo_inmueble']
                        modulo_inmuebles = form.cleaned_data['modulo_inmuebles']
                        modulo_agrupacion_inmuebles = form.cleaned_data['modulo_agrupacion_inmuebles']
                        modulo_adicionales_agrupacion_inmueble = form.cleaned_data['modulo_adicionales_agrupacion_inmueble']
                        modulo_contrato_venta = form.cleaned_data['modulo_contrato_venta']
                        modulo_clientes = form.cleaned_data['modulo_clientes']
                        modulo_documentos_venta = form.cleaned_data['modulo_documentos_venta']
                        modulo_reporte_fotografico = form.cleaned_data['modulo_reporte_fotografico']
                        #modulo juridico
                        modulo_juridico = form.cleaned_data['modulo_juridico']
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
                        for item in modulo_personal_administrativo_proyecto:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_personal_anexo_proyecto:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_capitulos_apu_proyecto:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_apu_proyecto:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_requisiciones:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_cotizaciones:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_orden_compra:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_informe_recepcion:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_almacen:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_informe_salida:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_orden_servicio:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_corte_diario_obra:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_acta_recibo_obra:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_requisiciones_indirectos:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_orden_giro:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_acta_conformidad:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_factura_orden_compra:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_encuestas:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_entidad_bancaria:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_seccion_proyecto:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_tipo_inmueble:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_inmuebles:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_agrupacion_inmuebles:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_adicionales_agrupacion_inmueble:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_clientes:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_contrato_venta:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_documentos_venta:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        for item in modulo_reporte_fotografico:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                        #Modulo juridico
                        for item in modulo_juridico:
                            permiso = Permission.objects.get(codename=item)
                            grupo.permissions.add(permiso)
                            
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, "Modifico grupo de usuario, nombre: "+grupo.name)
                        return HttpResponseRedirect('/inverboy/home/grupossearch/')
                    except:
                        form._errors["nombre_grupo"] = ErrorList([u"El grupo ya existe en el sistema."])
            return render_to_response('grupoadd.html', {'user': user, 'form': form })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


###### Modulo de sugerencias ######
#Nuevo registro buzon de sugerencias
def buzon_sugerencia_add(request):
    if request.user.is_authenticated():
        user = request.user
        form = BuzonSugerenciaForm()
        if request.method == 'POST':
            form = BuzonSugerenciaForm(request.POST)
            if form.is_valid():
                usuario = Usuario.objects.get(id=user.id)
                buzon_sugerencias = BuzonSugerencias()
                buzon_sugerencias.modulo = form.cleaned_data['modulo']
                buzon_sugerencias.observaciones = form.cleaned_data['observaciones'].strip()
                buzon_sugerencias.usuario = usuario
                buzon_sugerencias.save()
                return HttpResponseRedirect('/inverboy/home/')
        return render_to_response('buzonsugerenciaadd.html', { 'user': user, 'form': form })
    return HttpResponseRedirect('/inverboy/')


#Reporte de sugerencias
def reporte_buzon_sugerencias(request):
    if request.user.is_authenticated():
        user = request.user
        permisos = user.get_all_permissions()
        sugerencias = BuzonSugerencias.objects.filter(estado=1)
        tipo_busqueda = 1
        if request.method == 'POST':
            tipo_busqueda = int(request.POST['tipo_busqueda'])
            sugerencias = BuzonSugerencias.objects.filter(estado=tipo_busqueda)
        pag = Paginador(request, sugerencias, 20, 1)
        return render_to_response('reportesugerencias.html', {'user': user, 'permisos': permisos, 'sugerencias': pag, 'tipo_busqueda': tipo_busqueda})
    return HttpResponseRedirect('/inverboy/')


#Reporte de sugerencias
def modificar_estado_sugerencia(request, sugerencia_id, estado):
    if request.user.is_authenticated():
        sugerencia = BuzonSugerencias.objects.get(id=sugerencia_id)
        sugerencia.estado = estado
        sugerencia.save()
        return reporte_buzon_sugerencias(request)
    return HttpResponseRedirect('/inverboy/')


## NOVEDADES
def novedades(request, referencia, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        permisos = user.get_all_permissions()
        proyecto = Proyecto.objects.get(id = proyecto_id)
        #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
        usuario = Usuario.objects.get(id=user.id)
        if proyecto in usuario.lista_proyectos_vinculados():
            return render_to_response('novedades/' + referencia, {'user': user, 'permisos': permisos, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# ---- Funciones para administracion de la aplicacion ----

def comprobar_cantidades_presupuesto(request):
    for proyecto in Proyecto.objects.all():
        for apu in proyecto.apuproyecto_set.all():
            for suministro_apu in apu.suministroapuproyecto_set.all():
                # Comprueba lo requerido
                suministros_requisicion = suministro_apu.suministrorequisicion_set.filter(requisicion__estado__gte=2)
                cantidad_total_requerida = suministros_requisicion.aggregate(Sum('cantidad_requerida'))['cantidad_requerida__sum']
                if cantidad_total_requerida != None:
                    cantidad_total_requerida = round(cantidad_total_requerida, 2)
                    if cantidad_total_requerida != suministro_apu.cantidad_total_requerida:
                        grabar_script_evento_administracion('---- REQUISICIONES ----')
                        grabar_script_evento_administracion('ID SUMINISTRO: ' + str(suministro_apu.suministro.id) + ' - NOMBRE: ' + suministro_apu.suministro.nombre.encode('utf-8') + ' - APU: ' + suministro_apu.apu_proyecto.nombre_apu.encode('utf-8') + ' - PROYECTO: ' + proyecto.nombre.encode('utf-8'))
                        grabar_script_evento_administracion('CANTIDAD REQUERIDA ANTERIOR: ' + str(suministro_apu.cantidad_total_requerida))
                        grabar_script_evento_administracion('CANTIDAD REQUERIDA ACTUAL: ' + str(cantidad_total_requerida))
                        grabar_script_evento_administracion('---- REQUISICIONES ----')
                        suministro_apu.cantidad_total_requerida = cantidad_total_requerida
                        suministro_apu.save()

                # Comprueba lo comprado (OC-OS-OG)
                cantidad_comprometida = 0
                if SuministroOrdenCompra.objects.filter(suministro__suministro=suministro_apu):
                    cantidad_comprometida = SuministroOrdenCompra.objects.filter(suministro__suministro=suministro_apu).aggregate(Sum('cantidad_comprada'))['cantidad_comprada__sum']
                if SuministroOrdenServicio.objects.filter(suministro__suministro=suministro_apu):
                    if cantidad_comprometida != None:
                        cantidad_comprometida = cantidad_comprometida + SuministroOrdenServicio.objects.filter(suministro__suministro=suministro_apu).aggregate(Sum('cantidad'))['cantidad__sum']
                    else:
                        cantidad_comprometida = SuministroOrdenServicio.objects.filter(suministro__suministro=suministro_apu).aggregate(Sum('cantidad'))['cantidad__sum']
                if ItemOrdenGiro.objects.filter(suministro__suministro=suministro_apu):
                    if cantidad_comprometida != None:
                        cantidad_comprometida = cantidad_comprometida + ItemOrdenGiro.objects.filter(suministro__suministro=suministro_apu).aggregate(Sum('valor'))['valor__sum']
                    else:
                        cantidad_comprometida = ItemOrdenGiro.objects.filter(suministro__suministro=suministro_apu).aggregate(Sum('valor'))['valor__sum']
                if cantidad_comprometida != None:
                    cantidad_comprometida = round(cantidad_comprometida, 2)
                    if cantidad_comprometida != suministro_apu.cantidad_comprada:
                        grabar_script_evento_administracion('---- COMPROMETIDO ----')
                        grabar_script_evento_administracion('ID SUMINISTRO: ' + str(suministro_apu.suministro.id) + ' - NOMBRE: ' + suministro_apu.suministro.nombre.encode('utf-8') + ' - APU: ' + suministro_apu.apu_proyecto.nombre_apu.encode('utf-8') + ' - PROYECTO: ' + proyecto.nombre.encode('utf-8'))
                        grabar_script_evento_administracion('CANTIDAD COMPROMETIDA ANTERIOR: ' + str(suministro_apu.cantidad_comprada))
                        grabar_script_evento_administracion('CANTIDAD COMPROMETIDA ACTUAL: ' + str(cantidad_comprometida))
                        grabar_script_evento_administracion('---- COMPROMETIDO ----')
                        suministro_apu.cantidad_comprada = cantidad_comprometida
                        suministro_apu.save()

                # Comprueba la cantidad recibida (IR-CDO-AC)
                cantidad_ejecutada = 0
                if SuministroInformeRecepcion.objects.filter(suministro__suministro__suministro=suministro_apu):
                    cantidad_ejecutada = SuministroInformeRecepcion.objects.filter(suministro__suministro__suministro=suministro_apu).aggregate(Sum('cantidad'))['cantidad__sum']
                if SuministroCorteDiarioObra.objects.filter(suministro__suministro__suministro=suministro_apu):
                    if cantidad_ejecutada != None:
                        cantidad_ejecutada = cantidad_ejecutada + SuministroCorteDiarioObra.objects.filter(suministro__suministro__suministro=suministro_apu).aggregate(Sum('cantidad'))['cantidad__sum']
                    else:
                        cantidad_ejecutada = SuministroCorteDiarioObra.objects.filter(suministro__suministro__suministro=suministro_apu).aggregate(Sum('cantidad'))['cantidad__sum']
                if ItemActaConformidad.objects.filter(item_orden_giro__suministro__suministro=suministro_apu):
                    if cantidad_ejecutada != None:
                        cantidad_ejecutada = cantidad_ejecutada + ItemActaConformidad.objects.filter(item_orden_giro__suministro__suministro=suministro_apu).aggregate(Sum('valor'))['valor__sum']
                    else:
                        cantidad_ejecutada = ItemActaConformidad.objects.filter(item_orden_giro__suministro__suministro=suministro_apu).aggregate(Sum('valor'))['valor__sum']
                if cantidad_ejecutada != None:
                    cantidad_ejecutada = round(cantidad_ejecutada, 2)
                    if cantidad_ejecutada != suministro_apu.cantidad_almacen:
                        grabar_script_evento_administracion('---- EJECUTADO ----')
                        grabar_script_evento_administracion('ID SUMINISTRO: ' + str(suministro_apu.suministro.id) + ' - NOMBRE: ' + suministro_apu.suministro.nombre.encode('utf-8') + ' - APU: ' + suministro_apu.apu_proyecto.nombre_apu.encode('utf-8') + ' - PROYECTO: ' + proyecto.nombre.encode('utf-8'))
                        grabar_script_evento_administracion('CANTIDAD EJECUTADA ANTERIOR: ' + str(suministro_apu.cantidad_almacen))
                        grabar_script_evento_administracion('CANTIDAD EJECUTADA ACTUAL: ' + str(cantidad_ejecutada))
                        grabar_script_evento_administracion('---- EJECUTADO ----')
                        suministro_apu.cantidad_almacen = cantidad_ejecutada
                        suministro_apu.save()

                # Verificación de cantidades
                if suministro_apu.cantidad_total_requerida < suministro_apu.cantidad_comprada:
                    grabar_script_evento_administracion('---- CORREGIDO ----')
                    grabar_script_evento_administracion('ID SUMINISTRO: ' + str(suministro_apu.suministro.id) + ' - NOMBRE: ' + suministro_apu.suministro.nombre.encode('utf-8') + ' - APU: ' + suministro_apu.apu_proyecto.nombre_apu.encode('utf-8') + ' - PROYECTO: ' + proyecto.nombre.encode('utf-8'))
                    grabar_script_evento_administracion('CANTIDAD REQUERIDA ANTERIOR: ' + str(suministro_apu.cantidad_total_requerida))
                    grabar_script_evento_administracion('CANTIDAD REQUERIDA ACTUAL: ' + str(suministro_apu.cantidad_comprada))
                    grabar_script_evento_administracion('---- CORREGIDO ----')
                    suministro_apu.cantidad_total_requerida = suministro_apu.cantidad_comprada
                    suministro_apu.save()
                if suministro_apu.cantidad_comprada < suministro_apu.cantidad_almacen:
                    if suministro_apu.cantidad_total_requerida > suministro_apu.cantidad_almacen:
                        grabar_script_evento_administracion('---- CORREGIDO ----')
                        grabar_script_evento_administracion('ID SUMINISTRO: ' + str(suministro_apu.suministro.id) + ' - NOMBRE: ' + suministro_apu.suministro.nombre.encode('utf-8') + ' - APU: ' + suministro_apu.apu_proyecto.nombre_apu.encode('utf-8') + ' - PROYECTO: ' + proyecto.nombre.encode('utf-8'))
                        grabar_script_evento_administracion('CANTIDAD COMPRADA ANTERIOR: ' + str(suministro_apu.cantidad_comprada))
                        grabar_script_evento_administracion('CANTIDAD COMPRADA ACTUAL: ' + str(suministro_apu.cantidad_almacen))
                        grabar_script_evento_administracion('---- CORREGIDO ----')
                        suministro_apu.cantidad_comprada = suministro_apu.cantidad_almacen
                        suministro_apu.save()
                    else:
                        grabar_script_evento_administracion('ERROR CANTIDADES SUMINISTRO ID: ' + str(suministro_apu.suministro.id) + ' - NOMBRE: ' + suministro_apu.suministro.nombre.encode('utf-8') + ' - APU: ' + suministro_apu.apu_proyecto.nombre_apu.encode('utf-8') + ' - PROYECTO: ' + proyecto.nombre.encode('utf-8'))
    return HttpResponseRedirect('/inverboy/home/')


#Función para actualizar la tabla permisos
def actualizar_aplicacion(request):
    if request.user.is_authenticated():
        from django.contrib.contenttypes.models import ContentType
        from django.contrib.auth.models import Permission

        grabar_script_evento_administracion('---- ACTUALIZACION DE PERMISOS ----')
        #Lista de los permisos a actualizar en la tabla (insertar)
        tuplas_tabla_auth_permission = [
             #Permisos de lectura
             {'model_content_type': 'group', 'name': 'Can view group', 'codename': 'view_group'},
             {'model_content_type': 'usuario', 'name': 'Can view usuario', 'codename': 'view_usuario'},
             {'model_content_type': 'proveedor', 'name': 'Can view proveedor', 'codename': 'view_proveedor'},
             {'model_content_type': 'categoria', 'name': 'Can view categoria', 'codename': 'view_categoria'},
             {'model_content_type': 'suministro', 'name': 'Can view suministro', 'codename': 'view_suministro'},
             {'model_content_type': 'capitulo', 'name': 'Can view capitulo', 'codename': 'view_capitulo'},
             {'model_content_type': 'apu', 'name': 'Can view apu', 'codename': 'view_apu'},
             {'model_content_type': 'proyecto', 'name': 'Can view proyecto', 'codename': 'view_proyecto'},
             {'model_content_type': 'personaadministrativoproyecto', 'name': 'Can view persona administrativo proyecto', 'codename': 'view_personaadministrativoproyecto'},
             {'model_content_type': 'personaproyecto', 'name': 'Can view persona proyecto', 'codename': 'view_personaproyecto'},
             {'model_content_type': 'capituloapuproyecto', 'name': 'Can view capitulo apu proyecto', 'codename': 'view_capituloapuproyecto'},
             {'model_content_type': 'apuproyecto', 'name': 'Can view apu proyecto', 'codename': 'view_apuproyecto'},
             {'model_content_type': 'requisicion', 'name': 'Can view requisicion', 'codename': 'view_requisicion'},
             {'model_content_type': 'cotizacion', 'name': 'Can view cotizacion', 'codename': 'view_cotizacion'},
             {'model_content_type': 'ordencompra', 'name': 'Can view orden compra', 'codename': 'view_ordencompra'},
             {'model_content_type': 'informerecepcion', 'name': 'Can view informe recepcion', 'codename': 'view_informerecepcion'},
             {'model_content_type': 'suministroalmacen', 'name': 'Can view suministro almacen', 'codename': 'view_suministroalmacen'},
             {'model_content_type': 'informesalida', 'name': 'Can view informe salida', 'codename': 'view_informesalida'},
             {'model_content_type': 'ordenservicio', 'name': 'Can view orden servicio', 'codename': 'view_ordenservicio'},
             {'model_content_type': 'cortediarioobra', 'name': 'Can view corte diario obra', 'codename': 'view_cortediarioobra'},
             {'model_content_type': 'actareciboobra', 'name': 'Can view acta recibo obra', 'codename': 'view_actareciboobra'},
             {'model_content_type': 'ordengiro', 'name': 'Can view orden giro', 'codename': 'view_ordengiro'},
             {'model_content_type': 'actaconformidad', 'name': 'Can view acta conformidad', 'codename': 'view_actaconformidad'},
             {'model_content_type': 'facturaordencompra', 'name': 'Can view factura orden compra', 'codename': 'view_facturaordencompra'},
             #Permisos de aprobacion de requisiciones de suministros indirectos
             {'model_content_type': 'requisicion', 'name': 'Can approve requisicion', 'codename': 'approve_requisicion'},
             #Permisos de creacion y lectura de requisiciones de suministros indirectos
             {'model_content_type': 'requisicion', 'name': 'Can add requisicion indirectos', 'codename': 'add_requisicionindirectos'},
             #{'model_content_type': 'requisicion', 'name': 'Can view requisicion indirectos', 'codename': 'view_requisicionindirectos'}

             #Permisos de aprobacion de actas de recibo de obra
             {'model_content_type': 'actareciboobra', 'name': 'Can approve acta recibo obra', 'codename': 'approve_actareciboobra'},

             #Permisos adicionales de orden compra
             #Permiso para otorgar la modificacion de una orden compra
             {'model_content_type': 'ordencompra', 'name': 'Can assign change permission orden compra', 'codename': 'assignchangepermission_ordencompra'},

             #Permisos adicionales de orden servicio
             #Permiso para otorgar la modificacion de una orden servicio
             {'model_content_type': 'ordenservicio', 'name': 'Can assign change permission orden servicio', 'codename': 'assignchangepermission_ordenservicio'},

             #Aprobar la cantidad de dinero destinada para la cooperativa de una Acta de recibo de obra
             {'model_content_type': 'actareciboobra', 'name': 'Can approvee cooperativa acta recibo obra', 'codename': 'approve_cooperativaactareciboobra'},

             #### MODULO VENTAS ####
             {'model_content_type': 'proyecto', 'name': 'Can add documento venta', 'codename': 'add_documentoventa'},
             {'model_content_type': 'proyecto', 'name': 'Can view documento venta', 'codename': 'view_documentoventa'},
             {'model_content_type': 'encuesta', 'name': 'Can view encuesta', 'codename': 'view_encuesta'},
             {'model_content_type': 'entidadbancaria', 'name': 'Can view entidad bancaria', 'codename': 'view_entidadbancaria'},
             {'model_content_type': 'adicionalagrupacion', 'name': 'Can view adicional agrupacion', 'codename': 'view_adicionalagrupacion'},
             {'model_content_type': 'cliente', 'name': 'Can view cliente', 'codename': 'view_cliente'},
             {'model_content_type': 'seccionproyecto', 'name': 'Can view seccion proyecto', 'codename': 'view_seccionproyecto'},
             {'model_content_type': 'tipoinmueble', 'name': 'Can view tipo inmueble', 'codename': 'view_tipoinmueble'},
             {'model_content_type': 'inmueble', 'name': 'Can view inmueble', 'codename': 'view_inmueble'},
             #Permisos adicionales de inmueble
             #Permiso para otorgar la modificacion de un inmueble
             {'model_content_type': 'inmueble', 'name': 'Can assign change permission inmueble', 'codename': 'assignchangepermission_inmueble'},
             {'model_content_type': 'agrupacioninmueble', 'name': 'Can view agrupacion inmueble', 'codename': 'view_agrupacioninmueble'},
             {'model_content_type': 'contratoventa', 'name': 'Can view contrato venta', 'codename': 'view_contratoventa'},
             #Permisos adicionales de contrato venta
             #Permiso para otorgar la modificacion de un contrato venta
             {'model_content_type': 'contratoventa', 'name': 'Can assign change permission contrato venta', 'codename': 'assignchangepermission_contratoventa'},
             #Permiso para validacion de pagos en los contratos
             {'model_content_type': 'contratoventa', 'name': 'Can validate payments contrato venta', 'codename': 'validate_paymentcontratoventa'},
             #### MODULO VENTAS ####

             #### MODULO PLANES ####
             {'model_content_type': 'stage', 'name': 'Can create setup', 'codename': 'create_setup'},
             {'model_content_type': 'stage', 'name': 'Can upload chronological picture', 'codename': 'upload_chronologicalpicture'},
             {'model_content_type': 'stage', 'name': 'Can view stage', 'codename': 'view_stage'},
             #### MODULO PLANES ####
        ]

        #Verifica si los items (Modelos) anteriormente declarados exiten en la tabla "django_content_type"
        existen_items = True
        for item in tuplas_tabla_auth_permission:
            try:
                ContentType.objects.get(model=unicode(item['model_content_type']))
            except :
                existen_items = False
        if existen_items:
            for item in tuplas_tabla_auth_permission:
                try:
                    Permission.objects.get(codename=unicode(item['codename']))
                    grabar_script_evento_administracion('ERROR: EL PERMISO ' + unicode(item['codename']) + ' YA EXISTE EN EL SISTEMA.')
                except :
                    content_type = ContentType.objects.get(model=unicode(item['model_content_type']))
                    nuevo_permiso = Permission()
                    nuevo_permiso.name = unicode(item['name'])
                    nuevo_permiso.content_type = content_type
                    nuevo_permiso.codename = unicode(item['codename'])
                    nuevo_permiso.save()
                    grabar_script_evento_administracion('MSG: EL PERMISO ' + unicode(item['codename']) + ' SE HA REGISTRADO EN EL SISTEMA.')
        else:
            grabar_script_evento_administracion('ERROR: EL CONTENIDO DE LA TABLA DJANGO_Content_Type NO ESTA COMPLETO')
        grabar_script_evento_administracion('---- ACTUALIZACION DE PERMISOS - PROCESO FINALIZADO ----')

        #Actualiza las requisiciones segun el tipo = 1 - Excepto suministros indirectos, 2 - Suministros indirectos
        grabar_script_evento_administracion('---- ACTUALIZACION DE REQUISICIONES ----')
        requisiciones = Requisicion.objects.all()
        for requisicion in requisiciones:
            tipo_requisicion = 1
            for suministro in requisicion.get_suministros_agrupados():
                if suministro.suministro.suministro.clasificacion_general == 'Indirectos':
                    tipo_requisicion = 2
            requisicion.tipo_requisicion = tipo_requisicion
            requisicion.actualizar_estado()
            requisicion.save()
            grabar_script_evento_administracion('MSG: SE HA ACTUALIZADO LA REQ. ' + str(requisicion.id) + ' tipo_requisicion = ' + str(tipo_requisicion))
        grabar_script_evento_administracion('---- ACTUALIZACION DE REQUISICIONES - PROCESO FINALIZADO----')

        #Actualiza las ordenes_compra: 1-en ejecución, 2-Finalizadas
        grabar_script_evento_administracion('---- ACTUALIZACION DE ORDENES COMPRA ----')
        ordenes_compra = OrdenCompra.objects.filter(estado__in=[1,])
        for orden_compra in ordenes_compra:
            if len(orden_compra.suministroordencompra_set.filter(cantidad_facturada__lt=F('cantidad_comprada'))) == 0:
                orden_compra.estado = 2
            else:
                orden_compra.estado = 1
            orden_compra.save()
            grabar_script_evento_administracion('MSG: SE HA ACTUALIZADO LA OC. OC' + str(orden_compra.proyecto_id) + '-' + str(orden_compra.consecutivo))
        grabar_script_evento_administracion('---- ACTUALIZACION DE ORDENES DE COMPRA - PROCESO FINALIZADO----')

        #Actualiza las ordenes_servicio: 1-en ejecución, 2-Finalizadas
        grabar_script_evento_administracion('---- ACTUALIZACION DE ORDENES SERVICIO ----')
        ordenes_servicio = OrdenServicio.objects.filter(estado__in=[1, 2])
        for orden_servicio in ordenes_servicio:
            if len(orden_servicio.suministroordenservicio_set.filter(cantidad_entregada__lt=F('cantidad'))) == 0:
                orden_servicio.estado = 2
            else:
                orden_servicio.estado = 1
            orden_servicio.save()
            grabar_script_evento_administracion('MSG: SE HA ACTUALIZADO LA OS. OS' + str(orden_servicio.proyecto_id) + '-' + str(orden_servicio.consecutivo))
        grabar_script_evento_administracion('---- ACTUALIZACION DE ORDENES DE SERVICIO - PROCESO FINALIZADO----')
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def realizar_backup_grupos_usuario(request):
    if request.user.is_authenticated():
        import settings
        import os

        from xml.etree import ElementTree
        from xml.etree.ElementTree import Element
        from xml.etree.ElementTree import SubElement

        # <membership/>
        membership = Element( 'membership' )

        # <membership><groups/>
        groups = SubElement( membership, 'groups' )

        grupos_usuario = Group.objects.all()
        for grupo_usuario in grupos_usuario:
            
            # <membership><groups><group/>
            group = SubElement( groups, 'group', name=grupo_usuario.name )

            for permiso_grupo in grupo_usuario.permissions.all():
                # <membership><groups><group><user/>
                SubElement( group, 'codename', name=permiso_grupo.codename )
                #SubElement( group, 'user', name='charles' )

            # <membership><groups><group/>
            #group = SubElement( groups, 'group', name='administrators' )

            # <membership><groups><group><user/>
            #SubElement( group, 'user', name='peter' )

        output_file = open(os.path.join(settings.MEDIA_URL, 'dedalo', 'backups', 'membership.xml'), 'w')
        output_file.write( '<?xml version="1.0"?>' )
        output_file.write( ElementTree.tostring( membership ) )
        output_file.close()

        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def restaurar_backup_grupos_usuario(request):
    if request.user.is_authenticated():
        import settings
        import os

        from xml.etree import ElementTree
        #from lxml import etree

        from django.contrib.auth.models import Permission
        grabar_script_evento_administracion('---- RESTAURACION BACKUP GRUPOS DE USUARIO ----')

        with open(os.path.join(settings.MEDIA_URL, 'dedalo', 'backups', 'membership.xml'), 'rt') as f:
            document = ElementTree.parse(f)

        #document = ElementTree.parse(os.path.join(settings.MEDIA_URL, 'dedalo', 'backups', 'membership.xml'))

        #document = etree.parse(StringIO(os.path.join(settings.MEDIA_URL, 'dedalo', 'backups', 'membership.xml')))
        
        #Verifica que todos los permisos esten registrados en la tabla auth_permission
        existen_items = True
        for group in document.findall( 'groups/group' ):
            for node in group.getchildren():
                if node.tag == 'codename':
                    try:
                        Permission.objects.get(codename=unicode(node.attrib[ 'name' ]))
                    except :
                        existen_items = False
                        grabar_script_evento_administracion('ERROR: EL PERMISO ' + unicode(node.attrib[ 'name' ]) + ' NO EXISTE EN EL SISTEMA.')
        if existen_items == True:
            for group in document.findall( 'groups/group' ):
                grupo_usuario, creado = Group.objects.get_or_create(name=group.attrib[ 'name' ])
                for node in group.getchildren():
                    if node.tag == 'codename':
                        permiso = Permission.objects.get(codename=unicode(node.attrib[ 'name' ]))
                        grupo_usuario.permissions.add(permiso)
        else:
            grabar_script_evento_administracion('---- RESTAURACION BACKUP GRUPOS DE USUARIO - PROCESO NO EJECUTADO----')
        grabar_script_evento_administracion('---- RESTAURACION BACKUP GRUPOS DE USUARIO - PROCESO FINALIZADO----')
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Función para registrar eventos ocurridos en el script de actualización
def crear_archivo_texto(nombre_fichero):
    archivo = open(nombre_fichero, 'w')
    archivo.close()
    return archivo

def grabar_fichero_texto(nombre_fichero, linea=''):
    archivo = open(nombre_fichero, 'a')
    archivo.write(linea + '\n')
    archivo.close()

def grabar_script_evento_administracion(evento=''):
    import settings
    import os
    date = datetime.today()
    grabar_fichero_texto(os.path.join(settings.MEDIA_URL, 'dedalo', 'logs_administracion', 'eventos_script_administracion.txt'), str(date) + ' ' + evento)
