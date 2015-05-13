# -*- encoding: utf-8 -*-
from views_modulo_usuario import *
from funciones_views import *
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse
from inverboy.forms import *
## PAGINACION
from inverboy.paginator import *
## MANEJO DE ERRORES MANUALMENTE
from django.forms.util import ErrorList
## CONSULTAS ANIDADAS
from django.db.models import Q

#--------------------------------------------CLASIFICACION APUS--------------------------------------------------------------------

#Crear capituo APU
def capitulo_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_capitulo' in user.get_all_permissions():
            form = CapituloForm()
            if request.method == 'POST':
                form = CapituloForm(request.POST)
                if form.is_valid():
                    capitulo_existente = None
                    nombre = form.cleaned_data['nombre'].strip()
                    try:
                        capitulo_existente = Capitulo.objects.get(nombre_capitulo=nombre, tipo_capitulo=1)
                    except :
                        pass
                    if capitulo_existente == None:
                        capitulo = Capitulo()
                        capitulo.nombre_capitulo = nombre
                        capitulo.tipo_capitulo = 1
                        capitulo.estado_capitulo = 1
                        #try:
                        #    capitulo.validate_unique()
                        capitulo.save()
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, u'Registro capitulo APU, nombre: '+ unicode(capitulo.nombre_capitulo))
                        return HttpResponseRedirect('/inverboy/home/capitulossearch/')
                        #except :
                    else:
                        form._errors["nombre"] = ErrorList([u"El capitulo ya existe en el sistema."])
            return render_to_response('capituloadd.html', {'user': user, 'form': form})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar capitulo APU
def capitulo_change(request, capitulo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_capitulo' in user.get_all_permissions():
            capitulo = Capitulo.objects.get(id=capitulo_id)
            form = CapituloForm(initial={'nombre': capitulo.nombre_capitulo, 'estado': capitulo.estado_capitulo})
            if request.method == 'POST':
                form = CapituloForm(request.POST)
                if form.is_valid():
                    capitulo_existente = None
                    nombre = form.cleaned_data['nombre'].strip()
                    if normaliza(capitulo.nombre_capitulo.lower()) != normaliza(nombre.lower()):
                        try:
                            capitulo_existente = Capitulo.objects.get(nombre_capitulo=nombre, tipo_capitulo=1)
                        except :
                            pass
                    if capitulo_existente == None:
                        capitulo.nombre_capitulo = nombre
                        capitulo.estado_capitulo = form.cleaned_data['estado']
                        capitulo.save()
                        # Para modificar el estado de subcapitulos y APU's
                        Capitulo.objects.filter(capitulo_asociado=capitulo, tipo_capitulo=2).update(estado_capitulo=capitulo.estado_capitulo)
                        Apu.objects.filter(capitulo__capitulo_asociado=capitulo).update(estado_apu=capitulo.estado_capitulo)
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, u'Modifico capitulo APU, nombre: '+ unicode(capitulo.nombre_capitulo))
                        return HttpResponseRedirect('/inverboy/home/capitulossearch/')
                    else :
                        form._errors["nombre"] = ErrorList([u"El capitulo ya existe en el sistema."])
            return render_to_response('capituloadd.html', {'user': user, 'form': form, 'change': True})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Busqueda capitulos de APU maestro
def capitulos_search(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_capitulo' in user.get_all_permissions():
            criterio = ''
            capitulos = Capitulo.objects.filter(tipo_capitulo=1)
            if request.method == 'POST':
                criterio = request.POST['criterio'].strip()
                capitulos = capitulos.filter(Q(nombre_capitulo__icontains=criterio))
            pag = Paginador(request, capitulos, 20, 1)
            return render_to_response('reportecapitulos.html', {'user': user, 'capitulos': pag, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Crear subcapitulo
def subcapitulo_add(request, capitulo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_capitulo' in user.get_all_permissions():
            capitulos = Capitulo.objects.filter(tipo_capitulo=1, estado_capitulo=1)
            lista_capitulos = []
            item_nulo = Capitulo()
            item_nulo.id = 0
            item_nulo.nombre_capitulo = '----'
            lista_capitulos.append(item_nulo)
            for capitulo in capitulos:
                lista_capitulos.append(capitulo)
            form = SubCapituloForm(initial={'capitulo_asociado': capitulo_id})
            if request.method == 'POST':
                form = SubCapituloForm(request.POST)
                if form.is_valid():
                    subcapitulo_existente = None
                    nombre = form.cleaned_data['nombre'].strip()
                    capitulo = form.cleaned_data['capitulo_asociado']
                    try:
                        subcapitulo_existente = Capitulo.objects.get(capitulo_asociado=capitulo, nombre_capitulo=nombre, tipo_capitulo=2)
                    except:
                        pass
                    if subcapitulo_existente == None:
                        subCapitulo = Capitulo()
                        subCapitulo.nombre_capitulo = nombre
                        subCapitulo.tipo_capitulo = 2
                        subCapitulo.estado_capitulo = 1
                        subCapitulo.capitulo_asociado = capitulo
                        subCapitulo.save()
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, u'Registro subcapitulo APU, nombre: '+unicode(subCapitulo.nombre_capitulo))
                        return HttpResponseRedirect('/inverboy/home/subcapitulossearch/'+str(subCapitulo.capitulo_asociado_id)+'/')
                    else :
                        form._errors["nombre"] = ErrorList([u"El subcapitulo ya existe en el sistema."])
            return render_to_response('subcapituloadd.html', {'user': user, 'form': form })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Busqueda subcapitulos de APU maestro
def subcapitulos_search(request, capitulo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_capitulo' in user.get_all_permissions():
            criterio = ''
            capitulo = Capitulo.objects.get(id=capitulo_id, tipo_capitulo=1)
            subcapitulos = Capitulo.objects.filter(tipo_capitulo=2, capitulo_asociado=capitulo)
            if request.method == 'POST':
                criterio = request.POST['criterio'].strip()
                subcapitulos = subcapitulos.filter(Q(nombre_capitulo__icontains=criterio))
            pag = Paginador(request, subcapitulos, 20, 1)
            return render_to_response('reportesubcapitulos.html', {'user': user, 'subcapitulos': pag, 'capitulo': capitulo, 'criterio': criterio})
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar subcapitulo
def subcapitulos_change(request, subcapitulo_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_capitulo' in user.get_all_permissions():
            subcapitulo = Capitulo.objects.get(id=subcapitulo_id, tipo_capitulo=2)
            form = SubCapituloForm(initial={'capitulo_asociado': subcapitulo.capitulo_asociado, 'nombre': subcapitulo.nombre_capitulo, 'estado': subcapitulo.estado_capitulo})
            if request.method == 'POST':
                form = SubCapituloForm(request.POST)
                if form.is_valid():
                    subcapitulo_existente = None
                    capitulo = form.cleaned_data['capitulo_asociado']
                    nombre = form.cleaned_data['nombre'].strip()
                    if normaliza(subcapitulo.nombre_capitulo.lower()) != normaliza(nombre.lower()) or subcapitulo.capitulo_asociado != capitulo:
                        try:
                            subcapitulo_existente = Capitulo.objects.get(capitulo_asociado=capitulo, nombre_capitulo=nombre, tipo_capitulo=2)
                        except:
                            pass
                    if subcapitulo_existente == None:
                        subcapitulo.nombre_capitulo = form.cleaned_data['nombre'].strip()
                        subcapitulo.estado_capitulo = form.cleaned_data['estado']
                        subcapitulo.capitulo_asociado = form.cleaned_data['capitulo_asociado']
                        subcapitulo.save()
                        # Modificar estado APU's relacionados con subcapitulo
                        Apu.objects.filter(capitulo=subcapitulo).update(estado_apu=subcapitulo.estado_capitulo)
                        usuario_actual = Usuario.objects.get(id=user.id)
                        direccion_ip = request.META['REMOTE_ADDR']
                        registro_historial(direccion_ip, usuario_actual, u'Modifico subcapitulo APU, nombre: '+ unicode(subcapitulo.nombre_capitulo))
                        return HttpResponseRedirect('/inverboy/home/subcapitulossearch/'+str(subcapitulo.capitulo_asociado_id)+'/')
                    else:
                        msg = u"El subcapitulo ya existe en el sistema."
                        form._errors["nombre"] = form.error_class([msg])
            return render_to_response('subcapituloadd.html', {'user': user, 'form': form, 'change': True })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#-----------------------------------------------------------APU-----------------------------------------------------------------------------

#Crear APU maestro
def apu_add(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.add_apu' in user.get_all_permissions():
            capitulos = Capitulo.objects.filter(tipo_capitulo=1, estado_capitulo=1)
            lista_capitulos = []
            lista_subcapitulos = []
            capitulo_actual = Capitulo()
            subcapitulo_actual = Capitulo()
            item_nulo = Capitulo()
            item_nulo.id = 0
            item_nulo.nombre_capitulo = '----'
            lista_capitulos.append(item_nulo)
            for capitulo in capitulos:
                lista_capitulos.append(capitulo)
            form = ApuForm()
            suministros = []
            error = ''
            if request.method == 'POST':
                suministros = None
                try:
                    suministros = request.session['suministros']
                except :
                    pass
                if suministros != None:
                    form = ApuForm(request.POST)
                    apus_existentes = []
                    try:
                        if request.POST['capitulo'] != '0':
                            capitulo_actual = Capitulo.objects.get(id=request.POST['capitulo'], tipo_capitulo=1)
                            capitulo_apu = capitulo_actual
                            subcapitulos = Capitulo.objects.filter(capitulo_asociado=capitulo_actual, estado_capitulo=1)
                            if request.POST['subcapitulo'] != '0':
                                subcapitulo_actual = Capitulo.objects.get(id=request.POST['subcapitulo'], tipo_capitulo=2)
                                capitulo_apu = subcapitulo_actual
                            apus_existentes = Apu.objects.filter(capitulo=capitulo_apu)
                            lista_subcapitulos.append(item_nulo)
                            for subcapitulo in subcapitulos:
                                lista_subcapitulos.append(subcapitulo)
                    except :
                        pass

                    pag = Paginador(request, suministros, 20, 1)
                    if len(suministros) > 0:
                        if form.is_valid():
                            nombre_nuevo_apu = form.cleaned_data['nombre'].strip()
                            nombre_nuevo_apu = normaliza(nombre_nuevo_apu.lower())
                            for apu_existente in apus_existentes:
                                if normaliza(apu_existente.nombre_apu.lower()) == nombre_nuevo_apu:
                                    form._errors["nombre"] = ErrorList([u"El nombre del apu ya existe en el sistema."])
                                    return render_to_response ('apuadd.html',{'user': user, 'form':form, 'capitulos':  lista_capitulos, 'subcapitulos': lista_subcapitulos, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'suministros_apu': pag, 'error': error} )
                            apu = Apu()
                            apu.nombre_apu = form.cleaned_data['nombre'].strip()
                            apu.unidad_medida_apu = form.cleaned_data['unidad_medida']
                            apu.estado_apu = 1
                            usuario = Usuario.objects.get(id=user.id)
                            apu.usuario = usuario
                            apu.capitulo = capitulo_apu
                            #try:
                            #apu.validate_unique()
                            apu.precio_apu = 0
                            apu.save()
                            precio_apu = 0.0
                            for suministro in suministros:
                                suministro_apu = SuministroApu()
                                suministro_apu.cantidad_suministro = suministro['cantidad']
                                suministro_apu.precio_suministro = suministro['precio']
                                suministro = Suministro.objects.get(id=suministro['suministro'].id)
                                suministro_apu.suministro = suministro
                                suministro_apu.apu = apu
                                suministro_apu.save()
                                precio_apu = round(precio_apu + round((suministro_apu.precio_suministro * suministro_apu.cantidad_suministro), 2), 2)
                            apu.precio_apu = precio_apu
                            apu.save()
                            del request.session['suministros']
                            usuario_actual = Usuario.objects.get(id=user.id)
                            direccion_ip = request.META['REMOTE_ADDR']
                            registro_historial(direccion_ip, usuario_actual, "Registro APU, nombre: "+ unicode(apu.nombre_apu))
                            return HttpResponseRedirect('/inverboy/home/apusdetails/' + str(apu.id))
                            #except:
                            #    print 'error en campos unicos de apu'
                    else:
                        error = 'Debe ingresar por lo menos un suministro'
                else:
                    return HttpResponseRedirect('/inverboy/home/')
            else:
                request.session['suministros'] = suministros
                pag = []
            request.session['suministros_agregar'] = []
            return render_to_response ('apuadd.html',{'user': user, 'form': form, 'capitulos':  lista_capitulos, 'subcapitulos': lista_subcapitulos, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'suministros_apu': pag, 'error': error} )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Modificar apu
def apu_change(request, apu_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.change_apu' in user.get_all_permissions():
            apu = Apu.objects.get(id=apu_id)
            lista_capitulos = []
            lista_subcapitulos = []
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
            suministros_apu = apu.suministroapu_set.all()
            suministros = []
            for suministro in suministros_apu:
                suministros.append({ 'suministro': suministro.suministro, 'precio': suministro.precio_suministro, 'cantidad': suministro.cantidad_suministro })
            error = ''
            if request.method == 'POST':
                suministros = None
                try:
                    suministros = request.session['suministros']
                except :
                    pass
                if suministros != None:
                    form = ApuForm(request.POST)
                    apus_existentes = []
                    lista_subcapitulos = []
                    capitulo_actual = Capitulo()
                    subcapitulo_actual = Capitulo()
                    if request.POST['capitulo'] != '0':
                        capitulo_actual = Capitulo.objects.get(id=request.POST['capitulo'], tipo_capitulo=1)
                        capitulo_apu = capitulo_actual
                        subcapitulos = Capitulo.objects.filter(capitulo_asociado=capitulo_actual, estado_capitulo=1)
                        if request.POST['subcapitulo'] != '0':
                            subcapitulo_actual = Capitulo.objects.get(id=request.POST['subcapitulo'], tipo_capitulo=2)
                            capitulo_apu = subcapitulo_actual
                        apus_existentes = Apu.objects.filter(capitulo=capitulo_apu)
                        lista_subcapitulos.append(item_nulo)
                        for subcapitulo in subcapitulos:
                            lista_subcapitulos.append(subcapitulo)

                    if len(suministros) > 0:
                        if form.is_valid():
                            nuevo_nombre_apu = form.cleaned_data['nombre'].strip()
                            nuevo_nombre_apu = normaliza(nuevo_nombre_apu.lower())
                            if capitulo_apu == apu.capitulo and normaliza(apu.nombre_apu.lower()) == nuevo_nombre_apu:
                                apus_existentes = apus_existentes.exclude(id=apu.id)
                            for apu_existente in apus_existentes:
                                if normaliza(apu_existente.nombre_apu.lower()) == nuevo_nombre_apu:
                                    form._errors["nombre"] = ErrorList([u"El nombre del apu ya existe en el sistema."])
                                    pag = Paginador(request, suministros, 20, 1)
                                    return render_to_response ('apuadd.html',{'user': user, 'form': form, 'capitulos':  lista_capitulos, 'subcapitulos': lista_subcapitulos, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'suministros_apu': pag, 'change': True } )
                            valor_unitario = 0.0
                            tmp_suministros_apu = []
                            for suministro_apu in suministros:
                                suministro = Suministro.objects.get(id=suministro_apu['suministro'].id)
                                tmp_suministro = SuministroApu()
                                tmp_suministro.suministro = suministro
                                tmp_suministro.cantidad_suministro = suministro_apu['cantidad']
                                tmp_suministro.precio_suministro = suministro_apu['precio']
                                valor_unitario = round(valor_unitario + (round(tmp_suministro.cantidad_suministro * tmp_suministro.precio_suministro, 2)), 2)
                                tmp_suministros_apu.append(tmp_suministro)
                            apu.nombre_apu = form.cleaned_data['nombre'].strip()
                            apu.unidad_medida_apu = form.cleaned_data['unidad_medida']
                            apu.estado_apu = form.cleaned_data['estado']
                            usuario = Usuario.objects.get(id=user.id)
                            apu.usuario = usuario
                            apu.capitulo = capitulo_apu
                            #try:
                            #apu.validate_unique()
                            apu.precio_apu = valor_unitario
                            apu.save()
                            # Elimina los suministros de la BD que no se encuentran en la nueva lista de suministros
                            for suministro_apu in suministros_apu:
                                eliminar_suministro = True
                                for tmp_suministro in tmp_suministros_apu:
                                    if tmp_suministro.suministro.id == suministro_apu.suministro.id:
                                        eliminar_suministro = False
                                if eliminar_suministro == True:
                                    SuministroApu.objects.get(apu=apu, suministro__id=suministro_apu.suministro.id).delete()
                            for tmp_suministro in tmp_suministros_apu:
                                existe_suministro = False
                                for suministro_apu in suministros_apu:
                                    if suministro_apu.suministro.id == tmp_suministro.suministro.id:
                                        suministro_apu.cantidad_suministro = tmp_suministro.cantidad_suministro
                                        suministro_apu.precio_suministro = tmp_suministro.precio_suministro
                                        suministro_apu.save()
                                        existe_suministro = True
                                        break
                                if existe_suministro == False:
                                    tmp_suministro.apu = apu
                                    tmp_suministro.save()
                            del request.session['suministros']
                            usuario_actual = Usuario.objects.get(id=user.id)
                            direccion_ip = request.META['REMOTE_ADDR']
                            registro_historial(direccion_ip, usuario_actual, "Modifico APU, nombre: "+ unicode(apu.nombre_apu))
                            return HttpResponseRedirect('/inverboy/home/apusdetails/' + str(apu.id))
                            #except:
                            #    print 'error en campos unicos de apu'
                    else:
                        error = 'Debe ingresar por lo menos un suministro'
                else:
                    return HttpResponseRedirect('/inverboy/home/')
            request.session['suministros'] = suministros
            request.session['suministros_agregar'] = []
            pag = Paginador(request, suministros, 20, 1)
            return render_to_response ('apuadd.html',{'user': user, 'form':form, 'capitulos':  lista_capitulos, 'subcapitulos': lista_subcapitulos, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'suministros_apu': pag, 'error': error, 'change': True } )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Detalles apu
def apu_details(request, apu_id):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_apu' in user.get_all_permissions():
            apu = Apu.objects.get(id=apu_id)
            suministros = apu.suministroapu_set.all()
            pag = Paginador(request, suministros, 20, 1)
            return render_to_response ('apudetails.html',{ 'user': user, 'apu': apu, 'suministros_apu': pag } )
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')


#Busqueda APU'S maestros
def apus_search(request):
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        #Valida que el usuario tenga permisos para el ingreso al modulo ó sea miembro del staff (es administrador)
        if 'inverboy.view_apu' in user.get_all_permissions():
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
                capitulo_apu = Capitulo()
                if request.POST['capitulo'] != '0':
                    capitulo_actual = Capitulo.objects.get(tipo_capitulo=1, id=request.POST['capitulo'])
                    capitulo_apu = capitulo_actual
                    subcapitulos = Capitulo.objects.filter(tipo_capitulo=2, capitulo_asociado=capitulo_actual)
                    lista_subcapitulos.append(item_nulo)
                    for subcapitulo in subcapitulos:
                        lista_subcapitulos.append(subcapitulo)
                    if request.POST['subcapitulo'] != '0':
                        subcapitulo_actual = Capitulo.objects.get(tipo_capitulo=2, id=request.POST['subcapitulo'])
                        capitulo_apu = subcapitulo_actual
                form = BusquedaApuform(request.POST)
                if form.is_valid():
                    if capitulo_apu != Capitulo():
                        apus = apus.filter(Q(capitulo=capitulo_apu))
                    if form.cleaned_data['criterio'] != '':
                        criterio = form.cleaned_data['criterio'].strip()
                        apus = apus.filter(Q(nombre_apu__icontains=criterio))
            pag = Paginador(request, apus, 20, 1)
            return render_to_response('reporteapus.html', {'user': user, 'form': form, 'capitulos': capitulos, 'subcapitulos': lista_subcapitulos, 'apus': pag, 'criterio': criterio, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual })
        return HttpResponseRedirect('/inverboy/home/')
    return HttpResponseRedirect('/inverboy/')