from django.conf.urls.defaults import patterns, include, url

from online_status import urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Uncomment the next two lines to enable the dajax
from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Aplicacion.views.home', name='home'),
    # url(r'^Aplicacion/', include('Aplicacion.foo.urls')),

    (r'^inverboy/$', 'aplicacion.inverboy.views_proyecto.views_modulo_usuario.logear'),
    (r'^logout/$', 'aplicacion.inverboy.views_proyecto.views_modulo_usuario.logout_view'),
    (r'^inverboy/home/$', 'aplicacion.inverboy.views_proyecto.views_modulo_usuario.home'),
    (r'^inverboy/home/usuariochange/$', 'aplicacion.inverboy.views_proyecto.views_modulo_usuario.change_usuario'),
    (r'^inverboy/home/usuarioadd/$', 'aplicacion.inverboy.views_proyecto.views_modulo_usuario.usuario_add'),
    (r'^inverboy/home/usuariossearch/$', 'aplicacion.inverboy.views_proyecto.views_modulo_usuario.usuarios_search'),
    (r'^inverboy/home/usuarioschange/(?P<usuario_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_usuario.usuario_change'),
    (r'^inverboy/home/gruposadd/$', 'aplicacion.inverboy.views_proyecto.views_modulo_usuario.grupo_add'),
    (r'^inverboy/home/grupossearch/$', 'aplicacion.inverboy.views_proyecto.views_modulo_usuario.grupos_search'),
    (r'^inverboy/home/gruposdetails/(?P<grupo_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_usuario.grupo_details'),
    (r'^inverboy/home/gruposchange/(?P<grupo_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_usuario.grupo_change'),
    (r'^inverboy/home/proveedoradd/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proveedor.proveedor_add'),
    (r'^inverboy/home/proveedoressearch/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proveedor.proveedores_search'),
    (r'^inverboy/home/proveedoreschange/(?P<proveedor_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proveedor.proveedor_change'),
    (r'^inverboy/home/categoriaadd/$', 'aplicacion.inverboy.views_proyecto.views_modulo_suministros.categoria_add'),
    (r'^inverboy/home/especificacionadd/$', 'aplicacion.inverboy.views_proyecto.views_modulo_suministros.especificacion_add'),
    (r'^inverboy/home/especificacionadd/(?P<categoria_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_suministros.especificacion_add_categoria'),
    (r'^inverboy/home/tipoadd/$', 'aplicacion.inverboy.views_proyecto.views_modulo_suministros.tipo_add'),
    (r'^inverboy/home/tipoadd/(?P<especificacion_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_suministros.tipo_add_especificacion'),
    (r'^inverboy/home/categoriassearch/$', 'aplicacion.inverboy.views_proyecto.views_modulo_suministros.categorias_search'),
    (r'^inverboy/home/categoriaschange/(?P<categoria_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_suministros.categoria_change'),
    (r'^inverboy/home/especificacionessearch/(?P<categoria_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_suministros.especificaciones_search'),
    (r'^inverboy/home/especificacioneschange/(?P<especificacion_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_suministros.especificacion_change'),
    (r'^inverboy/home/tipossearch/(?P<especificacion_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_suministros.tipos_search'),
    (r'^inverboy/home/tiposchange/(?P<tipo_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_suministros.tipo_change'),
    (r'^inverboy/home/suministroadd/(?P<especificacion_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_suministros.suministro_add_especificacion'),
    (r'^inverboy/home/suministroadd/$', 'aplicacion.inverboy.views_proyecto.views_modulo_suministros.suministro_add'),
    ## PARA BUSCAR SUMINISTROS POR ESPECIFICACION(r'^inverboy/home/suministrosview/(?P<especificacion_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_suministros.suministros_view_especificacion'),
    (r'^inverboy/home/suministroschange/(?P<suministro_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_suministros.suministro_change'),
    (r'^inverboy/home/suministrossearch/$', 'aplicacion.inverboy.views_proyecto.views_modulo_suministros.suministros_search'),
    (r'^inverboy/home/capituloadd/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu.capitulo_add'),
    (r'^inverboy/home/capitulossearch/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu.capitulos_search'),
    (r'^inverboy/home/capituloschange/(?P<capitulo_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu.capitulo_change'),
    (r'^inverboy/home/subcapituloadd/(?P<capitulo_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu.subcapitulo_add'),
    (r'^inverboy/home/subcapitulossearch/(?P<capitulo_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu.subcapitulos_search'),
    (r'^inverboy/home/subcapituloschange/(?P<subcapitulo_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu.subcapitulos_change'),
    (r'^inverboy/home/apuadd/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu.apu_add'),
    (r'^inverboy/home/apussearch/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu.apus_search'),
    #(r'^inverboy/home/apussearch/$', 'aplicacion.inverboy.views.apus_search'),
    (r'^inverboy/home/apuschange/(?P<apu_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu.apu_change'),
    (r'^inverboy/home/apusdetails/(?P<apu_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu.apu_details'),

    #(r'^inverboy/home/capituloapuproyectoadd/$', 'aplicacion.inverboy.views.capitulo_apu_proyecto_add'),

    (r'^inverboy/home/proyectoadd/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.proyecto_add'),
    (r'^inverboy/home/proyectosview/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.proyectos_search'),
    (r'^inverboy/home/proyectodetails/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.proyecto_details'),
    (r'^inverboy/home/proyectochange/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.proyecto_change'),

    (r'^inverboy/home/capituloapuproyectoadd/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu_proyecto.capitulo_apu_proyecto_add'),
    (r'^inverboy/home/capitulosapuproyectochange/(?P<proyecto_id>\d+)/(?P<capitulo_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu_proyecto.capitulo_apu_proyecto_change'),
    (r'^inverboy/home/capitulosapuproyectosearch/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu_proyecto.capitulos_apu_proyecto_search'),
    (r'^inverboy/home/subcapituloapuproyectoadd/(?P<proyecto_id>\d+)/(?P<capitulo_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu_proyecto.subcapitulo_apu_proyecto_add'),
    (r'^inverboy/home/subcapitulosapuproyectosearch/(?P<proyecto_id>\d+)/(?P<capitulo_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu_proyecto.subcapitulos_apu_proyecto_search'),
    (r'^inverboy/home/subcapitulosapuproyectochange/(?P<proyecto_id>\d+)/(?P<capitulo_id>\d+)/(?P<subcapitulo_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu_proyecto.subcapitulo_apu_proyecto_change'),

    (r'^inverboy/home/apusmaestrosearch/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu_proyecto.apus_maestro_search'),
    (r'^inverboy/home/apumaestrodetails/(?P<proyecto_id>\d+)/(?P<apu_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu_proyecto.apu_maestro_details'),
    #(r'^inverboy/home/apuproyectoadd/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu_proyecto.apus_proyecto_view'),
    (r'^inverboy/home/apusproyectosearch/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu_proyecto.apus_proyecto_search'),
    (r'^inverboy/home/detallesapuproyecto/(?P<apu_proyecto_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu_proyecto.detalles_apu_proyecto'),
    (r'^inverboy/home/apusproyectochange/(?P<apu_proyecto_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu_proyecto.apu_proyecto_change'),
    # (r'^inverboy/home/apusproyectodetailsrequisicion/(?P<apu_proyecto_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu_proyecto.apu_proyecto_details_requisicion'),
    (r'^inverboy/home/reporteestadoapusproyecto/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_apu_proyecto.reporte_estado_apus_proyecto'),

    (r'^inverboy/home/requisicionproyectoadd/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.requisicion_add'),
    (r'^inverboy/home/apusproyectosearchrequisicionadd/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.apus_proyecto_search_requisicion_add'),
    (r'^inverboy/home/apuproyectodetailsrequisicionadd/(?P<apu_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.apu_proyecto_details_requisicion_add'),
    (r'^inverboy/home/suministrosapuproyectosearchrequisicionadd/(?P<apu_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.buscar_suministros_apu_proyecto_requisicion_add'),
    (r'^inverboy/home/requisicionadddetails/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.nueva_requisicion_details'),
    (r'^inverboy/home/requisicionproyectochange/(?P<requisicion_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.requisicion_proyecto_change'),
    (r'^inverboy/home/requisicionaprobar/(?P<requisicion_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.requisicion_aprobar'),
    (r'^inverboy/home/requisicionesproyectosearch/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.requisiciones_proyecto_search'),
    (r'^inverboy/home/requisicionesproyectodetails/(?P<requisicion_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.requisiciones_proyecto_details'),
    (r'^inverboy/home/requisicionesaprobarproyectosearch/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.requisiciones_aprobar_proyecto_search'),
    #Requisicion de indirectos para orden de giro
    (r'^inverboy/home/requisicionindirectosproyectoadd/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.requisicion_indirectos_add'),
    (r'^inverboy/home/apusproyectosearchrequisicionindirectosadd/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.apus_proyecto_search_requisicion_indirectos_add'),
    (r'^inverboy/home/apuproyectodetailsrequisicionindirectosadd/(?P<apu_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.apu_proyecto_details_requisicion_indirectos_add'),
    (r'^inverboy/home/requisicionindirectosadddetails/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.nueva_requisicion_indirectos_details'),
    (r'^inverboy/home/ordengiroproyectoadd/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.orden_giro_proyecto_add'),
    (r'^inverboy/home/ordenesgiroproyectosearch/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.ordenes_giro_proyecto_search'),
    (r'^inverboy/home/ordenesgiroproyectodetails/(?P<orden_giro_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.ordenes_giro_proyecto_details'),
    (r'^inverboy/home/actaconformidadaddordenesgiro/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.ordenes_giro_acta_conformidad_add'),
    (r'^inverboy/home/actaconformidadadd/(?P<orden_giro_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.acta_conformidad_add'),
    (r'^inverboy/home/actasconformidadproyectosearch/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.actas_conformidad_proyecto_search'),
    (r'^inverboy/home/actasconformidadproyectodetails/(?P<acta_conformidad_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.actas_conformidad_proyecto_details'),

    (r'^inverboy/home/compras/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.compras'),
    (r'^inverboy/home/comprasproveedor/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.compras_proveedor'),
    #(r'^inverboy/home/comprasproveedoressearch/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.compras_proveedores_search'),

    #(r'^inverboy/home/cotizacionesproyectoview/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.cotizaciones_proyecto_search'),
    (r'^inverboy/home/cotizacionesproyectosearch/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.cotizaciones_proyecto_search'),
    (r'^inverboy/home/cotizacionesproyectodetails/(?P<cotizacion_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.cotizaciones_proyecto_details'),

    #(r'^inverboy/home/ordenescompraproyectoview/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.ordenes_compra_proyecto_search'),
    (r'^inverboy/home/ordenescompraproyectosearch/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.ordenes_compra_proyecto_search'),
    (r'^inverboy/home/ordenescompraproyectodetails/(?P<orden_compra_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.ordenes_compra_proyecto_details'),
    (r'^inverboy/home/ordenescompraproyectochange/(?P<orden_compra_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.ordenes_compra_proyecto_change'),
    (r'^inverboy/home/anularordencompraproyecto/(?P<orden_compra_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.anular_orden_compra_proyecto'),

    (r'^inverboy/home/informerecepcionaddordenescompra/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.ordenes_compra_informe_recepcion_add'),
    (r'^inverboy/home/informerecepcionadd/(?P<orden_compra_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.informe_recepcion_add'),
    #(r'^inverboy/home/informesrecepcionproyectoview/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.informes_recepcion_proyecto_search'),
    (r'^inverboy/home/informesrecepcionproyectosearch/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.informes_recepcion_proyecto_search'),

    (r'^inverboy/home/informesrecepcionproyectodetails/(?P<informe_recepcion_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.informes_recepcion_proyecto_details'),

    #(r'^inverboy/home/suministrocomprar/(?P<suministro_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.suministro_comprar'),

    (r'^inverboy/home/suministrosalmacensearch/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.suministros_almacen_search'),

    (r'^inverboy/home/informesalidaadd/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.informe_salida_add'),
    (r'^inverboy/home/informessalidaproyectoview/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.informes_salida_proyecto_search'),
    (r'^inverboy/home/informessalidaproyectodetails/(?P<informe_salida_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.informes_salida_proyecto_details'),

    (r'^inverboy/home/ordenservicioadd/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.orden_servicio_add'),
    (r'^inverboy/home/ordenservicioproveedor/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.orden_servicio_proveedor'),
    (r'^inverboy/home/cotizacionesordenservicioproyectosearch/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.cotizaciones_orden_servicio_proyecto_search'),
    (r'^inverboy/home/ordenesservicioproyectosearch/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.ordenes_servicio_proyecto_search'),
    (r'^inverboy/home/ordenesservicioproyectodetails/(?P<orden_servicio_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.ordenes_servicio_proyecto_details'),
    (r'^inverboy/home/ordenesservicioproyectochange/(?P<orden_servicio_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.ordenes_servicio_proyecto_change'),
    (r'^inverboy/home/anularordenservicioproyecto/(?P<orden_servicio_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.anular_orden_servicio_proyecto'),
    (r'^inverboy/home/liquidarordenservicioproyecto/(?P<orden_servicio_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.liquidar_orden_servicio_proyecto'),

    (r'^inverboy/home/cortediarioobraaddordenesservicio/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.ordenes_servicio_corte_diario_obra_add'),
    (r'^inverboy/home/cortediarioobraadd/(?P<orden_servicio_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.corte_diario_obra_add'),
    (r'^inverboy/home/cortesdiarioobraproyectosearch/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.cortes_diario_obra_proyecto_search'),
    (r'^inverboy/home/cortesdiarioobraproyectodetails/(?P<corte_diario_obra_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.cortes_diario_obra_proyecto_details'),

    (r'^inverboy/home/actareciboobraproyectoadd/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.acta_recibo_obra_proyecto_add'),
    (r'^inverboy/home/actareciboobraproyectoaddordenessericioproveedor/(?P<proveedor_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.ordenes_servicio_proveedor_acta_recibo_obra_proyecto_add'),
    (r'^inverboy/home/actareciboobraproyectoadd/(?P<orden_servicio_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.items_orden_servicio_proveedor_acta_recibo_obra_proyecto_add'),
    (r'^inverboy/home/actareciboobraproyectoadd/(?P<proveedor_id>\d+)/(?P<orden_servicio_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.registrar_acta_recibo_obra_proyecto_add'),
    (r'^inverboy/home/actasreciboobraproyectosearch/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.actas_recibo_obra_proyecto_search'),
    (r'^inverboy/home/actasreciboobraproyectodetails/(?P<acta_recibo_obra_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.actas_recibo_obra_proyecto_details'),
    (r'^inverboy/home/actasreciboobraproyectochange/(?P<acta_recibo_obra_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.modificar_acta_recibo_obra'),
    (r'^inverboy/home/busquedaactasreciboobraproyectoaprobar/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.busqueda_actas_recibo_obra_aprobar'),
    (r'^inverboy/home/actareciboobraaprobar/(?P<acta_recibo_obra_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.acta_recibo_obra_aprobar'),

    (r'^inverboy/home/facturaordencompraproyectoaddproveedoresordenescompra/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.proveedores_ordenes_compra_factura_add'),
    (r'^inverboy/home/facturaordencompraproyectoaddordenescompraproveedor/(?P<proveedor_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.ordenes_compra_proveedor_factura_add'),
    (r'^inverboy/home/facturaordencompraproyectoaddinformesrecepcionordencompra/(?P<orden_compra_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.informes_recepcion_factura_orden_compra_add'),
    (r'^inverboy/home/facturaordencompraproyectoadddetalles/(?P<proveedor_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.detalles_factura_orden_compra_add'),
    (r'^inverboy/home/busquedafacturasordenescompraproyecto/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.busqueda_factura_orden_compra_proyecto'),
    (r'^inverboy/home/detallesfacturaordencompraproyecto/(?P<factura_orden_compra_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.factura_orden_compra_detalles'),
    (r'^inverboy/home/pdffacturaordencompraproyecto/(?P<factura_orden_compra_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.pdf_factura_orden_compra'),
    (r'^inverboy/home/eliminarfacturaordencompraproyecto/(?P<factura_orden_compra_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.eliminar_factura_orden_compra_proyecto'),

    #Reportes
    (r'^inverboy/home/reportepresupuestoproyectodiscriminadoapus/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.reporte_presupuesto_proyecto_discriminado_apus'),
    
    (r'^inverboy/home/reportepagoactasreciboobra/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.reporte_pago_actas_recibo_obra'),
    (r'^inverboy/home/reportevaloressuministrosordencompra/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.reporte_valor_suministros_orden_compra'),
    (r'^inverboy/home/reportesuministrosproyecto/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.reporte_analisis_cantidades_suministros_proyecto'),
    (r'^inverboy/home/reporteanalisispreciossuministrosapusproyecto/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.reporte_analisis_precios_apus_proyecto'),
    (r'^inverboy/home/reporteanalisispreciossuministrosproyecto/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.reporte_analisis_precios_suministros_proyecto'),

    #Buzon de sugerencias
    (r'^inverboy/home/sugerencias/$', 'aplicacion.inverboy.views_proyecto.views_modulo_usuario.buzon_sugerencia_add'),
    (r'^inverboy/home/reportesugerencias/$', 'aplicacion.inverboy.views_proyecto.views_modulo_usuario.reporte_buzon_sugerencias'),
    (r'^inverboy/home/modificarestadosugerencia/(?P<sugerencia_id>\d+)/(?P<estado>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_usuario.modificar_estado_sugerencia'),

    #Imprimir reportes
    (r'^inverboy/home/imprimir/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.drawPageFrame'),
    #Imprimir requisicion
    (r'^inverboy/home/imprimirrequisicion/(?P<requisicion_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.pdf_requisicion'),
    #Imprimir cotizacion
    (r'^inverboy/home/imprimircotizacion/(?P<cotizacion_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.pdf_cotizacion_orden'),
    #Imprimir orden_compra
    (r'^inverboy/home/imprimirordencompra/(?P<orden_compra_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.pdf_orden_compra'),
    #Imprimir informe_recepcion
    (r'^inverboy/home/imprimirinformerecepcion/(?P<informe_recepcion_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.pdf_informe_recepcion'),
    #Imprimir reporte almacen
    (r'^inverboy/home/imprimirreportealmacen/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.pdf_reporte_almacen'),
    #Imprimir informe_salida
    (r'^inverboy/home/imprimirinformesalida/(?P<informe_salida_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.pdf_informe_salida'),
    #Imprimir todos informe_salida
    (r'^inverboy/home/imprimirinformessalidas/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.pdf_informes_salidas'),
    #Imprimir orden_servicio
    (r'^inverboy/home/imprimirordenservicio/(?P<orden_servicio_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.pdf_orden_servicio'),
    #Imprimir acta_recibo_obra
    (r'^inverboy/home/imprimiractareciboobraproveedor/(?P<acta_recibo_obra_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.pdf_acta_recibo_obra_proveedor'),
    (r'^inverboy/home/imprimiractareciboobracontabilidad/(?P<acta_recibo_obra_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.pdf_acta_recibo_obra_contabilidad'),
    #Imprimir orden_giro
    (r'^inverboy/home/imprimirordengiro/(?P<orden_giro_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.pdf_orden_giro'),
    #Imprimir acta_conformidad
    (r'^inverboy/home/imprimiractaconformidad/(?P<acta_conformidad_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.pdf_acta_conformidad'),

    #Ventas
    #Imprimir apertura fiducuenta
    (r'^inverboy/home/imprimirdocumentoaperturafiducuenta/(?P<contrato_venta_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.pdf_documento_apertura_fiducuenta'),
    #Imprimir carta de instrucciones
    (r'^inverboy/home/imprimirdocumentocartainstrucciones/(?P<contrato_venta_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.pdf_documento_carta_instrucciones'),
    #Imprimir promesa compraventa
    (r'^inverboy/home/imprimirdocumentopromesacompraventa/(?P<contrato_venta_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.pdf_documento_promesa_compraventa'),

    (r'^$', 'aplicacion.inverboy.views_proyecto.views_modulo_usuario.logear'),

    # URLS para administracion de la aplicacion
    (r'^inverboy/home/actualizaraplicacion/$', 'aplicacion.inverboy.views_proyecto.views_modulo_usuario.actualizar_aplicacion'),
    (r'^inverboy/home/realizarbackupgruposusuario/$', 'aplicacion.inverboy.views_proyecto.views_modulo_usuario.realizar_backup_grupos_usuario'),
    (r'^inverboy/home/restaurarbackupgruposusuario/$', 'aplicacion.inverboy.views_proyecto.views_modulo_usuario.restaurar_backup_grupos_usuario'),

    (r'^inverboy/home/comprobarcantidadespresupuesto/$', 'aplicacion.inverboy.views_proyecto.views_modulo_usuario.comprobar_cantidades_presupuesto'),

    # Novedades
    (r'^inverboy/home/novedades/(?P<referencia>\S+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_usuario.novedades'),


    #### MODULO VENTAS ####

    (r'^inverboy/home/busquedadocumentosventas/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.busqueda_documentos_ventas'),
    (r'^inverboy/home/detallesdocumentoventas/(?P<documento>.+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.detalles_documento_ventas'),
    (r'^inverboy/home/registrardocumentoventaaperturafiducuenta/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.registrar_documento_venta_apertura_fiducuenta'),
    (r'^inverboy/home/registrardocumentoventacartainstrucciones/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.registrar_documento_venta_carta_instrucciones'),
    (r'^inverboy/home/registrardocumentoventapromesacompraventa/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.registrar_documento_venta_promesa_compraventa'),

    (r'^inverboy/home/nuevaentidadbancaria/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.nueva_entidad_bancaria'),
    (r'^inverboy/home/busquedaentidadesbancarias/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.busqueda_entidades_bancarias'),
    (r'^inverboy/home/modificarentidadbancaria/(?P<entidad_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.modificar_entidad_bancaria'),

    (r'^inverboy/home/nuevaencuesta/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.nueva_encuesta'),
    (r'^inverboy/home/busquedaencuestas/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.busqueda_encuestas'),
    (r'^inverboy/home/detallesencuesta/(?P<encuesta_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.detalles_encuesta'),
    (r'^inverboy/home/modificarencuesta/(?P<encuesta_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.modificar_encuesta'),

    (r'^inverboy/home/nuevotipoadicional/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.nuevo_tipo_adicional_agrupacion'),
    (r'^inverboy/home/busquedatipoadicionales/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.busqueda_tipos_adicional'),
    (r'^inverboy/home/modificartipoadicional/(?P<tipo_adicional_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.modificar_tipo_adicional'),

    (r'^inverboy/home/nuevoadicional/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.nuevo_adicional_agrupacion'),
    (r'^inverboy/home/busquedaadicionales/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.busqueda_adicionales'),
    (r'^inverboy/home/modificaradicional/(?P<adicional_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.modificar_adicional_agrupacion'),

    (r'^inverboy/home/nuevocliente/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.nuevo_cliente'),
    (r'^inverboy/home/busquedaclientes/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.busqueda_clientes'),
    (r'^inverboy/home/modificarcliente/(?P<cliente_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.modificar_cliente'),
    (r'^inverboy/home/detallescliente/(?P<cliente_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.detalles_cliente'),

    (r'^inverboy/home/nuevoprospectoventa/(?P<cliente_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.nuevo_prospecto_venta'),
    (r'^inverboy/home/detallesprospectoventa/(?P<cliente_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.detalles_prospecto_venta'),

    (r'^inverboy/home/nuevaseccionproyecto/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.nueva_seccion_proyecto'),
    (r'^inverboy/home/busquedaseccionesproyecto/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.busqueda_secciones_proyecto'),
    (r'^inverboy/home/modificarseccionproyecto/(?P<seccion_proyecto_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.modificar_seccion_proyecto'),
    (r'^inverboy/home/nuevotipoinmueble/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.nuevo_tipo_inmueble'),
    (r'^inverboy/home/busquedatipoinmuebles/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.busqueda_tipo_inmuebles'),
    (r'^inverboy/home/modificartipoinmueble/(?P<tipo_inmueble_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.modificar_tipo_inmueble'),
    (r'^inverboy/home/nuevoinmueble/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.nuevo_inmueble'),
    (r'^inverboy/home/busquedainmuebles/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.busqueda_inmuebles'),
    (r'^inverboy/home/modificarinmueble/(?P<inmueble_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.modificar_inmueble'),
    (r'^inverboy/home/modificacionmasivainmuebles/(?P<inmueble_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.modificacion_masiva_inmuebles'),
    (r'^inverboy/home/asignacionindividualpreciosinmuebles/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.asignacion_individual_precios_inmuebles'),
    (r'^inverboy/home/nuevaagrupacioninmueble/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.nueva_agrupacion_inmueble'),
    (r'^inverboy/home/busquedaagrupacioninmuebles/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.busqueda_agrupacion_inmuebles_proyecto'),
    (r'^inverboy/home/modificaragrupacioninmueble/(?P<agrupacion_inmueble_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.modificar_agrupacion_inmueble'),
    (r'^inverboy/home/eliminaragrupacioninmueble/(?P<agrupacion_inmueble_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.eliminar_agrupacion_inmueble'),
    # Crear un contrato de venta a partir de la busqueda de inmuebles en el proyecto
    (r'^inverboy/home/busquedaagrupacioninmueblesproyectonuevocontratoventa/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.busqueda_agrupacion_inmuebles_proyecto_nuevo_contrato_venta'),
    # Crear un contrato de venta a partir del prospecto de un cliente en un proyecto
    (r'^inverboy/home/nuevocontratoventa/(?P<agrupacion_inmueble_id>\d+)/(?P<prospecto_venta_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.nuevo_contrato_venta'),
    (r'^inverboy/home/busquedacontratoventa/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.busqueda_contrato_venta'),
    (r'^inverboy/home/detallescontratoventa/(?P<contrato_venta_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.detalles_contrato_venta'),
    (r'^inverboy/home/modificarcontratoventa/(?P<contrato_venta_id>\d+)/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.modificar_contrato_venta'),

    #Reportes
    (r'^inverboy/home/reportesventas/(?P<proyecto_id>\d+)/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.principal_reportes_ventas'),
      
    #### #### MODULO PLANES #### ####

    # Stages
    url(r'^inverboy/home/stageadd/(?P<project_id>\d+)/$', 'inverboy.views_proyecto.views_modulo_planes.new_stage', name='stage_add'),
    url(r'^inverboy/home/stagechange/(?P<stage_id>\d+)/(?P<project_id>\d+)/$', 'inverboy.views_proyecto.views_modulo_planes.change_stage', name='stage_change'),
    url(r'^inverboy/home/stagedelete/(?P<stage_id>\d+)/(?P<project_id>\d+)/$', 'inverboy.views_proyecto.views_modulo_planes.delete_stage', name='stage_delete'),
    url(r'^inverboy/home/stagesreport/(?P<project_id>\d+)/$', 'inverboy.views_proyecto.views_modulo_planes.stages_report', name='stages_report'),

    #Phases
    url(r'^inverboy/home/phaseadd/(?P<stage_id>\d+)/(?P<project_id>\d+)/$',
        'inverboy.ajax_archivos_proyecto.ajax_planes.ajax_server.new_phase', name='phase_add'),
    url(r'^inverboy/home/phasechange/(?P<phase_id>\d+)/(?P<project_id>\d+)/$',
        'inverboy.ajax_archivos_proyecto.ajax_planes.ajax_server.change_phase', name='phase_change'),
    url(r'^inverboy/home/phasedelete/(?P<phase_id>\d+)/(?P<stage_id>\d+)/(?P<project_id>\d+)/$', 'inverboy.views_proyecto.views_modulo_planes.delete_phase', name='phase_delete'),
    url(r'^inverboy/home/phasesreport/(?P<stage_id>\d+)/(?P<project_id>\d+)/$', 'inverboy.views_proyecto.views_modulo_planes.phases_report', name='phases_report'),

    #Planes
    url(r'^inverboy/home/newplane/(?P<phase_id>\d+)/(?P<project_id>\d+)/$',
        'inverboy.ajax_archivos_proyecto.ajax_planes.ajax_server.new_plane', name='new_plane'),
    url(r'^inverboy/home/planechange/(?P<image_plane_id>\d+)/(?P<project_id>\d+)/$',
        'inverboy.ajax_archivos_proyecto.ajax_planes.ajax_server.change_plane', name='change_plane'),
    url(r'^inverboy/home/planedescription/(?P<plane_id>\d+)/(?P<project_id>\d+)/$', 'inverboy.views_proyecto.views_modulo_planes.plane_description', name='plane_description'),
    url(r'^inverboy/home/imageplanedelete/(?P<image_plane_id>\d+)/(?P<project_id>\d+)/$', 'inverboy.views_proyecto.views_modulo_planes.delete_image_plane', name='image_plane_delete'),

    #Photographic zones
    url(r'^inverboy/home/cronologicalpicturesreport/(?P<photographic_zone_plane_id>\d+)/(?P<project_id>\d+)/$', 'inverboy.views_proyecto.views_modulo_planes.chronological_pictures_report', name='pictures_report'),
    url(r'^inverboy/home/cronologicalpicturesreport/(?P<chronological_picture_id>\d+)/(?P<photographic_zone_plane_id>\d+)/(?P<project_id>\d+)/$', 'inverboy.views_proyecto.views_modulo_planes.chronological_pictures_report_picture_details', name='picture_report'),
    url(r'^inverboy/home/deletecronologicalpicture/(?P<chronological_picture_id>\d+)/(?P<photographic_zone_plane_id>\d+)/(?P<project_id>\d+)/$', 'inverboy.views_proyecto.views_modulo_planes.delete_chronological_picture', name='picture_report'),

    #Upload multiple file's pictures
    url(r'^inverboy/home/chronologicalpicturesupload/(?P<project_id>\d+)/$', 'inverboy.views_proyecto.views_modulo_planes.upload_chronological_pictures', name='upload_chronological_pictures'),

    #Publications project report
    url(r'^inverboy/home/publicationsproject/(?P<project_id>\d+)/$', 'inverboy.views_proyecto.views_modulo_planes.publications_project', name='publications_project'),

    # Ajax Server
    url(r'^inverboy/home/ajax/photographiczonesplaneimageplaneadd/(?P<image_plane_id>\d+)/(?P<project_id>\d+)/$',
        'inverboy.ajax_archivos_proyecto.ajax_planes.ajax_server.photographiczonesplane_image_plane_add', name='photographiczonesplane_image_plane_add'),
    url(r'^inverboy/home/ajax/photographiczonesplaneimageplaneremove/(?P<image_plane_id>\d+)/(?P<photographiczoneplane_id>\d+)/(?P<project_id>\d+)/$',
        'inverboy.ajax_archivos_proyecto.ajax_planes.ajax_server.photographiczonesplane_image_plane_remove', name='photographiczonesplane_image_plane_remove'),
    url(r'^inverboy/home/ajax/getphotographiczonesplaneimageplane/(?P<image_plane_id>\d+)/(?P<project_id>\d+)/$',
        'inverboy.ajax_archivos_proyecto.ajax_planes.ajax_server.get_photographiczonesplane_image_plane', name='get_photographiczonesplane_image_plane'),

    url(r'^inverboy/home/ajax/newpublishedproject/(?P<project_id>\d+)/$',
        'inverboy.ajax_archivos_proyecto.ajax_planes.ajax_server.new_published_project', name='new_published_project'),

    url(r'^inverboy/home/ajax/newcommentpublishedproject/(?P<published_project_id>\d+)/(?P<project_id>\d+)/$',
        'inverboy.ajax_archivos_proyecto.ajax_planes.ajax_server.new_comment_published_project', name='new_comment_published_project'),

    url(r'^inverboy/home/ajax/commentspublishedproject/(?P<published_id>\d+)/(?P<project_id>\d+)/$',
        'inverboy.ajax_archivos_proyecto.ajax_planes.ajax_server.comments_published_project', name='comments_published_project'),

    url(r'^inverboy/home/ajax/pagedpublicationsproject/(?P<page>\d+)/(?P<project_id>\d+)/$',
        'inverboy.ajax_archivos_proyecto.ajax_planes.ajax_server.paged_publications_project', name='paged_publications_project'),

    url(r'^inverboy/home/ajax/listdatesphotographiczoneplaneproject/(?P<photographic_zone_plane_id>\d+)/(?P<project_id>\d+)/$',
        'inverboy.ajax_archivos_proyecto.ajax_planes.ajax_server.list_dates_photographic_zone_plane_project', name='list_dates_photographic_zone_plane_project'),

    #### #### MODULO PLANES #### ####

    ########### CAMBIOS DAVID #############



    url(r'^inverboy/home/cotizacionesproyectodetails/agregar_suministro_a_cotizacion/$', 'aplicacion.inverboy.views_proyecto.views_modulo_proyecto.agregar_suministro_a_cotizacion'),
    url(r'^inverboy/home/cuentas_banco/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.cuentas_por_banco'),
    url(r'^inverboy/home/lista_entidades_bancarias/$', 'aplicacion.inverboy.views_proyecto.views_modulo_ventas.lista_entidades_bancarias'),




    url(r'^plano/$', 'aplicacion.inverboy.views_proyecto.views_modulo_planes.form_plane'),


    ########## FIN CAMBIOS DAVID ##########
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the dajax:
    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    (r'^online/', include('online_status.urls')),

)
