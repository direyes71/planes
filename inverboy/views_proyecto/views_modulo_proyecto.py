# -*- encoding: utf-8 -*-
from funciones_views import *
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission
from inverboy.models import *
from inverboy.forms import  *
from datetime import *

from inverboy.decorators import user_is_logged
from inverboy.decorators import user_has_permission
from inverboy.decorators import user_is_member_project

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

#Importar la libreria para el manejo del carrito de compras en nueva requisición
from inverboy.carrocompras import Carro

#Libreria para separador de miles
from django.contrib.humanize.templatetags.humanize import intcomma

#Libreria pdfs pisa
from django.template.loader import render_to_string
from django.template import RequestContext

# FECHA
import datetime

from settings import TIEMPO_INACTIVIDAD

from django.contrib.auth.decorators import login_required
from django.core.cache import cache

# Crear proyecto
def proyecto_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_proyecto' in user.get_all_permissions():
            form = ProyectoForm()
            if request.method == 'POST':
                form = ProyectoForm(request.POST)
                if form.is_valid():
                    proyecto = Proyecto()
                    proyecto.nombre = form.cleaned_data['nombre'].strip()
                    proyecto.iniciales = form.cleaned_data['iniciales'].strip()
                    proyecto.tipo_proyecto = form.cleaned_data['tipo_proyecto'].strip()
                    proyecto.direccion = form.cleaned_data['direccion'].strip()
                    proyecto.municipio = form.cleaned_data['municipio']
                    proyecto.ext = form.cleaned_data['ext']
                    if form.cleaned_data['rete_ica'] != None:
                        proyecto.rete_ica = form.cleaned_data['rete_ica']
                    if form.cleaned_data['rete_fuente'] != None:
                        proyecto.rete_fuente = form.cleaned_data['rete_fuente']
                    proyecto.save()
                    #Si el usuario que registra el nuevo proyecto no es superusuario agrega una nueva vinculación del usuario con el nuevo proyecto creado
                    usuario = Usuario.objects.get(id=user.id)
                    if usuario.is_superuser == False:
                        persona_administrativo_proyecto = PersonaAdministrativoProyecto()
                        persona_administrativo_proyecto.proyecto = proyecto
                        persona_administrativo_proyecto.persona = usuario
                        persona_administrativo_proyecto.save()
                    return HttpResponseRedirect('/inverboy/home/proyectodetails/' + str(proyecto.id) + '/')
            return render_to_response('proyectoadd.html', {'user': user, 'form': form})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Reporte proyectos
def proyectos_search(request):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_proyecto' in user.get_all_permissions():
            if user.is_superuser or user.is_staff:
                proyectos = Proyecto.objects.all()
            else:
                usuario = Usuario.objects.get(id=user.id)
                proyectos = usuario.lista_proyectos_vinculados()
            criterio = ''
            form = BusquedaForm()
            if request.method == 'POST':
                form = BusquedaForm(request.POST)
                if form.is_valid():
                    criterio = form.cleaned_data['criterio'].strip()
                    if criterio != '':
                        proyectos = proyectos.filter(Q(nombre__icontains=criterio))
            pag = Paginador(request, proyectos, 20, 1)
            return render_to_response('proyectosview.html', {'user': user, 'form': form, 'proyectos': pag, 'criterio': criterio })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Detalles proyecto
def proyecto_details(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_proyecto' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                ids_usuarios_administracion_proyecto = proyecto.personaadministrativoproyecto_set.filter(estado_registro=True).values('persona_id')
                usuarios_administracion_proyecto = Usuario.objects.filter(id__in=ids_usuarios_administracion_proyecto)
                personas = proyecto.personaproyecto_set.filter(estado=True)
                return render_to_response('proyectodetails.html', {'user': user, 'proyecto': proyecto, 'usuarios_administracion_proyecto': usuarios_administracion_proyecto, 'personas': personas})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar proyecto
def proyecto_change(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_proyecto' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id = proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                form = ProyectoForm(initial={'nombre': proyecto.nombre, 'iniciales': proyecto.iniciales, 'tipo_proyecto': proyecto.tipo_proyecto, 'direccion': proyecto.direccion, 'departamento': proyecto.municipio.departamento, 'municipio': proyecto.municipio, 'ext': proyecto.ext, 'rete_ica': proyecto.rete_ica, 'rete_fuente': proyecto.rete_fuente})
                if request.method == 'POST':
                    form = ProyectoForm(instance=proyecto, data=request.POST)
                    if form.is_valid():
                        proyecto.nombre = form.cleaned_data['nombre'].strip()
                        proyecto.iniciales = form.cleaned_data['iniciales'].strip()
                        proyecto.tipo_proyecto = form.cleaned_data['tipo_proyecto'].strip()
                        proyecto.direccion = form.cleaned_data['direccion'].strip()
                        proyecto.municipio = form.cleaned_data['municipio']
                        proyecto.ext = form.cleaned_data['ext']
                        if form.cleaned_data['rete_ica'] != None:
                            proyecto.rete_ica = form.cleaned_data['rete_ica']
                        if form.cleaned_data['rete_fuente'] != None:
                            proyecto.rete_fuente = form.cleaned_data['rete_fuente']
                        proyecto.save()
                        return HttpResponseRedirect('/inverboy/home/proyectodetails/' + str(proyecto_id) + '/')
                return render_to_response('proyectoadd.html', {'user': user, 'form': form, 'modificar': True})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Nueva requisición
def requisicion_add(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_requisicion' in user.get_all_permissions():
            try:
                proyecto = Proyecto.objects.get(id=proyecto_id)
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                apus = proyecto.lista_apus_sin_indirectos()
                capitulos = proyecto.capituloapuproyecto_set.filter(tipo_capitulo=1, estado_capitulo=1)
                criterio = ''
                capitulo_actual = CapituloApuProyecto()
                subcapitulo_actual = CapituloApuProyecto()
                pag = Paginador(request, apus, 20, 1)
                carrito = Carro()
                request.session['carrito'] = carrito
                return render_to_response('requisicionadd.html', {'user': user, 'capitulos': capitulos, 'apus': pag, 'criterio': criterio, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'proyecto': proyecto, 'apus_view': True, 'tipo_busqueda': 1 })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def apus_proyecto_search_requisicion_add(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_requisicion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id = proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                carrito = None
                try:
                    carrito = request.session['carrito']
                except :
                    pass
                if carrito != None:
                    apus = proyecto.lista_apus_sin_indirectos()
                    capitulos = proyecto.capituloapuproyecto_set.filter(tipo_capitulo=1, estado_capitulo=True)
                    lista_subcapitulos = []
                    criterio = ''
                    capitulo_actual = CapituloApuProyecto()
                    subcapitulo_actual = CapituloApuProyecto()
                    item_nulo = CapituloApuProyecto()
                    item_nulo.id = 0
                    item_nulo.nombre_capitulo = '----'
                    tipo_busqueda = 1
                    if request.method == 'POST':
                        tipo_busqueda = int(request.POST['tipo_busqueda'])
                        criterio = request.POST['criterio'].strip()
                        criterio = criterio.replace("'",'"')
                        if tipo_busqueda == 1:
                            if request.POST['capitulo'] != '0':
                                capitulo_actual = CapituloApuProyecto.objects.get(tipo_capitulo=1, estado_capitulo=True, id=request.POST['capitulo'])
                                subcapitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=2, estado_capitulo=True, capitulo_asociado=capitulo_actual)
                                lista_subcapitulos.append(item_nulo)
                                for subcapitulo in subcapitulos:
                                    lista_subcapitulos.append(subcapitulo)
                                if request.POST['subcapitulo'] != '0':
                                    subcapitulo_actual = CapituloApuProyecto.objects.get(tipo_capitulo=2, estado_capitulo=True, id=request.POST['subcapitulo'])
                            if capitulo_actual != CapituloApuProyecto() and subcapitulo_actual == CapituloApuProyecto():
                                apus = apus.filter(Q(capitulo=capitulo_actual))
                            if subcapitulo_actual != CapituloApuProyecto():
                                apus = apus.filter(Q(capitulo=subcapitulo_actual))
                            apus = apus.filter(Q(nombre_apu__icontains=criterio))
                        elif tipo_busqueda == 2:
                            qry = "SELECT ap.* FROM inverboy_apuproyecto ap WHERE ap.estado_apu = TRUE AND ap.proyecto_id = " + str(proyecto_id) + " AND ap.id IN (	SELECT sap.apu_proyecto_id	FROM inverboy_suministroapuproyecto sap, inverboy_suministro s	WHERE sap.suministro_id = s.id	AND s.clasificacion_general != 'Indirectos'	AND s.nombre LIKE '%%" + criterio + "%%'	GROUP BY sap.apu_proyecto_id)"
                            apus = list(proyecto.apuproyecto_set.raw(qry))
                    pag = Paginador(request, apus, 20, 1)
                    return render_to_response('requisicionadd.html', {'user': user, 'capitulos': capitulos, 'subcapitulos': lista_subcapitulos, 'apus': pag, 'criterio': criterio, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'proyecto': proyecto, 'apus_view': True, 'tipo_busqueda': tipo_busqueda })
                else:
                    return proyecto_details(request, proyecto_id)
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def apu_proyecto_details_requisicion_add(request, apu_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_requisicion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                apu = proyecto.lista_apus_sin_indirectos().get(id=apu_id)
                suministros = apu.suministroapuproyecto_set.all()
                suministros_apu = []
                carrito = None
                try:
                    carrito = request.session['carrito']
                except :
                    pass
                if carrito != None:
                    for suministro in suministros:
                        suministro_apu = {'suministro': suministro, 'cantidad_nueva_requisicion': '', 'observaciones': '' }
                        if carrito.existe_articulo(suministro.id):
                            articulo = carrito.get_articulo(suministro.id)
                            suministro_apu['cantidad_nueva_requisicion'] = articulo['cantidad']
                            suministro_apu['observaciones'] = articulo['observaciones']
                        suministros_apu.append(suministro_apu)
                    pag = Paginador(request, suministros_apu, 20, 1)
                    return render_to_response('requisicionadd.html', { 'user': user, 'apu': apu, 'suministros_apu': pag, 'proyecto': proyecto, 'apu_details': True })
                else:
                    return proyecto_details(request, proyecto_id)
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Función para buscar suministros de un APU proyecto - requisición_add
def buscar_suministros_apu_proyecto_requisicion_add(request, apu_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_requisicion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                carrito = None
                try:
                    carrito = request.session['carrito']
                except :
                    pass
                if carrito != None:
                    apu = ApuProyecto.objects.get(id=apu_id, proyecto=proyecto)
                    suministros = apu.suministroapuproyecto_set.all()
                    criterio = ''
                    if request.method == 'POST':
                        criterio = request.POST['criterio'].strip()
                        if criterio != '':
                            suministros = suministros.filter(Q(suministro__nombre__icontains=criterio) | Q(suministro__sinonimos__icontains=criterio))
                    suministros_apu = []
                    for suministro in suministros:
                        suministro_apu = {'suministro': suministro, 'cantidad_nueva_requisicion': '', 'observaciones': ''}
                        if carrito.existe_articulo(suministro.id):
                            articulo = carrito.get_articulo(suministro.id)
                            suministro_apu['cantidad_nueva_requisicion'] = articulo['cantidad']
                            suministro_apu['observaciones'] = articulo['observaciones']
                        suministros_apu.append(suministro_apu)
                    pag = Paginador(request, suministros_apu, 20, 1)
                    return render_to_response('requisicionadd.html', { 'user': user, 'apu': apu, 'suministros_apu': pag, 'criterio': criterio, 'proyecto': proyecto, 'apu_details': True })
                else:
                    return proyecto_details(request, proyecto_id)
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Detalles de la nueva requisición
def nueva_requisicion_details(request, proyecto_id):
    import datetime
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_requisicion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
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
                    fecha_arribo = ''
                    error_fecha = ''
                    error = ''
                    if request.method == 'POST':
                        fecha_arribo = request.POST['fecha_arribo']
                        error_fecha = validar_cadena(fecha_arribo)
                        if error_fecha == '':
                            error_fecha = validar_fecha(fecha_arribo)
                        if error_fecha == '':
                            partes_fecha_arribo = fecha_arribo.split('-')
                            now = datetime.datetime.now()
                            fecha_actual = date(now.year, now.month, now.day)
                            fecha_arribo = date(int(partes_fecha_arribo[0]), int(partes_fecha_arribo[1]), int(partes_fecha_arribo[2]),)
                            diff = fecha_arribo - fecha_actual
                            if diff.days < 8:
                                error_fecha = 'La fecha de arribo no puede ser menor a 8 dias'
                        if (len(suministros_requisicion) == 0):
                            error = 'No hay suministros para requerir'
                        if error_fecha == '' and error == '':
                            requisicion = Requisicion()
                            requisicion.fecha_arribo = fecha_arribo
                            requisicion.proyecto = proyecto
                            requisicion.persona = usuario
                            requisicion.save()
                            for suministro_requisicion in suministros_requisicion:
                                suministro_requisicion.requisicion = requisicion
                                #Actualización de los suministros APU proyecto (En comentarios porque se deben realizar los descuentos hasta aprobar la requisicion)
                                #suministro_requisicion.suministro.cantidad_requerida = round(suministro_requisicion.suministro.cantidad_requerida + float(suministro_requisicion.cantidad_requerida), 2)
                                #suministro_requisicion.suministro.cantidad_total_requerida = round(suministro_requisicion.suministro.cantidad_total_requerida + float(suministro_requisicion.cantidad_requerida), 2)
                                suministro_requisicion.suministro.save()
                                suministro_requisicion.save()
                            del request.session['carrito']

                            # Redirecciona a los detalles del nuevo registro
                            mensaje = u'Se ha realizado la requisición'
                            pag = Paginador(request, suministros_requisicion, 20, 1)
                            return render_to_response('requisiciondetails.html', {'user': user, 'requisicion': requisicion, 'suministros': pag, 'proyecto': proyecto, 'mensaje': mensaje})
                    pag = Paginador(request, suministros_requisicion, 20, 1)
                    now = datetime.datetime.now()
                    fecha_actual = now.strftime("%Y-%m-%d")
                    return render_to_response('requisicionadd.html', {'user': user, 'suministros_requisicion': pag, 'proyecto': proyecto, 'fecha_actual': fecha_actual, 'fecha_arribo': fecha_arribo, 'error_fecha': error_fecha, 'error': error, 'nueva_requisicion_details': True } )
                else:
                    return proyecto_details(request, proyecto_id)
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Reporte requisiciones por aprobar
def requisiciones_aprobar_proyecto_search(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_requisicion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id = proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                requisiciones = proyecto.lista_requisiciones(tipo=[1], estado=[1], criterio=criterio)
                pag = Paginador(request, requisiciones, 20, 1)
                return render_to_response('reporterequisicionesaprobar.html', {'user': user, 'requisiciones': pag, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Reporte requisiciones aprobadas y en ejecución
def requisiciones_proyecto_search(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_requisicion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id = proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                fecha_inicial = {'valor': '', 'error': ''}
                fecha_final = {'valor': '', 'error': ''}
                criterio = ''
                parametro_fecha_inicial = ''
                parametro_fecha_final = ''
                if request.method == 'POST':
                    fecha_inicial['valor'] = request.POST['fecha_inicial'].strip()
                    fecha_final['valor'] = request.POST['fecha_final'].strip()
                    criterio = request.POST['criterio'].strip()

                    if fecha_inicial['valor'] != '':
                        validaciones_fecha = Validator().append([
                            Field('fecha_inicial', fecha_inicial['valor']).append([
                                IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                            ]),
                        ]).run(True).pop()

                        if validaciones_fecha['passed'] == True:
                            parametro_fecha_inicial = fecha_inicial['valor']
                        else:
                            for error in validaciones_fecha['errors']:
                                fecha_inicial['error'] = error

                    if fecha_final['valor'] != '':
                        validaciones_fecha = Validator().append([
                            Field('fecha_final', fecha_final['valor']).append([
                                IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                            ]),
                        ]).run(True).pop()

                        if validaciones_fecha['passed'] == True:
                            parametro_fecha_final = fecha_final['valor']
                        else:
                            for error in validaciones_fecha['errors']:
                                fecha_final['error'] = error
                requisiciones = proyecto.lista_requisiciones(tipo=[1, 2], estado=[2, 3], criterio=criterio, fecha_inicial=parametro_fecha_inicial, fecha_final=parametro_fecha_final)
                pag = Paginador(request, requisiciones, 20, 1)
                return render_to_response('reporterequisiciones.html', {'user': user, 'requisiciones': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Detalles requisicion
def requisiciones_proyecto_details(request, requisicion_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_requisicion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                requisicion = proyecto.requisicion_set.get(id=requisicion_id)
                suministros = requisicion.suministrorequisicion_set.all()
                pag = Paginador(request, suministros, 20, 1)
                return render_to_response('requisiciondetails.html', {'user': user, 'requisicion': requisicion, 'suministros': pag, 'proyecto': proyecto })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar requisicion
def requisicion_proyecto_change(request, requisicion_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_requisicion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                requisicion = proyecto.requisicion_set.get(id=requisicion_id)
                if requisicion.estado == 1:
                    suministros = requisicion.suministrorequisicion_set.all()
                    error_fecha = ''
                    error = ''
                    if request.method == 'POST':
                        carrito = None
                        try:
                            carrito = request.session['carrito']
                        except :
                            pass
                        if carrito != None:
                            articulos = carrito.items()
                            fecha_arribo = request.POST['fecha_arribo']
                            error_fecha = validar_cadena(fecha_arribo)
                            if error_fecha == '':
                                error_fecha = validar_fecha(fecha_arribo)
                            if error_fecha == '':
                                partes_fecha_arribo = fecha_arribo.split('-')
                                now = datetime.datetime.now()
                                fecha_actual = date(now.year, now.month, now.day)
                                fecha_arribo = date(int(partes_fecha_arribo[0]), int(partes_fecha_arribo[1]), int(partes_fecha_arribo[2]),)
                                diff = fecha_arribo - fecha_actual
                                if diff.days < 8:
                                    error_fecha = 'La fecha de arribo no puede ser menor a 8 dias'
                            if error_fecha == '':
                                if len(articulos) > 0:
                                    #Valida que las cantidades esten disponibles en los suministros de los APU's, y elimina los suministros que se hayan quitado de la lista
                                    for suministro in suministros:
                                        eliminar_suministro = True
                                        for articulo in articulos:
                                            if suministro.suministro.id == articulo['id']:
                                                eliminar_suministro = False
                                                if (articulo['cantidad'] > suministro.suministro.cantidadDisponibleRequerir()):
                                                    error = 'Las cantidades a requerir no estan disponibles'
                                        if eliminar_suministro == True:
                                            suministro.delete()
                                    if error == '':
                                        requisicion.fecha_arribo = fecha_arribo
                                        requisicion.persona = usuario
                                        requisicion.save()
                                        for articulo in articulos:
                                            suministro_apu_proyecto = SuministroApuProyecto.objects.get(id=articulo['id'])
                                            suministro_requisicion, creado = requisicion.suministrorequisicion_set.get_or_create(suministro=suministro_apu_proyecto)
                                            suministro_requisicion.cantidad_requerida = articulo['cantidad']
                                            suministro_requisicion.observaciones = articulo['observaciones']
                                            suministro_requisicion.save()
                                        #Elimina la variable de la sesion
                                        del request.session['carrito']
                                        return HttpResponseRedirect('/inverboy/home/requisicionesproyectodetails/' + str(requisicion_id) + '/' + str(proyecto_id) + '/')
                                else:
                                    #Si se eliminaron todos los suministros 
                                    requisicion.estado = 0
                                    requisicion.save()
                                    mensaje = u'Se ha anulado la requisición'
                                    personas = proyecto.personaproyecto_set.filter(estado=True)
                                    return render_to_response('proyectodetails.html', {'user': user, 'proyecto': proyecto, 'personas': personas, 'mensaje': mensaje })
                            else:
                                lista_suministros = []
                                for articulo in articulos:
                                    for suministro in suministros:
                                        if articulo['id'] == suministro.suministro.id:
                                            suministro.cantidad_requerida = articulo['cantidad']
                                            suministro.observaciones = articulo['observaciones']
                                            lista_suministros.append(suministro)
                                suministros = lista_suministros
                        else:
                            return HttpResponseRedirect('/inverboy/home/proyectodetails/' + str(proyecto_id) + '/')
                    else:
                        carrito = Carro()
                        for suministro in suministros:
                           #Crear el articulo para agregar al carrito
                           articulo = {'observaciones': suministro.observaciones, 'id': suministro.suministro.id, 'cantidad': suministro.cantidad_requerida}
                           carrito.set_articulo(articulo)
                           request.session['carrito'] = carrito
                    pag = Paginador(request, suministros, 20, 1)
                    return render_to_response('requisicionchange.html', {'user': user, 'requisicion': requisicion, 'suministros_requisicion': pag, 'proyecto': proyecto, 'error_fecha': error_fecha, 'error': error})
                return HttpResponseRedirect('/inverboy/home/proyectodetails/' + str(proyecto_id) + '/')
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Aprobar requisicion
def requisicion_aprobar(request, requisicion_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.approve_requisicion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                requisicion = proyecto.requisicion_set.get(id=requisicion_id)
                if requisicion.estado == 1:
                    suministros_requisicion = requisicion.suministrorequisicion_set.all()
                    #Se validan las cantidades disponibles a requerir
                    cantidades_disponibles = True
                    for suministro_requisicion in suministros_requisicion:
                        if (suministro_requisicion.cantidad_requerida > suministro_requisicion.suministro.cantidadDisponibleRequerir()):
                            cantidades_disponibles = False
                    if cantidades_disponibles == True:
                        requisicion.estado = 2
                        requisicion.save()
                        #Se actualizan las cantidades en los suministros APU proyecto
                        suministros_requisicion = requisicion.suministrorequisicion_set.all()
                        for suministro_requisicion in suministros_requisicion:
                            suministro_requisicion.suministro.cantidad_requerida = round(suministro_requisicion.suministro.cantidad_requerida + float(suministro_requisicion.cantidad_requerida), 2)
                            suministro_requisicion.suministro.cantidad_total_requerida = round(suministro_requisicion.suministro.cantidad_total_requerida + float(suministro_requisicion.cantidad_requerida), 2)
                            suministro_requisicion.suministro.save()
                return HttpResponseRedirect('/inverboy/home/requisicionesproyectodetails/' + str(requisicion_id) + '/' + str(proyecto_id) + '/')
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Nueva requisición de indirectos
def requisicion_indirectos_add(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_requisicionindirectos' in user.get_all_permissions():
            try:
                proyecto = Proyecto.objects.get(id=proyecto_id)
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                apus = proyecto.lista_apus_indirectos()
                pag = Paginador(request, apus, 20, 1)
                carrito = Carro()
                request.session['carrito'] = carrito
                return render_to_response('requisicionindirectosadd.html', {'user': user, 'apus': pag, 'criterio': criterio, 'proyecto': proyecto, 'apus_view': True })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def apus_proyecto_search_requisicion_indirectos_add(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_requisicionindirectos' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id = proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                carrito = None
                try:
                    carrito = request.session['carrito']
                except :
                    pass
                if carrito != None:
                    criterio = ''
                    if request.method == 'POST':
                        criterio = request.POST['criterio'].strip()
                    apus = proyecto.lista_apus_indirectos(criterio)
                    pag = Paginador(request, apus, 20, 1)
                    return render_to_response('requisicionindirectosadd.html', {'user': user, 'apus': pag, 'criterio': criterio, 'proyecto': proyecto, 'apus_view': True})
                else:
                    return proyecto_details(request, proyecto_id)
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def apu_proyecto_details_requisicion_indirectos_add(request, apu_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_requisicionindirectos' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                carrito = None
                try:
                    carrito = request.session['carrito']
                except :
                    pass
                if carrito != None:
                    apu = proyecto.apuproyecto_set.get(id=apu_id)
                    criterio = ''
                    if request.method == 'POST':
                        criterio = request.POST['criterio'].strip()
                    suministros = apu.suministroapuproyecto_set.filter(suministro__nombre__icontains=criterio)
                    suministros_apu = []
                    for suministro in suministros:
                        suministro_apu = {'suministro': suministro, 'cantidad_nueva_requisicion': '', 'observaciones': '' }
                        if carrito.existe_articulo(suministro.id):
                            articulo = carrito.get_articulo(suministro.id)
                            suministro_apu['cantidad_nueva_requisicion'] = articulo['cantidad']
                            suministro_apu['observaciones'] = articulo['observaciones']
                        suministros_apu.append(suministro_apu)
                    pag = Paginador(request, suministros_apu, 20, 1)
                    return render_to_response('requisicionindirectosadd.html', { 'user': user, 'apu': apu, 'suministros_apu': pag, 'criterio': criterio, 'proyecto': proyecto, 'apu_details': True })
                else:
                    return proyecto_details(request, proyecto_id)
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Detalles de la nueva requisición de indirectos
def nueva_requisicion_indirectos_details(request, proyecto_id):
    import datetime
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_requisicionindirectos' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
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
                    fecha_arribo = ''
                    error_fecha = ''
                    error = ''
                    if request.method == 'POST':
                        fecha_arribo = request.POST['fecha_arribo']
                        error_fecha = validar_cadena(fecha_arribo)
                        if error_fecha == '':
                            error_fecha = validar_fecha(fecha_arribo)
                        if error_fecha == '':
                            partes_fecha_arribo = fecha_arribo.split('-')
                            now = datetime.datetime.now()
                            fecha_actual = date(now.year, now.month, now.day)
                            fecha_arribo = date(int(partes_fecha_arribo[0]), int(partes_fecha_arribo[1]), int(partes_fecha_arribo[2]),)
                            diff = fecha_arribo - fecha_actual
                            if diff.days < 8:
                                error_fecha = 'La fecha de arribo no puede ser menor a 8 dias'
                        if (len(suministros_requisicion) == 0):
                            error = 'No hay suministros para requerir'
                        if error_fecha == '' and error == '':
                            requisicion = Requisicion()
                            requisicion.fecha_arribo = fecha_arribo
                            requisicion.tipo_requisicion = 2
                            #Por default el estado de una requisición de indirectos es Aprobada (2)
                            requisicion.estado = 2
                            requisicion.proyecto = proyecto
                            requisicion.persona = usuario
                            requisicion.save()
                            for suministro_requisicion in suministros_requisicion:
                                suministro_requisicion.requisicion = requisicion
                                suministro_requisicion.suministro.cantidad_requerida = round(suministro_requisicion.suministro.cantidad_requerida + float(suministro_requisicion.cantidad_requerida), 2)
                                suministro_requisicion.suministro.cantidad_total_requerida = round(suministro_requisicion.suministro.cantidad_total_requerida + float(suministro_requisicion.cantidad_requerida), 2)
                                suministro_requisicion.suministro.save()
                                suministro_requisicion.save()
                            del request.session['carrito']

                            # Redirecciona a los detalles del nuevo registro
                            mensaje = u'Se ha realizado la requisición de indirectos'
                            pag = Paginador(request, suministros_requisicion, 20, 1)
                            return render_to_response('requisiciondetails.html', {'user': user, 'requisicion': requisicion, 'suministros': pag, 'proyecto': proyecto, 'mensaje': mensaje})
                    pag = Paginador(request, suministros_requisicion, 20, 1)
                    now = datetime.datetime.now()
                    fecha_actual = now.strftime("%Y-%m-%d")
                    return render_to_response('requisicionindirectosadd.html', {'user': user, 'suministros_requisicion': pag, 'proyecto': proyecto, 'fecha_actual': fecha_actual, 'fecha_arribo': fecha_arribo, 'error_fecha': error_fecha, 'error': error, 'nueva_requisicion_details': True } )
                else:
                    return proyecto_details(request, proyecto_id)
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Cotizacion por suministro
def compras(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_cotizacion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                pag = Paginador(request, proyecto.get_suministros_pendientes_comprar_agrupados_suministro(criterio), 20, 1)
                return render_to_response('compras.html', {'user': user, 'suministros_requisiciones': pag, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Cotizacion por proveedor
def compras_proveedor(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_cotizacion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id = proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                qry = "SELECT p.* FROM inverboy_suministroproveedor sp, inverboy_proveedor p WHERE sp.proveedor_id = p.id AND p.estado_proveedor = TRUE AND sp.suministro_id IN (	SELECT s.id	FROM inverboy_suministrorequisicion sr, inverboy_requisicion r, inverboy_suministroapuproyecto sap, inverboy_suministro s	WHERE sap.suministro_id = s.id AND sr.suministro_id = sap.id	AND sr.cantidad_comprada < sr.cantidad_requerida	AND sr.requisicion_id = r.id	AND r.proyecto_id = " + str(proyecto_id) + "    AND r.estado = 2	AND s.clasificacion_general = 'Material'	GROUP BY s.id   )"
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                    if criterio != '':
                        criterio = criterio.replace("'",'"')
                        try:
                            criterio = int(criterio)
                            qry = qry + " AND p.identificacion = " + str(criterio)
                        except:
                            qry = qry + " AND (p.razon_social LIKE '%%" + criterio + "%%' OR p.nombre_comercial LIKE '%%" + criterio +"%%')"
                qry = qry + " GROUP BY p.id ORDER BY p.razon_social"
                proveedores = Proveedor.objects.raw(qry)
                lista_proveedores = list(proveedores)
                pag = Paginador(request, lista_proveedores, 20, 1)
                return render_to_response('comprasproveedor.html', { 'user': user, 'proveedores': pag, 'criterio': criterio, 'proyecto': proyecto })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Reporte cotizaciones
def cotizaciones_proyecto_search(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_cotizacion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id = proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                cotizaciones = proyecto.lista_cotizaciones(tipo=1, criterio=criterio)
                pag = Paginador(request, cotizaciones, 20, 1)
                return render_to_response('reportecotizaciones.html', {'user': user, 'cotizaciones': pag, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')

from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder

def agregar_suministro_a_cotizacion(request):
    if request.method == "POST" and request.is_ajax():
        user=request.user
        cotizacion_id = int(request.POST['cotizacion_id'])
        suministro_id = int(request.POST['suministro_id'])
        suministro = Suministro.objects.get(pk=suministro_id)
        cotizacion = Cotizacion.objects.get(pk=cotizacion_id)
        nuevo_suministro,created =  SuministroCotizacion.objects.get_or_create(suministro=suministro,cotizacion=cotizacion)
        if cotizacion.proyecto.get_suministros_pendientes_comprar_agrupados_suministro(suministro_id=suministro.id, tipo_cotizacion=cotizacion.tipo):
            if created:
                nuevo_suministro.save()
            suministro = nuevo_suministro
            return render_to_response("ajax/fila_suministro_cotizacion_orden_compra.html",locals())
        else:
            return HttpResponse("No esta pendiente")
    return HttpResponseRedirect('/')


#### David
def agregar_suministro_a_cotizacion_opti(request):
    if request.method == "POST" and request.is_ajax():
        user=request.user
        cotizacion_id = int(request.POST['cotizacion_id'])
        suministro_id = int(request.POST['suministro_id'])
        suministro = Suministro.objects.get(pk=suministro_id)
        cotizacion = Cotizacion.objects.get(pk=cotizacion_id)
        nuevo_suministro,created =  SuministroCotizacion.objects.get_or_create(suministro=suministro,cotizacion=cotizacion)
        if cotizacion.proyecto.get_suministros_pendientes_comprar_agrupados_suministro(suministro_id=suministro.id, tipo_cotizacion=cotizacion.tipo):
            if created:
                nuevo_suministro.save()
            else:
                return HttpResponse()
            suministro = nuevo_suministro
            suministro.cantidad_req = suministro.cantidad_total_requerida_suministro_proyecto()
            # cache.delete('suministros_cotizacion_%d' % cotizacion.pk)
            suministros = cache.get('suministros_cotizacion_%d' % cotizacion.pk)
            if suministros:
                suministros = list(suministros)
                suministros.append(suministro)
                cache.set('suministros_cotizacion_%d' % cotizacion.pk,suministros)
            return render_to_response("ajax/fila_suministro_cotizacion_orden_compra_opti.html",locals())
        else:
            return HttpResponse("No esta pendiente")
    return HttpResponseRedirect('/')
####

def suministros_bajo_categoria(categoria):
    sums = list(Suministro.objects.filter(estado_suministro=True,categoria=categoria))
    categorias = Categoria.objects.filter(estado=True, categoria_asociada=categoria)
    for c in categorias:
        return sums+suministros_bajo_categoria(c)
    return sums

def parent_categoria(categoria):
    if categoria.categoria_asociada == None:
        return categoria
    return parent_categoria(categoria.categoria_asociada)

def lista_proyectos_vinculados_cache(usuario):
    # if cache.get('%d_lista_proyectos' % usuario.id):
    #     return cache.get('%d_lista_proyectos' % usuario.id)
    lista = usuario.lista_proyectos_vinculados()
    # cache.set('%d_lista_proyectos' % usuario.id,lista)
    return lista

def suministros_requeridos_organizados(cotizacion):
    # if cache.get('suministros_requeridos_%d' % cotizacion.pk):
    #     return cache.get('suministros_requeridos_%d' % cotizacion.pk)
    categorias_suministros = Categoria.objects.filter(estado=True, categoria_asociada=None)
    todos_suministros = []
    suministros_requeridos = list(cotizacion.proyecto.get_suministros_pendientes_comprar_agrupados_suministro(tipo_cotizacion=cotizacion.tipo))
    requeridos = []
    for s in suministros_requeridos:
        requeridos.append(s.suministro.suministro)
    organizado_categorias = {}
    for r in requeridos:
        if not parent_categoria(r.categoria).nombre in organizado_categorias.keys():
            organizado_categorias[parent_categoria(r.categoria).nombre] = []
        organizado_categorias[parent_categoria(r.categoria).nombre].append(r)
    for c in categorias_suministros:
        if c.nombre in organizado_categorias.keys():
            todos_suministros.append([c,organizado_categorias[c.nombre]])
    # cache.set('suministros_requeridos_%d' % cotizacion.pk,todos_suministros)
    return todos_suministros

def lista_suministro_cotizacion(cotizacion):
    if cache.get('suministros_cotizacion_%d' % cotizacion.pk):
        return cache.get('suministros_cotizacion_%d' % cotizacion.pk)
    suministros_cotizacion = cotizacion.suministrocotizacion_set.all()
    for s in suministros_cotizacion:
        s.cantidad_req = s.cantidad_total_requerida_suministro_proyecto()
    cache.set('suministros_cotizacion_%d' % cotizacion.pk,suministros_cotizacion)
    return suministros_cotizacion

@login_required(login_url='/')
def guardar_cambios_cotizacion(request):
    request.session.set_expiry(TIEMPO_INACTIVIDAD)
    user = request.user
    if 'inverboy.view_cotizacion' in user.get_all_permissions() and request.is_ajax() and request.method=='POST':
        try:
            data = simplejson.loads(request.raw_post_data)
            cotizacion = Cotizacion.objects.get(pk= int(data['cotizacion_id']))
            for s in data['suministros']:
                suministro_cotizacion = SuministroCotizacion.objects.filter(pk=int(s['suministro_pk']))
                if suministro_cotizacion:
                    suministro_cotizacion = suministro_cotizacion[0]
                    if s['eliminado'] == '1':
                        suministro_cotizacion.delete()
                    else:
                        suministro_cotizacion.cantidad_cotizada = float(s['cantidad_cotizada'])
                        suministro_cotizacion.precio=float(s['precio'])
                        suministro_cotizacion.iva_suministro=float(s['iva'])
                        suministro_cotizacion.observaciones=s['observaciones'];
                        suministro_cotizacion.save()
            cache.delete('suministros_cotizacion_%d' % cotizacion.pk)
        except Exception,e:
            print e
        return HttpResponse("Guardado")
    return HttpResponseRedirect('/inverboy/home/')



@login_required(login_url='/')
def cotizaciones_proyecto_details_opti(request,cotizacion_id,proyecto_id):
    # return cotizaciones_proyecto_details(request,cotizacion_id,proyecto_id)
    request.session.set_expiry(TIEMPO_INACTIVIDAD)
    user = request.user
    if 'inverboy.view_cotizacion' in user.get_all_permissions():
        proyecto = Proyecto.objects.get(id=proyecto_id)
        usuario = Usuario.objects.get(id=user.id)
        if proyecto in lista_proyectos_vinculados_cache(usuario):
            cotizacion = Cotizacion.objects.filter(pk=cotizacion_id,proyecto=proyecto)
            if cotizacion:
                cotizacion = cotizacion[0]
                suministros_cotizacion = lista_suministro_cotizacion(cotizacion)
                
                todos_suministros = suministros_requeridos_organizados(cotizacion)
                now = datetime.datetime.now()
                if cotizacion.tipo == 1:
                    permiso_add_ordencompra = 'inverboy.add_ordencompra' in user.get_all_permissions()
                    if request.method == 'POST':
                        fecha_arribo = request.POST['fecha_arribo'].strip()
                        forma_pago = request.POST['forma_pago'].strip()
                        parametro_pago = request.POST['parametro_pago'].strip()
                        observaciones = request.POST['observaciones'].strip()
                        if suministros_cotizacion:
                            #Valida si las cantidades de la cotización estan entre el rango de las cantidades requeridas (por cada suministro)
                            cantidades_correctas = True
                            precios_correctos = True
                            pagina = 0
                            indice = 0
                            fecha_arribo = datetime.datetime.strptime(fecha_arribo,"%Y-%m-%d").date()
                            forma_pago = int(forma_pago)
                            if forma_pago == 1:#credito
                                parametro_pago = int(parametro_pago)
                            elif forma_pago == 4:# % anticipo
                                parametro_pago = float(parametro_pago)
                            if cantidades_correctas and precios_correctos:
                                orden_compra = OrdenCompra()
                                orden_compra.fecha_arribo = fecha_arribo
                                orden_compra.forma_pago = forma_pago
                                if forma_pago == 1:
                                    orden_compra.dias_credito = parametro_pago
                                elif forma_pago == 4:
                                    orden_compra.porcentaje_anticipo = parametro_pago
                                orden_compra.observaciones = observaciones
                                orden_compra.proyecto = proyecto
                                orden_compra.proveedor = cotizacion.proveedor
                                orden_compra.persona = usuario
                                orden_compra.save()

                                # Variable para redireccionar
                                suministros_orden_compra = []
                                for suministro_cotizacion in suministros_cotizacion:
                                    suministros = proyecto.get_suministros_pendientes_comprar(suministro_id=suministro_cotizacion.suministro.id, clasificacion_general=['Material'])
                                    #Registra suministro_orden_compra_item (Objeto que guarda las propiedades generales del suministro de la compra: precio, iva y observaciones)
                                    suministro_orden_compra_item = SuministroOrdenCompraItem()
                                    suministro_orden_compra_item.orden_compra = orden_compra
                                    suministro_orden_compra_item.suministro = suministro_cotizacion.suministro
                                    suministro_orden_compra_item.precio = suministro_cotizacion.precio
                                    suministro_orden_compra_item.iva_suministro = suministro_cotizacion.iva_suministro
                                    suministro_orden_compra_item.observaciones = suministro_cotizacion.observaciones
                                    suministro_orden_compra_item.save()

                                    # Variable para redireccionar
                                    suministros_orden_compra.append(suministro_orden_compra_item)

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
                                                suministro_orden_compra = SuministroOrdenCompra()
                                                suministro_orden_compra.suministro = suministro
                                                suministro_orden_compra.cantidad_comprada = cantidad_comprada_suministro_requicision
                                                suministro_orden_compra.suministro_orden_compra_item = suministro_orden_compra_item
                                                suministro_orden_compra.orden_compra = orden_compra
                                                suministro_orden_compra.save()
                                    # Actualiza el precio del suministro correspondiente al proveedor
                                    try:
                                        suministro_proveedor = SuministroProveedor.objects.get(suministro=suministro_cotizacion.suministro, proveedor=cotizacion.proveedor)
                                        suministro_proveedor.precio_suministro = suministro_cotizacion.precio
                                        suministro_proveedor.iva_suministro = suministro_cotizacion.iva_suministro
                                    except:
                                        suministro_proveedor = SuministroProveedor(suministro=suministro_cotizacion.suministro,proveedor=cotizacion.proveedor,precio_suministro=suministro_cotizacion.precio,iva_suministro=suministro_cotizacion.iva_suministro)
                                    suministro_proveedor.save()
                                    # Borra el suministro de las cotizaciones
                                    SuministroCotizacion.objects.filter(suministro=suministro_cotizacion.suministro).delete()
                                actualizar_estado_requisiciones(proyecto)
                                actualizar_cotizaciones(proyecto)
                                # Redirecciona a los detalles del nuevo registro
                                pag = Paginador(request, suministros_orden_compra, 20, 1)
                                #return render_to_response('ordencompradetails.html', {'user': user, 'orden_compra': orden_compra, 'suministros': pag, 'proyecto': proyecto})
                                return HttpResponse('/inverboy/home/ordenescompraproyectodetails/%s/%s/' % (orden_compra.pk,proyecto_id))
                    else:
                        # Actualiza los precios del suministro de acuerdo a la ultima compra realizada con el proveedor
                        cotizacion.actualizar_precios_proveedor_uorden_compra()
                    return render_to_response('cotizacion_details_opti.html',locals(), context_instance=RequestContext(request))
                elif cotizacion.tipo == 2:
                    return cotizaciones_proyecto_details(request,cotizacion_id,proyecto_id)
    return HttpResponseRedirect('/inverboy/home/')


#Detalles cotización
def cotizaciones_proyecto_details(request, cotizacion_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_cotizacion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                cotizacion = None
                try:
                    cotizacion = proyecto.cotizacion_set.get(id=cotizacion_id)
                except :
                    pass
                if cotizacion != None:
                    suministros_cotizacion = cotizacion.suministrocotizacion_set.all()
                    categorias_suministros = Categoria.objects.filter(estado=True, categoria_asociada=None)
                    todos_suministros = []
                    suministros_requeridos = list(cotizacion.proyecto.get_suministros_pendientes_comprar_agrupados_suministro(tipo_cotizacion=cotizacion.tipo))
                    requeridos = []
                    for s in suministros_requeridos:
                        requeridos.append(s.suministro.suministro)
                    organizado_categorias = {}
                    for r in requeridos:
                        if not parent_categoria(r.categoria).nombre in organizado_categorias.keys():
                            organizado_categorias[parent_categoria(r.categoria).nombre] = []
                        organizado_categorias[parent_categoria(r.categoria).nombre].append(r)
                    for c in categorias_suministros:
                        if c.nombre in organizado_categorias.keys():
                            todos_suministros.append([c,organizado_categorias[c.nombre]])
                    
                    #Parametro fecha actual orden_compra-orden_servicio
                    now = datetime.datetime.now()
                    fecha_actual = now.strftime("%Y-%m-%d")
                    #Error común (ordenes_compra-ordenes_servicio)
                    error = ''
                    #Parametros comunes cotización (ordenes_compra-ordenes_servicio)
                    fecha_arribo = ''
                    forma_pago = ''
                    parametro_pago = ''
                    observaciones = ''
                    #Errores comunes cotización (ordenes_compra-ordenes_servicio)
                    error_fecha_arribo = ''
                    error_forma_pago = ''
                    error_parametro_pago = ''
                    if cotizacion.tipo == 1:
                        #cotizacion orden de servicio
                        if request.method == 'POST':
                            fecha_arribo = request.POST['fecha_arribo'].strip()
                            forma_pago = request.POST['forma_pago'].strip()
                            parametro_pago = request.POST['parametro_pago'].strip()
                            observaciones = request.POST['observaciones'].strip()
                            if len(suministros_cotizacion) > 0:
                                #Valida si las cantidades de la cotización estan entre el rango de las cantidades requeridas (por cada suministro)
                                cantidades_correctas = True
                                for suministro_cotizacion in suministros_cotizacion:
                                    cantidad_requerida = suministro_cotizacion.cantidad_total_requerida_suministro_proyecto().cantidad_requerida
                                    if (suministro_cotizacion.cantidad_cotizada <= 0) or (suministro_cotizacion.cantidad_cotizada > cantidad_requerida):
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
                                    error = u'Revise las cantidades deben ser mayores a 0, pero menores que la cantidad requerida'
                                if error == '':
                                    if precios_correctos == False:
                                        error = u'Revise los precios, deben ser mayores a 0'

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

                                if forma_pago not in ['1', '2', '3', '4']:
                                    error_forma_pago = 'Campo obligatorio'

                                if error_forma_pago == '':
                                    forma_pago = int(forma_pago)
                                    if forma_pago == 1:
                                        error_parametro_pago = validar_cadena(parametro_pago)
                                        if error_parametro_pago == '':
                                            error_parametro_pago = validar_cantidad_int(parametro_pago)
                                            if error_parametro_pago == '':
                                                parametro_pago = int(parametro_pago)
                                                error_parametro_pago = validar_cantidad_int_0(parametro_pago)
                                                if error_parametro_pago == '':
                                                    error_parametro_pago = validar_int_digitos(parametro_pago, 3)
                                    elif forma_pago == 4:
                                        error_parametro_pago = validar_cadena(parametro_pago)
                                        if error_parametro_pago == '':
                                            error_parametro_pago = validar_cantidad_float(parametro_pago)
                                            if error_parametro_pago == '':
                                                parametro_pago = float(parametro_pago)
                                                error_parametro_pago = validar_cantidad_float_0(parametro_pago)
                                                if error_parametro_pago == '':
                                                    if parametro_pago > 100:
                                                        error_parametro_pago = u'El porcentaje no debe ser mayor a 100'
                                    elif forma_pago == 2 or forma_pago == 3:
                                        pass

                                if cantidades_correctas == True and precios_correctos == True and error_fecha_arribo == '' and error_forma_pago == '' and error_parametro_pago == '':

                                    orden_compra = OrdenCompra()
                                    orden_compra.fecha_arribo = fecha_arribo
                                    orden_compra.forma_pago = forma_pago
                                    if forma_pago == 1:
                                        orden_compra.dias_credito = parametro_pago
                                    elif forma_pago == 4:
                                        orden_compra.porcentaje_anticipo = parametro_pago
                                    orden_compra.observaciones = observaciones
                                    orden_compra.proyecto = proyecto
                                    orden_compra.proveedor = cotizacion.proveedor
                                    orden_compra.persona = usuario
                                    orden_compra.save()

                                    # Variable para redireccionar
                                    suministros_orden_compra = []
                                    for suministro_cotizacion in suministros_cotizacion:
                                        suministros = proyecto.get_suministros_pendientes_comprar(suministro_id=suministro_cotizacion.suministro.id, clasificacion_general=['Material'])
                                        #Registra suministro_orden_compra_item (Objeto que guarda las propiedades generales del suministro de la compra: precio, iva y observaciones)
                                        suministro_orden_compra_item = SuministroOrdenCompraItem()
                                        suministro_orden_compra_item.orden_compra = orden_compra
                                        suministro_orden_compra_item.suministro = suministro_cotizacion.suministro
                                        suministro_orden_compra_item.precio = suministro_cotizacion.precio
                                        suministro_orden_compra_item.iva_suministro = suministro_cotizacion.iva_suministro
                                        suministro_orden_compra_item.observaciones = suministro_cotizacion.observaciones
                                        suministro_orden_compra_item.save()

                                        # Variable para redireccionar
                                        suministros_orden_compra.append(suministro_orden_compra_item)

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
                                                    suministro_orden_compra = SuministroOrdenCompra()
                                                    suministro_orden_compra.suministro = suministro
                                                    suministro_orden_compra.cantidad_comprada = cantidad_comprada_suministro_requicision
                                                    suministro_orden_compra.suministro_orden_compra_item = suministro_orden_compra_item
                                                    suministro_orden_compra.orden_compra = orden_compra
                                                    suministro_orden_compra.save()
                                        # Actualiza el precio del suministro correspondiente al proveedor
                                        try:
                                            suministro_proveedor = SuministroProveedor.objects.get(suministro=suministro_cotizacion.suministro, proveedor=cotizacion.proveedor)
                                            suministro_proveedor.precio_suministro = suministro_cotizacion.precio
                                            suministro_proveedor.iva_suministro = suministro_cotizacion.iva_suministro
                                        except:
                                            suministro_proveedor = SuministroProveedor(suministro=suministro_cotizacion.suministro,proveedor=cotizacion.proveedor,precio_suministro=suministro_cotizacion.precio,iva_suministro=suministro_cotizacion.iva_suministro)
                                        suministro_proveedor.save()
                                        # Borra el suministro de las cotizaciones
                                        SuministroCotizacion.objects.filter(suministro=suministro_cotizacion.suministro).delete()
                                    actualizar_estado_requisiciones(proyecto)
                                    actualizar_cotizaciones(proyecto)

                                    # Redirecciona a los detalles del nuevo registro
                                    mensaje = u'Se ha realizado la orden de compra'
                                    pag = Paginador(request, suministros_orden_compra, 20, 1)
                                    return render_to_response('ordencompradetails.html', {'user': user, 'orden_compra': orden_compra, 'suministros': pag, 'proyecto': proyecto, 'mensaje': mensaje})
                                if precios_correctos == False:
                                    error = u'Hay precios con valor 0'
                                    pag = Paginador(request, suministros_cotizacion, 20, pagina)
                                else:
                                    pag = Paginador(request, suministros_cotizacion, 20, 1)
                            else:
                                actualizar_cotizaciones(proyecto)
                                mensaje = u'La cotización se ha eliminado'
                                personas = proyecto.personaproyecto_set.filter(estado=True)
                                return render_to_response('proyectodetails.html', {'user': user, 'proyecto': proyecto, 'personas': personas, 'mensaje': mensaje })
                        else:
                            # Actualiza los precios del suministro de acuerdo a la ultima compra realizada con el proveedor
                            cotizacion.actualizar_precios_proveedor_uorden_compra()
                            pag = Paginador(request, suministros_cotizacion, 20, 1)
                        return render_to_response('cotizaciondetails.html', {'todos_suministros':todos_suministros,'user': user, 'cotizacion': cotizacion, 'proyecto': proyecto, 'suministros': pag, 'fecha_actual': fecha_actual, 'fecha_arribo': fecha_arribo, 'forma_pago': forma_pago, 'parametro_pago': str(parametro_pago), 'observaciones': observaciones, 'error': error, 'error_fecha_arribo': error_fecha_arribo, 'error_forma_pago': error_forma_pago, 'error_parametro_pago': error_parametro_pago })
                    elif cotizacion.tipo == 2:
                        aplica_tercero = False
                        aplica_cooperativa = False
                        base_gravable_cooperativa = ''
                        porcentaje_iva_cooperativa = ''
                        amortizacion_anticipo = ''
                        retencion_garantia = ''
                        rete_ica = ''
                        rete_fuente = ''
                        tipo_iva = ''
                        a_i_u = ''
                        utilidad = ''
                        iva = ''
                        tercero = Proveedor()
                        terceros = []
                        error_amortizacion_anticipo = ''
                        error_retencion_garantia = ''
                        error_rete_ica = ''
                        error_rete_fuente = ''
                        error_a_i_u = ''
                        error_utilidad = ''
                        error_iva = ''
                        error_tercero = ''
                        error_base_gravable_cooperativa = ''
                        error_porcentaje_iva_cooperativa = ''
                        if proyecto.rete_ica != 0:
                            rete_ica = proyecto.rete_ica
                        if proyecto.rete_fuente != 0:
                            rete_fuente = proyecto.rete_fuente
                        if request.method == 'POST':
                            fecha_arribo = request.POST['fecha_arribo'].strip()
                            amortizacion_anticipo = request.POST['amortizacion_anticipo'].strip()
                            retencion_garantia = request.POST['retencion_garantia'].strip()
                            rete_ica = request.POST['rete_ica'].strip()
                            rete_fuente = request.POST['rete_fuente'].strip()
                            forma_pago = request.POST['forma_pago'].strip()
                            parametro_pago = request.POST['parametro_pago'].strip()
                            observaciones = request.POST['observaciones'].strip()

                            try:
                                aplica_tercero = request.POST['aplica_tercero']
                            except :
                                pass
                            tercero_id = request.POST['tercero']

                            try:
                                aplica_cooperativa = request.POST['aplica_cooperativa']
                            except :
                                pass
                            base_gravable_cooperativa = request.POST['base_gravable_cooperativa'].strip()
                            porcentaje_iva_cooperativa = request.POST['porcentaje_iva_cooperativa'].strip()

                            if cotizacion.proveedor.regimen_tributario == 1:
                                tipo_iva = int(request.POST['tipo_iva'])
                                iva = request.POST['iva'].strip()
                                if tipo_iva == 1:
                                    a_i_u = request.POST['a_i_u'].strip()
                                    utilidad = request.POST['utilidad'].strip()
                                if tipo_iva == 3:
                                    a_i_u = request.POST['a_i_u'].strip()
                                    
                            if len(suministros_cotizacion) > 0:
                                cantidades_correctas = True
                                for suministro_cotizacion in suministros_cotizacion:
                                    cantidad_requerida = suministro_cotizacion.cantidad_total_requerida_suministro_proyecto().cantidad_requerida
                                    if (suministro_cotizacion.cantidad_cotizada <= 0) or (suministro_cotizacion.cantidad_cotizada > cantidad_requerida):
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
                                    error = u'Revise las cantidades deben ser mayores a 0, pero menores que la cantidad requerida'
                                if error == '':
                                    if precios_correctos == False:
                                        error = u'Revise los precios, deben ser mayores a 0'
                                if fecha_arribo == '':
                                    error_fecha_arribo = u'Campo obligatorio'
                                if error_fecha_arribo == '':
                                    error_fecha_arribo = validar_fecha(fecha_arribo)
                                if error_fecha_arribo == '':
                                    partes_fecha_arribo = fecha_arribo.split('-')
                                    now = datetime.datetime.now()
                                    fecha_actual = date(now.year, now.month, now.day)
                                    fecha_arribo = date(int(partes_fecha_arribo[0]), int(partes_fecha_arribo[1]), int(partes_fecha_arribo[2]),)
                                    diff = fecha_arribo - fecha_actual
                                    if diff.days < 0:
                                        error_fecha_arribo = u'La fecha de arribo para la orden de compra no debe ser menor a la fecha actual'

                                error_forma_pago = ''
                                if forma_pago not in ['1', '2', '3', '4']:
                                    error_forma_pago = u'Campo obligatorio'

                                error_parametro_pago = ''

                                if error_forma_pago == '':
                                    forma_pago = int(forma_pago)
                                    if forma_pago == 4:
                                        error_parametro_pago = validar_cadena(parametro_pago)
                                    elif forma_pago == 1 or forma_pago == 2 or forma_pago == 3:
                                        pass

                                error_amortizacion_anticipo = validar_cadena(amortizacion_anticipo)
                                if error_amortizacion_anticipo == '':
                                    if error_amortizacion_anticipo == '':
                                        error_amortizacion_anticipo = validar_cantidad_float_digitos(amortizacion_anticipo)
                                        if error_amortizacion_anticipo == '':
                                            error_amortizacion_anticipo = validar_cantidad_float(amortizacion_anticipo)
                                            if error_amortizacion_anticipo == '':
                                                error_amortizacion_anticipo = validar_cantidad_float_negativo(amortizacion_anticipo)
                                                if error_amortizacion_anticipo == '':
                                                    if float(amortizacion_anticipo) > 100:
                                                        error_amortizacion_anticipo =  u'No debe ser un valor mayor a 100'

                                error_retencion_garantia = validar_cadena(retencion_garantia)
                                if error_retencion_garantia == '':
                                    error_retencion_garantia = validar_cantidad_float_digitos(retencion_garantia)
                                    if error_retencion_garantia == '':
                                        error_retencion_garantia = validar_cantidad_float(retencion_garantia)
                                        if error_retencion_garantia == '':
                                            error_retencion_garantia = validar_cantidad_float_negativo(retencion_garantia)
                                            if error_retencion_garantia == '':
                                                if float(retencion_garantia) > 100:
                                                    error_retencion_garantia = u'No debe ser un valor mayor a 100'


                                error_rete_ica = validar_cadena(rete_ica)
                                if error_rete_ica == '':
                                    error_rete_ica = validar_cantidad_float_digitos(rete_ica)
                                    if error_rete_ica == '':
                                        error_rete_ica = validar_cantidad_float(rete_ica)
                                        if error_rete_ica == '':
                                            error_rete_ica = validar_cantidad_float_negativo(rete_ica)
                                            if error_rete_ica == '':
                                                if float(rete_ica) > 100:
                                                    error_rete_ica = u'No debe ser un valor mayor a 100'

                                error_rete_fuente = validar_cadena(rete_fuente)
                                if error_rete_fuente == '':
                                    error_rete_fuente = validar_cantidad_float_digitos(rete_fuente)
                                    if error_rete_fuente == '':
                                        error_rete_fuente = validar_cantidad_float(rete_fuente)
                                        if error_rete_fuente == '':
                                            error_rete_fuente = validar_cantidad_float_negativo(rete_fuente)
                                            if error_rete_fuente == '':
                                                if float(rete_fuente) > 100:
                                                    error_rete_fuente = u'No debe ser un valor mayor a 100'

                                if cotizacion.proveedor.regimen_tributario == 1:
                                    error_iva = validar_cadena(iva)
                                    if error_iva == '':
                                        error_iva = validar_cantidad_float_digitos(iva)
                                        if error_iva == '':
                                            error_iva = validar_cantidad_float(iva)
                                            if error_iva == '':
                                                # Verifica si el tipo_iva = 2 (% de iva), si es asi el porcentaje de iva puede ser 0
                                                if tipo_iva == 2:
                                                    error_iva = validar_cantidad_float_negativo(iva)
                                                else:
                                                    error_iva = validar_cantidad_float_0(iva)
                                                if error_iva == '':
                                                    if float(iva) > 100:
                                                        error_iva = u'No debe ser un valor mayor a 100'
                                                        
                                    if tipo_iva == 1:
                                        error_a_i_u = validar_cadena(a_i_u)
                                        if error_a_i_u == '':
                                            error_a_i_u = validar_cantidad_float_digitos(a_i_u)
                                            if error_a_i_u == '':
                                                error_a_i_u = validar_cantidad_float(a_i_u)
                                                if error_a_i_u == '':
                                                    error_a_i_u = validar_cantidad_float_0(a_i_u)
                                                    if error_a_i_u == '':
                                                        if float(a_i_u) > 100:
                                                            error_a_i_u = u'No debe ser un valor mayor a 100'

                                        error_utilidad = validar_cadena(utilidad)
                                        if error_utilidad == '':
                                            error_utilidad = validar_cantidad_float_digitos(utilidad)
                                            if error_utilidad == '':
                                                error_utilidad = validar_cantidad_float(utilidad)
                                                if error_utilidad == '':
                                                    error_utilidad = validar_cantidad_float_0(utilidad)
                                                    if error_utilidad == '':
                                                        if float(utilidad) > 100:
                                                            error_utilidad = u'No debe ser un valor mayor a 100'

                                    elif tipo_iva == 3:
                                        error_a_i_u = validar_cadena(a_i_u)
                                        if error_a_i_u == '':
                                            error_a_i_u = validar_cantidad_float_digitos(a_i_u)
                                            if error_a_i_u == '':
                                                error_a_i_u = validar_cantidad_float(a_i_u)
                                                if error_a_i_u == '':
                                                    error_a_i_u = validar_cantidad_float_0(a_i_u)
                                                    if error_a_i_u == '':
                                                        if float(a_i_u) > 100:
                                                            error_a_i_u = u'No debe ser un valor mayor a 100'

                                if aplica_tercero:
                                    try:
                                        tercero = Proveedor.objects.get(id=tercero_id, estado_proveedor=True)
                                    except:
                                        error_tercero = 'Debe seleccionar un tercero'

                                if aplica_cooperativa:
                                    error_base_gravable_cooperativa = validar_cadena(base_gravable_cooperativa)
                                    if error_base_gravable_cooperativa == '':
                                        error_base_gravable_cooperativa = validar_cantidad_float_digitos(base_gravable_cooperativa)
                                        if error_base_gravable_cooperativa == '':
                                            error_base_gravable_cooperativa = validar_cantidad_float(base_gravable_cooperativa)
                                            if error_base_gravable_cooperativa == '':
                                                error_base_gravable_cooperativa = validar_cantidad_float_negativo(base_gravable_cooperativa)
                                                if error_base_gravable_cooperativa == '':
                                                    if float(base_gravable_cooperativa) > 100:
                                                        error_base_gravable_cooperativa = u'No debe ser un valor mayor a 100'

                                    error_porcentaje_iva_cooperativa = validar_cadena(porcentaje_iva_cooperativa)
                                    if error_porcentaje_iva_cooperativa == '':
                                        error_porcentaje_iva_cooperativa = validar_cantidad_float_digitos(porcentaje_iva_cooperativa)
                                        if error_porcentaje_iva_cooperativa == '':
                                            error_porcentaje_iva_cooperativa = validar_cantidad_float(porcentaje_iva_cooperativa)
                                            if error_porcentaje_iva_cooperativa == '':
                                                error_porcentaje_iva_cooperativa = validar_cantidad_float_negativo(porcentaje_iva_cooperativa)
                                                if error_porcentaje_iva_cooperativa == '':
                                                    if float(porcentaje_iva_cooperativa) > 100:
                                                        error_porcentaje_iva_cooperativa = u'No debe ser un valor mayor a 100'

                                if cantidades_correctas == True and precios_correctos == True and error_fecha_arribo == '' and error_forma_pago == '' and error_parametro_pago == '' and error_amortizacion_anticipo == '' and error_retencion_garantia == '' and error_rete_ica == '' and error_rete_fuente == '' and error_a_i_u == '' and error_utilidad == '' and error_iva == '' and error_base_gravable_cooperativa == '' and error_porcentaje_iva_cooperativa == '' and error_tercero == '':
                                    if fecha_arribo != '':
                                        orden_servicio = OrdenServicio()
                                        orden_servicio.fecha_entrega = fecha_arribo
                                        orden_servicio.rete_ica = rete_ica
                                        orden_servicio.rete_fuente = rete_fuente
                                        orden_servicio.forma_pago = forma_pago
                                        if forma_pago == 4:
                                            orden_servicio.parametro_pago = parametro_pago
                                        orden_servicio.amortizacion = float(amortizacion_anticipo)
                                        orden_servicio.retencion_garantia = retencion_garantia
                                        orden_servicio.observaciones = observaciones.strip()
                                        if aplica_tercero:
                                            orden_servicio.tercero = tercero
                                        if aplica_cooperativa:
                                            orden_servicio.aplica_cooperativa = True
                                            orden_servicio.base_gravable_cooperativa = base_gravable_cooperativa
                                            orden_servicio.porcentaje_iva_cooperativa = porcentaje_iva_cooperativa
                                        if cotizacion.proveedor.regimen_tributario == 1:
                                            orden_servicio.tipo_iva = tipo_iva
                                        orden_servicio.proyecto = proyecto
                                        orden_servicio.proveedor = cotizacion.proveedor
                                        orden_servicio.persona = usuario
                                        orden_servicio.save()
                                        # Variable para redireccionar
                                        suministros_orden_servicio = []
                                        for suministro_cotizacion in suministros_cotizacion:
                                            suministros = proyecto.get_suministros_pendientes_comprar(suministro_id=suministro_cotizacion.suministro.id, clasificacion_general=['Equipo', 'Mano de obra', 'Transporte', 'Plenitareas'])
                                            #Registra suministro_orden_compra_item (Objeto que guarda las propiedades generales del suministro de la compra: precio, iva y observaciones)
                                            suministro_orden_servicio_item = SuministroOrdenServicioItem()
                                            suministro_orden_servicio_item.orden_servicio = orden_servicio
                                            suministro_orden_servicio_item.suministro = suministro_cotizacion.suministro
                                            suministro_orden_servicio_item.precio = suministro_cotizacion.precio
                                            suministro_orden_servicio_item.iva_suministro = suministro_cotizacion.iva_suministro
                                            suministro_orden_servicio_item.save()

                                            # Variable para redireccionar
                                            suministros_orden_servicio.append(suministro_orden_servicio_item)

                                            cantidad_comprada = 0.0
                                            cantidad = suministro_cotizacion.cantidad_cotizada
                                            for suministro in suministros:
                                                cantidad_comprada_suministro_requicision = 0.0
                                                if cantidad_comprada < cantidad:
                                                    if (round(cantidad-cantidad_comprada, 2)) <= (round(suministro.cantidad_requerida-suministro.cantidad_comprada, 2)):
                                                        cantidad_comprada_suministro_requicision = round(cantidad - cantidad_comprada, 2)
                                                    elif (round(cantidad-cantidad_comprada, 2)) > (round(suministro.cantidad_requerida-suministro.cantidad_comprada, 2)):
                                                        cantidad_comprada_suministro_requicision = round(suministro.cantidad_requerida - suministro.cantidad_comprada, 2)
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
                                                        suministro_orden_servicio.suministro_orden_servicio_item = suministro_orden_servicio_item
                                                        suministro_orden_servicio.precio = suministro_cotizacion.precio
                                                        # IVA registrado en el suministro de la cotización
                                                        #suministro_orden_servicio.iva_suministro = suministro_cotizacion.iva_suministro
                                                        # IVA = 0 (debido a que el IVA actualmente se esta calculando sobre el valor total de la OS)
                                                        suministro_orden_servicio.iva_suministro = 0
                                                        suministro_orden_servicio.orden_servicio = orden_servicio
                                                        suministro_orden_servicio.save()
                                            # Actualiza el precio del suministro correspondiente al proveedor
                                            suministro_proveedor = SuministroProveedor.objects.get(suministro=suministro_cotizacion.suministro, proveedor=cotizacion.proveedor)
                                            suministro_proveedor.precio_suministro = suministro_cotizacion.precio
                                            # IVA registrado en la cotización (Se omite debido a que el IVA actualmente se esta calculando sobre el valor total de la OS)
                                            #suministro_proveedor.iva_suministro = suministro_cotizacion.iva_suministro
                                            suministro_proveedor.save()
                                            # Costo Total si se maneja IVA por suministro
                                            #costo_total_orden = round(costo_total_orden + (round(suministro_cotizacion.cantidad_cotizada * (round(suministro_cotizacion.precio + (round(suministro_cotizacion.precio * suministro_cotizacion.iva_suministro, 2)), 2)), 2)), 2)
                                            
                                            # Borra el suministro de las cotizaciones
                                            SuministroCotizacion.objects.filter(suministro=suministro_cotizacion.suministro).delete()
                                        if orden_servicio.proveedor.regimen_tributario == 1:
                                            iva = float(iva)
                                            orden_servicio.porcentaje_iva = iva
                                            if orden_servicio.tipo_iva == 1:
                                                a_i_u = float(a_i_u)
                                                utilidad = float(utilidad)
                                                orden_servicio.porcentaje_a_i_u = a_i_u
                                                orden_servicio.porcentaje_utilidad = utilidad
                                            if orden_servicio.tipo_iva == 3:
                                                a_i_u = float(a_i_u)
                                                orden_servicio.porcentaje_a_i_u = a_i_u
                                            orden_servicio.save()
                                        actualizar_estado_requisiciones(proyecto)
                                        actualizar_cotizaciones(proyecto)

                                        # Redirecciona a los detalles del nuevo registro
                                        mensaje = u'Se ha realizado la orden de servicio'
                                        pag = Paginador(request, suministros_orden_servicio, 20, 1)
                                        return render_to_response('ordenserviciodetails.html', {'user': user, 'orden_servicio': orden_servicio, 'suministros': pag, 'proyecto': proyecto, 'mensaje': mensaje})
                                if precios_correctos == False:
                                    pag = Paginador(request, suministros_cotizacion, 20, pagina)
                                else:
                                    pag = Paginador(request, suministros_cotizacion, 20, 1)
                                if aplica_tercero:
                                    terceros = Proveedor.objects.filter(estado_proveedor=True).exclude(id=cotizacion.proveedor.id).order_by('razon_social')
                            else:
                                actualizar_cotizaciones(proyecto)
                                mensaje = u'La cotización se ha eliminado'
                                personas = proyecto.personaproyecto_set.filter(estado=True)
                                return render_to_response('proyectodetails.html', {'user': user, 'proyecto': proyecto, 'personas': personas, 'mensaje': mensaje })
                        else:
                            pag = Paginador(request, suministros_cotizacion, 20, 1)
                        return render_to_response('cotizacionordenserviciodetails.html', {'todos_suministros':todos_suministros, 'user': user, 'cotizacion': cotizacion, 'proyecto': proyecto, 'suministros': pag, 'fecha_actual': fecha_actual, 'fecha_arribo': fecha_arribo, 'amortizacion_anticipo': amortizacion_anticipo, 'retencion_garantia': retencion_garantia, 'rete_ica': rete_ica, 'rete_fuente': rete_fuente, 'forma_pago': forma_pago, 'parametro_pago': parametro_pago, 'observaciones': observaciones, 'aplica_tercero': aplica_tercero, 'terceros': terceros, 'tercero': tercero, 'aplica_cooperativa': aplica_cooperativa, 'base_gravable_cooperativa': base_gravable_cooperativa, 'porcentaje_iva_cooperativa': porcentaje_iva_cooperativa, 'tipo_iva': tipo_iva, 'a_i_u': a_i_u, 'utilidad': utilidad, 'iva': iva, 'error_fecha_arribo': error_fecha_arribo, 'error_amortizacion_anticipo': error_amortizacion_anticipo, 'error_retencion_garantia': error_retencion_garantia, 'error_rete_ica': error_rete_ica, 'error_rete_fuente': error_rete_fuente, 'error_forma_pago': error_forma_pago, 'error_parametro_pago': error_parametro_pago, 'error_a_i_u': error_a_i_u, 'error_utilidad': error_utilidad, 'error_iva': error_iva, 'error_tercero': error_tercero, 'error_base_gravable_cooperativa': error_base_gravable_cooperativa, 'error_porcentaje_iva_cooperativa': error_porcentaje_iva_cooperativa, 'error': error })
                else:
                    return HttpResponseRedirect('/inverboy/home/proyectodetails/'+ str(proyecto.id) +'/')
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Funcion para actualizar el estado de las requisiciones según sus items comprados o por comprar
def actualizar_estado_requisiciones(proyecto):
    requisiciones = Requisicion.objects.filter(proyecto=proyecto)
    for requisicion in requisiciones:
        requisicion.actualizar_estado()


#Función para actualizar las cotizaciones de un proyecto
def actualizar_cotizaciones(proyecto):
    import datetime
    from datetime import date
    now = datetime.datetime.now()
    fecha_actual = date(now.year, now.month, now.day)
    # Borra las cotizaciones sin suministros y de mas de 8 dias de creación, que no han sido confirmadas como ordenes de compra
    cotizaciones = Cotizacion.objects.filter(proyecto=proyecto)
    for cotizacion in cotizaciones:
        fecha_creacion = date(cotizacion.fecha_creacion.year, cotizacion.fecha_creacion.month, cotizacion.fecha_creacion.day)
        diff = fecha_actual - fecha_creacion
        if (diff.days >= 8) or (len(cotizacion.suministrocotizacion_set.all())==0):
            cotizacion.suministrocotizacion_set.all().delete()
            cotizacion.delete()


#Función para actualizar el precio promedio de un suministro especifico en APU's maestros
def actualizar_valor_suministro_apus(suministro):
    suministros = SuministroApu.objects.filter(suministro=suministro)
    for suministro in suministros:
        suministro.valor_promedio()


#Reporte ordenes de compra
def ordenes_compra_proyecto_search(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_ordencompra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id = proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                fecha_inicial = {'valor': '', 'error': ''}
                fecha_final = {'valor': '', 'error': ''}
                criterio = ''
                parametro_fecha_inicial = ''
                parametro_fecha_final = ''
                if request.method == 'POST':
                    fecha_inicial['valor'] = request.POST['fecha_inicial'].strip()
                    fecha_final['valor'] = request.POST['fecha_final'].strip()
                    criterio = request.POST['criterio'].strip()

                    if fecha_inicial['valor'] != '':
                        validaciones_fecha = Validator().append([
                            Field('fecha_inicial', fecha_inicial['valor']).append([
                                IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                            ]),
                        ]).run(True).pop()

                        if validaciones_fecha['passed'] == True:
                            parametro_fecha_inicial = fecha_inicial['valor']
                        else:
                            for error in validaciones_fecha['errors']:
                                fecha_inicial['error'] = error

                    if fecha_final['valor'] != '':
                        validaciones_fecha = Validator().append([
                            Field('fecha_final', fecha_final['valor']).append([
                                IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                            ]),
                        ]).run(True).pop()

                        if validaciones_fecha['passed'] == True:
                            parametro_fecha_final = fecha_final['valor']
                        else:
                            for error in validaciones_fecha['errors']:
                                fecha_final['error'] = error
                ordenes_compra = proyecto.lista_ordenes_compra(criterio, fecha_inicial=parametro_fecha_inicial, fecha_final=parametro_fecha_final)
                pag = Paginador(request, ordenes_compra, 20, 1)
                return render_to_response('reporteordenescompra.html', {'user': user, 'ordenes_compra': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Detalles orden de compra
def ordenes_compra_proyecto_details(request, orden_compra_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_ordencompra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
                suministros = orden_compra.suministroordencompraitem_set.all()
                pag = Paginador(request, suministros, 20, 1)
                return render_to_response('ordencompradetails.html', {'user': user, 'orden_compra': orden_compra, 'suministros': pag, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar orden de compra
def ordenes_compra_proyecto_change(request, orden_compra_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_ordencompra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                error = ''
                subtotal = 0
                valor_iva = 0
                valor_total = 0
                orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
                if orden_compra.permite_modificaciones():
                    items_orden_compra = orden_compra.suministroordencompraitem_set.all()

                    #Parametros comunes cotización (ordenes_compra-ordenes_servicio)
                    fecha_arribo = orden_compra.fecha_arribo
                    forma_pago = orden_compra.forma_pago
                    parametro_pago = ''
                    if forma_pago == 1:
                        parametro_pago = orden_compra.dias_credito
                    if forma_pago == 4:
                        parametro_pago = orden_compra.porcentaje_anticipo
                    observaciones = orden_compra.observaciones

                    #Errores comunes cotización (ordenes_compra-ordenes_servicio)
                    error_fecha_arribo = ''
                    error_forma_pago = ''
                    error_parametro_pago = ''
                    if request.method == 'POST':
                        suministros = None
                        try:
                            suministros = request.session['suministros']
                        except :
                            pass
                        if suministros != None:
                            # Valida que las cantidades esten disponibles
                            cantidades_disponibles = True
                            for suministro in suministros:
                                cantidad_requerida = SuministroRequisicion.objects.filter(requisicion__proyecto=proyecto, suministro__suministro__id=suministro['suministro'].id, cantidad_comprada__lt=F('cantidad_requerida')).aggregate(Sum('cantidad_requerida'))['cantidad_requerida__sum']
                                # Si cantidades disponibles en requisicion la cantidad requerida es None, cero
                                if cantidad_requerida == None:
                                    cantidad_requerida = 0
                                cantidad_comprada_orden_actual = 0
                                try:
                                    cantidad_comprada_orden_actual = orden_compra.suministroordencompraitem_set.get(suministro__id=suministro['suministro'].id).suministroordencompra_set.aggregate(Sum('cantidad_comprada'))['cantidad_comprada__sum']
                                except :
                                    pass
                                cantidad_disponible = round(cantidad_requerida + cantidad_comprada_orden_actual, 2)
                                if suministro['cantidad'] > cantidad_disponible:
                                    cantidades_disponibles = False

                                #Calcula los valores de subtotal, valor iva y valor total de la orden de compra
                                subtotal = round(subtotal + (suministro['cantidad'] * suministro['precio']), 2)
                                valor_iva = round(valor_iva + (suministro['cantidad'] * suministro['precio'] * suministro['iva_suministro']), 2)
                            valor_total = round(subtotal + valor_iva, 2)

                            if cantidades_disponibles:
                                fecha_arribo = request.POST['fecha_arribo'].strip()
                                forma_pago = request.POST['forma_pago'].strip()
                                parametro_pago = request.POST['parametro_pago'].strip()
                                observaciones = request.POST['observaciones'].strip()
                                #Valida si las cantidades de la cotización estan entre el rango de las cantidades requeridas (por cada suministro)
                                precios_correctos = True
                                pagina = 0
                                indice = 0
                                for suministro in suministros:
                                    indice = indice + 1
                                    if suministro['precio'] <= 0:
                                        precios_correctos = False
                                        if pagina == 0:
                                            pagina = indice // 20
                                            if(indice % 20) > 0:
                                                pagina = pagina + 1
                                if error == '':
                                    if precios_correctos == False:
                                        error = u'Revise los precios, deben ser mayores a 0'

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

                                if forma_pago not in ['1', '2', '3', '4']:
                                    error_forma_pago = 'Campo obligatorio'

                                if error_forma_pago == '':
                                    forma_pago = int(forma_pago)
                                    if forma_pago == 1:
                                        error_parametro_pago = validar_cadena(parametro_pago)
                                        if error_parametro_pago == '':
                                            error_parametro_pago = validar_cantidad_int(parametro_pago)
                                            if error_parametro_pago == '':
                                                parametro_pago = int(parametro_pago)
                                                error_parametro_pago = validar_cantidad_int_0(parametro_pago)
                                                if error_parametro_pago == '':
                                                    error_parametro_pago = validar_int_digitos(parametro_pago, 3)
                                    elif forma_pago == 4:
                                        error_parametro_pago = validar_cadena(parametro_pago)
                                        if error_parametro_pago == '':
                                            error_parametro_pago = validar_cantidad_float(parametro_pago)
                                            if error_parametro_pago == '':
                                                parametro_pago = float(parametro_pago)
                                                error_parametro_pago = validar_cantidad_float_0(parametro_pago)
                                                if error_parametro_pago == '':
                                                    if parametro_pago > 100:
                                                        error_parametro_pago = u'El porcentaje no debe ser mayor a 100'
                                    elif forma_pago == 2 or forma_pago == 3:
                                        pass
                                # Si no existen errores en las validaciones
                                if precios_correctos == True and error_fecha_arribo == '' and error_forma_pago == '' and error_parametro_pago == '':
                                    if len(suministros) > 0:
                                        orden_compra.fecha_arribo = fecha_arribo
                                        orden_compra.forma_pago = forma_pago
                                        # Si la forma de pago es 3 (Anticipado) ó 4 (% Anticipo) se elimina el permiso para que se pueda modificar la orden de compra
                                        if orden_compra.forma_pago == 3 or orden_compra.forma_pago == 4:
                                            orden_compra.permiso_modificar = False
                                        else:
                                            orden_compra.permiso_modificar = True
                                        if forma_pago == 1:
                                            orden_compra.dias_credito = parametro_pago
                                        elif forma_pago == 4:
                                            orden_compra.porcentaje_anticipo = parametro_pago
                                        orden_compra.observaciones = observaciones
                                        orden_compra.persona = usuario
                                        orden_compra.save()

                                        # Elimina los suministros y actualiza los registros
                                        for item_orden_compra in items_orden_compra:
                                            eliminar_item = True
                                            for suministro in suministros:
                                                if item_orden_compra.suministro.id == suministro['suministro'].id:
                                                    eliminar_item = False
                                                    # Actualiza los registros
                                                    cantidad_actual_orden_compra = item_orden_compra.suministroordencompra_set.aggregate(Sum('cantidad_comprada'))['cantidad_comprada__sum']
                                                    if suministro['cantidad'] < cantidad_actual_orden_compra:
                                                        suministros_orden_compra = item_orden_compra.suministroordencompra_set.all()
                                                        suma_cantidades = 0
                                                        ultimo_suministro_orden_compra = None
                                                        for suministro_orden_compra in suministros_orden_compra:
                                                            if suma_cantidades < suministro['cantidad']:
                                                                suma_cantidades += suministro_orden_compra.cantidad_comprada
                                                                ultimo_suministro_orden_compra = suministro_orden_compra
                                                            else:
                                                                # Actualiza los registros
                                                                # Actualiza el suministro_apu_proyecto
                                                                suministro_apu = suministro_orden_compra.suministro.suministro
                                                                suministro_apu.cantidad_comprada = round(suministro_apu.cantidad_comprada - suministro_orden_compra.cantidad_comprada, 2)
                                                                suministro_apu.cantidad_requerida = round(suministro_apu.cantidad_requerida + suministro_orden_compra.cantidad_comprada, 2)
                                                                suministro_apu.save()
                                                                # Actualiza el suministro_requisicion
                                                                suministro_requisicion = suministro_orden_compra.suministro
                                                                suministro_requisicion.cantidad_comprada = round(suministro_requisicion.cantidad_comprada - suministro_orden_compra.cantidad_comprada, 2)
                                                                suministro_requisicion.save()

                                                                # Elimina el registro
                                                                suministro_orden_compra.delete()
                                                        if suma_cantidades > suministro['cantidad']:
                                                            diferencia = round(suma_cantidades - suministro['cantidad'], 2)
                                                            # Actualiza los registros
                                                            # Actualiza el suministro_apu_proyecto
                                                            suministro_apu = ultimo_suministro_orden_compra.suministro.suministro
                                                            suministro_apu.cantidad_comprada = round(suministro_apu.cantidad_comprada - diferencia, 2)
                                                            suministro_apu.cantidad_requerida = round(suministro_apu.cantidad_requerida + diferencia, 2)
                                                            suministro_apu.save()
                                                            # Actualiza el suministro_requisicion
                                                            suministro_requisicion = ultimo_suministro_orden_compra.suministro
                                                            suministro_requisicion.cantidad_comprada = round(suministro_requisicion.cantidad_comprada - diferencia, 2)
                                                            suministro_requisicion.save()
                                                            # Actualiza el suministro_orden_compra
                                                            ultimo_suministro_orden_compra.cantidad_comprada = round(ultimo_suministro_orden_compra.cantidad_comprada - diferencia, 2)
                                                            ultimo_suministro_orden_compra.save()

                                                    elif suministro['cantidad'] > cantidad_actual_orden_compra: # Si la nueva cantidad es mayor a la cantidad comprada
                                                        # Actualiza los registros
                                                        suministros_requisiciones = proyecto.get_suministros_pendientes_comprar(suministro_id=suministro['suministro'].id, clasificacion_general=['Material'])

                                                        cantidad_comprada = cantidad_actual_orden_compra
                                                        cantidad = suministro['cantidad']

                                                        for suministro_requisicion in suministros_requisiciones:
                                                            cantidad_comprada_suministro_requicision = 0.0
                                                            if cantidad_comprada < cantidad:
                                                                if (round(cantidad-cantidad_comprada, 2)) <= (round(suministro_requisicion.cantidad_requerida-suministro_requisicion.cantidad_comprada, 2)):
                                                                    cantidad_comprada_suministro_requicision = round(cantidad - cantidad_comprada, 2)
                                                                elif (round(cantidad-cantidad_comprada, 2)) > (round(suministro_requisicion.cantidad_requerida-suministro_requisicion.cantidad_comprada, 2)):
                                                                    cantidad_comprada_suministro_requicision = round(suministro_requisicion.cantidad_requerida-suministro_requisicion.cantidad_comprada, 2)
                                                                cantidad_comprada = round(cantidad_comprada + cantidad_comprada_suministro_requicision, 2)
                                                                if cantidad_comprada_suministro_requicision > 0:
                                                                    # Actualiza la cantidad comprada en suministro apu proyecto
                                                                    suministro_apu_proyecto = suministro_requisicion.suministro
                                                                    suministro_apu_proyecto.cantidad_comprada = round(suministro_apu_proyecto.cantidad_comprada + cantidad_comprada_suministro_requicision, 2)
                                                                    # Actualiza la cantidad requerida del suministro en el apu proyecto
                                                                    suministro_apu_proyecto.cantidad_requerida = round(suministro_apu_proyecto.cantidad_requerida - cantidad_comprada_suministro_requicision, 2)
                                                                    suministro_apu_proyecto.save()
                                                                    # Actualiza la cantidad comprada en suministro requicisión
                                                                    suministro_requisicion.cantidad_comprada = round(suministro_requisicion.cantidad_comprada + cantidad_comprada_suministro_requicision, 2)
                                                                    suministro_requisicion.save()

                                                                    try:
                                                                        suministro_orden_compra = orden_compra.suministroordencompra_set.get(suministro=suministro_requisicion, suministro_orden_compra_item=item_orden_compra)
                                                                        suministro_orden_compra.cantidad_comprada = round(suministro_orden_compra.cantidad_comprada + cantidad_comprada_suministro_requicision, 2)
                                                                        suministro_orden_compra.save()
                                                                    except :
                                                                        # Crea el nuevo suministro de la orden de compra
                                                                        suministro_orden_compra = SuministroOrdenCompra()
                                                                        suministro_orden_compra.suministro = suministro_requisicion
                                                                        suministro_orden_compra.cantidad_comprada = cantidad_comprada_suministro_requicision
                                                                        suministro_orden_compra.suministro_orden_compra_item = item_orden_compra
                                                                        suministro_orden_compra.orden_compra = orden_compra
                                                                        suministro_orden_compra.save()
                                                        # Actualiza el precio del suministro correspondiente al proveedor
                                                        suministro_proveedor = SuministroProveedor.objects.get(suministro=item_orden_compra.suministro, proveedor=orden_compra.proveedor)
                                                        suministro_proveedor.precio_suministro = item_orden_compra.precio
                                                        suministro_proveedor.iva_suministro = item_orden_compra.iva_suministro
                                                        suministro_proveedor.save()
                                                        # Borra el suministro de las cotizaciones
                                                        SuministroCotizacion.objects.filter(suministro=item_orden_compra.suministro).delete()
                                                    # Actualiza el precio en el item
                                                    item_orden_compra.precio = suministro['precio']
                                                    # Actualiza el iva en el item
                                                    item_orden_compra.iva_suministro = suministro['iva_suministro']
                                                    # Actualiza las en el item
                                                    item_orden_compra.iva_suministro = suministro['iva_suministro']
                                                    # Actualiza las obervaciones en el item
                                                    item_orden_compra.observaciones = suministro['observaciones']
                                                    item_orden_compra.save()
                                                    # Elimina el suministro de la lista de session para no tenerlo más en cuenta
                                                    suministros.remove(suministro)

                                            if eliminar_item:
                                                # Actualiza los registros
                                                suministros_orden_compra = item_orden_compra.suministroordencompra_set.all()
                                                for suministro_orden_compra in suministros_orden_compra:
                                                    # Actualiza el suministro_apu_proyecto
                                                    suministro_apu = suministro_orden_compra.suministro.suministro
                                                    suministro_apu.cantidad_comprada = round(suministro_apu.cantidad_comprada - suministro_orden_compra.cantidad_comprada, 2)
                                                    suministro_apu.cantidad_requerida = round(suministro_apu.cantidad_requerida + suministro_orden_compra.cantidad_comprada, 2)
                                                    suministro_apu.save()
                                                    # Actualiza el suministro_requisicion
                                                    suministro_requisicion = suministro_orden_compra.suministro
                                                    suministro_requisicion.cantidad_comprada = round(suministro_requisicion.cantidad_comprada - suministro_orden_compra.cantidad_comprada, 2)
                                                    suministro_requisicion.save()

                                                    # Elimina el registro
                                                    suministro_orden_compra.delete()
                                                # Elimina el registro
                                                item_orden_compra.delete()
                                        # Crea nuevos registros para los nuevos suministros adicionados
                                        for suministro in suministros:
                                            suministros_requisiciones = proyecto.get_suministros_pendientes_comprar(suministro_id=suministro['suministro'].id, clasificacion_general=['Material'])

                                            #Registra suministro_orden_compra_item (Objeto que guarda las propiedades generales del suministro de la compra: precio, iva y observaciones)
                                            suministro_orden_compra_item = SuministroOrdenCompraItem()
                                            suministro_orden_compra_item.orden_compra = orden_compra
                                            suministro_orden_compra_item.suministro = suministro['suministro']
                                            suministro_orden_compra_item.precio = suministro['precio']
                                            suministro_orden_compra_item.iva_suministro = suministro['iva_suministro']
                                            suministro_orden_compra_item.observaciones = suministro['observaciones']
                                            suministro_orden_compra_item.save()
                                            cantidad_comprada = 0.0
                                            cantidad = suministro['cantidad']

                                            for suministro_requisiciones in suministros_requisiciones:
                                                cantidad_comprada_suministro_requicision = 0.0
                                                if cantidad_comprada < cantidad:
                                                    if (round(cantidad-cantidad_comprada, 2)) <= (round(suministro_requisiciones.cantidad_requerida-suministro_requisiciones.cantidad_comprada, 2)):
                                                        cantidad_comprada_suministro_requicision = round(cantidad - cantidad_comprada, 2)
                                                    elif (round(cantidad-cantidad_comprada, 2)) > (round(suministro_requisiciones.cantidad_requerida-suministro_requisiciones.cantidad_comprada, 2)):
                                                        cantidad_comprada_suministro_requicision = round(suministro_requisiciones.cantidad_requerida-suministro_requisiciones.cantidad_comprada, 2)
                                                    cantidad_comprada = round(cantidad_comprada + cantidad_comprada_suministro_requicision, 2)
                                                    if cantidad_comprada_suministro_requicision > 0:
                                                        # Actualiza la cantidad comprada en suministro apu proyecto
                                                        suministro_apu_proyecto = suministro_requisiciones.suministro
                                                        suministro_apu_proyecto.cantidad_comprada = round(suministro_apu_proyecto.cantidad_comprada + cantidad_comprada_suministro_requicision, 2)
                                                        # Actualiza la cantidad requerida del suministro en el apu proyecto
                                                        suministro_apu_proyecto.cantidad_requerida = round(suministro_apu_proyecto.cantidad_requerida - cantidad_comprada_suministro_requicision, 2)
                                                        suministro_apu_proyecto.save()
                                                        # Actualiza la cantidad comprada en suministro requicisión
                                                        suministro_requisiciones.cantidad_comprada = round(suministro_requisiciones.cantidad_comprada + cantidad_comprada_suministro_requicision, 2)
                                                        suministro_requisiciones.save()
                                                        # Crea el nuevo suministro de la orden de compra
                                                        suministro_orden_compra = SuministroOrdenCompra()
                                                        suministro_orden_compra.suministro = suministro_requisiciones
                                                        suministro_orden_compra.cantidad_comprada = cantidad_comprada_suministro_requicision
                                                        suministro_orden_compra.suministro_orden_compra_item = suministro_orden_compra_item
                                                        suministro_orden_compra.orden_compra = orden_compra
                                                        suministro_orden_compra.save()
                                            # Actualiza el precio del suministro correspondiente al proveedor
                                            suministro_proveedor = SuministroProveedor.objects.get(suministro=suministro['suministro'].id, proveedor=orden_compra.proveedor)
                                            suministro_proveedor.precio_suministro = suministro['precio']
                                            suministro_proveedor.iva_suministro = suministro['iva_suministro']
                                            suministro_proveedor.save()
                                        actualizar_estado_requisiciones(proyecto)
                                        actualizar_cotizaciones(proyecto)
                                        # Elimina las variables de session
                                        del request.session['suministros']
                                        return HttpResponseRedirect('/inverboy/home/ordenescompraproyectodetails/' + str(orden_compra_id) + '/' + str(proyecto_id) + '/')
                                    else:
                                        # Si la lista de suministros esta vacia
                                        pass
                                else:
                                    # Si hay errores en las validaciones
                                    pass
                            else:
                                error = 'Las nuevas cantidades deben ser proporcionales a las cantidades requeridas'
                        else:
                            return HttpResponseRedirect('/inverboy/home/proyectodetails/' + str(proyecto_id) + '/')
                    else:
                        suministros = []
                        for item_orden_compra in items_orden_compra:
                            cantidad = item_orden_compra.suministroordencompra_set.all().aggregate(Sum('cantidad_comprada'))['cantidad_comprada__sum']
                            suministros.append({'suministro': item_orden_compra.suministro, 'cantidad': cantidad, 'precio': item_orden_compra.precio, 'iva_suministro': item_orden_compra.iva_suministro, 'observaciones': item_orden_compra.observaciones})
                            subtotal = round(subtotal + (cantidad * item_orden_compra.precio), 2)
                            valor_iva = round(valor_iva + (cantidad * item_orden_compra.precio * item_orden_compra.iva_suministro), 2)
                        valor_total = round(subtotal + valor_iva, 2)
                        request.session['suministros'] = suministros
                        request.session['suministros_agregar'] = []
                    pag = Paginador(request, suministros, 20, 1)
                    return render_to_response('ordencomprachange.html', {'user': user, 'orden_compra': orden_compra, 'suministros': pag, 'subtotal': subtotal, 'valor_iva': valor_iva, 'valor_total': valor_total, 'fecha_arribo': fecha_arribo, 'forma_pago': forma_pago, 'parametro_pago': str(parametro_pago), 'observaciones': observaciones, 'error': error, 'error_fecha_arribo': error_fecha_arribo, 'error_forma_pago': error_forma_pago, 'error_parametro_pago': error_parametro_pago, 'proyecto': proyecto})
                else:
                    return HttpResponseRedirect('/inverboy/home/proyectodetails/' + str(proyecto_id) + '/')
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Nuevo informe de recepción
def ordenes_compra_informe_recepcion_add(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_informerecepcion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id = proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                ordenes_compra = proyecto.lista_ordenes_compra(criterio=criterio, estado=1)
                for orden_compra in ordenes_compra:
                    if len(orden_compra.suministroordencompra_set.filter(cantidad_almacen__lt=F('cantidad_comprada'))) == 0:
                        ordenes_compra = ordenes_compra.exclude(id=orden_compra.id)
                pag = Paginador(request, ordenes_compra, 20, 1)
                return render_to_response('informerecepcionadd_1ordenescompra.html', {'user': user, 'ordenes_compra': pag, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def informe_recepcion_add(request, orden_compra_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_informerecepcion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
                error = ''
                numero_remision = ''
                error_numero_remision = ''
                observaciones = ''
                suministros_informe_recepcion = []
                if request.method == 'POST':
                    suministros_informe_recepcion = None
                    try:
                        suministros_informe_recepcion = request.session['suministros_informe_recepcion']
                    except :
                        pass
                    if suministros_informe_recepcion != None:
                        numero_remision = request.POST['numero_remision'].strip()
                        error_numero_remision = ''
                        if numero_remision != '':
                            error_numero_remision = validar_cadena_caracteres_especiales(numero_remision)
                        observaciones = request.POST['observaciones'].strip()
                        if len(suministros_informe_recepcion) > 0:
                            if error_numero_remision == '':
                                informe_recepcion = InformeRecepcion()
                                informe_recepcion.numero_remision = numero_remision
                                informe_recepcion.observaciones = observaciones
                                informe_recepcion.orden_compra = orden_compra
                                informe_recepcion.persona = usuario
                                informe_recepcion.save()

                                for suministro_informe in suministros_informe_recepcion:
                                    suministros = orden_compra.suministroordencompra_set.filter(suministro__suministro__suministro__id=suministro_informe['id'], orden_compra__proyecto=proyecto)
                                    suministros = suministros.order_by('suministro__requisicion__fecha_arribo')
                                    cantidad_recibida = 0.0
                                    cantidad = float(suministro_informe['cantidad'])
                                    for suministro in suministros:
                                        if cantidad_recibida < cantidad:
                                            cantidad_recibida_suministro_orden_compra = 0.0
                                            if (round(cantidad-cantidad_recibida, 2)) <= float(str(round(suministro.cantidad_comprada-suministro.cantidad_almacen, 2))):
                                                cantidad_recibida_suministro_orden_compra = round(cantidad - cantidad_recibida, 2)
                                            elif (round(cantidad-cantidad_recibida, 2)) > float(str(round(suministro.cantidad_comprada-suministro.cantidad_almacen, 2))):
                                                cantidad_recibida_suministro_orden_compra = round(suministro.cantidad_comprada-suministro.cantidad_almacen, 2)
                                            cantidad_recibida = round(cantidad_recibida + cantidad_recibida_suministro_orden_compra, 2)
                                            if cantidad_recibida_suministro_orden_compra > 0:
                                                # Actualiza la cantidad comprada en suministro apu proyecto
                                                suministro_apu_proyecto = suministro.suministro.suministro
                                                suministro_apu_proyecto.cantidad_almacen = round(suministro_apu_proyecto.cantidad_almacen + cantidad_recibida_suministro_orden_compra, 2)
                                                suministro_apu_proyecto.save()
                                                # Actualiza la cantidad comprada en el suministro requisicion
                                                suministro_requisicion = suministro.suministro
                                                suministro_requisicion.cantidad_almacen = round(suministro_requisicion.cantidad_almacen + cantidad_recibida_suministro_orden_compra, 2)
                                                suministro_requisicion.save()
                                                # Actualiza la cantidad comprada en el suministro orden compra
                                                suministro.cantidad_almacen = round(suministro.cantidad_almacen + cantidad_recibida_suministro_orden_compra, 2)
                                                suministro.save()
                                                # Crea el nuevo suministro del informe de recepción
                                                suministro_informe_recepcion = SuministroInformeRecepcion()
                                                suministro_informe_recepcion.suministro = suministro
                                                suministro_informe_recepcion.cantidad = cantidad_recibida_suministro_orden_compra
                                                suministro_informe_recepcion.informe_recepcion = informe_recepcion
                                                suministro_informe_recepcion.save()
                                        else:
                                            break
                                    suministros_almacen = SuministroAlmacen.objects.all()
                                    existe_suministro = False
                                    for suministro_almacen in suministros_almacen:
                                        if suministro_almacen.suministro.id == suministro_informe['id'] and suministro_almacen.proyecto == proyecto:
                                            suministro_almacen.cantidad_total = round(suministro_almacen.cantidad_total + cantidad, 2)
                                            suministro_almacen.cantidad_actual = round(suministro_almacen.cantidad_actual + cantidad, 2)
                                            suministro_almacen.save()
                                            existe_suministro = True
                                    if existe_suministro == False:
                                        suministro_almacen = SuministroAlmacen()
                                        suministro_almacen.cantidad_total = cantidad
                                        suministro_almacen.cantidad_actual = cantidad
                                        suministro_almacen.suministro = Suministro.objects.get(id=suministro_informe['id'])
                                        suministro_almacen.proyecto = proyecto
                                        suministro_almacen.save()
                                del request.session['suministros_informe_recepcion']

                                # Redirecciona a los detalles del nuevo registro
                                mensaje = u'Se ha realizado el informe de recepción'
                                suministros_informe_recepcion = informe_recepcion.get_suministros_agrupados_suministro()
                                pag = Paginador(request, suministros_informe_recepcion, 20, 1)
                                return render_to_response('informerecepciondetails.html', {'user': user, 'informe_recepcion': informe_recepcion, 'suministros': pag, 'proyecto': proyecto, 'mensaje': mensaje})
                        else:
                            error = u'No se han ingresado items en este informe de recepción'
                    else:
                        return proyecto_details(request, proyecto_id)
                else:
                    request.session['suministros_informe_recepcion'] = suministros_informe_recepcion
                suministros = orden_compra.suministroordencompra_set.all().order_by('suministro__suministro__suministro__nombre')
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
                        suministros_orden_compra.append({ 'suministro': suministro_tmp, 'cantidad_nuevo_informe': '' })

                for suministro_informe_recepcion in suministros_informe_recepcion:
                    for suministro_orden_compra in suministros_orden_compra:
                        if int(suministro_informe_recepcion['id']) == suministro_orden_compra['suministro'].suministro.suministro.suministro.id:
                            suministro_orden_compra['cantidad_nuevo_informe'] = suministro_informe_recepcion['cantidad']
                pag = Paginador(request, suministros_orden_compra, 20, 1)
                return render_to_response('informerecepcionadd.html', {'user': user, 'orden_compra': orden_compra, 'proyecto': proyecto, 'suministros': pag, 'numero_remision': numero_remision, 'error_numero_remision': error_numero_remision, 'observaciones': observaciones, 'error': error})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Reporte informes de recepción
def informes_recepcion_proyecto_search(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_informerecepcion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                fecha_inicial = {'valor': '', 'error': ''}
                fecha_final = {'valor': '', 'error': ''}
                criterio = ''
                parametro_fecha_inicial = ''
                parametro_fecha_final = ''
                if request.method == 'POST':
                    fecha_inicial['valor'] = request.POST['fecha_inicial'].strip()
                    fecha_final['valor'] = request.POST['fecha_final'].strip()
                    criterio = request.POST['criterio'].strip()

                    if fecha_inicial['valor'] != '':
                        validaciones_fecha = Validator().append([
                            Field('fecha_inicial', fecha_inicial['valor']).append([
                                IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                            ]),
                        ]).run(True).pop()

                        if validaciones_fecha['passed'] == True:
                            parametro_fecha_inicial = fecha_inicial['valor']
                        else:
                            for error in validaciones_fecha['errors']:
                                fecha_inicial['error'] = error

                    if fecha_final['valor'] != '':
                        validaciones_fecha = Validator().append([
                            Field('fecha_final', fecha_final['valor']).append([
                                IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                            ]),
                        ]).run(True).pop()

                        if validaciones_fecha['passed'] == True:
                            parametro_fecha_final = fecha_final['valor']
                        else:
                            for error in validaciones_fecha['errors']:
                                fecha_final['error'] = error
                informes_recepcion = proyecto.lista_informes_recepcion(criterio, fecha_inicial=parametro_fecha_inicial, fecha_final=parametro_fecha_final)
                pag = Paginador(request, informes_recepcion, 20, 1)
                return render_to_response('reporteinformesrecepcion.html', {'user': user, 'informes_recepcion': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Detalles informe de recepción
def informes_recepcion_proyecto_details(request, informe_recepcion_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_informerecepcion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                informe_recepcion = InformeRecepcion.objects.get(id=informe_recepcion_id, orden_compra__proyecto=proyecto)
                suministros = informe_recepcion.suministroinformerecepcion_set.all()
                suministros_informe_recepcion = []
                for suministro in suministros:
                    suministro_tmp = suministro
                    suministro_adicionado = False
                    for suministro_tmp2 in suministros_informe_recepcion:
                        if suministro_tmp2.suministro.suministro.suministro.suministro.id == suministro_tmp.suministro.suministro.suministro.suministro.id:
                            suministro_tmp2.cantidad = round(suministro_tmp2.cantidad + suministro_tmp.cantidad, 2)
                            suministro_tmp2.cantidad_facturada = round(suministro_tmp2.cantidad_facturada + suministro_tmp.cantidad_facturada, 2)
                            suministro_adicionado = True
                    if suministro_adicionado == False:
                        suministros_informe_recepcion.append(suministro_tmp)
                pag = Paginador(request, suministros_informe_recepcion, 20, 1)
                return render_to_response('informerecepciondetails.html', {'user': user, 'informe_recepcion': informe_recepcion, 'suministros': pag, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Busqueda suministros almacen
def suministros_almacen_search(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_suministroalmacen' in user.get_all_permissions():
            total_valor = 0.0
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                suministros = proyecto.suministroalmacen_set.all().order_by('suministro__nombre')
                for suministro in suministros:
                    total_valor+= suministro.get_valor_precio_x_cantidad()
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                    if criterio != '':
                        suministros = suministros.filter(Q(suministro__nombre__icontains=criterio) | Q(suministro__sinonimos__icontains=criterio))
                pag = Paginador(request, suministros, 20, 1)
                return render_to_response('reportesuministrosalmacen.html', {'user': user, 'suministros': pag, 'criterio': criterio, 'proyecto': proyecto, 'total_valor':total_valor})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Nuevo informe de salida de almacen
def informe_salida_add(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_informesalida' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                error = ''
                persona_proyecto = None
                observaciones = ''
                if request.method == 'POST':
                    suministros_informe_salida = None
                    try:
                        suministros_informe_salida = request.session['suministros_informe_salida']
                    except :
                        pass
                    if suministros_informe_salida != None:
                        observaciones = request.POST['observaciones'].strip()
                        try:
                            persona_proyecto = proyecto.personaproyecto_set.get(id=request.POST['persona'])
                        except :
                            pass
                        if len(suministros_informe_salida) > 0:
                            for suministro in suministros_informe_salida:
                                suministro_almacen = proyecto.suministroalmacen_set.get(id=suministro['id'])
                                cantidad = float(suministro['cantidad'])
                                #Verifica si la cantidad esta disponible
                                if cantidad > suministro_almacen:
                                    error = 'Las cantidades asignadas no estan disponibles'
                            if error == '':
                                if persona_proyecto != None:
                                    informe_salida = InformeSalida()
                                    informe_salida.observaciones = observaciones
                                    informe_salida.proyecto = proyecto
                                    informe_salida.persona_proyecto = persona_proyecto
                                    informe_salida.persona = usuario
                                    informe_salida.save()

                                    # Variable para redireccion
                                    suministros_informe = []
                                    for suministro in suministros_informe_salida:
                                        suministro_almacen = SuministroAlmacen.objects.get(id=suministro['id'], proyecto=proyecto)
                                        #Se crea el nuevo suministro_informe de salida_item
                                        suministro_informe_salida_item = SuministroInformeSalidaItem()
                                        suministro_informe_salida_item.suministro_almacen = suministro_almacen
                                        suministro_informe_salida_item.informe_salida = informe_salida
                                        suministro_informe_salida_item.save()

                                        # Variable para redireccion
                                        suministros_informe.append(suministro_informe_salida_item)

                                        for apu_proyecto in suministro['apus_proyecto']:
                                            suministro_apu_proyecto = ApuProyecto.objects.get(id=apu_proyecto['id']).suministroapuproyecto_set.get(suministro__id=suministro_almacen.suministro.id)
                                            cantidad = float(apu_proyecto['cantidad'])
                                            # Crea el nuevo suministro del informe de salida
                                            suministro_informe_salida = SuministroInformeSalida()
                                            suministro_informe_salida.cantidad = cantidad
                                            suministro_informe_salida.suministro_apu_proyecto = suministro_apu_proyecto
                                            suministro_informe_salida.suministro_informe_salida_item = suministro_informe_salida_item
                                            suministro_informe_salida.save()
                                        
                                        # Actualiza la cantidad actual en almacen del suministro
                                        cantidad = suministro['cantidad']
                                        suministro_almacen.cantidad_actual = round(suministro_almacen.cantidad_actual - cantidad, 2)
                                        suministro_almacen.save()
                                    del request.session['suministros_informe_salida']

                                    # Redirecciona a los detalles del nuevo registro
                                    mensaje = u'Se ha realizado el informe de salida'
                                    pag = Paginador(request, suministros_informe, 20, 1)
                                    return render_to_response('informesalidadetails.html', {'user': user, 'informe_salida': informe_salida, 'suministros': pag, 'proyecto': proyecto, 'mensaje': mensaje})
                                else:
                                    error = u'Debe seleccionar una persona responsable del informe de salida'
                        else:
                            error = u'No se han ingresado items en este informe de salida'
                    else:
                        return proyecto_details(request, proyecto_id)
                else:
                    suministros_informe_salida = []
                    request.session['suministros_informe_salida'] = suministros_informe_salida
                    try:
                        del request.session['apus_informe_salida']
                    except :
                        pass
                personas = proyecto.personaproyecto_set.filter(estado=True)
                suministros = SuministroAlmacen.objects.filter(proyecto=proyecto).order_by('suministro__nombre')
                suministros_almacen = []
                for suministro in suministros:
                    suministro_almacen = {'suministro': suministro, 'suministros_apus': [], 'cantidad_nuevo_informe': ''}
                    for suministro_informe_salida in suministros_informe_salida:
                        if suministro_informe_salida['id'] == suministro.id:
                            suministro_almacen['cantidad_nuevo_informe'] = suministro_informe_salida['cantidad']
                    suministros_almacen.append(suministro_almacen)
                pag = Paginador(request, suministros_almacen, 20, 1)
                return render_to_response('informesalidaadd.html', {'user': user, 'suministros': pag, 'proyecto': proyecto, 'personas': personas, 'persona_proyecto': persona_proyecto, 'pagina_suministro': 1, 'observaciones': observaciones, 'error': error })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Reporte informes de salida almacen
def informes_salida_proyecto_search(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_informesalida' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                fecha_inicial = {'valor': '', 'error': ''}
                fecha_final = {'valor': '', 'error': ''}
                criterio = ''
                parametro_fecha_inicial = ''
                parametro_fecha_final = ''
                if request.method == 'POST':
                    fecha_inicial['valor'] = request.POST['fecha_inicial'].strip()
                    fecha_final['valor'] = request.POST['fecha_final'].strip()
                    criterio = request.POST['criterio'].strip()

                    if fecha_inicial['valor'] != '':
                        validaciones_fecha = Validator().append([
                            Field('fecha_inicial', fecha_inicial['valor']).append([
                                IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                            ]),
                        ]).run(True).pop()

                        if validaciones_fecha['passed'] == True:
                            parametro_fecha_inicial = fecha_inicial['valor']
                        else:
                            for error in validaciones_fecha['errors']:
                                fecha_inicial['error'] = error

                    if fecha_final['valor'] != '':
                        validaciones_fecha = Validator().append([
                            Field('fecha_final', fecha_final['valor']).append([
                                IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                            ]),
                        ]).run(True).pop()

                        if validaciones_fecha['passed'] == True:
                            parametro_fecha_final = fecha_final['valor']
                        else:
                            for error in validaciones_fecha['errors']:
                                fecha_final['error'] = error
                informes_salida = proyecto.lista_informes_salida(criterio, fecha_inicial=parametro_fecha_inicial, fecha_final=parametro_fecha_final)
                pag = Paginador(request, informes_salida, 20, 1)
                return render_to_response('reporteinformessalida.html', {'user': user, 'informes_salida': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Detalles informe de salida almacen
def informes_salida_proyecto_details(request, informe_salida_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_informesalida' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                informe_salida = proyecto.informesalida_set.get(id=informe_salida_id)
                suministros = informe_salida.suministroinformesalidaitem_set.all()
                pag = Paginador(request, suministros, 20, 1)
                return render_to_response('informesalidadetails.html', {'user': user, 'informe_salida': informe_salida, 'suministros': pag, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Ordenes de servicio
def orden_servicio_add(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_cotizacion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id = proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                pag = Paginador(request, proyecto.get_suministros_pendientes_comprar_agrupados_suministro(criterio=criterio, tipo_cotizacion=2), 20, 1)
                return render_to_response('ordenservicioadd.html', {'user': user, 'suministros_requisiciones': pag, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def orden_servicio_proveedor(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_cotizacion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id = proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                qry = "SELECT p.* FROM inverboy_suministroproveedor sp, inverboy_proveedor p WHERE sp.proveedor_id = p.id AND p.estado_proveedor = TRUE AND sp.suministro_id IN (	SELECT s.id	FROM inverboy_suministrorequisicion sr, inverboy_requisicion r, inverboy_suministroapuproyecto sap, inverboy_suministro s	WHERE sap.suministro_id = s.id AND sr.suministro_id = sap.id	AND sr.cantidad_comprada < sr.cantidad_requerida	AND sr.requisicion_id = r.id	AND r.proyecto_id = " + str(proyecto_id) + "    AND r.estado = 2	AND s.clasificacion_general != 'Material'	GROUP BY s.id   )"
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                    if criterio != '':
                        criterio = criterio.replace("'",'"')
                        try:
                            criterio = int(criterio)
                            qry = qry + " AND p.identificacion = " + str(criterio)
                        except:
                            qry = qry + " AND (p.razon_social LIKE '%%" + criterio + "%%' OR p.nombre_comercial LIKE '%%" + criterio +"%%')"
                qry = qry + " GROUP BY p.id ORDER BY p.razon_social"
                proveedores = Proveedor.objects.raw(qry)
                lista_proveedores = list(proveedores)
                pag = Paginador(request, lista_proveedores, 20, 1)
                return render_to_response('ordenservicioproveedor.html', {'user': user, 'proveedores': pag, 'proyecto': proyecto, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Reporte cotizaciones ordenes de servicio
def cotizaciones_orden_servicio_proyecto_search(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_cotizacion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                cotizaciones = proyecto.lista_cotizaciones(tipo=2, criterio=criterio)
                pag = Paginador(request, cotizaciones, 20, 1)
                return render_to_response('reportecotizacionesordenservicio.html', {'user': user, 'cotizaciones': pag, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Reporte ordenes de servicio
def ordenes_servicio_proyecto_search(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_ordenservicio' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                fecha_inicial = {'valor': '', 'error': ''}
                fecha_final = {'valor': '', 'error': ''}
                criterio = ''
                parametro_fecha_inicial = ''
                parametro_fecha_final = ''
                if request.method == 'POST':
                    fecha_inicial['valor'] = request.POST['fecha_inicial'].strip()
                    fecha_final['valor'] = request.POST['fecha_final'].strip()
                    criterio = request.POST['criterio'].strip()

                    if fecha_inicial['valor'] != '':
                        validaciones_fecha = Validator().append([
                            Field('fecha_inicial', fecha_inicial['valor']).append([
                                IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                            ]),
                        ]).run(True).pop()

                        if validaciones_fecha['passed'] == True:
                            parametro_fecha_inicial = fecha_inicial['valor']
                        else:
                            for error in validaciones_fecha['errors']:
                                fecha_inicial['error'] = error

                    if fecha_final['valor'] != '':
                        validaciones_fecha = Validator().append([
                            Field('fecha_final', fecha_final['valor']).append([
                                IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                            ]),
                        ]).run(True).pop()

                        if validaciones_fecha['passed'] == True:
                            parametro_fecha_final = fecha_final['valor']
                        else:
                            for error in validaciones_fecha['errors']:
                                fecha_final['error'] = error
                ordenes_servicio = proyecto.lista_ordenes_servicio(criterio, fecha_inicial=parametro_fecha_inicial, fecha_final=parametro_fecha_final)
                pag = Paginador(request, ordenes_servicio, 20, 1)
                return render_to_response('reporteordenesservicio.html', {'user': user, 'ordenes_servicio': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Detalles orden de servicio
def ordenes_servicio_proyecto_details(request, orden_servicio_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_ordenservicio' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
                orden_servicio.calcular_valores()
                suministros = orden_servicio.suministroordenservicioitem_set.all()
                pag = Paginador(request, suministros, 20, 1)
                return render_to_response('ordenserviciodetails.html', {'user': user, 'orden_servicio': orden_servicio, 'suministros': pag, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar orden de servicio
def ordenes_servicio_proyecto_change(request, orden_servicio_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_ordenservicio' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
                if orden_servicio.permite_modificaciones():
                    valores_discriminados = {'subtotal': 0, 'valor_iva': 0, 'valor_total': 0}

                    error = ''
                    items_orden_servicio = orden_servicio.suministroordenservicioitem_set.all()
                    
                    terceros = []

                    if request.method == 'POST':
                        suministros = None
                        try:
                            suministros = request.session['suministros']
                        except :
                            pass
                        if suministros != None:
                            form = OrdenServicioForm(request.POST)
                            if form.is_valid():
                                if len(suministros) > 0:
                                    # Valida que las cantidades esten disponibles
                                    cantidades_disponibles = True
                                    for suministro in suministros:
                                        cantidad_requerida = None
                                        try:
                                            cantidad_requerida = SuministroRequisicion.objects.filter(requisicion__proyecto=proyecto, suministro__suministro__id=suministro['suministro'].id, cantidad_comprada__lt=F('cantidad_requerida')).aggregate(Sum('cantidad_requerida'))['cantidad_requerida__sum']
                                        except :
                                            pass
                                        if cantidad_requerida == None:
                                            cantidad_requerida = 0
                                        cantidad_comprada_orden_actual = None
                                        try:
                                            cantidad_comprada_orden_actual = orden_servicio.suministroordenservicioitem_set.get(suministro__id=suministro['suministro'].id).suministroordenservicio_set.aggregate(Sum('cantidad'))['cantidad__sum']
                                        except :
                                            pass
                                        if cantidad_comprada_orden_actual == None:
                                            cantidad_comprada_orden_actual = 0
                                        cantidad_disponible = round(cantidad_requerida + cantidad_comprada_orden_actual, 2)
                                        if suministro['cantidad'] > cantidad_disponible:
                                            cantidades_disponibles = False

                                        valores_discriminados['valor_total'] = round(valores_discriminados['valor_total'] + (suministro['cantidad'] * suministro['precio']), 2)

                                    if cantidades_disponibles:
                                        orden_servicio.fecha_extendida = form.cleaned_data['fecha_entrega']
                                        orden_servicio.observaciones = form.cleaned_data['observaciones'].strip()
                                        if orden_servicio.permite_modificar_propiedades():
                                            orden_servicio.amortizacion = form.cleaned_data['amortizacion_anticipo']
                                            # Si el porcentaje de amotizacion anticipo es mayor a cero se elimina el permiso para que se pueda modificar la orden de servicio
                                            if orden_servicio.amortizacion > 0:
                                                orden_servicio.permiso_modificar = False
                                            else:
                                                orden_servicio.permiso_modificar = True
                                            orden_servicio.retencion_garantia = form.cleaned_data['retencion_garantia']
                                            orden_servicio.rete_ica = form.cleaned_data['rete_ica']
                                            orden_servicio.rete_fuente = form.cleaned_data['rete_fuente']
                                            orden_servicio.forma_pago = form.cleaned_data['forma_pago']
                                            if orden_servicio.forma_pago == '4':
                                                orden_servicio.parametro_pago = form.cleaned_data['parametro_pago'].strip()
                                            else:
                                                orden_servicio.parametro_pago = ''
                                            if orden_servicio.proveedor.regimen_tributario == 1:
                                                orden_servicio.tipo_iva = form.cleaned_data['tipo_iva']
                                                orden_servicio.porcentaje_iva = form.cleaned_data['porcentaje_iva']
                                                if orden_servicio.tipo_iva == '1':
                                                    orden_servicio.porcentaje_a_i_u = form.cleaned_data['porcentaje_a_i_u']
                                                    orden_servicio.porcentaje_utilidad = form.cleaned_data['porcentaje_utilidad']
                                                if orden_servicio.tipo_iva == '3':
                                                    orden_servicio.porcentaje_a_i_u = form.cleaned_data['porcentaje_a_i_u']
                                            else:
                                                orden_servicio.tipo_iva = None
                                                orden_servicio.porcentaje_a_i_u = 0
                                                orden_servicio.porcentaje_utilidad = 0
                                                orden_servicio.porcentaje_iva = 0
                                            if form.cleaned_data['aplica_tercero']:
                                                orden_servicio.tercero = form.cleaned_data['tercero']
                                            else:
                                                orden_servicio.tercero = None
                                            if form.cleaned_data['aplica_cooperativa']:
                                                orden_servicio.aplica_cooperativa = form.cleaned_data['aplica_cooperativa']
                                                orden_servicio.base_gravable_cooperativa = form.cleaned_data['base_gravable_cooperativa']
                                                orden_servicio.porcentaje_iva_cooperativa = form.cleaned_data['porcentaje_iva_cooperativa']
                                            else:
                                                orden_servicio.aplica_cooperativa = False
                                                orden_servicio.base_gravable_cooperativa = 0
                                                orden_servicio.porcentaje_iva_cooperativa = 0
                                        orden_servicio.save()

                                        # Elimina los suministros y actualiza los registros
                                        suministros_afectados = []
                                        for item_orden_servicio in items_orden_servicio:
                                            eliminar_item = True
                                            for suministro in suministros:
                                                if item_orden_servicio.suministro.id == suministro['suministro'].id:
                                                    item_orden_servicio.precio = suministro['precio']
                                                    item_orden_servicio.observaciones = suministro['observaciones']
                                                    item_orden_servicio.save()
                                                    eliminar_item = False
                                                    # Actualiza los registros
                                                    cantidad_actual_orden_servicio = None
                                                    try:
                                                        cantidad_actual_orden_servicio = item_orden_servicio.suministroordenservicio_set.aggregate(Sum('cantidad'))['cantidad__sum']
                                                    except :
                                                        pass
                                                    if cantidad_actual_orden_servicio == None:
                                                        cantidad_actual_orden_servicio = 0
                                                    if suministro['cantidad'] < cantidad_actual_orden_servicio:
                                                        suministros_orden_servicio = item_orden_servicio.suministroordenservicio_set.all()
                                                        suma_cantidades = 0
                                                        ultimo_suministro_orden_servicio = None
                                                        for suministro_orden_servicio in suministros_orden_servicio:
                                                            if suma_cantidades < suministro['cantidad']:
                                                                suma_cantidades += suministro_orden_servicio.cantidad
                                                                ultimo_suministro_orden_servicio = suministro_orden_servicio
                                                            else:
                                                                # Actualiza los registros
                                                                # Actualiza el suministro_apu_proyecto
                                                                suministro_apu = suministro_orden_servicio.suministro.suministro
                                                                suministro_apu.cantidad_comprada = round(suministro_apu.cantidad_comprada - suministro_orden_servicio.cantidad, 2)
                                                                suministro_apu.cantidad_requerida = round(suministro_apu.cantidad_requerida + suministro_orden_servicio.cantidad, 2)
                                                                suministro_apu.save()
                                                                # Actualiza el suministro_requisicion
                                                                suministro_requisicion = suministro_orden_servicio.suministro
                                                                suministro_requisicion.cantidad_comprada = round(suministro_requisicion.cantidad_comprada - suministro_orden_servicio.cantidad, 2)
                                                                suministro_requisicion.save()

                                                                # Elimina el registro
                                                                suministro_orden_servicio.delete()
                                                        if suma_cantidades > suministro['cantidad']:
                                                            diferencia = round(suma_cantidades - suministro['cantidad'], 2)
                                                            # Actualiza los registros
                                                            # Actualiza el suministro_apu_proyecto
                                                            suministro_apu = ultimo_suministro_orden_servicio.suministro.suministro
                                                            suministro_apu.cantidad_comprada = round(suministro_apu.cantidad_comprada - diferencia, 2)
                                                            suministro_apu.cantidad_requerida = round(suministro_apu.cantidad_requerida + diferencia, 2)
                                                            suministro_apu.save()
                                                            # Actualiza el suministro_requisicion
                                                            suministro_requisicion = ultimo_suministro_orden_servicio.suministro
                                                            suministro_requisicion.cantidad_comprada = round(suministro_requisicion.cantidad_comprada - diferencia, 2)
                                                            suministro_requisicion.save()
                                                            # Actualiza el suministro_orden_servicio
                                                            ultimo_suministro_orden_servicio.cantidad = round(ultimo_suministro_orden_servicio.cantidad - diferencia, 2)
                                                            ultimo_suministro_orden_servicio.save()

                                                    elif suministro['cantidad'] > cantidad_actual_orden_servicio: # Si la nueva cantidad es mayor a la cantidad comprada
                                                        # Actualiza los registros
                                                        suministros_requisiciones = proyecto.get_suministros_pendientes_comprar(suministro_id=suministro['suministro'].id, clasificacion_general=['Equipo', 'Mano de obra', 'Transporte', 'Plenitareas'])

                                                        cantidad_comprada = cantidad_actual_orden_servicio
                                                        cantidad = suministro['cantidad']

                                                        for suministro_requisicion in suministros_requisiciones:
                                                            cantidad_comprada_suministro_requicision = 0.0
                                                            if cantidad_comprada < cantidad:
                                                                if (round(cantidad-cantidad_comprada, 2)) <= (round(suministro_requisicion.cantidad_requerida-suministro_requisicion.cantidad_comprada, 2)):
                                                                    cantidad_comprada_suministro_requicision = round(cantidad - cantidad_comprada, 2)
                                                                elif (round(cantidad-cantidad_comprada, 2)) > (round(suministro_requisicion.cantidad_requerida-suministro_requisicion.cantidad_comprada, 2)):
                                                                    cantidad_comprada_suministro_requicision = round(suministro_requisicion.cantidad_requerida-suministro_requisicion.cantidad_comprada, 2)
                                                                cantidad_comprada = round(cantidad_comprada + cantidad_comprada_suministro_requicision, 2)
                                                                if cantidad_comprada_suministro_requicision > 0:
                                                                    # Actualiza la cantidad comprada en suministro apu proyecto
                                                                    suministro_apu_proyecto = suministro_requisicion.suministro
                                                                    suministro_apu_proyecto.cantidad_comprada = round(suministro_apu_proyecto.cantidad_comprada + cantidad_comprada_suministro_requicision, 2)
                                                                    # Actualiza la cantidad requerida del suministro en el apu proyecto
                                                                    suministro_apu_proyecto.cantidad_requerida = round(suministro_apu_proyecto.cantidad_requerida - cantidad_comprada_suministro_requicision, 2)
                                                                    suministro_apu_proyecto.save()
                                                                    # Actualiza la cantidad comprada en suministro requicisión
                                                                    suministro_requisicion.cantidad_comprada = round(suministro_requisicion.cantidad_comprada + cantidad_comprada_suministro_requicision, 2)
                                                                    suministro_requisicion.save()

                                                                    try:
                                                                        suministro_orden_servicio = orden_servicio.suministroordenservicio_set.get(suministro=suministro_requisicion, suministro_orden_servicio_item=item_orden_servicio)
                                                                        suministro_orden_servicio.cantidad = round(suministro_orden_servicio.cantidad + cantidad_comprada_suministro_requicision, 2)
                                                                        suministro_orden_servicio.save()
                                                                    except :
                                                                        # Crea el nuevo suministro de la orden de servicio
                                                                        suministro_orden_servicio = SuministroOrdenServicio()
                                                                        suministro_orden_servicio.suministro = suministro_requisicion
                                                                        suministro_orden_servicio.cantidad = cantidad_comprada_suministro_requicision
                                                                        suministro_orden_servicio.suministro_orden_servicio_item = item_orden_servicio
                                                                        suministro_orden_servicio.orden_servicio = orden_servicio
                                                                        suministro_orden_servicio.save()
                                                        # Actualiza el precio del suministro correspondiente al proveedor
                                                        suministro_proveedor = SuministroProveedor.objects.get(suministro=item_orden_servicio.suministro, proveedor=orden_servicio.proveedor)
                                                        suministro_proveedor.precio_suministro = item_orden_servicio.precio
                                                        suministro_proveedor.save()
                                                        # Borra el suministro de las cotizaciones
                                                        SuministroCotizacion.objects.filter(suministro=item_orden_servicio.suministro).delete()
                                                    # Elimina el suministro de la lista de session para no tenerlo más en cuenta
                                                    suministros_afectados.append(suministro)
                                            if eliminar_item:
                                                # Actualiza los registros
                                                suministros_orden_servicio = item_orden_servicio.suministroordenservicio_set.all()
                                                for suministro_orden_servicio in suministros_orden_servicio:
                                                    # Actualiza el suministro_apu_proyecto
                                                    suministro_apu = suministro_orden_servicio.suministro.suministro
                                                    suministro_apu.cantidad_comprada = round(suministro_apu.cantidad_comprada - suministro_orden_servicio.cantidad, 2)
                                                    suministro_apu.cantidad_requerida = round(suministro_apu.cantidad_requerida + suministro_orden_servicio.cantidad, 2)
                                                    suministro_apu.save()
                                                    # Actualiza el suministro_requisicion
                                                    suministro_requisicion = suministro_orden_servicio.suministro
                                                    suministro_requisicion.cantidad_comprada = round(suministro_requisicion.cantidad_comprada - suministro_orden_servicio.cantidad, 2)
                                                    suministro_requisicion.save()

                                                    # Elimina el registro
                                                    suministro_orden_servicio.delete()
                                                # Elimina el registro
                                                item_orden_servicio.delete()

                                        # Elimina el suministro de la lista de session para no tenerlo más en cuenta
                                        for suministro_afectado in suministros_afectados:
                                            suministros.remove(suministro_afectado)

                                        # Crea nuevos registros para los nuevos suministros adicionados
                                        for suministro in suministros:
                                            suministros_requisiciones = proyecto.get_suministros_pendientes_comprar(suministro_id=suministro['suministro'].id, clasificacion_general=['Equipo', 'Mano de obra', 'Transporte', 'Plenitareas'])

                                            #Registra suministro_orden_servicio_item (Objeto que guarda las propiedades generales del suministro de la compra: precio y observaciones)
                                            suministro_orden_servicio_item = SuministroOrdenServicioItem()
                                            suministro_orden_servicio_item.orden_servicio = orden_servicio
                                            suministro_orden_servicio_item.suministro = suministro['suministro']
                                            suministro_orden_servicio_item.precio = suministro['precio']
                                            suministro_orden_servicio_item.observaciones = suministro['observaciones']
                                            suministro_orden_servicio_item.save()
                                            cantidad_comprada = 0.0
                                            cantidad = suministro['cantidad']

                                            for suministro_requisiciones in suministros_requisiciones:
                                                cantidad_comprada_suministro_requicision = 0.0
                                                if cantidad_comprada < cantidad:
                                                    if (round(cantidad-cantidad_comprada, 2)) <= (round(suministro_requisiciones.cantidad_requerida-suministro_requisiciones.cantidad_comprada, 2)):
                                                        cantidad_comprada_suministro_requicision = round(cantidad - cantidad_comprada, 2)
                                                    elif (round(cantidad-cantidad_comprada, 2)) > (round(suministro_requisiciones.cantidad_requerida-suministro_requisiciones.cantidad_comprada, 2)):
                                                        cantidad_comprada_suministro_requicision = round(suministro_requisiciones.cantidad_requerida-suministro_requisiciones.cantidad_comprada, 2)
                                                    cantidad_comprada = round(cantidad_comprada + cantidad_comprada_suministro_requicision, 2)
                                                    if cantidad_comprada_suministro_requicision > 0:
                                                        # Actualiza la cantidad comprada en suministro apu proyecto
                                                        suministro_apu_proyecto = suministro_requisiciones.suministro
                                                        suministro_apu_proyecto.cantidad_comprada = round(suministro_apu_proyecto.cantidad_comprada + cantidad_comprada_suministro_requicision, 2)
                                                        # Actualiza la cantidad requerida del suministro en el apu proyecto
                                                        suministro_apu_proyecto.cantidad_requerida = round(suministro_apu_proyecto.cantidad_requerida - cantidad_comprada_suministro_requicision, 2)
                                                        suministro_apu_proyecto.save()
                                                        # Actualiza la cantidad comprada en suministro requicisión
                                                        suministro_requisiciones.cantidad_comprada = round(suministro_requisiciones.cantidad_comprada + cantidad_comprada_suministro_requicision, 2)
                                                        suministro_requisiciones.save()
                                                        # Crea el nuevo suministro de la orden de servicio
                                                        suministro_orden_servicio = SuministroOrdenServicio()
                                                        suministro_orden_servicio.suministro = suministro_requisiciones
                                                        suministro_orden_servicio.cantidad = cantidad_comprada_suministro_requicision
                                                        suministro_orden_servicio.suministro_orden_servicio_item = suministro_orden_servicio_item
                                                        suministro_orden_servicio.orden_servicio = orden_servicio
                                                        suministro_orden_servicio.save()
                                            # Actualiza el precio del suministro correspondiente al proveedor
                                            suministro_proveedor = SuministroProveedor.objects.get(suministro=suministro['suministro'].id, proveedor=orden_servicio.proveedor)
                                            suministro_proveedor.precio_suministro = suministro['precio']
                                            suministro_proveedor.save()
                                        actualizar_estado_requisiciones(proyecto)
                                        actualizar_cotizaciones(proyecto)
                                        # Elimina las variables de session
                                        del request.session['suministros']
                                        return HttpResponseRedirect('/inverboy/home/ordenesservicioproyectodetails/' + str(orden_servicio_id) + '/' + str(proyecto_id) + '/')
                                    else:
                                        error = 'Las nuevas cantidades deben ser proporcionales a las cantidades requeridas'
                                else:
                                    # Acciones a ejecutar si se han eliminado todos los suministros de la oreden de servicio
                                    error = 'Se eliminaron todos los suministros!!'
                        else:
                            return HttpResponseRedirect('/inverboy/home/proyectodetails/' + str(proyecto_id) + '/')
                    else:
                        suministros = []

                        for item_orden_servicio in items_orden_servicio:
                            cantidad = item_orden_servicio.suministroordenservicio_set.all().aggregate(Sum('cantidad'))['cantidad__sum']
                            observaciones = ''
                            if item_orden_servicio.observaciones != None:
                                observaciones = item_orden_servicio.observaciones
                            suministros.append({'suministro': item_orden_servicio.suministro, 'cantidad': cantidad, 'precio': item_orden_servicio.precio, 'observaciones': observaciones})
                            valores_discriminados['valor_total'] = round(valores_discriminados['valor_total'] + (cantidad * item_orden_servicio.precio), 2)

                        request.session['suministros'] = suministros
                        request.session['suministros_agregar'] = []

                        form = OrdenServicioForm(initial={'fecha_entrega': orden_servicio.fecha_entrega, 'amortizacion_anticipo': orden_servicio.amortizacion, 'retencion_garantia': orden_servicio.retencion_garantia, 'rete_ica': orden_servicio.rete_ica, 'rete_fuente':orden_servicio.rete_fuente, 'forma_pago': str(orden_servicio.forma_pago), 'parametro_pago': orden_servicio.parametro_pago, 'observaciones': orden_servicio.observaciones, 'tipo_iva': str(orden_servicio.tipo_iva), 'porcentaje_a_i_u': orden_servicio.porcentaje_a_i_u, 'porcentaje_utilidad': orden_servicio.porcentaje_utilidad, 'porcentaje_iva': orden_servicio.porcentaje_iva, 'aplica_tercero': orden_servicio.tercero, 'tercero': orden_servicio.tercero, 'aplica_cooperativa': orden_servicio.aplica_cooperativa, 'base_gravable_cooperativa': orden_servicio.base_gravable_cooperativa, 'porcentaje_iva_cooperativa': orden_servicio.porcentaje_iva_cooperativa})

                    terceros = Proveedor.objects.filter(estado_proveedor=True).exclude(id=orden_servicio.proveedor.id).order_by('razon_social').order_by('razon_social')
                    form.fields['tercero'].queryset = terceros

                    pag = Paginador(request, suministros, 20, 1)
                    return render_to_response('ordenserviciochange.html', {'user': user, 'form': form, 'orden_servicio': orden_servicio, 'suministros': pag, 'valores_discriminados': valores_discriminados, 'terceros': terceros, 'error': error, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Nuevo corte diario de obra
def ordenes_servicio_corte_diario_obra_add(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_cortediarioobra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                ordenes_servicio = proyecto.lista_ordenes_servicio(criterio=criterio, estado=1)
                for orden_servicio in ordenes_servicio:
                    if len(orden_servicio.suministroordenservicio_set.filter(cantidad_entregada__lt=F('cantidad'))) == 0:
                        ordenes_servicio = ordenes_servicio.exclude(id=orden_servicio.id)
                pag = Paginador(request, ordenes_servicio, 20, 1)
                return render_to_response('cortediarioobraadd_1ordenesservicio.html', {'user': user, 'ordenes_servicio': pag, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def corte_diario_obra_add(request, orden_servicio_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_cortediarioobra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
                fecha_actual = date.today()
                error_permiso_registo = ''
                cortes_diarios_obra_fecha_actual = orden_servicio.cortediarioobra_set.filter(fecha_corte__year=fecha_actual.year, fecha_corte__month=fecha_actual.month, fecha_corte__day=fecha_actual.day)
                if len(cortes_diarios_obra_fecha_actual) > 0:
                    if len(cortes_diarios_obra_fecha_actual.filter(persona=usuario)) > 0:
                        error_permiso_registo = 'Ya ha realizado el corte diario de obra del dia de hoy'

                if error_permiso_registo == '':
                    error = ''
                    if request.method == 'POST':
                        suministros_corte_diario_obra = None
                        try:
                            suministros_corte_diario_obra = request.session['suministros_corte_diario_obra']
                        except :
                            pass
                        if suministros_corte_diario_obra != None:
                            if len(suministros_corte_diario_obra) > 0:
                                corte_diario_obra = CorteDiarioObra()
                                corte_diario_obra.orden_servicio = orden_servicio
                                corte_diario_obra.persona = usuario
                                corte_diario_obra.save()
                                for suministro in suministros_corte_diario_obra:
                                    suministros = orden_servicio.suministroordenservicio_set.filter(suministro__suministro__suministro__id=suministro['id'])
                                    suministros = suministros.order_by('suministro__requisicion__fecha_arribo')
                                    cantidad_recibida = 0.0
                                    cantidad = float(suministro['cantidad'])
                                    for suministro in suministros:
                                        cantidad_recibida_suministro_orden_servicio = 0.0
                                        if cantidad_recibida < cantidad:
                                            if (round(cantidad-cantidad_recibida, 2)) <= float(str(round(suministro.cantidad-suministro.cantidad_entregada, 2))):
                                                cantidad_recibida_suministro_orden_servicio = round(cantidad - cantidad_recibida, 2)
                                            elif (round(cantidad-cantidad_recibida, 2)) > float(str(round(suministro.cantidad-suministro.cantidad_entregada, 2))):
                                                cantidad_recibida_suministro_orden_servicio = round(suministro.cantidad - suministro.cantidad_entregada, 2)
                                            cantidad_recibida = round(cantidad_recibida + cantidad_recibida_suministro_orden_servicio, 2)
                                            if cantidad_recibida_suministro_orden_servicio > 0:
                                                # Actualiza la cantidad comprada en suministro apu proyecto
                                                suministro_apu_proyecto = suministro.suministro.suministro
                                                suministro_apu_proyecto.cantidad_almacen = round(suministro_apu_proyecto.cantidad_almacen + cantidad_recibida_suministro_orden_servicio, 2)
                                                suministro_apu_proyecto.save()
                                                # Si el suministro pertenece a un apu de manejo estandar se actualiza las cantidades aproximadas
                                                if suministro_apu_proyecto.apu_proyecto.apu_manejo_estandar == True and suministro_apu_proyecto.id == suministro_apu_proyecto.apu_proyecto.suministro_estandar.id:
                                                    apu_proyecto = suministro_apu_proyecto.apu_proyecto
                                                    apu_proyecto.actualizar_aproximacion_cantidad_suministros()
                                                # Actualiza la cantidad comprada en el suministro requisicion
                                                suministro_requisicion = suministro.suministro
                                                suministro_requisicion.cantidad_almacen = round(suministro_requisicion.cantidad_almacen + cantidad_recibida_suministro_orden_servicio, 2)
                                                suministro_requisicion.save()
                                                # Actualiza la cantidad comprada en el suministro orden de servicio
                                                suministro.cantidad_entregada = round(suministro.cantidad_entregada + cantidad_recibida_suministro_orden_servicio, 2)
                                                suministro.save()
                                                # Crea el nuevo suministro del acta de obra
                                                suministro_corte_diario_obra = SuministroCorteDiarioObra()
                                                suministro_corte_diario_obra.suministro = suministro
                                                suministro_corte_diario_obra.cantidad = cantidad_recibida_suministro_orden_servicio
                                                suministro_corte_diario_obra.corte_diario_obra = corte_diario_obra
                                                suministro_corte_diario_obra.save()
                                del request.session['suministros_corte_diario_obra']

                                # Redirecciona a los detalles del nuevo registro
                                mensaje = u'Se ha realizado el corte diario de obra'
                                suministros = corte_diario_obra.suministrocortediarioobra_set.all()
                                suministros_corte_diario_obra = []
                                for suministro in suministros:
                                    suministro_tmp = suministro
                                    suministro_adicionado = False
                                    for suministro_tmp2 in suministros_corte_diario_obra:
                                        if suministro_tmp2.suministro.suministro.suministro.suministro.id == suministro_tmp.suministro.suministro.suministro.suministro.id:
                                            suministro_tmp2.cantidad = round(suministro_tmp2.cantidad + suministro_tmp.cantidad, 2)
                                            suministro_adicionado = True
                                    if suministro_adicionado == False:
                                        suministros_corte_diario_obra.append(suministro_tmp)
                                pag = Paginador(request, suministros_corte_diario_obra, 20, 1)
                                return render_to_response('cortediarioobradetails.html', {'user': user, 'corte_diario_obra': corte_diario_obra, 'suministros': pag, 'proyecto': proyecto, 'mensaje': mensaje})
                            else:
                                error = u'No se han ingresado items en este corte diario de obra'
                    else:
                        request.session['suministros_corte_diario_obra'] = []
                    suministros = orden_servicio.suministroordenservicio_set.all().order_by('suministro__suministro__suministro__nombre')
                    suministros_orden_servicio = []
                    for suministro in suministros:
                        suministro_tmp = suministro
                        suministro_adicionado = False
                        for suministro_tmp2 in suministros_orden_servicio:
                            if suministro_tmp2['suministro'].suministro.suministro.suministro.id == suministro_tmp.suministro.suministro.suministro.id:
                                suministro_tmp2['suministro'].cantidad = round(suministro_tmp2['suministro'].cantidad + suministro_tmp.cantidad, 2)
                                suministro_tmp2['suministro'].cantidad_entregada = round(suministro_tmp2['suministro'].cantidad_entregada + suministro_tmp.cantidad_entregada, 2)
                                suministro_tmp2['porcentaje_entregado'] = round((round(100 * suministro_tmp2['suministro'].cantidad_entregada, 2))/suministro_tmp2['suministro'].cantidad, 2)
                                suministro_adicionado = True
                        if suministro_adicionado == False:
                            suministros_orden_servicio.append({'suministro': suministro_tmp, 'cantidad_nuevo_informe': '', 'porcentaje_entregado': round(((round(100*suministro_tmp.cantidad_entregada, 2))/suministro_tmp.cantidad), 2), 'nuevo_porcentaje_entregado': ''})
                    pag = Paginador(request, suministros_orden_servicio, 20, 1)
                    return render_to_response('cortediarioobraadd.html', {'user': user, 'orden_servicio': orden_servicio, 'proyecto': proyecto, 'suministros': pag, 'error': error })
                else:
                    mensaje = error_permiso_registo
                    personas = proyecto.personaproyecto_set.filter(estado=True)
                    return render_to_response('proyectodetails.html', {'user': user, 'proyecto': proyecto, 'personas': personas, 'mensaje': mensaje})

        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Reporte cortes diarios de obra
def cortes_diario_obra_proyecto_search(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_cortediarioobra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                fecha_inicial = {'valor': '', 'error': ''}
                fecha_final = {'valor': '', 'error': ''}
                criterio = ''
                parametro_fecha_inicial = ''
                parametro_fecha_final = ''
                if request.method == 'POST':
                    fecha_inicial['valor'] = request.POST['fecha_inicial'].strip()
                    fecha_final['valor'] = request.POST['fecha_final'].strip()
                    criterio = request.POST['criterio'].strip()

                    if fecha_inicial['valor'] != '':
                        validaciones_fecha = Validator().append([
                            Field('fecha_inicial', fecha_inicial['valor']).append([
                                IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                            ]),
                        ]).run(True).pop()

                        if validaciones_fecha['passed'] == True:
                            parametro_fecha_inicial = fecha_inicial['valor']
                        else:
                            for error in validaciones_fecha['errors']:
                                fecha_inicial['error'] = error

                    if fecha_final['valor'] != '':
                        validaciones_fecha = Validator().append([
                            Field('fecha_final', fecha_final['valor']).append([
                                IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                            ]),
                        ]).run(True).pop()

                        if validaciones_fecha['passed'] == True:
                            parametro_fecha_final = fecha_final['valor']
                        else:
                            for error in validaciones_fecha['errors']:
                                fecha_final['error'] = error

                costes_diario_obra = proyecto.lista_cortes_diario_obra(criterio=criterio, fecha_inicial=parametro_fecha_inicial, fecha_final=parametro_fecha_final)
                pag = Paginador(request, costes_diario_obra, 20, 1)
                return render_to_response('reportecortesdiarioobra.html', {'user': user, 'cortes_diario_obra': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Detalles corte diario de obra
def cortes_diario_obra_proyecto_details(request, corte_diario_obra_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_cortediarioobra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                corte_diario_obra = CorteDiarioObra.objects.get(id=corte_diario_obra_id, orden_servicio__proyecto=proyecto)
                suministros = corte_diario_obra.suministrocortediarioobra_set.all()
                suministros_corte_diario_obra = []
                for suministro in suministros:
                    suministro_tmp = suministro
                    suministro_adicionado = False
                    for suministro_tmp2 in suministros_corte_diario_obra:
                        if suministro_tmp2.suministro.suministro.suministro.suministro.id == suministro_tmp.suministro.suministro.suministro.suministro.id:
                            suministro_tmp2.cantidad = round(suministro_tmp2.cantidad + suministro_tmp.cantidad, 2)
                            suministro_adicionado = True
                    if suministro_adicionado == False:
                        suministros_corte_diario_obra.append(suministro_tmp)
                pag = Paginador(request, suministros_corte_diario_obra, 20, 1)
                return render_to_response('cortediarioobradetails.html', {'user': user, 'corte_diario_obra': corte_diario_obra, 'suministros': pag, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Acta de recibo de obra
def acta_recibo_obra_proyecto_add(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_actareciboobra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                qry = "SELECT p.* FROM inverboy_proveedor p, inverboy_ordenservicio os, inverboy_cortediarioobra cdo WHERE ((p.id = os.proveedor_id AND os.tercero_id IS NULL) OR (p.id = os.tercero_id)) AND cdo.orden_servicio_id = os.id AND cdo.estado = TRUE AND os.proyecto_id = %s" % proyecto_id
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                    if criterio != '':
                        criterio = criterio.replace("'",'"')
                        try:
                            int(criterio)
                            qry = qry + " AND p.identificacion = %s " % criterio
                        except :
                            qry = qry + " AND (p.razon_social LIKE '%%" + criterio + "%%' OR p.nombre_comercial LIKE '%%" + criterio + "%%')"
                qry = qry + " GROUP BY p.id"
                proveedores = list(Proveedor.objects.raw(qry))
                pag = Paginador(request, proveedores, 20, 1)
                return render_to_response('actareciboobraadd_1proveedores.html', {'user': user, 'proveedores': pag, 'criterio': criterio, 'proyecto': proyecto })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Ordenes de servicio de proveedor Acta de recibo de obra
def ordenes_servicio_proveedor_acta_recibo_obra_proyecto_add(request, proveedor_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_actareciboobra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                proveedor = Proveedor.objects.get(id=proveedor_id)
                qry = "SELECT os.* FROM inverboy_ordenservicio os, inverboy_proveedor p, inverboy_cortediarioobra cdo WHERE p.id = " + str(proveedor_id) + " AND ((p.id = os.proveedor_id AND os.tercero_id IS NULL) OR (p.id = os.tercero_id)) AND cdo.orden_servicio_id = os.id AND cdo.estado = TRUE AND os.proyecto_id = " + str(proyecto_id) + " GROUP BY os.id"
                ordenes_servicio = list(proyecto.ordenservicio_set.raw(qry))
                pag = Paginador(request, ordenes_servicio, 20, 1)
                return render_to_response('actareciboobraadd_2ordenesservicioproveedor.html', {'user': user, 'proveedor': proveedor, 'ordenes_servicio': pag, 'proyecto': proyecto })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Items orden de servicio Acta de recibo de obra
def items_orden_servicio_proveedor_acta_recibo_obra_proyecto_add(request, orden_servicio_id, proyecto_id):
    from django.db.models import Sum
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_actareciboobra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
                #Fecha en blanco
                fecha_inicio = ''
                fecha_inicio_rango = '2013-01-01'
                #Fecha actual
                fecha = datetime.date.today()
                hoy = fecha.strftime("%Y-%m-%d")
                fecha_fin = hoy
                error_fecha_inicio = ''
                error_fecha_fin = ''
                if request.method == 'POST':
                    fecha_inicio = request.POST['fecha_inicio'].strip()
                    fecha_fin = request.POST['fecha_fin'].strip()
                    if fecha_inicio != '':
                        error_fecha_inicio = validar_fecha(fecha_inicio)
                    error_fecha_fin = validar_fecha(fecha_fin)
                    if error_fecha_inicio == '' and error_fecha_fin == '':
                        if fecha_inicio != '':
                            fecha_inicio_rango = fecha_inicio
                        if fecha_fin == '':
                            fecha_fin = hoy
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

                #Formulario busqueda fecha
                return render_to_response('actareciboobraadd_3itemsordenesservicio.html', { 'user': user, 'orden_servicio': orden_servicio, 'matriz': matriz, 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin, 'error_fecha_inicio': error_fecha_inicio, 'error_fecha_fin': error_fecha_fin, 'proyecto': proyecto })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Guardar registro acta de recibo de obra
def registrar_acta_recibo_obra_proyecto_add(request, proveedor_id, orden_servicio_id, proyecto_id):
    from django.db.models import Sum
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_actareciboobra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
                proveedor = orden_servicio.proveedor
                #Fecha en blanco
                fecha_inicio = ''
                fecha_inicio_rango = '2013-01-01'
                #Fecha actual
                fecha = datetime.date.today()
                hoy = fecha.strftime("%Y-%m-%d")
                fecha_fin = hoy
                error_fecha_inicio = ''
                error_fecha_fin = ''
                fecha_inicio = request.POST['fecha_inicio'].strip()
                fecha_fin = request.POST['fecha_fin'].strip()
                if fecha_inicio != '':
                    error_fecha_inicio = validar_fecha(fecha_inicio)
                error_fecha_fin = validar_fecha(fecha_fin)
                if error_fecha_inicio == '' and error_fecha_fin == '':
                    if fecha_inicio != '':
                        fecha_inicio_rango = fecha_inicio
                    if fecha_fin == '':
                        fecha_fin = hoy
                    fecha_fin_rango = fecha_fin + ' 23:59:59'
                    suministros_cortes_diario_obra = SuministroCorteDiarioObra.objects.filter(corte_diario_obra__orden_servicio=orden_servicio, corte_diario_obra__estado=True, corte_diario_obra__fecha_corte__range=(fecha_inicio_rango, fecha_fin_rango))
                else:
                    suministros_cortes_diario_obra = []

                if len(suministros_cortes_diario_obra):
                    ids_cortes_obra_diario = suministros_cortes_diario_obra.values('corte_diario_obra__id').annotate(cantidad_total=Sum('cantidad'))

                    #Registro acta recibo de obra
                    acta_recibo_obra = ActaReciboObra()
                    acta_recibo_obra.orden_servicio = orden_servicio
                    acta_recibo_obra.persona = usuario
                    acta_recibo_obra.save()

                    # Verifica si la OS tiene amortizacion anticipo si es asi actualiza la OS cambiandole el permiso_modificar a False
                    if orden_servicio.amortizacion > 0:
                        orden_servicio.permiso_modificar = False
                        orden_servicio.save()

                    #Registro items acta recibo de obra
                    for id_corte_obra_diario in ids_cortes_obra_diario:
                        corte_obra_diario = CorteDiarioObra.objects.get(id=id_corte_obra_diario['corte_diario_obra__id'])
                        corte_obra_diario.estado = False
                        corte_obra_diario.save()
                        item_acta_recibo_obra = ItemActaReciboObra()
                        item_acta_recibo_obra.corte_diario_obra = corte_obra_diario
                        item_acta_recibo_obra.acta_recibo_obra = acta_recibo_obra
                        item_acta_recibo_obra.save()

                    acta_recibo_obra.descuento = request.POST['descuento']
                    acta_recibo_obra.observaciones_descuento= request.POST['observaciones_descuento']
                    acta_recibo_obra.observaciones = request.POST['observaciones']
                    acta_recibo_obra.save()

                    # Redirecciona a los detalles del nuevo registro
                    mensaje = u'Se ha realizado el acta de recibo de obra'

                    return HttpResponseRedirect('/inverboy/home/actasreciboobraproyectodetails/' + str(acta_recibo_obra.id) + '/' + str(proyecto_id) + '/')
                else:
                    mensaje = u'No hay cortes de obra diario registrados en el rango de fechas indicadas'
                    personas = proyecto.personaproyecto_set.filter(estado=True)
                    return render_to_response('proyectodetails.html', {'user': user, 'proyecto': proyecto, 'personas': personas, 'mensaje': mensaje })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Reporte actas de recibo de obra
def actas_recibo_obra_proyecto_search(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_actareciboobra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                fecha_inicial = {'valor': '', 'error': ''}
                fecha_final = {'valor': '', 'error': ''}
                criterio = ''
                parametro_fecha_inicial = ''
                parametro_fecha_final = ''
                if request.method == 'POST':
                    fecha_inicial['valor'] = request.POST['fecha_inicial'].strip()
                    fecha_final['valor'] = request.POST['fecha_final'].strip()
                    criterio = request.POST['criterio'].strip()

                    if fecha_inicial['valor'] != '':
                        validaciones_fecha = Validator().append([
                            Field('fecha_inicial', fecha_inicial['valor']).append([
                                IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                            ]),
                        ]).run(True).pop()

                        if validaciones_fecha['passed'] == True:
                            parametro_fecha_inicial = fecha_inicial['valor']
                        else:
                            for error in validaciones_fecha['errors']:
                                fecha_inicial['error'] = error

                    if fecha_final['valor'] != '':
                        validaciones_fecha = Validator().append([
                            Field('fecha_final', fecha_final['valor']).append([
                                IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                            ]),
                        ]).run(True).pop()

                        if validaciones_fecha['passed'] == True:
                            parametro_fecha_final = fecha_final['valor']
                        else:
                            for error in validaciones_fecha['errors']:
                                fecha_final['error'] = error
                actas_recibo_obra = proyecto.lista_actas_recibo_obra(criterio=criterio, fecha_inicial=parametro_fecha_inicial, fecha_final=parametro_fecha_final)
                pag = Paginador(request, actas_recibo_obra, 20, 1)
                return render_to_response('reporteactasreciboobra.html', {'user': user, 'actas_recibo_obra': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Detalles acta de recibo de obra
def actas_recibo_obra_proyecto_details(request, acta_recibo_obra_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_actareciboobra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                acta_recibo_obra = ActaReciboObra.objects.get(id=acta_recibo_obra_id, orden_servicio__proyecto=proyecto)
                acta_recibo_obra.calcular_valores(opcion_discriminacion_capitulos=True, opcion_discriminacion_subcapitulos=True)
                return render_to_response('actareciboobradetails.html', {'user': user, 'acta_recibo_obra': acta_recibo_obra, 'proyecto': proyecto })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


@user_is_logged
@user_has_permission(permission='inverboy.change_actareciboobra')
@user_is_member_project
def modificar_acta_recibo_obra(request, acta_recibo_obra_id, proyecto_id):
    user = request.user
    proyecto = Proyecto.objects.get(id=proyecto_id)
    acta_recibo_obra = ActaReciboObra.objects.get(id=acta_recibo_obra_id, orden_servicio__proyecto=proyecto)
    if acta_recibo_obra.permite_modificar():
        acta_recibo_obra.calcular_valores()
        if request.method == 'POST':
            items_acta_recibo_obra = request.session['items_acta_recibo_obra']
            for item_acta_recibo_obra in items_acta_recibo_obra['lista_items']:
                for registro in item_acta_recibo_obra['registros']:
                    for item_registro in registro['registros']:
                        suministro_corte_diario = SuministroCorteDiarioObra.objects.get(id=item_registro['id'])
                        if suministro_corte_diario.cantidad != registro['cantidad']:
                            # Actualiza las cantidades
                            diferencia = round(suministro_corte_diario.cantidad - registro['cantidad'], 2)
                            suministro_apu = suministro_corte_diario.suministro.suministro.suministro
                            suministro_apu.cantidad_almacen = round(suministro_apu.cantidad_almacen - diferencia, 2)
                            suministro_apu.save()
                            suministro_requisicion = suministro_corte_diario.suministro.suministro
                            suministro_requisicion.cantidad_almacen = round(suministro_requisicion.cantidad_almacen - diferencia, 2)
                            suministro_requisicion.save()
                            suministro_orden = suministro_corte_diario.suministro
                            suministro_orden.cantidad_entregada = round(suministro_orden.cantidad_entregada - diferencia, 2)
                            suministro_orden.save()
                            suministro_corte_diario.cantidad = round(suministro_corte_diario.cantidad - diferencia, 2)
                            suministro_corte_diario.save()
            return HttpResponseRedirect('/inverboy/home/actasreciboobraproyectodetails/' + str(acta_recibo_obra_id) + '/' + str(proyecto_id) + '/')
        else:
            # Se carga en la session los items del acta
            items_acta_recibo_obra = acta_recibo_obra.items_acta_recibo_obra()
            request.session['items_acta_recibo_obra'] = items_acta_recibo_obra
        return render_to_response('modificaractareciboobra.html', {'user': user, 'acta_recibo_obra': acta_recibo_obra, 'items_acta_recibo_obra': items_acta_recibo_obra, 'proyecto': proyecto})
    return HttpResponseRedirect('/inverboy/home/')


@user_is_logged
@user_has_permission(permission='inverboy.view_actareciboobra')
@user_is_member_project
#Reporte actas de recibo de obra por aprobar
def busqueda_actas_recibo_obra_aprobar(request, proyecto_id):
    user = request.user
    proyecto = Proyecto.objects.get(id=proyecto_id)
    #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
    usuario = Usuario.objects.get(id=user.id)
    if proyecto in usuario.lista_proyectos_vinculados():
        fecha_inicial = {'valor': '', 'error': ''}
        fecha_final = {'valor': '', 'error': ''}
        criterio = ''
        parametro_fecha_inicial = ''
        parametro_fecha_final = ''
        if request.method == 'POST':
            fecha_inicial['valor'] = request.POST['fecha_inicial'].strip()
            fecha_final['valor'] = request.POST['fecha_final'].strip()
            criterio = request.POST['criterio'].strip()

            if fecha_inicial['valor'] != '':
                validaciones_fecha = Validator().append([
                    Field('fecha_inicial', fecha_inicial['valor']).append([
                        IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                    ]),
                ]).run(True).pop()

                if validaciones_fecha['passed'] == True:
                    parametro_fecha_inicial = fecha_inicial['valor']
                else:
                    for error in validaciones_fecha['errors']:
                        fecha_inicial['error'] = error

            if fecha_final['valor'] != '':
                validaciones_fecha = Validator().append([
                    Field('fecha_final', fecha_final['valor']).append([
                        IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                    ]),
                ]).run(True).pop()

                if validaciones_fecha['passed'] == True:
                    parametro_fecha_final = fecha_final['valor']
                else:
                    for error in validaciones_fecha['errors']:
                        fecha_final['error'] = error
        actas_recibo_obra = proyecto.lista_actas_recibo_obra(criterio=criterio, fecha_inicial=parametro_fecha_inicial, fecha_final=parametro_fecha_final, estado_registro=1)
        pag = Paginador(request, actas_recibo_obra, 20, 1)
        return render_to_response('reporteactasreciboobraaprobar.html', {'user': user, 'actas_recibo_obra': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto})


@user_is_logged
@user_has_permission(permission='inverboy.approve_actareciboobra')
@user_is_member_project
#Aprobar acta recibo de obra
def acta_recibo_obra_aprobar(request, acta_recibo_obra_id, proyecto_id):
    proyecto = Proyecto.objects.get(id=proyecto_id)
    acta_recibo_obra = ActaReciboObra.objects.get(orden_servicio__proyecto=proyecto, id=acta_recibo_obra_id)
    if acta_recibo_obra.estado_registro_acta == 1:
        acta_recibo_obra.estado_registro_acta = 2
        acta_recibo_obra.save()
        return HttpResponseRedirect('/inverboy/home/actasreciboobraproyectodetails/' + str(acta_recibo_obra_id) + '/' + str(proyecto_id) + '/')
    return HttpResponseRedirect('/inverboy/home/')


#Nueva orden de giro
def orden_giro_proyecto_add(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_ordengiro' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id = proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            proveedor = None
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                mensaje_error = ''
                if request.method == 'POST':
                    suministros_orden_giro = None
                    try:
                        suministros_orden_giro = request.session['suministros_orden_giro']
                    except :
                        pass
                    if suministros_orden_giro != None:
                        proveedor_id = request.POST['proveedor']
                        if proveedor_id != '':
                            proveedor = Proveedor.objects.get(id=proveedor_id)
                        else:
                            mensaje_error = u'Debe seleccionar un proveedor'
                        if mensaje_error == '':
                            if len(suministros_orden_giro) > 0:
                                #Validar si las cantidades estan disponibles
                                cantidades_disponibles = True
                                for suministro_orden_giro in suministros_orden_giro:
                                    if proyecto.validar_cantidad_suministro_pendientes_comprar(suministro_requisicion_id=suministro_orden_giro['suministro_id'], cantidad_evaluar=suministro_orden_giro['cantidad'], clasificacion_general=['Indirectos']) == False:
                                        cantidades_disponibles = False
                                if cantidades_disponibles == True:
                                    orden_giro = OrdenGiro()
                                    orden_giro.proyecto = proyecto
                                    orden_giro.proveedor = proveedor
                                    orden_giro.persona = usuario
                                    orden_giro.save()

                                    #Variable para redireccion
                                    items = []
                                    
                                    for suministro_orden_giro in suministros_orden_giro:
                                        suministro_requisicion = list(proyecto.get_suministros_pendientes_comprar(suministro_requisicion_id=suministro_orden_giro['suministro_id'], clasificacion_general=['Indirectos'])).pop()

                                        #Se actualiza el suministro_apu_proyecto
                                        suministro_apu_proyecto = suministro_requisicion.suministro
                                        suministro_apu_proyecto.cantidad_requerida = round(suministro_apu_proyecto.cantidad_requerida - suministro_orden_giro['cantidad'],2)
                                        suministro_apu_proyecto.cantidad_comprada = round(suministro_apu_proyecto.cantidad_comprada + suministro_orden_giro['cantidad'],2)
                                        suministro_apu_proyecto.save()

                                        #Se actualiza el suministro_requisicion
                                        suministro_requisicion.cantidad_comprada = round(suministro_requisicion.cantidad_comprada + suministro_orden_giro['cantidad'],2)
                                        suministro_requisicion.save()

                                        item_orden_giro = ItemOrdenGiro()
                                        item_orden_giro.valor = suministro_orden_giro['cantidad']
                                        item_orden_giro.descripcion = suministro_orden_giro['observaciones']
                                        item_orden_giro.suministro = suministro_requisicion
                                        item_orden_giro.orden_giro = orden_giro
                                        item_orden_giro.save()

                                        #Variable para redireccion
                                        items.append(item_orden_giro)

                                    del request.session['suministros_orden_giro']

                                    # Redirecciona a los detalles del nuevo registro
                                    mensaje = u'Se ha registrado la orden de giro'
                                    pag = Paginador(request, items, 20, 1)
                                    return render_to_response('ordengirodetails.html', {'user': user, 'orden_giro': orden_giro, 'items': pag, 'proyecto': proyecto, 'mensaje': mensaje})
                                else:
                                    mensaje_error = u'Las cantidades no se ecnuentran disponibles'
                            else:
                                mensaje_error = u'No hay items en la nueva orden de giro'
                    else:
                        return proyecto_details(request, proyecto_id)
                else:
                    suministros_orden_giro = []
                    request.session['suministros_orden_giro'] = suministros_orden_giro

                #Visualiza los suministros requeridos con la cantidad a cotizar
                suministros_pendientes = proyecto.get_suministros_pendientes_comprar(clasificacion_general=['Indirectos'])
                suministros_requisiciones = []
                for suministro_pendientes in suministros_pendientes:
                    suministro_requisicion = { 'suministro': suministro_pendientes, 'cantidad_nueva_orden_giro': '', 'observaciones': '' }
                    for suministro_orden_giro in suministros_orden_giro:
                        if suministro_pendientes.id == suministro_orden_giro['suministro_id']:
                            suministro_requisicion['cantidad_nueva_orden_giro'] = suministro_orden_giro['cantidad']
                            suministro_requisicion['observaciones'] = suministro_orden_giro['observaciones']
                    suministros_requisiciones.append(suministro_requisicion)

                pag = Paginador(request, suministros_requisiciones, 20, 1)
                return render_to_response('ordengiroadd.html', {'user': user, 'suministros_requisiciones': pag, 'criterio': criterio, 'proveedor': proveedor, 'proyecto': proyecto, 'mensaje_error': mensaje_error})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Reporte ordenes de giro
def ordenes_giro_proyecto_search(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_ordengiro' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                fecha_inicial = {'valor': '', 'error': ''}
                fecha_final = {'valor': '', 'error': ''}
                criterio = ''
                parametro_fecha_inicial = ''
                parametro_fecha_final = ''
                if request.method == 'POST':
                    fecha_inicial['valor'] = request.POST['fecha_inicial'].strip()
                    fecha_final['valor'] = request.POST['fecha_final'].strip()
                    criterio = request.POST['criterio'].strip()

                    if fecha_inicial['valor'] != '':
                        validaciones_fecha = Validator().append([
                            Field('fecha_inicial', fecha_inicial['valor']).append([
                                IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                            ]),
                        ]).run(True).pop()

                        if validaciones_fecha['passed'] == True:
                            parametro_fecha_inicial = fecha_inicial['valor']
                        else:
                            for error in validaciones_fecha['errors']:
                                fecha_inicial['error'] = error

                    if fecha_final['valor'] != '':
                        validaciones_fecha = Validator().append([
                            Field('fecha_final', fecha_final['valor']).append([
                                IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                            ]),
                        ]).run(True).pop()

                        if validaciones_fecha['passed'] == True:
                            parametro_fecha_final = fecha_final['valor']
                        else:
                            for error in validaciones_fecha['errors']:
                                fecha_final['error'] = error
                ordenes_giro = proyecto.lista_ordenes_giro(criterio=criterio, fecha_inicial=parametro_fecha_inicial, fecha_final=parametro_fecha_final)
                pag = Paginador(request, ordenes_giro, 20, 1)
                return render_to_response('reporteordenesgiro.html', {'user': user, 'ordenes_giro': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Detalles orden_giro
def ordenes_giro_proyecto_details(request, orden_giro_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_ordengiro' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                orden_giro = proyecto.ordengiro_set.get(id=orden_giro_id)
                items = orden_giro.itemordengiro_set.all()
                pag = Paginador(request, items, 20, 1)
                return render_to_response('ordengirodetails.html', {'user': user, 'orden_giro': orden_giro, 'items': pag, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Nueva acta de conformidad
def ordenes_giro_acta_conformidad_add(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_actaconformidad' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id = proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                ordenes_giro = proyecto.lista_ordenes_giro(criterio=criterio, estado=1)
                pag = Paginador(request, ordenes_giro, 20, 1)
                return render_to_response('actaconformidadadd_1ordenesgiro.html', {'user': user, 'ordenes_giro': pag, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def acta_conformidad_add(request, orden_giro_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_actaconformidad' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                orden_giro = proyecto.ordengiro_set.get(id=orden_giro_id)
                error = ''
                if request.method == 'POST':
                    items_acta_conformidad = None
                    try:
                        items_acta_conformidad = request.session['items_acta_conformidad']
                    except :
                        pass
                    if items_acta_conformidad != None:
                        if len(items_acta_conformidad) > 0:
                            cantidades_disponibles = True
                            for item_acta_conformidad in items_acta_conformidad:
                                if orden_giro.itemordengiro_set.get(id=item_acta_conformidad['id']).valor_disponible(item_acta_conformidad['valor']) == False:
                                    cantidades_disponibles = False
                            if cantidades_disponibles == True:
                                acta_conformidad = ActaConformidad()
                                acta_conformidad.orden_giro = orden_giro
                                acta_conformidad.persona = usuario
                                acta_conformidad.save()

                                #Variable para redireccion
                                items = []

                                for item_acta_conformidad in items_acta_conformidad:
                                    item_orden_giro = orden_giro.itemordengiro_set.get(id=item_acta_conformidad['id'])
                                    # Actualiza la cantidad comprada en suministro apu proyecto
                                    suministro_apu_proyecto = item_orden_giro.suministro.suministro
                                    suministro_apu_proyecto.cantidad_almacen = round(suministro_apu_proyecto.cantidad_almacen + item_acta_conformidad['valor'], 2)
                                    suministro_apu_proyecto.save()
                                    # Actualiza la cantidad comprada en el suministro requisicion
                                    suministro_requisicion = item_orden_giro.suministro
                                    suministro_requisicion.cantidad_almacen = round(suministro_requisicion.cantidad_almacen + item_acta_conformidad['valor'], 2)
                                    suministro_requisicion.save()
                                    # Crea el nuevo suministro de acta de conformidad
                                    nuevo_item_acta_conformidad = ItemActaConformidad()
                                    nuevo_item_acta_conformidad.valor = item_acta_conformidad['valor']
                                    nuevo_item_acta_conformidad.item_orden_giro = item_orden_giro
                                    nuevo_item_acta_conformidad.acta_conformidad = acta_conformidad
                                    nuevo_item_acta_conformidad.save()

                                    #Variable para redireccion
                                    items.append(nuevo_item_acta_conformidad)

                                #Actualizar estado de la orden de giro
                                orden_giro.actualizar_estado()

                                del request.session['items_acta_conformidad']

                                # Redirecciona a los detalles del nuevo registro
                                mensaje = u'Se ha realizado el acta de conformidad'
                                pag = Paginador(request, items, 20, 1)
                                return render_to_response('actaconformidaddetails.html', {'user': user, 'acta_conformidad': acta_conformidad, 'items': pag, 'proyecto': proyecto, 'mensaje': mensaje})
                        else:
                            error = u'No se han ingresado items en esta orden de giro'
                    else:
                        return proyecto_details(request, proyecto_id)
                else:
                    request.session['items_acta_conformidad'] = []
                items = orden_giro.itemordengiro_set.all().order_by('suministro__suministro__suministro__nombre')
                items_orden_giro = []
                for item in items:
                    items_orden_giro.append({'item': item, 'valor_nueva_acta': ''})
                pag = Paginador(request, items_orden_giro, 20, 1)
                return render_to_response('actaconformidadadd_2itemsordengiro.html', {'user': user, 'orden_giro': orden_giro, 'proyecto': proyecto, 'items': pag, 'error': error })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Reporte actas de conformidad
def actas_conformidad_proyecto_search(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_actaconformidad' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                fecha_inicial = {'valor': '', 'error': ''}
                fecha_final = {'valor': '', 'error': ''}
                criterio = ''
                parametro_fecha_inicial = ''
                parametro_fecha_final = ''
                if request.method == 'POST':
                    fecha_inicial['valor'] = request.POST['fecha_inicial'].strip()
                    fecha_final['valor'] = request.POST['fecha_final'].strip()
                    criterio = request.POST['criterio'].strip()

                    if fecha_inicial['valor'] != '':
                        validaciones_fecha = Validator().append([
                            Field('fecha_inicial', fecha_inicial['valor']).append([
                                IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                            ]),
                        ]).run(True).pop()

                        if validaciones_fecha['passed'] == True:
                            parametro_fecha_inicial = fecha_inicial['valor']
                        else:
                            for error in validaciones_fecha['errors']:
                                fecha_inicial['error'] = error

                    if fecha_final['valor'] != '':
                        validaciones_fecha = Validator().append([
                            Field('fecha_final', fecha_final['valor']).append([
                                IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                            ]),
                        ]).run(True).pop()

                        if validaciones_fecha['passed'] == True:
                            parametro_fecha_final = fecha_final['valor']
                        else:
                            for error in validaciones_fecha['errors']:
                                fecha_final['error'] = error
                actas_conformidad = proyecto.lista_actas_conformidad(criterio, fecha_inicial=parametro_fecha_inicial, fecha_final=parametro_fecha_final)
                pag = Paginador(request, actas_conformidad, 20, 1)
                return render_to_response('reporteactasconformidad.html', {'user': user, 'actas_conformidad': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Detalles acta_conformidad
def actas_conformidad_proyecto_details(request, acta_conformidad_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_actaconformidad' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                acta_conformidad = ActaConformidad.objects.get(id=acta_conformidad_id, orden_giro__proyecto=proyecto)
                items = acta_conformidad.itemactaconformidad_set.all()
                pag = Paginador(request, items, 20, 1)
                return render_to_response('actaconformidaddetails.html', {'user': user, 'acta_conformidad': acta_conformidad, 'items': pag, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Nueva Factura
def proveedores_ordenes_compra_factura_add(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_facturaordencompra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                #Elimina las variables temporales
                try:
                    del request.session['items_factura']
                except :
                    pass
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                proveedores = proyecto.lista_proveedores_ordenes_compra_en_ejecucion_por_facturar(criterio=criterio)
                pag = Paginador(request, proveedores, 20, 1)
                return render_to_response('facturaordencompraadd_1proveedores.html', {'user': user, 'proveedores': pag, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def ordenes_compra_proveedor_factura_add(request, proveedor_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_facturaordencompra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                proveedor = Proveedor.objects.get(id=proveedor_id)
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                ordenes_compra = proyecto.lista_ordenes_compra_en_ejecucion_por_facturar(criterio=criterio, proveedor=proveedor)
                pag = Paginador(request, ordenes_compra, 20, 1)
                return render_to_response('facturaordencompraadd_2ordenescompraproveedor.html', {'user': user, 'ordenes_compra': pag, 'proveedor': proveedor, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def informes_recepcion_factura_orden_compra_add(request, orden_compra_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_facturaordencompra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()

                #Inicializacion de variables
                items_factura = None
                try:
                    items_factura = request.session['items_factura']
                except :
                    pass
                if items_factura == None:
                    items_factura = []

                #Elimina las variables temporales
                try:
                    del request.session['items_factura_agregar']
                except :
                    pass

                informes_recepcion = orden_compra.lista_informes_recepcion_por_facturar(criterio)
                request.session['items_factura'] = items_factura
                pag = Paginador(request, informes_recepcion, 20, 1)
                return render_to_response('facturaordencompraadd_3informesrecepcionordencompra.html', {'user': user, 'informes_recepcion': pag, 'orden_compra': orden_compra, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def detalles_factura_orden_compra_add(request, proveedor_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_facturaordencompra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                items_factura = None
                try:
                    items_factura = request.session['items_factura']
                except :
                    pass
                if items_factura != None:
                    proveedor = Proveedor.objects.get(id=proveedor_id)
                    error = ''
                    error_numero_factura = ''
                    numero_factura = ''
                    if request.method == 'POST':
                        if len(items_factura) > 0:
                            cantidades_disponibles = True
                            for item_factura in items_factura:
                                informe_recepcion = InformeRecepcion.objects.get(id=item_factura['informe_recepcion_id'])
                                suministro = informe_recepcion.get_suministro(item_factura['id'])
                                if float(item_factura['cantidad']) > round(suministro.cantidad - suministro.cantidad_facturada, 2):
                                    cantidades_disponibles = False
                            if cantidades_disponibles == True:
                                numero_factura = request.POST['numero_factura'].strip()
                                error_numero_factura = validar_cadena(numero_factura)
                                if error_numero_factura == '':
                                    error_numero_factura = validar_cadena_caracteres_especiales(numero_factura)
                                if error_numero_factura == '':
                                    error_numero_factura = validar_long_max_cadena(numero_factura, 15)
                                if error_numero_factura == '':
                                    factura = FacturaOrdencompra()
                                    factura.numero_factura = numero_factura
                                    factura.proveedor = proveedor
                                    factura.proyecto = proyecto
                                    factura.persona = usuario
                                    factura.save()

                                    for item_factura in items_factura:
                                        informe_recepcion = InformeRecepcion.objects.get(id=item_factura['informe_recepcion_id'])
                                        suministros = informe_recepcion.suministroinformerecepcion_set.filter(suministro__suministro__suministro__suministro__id=item_factura['id'], cantidad_facturada__lt=F('cantidad')).order_by('suministro__suministro__requisicion__fecha_arribo')
                                        cantidad_facturada = 0.0
                                        cantidad = item_factura['cantidad']

                                        #Se crea el item factura orden compra
                                        suministro_base = Suministro.objects.get(id=item_factura['id'])
                                        item_factura_orden_compra, transaccion = ItemFacturaOrdenCompra.objects.get_or_create(suministro=suministro_base, factura=factura)
                                        
                                        for suministro in suministros:
                                            cantidad_facturada_suministro_informe_recepcion = 0.0
                                            if cantidad_facturada < cantidad:
                                                if (round(cantidad - cantidad_facturada, 2)) <= (round(suministro.cantidad - suministro.cantidad_facturada, 2)):
                                                    cantidad_facturada_suministro_informe_recepcion = round(cantidad - cantidad_facturada, 2)
                                                elif (round(cantidad - cantidad_facturada, 2)) > (round(suministro.cantidad - suministro.cantidad_facturada, 2)):
                                                    cantidad_facturada_suministro_informe_recepcion = round(suministro.cantidad - suministro.cantidad_facturada, 2)
                                                cantidad_facturada = round(cantidad_facturada + cantidad_facturada_suministro_informe_recepcion, 2)
                                                if cantidad_facturada_suministro_informe_recepcion > 0:
                                                    # Actualiza la cantidad facturada en suministro en la orden de compra
                                                    suministro_orden_compra = suministro.suministro
                                                    suministro_orden_compra.cantidad_facturada = round(suministro_orden_compra.cantidad_facturada + cantidad_facturada_suministro_informe_recepcion, 2)
                                                    suministro_orden_compra.save()
                                                    # Actualiza la cantidad facturada en suministro informe de recepción
                                                    suministro.cantidad_facturada = round(suministro.cantidad_facturada + cantidad_facturada_suministro_informe_recepcion, 2)
                                                    suministro.save()
                                                    # Crea el nuevo suministro de la factura orden de compra
                                                    suministro_factura_orden_compra = SuministroFacturaOrdenCompra()
                                                    suministro_factura_orden_compra.cantidad = cantidad_facturada_suministro_informe_recepcion
                                                    suministro_factura_orden_compra.suministro_informe_recepcion = suministro
                                                    suministro_factura_orden_compra.item_factura_orden_compra = item_factura_orden_compra
                                                    suministro_factura_orden_compra.save()
                                    del request.session['items_factura']

                                    # Redirecciona a los detalles del nuevo registro
                                    mensaje = u'Se ha realizado la nueva factura'

                                    items = factura.itemfacturaordencompra_set.all()

                                    #Calculo de valores por discriminacion de orden de compra
                                    valor_discriminado_ordenes_compra = []

                                    #Calculo de valores por discriminación de clasificación (capitulos)
                                    valor_discriminado_capitulos = []
                                    valor_factura_sin_iva = 0
                                    valor_iva_factura = 0
                                    valor_total_factura = 0
                                    for item_factura in items:
                                        suministros_item_factura = item_factura.suministrofacturaordencompra_set.all().order_by('suministro_informe_recepcion__informe_recepcion__orden_compra__consecutivo')
                                        for suministro_item_factura in suministros_item_factura:
                                            existe_capitulo = False
                                            for item in valor_discriminado_capitulos:
                                                capitulo = item['capitulo']
                                                if item['capitulo'].tipo_capitulo == 2:
                                                   capitulo = item['capitulo'].capitulo_asociado
                                                if (suministro_item_factura.suministro_informe_recepcion.suministro.suministro.suministro.apu_proyecto.capitulo.id == capitulo.id) or (suministro_item_factura.suministro_informe_recepcion.suministro.suministro.suministro.apu_proyecto.capitulo.tipo_capitulo == 2 and suministro_item_factura.suministro_informe_recepcion.suministro.suministro.suministro.apu_proyecto.capitulo.capitulo_asociado.id == capitulo.id):
                                                    valor_sin_iva = round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2)
                                                    valor_iva = round(round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2) * suministro_item_factura.item_factura_orden_compra.porcentaje_iva(), 2)
                                                    valor_con_iva = round(valor_sin_iva + valor_iva, 2)
                                                    item['valor_sin_iva'] = round(item['valor_sin_iva'] + valor_sin_iva, 2)
                                                    item['valor_iva'] = round(item['valor_iva'] + valor_iva, 2)
                                                    item['valor_con_iva'] = round(item['valor_con_iva'] + valor_con_iva, 2)
                                                    valor_factura_sin_iva = round(valor_factura_sin_iva + valor_sin_iva, 2)
                                                    valor_iva_factura = round(valor_iva_factura + valor_iva, 2)
                                                    valor_total_factura = round(valor_total_factura + valor_con_iva, 2)
                                                    existe_capitulo = True
                                            if existe_capitulo == False:
                                                valor_sin_iva = round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2)
                                                valor_iva = round(round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2) * suministro_item_factura.item_factura_orden_compra.porcentaje_iva(), 2)
                                                valor_con_iva = round(valor_sin_iva + valor_iva, 2)
                                                valor_discriminado_capitulos.append({'capitulo': suministro_item_factura.suministro_informe_recepcion.suministro.suministro.suministro.apu_proyecto.capitulo, 'valor_sin_iva': valor_sin_iva, 'valor_iva': valor_iva, 'valor_con_iva': valor_con_iva})
                                                valor_factura_sin_iva = round(valor_factura_sin_iva + valor_sin_iva, 2)
                                                valor_iva_factura = round(valor_iva_factura + valor_iva, 2)
                                                valor_total_factura = round(valor_total_factura + valor_con_iva, 2)

                                            #Calculo de valores por discriminación de orden de compra
                                            existe_orden_compra = False
                                            for item in valor_discriminado_ordenes_compra:
                                                if item['orden_compra'].id == suministro_item_factura.suministro_informe_recepcion.informe_recepcion.orden_compra.id:
                                                    existe_orden_compra = True
                                                    existe_suministro_orden_compra = False
                                                    for suministro in item['suministros']:
                                                        if suministro_item_factura.item_factura_orden_compra.suministro.id == suministro['suministro'].id:
                                                            existe_suministro_orden_compra = True
                                                            valor_sin_iva = round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2)
                                                            valor_iva = round(round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2) * suministro_item_factura.item_factura_orden_compra.porcentaje_iva(), 2)
                                                            valor_con_iva = round(valor_sin_iva + valor_iva, 2)

                                                            suministro['cantidad'] = round(suministro['cantidad'] + suministro_item_factura.cantidad, 2)
                                                            suministro['valor_sin_iva'] = round(suministro['valor_sin_iva'] + valor_sin_iva, 2)
                                                            suministro['valor_iva'] = round(suministro['valor_iva'] + valor_iva, 2)
                                                            suministro['valor_con_iva'] = round(suministro['valor_con_iva'] + valor_con_iva, 2)

                                                            item['valor_sin_iva'] = round(item['valor_sin_iva'] + valor_sin_iva, 2)
                                                            item['valor_iva'] = round(item['valor_iva'] + valor_iva, 2)
                                                            item['valor_con_iva'] = round(item['valor_con_iva'] + valor_con_iva, 2)

                                                    if existe_suministro_orden_compra == False:
                                                        valor_sin_iva = round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2)
                                                        valor_iva = round(round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2) * suministro_item_factura.item_factura_orden_compra.porcentaje_iva(), 2)
                                                        valor_con_iva = round(valor_sin_iva + valor_iva, 2)
                                                        item['suministros'].append({'suministro': suministro_item_factura.item_factura_orden_compra.suministro, 'cantidad': suministro_item_factura.cantidad, 'valor_sin_iva': valor_sin_iva, 'valor_iva': valor_iva, 'valor_con_iva': valor_con_iva})

                                                        item['valor_sin_iva'] = round(item['valor_sin_iva'] + valor_sin_iva, 2)
                                                        item['valor_iva'] = round(item['valor_iva'] + valor_iva, 2)
                                                        item['valor_con_iva'] = round(item['valor_con_iva'] + valor_con_iva, 2)
                                            if existe_orden_compra == False:
                                                valor_sin_iva = round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2)
                                                valor_iva = round(round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2) * suministro_item_factura.item_factura_orden_compra.porcentaje_iva(), 2)
                                                valor_con_iva = round(valor_sin_iva + valor_iva, 2)
                                                valor_discriminado_ordenes_compra.append({'orden_compra': suministro_item_factura.suministro_informe_recepcion.informe_recepcion.orden_compra, 'suministros': [{'suministro': suministro_item_factura.item_factura_orden_compra.suministro, 'cantidad': suministro_item_factura.cantidad, 'valor_sin_iva': valor_sin_iva, 'valor_iva': valor_iva, 'valor_con_iva': valor_con_iva}], 'valor_sin_iva': valor_sin_iva, 'valor_iva': valor_iva, 'valor_con_iva': valor_con_iva})

                                    pag = Paginador(request, items, 20, 1)
                                    return render_to_response('detallesfacturaordencompra.html', {'user': user, 'factura_orden_compra': factura, 'items_factura': pag, 'valor_discriminado_capitulos': valor_discriminado_capitulos, 'valor_discriminado_ordenes_compra': valor_discriminado_ordenes_compra, 'valor_factura_sin_iva': valor_factura_sin_iva, 'valor_iva_factura': valor_iva_factura, 'valor_total_factura': valor_total_factura, 'proyecto': proyecto, 'mensaje': mensaje})
                            else:
                                mensaje = u'Las cantidades no se encuentran disponibles'
                                personas = proyecto.personaproyecto_set.filter(estado=True)
                                return render_to_response('proyectodetails.html', {'user': user, 'proyecto': proyecto, 'personas': personas, 'mensaje': mensaje})
                        else:
                            error = u'No se han ingresado items en esta factura de orden de compra'
                else:
                    return proyecto_details(request, proyecto_id)

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
                pag = Paginador(request, lista_items_factura, 20, 1)
                return render_to_response('facturaordencompraadd_4detalles.html', {'user': user, 'proveedor': proveedor, 'items_factura': pag, 'numero_factura': numero_factura, 'discriminacion_valores': discriminacion_valores, 'proyecto': proyecto, 'error': error, 'error_numero_factura': error_numero_factura})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def busqueda_factura_orden_compra_proyecto(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_facturaordencompra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                fecha_inicial = {'valor': '', 'error': ''}
                fecha_final = {'valor': '', 'error': ''}
                criterio = ''
                parametro_fecha_inicial = ''
                parametro_fecha_final = ''
                if request.method == 'POST':
                    fecha_inicial['valor'] = request.POST['fecha_inicial'].strip()
                    fecha_final['valor'] = request.POST['fecha_final'].strip()
                    criterio = request.POST['criterio'].strip()

                    if fecha_inicial['valor'] != '':
                        validaciones_fecha = Validator().append([
                            Field('fecha_inicial', fecha_inicial['valor']).append([
                                IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                            ]),
                        ]).run(True).pop()

                        if validaciones_fecha['passed'] == True:
                            parametro_fecha_inicial = fecha_inicial['valor']
                        else:
                            for error in validaciones_fecha['errors']:
                                fecha_inicial['error'] = error

                    if fecha_final['valor'] != '':
                        validaciones_fecha = Validator().append([
                            Field('fecha_final', fecha_final['valor']).append([
                                IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                            ]),
                        ]).run(True).pop()

                        if validaciones_fecha['passed'] == True:
                            parametro_fecha_final = fecha_final['valor']
                        else:
                            for error in validaciones_fecha['errors']:
                                fecha_final['error'] = error
                facturas = proyecto.lista_facturas_ordenes_compra(criterio, fecha_inicial=parametro_fecha_inicial, fecha_final=parametro_fecha_final)
                pag = Paginador(request, facturas, 20, 1)
                return render_to_response('reportefacturasordenescompra.html', {'user': user, 'facturas_ordenes_compra': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def factura_orden_compra_detalles(request, factura_orden_compra_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        existen_subcapitulos = False
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_facturaordencompra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                factura = proyecto.facturaordencompra_set.get(id=factura_orden_compra_id)
                items_factura = factura.itemfacturaordencompra_set.all()

                #Calculo de valores por discriminacion de orden de compra
                valor_discriminado_ordenes_compra = []

                 #Calculo de valores por discriminación de clasificación (capitulos)
                valor_discriminado_capitulos = []
                valor_factura_sin_iva = 0
                valor_iva_factura = 0
                valor_total_factura = 0

                for item_factura in items_factura:
                    suministros_item_factura = item_factura.suministrofacturaordencompra_set.all().order_by('suministro_informe_recepcion__informe_recepcion__orden_compra__consecutivo')
                    for suministro_item_factura in suministros_item_factura:
                        existe_capitulo = False
                        for item in valor_discriminado_capitulos:
                            capitulo = item['capitulo']
                            if item['capitulo'].tipo_capitulo == 2:
                                capitulo = item['capitulo'].capitulo_asociado
                                existen_subcapitulos = True
                                
                            if (suministro_item_factura.suministro_informe_recepcion.suministro.suministro.suministro.apu_proyecto.capitulo.id == capitulo.id) or (suministro_item_factura.suministro_informe_recepcion.suministro.suministro.suministro.apu_proyecto.capitulo.tipo_capitulo == 2 and suministro_item_factura.suministro_informe_recepcion.suministro.suministro.suministro.apu_proyecto.capitulo.capitulo_asociado.id == capitulo.id):
                                valor_sin_iva = round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2)
                                valor_iva = round(round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2) * suministro_item_factura.item_factura_orden_compra.porcentaje_iva(), 2)
                                valor_con_iva = round(valor_sin_iva + valor_iva, 2)
                                item['valor_sin_iva'] = round(item['valor_sin_iva'] + valor_sin_iva, 2)
                                item['valor_iva'] = round(item['valor_iva'] + valor_iva, 2)
                                item['valor_con_iva'] = round(item['valor_con_iva'] + valor_con_iva, 2)
                                valor_factura_sin_iva = round(valor_factura_sin_iva + valor_sin_iva, 2)
                                valor_iva_factura = round(valor_iva_factura + valor_iva, 2)
                                valor_total_factura = round(valor_total_factura + valor_con_iva, 2)
                                existe_capitulo = True
                        if existe_capitulo == False:
                            valor_sin_iva = round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2)
                            valor_iva = round(round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2) * suministro_item_factura.item_factura_orden_compra.porcentaje_iva(), 2)
                            valor_con_iva = round(valor_sin_iva + valor_iva, 2)
                            valor_discriminado_capitulos.append({'capitulo': suministro_item_factura.suministro_informe_recepcion.suministro.suministro.suministro.apu_proyecto.capitulo, 'valor_sin_iva': valor_sin_iva, 'valor_iva': valor_iva, 'valor_con_iva': valor_con_iva})
                            valor_factura_sin_iva = round(valor_factura_sin_iva + valor_sin_iva, 2)
                            valor_iva_factura = round(valor_iva_factura + valor_iva, 2)
                            valor_total_factura = round(valor_total_factura + valor_con_iva, 2)


                #Calculo de valores por discriminación de clasificación (subcapitulos)
                valor_discriminado_subcapitulos = []
                valor_factura_sin_iva = 0
                valor_iva_factura = 0
                valor_total_factura = 0
                capitulo_asociado = ''

                for item_factura in items_factura:
                    suministros_item_factura = item_factura.suministrofacturaordencompra_set.all().order_by('suministro_informe_recepcion__informe_recepcion__orden_compra__consecutivo')
                    for suministro_item_factura in suministros_item_factura:
                        existe_capitulo = False
                        for item in valor_discriminado_subcapitulos:
                            capitulo = item['capitulo']
                            if item['capitulo'].tipo_capitulo == 2:
                                capitulo = item['capitulo']
                                capitulo_asociado = item['capitulo'].capitulo_asociado
                                existen_subcapitulos = True
                            if (suministro_item_factura.suministro_informe_recepcion.suministro.suministro.suministro.apu_proyecto.capitulo.id == capitulo.id) or (suministro_item_factura.suministro_informe_recepcion.suministro.suministro.suministro.apu_proyecto.capitulo.tipo_capitulo == 2 and suministro_item_factura.suministro_informe_recepcion.suministro.suministro.suministro.apu_proyecto.capitulo.capitulo_asociado.id == capitulo.id):
                                valor_sin_iva = round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2)
                                valor_iva = round(round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2) * suministro_item_factura.item_factura_orden_compra.porcentaje_iva(), 2)
                                valor_con_iva = round(valor_sin_iva + valor_iva, 2)
                                item['valor_sin_iva'] = round(item['valor_sin_iva'] + valor_sin_iva, 2)
                                item['valor_iva'] = round(item['valor_iva'] + valor_iva, 2)
                                item['valor_con_iva'] = round(item['valor_con_iva'] + valor_con_iva, 2)
                                valor_factura_sin_iva = round(valor_factura_sin_iva + valor_sin_iva, 2)
                                valor_iva_factura = round(valor_iva_factura + valor_iva, 2)
                                valor_total_factura = round(valor_total_factura + valor_con_iva, 2)
                                existe_capitulo = True
                        if existe_capitulo == False:
                            valor_sin_iva = round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2)
                            valor_iva = round(round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2) * suministro_item_factura.item_factura_orden_compra.porcentaje_iva(), 2)
                            valor_con_iva = round(valor_sin_iva + valor_iva, 2)
                            valor_discriminado_subcapitulos.append({'capitulo': suministro_item_factura.suministro_informe_recepcion.suministro.suministro.suministro.apu_proyecto.capitulo, 'capitulo_asociado': capitulo_asociado, 'valor_sin_iva': valor_sin_iva, 'valor_iva': valor_iva, 'valor_con_iva': valor_con_iva})
                            valor_factura_sin_iva = round(valor_factura_sin_iva + valor_sin_iva, 2)
                            valor_iva_factura = round(valor_iva_factura + valor_iva, 2)
                            valor_total_factura = round(valor_total_factura + valor_con_iva, 2)

                        #Calculo de valores por discriminación de orden de compra
                        existe_orden_compra = False
                        for item in valor_discriminado_ordenes_compra:
                            if item['orden_compra'].id == suministro_item_factura.suministro_informe_recepcion.informe_recepcion.orden_compra.id:
                                existe_orden_compra = True
                                existe_suministro_orden_compra = False
                                for suministro in item['suministros']:
                                    if suministro_item_factura.item_factura_orden_compra.suministro.id == suministro['suministro'].id:
                                        existe_suministro_orden_compra = True
                                        valor_sin_iva = round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2)
                                        valor_iva = round(round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2) * suministro_item_factura.item_factura_orden_compra.porcentaje_iva(), 2)
                                        valor_con_iva = round(valor_sin_iva + valor_iva, 2)

                                        suministro['cantidad'] = round(suministro['cantidad'] + suministro_item_factura.cantidad, 2)
                                        suministro['valor_sin_iva'] = round(suministro['valor_sin_iva'] + valor_sin_iva, 2)
                                        suministro['valor_iva'] = round(suministro['valor_iva'] + valor_iva, 2)
                                        suministro['valor_con_iva'] = round(suministro['valor_con_iva'] + valor_con_iva, 2)

                                        item['valor_sin_iva'] = round(item['valor_sin_iva'] + valor_sin_iva, 2)
                                        item['valor_iva'] = round(item['valor_iva'] + valor_iva, 2)
                                        item['valor_con_iva'] = round(item['valor_con_iva'] + valor_con_iva, 2)

                                if existe_suministro_orden_compra == False:
                                    valor_sin_iva = round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2)
                                    valor_iva = round(round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2) * suministro_item_factura.item_factura_orden_compra.porcentaje_iva(), 2)
                                    valor_con_iva = round(valor_sin_iva + valor_iva, 2)
                                    item['suministros'].append({'suministro': suministro_item_factura.item_factura_orden_compra.suministro, 'cantidad': suministro_item_factura.cantidad, 'valor_sin_iva': valor_sin_iva, 'valor_iva': valor_iva, 'valor_con_iva': valor_con_iva})
                                    
                                    item['valor_sin_iva'] = round(item['valor_sin_iva'] + valor_sin_iva, 2)
                                    item['valor_iva'] = round(item['valor_iva'] + valor_iva, 2)
                                    item['valor_con_iva'] = round(item['valor_con_iva'] + valor_con_iva, 2)
                        if existe_orden_compra == False:
                            valor_sin_iva = round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2)
                            valor_iva = round(round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2) * suministro_item_factura.item_factura_orden_compra.porcentaje_iva(), 2)
                            valor_con_iva = round(valor_sin_iva + valor_iva, 2)
                            valor_discriminado_ordenes_compra.append({'orden_compra': suministro_item_factura.suministro_informe_recepcion.informe_recepcion.orden_compra, 'suministros': [{'suministro': suministro_item_factura.item_factura_orden_compra.suministro, 'cantidad': suministro_item_factura.cantidad, 'valor_sin_iva': valor_sin_iva, 'valor_iva': valor_iva, 'valor_con_iva': valor_con_iva}], 'valor_sin_iva': valor_sin_iva, 'valor_iva': valor_iva, 'valor_con_iva': valor_con_iva})

                pag = Paginador(request, items_factura, 20, 1)
                return render_to_response('detallesfacturaordencompra.html', {'user': user, 'factura_orden_compra': factura, 'items_factura': pag, 'valor_discriminado_capitulos': valor_discriminado_capitulos, 'valor_discriminado_subcapitulos': valor_discriminado_subcapitulos, 'valor_discriminado_ordenes_compra': valor_discriminado_ordenes_compra, 'valor_factura_sin_iva': valor_factura_sin_iva, 'valor_iva_factura': valor_iva_factura, 'valor_total_factura': valor_total_factura, 'proyecto': proyecto, 'existen_subcapitulos': existen_subcapitulos})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def reporte_presupuesto_proyecto_discriminado_apus(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_apuproyecto' or 'inverboy.view_actareciboobra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():

                presupuesto_proyecto = Proyecto()
                presupuesto_proyecto.capitulos = []
                valor_presupuesto_proyecto = proyecto.valor_total_presupuesto_proyecto()

                for capitulo in proyecto.lista_capitulos_activos():
                    valor_capitulo = 0
                    capitulo.apus = []
                    for apu_proyecto in capitulo.lista_apus_proyecto_activos():
                        apu_proyecto.porcentaje_valor_total_proyecto = round((apu_proyecto.valor_total * 100) / decimal.Decimal(valor_presupuesto_proyecto), 4)
                        capitulo.apus.append(apu_proyecto)
                        valor_capitulo = round(decimal.Decimal(valor_capitulo) + apu_proyecto.valor_total, 2)

                    capitulo.subcapitulos = []

                    for subcapitulo in capitulo.lista_subcapitulos_activos():
                        subcapitulo.apus = []
                        valor_subcapitulo = 0
                        for apu_proyecto in subcapitulo.lista_apus_proyecto_activos():
                            apu_proyecto.porcentaje_valor_total_proyecto = round((apu_proyecto.valor_total * 100) / decimal.Decimal(valor_presupuesto_proyecto), 4)
                            subcapitulo.apus.append(apu_proyecto)
                            valor_subcapitulo = round(decimal.Decimal(valor_subcapitulo) + apu_proyecto.valor_total, 2)
                        valor_capitulo = round(valor_capitulo + valor_subcapitulo, 2)
                        subcapitulo.porcentaje_valor_total_proyecto = round((valor_subcapitulo * 100) / valor_presupuesto_proyecto, 4)
                        subcapitulo.valor_capitulo = valor_subcapitulo
                        capitulo.subcapitulos.append(subcapitulo)
                    capitulo.valor_capitulo = valor_capitulo
                    capitulo.porcentaje_valor_total_proyecto = round((valor_capitulo * 100) / valor_presupuesto_proyecto, 4)
                    presupuesto_proyecto.capitulos.append(capitulo)
                presupuesto_proyecto.valor_presupuesto_proyecto = valor_presupuesto_proyecto

                return render_to_response('reportepresupuestoproyectodiscriminadoapus2.html', {'user': user, 'presupuesto_proyecto': presupuesto_proyecto, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def reporte_pago_actas_recibo_obra(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_actareciboobra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                fecha_inicial = ''
                fecha_final = ''
                tipo_busqueda = 1
                criterio = ''
                error_fecha_inicial = ''
                error_fecha_final = ''
                total_pagar_actas = 0
                actas_recibo_obra = []
                if request.method == 'POST':
                    fecha_inicial = request.POST['fecha_inicial'].strip()
                    fecha_final = request.POST['fecha_final'].strip()
                    tipo_busqueda = int(request.POST['tipo_busqueda'])
                    criterio = request.POST['criterio'].strip()
                    error_fecha_inicial = validar_fecha(fecha_inicial)
                    error_fecha_final = validar_fecha(fecha_final)
                    if error_fecha_inicial == '' and error_fecha_final == '':
                        formato_fecha_inicial = fecha_inicial + ' 00:00:00'
                        formato_fecha_final = fecha_final + ' 23:59:59'
                        actas_recibo_obra = ActaReciboObra.objects.filter(orden_servicio__proyecto=proyecto, fecha_acta__gt=formato_fecha_inicial, fecha_acta__lt=formato_fecha_final).order_by('consecutivo')
                        if tipo_busqueda == 1:
                            actas_recibo_obra = actas_recibo_obra.filter(Q(orden_servicio__proveedor__razon_social__icontains=criterio) | Q(orden_servicio__proveedor__nombre_comercial__icontains=criterio))
                        elif tipo_busqueda == 2:
                            actas_recibo_obra = actas_recibo_obra.filter(Q(orden_servicio__tercero__razon_social__icontains=criterio) | Q(orden_servicio__tercero__nombre_comercial__icontains=criterio))
                        elif tipo_busqueda == 3:
                            actas_recibo_obra = actas_recibo_obra.filter(Q(orden_servicio__proveedor__razon_social__icontains=criterio) | Q(orden_servicio__proveedor__nombre_comercial__icontains=criterio) | Q(orden_servicio__tercero__razon_social__icontains=criterio) | Q(orden_servicio__tercero__nombre_comercial__icontains=criterio))

                for acta_recibo_obra in actas_recibo_obra:
                    items_acta_recibo_obra = acta_recibo_obra.itemactareciboobra_set.all()
                    total_pagar_acta_actual = 0
                    for item_acta_recibo_obra in items_acta_recibo_obra:
                        corte_diario_obra = item_acta_recibo_obra.corte_diario_obra
                        suministros_corte_diario_obra = corte_diario_obra.suministrocortediarioobra_set.all()
                        for suministro_corte_diario_obra in suministros_corte_diario_obra:
                            total_pagar_actas = round(total_pagar_actas + (suministro_corte_diario_obra.cantidad * suministro_corte_diario_obra.suministro.suministro_orden_servicio_item.precio), 2)
                            total_pagar_acta_actual = round(total_pagar_acta_actual + (suministro_corte_diario_obra.cantidad * suministro_corte_diario_obra.suministro.suministro_orden_servicio_item.precio), 2)
                    acta_recibo_obra.total_pagar = total_pagar_acta_actual
                pag = Paginador(request, actas_recibo_obra, 20, 1)
                return render_to_response('reportepagoactasreciboobra.html', {'user': user, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'tipo_busqueda': tipo_busqueda, 'criterio': criterio, 'actas_recibo_obra': pag, 'total_pagar_actas': total_pagar_actas, 'error_fecha_inicial': error_fecha_inicial, 'error_fecha_final': error_fecha_final, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def reporte_valor_suministros_orden_compra(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_apuproyecto' or 'inverboy.view_actareciboobra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                ids_suministros = SuministroApuProyecto.objects.filter(apu_proyecto__proyecto=proyecto, suministro__clasificacion_general='Material', suministro__nombre__icontains=criterio).order_by('suministro__nombre').values('suministro__id')

                ids_suministros.query.group_by = ['inverboy_suministroapuproyecto.suministro_id']

                suministros = []
                for id_suministro in ids_suministros:
                    suministro_base = Suministro.objects.get(id=id_suministro['suministro__id'])
                    if len(SuministroOrdenCompraItem.objects.filter(suministro__id=id_suministro['suministro__id'])) > 0:
                        suministro = {'suministro': suministro_base, 'valor_minimo': '-', 'fecha_valor_minimo': '-', 'valor_maximo': '-', 'fecha_valor_maximo': '-', 'valor_actual': 0, 'fecha_valor_actual': '-'}
                        suministros_orden_compra_item = SuministroOrdenCompraItem.objects.filter(suministro__id=id_suministro['suministro__id']).order_by('-orden_compra__fecha_creacion', '-id')
                        ultimo_item_comprado = suministros_orden_compra_item[0]
                        suministro['valor_actual'] = round(ultimo_item_comprado.precio + (ultimo_item_comprado.precio * ultimo_item_comprado.iva_suministro), 2)
                        suministro['fecha_valor_actual'] = ultimo_item_comprado.orden_compra.fecha_creacion
                        for suministro_orden_compra_item in suministros_orden_compra_item:
                            if suministro['valor_minimo'] == '-':
                                if round(suministro_orden_compra_item.precio + (suministro_orden_compra_item.precio * suministro_orden_compra_item.iva_suministro), 2) < suministro['valor_actual']:
                                    suministro['valor_minimo'] = round(suministro_orden_compra_item.precio + (suministro_orden_compra_item.precio * suministro_orden_compra_item.iva_suministro), 2)
                                    suministro['fecha_valor_minimo'] = suministro_orden_compra_item.orden_compra.fecha_creacion
                            elif round(suministro_orden_compra_item.precio + (suministro_orden_compra_item.precio * suministro_orden_compra_item.iva_suministro), 2) < suministro['valor_minimo']:
                                suministro['valor_minimo'] = round(suministro_orden_compra_item.precio + (suministro_orden_compra_item.precio * suministro_orden_compra_item.iva_suministro), 2)
                                suministro['fecha_valor_minimo'] = suministro_orden_compra_item.orden_compra.fecha_creacion
                            if suministro['valor_maximo'] == '-':
                                if round(suministro_orden_compra_item.precio + (suministro_orden_compra_item.precio * suministro_orden_compra_item.iva_suministro), 2) > suministro['valor_actual']:
                                    suministro['valor_maximo'] = round(suministro_orden_compra_item.precio + (suministro_orden_compra_item.precio * suministro_orden_compra_item.iva_suministro), 2)
                                    suministro['fecha_valor_maximo'] = suministro_orden_compra_item.orden_compra.fecha_creacion
                            elif round(suministro_orden_compra_item.precio + (suministro_orden_compra_item.precio * suministro_orden_compra_item.iva_suministro), 2) > suministro['valor_maximo']:
                                suministro['valor_maximo'] = round(suministro_orden_compra_item.precio + (suministro_orden_compra_item.precio * suministro_orden_compra_item.iva_suministro), 2)
                                suministro['fecha_valor_maximo'] = suministro_orden_compra_item.orden_compra.fecha_creacion

                        suministros.append(suministro)

                return render_to_response('reportevalorsuministrosordencompra.html', {'user': user, 'suministros': suministros, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def reporte_analisis_cantidades_suministros_proyecto(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_apuproyecto' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                lista_suministros_apus_proyecto = []
                suministros_apus_proyecto = SuministroApuProyecto.objects.filter(Q(apu_proyecto__proyecto=proyecto), Q(suministro__nombre__icontains=criterio) | Q(suministro__sinonimos__icontains=criterio)).order_by('suministro__nombre')
                ids_suministros = []
                for suministro_apu in suministros_apus_proyecto:
                    if suministro_apu.suministro_id not in ids_suministros:
                        suministro_apu.cantidad_suministro = round(suministro_apu.cantidad_suministro * float(suministro_apu.apu_proyecto.cantidad_total), 2)
                        lista_suministros_apus_proyecto.append(suministro_apu)
                        ids_suministros.append(suministro_apu.suministro_id)
                    else:
                        for suministro_apu_proyecto in lista_suministros_apus_proyecto:
                            if suministro_apu.suministro_id == suministro_apu_proyecto.suministro_id:
                                suministro_apu_proyecto.cantidad_suministro = round(suministro_apu_proyecto.cantidad_suministro + round(suministro_apu.cantidad_suministro * float(suministro_apu.apu_proyecto.cantidad_total), 2))
                                suministro_apu_proyecto.cantidad_total_requerida = round(suministro_apu_proyecto.cantidad_total_requerida + suministro_apu.cantidad_total_requerida, 2)
                                suministro_apu_proyecto.cantidad_comprada = round(suministro_apu_proyecto.cantidad_comprada + suministro_apu.cantidad_comprada, 2)
                                suministro_apu_proyecto.cantidad_almacen = round(suministro_apu_proyecto.cantidad_almacen + suministro_apu.cantidad_almacen, 2)
                for suministro_apu_proyecto in lista_suministros_apus_proyecto:
                    cantidad_facturada = 0
                    valor_facturado = 0
                    # Valores ordenes de compra
                    items_ordenes_compra = SuministroOrdenCompraItem.objects.filter(orden_compra__proyecto=proyecto, suministro=suministro_apu_proyecto.suministro)
                    if items_ordenes_compra:
                        for item_orden_compra in items_ordenes_compra:
                            cantidad_facturada_item, valor_facturado_item = item_orden_compra.cantidad_facturada_valor_facturado()
                            cantidad_facturada = round(cantidad_facturada + cantidad_facturada_item, 2)
                            valor_facturado = round(valor_facturado + valor_facturado_item, 2)
                    # Valores ordenes de servicio
                    items_ordenes_servicio = SuministroOrdenServicioItem.objects.filter(orden_servicio__proyecto=proyecto, suministro=suministro_apu_proyecto.suministro)
                    if items_ordenes_servicio:
                        for item_orden_servicio in items_ordenes_servicio:
                            cantidad_facturada_item, valor_facturado_item = item_orden_servicio.cantidad_facturada_valor_facturado()
                            cantidad_facturada = round(cantidad_facturada + cantidad_facturada_item, 2)
                            valor_facturado = round(valor_facturado + valor_facturado_item, 2)
                    # Valores ordenes de giro
                    items_ordenes_giro = ItemOrdenGiro.objects.filter(orden_giro__proyecto=proyecto, suministro__suministro__suministro=suministro_apu_proyecto.suministro)
                    if items_ordenes_giro:
                        for item_orden_giro in items_ordenes_giro:
                            valor_facturado_item = item_orden_giro.valor_facturado()
                            cantidad_facturada = round(cantidad_facturada + valor_facturado_item, 2)
                            valor_facturado = round(valor_facturado + valor_facturado_item, 2)
                    suministro_apu_proyecto.cantidad_facturada = cantidad_facturada
                    suministro_apu_proyecto.valor_facturado = valor_facturado
                return render_to_response('reporteanalisiscantidadessuministrosproyecto.html', {'user': user, 'suministros': lista_suministros_apus_proyecto, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def reporte_analisis_precios_apus_proyecto(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_apuproyecto' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                return render_to_response('reporteanalisispreciossuministrosapusproyecto.html', {'user': user, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def reporte_analisis_precios_suministros_proyecto(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_apuproyecto' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                suministros_orden_compra = SuministroOrdenCompraItem.objects.filter(orden_compra__proyecto=proyecto, suministro__nombre__icontains=criterio)
                suministros = []
                ids_suministros = []
                for suministro_orden_compra in suministros_orden_compra:
                    if not suministro_orden_compra.suministro_id in ids_suministros:
                        cantidad_comprada = suministro_orden_compra.cantidad_comprada_item()
                        suministros.append({'suministro': suministro_orden_compra.suministro, 'cantidad': cantidad_comprada, 'precio_ejecutado_ordenes_compra': round(round(cantidad_comprada * suministro_orden_compra.precio, 2) + round(cantidad_comprada * suministro_orden_compra.precio * suministro_orden_compra.iva_suministro, 2), 2)})
                        ids_suministros.append(suministro_orden_compra.suministro_id)
                    else:
                        for suministro in suministros:
                            if suministro['suministro'].id == suministro_orden_compra.suministro_id:
                                cantidad_comprada = suministro_orden_compra.cantidad_comprada_item()
                                suministro['precio_ejecutado_ordenes_compra'] = round(suministro['precio_ejecutado_ordenes_compra'] + round(round(cantidad_comprada * suministro_orden_compra.precio, 2) + round(cantidad_comprada * suministro_orden_compra.precio * suministro_orden_compra.iva_suministro, 2), 2), 2)
                                suministro['cantidad'] = round(suministro['cantidad'] + cantidad_comprada, 2)
                tamanio_lista = len(suministros)
                indice_i = 0
                while indice_i < tamanio_lista:
                    indice_j = indice_i + 1
                    while indice_j < tamanio_lista:
                        if suministros[indice_j]['precio_ejecutado_ordenes_compra'] > suministros[indice_i]['precio_ejecutado_ordenes_compra']:
                            suministro = suministros[indice_i]
                            suministros[indice_i] = suministros[indice_j]
                            suministros[indice_j] = suministro
                        indice_j += 1
                    indice_i += 1
                return render_to_response('reporteanalisispreciossuministrosproyecto.html', {'user': user, 'suministros': suministros, 'criterio': criterio, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#### FUNCIONES PARA ANULACIONES ####

# Función para anular una orden de compra
def anular_orden_compra_proyecto(request, orden_compra_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.delete_ordencompra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
                if len(orden_compra.informerecepcion_set.all()) == 0:
                    for item_orden_compra in orden_compra.suministroordencompraitem_set.all():
                        for suministro_orden_compra in item_orden_compra.suministroordencompra_set.all():
                            #Actualizar suministro_apu_proyecto
                            suministro_apu_proyecto = suministro_orden_compra.suministro.suministro
                            suministro_apu_proyecto.cantidad_requerida = round(suministro_apu_proyecto.cantidad_requerida + suministro_orden_compra.cantidad_comprada, 2)
                            suministro_apu_proyecto.cantidad_comprada = round(suministro_apu_proyecto.cantidad_comprada - suministro_orden_compra.cantidad_comprada, 2)
                            suministro_apu_proyecto.save()
                            #Actualizar suministro_requisicion
                            suministro_requisicion = suministro_orden_compra.suministro
                            suministro_requisicion.cantidad_comprada = round(suministro_requisicion.cantidad_comprada - suministro_orden_compra.cantidad_comprada, 2)
                            suministro_requisicion.save()
                            #Actualiza el estado de la requisición
                            suministro_requisicion.requisicion.actualizar_estado()
                            #Si se requiere eliminar el registro
                            suministro_orden_compra.delete()
                        #Si se requiere eliminar el registro
                        item_orden_compra.delete()
                    #Si se requiere eliminar el registro
                    orden_compra.delete()
                    #Si no se requiere eliminar el registro quitar comentarios de las siguientes dos lineas
                    #orden_servicio.estado = 4
                    #orden_servicio.save()
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


# Función para anular una orden de servicio
def anular_orden_servicio_proyecto(request, orden_servicio_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.delete_ordenservicio' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
                if len(orden_servicio.cortediarioobra_set.all()) == 0:
                    for item_orden_servicio in orden_servicio.suministroordenservicioitem_set.all():
                        for suministro_orden_servicio in item_orden_servicio.suministroordenservicio_set.all():
                            #Actualizar suministro_apu_proyecto
                            suministro_apu_proyecto = suministro_orden_servicio.suministro.suministro
                            suministro_apu_proyecto.cantidad_requerida = round(suministro_apu_proyecto.cantidad_requerida + suministro_orden_servicio.cantidad, 2)
                            suministro_apu_proyecto.cantidad_comprada = round(suministro_apu_proyecto.cantidad_comprada - suministro_orden_servicio.cantidad, 2)
                            suministro_apu_proyecto.save()
                            #Actualizar suministro_requisicion
                            suministro_requisicion = suministro_orden_servicio.suministro
                            suministro_requisicion.cantidad_comprada = round(suministro_requisicion.cantidad_comprada - suministro_orden_servicio.cantidad, 2)
                            suministro_requisicion.save()
                            #Actualiza el estado de la requisición
                            suministro_requisicion.requisicion.actualizar_estado()
                            #Si se requiere eliminar el registro
                            suministro_orden_servicio.delete()
                        #Si se requiere eliminar el registro
                        item_orden_servicio.delete()
                    #Si se requiere eliminar el registro
                    orden_servicio.delete()
                    #Si no se requiere eliminar el registro quitar comentarios de las siguientes dos lineas
                    #orden_servicio.estado = 4
                    #orden_servicio.save()
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def eliminar_factura_orden_compra_proyecto(request, factura_orden_compra_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.delete_facturaordencompra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                factura_orden_compra = FacturaOrdencompra.objects.get(orden_compra__proyecto=proyecto, id=factura_orden_compra_id)
                items_factura = factura_orden_compra.itemfacturaordencompra_set.all()
                for item in items_factura:
                    suministros_item_factura = item.suministrofacturaordencompra_set.all()
                    for suministro in suministros_item_factura:
                        # Actualiza la cantidad facturada en suministro en la orden de compra
                        suministro_orden_compra = suministro.suministro_informe_recepcion.suministro
                        suministro_orden_compra.cantidad_facturada = round(suministro_orden_compra.cantidad_facturada - suministro.cantidad, 2)
                        suministro_orden_compra.save()
                        # Actualiza la cantidad facturada en suministro informe de recepción
                        suministro_informe_recepcion = suministro.suministro_informe_recepcion
                        suministro_informe_recepcion.cantidad_facturada = round(suministro_informe_recepcion.cantidad_facturada - suministro.cantidad, 2)
                        suministro_informe_recepcion.save()
                        #Elimina el suministro_factura orden_compra
                        suministro.delete()
                    # Elimina el item_factura_orden_compra
                    item.delete()
                # Elimina la factura_orden_compra
                factura_orden_compra.delete()
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')



#### FUNCIONES PARA LIQUIDACIONES ####

# Función para liquidar una orden de servicio
def liquidar_orden_servicio_proyecto(request, orden_servicio_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.delete_ordenservicio' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
                items_orden_servicio = orden_servicio.suministroordenservicioitem_set.all()
                for item_orden_servicio in items_orden_servicio:
                    for suministro_orden_servicio in item_orden_servicio.suministroordenservicio_set.filter(cantidad_entregada__lt=F('cantidad')):
                        #Actualizar suministro_apu_proyecto
                        suministro_apu_proyecto = suministro_orden_servicio.suministro.suministro
                        suministro_apu_proyecto.cantidad_requerida = round(suministro_apu_proyecto.cantidad_requerida + round(suministro_orden_servicio.cantidad - suministro_orden_servicio.cantidad_entregada, 2), 2)
                        suministro_apu_proyecto.cantidad_comprada = round(suministro_apu_proyecto.cantidad_comprada - round(suministro_orden_servicio.cantidad - suministro_orden_servicio.cantidad_entregada, 2), 2)
                        suministro_apu_proyecto.save()
                        #Actualizar suministro_requisicion
                        suministro_requisicion = suministro_orden_servicio.suministro
                        suministro_requisicion.cantidad_comprada = round(suministro_requisicion.cantidad_comprada - round(suministro_orden_servicio.cantidad - suministro_orden_servicio.cantidad_entregada, 2), 2)
                        suministro_requisicion.save()
                        #Actualiza el estado de la requisición
                        suministro_requisicion.requisicion.actualizar_estado()
                        #Actualiza el suministro de la orden de servicio
                        suministro_orden_servicio.cantidad = suministro_orden_servicio.cantidad_entregada
                        suministro_orden_servicio.save()
                        #Si se requiere eliminar el registro por completo
                        if suministro_orden_servicio.cantidad_entregada == 0:
                            suministro_orden_servicio.delete()
                    #Si se requiere eliminar el registro por completo
                    if len(item_orden_servicio.suministroordenservicio_set.all()) == 0:
                        item_orden_servicio.delete()
                #Si se requiere eliminar el registro por completo
                if len(orden_servicio.suministroordenservicioitem_set.all()) == 0:
                    orden_servicio.delete()
                #Si no se requiere eliminar el registro
                orden_servicio.estado = 3
                orden_servicio.save()
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#### FUNCIONES PARA IMPRIMIR PDFS CON REPORTLAB ####

def drawPageFrame(request):

    import os

    #Obtenemos de platypus las clases Paragraph, para escribir párrafos Image, para insertar imágenes y SimpleDocTemplate para definir el DocTemplate. Además importamos Spacer, para incluir espacios .

    from reportlab.platypus import Paragraph
    from reportlab.platypus import Image
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
    from reportlab.platypus import Spacer

    #Importamos clase de hoja de estilo de ejemplo.

    from reportlab.lib.styles import getSampleStyleSheet

    #Se importa el tamaño de la hoja.

    from reportlab.lib.pagesizes import letter

    #Y los colores.

    from reportlab.lib import colors

    #Creamos un PageTemplate de ejemplo.

    estiloHoja = getSampleStyleSheet()


    #Font texto
    from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY

    #Inicializamos la lista Platypus Story.

    story = []

    #Definimos cómo queremos que sea el estilo de la PageTemplate.

    """
    cabecera = estiloHoja['Heading4']

    #No se hará un salto de página después de escribir la cabecera (valor 1 en caso contrario).

    cabecera.pageBreakBefore=0

    #Se quiere que se empiece en la primera página a escribir. Si es distinto de 0 deja la primera hoja en blanco.

    cabecera.keepWithNext=0

    #Color de la cabecera.

    cabecera.backColor=colors.cyan

    #Incluimos un Flowable, que en este caso es un párrafo.

    parrafo = Paragraph("CABECERA DEL DOCUMENTO ",cabecera)

    #Lo incluimos en el Platypus story.

    story.append(parrafo)

    """
    

    """
    #Definimos un párrafo. Vamos a crear un texto largo para demostrar cómo se genera más de una hoja.

    cadena = " El Viaje del Navegante " * 600

    #Damos un estilo BodyText al segundo párrafo, que será el texto a escribir.

    estilo = estiloHoja['BodyText']
    parrafo2 = Paragraph(cadena, estilo)

    #Y lo incluimos en el story.

    story.append(parrafo2)

    #Dejamos espacio.

    story.append(Spacer(0,20))

    #Ahora incluimos una imagen.

    """

    fichero_imagen = "rotulo.png"
    imagen_logo = Image(os.path.realpath(fichero_imagen),width=575,height=70)
    story.append(imagen_logo)

    story.append(Spacer(0,20))

    usuarios = Usuario.objects.all()


    
    #Estilos de la tabla para cabeceras y datos
    thead = estiloHoja["Normal"]
    thead.alignment=TA_CENTER
    tbody = estiloHoja["BodyText"]
    tbody.alignment=TA_JUSTIFY

    #donde textox_bd es el texto que proviene directamente de la BD

    datos = []

    #cabecera = [Paragraph(str('Identificacion'),thead), Paragraph(str('Nombre de usuario'),thead), Paragraph(str('Nombres'),thead), Paragraph(str('Apellidos'),thead), Paragraph(str('Cargo'),thead), Paragraph(str('Telefono'),thead), Paragraph(str('Estado'),thead)]

    cabecera = [Paragraph(str('Identificacion'),thead), Paragraph(str('Nombre de usuario'),thead), Paragraph(str('Nombres'),thead), Paragraph(str('Apellidos'),thead)]

    datos.append(cabecera)



    #for usuario in usuarios:
    #    datos.append([Paragraph(str(usuario.identificacion),tbody), Paragraph(usuario.username,tbody), Paragraph(usuario.first_name,tbody), Paragraph(usuario.last_name,tbody), Paragraph(usuario.cargo,tbody), Paragraph(str(usuario.celular),tbody), Paragraph(str(usuario.is_active),tbody)])


    for usuario in usuarios:
        datos.append([Paragraph(str(usuario.identificacion),tbody), Paragraph(usuario.username,tbody), Paragraph(usuario.first_name,tbody), Paragraph(usuario.last_name,tbody)])



    tabla = Table(data=datos)

    # First the top row, with all the text centered and in Times-Bold,
    # and one line above, one line below.
    ts = [('ALIGN', (1,1), (-1,-1), 'CENTER'),
         ('LINEABOVE', (0,0), (-1,0), 1, colors.purple),
         ('LINEBELOW', (0,0), (-1,0), 1, colors.purple),
         ('FONT', (0,0), (-1,0), 'Times-Bold'),

    # The bottom row has one line above, and three lines below of
    # various colors and spacing.
         ('LINEABOVE', (0,-1), (-1,-1), 1, colors.purple),
         ('LINEBELOW', (0,-1), (-1,-1), 0.5, colors.purple,
          1, None, None, 4,1),
         ('LINEBELOW', (0,-1), (-1,-1), 1, colors.red),
         ('FONT', (0,-1), (-1,-1), 'Times-Bold')]


    tabla.setStyle(TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.black),
                                           ('BOX',(0,0),(-1,-1),0.25, colors.black),]))


    tabla.wrap(400, None)

    story.append(tabla)

    """
    estilo = estiloHoja['BodyText']

    for usuario in usuarios:
        parrafo = Paragraph(usuario.username, estilo)

        #Y lo incluimos en el story.

        story.append(parrafo)
    """

    #Creamos un DocTemplate en una hoja DIN letter, en la que se muestra el texto enmarcado (showBoundary=1) por un recuadro.
    doc=SimpleDocTemplate("ejemplo1.pdf",pagesize=letter, topMargin=5, leftMargin=15, rightMargin=15)

    #Construimos el Platypus story.

    doc.build(story)

    #return response


def pdf_requisicion(request, requisicion_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_requisicion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():

                requisicion = proyecto.requisicion_set.get(id=requisicion_id)

                suministros = requisicion.get_suministros_agrupados()

                import os

                #Obtenemos de platypus las clases Paragraph, para escribir párrafos Image, para insertar imágenes y SimpleDocTemplate para definir el DocTemplate. Además importamos Spacer, para incluir espacios .
                from reportlab.platypus import Paragraph, Table
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
                from reportlab.platypus import Spacer

                #Importamos clase de hoja de estilo de ejemplo.
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

                #Se importa el tamaño de la hoja.
                from reportlab.lib.pagesizes import letter

                #Y los colores.
                from reportlab.lib import colors

                #Creamos un PageTemplate de ejemplo.
                estiloHoja = getSampleStyleSheet()

                #Font texto
                from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY

                #Inicializamos la lista Platypus Story.
                story = []


                #Definimos el rotulo.
                fichero_imagen = "rotulorequisicion.jpg"
                rotulo = generar_rotulo(fichero_imagen, 525, 70)
                story.append(rotulo)

                story.append(Spacer(0,10))

                datos = []

                #Estilos de la tabla para cabeceras
                especificaciones = {'name': 'cabeceraTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_CENTER, 'borderRadius': 0.5}
                thead = generar_estilo(especificaciones)

                #Estilos de la tabla para datos
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_JUSTIFY, 'borderRadius': 0.5}
                tbody = generar_estilo(especificaciones)
                #Ajustar a la izquierda
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_LEFT, 'borderRadius': 0.5}
                tbody_ajustar_izquierda = generar_estilo(especificaciones)
                #Ajustar a la derecha
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_RIGHT, 'borderRadius': 0.5}
                tbody_ajustar_derecha = generar_estilo(especificaciones)

                #Estilo para registro
                especificaciones = {'name': 'cabeceraTabla', 'fontSize': 6, 'leading': 8, 'alignment': TA_LEFT, 'borderRadius': 0.5}
                tregistro = generar_estilo(especificaciones)

                datos.append([Paragraph('PROYECTO: ', thead), Paragraph('REQ. No. : ', thead), Paragraph('Fecha de registro: ' + str(requisicion.fecha_creacion.date()), tbody)])
                datos.append([Paragraph(unicode(proyecto.nombre), thead), Paragraph('RE' + str(proyecto.id) + ' - ' + str(requisicion.consecutivo), thead), Paragraph('Fecha arribo: ' + str(requisicion.fecha_arribo), tbody)])

                tabla = Table(data=datos, colWidths=[291, 84, 150])

                tabla.setStyle(TableStyle([('LINEAFTER', (0,0),(-1,-1),0.25, colors.black),
                                                       ('BOX', (0,0),(-1,-1),0.25, colors.black),]))

                story.append(tabla)

                story.append(Spacer(0,10))


                #donde textox_bd es el texto que proviene directamente de la BD
                datos = []

                #Datos de cabecera de la tabla
                cabecera = [Paragraph(str('No.'), thead), Paragraph(str('COD.'), thead), Paragraph(str('SUMINISTRO'), thead), Paragraph(str('CANT.'), thead), Paragraph(str('UNIDAD'), thead), Paragraph(str('OBSERVACIONES'), thead)]

                datos.append(cabecera)

                #Datos cuerpo de la tabla
                indice = 1
                for suministro in suministros:
                    datos.append([Paragraph(str(indice), thead), Paragraph(str(suministro.suministro.suministro.get_codigo_suministro()), thead), Paragraph(unicode(suministro.suministro.suministro.nombre), tbody), Paragraph(str(intcomma(suministro.cantidad_requerida)), tbody_ajustar_derecha), Paragraph(suministro.suministro.suministro.unidad_medida, thead), Paragraph(unicode(suministro.observaciones), tbody)])
                    indice = indice + 1

                tabla = Table(data=datos, colWidths=[24, 42, 225, 42, 42, 150])


                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.black),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                #tabla.wrap(400, None)

                story.append(tabla)

                story.append(Spacer(0,10))

                #Firma de la persona que registro la requisición
                registro = Paragraph(u'Registró: ' + unicode(requisicion.persona.first_name).upper() + ' ' + unicode(requisicion.persona.last_name).upper() + ', ' + unicode(requisicion.persona.cargo), tregistro)
                story.append(registro)

                # Creamos el objeto HttpResponse con los headers apropiados para PDF.
                response = HttpResponse(mimetype='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=requisicion.pdf'

                #Creamos un DocTemplate en una hoja DIN letter, en la que se muestra el texto enmarcado (showBoundary=1) por un recuadro.
                doc=SimpleDocTemplate(response, pagesize=letter, topMargin=16, leftMargin=15, rightMargin=15, bottomMargin=5)

                #Construimos el Platypus story.

                doc.build(story, canvasmaker=NumberedCanvas)
                #doc.build(story)

                return response
                #return requisiciones_proyecto_details(request, requisicion_id, proyecto_id)
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def pdf_cotizacion_orden(request, cotizacion_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_cotizacion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():

                cotizacion = None
                try:
                    cotizacion = proyecto.cotizacion_set.get(id=cotizacion_id)
                except :
                    pass

                if cotizacion != None:
                    suministros = cotizacion.suministrocotizacion_set.all()

                    #Obtenemos de platypus las clases Paragraph, para escribir párrafos Image, para insertar imágenes y SimpleDocTemplate para definir el DocTemplate. Además importamos Spacer, para incluir espacios .
                    from reportlab.platypus import Paragraph, Table
                    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
                    from reportlab.platypus import Spacer

                    #Importamos clase de hoja de estilo de ejemplo.
                    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

                    #Se importa el tamaño de la hoja.
                    from reportlab.lib.pagesizes import letter

                    #Y los colores.
                    from reportlab.lib import colors

                    #Creamos un PageTemplate de ejemplo.
                    estiloHoja = getSampleStyleSheet()

                    #Font texto
                    from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY

                    #Inicializamos la lista Platypus Story.
                    story = []


                    #Definimos el rotulo.
                    fichero_imagen = "rotulocotizacionordencompra.jpg"
                    if cotizacion.tipo == 2:
                        fichero_imagen = "rotulocotizacionordenservicio.jpg"
                    rotulo = generar_rotulo(fichero_imagen, 525, 70)
                    story.append(rotulo)

                    story.append(Spacer(0,10))

                    #Estilos de la tabla para cabeceras
                    especificaciones = {'name': 'cabeceraTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_CENTER, 'borderRadius': 0.5}
                    thead = generar_estilo(especificaciones)

                    #Estilos de la tabla para datos
                    especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_JUSTIFY, 'borderRadius': 0.5}
                    tbody = generar_estilo(especificaciones)
                    #Ajustar a la izquierda
                    especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_LEFT, 'borderRadius': 0.5}
                    tbody_ajustar_izquierda = generar_estilo(especificaciones)
                    #Ajustar a la derecha
                    especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_RIGHT, 'borderRadius': 0.5}
                    tbody_ajustar_derecha = generar_estilo(especificaciones)

                    #Estilo para registro
                    especificaciones = {'name': 'cabeceraTabla', 'fontSize': 6, 'leading': 8, 'alignment': TA_LEFT, 'borderRadius': 0.5}
                    tregistro = generar_estilo(especificaciones)

                    datos = []

                    datos.append([Paragraph('PROVEEDOR: ' + unicode(cotizacion.proveedor.razon_social), tbody), Paragraph('NIT: ' + str(cotizacion.proveedor.identificacion), tbody)])
                    datos.append([Paragraph('TELEFONO: ' + cotizacion.proveedor.telefono_1, tbody), Paragraph('E-MAIL: ' + cotizacion.proveedor.email, tbody)])

                    tabla = Table(data=datos, colWidths=[262.5, 262.5])

                    estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                           ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                    tabla.setStyle(estilo_tabla)

                    story.append(tabla)

                    story.append(Spacer(0,10))

                    story.append(Paragraph(u'Solicitamos cotizar los siguientes suministros para el proyecto referenciado', thead))

                    story.append(Spacer(0,10))

                    datos = []

                    datos.append([Paragraph('PROYECTO: ' + unicode(cotizacion.proyecto.nombre), tbody), Paragraph('CIUDAD: ' + unicode(cotizacion.proyecto.municipio.nombre) + ', ' + unicode(cotizacion.proyecto.municipio.departamento.nombre), tbody)])
                    datos.append([Paragraph('DIRECCION: ' + unicode(cotizacion.proyecto.direccion), tbody), Paragraph('', tbody)])

                    tabla = Table(data=datos, colWidths=[262.5, 262.5])

                    estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                           ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                    tabla.setStyle(estilo_tabla)

                    story.append(tabla)

                    story.append(Spacer(0,10))

                    #donde textox_bd es el texto que proviene directamente de la BD
                    datos = []

                    #Datos de cabecera de la tabla
                    cabecera = [Paragraph(str('No.'), thead), Paragraph(str('DESCRIPCION'), thead), Paragraph(str('CANT.'), thead), Paragraph(str('UNIDAD'), thead), Paragraph(str('OBSERVACIONES'), thead)]

                    datos.append(cabecera)

                    #Datos cuerpo de la tabla
                    indice = 1
                    for suministro in suministros:
                        datos.append([Paragraph(str(indice), thead), Paragraph(unicode(suministro.suministro.nombre), tbody), Paragraph(str(intcomma(suministro.cantidad_cotizada)), tbody_ajustar_derecha), Paragraph(suministro.suministro.unidad_medida, thead), Paragraph(unicode(suministro.observaciones), tbody)])
                        indice = indice + 1

                    tabla = Table(data=datos, colWidths=[24, 267, 42, 42, 150])


                    estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.black),
                                                           ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                    tabla.setStyle(estilo_tabla)

                    #tabla.wrap(400, None)

                    story.append(tabla)

                    story.append(Spacer(0,10))

                    #Informacion de compras y contratación
                    fichero_imagen = "rotuloinformacioncomprascotizacion.jpg"
                    informacion_compras = generar_rotulo(fichero_imagen, 525, 40)
                    story.append(informacion_compras)

                    story.append(Spacer(0,10))

                    #Firma de la persona que registro la requisición
                    registro = Paragraph(u'Registró: ' + unicode(cotizacion.persona).upper() + ', ' + unicode(cotizacion.persona.cargo) + ' - Fecha de registro: ' + str(cotizacion.fecha_creacion.date()), tregistro)
                    story.append(registro)

                    # Creamos el objeto HttpResponse con los headers apropiados para PDF.
                    response = HttpResponse(mimetype='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename=cotizacion.pdf'

                    #Creamos un DocTemplate en una hoja DIN letter, en la que se muestra el texto enmarcado (showBoundary=1) por un recuadro.
                    doc=SimpleDocTemplate(response, pagesize=letter, topMargin=16, leftMargin=15, rightMargin=15, bottomMargin=5)

                    #Construimos el Platypus story.

                    doc.build(story, canvasmaker=NumberedCanvas)
                    #doc.build(story)

                    return response

        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def pdf_orden_compra(request, orden_compra_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_ordencompra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)

                suministros = orden_compra.get_suministros_agrupados_suministro()

                #Obtenemos de platypus las clases Paragraph, para escribir párrafos Image, para insertar imágenes y SimpleDocTemplate para definir el DocTemplate. Además importamos Spacer, para incluir espacios .
                from reportlab.platypus import Paragraph, Table
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
                from reportlab.platypus import Spacer

                #Importamos clase de hoja de estilo de ejemplo.
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

                #Se importa el tamaño de la hoja.
                from reportlab.lib.pagesizes import letter

                #Y los colores.
                from reportlab.lib import colors

                #Creamos un PageTemplate de ejemplo.
                estiloHoja = getSampleStyleSheet()

                #Font texto
                from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY

                #Inicializamos la lista Platypus Story.
                story = []

                #Definimos el rotulo.
                fichero_imagen = "rotuloordencompra.jpg"
                rotulo = generar_rotulo(fichero_imagen, 525, 70)
                story.append(rotulo)

                story.append(Spacer(0,10))

                #Estilos de la tabla para cabeceras
                especificaciones = {'name': 'cabeceraTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_CENTER, 'borderRadius': 0.5}
                thead = generar_estilo(especificaciones)

                #Estilos de la tabla para datos
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_JUSTIFY, 'borderRadius': 0.5}
                tbody = generar_estilo(especificaciones)
                #Ajustar a la izquierda
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_LEFT, 'borderRadius': 0.5}
                tbody_ajustar_izquierda = generar_estilo(especificaciones)
                #Ajustar a la derecha
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_RIGHT, 'borderRadius': 0.5}
                tbody_ajustar_derecha = generar_estilo(especificaciones)

                #Estilo para registro
                especificaciones = {'name': 'cabeceraTabla', 'fontSize': 6, 'leading': 8, 'alignment': TA_LEFT, 'borderRadius': 0.5}
                tregistro = generar_estilo(especificaciones)

                datos = []

                datos.append([Paragraph('PROVEEDOR: ' + unicode(orden_compra.proveedor.razon_social), tbody), Paragraph('NIT: ' + str(orden_compra.proveedor.identificacion), tbody)])
                datos.append([Paragraph('TELEFONO: ' + orden_compra.proveedor.telefono_1, tbody), Paragraph('E-MAIL: ' + orden_compra.proveedor.email, tbody)])

                tabla = Table(data=datos, colWidths=[262.5, 262.5])

                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                story.append(tabla)

                story.append(Spacer(0,10))

                nombre_almacenista = ' - '
                try:
                    # Consulta almacenista de obra
                    almacenista = proyecto.personaadministrativoproyecto_set.get(persona__cargo='ALMACENISTA', estado_registro=True)
                    nombre_almacenista = unicode(almacenista.persona.first_name).upper() + ' ' + unicode(almacenista.persona.last_name).upper()
                except :
                    pass

                story.append(Paragraph(u'Solicitamos despachar los siguientes suministros para el proyecto referenciado y hacer entrega a: ' + unicode(nombre_almacenista) + ' almacenista de la obra', thead))

                story.append(Spacer(0,10))

                datos = []

                datos.append([Paragraph('<b>ORDEN DE COMPRA No.: OC' + str(proyecto.id) + ' - ' + str(orden_compra.consecutivo) + '</b>', tbody), Paragraph('FECHA DE REGISTRO: ' + str(orden_compra.fecha_creacion.date()), tbody)])
                datos.append([Paragraph('PROYECTO: ' + unicode(orden_compra.proyecto.nombre), tbody), Paragraph('CIUDAD: ' + unicode(orden_compra.proyecto.municipio.nombre) + ', ' + unicode(orden_compra.proyecto.municipio.departamento.nombre), tbody)])
                datos.append([Paragraph('DIRECCION: ' + unicode(orden_compra.proyecto.direccion), tbody), Paragraph('FECHA DE ENTREGA: ' + str(orden_compra.fecha_arribo), tbody)])

                tabla = Table(data=datos, colWidths=[262.5, 262.5])

                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                story.append(tabla)

                story.append(Spacer(0,10))

                #donde textox_bd es el texto que proviene directamente de la BD
                datos = []

                #Datos de cabecera de la tabla
                cabecera = [Paragraph(str('No.'), thead), Paragraph(str('DESCRIPCION'), thead), Paragraph(str('CANT.'), thead), Paragraph(str('UNIDAD'), thead), Paragraph(str('VALOR UNITARIO'), thead), Paragraph(str('VALOR ITEM'), thead), Paragraph(str('IVA'), thead), Paragraph(str('OBSERVACIONES'), thead)]

                datos.append(cabecera)

                #Datos cuerpo de la tabla
                indice = 1
                for suministro in suministros:
                    datos.append([Paragraph(str(indice), thead), Paragraph(unicode(suministro.suministro.suministro.suministro.nombre), tbody), Paragraph(str(intcomma(suministro.cantidad_comprada)), tbody_ajustar_derecha), Paragraph(suministro.suministro.suministro.suministro.unidad_medida, thead), Paragraph(str(intcomma(suministro.suministro_orden_compra_item.precio)), tbody_ajustar_derecha), Paragraph(str(intcomma(round(suministro.cantidad_comprada * suministro.suministro_orden_compra_item.precio, 2))), tbody_ajustar_derecha), Paragraph(str(int(suministro.suministro_orden_compra_item.iva_suministro * 100)) + '%', tbody_ajustar_derecha), Paragraph(unicode(suministro.suministro_orden_compra_item.observaciones), tbody)])
                    indice = indice + 1

                tabla = Table(data=datos, colWidths=[24, 190, 42, 42, 52, 60, 25, 90])


                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.black),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                #tabla.wrap(400, None)

                story.append(tabla)

                story.append(Spacer(0,10))

                datos = []

                #Contenido1 = forma de pago, valor en letras
                contenido1 = []
                forma_pago = ''
                if orden_compra.forma_pago == 1:
                    forma_pago = 'Credito, a ' + str(orden_compra.dias_credito)
                elif orden_compra.forma_pago == 2:
                    forma_pago = 'Contra-entrega'
                elif orden_compra.forma_pago == 3:
                    forma_pago = 'Anticipado'
                elif orden_compra.forma_pago == 4:
                    forma_pago = str(orden_compra.porcentaje_anticipo) + ' % anticipo'
                valor = orden_compra.valor_total()
                valor_letras = to_word(int(valor), 'COP')
                valor_letras = 'Son: ' + valor_letras + ' con ' + str(valor).split('.')[1] + ' centavos.'
                contenido1.append([Paragraph('Forma de pago: ' + forma_pago, tbody)])
                contenido1.append([Paragraph('', tbody)])
                contenido1.append([Paragraph('', tbody)])
                contenido1.append([Paragraph(valor_letras, tbody)])
                #tabla_contenido1 sin estilo para que no se vean los bordes
                tabla_contenido1 = Table(data=contenido1, colWidths=[360])
                estilo_tabla = TableStyle([('LINEABOVE', (0,0),(-1,-1),0.25, colors.black),
                                                       ('LINEABOVE',(0,0),(-1,-1),0.25, colors.black),])
                #tabla_contenido1.setStyle(estilo_tabla)

                #Contenido2 = valor total sin iva, valor del iva, valor total
                contenido2 = []
                contenido2.append([Paragraph('<b>Valor: </b>', tbody_ajustar_derecha), Paragraph(str(intcomma(orden_compra.valor_total_sin_iva())), tbody_ajustar_derecha)])
                contenido2.append([Paragraph('<b>IVA: </b>', tbody_ajustar_derecha), Paragraph(str(intcomma(orden_compra.valor_iva())), tbody_ajustar_derecha)])
                contenido2.append([Paragraph('<b>Valor total: </b>', tbody_ajustar_derecha), Paragraph(str(intcomma(orden_compra.valor_total())), tbody_ajustar_derecha)])
                tabla_contenido2 = Table(data=contenido2, colWidths=[60, 80])
                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.black),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])
                tabla_contenido2.setStyle(estilo_tabla)

                datos.append([tabla_contenido1, tabla_contenido2])


                tabla = Table(data=datos, colWidths=[370, 155])

                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.black),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                story.append(tabla)

                story.append(Spacer(0,10))

                #Observaciones de la orden de compra
                datos = []

                datos.append([Paragraph('Observaciones: ' + unicode(orden_compra.observaciones) + '\n' + 'Adjuntar certificado de calidad de los suministros.', tbody)])

                tabla = Table(data=datos, colWidths=[525])

                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.black),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                story.append(tabla)

                story.append(Spacer(0,5))

                #Informacion de la orden de compra
                fichero_imagen = "rotuloinformacionordencompra.jpg"
                informacion_orden_compra = generar_rotulo(fichero_imagen, 525, 40)
                story.append(informacion_orden_compra)

                #Firma persona elaboró
                story.append(Paragraph(u'Registró: ' + unicode(orden_compra.persona.first_name).upper() + ' ' + unicode(orden_compra.persona.last_name).upper() + ', ' + unicode(orden_compra.persona.cargo), tregistro))

                # Creamos el objeto HttpResponse con los headers apropiados para PDF.
                response = HttpResponse(mimetype='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=ordencompra.pdf'

                #Creamos un DocTemplate en una hoja DIN letter, en la que se muestra el texto enmarcado (showBoundary=1) por un recuadro.
                doc=SimpleDocTemplate(response, pagesize=letter, topMargin=16, leftMargin=15, rightMargin=15, bottomMargin=5)

                #Construimos el Platypus story.

                doc.build(story, canvasmaker=NumberedCanvas)
                #doc.build(story)

                return response

        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def pdf_informe_recepcion(request, informe_recepcion_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_informerecepcion' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                informe_recepcion = InformeRecepcion.objects.get(id=informe_recepcion_id)

                suministros = informe_recepcion.get_suministros_agrupados_suministro()

                #Obtenemos de platypus las clases Paragraph, para escribir párrafos Image, para insertar imágenes y SimpleDocTemplate para definir el DocTemplate. Además importamos Spacer, para incluir espacios .
                from reportlab.platypus import Paragraph, Table
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
                from reportlab.platypus import Spacer

                #Importamos clase de hoja de estilo de ejemplo.
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

                #Se importa el tamaño de la hoja.
                from reportlab.lib.pagesizes import letter

                #Y los colores.
                from reportlab.lib import colors

                #Creamos un PageTemplate de ejemplo.
                estiloHoja = getSampleStyleSheet()

                #Font texto
                from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY

                #Inicializamos la lista Platypus Story.
                story = []

                #Definimos el rotulo.
                fichero_imagen = "rotuloinformerecepcion.jpg"
                rotulo = generar_rotulo(fichero_imagen, 525, 70)
                story.append(rotulo)

                story.append(Spacer(0,10))

                #Estilos de la tabla para cabeceras
                especificaciones = {'name': 'cabeceraTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_CENTER, 'borderRadius': 0.5}
                thead = generar_estilo(especificaciones)

                #Estilos de la tabla para datos
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_JUSTIFY, 'borderRadius': 0.5}
                tbody = generar_estilo(especificaciones)
                #Ajustar a la izquierda
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_LEFT, 'borderRadius': 0.5}
                tbody_ajustar_izquierda = generar_estilo(especificaciones)
                #Ajustar a la derecha
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_RIGHT, 'borderRadius': 0.5}
                tbody_ajustar_derecha = generar_estilo(especificaciones)

                #Estilo para registro
                especificaciones = {'name': 'cabeceraTabla', 'fontSize': 6, 'leading': 8, 'alignment': TA_LEFT, 'borderRadius': 0.5}
                tregistro = generar_estilo(especificaciones)

                datos = []

                datos.append([Paragraph('PROVEEDOR: ' + unicode(informe_recepcion.orden_compra.proveedor.razon_social), tbody), Paragraph('NIT: ' + str(informe_recepcion.orden_compra.proveedor.identificacion), tbody)])
                datos.append([Paragraph('TELEFONO: ' + informe_recepcion.orden_compra.proveedor.telefono_1, tbody), Paragraph('E-MAIL: ' + informe_recepcion.orden_compra.proveedor.email, tbody)])

                tabla = Table(data=datos, colWidths=[262.5, 262.5])

                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                story.append(tabla)

                story.append(Spacer(0,10))

                datos = []

                datos.append([Paragraph('<b>ORDEN DE COMPRA No.: OC' + str(proyecto.id) + ' - ' + str(informe_recepcion.orden_compra.consecutivo) + '</b>', tbody), Paragraph('No. remision: ' + informe_recepcion.numero_remision, tbody)])
                datos.append([Paragraph('<b>INFORME DE RECEPCION No.: IR' + str(proyecto.id) + ' - ' + str(informe_recepcion.consecutivo) + '</b>', tbody), Paragraph('FECHA DE REGISTRO: ' + str(informe_recepcion.fecha_informe.date()), tbody)])
                datos.append([Paragraph('PROYECTO: ' + unicode(informe_recepcion.orden_compra.proyecto.nombre), tbody), Paragraph('CIUDAD: ' + unicode(informe_recepcion.orden_compra.proyecto.municipio.nombre) + ', ' + unicode(informe_recepcion.orden_compra.proyecto.municipio.departamento.nombre), tbody)])
                datos.append([Paragraph('DIRECCION: ' + proyecto.direccion, tbody), Paragraph('', tbody)])

                tabla = Table(data=datos, colWidths=[262.5, 262.5])

                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                story.append(tabla)

                story.append(Spacer(0,10))

                datos = []

                datos.append([Paragraph('Observaciones: ' + unicode(informe_recepcion.observaciones), tbody)])

                tabla = Table(data=datos, colWidths=[525])

                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                story.append(tabla)

                story.append(Spacer(0,10))

                #donde textox_bd es el texto que proviene directamente de la BD
                datos = []

                #Datos de cabecera de la tabla
                cabecera = [Paragraph(str('No.'), thead), Paragraph(str('DESCRIPCION'), thead), Paragraph(str('CANT.'), thead), Paragraph(str('UNIDAD'), thead)]

                datos.append(cabecera)

                #Datos cuerpo de la tabla
                indice = 1
                for suministro in suministros:
                    datos.append([Paragraph(str(indice), thead), Paragraph(unicode(suministro.suministro.suministro.suministro.suministro.nombre), tbody), Paragraph(str(intcomma(suministro.cantidad)), tbody_ajustar_derecha), Paragraph(suministro.suministro.suministro.suministro.suministro.unidad_medida, thead)])
                    indice = indice + 1

                tabla = Table(data=datos, colWidths=[24, 396, 55, 50])


                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.black),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                #tabla.wrap(400, None)

                story.append(tabla)

                story.append(Spacer(0,10))

                #Observaciones de la orden de compra
                datos = []
                datos.append([Paragraph(u'<b>Importante: </b> Para realizar el pago de la respectiva factura, es indispensable adjuntar este documento.', tbody)])
                tabla = Table(data=datos, colWidths=[525])
                story.append(tabla)

                story.append(Spacer(0,20))

                #Firma almacenista
                datos = []
                datos.append([Paragraph('____________________________________', thead)])
                nombre_almacenista = ''
                try:
                    # Consulta almacenista de obra
                    almacenista = proyecto.personaadministrativoproyecto_set.get(persona__cargo='ALMACENISTA', estado_registro=True)
                    nombre_almacenista = unicode(almacenista.persona.first_name).upper() + ' ' + unicode(almacenista.persona.last_name).upper()
                except :
                    pass
                datos.append([Paragraph(unicode(nombre_almacenista.upper()), thead)])
                datos.append([Paragraph('ALMACENISTA', thead)])
                tabla = Table(data=datos, colWidths=[525])
                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.white),])
                tabla.setStyle(estilo_tabla)
                story.append(tabla)

                story.append(Spacer(0,5))

                #Firma persona elaboró
                story.append(Paragraph(u'Registró: ' + unicode(informe_recepcion.persona.first_name).upper() + ' ' + unicode(informe_recepcion.persona.last_name).upper() + ', ' + unicode(informe_recepcion.persona.cargo), tregistro))

                # Creamos el objeto HttpResponse con los headers apropiados para PDF.
                response = HttpResponse(mimetype='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=informerecepcion.pdf'

                #Creamos un DocTemplate en una hoja DIN letter, en la que se muestra el texto enmarcado (showBoundary=1) por un recuadro.
                doc=SimpleDocTemplate(response, pagesize=letter, topMargin=16, leftMargin=15, rightMargin=15, bottomMargin=5)

                #Construimos el Platypus story.

                doc.build(story, canvasmaker=NumberedCanvas)
                #doc.build(story)

                return response
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def pdf_reporte_almacen(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_suministroalmacen' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                suministros = proyecto.suministroalmacen_set.all().order_by('suministro__nombre')
                fecha_actual = datetime.datetime.now()
                almacenista = Usuario()
                try:
                    # Consulta almacenista de obra
                    almacenista = proyecto.personaadministrativoproyecto_set.get(persona__cargo='ALMACENISTA', estado_registro=True)
                    almacenista = almacenista.persona
                except :
                    pass
                imagen_cabecera = 'pdfs/rotuloreportealmacen.jpg'
                html = render_to_string('pdfreportealmacen.html', {'pagesize': 'letter', 'orientation': 'portrait', 'margin': '1cm', 'imagen_cabecera': imagen_cabecera, 'fecha_actual': fecha_actual, 'almacenista': almacenista, 'suministros': suministros, 'proyecto': proyecto}, context_instance=RequestContext(request))
                return generar_pdf(html, proyecto_id)
                #return render_to_pdf('pdffacturaordencompra.html', {'user': user, 'factura_orden_compra': factura, 'items_factura': items_factura, 'valor_discriminado_capitulos': valor_discriminado_capitulos, 'valor_factura_sin_iva': valor_factura_sin_iva, 'valor_iva_factura': valor_iva_factura, 'valor_total_factura': valor_total_factura, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def pdf_informe_salida(request, informe_salida_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_informesalida' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                informe_salida = proyecto.informesalida_set.get(id=informe_salida_id)

                suministros = informe_salida.suministroinformesalidaitem_set.all()

                #Obtenemos de platypus las clases Paragraph, para escribir párrafos Image, para insertar imágenes y SimpleDocTemplate para definir el DocTemplate. Además importamos Spacer, para incluir espacios .
                from reportlab.platypus import Paragraph, Table
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
                from reportlab.platypus import Spacer

                #Importamos clase de hoja de estilo de ejemplo.
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

                #Se importa el tamaño de la hoja.
                from reportlab.lib.pagesizes import letter

                #Y los colores.
                from reportlab.lib import colors

                #Creamos un PageTemplate de ejemplo.
                estiloHoja = getSampleStyleSheet()

                #Font texto
                from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY

                #Inicializamos la lista Platypus Story.
                story = []

                #Definimos el rotulo.
                fichero_imagen = "rotuloinformesalida.jpg"
                rotulo = generar_rotulo(fichero_imagen, 525, 70)
                story.append(rotulo)

                story.append(Spacer(0,10))

                #Estilos de la tabla para cabeceras
                especificaciones = {'name': 'cabeceraTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_CENTER, 'borderRadius': 0.5}
                thead = generar_estilo(especificaciones)

                #Estilos de la tabla para datos
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_JUSTIFY, 'borderRadius': 0.5}
                tbody = generar_estilo(especificaciones)
                #Ajustar a la izquierda
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_LEFT, 'borderRadius': 0.5}
                tbody_ajustar_izquierda = generar_estilo(especificaciones)
                #Ajustar a la derecha
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_RIGHT, 'borderRadius': 0.5}
                tbody_ajustar_derecha = generar_estilo(especificaciones)

                #Estilo para registro
                especificaciones = {'name': 'cabeceraTabla', 'fontSize': 6, 'leading': 8, 'alignment': TA_LEFT, 'borderRadius': 0.5}
                tregistro = generar_estilo(especificaciones)

                datos = []

                datos.append([Paragraph('SALIDA DE ALMACEN No.: SA' + str(proyecto.id) + ' - ' + str(informe_salida.consecutivo), tbody), Paragraph('FECHA DE REGISTRO: ' + str(informe_salida.fecha_informe.date()), tbody)])
                datos.append([Paragraph('PROYECTO: ' + unicode(informe_salida.proyecto.nombre), tbody), Paragraph('CIUDAD: ' + unicode(informe_salida.proyecto.municipio.nombre) + ', ' + unicode(informe_salida.proyecto.municipio.departamento.nombre), tbody)])
                datos.append([Paragraph('DIRECCION: ' + unicode(informe_salida.proyecto.direccion), tbody), Paragraph('', tbody)])

                tabla = Table(data=datos, colWidths=[262.5, 262.5])

                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                story.append(tabla)

                story.append(Spacer(0,10))

                datos = []

                datos.append([Paragraph('Observaciones: ' + unicode(informe_salida.observaciones), tbody)])

                tabla = Table(data=datos, colWidths=[525])

                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                story.append(tabla)

                story.append(Spacer(0,10))

                #donde textox_bd es el texto que proviene directamente de la BD
                datos = []

                #Datos de cabecera de la tabla
                cabecera = [Paragraph(str('No.'), thead), Paragraph(str('DESCRIPCION'), thead), Paragraph(str('CANT.'), thead), Paragraph(str('UNIDAD'), thead)]

                datos.append(cabecera)

                #Datos cuerpo de la tabla
                indice = 1
                for suministro in suministros:
                    datos.append([Paragraph(str(indice), thead), Paragraph(unicode(suministro.suministro_almacen.suministro.nombre), tbody), Paragraph(str(intcomma(suministro.cantidad())), tbody_ajustar_derecha), Paragraph(suministro.suministro_almacen.suministro.unidad_medida, thead)])
                    indice = indice + 1

                tabla = Table(data=datos, colWidths=[24, 396, 55, 50])


                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.black),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                #tabla.wrap(400, None)

                story.append(tabla)

                story.append(Spacer(0,10))

                #Firmas autorización
                datos = []
                datos.append([Paragraph('____________________________________', thead), Paragraph('____________________________________', thead)])
                nombre_almacenista = ''
                try:
                    # Consulta almacenista de obra
                    almacenista = proyecto.personaadministrativoproyecto_set.get(persona__cargo='ALMACENISTA', estado_registro=True)
                    nombre_almacenista = unicode(almacenista.persona.first_name).upper() + ' ' + unicode(almacenista.persona.last_name).upper()
                except :
                    pass

                datos.append([Paragraph(nombre_almacenista.upper(), thead), Paragraph(unicode(informe_salida.persona_proyecto.nombre).upper(), thead)])
                datos.append([Paragraph('ALMACENISTA', thead), Paragraph(unicode(informe_salida.persona_proyecto.cargo).upper(), thead)])
                tabla = Table(data=datos, colWidths=[262.5, 262.5])
                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.white),])
                tabla.setStyle(estilo_tabla)
                story.append(tabla)

                story.append(Spacer(0,5))

                #Firma persona elaboró
                story.append(Paragraph(u'Registró: ' + unicode(informe_salida.persona.first_name).upper() + ' ' + unicode(informe_salida.persona.last_name).upper() + ', ' + unicode(informe_salida.persona.cargo), tregistro))

                # Creamos el objeto HttpResponse con los headers apropiados para PDF.
                response = HttpResponse(mimetype='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=informesalida.pdf'

                #Creamos un DocTemplate en una hoja DIN letter, en la que se muestra el texto enmarcado (showBoundary=1) por un recuadro.
                doc=SimpleDocTemplate(response, pagesize=letter, topMargin=16, leftMargin=15, rightMargin=15, bottomMargin=5)

                #Construimos el Platypus story.

                doc.build(story, canvasmaker=NumberedCanvas)
                #doc.build(story)

                return response
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def pdf_informes_salidas(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_informesalida' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():



                #Obtenemos de platypus las clases Paragraph, para escribir párrafos Image, para insertar imágenes y SimpleDocTemplate para definir el DocTemplate. Además importamos Spacer, para incluir espacios .
                from reportlab.platypus import Paragraph, Table
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
                from reportlab.platypus import Spacer, PageBreak

                #Importamos clase de hoja de estilo de ejemplo.
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

                #Se importa el tamaño de la hoja.
                from reportlab.lib.pagesizes import letter

                #Y los colores.
                from reportlab.lib import colors

                #Creamos un PageTemplate de ejemplo.
                estiloHoja = getSampleStyleSheet()

                #Font texto
                from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY

                #Inicializamos la lista Platypus Story.
                story = []

                informes_salida = proyecto.informesalida_set.all()

                for informe_salida in informes_salida:

                    suministros = informe_salida.suministroinformesalidaitem_set.all()

                    #Definimos el rotulo.
                    fichero_imagen = "rotuloinformesalida.jpg"
                    rotulo = generar_rotulo(fichero_imagen, 525, 70)
                    story.append(rotulo)

                    story.append(Spacer(0,10))

                    #Estilos de la tabla para cabeceras
                    especificaciones = {'name': 'cabeceraTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_CENTER, 'borderRadius': 0.5}
                    thead = generar_estilo(especificaciones)

                    #Estilos de la tabla para datos
                    especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_JUSTIFY, 'borderRadius': 0.5}
                    tbody = generar_estilo(especificaciones)
                    #Ajustar a la izquierda
                    especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_LEFT, 'borderRadius': 0.5}
                    tbody_ajustar_izquierda = generar_estilo(especificaciones)
                    #Ajustar a la derecha
                    especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_RIGHT, 'borderRadius': 0.5}
                    tbody_ajustar_derecha = generar_estilo(especificaciones)

                    #Estilo para registro
                    especificaciones = {'name': 'cabeceraTabla', 'fontSize': 6, 'leading': 8, 'alignment': TA_LEFT, 'borderRadius': 0.5}
                    tregistro = generar_estilo(especificaciones)

                    datos = []

                    datos.append([Paragraph('SALIDA DE ALMACEN No.: SA' + str(proyecto.id) + ' - ' + str(informe_salida.consecutivo), tbody), Paragraph('FECHA DE REGISTRO: ' + str(informe_salida.fecha_informe.date()), tbody)])
                    datos.append([Paragraph('PROYECTO: ' + unicode(informe_salida.proyecto.nombre), tbody), Paragraph('CIUDAD: ' + unicode(informe_salida.proyecto.municipio.nombre) + ', ' + unicode(informe_salida.proyecto.municipio.departamento.nombre), tbody)])
                    datos.append([Paragraph('DIRECCION: ' + unicode(informe_salida.proyecto.direccion), tbody), Paragraph('', tbody)])

                    tabla = Table(data=datos, colWidths=[262.5, 262.5])

                    estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                           ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                    tabla.setStyle(estilo_tabla)

                    story.append(tabla)

                    story.append(Spacer(0,10))

                    datos = []

                    datos.append([Paragraph('Observaciones: ' + unicode(informe_salida.observaciones), tbody)])

                    tabla = Table(data=datos, colWidths=[525])

                    estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                           ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                    tabla.setStyle(estilo_tabla)

                    story.append(tabla)

                    story.append(Spacer(0,10))

                    #donde textox_bd es el texto que proviene directamente de la BD
                    datos = []

                    #Datos de cabecera de la tabla
                    cabecera = [Paragraph(str('No.'), thead), Paragraph(str('DESCRIPCION'), thead), Paragraph(str('CANT.'), thead), Paragraph(str('UNIDAD'), thead)]

                    datos.append(cabecera)

                    #Datos cuerpo de la tabla
                    indice = 1
                    for suministro in suministros:
                        datos.append([Paragraph(str(indice), thead), Paragraph(unicode(suministro.suministro_almacen.suministro.nombre), tbody), Paragraph(str(intcomma(suministro.cantidad())), tbody_ajustar_derecha), Paragraph(suministro.suministro_almacen.suministro.unidad_medida, thead)])
                        indice = indice + 1

                    tabla = Table(data=datos, colWidths=[24, 396, 55, 50])


                    estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.black),
                                                           ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                    tabla.setStyle(estilo_tabla)

                    #tabla.wrap(400, None)

                    story.append(tabla)

                    story.append(Spacer(0,10))

                    #Firmas autorización
                    datos = []
                    datos.append([Paragraph('____________________________________', thead), Paragraph('____________________________________', thead)])
                    nombre_almacenista = ''
                    try:
                        # Consulta almacenista de obra
                        almacenista = proyecto.personaadministrativoproyecto_set.get(persona__cargo='ALMACENISTA', estado_registro=True)
                        nombre_almacenista = unicode(almacenista.persona.first_name).upper() + ' ' + unicode(almacenista.persona.last_name).upper()
                    except :
                        pass

                    datos.append([Paragraph(nombre_almacenista.upper(), thead), Paragraph(unicode(informe_salida.persona_proyecto.nombre).upper(), thead)])
                    datos.append([Paragraph('ALMACENISTA', thead), Paragraph(unicode(informe_salida.persona_proyecto.cargo).upper(), thead)])
                    tabla = Table(data=datos, colWidths=[262.5, 262.5])
                    estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                           ('BOX',(0,0),(-1,-1),0.25, colors.white),])
                    tabla.setStyle(estilo_tabla)
                    story.append(tabla)

                    story.append(Spacer(0,5))

                    #Firma persona elaboró
                    story.append(Paragraph(u'Registró: ' + unicode(informe_salida.persona.first_name).upper() + ' ' + unicode(informe_salida.persona.last_name).upper() + ', ' + unicode(informe_salida.persona.cargo), tregistro))

                    story.append(PageBreak())

                # Creamos el objeto HttpResponse con los headers apropiados para PDF.
                response = HttpResponse(mimetype='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=informesalida.pdf'

                #Creamos un DocTemplate en una hoja DIN letter, en la que se muestra el texto enmarcado (showBoundary=1) por un recuadro.
                doc=SimpleDocTemplate(response, pagesize=letter, topMargin=16, leftMargin=15, rightMargin=15, bottomMargin=5)

                #Construimos el Platypus story.

                doc.build(story, canvasmaker=NumberedCanvas)
                #doc.build(story)

                return response
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def pdf_orden_servicio(request, orden_servicio_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_ordenservicio' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
                orden_servicio.calcular_valores()

                suministros = orden_servicio.get_suministros_agrupados_suministro()

                #Obtenemos de platypus las clases Paragraph, para escribir párrafos Image, para insertar imágenes y SimpleDocTemplate para definir el DocTemplate. Además importamos Spacer, para incluir espacios .
                from reportlab.platypus import Paragraph, Table
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
                from reportlab.platypus import Spacer

                #Importamos clase de hoja de estilo de ejemplo.
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

                #Se importa el tamaño de la hoja.
                from reportlab.lib.pagesizes import letter

                #Y los colores.
                from reportlab.lib import colors

                #Creamos un PageTemplate de ejemplo.
                estiloHoja = getSampleStyleSheet()

                #Font texto
                from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY

                #Inicializamos la lista Platypus Story.
                story = []

                #Definimos el rotulo.
                fichero_imagen = "rotuloordenservicio.jpg"
                rotulo = generar_rotulo(fichero_imagen, 525, 70)
                story.append(rotulo)

                story.append(Spacer(0,10))

                #Estilos de la tabla para cabeceras
                especificaciones = {'name': 'cabeceraTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_CENTER, 'borderRadius': 0.5}
                thead = generar_estilo(especificaciones)

                #Estilos de la tabla para datos
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_JUSTIFY, 'borderRadius': 0.5}
                tbody = generar_estilo(especificaciones)
                #Ajustar a la izquierda
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_LEFT, 'borderRadius': 0.5}
                tbody_ajustar_izquierda = generar_estilo(especificaciones)
                #Ajustar a la derecha
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_RIGHT, 'borderRadius': 0.5}
                tbody_ajustar_derecha = generar_estilo(especificaciones)

                #Estilo para registro
                especificaciones = {'name': 'cabeceraTabla', 'fontSize': 6, 'leading': 8, 'alignment': TA_LEFT, 'borderRadius': 0.5}
                tregistro = generar_estilo(especificaciones)

                datos = []

                if orden_servicio.tercero != None:
                    datos.append([Paragraph('PROVEEDOR: ' + unicode(orden_servicio.proveedor.razon_social + ' - Supervisor: ' + orden_servicio.tercero.razon_social), tbody), Paragraph('NIT: ' + str(orden_servicio.proveedor.identificacion), tbody)])
                else:
                    datos.append([Paragraph('PROVEEDOR: ' + unicode(orden_servicio.proveedor.razon_social), tbody), Paragraph('NIT: ' + str(orden_servicio.proveedor.identificacion), tbody)])
                datos.append([Paragraph('TELEFONO: ' + orden_servicio.proveedor.telefono_1, tbody), Paragraph('E-MAIL: ' + orden_servicio.proveedor.email, tbody)])

                tabla = Table(data=datos, colWidths=[262.5, 262.5])

                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                story.append(tabla)

                story.append(Spacer(0,10))

                story.append(Paragraph(u'Con la siguiente orden de servicio queda autorizado para ejecutar las siguientes actividades', thead))

                story.append(Spacer(0,10))

                aplica_cooperativa = 'No'

                if orden_servicio.aplica_cooperativa:
                    aplica_cooperativa = 'Si'

                datos = []

                datos.append([Paragraph('<b>ORDEN DE SERVICIO No.: OS' + str(proyecto.id) + ' - ' + str(orden_servicio.consecutivo) + '</b>', tbody), Paragraph('FECHA DE REGISTRO: ' + str(orden_servicio.fecha_creacion.date()), tbody)])
                datos.append([Paragraph('PROYECTO: ' + unicode(orden_servicio.proyecto.nombre), tbody), Paragraph('CIUDAD: ' + unicode(orden_servicio.proyecto.municipio.nombre) + ', ' + unicode(orden_servicio.proyecto.municipio.departamento.nombre), tbody)])
                datos.append([Paragraph('DIRECCION: ' + unicode(orden_servicio.proyecto.direccion), tbody), Paragraph('FECHA MAX. ENTREGA: ' + str(orden_servicio.fecha_entrega), tbody)])

                tabla = Table(data=datos, colWidths=[262.5, 262.5])

                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                story.append(tabla)

                #Información de impuestos y de amortización anticipo
                datos = []
                if orden_servicio.tipo_iva != None:
                    if orden_servicio.tipo_iva == 1:
                        datos.append([Paragraph('%Anticipo: ' + str(orden_servicio.amortizacion), tbody), Paragraph('%Retegarantia: ' + str(orden_servicio.retencion_garantia), tbody), Paragraph('%A.I.U.: ' + str(orden_servicio.porcentaje_a_i_u), tbody), Paragraph('%Utilidad: ' + str(orden_servicio.porcentaje_utilidad), tbody), Paragraph('%IVA Utilidad: ' + str(orden_servicio.porcentaje_iva), tbody), Paragraph('Rtica: ' + str(orden_servicio.rete_ica), tbody), Paragraph('Rtfuente: ' + str(orden_servicio.rete_fuente), tbody)])
                        tabla = Table(data=datos, colWidths=[75, 90, 75, 68, 85, 64, 68])
                    elif orden_servicio.tipo_iva == 2:
                        datos.append([Paragraph('%Anticipo: ' + str(orden_servicio.amortizacion), tbody), Paragraph('%Retegarantia: ' + str(orden_servicio.retencion_garantia), tbody), Paragraph('%IVA: ' + str(orden_servicio.porcentaje_iva), tbody), Paragraph('Rtica: ' + str(orden_servicio.rete_ica), tbody), Paragraph('Rtfuente: ' + str(orden_servicio.rete_fuente), tbody)])
                        tabla = Table(data=datos, colWidths=[105, 105, 105, 105, 105])
                    elif orden_servicio.tipo_iva == 3:
                        datos.append([Paragraph('%Anticipo: ' + str(orden_servicio.amortizacion), tbody), Paragraph('%Retegarantia: ' + str(orden_servicio.retencion_garantia), tbody), Paragraph('%A.I.U.: ' + str(orden_servicio.porcentaje_a_i_u), tbody), Paragraph('%IVA: ' + str(orden_servicio.porcentaje_iva), tbody), Paragraph('Rtica: ' + str(orden_servicio.rete_ica), tbody), Paragraph('Rtfuente: ' + str(orden_servicio.rete_fuente), tbody)])
                        tabla = Table(data=datos, colWidths=[87.5, 87.5, 87.5, 87.5, 87.5, 87.5])
                else:
                    datos.append([Paragraph('%Amortiz. Ant.: ' + str(orden_servicio.amortizacion), tbody), Paragraph('%Retegarantia: ' + str(orden_servicio.retencion_garantia), tbody), Paragraph('Rtica: ' + str(orden_servicio.rete_ica), tbody), Paragraph('Rtfuente: ' + str(orden_servicio.rete_fuente), tbody)])
                    tabla = Table(data=datos, colWidths=[131.25, 131.25, 131.25, 131.25])
                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])
                tabla.setStyle(estilo_tabla)
                story.append(tabla)

                #Informacion de la cooperativa
                if orden_servicio.aplica_cooperativa:
                    datos = []
                    datos.append([Paragraph('Aplica cooperativa: ' + aplica_cooperativa, tbody), Paragraph('%Base gravable: ' + str(orden_servicio.base_gravable_cooperativa), tbody), Paragraph('%IVA: ' + str(orden_servicio.porcentaje_iva_cooperativa), tbody), Paragraph('', tbody)])
                    tabla = Table(data=datos, colWidths=[131.25, 131.25, 131.25, 131.25])
                    estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])
                    tabla.setStyle(estilo_tabla)
                    story.append(tabla)

                story.append(Spacer(0,10))

                #donde textox_bd es el texto que proviene directamente de la BD
                datos = []

                #Datos de cabecera de la tabla
                cabecera = [Paragraph(str('No.'), thead), Paragraph(str('DESCRIPCION'), thead), Paragraph(str('CANT.'), thead), Paragraph(str('UNIDAD'), thead), Paragraph(str('VALOR UNITARIO'), thead), Paragraph(str('VALOR ITEM'), thead)]

                datos.append(cabecera)

                #Datos cuerpo de la tabla
                indice = 1
                for suministro in suministros:
                    datos.append([Paragraph(str(indice), thead), Paragraph(unicode(suministro.suministro.suministro.suministro.nombre), tbody), Paragraph(str(intcomma(suministro.cantidad)), tbody_ajustar_derecha), Paragraph(suministro.suministro.suministro.suministro.unidad_medida, thead), Paragraph(str(intcomma(suministro.suministro_orden_servicio_item.precio)), tbody_ajustar_derecha), Paragraph(str(intcomma(round(suministro.cantidad * suministro.suministro_orden_servicio_item.precio, 2))), tbody_ajustar_derecha)])
                    indice = indice + 1

                tabla = Table(data=datos, colWidths=[24, 293, 42, 42, 58, 66])


                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.black),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                #tabla.wrap(400, None)

                story.append(tabla)

                story.append(Spacer(0,10))

                datos = []

                #Contenido1 = forma de pago, valor en letras
                contenido1 = []
                forma_pago = ''
                if orden_servicio.forma_pago == 1:
                    forma_pago = 'Anticipado'
                elif orden_servicio.forma_pago == 2:
                    forma_pago = 'Contra-entrega'
                elif orden_servicio.forma_pago == 3:
                    forma_pago = 'Cortes de obra'
                elif orden_servicio.forma_pago == 4:
                    forma_pago = 'Otro: ' + orden_servicio.parametro_pago
                valor = orden_servicio.str_valor_total
                valor_letras = to_word(int(valor), 'COP')
                valor_letras = 'Son: ' + valor_letras + ' con ' + str(valor).split('.')[1] + ' centavos.'
                contenido1.append([Paragraph('Forma de pago: ' + forma_pago, tbody)])
                contenido1.append([Paragraph('', tbody)])
                contenido1.append([Paragraph('', tbody)])
                contenido1.append([Paragraph(valor_letras, tbody)])
                #tabla_contenido1 sin estilo para que no se vean los bordes
                tabla_contenido1 = Table(data=contenido1, colWidths=[360])
                estilo_tabla = TableStyle([('LINEABOVE', (0,0),(-1,-1),0.25, colors.black),
                                                       ('LINEABOVE',(0,0),(-1,-1),0.25, colors.black),])
                #tabla_contenido1.setStyle(estilo_tabla)

                #Contenido2 = valor total sin iva, valor del iva, valor total
                contenido2 = []

                if orden_servicio.tipo_iva != None:
                    if orden_servicio.tipo_iva == 1:
                        contenido2.append([Paragraph('<b>Costo directo: </b>', tbody_ajustar_derecha), Paragraph(str(intcomma(orden_servicio.str_valor_costo_directo)), tbody_ajustar_derecha)])
                        contenido2.append([Paragraph('<b>AIU: </b>', tbody_ajustar_derecha), Paragraph(str(intcomma(orden_servicio.str_valor_aiu)), tbody_ajustar_derecha)])
                        contenido2.append([Paragraph('<b>Subtotal: </b>', tbody_ajustar_derecha), Paragraph(str(intcomma(orden_servicio.str_valor_subtotal)), tbody_ajustar_derecha)])
                        contenido2.append([Paragraph('<b>Valor IVA: </b>', tbody_ajustar_derecha), Paragraph(str(intcomma(orden_servicio.str_valor_iva)), tbody_ajustar_derecha)])
                        contenido2.append([Paragraph('<b>Valor total: </b>', tbody_ajustar_derecha), Paragraph(str(intcomma(orden_servicio.str_valor_total)), tbody_ajustar_derecha)])
                    if orden_servicio.tipo_iva == 2:
                        contenido2.append([Paragraph('<b>Subtotal: </b>', tbody_ajustar_derecha), Paragraph(str(intcomma(orden_servicio.str_valor_subtotal)), tbody_ajustar_derecha)])
                        contenido2.append([Paragraph('<b>Valor IVA: </b>', tbody_ajustar_derecha), Paragraph(str(intcomma(orden_servicio.str_valor_iva)), tbody_ajustar_derecha)])
                        contenido2.append([Paragraph('<b>Valor total: </b>', tbody_ajustar_derecha), Paragraph(str(intcomma(orden_servicio.str_valor_total)), tbody_ajustar_derecha)])
                    if orden_servicio.tipo_iva == 3:
                        contenido2.append([Paragraph('<b>Costo directo: </b>', tbody_ajustar_derecha), Paragraph(str(intcomma(orden_servicio.str_valor_costo_directo)), tbody_ajustar_derecha)])
                        contenido2.append([Paragraph('<b>AIU: </b>', tbody_ajustar_derecha), Paragraph(str(intcomma(orden_servicio.str_valor_aiu)), tbody_ajustar_derecha)])
                        contenido2.append([Paragraph('<b>Subtotal: </b>', tbody_ajustar_derecha), Paragraph(str(intcomma(orden_servicio.str_valor_subtotal)), tbody_ajustar_derecha)])
                        contenido2.append([Paragraph('<b>Valor IVA: </b>', tbody_ajustar_derecha), Paragraph(str(intcomma(orden_servicio.str_valor_iva)), tbody_ajustar_derecha)])
                        contenido2.append([Paragraph('<b>Valor total: </b>', tbody_ajustar_derecha), Paragraph(str(intcomma(orden_servicio.str_valor_total)), tbody_ajustar_derecha)])
                else:
                    contenido2.append([Paragraph('<b>Subtotal: </b>', tbody_ajustar_derecha), Paragraph(str(intcomma(orden_servicio.str_valor_subtotal)), tbody_ajustar_derecha)])
                    contenido2.append([Paragraph('<b>Total: </b>', tbody_ajustar_derecha), Paragraph(str(intcomma(orden_servicio.str_valor_total)), tbody_ajustar_derecha)])

                tabla_contenido2 = Table(data=contenido2, colWidths=[60, 80])

                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.black),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])
                tabla_contenido2.setStyle(estilo_tabla)

                datos.append([tabla_contenido1, tabla_contenido2])


                tabla = Table(data=datos, colWidths=[370, 155])

                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.black),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                story.append(tabla)

                story.append(Spacer(0,10))

                #Observaciones de la orden de servicio
                datos = []

                datos.append([Paragraph('Observaciones: ' + unicode(orden_servicio.observaciones), tbody)])

                tabla = Table(data=datos, colWidths=[525])

                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.black),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                story.append(tabla)

                story.append(Spacer(0,5))

                #Firmas de autorización
                datos = []
                datos.append([Paragraph('', thead), Paragraph('', thead)])
                datos.append([Paragraph('', thead), Paragraph('', thead)])
                datos.append([Paragraph('____________________________________', thead), Paragraph('____________________________________', thead)])
                datos.append([Paragraph(unicode(orden_servicio.persona.first_name).upper() + ' ' + unicode(orden_servicio.persona.last_name).upper(), thead), Paragraph(unicode(orden_servicio.proveedor.razon_social.upper()), thead)])
                datos.append([Paragraph(unicode(orden_servicio.persona.cargo).upper(), thead), Paragraph('CONTRATISTA', thead)])
                tabla = Table(data=datos, colWidths=[262.5, 262.5])
                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.white),])
                tabla.setStyle(estilo_tabla)
                story.append(tabla)

                story.append(Spacer(0,5))

                #Firma persona elaboró
                story.append(Paragraph(u'Registró: ' + unicode(orden_servicio.persona.first_name).upper() + ' ' + unicode(orden_servicio.persona.last_name).upper() + ', ' + unicode(orden_servicio.persona.cargo), tregistro))

                # Creamos el objeto HttpResponse con los headers apropiados para PDF.
                response = HttpResponse(mimetype='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=ordenservicio.pdf'

                #Creamos un DocTemplate en una hoja DIN letter, en la que se muestra el texto enmarcado (showBoundary=1) por un recuadro.
                doc=SimpleDocTemplate(response, pagesize=letter, topMargin=16, leftMargin=15, rightMargin=15, bottomMargin=5)

                #Construimos el Platypus story.

                doc.build(story, canvasmaker=NumberedCanvas)
                #doc.build(story)

                return response
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def pdf_orden_giro(request, orden_giro_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_ordengiro' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                orden_giro = proyecto.ordengiro_set.get(id=orden_giro_id)

                items_orden_giro = orden_giro.itemordengiro_set.all()

                #Obtenemos de platypus las clases Paragraph, para escribir párrafos Image, para insertar imágenes y SimpleDocTemplate para definir el DocTemplate. Además importamos Spacer, para incluir espacios .
                from reportlab.platypus import Paragraph, Table
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
                from reportlab.platypus import Spacer

                #Importamos clase de hoja de estilo de ejemplo.
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

                #Se importa el tamaño de la hoja.
                from reportlab.lib.pagesizes import letter

                #Y los colores.
                from reportlab.lib import colors

                #Creamos un PageTemplate de ejemplo.
                estiloHoja = getSampleStyleSheet()

                #Font texto
                from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY

                #Inicializamos la lista Platypus Story.
                story = []

                #Definimos el rotulo.
                fichero_imagen = "rotuloordengiro.jpg"
                rotulo = generar_rotulo(fichero_imagen, 525, 70)
                story.append(rotulo)

                story.append(Spacer(0,10))

                #Estilos de la tabla para cabeceras
                especificaciones = {'name': 'cabeceraTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_CENTER, 'borderRadius': 0.5}
                thead = generar_estilo(especificaciones)

                #Estilos de la tabla para datos
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_JUSTIFY, 'borderRadius': 0.5}
                tbody = generar_estilo(especificaciones)
                #Ajustar a la izquierda
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_LEFT, 'borderRadius': 0.5}
                tbody_ajustar_izquierda = generar_estilo(especificaciones)
                #Ajustar a la derecha
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_RIGHT, 'borderRadius': 0.5}
                tbody_ajustar_derecha = generar_estilo(especificaciones)

                #Estilo para registro
                especificaciones = {'name': 'cabeceraTabla', 'fontSize': 6, 'leading': 8, 'alignment': TA_LEFT, 'borderRadius': 0.5}
                tregistro = generar_estilo(especificaciones)

                datos = []

                datos.append([Paragraph('PROVEEDOR: ' + unicode(orden_giro.proveedor.razon_social), tbody), Paragraph('NIT: ' + str(orden_giro.proveedor.identificacion), tbody)])
                datos.append([Paragraph('TELEFONO: ' + orden_giro.proveedor.telefono_1, tbody), Paragraph('E-MAIL: ' + orden_giro.proveedor.email, tbody)])

                tabla = Table(data=datos, colWidths=[262.5, 262.5])

                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                story.append(tabla)

                story.append(Spacer(0,10))

                story.append(Paragraph('Con la presente orden de giro queda autorizado para ejecutar las siguientes actividades', thead))

                story.append(Spacer(0,10))

                datos = []

                datos.append([Paragraph('<b>ORDEN DE GIRO No.: OG' + str(proyecto.id) + ' - ' + str(orden_giro.consecutivo) + '</b>', tbody), Paragraph('FECHA DE REGISTRO: ' + str(orden_giro.fecha_registro.date()), tbody)])
                datos.append([Paragraph('PROYECTO: ' + unicode(orden_giro.proyecto.nombre), tbody), Paragraph('CIUDAD: ' + unicode(orden_giro.proyecto.municipio.nombre) + ', ' + unicode(orden_giro.proyecto.municipio.departamento.nombre), tbody)])
                datos.append([Paragraph('DIRECCION: ' + unicode(orden_giro.proyecto.direccion), tbody), Paragraph('', tbody)])

                tabla = Table(data=datos, colWidths=[262.5, 262.5])

                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                story.append(tabla)

                story.append(Spacer(0,10))

                #donde textox_bd es el texto que proviene directamente de la BD
                datos = []

                #Datos de cabecera de la tabla
                cabecera = [Paragraph(str('No.'), thead), Paragraph(str('DESCRIPCION'), thead), Paragraph(str('VALOR ITEM'), thead)]

                datos.append(cabecera)

                #Datos cuerpo de la tabla
                indice = 1
                for item_orden_giro in items_orden_giro:
                    datos.append([Paragraph(str(indice), thead), Paragraph(unicode(item_orden_giro.descripcion), tbody), Paragraph(str(intcomma(item_orden_giro.valor)), tbody_ajustar_derecha)])
                    indice = indice + 1

                tabla = Table(data=datos, colWidths=[24, 401, 100])


                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.black),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                #tabla.wrap(400, None)

                story.append(tabla)

                story.append(Spacer(0,15))

                datos = []

                #Datos cuerpo de la tabla
                datos.append([Paragraph('Valor total', tbody_ajustar_derecha), Paragraph(str(intcomma(orden_giro.valor_total())), tbody_ajustar_derecha)])

                tabla = Table(data=datos, colWidths=[425, 100])


                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.white),])

                tabla.setStyle(estilo_tabla)

                #tabla.wrap(400, None)

                story.append(tabla)

                story.append(Spacer(0,15))

                #Firmas de autorización
                datos = []
                datos.append([Paragraph('', thead), Paragraph('', thead)])
                datos.append([Paragraph('', thead), Paragraph('', thead)])
                datos.append([Paragraph('____________________________________', thead), Paragraph('____________________________________', thead)])
                datos.append([Paragraph(unicode(orden_giro.persona.first_name).upper() + ' ' + unicode(orden_giro.persona.last_name).upper(), thead), Paragraph(unicode(orden_giro.proveedor.razon_social.upper()), thead)])
                datos.append([Paragraph(unicode(orden_giro.persona.cargo).upper(), thead), Paragraph('PROVEEDOR', thead)])
                tabla = Table(data=datos, colWidths=[262.5, 262.5])
                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.white),])
                tabla.setStyle(estilo_tabla)
                story.append(tabla)

                story.append(Spacer(0,5))

                #Firma persona elaboró
                story.append(Paragraph(u'Registró: ' + unicode(orden_giro.persona.first_name).upper() + ' ' + unicode(orden_giro.persona.last_name).upper() + ', ' + unicode(orden_giro.persona.cargo), tregistro))

                # Creamos el objeto HttpResponse con los headers apropiados para PDF.
                response = HttpResponse(mimetype='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=ordengiro.pdf'

                #Creamos un DocTemplate en una hoja DIN letter, en la que se muestra el texto enmarcado (showBoundary=1) por un recuadro.
                doc=SimpleDocTemplate(response, pagesize=letter, topMargin=16, leftMargin=15, rightMargin=15, bottomMargin=5)

                #Construimos el Platypus story.

                doc.build(story, canvasmaker=NumberedCanvas)
                #doc.build(story)

                return response

        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def pdf_acta_conformidad(request, acta_conformidad_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_actaconformidad' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                acta_conformidad = ActaConformidad.objects.get(id=acta_conformidad_id, orden_giro__proyecto=proyecto)
                items_acta_conformidad = acta_conformidad.itemactaconformidad_set.all()

                #Obtenemos de platypus las clases Paragraph, para escribir párrafos Image, para insertar imágenes y SimpleDocTemplate para definir el DocTemplate. Además importamos Spacer, para incluir espacios .
                from reportlab.platypus import Paragraph, Table
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
                from reportlab.platypus import Spacer

                #Importamos clase de hoja de estilo de ejemplo.
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

                #Se importa el tamaño de la hoja.
                from reportlab.lib.pagesizes import letter

                #Y los colores.
                from reportlab.lib import colors

                #Creamos un PageTemplate de ejemplo.
                estiloHoja = getSampleStyleSheet()

                #Font texto
                from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY

                #Inicializamos la lista Platypus Story.
                story = []

                #Definimos el rotulo.
                #-----
                """
                fichero_imagen = "rotuloactaconformidad.jpg"
                rotulo = generar_rotulo(fichero_imagen, 525, 70)
                story.append(rotulo)
                """
                #-----

                story.append(Spacer(0,10))

                #Estilos de la tabla para cabeceras
                especificaciones = {'name': 'cabeceraTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_CENTER, 'borderRadius': 0.5}
                thead = generar_estilo(especificaciones)

                #Estilos de la tabla para datos
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_JUSTIFY, 'borderRadius': 0.5}
                tbody = generar_estilo(especificaciones)
                #Ajustar a la izquierda
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_LEFT, 'borderRadius': 0.5}
                tbody_ajustar_izquierda = generar_estilo(especificaciones)
                #Ajustar a la derecha
                especificaciones = {'name': 'datosTabla', 'fontSize': 8, 'leading': 8, 'alignment': TA_RIGHT, 'borderRadius': 0.5}
                tbody_ajustar_derecha = generar_estilo(especificaciones)

                #Estilo para registro
                especificaciones = {'name': 'cabeceraTabla', 'fontSize': 6, 'leading': 8, 'alignment': TA_LEFT, 'borderRadius': 0.5}
                tregistro = generar_estilo(especificaciones)

                datos = []

                datos.append([Paragraph('PROVEEDOR: ' + unicode(acta_conformidad.orden_giro.proveedor.razon_social), tbody), Paragraph('NIT: ' + str(acta_conformidad.orden_giro.proveedor.identificacion), tbody)])
                datos.append([Paragraph('TELEFONO: ' + acta_conformidad.orden_giro.proveedor.telefono_1, tbody), Paragraph('E-MAIL: ' + acta_conformidad.orden_giro.proveedor.email, tbody)])

                tabla = Table(data=datos, colWidths=[262.5, 262.5])

                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                story.append(tabla)

                story.append(Spacer(0,10))

                datos = []

                datos.append([Paragraph('<b>ACTA DE CONFORMIDAD No.: AC' + str(proyecto.id) + ' - ' + str(acta_conformidad.consecutivo) + '</b>', tbody), Paragraph('FECHA DE REGISTRO: ' + str(acta_conformidad.fecha_registro) + '</b>', tbody)])
                datos.append([Paragraph('<b>ORDEN DE GIRO No.: OG' + str(proyecto.id) + ' - ' + str(acta_conformidad.orden_giro.consecutivo) + '</b>', tbody), Paragraph('', tbody)])
                datos.append([Paragraph('PROYECTO: ' + unicode(acta_conformidad.orden_giro.proyecto.nombre), tbody), Paragraph('CIUDAD: ' + unicode(acta_conformidad.orden_giro.proyecto.municipio.nombre) + ', ' + unicode(acta_conformidad.orden_giro.proyecto.municipio.departamento.nombre), tbody)])
                datos.append([Paragraph('DIRECCION: ' + unicode(acta_conformidad.orden_giro.proyecto.direccion), tbody), Paragraph('', tbody)])

                tabla = Table(data=datos, colWidths=[262.5, 262.5])

                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])

                tabla.setStyle(estilo_tabla)

                story.append(tabla)

                story.append(Spacer(0,10))

                #donde textox_bd es el texto que proviene directamente de la BD
                datos_tabla_global = []
                datos_tabla_1 = []
                datos_tabla_2 = []

                #Datos de cabecera de la tabla

                #Tabla_global
                cabecera_tabla_global = [Paragraph(str(u'CONDICIONES ORIGINALES'), thead), Paragraph(str(u'ACTA ACTUAL'), thead)]
                                
                #Tabla_1
                cabecera_tabla_1 = [Paragraph(str('No.'), thead), Paragraph(str('DESCRIPCION'), thead), Paragraph(str('VALOR ITEM'), thead)]

                #Tabla_2
                cabecera_tabla_2 = [Paragraph(str('VALOR ITEM'), thead)]


                datos_tabla_global.append(cabecera_tabla_global)

                datos_tabla_1.append(cabecera_tabla_1)

                datos_tabla_2.append(cabecera_tabla_2)

                #Datos cuerpo de la tabla
                indice = 1
                for item_acta_conformidad in items_acta_conformidad:
                    datos_tabla_1.append([Paragraph(str(indice), thead), Paragraph(unicode(item_acta_conformidad.item_orden_giro.descripcion), tbody), Paragraph(str(intcomma(item_acta_conformidad.item_orden_giro.valor)), tbody_ajustar_derecha)])
                    datos_tabla_2.append([Paragraph(str(intcomma(item_acta_conformidad.valor)), tbody_ajustar_derecha)])

                    indice = indice + 1

                tabla_1 = Table(data=datos_tabla_1, colWidths=[24, 280, 100])
                estilo_tabla_1 = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.black),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])
                tabla_1.setStyle(estilo_tabla_1)


                tabla_2 = Table(data=datos_tabla_2, colWidths=[100])
                estilo_tabla_2 = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.black),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])
                tabla_2.setStyle(estilo_tabla_2)

                datos_tabla_global.append([tabla_1, tabla_2])

                tabla_global = Table(data=datos_tabla_global, colWidths=[415, 110])

                story.append(tabla_global)

                story.append(Spacer(0,5))

                datos = []

                datos.append([Paragraph('Valor total:', tbody_ajustar_derecha), Paragraph(str(intcomma(acta_conformidad.valor_total())), tbody_ajustar_derecha)])

                tabla = Table(data=datos, colWidths=[100, 100])
                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.black),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.black),])
                tabla.setStyle(estilo_tabla)

                story.append(tabla)

                story.append(Spacer(0,10))

                #Firmas de autorización
                datos = []
                datos.append([Paragraph('', thead), Paragraph('', thead)])
                datos.append([Paragraph('', thead), Paragraph('', thead)])
                datos.append([Paragraph('____________________________________', thead), Paragraph('____________________________________', thead)])
                datos.append([Paragraph(unicode(acta_conformidad.persona.first_name).upper() + ' ' + unicode(acta_conformidad.persona.last_name).upper(), thead), Paragraph(unicode(acta_conformidad.orden_giro.proveedor.razon_social.upper()), thead)])
                datos.append([Paragraph(unicode(acta_conformidad.persona.cargo).upper(), thead), Paragraph('PROVEEDOR', thead)])
                tabla = Table(data=datos, colWidths=[262.5, 262.5])
                estilo_tabla = TableStyle([('GRID', (0,0),(-1,-1),0.25, colors.white),
                                                       ('BOX',(0,0),(-1,-1),0.25, colors.white),])
                tabla.setStyle(estilo_tabla)
                story.append(tabla)

                story.append(Spacer(0,5))

                #Firma persona elaboró
                story.append(Paragraph(u'Registró: ' + unicode(acta_conformidad.persona.first_name).upper() + ' ' + unicode(acta_conformidad.persona.last_name).upper() + ', ' + unicode(acta_conformidad.persona.cargo), tregistro))

                # Creamos el objeto HttpResponse con los headers apropiados para PDF.
                response = HttpResponse(mimetype='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=actaconformidad.pdf'

                #Creamos un DocTemplate en una hoja DIN letter, en la que se muestra el texto enmarcado (showBoundary=1) por un recuadro.
                doc=SimpleDocTemplate(response, pagesize=letter, topMargin=16, leftMargin=15, rightMargin=15, bottomMargin=5)

                #Construimos el Platypus story.

                doc.build(story, canvasmaker=NumberedCanvas)
                #doc.build(story)

                return response

        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')



def pdf_nuevo_acta_conformidad(request, acta_conformidad_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_actareciboobra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                acta_conformidad = ActaConformidad.objects.get(id=acta_conformidad_id, orden_giro__proyecto=proyecto)
                items = acta_conformidad.itemactaconformidad_set.all()
                imagen_cabecera = 'pdfs/rotuloactaconformidad.jpg'
                html = render_to_string('pdfactaconformidad.html', {'pagesize': 'letter', 'orientation': 'portrait', 'margin': '1cm', 'imagen_cabecera': imagen_cabecera, 'acta_conformidad': acta_conformidad, 'proyecto': proyecto, 'items': items}, context_instance=RequestContext(request))
                return generar_pdf(html, acta_conformidad_id)
                    #return render_to_pdf('pdffacturaordencompra.html', {'user': user, 'factura_orden_compra': factura, 'items_factura': items_factura, 'valor_discriminado_capitulos': valor_discriminado_capitulos, 'valor_factura_sin_iva': valor_factura_sin_iva, 'valor_iva_factura': valor_iva_factura, 'valor_total_factura': valor_total_factura, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')



def pdf_factura_orden_compra(request, factura_orden_compra_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        existen_subcapitulos = False
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_facturaordencompra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                factura = proyecto.facturaordencompra_set.get(id=factura_orden_compra_id)
                items_factura = factura.itemfacturaordencompra_set.all()

                #Calculo de valores por discriminacion de orden de compra
                valor_discriminado_ordenes_compra = []

                #Calculo de valores por discriminación de clasificación (capitulos)
                valor_discriminado_capitulos = []
                valor_factura_sin_iva = 0
                valor_iva_factura = 0
                valor_total_factura = 0
                for item_factura in items_factura:
                    for suministro_item_factura in item_factura.suministrofacturaordencompra_set.all():
                        existe_capitulo = False
                        for item in valor_discriminado_capitulos:
                            if suministro_item_factura.suministro_informe_recepcion.suministro.suministro.suministro.apu_proyecto.capitulo.id == item['capitulo'].id:
                                valor_sin_iva = round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2)
                                valor_iva = round(round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2) * suministro_item_factura.item_factura_orden_compra.porcentaje_iva(), 2)
                                valor_con_iva = round(valor_sin_iva + valor_iva, 2)
                                item['valor_sin_iva'] = round(item['valor_sin_iva'] + valor_sin_iva, 2)
                                item['valor_iva'] = round(item['valor_iva'] + valor_iva, 2)
                                item['valor_con_iva'] = round(item['valor_con_iva'] + valor_con_iva, 2)
                                valor_factura_sin_iva = round(valor_factura_sin_iva + valor_sin_iva, 2)
                                valor_iva_factura = round(valor_iva_factura + valor_iva, 2)
                                valor_total_factura = round(valor_total_factura + valor_con_iva, 2)
                                existe_capitulo = True
                        if existe_capitulo == False:
                            valor_sin_iva = round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2)
                            valor_iva = round(round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2) * suministro_item_factura.item_factura_orden_compra.porcentaje_iva(), 2)
                            valor_con_iva = round(valor_sin_iva + valor_iva, 2)
                            valor_discriminado_capitulos.append({'capitulo': suministro_item_factura.suministro_informe_recepcion.suministro.suministro.suministro.apu_proyecto.capitulo, 'valor_sin_iva': valor_sin_iva, 'valor_iva': valor_iva, 'valor_con_iva': valor_con_iva})
                            valor_factura_sin_iva = round(valor_factura_sin_iva + valor_sin_iva, 2)
                            valor_iva_factura = round(valor_iva_factura + valor_iva, 2)
                            valor_total_factura = round(valor_total_factura + valor_con_iva, 2)

                #Calculo de valores por discriminación de clasificación (subcapitulos)
                valor_discriminado_subcapitulos = []
                valor_factura_sin_iva = 0
                valor_iva_factura = 0
                valor_total_factura = 0
                capitulo_asociado = ''

                for item_factura in items_factura:
                    suministros_item_factura = item_factura.suministrofacturaordencompra_set.all().order_by('suministro_informe_recepcion__informe_recepcion__orden_compra__consecutivo')
                    for suministro_item_factura in suministros_item_factura:
                        existe_capitulo = False
                        for item in valor_discriminado_subcapitulos:
                            capitulo = item['capitulo']
                            if item['capitulo'].tipo_capitulo == 2:
                                capitulo = item['capitulo']
                                capitulo_asociado = item['capitulo'].capitulo_asociado
                                existen_subcapitulos = True
                            if (suministro_item_factura.suministro_informe_recepcion.suministro.suministro.suministro.apu_proyecto.capitulo.id == capitulo.id) or (suministro_item_factura.suministro_informe_recepcion.suministro.suministro.suministro.apu_proyecto.capitulo.tipo_capitulo == 2 and suministro_item_factura.suministro_informe_recepcion.suministro.suministro.suministro.apu_proyecto.capitulo.capitulo_asociado.id == capitulo.id):
                                valor_sin_iva = round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2)
                                valor_iva = round(round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2) * suministro_item_factura.item_factura_orden_compra.porcentaje_iva(), 2)
                                valor_con_iva = round(valor_sin_iva + valor_iva, 2)
                                item['valor_sin_iva'] = round(item['valor_sin_iva'] + valor_sin_iva, 2)
                                item['valor_iva'] = round(item['valor_iva'] + valor_iva, 2)
                                item['valor_con_iva'] = round(item['valor_con_iva'] + valor_con_iva, 2)
                                valor_factura_sin_iva = round(valor_factura_sin_iva + valor_sin_iva, 2)
                                valor_iva_factura = round(valor_iva_factura + valor_iva, 2)
                                valor_total_factura = round(valor_total_factura + valor_con_iva, 2)
                                existe_capitulo = True
                        if existe_capitulo == False:
                            valor_sin_iva = round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2)
                            valor_iva = round(round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2) * suministro_item_factura.item_factura_orden_compra.porcentaje_iva(), 2)
                            valor_con_iva = round(valor_sin_iva + valor_iva, 2)
                            valor_discriminado_subcapitulos.append({'capitulo': suministro_item_factura.suministro_informe_recepcion.suministro.suministro.suministro.apu_proyecto.capitulo, 'capitulo_asociado': capitulo_asociado, 'valor_sin_iva': valor_sin_iva, 'valor_iva': valor_iva, 'valor_con_iva': valor_con_iva})
                            valor_factura_sin_iva = round(valor_factura_sin_iva + valor_sin_iva, 2)
                            valor_iva_factura = round(valor_iva_factura + valor_iva, 2)
                            valor_total_factura = round(valor_total_factura + valor_con_iva, 2)
                        
                        #Calculo de valores por discriminación de orden de compra
                        existe_orden_compra = False
                        for item in valor_discriminado_ordenes_compra:
                            if item['orden_compra'].id == suministro_item_factura.suministro_informe_recepcion.informe_recepcion.orden_compra.id:
                                existe_orden_compra = True
                                existe_suministro_orden_compra = False
                                for suministro in item['suministros']:
                                    if suministro_item_factura.item_factura_orden_compra.suministro.id == suministro['suministro'].id:
                                        existe_suministro_orden_compra = True
                                        valor_sin_iva = round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2)
                                        valor_iva = round(round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2) * suministro_item_factura.item_factura_orden_compra.porcentaje_iva(), 2)
                                        valor_con_iva = round(valor_sin_iva + valor_iva, 2)

                                        suministro['cantidad'] = round(suministro['cantidad'] + suministro_item_factura.cantidad, 2)
                                        suministro['valor_sin_iva'] = round(suministro['valor_sin_iva'] + valor_sin_iva, 2)
                                        suministro['valor_iva'] = round(suministro['valor_iva'] + valor_iva, 2)
                                        suministro['valor_con_iva'] = round(suministro['valor_con_iva'] + valor_con_iva, 2)

                                        item['valor_sin_iva'] = round(item['valor_sin_iva'] + valor_sin_iva, 2)
                                        item['valor_iva'] = round(item['valor_iva'] + valor_iva, 2)
                                        item['valor_con_iva'] = round(item['valor_con_iva'] + valor_con_iva, 2)

                                if existe_suministro_orden_compra == False:
                                    valor_sin_iva = round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2)
                                    valor_iva = round(round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2) * suministro_item_factura.item_factura_orden_compra.porcentaje_iva(), 2)
                                    valor_con_iva = round(valor_sin_iva + valor_iva, 2)
                                    item['suministros'].append({'suministro': suministro_item_factura.item_factura_orden_compra.suministro, 'cantidad': suministro_item_factura.cantidad, 'valor_sin_iva': valor_sin_iva, 'valor_iva': valor_iva, 'valor_con_iva': valor_con_iva})

                                    item['valor_sin_iva'] = round(item['valor_sin_iva'] + valor_sin_iva, 2)
                                    item['valor_iva'] = round(item['valor_iva'] + valor_iva, 2)
                                    item['valor_con_iva'] = round(item['valor_con_iva'] + valor_con_iva, 2)
                        if existe_orden_compra == False:
                            valor_sin_iva = round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2)
                            valor_iva = round(round(suministro_item_factura.cantidad * suministro_item_factura.item_factura_orden_compra.valor_unitario_item_sin_iva(), 2) * suministro_item_factura.item_factura_orden_compra.porcentaje_iva(), 2)
                            valor_con_iva = round(valor_sin_iva + valor_iva, 2)
                            valor_discriminado_ordenes_compra.append({'orden_compra': suministro_item_factura.suministro_informe_recepcion.informe_recepcion.orden_compra, 'suministros': [{'suministro': suministro_item_factura.item_factura_orden_compra.suministro, 'cantidad': suministro_item_factura.cantidad, 'valor_sin_iva': valor_sin_iva, 'valor_iva': valor_iva, 'valor_con_iva': valor_con_iva}], 'valor_sin_iva': valor_sin_iva, 'valor_iva': valor_iva, 'valor_con_iva': valor_con_iva})

                imagen_cabecera = 'pdfs/rotulofacturaordencompra.jpg'
                html = render_to_string('pdffacturaordencompra.html', {'pagesize': 'letter', 'orientation': 'portrait', 'margin': '1cm', 'imagen_cabecera': imagen_cabecera, 'factura_orden_compra': factura, 'items_factura': items_factura, 'valor_discriminado_capitulos': valor_discriminado_capitulos, 'valor_discriminado_subcapitulos': valor_discriminado_subcapitulos, 'valor_discriminado_ordenes_compra': valor_discriminado_ordenes_compra, 'valor_factura_sin_iva': valor_factura_sin_iva, 'valor_iva_factura': valor_iva_factura, 'valor_total_factura': valor_total_factura, 'proyecto': proyecto, 'existen_subcapitulos': existen_subcapitulos}, context_instance=RequestContext(request))
                return generar_pdf(html, factura_orden_compra_id)
                #return render_to_pdf('pdffacturaordencompra.html', {'user': user, 'factura_orden_compra': factura, 'items_factura': items_factura, 'valor_discriminado_capitulos': valor_discriminado_capitulos, 'valor_factura_sin_iva': valor_factura_sin_iva, 'valor_iva_factura': valor_iva_factura, 'valor_total_factura': valor_total_factura, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def pdf_acta_recibo_obra_proveedor(request, acta_recibo_obra_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_actareciboobra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                acta_recibo_obra = ActaReciboObra.objects.get(id=acta_recibo_obra_id, orden_servicio__proyecto=proyecto)
                if acta_recibo_obra.permite_imprimir():
                    acta_recibo_obra.calcular_valores()
                    imagen_cabecera = 'pdfs/rotuloactareciboobra.jpg'
                    html = render_to_string('pdfactareciboobraproveedor.html', {'pagesize': 'letter', 'orientation': 'portrait', 'margin': '1cm', 'imagen_cabecera': imagen_cabecera, 'acta_recibo_obra': acta_recibo_obra, 'proyecto': proyecto}, context_instance=RequestContext(request))
                    return generar_pdf(html, acta_recibo_obra_id)
                    #return render_to_pdf('pdffacturaordencompra.html', {'user': user, 'factura_orden_compra': factura, 'items_factura': items_factura, 'valor_discriminado_capitulos': valor_discriminado_capitulos, 'valor_factura_sin_iva': valor_factura_sin_iva, 'valor_iva_factura': valor_iva_factura, 'valor_total_factura': valor_total_factura, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


def pdf_acta_recibo_obra_contabilidad(request, acta_recibo_obra_id, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_actareciboobra' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                acta_recibo_obra = ActaReciboObra.objects.get(id=acta_recibo_obra_id, orden_servicio__proyecto=proyecto)
                if acta_recibo_obra.permite_imprimir():
                    acta_recibo_obra.calcular_valores(opcion_discriminacion_capitulos=True, opcion_discriminacion_subcapitulos=True)
                    imagen_cabecera = 'pdfs/rotuloactareciboobra.jpg'
                    html = render_to_string('pdfactareciboobracontabilidad.html', {'pagesize': 'letter', 'orientation': 'portrait', 'margin': '1cm', 'imagen_cabecera': imagen_cabecera, 'acta_recibo_obra': acta_recibo_obra, 'proyecto': proyecto}, context_instance=RequestContext(request))
                    return generar_pdf(html, acta_recibo_obra_id)
                    #return render_to_pdf('pdffacturaordencompra.html', {'user': user, 'factura_orden_compra': factura, 'items_factura': items_factura, 'valor_discriminado_capitulos': valor_discriminado_capitulos, 'valor_factura_sin_iva': valor_factura_sin_iva, 'valor_iva_factura': valor_iva_factura, 'valor_total_factura': valor_total_factura, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


"""
def orden_trabajo_pdf(request, id):
    orden=get_object_or_404(OrdenTrabajo, id=id)
    html = render_to_string('orden_trabajo_pdf.html',
        {'pagesize':'letter', 'orden':orden},
        context_instance=RequestContext(request))
    return generar_pdf(html, id)
"""


def myFirstPage(canvas, doc):
            canvas.saveState()
            canvas.rotate(90)
            canvas.restoreState()


def myLaterPages(canvas, doc):
            canvas.saveState()
            canvas.rotate(90)
            canvas.restoreState()


from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.platypus import Paragraph, Image, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import Indenter
from reportlab.platypus.flowables import KeepTogether, Flowable, ParagraphAndImage
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER, landscape, portrait, cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib import colors

import cStringIO as StringIO
#import ho.pisa as pisa
import cgi
#import historico
import csv
import re


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 6)
        self.drawRightString(210*mm, 272*mm,
			"Página %d de %d" % (self._pageNumber, page_count))



#### Libreria para convertir numeros a letras
#! /usr/bin/env python
# -*- coding: utf-8 -*-
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