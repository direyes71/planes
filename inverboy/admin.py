# -*- encoding: utf-8 -*-
from inverboy.models import *
# from django.contrib import admin
from django.db.models import get_models, get_app
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
#---------------Todos los modelos ----------------
#def autoregister(*app_list):
#    for app_name in app_list:
#        app_models = get_app(app_name)
#        for model in get_models(app_models):
#            try:
#                admin.site.register(model)
#            except AlreadyRegistered:
#                pass

#autoregister('inverboy')
#----------------------------------------------
# class AuthorAdmin(admin.ModelAdmin):
# 	pass
# admin.site.register(EntidadBancaria,AuthorAdmin)
# admin.site.register(NumeroCuenta,AuthorAdmin)
# admin_register(namespace=globals())

#Modelos Admin

#Modelo Admin apu Proyecto
class apuProyectoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_apu')
    search_fields = ('id', 'nombre_apu')

#Modelo Admin apu Proyecto
class suministrosApuProyectoAdmin(admin.ModelAdmin):
    list_display = ('id', 'suministro', 'apu_id_asociado')
    search_fields = ('apu_proyecto__id', 'id')

#Modelo Admin Requisicion
class requisicionAdmin(admin.ModelAdmin):
    list_display = ('id','consecutivo', 'proyecto')
    search_fields = ('id', 'consecutivo')

#Modelo Admin Suministros Requisicion
#class RequisicionAdmin2(admin.ModelAdmin):
    #list_filter = ('id'== 1)
#    list_display = ('id','suministro')
#    search_fields = ('requisicion__id', 'id')

#Modelo Admin Orden de Compra
class ordenCompraAdmin(admin.ModelAdmin):
    list_display = ('id','consecutivo', 'proyecto')
    search_fields = ('id', 'consecutivo')


#Modelo Admin Informe de Recepcion
class informeRecepcionAdmin(admin.ModelAdmin):
    list_display = ('id','consecutivo', 'orden_compra')
    search_fields = ('id', 'consecutivo')

#Modelo Admin Informe de Recepcion
class informeSalidaAdmin(admin.ModelAdmin):
    list_display = ('id','consecutivo', 'proyecto')
    search_fields = ('id', 'consecutivo')

#Modelo Admin Factura Orden de Compra
class facturaOrdenCompraAdmin(admin.ModelAdmin):
    list_display = ('id','consecutivo', 'proyecto')
    search_fields = ('id', 'consecutivo')

#Modelo Admin Orden de Servicio
class ordenServicioAdmin(admin.ModelAdmin):
    list_display = ('id','consecutivo', 'proyecto')
    search_fields = ('id', 'consecutivo')

#Modelo Admin Corte Diario de Obra
class corteDiarioAdmin(admin.ModelAdmin):
    list_display = ('id','consecutivo', 'orden_servicio_id_asociado')
    search_fields = ('id', 'orden_servicio_id_asociado')

#Modelo Admin Acta recibo de Obra
class actaReciboObraAdmin(admin.ModelAdmin):
    list_display = ('id','consecutivo', 'orden_servicio_id_asociado')
    search_fields = ('id', 'orden_servicio_id_asociado')

#Modelo Admin Orden de Giro
class ordenGiroAdmin(admin.ModelAdmin):
    list_display = ('id','consecutivo', 'proyecto')
    search_fields = ('id', 'consecutivo')

#Modelo Admin Acta de Conformidad
class actaConformidadAdmin(admin.ModelAdmin):
    list_display = ('id','consecutivo', 'orden_giro_id_asociado')
    search_fields = ('id', 'orden_giro_id_asociado')

#-------------------------------------------------------------
#Apu proyecto
admin.site.register(ApuProyecto,apuProyectoAdmin)
admin.site.register(SuministroApuProyecto,suministrosApuProyectoAdmin)

#Requisiciones
admin.site.register(Requisicion, requisicionAdmin)
admin.site.register(SuministroRequisicion)

#Orden de Compra
admin.site.register(OrdenCompra, ordenCompraAdmin)
admin.site.register(SuministroOrdenCompraItem)
admin.site.register(SuministroOrdenCompra)

#Informe de recepcion
admin.site.register(InformeRecepcion, informeRecepcionAdmin)
admin.site.register(SuministroInformeRecepcion)
admin.site.register(SuministroAlmacen)

#Informe de salida
admin.site.register(InformeSalida, informeSalidaAdmin)
admin.site.register(SuministroInformeSalida)
admin.site.register(SuministroInformeSalidaItem)

#Factura Orden de compra
admin.site.register(FacturaOrdencompra, facturaOrdenCompraAdmin)
admin.site.register(SuministroFacturaOrdenCompra)
admin.site.register(ItemFacturaOrdenCompra)

#--------------------------------------------------------------
#Orden de Servicio
admin.site.register(OrdenServicio, ordenServicioAdmin)
admin.site.register(SuministroOrdenServicioItem)
admin.site.register(SuministroOrdenServicio)

#Corte Diario de Obra
admin.site.register(CorteDiarioObra, corteDiarioAdmin)
admin.site.register(SuministroCorteDiarioObra)

#Acta recibo de Obra
admin.site.register(ActaReciboObra, actaReciboObraAdmin)
admin.site.register(ItemActaReciboObra)

#Orden de Giro
admin.site.register(OrdenGiro, ordenGiroAdmin)
admin.site.register(ItemOrdenGiro)

#Acta de Conformidad
admin.site.register(ActaConformidad, actaConformidadAdmin)
admin.site.register(ItemActaConformidad)

#Clientes
admin.site.register(Cliente)

#Seccion Proyecto
admin.site.register(SeccionProyecto)

#Tipo Inmueble
admin.site.register(TipoInmueble)

#Inmueble
admin.site.register(Inmueble)

#Agrupación Inmueble
admin.site.register(AgrupacionInmueble)
admin.site.register(ItemAgrupacionInmueble)

#Encuesta
admin.site.register(Encuesta)

#Prospecto de Venta
admin.site.register(ProspectoVenta)
admin.site.register(AgrupacionesInmuebleProspectoVenta)

#Contrato de Venta
admin.site.register(ContratoVenta)
admin.site.register(AgrupacionInmuebleContratoVenta)
admin.site.register(AdicionalAgrupacionContratoVenta)
admin.site.register(ClienteContratoVenta)
admin.site.register(ContactoCliente)
admin.site.register(PagoEntidadContratoVenta)
admin.site.register(PagoEfectivoContratoVenta)
admin.site.register(AbonoPagoEfectivoContratoVenta)
admin.site.register(NotificacionVenta)
admin.site.register(ModificacionContratoVenta)
admin.site.register(Proyecto)



#admin.site.register(SuministroRequisicion)
#admin.site.register()
#admin.site.register()