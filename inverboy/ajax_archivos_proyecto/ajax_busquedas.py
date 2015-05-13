# -*- encoding: utf-8 -*-
from dajaxice.core import dajaxice_functions
from dajax.core import Dajax
from django.template.loader import render_to_string
from inverboy.models import *
# PAGINACION
from inverboy.paginator import *
## CONSULTAS ANIDADAS
from django.db.models import Q


#---------------------------- USUARIOS ---------------------------------------------
# FUNCION PARA BUSCAR UNO O VARIOS USUARIOS
def buscar_usuarios2(request, pagina, criterio, cargo_usuario, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        #Se asigna la variable guardada en la session
        personas_seleccionadas = request.session['personas_seleccionadas']
        qry = "SELECT * FROM inverboy_usuario u, auth_user au WHERE u.user_ptr_id=au.id AND au.is_active=1"
        criterio = criterio.strip()
        if criterio != "":
            if criterio != '':
                criterio = criterio.replace("'",'"')
                try:
                    criterio = int(criterio)
                    qry = qry + " AND identificacion="+str(criterio)
                except:
                    qry = qry + " AND (CONCAT(first_name, ' ', last_name) LIKE '%%" + criterio + "%%' OR username LIKE '%%"+criterio+"%%')"
        if(cargo_usuario!="0"):
            qry = qry + " AND cargo='" + cargo_usuario + "'"
        usuarios = Usuario.objects.raw(qry)
        lista_usuarios = []
        for usuario in usuarios:
            lista_usuarios.append(usuario)
        pag = Paginador(request, lista_usuarios, 20, pagina)
        user = request.user
        render =  render_to_string('ajax/personassearchproyecto.html', {'user': user, 'lista_usuarios': pag, 'criterio': criterio, 'cargo_usuario': cargo_usuario, 'personas_seleccionadas': personas_seleccionadas, 'proyecto': proyecto })
        dajax.assign('#light','innerHTML', render)
        dajax.script("document.getElementById('light').style.display='block';")
        dajax.script("document.getElementById('fade').style.display='block';")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

#---------------------------- PROVEEDORES ---------------------------------------------

# FUNCION PARA BUSCAR UNO O VARIOS PROVEEDORES
def buscar_proveedores2(request, pagina, criterio):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proveedores = Proveedor.objects.all()
        if criterio != "":
            try:
                criterio = int(criterio)
                proveedores = proveedores.filter(identificacion=criterio)
            except:
                proveedores = proveedores.filter(Q(razon_social__icontains=criterio) | Q(nombre_comercial=criterio))
        pag = Paginador(request, proveedores, 20, pagina)
        user = request.user
        permisos_usuario = user.get_all_permissions()
        render = render_to_string('ajax/tabla_busqueda_proveedores.html', {'user': user, 'permisos': permisos_usuario, 'lista_proveedores': pag, 'criterio': criterio})
        dajax.assign('#light','innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


# Función para buscar uno o mas proveedores, en suministro add
def buscar_proveedores_suministro_add2(request, pagina, criterio):
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
            proveedores_agregar = request.session['proveedores_agregar']
            render = render_to_string('ajax/tabla_busqueda_proveedores.html', {'user': user, 'lista_proveedores': pag, 'criterio': criterio, 'proveedores_agregar': proveedores_agregar})
            dajax.assign('#light','innerHTML', render)
            dajax.script("document.getElementById('light').style.display='block';")
            dajax.script("document.getElementById('fade').style.display='block';")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------------------------- SUMINISTROS ---------------------------------------------

# Función para busqueda de suministros
def buscar_suministros2(request, pagina, clasificacion_general, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        lista_suministros = None
        try:
            lista_suministros = request.session['suministros']
        except :
            pass
        if lista_suministros != None:
            suministros = Suministro.objects.filter(estado_suministro=True)
            if clasificacion_general != '0':
                suministros = suministros.filter(clasificacion_general=clasificacion_general)
            criterio = criterio.strip()
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
            suministros_agregar = request.session['suministros_agregar']
            user = request.user
            render = render_to_string('ajax/tabla_busqueda_suministros.html', {'user': user, 'lista_suministros': pag, 'clasificacion_general': clasificacion_general, 'criterio': criterio, 'suministros_agregar': suministros_agregar, 'proyecto': proyecto })
            dajax.assign('#light','innerHTML', render)
            dajax.script("document.getElementById('light').style.display='block';")
            dajax.script("document.getElementById('fade').style.display='block';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

#---------------------------- APUS ---------------------------------------------
# FUNCION PARA BUSCAR UNO O VARIOS SUMINISTROS
def buscar_suministros_apu_add2(request, pagina, clasificacion_general, criterio):
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
            suministros = Suministro.objects.filter(estado_suministro=True)
            if clasificacion_general != '0':
                suministros = suministros.filter(clasificacion_general=clasificacion_general)
            criterio = criterio.strip()
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
            suministros_agregar = request.session['suministros_agregar']
            render = render_to_string('ajax/busquedasuministrosapuadd.html', {'user': user, 'lista_suministros': pag, 'clasificacion_general': clasificacion_general, 'criterio': criterio, 'suministros_agregar': suministros_agregar})
            dajax.assign('#light','innerHTML', render)
            dajax.script("document.getElementById('light').style.display='block';")
            dajax.script("document.getElementById('fade').style.display='block';")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------------------------- APUS PROYECTO ---------------------------------------------

# FUNCION PARA BUSCAR UNO O VARIOS APU'S
def buscar_apus_proyecto2(request, pagina, capitulo_id, subcapitulo_id, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        apus = ApuProyecto.objects.filter(proyecto=proyecto)
        if capitulo_id != '0':
            capitulo_actual = CapituloApuProyecto.objects.get(id=capitulo_id, tipo_capitulo=1)
            if subcapitulo_id != '0':
                capitulo_actual = CapituloApuProyecto.objects.get(id=subcapitulo_id, tipo_capitulo=2)
            apus = apus.filter(capitulo=capitulo_actual)
        if criterio != "":
            apus = apus.filter(Q(nombre_apu__icontains=criterio))
        lista_apus = []
        for apu in apus:
            lista_apus.append(apu)
        pag = Paginador(request, lista_apus, 20, pagina)
        user = request.user
        render =  render_to_string('ajax/apusproyectosearchrequisicion.html', {'user': user, 'apus': pag, 'criterio': criterio, 'proyecto': proyecto })
        dajax.assign('#id_reporte_apus','innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#Función para buscar items de una orden de compra informe_recepción_add
def buscar_items_orden_compra_informe_recepcion2(request, pagina, criterio, orden_compra_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros_informe_recepcion = None
        try:
            suministros_informe_recepcion = request.session['suministros_informe_recepcion']
        except :
            pass
        if suministros_informe_recepcion != None:
            orden_compra = OrdenCompra.objects.get(id=orden_compra_id)
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
                    #suministros_orden_compra.append(suministro_tmp)
                    suministros_orden_compra.append({'suministro': suministro_tmp, 'cantidad_nuevo_informe': ''})
            for suministro_informe_recepcion in suministros_informe_recepcion:
                for suministro_orden_compra in suministros_orden_compra:
                    if suministro_informe_recepcion['id'] == suministro_orden_compra['suministro'].suministro.suministro.suministro.id:
                        suministro_orden_compra['cantidad_nuevo_informe'] = suministro_informe_recepcion['cantidad']
            pag = Paginador(request, suministros_orden_compra, 20, pagina)
            user = request.user
            render =  render_to_string('ajax/suministrosordencomprasearchinformerecepcion.html', {'user': user, 'suministros': pag, 'criterio': criterio, 'orden_compra': orden_compra, 'proyecto': proyecto })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#Función para buscar suministros en almacen informe_salida_add
def buscar_suministros_almacen_informe_salida2(request, pagina, criterio_suministro, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros_informe_salida = None
        try:
            suministros_informe_salida = request.session['suministros_informe_salida']
        except :
            pass
        if suministros_informe_salida != None:
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
            pag = Paginador(request, suministros_almacen, 20, pagina)
            user = request.user
            render = render_to_string('ajax/suministrosalmacensearchinformesalida.html', {'user': user, 'suministros': pag, 'criterio_suministro': criterio_suministro, 'proyecto': proyecto })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def buscar_proveedores_suministro_contizacion_add2(request, suministro_id, criterio, proyecto_id):
    import datetime
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        #Verifica si el suministro es un material
        if Suministro.objects.get(id=suministro_id).clasificacion_general == 'Material':
            suministro_comprar = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(suministro_id=suministro_id)[0]
        #Si no el suministro no es un material
        else:
            suministro_comprar = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(suministro_id=suministro_id, tipo_cotizacion=2)[0]

        criterio = criterio.strip()
        pag = Paginador(request, suministro_comprar.suministro.suministro.get_proveedores_activos_suministro(criterio=criterio), 20, 1)

        now = datetime.datetime.now()
        fecha_actual = now.strftime("%Y-%m-%d")
        render = render_to_string('ajax/suministrocotizarproveedoressearch.html', {'user': user, 'suministro_proveedores': pag, 'suministro_comprar': suministro_comprar, 'fecha_actual': fecha_actual, 'criterio_proveedor': criterio, 'proyecto': proyecto } )
        dajax.assign('#light', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#Función para buscar suministros requeridos cotizacion_add
def buscar_suministros_proveedor_contizacion_add2(request, criterio, proveedor_id, proyecto_id):
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
            proveedor = Proveedor.objects.get(id=proveedor_id)

            criterio = criterio.strip()

            #Visualiza los suministros requeridos con la cantidad a cotizar
            suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(criterio=criterio, proveedor_id=proveedor_id)
            suministros_comprar = []
            for suministro_requisiciones in suministros_requisiciones:
                suministro_comprar = {'suministro': suministro_requisiciones, 'cantidad_nueva_cotizacion': '', 'observaciones': suministro_requisiciones.observaciones}
                for suministro_cotizacion in suministros_cotizacion:
                    if suministro_requisiciones.suministro.suministro.id == suministro_cotizacion['suministro_id']:
                        suministro_comprar['cantidad_nueva_cotizacion'] = suministro_cotizacion['cantidad']
                        suministro_comprar['observaciones'] = suministro_cotizacion['observaciones']
                suministros_comprar.append(suministro_comprar)

            pag = Paginador(request, suministros_comprar, 20, 1)
            user = request.user
            render = render_to_string('ajax/suministrosrequisicionesproveedorsearch.html', {'user': user, 'suministros_requisiciones': pag, 'proveedor': proveedor, 'criterio': criterio, 'proyecto': proyecto } )
            dajax.assign('#light', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


# FUNCION PARA BUSCAR SUMINISTROS APU PROYECTO COTIZACION ORDEN SERVICIO ADD
def buscar_suministros_proveedor_contizacion_orden_servicio_add2(request, criterio, proveedor_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)

        proveedor = Proveedor.objects.get(id=proveedor_id)

        criterio = criterio.strip()

        criterio = criterio.replace("'",'"')
                        
        qry = "SELECT sr.id, sr.suministro_id, SUM(sr.cantidad_requerida) AS cantidad_requerida, SUM(sr.cantidad_comprada) AS cantidad_comprada, SUM(sr.cantidad_almacen) AS cantidad_almacen, CONCAT(sr.observaciones) AS observaciones, requisicion_id FROM inverboy_suministro s, inverboy_suministroapuproyecto sap, inverboy_suministrorequisicion sr, inverboy_requisicion r WHERE sap.suministro_id = s.id AND sr.suministro_id = sap.id AND sr.cantidad_comprada < sr.cantidad_requerida AND r.proyecto_id = "+ str(proyecto_id) +" AND sr.requisicion_id = r.id AND s.nombre LIKE '%%" + criterio + "%%' AND s.id IN ( SELECT suministro_id FROM inverboy_suministroproveedor WHERE proveedor_id = " + str(proveedor_id) + " ) AND s.clasificacion_general != 'Material' GROUP BY s.id ORDER BY s.nombre" #Consulta

        suministros_requisiciones = SuministroRequisicion.objects.raw(qry)

        suministros_comprar = []
        for suministro_requisiciones in suministros_requisiciones:
            suministro_tmp = {'suministro': suministro_requisiciones, 'cantidad_nueva_cotizacion': ''}

            # suministro_tmp = suministro_requisiciones
            suministro_adicionado = False
            for suministro_tmp2 in suministros_comprar:
                if suministro_tmp2['suministro'].suministro.suministro.id == suministro_tmp['suministro'].suministro.suministro.id:
                    suministro_tmp2['suministro'].cantidad_requerida = round(suministro_tmp2['suministro'].cantidad_requerida + (round(suministro_tmp['suministro'].cantidad_requerida-suministro_tmp['suministro'].cantidad_comprada, 2)), 2)
                    suministro_adicionado = True
            if suministro_adicionado == False:
                suministro_tmp['suministro'].cantidad_requerida = round(suministro_tmp['suministro'].cantidad_requerida - suministro_tmp['suministro'].cantidad_comprada, 2)
                suministro_tmp['suministro'].cantidad_comprada = 0
                suministros_comprar.append(suministro_tmp)

        suministros_cotizacion = request.session['suministros_cotizacion']

        for suministro_cotizacion in suministros_cotizacion:
            for suministro_comprar in suministros_comprar:
                if suministro_cotizacion['suministro_id'] == suministro_comprar['suministro'].suministro.suministro.id:
                    suministro_comprar['cantidad_nueva_cotizacion'] = suministro_cotizacion['cantidad']
        pag = Paginador(request, suministros_comprar, 20, 1)
        user = request.user
        permisos_usuario = user.get_all_permissions()
        render = render_to_string('ajax/suministrosrequisicionesproveedorsearchordenservicioadd.html', {'user': user, 'permisos': permisos_usuario, 'suministros_requisiciones': pag, 'proveedor': proveedor, 'criterio': criterio, 'proyecto': proyecto } )
        dajax.assign('#light', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


# Función para buscar suministros de un proveedor especifico
def buscar_suministros_proveedor_contizacion_orden_servicio_add2(request, criterio, proveedor_id, proyecto_id):
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
            for suministro_requisiciones in suministros_requisiciones:
                suministro_comprar = {'suministro': suministro_requisiciones, 'cantidad_nueva_cotizacion': ''}
                for suministro_cotizacion in suministros_cotizacion:
                    if suministro_requisiciones.suministro.suministro.id == suministro_cotizacion['suministro_id']:
                        suministro_comprar['cantidad_nueva_cotizacion'] = suministro_cotizacion['cantidad']
                suministros_comprar.append(suministro_comprar)

            pag = Paginador(request, suministros_comprar, 20, 1)

            render = render_to_string('ajax/suministrosrequisicionesproveedorsearchordenservicioadd.html', {'user': user, 'suministros_requisiciones': pag, 'proveedor': proveedor, 'criterio': criterio, 'proyecto': proyecto } )
            dajax.assign('#light', 'innerHTML', render)
            dajax.script("document.getElementById('light').style.display='block';")
            dajax.script("document.getElementById('fade').style.display='block';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#Función para buscar items orden de servicio-cotediarioobra_add
def buscar_items_orden_servicio_corte_diario_obra2(request, pagina, criterio, orden_servicio_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros_corte_diario_obra = None
        try:
            suministros_corte_diario_obra = request.session['suministros_corte_diario_obra']
        except :
            pass
        if suministros_corte_diario_obra != None:
            orden_servicio = OrdenServicio.objects.get(id=orden_servicio_id)
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
                    suministros_orden_servicio.append({'suministro': suministro_tmp, 'cantidad_nuevo_informe': '', 'porcentaje_entregado': round(((round(100*suministro_tmp.cantidad_entregada, 2))/suministro_tmp.cantidad), 2), 'nuevo_porcentaje_entregado': ''})

            for suministro_corte_diario_obra in suministros_corte_diario_obra:
                for suministro_orden_servicio in suministros_orden_servicio:
                    if suministro_corte_diario_obra['id'] == suministro_orden_servicio['suministro'].suministro.suministro.suministro.id:
                        suministro_orden_servicio['cantidad_nuevo_informe'] = suministro_corte_diario_obra['cantidad']
                        suministro_orden_servicio['nuevo_porcentaje_entregado'] = suministro_corte_diario_obra['nuevo_porcentaje_entregado']
            pag = Paginador(request, suministros_orden_servicio, 20, pagina)
            render =  render_to_string('ajax/suministrosordenserviciosearchcortediarioobra.html', {'user': user, 'suministros': pag, 'criterio': criterio, 'orden_servicio': orden_servicio, 'proyecto': proyecto })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#Función para buscar items orden de giro_proyecto_add
def buscar_items_orden_giro_proyecto_add2(request, pagina, criterio, proyecto_id):
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
            criterio = criterio.strip()
            suministros_pendientes = proyecto.get_suministros_pendientes_comprar(criterio=criterio, clasificacion_general=['Indirectos'])
            suministros_requisiciones = []
            for suministro_pendientes in suministros_pendientes:
                suministro_requisicion = {'suministro': suministro_pendientes, 'cantidad_nueva_orden_giro': '', 'observaciones': ''}
                for suministro_orden_giro in suministros_orden_giro:
                    if suministro_pendientes.id == suministro_orden_giro['suministro_id']:
                        suministro_requisicion['cantidad_nueva_orden_giro'] = suministro_orden_giro['cantidad']
                        suministro_requisicion['observaciones'] = suministro_orden_giro['observaciones']
                suministros_requisiciones.append(suministro_requisicion)
            pag = Paginador(request, suministros_requisiciones, 20, pagina)
            render =  render_to_string('ajax/suministrosrequisicionessearchordengiroadd.html', {'user': user, 'suministros_requisiciones': pag, 'criterio': criterio, 'proyecto': proyecto})
            dajax.assign('#id_reporte_suministros_requisiciones','innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#Función para buscar proveedores orden de giro_proyecto_add
def buscar_proveedores_orden_giro_proyecto_add2(request, pagina, criterio, proyecto_id):
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
            #Visualiza los proveedores que tienen asociado el suministro
            criterio = criterio.strip()
            proveedores = []
            suministros_requisiciones = proyecto.get_suministros_pendientes_comprar(clasificacion_general=['Indirectos'])
            for suministro_requisicion in suministros_requisiciones:
                proveedores_suministro = suministro_requisicion.suministro.suministro.get_proveedores_activos_suministro(criterio)
                for proveedor_suministro in proveedores_suministro:
                    if proveedor_suministro.proveedor not in proveedores:
                        proveedores.append(proveedor_suministro.proveedor)
            pag = Paginador(request, proveedores, 20, pagina)
            render =  render_to_string('ajax/proveedoressearchordengiroadd.html', {'user': user, 'proveedores': pag, 'criterio': criterio, 'proyecto': proyecto})
            dajax.assign('#light','innerHTML', render)
            dajax.script("document.getElementById('fade').style.display='block';")
            dajax.script("document.getElementById('light').style.display='block';")
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def buscar_items_acta_conformidad_add2(request, pagina, criterio, orden_giro_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        items_acta_conformidad = None
        try:
            items_acta_conformidad = request.session['items_acta_conformidad']
        except :
            pass
        if items_acta_conformidad != None:
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
            user = request.user
            render =  render_to_string('ajax/itemsordengirosearchactaconformidad.html', {'user': user, 'items': pag, 'criterio': criterio, 'orden_giro': orden_giro, 'proyecto': proyecto })
            dajax.assign('#id_reporte_items','innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()