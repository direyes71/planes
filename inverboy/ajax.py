from ajax_archivos_proyecto.ajax_busquedas import *
from ajax_archivos_proyecto.ajax_paginacion import *
from ajax_archivos_proyecto.ajax_cargar_funciones import *
from ajax_archivos_proyecto.ajax_funciones_modulos import *
from ajax_archivos_proyecto.ajax_modulo_ventas.ajax_funciones_modulo_ventas import *
from dajaxice.core import dajaxice_functions

from dajax.core import Dajax
from django.template.loader import render_to_string
from inverboy.models import *
#from Inverboy.views import *

# PAGINACION
from inverboy.paginator import *

## CONSULTAS ANIDADAS
from django.db.models import Q

#---------------------------------------------------------------------------------------
#AJAX PARA BUSQUEDAS
def buscar_usuarios(request, pagina, criterio, cargo_usuario, proyecto_id):
    return buscar_usuarios2(request, pagina, criterio, cargo_usuario, proyecto_id)
dajaxice_functions.register(buscar_usuarios)

def buscar_proveedores(request, pagina, criterio):
    return buscar_proveedores2(request, pagina, criterio)
dajaxice_functions.register(buscar_proveedores)

def buscar_proveedores_suministro_add(request, pagina, criterio):
    return buscar_proveedores_suministro_add2(request, pagina, criterio)
dajaxice_functions.register(buscar_proveedores_suministro_add)

def buscar_suministros(request, pagina, clasificacion_general, criterio, proyecto_id):
    return buscar_suministros2(request, pagina, clasificacion_general, criterio, proyecto_id)
dajaxice_functions.register(buscar_suministros)

def buscar_suministros_apu_add(request, pagina, clasificacion_general, criterio):
    return buscar_suministros_apu_add2(request, pagina, clasificacion_general, criterio)
dajaxice_functions.register(buscar_suministros_apu_add)

def buscar_apus_proyecto(request, capitulo_id, subcapitulo_id, criterio, proyecto_id):
    return buscar_apus_proyecto2(request, 1, capitulo_id, subcapitulo_id, criterio, proyecto_id)
dajaxice_functions.register(buscar_apus_proyecto)

def buscar_proveedores_suministro_contizacion_add(request, suministro_id, criterio, proyecto_id):
    return buscar_proveedores_suministro_contizacion_add2(request, suministro_id, criterio, proyecto_id)
dajaxice_functions.register(buscar_proveedores_suministro_contizacion_add)

def buscar_suministros_proveedor_contizacion_add(request, criterio, proveedor_id, proyecto_id):
    return buscar_suministros_proveedor_contizacion_add2(request, criterio, proveedor_id, proyecto_id)
dajaxice_functions.register(buscar_suministros_proveedor_contizacion_add)

def buscar_items_orden_compra_informe_recepcion(request, criterio, orden_compra_id, proyecto_id):
    return buscar_items_orden_compra_informe_recepcion2(request, 1, criterio, orden_compra_id, proyecto_id)
dajaxice_functions.register(buscar_items_orden_compra_informe_recepcion)

def buscar_suministros_almacen_informe_salida(request, criterio_suministro, proyecto_id):
    return buscar_suministros_almacen_informe_salida2(request, 1, criterio_suministro, proyecto_id)
dajaxice_functions.register(buscar_suministros_almacen_informe_salida)

def buscar_suministros_apu_proyecto_requisicion(request, criterio, apu_id, proyecto_id):
    buscar_suministros_apu_proyecto_requisicion2(request, 1, criterio, apu_id, proyecto_id)
dajaxice_functions.register(buscar_suministros_apu_proyecto_requisicion)

def buscar_suministros_proveedor_contizacion_orden_servicio_add(request, criterio='', proveedor_id=0, proyecto_id=0):
    return buscar_suministros_proveedor_contizacion_orden_servicio_add2(request, criterio, proveedor_id, proyecto_id)
dajaxice_functions.register(buscar_suministros_proveedor_contizacion_orden_servicio_add)

def buscar_items_orden_servicio_corte_diario_obra(request, criterio, orden_servicio_id, proyecto_id):
    return buscar_items_orden_servicio_corte_diario_obra2(request, 1, criterio, orden_servicio_id, proyecto_id)
dajaxice_functions.register(buscar_items_orden_servicio_corte_diario_obra)

def buscar_items_orden_giro_proyecto_add(request, pagina, criterio, proyecto_id):
    return buscar_items_orden_giro_proyecto_add2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(buscar_items_orden_giro_proyecto_add)

def buscar_proveedores_orden_giro_proyecto_add(request, pagina, criterio, proyecto_id):
    return buscar_proveedores_orden_giro_proyecto_add2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(buscar_proveedores_orden_giro_proyecto_add)

def buscar_items_acta_conformidad_add(request, pagina, criterio, orden_giro_id, proyecto_id):
    return buscar_items_acta_conformidad_add2(request, pagina, criterio, orden_giro_id, proyecto_id)
dajaxice_functions.register(buscar_items_acta_conformidad_add)

#---------------------------------------------------------------------------------------
#AJAX PARA CARGAR FUNCIONES

def cargar_municipios(request, option, elemento):
    return cargar_municipios2(request, option, elemento)
dajaxice_functions.register(cargar_municipios)

def cargar_especificaciones(request, option, html):
    return cargar_especificaciones2(request, option, html)
dajaxice_functions.register(cargar_especificaciones)

def cargar_tipos(request, option, html):
    return cargar_tipos2(request, option, html)
dajaxice_functions.register(cargar_tipos)

def cargar_subcapitulos(request, option, html):
    return cargar_subcapitulos2(request, option, html)
dajaxice_functions.register(cargar_subcapitulos)

def cargar_subcapitulos_apus_proyectos(request, option, elemento):
    return cargar_subcapitulos_apus_proyectos2(request, option, elemento)
dajaxice_functions.register(cargar_subcapitulos_apus_proyectos)

def cargar_subcapitulos_apus_proyectos_busqueda(request, option, elemento):
    return cargar_subcapitulos_apus_proyectos_busqueda2(request, option, elemento)
dajaxice_functions.register(cargar_subcapitulos_apus_proyectos_busqueda)

def informacion_proveedor(request, id, indice):
    return informacion_proveedor2(request, id, indice)
dajaxice_functions.register(informacion_proveedor)

def informacion_suministro(request, id, indice):
    return informacion_suministro2(request, id, indice)
dajaxice_functions.register(informacion_suministro)

def informacion_proyecto(request, id, indice):
    return informacion_proyecto2(request, id, indice)
dajaxice_functions.register(informacion_proyecto)

def cargar_terceros_orden_servicio_add(request, proveedor_id, proyecto_id):
    return cargar_terceros_orden_servicio_add2(request, proveedor_id, proyecto_id)
dajaxice_functions.register(cargar_terceros_orden_servicio_add)

#### #### MODULO VENTAS #### ####
def informacion_cliente(request, cliente_id, indice):
    return informacion_cliente2(request, cliente_id, indice)
dajaxice_functions.register(informacion_cliente)
#### #### MODULO VENTAS #### ####

#--------------------------------------------------------------------------------------------
# AJAX PARA PAGINACION

def paginar_grupos_usuario(request, pagina, html, criterio):
    return paginar_grupos_usuario2(request, pagina,html, criterio)
dajaxice_functions.register(paginar_grupos_usuario)

def paginar_usuarios(request, pagina,html, criterio):
    return paginar_usuarios2(request, pagina,html, criterio)
dajaxice_functions.register(paginar_usuarios)

def paginar_proveedores(request, pagina, html, criterio):
    return paginar_proveedores2(request, pagina, html, criterio)
dajaxice_functions.register(paginar_proveedores)

def paginar_proveedores_compras(request, pagina, criterio, proyecto_id):
    return paginar_proveedores_compras2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_proveedores_compras)

def paginar_categorias_suministro(request, pagina, html, criterio):
    return paginar_categorias_suministro2(request, pagina, html, criterio)
dajaxice_functions.register(paginar_categorias_suministro)

def paginar_especificaciones_suministro(request, pagina, html, categoria_id, criterio):
    return paginar_especificaciones_suministro2(request, pagina, html, categoria_id, criterio)
dajaxice_functions.register(paginar_especificaciones_suministro)

def paginar_tipos_suministro(request, pagina, html, especificacion_id, criterio):
    return paginar_tipos_suministro2(request, pagina, html, especificacion_id, criterio)
dajaxice_functions.register(paginar_tipos_suministro)

def paginar_suministros(request, pagina, html, criterio):
    return paginar_suministros2(request, pagina, html, criterio)
dajaxice_functions.register(paginar_suministros)

def paginar_capitulos_apus(request, pagina, html, criterio):
    return paginar_capitulos_apus2(request, pagina, html, criterio)
dajaxice_functions.register(paginar_capitulos_apus)

def paginar_subcapitulos_apus(request, pagina, html, capitulo_id, criterio):
    return paginar_subcapitulos_apus2(request, pagina, html, capitulo_id, criterio)
dajaxice_functions.register(paginar_subcapitulos_apus)

def paginar_proveedores_suministro_add(request, pagina=1):
    return paginar_proveedores_suministro_add2(request, pagina)
dajaxice_functions.register(paginar_proveedores_suministro_add)

def paginar_suministros_apu_add(request, pagina):
    return paginar_suministros_apu_add2(request, pagina)
dajaxice_functions.register(paginar_suministros_apu_add)

def paginar_suministros_apu_details(request, apu_id, pagina):
    return paginar_suministros_apu_details2(request, apu_id, pagina)
dajaxice_functions.register(paginar_suministros_apu_details)

def paginar_apus(request, pagina, html, criterio, capitulo_id, subcapitulo_id):
    return paginar_apus2(request, pagina, html, criterio, capitulo_id, subcapitulo_id)
dajaxice_functions.register(paginar_apus)

def paginar_proyectos(request, pagina, criterio):
    return paginar_proyectos2(request, pagina, criterio)
dajaxice_functions.register(paginar_proyectos)

def paginar_capitulos_apu_proyecto(request, pagina, criterio, proyecto_id):
    return paginar_capitulos_apu_proyecto2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_capitulos_apu_proyecto)

def paginar_subcapitulos_apu_proyecto(request, pagina, criterio, proyecto_id, capitulo_id):
    return paginar_subcapitulos_apu_proyecto2(request, pagina, criterio, proyecto_id, capitulo_id)
dajaxice_functions.register(paginar_subcapitulos_apu_proyecto)

def paginar_apus_maestros_proyecto(request, pagina, criterio, capitulo_id, subcapitulo_id, proyecto_id):
    return paginar_apus_maestros_proyecto2(request, pagina, criterio, capitulo_id, subcapitulo_id, proyecto_id)
dajaxice_functions.register(paginar_apus_maestros_proyecto)

def paginar_suministros_apu_proyecto_add(request, pagina, proyecto_id):
    return paginar_suministros_apu_proyecto_add2(request, pagina, proyecto_id)
dajaxice_functions.register(paginar_suministros_apu_proyecto_add)

def paginar_apus_proyecto(request, pagina, html, criterio, capitulo_id, subcapitulo_id, proyecto_id):
    return paginar_apus_proyecto2(request, pagina, html, criterio, capitulo_id, subcapitulo_id, proyecto_id)
dajaxice_functions.register(paginar_apus_proyecto)

def paginar_suministros_apu_proyecto(request, pagina, apu_proyecto_id, proyecto_id):
    return paginar_suministros_apu_proyecto2(request, pagina, apu_proyecto_id, proyecto_id)
dajaxice_functions.register(paginar_suministros_apu_proyecto)

def paginar_apus_proyecto_requisicion(request, pagina, criterio, tipo_busqueda, capitulo_id, subcapitulo_id, proyecto_id):
    return paginar_apus_proyecto_requisicion2(request, pagina, criterio, tipo_busqueda, capitulo_id, subcapitulo_id, proyecto_id)
dajaxice_functions.register(paginar_apus_proyecto_requisicion)

def paginar_suministros_apu_proyecto_requisicion_add(request, pagina, criterio, apu_id, proyecto_id):
    return paginar_suministros_apu_proyecto_requisicion_add2(request, pagina, criterio, apu_id, proyecto_id)
dajaxice_functions.register(paginar_suministros_apu_proyecto_requisicion_add)

def paginar_requisiciones(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    return paginar_requisiciones2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id)
dajaxice_functions.register(paginar_requisiciones)

def paginar_requisiciones_aprobar(request, pagina, criterio, proyecto_id):
    return paginar_requisiciones_aprobar2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_requisiciones_aprobar)

def paginar_suministros_requisicion_add(request, pagina, proyecto_id):
    return paginar_suministros_requisicion_add2(request, pagina, proyecto_id)
dajaxice_functions.register(paginar_suministros_requisicion_add)

def paginar_suministros_requisicion(request, pagina, requisicion_id, proyecto_id):
    return paginar_suministros_requisicion2(request, pagina, requisicion_id, proyecto_id)
dajaxice_functions.register(paginar_suministros_requisicion)

def paginar_apus_proyecto_requisicion_indirectos_add(request, pagina, criterio, proyecto_id):
    return paginar_apus_proyecto_requisicion_indirectos_add2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_apus_proyecto_requisicion_indirectos_add)

def paginar_suministros_apu_proyecto_requisicion_indirectos_add(request, pagina, criterio, apu_id, proyecto_id):
    return paginar_suministros_apu_proyecto_requisicion_indirectos_add2(request, pagina, criterio, apu_id, proyecto_id)
dajaxice_functions.register(paginar_suministros_apu_proyecto_requisicion_indirectos_add)

def paginar_suministros_requisicion_indirectos_add(request, pagina, proyecto_id):
    return paginar_suministros_requisicion_indirectos_add2(request, pagina, proyecto_id)
dajaxice_functions.register(paginar_suministros_requisicion_indirectos_add)

def paginar_suministros_requisiciones_cotizacion_add(request, pagina, criterio, proyecto_id):
    return paginar_suministros_requisiciones_cotizacion_add2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_suministros_requisiciones_cotizacion_add)

def paginar_suministros_proveedor_cotizacion_add(request, pagina, criterio, proveedor_id, proyecto_id):
    return paginar_suministros_proveedor_cotizacion_add2(request, pagina, criterio, proveedor_id, proyecto_id)
dajaxice_functions.register(paginar_suministros_proveedor_cotizacion_add)

def paginar_proveedores_suministro_cotizacion_add(request, pagina, suministro_id, criterio, proyecto_id):
    return paginar_proveedores_suministro_cotizacion_add2(request, pagina, suministro_id, criterio, proyecto_id)
dajaxice_functions.register(paginar_proveedores_suministro_cotizacion_add)

def paginar_cotizaciones(request, pagina, criterio, proyecto_id):
    return paginar_cotizaciones2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_cotizaciones)

def paginar_suministros_cotizacion(request, pagina, cotizacion_id, proyecto_id):
    return paginar_suministros_cotizacion2(request, pagina, cotizacion_id, proyecto_id)
dajaxice_functions.register(paginar_suministros_cotizacion)

def paginar_cotizaciones_orden_servicio(request, pagina, criterio, proyecto_id):
    return paginar_cotizaciones_orden_servicio2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_cotizaciones_orden_servicio)

def paginar_ordenes_compra(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    return paginar_ordenes_compra2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id)
dajaxice_functions.register(paginar_ordenes_compra)

def paginar_suministros_orden_compra(request, pagina, orden_compra_id, proyecto_id):
    return paginar_suministros_orden_compra2(request, pagina, orden_compra_id, proyecto_id)
dajaxice_functions.register(paginar_suministros_orden_compra)

def paginar_suministros_proveedor_orden_compra_change(request, pagina, criterio, orden_compra_id, proyecto_id):
    return paginar_suministros_proveedor_orden_compra_change2(request, pagina, criterio, orden_compra_id, proyecto_id)
dajaxice_functions.register(paginar_suministros_proveedor_orden_compra_change)

def paginar_suministros_orden_compra_change(request, pagina, orden_compra_id, proyecto_id):
    return paginar_suministros_orden_compra_change2(request, pagina, orden_compra_id, proyecto_id)
dajaxice_functions.register(paginar_suministros_orden_compra_change)

def paginar_items_informe_recepcion(request, pagina, criterio, orden_compra_id, proyecto_id):
    return paginar_items_informe_recepcion2(request, pagina, criterio, orden_compra_id, proyecto_id)
dajaxice_functions.register(paginar_items_informe_recepcion)

def paginar_suministros_almacen(request, pagina, criterio, proyecto_id):
    return paginar_suministros_almacen2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_suministros_almacen)

def paginar_suministros_almacen_informe_salida_add(request, pagina, criterio_suministro, proyecto_id):
    return paginar_suministros_almacen_informe_salida_add2(request, pagina, criterio_suministro, proyecto_id)
dajaxice_functions.register(paginar_suministros_almacen_informe_salida_add)

def paginar_ordenes_compra_informe_recepcion_add(request, pagina, criterio, proyecto_id):
    return paginar_ordenes_compra_informe_recepcion_add2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_ordenes_compra_informe_recepcion_add)

def paginar_informes_entrega(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    return paginar_informes_entrega2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id)
dajaxice_functions.register(paginar_informes_entrega)

def paginar_suministros_informe_recepcion(request, pagina, informe_recepcion_id, proyecto_id):
    return paginar_suministros_informe_recepcion2(request, pagina, informe_recepcion_id, proyecto_id)
dajaxice_functions.register(paginar_suministros_informe_recepcion)

def paginar_informes_salida(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    return paginar_informes_salida2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id)
dajaxice_functions.register(paginar_informes_salida)

def paginar_suministros_informe_salida(request, pagina, informe_salida_id, proyecto_id):
    return paginar_suministros_informe_salida2(request, pagina, informe_salida_id, proyecto_id)
dajaxice_functions.register(paginar_suministros_informe_salida)

def paginar_suministros_requisiciones_cotizacion_orden_servicio_add(request, pagina, criterio, proyecto_id):
    return paginar_suministros_requisiciones_cotizacion_orden_servicio_add2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_suministros_requisiciones_cotizacion_orden_servicio_add)

def paginar_proveedores_orden_servicio_add(request, pagina, criterio, proyecto_id):
    return paginar_proveedores_orden_servicio_add2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_proveedores_orden_servicio_add)

def paginar_suministros_proveedor_cotizacion_orden_servicio_add(request, pagina, criterio, proveedor_id, proyecto_id):
    return paginar_suministros_proveedor_cotizacion_orden_servicio_add2(request, pagina, criterio, proveedor_id, proyecto_id)
dajaxice_functions.register(paginar_suministros_proveedor_cotizacion_orden_servicio_add)

def paginar_ordenes_servicio(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    return paginar_ordenes_servicio2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id)
dajaxice_functions.register(paginar_ordenes_servicio)

def paginar_suministros_orden_servicio(request, pagina, orden_servicio_id, proyecto_id):
    return paginar_suministros_orden_servicio2(request, pagina, orden_servicio_id, proyecto_id)
dajaxice_functions.register(paginar_suministros_orden_servicio)

def paginar_suministros_orden_servicio_change(request, pagina, orden_servicio_id, proyecto_id):
    return paginar_suministros_orden_servicio_change2(request, pagina, orden_servicio_id, proyecto_id)
dajaxice_functions.register(paginar_suministros_orden_servicio_change)

def paginar_suministros_proveedor_orden_servicio_change(request, pagina, criterio, orden_servicio_id, proyecto_id):
    return paginar_suministros_proveedor_orden_servicio_change2(request, pagina, criterio, orden_servicio_id, proyecto_id)
dajaxice_functions.register(paginar_suministros_proveedor_orden_servicio_change)

def paginar_ordenes_servicio_corte_diario_obra_add(request, pagina, criterio, proyecto_id):
    return paginar_ordenes_servicio_corte_diario_obra_add2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_ordenes_servicio_corte_diario_obra_add)

def paginar_items_corte_diario_obra_add(request, pagina, criterio, orden_servicio_id, proyecto_id):
    return paginar_items_corte_diario_obra_add2(request, pagina, criterio, orden_servicio_id, proyecto_id)
dajaxice_functions.register(paginar_items_corte_diario_obra_add)

def paginar_cortes_diario_obra(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    return paginar_cortes_diario_obra2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id)
dajaxice_functions.register(paginar_cortes_diario_obra)

def paginar_suministros_corte_diario_obra(request, pagina, corte_diario_obra_id, proyecto_id):
    return paginar_suministros_corte_diario_obra2(request, pagina, corte_diario_obra_id, proyecto_id)
dajaxice_functions.register(paginar_suministros_corte_diario_obra)

def paginar_proveedores_acta_recibo_obra_add(request, pagina, criterio, proyecto_id):
    return paginar_proveedores_acta_recibo_obra_add2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_proveedores_acta_recibo_obra_add)

def paginar_ordenes_servicio_acta_recibo_obra_add(request, pagina, proveedor_id, proyecto_id):
    return paginar_ordenes_servicio_acta_recibo_obra_add2(request, pagina, proveedor_id, proyecto_id)
dajaxice_functions.register(paginar_ordenes_servicio_acta_recibo_obra_add)

def paginar_actas_recibo_obra(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    return paginar_actas_recibo_obra2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id)
dajaxice_functions.register(paginar_actas_recibo_obra)

def paginar_actas_recibo_obra_aprobar(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    return paginar_actas_recibo_obra_aprobar2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id)
dajaxice_functions.register(paginar_actas_recibo_obra_aprobar)

def paginar_actas_recibo_obra_reporte_pago(request, pagina, criterio, fecha_inicial, fecha_final, tipo_busqueda, proyecto_id):
    return paginar_actas_recibo_obra_reporte_pago2(request, pagina, criterio, fecha_inicial, fecha_final, tipo_busqueda, proyecto_id)
dajaxice_functions.register(paginar_actas_recibo_obra_reporte_pago)

def paginar_suministros_requisiciones_orden_giro_add(request, pagina, criterio, proyecto_id):
    return paginar_suministros_requisiciones_orden_giro_add2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_suministros_requisiciones_orden_giro_add)

def paginar_proveedores_orden_giro_add(request, pagina, criterio, proyecto_id):
    return paginar_proveedores_orden_giro_add2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_proveedores_orden_giro_add)

def paginar_ordenes_giro(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    return paginar_ordenes_giro2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id)
dajaxice_functions.register(paginar_ordenes_giro)

def paginar_items_orden_giro(request, pagina, orden_giro_id, proyecto_id):
    return paginar_items_orden_giro2(request, pagina, orden_giro_id, proyecto_id)
dajaxice_functions.register(paginar_items_orden_giro)

def paginar_ordenes_giro_acta_conformidad_add(request, pagina, criterio, proyecto_id):
    return paginar_ordenes_giro_acta_conformidad_add2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_ordenes_giro_acta_conformidad_add)

def paginar_actas_conformidad(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    return paginar_actas_conformidad2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id)
dajaxice_functions.register(paginar_actas_conformidad)

def paginar_items_acta_conformidad(request, pagina, acta_conformidad_id, proyecto_id):
    return paginar_items_acta_conformidad2(request, pagina, acta_conformidad_id, proyecto_id)
dajaxice_functions.register(paginar_items_acta_conformidad)

def paginar_proveedores_factura_orden_compra_proyecto_add(request, pagina, criterio, proyecto_id):
    return paginar_proveedores_factura_orden_compra_proyecto_add2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_proveedores_factura_orden_compra_proyecto_add)

def paginar_ordenes_compra_proveedor_factura_orden_compra_proyecto_add(request, pagina, proveedor_id, criterio, proyecto_id):
    return paginar_ordenes_compra_proveedor_factura_orden_compra_proyecto_add2(request, pagina, proveedor_id, criterio, proyecto_id)
dajaxice_functions.register(paginar_ordenes_compra_proveedor_factura_orden_compra_proyecto_add)

def paginar_informes_recepcion_factura_orden_compra_proyecto_add(request, pagina, orden_compra_id, criterio, proyecto_id):
    return paginar_informes_recepcion_factura_orden_compra_proyecto_add2(request, pagina, orden_compra_id, criterio, proyecto_id)
dajaxice_functions.register(paginar_informes_recepcion_factura_orden_compra_proyecto_add)

def paginar_items_factura_orden_compra_add(request, pagina, proveedor_id, proyecto_id):
    return paginar_items_factura_orden_compra_add2(request, pagina, proveedor_id, proyecto_id)
dajaxice_functions.register(paginar_items_factura_orden_compra_add)

def paginar_facturas_ordenes_compra(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id):
    return paginar_facturas_ordenes_compra2(request, pagina, criterio, fecha_inicial, fecha_final, proyecto_id)
dajaxice_functions.register(paginar_facturas_ordenes_compra)

def paginar_items_factura_orden_compra(request, pagina, factura_orden_compra_id, proyecto_id):
    return paginar_items_factura_orden_compra2(request, pagina, factura_orden_compra_id, proyecto_id)
dajaxice_functions.register(paginar_items_factura_orden_compra)

#### #### MODULO VENTAS #### ####

def paginar_encuestas(request, pagina, criterio):
    return paginar_encuestas2(request, pagina, criterio)
dajaxice_functions.register(paginar_encuestas)

def paginar_tipos_adicional(request, pagina, criterio, proyecto_id):
    return paginar_tipos_adicional2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_tipos_adicional)

def paginar_adicionales(request, pagina, tipo_adicional_id=None, criterio='', proyecto_id=None):
    return paginar_adicionales2(request, pagina, tipo_adicional_id, criterio, proyecto_id)
dajaxice_functions.register(paginar_adicionales)

def paginar_clientes(request, pagina, criterio, proyecto_id):
    return paginar_clientes2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_clientes)

def paginar_secciones_proyecto(request, pagina, criterio, proyecto_id):
    return paginar_secciones_proyecto2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_secciones_proyecto)

def paginar_tipo_inmuebles(request, pagina, criterio, proyecto_id):
    return paginar_tipo_inmuebles2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_tipo_inmuebles)

def paginar_inmuebles(request, pagina, tipo_inmueble_id, seccion_proyecto_id, criterio, proyecto_id):
    return paginar_inmuebles2(request, pagina, tipo_inmueble_id, seccion_proyecto_id, criterio, proyecto_id)
dajaxice_functions.register(paginar_inmuebles)

def paginar_agrupaciones(request, pagina, criterio, proyecto_id):
    return paginar_agrupaciones2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_agrupaciones)

def paginar_busqueda_agrupaciones_nuevo_prospecto_venta(request, pagina, criterio, proyecto_id):
    return paginar_busqueda_agrupaciones_nuevo_prospecto_venta2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_busqueda_agrupaciones_nuevo_prospecto_venta)

def paginar_busqueda_agrupaciones_detalles_prospecto_venta(request, pagina, criterio, prospecto_venta_id, proyecto_id):
    return paginar_busqueda_agrupaciones_detalles_prospecto_venta2(request, pagina, criterio, prospecto_venta_id, proyecto_id)
dajaxice_functions.register(paginar_busqueda_agrupaciones_detalles_prospecto_venta)

def paginar_agrupaciones_nuevo_contrato_venta(request, pagina, criterio, proyecto_id):
    return paginar_agrupaciones_nuevo_contrato_venta2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_agrupaciones_nuevo_contrato_venta)

def paginar_busqueda_clientes_nuevo_contrato_venta(request, pagina, criterio, prospecto_venta_id, proyecto_id):
    return paginar_busqueda_clientes_nuevo_contrato_venta2(request, pagina, criterio, prospecto_venta_id, proyecto_id)
dajaxice_functions.register(paginar_busqueda_clientes_nuevo_contrato_venta)

def paginar_busqueda_adicionales_agrupacion_inmueble_nuevo_contrato_venta(request, pagina, tipo_adicional_id=None, criterio='', prospecto_venta_id=None, proyecto_id=None):
    return paginar_busqueda_adicionales_agrupacion_inmueble_nuevo_contrato_venta2(request, pagina, tipo_adicional_id, criterio, prospecto_venta_id, proyecto_id)
dajaxice_functions.register(paginar_busqueda_adicionales_agrupacion_inmueble_nuevo_contrato_venta)

def paginar_busqueda_agrupaciones_inmueble_agregar_convenio_prospecto_venta(request, pagina, criterio, prospecto_venta_id, proyecto_id):
    return paginar_busqueda_agrupaciones_inmueble_agregar_convenio_prospecto_venta2(request, pagina, criterio, prospecto_venta_id, proyecto_id)
dajaxice_functions.register(paginar_busqueda_agrupaciones_inmueble_agregar_convenio_prospecto_venta)

def paginar_contratos_venta(request, pagina, criterio, proyecto_id):
    return paginar_contratos_venta2(request, pagina, criterio, proyecto_id)
dajaxice_functions.register(paginar_contratos_venta)

def paginar_busqueda_adicionales_agrupacion_inmueble_modificar_contrato_venta(request, pagina, tipo_adicional_id=None, criterio='', contrato_venta_id=None, proyecto_id=None):
    return paginar_busqueda_adicionales_agrupacion_inmueble_modificar_contrato_venta2(request, pagina, tipo_adicional_id, criterio, contrato_venta_id, proyecto_id)
dajaxice_functions.register(paginar_busqueda_adicionales_agrupacion_inmueble_modificar_contrato_venta)

def paginar_busqueda_clientes_modificar_contrato_venta(request, pagina, criterio, contrato_venta_id, proyecto_id):
    return paginar_busqueda_clientes_modificar_contrato_venta2(request, pagina, criterio, contrato_venta_id, proyecto_id)
dajaxice_functions.register(paginar_busqueda_clientes_modificar_contrato_venta)

#### #### MODULO VENTAS #### ####
#---------------------------------------------------------------------------------------------------
#AJAX CON FUNCIONES PARA CADA MODULO

def ventana_contacto_proveedor(request):
    return ventana_contacto_proveedor2(request)
dajaxice_functions.register(ventana_contacto_proveedor)

def agregar_contacto_proveedor(request, nombre, cargo, telefono, ext, celular, email):
    return agregar_contacto_proveedor2(request, nombre, cargo, telefono, ext, celular, email)
dajaxice_functions.register(agregar_contacto_proveedor)

def ventana_modificar_contacto_proveedor(request, indice):
    return ventana_modificar_contacto_proveedor2(request, indice)
dajaxice_functions.register(ventana_modificar_contacto_proveedor)

def modificar_contacto_proveedor(request, indice, nombre, cargo, telefono, ext, celular, email):
    return modificar_contacto_proveedor2(request, indice, nombre, cargo, telefono, ext, celular, email)
dajaxice_functions.register(modificar_contacto_proveedor)

def eliminar_contacto_proveedor(request, indice):
    return eliminar_contacto_proveedor2(request, indice)
dajaxice_functions.register(eliminar_contacto_proveedor)

def seleccionar_proveedor_lista_proveedores_suministro_add(request, parametro, proveedor_id, pagina, criterio):
    return seleccionar_proveedor_lista_proveedores_suministro_add2(request, parametro, proveedor_id, pagina, criterio)
dajaxice_functions.register(seleccionar_proveedor_lista_proveedores_suministro_add)

def agregar_proveedor_suministro_add(request, proveedor_id, precio, iva, criterio, pagina):
    return agregar_proveedor_suministro_add2(request, proveedor_id, precio, iva, criterio, pagina)
dajaxice_functions.register(agregar_proveedor_suministro_add)

def agregar_proveedores_suministro_add(request):
    return agregar_proveedores_suministro_add2(request)
dajaxice_functions.register(agregar_proveedores_suministro_add)

def cancelar_agregar_proveedores_suministro_add(request):
    return cancelar_agregar_proveedores_suministro_add2(request)
dajaxice_functions.register(cancelar_agregar_proveedores_suministro_add)

def eliminar_proveedor_suministro_add(request, proveedor_id, pagina):
    return eliminar_proveedor_suministro_add2(request, proveedor_id, pagina)
dajaxice_functions.register(eliminar_proveedor_suministro_add)

def activar_input_precio_proveedor_suministro_add(request, proveedor_id, pagina):
    return activar_input_precio_proveedor_suministro_add2(request, proveedor_id, pagina)
dajaxice_functions.register(activar_input_precio_proveedor_suministro_add)

def modificar_precio_proveedor_suministro_add(request, proveedor_id, precio, pagina):
    return modificar_precio_proveedor_suministro_add2(request, proveedor_id, precio, pagina)
dajaxice_functions.register(modificar_precio_proveedor_suministro_add)

def activar_input_iva_proveedor_suministro_add(request, proveedor_id, pagina):
    return activar_input_iva_proveedor_suministro_add2(request, proveedor_id, pagina)
dajaxice_functions.register(activar_input_iva_proveedor_suministro_add)

def modificar_iva_proveedor_suministro_add(request, proveedor_id, iva, pagina):
    return modificar_iva_proveedor_suministro_add2(request, proveedor_id, iva, pagina)
dajaxice_functions.register(modificar_iva_proveedor_suministro_add)

def seleccionar_suministro_lista_suministros_apu_add(request, parametro, suministro_id, pagina, clasificacion_general, criterio):
    return seleccionar_suministro_lista_suministros_apu_add2(request, parametro, suministro_id, pagina, clasificacion_general, criterio)
dajaxice_functions.register(seleccionar_suministro_lista_suministros_apu_add)

def agregar_suministro_apu_add(request, suministro_id, cantidad, clasificacion_general, criterio, pagina):
    return agregar_suministro_apu_add2(request, suministro_id, cantidad, clasificacion_general, criterio, pagina)
dajaxice_functions.register(agregar_suministro_apu_add)

def agregar_suministros_apu_add(request):
    return agregar_suministros_apu_add2(request)
dajaxice_functions.register(agregar_suministros_apu_add)

def cancelar_agregar_suministros_apu_add(request):
    return cancelar_agregar_suministros_apu_add2(request)
dajaxice_functions.register(cancelar_agregar_suministros_apu_add)

def eliminar_suministro_apu_add(request, suministro_id, pagina):
    return eliminar_suministro_apu_add2(request, suministro_id, pagina)
dajaxice_functions.register(eliminar_suministro_apu_add)

def activar_input_precio_suministro_apu_add(request, suministro_id, pagina):
    return activar_input_precio_suministro_apu_add2(request, suministro_id, pagina)
dajaxice_functions.register(activar_input_precio_suministro_apu_add)

def modificar_precio_suministro_apu_add(request, suministro_id, precio, pagina):
    return modificar_precio_suministro_apu_add2(request, suministro_id, precio, pagina)
dajaxice_functions.register(modificar_precio_suministro_apu_add)

def activar_input_cantidad_suministro_apu_add(request, suministro_id, pagina):
    return activar_input_cantidad_suministro_apu_add2(request, suministro_id, pagina)
dajaxice_functions.register(activar_input_cantidad_suministro_apu_add)

def modificar_cantidad_suministro_apu_add(request, suministro_id, cantidad, pagina):
    return modificar_cantidad_suministro_apu_add2(request, suministro_id, cantidad, pagina)
dajaxice_functions.register(modificar_cantidad_suministro_apu_add)

def ventana_anadir_persona_administrativo_proyecto(request, proyecto_id):
    return ventana_anadir_persona_administrativo_proyecto2(request, proyecto_id)
dajaxice_functions.register(ventana_anadir_persona_administrativo_proyecto)

def seleccionar_usuario_persona_administrativo_proyecto_add(request, usuario_id, pagina, criterio, cargo_usuario, proyecto_id):
    return seleccionar_usuario_persona_administrativo_proyecto_add2(request, usuario_id, pagina, criterio, cargo_usuario, proyecto_id)
dajaxice_functions.register(seleccionar_usuario_persona_administrativo_proyecto_add)

def anadir_personas_administrativo_proyecto_add(request, proyecto_id):
    return anadir_personas_administrativo_proyecto_add2(request, proyecto_id)
dajaxice_functions.register(anadir_personas_administrativo_proyecto_add)

def cancelar_anadir_persona_administrativo_proyecto_add(request, proyecto_id):
    return cancelar_anadir_persona_administrativo_proyecto_add2(request, proyecto_id)
dajaxice_functions.register(cancelar_anadir_persona_administrativo_proyecto_add)

def eliminar_persona_administrativo_proyecto(request, usuario_id, proyecto_id):
    return eliminar_persona_administrativo_proyecto2(request, usuario_id, proyecto_id)
dajaxice_functions.register(eliminar_persona_administrativo_proyecto)

def ventana_persona_proyecto_add(request, proyecto_id):
    return ventana_persona_proyecto_add2(request, proyecto_id)
dajaxice_functions.register(ventana_persona_proyecto_add)

def anadir_persona_anexa_proyecto(request, identificacion, nombre, cargo, telefono, proveedor, proyecto_id):
    return anadir_persona_anexa_proyecto2(request, identificacion, nombre, cargo, telefono, proveedor, proyecto_id)
dajaxice_functions.register(anadir_persona_anexa_proyecto)

def ventana_modificar_persona_anexa_proveedor(request, persona_id, proyecto_id):
    return ventana_modificar_persona_anexa_proyecto2(request, persona_id, proyecto_id)
dajaxice_functions.register(ventana_modificar_persona_anexa_proveedor)

def modificar_persona_anexa_proyecto(request, persona_id, identificacion, nombre, cargo, telefono, proveedor, proyecto_id):
    return modificar_persona_anexa_proyecto2(request, persona_id, identificacion, nombre, cargo, telefono, proveedor, proyecto_id)
dajaxice_functions.register(modificar_persona_anexa_proyecto)

def eliminar_persona_proyecto(request, persona_id, proyecto_id):
    return eliminar_persona_proyecto2(request, persona_id, proyecto_id)
dajaxice_functions.register(eliminar_persona_proyecto)

def agregar_suministro_apu_proyecto_add(request, suministro_id, cantidad, clasificacion_general, criterio, pagina, proyecto_id):
    return agregar_suministro_apu_proyecto_add2(request, suministro_id, cantidad, clasificacion_general, criterio, pagina, proyecto_id)
dajaxice_functions.register(agregar_suministro_apu_proyecto_add)

def agregar_suministros_apu_proyecto_add(request, proyecto_id):
    return agregar_suministros_apu_proyecto_add2(request, proyecto_id)
dajaxice_functions.register(agregar_suministros_apu_proyecto_add)

def cancelar_agregar_suministros_apu_proyecto_add(request, proyecto_id):
    return cancelar_agregar_suministros_apu_proyecto_add2(request, proyecto_id)
dajaxice_functions.register(cancelar_agregar_suministros_apu_proyecto_add)

def eliminar_suministro_apu_proyecto_add(request, suministro_id, pagina, proyecto_id):
    return eliminar_suministro_apu_proyecto_add2(request, suministro_id, pagina, proyecto_id)
dajaxice_functions.register(eliminar_suministro_apu_proyecto_add)

def seleccionar_suministro_lista_suministros_apu_proyecto_add(request, parametro, suministro_id, pagina, clasificacion_general, criterio, proyecto_id):
    return seleccionar_suministro_lista_suministros_apu_proyecto_add2(request, parametro, suministro_id, pagina, clasificacion_general, criterio, proyecto_id)
dajaxice_functions.register(seleccionar_suministro_lista_suministros_apu_proyecto_add)

def calcular_valor_apu_proyecto_add(request, cantidad_proyecto, cantidad_apu, proyecto_id):
    return calcular_valor_apu_proyecto_add2(request, cantidad_proyecto, cantidad_apu, proyecto_id)
dajaxice_functions.register(calcular_valor_apu_proyecto_add)

def activar_input_precio_suministro_apu_proyecto_add(request, suministro_id, pagina, proyecto_id):
    return activar_input_precio_suministro_apu_proyecto_add2(request, suministro_id, pagina, proyecto_id)
dajaxice_functions.register(activar_input_precio_suministro_apu_proyecto_add)

def modificar_precio_suministro_apu_proyecto_add(request, suministro_id, precio, pagina, proyecto_id):
    return modificar_precio_suministro_apu_proyecto_add2(request, suministro_id, precio, pagina, proyecto_id)
dajaxice_functions.register(modificar_precio_suministro_apu_proyecto_add)

def activar_input_cantidad_suministro_apu_proyecto_add(request, suministro_id, pagina, proyecto_id):
    return activar_input_cantidad_suministro_apu_proyecto_add2(request, suministro_id, pagina, proyecto_id)
dajaxice_functions.register(activar_input_cantidad_suministro_apu_proyecto_add)

def modificar_cantidad_suministro_apu_proyecto_add(request, suministro_id, cantidad, cantidad_proyecto=None, cantidad_apu=None, pagina=1, proyecto_id=None):
    return modificar_cantidad_suministro_apu_proyecto_add2(request, suministro_id, cantidad, cantidad_proyecto, cantidad_apu, pagina, proyecto_id)
dajaxice_functions.register(modificar_cantidad_suministro_apu_proyecto_add)

def cambiar_manejo_estandar_apu_proyecto_add(request, parametro, proyecto_id):
    return cambiar_manejo_estandar_apu_proyecto_add2(request, parametro, proyecto_id)
dajaxice_functions.register(cambiar_manejo_estandar_apu_proyecto_add)

def asignar_suministro_estandar_apu_proyecto_add(request, suministro_id, parametro, pagina, proyecto_id):
    return asignar_suministro_estandar_apu_proyecto_add2(request, suministro_id, parametro, pagina, proyecto_id)
dajaxice_functions.register(asignar_suministro_estandar_apu_proyecto_add)

def modificar_apu_proyecto_manejo_estandar(request, proyecto_id):
    return eliminar_persona_proyecto2(request, persona_id, proyecto_id)
dajaxice_functions.register(eliminar_persona_proyecto)

def anadir_suministro_carrito(request, suministro_id, cantidad_requerir, observaciones, pagina, criterio, apu_id, proyecto_id):
    return anadir_suministro_carrito2(request, suministro_id, cantidad_requerir, observaciones, pagina, criterio, apu_id, proyecto_id)
dajaxice_functions.register(anadir_suministro_carrito)

def activar_modificar_suministro_carrito(request, suministro_id, apu_id, pagina, criterio, proyecto_id):
    return activar_modificar_suministro_carrito2(request, suministro_id, apu_id, pagina, criterio, proyecto_id)
dajaxice_functions.register(activar_modificar_suministro_carrito)

def activar_input_cantidad_suministro_carrito(request, suministro_id, pagina, proyecto_id):
    return activar_input_cantidad_suministro_carrito2(request, suministro_id, pagina, proyecto_id)
dajaxice_functions.register(activar_input_cantidad_suministro_carrito)

def modificar_suministro_carrito(request, suministro_id, cantidad_requerir, observaciones, pagina, proyecto_id):
    return modificar_suministro_carrito2(request, suministro_id, cantidad_requerir, observaciones, pagina, proyecto_id)
dajaxice_functions.register(modificar_suministro_carrito)

def del_suministro_carrito(request, suministro_id, pagina, proyecto_id):
    return del_suministro_carrito2(request, suministro_id, pagina, proyecto_id)
dajaxice_functions.register(del_suministro_carrito)

def anadir_suministro_carrito_requisicion_indirectos_add(request, suministro_id, cantidad_requerir, observaciones, pagina, criterio, apu_id, proyecto_id):
    return anadir_suministro_carrito_requisicion_indirectos_add2(request, suministro_id, cantidad_requerir, observaciones, pagina, criterio, apu_id, proyecto_id)
dajaxice_functions.register(anadir_suministro_carrito_requisicion_indirectos_add)

def activar_modificar_suministro_carrito_requisicion_indirectos_add(request, suministro_id, apu_id, pagina, criterio, proyecto_id):
    return activar_modificar_suministro_carrito_requisicion_indirectos_add2(request, suministro_id, apu_id, pagina, criterio, proyecto_id)
dajaxice_functions.register(activar_modificar_suministro_carrito_requisicion_indirectos_add)

def activar_input_cantidad_suministro_carrito_requisicion_indirectos_add(request, suministro_id, pagina, proyecto_id):
    return activar_input_cantidad_suministro_carrito_requisicion_indirectos_add2(request, suministro_id, pagina, proyecto_id)
dajaxice_functions.register(activar_input_cantidad_suministro_carrito_requisicion_indirectos_add)

def modificar_suministro_carrito_requisicion_indirectos_add(request, suministro_id, cantidad_requerir, observaciones, pagina, proyecto_id):
    return modificar_suministro_carrito_requisicion_indirectos_add2(request, suministro_id, cantidad_requerir, observaciones, pagina, proyecto_id)
dajaxice_functions.register(modificar_suministro_carrito_requisicion_indirectos_add)

def del_suministro_carrito_requisicion_indirectos_add(request, suministro_id, pagina, proyecto_id):
    return del_suministro_carrito_requisicion_indirectos_add2(request, suministro_id, pagina, proyecto_id)
dajaxice_functions.register(del_suministro_carrito_requisicion_indirectos_add)

def apus_proyecto(request, proyecto_id):
    return apus_proyecto2(request, proyecto_id)
dajaxice_functions.register(apus_proyecto)

def nueva_requisicion_details(request, proyecto_id):
    return nueva_requisicion_details2(request, proyecto_id)
dajaxice_functions.register(nueva_requisicion_details)

def realizar_requisicion(request, proyecto_id, fecha_arribo):
    return realizar_requisicion2(request, proyecto_id, fecha_arribo)
dajaxice_functions.register(realizar_requisicion)

def suministro_cotizar(request, suministro_id, proyecto_id):
    return suministro_cotizar2(request, suministro_id, proyecto_id)
dajaxice_functions.register(suministro_cotizar)

def seleccionar_proveedor_lista_proveedores_suministro_cotizacion_add(request, parametro, suministro_id, proveedor_id, pagina, criterio, proyecto_id):
    return seleccionar_proveedor_lista_proveedores_suministro_cotizacion_add2(request, parametro, suministro_id, proveedor_id, pagina, criterio, proyecto_id)
dajaxice_functions.register(seleccionar_proveedor_lista_proveedores_suministro_cotizacion_add)

def cotizar_suministro_proveedor(request, suministro_id, proveedor_id, cantidad, observaciones, pagina, criterio, proyecto_id):
    return cotizar_suministro_proveedor2(request, suministro_id, proveedor_id, cantidad, observaciones, pagina, criterio, proyecto_id)
dajaxice_functions.register(cotizar_suministro_proveedor)

def anadir_suministro_cotizacion(request, pagina, suministro_id, cantidad, observaciones, proveedor_id, criterio, proyecto_id):
    return anadir_suministro_cotizacion2(request, pagina, suministro_id, cantidad, observaciones, proveedor_id, criterio, proyecto_id)
dajaxice_functions.register(anadir_suministro_cotizacion)

def activar_input_cantidad_suministro_cotizacion_add(request, pagina, suministro_id, proveedor_id, criterio, proyecto_id):
    return activar_input_cantidad_suministro_cotizacion_add2(request, pagina, suministro_id, proveedor_id, criterio, proyecto_id)
dajaxice_functions.register(activar_input_cantidad_suministro_cotizacion_add)

def cotizar_todos_suministros_proveedor(request, proveedor_id, proyecto_id):
    return cotizar_todos_suministros_proveedor2(request, proveedor_id, proyecto_id)
dajaxice_functions.register(cotizar_todos_suministros_proveedor)

def eliminar_suministro_cotizacion(request, suministro_id, cotizacion_id, proyecto_id):
    return eliminar_suministro_cotizacion2(request, suministro_id, cotizacion_id, proyecto_id)
dajaxice_functions.register(eliminar_suministro_cotizacion)

## Provisional
def eliminar_suministros_cotizacion(request):
    return eliminar_suministros_cotizacion2(request)
dajaxice_functions.register(eliminar_suministros_cotizacion)

def eliminar_todos_suministros_cotizacion(request):
    return eliminar_todos_suministros_cotizacion2(request)
dajaxice_functions.register(eliminar_todos_suministros_cotizacion)
## Provisional

def activar_input_cantidad_suministro_cotizacion_orden_compra_add(request, pagina, suministro_id, cotizacion_id, proyecto_id):
    return activar_input_cantidad_suministro_cotizacion_orden_compra_add2(request, pagina, suministro_id, cotizacion_id, proyecto_id)
dajaxice_functions.register(activar_input_cantidad_suministro_cotizacion_orden_compra_add)

def modificar_suministro_cotizacion(request, suministro_id, cantidad, cotizacion_id, pagina, proyecto_id):
    return modificar_suministro_cotizacion2(request, suministro_id, cantidad, cotizacion_id, pagina, proyecto_id)
dajaxice_functions.register(modificar_suministro_cotizacion)

def modificar_suministro_cotizacion_orden_servicio(request, suministro_id, cantidad, cotizacion_id, pagina, proyecto_id):
    return modificar_suministro_cotizacion_orden_servicio2(request, suministro_id, cantidad, cotizacion_id, pagina, proyecto_id)
dajaxice_functions.register(modificar_suministro_cotizacion_orden_servicio)

def activar_input_precio_suministro_cotizacion_orden_compra_add(request, pagina, suministro_id, cotizacion_id, proyecto_id):
    return activar_input_precio_suministro_cotizacion_orden_compra_add2(request, pagina, suministro_id, cotizacion_id, proyecto_id)
dajaxice_functions.register(activar_input_precio_suministro_cotizacion_orden_compra_add)

def modificar_precio_suministro_cotizacion(request, suministro_id, precio, cotizacion_id, pagina, proyecto_id):
    return modificar_precio_suministro_cotizacion2(request, suministro_id, precio, cotizacion_id, pagina, proyecto_id)
dajaxice_functions.register(modificar_precio_suministro_cotizacion)

def modificar_iva_suministro_cotizacion(request, suministro_id, cotizacion_id, iva, pagina, proyecto_id):
    return modificar_iva_suministro_cotizacion2(request, suministro_id, cotizacion_id, iva, pagina, proyecto_id)
dajaxice_functions.register(modificar_iva_suministro_cotizacion)

def activar_input_observaciones_suministro_cotizacion_orden_compra_add(request, pagina, suministro_id, cotizacion_id, proyecto_id):
    return activar_input_observaciones_suministro_cotizacion_orden_compra_add2(request, pagina, suministro_id, cotizacion_id, proyecto_id)
dajaxice_functions.register(activar_input_observaciones_suministro_cotizacion_orden_compra_add)

def modificar_observaciones_suministro_cotizacion(request, suministro_id, observaciones, cotizacion_id, pagina, proyecto_id):
    return modificar_observaciones_suministro_cotizacion2(request, suministro_id, observaciones, cotizacion_id, pagina, proyecto_id)
dajaxice_functions.register(modificar_observaciones_suministro_cotizacion)

def realizar_cotizacion(request, proyecto_id):
    return realizar_cotizacion2(request, proyecto_id)
dajaxice_functions.register(realizar_cotizacion)

def realizar_orden_compra(request, cotizacion_id, fecha_arribo, forma_pago, parametro_pago, observaciones, proyecto_id):
    return realizar_orden_compra2(request, cotizacion_id, fecha_arribo, forma_pago, parametro_pago, observaciones, proyecto_id)
dajaxice_functions.register(realizar_orden_compra)

def eliminar_suministro_orden_compra(request, suministro_id, orden_compra_id, proyecto_id):
    return eliminar_suministro_orden_compra2(request, suministro_id, orden_compra_id, proyecto_id)
dajaxice_functions.register(eliminar_suministro_orden_compra)

def activar_input_cantidad_suministro_orden_compra_change(request, pagina, suministro_id, orden_compra_id, proyecto_id):
    return activar_input_cantidad_suministro_orden_compra_change2(request, pagina, suministro_id, orden_compra_id, proyecto_id)
dajaxice_functions.register(activar_input_cantidad_suministro_orden_compra_change)

def modificar_cantidad_suministro_orden_compra_change(request, suministro_id, cantidad, orden_compra_id, pagina, proyecto_id):
    return modificar_cantidad_suministro_orden_compra_change2(request, suministro_id, cantidad, orden_compra_id, pagina, proyecto_id)
dajaxice_functions.register(modificar_cantidad_suministro_orden_compra_change)

def activar_input_precio_suministro_orden_compra_change(request, pagina, suministro_id, orden_compra_id, proyecto_id):
    return activar_input_precio_suministro_orden_compra_change2(request, pagina, suministro_id, orden_compra_id, proyecto_id)
dajaxice_functions.register(activar_input_precio_suministro_orden_compra_change)

def modificar_precio_suministro_orden_compra_change(request, suministro_id, precio, orden_compra_id, pagina, proyecto_id):
    return modificar_precio_suministro_orden_compra_change2(request, suministro_id, precio, orden_compra_id, pagina, proyecto_id)
dajaxice_functions.register(modificar_precio_suministro_orden_compra_change)

def modificar_iva_suministro_orden_compra_change(request, suministro_id, iva, orden_compra_id, pagina, proyecto_id):
    return modificar_iva_suministro_orden_compra_change2(request, suministro_id, iva, orden_compra_id, pagina, proyecto_id)
dajaxice_functions.register(modificar_iva_suministro_orden_compra_change)

def activar_input_observaciones_suministro_orden_compra_change(request, pagina, suministro_id, orden_compra_id, proyecto_id):
    return activar_input_observaciones_suministro_orden_compra_change2(request, pagina, suministro_id, orden_compra_id, proyecto_id)
dajaxice_functions.register(activar_input_observaciones_suministro_orden_compra_change)

def modificar_observaciones_suministro_orden_compra_change(request, suministro_id, observaciones, orden_compra_id, pagina, proyecto_id):
    return modificar_observaciones_suministro_orden_compra_change2(request, suministro_id, observaciones, orden_compra_id, pagina, proyecto_id)
dajaxice_functions.register(modificar_observaciones_suministro_orden_compra_change)

def suministros_proveedor_orden_compra_change(request, orden_compra_id, criterio=None, proyecto_id=None):
    return suministros_proveedor_orden_compra_change2(request, orden_compra_id, criterio, proyecto_id)
dajaxice_functions.register(suministros_proveedor_orden_compra_change)

def anadir_suministro_orden_compra_change(request, pagina, suministro_id, cantidad, precio, iva_suministro, observaciones, orden_compra_id, criterio, proyecto_id):
    return anadir_suministro_orden_compra_change2(request, pagina, suministro_id, cantidad, precio, iva_suministro, observaciones, orden_compra_id, criterio, proyecto_id)
dajaxice_functions.register(anadir_suministro_orden_compra_change)

def activar_input_suministro_agregar_orden_compra_change(request, pagina, suministro_id, orden_compra_id, criterio, proyecto_id):
    return activar_input_suministro_agregar_orden_compra_change2(request, pagina, suministro_id, orden_compra_id, criterio, proyecto_id)
dajaxice_functions.register(activar_input_suministro_agregar_orden_compra_change)

def anadir_todos_suministros_orden_compra_change(request, orden_compra_id, proyecto_id):
    return anadir_todos_suministros_orden_compra_change2(request, orden_compra_id, proyecto_id)
dajaxice_functions.register(anadir_todos_suministros_orden_compra_change)

def anadir_suministros_orden_compra_change(request, orden_compra_id, proyecto_id):
    return anadir_suministros_orden_compra_change2(request, orden_compra_id, proyecto_id)
dajaxice_functions.register(anadir_suministros_orden_compra_change)

def cancelar_anadir_suministros_orden_compra_change(request, proyecto_id):
    return cancelar_anadir_suministros_orden_compra_change2(request, proyecto_id)
dajaxice_functions.register(cancelar_anadir_suministros_orden_compra_change)

def asignar_modificacion_orden_compra(request, permiso, orden_compra_id, proyecto_id):
    return asignar_modificacion_orden_compra2(request, permiso, orden_compra_id, proyecto_id)
dajaxice_functions.register(asignar_modificacion_orden_compra)

def compra_suministros_proveedor(request, proveedor_id, proyecto_id):
    return compra_suministros_proveedor2(request, proveedor_id, proyecto_id)
dajaxice_functions.register(compra_suministros_proveedor)

def agregar_suministro_informe_recepcion(request, pagina, suministro_id, orden_compra_id, criterio, proyecto_id, cantidad):
    return agregar_suministro_informe_recepcion2(request, pagina, suministro_id, orden_compra_id, criterio, proyecto_id, cantidad)
dajaxice_functions.register(agregar_suministro_informe_recepcion)

def activar_modificar_suministro_informe_recepcion(request, pagina, suministro_id, orden_compra_id, criterio, proyecto_id):
    return activar_modificar_suministro_informe_recepcion2(request, pagina, suministro_id, orden_compra_id, criterio, proyecto_id)
dajaxice_functions.register(activar_modificar_suministro_informe_recepcion)

def ventana_agregar_suministro_informe_salida(request, pagina, suministro_id, criterio_apu, criterio_suministro, pagina_suministro, proyecto_id):
    return ventana_agregar_suministro_informe_salida2(request, pagina, suministro_id, criterio_apu, criterio_suministro, pagina_suministro, proyecto_id)
dajaxice_functions.register(ventana_agregar_suministro_informe_salida)

def agregar_cantidad_apu_proyecto_informe_salida(request, pagina, suministro_id, apu_proyecto_id, cantidad, criterio_apu, criterio_suministro, pagina_suministro, proyecto_id):
    return agregar_cantidad_apu_proyecto_informe_salida2(request, pagina, suministro_id, apu_proyecto_id, cantidad, criterio_apu, criterio_suministro, pagina_suministro, proyecto_id)
dajaxice_functions.register(agregar_cantidad_apu_proyecto_informe_salida)

def activar_input_cantidad_apu_proyecto_informe_salida(request, pagina, suministro_id, apu_proyecto_id, criterio_apu, criterio_suministro, pagina_suministro, proyecto_id):
    return activar_input_cantidad_apu_proyecto_informe_salida2(request, pagina, suministro_id, apu_proyecto_id, criterio_apu, criterio_suministro, pagina_suministro, proyecto_id)
dajaxice_functions.register(activar_input_cantidad_apu_proyecto_informe_salida)

def agregar_suministro_informe_salida(request, pagina, suministro_id, criterio_suministro, pagina_suministro, proyecto_id):
    return agregar_suministro_informe_salida2(request, pagina, suministro_id, criterio_suministro, pagina_suministro, proyecto_id)
dajaxice_functions.register(agregar_suministro_informe_salida)

def cancelar_agregar_suministro_informe_salida(request, proyecto_id):
    return cancelar_agregar_suministro_informe_salida2(request, proyecto_id)
dajaxice_functions.register(cancelar_agregar_suministro_informe_salida)

def activar_input_cantidad_suministro_informe_salida(request, pagina, suministro_id, criterio, proyecto_id):
    return activar_input_cantidad_suministro_informe_salida2(request, pagina, suministro_id, criterio, proyecto_id)
dajaxice_functions.register(activar_input_cantidad_suministro_informe_salida)

#Ordenes de servicio
def seleccionar_proveedor_lista_proveedores_suministro_cotizacion_orden_servicio_add(request, parametro, suministro_id, proveedor_id, pagina, criterio, proyecto_id):
    return seleccionar_proveedor_lista_proveedores_suministro_cotizacion_orden_serivicio_add2(request, parametro, suministro_id, proveedor_id, pagina, criterio, proyecto_id)
dajaxice_functions.register(seleccionar_proveedor_lista_proveedores_suministro_cotizacion_orden_servicio_add)

def suministro_orden_servicio_cotizar(request, suministro_id, proyecto_id):
    return suministro_orden_servicio_cotizar2(request, suministro_id, proyecto_id)
dajaxice_functions.register(suministro_orden_servicio_cotizar)

def cotizar_suministro_orden_servicio_proveedor(request, suministro_id, proveedor_id, cantidad, pagina, criterio, proyecto_id):
    return cotizar_suministro_orden_servicio_proveedor2(request, suministro_id, proveedor_id, cantidad, pagina, criterio, proyecto_id)
dajaxice_functions.register(cotizar_suministro_orden_servicio_proveedor)

def anadir_suministro_cotizacion_orden_servicio(request, pagina, suministro_id, proveedor_id, criterio, proyecto_id, cantidad):
    return anadir_suministro_cotizacion_orden_servicio2(request, pagina, suministro_id, proveedor_id, criterio, proyecto_id, cantidad)
dajaxice_functions.register(anadir_suministro_cotizacion_orden_servicio)

def cotizar_todos_suministros_proveedor_orden_servicio_add(request, proveedor_id, proyecto_id):
    return cotizar_todos_suministros_proveedor_orden_servicio_add2(request, proveedor_id, proyecto_id)
dajaxice_functions.register(cotizar_todos_suministros_proveedor_orden_servicio_add)

def activar_input_cantidad_suministro_cotizacion_orden_servicio_add(request, pagina, suministro_id, proveedor_id, criterio, proyecto_id):
    return activar_input_cantidad_suministro_cotizacion_orden_servicio_add2(request, pagina, suministro_id, proveedor_id, criterio, proyecto_id)
dajaxice_functions.register(activar_input_cantidad_suministro_cotizacion_orden_servicio_add)

def activar_input_cantidad_suministro_cotizacion_realizar_orden_servicio(request, pagina, suministro_id, cotizacion_id, proyecto_id):
    return activar_input_cantidad_suministro_cotizacion_realizar_orden_servicio2(request, pagina, suministro_id, cotizacion_id, proyecto_id)
dajaxice_functions.register(activar_input_cantidad_suministro_cotizacion_realizar_orden_servicio)

def activar_input_precio_suministro_cotizacion_realizar_orden_servicio(request, pagina, suministro_id, cotizacion_id, proyecto_id):
    return activar_input_precio_suministro_cotizacion_realizar_orden_servicio2(request, pagina, suministro_id, cotizacion_id, proyecto_id)
dajaxice_functions.register(activar_input_precio_suministro_cotizacion_realizar_orden_servicio)

def cambiar_tipo_iva_cotizacion_orden_servicio_add(request, parametro, proyecto_id):
    return cambiar_tipo_iva_cotizacion_orden_servicio_add2(request, parametro, proyecto_id)
dajaxice_functions.register(cambiar_tipo_iva_cotizacion_orden_servicio_add)

def orden_servicio_suministros_proveedor(request, proveedor_id, proyecto_id):
    return orden_servicio_suministros_proveedor2(request, proveedor_id, proyecto_id)
dajaxice_functions.register(orden_servicio_suministros_proveedor)

def realizar_cotizacion_orden_servicio(request, proyecto_id):
    return realizar_cotizacion_orden_servicio_add2(request, proyecto_id)
dajaxice_functions.register(realizar_cotizacion_orden_servicio)

def cancelar_cotizacion_orden_servicio(request, proyecto_id):
    return cancelar_cotizacion_orden_servicio_add2(request, proyecto_id)
dajaxice_functions.register(cancelar_cotizacion_orden_servicio)

def activar_input_cantidad_suministro_orden_servicio_change(request, pagina, suministro_id, orden_servicio_id, proyecto_id):
    return activar_input_cantidad_suministro_orden_servicio_change2(request, pagina, suministro_id, orden_servicio_id, proyecto_id)
dajaxice_functions.register(activar_input_cantidad_suministro_orden_servicio_change)

def modificar_cantidad_suministro_orden_servicio_change(request, suministro_id, cantidad, orden_servicio_id, pagina, proyecto_id):
    return modificar_cantidad_suministro_orden_servicio_change2(request, suministro_id, cantidad, orden_servicio_id, pagina, proyecto_id)
dajaxice_functions.register(modificar_cantidad_suministro_orden_servicio_change)

def activar_input_precio_suministro_orden_servicio_change(request, pagina, suministro_id, orden_servicio_id, proyecto_id):
    return activar_input_precio_suministro_orden_servicio_change2(request, pagina, suministro_id, orden_servicio_id, proyecto_id)
dajaxice_functions.register(activar_input_precio_suministro_orden_servicio_change)

def modificar_precio_suministro_orden_servicio_change(request, suministro_id, precio, orden_servicio_id, pagina, proyecto_id):
    return modificar_precio_suministro_orden_servicio_change2(request, suministro_id, precio, orden_servicio_id, pagina, proyecto_id)
dajaxice_functions.register(modificar_precio_suministro_orden_servicio_change)

def activar_input_observaciones_suministro_orden_servicio_change(request, pagina, suministro_id, orden_servicio_id, proyecto_id):
    return activar_input_observaciones_suministro_orden_servicio_change2(request, pagina, suministro_id, orden_servicio_id, proyecto_id)
dajaxice_functions.register(activar_input_observaciones_suministro_orden_servicio_change)

def modificar_observaciones_suministro_orden_servicio_change(request, suministro_id, observaciones, orden_servicio_id, pagina, proyecto_id):
    return modificar_observaciones_suministro_orden_servicio_change2(request, suministro_id, observaciones, orden_servicio_id, pagina, proyecto_id)
dajaxice_functions.register(modificar_observaciones_suministro_orden_servicio_change)

def suministros_proveedor_orden_servicio_change(request, orden_servicio_id, criterio=None, proyecto_id=None):
    return suministros_proveedor_orden_servicio_change2(request, orden_servicio_id, criterio, proyecto_id)
dajaxice_functions.register(suministros_proveedor_orden_servicio_change)

def anadir_suministro_orden_servicio_change(request, pagina, suministro_id, cantidad, precio, observaciones, orden_servicio_id, criterio, proyecto_id):
    return anadir_suministro_orden_servicio_change2(request, pagina, suministro_id, cantidad, precio, observaciones, orden_servicio_id, criterio, proyecto_id)
dajaxice_functions.register(anadir_suministro_orden_servicio_change)

def activar_input_suministro_agregar_orden_servicio_change(request, pagina, suministro_id, orden_servicio_id, criterio, proyecto_id):
    return activar_input_suministro_agregar_orden_servicio_change2(request, pagina, suministro_id, orden_servicio_id, criterio, proyecto_id)
dajaxice_functions.register(activar_input_suministro_agregar_orden_servicio_change)

def anadir_suministros_orden_servicio_change(request, orden_servicio_id, proyecto_id):
    return anadir_suministros_orden_servicio_change2(request, orden_servicio_id, proyecto_id)
dajaxice_functions.register(anadir_suministros_orden_servicio_change)

def cancelar_anadir_suministros_orden_servicio_change(request, proyecto_id):
    return cancelar_anadir_suministros_orden_servicio_change2(request, proyecto_id)
dajaxice_functions.register(cancelar_anadir_suministros_orden_servicio_change)

def eliminar_suministro_orden_servicio(request, suministro_id, orden_servicio_id, proyecto_id):
    return eliminar_suministro_orden_servicio2(request, suministro_id, orden_servicio_id, proyecto_id)
dajaxice_functions.register(eliminar_suministro_orden_servicio)

def asignar_modificacion_orden_servicio(request, permiso, orden_servicio_id, proyecto_id):
    return asignar_modificacion_orden_servicio2(request, permiso, orden_servicio_id, proyecto_id)
dajaxice_functions.register(asignar_modificacion_orden_servicio)

def realizar_orden_servicio(request, cotizacion_id, fecha_arribo, forma_pago, parametro_pago, amortizacion, retencion_garantia, rete_ica, rete_fuente, observaciones, a_i_u, utilidad, iva, proyecto_id):
    return realizar_orden_servicio2(request, cotizacion_id, fecha_arribo, forma_pago, parametro_pago, amortizacion, retencion_garantia, rete_ica, rete_fuente, observaciones, a_i_u, utilidad, iva, proyecto_id)
dajaxice_functions.register(realizar_orden_servicio)

def agregar_suministro_corte_diario_obra_add(request, pagina, suministro_id, orden_servicio_id, criterio, proyecto_id, cantidad):
    return agregar_suministro_corte_diario_obra_add2(request, pagina, suministro_id, orden_servicio_id, criterio, proyecto_id, cantidad)
dajaxice_functions.register(agregar_suministro_corte_diario_obra_add)

def activar_modificar_suministro_corte_diario_obra_add(request, pagina, suministro_id, orden_servicio_id, criterio, proyecto_id):
    return activar_modificar_suministro_corte_diario_obra_add2(request, pagina, suministro_id, orden_servicio_id, criterio, proyecto_id)
dajaxice_functions.register(activar_modificar_suministro_corte_diario_obra_add)

#Acta de recibo de obra
def detalles_cantidad_suministro_acta_recibo_obra_add(request, suministro_id, fecha_especifica, orden_servicio_id, fecha_inicio, fecha_fin, proyecto_id):
    return detalles_cantidad_suministro_acta_recibo_obra_add2(request, suministro_id, fecha_especifica, orden_servicio_id, fecha_inicio, fecha_fin, proyecto_id)
dajaxice_functions.register(detalles_cantidad_suministro_acta_recibo_obra_add)

def activar_input_cantidad_suministro_acta_recibo_obra_add(request, corte_diario_obra_id, suministro_id, fecha_especifica, orden_servicio_id, fecha_inicio, fecha_fin, proyecto_id):
    return activar_input_cantidad_suministro_acta_recibo_obra_add2(request, corte_diario_obra_id, suministro_id, fecha_especifica, orden_servicio_id, fecha_inicio, fecha_fin, proyecto_id)
dajaxice_functions.register(activar_input_cantidad_suministro_acta_recibo_obra_add)

def modificar_cantidad_suministro_acta_recibo_obra_add(request, corte_diario_obra_id, suministro_id, cantidad, fecha_especifica, orden_servicio_id, fecha_inicio, fecha_fin, proyecto_id):
    return modificar_cantidad_suministro_acta_recibo_obra_add2(request, corte_diario_obra_id, suministro_id, cantidad, fecha_especifica, orden_servicio_id, fecha_inicio, fecha_fin, proyecto_id)
dajaxice_functions.register(modificar_cantidad_suministro_acta_recibo_obra_add)

def registrar_cantidad_suministro_acta_recibo_obra_add(request, orden_servicio_id, fecha_inicio, fecha_fin, proyecto_id):
    return registrar_cantidad_suministro_acta_recibo_obra_add2(request, orden_servicio_id, fecha_inicio, fecha_fin, proyecto_id)
dajaxice_functions.register(registrar_cantidad_suministro_acta_recibo_obra_add)

def asignar_valor_cooperativa_acta_recibo_obra(request, acta_recibo_obra_id, valor_cooperativa, proyecto_id):
    return asignar_valor_cooperativa_acta_recibo_obra2(request, acta_recibo_obra_id, valor_cooperativa, proyecto_id)
dajaxice_functions.register(asignar_valor_cooperativa_acta_recibo_obra)

def cerrar_acta_recibo_obra(request, acta_recibo_obra_id, valor_cooperativa, proyecto_id):
    return cerrar_acta_recibo_obra2(request, acta_recibo_obra_id, valor_cooperativa, proyecto_id)
dajaxice_functions.register(cerrar_acta_recibo_obra)

def detalles_cantidad_suministro_modificar_acta_recibo_obra(request, suministro_id, fecha_especifica, acta_recibo_obra_id, proyecto_id):
    return detalles_cantidad_suministro_modificar_acta_recibo_obra2(request, suministro_id, fecha_especifica, acta_recibo_obra_id, proyecto_id)
dajaxice_functions.register(detalles_cantidad_suministro_modificar_acta_recibo_obra)

def activar_input_modificar_cantidad_suministro_modificar_acta_recibo_obra(request, registro_id, acta_recibo_obra_id, proyecto_id):
    return activar_input_modificar_cantidad_suministro_modificar_acta_recibo_obra2(request, registro_id, acta_recibo_obra_id, proyecto_id)
dajaxice_functions.register(activar_input_modificar_cantidad_suministro_modificar_acta_recibo_obra)

def modificar_cantidad_suministro_modificar_acta_recibo_obra(request, registro_id, cantidad, acta_recibo_obra_id, proyecto_id):
    return modificar_cantidad_suministro_modificar_acta_recibo_obra2(request, registro_id, cantidad, acta_recibo_obra_id, proyecto_id)
dajaxice_functions.register(modificar_cantidad_suministro_modificar_acta_recibo_obra)

def registrar_cantidad_suministro_modificar_acta_recibo_obra(request, acta_recibo_obra_id, proyecto_id):
    return registrar_cantidad_suministro_modificar_acta_recibo_obra2(request, acta_recibo_obra_id, proyecto_id)
dajaxice_functions.register(registrar_cantidad_suministro_modificar_acta_recibo_obra)

def cancelar_registrar_cantidad_suministro_modificar_acta_recibo_obra(request, acta_recibo_obra_id, proyecto_id):
    return cancelar_registrar_cantidad_suministro_modificar_acta_recibo_obra2(request, acta_recibo_obra_id, proyecto_id)
dajaxice_functions.register(cancelar_registrar_cantidad_suministro_modificar_acta_recibo_obra)

def asignar_numero_factura_acta_recibo_obra(request, acta_recibo_obra_id, numero_factura, proyecto_id):
    return asignar_numero_factura_acta_recibo_obra2(request, acta_recibo_obra_id, numero_factura, proyecto_id)
dajaxice_functions.register(asignar_numero_factura_acta_recibo_obra)

def cerrar_numero_factura_acta_recibo_obra(request, acta_recibo_obra_id, numero_factura, proyecto_id):
    return cerrar_numero_factura_acta_recibo_obra2(request, acta_recibo_obra_id, numero_factura, proyecto_id)
dajaxice_functions.register(cerrar_numero_factura_acta_recibo_obra)

#Ordenes de giro
def anadir_suministro_orden_giro(request, pagina, suministro_id, cantidad, observaciones, criterio, proyecto_id):
    return anadir_suministro_orden_giro2(request, pagina, suministro_id, cantidad, observaciones, criterio, proyecto_id)
dajaxice_functions.register(anadir_suministro_orden_giro)

def activar_modificar_suministro_orden_giro_add(request, pagina, suministro_id, criterio, proyecto_id):
    return activar_modificar_suministro_orden_giro_add2(request, pagina, suministro_id, criterio, proyecto_id)
dajaxice_functions.register(activar_modificar_suministro_orden_giro_add)

def seleccionar_proveedor_orden_giro_proyecto_add(request, proveedor_id, proyecto_id):
    return seleccionar_proveedor_orden_giro_proyecto_add2(request, proveedor_id, proyecto_id)
dajaxice_functions.register(seleccionar_proveedor_orden_giro_proyecto_add)

def agregar_item_acta_conformidad_add(request, pagina, item_id, orden_giro_id, criterio, proyecto_id, valor):
    return agregar_item_acta_conformidad_add2(request, pagina, item_id, orden_giro_id, criterio, proyecto_id, valor)
dajaxice_functions.register(agregar_item_acta_conformidad_add)

def activar_modificar_item_acta_conformidad_add(request, pagina, item_id, orden_giro_id, criterio, proyecto_id):
    return activar_modificar_item_acta_conformidad_add2(request, pagina, item_id, orden_giro_id, criterio, proyecto_id)
dajaxice_functions.register(activar_modificar_item_acta_conformidad_add)

def ventana_agregar_suministro_factura_orden_compra(request, pagina, informe_recepcion_id, criterio, proyecto_id):
    return ventana_agregar_suministro_factura_orden_compra2(request, pagina, informe_recepcion_id, criterio, proyecto_id)
dajaxice_functions.register(ventana_agregar_suministro_factura_orden_compra)

def agregar_item_factura_orden_compra(request, pagina, suministro_id, informe_recepcion_id, cantidad, criterio, proyecto_id):
    return agregar_item_factura_orden_compra2(request, pagina, suministro_id, informe_recepcion_id, cantidad, criterio, proyecto_id)
dajaxice_functions.register(agregar_item_factura_orden_compra)

def activar_input_cantidad_item_factura_orden_compra(request, pagina, suministro_id, informe_recepcion_id, criterio, proyecto_id):
    return activar_input_cantidad_item_factura_orden_compra2(request, pagina, suministro_id, informe_recepcion_id, criterio, proyecto_id)
dajaxice_functions.register(activar_input_cantidad_item_factura_orden_compra)

def agregar_items_factura_orden_compra(request, informe_recepcion_id, proyecto_id):
    return agregar_items_factura_orden_compra2(request, informe_recepcion_id, proyecto_id)
dajaxice_functions.register(agregar_items_factura_orden_compra)

def cancelar_agregar_items_factura_orden_compra(request, proyecto_id):
    return cancelar_agregar_items_factura_orden_compra2(request, proyecto_id)
dajaxice_functions.register(cancelar_agregar_items_factura_orden_compra)

def eliminar_item_factura_orden_compra_add(request, suministro_id, informe_recepcion_id, pagina, proveedor_id, proyecto_id):
    return eliminar_item_factura_orden_compra_add2(request, suministro_id, informe_recepcion_id, pagina, proveedor_id, proyecto_id)
dajaxice_functions.register(eliminar_item_factura_orden_compra_add)

def activar_input_cantidad_item_factura_orden_compra_add(request, pagina, suministro_id, informe_recepcion_id, proveedor_id, proyecto_id):
    return activar_input_cantidad_item_factura_orden_compra_add2(request, pagina, suministro_id, informe_recepcion_id, proveedor_id, proyecto_id)
dajaxice_functions.register(activar_input_cantidad_item_factura_orden_compra_add)

def modificar_cantidad_item_factura_orden_compra_add(request, suministro_id, informe_recepcion_id, cantidad, pagina, proveedor_id, proyecto_id):
    return modificar_cantidad_item_factura_orden_compra_add2(request, suministro_id, informe_recepcion_id, cantidad, pagina, proveedor_id, proyecto_id)
dajaxice_functions.register(modificar_cantidad_item_factura_orden_compra_add)

def facturar_todos_suministros_informe_recepcion_factura_orden_compra_add(request, informe_recepcion_id, proyecto_id):
    return facturar_todos_suministros_informe_recepcion_factura_orden_compra_add2(request, informe_recepcion_id, proyecto_id)
dajaxice_functions.register(facturar_todos_suministros_informe_recepcion_factura_orden_compra_add)

def asignar_descuento_acta_recibo_obra(request, orden_servicio_id, proyecto_id, descuento=None):
    return asignar_descuento_acta_recibo_obra2(request, orden_servicio_id, proyecto_id, descuento)
dajaxice_functions.register(asignar_descuento_acta_recibo_obra)


#---------------------------------------------------------------------------------------------------

#### #### MODULO VENTAS #### ####

def agregar_pregunta_nueva_encuesta(request, datos):
    return agregar_pregunta_nueva_encuesta2(request, datos)
dajaxice_functions.register(agregar_pregunta_nueva_encuesta)

def eliminar_pregunta_nueva_encuesta(request, indice):
    return eliminar_pregunta_nueva_encuesta2(request, indice)
dajaxice_functions.register(eliminar_pregunta_nueva_encuesta)

def validar_identificacion_nuevo_cliente(request, identificacion, proyecto_id):
    return validar_identificacion_nuevo_cliente2(request, identificacion, proyecto_id)
dajaxice_functions.register(validar_identificacion_nuevo_cliente)

def ventana_contacto_cliente(request, proyecto_id):
    return ventana_contacto_cliente2(request, proyecto_id)
dajaxice_functions.register(ventana_contacto_cliente)

def agregar_contacto_cliente(request, datos):
    return agregar_contacto_cliente2(request, datos)
dajaxice_functions.register(agregar_contacto_cliente)

def ventana_modificar_contacto_cliente(request, indice):
    return ventana_modificar_contacto_cliente2(request, indice)
dajaxice_functions.register(ventana_modificar_contacto_cliente)

def modificar_contacto_cliente(request, datos):
    return modificar_contacto_cliente2(request, datos)
dajaxice_functions.register(modificar_contacto_cliente)

def eliminar_contacto_cliente(request, indice):
    return eliminar_contacto_cliente2(request, indice)
dajaxice_functions.register(eliminar_contacto_cliente)

def asignar_modificacion_inmueble_proyecto(request, permiso, inmueble_id, pagina, tipo_inmueble_id, seccion_proyecto_id, criterio, proyecto_id):
    return asignar_modificacion_inmueble_proyecto2(request, permiso, inmueble_id, pagina, tipo_inmueble_id, seccion_proyecto_id, criterio, proyecto_id)
dajaxice_functions.register(asignar_modificacion_inmueble_proyecto)

def busqueda_inmuebles_nuevo_prospecto_venta(request, proyecto_id, datos=None):
    return busqueda_inmuebles_nuevo_prospecto_venta2(request, proyecto_id, datos)
dajaxice_functions.register(busqueda_inmuebles_nuevo_prospecto_venta)

def seleccionar_agrupacion_inmuebles_nuevo_prospecto_venta(request, agrupacion_inmueble_id, parametro, criterio, pagina, proyecto_id):
    return seleccionar_agrupacion_inmuebles_nuevo_prospecto_venta2(request, agrupacion_inmueble_id, parametro, criterio, pagina, proyecto_id)
dajaxice_functions.register(seleccionar_agrupacion_inmuebles_nuevo_prospecto_venta)

def agregar_agrupaciones_inmuebles_nuevo_prospecto_venta(request, proyecto_id):
    return agregar_agrupaciones_inmuebles_nuevo_prospecto_venta2(request, proyecto_id)
dajaxice_functions.register(agregar_agrupaciones_inmuebles_nuevo_prospecto_venta)

def eliminar_agrupacion_inmuebles_nuevo_prospecto_venta(request, agrupacion_inmuebles_id, proyecto_id):
    return eliminar_agrupacion_inmuebles_nuevo_prospecto_venta2(request, agrupacion_inmuebles_id, proyecto_id)
dajaxice_functions.register(eliminar_agrupacion_inmuebles_nuevo_prospecto_venta)

def nueva_notificacion_nuevo_prospecto_venta(request, proyecto_id, datos=None):
    return nueva_notificacion_nuevo_prospecto_venta2(request, proyecto_id, datos)
dajaxice_functions.register(nueva_notificacion_nuevo_prospecto_venta)

def eliminar_notificacion_nuevo_prospecto_venta(request, indice, proyecto_id):
    return eliminar_notificacion_nuevo_prospecto_venta2(request, indice, proyecto_id)
dajaxice_functions.register(eliminar_notificacion_nuevo_prospecto_venta)

def modificar_notificacion_nuevo_prospecto_venta(request, proyecto_id, datos=None, indice=None):
    return modificar_notificacion_nuevo_prospecto_venta2(request, proyecto_id, datos, indice)
dajaxice_functions.register(modificar_notificacion_nuevo_prospecto_venta)

def busqueda_inmuebles_detalles_prospecto_venta(request, prospecto_venta_id, proyecto_id, datos=None):
    return busqueda_inmuebles_detalles_prospecto_venta2(request, prospecto_venta_id, proyecto_id, datos)
dajaxice_functions.register(busqueda_inmuebles_detalles_prospecto_venta)

def seleccionar_agrupacion_inmuebles_detalles_prospecto_venta(request, prospecto_venta_id, agrupacion_inmueble_id, parametro, criterio, pagina, proyecto_id):
    return seleccionar_agrupacion_inmuebles_detalles_prospecto_venta2(request, prospecto_venta_id, agrupacion_inmueble_id, parametro, criterio, pagina, proyecto_id)
dajaxice_functions.register(seleccionar_agrupacion_inmuebles_detalles_prospecto_venta)

def agregar_agrupaciones_inmuebles_detalles_prospecto_venta(request, prospecto_venta_id, proyecto_id):
    return agregar_agrupaciones_inmuebles_detalles_prospecto_venta2(request, prospecto_venta_id, proyecto_id)
dajaxice_functions.register(agregar_agrupaciones_inmuebles_detalles_prospecto_venta)

def nueva_notificacion_detalles_prospecto_venta(request, prospecto_venta_id, proyecto_id, datos=None):
    return nueva_notificacion_detalles_prospecto_venta2(request, prospecto_venta_id, proyecto_id, datos)
dajaxice_functions.register(nueva_notificacion_detalles_prospecto_venta)

def contestar_notificacion_prospecto_venta(request, proyecto_id, datos=None, notificacion_id=None):
    return contestar_notificacion_prospecto_venta2(request, proyecto_id, datos, notificacion_id)
dajaxice_functions.register(contestar_notificacion_prospecto_venta)

def agregar_convenio_prospecto_venta(request, prospecto_venta_id, proyecto_id, datos=None):
    return agregar_convenio_prospecto_venta2(request, prospecto_venta_id, proyecto_id, datos)
dajaxice_functions.register(agregar_convenio_prospecto_venta)

def busqueda_agrupaciones_inmueble_agregar_convenio_prospecto_venta(request, prospecto_venta_id, proyecto_id, datos=None):
    return busqueda_agrupaciones_inmueble_agregar_convenio_prospecto_venta2(request, prospecto_venta_id, proyecto_id, datos)
dajaxice_functions.register(busqueda_agrupaciones_inmueble_agregar_convenio_prospecto_venta)

def validar_identificacion_inmueble(request, identificacion, identificacion_actual=None, proyecto_id=None):
    return validar_identificacion_inmueble2(request, identificacion, identificacion_actual, proyecto_id)
dajaxice_functions.register(validar_identificacion_inmueble)

def activar_input_precio_asignacion_individual_precios(request, inmueble_id, tipo_inmueble_id, seccion_proyecto_id, criterio, proyecto_id):
    return activar_input_precio_asignacion_individual_precios2(request, inmueble_id, tipo_inmueble_id, seccion_proyecto_id, criterio, proyecto_id)
dajaxice_functions.register(activar_input_precio_asignacion_individual_precios)

def asignar_precio_asignacion_individual_precios(request, inmueble_id, precio, lista_precios, tipo_inmueble_id, seccion_proyecto_id, criterio, proyecto_id):
    return asignar_precio_asignacion_individual_precios2(request, inmueble_id, precio, lista_precios, tipo_inmueble_id, seccion_proyecto_id, criterio, proyecto_id)
dajaxice_functions.register(asignar_precio_asignacion_individual_precios)

def busqueda_inmuebles_modificacion_masiva(request, inmueble_id, seccion_proyecto_id, criterio, proyecto_id):
    return busqueda_inmuebles_modificacion_masiva2(request, inmueble_id, seccion_proyecto_id, criterio, proyecto_id)
dajaxice_functions.register(busqueda_inmuebles_modificacion_masiva)

def busqueda_inmuebles_agrupacion_inmueble_add(request, datos):
    return busqueda_inmuebles_agrupacion_inmueble_add2(request, datos)
dajaxice_functions.register(busqueda_inmuebles_agrupacion_inmueble_add)

def agregar_inmueble_agrupacion_inmueble_add(request, inmueble_id, proyecto_id):
    return agregar_inmueble_agrupacion_inmueble_add2(request, inmueble_id, proyecto_id)
dajaxice_functions.register(agregar_inmueble_agrupacion_inmueble_add)

def eliminar_inmueble_agrupacion_inmueble_add(request, inmueble_id, proyecto_id):
    return eliminar_inmueble_agrupacion_inmueble_add2(request, inmueble_id, proyecto_id)
dajaxice_functions.register(eliminar_inmueble_agrupacion_inmueble_add)

def busqueda_clientes_nuevo_contrato_venta(request, prospecto_venta_id, proyecto_id, datos=None):
    return busqueda_clientes_nuevo_contrato_venta2(request, prospecto_venta_id, proyecto_id, datos)
dajaxice_functions.register(busqueda_clientes_nuevo_contrato_venta)

def seleccionar_cliente_nuevo_contrato_venta(request, cliente_id, parametro, criterio, pagina, prospecto_venta_id, proyecto_id):
    return seleccionar_cliente_nuevo_contrato_venta2(request, cliente_id, parametro, criterio, pagina, prospecto_venta_id, proyecto_id)
dajaxice_functions.register(seleccionar_cliente_nuevo_contrato_venta)

def agregar_clientes_nuevo_contrato_venta(request, prospecto_venta_id, proyecto_id):
    return agregar_clientes_nuevo_contrato_venta2(request, prospecto_venta_id, proyecto_id)
dajaxice_functions.register(agregar_clientes_nuevo_contrato_venta)

def eliminar_cliente_nuevo_contrato_venta(request, cliente_id, prospecto_venta_id, proyecto_id):
    return eliminar_cliente_nuevo_contrato_venta2(request, cliente_id, prospecto_venta_id, proyecto_id)
dajaxice_functions.register(eliminar_cliente_nuevo_contrato_venta)

def busqueda_adicionales_agrupacion_nuevo_contrato_venta(request, prospecto_venta_id, proyecto_id, datos=None):
    return busqueda_adicionales_agrupacion_nuevo_contrato_venta2(request, prospecto_venta_id, proyecto_id, datos)
dajaxice_functions.register(busqueda_adicionales_agrupacion_nuevo_contrato_venta)

def seleccionar_adicional_agrupacion_inmueble_nuevo_contrato_venta(request, adicional_agrupacion_inmueble_id, parametro, pagina, tipo_adicional_id=None, criterio='', prospecto_venta_id=None, proyecto_id=None):
    return seleccionar_adicional_agrupacion_inmueble_nuevo_contrato_venta2(request, adicional_agrupacion_inmueble_id, parametro, pagina, tipo_adicional_id, criterio, prospecto_venta_id, proyecto_id)
dajaxice_functions.register(seleccionar_adicional_agrupacion_inmueble_nuevo_contrato_venta)

def agregar_adicionales_agrupacion_inmueble_nuevo_contrato_venta(request, agrupacion_inmueble_id, prospecto_venta_id, proyecto_id):
    return agregar_adicionales_agrupacion_inmueble_nuevo_contrato_venta2(request, agrupacion_inmueble_id, prospecto_venta_id, proyecto_id)
dajaxice_functions.register(agregar_adicionales_agrupacion_inmueble_nuevo_contrato_venta)

def eliminar_adicional_agrupacion_inmueble_nuevo_contrato_venta(request, adicional_agrupacion_inmueble_id, agrupacion_inmueble_id, prospecto_venta_id, proyecto_id):
    return eliminar_adicional_agrupacion_inmueble_nuevo_contrato_venta2(request, adicional_agrupacion_inmueble_id, agrupacion_inmueble_id, prospecto_venta_id, proyecto_id)
dajaxice_functions.register(eliminar_adicional_agrupacion_inmueble_nuevo_contrato_venta)

def seleccionar_forma_pago_nuevo_contrato_venta(request, forma_pago, prospecto_venta_id, proyecto_id):
    return seleccionar_forma_pago_nuevo_contrato_venta2(request, forma_pago, prospecto_venta_id, proyecto_id)
dajaxice_functions.register(seleccionar_forma_pago_nuevo_contrato_venta)

def agregar_pago_entidad_nuevo_contrato_venta(request, agrupacion_inmueble_id, datos=None, proyecto_id=None):
    return agregar_pago_entidad_nuevo_contrato_venta2(request, agrupacion_inmueble_id, datos, proyecto_id)
dajaxice_functions.register(agregar_pago_entidad_nuevo_contrato_venta)

def eliminar_pago_entidad_nuevo_contrato_venta(request, agrupacion_inmueble_id, indice, proyecto_id=None):
    return eliminar_pago_entidad_nuevo_contrato_venta2(request, agrupacion_inmueble_id, indice, proyecto_id)
dajaxice_functions.register(eliminar_pago_entidad_nuevo_contrato_venta)

def modificar_pago_entidad_nuevo_contrato_venta(request, agrupacion_inmueble_id, datos=None, indice=None, proyecto_id=None):
    return modificar_pago_entidad_nuevo_contrato_venta2(request, agrupacion_inmueble_id, datos, indice, proyecto_id)
dajaxice_functions.register(modificar_pago_entidad_nuevo_contrato_venta)

def asignar_monto_credito_nuevo_contrato_venta(request, agrupacion_inmueble_id, monto_credito, proyecto_id):
    return asignar_monto_credito_nuevo_contrato_venta2(request, agrupacion_inmueble_id, monto_credito, proyecto_id)
dajaxice_functions.register(asignar_monto_credito_nuevo_contrato_venta)

def activar_asignar_monto_credito_nuevo_contrato_venta(request):
    return activar_asignar_monto_credito_nuevo_contrato_venta2(request)
dajaxice_functions.register(activar_asignar_monto_credito_nuevo_contrato_venta)

def seleccionar_numero_cuotas_efectivo_nuevo_contrato_venta(request, agrupacion_inmueble_id, numero_cuotas, prospecto_venta_id, proyecto_id):
    return seleccionar_numero_cuotas_efectivo_nuevo_contrato_venta2(request, agrupacion_inmueble_id, numero_cuotas, prospecto_venta_id, proyecto_id)
dajaxice_functions.register(seleccionar_numero_cuotas_efectivo_nuevo_contrato_venta)

def agregar_pago_efectivo_nuevo_contrato_venta(request, agrupacion_inmueble_id=None, datos=None, proyecto_id=None):
    return agregar_pago_efectivo_nuevo_contrato_venta2(request, agrupacion_inmueble_id, datos, proyecto_id)
dajaxice_functions.register(agregar_pago_efectivo_nuevo_contrato_venta)

def modificar_pago_efectivo_nuevo_contrato_venta(request, agrupacion_inmueble_id, datos=None, indice=None, proyecto_id=None):
    return modificar_pago_efectivo_nuevo_contrato_venta2(request, agrupacion_inmueble_id, datos, indice, proyecto_id)
dajaxice_functions.register(modificar_pago_efectivo_nuevo_contrato_venta)

def eliminar_pago_efectivo_nuevo_contrato_venta(request, agrupacion_inmueble_id, indice, proyecto_id):
    return eliminar_pago_efectivo_nuevo_contrato_venta2(request, agrupacion_inmueble_id, indice, proyecto_id)
dajaxice_functions.register(eliminar_pago_efectivo_nuevo_contrato_venta)

def busqueda_adicionales_agrupacion_modificar_contrato_venta(request, contrato_venta_id, proyecto_id, datos=None):
    return busqueda_adicionales_agrupacion_modificar_contrato_venta2(request, contrato_venta_id, proyecto_id, datos)
dajaxice_functions.register(busqueda_adicionales_agrupacion_modificar_contrato_venta)

def busqueda_clientes_modificar_contrato_venta(request, contrato_venta_id, proyecto_id, datos=None):
    return busqueda_clientes_modificar_contrato_venta2(request, contrato_venta_id, proyecto_id, datos)
dajaxice_functions.register(busqueda_clientes_modificar_contrato_venta)

def seleccionar_cliente_modificar_contrato_venta(request, cliente_id, parametro, criterio, pagina, contrato_venta_id, proyecto_id):
    return seleccionar_cliente_modificar_contrato_venta2(request, cliente_id, parametro, criterio, pagina, contrato_venta_id, proyecto_id)
dajaxice_functions.register(seleccionar_cliente_modificar_contrato_venta)

def agregar_clientes_modificar_contrato_venta(request, contrato_venta_id, proyecto_id):
    return agregar_clientes_modificar_contrato_venta2(request, contrato_venta_id, proyecto_id)
dajaxice_functions.register(agregar_clientes_modificar_contrato_venta)

def eliminar_cliente_modificar_contrato_venta(request, cliente_id, contrato_venta_id, proyecto_id):
    return eliminar_cliente_modificar_contrato_venta2(request, cliente_id, contrato_venta_id, proyecto_id)
dajaxice_functions.register(eliminar_cliente_modificar_contrato_venta)

def seleccionar_forma_pago_modificar_contrato_venta(request, forma_pago, contrato_venta_id, proyecto_id):
    return seleccionar_forma_pago_modificar_contrato_venta2(request, forma_pago, contrato_venta_id, proyecto_id)
dajaxice_functions.register(seleccionar_forma_pago_modificar_contrato_venta)

def asignar_monto_credito_modificar_contrato_venta(request, contrato_venta_id, monto_credito, proyecto_id):
    return asignar_monto_credito_modificar_contrato_venta2(request, contrato_venta_id, monto_credito, proyecto_id)
dajaxice_functions.register(asignar_monto_credito_modificar_contrato_venta)

def seleccionar_adicional_agrupacion_inmueble_modificar_contrato_venta(request, adicional_agrupacion_inmueble_id, parametro, pagina, tipo_adicional_id=None, criterio='', contrato_venta_id=None, proyecto_id=None):
    return seleccionar_adicional_agrupacion_inmueble_modificar_contrato_venta2(request, adicional_agrupacion_inmueble_id, parametro, pagina, tipo_adicional_id, criterio, contrato_venta_id, proyecto_id)
dajaxice_functions.register(seleccionar_adicional_agrupacion_inmueble_modificar_contrato_venta)

def agregar_adicionales_agrupacion_inmueble_modificar_contrato_venta(request, contrato_venta_id, proyecto_id):
    return agregar_adicionales_agrupacion_inmueble_modificar_contrato_venta2(request, contrato_venta_id, proyecto_id)
dajaxice_functions.register(agregar_adicionales_agrupacion_inmueble_modificar_contrato_venta)

def eliminar_adicional_agrupacion_inmueble_modificar_contrato_venta(request, indice, contrato_venta_id, proyecto_id):
    return eliminar_adicional_agrupacion_inmueble_modificar_contrato_venta2(request, indice, contrato_venta_id, proyecto_id)
dajaxice_functions.register(eliminar_adicional_agrupacion_inmueble_modificar_contrato_venta)

def agregar_pago_entidad_modificar_contrato_venta(request, contrato_venta_id, datos=None, proyecto_id=None):
    return agregar_pago_entidad_modificar_contrato_venta2(request, contrato_venta_id, datos, proyecto_id)
dajaxice_functions.register(agregar_pago_entidad_modificar_contrato_venta)

def eliminar_pago_entidad_modificar_contrato_venta(request, contrato_venta_id, indice, proyecto_id=None):
    return eliminar_pago_entidad_modificar_contrato_venta2(request, contrato_venta_id, indice, proyecto_id)
dajaxice_functions.register(eliminar_pago_entidad_modificar_contrato_venta)

def modificar_pago_entidad_modificar_contrato_venta(request, contrato_venta_id, datos=None, indice=None, proyecto_id=None):
    return modificar_pago_entidad_modificar_contrato_venta2(request, contrato_venta_id, datos, indice, proyecto_id)
dajaxice_functions.register(modificar_pago_entidad_modificar_contrato_venta)

def seleccionar_numero_cuotas_efectivo_modificar_contrato_venta(request, numero_cuotas, contrato_venta_id, proyecto_id):
    return seleccionar_numero_cuotas_efectivo_modificar_contrato_venta2(request, numero_cuotas, contrato_venta_id, proyecto_id)
dajaxice_functions.register(seleccionar_numero_cuotas_efectivo_modificar_contrato_venta)

def agregar_pago_efectivo_modificar_contrato_venta(request, contrato_venta_id=None, datos=None, proyecto_id=None):
    return agregar_pago_efectivo_modificar_contrato_venta2(request, contrato_venta_id, datos, proyecto_id)
dajaxice_functions.register(agregar_pago_efectivo_modificar_contrato_venta)

def eliminar_pago_efectivo_modificar_contrato_venta(request, contrato_venta_id, indice, proyecto_id):
    return eliminar_pago_efectivo_modificar_contrato_venta2(request, contrato_venta_id, indice, proyecto_id)
dajaxice_functions.register(eliminar_pago_efectivo_modificar_contrato_venta)

def modificar_pago_efectivo_modificar_contrato_venta(request, contrato_venta_id, datos=None, indice=None, proyecto_id=None):
    return modificar_pago_efectivo_modificar_contrato_venta2(request, contrato_venta_id, datos, indice, proyecto_id)
dajaxice_functions.register(modificar_pago_efectivo_modificar_contrato_venta)

def registrar_abono_entidad_contrato_venta(request, contrato_venta_id, proyecto_id, pago_entidad_contrato_venta_id=None, datos=None):
    return registrar_abono_entidad_contrato_venta2(request, contrato_venta_id, proyecto_id, pago_entidad_contrato_venta_id, datos)
dajaxice_functions.register(registrar_abono_entidad_contrato_venta)

def eliminar_abono_entidad_contrato_venta(request, pago_entidad_contrato_venta_id, contrato_venta_id, proyecto_id):
    return eliminar_abono_entidad_contrato_venta2(request, pago_entidad_contrato_venta_id, contrato_venta_id, proyecto_id)
dajaxice_functions.register(eliminar_abono_entidad_contrato_venta)

def validar_abono_entidad_contrato_venta(request, pago_entidad_contrato_venta_id, contrato_venta_id, proyecto_id):
    return validar_abono_entidad_contrato_venta2(request, pago_entidad_contrato_venta_id, contrato_venta_id, proyecto_id)
dajaxice_functions.register(validar_abono_entidad_contrato_venta)

def registrar_abono_efectivo_contrato_venta(request, contrato_venta_id, proyecto_id, datos=None):
    return registrar_abono_efectivo_contrato_venta2(request, contrato_venta_id, proyecto_id, datos)
dajaxice_functions.register(registrar_abono_efectivo_contrato_venta)

def eliminar_abono_efectivo_contrato_venta(request, abono_pago_efectivo_contrato_venta_id, contrato_venta_id, proyecto_id):
    return eliminar_abono_efectivo_contrato_venta2(request, abono_pago_efectivo_contrato_venta_id, contrato_venta_id, proyecto_id)
dajaxice_functions.register(eliminar_abono_efectivo_contrato_venta)

def validar_abono_efectivo_contrato_venta(request, abono_pago_efectivo_contrato_venta_id, contrato_venta_id, proyecto_id, datos=None):
    return validar_abono_efectivo_contrato_venta2(request, abono_pago_efectivo_contrato_venta_id, contrato_venta_id, proyecto_id, datos)
dajaxice_functions.register(validar_abono_efectivo_contrato_venta)

def asignar_numero_cuenta_fiducia_contrato_venta(request, contrato_venta_id, proyecto_id, numero_fiducuenta=None):
    return asignar_numero_cuenta_fiducia_contrato_venta2(request, contrato_venta_id, proyecto_id, numero_fiducuenta)
dajaxice_functions.register(asignar_numero_cuenta_fiducia_contrato_venta)

def asignar_fecha_escritura_contrato_venta(request, contrato_venta_id, proyecto_id, fecha_escritura=None):
    return asignar_fecha_escritura_contrato_venta2(request, contrato_venta_id, proyecto_id, fecha_escritura)
dajaxice_functions.register(asignar_fecha_escritura_contrato_venta)

def asignar_referencia_inmueble_contrato_venta(request, contrato_venta_id, proyecto_id, referencia_inmueble=None):
    return asignar_referencia_inmueble_contrato_venta2(request, contrato_venta_id, proyecto_id, referencia_inmueble)
dajaxice_functions.register(asignar_referencia_inmueble_contrato_venta)
#### #### MODULO VENTAS #### ####