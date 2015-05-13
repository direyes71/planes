# -*- encoding: utf-8 -*-

from funciones_views import *
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse
from inverboy.forms import *
## PAGINACION
from inverboy.paginator import *
## MANEJO DE ERRORES MANUALMENTE
from django.forms.util import ErrorList
## CONSULTAS ANIDADAS
from django.db.models import Q
from settings import TIEMPO_INACTIVIDAD

from django.db.models import Sum, Max

#-----------------------------------------------------------Clasificación de Apu proyecto--------------------------------------------------------------------

#ACrear capitulo APU proyecto
def capitulo_apu_proyecto_add(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_capituloapuproyecto' in user.get_all_permissions():
            try:
                proyecto = Proyecto.objects.get(id=proyecto_id)
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
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
                        if capitulos_apu_proyecto.filter(Q(nombre_capitulo__iexact=form.cleaned_data['nombre'].strip())):
                            form._errors["nombre"] = ErrorList([u"El nombre ya se encuentra asignado a un capitulo del proyecto."])
                            capitulo_apu_existe = True
                        if capitulo_apu_existe == False:
                            capitulo = CapituloApuProyecto()
                            capitulo.codigo = form.cleaned_data['codigo']
                            capitulo.nombre_capitulo = form.cleaned_data['nombre'].strip()
                            capitulo.tipo_capitulo = 1
                            capitulo.estado_capitulo = 1
                            capitulo.proyecto = proyecto
                            capitulo.save()
                            direccion_ip = request.META['REMOTE_ADDR']
                            registro_historial(direccion_ip, usuario, u'Registro capitulo apu proyecto, codigo: '+str(capitulo.codigo)+", nombre: "+unicode(capitulo.nombre_capitulo)+", proyecto: "+unicode(proyecto.nombre))
                            return HttpResponseRedirect('/inverboy/home/capitulosapuproyectosearch/'+str(proyecto.id)+'/')
                return render_to_response('capituloapuproyectoadd.html', {'user': user, 'form': form, 'proyecto': proyecto, 'titulo': titulo})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar Capitulo APU proyecto
def capitulo_apu_proyecto_change(request, proyecto_id, capitulo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_capituloapuproyecto' in user.get_all_permissions():
            try:
                proyecto = Proyecto.objects.get(id=proyecto_id)
                capitulo = CapituloApuProyecto.objects.get(tipo_capitulo=1, id=capitulo_id)
                if proyecto != capitulo.proyecto:
                    return HttpResponseRedirect('/inverboy/home/')
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
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
                        nuevo_nombre = form.cleaned_data['nombre'].strip()
                        nuevo_nombre = normaliza(nuevo_nombre.lower())
                        if normaliza(capitulo.nombre_capitulo.lower()) != nuevo_nombre:
                            if capitulos_apu_proyecto.filter(Q(nombre_capitulo__iexact=form.cleaned_data['nombre'].strip())):
                                form._errors["nombre"] = ErrorList([u"El nombre ya se encuentra asignado a un capitulo del proyecto."])
                                capitulo_apu_existe = True
                        if capitulo_apu_existe == False:
                            capitulo.codigo = form.cleaned_data['codigo']
                            capitulo.nombre_capitulo = form.cleaned_data['nombre'].strip()
                            capitulo.estado_capitulo = form.cleaned_data['estado']
                            capitulo.save()
                            capitulo.apuproyecto_set.update(estado_apu=form.cleaned_data['estado'])
                            subcapitulos = CapituloApuProyecto.objects.filter(capitulo_asociado=capitulo, tipo_capitulo=2)
                            for subcapitulo in subcapitulos:
                                subcapitulo.estado_capitulo = form.cleaned_data['estado']
                                subcapitulo.save()
                                subcapitulo.apuproyecto_set.all().update(estado_apu=form.cleaned_data['estado'])
                            
                            direccion_ip = request.META['REMOTE_ADDR']
                            registro_historial(direccion_ip, usuario, u'Modifico capitulo apu proyecto, codigo: '+str(capitulo.codigo)+", nombre: "+unicode(capitulo.nombre_capitulo)+", proyecto: "+unicode(proyecto.nombre))
                            return HttpResponseRedirect('/inverboy/home/capitulosapuproyectosearch/'+str(proyecto.id)+'/')
                return render_to_response('capituloapuproyectoadd.html', {'user': user, 'form': form, 'titulo': titulo, 'proyecto': proyecto, 'change': True})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Busqueda capitulos APU proyecto
def capitulos_apu_proyecto_search(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_capituloapuproyecto' in user.get_all_permissions():
            try:
                proyecto = Proyecto.objects.get(id=proyecto_id)
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                capitulos = proyecto.capituloapuproyecto_set.filter(tipo_capitulo=1)
                try:
                    criterio = int(criterio)
                    capitulos = capitulos.filter(Q(codigo=criterio))
                except:
                    capitulos = capitulos.filter(Q(nombre_capitulo__icontains=criterio))
                pag = Paginador(request, capitulos, 20, 1)
                return render_to_response('reportecapitulosapuproyecto.html', {'user': user, 'proyecto': proyecto, 'capitulos': pag, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Crear subcapitulo APU proyecto
def subcapitulo_apu_proyecto_add(request, proyecto_id, capitulo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_capituloapuproyecto' in user.get_all_permissions():
            try:
                proyecto = Proyecto.objects.get(id=proyecto_id)
                capitulo = CapituloApuProyecto.objects.get(tipo_capitulo=1, id=capitulo_id)
                if proyecto != capitulo.proyecto:
                    return HttpResponseRedirect('/inverboy/home/')
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                form = CapituloApuProyectoForm()
                titulo = "Nuevo subcapitulo APU's"
                if request.method == 'POST':
                    form = CapituloApuProyectoForm(request.POST)
                    if form.is_valid():
                        subcapitulos_apu_proyecto = CapituloApuProyecto.objects.filter(tipo_capitulo=2, proyecto=proyecto, capitulo_asociado=capitulo)
                        capitulo_apu_existe = False
                        if subcapitulos_apu_proyecto.filter(Q(codigo=form.cleaned_data['codigo'])):
                            form._errors["codigo"] = ErrorList([u"El codigo ya se encuentra asignado a un subcapitulo del proyecto."])
                            capitulo_apu_existe = True
                        if subcapitulos_apu_proyecto.filter(Q(nombre_capitulo__iexact=form.cleaned_data['nombre'].strip())):
                            form._errors["nombre"] = ErrorList([u"El nombre ya se encuentra asignado a un subcapitulo del proyecto."])
                            capitulo_apu_existe = True
                        if capitulo_apu_existe == False:
                            subcapitulo = CapituloApuProyecto()
                            subcapitulo.codigo = form.cleaned_data['codigo']
                            subcapitulo.nombre_capitulo = form.cleaned_data['nombre'].strip()
                            subcapitulo.tipo_capitulo = 2
                            subcapitulo.estado_capitulo = 1
                            subcapitulo.capitulo_asociado = capitulo
                            subcapitulo.proyecto = proyecto
                            subcapitulo.save()

                            direccion_ip = request.META['REMOTE_ADDR']
                            registro_historial(direccion_ip, usuario, u'Registro subcapitulo apu proyecto, codigo: '+str(subcapitulo.codigo)+u', nombre: '+unicode(subcapitulo.nombre_capitulo)+u', capitulo'+unicode(capitulo.nombre_capitulo)+u', proyecto: '+unicode(proyecto.nombre))
                            return HttpResponseRedirect('/inverboy/home/subcapitulosapuproyectosearch/'+str(proyecto.id)+'/'+str(capitulo.id)+'/')
                return render_to_response('subcapituloapuproyectoadd.html', {'user': user, 'form': form, 'proyecto': proyecto, 'capitulo': capitulo, 'titulo': titulo })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar subcapitulo APU proyecto
def subcapitulo_apu_proyecto_change(request, proyecto_id, capitulo_id, subcapitulo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_capituloapuproyecto' in user.get_all_permissions():
            try:
                proyecto = Proyecto.objects.get(id=proyecto_id)
                capitulo = CapituloApuProyecto.objects.get(tipo_capitulo=1, id=capitulo_id)
                subcapitulo = CapituloApuProyecto.objects.get(tipo_capitulo=2, id=subcapitulo_id)
                if proyecto != capitulo.proyecto or proyecto != subcapitulo.proyecto or capitulo != subcapitulo.capitulo_asociado:
                    return HttpResponseRedirect('/inverboy/home/')
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                form = CapituloApuProyectoForm(initial={'codigo': subcapitulo.codigo, 'nombre': subcapitulo.nombre_capitulo, 'estado': subcapitulo.estado_capitulo})
                titulo = u"Modificar subcapitulo APU's"
                if request.method == 'POST':
                    form = CapituloApuProyectoForm(request.POST)
                    if form.is_valid():
                        subcapitulos_apu_proyecto = CapituloApuProyecto.objects.filter(tipo_capitulo=2, proyecto=proyecto, capitulo_asociado=capitulo)
                        subcapitulo_apu_existe = False
                        if subcapitulo.codigo != form.cleaned_data['codigo']:
                            if subcapitulos_apu_proyecto.filter(Q(codigo=form.cleaned_data['codigo'])):
                                form._errors["codigo"] = ErrorList([u"El codigo ya se encuentra asignado a un capitulo del proyecto."])
                                subcapitulo_apu_existe = True
                        nuevo_nombre = form.cleaned_data['nombre'].strip()
                        nuevo_nombre = normaliza(nuevo_nombre.lower())
                        if normaliza(subcapitulo.nombre_capitulo.lower()) != nuevo_nombre:
                            if subcapitulos_apu_proyecto.filter(Q(nombre_capitulo__iexact=form.cleaned_data['nombre'].strip())):
                                form._errors["nombre"] = ErrorList([u"El nombre ya se encuentra asignado a un subcapitulo del proyecto."])
                                subcapitulo_apu_existe = True
                        if subcapitulo_apu_existe == False:
                            subcapitulo.codigo = form.cleaned_data['codigo']
                            subcapitulo.nombre_capitulo = form.cleaned_data['nombre'].strip()
                            subcapitulo.estado_capitulo = form.cleaned_data['estado']
                            subcapitulo.save()

                            direccion_ip = request.META['REMOTE_ADDR']
                            registro_historial(direccion_ip, usuario, u'Modifico subcapitulo apu proyecto, codigo: '+str(subcapitulo.codigo)+u', nombre: '+unicode(subcapitulo.nombre_capitulo)+u', capitulo'+unicode(capitulo.nombre_capitulo)+u', proyecto: '+unicode(proyecto.nombre))
                            return HttpResponseRedirect('/inverboy/home/subcapitulosapuproyectosearch/'+str(proyecto.id)+'/'+str(capitulo.id)+'/')
                return render_to_response('subcapituloapuproyectoadd.html', {'user': user, 'form': form, 'titulo': titulo, 'proyecto': proyecto, 'capitulo': capitulo, 'change': True})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Busqueda subcapitulo APU proyecto
def subcapitulos_apu_proyecto_search(request, proyecto_id, capitulo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_capituloapuproyecto' in user.get_all_permissions():
            try:
                proyecto = Proyecto.objects.get(id=proyecto_id)
                capitulo = CapituloApuProyecto.objects.get(id=capitulo_id)
                if proyecto != capitulo.proyecto:
                    return HttpResponseRedirect('/inverboy/home/')
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                criterio = ''
                if request.method == 'POST':
                    criterio = request.POST['criterio'].strip()
                subcapitulos = proyecto.capituloapuproyecto_set.filter(tipo_capitulo=2, capitulo_asociado=capitulo)
                try:
                    criterio = int(criterio)
                    subcapitulos = subcapitulos.filter(Q(codigo=criterio))
                except:
                    subcapitulos = subcapitulos.filter(Q(nombre_capitulo__icontains=criterio))
                pag = Paginador(request, subcapitulos, 20, 1)
                return render_to_response('reportesubcapitulosapuproyecto.html', {'user': user, 'proyecto': proyecto, 'subcapitulos': pag, 'criterio': criterio, 'proyecto': proyecto, 'capitulo': capitulo })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#----------------------------------------------------Apus proyecto---------------------------------------------------------------------------------------------

#### Crear APU proyecto ####
#Busqueda APU maestro
def apus_maestro_search(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_apuproyecto' in user.get_all_permissions():
            try:
                proyecto = Proyecto.objects.get(id=proyecto_id)
            except :
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                apus = Apu.objects.filter(estado_apu=True)
                capitulos = Capitulo.objects.filter(tipo_capitulo=1, estado_capitulo=True)
                lista_subcapitulos = []
                criterio = ""
                capitulo_actual = Capitulo()
                subcapitulo_actual = Capitulo()
                if request.method == 'POST':
                    if request.POST['capitulo'] != '0':
                        capitulo_actual = Capitulo.objects.get(tipo_capitulo=1, estado_capitulo=True, id=request.POST['capitulo'])
                        subcapitulos = Capitulo.objects.filter(tipo_capitulo=2, estado_capitulo=True, capitulo_asociado=capitulo_actual)
                        for subcapitulo in subcapitulos:
                            lista_subcapitulos.append(subcapitulo)
                        if request.POST['subcapitulo'] != '0':
                            subcapitulo_actual = Capitulo.objects.get(tipo_capitulo=2, estado_capitulo=True, id=request.POST['subcapitulo'])
                    if subcapitulo_actual != Capitulo():
                        apus = apus.filter(Q(capitulo=subcapitulo_actual))
                    criterio = request.POST['criterio'].strip()
                    if criterio != '':
                        apus = apus.filter(Q(nombre_apu__icontains=criterio))
                pag = Paginador(request, apus, 20, 1)
                return render_to_response('busquedaapus.html', {'user': user, 'capitulos': capitulos, 'subcapitulos': lista_subcapitulos, 'apus': pag, 'criterio': criterio, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'proyecto': proyecto })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Detalles apu maestro
def apu_maestro_details(request, proyecto_id, apu_id):
    from decimal import *
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_apuproyecto' in user.get_all_permissions():
            try:
                proyecto = Proyecto.objects.get(id=proyecto_id)
                apu = Apu.objects.get(id=apu_id)
            except :
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                lista_capitulos = []
                lista_subcapitulos = []
                suministros_apu = apu.suministroapu_set.all()
                suministros = []
                subcapitulo_actual = apu.capitulo
                capitulo_actual = subcapitulo_actual.capitulo_asociado
                capitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=1, estado_capitulo=1, proyecto=proyecto)
                item_nulo = Capitulo()
                item_nulo.id = 0
                item_nulo.nombre_capitulo = '----'
                lista_capitulos.append(item_nulo)
                for capitulo in capitulos:
                    lista_capitulos.append(capitulo)
                form = ApuProyectoForm(initial={'nombre': apu.nombre_apu})
                error = ''
                apu_manejo_estandar = False
                suministro_estandar = None
                if request.method == 'POST':
                    suministros = None
                    try:
                        suministros = request.session['suministros']
                    except :
                        pass
                    if suministros != None:
                        apu_manejo_estandar = request.session['apu_manejo_estandar']
                        suministro_estandar = request.session['id_suministro_estandar']
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
                            for subcapitulo in subcapitulos:
                                lista_subcapitulos.append(subcapitulo)
                        if len(suministros) > 0:
                            if apu_manejo_estandar == True:
                                if suministro_estandar == None:
                                    error = 'Debe seleccionar un suministro (Mano de obra) estandar'
                            if error == '':
                                if form.is_valid():
                                    nombre_nuevo_apu = form.cleaned_data['nombre'].strip()
                                    nombre_nuevo_apu = normaliza(nombre_nuevo_apu.lower())
                                    for apu_existente in apus_existentes:
                                        if normaliza(apu_existente.nombre_apu.lower()) == nombre_nuevo_apu:
                                            form._errors["nombre"] = ErrorList([u"El nombre del apu ya existe en el sistema."])
                                            pag = Paginador(request, suministros, 20, 1)
                                            return render_to_response ('apumaestrodetails.html',{'user': user, 'form':form, 'apu': apu, 'capitulos':  lista_capitulos, 'subcapitulos': lista_subcapitulos, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'suministros_apu': pag, 'apu_manejo_estandar': apu_manejo_estandar, 'suministro_estandar': suministro_estandar, 'proyecto': proyecto, 'error': error } )
                                    valor_unitario = 0.0
                                    suministros_apu = []
                                    for suministro_apu in suministros:
                                        suministro = Suministro.objects.get(id=suministro_apu['suministro'].id)
                                        suninistro_apu_proyecto = SuministroApuProyecto()
                                        suninistro_apu_proyecto.suministro = suministro
                                        suninistro_apu_proyecto.cantidad_suministro = suministro_apu['cantidad']
                                        suninistro_apu_proyecto.precio_suministro = suministro_apu['precio']
                                        suninistro_apu_proyecto.precio_total = round(suninistro_apu_proyecto.cantidad_suministro * suninistro_apu_proyecto.precio_suministro, 2)
                                        valor_unitario = round(valor_unitario + suninistro_apu_proyecto.precio_total, 2)
                                        suministros_apu.append(suninistro_apu_proyecto)
                                    cantidad_proyecto = float(form.cleaned_data['cantidad_proyecto'])
                                    cantidad_apu = float(form.cleaned_data['cantidad_apu'])
                                    cantidad_total = round(cantidad_proyecto * cantidad_apu, 2)

                                    valor_total = round(valor_unitario * cantidad_proyecto * cantidad_apu, 2)
                                    apu_proyecto = ApuProyecto()
                                    apu_proyecto.nombre_apu = form.cleaned_data['nombre'].strip()
                                    apu_proyecto.unidad_medida_apu = apu.unidad_medida_apu
                                    apu_proyecto.cantidad_proyecto = cantidad_proyecto
                                    apu_proyecto.cantidad_apu = cantidad_apu

                                    if proyecto.proceso_proyecto == 2:
                                        apu_proyecto.pertenece_presupuesto = False

                                    #valor_unitario = Decimal(valor_unitario).quantize(Decimal(10) ** -2)
                                    #cantidad_total = Decimal(cantidad_total).quantize(Decimal(10) ** -2)
                                    #valor_total = Decimal(valor_total).quantize(Decimal(10) ** -2)

                                    # Función de redondeo con round()
                                    valor_unitario = round(valor_unitario, 2)
                                    cantidad_total = round(cantidad_total, 2)
                                    valor_total = round(valor_total, 2)

                                    # Función de redondeo con .f
                                    #valor_unitario = "%.2f" % valor_unitario
                                    #cantidad_total = "%.2f" % cantidad_total
                                    #valor_total = "%.2f" % valor_total


                                    apu_proyecto.cantidad_total = cantidad_total
                                    apu_proyecto.valor_unitario = valor_unitario
                                    apu_proyecto.valor_total = valor_total
                                    apu_proyecto.apu_manejo_estandar = apu_manejo_estandar
                                    apu_proyecto.proyecto = proyecto
                                    apu_proyecto.capitulo = capitulo_apu
                                    #try:
                                        #apu_proyecto.validate_unique()
                                    apu_proyecto.save()
                                    for suministro_apu in suministros_apu:
                                        suministro_apu.apu_proyecto = apu_proyecto
                                        if apu_proyecto.proyecto.proceso_proyecto == 2:
                                            suministro_apu.pertenece_presupuesto = False
                                        suministro_apu.save()
                                        if suministro_apu.suministro.id == suministro_estandar:
                                            apu_proyecto.suministro_estandar = suministro_apu
                                            apu_proyecto.save()
                                    del request.session['suministros']
                                    
                                    direccion_ip = request.META['REMOTE_ADDR']
                                    registro_historial(direccion_ip, usuario, "Registro APU proyecto, nombre: "+ unicode(apu_proyecto.nombre_apu) +", en proyecto: "+ unicode(proyecto.nombre))
                                    return HttpResponseRedirect('/inverboy/home/detallesapuproyecto/' + str(apu_proyecto.id) + '/' + str(proyecto_id) + '/')
                                    #except:
                                    #    print 'error en campos unicos de apu'
                        else:
                            error = 'Debe ingresar por lo menos un suministro'
                    else:
                        return HttpResponseRedirect('/inverboy/home/proyectodetails/' + str(proyecto.id) + '/')
                else:
                    for suministro in suministros_apu:
                        suministros.append({'suministro': suministro.suministro, 'precio': suministro.precio_suministro, 'cantidad': suministro.cantidad_suministro})
                    request.session['suministros_agregar'] = []
                request.session['apu_manejo_estandar'] = apu_manejo_estandar
                request.session['id_suministro_estandar'] = suministro_estandar
                request.session['suministros'] = suministros
                pag = Paginador(request, suministros, 20, 1)
                return render_to_response ('apumaestrodetails.html',{'user': user, 'form':form, 'apu': apu, 'capitulos':  lista_capitulos, 'subcapitulos': lista_subcapitulos, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'suministros_apu': pag, 'apu_manejo_estandar': apu_manejo_estandar, 'suministro_estandar': suministro_estandar, 'proyecto': proyecto, 'error': error } )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar apu proyecto
def apu_proyecto_change(request, apu_proyecto_id, proyecto_id):
    from decimal import *
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_apuproyecto' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                apu_proyecto = ApuProyecto.objects.get(id=apu_proyecto_id, proyecto=proyecto)
                lista_capitulos = []
                lista_subcapitulos = []
                lista_suministros = apu_proyecto.suministroapuproyecto_set.all()
                capitulo_actual = apu_proyecto.capitulo
                subcapitulo_actual = CapituloApuProyecto()
                if capitulo_actual.tipo_capitulo == 2:
                    subcapitulo_actual = capitulo_actual
                    capitulo_actual = capitulo_actual.capitulo_asociado
                capitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=1, estado_capitulo=1, proyecto=proyecto)
                subcapitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=2, estado_capitulo=1, capitulo_asociado=capitulo_actual, proyecto=proyecto)
                for capitulo in capitulos:
                    lista_capitulos.append(capitulo)
                for subcapitulo in subcapitulos:
                    lista_subcapitulos.append(subcapitulo)
                form = ApuProyectoForm(initial={'nombre': apu_proyecto.nombre_apu, 'cantidad_proyecto': apu_proyecto.cantidad_proyecto, 'cantidad_apu': apu_proyecto.cantidad_apu, 'cantidad_total': apu_proyecto.cantidad_total, 'valor_unitario': apu_proyecto.valor_unitario, 'valor_total': apu_proyecto.valor_total, 'apu_manejo_estandar': apu_proyecto.apu_manejo_estandar, 'estado': apu_proyecto.estado_apu })
                error = ''
                suministros_apu = apu_proyecto.suministroapuproyecto_set.all()
                suministros = []
                for suministro in suministros_apu:
                    suministros.append({ 'suministro': suministro.suministro, 'precio': suministro.precio_suministro, 'cantidad': suministro.cantidad_suministro })
                apu_manejo_estandar = False
                suministro_estandar = None
                if request.method == 'POST':
                    suministros = None
                    try:
                        suministros = request.session['suministros']
                    except :
                        pass
                    if suministros != None:
                        #Valida el id en session del APU proyecto que se desea modificar
                        if int(request.session['apu_proyecto_id']) == int(apu_proyecto_id):
                            apu_manejo_estandar = request.session['apu_manejo_estandar']
                            suministro_estandar = request.session['id_suministro_estandar']
                            form = ApuProyectoForm(request.POST)
                            apus_existentes = []
                            lista_subcapitulos = []
                            capitulo_actual = CapituloApuProyecto()
                            subcapitulo_actual = CapituloApuProyecto()
                            if request.POST['capitulo'] != '0':
                                capitulo_actual = CapituloApuProyecto.objects.get(id=request.POST['capitulo'], tipo_capitulo=1, proyecto=proyecto)
                                apus_existentes = ApuProyecto.objects.filter(capitulo=capitulo_actual, proyecto=proyecto)
                                subcapitulos = CapituloApuProyecto.objects.filter(capitulo_asociado=capitulo_actual, estado_capitulo=1, proyecto=proyecto)
                                capitulo_apu = capitulo_actual
                                if request.POST['subcapitulo'] != '0':
                                    subcapitulo_actual = CapituloApuProyecto.objects.get(id=request.POST['subcapitulo'], tipo_capitulo=2, proyecto=proyecto)
                                    capitulo_apu = subcapitulo_actual
                                    apus_existentes = ApuProyecto.objects.filter(capitulo=subcapitulo_actual, proyecto=proyecto)
                                for subcapitulo in subcapitulos:
                                    lista_subcapitulos.append(subcapitulo)
                            suministros = request.session['suministros']
                            if len(suministros) > 0:
                                if apu_manejo_estandar == True:
                                    if suministro_estandar == None:
                                        error = 'Debe seleccionar un suministro (Mano de obra) estandar'
                                if error == '':
                                    if form.is_valid():
                                        nombre_nuevo_apu = form.cleaned_data['nombre'].strip()
                                        nombre_nuevo_apu = normaliza(nombre_nuevo_apu.lower())
                                        if normaliza(apu_proyecto.nombre_apu.lower()) != nombre_nuevo_apu:
                                            for apu_existente in apus_existentes:
                                                if normaliza(apu_existente.nombre_apu.lower()) == nombre_nuevo_apu:
                                                    form._errors["nombre"] = ErrorList([u"El nombre del apu ya existe en el sistema."])
                                                    pag = Paginador(request, suministros, 20, 1)
                                                    return render_to_response ('apuproyectochange.html',{'user': user, 'form':form, 'apu': apu_proyecto, 'capitulos':  lista_capitulos, 'subcapitulos': lista_subcapitulos, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'suministros_apu': pag, 'apu_manejo_estandar': apu_manejo_estandar, 'suministro_estandar': suministro_estandar, 'proyecto': proyecto, 'error': error } )

                                        cantidad_proyecto = float(form.cleaned_data['cantidad_proyecto'])
                                        cantidad_apu = float(form.cleaned_data['cantidad_apu'])
                                        cantidad_total = round(cantidad_proyecto * cantidad_apu, 2)

                                        #Valida que las cantidades de los suministros no sean menores a las cantidades requeridas de los mismos
                                        cantidades_correctas = True
                                        for suministro_apu in suministros:
                                            try:
                                                suministro_apu_proyecto = apu_proyecto.suministroapuproyecto_set.get(suministro__id=suministro_apu['suministro'].id)
                                                if (suministro_apu['cantidad'] * cantidad_total) < suministro_apu_proyecto.cantidad_total_requerida:
                                                    cantidades_correctas = False
                                            except :
                                                pass

                                        if cantidades_correctas == True:
                                            valor_unitario = 0.0
                                            tmp_suministros_apu = []
                                            for suministro_apu in suministros:
                                                suministro = Suministro.objects.get(id=suministro_apu['suministro'].id)
                                                suninistro_apu_proyecto = SuministroApuProyecto()
                                                suninistro_apu_proyecto.suministro = suministro
                                                suninistro_apu_proyecto.cantidad_suministro = suministro_apu['cantidad']
                                                suninistro_apu_proyecto.precio_suministro = suministro_apu['precio']
                                                suninistro_apu_proyecto.precio_total = round(suninistro_apu_proyecto.cantidad_suministro * suninistro_apu_proyecto.precio_suministro, 2)
                                                valor_unitario = round(valor_unitario + suninistro_apu_proyecto.precio_total, 2)
                                                tmp_suministros_apu.append(suninistro_apu_proyecto)


                                            valor_total = round(valor_unitario * cantidad_total, 2)
                                            apu_proyecto.nombre_apu = form.cleaned_data['nombre'].strip()
                                            # Verifica si el proyecto no esta en presupuesto
                                            if proyecto.proceso_proyecto == 2:
                                                historial = HistorialAdicionApuProyecto()
                                                historial.apu_proyecto = apu_proyecto
                                                historial.usuario = usuario
                                                historial.save()

                                            # Verifica si el proyecto no esta en presupuesto
                                            if proyecto.proceso_proyecto == 2 and apu_proyecto.cantidad_proyecto != cantidad_proyecto:
                                                historial.cantidad_proyecto = round(cantidad_proyecto - apu_proyecto.cantidad_proyecto, 2)
                                                historial.save()
                                            apu_proyecto.cantidad_proyecto = cantidad_proyecto
                                            # Verifica si el proyecto no esta en presupuesto
                                            if proyecto.proceso_proyecto == 2 and apu_proyecto.cantidad_apu != cantidad_apu:
                                                historial.cantidad_apu = round(cantidad_apu - apu_proyecto.cantidad_apu, 2)
                                                historial.save()
                                            apu_proyecto.cantidad_apu = cantidad_apu

                                            # Función de redondeo con round()
                                            valor_unitario = round(valor_unitario, 2)
                                            cantidad_total = round(cantidad_total, 2)
                                            valor_total = round(valor_total, 2)

                                            apu_proyecto.cantidad_total = cantidad_total
                                            apu_proyecto.valor_unitario = valor_unitario
                                            apu_proyecto.valor_total = valor_total
                                            apu_proyecto.apu_manejo_estandar = apu_manejo_estandar
                                            apu_proyecto.suministro_estandar = None
                                            apu_proyecto.proyecto = proyecto
                                            apu_proyecto.capitulo = capitulo_apu
                                            apu_proyecto.estado_apu = form.cleaned_data['estado']
                                            #try:
                                                #apu_proyecto.validate_unique()
                                            apu_proyecto.save()

                                            # Elimina los suministros de la BD que no se encuentran en la nueva lista de suministros
                                            for suministro_apu in suministros_apu:
                                                eliminar_suministro = True
                                                for tmp_suministro in tmp_suministros_apu:
                                                    if tmp_suministro.suministro.id == suministro_apu.suministro.id:
                                                        eliminar_suministro = False
                                                if eliminar_suministro == True:
                                                    suministro_apu_proyecto = SuministroApuProyecto.objects.get(apu_proyecto=apu_proyecto, suministro__id=suministro_apu.suministro.id)
                                                    if len(suministro_apu_proyecto.suministrorequisicion_set.all()) == 0:
                                                        suministro_apu_proyecto.delete()

                                            #Actualiza las cantidades en los suministros ya existentes en el APU
                                            for tmp_suministro in tmp_suministros_apu:
                                                existe_suministro = False
                                                suministro_apu = None
                                                for suministro_apu in suministros_apu:
                                                    if suministro_apu.suministro.id == tmp_suministro.suministro.id:
                                                        # Si el proyecto no se encuentra en presupuesto se crea una nueva adición al suministro Apu proyecto
                                                        if proyecto.proceso_proyecto == 2 and suministro_apu.cantidad_suministro != tmp_suministro.cantidad_suministro:
                                                            adicion_suministro_apu_proyecto = AdicionSuministroApuProyecto()
                                                            adicion_suministro_apu_proyecto.cantidad = round(tmp_suministro.cantidad_suministro - suministro_apu.cantidad_suministro, 4)
                                                            adicion_suministro_apu_proyecto.suministro = suministro_apu
                                                            adicion_suministro_apu_proyecto.historial_adicion_apu_proyecto = historial
                                                            adicion_suministro_apu_proyecto.save()

                                                        # Actualiza la cantidad en el suministro Apu proyecto
                                                        suministro_apu.cantidad_suministro = tmp_suministro.cantidad_suministro
                                                        suministro_apu.precio_suministro = tmp_suministro.precio_suministro
                                                        suministro_apu.precio_total = tmp_suministro.precio_total
                                                        suministro_apu.save()
                                                        existe_suministro = True
                                                        break
                                                if existe_suministro == False:
                                                    tmp_suministro.apu_proyecto = apu_proyecto
                                                    # Si el proyecto no se encuentra en presupuesto el nuevo suministro no pertenece al presupuesto
                                                    if proyecto.proceso_proyecto == 2:
                                                        tmp_suministro.pertenece_presupuesto = False
                                                    tmp_suministro.save()
                                                    suministro_apu = tmp_suministro
                                                if suministro_apu.suministro.id == suministro_estandar:
                                                    apu_proyecto.suministro_estandar = suministro_apu
                                                    apu_proyecto.save()

                                            # Se eliminan las variables de la session
                                            del request.session['suministros']
                                            del request.session['apu_manejo_estandar']
                                            del request.session['id_suministro_estandar']
                                            del request.session['apu_proyecto_id']
                                            del request.session['suministros_agregar']

                                            direccion_ip = request.META['REMOTE_ADDR']
                                            registro_historial(direccion_ip, usuario, u'Modifico APU proyecto, nombre: '+unicode(apu_proyecto.nombre_apu)+u', en proyecto: '+unicode(proyecto.nombre))
                                            return HttpResponseRedirect('/inverboy/home/detallesapuproyecto/' + str(apu_proyecto_id) + '/' + str(proyecto_id) + '/')
                                            #except:
                                            #    print 'error en campos unicos de apu'
                                        else:
                                            error = 'Algunas cantidades son inferiores a las cantidades requeridas'
                            else:
                                error = 'Debe ingresar por lo menos un suministro'
                        else:
                            apu_proyecto = proyecto.apuproyecto_set.get(id=request.session['apu_proyecto_id'])
                            mensaje = u'No puede modificar este APU proyecto, actualmente se encuentra modificando el APU proyecto: ' + unicode(apu_proyecto.nombre_apu)
                            personas = proyecto.personaproyecto_set.filter(estado=True)
                            return render_to_response('proyectodetails.html', {'user': user, 'proyecto': proyecto, 'personas': personas, 'mensaje': mensaje})
                    else:
                        return HttpResponseRedirect('/inverboy/home/proyectodetails/' + str(proyecto.id) + '/')
                else:
                    if apu_proyecto.apu_manejo_estandar:
                        apu_manejo_estandar = apu_proyecto.apu_manejo_estandar
                        suministro_estandar = apu_proyecto.suministro_estandar.suministro.id
                    request.session['apu_manejo_estandar'] = apu_manejo_estandar
                    request.session['id_suministro_estandar'] = suministro_estandar
                    request.session['apu_proyecto_id'] = apu_proyecto_id
                request.session['suministros'] = suministros
                request.session['suministros_agregar'] = []
                pag = Paginador(request, suministros, 20, 1)
                return render_to_response ('apuproyectochange.html',{'user': user, 'form':form, 'apu': apu_proyecto, 'capitulos':  lista_capitulos, 'subcapitulos': lista_subcapitulos, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'suministros_apu': pag, 'apu_manejo_estandar': apu_manejo_estandar, 'suministro_estandar': suministro_estandar, 'proyecto': proyecto, 'error': error } )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Busqueda APU's de proyecto
def apus_proyecto_search(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_apuproyecto' in user.get_all_permissions():
            try:
                proyecto = Proyecto.objects.get(id=proyecto_id)
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                apus = proyecto.apuproyecto_set.all()
                capitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=1, estado_capitulo=1, proyecto=proyecto)
                lista_subcapitulos = []
                criterio = ""
                capitulo_actual = CapituloApuProyecto()
                subcapitulo_actual = CapituloApuProyecto()
                form = BusquedaApuProyectoform()
                if request.method == 'POST':
                    if request.POST['capitulo'] != '0':
                        capitulo_actual = CapituloApuProyecto.objects.get(tipo_capitulo=1, id=request.POST['capitulo'])
                        subcapitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=2, estado_capitulo=True, capitulo_asociado=capitulo_actual)
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
                            criterio = form.cleaned_data['criterio'].strip()
                            apus = apus.filter(Q(nombre_apu__icontains=criterio))
                pag = Paginador(request, apus, 20, 1)
                return render_to_response('reporteapusproyecto.html', {'user': user, 'form': form, 'capitulos': capitulos, 'subcapitulos': lista_subcapitulos, 'apus': pag, 'criterio': criterio, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'proyecto': proyecto })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Detalles APU proyecto
def detalles_apu_proyecto(request, apu_proyecto_id, proyecto_id):
    from decimal import *
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_apuproyecto' in user.get_all_permissions():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                apu_proyecto = proyecto.apuproyecto_set.get(id=apu_proyecto_id)
                suministros = apu_proyecto.suministroapuproyecto_set.all()
                pag = Paginador(request, suministros, 20, 1)
                return render_to_response ('detallesapuproyecto.html',{'user': user, 'apu': apu_proyecto, 'suministros': pag, 'proyecto': proyecto} )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Busqueda APU's de proyecto
def reporte_estado_apus_proyecto(request, proyecto_id):
    if request.user.is_authenticated():
        request.session.set_expiry(TIEMPO_INACTIVIDAD)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_apuproyecto' in user.get_all_permissions():
            try:
                proyecto = Proyecto.objects.get(id=proyecto_id)
            except:
                return HttpResponseRedirect('/inverboy/home/')
            #Valida que el usuario tenga vinculo con el proyecto ó sea miembro del staff (es administrador)
            usuario = Usuario.objects.get(id=user.id)
            if proyecto in usuario.lista_proyectos_vinculados():
                return render_to_response('reporteestadoapusproyecto.html', {'user': user, 'proyecto': proyecto})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')