# -*- encoding: utf-8 -*-
from dajaxice.core import dajaxice_functions
from dajax.core import Dajax
from django.template.loader import render_to_string
from inverboy.models import *
# PAGINACION
from inverboy.paginator import *
## CONSULTAS ANIDADAS
from django.db.models import Q
from django.template.loader import render_to_string

# Libreria de validaciones
#from validator.core import Validator, Field
#from validator.rules import *


#---------- PAGINACION USUARIOS ----------------------------------------
def paginar_grupos_usuario2(request, pagina, html, criterio):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        grupos = Group.objects.all()
        if criterio != "":
            grupos = grupos.filter(Q(name__icontains=criterio))
        pag = Paginador(request, grupos, 20, pagina)
        user = request.user
        render = render_to_string('ajax/grupousuariosearch.html', {'user': user, 'grupos': pag, 'criterio': criterio})
        dajax.assign('#id_reporte_grupos', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_usuarios2(request, pagina, html, criterio):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        qry = "SELECT * FROM inverboy_usuario, auth_user WHERE user_ptr_id=id"
        if criterio != "":
            if criterio != '':
                criterio = criterio.replace("'",'"')
                try:
                    criterio = int(criterio)
                    qry = qry + " AND identificacion="+str(criterio)
                except:
                    qry = qry + " AND (CONCAT(first_name, ' ', last_name) LIKE '%%" + criterio + "%%' OR username LIKE '%%"+criterio+"%%')"
        usuarios = Usuario.objects.raw(qry)
        lista_usuarios = []
        for usuario in usuarios:
            lista_usuarios.append(usuario)
        pag = Paginador(request, lista_usuarios, 20, pagina)
        user = request.user
        render = render_to_string('ajax/usuariosearch.html',{'user': user, 'usuarios': pag, 'criterio': criterio} )
        dajax.assign('#id_reporte_usuarios', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

#---------- PAGINACION PROVEEDORES ----------------------------------------

def paginar_proveedores2(request, pagina, html, criterio):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proveedores = Proveedor.objects.all()
        criterio = criterio.strip()
        if criterio != "":
            try:
                criterio = int(criterio)
                proveedores = proveedores.filter(identificacion=criterio)
            except:
                proveedores = proveedores.filter(Q(razon_social__icontains=criterio) | Q(nombre_comercial__icontains=criterio))
        pag = Paginador(request, proveedores, 20, pagina)
        user = request.user
        render = render_to_string('ajax/proveedorsearch.html', {'user': user, 'proveedores': pag, 'criterio': criterio} )
        dajax.assign('#id_reporte_proveedores', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_proveedores_compras2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        qry = "SELECT p.* FROM inverboy_suministroproveedor sp, inverboy_proveedor p WHERE sp.proveedor_id = p.id AND p.estado_proveedor = TRUE AND sp.suministro_id IN (	SELECT s.id	FROM inverboy_suministrorequisicion sr, inverboy_requisicion r, inverboy_suministroapuproyecto sap, inverboy_suministro s	WHERE sap.suministro_id = s.id AND sr.suministro_id = sap.id	AND sr.cantidad_comprada < sr.cantidad_requerida	AND sr.requisicion_id = r.id	AND r.proyecto_id = " + str(proyecto_id) + "    AND r.estado = 2	AND s.clasificacion_general = 'Material'	GROUP BY s.id   )"
        criterio = criterio.strip()
        if criterio != "":
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
        pag = Paginador(request, lista_proveedores, 20, pagina)
        render = render_to_string('ajax/comprasproveedoressearch.html', {'user': user, 'proveedores': pag, 'criterio': criterio, 'proyecto': proyecto } )
        dajax.assign('#id_reporte_proveedores', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------- PAGINACION SUMINISTROS ----------------------------------------

def paginar_categorias_suministro2(request, pagina, html, criterio):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        categorias = Categoria.objects.filter(tipo=1)
        if criterio != "":
            categorias = categorias.filter(Q(nombre__icontains=criterio))
        pag = Paginador(request, categorias, 20, pagina)
        user = request.user
        render = render_to_string('ajax/categoriasearch.html', {'user': user, 'categorias': pag, 'criterio': criterio})
        dajax.assign('#id_reporte_categorias', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

def paginar_especificaciones_suministro2(request, pagina, html, categoria_id, criterio):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        categoria = Categoria.objects.get(id=categoria_id, tipo=1)
        especificaciones = Categoria.objects.filter(tipo=2, categoria_asociada=categoria)
        if criterio != "":
            especificaciones = especificaciones.filter(Q(nombre__icontains=criterio))
        pag = Paginador(request, especificaciones, 20, pagina)
        user = request.user
        render = render_to_string('ajax/especificacionsearch.html', {'user': user, 'especificaciones': pag, 'categoria': categoria, 'criterio': criterio})
        dajax.assign('#id_reporte_especificaciones', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

def paginar_tipos_suministro2(request, pagina, html, especificacion_id, criterio):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        especificacion = Categoria.objects.get(id=especificacion_id, tipo=2)
        categoria = especificacion.categoria_asociada
        tipos = Categoria.objects.filter(tipo=3, categoria_asociada=especificacion)
        if criterio != "":
            tipos = tipos.filter(Q(nombre__icontains=criterio))
        pag = Paginador(request, tipos, 20, pagina)
        user = request.user
        render = render_to_string('ajax/tiposearch.html', {'user': user, 'tipos': pag, 'categoria': categoria, 'especificacion': especificacion, 'criterio': criterio})
        dajax.assign('#id_reporte_tipos', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

def paginar_proveedores_suministro_add2(request, pagina):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        permisos_usuario = user.get_all_permissions()
        proveedores = request.session['proveedores']
        pag = Paginador(request, proveedores, 20, pagina)
        render = render_to_string('ajax/proveedoressuministro.html', {'user': user, 'permisos': permisos_usuario, 'suministro_proveedores': pag })
        dajax.assign('#id_reporte_proveedores','innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

def paginar_suministros2(request, pagina, html, criterio):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        suministros = Suministro.objects.all()
        if criterio != "":
            suministros = suministros.filter(Q(nombre__icontains=criterio) | Q(sinonimos__icontains=criterio))
        pag = Paginador(request, suministros, 20, pagina)
        user = request.user
        render = render_to_string('ajax/suministrosearch.html', {'user': user, 'suministros': pag, 'criterio': criterio} )
        dajax.assign('#id_reporte_suministros', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

#---------- PAGINACION APUS ----------------------------------------

def paginar_suministros_apu_add2(request, pagina):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        permisos_usuario = user.get_all_permissions()
        suministros = request.session['suministros']
        pag = Paginador(request, suministros, 20, pagina)
        render = render_to_string('ajax/suministrosapuadd.html', {'user': user, 'permisos': permisos_usuario, 'suministros_apu': pag })
        dajax.assign('#id_reporte_suministros','innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_suministros_apu_details2(request, apu_id, pagina):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        apu = Apu.objects.get(id=apu_id)
        suministros = apu.suministroapu_set.all()
        pag = Paginador(request, suministros, 20, pagina)
        render = render_to_string('ajax/suministrosapudetails.html', {'user': user, 'apu': apu, 'suministros_apu': pag })
        dajax.assign('#id_reporte_suministros','innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_capitulos_apus2(request, pagina, html, criterio):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        capitulos = Capitulo.objects.filter(tipo_capitulo=1)
        if criterio != "":
            capitulos = capitulos.filter(Q(nombre_capitulo__icontains=criterio))
        pag = Paginador(request, capitulos, 20, pagina)
        user = request.user
        render = render_to_string('ajax/capitulosearch.html', {'user': user, 'capitulos': pag, 'criterio': criterio})
        dajax.assign('#id_reporte_capitulos', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

def paginar_subcapitulos_apus2(request, pagina, html, capitulo_id, criterio):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        capitulo = Capitulo.objects.get(id=capitulo_id, tipo_capitulo=1)
        subcapitulos = Capitulo.objects.filter(tipo_capitulo=2, capitulo_asociado=capitulo)
        if criterio != "":
            subcapitulos = subcapitulos.filter(Q(nombre_capitulo__icontains=criterio))
        pag = Paginador(request, subcapitulos, 20, pagina)
        user = request.user
        render = render_to_string('ajax/subcapitulosearch.html', {'user': user, 'subcapitulos': pag, 'capitulo': capitulo, 'criterio': criterio})
        dajax.assign('#id_reporte_subcapitulos', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

def paginar_apus2(request, pagina, html, criterio, capitulo_id, subcapitulo_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        apus = Apu.objects.all()
        capitulo_actual = Capitulo()
        subcapitulo_actual= Capitulo()
        capitulos = Capitulo.objects.filter(tipo_capitulo=1)
        subcapitulos = []
        if capitulo_id != 'None':
            capitulo_actual = Capitulo.objects.get(tipo_capitulo=1, id=capitulo_id)
            if subcapitulo_id != 'None':
                subcapitulo_actual = Capitulo.objects.get(tipo_capitulo=2, id=subcapitulo_id)
                apus = apus.filter(capitulo=subcapitulo_actual)
            subcapitulos = Capitulo.objects.filter(tipo_capitulo=2, capitulo_asociado=capitulo_actual)
        if criterio != "":
            apus = apus.filter(Q(nombre_apu__icontains=criterio))
        pag = Paginador(request, apus, 20, pagina)
        user = request.user
        render = render_to_string('ajax/apusearch.html', {'user': user, 'apus': pag, 'capitulos': capitulos, 'subcapitulos': subcapitulos, 'criterio': criterio, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual } )
        dajax.assign('#id_reporte_apus', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_apus_maestros_proyecto2(request, pagina, criterio, capitulo_id, subcapitulo_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        try:
            proyecto = Proyecto.objects.get(id=proyecto_id)
        except:
            return
        apus = Apu.objects.filter(estado_apu=True)
        capitulo_actual = Capitulo()
        subcapitulo_actual= Capitulo()
        capitulos = Capitulo.objects.filter(tipo_capitulo=1, estado_capitulo=True)
        subcapitulos = []
        if capitulo_id != 'None':
            capitulo_actual = Capitulo.objects.get(tipo_capitulo=1, id=capitulo_id)
            if subcapitulo_id != 'None':
                subcapitulo_actual = Capitulo.objects.get(tipo_capitulo=2, id=subcapitulo_id)
                apus = apus.filter(capitulo=subcapitulo_actual)
            subcapitulos = Capitulo.objects.filter(tipo_capitulo=2, capitulo_asociado=capitulo_actual)
        if criterio != "":
            apus = apus.filter(Q(nombre_apu__icontains=criterio))
        pag = Paginador(request, apus, 20, pagina)
        user = request.user
        render = render_to_string('ajax/apusmaestrosearch.html', {'user': user, 'apus': pag, 'capitulos': capitulos, 'subcapitulos': subcapitulos, 'criterio': criterio, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'proyecto': proyecto } )
        dajax.assign('#id_reporte_apus', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------- PAGINACION PROYECTOS ----------------------------------------

def paginar_proyectos2(request, pagina, criterio):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if user.is_superuser or user.is_staff:
            proyectos = Proyecto.objects.all()
        else:
            usuario = Usuario.objects.get(id=user.id)
            proyectos = usuario.lista_proyectos_vinculados()
        criterio = criterio.strip()
        if criterio != '':
            proyectos = proyectos.filter(Q(nombre__icontains=criterio))
        pag = Paginador(request, proyectos, 20, pagina)
        render = render_to_string('ajax/proyectossearch.html' , {'user': user, 'proyectos': pag, 'criterio': criterio})
        dajax.assign('#id_proyectos', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------- PAGINACION APUS PROYECTO ----------------------------------------
def paginar_capitulos_apu_proyecto2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        try:
            proyecto = Proyecto.objects.get(id=proyecto_id)
        except:
            #return HttpResponseRedirect('/inverboy/home/')
            return
        capitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=1, proyecto=proyecto)
        if criterio != "":
            try:
                criterio = int(criterio)
                capitulos = capitulos.filter(Q(codigo=criterio))
            except:
                capitulos = capitulos.filter(Q(nombre_capitulo__icontains=criterio))
        pag = Paginador(request, capitulos, 20, pagina)
        user = request.user
        render = render_to_string('ajax/capitulosapuproyectosearch.html', {'user': user, 'capitulos': pag, 'criterio': criterio, 'proyecto': proyecto })
        dajax.assign('#id_reporte_capitulos', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_subcapitulos_apu_proyecto2(request, pagina, criterio, proyecto_id, capitulo_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        try:
            proyecto = Proyecto.objects.get(id=proyecto_id)
            capitulo = CapituloApuProyecto.objects.get(id=capitulo_id)
            if proyecto != capitulo.proyecto:
                return
        except:
            return
        subcapitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=2, capitulo_asociado=capitulo, proyecto=proyecto)
        if criterio != "":
            try:
                criterio = int(criterio)
                subcapitulos = subcapitulos.filter(Q(codigo=criterio))
            except:
                subcapitulos = subcapitulos.filter(Q(nombre_capitulo__icontains=criterio))
        pag = Paginador(request, subcapitulos, 20, pagina)
        user = request.user
        render = render_to_string('ajax/subcapitulosapuproyectosearch.html', {'user': user, 'subcapitulos': pag, 'criterio': criterio, 'proyecto': proyecto, 'capitulo': capitulo })
        dajax.assign('#id_reporte_subcapitulos', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


# FUNCION PARA CARGAR LOS SUBCAPITULOS DE UN CAPITULO DE APU DE PROYECTO ESPECIFICO
def cargar_subcapitulos_apus_proyectos2(request, option, elemento):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        subcapitulos = CapituloApuProyecto.objects.filter(tipo_capitulo=2, capitulo_asociado = int(option), estado_capitulo=1)
        # lista_subcapitulos = []
        out = '<option value="0">----</option>'
        for subcapitulo in subcapitulos:
            out = out + '<option value="'+str(subcapitulo.id)+'">'+subcapitulo.nombre_capitulo+'</option>'
        dajax.assign('#'+elemento,'innerHTML', out)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_suministros_apu_proyecto_add2(request, pagina, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            pag = Paginador(request, suministros, 20, pagina)
            apu_manejo_estandar = request.session['apu_manejo_estandar']
            suministro_estandar = request.session['id_suministro_estandar']
            render = render_to_string('ajax/suministrosapuproyectoadd.html', {'user': user, 'suministros_apu': pag, 'apu_manejo_estandar': apu_manejo_estandar, 'suministro_estandar': suministro_estandar, 'proyecto': proyecto })
            dajax.assign('#id_reporte_suministros','innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/' + str(proyecto.id) + '/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_apus_proyecto2(request, pagina, html, criterio, capitulo_id, subcapitulo_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        apus = proyecto.apuproyecto_set.all()
        capitulo_actual = CapituloApuProyecto()
        subcapitulo_actual= CapituloApuProyecto()
        capitulos = proyecto.capituloapuproyecto_set.filter(tipo_capitulo=1)
        subcapitulos = []
        if capitulo_id != 'None':
            capitulo_actual = proyecto.capituloapuproyecto_set.get(tipo_capitulo=1, id=capitulo_id)
            if subcapitulo_id != 'None':
                subcapitulo_actual = proyecto.capituloapuproyecto_set.get(tipo_capitulo=2, id=subcapitulo_id)
                apus = apus.filter(capitulo=subcapitulo_actual)
            else:
                apus = apus.filter(capitulo=capitulo_actual)
            subcapitulos = proyecto.capituloapuproyecto_set.filter(tipo_capitulo=2, capitulo_asociado=capitulo_actual)
        criterio = criterio.strip()
        if criterio != '':
            apus = apus.filter(Q(nombre_apu__icontains=criterio))
        pag = Paginador(request, apus, 20, pagina)
        user = request.user
        render = render_to_string('ajax/apusproyectosearch.html', {'user': user, 'apus': pag, 'capitulos': capitulos, 'subcapitulos': subcapitulos, 'criterio': criterio, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'proyecto': proyecto } )
        dajax.assign('#id_reporte_apus', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_suministros_apu_proyecto2(request, pagina, apu_proyecto_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        apu_proyecto = proyecto.apuproyecto_set.get(id=apu_proyecto_id)
        suministros = apu_proyecto.suministroapuproyecto_set.all()
        pag = Paginador(request, suministros, 20, pagina)
        render = render_to_string('ajax/suministrosapuproyectodetalles.html', {'user': user, 'apu': apu_proyecto, 'suministros': pag, 'proyecto': proyecto })
        dajax.assign('#id_reporte_suministros','innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------- PAGINACION APUS PROYECTO PARA UNA NUEVA REQUISICION----------------------------------------
def paginar_apus_proyecto_requisicion2(request, pagina, criterio, tipo_busqueda, capitulo_id, subcapitulo_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        carrito = None
        try:
            carrito = request.session['carrito']
        except :
            pass
        if carrito != None:
            apus = proyecto.lista_apus_sin_indirectos()
            capitulo_actual = CapituloApuProyecto()
            subcapitulo_actual= CapituloApuProyecto()
            capitulos = proyecto.capituloapuproyecto_set.filter(tipo_capitulo=1, estado_capitulo=True)
            subcapitulos = []
            criterio = criterio.strip()
            criterio = criterio.replace("'",'"')
            if tipo_busqueda == 1:
                if capitulo_id != 'None':
                    capitulo_actual = proyecto.capituloapuproyecto_set.get(tipo_capitulo=1, estado_capitulo=True, id=capitulo_id)
                    subcapitulos = proyecto.capituloapuproyecto_set.filter(tipo_capitulo=2, estado_capitulo=True, capitulo_asociado=capitulo_actual)
                    if subcapitulo_id != 'None':
                        subcapitulo_actual = proyecto.capituloapuproyecto_set.get(tipo_capitulo=2, estado_capitulo=True, id=subcapitulo_id)
                if capitulo_actual != CapituloApuProyecto() and subcapitulo_actual == CapituloApuProyecto():
                    apus = apus.filter(Q(capitulo=capitulo_actual))
                if subcapitulo_actual != CapituloApuProyecto():
                    apus = apus.filter(Q(capitulo=subcapitulo_actual))
                apus = apus.filter(Q(nombre_apu__icontains=criterio))
            elif tipo_busqueda == 2:
                qry = "SELECT ap.* FROM inverboy_apuproyecto ap WHERE ap.estado_apu = TRUE AND ap.proyecto_id = " + str(proyecto_id) + " AND ap.id IN (	SELECT sap.apu_proyecto_id	FROM inverboy_suministroapuproyecto sap, inverboy_suministro s	WHERE sap.suministro_id = s.id	AND s.clasificacion_general != 'Indirectos'	AND s.nombre LIKE '%%" + criterio + "%%'	GROUP BY sap.apu_proyecto_id)"
                apus = list(proyecto.apuproyecto_set.raw(qry))
            pag = Paginador(request, apus, 20, pagina)
            user = request.user
            render = render_to_string('ajax/apusproyectosearchrequisicion.html', {'user': user, 'apus': pag, 'capitulos': capitulos, 'subcapitulos': subcapitulos, 'criterio': criterio, 'capitulo_actual': capitulo_actual, 'subcapitulo_actual': subcapitulo_actual, 'tipo_busqueda': tipo_busqueda, 'proyecto': proyecto } )
            dajax.assign('#id_reporte_apus', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------- PAGINACION REQUISICIONES POR APROBAR PROYECTO----------------------------------------
def paginar_requisiciones_aprobar2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        requisiciones = proyecto.lista_requisiciones(tipo=[1], estado=[1], criterio=criterio)
        pag = Paginador(request, requisiciones, 20, pagina)
        user = request.user
        render = render_to_string('ajax/requisicionesaprobarsearch.html', {'user': user, 'requisiciones': pag, 'criterio': criterio, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_requisiciones', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------- PAGINACION REQUISICIONES PROYECTO----------------------------------------
def paginar_requisiciones2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        fecha_inicial = fecha_inicial.strip()
        fecha_final = fecha_final.strip()
        fecha_inicial = {'valor': fecha_inicial, 'error': ''}
        fecha_final = {'valor': fecha_final, 'error': ''}
        parametro_fecha_inicial = ''
        parametro_fecha_final = ''

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
        pag = Paginador(request, requisiciones, 20, pagina)
        user = request.user
        render = render_to_string('ajax/requisicionessearch.html', {'user': user, 'requisiciones': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_requisiciones', 'innerHTML', render)
        dajax.script("Calendar.setup({inputField:'id_fecha_inicial',ifFormat:'%Y-%m-%d',button:'lanzador_f_i'});")
        dajax.script("Calendar.setup({inputField:'id_fecha_final',ifFormat:'%Y-%m-%d',button:'lanzador_f_f'});")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_suministros_apu_proyecto_requisicion_add2(request, pagina, criterio, apu_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        #Revisa si el carrito de la nueva requisición existe
        carrito = None
        try:
            carrito = request.session['carrito']
        except :
            pass
        if carrito != None:
            apu = ApuProyecto.objects.get(id=apu_id, proyecto=proyecto)
            suministros = apu.suministroapuproyecto_set.all()
            criterio = criterio.strip()
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
            pag = Paginador(request, suministros_apu, 20, pagina)
            user = request.user
            render = render_to_string('ajax/contenidoapuproyectodetails.html', {'user': user, 'suministros_apu': pag, 'criterio': criterio, 'apu': apu, 'proyecto': proyecto} )
            dajax.assign('#id_contenido_suministros_apu', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_suministros_requisicion_add2(request, pagina, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        #Revisa si el carrito de la nueva requisición existe
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
            pag = Paginador(request, suministros_requisicion, 20, pagina)
            user = request.user
            render = render_to_string('ajax/nuevarequisiciondetails.html', {'user': user, 'suministros_requisicion': pag, 'proyecto': proyecto} )
            dajax.assign('#id_contenido', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_suministros_requisicion2(request, pagina, requisicion_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        requisicion = proyecto.requisicion_set.get(id=requisicion_id)
        suministros = requisicion.suministrorequisicion_set.all()
        pag = Paginador(request, suministros, 20, pagina)
        user = request.user
        render = render_to_string('ajax/suministrosrequisicionsearch.html', {'user': user, 'requisicion': requisicion, 'suministros': pag, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_suministros', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_apus_proyecto_requisicion_indirectos_add2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        carrito = None
        try:
            carrito = request.session['carrito']
        except :
            pass
        if carrito != None:
            criterio = criterio.strip()
            apus = proyecto.lista_apus_indirectos(criterio)
            pag = Paginador(request, apus, 20, pagina)
            user = request.user
            render = render_to_string('ajax/apusproyectosearchrequisicionindirectosadd.html', {'user': user, 'apus': pag, 'criterio': criterio, 'proyecto': proyecto } )
            dajax.assign('#id_reporte_apus', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_suministros_apu_proyecto_requisicion_indirectos_add2(request, pagina, criterio, apu_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        #Revisa si el carrito de la nueva requisición existe
        carrito = None
        try:
            carrito = request.session['carrito']
        except :
            pass
        if carrito != None:
            apu = proyecto.apuproyecto_set.get(id=apu_id)
            suministros = apu.suministroapuproyecto_set.all()
            criterio = criterio.strip()
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
            pag = Paginador(request, suministros_apu, 20, pagina)
            user = request.user
            render = render_to_string('ajax/contenidoapuproyectodetailsrequisicionindirectosadd.html', {'user': user, 'suministros_apu': pag, 'criterio': criterio, 'apu': apu, 'proyecto': proyecto} )
            dajax.assign('#id_contenido_suministros_apu', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_suministros_requisicion_indirectos_add2(request, pagina, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        #Revisa si el carrito de la nueva requisición existe
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
            pag = Paginador(request, suministros_requisicion, 20, pagina)
            user = request.user
            render = render_to_string('ajax/nuevarequisicionindirectosdetails.html', {'user': user, 'suministros_requisicion': pag, 'proyecto': proyecto} )
            dajax.assign('#id_contenido', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#PAGINACIÓN SUMINISTROS DE REQUISICIONES PARA UNA NUEVA COTIZACIÓN
def paginar_suministros_requisiciones_cotizacion_add2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        pag = Paginador(request, proyecto.get_suministros_pendientes_comprar_agrupados_suministro(criterio), 20, pagina)
        user = request.user
        render = render_to_string('ajax/suministrosrequisicionessearch.html', {'user': user, 'suministros_requisiciones': pag, 'criterio': criterio, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_suministros_requisiciones', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_proveedores_suministro_cotizacion_add2(request, pagina, suministro_id, criterio, proyecto_id):
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
        pag = Paginador(request, suministro_comprar.suministro.suministro.get_proveedores_activos_suministro(criterio=criterio), 20, pagina)

        now = datetime.datetime.now()
        fecha_actual = now.strftime("%Y-%m-%d")
        render = render_to_string('ajax/suministrocotizarproveedoressearch.html', {'user': user, 'suministro_proveedores': pag, 'suministro_comprar': suministro_comprar, 'fecha_actual': fecha_actual, 'criterio_proveedor': criterio, 'proyecto': proyecto } )
        dajax.assign('#light', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#PAGINACIÓN SUMINISTROS DE REQUISICIONES PARA UNA NUEVA COTIZACIÓN
def paginar_suministros_proveedor_cotizacion_add2(request, pagina, criterio, proveedor_id, proyecto_id):
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

            pag = Paginador(request, suministros_comprar, 20, pagina)
            user = request.user
            permisos_usuario = user.get_all_permissions()
            render = render_to_string('ajax/suministrosrequisicionesproveedorsearch.html', {'user': user, 'permisos': permisos_usuario, 'suministros_requisiciones': pag, 'proveedor': proveedor, 'criterio': criterio, 'proyecto': proyecto } )
            dajax.assign('#light', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------- PAGINACION COTIZACIONES ----------------------------------------
def paginar_cotizaciones2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        cotizaciones = proyecto.lista_cotizaciones(tipo=1, criterio=criterio)
        pag = Paginador(request, cotizaciones, 20, pagina)
        user = request.user
        render = render_to_string('ajax/cotizacionessearch.html', {'user': user, 'cotizaciones': pag, 'criterio': criterio, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_cotizaciones', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------- PAGINACION SUMINISTROS DE COTIZACIÓN ----------------------------------------
def paginar_suministros_cotizacion2(request, pagina, cotizacion_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        proyecto = Proyecto.objects.get(id=proyecto_id)
        cotizacion = proyecto.cotizacion_set.get(id=cotizacion_id)
        suministros = cotizacion.suministrocotizacion_set.all()
        pag = Paginador(request, suministros, 20, pagina)
        user = request.user
        if cotizacion.tipo == 1:
            render = render_to_string('ajax/suministroscotizacionsearch.html', {'user': user, 'suministros': pag, 'cotizacion': cotizacion, 'proyecto': proyecto} )
        elif cotizacion.tipo == 2:
            render = render_to_string('ajax/suministroscotizacionordenserviciosearch.html', {'user': user, 'suministros': pag, 'cotizacion': cotizacion, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_suministros', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------- PAGINACION COTIZACIONES ORDENES DE SERIVICIO----------------------------------------
def paginar_cotizaciones_orden_servicio2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        cotizaciones = proyecto.lista_cotizaciones(tipo=2, criterio=criterio)
        pag = Paginador(request, cotizaciones, 20, pagina)
        user = request.user
        render = render_to_string('ajax/cotizacionesordenserviciosearch.html', {'user': user, 'cotizaciones': pag, 'criterio': criterio, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_cotizaciones', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------- PAGINACION ORDENES DE COMPRA ----------------------------------------
def paginar_ordenes_compra2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        fecha_inicial = fecha_inicial.strip()
        fecha_final = fecha_final.strip()
        fecha_inicial = {'valor': fecha_inicial, 'error': ''}
        fecha_final = {'valor': fecha_final, 'error': ''}
        parametro_fecha_inicial = ''
        parametro_fecha_final = ''

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
        pag = Paginador(request, ordenes_compra, 20, pagina)
        user = request.user
        render = render_to_string('ajax/ordenescomprasearch.html', {'user': user, 'ordenes_compra': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_ordenes_compra', 'innerHTML', render)
        dajax.script("Calendar.setup({inputField:'id_fecha_inicial',ifFormat:'%Y-%m-%d',button:'lanzador_f_i'});")
        dajax.script("Calendar.setup({inputField:'id_fecha_final',ifFormat:'%Y-%m-%d',button:'lanzador_f_f'});")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_suministros_orden_compra2(request, pagina, orden_compra_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        proyecto = Proyecto.objects.get(id=proyecto_id)
        orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
        suministros = orden_compra.suministroordencompraitem_set.all()
        pag = Paginador(request, suministros, 20, pagina)
        user = request.user
        render = render_to_string('ajax/suministrosordencomprasearch.html', {'user': user, 'orden_compra': orden_compra, 'suministros': pag, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_suministros', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_suministros_proveedor_orden_compra_change2(request, pagina, criterio, orden_compra_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)

        suministros = None
        suministros_agregar = None
        try:
            suministros = request.session['suministros']
            suministros_agregar = request.session['suministros_agregar']
        except :
            pass
        if suministros != None and suministros_agregar != None:

            orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)

            criterio = criterio.strip()

            ids_suministros_excluir = []
            for suministro in suministros:
                ids_suministros_excluir.append(suministro['suministro'].id)

            #Visualiza los suministros requeridos con la cantidad a cotizar
            if criterio != None:
                criterio = criterio.strip()
            else:
                criterio = ''
            suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(criterio=criterio, proveedor_id=orden_compra.proveedor.id, exclude_suministros_id=ids_suministros_excluir)
            suministros_comprar = []
            for suministro_requisiciones in suministros_requisiciones:
                suministro_orden_compra_item = None
                try:
                    suministro_orden_compra_item = orden_compra.suministroordencompraitem_set.get(suministro=suministro_requisiciones.suministro.suministro)
                except :
                    pass
                if suministro_orden_compra_item != None:
                    suministro_requisiciones.cantidad_requerida = round(suministro_requisiciones.cantidad_requerida + suministro_orden_compra_item.suministroordencompra_set.aggregate(Sum('cantidad_comprada'))['cantidad_comprada__sum'], 2)
                suministro_comprar = {'suministro': suministro_requisiciones, 'cantidad': '', 'precio': '', 'iva_suministro': '', 'observaciones': suministro_requisiciones.observaciones}
                for suministro_agregar in suministros_agregar:
                    if suministro_requisiciones.suministro.suministro.id == suministro_agregar['suministro'].id:
                        suministro_comprar['cantidad'] = suministro_agregar['cantidad']
                        suministro_comprar['precio'] = suministro_agregar['precio']
                        suministro_comprar['iva_suministro'] = suministro_agregar['iva_suministro']
                        suministro_comprar['observaciones'] = suministro_agregar['observaciones']
                suministros_comprar.append(suministro_comprar)

            pag = Paginador(request, suministros_comprar, 20, pagina)
            render = render_to_string('ajax/suministrosrequisicionesproveedorsearchordencomprachange.html', {'user': user, 'suministros_requisiciones': pag, 'orden_compra': orden_compra, 'criterio': criterio, 'proyecto': proyecto} )
            dajax.assign('#light', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_suministros_orden_compra_change2(request, pagina, orden_compra_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
            # Verifica que se pueda modificar la orden de compra
            if len(orden_compra.informerecepcion_set.all()) == 0 and orden_compra.permiso_modificar:
                subtotal = 0
                valor_iva = 0
                valor_total = 0

                for suministro in suministros:
                    subtotal = round(subtotal + (suministro['cantidad'] * suministro['precio']), 2)
                    valor_iva = round(valor_iva + (suministro['cantidad'] * suministro['precio'] * suministro['iva_suministro']), 2)
                valor_total = round(subtotal + valor_iva, 2)
                error = {}
                pag = Paginador(request, suministros, 20, pagina)
                render = render_to_string('ajax/suministrosordencomprachange.html', {'user': user, 'orden_compra': orden_compra, 'suministros': pag, 'subtotal': subtotal, 'valor_iva': valor_iva, 'valor_total': valor_total, 'proyecto': proyecto, 'error': error})
                dajax.assign('#id_reporte_suministros', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_items_informe_recepcion2(request, pagina, criterio, orden_compra_id, proyecto_id):
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
                    suministros_orden_compra.append({'suministro': suministro_tmp, 'cantidad_nuevo_informe': ''})
            suministros_informe_recepcion = request.session['suministros_informe_recepcion']
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


#---------- PAGINACION SUMINISTROS DE ALMACEN ----------------------------------------
def paginar_suministros_almacen2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = proyecto.suministroalmacen_set.all().order_by('suministro__nombre')
        if criterio != "":
            suministros = suministros.filter(Q(suministro__nombre__icontains=criterio) | Q(suministro__sinonimos__icontains=criterio))
        pag = Paginador(request, suministros, 20, pagina)
        user = request.user
        render = render_to_string('ajax/suministrosalmacensearch.html', {'user': user, 'suministros': pag, 'criterio': criterio, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_suministros', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_suministros_almacen_informe_salida_add2(request, pagina, criterio_suministro, proyecto_id):
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
            suministros = SuministroAlmacen.objects.filter(proyecto=proyecto).order_by('suministro__nombre')
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
            render = render_to_string('ajax/suministrosalmacensearchinformesalida.html', {'user': user, 'suministros': pag, 'criterio_suministro': criterio_suministro, 'pagina_suministro': pagina, 'proyecto': proyecto} )
            dajax.assign('#id_reporte_suministros', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()

#-------------------------------------------------------------------------------------------------

#---------- PAGINACION ORDENES DE COMPRA INFORME DE RECEPCION ADD----------------------------------------
def paginar_ordenes_compra_informe_recepcion_add2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        proyecto = Proyecto.objects.get(id = proyecto_id)
        criterio = criterio.strip()
        ordenes_compra = proyecto.lista_ordenes_compra(criterio=criterio, estado=1)
        for orden_compra in ordenes_compra:
            if len(orden_compra.suministroordencompra_set.filter(cantidad_almacen__lt=F('cantidad_comprada'))) == 0:
                ordenes_compra = ordenes_compra.exclude(id=orden_compra.id)
        pag = Paginador(request, ordenes_compra, 20, pagina)
        user = request.user
        render = render_to_string('ajax/ordenescomprasearchinformerecepcionadd.html', {'user': user, 'ordenes_compra': pag, 'criterio': criterio, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_ordenes_compra', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


# #PAGINACION INFORMES ENTREGA
def paginar_informes_entrega2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        fecha_inicial = fecha_inicial.strip()
        fecha_final = fecha_final.strip()
        fecha_inicial = {'valor': fecha_inicial, 'error': ''}
        fecha_final = {'valor': fecha_final, 'error': ''}
        parametro_fecha_inicial = ''
        parametro_fecha_final = ''

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
        pag = Paginador(request, informes_recepcion, 20, pagina)
        user = request.user
        render = render_to_string('ajax/informesrecepcionsearch.html', {'user': user, 'informes_recepcion': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto})
        dajax.assign('#id_reporte_informes_entrega', 'innerHTML', render)
        dajax.script("Calendar.setup({inputField:'id_fecha_inicial',ifFormat:'%Y-%m-%d',button:'lanzador_f_i'});")
        dajax.script("Calendar.setup({inputField:'id_fecha_final',ifFormat:'%Y-%m-%d',button:'lanzador_f_f'});")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_suministros_informe_recepcion2(request, pagina, informe_recepcion_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        informe_recepcion = InformeRecepcion.objects.get(id=informe_recepcion_id, orden_compra__proyecto=proyecto)
        suministros = informe_recepcion.suministroinformerecepcion_set.all()
        suministros_informe_recepcion = []
        for suministro in suministros:
            suministro_tmp = suministro
            suministro_adicionado = False
            for suministro_tmp2 in suministros_informe_recepcion:
                if suministro_tmp2.suministro.suministro.suministro.suministro.id == suministro_tmp.suministro.suministro.suministro.suministro.id:
                    suministro_tmp2.cantidad = round(suministro_tmp2.cantidad + suministro_tmp.cantidad, 2)
                    suministro_adicionado = True
            if suministro_adicionado == False:
                suministros_informe_recepcion.append(suministro_tmp)
        pag = Paginador(request, suministros_informe_recepcion, 20, pagina)
        user = request.user
        render = render_to_string('ajax/suministrosinformerecepcionsearch.html', {'user': user, 'suministros': pag, 'informe_recepcion': informe_recepcion, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_suministros', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_informes_salida2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        fecha_inicial = fecha_inicial.strip()
        fecha_final = fecha_final.strip()
        fecha_inicial = {'valor': fecha_inicial, 'error': ''}
        fecha_final = {'valor': fecha_final, 'error': ''}
        parametro_fecha_inicial = ''
        parametro_fecha_final = ''

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
        pag = Paginador(request, informes_salida, 20, pagina)
        user = request.user
        render = render_to_string('ajax/informessalidasearch.html', {'user': user, 'informes_salida': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_informes_salida', 'innerHTML', render)
        dajax.script("Calendar.setup({inputField:'id_fecha_inicial',ifFormat:'%Y-%m-%d',button:'lanzador_f_i'});")
        dajax.script("Calendar.setup({inputField:'id_fecha_final',ifFormat:'%Y-%m-%d',button:'lanzador_f_f'});")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_suministros_informe_salida2(request, pagina, informe_salida_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        informe_salida = proyecto.informesalida_set.get(id=informe_salida_id)
        suministros = informe_salida.suministroinformesalidaitem_set.all()
        pag = Paginador(request, suministros, 20, pagina)
        user = request.user
        render = render_to_string('ajax/suministrosinformesalidasearch.html', {'user': user, 'suministros': pag, 'informe_salida': informe_salida, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_suministros', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#PAGINACIÓN SUMINISTROS DE REQUISICIONES PARA UNA NUEVA COTIZACIÓN DE ORDEN DE SERVICIO
def paginar_suministros_requisiciones_cotizacion_orden_servicio_add2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        pag = Paginador(request, proyecto.get_suministros_pendientes_comprar_agrupados_suministro(criterio=criterio, tipo_cotizacion=2), 20, pagina)
        render = render_to_string('ajax/suministrosrequisicionessearchordenservicioadd.html', {'user': user, 'suministros_requisiciones': pag, 'criterio': criterio, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_suministros_requisiciones', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#Paginar proveedores orden de servicio_add
def paginar_proveedores_orden_servicio_add2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        criterio = criterio.replace("'",'"')
        qry = "SELECT p.* FROM inverboy_suministroproveedor sp, inverboy_proveedor p WHERE sp.proveedor_id = p.id AND p.estado_proveedor = TRUE AND sp.suministro_id IN (	SELECT s.id	FROM inverboy_suministrorequisicion sr, inverboy_requisicion r, inverboy_suministroapuproyecto sap, inverboy_suministro s	WHERE sap.suministro_id = s.id AND sr.suministro_id = sap.id	AND sr.cantidad_comprada < sr.cantidad_requerida	AND sr.requisicion_id = r.id	AND r.proyecto_id = " + str(proyecto_id) + "    AND r.estado = 2	AND s.clasificacion_general != 'Material'	GROUP BY s.id   )"
        criterio = criterio.strip()
        if criterio != '':
            try:
                criterio = int(criterio)
                qry = qry + " AND p.identificacion = " + str(criterio)
            except:
                qry = qry + " AND (p.razon_social LIKE '%%" + criterio + "%%' OR p.nombre_comercial LIKE '%%" + criterio +"%%')"
        qry = qry + " GROUP BY p.id ORDER BY p.razon_social"

        proveedores = Proveedor.objects.raw(qry)

        lista_proveedores = list(proveedores)

        pag = Paginador(request, lista_proveedores, 20, pagina)

        render = render_to_string('ajax/ordenservicioproveedoressearch.html', {'user': user, 'proveedores': pag, 'criterio': criterio, 'proyecto': proyecto } )
        dajax.assign('#id_reporte_proveedores', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#PAGINACIÓN SUMINISTROS DE REQUISICIONES PARA UNA NUEVA COTIZACIÓN DE ORDEN DE SERVICIO
def paginar_suministros_proveedor_cotizacion_orden_servicio_add2(request, pagina, criterio, proveedor_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
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
            suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(criterio=criterio, proveedor_id=proveedor_id, tipo_cotizacion=2)
            suministros_comprar = []
            for suministro_requisiciones in suministros_requisiciones:
                suministro_comprar = {'suministro': suministro_requisiciones, 'cantidad_nueva_cotizacion': ''}
                for suministro_cotizacion in suministros_cotizacion:
                    if suministro_requisiciones.suministro.suministro.id == suministro_cotizacion['suministro_id']:
                        suministro_comprar['cantidad_nueva_cotizacion'] = suministro_cotizacion['cantidad']
                suministros_comprar.append(suministro_comprar)

            pag = Paginador(request, suministros_comprar, 20, pagina)

            render = render_to_string('ajax/suministrosrequisicionesproveedorsearchordenservicioadd.html', {'user': user, 'suministros_requisiciones': pag, 'proveedor': proveedor, 'criterio': criterio, 'proyecto': proyecto } )
            dajax.assign('#light', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------- PAGINACION ORDENES DE SERVICIO ----------------------------------------
def paginar_ordenes_servicio2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        fecha_inicial = fecha_inicial.strip()
        fecha_final = fecha_final.strip()
        fecha_inicial = {'valor': fecha_inicial, 'error': ''}
        fecha_final = {'valor': fecha_final, 'error': ''}
        parametro_fecha_inicial = ''
        parametro_fecha_final = ''

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

        pag = Paginador(request, ordenes_servicio, 20, pagina)
        user = request.user
        render = render_to_string('ajax/ordenesserviciosearch.html', {'user': user, 'ordenes_servicio': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_ordenes_servicio', 'innerHTML', render)
        dajax.script("Calendar.setup({inputField:'id_fecha_inicial',ifFormat:'%Y-%m-%d',button:'lanzador_f_i'});")
        dajax.script("Calendar.setup({inputField:'id_fecha_final',ifFormat:'%Y-%m-%d',button:'lanzador_f_f'});")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------- PAGINACION SUMINISTROS DE ORDEN SERVICIO ----------------------------------------
def paginar_suministros_orden_servicio2(request, pagina, orden_servicio_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        proyecto = Proyecto.objects.get(id=proyecto_id)
        orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
        suministros = orden_servicio.suministroordenservicioitem_set.all()
        pag = Paginador(request, suministros, 20, pagina)
        user = request.user
        render = render_to_string('ajax/suministrosordenserviciosearch.html', {'user': user, 'suministros': pag, 'orden_servicio': orden_servicio, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_suministros', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_suministros_orden_servicio_change2(request, pagina, orden_servicio_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        suministros = None
        try:
            suministros = request.session['suministros']
        except :
            pass
        if suministros != None:
            orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
            # Verifica que se pueda modificar la orden de servicio
            if orden_servicio.permite_modificaciones():
                valores_discriminados = {'subtotal': 0, 'valor_iva': 0, 'valor_total': 0}

                for suministro in suministros:
                    valores_discriminados['valor_total'] = round(valores_discriminados['valor_total'] + (suministro['cantidad'] * suministro['precio']), 2)

                pag = Paginador(request, suministros, 20, pagina)
                render = render_to_string('ajax/suministrosordenserviciochange.html', {'user': user, 'orden_servicio': orden_servicio, 'suministros': pag, 'valores_discriminados': valores_discriminados, 'proyecto': proyecto})
                dajax.assign('#id_reporte_suministros', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_suministros_proveedor_orden_servicio_change2(request, pagina, criterio, orden_servicio_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)

        suministros = None
        suministros_agregar = None
        try:
            suministros = request.session['suministros']
            suministros_agregar = request.session['suministros_agregar']
        except :
            pass
        if suministros != None and suministros_agregar != None:

            orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)

            criterio = criterio.strip()

            ids_suministros_excluir = []
            for suministro in suministros:
                ids_suministros_excluir.append(suministro['suministro'].id)

            #Visualiza los suministros requeridos con la cantidad a cotizar
            criterio = criterio.strip()
            suministros_requisiciones = proyecto.get_suministros_pendientes_comprar_agrupados_suministro(criterio=criterio, proveedor_id=orden_servicio.proveedor.id, tipo_cotizacion=2, exclude_suministros_id=ids_suministros_excluir)
            suministros_comprar = []
            for suministro_requisiciones in suministros_requisiciones:
                suministro_orden_servicio_item = None
                try:
                    suministro_orden_servicio_item = orden_servicio.suministroordenservicioitem_set.get(suministro=suministro_requisiciones.suministro.suministro)
                except :
                    pass
                if suministro_orden_servicio_item != None:
                    suministro_requisiciones.cantidad_requerida = round(suministro_requisiciones.cantidad_requerida + suministro_orden_servicio_item.suministroordenservicio_set.aggregate(Sum('cantidad'))['cantidad__sum'], 2)
                suministro_comprar = {'suministro': suministro_requisiciones, 'cantidad': '', 'precio': '', 'iva_suministro': '', 'observaciones': suministro_requisiciones.observaciones}
                for suministro_agregar in suministros_agregar:
                    if suministro_requisiciones.suministro.suministro.id == suministro_agregar['suministro'].id:
                        suministro_comprar['cantidad'] = suministro_agregar['cantidad']
                        suministro_comprar['precio'] = suministro_agregar['precio']
                        suministro_comprar['observaciones'] = suministro_agregar['observaciones']
                suministros_comprar.append(suministro_comprar)

            pag = Paginador(request, suministros_comprar, 20, pagina)
            render = render_to_string('ajax/suministrosrequisicionesproveedorsearchordenserviciochange.html', {'user': user, 'suministros_requisiciones': pag, 'orden_servicio': orden_servicio, 'criterio': criterio, 'proyecto': proyecto} )
            dajax.assign('#light', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/proyectodetails/'+str(proyecto_id)+'/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------- PAGINACION ORDENES DE SERVICIO ----------------------------------------
def paginar_ordenes_servicio_corte_diario_obra_add2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        ordenes_servicio = proyecto.lista_ordenes_servicio(criterio=criterio, estado=1)
        for orden_servicio in ordenes_servicio:
            if len(orden_servicio.suministroordenservicio_set.filter(cantidad_entregada__lt=F('cantidad'))) == 0:
                ordenes_servicio = ordenes_servicio.exclude(id=orden_servicio.id)
        pag = Paginador(request, ordenes_servicio, 20, pagina)
        user = request.user
        render = render_to_string('ajax/ordenesserviciosearchcortediarioobraadd.html', {'user': user, 'ordenes_servicio': pag, 'criterio': criterio, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_ordenes_servicio', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_items_corte_diario_obra_add2(request, pagina, criterio, orden_servicio_id, proyecto_id):
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
            orden_servicio = proyecto.ordenservicio_set.get(id=orden_servicio_id)
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


def paginar_cortes_diario_obra2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        fecha_inicial = fecha_inicial.strip()
        fecha_final = fecha_final.strip()
        fecha_inicial = {'valor': fecha_inicial, 'error': ''}
        fecha_final = {'valor': fecha_final, 'error': ''}
        parametro_fecha_inicial = ''
        parametro_fecha_final = ''

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

        cortes_diario_obra = proyecto.lista_cortes_diario_obra(criterio=criterio, fecha_inicial=parametro_fecha_inicial, fecha_final=parametro_fecha_final)
        pag = Paginador(request, cortes_diario_obra, 20, pagina)
        user = request.user
        render = render_to_string('ajax/cortesdiarioobrasearch.html', {'user': user, 'cortes_diario_obra': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_cortes_diario_obra', 'innerHTML', render)
        dajax.script("Calendar.setup({inputField:'id_fecha_inicial',ifFormat:'%Y-%m-%d',button:'lanzador_f_i'});")
        dajax.script("Calendar.setup({inputField:'id_fecha_final',ifFormat:'%Y-%m-%d',button:'lanzador_f_f'});")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_suministros_corte_diario_obra2(request, pagina, corte_diario_obra_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
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
        pag = Paginador(request, suministros_corte_diario_obra, 20, pagina)
        user = request.user
        render = render_to_string('ajax/suministroscortediarioobrasearch.html', {'user': user, 'suministros': pag, 'corte_diario_obra': corte_diario_obra, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_suministros', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_proveedores_acta_recibo_obra_add2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        qry = "SELECT p.* FROM inverboy_proveedor p, inverboy_ordenservicio os, inverboy_cortediarioobra cdo WHERE ((p.id = os.proveedor_id AND os.tercero_id IS NULL) OR (p.id = os.tercero_id)) AND cdo.orden_servicio_id = os.id AND cdo.estado = TRUE AND os.proyecto_id = %s" % proyecto_id
        criterio = criterio.strip()
        if criterio != '':
            criterio = criterio.replace("'",'"')
            try:
                int(criterio)
                qry = qry + " AND p.identificacion = " + str(criterio)
            except :
                qry = qry + " AND (p.razon_social LIKE '%%" + criterio + "%%' OR p.nombre_comercial LIKE '%%" + str(criterio) + "%%')"
        qry = qry + " GROUP BY p.id"
        proveedores = list(Proveedor.objects.raw(qry))
        pag = Paginador(request, proveedores, 20, pagina)
        render = render_to_string('ajax/proveedoressearchactareciboobraadd.html', {'user': user, 'proveedores': pag, 'criterio': criterio, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_proveedores', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------- Paginación ordenes de servocio acta_recibo_obra_add ----------------------------------------
def paginar_ordenes_servicio_acta_recibo_obra_add2(request, pagina, proveedor_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        proveedor = Proveedor.objects.get(id=proveedor_id)
        qry = "SELECT os.* FROM inverboy_ordenservicio os, inverboy_proveedor p, inverboy_cortediarioobra cdo WHERE p.id = " + str(proveedor_id) + " AND ((p.id = os.proveedor_id AND os.tercero_id IS NULL) OR (p.id = os.tercero_id)) AND cdo.orden_servicio_id = os.id AND cdo.estado = TRUE AND os.proyecto_id = " + str(proyecto_id) + " GROUP BY os.id"
        ordenes_servicio = list(proyecto.ordenservicio_set.raw(qry))
        pag = Paginador(request, ordenes_servicio, 20, pagina)
        render = render_to_string('ajax/ordenesservicioproveedorsearchactareciboobraadd.html', {'user': user, 'ordenes_servicio': pag, 'proveedor': proveedor, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_ordenes_servicio', 'innerHTML', render)
        #return HttpResponseRedirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_actas_recibo_obra2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        fecha_inicial = fecha_inicial.strip()
        fecha_final = fecha_final.strip()
        fecha_inicial = {'valor': fecha_inicial, 'error': ''}
        fecha_final = {'valor': fecha_final, 'error': ''}
        parametro_fecha_inicial = ''
        parametro_fecha_final = ''

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
        pag = Paginador(request, actas_recibo_obra, 20, pagina)
        render = render_to_string('ajax/actasreciboobrasearch.html', {'user': user, 'actas_recibo_obra': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto})
        dajax.assign('#id_reporte_actas_recibo_obra', 'innerHTML', render)
        dajax.script("Calendar.setup({inputField:'id_fecha_inicial',ifFormat:'%Y-%m-%d',button:'lanzador_f_i'});")
        dajax.script("Calendar.setup({inputField:'id_fecha_final',ifFormat:'%Y-%m-%d',button:'lanzador_f_f'});")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_actas_recibo_obra_aprobar2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        fecha_inicial = fecha_inicial.strip()
        fecha_final = fecha_final.strip()
        fecha_inicial = {'valor': fecha_inicial, 'error': ''}
        fecha_final = {'valor': fecha_final, 'error': ''}
        parametro_fecha_inicial = ''
        parametro_fecha_final = ''

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
        pag = Paginador(request, actas_recibo_obra, 20, pagina)
        render = render_to_string('ajax/busquedaactasreciboobraaprobar.html', {'user': user, 'actas_recibo_obra': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto})
        dajax.assign('#id_reporte_actas_recibo_obra', 'innerHTML', render)
        dajax.script("Calendar.setup({inputField:'id_fecha_inicial',ifFormat:'%Y-%m-%d',button:'lanzador_f_i'});")
        dajax.script("Calendar.setup({inputField:'id_fecha_final',ifFormat:'%Y-%m-%d',button:'lanzador_f_f'});")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_actas_recibo_obra_reporte_pago2(request, pagina, criterio, fecha_inicial, fecha_final, tipo_busqueda, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        fecha_inicial = fecha_inicial.strip()
        fecha_final = fecha_final.strip()
        tipo_busqueda = int(tipo_busqueda)
        criterio = criterio.strip()
        total_pagar_actas = 0
        actas_recibo_obra = []

        error_fecha_inicial = ''
        error_fecha_final = ''
        if fecha_inicial != '':
            validaciones_fecha = Validator().append([
                Field('fecha_inicial', fecha_inicial).append([
                    IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                ]),
            ]).run(True).pop()

            if validaciones_fecha['passed'] == False:
                for error in validaciones_fecha['errors']:
                    error_fecha_inicial = error

        if fecha_final != '':
            validaciones_fecha = Validator().append([
                Field('fecha_final', fecha_final).append([
                    IsRequired('Este campo es obligatorio.'), Regex("^(19|20)[0-9]{2}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])?$", error='La fecha no tiene el formato correcto.'),
                ]),
            ]).run(True).pop()

            if validaciones_fecha['passed'] == False:
                for error in validaciones_fecha['errors']:
                    error_fecha_final = error

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

        if criterio != '':
            actas_recibo_obra = actas_recibo_obra.filter(Q(orden_servicio__proveedor__razon_social__icontains=criterio) | Q(orden_servicio__proveedor__nombre_comercial__icontains=criterio))

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
        pag = Paginador(request, actas_recibo_obra, 20, pagina)
        render = render_to_string('ajax/actasreciboobrasearchreportepago.html', {'user': user, 'actas_recibo_obra': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'tipo_busqueda': tipo_busqueda, 'proyecto': proyecto})
        dajax.assign('#id_reporte_actas_recibo_obra', 'innerHTML', render)
        dajax.script("Calendar.setup({inputField:'id_fecha_inicial',ifFormat:'%Y-%m-%d',button:'lanzador'});")
        dajax.script("Calendar.setup({inputField:'id_fecha_final',ifFormat:'%Y-%m-%d',button:'lanzador2'});")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#Paginación de suministros requeridos para realizar una nueva orden de giro
def paginar_suministros_requisiciones_orden_giro_add2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()

        #Visualiza los suministros requeridos con la cantidad a cotizar
        suministros_pendientes = proyecto.get_suministros_pendientes_comprar(criterio=criterio, clasificacion_general=['Indirectos'])
        suministros_requisiciones = []
        for suministro_pendientes in suministros_pendientes:
            suministro_requisicion = { 'suministro': suministro_pendientes, 'cantidad_nueva_orden_giro': '', 'observaciones': suministro_pendientes.observaciones }
            for suministro_orden_giro in suministros_orden_giro:
                if suministro_pendientes.id == suministro_orden_giro['suministro_id']:
                    suministro_requisicion['cantidad_nueva_orden_giro'] = suministro_orden_giro['cantidad']
                    suministro_requisicion['observaciones'] = suministro_orden_giro['observaciones']
            suministros_requisiciones.append(suministro_requisicion)

        pag = Paginador(request, suministros_requisiciones, 20, pagina)
        
        render = render_to_string('ajax/suministrosrequisicionessearchordengiroadd.html', {'user': user, 'suministros_requisiciones': pag, 'criterio': criterio, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_suministros_requisiciones', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_proveedores_orden_giro_add2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        proveedores = Proveedor.objects.filter(estado_proveedor=True)
        criterio = criterio.strip()
        if criterio != '':
            try:
                criterio = int(criterio)
                proveedores = proveedores.filter(identificacion=criterio)
            except :
                proveedores = proveedores.filter(Q(razon_social__icontains=criterio))
        pag = Paginador(request, proveedores, 20, pagina)
        render = render_to_string('ajax/proveedoressearchordengiroadd.html', {'user': user, 'proveedores': pag, 'criterio': criterio, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_proveedores', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_ordenes_giro2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        fecha_inicial = fecha_inicial.strip()
        fecha_final = fecha_final.strip()
        fecha_inicial = {'valor': fecha_inicial, 'error': ''}
        fecha_final = {'valor': fecha_final, 'error': ''}
        parametro_fecha_inicial = ''
        parametro_fecha_final = ''

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
        pag = Paginador(request, ordenes_giro, 20, pagina)
        render = render_to_string('ajax/ordenesgirosearch.html', {'user': user, 'ordenes_giro': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_ordenes_giro', 'innerHTML', render)
        dajax.script("Calendar.setup({inputField:'id_fecha_inicial',ifFormat:'%Y-%m-%d',button:'lanzador_f_i'});")
        dajax.script("Calendar.setup({inputField:'id_fecha_final',ifFormat:'%Y-%m-%d',button:'lanzador_f_f'});")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_items_orden_giro2(request, pagina, orden_giro_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        orden_giro = proyecto.ordengiro_set.get(id=orden_giro_id)
        pag = Paginador(request, orden_giro.itemordengiro_set.all(), 20, pagina)
        render = render_to_string('ajax/itemsordengirosearch.html', {'user': user, 'orden_giro': orden_giro, 'items': pag, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_items', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#---------- PAGINACION ORDENES DE GIRO ACTA DE CONFORMIDAD ADD----------------------------------------
def paginar_ordenes_giro_acta_conformidad_add2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        proyecto = Proyecto.objects.get(id = proyecto_id)
        criterio = criterio.strip()
        criterio = criterio.strip()
        ordenes_giro = proyecto.lista_ordenes_giro(criterio=criterio, estado=1)
        pag = Paginador(request, ordenes_giro, 20, pagina)
        user = request.user
        render = render_to_string('ajax/ordenesgirosearchactaconformidadadd.html', {'user': user, 'ordenes_giro': pag, 'criterio': criterio, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_ordenes_giro', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_actas_conformidad2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        fecha_inicial = fecha_inicial.strip()
        fecha_final = fecha_final.strip()
        fecha_inicial = {'valor': fecha_inicial, 'error': ''}
        fecha_final = {'valor': fecha_final, 'error': ''}
        parametro_fecha_inicial = ''
        parametro_fecha_final = ''

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
        pag = Paginador(request, actas_conformidad, 20, pagina)
        render = render_to_string('ajax/actasconformidadsearch.html', {'user': user, 'actas_conformidad': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto})
        dajax.assign('#id_reporte_actas_conformidad', 'innerHTML', render)
        dajax.script("Calendar.setup({inputField:'id_fecha_inicial',ifFormat:'%Y-%m-%d',button:'lanzador_f_i'});")
        dajax.script("Calendar.setup({inputField:'id_fecha_final',ifFormat:'%Y-%m-%d',button:'lanzador_f_f'});")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_items_acta_conformidad2(request, pagina, acta_conformidad_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        acta_conformidad = ActaConformidad.objects.get(id=acta_conformidad_id, orden_giro__proyecto=proyecto)
        items = acta_conformidad.itemactaconformidad_set.all()
        pag = Paginador(request, items, 20, pagina)
        render = render_to_string('ajax/itemsactaconformidadsearch.html', {'user': user, 'acta_conformidad': acta_conformidad, 'items': pag, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_items', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_proveedores_factura_orden_compra_proyecto_add2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        proveedores = proyecto.lista_proveedores_ordenes_compra_en_ejecucion_por_facturar(criterio=criterio)
        pag = Paginador(request, proveedores, 20, pagina)
        render = render_to_string('ajax/proveedoressearchfacturaordencompraadd.html', {'user': user, 'proveedores': pag, 'criterio': criterio, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_proveedores', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_ordenes_compra_proveedor_factura_orden_compra_proyecto_add2(request, pagina, proveedor_id, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        proveedor = Proveedor.objects.get(id=proveedor_id)
        criterio = criterio.strip()
        ordenes_compra = proyecto.lista_ordenes_compra_en_ejecucion_por_facturar(criterio=criterio, proveedor=proveedor)
        pag = Paginador(request, ordenes_compra, 20, pagina)
        render = render_to_string('ajax/ordenescompraproveedorsearchfacturaordencompraadd.html', {'user': user, 'ordenes_compra': pag, 'proveedor': proveedor, 'criterio': criterio, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_ordenes_compra', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_informes_recepcion_factura_orden_compra_proyecto_add2(request, pagina, orden_compra_id, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        orden_compra = proyecto.ordencompra_set.get(id=orden_compra_id)
        informes_recepcion = orden_compra.lista_informes_recepcion_por_facturar(criterio)
        pag = Paginador(request, informes_recepcion, 20, pagina)
        render = render_to_string('ajax/informesrecepcionordencomprasearchfacturaordencompraadd.html', {'user': user, 'informes_recepcion': pag, 'orden_compra': orden_compra, 'criterio': criterio, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_informes_recepcion', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_items_factura_orden_compra_add2(request, pagina, proveedor_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        items_factura = None
        try:
            items_factura = request.session['items_factura']
        except :
            pass
        if items_factura != None:
            proveedor = Proveedor.objects.get(id=proveedor_id)

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

            pag = Paginador(request, lista_items_factura, 20, pagina)
            render = render_to_string('ajax/itemsfacturaordencompraadd.html', {'user': user, 'proveedor': proveedor, 'items_factura': pag, 'discriminacion_valores': discriminacion_valores, 'proyecto': proyecto})
            dajax.assign('#id_reporte_items', 'innerHTML', render)
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_facturas_ordenes_compra2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        fecha_inicial = fecha_inicial.strip()
        fecha_final = fecha_final.strip()
        fecha_inicial = {'valor': fecha_inicial, 'error': ''}
        fecha_final = {'valor': fecha_final, 'error': ''}
        parametro_fecha_inicial = ''
        parametro_fecha_final = ''

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
        pag = Paginador(request, facturas, 20, pagina)
        render = render_to_string('ajax/facturasordenescomprasearch.html', {'user': user, 'facturas_ordenes_compra': pag, 'criterio': criterio, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_facturas', 'innerHTML', render)
        dajax.script("Calendar.setup({inputField:'id_fecha_inicial',ifFormat:'%Y-%m-%d',button:'lanzador_f_i'});")
        dajax.script("Calendar.setup({inputField:'id_fecha_final',ifFormat:'%Y-%m-%d',button:'lanzador_f_f'});")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_items_factura_orden_compra2(request, pagina, factura_orden_compra_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        factura = FacturaOrdencompra.objects.get(id=factura_orden_compra_id)
        items_factura = factura.itemfacturaordencompra_set.all()
        pag = Paginador(request, items_factura, 20, pagina)
        user = request.user
        render = render_to_string('ajax/itemsfacturaordencomprasearch.html', {'user': user, 'items_factura': pag, 'factura_orden_compra': factura, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_items', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#### #### MODULO VENTAS #### ####

def paginar_encuestas2(request, pagina, criterio):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        criterio = criterio.strip()
        encuestas = Encuesta.objects.all()
        if request.method == 'POST':
            criterio = criterio.strip()
            if criterio != '':
                encuestas = encuestas.filter(Q(titulo__icontains=criterio) | Q(descripcion__icontains=criterio))
        pag = Paginador(request, encuestas, 20, pagina)
        user = request.user
        render = render_to_string('ajax/ventas/busquedaencuesta.html', {'user': user, 'encuestas': pag, 'criterio': criterio} )
        dajax.assign('#id_reporte_encuestas', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_tipos_adicional2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        tipos_adicional = proyecto.adicionalagrupacion_set.filter(item_adicional=False, nombre__icontains=criterio)
        pag = Paginador(request, tipos_adicional, 20, pagina)
        user = request.user
        render = render_to_string('ajax/ventas/busquedatipoadicional.html', {'user': user, 'tipos_adicional': pag, 'criterio': criterio, 'proyecto': proyecto})
        dajax.assign('#id_reporte_tipos_adicional', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_adicionales2(request, pagina, tipo_adicional_id, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        tipo_adicional = None
        if tipo_adicional_id != None:
            tipo_adicional = proyecto.adicionalagrupacion_set.filter(item_adicional=False, id=tipo_adicional)
        else:
            tipo_adicional = None
        adicionales = proyecto.lista_adicionales_agrupaciones_inmueble(tipo_adicional=tipo_adicional, criterio=criterio)
        pag = Paginador(request, adicionales, 20, pagina)

        tipos_adicional = proyecto.adicionalagrupacion_set.filter(item_adicional=False)
        user = request.user
        render = render_to_string('ajax/ventas/busquedaadicional.html', {'user': user, 'adicionales': pag, 'tipos_adicional': tipos_adicional, 'tipo_adicional_actual': tipo_adicional, 'criterio': criterio, 'proyecto': proyecto})
        dajax.assign('#id_reporte_adicionales', 'innerHTML', render)
        dajax.script("var config = {'.chosen-select': {}, '.chosen-select-deselect': {allow_single_deselect:true}, '.chosen-select-no-single': {disable_search_threshold:10}, '.chosen-select-no-results': {no_results_text:'Oops, nothing found!'}, '.chosen-select-width' : {width:'95%'} }; for (var selector in config) {$(selector).chosen(config[selector]); }")
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_clientes2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        clientes = Cliente.objects.all()
        criterio = criterio.strip()
        if criterio != "":
            try:
                criterio = int(criterio)
                clientes = clientes.filter(identificacion=criterio)
            except:
                clientes = clientes.filter(Q(nombre_1__icontains=criterio) | Q(nombre_2__icontains=criterio) | Q(apellido_1__icontains=criterio) | Q(apellido_2__icontains=criterio))
        pag = Paginador(request, clientes, 20, pagina)
        user = request.user
        render = render_to_string('ajax/ventas/busquedacliente.html', {'user': user, 'clientes': pag, 'criterio': criterio, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_clientes', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_secciones_proyecto2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        secciones_proyecto = proyecto.seccionproyecto_set.all()
        criterio = criterio.strip()
        if criterio != "":
            secciones_proyecto = secciones_proyecto.filter(Q(nombre__icontains=criterio) | Q(iniciales__icontains=criterio))
        pag = Paginador(request, secciones_proyecto, 20, pagina)
        user = request.user
        render = render_to_string('ajax/ventas/busquedaseccionproyecto.html', {'user': user, 'secciones_proyecto': pag, 'criterio': criterio, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_secciones_proyecto', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_tipo_inmuebles2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        tipo_inmuebles = TipoInmueble.objects.all()
        criterio = criterio.strip()
        if criterio != "":
            tipo_inmuebles = tipo_inmuebles.filter(nombre__icontains=criterio)
        pag = Paginador(request, tipo_inmuebles, 20, pagina)
        user = request.user
        render = render_to_string('ajax/ventas/busquedatipoinmueble.html', {'user': user, 'tipo_inmuebles': pag, 'criterio': criterio, 'proyecto': proyecto} )
        dajax.assign('#id_reporte_tipo_inmueble', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_inmuebles2(request, pagina, tipo_inmueble_id, seccion_proyecto_id, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
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
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_agrupaciones2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        agrupacion_inmuebles = proyecto.lista_agrupaciones_inmueble(criterio=criterio)
        pag = Paginador(request, agrupacion_inmuebles, 20, pagina)
        user = request.user
        render = render_to_string('ajax/ventas/busquedaagrupacioninmueblesproyecto.html', {'user': user, 'agrupacion_inmuebles': pag, 'criterio': criterio, 'proyecto': proyecto})
        dajax.assign('#id_reporte_agrupacion_inmuebles', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_busqueda_agrupaciones_nuevo_prospecto_venta2(request, pagina, criterio, proyecto_id):
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

                # Excluye las agrupaciones que ya se encuentran en el prospecto
                ids_inmuebles_interes_prospecto = []
                for inmueble_interes in inmuebles_interes:
                    ids_inmuebles_interes_prospecto.append(inmueble_interes.id)
                inmuebles = inmuebles.exclude(id__in=ids_inmuebles_interes_prospecto)

                pag = Paginador(request, inmuebles, 20, pagina)
                render = render_to_string('ajax/ventas/busquedainmueblesnuevoprospectoventa.html', {'user': user, 'agrupaciones': pag, 'agrupaciones_seleccionadas': inmuebles_agregar, 'criterio': criterio})
                dajax.assign('#light', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_busqueda_agrupaciones_detalles_prospecto_venta2(request, pagina, criterio, prospecto_venta_id, proyecto_id):
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

                # Excluye las agruapciones que ya se encuentran en el prospecto
                prospecto_venta = proyecto.prospectoventa_set.get(id=prospecto_venta_id)
                ids_inmuebles_prospecto = []
                for agrupacion_prospecto in prospecto_venta.agrupacionesinmuebleprospectoventa_set.all():
                    ids_inmuebles_prospecto.append(agrupacion_prospecto.agrupacion_inmueble.id)
                inmuebles = inmuebles.exclude(id__in=ids_inmuebles_prospecto)

                pag = Paginador(request, inmuebles, 20, pagina)
                render = render_to_string('ajax/ventas/busquedainmueblesnuevoprospectoventa.html', {'user': user, 'agrupaciones': pag, 'agrupaciones_seleccionadas': inmuebles_agregar, 'criterio': criterio, 'proyecto': proyecto})
                dajax.assign('#light', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_agrupaciones_nuevo_contrato_venta2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        agrupacion_inmuebles = proyecto.lista_agrupaciones_inmueble(criterio=criterio).filter(agrupacion_contrato_venta=None)
        pag = Paginador(request, agrupacion_inmuebles, 20, pagina)
        user = request.user
        render = render_to_string('ajax/ventas/busquedaagrupacioninmueblesnuevocontratoventa.html', {'user': user, 'agrupacion_inmuebles': pag, 'criterio': criterio, 'proyecto': proyecto})
        dajax.assign('#id_reporte_agrupacion_inmuebles', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_busqueda_clientes_nuevo_contrato_venta2(request, pagina, criterio, prospecto_venta_id, proyecto_id):
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
                clientes = clientes.filter(Q(nombre_1__icontains=criterio) | Q(nombre_2__icontains=criterio) | Q(apellido_1__icontains=criterio) | Q(apellido_2__icontains=criterio))

                # Excluye los clientes que ya se encuentran en el contrato
                clientes = clientes.exclude(id=prospecto_venta.cliente.id)
                ids_clientes_contrato = []
                for cliente_contrato in clientes_contrato:
                    ids_clientes_contrato.append(cliente_contrato.id)
                clientes = clientes.exclude(id__in=ids_clientes_contrato)
                pag = Paginador(request, clientes, 20, pagina)
                render = render_to_string('ajax/ventas/busquedaclientesnuevocontratoventa.html', {'user': user, 'clientes': pag, 'clientes_seleccionados': clientes_agregar, 'criterio': criterio, 'prospecto_venta': prospecto_venta, 'proyecto': proyecto})
                dajax.assign('#light', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_busqueda_adicionales_agrupacion_inmueble_nuevo_contrato_venta2(request, pagina, tipo_adicional, criterio, prospecto_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
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

                criterio = criterio.strip()

                # Filtra los adicionales del proyecto
                if tipo_adicional != None and tipo_adicional != '':
                    tipo_adicional = AdicionalAgrupacion.objects.get(id=tipo_adicional)
                else:
                    tipo_adicional = None

                adicionales_agrupacion_inmueble = proyecto.lista_adicionales_agrupaciones_inmueble(tipo_adicional=tipo_adicional, criterio=criterio)

                # Excluye los adicionales que ya se encuentran en el contrato
                ids_adicionales_contrato = []
                for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                    ids_adicionales_contrato.append(adicional_agrupacion_inmueble_contrato.id)
                adicionales_agrupacion_inmueble = adicionales_agrupacion_inmueble.exclude(id__in=ids_adicionales_contrato)
                pag = Paginador(request, adicionales_agrupacion_inmueble, 20, pagina)
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


def paginar_busqueda_adicionales_agrupacion_inmueble_nuevo_contrato_venta2(request, pagina, tipo_adicional_id, criterio, prospecto_venta_id, proyecto_id):
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
                tipo_adicional = None
                criterio = criterio.strip()

                # Filtra los adicionales del proyecto
                if tipo_adicional_id != None:
                    tipo_adicional = AdicionalAgrupacion.objects.get(id=tipo_adicional_id)
                
                adicionales_agrupacion_inmueble = proyecto.lista_adicionales_agrupaciones_inmueble(tipo_adicional=tipo_adicional, criterio=criterio)

                # Excluye los adicionales que ya se encuentran en el contrato
                ids_adicionales_contrato = []
                for adicional_agrupacion_inmueble_contrato in adicionales_agrupacion_inmueble_contrato:
                    ids_adicionales_contrato.append(adicional_agrupacion_inmueble_contrato.id)
                adicionales_agrupacion_inmueble = adicionales_agrupacion_inmueble.exclude(id__in=ids_adicionales_contrato)
                pag = Paginador(request, adicionales_agrupacion_inmueble, 20, pagina)
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


def paginar_busqueda_agrupaciones_inmueble_agregar_convenio_prospecto_venta2(request, pagina, criterio, prospecto_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        if request.is_ajax():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            prospecto_venta = proyecto.prospectoventa_set.get(id=prospecto_venta_id)
            criterio = criterio.strip()
            # Lista solo las agrupaciones que no esten comprometidas
            agrupacion_inmuebles = proyecto.lista_agrupaciones_inmueble(criterio=criterio).filter(agrupacion_contrato_venta=None)
            pag = Paginador(request, agrupacion_inmuebles, 20, pagina)
            render = render_to_string('ajax/ventas/busquedainmueblesproyectonuevoconvenioprospectoventa.html', {'user': user, 'prospecto_venta': prospecto_venta, 'agrupaciones_inmueble': pag, 'criterio': criterio, 'proyecto': proyecto})
            dajax.assign('#light', 'innerHTML', render)
            dajax.script("document.getElementById('light').style.display='block';")
            dajax.script("document.getElementById('fade').style.display='block';")
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_contratos_venta2(request, pagina, criterio, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        proyecto = Proyecto.objects.get(id=proyecto_id)
        criterio = criterio.strip()
        # Lista los contratos
        contratos_venta = proyecto.lista_contratos(criterio=criterio)
        pag = Paginador(request, contratos_venta, 20, pagina)
        render = render_to_string('ajax/ventas/busquedacontratoventa.html', {'user': user, 'contratos_venta': pag, 'criterio': criterio, 'proyecto': proyecto})
        dajax.assign('#id_reporte_ventas', 'innerHTML', render)
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


def paginar_busqueda_adicionales_agrupacion_inmueble_modificar_contrato_venta2(request, pagina, tipo_adicional_id, criterio, contrato_venta_id, proyecto_id):
    dajax = Dajax()
    if request.user.is_authenticated():
        request.session.set_expiry(600)
        user = request.user
        clientes_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        pagos_entidades_contrato = None
        cuotas_efectivo_contrato = None
        adicionales_agrupacion_inmueble_contrato = None
        adicionales_agregar = None
        try:
            clientes_contrato = request.session['clientes_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
            pagos_entidades_contrato = request.session['pagos_entidades_contrato']
            cuotas_efectivo_contrato = request.session['cuotas_efectivo_contrato']
            adicionales_agrupacion_inmueble_contrato = request.session['adicionales_agrupacion_inmueble_contrato']
            adicionales_agregar = request.session['adicionales_agregar']
        except :
            pass
        if clientes_contrato != None and adicionales_agrupacion_inmueble_contrato != None and pagos_entidades_contrato != None and cuotas_efectivo_contrato != None and adicionales_agrupacion_inmueble_contrato != None and adicionales_agregar != None:
            if request.is_ajax():
                proyecto = Proyecto.objects.get(id=proyecto_id)
                contrato_venta = proyecto.contratoventa_set.get(id=contrato_venta_id)
                tipo_adicional = None
                criterio = criterio.strip()

                # Filtra los adicionales del proyecto
                if tipo_adicional_id != None:
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
                pag = Paginador(request, adicionales_agrupacion_inmueble, 20, pagina)
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


def paginar_busqueda_clientes_modificar_contrato_venta2(request, pagina, criterio, contrato_venta_id, proyecto_id):
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
                clientes = clientes.filter(Q(nombre_1__icontains=criterio) | Q(nombre_2__icontains=criterio) | Q(apellido_1__icontains=criterio) | Q(apellido_2__icontains=criterio))

                # Excluye los clientes que ya se encuentran en el contrato
                ids_clientes_contrato = []
                for cliente_contrato in clientes_contrato:
                    ids_clientes_contrato.append(cliente_contrato.id)
                clientes = clientes.exclude(id__in=ids_clientes_contrato)
                pag = Paginador(request, clientes, 20, pagina)
                render = render_to_string('ajax/ventas/busquedaclientesmodificarcontratoventa.html', {'user': user, 'clientes': pag, 'clientes_seleccionados': clientes_agregar, 'criterio': criterio, 'contrato_venta': contrato_venta, 'proyecto': proyecto})
                dajax.assign('#light', 'innerHTML', render)
            else:
                dajax.redirect('/inverboy/home/')
        else:
            dajax.redirect('/inverboy/home/')
    else:
        dajax.redirect('/inverboy/')
    return dajax.json()


#### #### MODULO VENTAS #### ####