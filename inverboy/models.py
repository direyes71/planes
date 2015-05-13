# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User, Group
import decimal

from django.db.models import Sum, Max

#CONSULTAS ANIDADAS
from django.db.models import Q

#Libreria para comparar atributos de un modelo (En BD compara 2 columnas de la misma tabla)
from django.db.models import F

from django_thumbs.db.models import ImageWithThumbsField
import settings

# Create your models here.


#Listado de departamentos y municipios
class Pais(models.Model):
    nombre = models.CharField(max_length=40)
    class Meta:
        verbose_name_plural = "paises"

    def __unicode__(self):
        return self.nombre

class Departamento(models.Model):
    nombre = models.CharField(max_length=40)
    pais = models.ForeignKey(Pais)

    def __unicode__(self):
        return self.nombre

class Municipio(models.Model):
    nombre = models.CharField(max_length=40)
    pais  = models.ForeignKey(Pais)
    departamento = models.ForeignKey(Departamento)

    def __unicode__(self):
        return self.nombre


# Modelo Usuario
class Usuario(User):
    identificacion = models.BigIntegerField(unique=True)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=30)
    celular = models.CharField(max_length=10)
    telefono = models.CharField(max_length=10, null=True)
    cargo = models.CharField(max_length=40, null=True)
    municipio = models.ForeignKey(Municipio)

    def __unicode__(self):
		return unicode(self.first_name) + ' ' + unicode(self.last_name)

    def full_name(self):
		return self.first_name + ' ' + self.last_name

    def lista_proyectos_vinculados(self):
        proyectos = []
        #Si es superusuario tiene vinculo a todos los proyectos
        if self.is_superuser:
            proyectos = Proyecto.objects.all()
        #Si no es superusuario
        else:
            vinculos_proyectos = self.personaadministrativoproyecto_set.filter(estado_registro=True)
            ids_proyectos = []
            for vinculo in vinculos_proyectos:
                ids_proyectos.append(vinculo.proyecto.id)
            proyectos = Proyecto.objects.filter(id__in=ids_proyectos)
        return proyectos


class Historial(models.Model):
    usuario = models.ForeignKey(Usuario)
    direccion_ip = models.CharField(max_length=30)
    actividad = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)


class Proveedor(models.Model):
    identificacion = models.BigIntegerField(unique=True)
    razon_social = models.CharField(max_length=80)
    nombre_comercial = models.CharField(max_length=40, null=True, blank=True)
    tipo = models.SmallIntegerField(max_length=1) # Persona Natural ó Juridica
    regimen_tributario = models.IntegerField(max_length=1) #Regimen tributario: 1-Común, 2-Simplificado
    direccion = models.CharField(max_length=30)
    telefono_1 = models.CharField(max_length=10)
    telefono_2 = models.CharField(max_length=10, null=True, blank=True)
    fax = models.CharField(max_length=10, null=True, blank=True)
    web_site = models.CharField(max_length=40, null=True, blank=True)
    email = models.CharField(max_length=40, null=True, blank=True)
    estado_proveedor = models.BooleanField(default=True) # Activo ó inactivo
    observaciones = models.TextField(null=True, blank=True)
    municipio = models.ForeignKey(Municipio)

    class Meta:
        verbose_name_plural = "Proveedores"

    def __unicode__(self):
		return "id=%s - razonsocial=%s" % (self.pk, unicode(self.razon_social))


class Contacto(models.Model):
    nombre_contacto = models.CharField(max_length=80)
    cargo_contacto = models.IntegerField(max_length=1)
    telefono_contacto = models.CharField(max_length=10)
    ext_contacto = models.CharField(max_length=4, null=True, blank=True)
    celular_contacto = models.CharField(max_length=10, null=True, blank=True)
    email_contacto = models.CharField(max_length=40, null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor)


class Categoria(models.Model):
    nombre = models.CharField(max_length=40)
    tipo = models.SmallIntegerField(max_length=1) # Categoria, especificacion ó tipo
    estado = models.BooleanField(default=True) # Activo ó inactivo
    categoria_asociada = models.ForeignKey('self', null=True, blank=True) # Categoria padre

    def __unicode__(self):
		return self.nombre
    

class Suministro(models.Model):
    clasificacion_general = models.CharField(max_length=12)
    codigo = models.SmallIntegerField()
    nombre = models.CharField(max_length=80)
    sinonimos = models.TextField(null=True, blank=True)
    representativo = models.IntegerField(max_length=1)
    unidad_embalaje = models.FloatField(max_length=10.00, default=-1)
    unidad_medida = models.CharField(max_length=12)
    dias_compra = models.PositiveIntegerField()
    requiere_cartilla = models.BooleanField(default=False) # Si el suministro requiere numero de cartilla a la hora de requerir (True/False)
    promedio_precio_suministro = models.FloatField(default=0)
    estado_suministro = models.BooleanField(default=True) # Activo ó inactivo
    peso = models.FloatField(null=True, max_length=10.0, blank=True)
    largo = models.FloatField(null=True, max_length=10.0, blank=True)
    alto = models.FloatField(null=True, max_length=10.0, blank=True)
    ancho = models.FloatField(null=True, max_length=10.0, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True) # Se coloca la fecha actual en la que se creo el objeto
    fecha_actualizacion = models.DateTimeField(auto_now=True) # Se actualiza a la fecha actual cada vez que se actualice el objeto
    categoria = models.ForeignKey(Categoria)
    usuario = models.ForeignKey(Usuario)

    def get_proveedores_activos_suministro(self, criterio=''):
        proveedores = self.suministroproveedor_set.filter(proveedor__estado_proveedor=True)
        if criterio != '':
            try:
                criterio = int(criterio)
                proveedores.filter(Q(proveedor__identificacion=criterio))
            except :
                proveedores = proveedores.filter(Q(proveedor__razon_social__icontains=criterio)|Q(proveedor__nombre_comercial__icontains=criterio))
        return proveedores

    def get_codigo_suministro(self):
        codigo = self.codigo
        clasificacion = self.categoria
        while(clasificacion != None):
            codigo = str(clasificacion.id) + '.' + str(codigo)
            clasificacion = clasificacion.categoria_asociada
        return codigo

    def __unicode__(self):
        return self.nombre


class SuministroProveedor(models.Model):
    precio_suministro = models.FloatField()
    iva_suministro = models.FloatField()
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    suministro = models.ForeignKey(Suministro)
    proveedor = models.ForeignKey(Proveedor)

    def __unicode__(self):
        return self.suministro
    class Meta:
        unique_together = ('suministro', 'proveedor')



class Capitulo(models.Model):
    nombre_capitulo = models.CharField(max_length=40)
    tipo_capitulo = models.SmallIntegerField(max_length=1) # Capitulo ó subcapitulo
    estado_capitulo = models.BooleanField(default=1) # Activo ó inactivo
    capitulo_asociado = models.ForeignKey('self', null=True, blank=True) # Capitulo padre

    def __unicode__(self):
		return self.nombre_capitulo


class Apu(models.Model):
    nombre_apu = models.CharField(max_length=60)
    unidad_medida_apu = models.CharField(max_length=12)
    estado_apu = models.BooleanField(default=True) # Activo ó inactivo
    fecha_creacion_apu = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion_apu = models.DateTimeField(auto_now=True)
    precio_apu = models.FloatField()
    capitulo = models.ForeignKey(Capitulo)
    usuario = models.ForeignKey(Usuario)

    def valor_promedio(self):
        suministros_apu = self.suministroapu_set.all()
        valor_promedio = 0
        for suministro_apu in suministros_apu:
            valor_promedio = round(valor_promedio + (round(suministro_apu.valor_promedio() * suministro_apu.cantidad_suministro, 2)), 2)
        return valor_promedio

    def actualizar_promedio_valor_suministros_apu(self):
        suministros = self.suministroapu_set.all()
        for suministro in suministros:
            suministro.valor_promedio()

    def __unicode__(self):
        return self.nombre_apu

class SuministroApu(models.Model):
    cantidad_suministro = models.FloatField()
    precio_suministro  = models.FloatField()
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    suministro = models.ForeignKey(Suministro)
    apu = models.ForeignKey(Apu)

    def valor_promedio(self):
        promedio = 0
        suministro_proveedores = self.suministro.suministroproveedor_set.all()
        for suministro_proveedor in suministro_proveedores:
            promedio = round(promedio + (round(suministro_proveedor.precio_suministro + (round(suministro_proveedor.precio_suministro * suministro_proveedor.iva_suministro, 2)), 2)), 2)
        promedio = round(promedio / len(suministro_proveedores), 2)
        self.precio_suministro = "%.2f" % promedio
        self.save()
        return promedio
    
    #Retorna el valor parcial del suministro en el APU (cantidad_suministro * precio_suministro)
    def valor_parcial(self):
        return round(self.cantidad_suministro * self.precio_suministro, 2)

    def __unicode__(self):
       return self.suministro


class Proyecto(models.Model):
    nombre = models.CharField(max_length=30)
    iniciales = models.CharField(max_length=4)
    direccion = models.CharField(max_length=30)
    ext = models.IntegerField(max_length=3,null=True, blank=True)
    tipo_proyecto = models.CharField(max_length=40)
    estado_proyecto = models.SmallIntegerField(max_length=1, default=1) # 1 - Activo, 0 - Inactivo
    proceso_proyecto = models.SmallIntegerField(default=1) # Proceso del proyecto: En presupuesto, en ejecucuion, terminado
    rete_ica = models.FloatField(default=0) # Valor rete_ica según el municipio de ubicacion del proyecto
    rete_fuente = models.FloatField(default=0) # Valor rete_fuente según el municipio de ubicacion del proyecto
    apertura_fiducuenta = models.TextField(null=True,blank=True) # Imprimir en cualquier momento
    carta_instrucciones = models.TextField(null=True,blank=True) # Imprimir desde separado
    promesa_compraventa = models.TextField(null=True,blank=True) # Al imprimir pasa el contrato a estado 3-Vendido imprimir pasa el contrato a estado 3-Vendido
    municipio = models.ForeignKey(Municipio)

    class Meta:
        unique_together = (('nombre', 'municipio'), ('iniciales', 'municipio')) # No se bede duplicar el nombre ni las iniciales de un proyecto en el mismo municipio

    def lista_capitulos_activos(self):
        capitulos = self.capituloapuproyecto_set.filter(tipo_capitulo=1, estado_capitulo=True)
        return capitulos

    def valor_total_presupuesto_proyecto(self):
        valor_total_presupuesto_proyecto = 0
        for capitulo in self.capituloapuproyecto_set.filter(tipo_capitulo=1, estado_capitulo=True):
            valor_total_presupuesto_proyecto = round(valor_total_presupuesto_proyecto + capitulo.valor_total_capitulo(), 2)
        return valor_total_presupuesto_proyecto
    
    #Retorna todos los suministros pendientes (SuministroRequisicion) por comprar agrupados por Suministro
    def get_suministros_pendientes_comprar_agrupados_suministro(self, criterio='', proveedor_id=None, suministro_id=None, tipo_cotizacion=1, exclude_suministros_id=None):
        #Suministros cuya requisición este aprobada
        suministros = SuministroRequisicion.objects.filter(requisicion__proyecto=self, requisicion__estado__in=[2, 3], cantidad_comprada__lt=F('cantidad_requerida'))

        if exclude_suministros_id != None:
            suministros = suministros.exclude(suministro__suministro__id__in=exclude_suministros_id)

        if tipo_cotizacion == 1:
            suministros = suministros.filter(suministro__suministro__clasificacion_general='Material')
        elif tipo_cotizacion == 2:
            suministros = suministros.exclude(suministro__suministro__clasificacion_general='Material')
            suministros = suministros.exclude(suministro__suministro__clasificacion_general='Indirectos')
        if criterio != '':
            suministros = suministros.filter(Q(suministro__suministro__nombre__icontains=criterio) | Q(suministro__suministro__sinonimos__icontains=criterio))
        if proveedor_id != None:
            suministros_proveedor = SuministroProveedor.objects.filter(proveedor__id=proveedor_id)
            ids_suministros_proveedor = []
            for suministro_proveedor in suministros_proveedor:
                ids_suministros_proveedor.append(suministro_proveedor.suministro_id)
            suministros = suministros.filter(suministro__suministro__id__in=ids_suministros_proveedor)

        if suministro_id != None:
            suministros = suministros.filter(suministro__suministro__id=suministro_id)

        suministros = suministros.order_by('suministro__suministro__nombre', 'requisicion__fecha_arribo')

        #Lista a retornar
        lista_suministros = []
        #Agrupar por suministro
        for suministro in suministros:
            suministro_adicionado = False
            for suministro_lista in lista_suministros:
                if suministro_lista.suministro.suministro.id == suministro.suministro.suministro.id:
                    suministro_lista.cantidad_requerida = round(suministro_lista.cantidad_requerida + (round(suministro.cantidad_requerida - suministro.cantidad_comprada, 2)), 2)
                    suministro_lista.cantidad_comprada = round(suministro_lista.cantidad_comprada + suministro.cantidad_comprada, 2)
                    if suministro.observaciones != '':
                        if suministro_lista.observaciones != '':
                            observaciones = suministro_lista.observaciones + ', ' + suministro.observaciones
                        else:
                            observaciones = suministro_lista.observaciones + suministro.observaciones
                        observaciones = observaciones.strip()
                        suministro_lista.observaciones = observaciones
                    suministro_adicionado = True
            if suministro_adicionado == False:
                suministro.cantidad_requerida = round(suministro.cantidad_requerida - suministro.cantidad_comprada, 2)
                lista_suministros.append(suministro)
        return lista_suministros

    def numero_requisiciones_pendientes_aprobar(self):
        numero_requisiciones_pendientes_aprobar = len(self.requisicion_set.filter(estado=1))
        return numero_requisiciones_pendientes_aprobar

    def numero_actas_recibo_obra_pendientes_aprobar(self):
        numero_actas_recibo_obra_pendientes_aprobar = len(ActaReciboObra.objects.filter(orden_servicio__proyecto=self, estado_registro_acta=1))
        return numero_actas_recibo_obra_pendientes_aprobar

    #Retorna todos los suministros pendientes (SuministroRequuisicion) por comprar, sin agruparlos por Suministro
    def get_suministros_pendientes_comprar(self, criterio='', proveedor_id=None, suministro_id=None, suministro_requisicion_id=None, clasificacion_general=[]):
        suministros = SuministroRequisicion.objects.filter(requisicion__proyecto=self, requisicion__estado=2, suministro__suministro__clasificacion_general__in=clasificacion_general)
        if criterio != '':
            suministros = suministros.filter(Q(suministro__suministro__nombre__icontains=criterio) | Q(suministro__suministro__sinonimos__icontains=criterio))
        if proveedor_id != None:
            suministros_proveedor = SuministroProveedor.objects.filter(proveedor__id=proveedor_id)
            ids_suministros_proveedor = []
            for suministro_proveedor in suministros_proveedor:
                ids_suministros_proveedor.append(suministro_proveedor.suministro_id)
            suministros = suministros.filter(id__in=ids_suministros_proveedor)

        if suministro_id != None:
            suministros = suministros.filter(suministro__suministro__id=suministro_id)
        
        if suministro_requisicion_id != None:
            suministros = suministros.filter(id=suministro_requisicion_id)

        suministros = suministros.filter(cantidad_comprada__lt=F('cantidad_requerida'))
        suministros = suministros.order_by('requisicion__fecha_arribo', 'suministro__suministro__nombre')
        return suministros

    #Retorna TRUE si la cantidad disponible a comprar es correcta
    def validar_cantidad_suministro_pendientes_comprar(self, suministro_requisicion_id=None, cantidad_evaluar=0, clasificacion_general=[]):
        suministro_requisicion = list(self.get_suministros_pendientes_comprar(suministro_requisicion_id=suministro_requisicion_id, clasificacion_general=clasificacion_general)).pop()
        cantidad_disponible = False
        if cantidad_evaluar <= round(suministro_requisicion.cantidad_requerida - suministro_requisicion.cantidad_comprada, 2):
            cantidad_disponible = True
        return cantidad_disponible


    #Lista los APU's que tienen suministos (sin indirectos)
    def lista_apus_sin_indirectos(self, criterio=''):
        ids_apus = []
        for apu in self.apuproyecto_set.filter(estado_apu=True, nombre_apu__icontains=criterio):
            if len(apu.suministroapuproyecto_set.filter(suministro__clasificacion_general='Indirectos')) == 0:
                ids_apus.append(apu.id)
        apus = self.apuproyecto_set.filter(id__in=ids_apus)
        return apus
    
    #Lista los APU's que tienen suministos indirectos
    def lista_apus_indirectos(self, criterio=''):
        apus = []
        criterio = criterio.strip()
        for apu in self.apuproyecto_set.filter(estado_apu=True, nombre_apu__icontains=criterio):
            apu_indirectos = False
            for suministro in apu.suministroapuproyecto_set.all():
                if suministro.suministro.clasificacion_general == 'Indirectos':
                    apu_indirectos = True
            if apu_indirectos == True:
                apus.append(apu)
        return apus

    #Lista de cotizaciones del proyecto
    def lista_cotizaciones(self, tipo=None, criterio=''):
        cotizaciones = self.cotizacion_set.all()
        if tipo != None:
            cotizaciones = cotizaciones.filter(tipo=tipo)
        if criterio != '':
            try:
                #Busqueda por ID
                criterio = int(criterio)
                cotizaciones = cotizaciones.filter(id=criterio)
            except :
                if len(cotizaciones.filter(proveedor__razon_social__icontains=criterio)) > 0:
                    #Busqueda por proveedor
                    cotizaciones = cotizaciones.filter(proveedor__razon_social__icontains=criterio)
                else:
                    #Busqueda por suministro
                    ids_cotizaciones_excluir = []
                    for cotizacion in cotizaciones:
                        if len(cotizacion.suministrocotizacion_set.filter(suministro__nombre__icontains=criterio)) == 0:
                            ids_cotizaciones_excluir.append(cotizacion.id)
                    if len(ids_cotizaciones_excluir) > 0:
                        cotizaciones = cotizaciones.exclude(id__in=ids_cotizaciones_excluir)
        cotizaciones = cotizaciones.order_by('id', 'proveedor__razon_social')
        return cotizaciones

    def lista_ordenes_compra(self, criterio='', estado=None, proveedor=None, fecha_inicial='', fecha_final=''):
        import re
        ordenes_compra = self.ordencompra_set.all()
        if fecha_inicial != '':
            ordenes_compra = ordenes_compra.filter(fecha_creacion__gt=fecha_inicial + ' 00:00:00')
        if fecha_final != '':
            ordenes_compra = ordenes_compra.filter(fecha_creacion__lt=fecha_final + ' 23:59:59')
        if criterio != '':
            #Realiza la busqueda por codificación (OC#-##)
            patron = re.compile('^OC[0-9]+\-[0-9]+$', re.IGNORECASE)
            resultado = patron.search(criterio)
            if resultado != None:
                criterio = criterio.split('-')
                proyecto_id = criterio[0][2:]
                if self.id == int(proyecto_id):
                    ordenes_compra = ordenes_compra.filter(consecutivo=criterio[1])
                else:
                    ordenes_compra = ordenes_compra.filter(id=0)
            #Si la busqueda no es por codificación (OC#-##)
            else:
                if len(ordenes_compra.filter(proveedor__razon_social__icontains=criterio)) > 0:
                    #Busqueda por proveedor
                    ordenes_compra = ordenes_compra.filter(proveedor__razon_social__icontains=criterio)
                else:
                    #Busqueda por suministro
                    ids_ordenes_compra_excluir = []
                    for orden_compra in ordenes_compra:
                        if len(orden_compra.suministroordencompraitem_set.filter(suministro__nombre__icontains=criterio)) == 0:
                            ids_ordenes_compra_excluir.append(orden_compra.id)
                    if len(ids_ordenes_compra_excluir) > 0:
                        ordenes_compra = ordenes_compra.exclude(id__in=ids_ordenes_compra_excluir)
        if estado != None:
            ordenes_compra = ordenes_compra.filter(estado=1)
        if proveedor != None:
            ordenes_compra = ordenes_compra.filter(proveedor=proveedor)
        if fecha_inicial != '' or fecha_final != '':
            ordenes_compra = ordenes_compra.order_by('fecha_creacion', 'consecutivo')
        else:
            ordenes_compra = ordenes_compra.order_by('consecutivo')
        return ordenes_compra

    def lista_informes_recepcion(self, criterio='', fecha_inicial='', fecha_final=''):
        import re
        informes_recepcion = InformeRecepcion.objects.filter(orden_compra__proyecto=self)
        if fecha_inicial != '':
            informes_recepcion = informes_recepcion.filter(fecha_informe__gt=fecha_inicial + ' 00:00:00')
        if fecha_final != '':
            informes_recepcion = informes_recepcion.filter(fecha_informe__lt=fecha_final + ' 23:59:59')
        if criterio != '':
            #Realiza la busqueda por codificación (IR#-##)
            patron = re.compile('^IR[0-9]+\-[0-9]+$', re.IGNORECASE)
            resultado = patron.search(criterio)
            if resultado != None:
                criterio = criterio.split('-')
                proyecto_id = criterio[0][2:]
                if self.id == int(proyecto_id):
                    informes_recepcion = informes_recepcion.filter(consecutivo=criterio[1])
                else:
                    informes_recepcion = informes_recepcion.filter(id=0)
            #Si la busqueda no es por codificación (IR#-##)
            else:
                #Realiza la busqueda por codificación (OC#-##)
                patron = re.compile('^OC[0-9]+\-[0-9]+$', re.IGNORECASE)
                resultado = patron.search(criterio)
                if resultado != None:
                    criterio = criterio.split('-')
                    proyecto_id = criterio[0][2:]
                    if self.id == int(proyecto_id):
                        informes_recepcion = informes_recepcion.filter(orden_compra__consecutivo=criterio[1])
                    else:
                        informes_recepcion = informes_recepcion.filter(id=0)
                else:
                    if len(informes_recepcion.filter(orden_compra__proveedor__razon_social__icontains=criterio)) > 0:
                        #Busqueda por proveedor
                        informes_recepcion = informes_recepcion.filter(orden_compra__proveedor__razon_social__icontains=criterio)
                    elif len(informes_recepcion.filter(numero_remision=criterio)) > 0:
                        informes_recepcion = informes_recepcion.filter(numero_remision=criterio)
                    else:
                        #Busqueda por suministro
                        ids_informes_recepcion_excluir = []
                        for informe_recepcion in informes_recepcion:
                            if len(informe_recepcion.suministroinformerecepcion_set.filter(suministro__suministro__suministro__suministro__nombre__icontains=criterio)) == 0:
                                ids_informes_recepcion_excluir.append(informe_recepcion.id)
                        if len(ids_informes_recepcion_excluir) > 0:
                            informes_recepcion = informes_recepcion.exclude(id__in=ids_informes_recepcion_excluir)
        if fecha_inicial != '' or fecha_final != '':
            informes_recepcion = informes_recepcion.order_by('fecha_informe', 'consecutivo')
        else:
            informes_recepcion = informes_recepcion.order_by('consecutivo', 'orden_compra__proveedor__razon_social')
        return informes_recepcion

    def lista_informes_salida(self, criterio='', fecha_inicial='', fecha_final=''):
        import re
        informes_salida = self.informesalida_set.all()
        if fecha_inicial != '':
            informes_salida = informes_salida.filter(fecha_informe__gt=fecha_inicial + ' 00:00:00')
        if fecha_final != '':
            informes_salida = informes_salida.filter(fecha_informe__lt=fecha_final + ' 23:59:59')
        if criterio != '':
            #Realiza la busqueda por codificación (SA#-##)
            patron = re.compile('^SA[0-9]+\-[0-9]+$', re.IGNORECASE)
            resultado = patron.search(criterio)
            if resultado != None:
                criterio = criterio.split('-')
                proyecto_id = criterio[0][2:]
                if self.id == int(proyecto_id):
                    informes_salida = informes_salida.filter(consecutivo=criterio[1])
                else:
                    informes_salida = informes_salida.filter(id=0)
            #Si la busqueda no es por codificación (SA#-##)
            else:
                #Busqueda por suministro
                ids_informes_salida_excluir = []
                for informe_salida in informes_salida:
                    if len(informe_salida.suministroinformesalidaitem_set.filter(suministro_almacen__suministro__nombre__icontains=criterio)) == 0:
                        ids_informes_salida_excluir.append(informe_salida.id)
                if len(ids_informes_salida_excluir) > 0:
                    informes_salida = informes_salida.exclude(id__in=ids_informes_salida_excluir)
        if fecha_inicial != '' or fecha_final != '':
            informes_salida = informes_salida.order_by('fecha_informe', 'consecutivo')
        else:
            informes_salida = informes_salida.order_by('consecutivo')

        return informes_salida

    def lista_ordenes_servicio(self, criterio='', estado=None, fecha_inicial='', fecha_final=''):
        import re
        ordenes_servicio = self.ordenservicio_set.all()
        if fecha_inicial != '':
            ordenes_servicio = ordenes_servicio.filter(fecha_creacion__gt=fecha_inicial + ' 00:00:00')
        if fecha_final != '':
            ordenes_servicio = ordenes_servicio.filter(fecha_creacion__lt=fecha_final + ' 23:59:59')
        if criterio != '':
            #Realiza la busqueda por codificación (OS#-##)
            patron = re.compile('^OS[0-9]+\-[0-9]+$', re.IGNORECASE)
            resultado = patron.search(criterio)
            if resultado != None:
                criterio = criterio.split('-')
                proyecto_id = criterio[0][2:]
                if self.id == int(proyecto_id):
                    ordenes_servicio = ordenes_servicio.filter(consecutivo=criterio[1])
                else:
                    ordenes_servicio = ordenes_servicio.filter(id=0)
            #Si la busqueda no es por codificación (OS#-##)
            else:
                if len(ordenes_servicio.filter(Q(proveedor__razon_social__icontains=criterio) | Q(tercero__razon_social__icontains=criterio))) > 0:
                    #Busqueda por proveedor ó por tercero
                    ordenes_servicio = ordenes_servicio.filter(Q(proveedor__razon_social__icontains=criterio) | Q(tercero__razon_social__icontains=criterio))
                else:
                    #Busqueda por suministro
                    ids_ordenes_servicio_excluir = []
                    for orden_servicio in ordenes_servicio:
                        if len(orden_servicio.suministroordenservicioitem_set.filter(suministro__nombre__icontains=criterio)) == 0:
                            ids_ordenes_servicio_excluir.append(orden_servicio.id)
                    if len(ids_ordenes_servicio_excluir) > 0:
                        ordenes_servicio = ordenes_servicio.exclude(id__in=ids_ordenes_servicio_excluir)
        if estado != None:
            ordenes_servicio = ordenes_servicio.filter(estado=estado)
        if fecha_inicial != '' or fecha_final != '':
            ordenes_servicio = ordenes_servicio.order_by('fecha_creacion')
        else:
            ordenes_servicio = ordenes_servicio.order_by('consecutivo')
        return ordenes_servicio

    def lista_cortes_diario_obra(self, criterio='', estado=None, fecha_inicial='', fecha_final=''):
        import re
        cortes_diario_obra = CorteDiarioObra.objects.filter(orden_servicio__proyecto=self)
        if fecha_inicial != '':
            cortes_diario_obra = cortes_diario_obra.filter(fecha_corte__gt=fecha_inicial + ' 00:00:00')
        if fecha_final != '':
            cortes_diario_obra = cortes_diario_obra.filter(fecha_corte__lt=fecha_final + ' 23:59:59')
        if criterio != '':
            #Realiza la busqueda por codificación (CDO#-##)
            patron = re.compile('^CDO[0-9]+\-[0-9]+$', re.IGNORECASE)
            resultado = patron.search(criterio)
            if resultado != None:
                criterio = criterio.split('-')
                proyecto_id = criterio[0][3:]
                if self.id == int(proyecto_id):
                    cortes_diario_obra = cortes_diario_obra.filter(consecutivo=criterio[1])
                else:
                    cortes_diario_obra = cortes_diario_obra.filter(id=0)
            #Si la busqueda no es por codificación (CDO#-##)
            else:
                #Realiza la busqueda por codificación (OS#-##)
                patron = re.compile('^OS[0-9]+\-[0-9]+$', re.IGNORECASE)
                resultado = patron.search(criterio)
                if resultado != None:
                    criterio = criterio.split('-')
                    proyecto_id = criterio[0][2:]
                    if self.id == int(proyecto_id):
                        cortes_diario_obra = cortes_diario_obra.filter(orden_servicio__consecutivo=criterio[1])
                    else:
                        cortes_diario_obra = cortes_diario_obra.filter(id=0)
                else:
                    if len(cortes_diario_obra.filter(Q(persona__first_name__icontains=criterio) | Q(persona__last_name__icontains=criterio))) > 0:
                        cortes_diario_obra = cortes_diario_obra.filter(Q(persona__first_name__icontains=criterio) | Q(persona__last_name__icontains=criterio))
                    else:
                        #Busqueda por suministro
                        ids_cortes_diario_obra_excluir = []
                        for corte_diario_obra in cortes_diario_obra:
                            if len(corte_diario_obra.suministrocortediarioobra_set.filter(suministro__suministro_orden_servicio_item__suministro__nombre__icontains=criterio)) == 0:
                                ids_cortes_diario_obra_excluir.append(corte_diario_obra.id)
                        if len(ids_cortes_diario_obra_excluir) > 0:
                            cortes_diario_obra = cortes_diario_obra.exclude(id__in=ids_cortes_diario_obra_excluir)
        if estado != None:
            cortes_diario_obra = cortes_diario_obra.filter(estado=estado)
        if fecha_inicial != '' or fecha_final != '':
            cortes_diario_obra = cortes_diario_obra.order_by('fecha_corte')
        else:
            cortes_diario_obra = cortes_diario_obra.order_by('orden_servicio__consecutivo', 'consecutivo')
        return cortes_diario_obra

    def lista_actas_recibo_obra(self, criterio='', estado=None, fecha_inicial='', fecha_final='', estado_registro=2):
        import re
        actas_recibo_obra = ActaReciboObra.objects.filter(orden_servicio__proyecto=self)
        if fecha_inicial != '':
            actas_recibo_obra = actas_recibo_obra.filter(fecha_acta__gt=fecha_inicial + ' 00:00:00')
        if fecha_final != '':
            actas_recibo_obra = actas_recibo_obra.filter(fecha_acta__lt=fecha_final + ' 23:59:59')
        if criterio != '':
            #Realiza la busqueda por codificación (ARO#-##)
            patron = re.compile('^ARO[0-9]+\-[0-9]+$', re.IGNORECASE)
            resultado = patron.search(criterio)
            if resultado != None:
                criterio = criterio.split('-')
                proyecto_id = criterio[0][3:]
                if self.id == int(proyecto_id):
                    actas_recibo_obra = actas_recibo_obra.filter(consecutivo=criterio[1])
                else:
                    actas_recibo_obra = actas_recibo_obra.filter(id=0)
            #Si la busqueda no es por codificación (ARO#-##)
            else:
                #Realiza la busqueda por codificación (OS#-##)
                patron = re.compile('^OS[0-9]+\-[0-9]+$', re.IGNORECASE)
                resultado = patron.search(criterio)
                if resultado != None:
                    criterio = criterio.split('-')
                    proyecto_id = criterio[0][2:]
                    if self.id == int(proyecto_id):
                        actas_recibo_obra = actas_recibo_obra.filter(orden_servicio__consecutivo=criterio[1])
                    else:
                        actas_recibo_obra = actas_recibo_obra.filter(id=0)
                #Si la busqueda no es por codificación (OS#-##)
                else:
                    if len(actas_recibo_obra.filter(Q(orden_servicio__proveedor__razon_social__icontains=criterio) | Q(orden_servicio__tercero__razon_social__icontains=criterio))) > 0:
                        #Busqueda por proveedor o por tercero
                        actas_recibo_obra = actas_recibo_obra.filter(Q(orden_servicio__proveedor__razon_social__icontains=criterio) | Q(orden_servicio__tercero__razon_social__icontains=criterio))
                    else:
                        #Busqueda por suministro
                        ids_actas_recibo_obra_excluir = []
                        for acta_recibo_obra in actas_recibo_obra:
                            items_acta_recibo_obra = acta_recibo_obra.itemactareciboobra_set.all()
                            excluir_acta = True
                            for item_acta_recibo_obra in items_acta_recibo_obra:
                                if len(item_acta_recibo_obra.corte_diario_obra.suministrocortediarioobra_set.filter(suministro__suministro_orden_servicio_item__suministro__nombre__icontains=criterio)) > 0:
                                    excluir_acta = False
                            if excluir_acta == True:
                                ids_actas_recibo_obra_excluir.append(acta_recibo_obra.id)
                        if len(ids_actas_recibo_obra_excluir) > 0:
                            actas_recibo_obra = actas_recibo_obra.exclude(id__in=ids_actas_recibo_obra_excluir)
        if estado != None:
            actas_recibo_obra = actas_recibo_obra.filter(estado_acta=estado)
        actas_recibo_obra = actas_recibo_obra.filter(estado_registro_acta=estado_registro)
        if fecha_inicial != '' or fecha_final != '':
            actas_recibo_obra = actas_recibo_obra.order_by('fecha_acta')
        else:
            actas_recibo_obra = actas_recibo_obra.order_by('-consecutivo')
        return actas_recibo_obra

    def lista_ordenes_giro(self, criterio='', estado=None, fecha_inicial='', fecha_final=''):
        import re
        ordenes_giro = self.ordengiro_set.all()
        if fecha_inicial != '':
            ordenes_giro = ordenes_giro.filter(fecha_registro__gt=fecha_inicial + ' 00:00:00')
        if fecha_final != '':
            ordenes_giro = ordenes_giro.filter(fecha_registro__lt=fecha_final + ' 23:59:59')
        if criterio != '':
            #Realiza la busqueda por codificación (OG#-##)
            patron = re.compile('^OG[0-9]+\-[0-9]+$', re.IGNORECASE)
            resultado = patron.search(criterio)
            if resultado != None:
                criterio = criterio.split('-')
                proyecto_id = criterio[0][2:]
                if self.id == int(proyecto_id):
                    ordenes_giro = ordenes_giro.filter(consecutivo=criterio[1])
                else:
                    ordenes_giro = ordenes_giro.filter(id=0)
            #Si la busqueda no es por codificación (OG#-##)
            else:
                if len(ordenes_giro.filter(proveedor__razon_social__icontains=criterio)) > 0:
                    #Busqueda por proveedor
                    ordenes_giro = ordenes_giro.filter(proveedor__razon_social__icontains=criterio)
                else:
                    #Busqueda por suministro
                    ids_ordenes_giro_excluir = []
                    for orden_giro in ordenes_giro:
                        if len(orden_giro.itemordengiro_set.filter(descripcion__icontains=criterio)) == 0:
                            ids_ordenes_giro_excluir.append(orden_giro.id)
                    if len(ids_ordenes_giro_excluir) > 0:
                        ordenes_giro = ordenes_giro.exclude(id__in=ids_ordenes_giro_excluir)
        if estado != None:
            ordenes_giro = ordenes_giro.filter(estado=estado)
        if fecha_inicial != '' or fecha_final != '':
            ordenes_giro = ordenes_giro.order_by('fecha_registro')
        else:
            ordenes_giro = ordenes_giro.order_by('consecutivo')
        return ordenes_giro

    def lista_actas_conformidad(self, criterio='', fecha_inicial='', fecha_final=''):
        import re
        actas_conformidad = ActaConformidad.objects.filter(orden_giro__proyecto=self)
        if fecha_inicial != '':
            actas_conformidad = actas_conformidad.filter(fecha_registro__gt=fecha_inicial + ' 00:00:00')
        if fecha_final != '':
            actas_conformidad = actas_conformidad.filter(fecha_registro__lt=fecha_final + ' 23:59:59')
        if criterio != '':
            #Realiza la busqueda por codificación (AC#-##)
            patron = re.compile('^AC[0-9]+\-[0-9]+$', re.IGNORECASE)
            resultado = patron.search(criterio)
            if resultado != None:
                criterio = criterio.split('-')
                proyecto_id = criterio[0][2:]
                if self.id == int(proyecto_id):
                    actas_conformidad = actas_conformidad.filter(consecutivo=criterio[1])
                else:
                    actas_conformidad = actas_conformidad.filter(id=0)
            #Si la busqueda no es por codificación (AC#-##)
            else:
                #Realiza la busqueda por codificación (OG#-##)
                patron = re.compile('^OG[0-9]+\-[0-9]+$', re.IGNORECASE)
                resultado = patron.search(criterio)
                if resultado != None:
                    criterio = criterio.split('-')
                    proyecto_id = criterio[0][2:]
                    if self.id == int(proyecto_id):
                        actas_conformidad = actas_conformidad.filter(orden_giro__consecutivo=criterio[1])
                    else:
                        actas_conformidad = actas_conformidad.filter(id=0)
                #Si la busqueda no es por codificación (OG#-##)
                else:
                    if len(actas_conformidad.filter(orden_giro__proveedor__razon_social__icontains=criterio)) > 0:
                        #Busqueda por proveedor
                        actas_conformidad = actas_conformidad.filter(orden_giro__proveedor__razon_social__icontains=criterio)
                    else:
                        #Busqueda por suministro
                        ids_actas_conformidad_excluir = []
                        for acta_conformidad in actas_conformidad:
                            if len(acta_conformidad.itemactaconformidad_set.filter(item_orden_giro__descripcion__icontains=criterio)) == 0:
                                ids_actas_conformidad_excluir.append(acta_conformidad.id)
                        if len(ids_actas_conformidad_excluir) > 0:
                            actas_conformidad = actas_conformidad.exclude(id__in=ids_actas_conformidad_excluir)
        if fecha_inicial != '' or fecha_final != '':
            actas_conformidad = actas_conformidad.order_by('fecha_registro')
        else:
            actas_conformidad = actas_conformidad.order_by('consecutivo')
        return actas_conformidad

    def lista_facturas_ordenes_compra(self, criterio='', fecha_inicial='', fecha_final=''):
        import re
        facturas = self.facturaordencompra_set.all()
        if fecha_inicial != '':
            facturas = facturas.filter(fecha_registro__gt=fecha_inicial + ' 00:00:00')
        if fecha_final != '':
            facturas = facturas.filter(fecha_registro__lt=fecha_final + ' 23:59:59')
        if criterio != '':
            #Realiza la busqueda por codificación (FOC#-##)
            patron = re.compile('^FOC[0-9]+\-[0-9]+$', re.IGNORECASE)
            resultado = patron.search(criterio)
            if resultado != None:
                criterio = criterio.split('-')
                proyecto_id = criterio[0][3:]
                if self.id == int(proyecto_id):
                    facturas = facturas.filter(consecutivo=criterio[1])
                else:
                    facturas = facturas.filter(id=0)
            #Si la busqueda no es por codificación (FOC#-##)
            else:
                facturas = facturas.filter(Q(numero_factura=criterio) | Q(proveedor__razon_social__icontains=criterio))
        if fecha_inicial != '' or fecha_final != '':
            facturas = facturas.order_by('fecha_registro')
        else:
            facturas = facturas.order_by('consecutivo')
        return facturas

    def lista_apus_contienen_suministro(self, suministro_id, criterio=''):
        suministro = Suministro.objects.get(id=suministro_id)
        ids_apus = suministro.suministroapuproyecto_set.filter(apu_proyecto__proyecto=self, apu_proyecto__estado_apu=True).values('apu_proyecto_id').distinct('apu_proyecto_id')
        apus_proyecto = self.apuproyecto_set.filter(id__in=ids_apus)
        if criterio != '':
            apus_proyecto = apus_proyecto.filter(nombre_apu__icontains=criterio)
        return apus_proyecto

    def lista_requisiciones(self, tipo=None, estado=None, criterio='', fecha_inicial='', fecha_final=''):
        import re
        requisiciones = self.requisicion_set.all()
        if tipo != None:
            requisiciones = requisiciones.filter(tipo_requisicion__in=tipo)
        if estado != None:
            requisiciones = requisiciones.filter(estado__in=estado)
        if fecha_inicial != '':
            requisiciones = requisiciones.filter(fecha_creacion__gt=fecha_inicial + ' 00:00:00')
        if fecha_final != '':
            requisiciones = requisiciones.filter(fecha_creacion__lt=fecha_final + ' 23:59:59')
        if criterio != '':
            #Realiza la busqueda por codificación (RE#-##)
            patron = re.compile('^RE[0-9]+\-[0-9]+$', re.IGNORECASE)
            resultado = patron.search(criterio)
            if resultado != None:
                criterio = criterio.split('-')
                proyecto_id = criterio[0][2:]
                if self.id == int(proyecto_id):
                    requisiciones = requisiciones.filter(consecutivo=criterio[1])
                else:
                    requisiciones = requisiciones.filter(id=0)
            #Si la busqueda no es por codificación (RE#-##)
            else:
                #Busqueda por suministro
                ids_requisiciones_excluir = []
                for requisicion in requisiciones:
                    if len(requisicion.suministrorequisicion_set.filter(suministro__suministro__nombre__icontains=criterio)) == 0:
                        ids_requisiciones_excluir.append(requisicion.id)
                if len(ids_requisiciones_excluir) > 0:
                    requisiciones = requisiciones.exclude(id__in=ids_requisiciones_excluir)
        if fecha_inicial != '' or fecha_final != '':
            requisiciones = requisiciones.order_by('fecha_creacion', 'consecutivo')
        else:
            requisiciones = requisiciones.order_by('consecutivo')
        return requisiciones
    
    def lista_proveedores_ordenes_compra_en_ejecucion_por_facturar(self, criterio=''):
        proveedores = []
        ordenes_compra = self.ordencompra_set.filter(estado=1)
        for orden_compra in ordenes_compra:
            if len(orden_compra.lista_informes_recepcion_por_facturar()) == 0:
                ordenes_compra = ordenes_compra.exclude(id=orden_compra.id)
        if criterio != '':
            try:
                criterio = int(criterio)
                ordenes_compra = ordenes_compra.filter(proveedor__identificacion=criterio)
            except :
                ordenes_compra = ordenes_compra.filter(proveedor__razon_social__icontains=criterio)
        for orden_compra in ordenes_compra:
            if not orden_compra.proveedor in proveedores:
                proveedores.append(orden_compra.proveedor)
        return proveedores

    def lista_ordenes_compra_en_ejecucion_por_facturar(self, criterio='', proveedor=None):
        import re
        ordenes_compra = self.ordencompra_set.filter(estado=1, proveedor=proveedor)
        for orden_compra in ordenes_compra:
            if len(orden_compra.lista_informes_recepcion_por_facturar()) == 0:
                ordenes_compra = ordenes_compra.exclude(id=orden_compra.id)
        if criterio != '':
            #Realiza la busqueda por codificación (OC#-##)
            patron = re.compile('^OC[0-9]+\-[0-9]+$', re.IGNORECASE)
            resultado = patron.search(criterio)
            if resultado != None:
                criterio = criterio.split('-')
                proyecto_id = criterio[0][2:]
                if self.id == int(proyecto_id):
                    ordenes_compra = ordenes_compra.filter(consecutivo=criterio[1])
                else:
                    ordenes_compra = ordenes_compra.filter(id=0)
            #Si la busqueda no es por codificación (OC#-##)
            else:
                ordenes_compra = ordenes_compra.filter(id=0)
        return ordenes_compra

    #Lista de secciones del proyecto
    def lista_secciones(self):
        return self.seccionproyecto_set.all()

    #Lista de inmuebles del proyecto
    def lista_inmuebles(self, orden=None):
        if orden == None:
            orden = 'identificacion'
        return self.inmueble_set.filter(estado_registro=True).order_by(orden)

    #Lista de agrupaciones del proyecto
    def lista_agrupaciones_inmueble(self, criterio='', orden=None):
        agrupaciones_inmueble = self.agrupacioninmueble_set.filter(estado_registro=True)
        if criterio != '':
            agrupaciones_inmueble = agrupaciones_inmueble.filter(identificacion__icontains=criterio)
        if orden == None:
            orden = 'identificacion'
        agrupaciones_inmueble = agrupaciones_inmueble.order_by(orden)
        return agrupaciones_inmueble

    #Lista de adicionales a contratos de venta registrados en proyecto
    def lista_tipos_adicionales_agrupaciones_inmueble(self, criterio=''):
        tipos_adicionales_agrupaciones_inmueble = self.adicionalagrupacion_set.filter(item_adicional=False, nombre__icontains=criterio)
        return tipos_adicionales_agrupaciones_inmueble

    #Lista de adicionales a contratos de venta registrados en proyecto
    def lista_adicionales_agrupaciones_inmueble(self, tipo_adicional=None, criterio=''):
        adicionales_agrupaciones_inmueble = AdicionalAgrupacion.objects.filter(Q(item_adicional=True) & Q(nombre__icontains=criterio) & (Q(proyecto=self) | Q(tipo_adicional__proyecto=self)))
        if tipo_adicional != None:
            adicionales_agrupaciones_inmueble = adicionales_agrupaciones_inmueble.filter(tipo_adicional=tipo_adicional)
        return adicionales_agrupaciones_inmueble

    # Lista solo los contratos que pasaron de reserva a separados
    def lista_contratos(self, estado_contrato=None, criterio=''):
        contratos_venta = self.contratoventa_set.filter(estado_registro=True)
        if estado_contrato != None:
            for contrato_venta in contratos_venta:
                if not contrato_venta.estadocontratoventa_set.filter(estado_contrato=estado_contrato, estado_registro=True):
                    contratos_venta = contratos_venta.exclude(id=contrato_venta.id)
        if criterio != '':
            if len(contratos_venta.filter(identificacion=criterio)) > 0:
                contratos_venta = contratos_venta.filter(identificacion__icontains=criterio)
            else:
                ids_contratos_venta_busqueda_cliente = []
                for contrato_venta in contratos_venta:
                    if len(contrato_venta.clientecontratoventa_set.filter(Q(cliente__nombre_1__icontains=criterio) | Q(cliente__nombre_2__icontains=criterio) | Q(cliente__apellido_1__icontains=criterio) | Q(cliente__apellido_2__icontains=criterio))) > 0:
                        ids_contratos_venta_busqueda_cliente.append(contrato_venta.id)
                contratos_venta = contratos_venta.filter(id__in=ids_contratos_venta_busqueda_cliente)
        return contratos_venta

    def str_apertura_fiducuenta(self):
        from django.utils.safestring import mark_safe
        from django.utils.text import normalize_newlines
        str_apertura_fiducuenta = ''
        if self.apertura_fiducuenta:
            str_apertura_fiducuenta = normalize_newlines(self.apertura_fiducuenta)
            str_apertura_fiducuenta = mark_safe(str_apertura_fiducuenta.replace('\n', '<br />'))
        return str_apertura_fiducuenta

    def str_carta_instrucciones(self):
        from django.utils.safestring import mark_safe
        from django.utils.text import normalize_newlines
        str_carta_instrucciones = ''
        if self.carta_instrucciones:
            str_carta_instrucciones = normalize_newlines(self.carta_instrucciones)
            str_carta_instrucciones = mark_safe(str_carta_instrucciones.replace('\n', '<br />'))
        return str_carta_instrucciones

    def str_promesa_compraventa(self):
        from django.utils.safestring import mark_safe
        from django.utils.text import normalize_newlines
        str_promesa_compraventa = ''
        if self.promesa_compraventa:
            str_promesa_compraventa = normalize_newlines(self.promesa_compraventa)
            str_promesa_compraventa = mark_safe(str_promesa_compraventa.replace('\n', '<br />'))
            str_promesa_compraventa = mark_safe(str_promesa_compraventa.replace('**', '<strong>'))
            str_promesa_compraventa = mark_safe(str_promesa_compraventa.replace('--', '</strong>'))
        return str_promesa_compraventa

    #Lista de publicaciones en el proyecto
    def publications_list(self, number=None):
        if number == None:
            number = 20
        publications = self.publishedproject_set.all().order_by('-publication_date')
        if publications.count() > number and number > 0:
            publications = publications[:number]
        return publications

    #Funciones para el reporte de novedades
    def novedades_modulo_apus_proyecto(self):
        return 'novedadesapusproyecto.html'

    def novedades_modulo_requisiciones_proyecto(self):
        return 'novedadesrequisicion.html'

    def novedades_modulo_ordenes_compra_proyecto(self):
        return 'novedadesordencompra.html'

    def novedades_modulo_almacen_proyecto(self):
        return 'novedadesalmacen.html'

    def novedades_modulo_ordenes_servicio_proyecto(self):
        return 'novedadesordenservicio.html'

    def novedades_modulo_indirectos_proyecto(self):
        return 'novedadesindirectos.html'

    def novedades_modulo_facturacion_proyecto(self):
        return 'novedadesfacturacion.html'

    def novedades_modulo_reportes_proyecto(self):
        return ''

    def __unicode__(self):
        return unicode(self.nombre)

class PersonaProyecto(models.Model):
    identificacion = models.BigIntegerField()
    nombre = models.CharField(max_length=80)
    cargo = models.CharField(max_length=40)
    telefono = models.CharField(max_length=10)
    estado = models.BooleanField(default=True) # Estado = 1 Cuando esta activa en el proyecto, Estado = 2 Cuando esta inactiva en el proyecto
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_eliminacion = models.DateTimeField(auto_now=True)
    proveedor = models.ForeignKey(Proveedor) # Debe ser una persona (Proveedor) la cual anexa al proyecto la persona
    proyecto = models.ForeignKey(Proyecto)
    persona = models.ForeignKey(Usuario)

    class Meta:
        unique_together = ('identificacion', 'proyecto')


class PersonaAdministrativoProyecto(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_eliminacion = models.DateTimeField(auto_now=True)
    estado_registro = models.BooleanField(default=True) # Estado del registro 0 = Inactivo, 1 = Activo
    proyecto = models.ForeignKey(Proyecto)
    persona = models.ForeignKey(Usuario)

    class Meta:
        unique_together = ('proyecto', 'persona')


class CapituloApuProyecto(models.Model):
    codigo = models.SmallIntegerField()
    nombre_capitulo = models.CharField(max_length=40)
    tipo_capitulo = models.SmallIntegerField(max_length=1) # Capitulo ó subcapitulo
    estado_capitulo = models.BooleanField(default=True) # Activo ó inactivo
    capitulo_asociado = models.ForeignKey('self', null=True, blank=True) # Capitulo padre
    proyecto = models.ForeignKey(Proyecto)

    def __unicode__(self):
		return self.nombre_capitulo

    def subcapitulos(self):
        subcapitulos = False
        if len(CapituloApuProyecto.objects.filter(capitulo_asociado=self, estado_capitulo=True)) > 0:
            subcapitulos = True
        return subcapitulos

    def apus_proyecto(self):
        apus_proyecto = False
        if len(self.apuproyecto_set.filter(estado_apu=True)) > 0:
            apus_proyecto = True
        return apus_proyecto

    def lista_subcapitulos_activos(self):
        subcapitulos = self.capituloapuproyecto_set.filter(tipo_capitulo=2, estado_capitulo=True)
        return subcapitulos

    def lista_apus_proyecto_activos(self):
        apus_proyecto = self.apuproyecto_set.filter(estado_apu=True)
        return apus_proyecto

    def valor_apus_proyecto_capitulo(self):
        valor = 0
        #Sumatoria de los APU's correspondientes al capitulo
        for apu_proyecto in self.apuproyecto_set.filter(estado_apu=True):
            valor = round(decimal.Decimal(valor) + apu_proyecto.valor_total, 2)
        return valor

    def valor_total_capitulo(self):
        valor_total = 0
        for apu_proyecto in self.apuproyecto_set.filter(estado_apu=True):
            valor_total = round(decimal.Decimal(valor_total) + apu_proyecto.valor_total, 2)
        for subcapitulo in self.capituloapuproyecto_set.filter(estado_capitulo=True):
            for apu_proyecto in subcapitulo.apuproyecto_set.filter(estado_apu=True):
                valor_total = round(decimal.Decimal(valor_total) + apu_proyecto.valor_total, 2)
        return valor_total

    def porcentaje_sobre_valor_total_proyecto(self):
        porcentaje_sobre_valor_total_proyecto = round((self.valor_total_capitulo() * 100) / self.proyecto.valor_total_presupuesto_proyecto() , 2)
        return porcentaje_sobre_valor_total_proyecto

    def valor_total_comprado_contratado(self):
        valor_total_comprado_contratado= 0
        for apu_proyecto in self.apuproyecto_set.all():
            valor_total_comprado_contratado = valor_total_comprado_contratado + apu_proyecto.precio_ejecutado_ordenes_compra_ordenes_servicio()
        return valor_total_comprado_contratado

    def valor_total_facturado(self):
        valor_total_facturado= 0
        for apu_proyecto in self.apuproyecto_set.all():
            valor_total_facturado = valor_total_facturado + apu_proyecto.precio_facturado()
        return valor_total_facturado


class ApuProyecto(models.Model):
    nombre_apu = models.CharField(max_length=60)
    unidad_medida_apu = models.CharField(max_length=12)
    cantidad_proyecto = models.FloatField()
    cantidad_apu = models.FloatField()
    cantidad_total = models.DecimalField(max_digits=20, decimal_places=2)
    valor_unitario = models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)
    valor_total = models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)
    estado_apu = models.BooleanField(default=True) # Apu Activo ó inactivo
    pertenece_presupuesto = models.BooleanField(default=True) # Si el APU fue creado en el presupuesto el valor es True si no pertenece a una adición del presupuesto el valor es False
    apu_manejo_estandar = models.BooleanField()
    suministro_estandar = models.OneToOneField('SuministroApuProyecto', null=True, blank=True)
    proyecto = models.ForeignKey(Proyecto)
    capitulo = models.ForeignKey(CapituloApuProyecto)

    def actualizar_aproximacion_cantidad_suministros(self):
        suministros = self.suministroapuproyecto_set.filter(Q(suministro__clasificacion_general='Equipo') | Q(suministro__clasificacion_general='Mano de obra') | Q(suministro__clasificacion_general='Material') | Q(suministro__clasificacion_general='Transporte'))
        for suministro in suministros:
            suministro.actualizar_aproximacion_cantidad_suministro()

    def porcentaje_sobre_valor_total_proyecto(self):
        porcentaje_sobre_valor_total_proyecto = round((self.valor_total * 100) / self.proyecto.valor_total_presupuesto_proyecto(), 2)
        return porcentaje_sobre_valor_total_proyecto

    def lista_suministros(self, clasificacion_general=None):
        suministros_apu = self.suministroapuproyecto_set.all()
        if clasificacion_general != None:
            suministros_apu = suministros_apu.filter(suministro__clasificacion_general=clasificacion_general)
        else:
            suministros_apu = suministros_apu.filter(suministro__clasificacion_general='Material')
        return suministros_apu

    def valor_comprado(self):
        valor_comprado = 0

        for suministro in self.suministroapuproyecto_set.all():
            valor_comprado= valor_comprado + round(suministro.cantidad_comprada * suministro.precio_suministro)
        return valor_comprado

    def precio_ejecutado_ordenes_compra_ordenes_servicio(self):
        precio_ejecutado_ordenes_compra_ordenes_servicio = 0
        for suministro in self.suministroapuproyecto_set.all():
            precio_ejecutado_ordenes_compra_ordenes_servicio= precio_ejecutado_ordenes_compra_ordenes_servicio + suministro.precio_ejecutado_comprado_contratado()
        return precio_ejecutado_ordenes_compra_ordenes_servicio

    def precio_facturado(self):
        precio_facturado = 0
        for suministro in self.suministroapuproyecto_set.all():
            precio_facturado = precio_facturado + suministro.precio_facturado()
        return precio_facturado

    class Meta():
        verbose_name_plural = "01.1. Apu Proyecto" + str(settings.DATABASES)

class SuministroApuProyecto(models.Model):
    cantidad_suministro = models.FloatField()
    precio_suministro  = models.FloatField()
    precio_total = models.FloatField()
    cantidad_requerida = models.FloatField(default=0) # Cantidad actual en tiempo
    cantidad_total_requerida = models.FloatField(default=0) # Historial de la cantidad
    cantidad_comprada = models.FloatField(default=0) # Cantidad actual en tiempo
    cantidad_almacen = models.FloatField(default=0) # Cantidad actual en tiempo
    # Parametros de aproximación de consumo de materiales según Actas de obra
    aproximacion_cantidad_suministro = models.FloatField(default=0)
    pertenece_presupuesto = models.BooleanField(default=True) # Si el APU fue creado en el presupuesto el valor es True si no pertenece a una adición del presupuesto el valor es False
    suministro = models.ForeignKey(Suministro)
    apu_proyecto = models.ForeignKey(ApuProyecto)

    def cantidadDisponibleRequerir(self):
        cantidad_total_suministro = round(decimal.Decimal(self.cantidad_suministro) * self.apu_proyecto.cantidad_total, 2)
        return round(decimal.Decimal(cantidad_total_suministro) - decimal.Decimal(self.cantidad_total_requerida), 2)

    def cantidadTotalApuProyecto(self):
        return round(decimal.Decimal(self.cantidad_suministro) * self.apu_proyecto.cantidad_total, 2)

    def precioTotalApuProyecto(self):
        return round(self.cantidadTotalApuProyecto() * self.precio_suministro, 2)

    def actualizar_aproximacion_cantidad_suministro(self):
        self.aproximacion_cantidad_suministro = round((self.apu_proyecto.suministro_estandar.cantidad_almacen * self.cantidad_suministro) / self.apu_proyecto.suministro_estandar.cantidad_suministro, 2)
        self.save()

    def cantidad_salidas_almacen(self):
        cantidad_salidas_almacen = self.suministroinformesalida_set.all().aggregate(Sum('cantidad'))['cantidad__sum']
        if cantidad_salidas_almacen == None:
            cantidad_salidas_almacen = 0
        return cantidad_salidas_almacen

    def precio_ejecutado_ordenes_compra(self):
        precio_ejecutado_ordenes_compra = 0
        suministros_orden_compra = SuministroOrdenCompra.objects.filter(suministro__suministro=self)
        for suministro_orden_compra in suministros_orden_compra:
            precio_ejecutado_ordenes_compra = round(precio_ejecutado_ordenes_compra + round(round(suministro_orden_compra.cantidad_comprada * suministro_orden_compra.suministro_orden_compra_item.precio, 2) + round(suministro_orden_compra.cantidad_comprada * suministro_orden_compra.suministro_orden_compra_item.precio * suministro_orden_compra.suministro_orden_compra_item.iva_suministro, 2), 2), 2)
        return precio_ejecutado_ordenes_compra

    def precio_ejecutado_ordenes_servicio(self):
        precio_ejecutado_ordenes_servicio = 0
        suministros_orden_servicio = SuministroOrdenServicio.objects.filter(suministro__suministro=self)
        for suministro_orden_servicio in suministros_orden_servicio:
            precio_ejecutado_ordenes_servicio = round(precio_ejecutado_ordenes_servicio + round(round(suministro_orden_servicio.cantidad * suministro_orden_servicio.suministro_orden_servicio_item.precio, 2) + round(suministro_orden_servicio.cantidad * suministro_orden_servicio.suministro_orden_servicio_item.precio * suministro_orden_servicio.suministro_orden_servicio_item.iva_suministro, 2), 2), 2)
        return precio_ejecutado_ordenes_servicio

    def precio_ejecutado_ordenes_giro(self):
        precio_ejecutado_ordenes_giro = 0
        items_orden_giro = ItemOrdenGiro.objects.filter(suministro__suministro=self)
        for item_orden_giro in items_orden_giro:
            precio_ejecutado_ordenes_giro = round(precio_ejecutado_ordenes_giro + round(item_orden_giro.valor, 2) , 2)
        return precio_ejecutado_ordenes_giro

    def precio_ejecutado_comprado_contratado(self):
        precio_ejecutado_comprado_contratado = 0
        if self.suministro.clasificacion_general == 'Material':
            suministros_orden_compra = SuministroOrdenCompra.objects.filter(suministro__suministro=self)
            for suministro_orden_compra in suministros_orden_compra:
                precio_ejecutado_comprado_contratado = round(precio_ejecutado_comprado_contratado + round(round(suministro_orden_compra.cantidad_comprada * suministro_orden_compra.suministro_orden_compra_item.precio, 2) + round(suministro_orden_compra.cantidad_comprada * suministro_orden_compra.suministro_orden_compra_item.precio * suministro_orden_compra.suministro_orden_compra_item.iva_suministro, 2), 2), 2)

        elif self.suministro.clasificacion_general == 'Indirectos':
            items_orden_giro = ItemOrdenGiro.objects.filter(suministro__suministro=self)
            for item_orden_giro in items_orden_giro:
                precio_ejecutado_comprado_contratado = round(precio_ejecutado_comprado_contratado + round(item_orden_giro.valor, 2) , 2)

        else:
            suministros_orden_servicio = SuministroOrdenServicio.objects.filter(suministro__suministro=self)
            for suministro_orden_servicio in suministros_orden_servicio:
                precio_ejecutado_comprado_contratado = round(precio_ejecutado_comprado_contratado + round(round(suministro_orden_servicio.cantidad * suministro_orden_servicio.suministro_orden_servicio_item.precio, 2) + round(suministro_orden_servicio.cantidad * suministro_orden_servicio.suministro_orden_servicio_item.precio * suministro_orden_servicio.suministro_orden_servicio_item.iva_suministro, 2), 2), 2)

        return precio_ejecutado_comprado_contratado


    def precio_facturado(self):
        precio_facturado = 0
        if self.suministro.clasificacion_general == 'Material':
            suministros_factura_orden_compra = SuministroFacturaOrdenCompra.objects.filter(suministro_informe_recepcion__suministro__suministro__suministro =self)
            for suministro_factura_orden_compra in suministros_factura_orden_compra:
                precio_facturado = round(precio_facturado + round(round(suministro_factura_orden_compra.cantidad * suministro_factura_orden_compra.suministro_informe_recepcion.suministro.suministro_orden_compra_item.precio, 2) + round(suministro_factura_orden_compra.cantidad * suministro_factura_orden_compra.suministro_informe_recepcion.suministro.suministro_orden_compra_item.precio * suministro_factura_orden_compra.suministro_informe_recepcion.suministro.suministro_orden_compra_item.iva_suministro, 2), 2), 2)

        elif self.suministro.clasificacion_general == 'Indirectos':
            items_acta_conformidad = ItemActaConformidad.objects.filter(item_orden_giro__suministro__suministro=self)
            for item_acta_conformidad in items_acta_conformidad:
                precio_facturado = round(precio_facturado + round(item_acta_conformidad.valor, 2) , 2)

        else:
            suministros_corte_diario_obra = SuministroCorteDiarioObra.objects.filter(suministro__suministro__suministro=self)
            for suministro_corte_diario_obra in suministros_corte_diario_obra:
                precio_facturado = round(precio_facturado + round(round(suministro_corte_diario_obra.cantidad * suministro_corte_diario_obra.suministro.suministro_orden_servicio_item.precio, 2) + round(suministro_corte_diario_obra.cantidad * suministro_corte_diario_obra.suministro.suministro_orden_servicio_item.precio * suministro_corte_diario_obra.suministro.suministro_orden_servicio_item.iva_suministro, 2), 2), 2)
        return precio_facturado

    def apu_id_asociado(self):
        return self.apu_proyecto.id

    class Meta:
        verbose_name_plural = "01.2. Suministros Apu Proyecto"

class HistorialAdicionApuProyecto(models.Model):
    fecha_registro = models.DateTimeField(auto_now_add=True)
    cantidad_proyecto = models.FloatField(null=True, blank=True)
    cantidad_apu = models.FloatField(null=True, blank=True)
    apu_proyecto = models.ForeignKey(ApuProyecto)
    usuario = models.ForeignKey(Usuario)
    

class AdicionSuministroApuProyecto(models.Model):
    cantidad = models.FloatField()
    suministro = models.ForeignKey(SuministroApuProyecto)
    historial_adicion_apu_proyecto = models.ForeignKey(HistorialAdicionApuProyecto)

    class Meta:
        unique_together = ('historial_adicion_apu_proyecto', 'suministro')


        
class Requisicion(models.Model):
    consecutivo = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_arribo = models.DateField()
    estado = models.SmallIntegerField(default=1) # Estado de la requisicion: 0 - Anulada, 1 - Por aprobar, 2 - Aprobada (En ejecución), 3 - (Finalizada) sus items ya estan en almacen
    tipo_requisicion = models.SmallIntegerField(default=1) #Tipo_requisición = 1 - Todos los suministros excepto indirectos, 2 - Suministros indirectos
    proyecto = models.ForeignKey(Proyecto)
    persona = models.ForeignKey(Usuario)

    class Meta:
        unique_together = ('consecutivo', 'proyecto')
        verbose_name_plural = "02.1. Requisicion"

    def save(self):
        if self.consecutivo == None:
            'Get last value of Code and Number from database, and increment before save'
            consecutivo = self.proyecto.requisicion_set.all().aggregate(Max('consecutivo'))['consecutivo__max']
            if consecutivo == None:
                consecutivo = 1
            else:
                consecutivo = consecutivo + 1
            self.consecutivo = consecutivo
        super(Requisicion, self).save()

    #Lista de los suministros de la requisicion agrupados por suministro
    def get_suministros_agrupados(self):
        suministros = self.suministrorequisicion_set.all()
        suministros_requisicion = []
        for suministro in suministros:
            suministro_agregado = False
            for suministro_requisicion in suministros_requisicion:
                if suministro.suministro.suministro.id == suministro_requisicion.suministro.suministro.id:
                    suministro_requisicion.cantidad_requerida = round(suministro_requisicion.cantidad_requerida + suministro.cantidad_requerida, 2)
                    suministro_requisicion.cantidad_comprada = round(suministro_requisicion.cantidad_comprada + suministro.cantidad_comprada, 2)
                    suministro_requisicion.cantidad_almacen = round(suministro_requisicion.cantidad_almacen + suministro.cantidad_almacen, 2)
                    if suministro_requisicion.observaciones == '':
                        suministro_requisicion.observaciones = suministro.observaciones
                    else:
                        suministro_requisicion.observaciones = suministro_requisicion.observaciones + ', ' + suministro.observaciones
                    suministro_agregado = True
            if suministro_agregado == False:
                suministros_requisicion.append(suministro)
        return suministros_requisicion

    def actualizar_estado(self):
        if self.estado > 1:
            if len(self.suministrorequisicion_set.filter(cantidad_requerida__gt=F('cantidad_comprada'))) > 0 or len(self.suministrorequisicion_set.filter(cantidad_comprada__gt=F('cantidad_almacen'))) > 0:
                self.estado = 2
            else:
                self.estado = 3
            self.save()

    def str_tipo_requisicion(self):
        str_tipo_requisicion = ''
        #Si el tipo_requisicion = 1 retorna string con valor de suministros: Materiales, plenitareas
        if self.tipo_requisicion == 1:
            str_tipo_requisicion = 'Suministros'
        #Si el tipo_requisicion = 2 retorna string con valor de suministros indirectos
        elif self.tipo_requisicion == 2:
            str_tipo_requisicion = 'Indirectos'
        return str_tipo_requisicion

    def str_estado_requisicion(self):
        str_estado_requisicion = ''
        #Si el estado_requisicion = 0 - la requisicion se encuentra anulada
        if self.estado == 0:
            str_estado_requisicion = 'Anulada'
        #Si el tipo_requisicion = 1 - la requisicion se encuentra por aprobar
        elif self.estado == 1:
            str_estado_requisicion = 'Por aprobar'
        #Si el tipo_requisicion = 2 - la requisicion se encuentra aprobada
        elif self.estado == 2:
            str_estado_requisicion = 'Aprobada'
        #Si el tipo_requisicion = 2 - la requisicion se encuentra finalizada
        elif self.estado == 3:
            str_estado_requisicion = 'Finalizada'
        return str_estado_requisicion

    
class SuministroRequisicion(models.Model):
    suministro = models.ForeignKey(SuministroApuProyecto)
    cantidad_requerida = models.FloatField(default=0)
    cantidad_comprada = models.FloatField(default=0)
    cantidad_almacen = models.FloatField(default=0)
    observaciones = models.TextField()
    requisicion = models.ForeignKey(Requisicion)

    def cantidad_total_requerida_proyecto(self):
        cantidad_total_requerida = 0
        if self.suministro.suministro.clasificacion_general == 'Indirectos':
            cantidad_total_requerida = round(self.cantidad_requerida - self.cantidad_comprada, 2)
        else:
            from django.db.models import Sum
            cantidad_total_requerida = SuministroRequisicion.objects.filter(suministro__suministro__id=self.suministro.suministro.id, requisicion__proyecto=self.requisicion.proyecto).aggregate(Sum('cantidad_requerida'))
            cantidad_total_comprada = SuministroRequisicion.objects.filter(suministro__suministro__id=self.suministro.suministro.id, requisicion__proyecto=self.requisicion.proyecto).aggregate(Sum('cantidad_comprada'))
            cantidad_total_requerida = round(cantidad_total_requerida['cantidad_requerida__sum'] - cantidad_total_comprada['cantidad_comprada__sum'], 2)
        return cantidad_total_requerida

    def cantidad_total_comprada_proyecto(self):
        cantidad_total_comprada = 0
        if self.suministro.suministro.clasificacion_general == 'Indirectos':
            cantidad_total_comprada = self.cantidad_comprada
        else:
            from django.db.models import Sum
            cantidad_total_comprada = SuministroRequisicion.objects.filter(suministro__suministro__id=self.suministro.suministro.id, requisicion__proyecto=self.requisicion.proyecto).aggregate(Sum('cantidad_comprada'))['cantidad_comprada__sum']
        return cantidad_total_comprada

    def __unicode__(self):
        return "id=%s - sum=%s - requisicion_id=%s --- apu_proyecto_id=%s" % (self.id, unicode(self.suministro.suministro.nombre), self.requisicion.id, self.suministro.apu_proyecto.id)

    class Meta:
        verbose_name_plural = "02.2. Suministros Requisicion"


class Cotizacion(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    tipo = models.SmallIntegerField(max_length=1) # Tipo 1 = Orden de compra, Tipo = 2 orden de servicio
    proyecto = models.ForeignKey(Proyecto)
    proveedor = models.ForeignKey(Proveedor)
    persona = models.ForeignKey(Usuario)

    #Actualiza los precios de la cotizacion al precio de la ultima orden realizada (Solo en los suministros que contengan el precio = 0)
    def actualizar_precios_proveedor_uorden_compra(self):
        for suministro in self.suministrocotizacion_set.all():
            if suministro.precio == 0:
                suministro.precio_proveedor_uorden_compra()
                suministro.save()

    #Valor sin IVA de la cotización
    def subtotal(self):
        subtotal = 0
        suministros_cotizacion = self.suministrocotizacion_set.all()
        for suministro in suministros_cotizacion:
            subtotal = round(subtotal + round(suministro.cantidad_cotizada * suministro.precio, 2), 2)
        return subtotal

    #Valor del IVA
    def valor_iva(self):
        valor_iva = 0
        suministros_cotizacion = self.suministrocotizacion_set.all()
        for suministro in suministros_cotizacion:
            valor_iva = round(valor_iva + round(round(suministro.cantidad_cotizada * suministro.precio, 2) * suministro.iva_suministro, 2), 2)
        return valor_iva

    #Valor total de la cotización
    def valor_total(self):
        valor_total = self.subtotal() + self.valor_iva()
        return valor_total

class SuministroCotizacion(models.Model):
    cantidad_cotizada = models.FloatField(default=0)
    precio = models.FloatField(null=True, default=0, blank=True)
    iva_suministro = models.FloatField(default=0)
    observaciones = models.TextField(default='')
    suministro = models.ForeignKey(Suministro)
    cotizacion = models.ForeignKey(Cotizacion)

    def precio_proveedor_uorden_compra(self):
        try:
            suministros = SuministroOrdenCompraItem.objects.filter(suministro__id=self.suministro.id, orden_compra__proveedor=self.cotizacion.proveedor).order_by('-orden_compra__fecha_creacion')
            self.precio = suministros.__getitem__(0).precio
            self.iva_suministro = suministros.__getitem__(0).iva_suministro
        except:
            print 'Error precio suministro ultima orden de compra'

    def cantidad_total_requerida_suministro_proyecto(self):
        suministro = self.cotizacion.proyecto.get_suministros_pendientes_comprar_agrupados_suministro(suministro_id=self.suministro.id, tipo_cotizacion=self.cotizacion.tipo).pop()
        return suministro


class OrdenCompra(models.Model):
    consecutivo = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_arribo = models.DateField(null=True, blank=True)
    estado = models.SmallIntegerField(default=1) # Estado de la orden de compra: 0 - Anulada, 1 - En ejecución(En recepción - Facturación), 2 - Finalizada ó (Facturada)
    forma_pago = models.SmallIntegerField() # Formas de pago: 1=Credito, 2=Contra-entrega, 3=Anticipado, 4=%Anticipo
    porcentaje_anticipo = models.FloatField(null=True, blank=True)
    dias_credito = models.IntegerField(null=True, blank=True)
    observaciones = models.TextField()
    observaciones_registro = models.TextField()
    permiso_modificar = models.BooleanField(default=True)
    proyecto = models.ForeignKey(Proyecto)
    proveedor = models.ForeignKey(Proveedor)
    persona = models.ForeignKey(Usuario)

    class Meta:
        unique_together = ('consecutivo', 'proyecto')
        verbose_name_plural = "03.1. Ordenes de Compra"

    def save(self):
        if self.consecutivo == None:
            'Get last value of Code and Number from database, and increment before save'
            consecutivo = self.proyecto.ordencompra_set.all().aggregate(Max('consecutivo'))['consecutivo__max']
            if consecutivo == None:
                consecutivo = 1
            else:
                consecutivo = consecutivo + 1
            self.consecutivo = consecutivo

        if self.id == None:
            if self.forma_pago == 3 or self.forma_pago == 4:
                self.permiso_modificar = False

        super(OrdenCompra, self).save()

    #Lista los suministros de la orden de compra agrupados por suministro
    def get_suministros_agrupados_suministro(self):
        suministros = self.suministroordencompra_set.all()
        suministros_orden_compra = []
        for suministro in suministros:
            suministro_agregado = False
            for suministro_orden_compra in suministros_orden_compra:
                if suministro_orden_compra.suministro.suministro.suministro.id == suministro.suministro.suministro.suministro.id:
                    suministro_orden_compra.cantidad_comprada = round(suministro_orden_compra.cantidad_comprada + suministro.cantidad_comprada, 2)
                    suministro_orden_compra.cantidad_almacen = round(suministro_orden_compra.cantidad_almacen + suministro.cantidad_almacen, 2)
                    suministro_agregado = True
            if suministro_agregado == False:
                suministros_orden_compra.append(suministro)
        return suministros_orden_compra

    #Retorna el valor total del iva
    def valor_iva(self):
        suministros = self.get_suministros_agrupados_suministro()
        valor_total = 0
        for suministro in suministros:
            valor_total = round(valor_total + round(suministro.cantidad_comprada * suministro.suministro_orden_compra_item.precio, 2) * suministro.suministro_orden_compra_item.iva_suministro, 2)
        return  valor_total

    #Retorna el valor total omitiendo el iva de los suministros
    def valor_total_sin_iva(self):
        suministros = self.get_suministros_agrupados_suministro()
        valor_total = 0
        for suministro in suministros:
            valor_total = round(valor_total + round(suministro.cantidad_comprada * suministro.suministro_orden_compra_item.precio, 2), 2)
        return  valor_total

    #Retorna el valor total de la orden de compra
    def valor_total(self):
        valor_total = round(self.valor_total_sin_iva() + self.valor_iva(), 2)
        return  valor_total

    #Actualiza el estado de la orden de compra
    def actualizar_estado(self):
        orden_compra_facturada = True
        for suministro_orden_compra in self.suministroordencompra_set.all():
            cantidad_facturada = ItemFacturaOrdenCompra.objects.filter(suministro_informe_recepcion__suministro=suministro_orden_compra).aggregate(Sum('cantidad'))
            if cantidad_facturada != None:
                if cantidad_facturada < suministro_orden_compra.cantidad_total_comprada():
                    orden_compra_facturada = False
                    break
            else:
                orden_compra_facturada = False
                break
        if orden_compra_facturada == True:
            self.estado = 2
            self.save()

    def lista_informes_recepcion_por_facturar(self, criterio=''):
        import re
        informes_recepcion = self.informerecepcion_set.all()
        for informe_recepcion in informes_recepcion:
            if len(informe_recepcion.suministroinformerecepcion_set.filter(cantidad_facturada__lt=F('cantidad'))) == 0:
                informes_recepcion = informes_recepcion.exclude(id=informe_recepcion.id)
        if criterio != '':
            #Realiza la busqueda por codificación (IR#-##)
            patron = re.compile('^IR[0-9]+\-[0-9]+$', re.IGNORECASE)
            resultado = patron.search(criterio)
            if resultado != None:
                criterio = criterio.split('-')
                proyecto_id = criterio[0][2:]
                if self.proyecto.id == int(proyecto_id):
                    informes_recepcion = informes_recepcion.filter(consecutivo=criterio[1])
                else:
                    informes_recepcion = informes_recepcion.filter(id=0)
            #Si la busqueda no es por codificación (IR#-##)
            else:
                 informes_recepcion = informes_recepcion.filter(id=0)
        return informes_recepcion

    def permite_modificar(self):
        permite_modificar = False
        if len(self.informerecepcion_set.all()) == 0:
            permite_modificar = True
        return permite_modificar
    
    def permite_modificaciones(self):
        permite_modificaciones = False
        if len(self.informerecepcion_set.all()) == 0 and self.permiso_modificar:
            permite_modificaciones = True
        return permite_modificaciones


#Complemento del suministro orden de compra, en donde se registra el precio, el iva, y las observaciones del suministro agrupados por el suministro base
class SuministroOrdenCompraItem(models.Model):
    orden_compra = models.ForeignKey(OrdenCompra)
    suministro = models.ForeignKey(Suministro)
    precio = models.FloatField(default=0)
    iva_suministro = models.FloatField(default=0)
    observaciones = models.TextField(null=True, blank=True)
    
    class Meta:
        unique_together = ('orden_compra', 'suministro')
        verbose_name_plural = "03.2. Item Suministros Orden de Compra"

    def cantidad_comprada_item(self):
        cantidad_comprada = self.suministroordencompra_set.all().aggregate(Sum('cantidad_comprada'))['cantidad_comprada__sum']
        if cantidad_comprada == None:
            cantidad_comprada = 0
        return cantidad_comprada

    def cantidad_almacen_item(self):
        cantidad_almacen = self.suministroordencompra_set.all().aggregate(Sum('cantidad_almacen'))['cantidad_almacen__sum']
        if cantidad_almacen == None:
            cantidad_almacen = 0
        return cantidad_almacen

    def cantidad_facturada(self):
        cantidad_facturada = self.suministroordencompra_set.all().aggregate(Sum('cantidad_facturada'))['cantidad_facturada__sum']
        if cantidad_facturada == None:
            cantidad_facturada = 0
        return cantidad_facturada

    def cantidad_facturada_valor_facturado(self):
        cantidad_facturada = self.cantidad_facturada()
        subtotal_facturado = round(cantidad_facturada * self.precio, 2)
        iva_facturado = round(cantidad_facturada * self.precio * self.iva_suministro, 2)
        valor_facturado = round(subtotal_facturado + iva_facturado , 2)
        return cantidad_facturada, valor_facturado

    def __unicode__(self):
        return "id=%s - sum=%s --- orden_compra_id=%s" % (self.id, unicode(self.suministro.nombre), self.orden_compra.id)

#Suministros de la orden de compra
class SuministroOrdenCompra(models.Model):
    cantidad_comprada = models.FloatField(default=0)
    suministro_orden_compra_item = models.ForeignKey(SuministroOrdenCompraItem)
    cantidad_almacen = models.FloatField(default=0)
    cantidad_facturada = models.FloatField(default=0)
    suministro = models.ForeignKey(SuministroRequisicion)
    orden_compra = models.ForeignKey(OrdenCompra)
    
    def cantidad_total_comprada(self):
        from django.db.models import Sum
        cantidad_total_comprada = SuministroOrdenCompra.objects.filter(suministro__suministro__suministro__id=self.suministro.suministro.suministro.id, orden_compra=self.orden_compra).aggregate(Sum('cantidad_comprada'))
        return cantidad_total_comprada['cantidad_comprada__sum']
    
    def cantidad_total_recepcion(self):
        from django.db.models import Sum
        cantidad_total_recepcion = SuministroOrdenCompra.objects.filter(suministro__suministro__suministro__id=self.suministro.suministro.suministro.id, orden_compra=self.orden_compra).aggregate(Sum('cantidad_almacen'))
        return cantidad_total_recepcion['cantidad_almacen__sum']

    def __unicode__(self):
        return "id=%s - sum=%s - orden_compra_id=%s --- requisicion_id=%s" % (self.id, unicode(self.suministro.suministro.suministro.nombre), self.orden_compra.id, self.suministro.requisicion.id)

    class Meta:
        verbose_name_plural = "03.3. Suministros Orden de Compra"

class InformeRecepcion(models.Model):
    consecutivo = models.IntegerField()
    fecha_informe = models.DateTimeField(auto_now_add=True)
    numero_remision = models.CharField(max_length=30)
    observaciones = models.TextField()
    orden_compra = models.ForeignKey(OrdenCompra)
    persona = models.ForeignKey(Usuario)

    def save(self):
        if self.consecutivo == None:
            'Get last value of Code and Number from database, and increment before save'
            consecutivo = InformeRecepcion.objects.filter(orden_compra__proyecto=self.orden_compra.proyecto).aggregate(Max('consecutivo'))['consecutivo__max']
            if consecutivo == None:
                consecutivo = 1
            else:
                consecutivo = consecutivo + 1
            self.consecutivo = consecutivo
        super(InformeRecepcion, self).save()

    #Lista los suministros del informe de recepción agrupados por suministro
    def get_suministros_agrupados_suministro(self, criterio=''):
        suministros = self.suministroinformerecepcion_set.filter(suministro__suministro_orden_compra_item__suministro__nombre__icontains=criterio)
        suministros_informe_recepcion = []
        for suministro in suministros:
            suministro_agregado = False
            for suministro_informe_recepcion in suministros_informe_recepcion:
                if suministro_informe_recepcion.suministro.suministro.suministro.suministro.id == suministro.suministro.suministro.suministro.suministro.id:
                    suministro_informe_recepcion.cantidad = round(suministro_informe_recepcion.cantidad + suministro.cantidad, 2)
                    suministro_informe_recepcion.cantidad_facturada = round(suministro_informe_recepcion.cantidad_facturada + suministro.cantidad_facturada, 2)
                    suministro_agregado = True
            if suministro_agregado == False:
                suministros_informe_recepcion.append(suministro)
        return suministros_informe_recepcion

    #Retorna suministro del informe de recepción agrupado por suministro y discriminado por el mismo
    def get_suministro(self, suministro_id):
        suministros = self.suministroinformerecepcion_set.filter(suministro__suministro_orden_compra_item__suministro__id=suministro_id)
        suministro_informe_recepcion = SuministroInformeRecepcion()
        for suministro in suministros:
            if suministro_informe_recepcion == SuministroInformeRecepcion():
                suministro_informe_recepcion = suministro
            else:
                suministro_informe_recepcion.cantidad = round(suministro_informe_recepcion.cantidad + suministro.cantidad, 2)
                suministro_informe_recepcion.cantidad_facturada = round(suministro_informe_recepcion.cantidad_facturada + suministro.cantidad_facturada, 2)
        return suministro_informe_recepcion

    class Meta:
        verbose_name_plural = "04.1. Informes de recepcion"


class SuministroInformeRecepcion(models.Model):
    cantidad = models.FloatField(default=0)
    cantidad_facturada = models.FloatField(default=0)
    suministro = models.ForeignKey(SuministroOrdenCompra)
    informe_recepcion = models.ForeignKey(InformeRecepcion)

    #Discriminación de los capitulos afectados en el informe de recepción
    def get_discriminacion_capitulos_apus_proyecto(self):
        capitulos = []
        suministros_informe_recepcion = SuministroInformeRecepcion.objects.filter(suministro__suministro__suministro__suministro=self.suministro.suministro.suministro.suministro, informe_recepcion=self.informe_recepcion)
        for suministro_informe_recepcion in suministros_informe_recepcion:
            capitulo = suministro_informe_recepcion.suministro.suministro.suministro.apu_proyecto.capitulo
            if capitulo not in capitulos:
                capitulos.append(capitulo)
        return capitulos

    def __unicode__(self):
        return "id=%s - sum=%s - informe_recepcion_id=%s --- orden_compra_id=%s" % (self.id, unicode(self.suministro.suministro.suministro.suministro.nombre), self.informe_recepcion.id, self.suministro.orden_compra.id)

    class Meta:
        verbose_name_plural = "04.2. Suministros Informes de recepcion"

class SuministroAlmacen(models.Model):
    cantidad_total = models.FloatField(default=0)
    cantidad_actual = models.FloatField(default=0)
    suministro = models.ForeignKey(Suministro)
    proyecto = models.ForeignKey(Proyecto)

    class Meta:
         unique_together = (("suministro", "proyecto"),)

    def get_valor_precio_x_cantidad(self):
        precio = 0.0
        for suministro in self.suministro.suministroordencompraitem_set.all():
            precio = suministro.precio
        valor= self.cantidad_actual * precio
        return valor

    def __unicode__(self):
        return "id=%s - sum=%s - cantidaxprecio=%s proyecto=%s" % (self.id, unicode(self.suministro.nombre), self.get_valor_precio_x_cantidad(), self.proyecto)

        

class InformeSalida(models.Model):
    consecutivo = models.IntegerField()
    fecha_informe = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField()
    proyecto = models.ForeignKey(Proyecto)
    persona_proyecto = models.ForeignKey(PersonaProyecto)
    persona = models.ForeignKey(Usuario)

    class Meta:
        unique_together = (("consecutivo", "proyecto"),)
        verbose_name_plural = "05.1. Informes de salida"

    def save(self):
        if self.consecutivo == None:
            'Get last value of Code and Number from database, and increment before save'
            consecutivo = self.proyecto.informesalida_set.all().aggregate(Max('consecutivo'))['consecutivo__max']
            if consecutivo == None:
                consecutivo = 1
            else:
                consecutivo = consecutivo + 1
            self.consecutivo = consecutivo
        super(InformeSalida, self).save()


class SuministroInformeSalidaItem(models.Model):
    suministro_almacen = models.ForeignKey(SuministroAlmacen)
    informe_salida = models.ForeignKey(InformeSalida)

    class Meta:
        unique_together = (("suministro_almacen", "informe_salida"),)
        verbose_name_plural = "05.2. Item Suministros Informe de Salida"
        
    def cantidad(self):
        cantidad = self.suministroinformesalida_set.all().aggregate(Sum('cantidad'))['cantidad__sum']
        if cantidad == None:
            cantidad = 0
        return cantidad

    def __unicode__(self):
        return "id=%s - sum=%s" % (self.id, unicode(self.suministro_almacen.suministro.nombre))

class SuministroInformeSalida(models.Model):
    cantidad = models.FloatField()
    suministro_apu_proyecto = models.ForeignKey(SuministroApuProyecto)
    suministro_informe_salida_item = models.ForeignKey(SuministroInformeSalidaItem)

    class Meta:
        verbose_name_plural = "05.3. Suministros Informe de Salida"

    def __unicode__(self):
        return "id=%s - sum=%s" % (self.id, unicode(self.suministro_informe_salida_item.suministro_almacen.suministro.nombre))

class OrdenServicio(models.Model):
    consecutivo = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateField()
    fecha_extendida = models.DateField(null=True, blank=True)
    rete_ica = models.FloatField()
    rete_fuente = models.FloatField()
    forma_pago = models.SmallIntegerField() # Formas de pago: 2=Contra-entrega, 3=Cortes de obra, 4=Otro => Cual?
    parametro_pago = models.TextField(null=True, blank=True)
    amortizacion = models.FloatField()
    retencion_garantia = models.FloatField()
    porcentaje_a_i_u = models.FloatField(null=True, blank=True)
    porcentaje_utilidad = models.FloatField(null=True, blank=True)
    porcentaje_iva = models.FloatField(null=True, blank=True)
    observaciones = models.TextField()
    estado = models.SmallIntegerField(default=1) # Estado de la orden de servicio = 1 - Activa, 2 - Finalizada, 3 - Liquidada, 4 - Anulada
    aplica_cooperativa = models.BooleanField(default=False) # Campo para verificación en las actas de recibo de obra
    base_gravable_cooperativa = models.FloatField(default=0)
    porcentaje_iva_cooperativa = models.FloatField(default=0)
    tipo_iva = models.SmallIntegerField(null=True, blank=True) # Tipo_iva: Null - No aplica, 1 - IVA/Utilidad, 2 - porcentaje iva, 3 - IVA/AIU
    observaciones_registro = models.TextField(null=True, blank=True)
    permiso_modificar = models.BooleanField(default=True)
    proyecto = models.ForeignKey(Proyecto)
    proveedor = models.ForeignKey(Proveedor)
    tercero = models.ForeignKey('Proveedor', related_name='relacion_tercero', null=True, blank=True)
    persona = models.ForeignKey(Usuario)

    class Meta:
        unique_together = (("consecutivo", "proyecto"),)
        verbose_name_plural = "07.1. Orden de Servicio"

    def save(self):
        if self.consecutivo == None:
            'Get last value of Code and Number from database, and increment before save'
            consecutivo = self.proyecto.ordenservicio_set.all().aggregate(Max('consecutivo'))['consecutivo__max']
            if consecutivo == None:
                consecutivo = 1
            else:
                consecutivo = consecutivo + 1
            self.consecutivo = consecutivo

        if self.id == None:
            if float(self.amortizacion) > 0:
                self.permiso_modificar = False

        super(OrdenServicio, self).save()

    #Lista los suministros de la orden de compra agrupados por suministro
    def get_suministros_agrupados_suministro(self):
        suministros = self.suministroordenservicio_set.all()
        suministros_orden_servicio = []
        for suministro in suministros:
            suministro_agregado = False
            for suministro_orden_servicio in suministros_orden_servicio:
                if suministro_orden_servicio.suministro.suministro.suministro.id == suministro.suministro.suministro.suministro.id:
                    suministro_orden_servicio.cantidad = round(suministro_orden_servicio.cantidad + suministro.cantidad, 2)
                    suministro_orden_servicio.cantidad_entregada = round(suministro_orden_servicio.cantidad_entregada + suministro.cantidad_entregada, 2)
                    suministro_agregado = True
            if suministro_agregado == False:
                suministros_orden_servicio.append(suministro)
        return suministros_orden_servicio

    def calcular_valores(self):
        # Calcular el valor total de la orden de servicio
        suministros = self.get_suministros_agrupados_suministro()
        valor_total = 0
        for suministro in suministros:
            valor_total = round(valor_total + round(suministro.cantidad * suministro.suministro_orden_servicio_item.precio, 2), 2)
        self.str_valor_total = valor_total

        # Calcula el valor subtotal igual al valor total por default
        self.str_valor_subtotal = self.str_valor_total

        if self.tipo_iva != None:
            if self.tipo_iva == 1:
                # Calculo del valor costo directo
                porcentaje_costo_directo = 100 / (100 + self.porcentaje_a_i_u + ((self.porcentaje_iva / 100) * (self.porcentaje_utilidad)))
                self.str_valor_costo_directo = round(self.str_valor_total * porcentaje_costo_directo, 2)
                # calculo del valor aiu
                self.str_valor_aiu = round(self.str_valor_costo_directo * (self.porcentaje_a_i_u / 100), 2)
                # Calculo del valor utilidad
                self.str_valor_utilidad = round(self.str_valor_costo_directo * (self.porcentaje_utilidad / 100), 2)
                # Calculo del valor IVA
                self.str_valor_iva = round(self.str_valor_utilidad * (self.porcentaje_iva / 100), 2)
                # Calculo del valor subtotal
                self.str_valor_subtotal = round(self.str_valor_costo_directo + self.str_valor_aiu, 2)
            elif self.tipo_iva == 2:
                # Calculo del valor subtotal
                self.str_valor_subtotal = round(self.str_valor_total / (1 + (self.porcentaje_iva / 100)), 2)
                # Calculo del valor IVA
                self.str_valor_iva = round(self.str_valor_subtotal * (self.porcentaje_iva / 100), 2)
                # Calculo del valor IVA
                self.str_valor_iva = round(self.str_valor_subtotal * (self.porcentaje_iva / 100), 2)
            elif self.tipo_iva == 3:
                # Calculo del valor subtotal
                self.str_valor_subtotal = round(self.str_valor_total / (1 + ((self.porcentaje_a_i_u / 100) * (self.porcentaje_iva / 100))), 2)
                # Calculo del valor costo directo
                self.str_valor_costo_directo = round(self.str_valor_subtotal * (1 - (self.porcentaje_a_i_u / 100)), 2)
                # calculo del valor aiu
                self.str_valor_aiu = round(self.str_valor_subtotal * (self.porcentaje_a_i_u / 100), 2)
                # Calculo del valor IVA
                self.str_valor_iva = round(self.str_valor_subtotal * (self.porcentaje_a_i_u / 100) * (self.porcentaje_iva / 100), 2)

    # Retorna el tipo de iva (String)
    def str_tipo_iva(self):
        str_tipo_iva = ''
        if self.tipo_iva != None:
            if self.tipo_iva == 1:
                str_tipo_iva = 'IVA/Utilidad'
            if self.tipo_iva == 2:
                str_tipo_iva = '% IVA'
            if self.tipo_iva == 3:
                str_tipo_iva = 'IVA/AIU'
        return str_tipo_iva

    def permite_modificar(self):
        permite_modificar = False
        if len(self.actareciboobra_set.all()) == 0:
            permite_modificar = True
        return permite_modificar

    def permite_modificaciones(self):
        permite_modificaciones = True
        if self.amortizacion > 0 and (self.permiso_modificar == 0 or len(self.actareciboobra_set.all()) > 0):
            permite_modificaciones = False
        return permite_modificaciones

    def permite_modificar_propiedades(self):
        permite_modificar_propiedades = True
        if self.permite_modificaciones() == False or len(self.actareciboobra_set.all()) > 0:
            permite_modificar_propiedades = False
        return permite_modificar_propiedades

    def actualizar_estado(self):
        if len(self.suministroordenservicio_set.filter(cantidad_entregada__lt=F('cantidad'))) == 0:
            self.estado = 2
            self.save()

#Complemento del suministro orden de servicio, en donde se registra el precio, el iva, y las observaciones del suministro agrupados por el suministro base
class SuministroOrdenServicioItem(models.Model):
    orden_servicio = models.ForeignKey(OrdenServicio)
    suministro = models.ForeignKey(Suministro)
    precio = models.FloatField(default=0)
    iva_suministro = models.FloatField(default=0)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('orden_servicio', 'suministro')
        verbose_name_plural = "07.2. Item Suministros Orden de Servicio"

    def cantidad_total_contratada(self):
        from django.db.models import Sum
        cantidad_total_contratada = self.suministroordenservicio_set.all().aggregate(Sum('cantidad'))['cantidad__sum']
        if cantidad_total_contratada == None:
            cantidad_total_contratada = 0
        return cantidad_total_contratada

    def cantidad_total_entregada(self):
        from django.db.models import Sum
        cantidad_total_entregada = self.suministroordenservicio_set.all().aggregate(Sum('cantidad_entregada'))['cantidad_entregada__sum']
        if cantidad_total_entregada == None:
            cantidad_total_entregada = 0
        return cantidad_total_entregada

    def valor_sin_iva_item(self):
        valor_item = round(self.cantidad_total_contratada() * self.precio, 2)
        return valor_item

    def valor_iva_item(self):
        valor_iva = 0
        if self.iva_suministro > 0:
            valor_iva = round(self.valor_sin_iva_item() * self.iva_suministro , 2)
        return valor_iva
    
    def valor_total_item(self):
        valor_total = round(self.valor_sin_iva_item() + self.valor_iva_item(), 2)
        return valor_total

    def cantidad_facturada(self):
        cantidad_facturada = 0
        for suministro_orden_servicio in self.suministroordenservicio_set.all():
            cantidad_facturada_suministro = suministro_orden_servicio.suministrocortediarioobra_set.filter(corte_diario_obra__estado=False).aggregate(Sum('cantidad'))['cantidad__sum']
            if cantidad_facturada_suministro != None:
                cantidad_facturada = round(cantidad_facturada + cantidad_facturada_suministro, 2)
        return cantidad_facturada

    def cantidad_facturada_valor_facturado(self):
        cantidad_facturada = self.cantidad_facturada()
        if cantidad_facturada == None:
            a = 2
        valor_facturado = round(cantidad_facturada * self.precio , 2)
        return cantidad_facturada, valor_facturado

    def __unicode__(self):
        return "id=%s - sum=%s --- orden_servicio_id=%s" % (self.id, unicode(self.suministro.nombre), self.orden_servicio.id)

class SuministroOrdenServicio(models.Model):
    cantidad = models.FloatField(default=0) # Cantidad contratada
    suministro_orden_servicio_item = models.ForeignKey(SuministroOrdenServicioItem)
    cantidad_entregada = models.FloatField(default=0) # Cantidad entregada actualmente según cantidad contratada
    suministro = models.ForeignKey(SuministroRequisicion)
    orden_servicio = models.ForeignKey(OrdenServicio)

    class Meta:
        verbose_name_plural = "07.3. Suministros Orden de Servicio"

    def __unicode__(self):
        return "id=%s - sum=%s - orden_servicio_id=%s --- requisicion_id=%s" % (self.id, unicode(self.suministro.suministro.suministro.nombre), self.orden_servicio.id, self.suministro.requisicion.id)



class CorteDiarioObra(models.Model):
    consecutivo = models.IntegerField()
    fecha_corte = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True) # Estado corte de obra True = Activa, False = Finalizada o pagada (Ya se encuentra en Acta de recibo de obra)
    orden_servicio = models.ForeignKey(OrdenServicio)
    persona = models.ForeignKey(Usuario)

    def save(self):
        if self.consecutivo == None:
            'Get last value of Code and Number from database, and increment before save'
            consecutivo = CorteDiarioObra.objects.filter(orden_servicio__proyecto=self.orden_servicio.proyecto).aggregate(Max('consecutivo'))['consecutivo__max']
            if consecutivo == None:
                consecutivo = 1
            else:
                consecutivo = consecutivo + 1
            self.consecutivo = consecutivo
        super(CorteDiarioObra, self).save()

    def get_consecutivo(self):
        return 'CDO' + str(self.orden_servicio.proyecto.id) + '-' + str(self.consecutivo)

    def orden_servicio_id_asociado(self):
        return self.orden_servicio.id

    #Retorna suministro
    def get_suministro(self, suministro_id):
        suministros_corte_diario_obra = self.suministrocortediarioobra_set.filter(suministro__suministro_orden_servicio_item__suministro__id=suministro_id)
        suministro = SuministroCorteDiarioObra()
        for suministro_corte_diario_obra in suministros_corte_diario_obra:
            if suministro == SuministroCorteDiarioObra():
                suministro = suministro_corte_diario_obra
            else:
                suministro.cantidad = round(suministro.cantidad + suministro_corte_diario_obra.cantidad, 2)
        return suministro

    #Modifica la cantidad del corte diario de un suministro
    def modificar_cantidad_suministro(self, suministro_id, cantidad):
        suministro_corte_diario_obra = self.get_suministro(suministro_id)
        if cantidad < suministro_corte_diario_obra.cantidad:
            if cantidad == 0:
                suministros_corte_diario_obra = self.suministrocortediarioobra_set.filter(suministro__suministro_orden_servicio_item__suministro__id=suministro_id)
                for suministro_corte_diario_obra in suministros_corte_diario_obra:
                    #Actualiza las cantidades en suministro_orden_compra, suministro_requisición y suministro APU proyecto
                    #Suministro orden de servicio
                    suministro_corte_diario_obra.suministro.cantidad_entregada = round(suministro_corte_diario_obra.suministro.cantidad_entregada - suministro_corte_diario_obra.cantidad, 2)
                    suministro_corte_diario_obra.suministro.save()
                    #Suministro Requisición
                    suministro_corte_diario_obra.suministro.suministro.cantidad_almacen = round(suministro_corte_diario_obra.suministro.suministro.cantidad_almacen - suministro_corte_diario_obra.cantidad, 2)
                    suministro_corte_diario_obra.suministro.suministro.save()
                    #Suministro Apu proyecto
                    suministro_corte_diario_obra.suministro.suministro.suministro.cantidad_almacen = round(suministro_corte_diario_obra.suministro.suministro.suministro.cantidad_almacen - suministro_corte_diario_obra.cantidad, 2)
                    suministro_corte_diario_obra.suministro.suministro.suministro.save()
                    suministro_corte_diario_obra.delete()
                # Elimina el corte diario de obra si se eliminaron todos sus items
                if len(self.suministrocortediarioobra_set.all()) == 0:
                    self.delete()
            else:
                suministros_corte_diario_obra = self.suministrocortediarioobra_set.filter(suministro__suministro_orden_servicio_item__suministro__id=suministro_id)
                suma_items = 0
                ultimo_suministro_lista = SuministroCorteDiarioObra()
                for suministro_corte_diario_obra in suministros_corte_diario_obra:
                    if suma_items == 0:
                        suma_items = suministro_corte_diario_obra.cantidad
                        ultimo_suministro_lista = suministro_corte_diario_obra
                    else:
                        if suma_items > cantidad:
                            #Actualiza las cantidades en suministro_orden_compra, suministro_requisición y suministro APU proyecto
                            #Suministro orden de servicio
                            suministro_corte_diario_obra.suministro.cantidad_entregada = round(suministro_corte_diario_obra.suministro.cantidad_entregada - suministro_corte_diario_obra.cantidad, 2)
                            suministro_corte_diario_obra.suministro.save()
                            #Suministro Requisición
                            suministro_corte_diario_obra.suministro.suministro.cantidad_almacen = round(suministro_corte_diario_obra.suministro.suministro.cantidad_almacen - suministro_corte_diario_obra.cantidad, 2)
                            suministro_corte_diario_obra.suministro.suministro.save()
                            #Suministro Apu proyecto
                            suministro_corte_diario_obra.suministro.suministro.suministro.cantidad_almacen = round(suministro_corte_diario_obra.suministro.suministro.suministro.cantidad_almacen - suministro_corte_diario_obra.cantidad, 2)
                            suministro_corte_diario_obra.suministro.suministro.suministro.save()
                            suministro_corte_diario_obra.delete()
                        else:
                            suma_items = round(suma_items + suministro_corte_diario_obra.cantidad, 2)
                            ultimo_suministro_lista = suministro_corte_diario_obra
                        
                if suma_items > cantidad:
                    ultimo_suministro_lista.modificar_cantidad(round(suma_items - cantidad, 2))

    class Meta:
        verbose_name_plural = "08.1. Corte Diario de Obra"

class SuministroCorteDiarioObra(models.Model):
    cantidad = models.FloatField(default=0)
    suministro = models.ForeignKey(SuministroOrdenServicio)
    corte_diario_obra = models.ForeignKey(CorteDiarioObra)
    
    #Actualizar cantidad del suministro en corte diario de obra acta_recibo_obra_add
    def modificar_cantidad(self, cantidad):
        #Se actualzan todas las cantidades en cascada
        self.cantidad = round(self.cantidad - cantidad, 2)
        self.save()
        #Suministro orden de servicio
        self.suministro.cantidad_entregada = round(self.suministro.cantidad_entregada - cantidad, 2)
        self.suministro.save()
        #Suministro Requisición
        self.suministro.suministro.cantidad_almacen = round(self.suministro.suministro.cantidad_almacen - cantidad, 2)
        self.suministro.suministro.save()
        #Suministro Apu proyecto
        self.suministro.suministro.suministro.cantidad_almacen = round(self.suministro.suministro.suministro.cantidad_almacen - cantidad, 2)
        self.suministro.suministro.suministro.save()

    def __unicode__(self):
        return "id=%s - sum=%s - corte_diario_id=%s" % (self.id, unicode(self.suministro.suministro.suministro.suministro.nombre), self.corte_diario_obra.id)

    class Meta:
        verbose_name_plural = "08.2. Suministro Corte Diario de Obra"

ESTADO_ACTA_RECIBO_OBRA_ANULADA = 0
ESTADO_ACTA_RECIBO_OBRA_POR_APROBAR = 1
ESTADO_ACTA_RECIBO_OBRA_APROBADA = 2

ESTADO_ACTA_RECIBO_OBRA_CHOICES = (
    (ESTADO_ACTA_RECIBO_OBRA_ANULADA, u'Anulada'),
    (ESTADO_ACTA_RECIBO_OBRA_POR_APROBAR, u'Por aprobar'),
    (ESTADO_ACTA_RECIBO_OBRA_APROBADA, u'Aprobada'),
)

class ActaReciboObra(models.Model):
    consecutivo = models.IntegerField()
    fecha_acta = models.DateTimeField(auto_now_add=True)
    valor_cooperativa = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    observaciones_descuento = models.TextField()
    estado_acta = models.SmallIntegerField(default=1) #Estado acta: 1 - Se puede modificar el valor_cooperativa, 2 - Cerrada (No se puede modificar el valor_cooperativa)
    estado_registro_acta = models.PositiveSmallIntegerField(choices=ESTADO_ACTA_RECIBO_OBRA_CHOICES, default=1, null=True, blank=True, verbose_name=u'estado',)
    orden_servicio = models.ForeignKey(OrdenServicio)
    persona = models.ForeignKey(Usuario)
    numero_factura = models.CharField(max_length=40, null=True, blank=True)
    cerrado_numero_factura = models.BooleanField(default=False)
    observaciones = models.TextField(null=True, blank=True)

    def save(self):
        if self.consecutivo == None:
            'Get last value of Code and Number from database, and increment before save'
            consecutivo = ActaReciboObra.objects.filter(orden_servicio__proyecto=self.orden_servicio.proyecto).aggregate(Max('consecutivo'))['consecutivo__max']
            if consecutivo == None:
                consecutivo = 1
            else:
                consecutivo = consecutivo + 1
            self.consecutivo = consecutivo
        super(ActaReciboObra, self).save()

    def items_acta_recibo_obra(self):
        """Estructura de la lista de items para el acta de recibo de obra
            {'suministro': 1, 'cantidad': 1, 'registros': [{'fecha_registro': 'ff', 'cantidad': 1, 'registros': [{'id': 1, 'consecutivo': 'CDO#-##', 'usuario': 'us', 'cantidad': 1}]}]}

            Funcion compara_fechas_registro: Ordena los items según la fecha de registro
        """
        etiquetas_cabecera = []
        lista_items_acta_recibo_obra = []
        items_acta_recibo_obra = self.itemactareciboobra_set.all()
        for item_acta_recibo_obra in items_acta_recibo_obra:
            items_corte_diario = item_acta_recibo_obra.corte_diario_obra.suministrocortediarioobra_set.all()
            for item_corte_diario_obra in items_corte_diario:
                id = item_corte_diario_obra.id
                consecutivo = item_acta_recibo_obra.corte_diario_obra.get_consecutivo()
                suministro_base = item_corte_diario_obra.suministro.suministro.suministro.suministro
                fecha_registro = item_corte_diario_obra.corte_diario_obra.fecha_corte.strftime('%Y-%m-%d')
                usuario_registro = item_corte_diario_obra.corte_diario_obra.persona.full_name()
                cantidad = item_corte_diario_obra.cantidad
                item_adicionado = False
                for item_lista_acta_recibo_obra in lista_items_acta_recibo_obra:
                    if item_lista_acta_recibo_obra['suministro'].id == suministro_base.id:
                        for registro in item_lista_acta_recibo_obra['registros']:
                            if registro['fecha_registro'] == fecha_registro:
                                registro['registros'].append({'id': id, 'consecutivo': consecutivo, 'usuario': usuario_registro, 'cantidad': cantidad})
                                registro['cantidad'] = round(registro['cantidad'] + cantidad, 2)
                                item_adicionado = True
                        if not item_adicionado:
                            item_lista_acta_recibo_obra['registros'].append({'fecha_registro': fecha_registro, 'cantidad': cantidad, 'registros': [{'id': id, 'consecutivo': consecutivo, 'usuario': usuario_registro, 'cantidad': cantidad}]})
                            item_adicionado = True
                        item_lista_acta_recibo_obra['cantidad'] = round(item_lista_acta_recibo_obra['cantidad'] + cantidad, 2)
                if not item_adicionado:
                    lista_items_acta_recibo_obra.append({'suministro': suministro_base, 'cantidad': cantidad, 'registros': [{'fecha_registro': fecha_registro, 'cantidad': cantidad, 'registros': [{'id': id, 'consecutivo': consecutivo, 'usuario': usuario_registro, 'cantidad': cantidad}]}]})
                if not fecha_registro in etiquetas_cabecera:
                    etiquetas_cabecera.append(fecha_registro)
                    etiquetas_cabecera = sorted(etiquetas_cabecera)

        def compara_fechas_registro( x, y ) :
            # x e y son objetos de los que se desea ordenar
            if x['fecha_registro'] < y['fecha_registro'] :
                rst = -1
            elif x['fecha_registro'] > y['fecha_registro'] :
                rst = 1
            else :
                rst = 0
            return rst
        for item_lista_acta_recibo_obra in lista_items_acta_recibo_obra:
            item_lista_acta_recibo_obra['registros'].sort(compara_fechas_registro)

        etiquetas_cabecera = ['Suministro', 'Cantidad', 'U. medida'] + etiquetas_cabecera
        return {'etiquetas_cabecera': etiquetas_cabecera, 'lista_items': lista_items_acta_recibo_obra}

    def lista_items_acta_recibo_obra(self):
        items_acta_recibo_obra = self.itemactareciboobra_set.all()
        ids_cortes_diario_obra = []
        for item_acta_recibo_obra in items_acta_recibo_obra:
            ids_cortes_diario_obra.append(item_acta_recibo_obra.corte_diario_obra.id)
        suministros_cortes_diario_obra = SuministroCorteDiarioObra.objects.filter(corte_diario_obra__in=ids_cortes_diario_obra)
        suministros = []
        for suministro_cortes_diario_obra in suministros_cortes_diario_obra:
            suministro_agregado = False
            for suministro in suministros:
                if suministro.suministro.suministro.suministro.suministro.id == suministro_cortes_diario_obra.suministro.suministro.suministro.suministro.id:
                    suministro.cantidad = round(suministro.cantidad + suministro_cortes_diario_obra.cantidad, 2)
                    suministro_agregado = True
            if suministro_agregado == False:
                suministros.append(suministro_cortes_diario_obra)
        return suministros

    def str_estado(self):
        return ESTADO_ACTA_RECIBO_OBRA_CHOICES[self.estado_registro_acta][1]

    def permite_modificar(self):
        """Verifica que el acta se encuentre en estado 1 (Por aprobar)
        """
        if self.estado_registro_acta == 1:
            return True
        return False

    def permite_imprimir(self):
        """Verifica que el acta no se encuentre en estado 1 (Por aprobar)
        """
        if self.estado_registro_acta != 1:
            return True
        return False

    def calcular_valores(self, opcion_discriminacion_capitulos=False, opcion_discriminacion_subcapitulos=False):

        # Suministros cortes diario obra que componen el acta de recibo de obra
        ids_cortes_diario_obra = self.itemactareciboobra_set.values('corte_diario_obra__id')
        suministros_corte_diario_obra = SuministroCorteDiarioObra.objects.filter(corte_diario_obra__id__in=ids_cortes_diario_obra)

        valor_corte = 0
        for suministro_corte_diario_obra in suministros_corte_diario_obra:
            valor_corte = round(valor_corte + (round(suministro_corte_diario_obra.cantidad * suministro_corte_diario_obra.suministro.suministro_orden_servicio_item.precio, 2)), 2)
        self.str_valor_corte = valor_corte

        # Calculo de los valores del acta de recibo de obra (Cooperativa - Proveedor)

        proporcion_cooperativa = self.valor_cooperativa / self.str_valor_corte
        proporcion_proveedor = 1 - proporcion_cooperativa

        self.str_valor_total_proveedor = round(self.str_valor_corte * proporcion_proveedor, 2)

        # Calcula el valor subtotal igual al valor total por default
        self.str_valor_subtotal_proveedor = self.str_valor_total_proveedor

        if self.orden_servicio.tipo_iva != None:
            if self.orden_servicio.tipo_iva == 1:
                # Calculo del valor costo directo
                porcentaje_costo_directo = 100 / (100 + self.orden_servicio.porcentaje_a_i_u + ((self.orden_servicio.porcentaje_iva / 100) * (self.orden_servicio.porcentaje_utilidad)))
                self.str_valor_costo_directo_proveedor = round(self.str_valor_total_proveedor * porcentaje_costo_directo, 2)
                # calculo del valor aiu
                self.str_valor_aiu_proveedor = round(self.str_valor_costo_directo_proveedor * (self.orden_servicio.porcentaje_a_i_u / 100), 2)
                # Calculo del valor utilidad
                self.str_valor_utilidad_proveedor = round(self.str_valor_costo_directo_proveedor * (self.orden_servicio.porcentaje_utilidad / 100), 2)
                # Calculo del valor IVA
                self.str_valor_iva_proveedor = round(self.str_valor_utilidad_proveedor * (self.orden_servicio.porcentaje_iva / 100), 2)
                # Calculo del valor subtotal
                self.str_valor_subtotal_proveedor = round(self.str_valor_costo_directo_proveedor + self.str_valor_aiu_proveedor, 2)
            elif self.orden_servicio.tipo_iva == 2:
                # Calculo del valor subtotal
                self.str_valor_subtotal_proveedor = round(self.str_valor_total_proveedor / (1 + (self.orden_servicio.porcentaje_iva / 100)), 2)
                # Calculo del valor IVA
                self.str_valor_iva_proveedor = round(self.str_valor_subtotal_proveedor * (self.orden_servicio.porcentaje_iva / 100), 2)
            elif self.orden_servicio.tipo_iva == 3:
                # Calculo del valor subtotal
                self.str_valor_subtotal_proveedor = round(self.str_valor_total_proveedor / (1 + ((self.orden_servicio.porcentaje_a_i_u / 100) * (self.orden_servicio.porcentaje_iva / 100))), 2)
                # Calculo del valor costo directo
                self.str_valor_costo_directo_proveedor = round(self.str_valor_subtotal_proveedor * (1 - (self.orden_servicio.porcentaje_a_i_u / 100)), 2)
                # calculo del valor aiu
                self.str_valor_aiu_proveedor = round(self.str_valor_subtotal_proveedor * (self.orden_servicio.porcentaje_a_i_u / 100), 2)
                # Calculo del valor IVA
                self.str_valor_iva_proveedor = round(self.str_valor_subtotal_proveedor * (self.orden_servicio.porcentaje_a_i_u / 100) * (self.orden_servicio.porcentaje_iva / 100), 2)

        # Calcula el valor anticipo
        self.str_valor_anticipo = round(self.str_valor_corte * (self.orden_servicio.amortizacion / 100), 2)

        # Calcula el valor retegarantia
        self.str_valor_retegarantia = round(self.str_valor_corte * (self.orden_servicio.retencion_garantia / 100), 2)

        # Calcula el valor rete_ica
        self.str_valor_reteica_proveedor = round(self.str_valor_subtotal_proveedor * (self.orden_servicio.rete_ica / 1000), 2)

        # Calcula el valor rete_fuente
        self.str_valor_retefuente_proveedor = round(self.str_valor_subtotal_proveedor * (self.orden_servicio.rete_fuente / 100), 2)

        # Calcula el neto a pagar al proveedor
        self.str_neto_pagar_proveedor = round(self.str_valor_corte - (self.valor_cooperativa + self.str_valor_anticipo + self.str_valor_retegarantia + self.str_valor_reteica_proveedor + self.str_valor_retefuente_proveedor + self.descuento), 2)

        # Suministros del acta de recibo de obra
        suministros = []

        # Seccion para discriminar los valores por capitulo
        discriminacion_capitulos = []
        discriminacion_subcapitulos = []
        existen_subcapitulos = False

        for suministro_corte_diario_obra in suministros_corte_diario_obra:
            # Agrupación de suministros
            suministro_agregado = False
            for suministro in suministros:
                if suministro.suministro.suministro.suministro.suministro.id == suministro_corte_diario_obra.suministro.suministro.suministro.suministro.id:
                    suministro.cantidad = round(suministro.cantidad + suministro_corte_diario_obra.cantidad, 2)
                    suministro.valor_item = round(suministro.cantidad * suministro_corte_diario_obra.suministro.suministro_orden_servicio_item.precio, 2)
                    suministro_agregado = True
            if suministro_agregado == False:
                suministro_corte_diario_obra.valor_item = round(suministro_corte_diario_obra.cantidad * suministro_corte_diario_obra.suministro.suministro_orden_servicio_item.precio, 2)
                suministros.append(suministro_corte_diario_obra)

            # Discriminación por capitulos
            if opcion_discriminacion_capitulos:
                # Calculo del porcentaje de costo directo
                if self.orden_servicio.tipo_iva != None:
                    if self.orden_servicio.tipo_iva == 1:
                        porcentaje_costo_directo_proveedor = 100 / (100 + self.orden_servicio.porcentaje_a_i_u + ((self.orden_servicio.porcentaje_iva / 100) * (self.orden_servicio.porcentaje_utilidad)))
                capitulo_suministro = suministro_corte_diario_obra.suministro.suministro.suministro.apu_proyecto.capitulo
                if capitulo_suministro.tipo_capitulo == 2:
                    capitulo_suministro = capitulo_suministro.capitulo_asociado
                    existen_subcapitulos = True
                existe_capitulo = False
                for capitulo in discriminacion_capitulos:
                    if capitulo['capitulo'].id == capitulo_suministro.id:
                        valor_total_capitulo = round(capitulo['valor_total_capitulo'] + (suministro_corte_diario_obra.cantidad * suministro_corte_diario_obra.suministro.suministro_orden_servicio_item.precio), 2)

                        valor_subtotal_cooperativa = round(valor_total_capitulo * proporcion_cooperativa, 2)
                        valor_base_gravable_cooperativa = round(valor_subtotal_cooperativa * (self.orden_servicio.base_gravable_cooperativa / 100), 2)
                        valor_iva_cooperativa = round(valor_base_gravable_cooperativa * (self.orden_servicio.porcentaje_iva_cooperativa / 100), 2)
                        valor_total_cooperativa = round(valor_subtotal_cooperativa + valor_iva_cooperativa, 2)

                        valor_total_proveedor = round(valor_total_capitulo * proporcion_proveedor, 2)
                        base_iva_proveedor = 0
                        valor_iva_proveedor = 0
                        valor_costo_directo_proveedor = 0
                        if self.orden_servicio.tipo_iva != None:
                            if self.orden_servicio.tipo_iva == 1:
                                valor_costo_directo_proveedor = round(valor_total_proveedor * porcentaje_costo_directo, 2)
                                base_iva_proveedor = round(valor_costo_directo_proveedor * (self.orden_servicio.porcentaje_utilidad / 100), 2)
                            elif self.orden_servicio.tipo_iva == 2:
                                base_iva_proveedor = round(valor_total_proveedor / (1 + (self.orden_servicio.porcentaje_iva / 100)), 2)
                            elif self.orden_servicio.tipo_iva == 3:
                                valor_costo_directo_proveedor = round((valor_total_proveedor / (1 + ((self.orden_servicio.porcentaje_a_i_u / 100) * (self.orden_servicio.porcentaje_iva / 100)))) * ( 1 - (self.orden_servicio.porcentaje_a_i_u / 100)), 2)
                                base_iva_proveedor = round((valor_total_proveedor / (1 + ((self.orden_servicio.porcentaje_a_i_u / 100) * (self.orden_servicio.porcentaje_iva / 100)))) * (self.orden_servicio.porcentaje_a_i_u / 100), 2)
                            valor_iva_proveedor = round(base_iva_proveedor * (self.orden_servicio.porcentaje_iva / 100), 2)

                        valor_subtotal_proveedor = valor_total_proveedor - valor_iva_proveedor

                        capitulo['valor_total_capitulo'] = valor_total_capitulo

                        capitulo['valor_subtotal_cooperativa'] = valor_subtotal_cooperativa
                        capitulo['valor_base_gravable_cooperativa'] = valor_base_gravable_cooperativa
                        capitulo['valor_iva_cooperativa'] = valor_iva_cooperativa
                        capitulo['valor_total_cooperativa'] = valor_total_cooperativa

                        capitulo['valor_total_proveedor'] = valor_total_proveedor
                        capitulo['valor_costo_directo_proveedor'] = valor_costo_directo_proveedor
                        capitulo['valor_subtotal_proveedor'] = valor_subtotal_proveedor
                        capitulo['base_iva_proveedor'] = base_iva_proveedor
                        capitulo['valor_iva_proveedor'] = valor_iva_proveedor

                        existe_capitulo = True
                if existe_capitulo == False:
                    valor_total_capitulo = round(suministro_corte_diario_obra.cantidad * suministro_corte_diario_obra.suministro.suministro_orden_servicio_item.precio, 2)

                    valor_subtotal_cooperativa = round(valor_total_capitulo * proporcion_cooperativa, 2)
                    valor_base_gravable_cooperativa = round(valor_subtotal_cooperativa * (self.orden_servicio.base_gravable_cooperativa / 100), 2)
                    valor_iva_cooperativa = round(valor_base_gravable_cooperativa * (self.orden_servicio.porcentaje_iva_cooperativa / 100), 2)
                    valor_total_cooperativa = round(valor_subtotal_cooperativa + valor_iva_cooperativa, 2)

                    valor_total_proveedor = round(valor_total_capitulo * proporcion_proveedor, 2)
                    base_iva_proveedor = 0
                    valor_iva_proveedor = 0
                    valor_costo_directo_proveedor = 0
                    if self.orden_servicio.tipo_iva != None:
                        if self.orden_servicio.tipo_iva == 1:
                            valor_costo_directo_proveedor = round(valor_total_proveedor * porcentaje_costo_directo, 2)
                            base_iva_proveedor = round(valor_costo_directo_proveedor * (self.orden_servicio.porcentaje_utilidad / 100), 2)
                        elif self.orden_servicio.tipo_iva == 2:
                            base_iva_proveedor = round(valor_total_proveedor / (1 + (self.orden_servicio.porcentaje_iva / 100)), 2)
                        elif self.orden_servicio.tipo_iva == 3:
                            valor_costo_directo_proveedor = round((valor_total_proveedor / (1 + ((self.orden_servicio.porcentaje_a_i_u / 100) * (self.orden_servicio.porcentaje_iva / 100)))) * ( 1 - (self.orden_servicio.porcentaje_a_i_u / 100)), 2)
                            base_iva_proveedor = round((valor_total_proveedor / (1 + ((self.orden_servicio.porcentaje_a_i_u / 100) * (self.orden_servicio.porcentaje_iva / 100)))) * (self.orden_servicio.porcentaje_a_i_u / 100), 2)
                        valor_iva_proveedor = round(base_iva_proveedor * (self.orden_servicio.porcentaje_iva / 100), 2)

                    valor_subtotal_proveedor = valor_total_proveedor - valor_iva_proveedor

                    discriminacion_capitulos.append({'capitulo': capitulo_suministro, 'valor_total_capitulo': valor_total_capitulo, 'valor_subtotal_cooperativa': valor_subtotal_cooperativa,
                                                     'valor_base_gravable_cooperativa': valor_base_gravable_cooperativa, 'valor_iva_cooperativa': valor_iva_cooperativa, 'valor_total_cooperativa': valor_total_cooperativa,
                                                     'valor_total_proveedor': valor_total_proveedor, 'valor_costo_directo_proveedor': valor_costo_directo_proveedor, 'valor_subtotal_proveedor': valor_subtotal_proveedor,
                                                     'base_iva_proveedor': base_iva_proveedor, 'valor_iva_proveedor': valor_iva_proveedor})

            # Discriminación por subcapitulos
            if opcion_discriminacion_subcapitulos:
                lista_variable = discriminacion_subcapitulos
                # Calculo del porcentaje de costo directo
                if self.orden_servicio.tipo_iva != None:
                    if self.orden_servicio.tipo_iva == 1:
                        porcentaje_costo_directo_proveedor = 100 / (100 + self.orden_servicio.porcentaje_a_i_u + ((self.orden_servicio.porcentaje_iva / 100) * (self.orden_servicio.porcentaje_utilidad)))
                capitulo_suministro = suministro_corte_diario_obra.suministro.suministro.suministro.apu_proyecto.capitulo
                subcapitulo_suministro = ''
                capitulo_asociado = ''

                # q sea discriminacion x subcapitulos mas no por capitulos
                if capitulo_suministro.tipo_capitulo == 2:
                    capitulo_suministro = capitulo_suministro
                    capitulo_asociado = capitulo_suministro.capitulo_asociado
                    #capitulo_suministro = capitulo_suministro.capitulo_asociado

                existe_capitulo = False

                for capitulo in discriminacion_subcapitulos:
                    if capitulo['capitulo'].id == capitulo_suministro.id :

                        valor_total_capitulo = round(capitulo['valor_total_capitulo'] + (suministro_corte_diario_obra.cantidad * suministro_corte_diario_obra.suministro.suministro_orden_servicio_item.precio), 2)
                        valor_subtotal_cooperativa = round(valor_total_capitulo * proporcion_cooperativa, 2)
                        valor_base_gravable_cooperativa = round(valor_subtotal_cooperativa * (self.orden_servicio.base_gravable_cooperativa / 100), 2)
                        valor_iva_cooperativa = round(valor_base_gravable_cooperativa * (self.orden_servicio.porcentaje_iva_cooperativa / 100), 2)
                        valor_total_cooperativa = round(valor_subtotal_cooperativa + valor_iva_cooperativa, 2)

                        valor_total_proveedor = round(valor_total_capitulo * proporcion_proveedor, 2)
                        base_iva_proveedor = 0
                        valor_iva_proveedor = 0
                        valor_costo_directo_proveedor = 0

                        if self.orden_servicio.tipo_iva != None:
                            if self.orden_servicio.tipo_iva == 1:
                                valor_costo_directo_proveedor = round(valor_total_proveedor * porcentaje_costo_directo, 2)
                                base_iva_proveedor = round(valor_costo_directo_proveedor * (self.orden_servicio.porcentaje_utilidad / 100), 2)
                            elif self.orden_servicio.tipo_iva == 2:
                                base_iva_proveedor = round(valor_total_proveedor / (1 + (self.orden_servicio.porcentaje_iva / 100)), 2)
                            elif self.orden_servicio.tipo_iva == 3:
                                valor_costo_directo_proveedor = round((valor_total_proveedor / (1 + ((self.orden_servicio.porcentaje_a_i_u / 100) * (self.orden_servicio.porcentaje_iva / 100)))) * ( 1 - (self.orden_servicio.porcentaje_a_i_u / 100)), 2)
                                base_iva_proveedor = round((valor_total_proveedor / (1 + ((self.orden_servicio.porcentaje_a_i_u / 100) * (self.orden_servicio.porcentaje_iva / 100)))) * (self.orden_servicio.porcentaje_a_i_u / 100), 2)
                            valor_iva_proveedor = round(base_iva_proveedor * (self.orden_servicio.porcentaje_iva / 100), 2)

                        valor_subtotal_proveedor = valor_total_proveedor - valor_iva_proveedor

                        capitulo['valor_total_capitulo'] = valor_total_capitulo

                        capitulo['valor_subtotal_cooperativa'] = valor_subtotal_cooperativa
                        capitulo['valor_base_gravable_cooperativa'] = valor_base_gravable_cooperativa
                        capitulo['valor_iva_cooperativa'] = valor_iva_cooperativa
                        capitulo['valor_total_cooperativa'] = valor_total_cooperativa

                        capitulo['valor_total_proveedor'] = valor_total_proveedor
                        capitulo['valor_costo_directo_proveedor'] = valor_costo_directo_proveedor
                        capitulo['valor_subtotal_proveedor'] = valor_subtotal_proveedor
                        capitulo['base_iva_proveedor'] = base_iva_proveedor
                        capitulo['valor_iva_proveedor'] = valor_iva_proveedor
                        existe_capitulo = True
                        
                if existe_capitulo == False:
                    valor_total_capitulo = round(suministro_corte_diario_obra.cantidad * suministro_corte_diario_obra.suministro.suministro_orden_servicio_item.precio, 2)

                    valor_subtotal_cooperativa = round(valor_total_capitulo * proporcion_cooperativa, 2)
                    valor_base_gravable_cooperativa = round(valor_subtotal_cooperativa * (self.orden_servicio.base_gravable_cooperativa / 100), 2)
                    valor_iva_cooperativa = round(valor_base_gravable_cooperativa * (self.orden_servicio.porcentaje_iva_cooperativa / 100), 2)
                    valor_total_cooperativa = round(valor_subtotal_cooperativa + valor_iva_cooperativa, 2)

                    valor_total_proveedor = round(valor_total_capitulo * proporcion_proveedor, 2)
                    base_iva_proveedor = 0
                    valor_iva_proveedor = 0
                    valor_costo_directo_proveedor = 0

                    if self.orden_servicio.tipo_iva != None:
                        if self.orden_servicio.tipo_iva == 1:
                            valor_costo_directo_proveedor = round(valor_total_proveedor * porcentaje_costo_directo, 2)
                            base_iva_proveedor = round(valor_costo_directo_proveedor * (self.orden_servicio.porcentaje_utilidad / 100), 2)
                        elif self.orden_servicio.tipo_iva == 2:
                            base_iva_proveedor = round(valor_total_proveedor / (1 + (self.orden_servicio.porcentaje_iva / 100)), 2)
                        elif self.orden_servicio.tipo_iva == 3:
                            valor_costo_directo_proveedor = round((valor_total_proveedor / (1 + ((self.orden_servicio.porcentaje_a_i_u / 100) * (self.orden_servicio.porcentaje_iva / 100)))) * ( 1 - (self.orden_servicio.porcentaje_a_i_u / 100)), 2)
                            base_iva_proveedor = round((valor_total_proveedor / (1 + ((self.orden_servicio.porcentaje_a_i_u / 100) * (self.orden_servicio.porcentaje_iva / 100)))) * (self.orden_servicio.porcentaje_a_i_u / 100), 2)
                        valor_iva_proveedor = round(base_iva_proveedor * (self.orden_servicio.porcentaje_iva / 100), 2)

                    valor_subtotal_proveedor = valor_total_proveedor - valor_iva_proveedor


                    discriminacion_subcapitulos.append({'capitulo': capitulo_suministro,'capitulo_asociado': capitulo_asociado, 'tipo_capitulo': capitulo_suministro.tipo_capitulo, 'valor_total_capitulo': valor_total_capitulo, 'valor_subtotal_cooperativa': valor_subtotal_cooperativa,
                                                     'valor_base_gravable_cooperativa': valor_base_gravable_cooperativa, 'valor_iva_cooperativa': valor_iva_cooperativa, 'valor_total_cooperativa': valor_total_cooperativa,
                                                     'valor_total_proveedor': valor_total_proveedor, 'valor_costo_directo_proveedor': valor_costo_directo_proveedor, 'valor_subtotal_proveedor': valor_subtotal_proveedor,
                                                     'base_iva_proveedor': base_iva_proveedor, 'valor_iva_proveedor': valor_iva_proveedor})

        self.suministros = suministros
        self.discriminacion_capitulos = discriminacion_capitulos
        self.discriminacion_subcapitulos = discriminacion_subcapitulos
        self.existen_subcapitulos = existen_subcapitulos
        
    def valor_corte(self):
        valor_corte = 0
        suministros = self.lista_items_acta_recibo_obra()
        for suministro in suministros:
            valor_corte = round(valor_corte + (round(suministro.cantidad * suministro.suministro.suministro_orden_servicio_item.precio, 2)), 2)
        self.str_valor_corte = valor_corte
        return valor_corte

    def valor_anticipo(self):
        valor_corte = None
        try:
            valor_corte = self.str_valor_corte
        except :
            pass
        if valor_corte == None:
            valor_corte = self.valor_corte()
        valor_anticipo = round(valor_corte * (self.orden_servicio.amortizacion / 100), 2)
        return valor_anticipo

    def valor_retegarantia(self):
        valor_retegarantia = round(self.str_valor_corte * (self.orden_servicio.retencion_garantia / 100), 2)
        return valor_retegarantia

    # Total a facturar
    def valor_proveedor(self):
        valor_proveedor = round(self.str_valor_corte - self.valor_cooperativa, 2)
        return valor_proveedor

    # Los datos a continuación relacionados se desprenden del valor_proveedor
    def costo_directo_proveedor(self):
        costo_directo = 0
        if self.orden_servicio.tipo_iva == 1 or self.orden_servicio.tipo_iva == 3:
            costo_directo = round(self.valor_proveedor() * self.orden_servicio.porcentaje_costo_directo(), 2)
        elif self.orden_servicio.tipo_iva == 2:
            costo_directo = round(self.valor_proveedor() / (1 + (self.orden_servicio.porcentaje_iva / 100)), 2)
        return costo_directo

    def valor_aiu_proveedor(self):
        aiu = round(self.costo_directo_proveedor() * (self.orden_servicio.porcentaje_a_i_u / 100), 2)
        return aiu

    def valor_utilidad_proveedor(self):
        utilidad = round(self.costo_directo_proveedor() * (self.orden_servicio.porcentaje_utilidad / 100), 2)
        return utilidad

    def valor_iva_proveedor(self):
        valor_iva = 0
        if self.orden_servicio.proveedor.regimen_tributario == 1:
            if self.orden_servicio.tipo_iva == 1:
                valor_iva = round(self.valor_utilidad_proveedor() * (self.orden_servicio.porcentaje_iva / 100), 2)
            elif self.orden_servicio.tipo_iva == 2:
                valor_iva = round(self.costo_directo_proveedor() * (self.orden_servicio.porcentaje_iva / 100), 2)
            if self.orden_servicio.tipo_iva == 3:
                valor_iva = round(self.valor_aiu_proveedor() * (self.orden_servicio.porcentaje_iva / 100), 2)
        return valor_iva

    def valor_reteica(self):
        valor_reteica = round((self.valor_proveedor() - self.valor_iva_proveedor()) * (self.orden_servicio.rete_ica / 1000), 2)
        return valor_reteica

    def valor_retefuente(self):
        valor_retefuente = round((self.valor_proveedor() - self.valor_iva_proveedor()) * (self.orden_servicio.rete_fuente / 100), 2)
        return valor_retefuente

    def neto_pagar_proveedor(self):
        neto_pagar = round(self.str_valor_corte - (self.valor_cooperativa + self.valor_anticipo() + self.valor_retegarantia() + self.valor_reteica() + self.valor_retefuente() + self.descuento), 2)
        return neto_pagar

    def valor_maximo_cooperativa(self):
        # Valor Minimo para el proveedor
        base_minimo_proveedor = self.descuento + self.valor_anticipo() + self.valor_retegarantia()
        base_minimo_proveedor = base_minimo_proveedor + (base_minimo_proveedor * self.orden_servicio.rete_fuente / 100) + (base_minimo_proveedor * self.orden_servicio.rete_ica / 1000)
        valor_maximo_cooperativa = round(self.str_valor_corte - (base_minimo_proveedor + ((base_minimo_proveedor * (self.orden_servicio.rete_fuente / 100)) + (base_minimo_proveedor * (self.orden_servicio.rete_ica / 1000)))), 2)
        return valor_maximo_cooperativa

    def orden_servicio_id_asociado(self):
        return self.orden_servicio.id

    class Meta:
        verbose_name_plural = "09.1. Acta Recibo de Obra"
    
class ItemActaReciboObra(models.Model):
    corte_diario_obra = models.ForeignKey(CorteDiarioObra)
    acta_recibo_obra = models.ForeignKey(ActaReciboObra)

    class Meta:
        verbose_name_plural = "09.2. Item Acta Recibo de Obra"

    def __unicode__(self):
        return "id=%s  - acta_recibo_id=%s --- corte_diario_id=%s" % (self.id, self.acta_recibo_obra.id, self.corte_diario_obra.id)


class OrdenGiro(models.Model):
    consecutivo = models.IntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    estado = models.SmallIntegerField(default=1) #Estado de la orden de giro = 1-Creada
    proyecto = models.ForeignKey(Proyecto)
    proveedor = models.ForeignKey(Proveedor)
    persona = models.ForeignKey(Usuario)
    class Meta:
        unique_together = (("consecutivo", "proyecto"),)
        verbose_name_plural = "10.1. Orden de Giro"

    def save(self):
        if self.consecutivo == None:
            'Get last value of Code and Number from database, and increment before save'
            consecutivo = self.proyecto.ordengiro_set.all().aggregate(Max('consecutivo'))['consecutivo__max']
            if consecutivo == None:
                consecutivo = 1
            else:
                consecutivo = consecutivo + 1
            self.consecutivo = consecutivo
        super(OrdenGiro, self).save()

    #Calcula el valor total de la orden de giro
    def valor_total(self):
        valor_total = 0
        for item in self.itemordengiro_set.all():
            valor_total = round(valor_total + item.valor, 2)
        return valor_total

    #Actualiza el estado de la orden de giro de 1 - Creada a 2 - Pagada(Actas de conformidad)
    def actualizar_estado(self):
        items_pagados = True
        for item in self.itemordengiro_set.all():
            if item.item_pagado_actas() == False:
                items_pagados = False
        if items_pagados == True:
            self.estado = 2
            self.save()
            

class ItemOrdenGiro(models.Model):
    valor = models.FloatField()
    descripcion = models.TextField()
    suministro = models.ForeignKey(SuministroRequisicion)
    orden_giro = models.ForeignKey(OrdenGiro)

    class Meta:
        unique_together = ('suministro', 'orden_giro')
        verbose_name_plural = "10.2. Item Orden de Giro"

    def valor_pagado_actas(self):
        valor_pagado_actas = self.itemactaconformidad_set.all().aggregate(Sum('valor'))['valor__sum']
        if valor_pagado_actas == None:
            valor_pagado_actas = 0
        return valor_pagado_actas

    def valor_disponible(self, valor_evaluar):
        valor_disponible = False
        if valor_evaluar <= round(self.valor - self.valor_pagado_actas(), 2):
            valor_disponible = True
        return valor_disponible

    def item_pagado_actas(self):
        item_pagado = False
        if self.valor == self.valor_pagado_actas():
            item_pagado = True
        return item_pagado

    def valor_facturado(self):
        valor_facturado = self.itemactaconformidad_set.all().aggregate(Sum('valor'))['valor__sum']
        if valor_facturado == None:
            valor_facturado = 0
        return valor_facturado

    def __unicode__(self):
        return "id=%s - orden_giro=%s --- requisicion_id=%s" % (self.id, self.orden_giro.id, self.suministro.requisicion.id )

class ActaConformidad(models.Model):
    consecutivo = models.IntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    orden_giro = models.ForeignKey(OrdenGiro)
    persona = models.ForeignKey(Usuario)

    def save(self):
        if self.consecutivo == None:
            'Get last value of Code and Number from database, and increment before save'
            consecutivo = ActaConformidad.objects.filter(orden_giro__proyecto=self.orden_giro.proyecto).aggregate(Max('consecutivo'))['consecutivo__max']
            if consecutivo == None:
                consecutivo = 1
            else:
                consecutivo = consecutivo + 1
            self.consecutivo = consecutivo
        super(ActaConformidad, self).save()

    def valor_total(self):
        valor_total = 0
        for item_acta_conformidad in self.itemactaconformidad_set.all():
            valor_total = round(valor_total + item_acta_conformidad.valor, 2)
        return valor_total

    def orden_giro_id_asociado(self):
        return self.orden_giro.id

    def capitulos_items(self):
        capitulos_items = []
        for item_acta_conformidad in self.itemactaconformidad_set.all():
            capitulos_items.append({'capitulo': item_acta_conformidad.item_orden_giro.suministro.suministro.apu_proyecto.capitulo, 'valor': item_acta_conformidad.valor, 'tipo_capitulo': item_acta_conformidad.item_orden_giro.suministro.suministro.apu_proyecto.capitulo.tipo_capitulo })

        return capitulos_items


    def __unicode__(self):
        return "id=%s" % (self.id)

    class Meta:
        verbose_name_plural = "11.1. Acta de Conformidad"

class ItemActaConformidad(models.Model):
    valor = models.FloatField()
    item_orden_giro = models.ForeignKey(ItemOrdenGiro)
    acta_conformidad = models.ForeignKey(ActaConformidad)
    
    class Meta:
        unique_together = ('item_orden_giro', 'acta_conformidad')
        verbose_name_plural = "11.2. Item Acta de Conformidad"

    def __unicode__(self):
        return "id:%s - sum=%s - acta_conformidad=%s " % (self.id, unicode(self.item_orden_giro.suministro.suministro.suministro.nombre),self.acta_conformidad.id )



class FacturaOrdencompra(models.Model):
    consecutivo = models.IntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    numero_factura = models.CharField(max_length=15)
    proveedor = models.ForeignKey(Proveedor)
    proyecto = models.ForeignKey(Proyecto)
    persona = models.ForeignKey(Usuario)

    def save(self):
        if self.consecutivo == None:
            'Get last value of Code and Number from database, and increment before save'
            consecutivo = self.proyecto.facturaordencompra_set.all().aggregate(Max('consecutivo'))['consecutivo__max']
            if consecutivo == None:
                consecutivo = 1
            else:
                consecutivo = consecutivo + 1
            self.consecutivo = consecutivo
        super(FacturaOrdencompra, self).save()

    def subtotal(self):
        subtotal = 0
        for item in self.itemfacturaordencompra_set.all():
            subtotal = round(subtotal + item.valor_total_item_sin_iva(), 2)
        return subtotal

    def valor_iva(self):
        valor_iva = 0
        for item in self.itemfacturaordencompra_set.all():
            valor_iva = round(valor_iva + item.valor_iva_item(), 2)
        return valor_iva

    def valor_total(self):
        valor_total = 0
        for item in self.itemfacturaordencompra_set.all():
            valor_total = round(valor_total + item.valor_total_item(), 2)
        return valor_total

    def get_ordenes_compra(self):
        ordenes_compra = []
        items_factura = self.itemfacturaordencompra_set.all()
        for item_factura in items_factura:
            suministros_factura = item_factura.suministrofacturaordencompra_set.all()
            for suministro_factura in suministros_factura:
                if not suministro_factura.suministro_informe_recepcion.informe_recepcion.orden_compra in ordenes_compra:
                    ordenes_compra.append(suministro_factura.suministro_informe_recepcion.informe_recepcion.orden_compra)
        return ordenes_compra

    class Meta:
        verbose_name_plural = "06.1. Factura Orden de Compra"
    
class ItemFacturaOrdenCompra(models.Model):
    #La factura y el suministro no pueden ser unicos
    factura = models.ForeignKey(FacturaOrdencompra)
    suministro = models.ForeignKey(Suministro)

    class Meta:
        unique_together = ('factura', 'suministro')
        verbose_name_plural = "06.2. Item Suministros Factura Orden de Compra"

    #Retorna la sumatoria (cantidad) del item
    def cantidad_item(self):
        cantidad_item = self.suministrofacturaordencompra_set.all().aggregate(Sum('cantidad'))['cantidad__sum']
        if cantidad_item == None:
            cantidad_item = 0
        return cantidad_item

    #Retorna el valor unitario del item de la factura
    def valor_unitario_item_sin_iva(self):
        valor_unitario = self.suministrofacturaordencompra_set.all()[0].suministro_informe_recepcion.suministro.suministro_orden_compra_item.precio
        return valor_unitario

    #Retorna el valor total del item de la factura (cantidad * valor unitario)
    def valor_total_item_sin_iva(self):
        valor_total_item = round(self.cantidad_item() * self.valor_unitario_item_sin_iva(), 2)
        return valor_total_item

    #Retorna el porcentaje del iva
    def porcentaje_iva(self):
        porcentaje_iva = self.suministrofacturaordencompra_set.all()[0].suministro_informe_recepcion.suministro.suministro_orden_compra_item.iva_suministro
        return porcentaje_iva

    #Retorna el str porcentaje del iva
    def str_porcentaje_iva(self):
        porcentaje_iva = self.suministrofacturaordencompra_set.all()[0].suministro_informe_recepcion.suministro.suministro_orden_compra_item.iva_suministro * 100
        str_porcentaje_iva = str(porcentaje_iva) + ' %'
        return str_porcentaje_iva

    #Retorna el valor del iva del item
    def valor_iva_item(self):
        valor_iva_item = round(self.valor_total_item_sin_iva() * self.porcentaje_iva(), 2)
        return valor_iva_item

    #Retorna el valor total del item de la factura (cantidad * valor unitario) + iva
    def valor_total_item(self):
        valor_total_item = round(self.valor_total_item_sin_iva() + self.valor_iva_item(), 2)
        return valor_total_item

    def __unicode__(self):
        return "id=%s - sum=%s - factura_id=%s" % (self.id,unicode(self.suministro.nombre), self.factura.id)
    
class SuministroFacturaOrdenCompra(models.Model):
    cantidad = models.FloatField()
    suministro_informe_recepcion = models.ForeignKey(SuministroInformeRecepcion)
    item_factura_orden_compra = models.ForeignKey(ItemFacturaOrdenCompra)
    
    class Meta:
        unique_together = ('suministro_informe_recepcion', 'item_factura_orden_compra')
        verbose_name_plural = "06.3. Suministros Factura Orden de Compra"

    def __unicode__(self):
        return "id=%s - sum=%s - informe_recepcion_id=%s" % (self.id,unicode(self.item_factura_orden_compra.suministro.nombre), self.suministro_informe_recepcion.informe_recepcion.id)

#### #### MODULO DE VENTAS #### ####


class AdicionalAgrupacion(models.Model):
    nombre = models.CharField(max_length=140) # Tipo adicional / Item adicional
    descripcion = models.TextField(max_length=2000) # Item adicional
    valor = models.FloatField(default=0) # Item adicional
    item_adicional = models.BooleanField(default=False)
    proyecto = models.ForeignKey(Proyecto, null=True, blank=True) # Tipo adicional / Item adicional
    tipo_adicional = models.ForeignKey('self', null=True, blank=True) # Item tipo adicional

    class Meta:
        unique_together = (('nombre', 'proyecto'), ('nombre', 'tipo_adicional')) # No se bede duplicar el nombre de un tipo de adicional en el proyecto, ni el nombre de un adicional dentro de un tipo de adicional

    def __unicode__(self):
		return unicode(self.nombre)

    
## Entidad cliente ##

TIPO_IDENTIFICACION_CLIENTE = ((1, 'Cedula de ciudadania'),
                (2, 'Cedula extranjera'),
                (3, 'Nit'))

ABREVIATURA_TIPO_IDENTIFICACION_CLIENTE = ((1, 'C.C.'),
                (2, 'C.E.'),
                (3, 'Nit'))

ESTADO_CIVIL = ((1, 'Soltero (a) - Sin sociedad marital'),
                (2, 'Casado - Con sociedad conyugal vigente'),
                (3, 'Casado - Con sociedad conyugal disuelta y liquidada'),
                (4, 'Soltero (a) - Por estado de viudez'),
                (5, 'Soltero (a) - Con sociedad marital de hecho'))

INGRESOS_MENSUALES = ((0, ''),
                (1, 'Menos de un salario minimo'),
                (2, 'Entre 1 salario minimo y menos de 2'),
                (3, 'Entre 2 salarios minimos y menos de 4'),
                (4, 'Entre 4 salarios minimos y menos de 6'),
                (5, 'Mas de 6 salarios minimos'))

class Cliente(models.Model):
    tipo_identificacion = models.SmallIntegerField(choices=TIPO_IDENTIFICACION_CLIENTE)
    identificacion = models.BigIntegerField(unique=True)
    nombre_1 = models.CharField(max_length=20)
    nombre_2 = models.CharField(max_length=50)
    apellido_1 = models.CharField(max_length=20)
    apellido_2 = models.CharField(max_length=20)
    municipio_documento = models.ForeignKey(Municipio)
    estado_civil = models.SmallIntegerField(choices=ESTADO_CIVIL)
    municipio_residencia = models.ForeignKey('Municipio', related_name='relacion_municipio_residencia')
    direccion_residencia = models.CharField(max_length=30)
    telefono_1 = models.CharField(max_length=10) # Telefono ó celular
    telefono_2 = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    # Informacion laboral
    empresa = models.CharField(max_length=40, null=True, blank=True)
    telefono_empresa = models.CharField(max_length=10, null=True, blank=True) # Telefono ó celular
    extension_telefono_empresa = models.CharField(max_length=6,null=True,blank=True,default="")
    direccion_empresa = models.CharField(max_length=30, null=True, blank=True)
    ingresos_mensuales = models.SmallIntegerField(choices=INGRESOS_MENSUALES)
    observaciones = models.TextField()

    # Informacion del registro en la BD
    estado = models.BooleanField(default=True) # Estado del registro: 1-Activo, 0-Inactivo
    usuario_registro = models.ForeignKey(Usuario)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __unicode__(self):
		return unicode(self.nombre_1) + ' ' + unicode(self.nombre_2) + ' ' + unicode(self.apellido_1) + ' ' + unicode(self.apellido_2)

    def str_tipo_identificacion(self):
        tipo_identificacion = TIPO_IDENTIFICACION_CLIENTE[self.tipo_identificacion - 1][1]
        return tipo_identificacion

    def str_abreviatura_tipo_identificacion(self):
        tipo_identificacion = ABREVIATURA_TIPO_IDENTIFICACION_CLIENTE[self.tipo_identificacion - 1][1]
        return tipo_identificacion

    def str_estado_civil(self):
        estado_civil = ESTADO_CIVIL[self.estado_civil - 1][1]
        return estado_civil

    # Valida si existe el prospecto de venta del cliente en el proyecto
    def existe_prospecto_venta_proyecto(self, proyecto):
        prospecto_venta_proyecto = None
        try:
            prospecto_venta_proyecto = self.prospectoventa_set.get(proyecto=proyecto)
        except :
            pass
        self.prospecto_venta_proyecto = prospecto_venta_proyecto

    class Meta:
        verbose_name_plural = "12.1. Cliente"
        

class ContactoCliente(models.Model):
    nombre = models.CharField(max_length=140)
    telefono = models.CharField(max_length=10)
    municipio = models.ForeignKey(Municipio)
    email = models.EmailField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente)

    def __unicode__(self):
        return self.cliente.id


class SeccionProyecto(models.Model):
    nombre = models.CharField(max_length=140)
    iniciales = models.CharField(max_length=10)
    proyecto = models.ForeignKey(Proyecto)

    class Meta:
        unique_together = (('nombre', 'proyecto'), ('iniciales', 'proyecto')) # No se bede duplicar el nombre ni las iniciales dentro de una sección del proyecto
        verbose_name_plural = "13.1. Seccion Proyecto"

    def __unicode__(self):
		return unicode(self.nombre)


class TipoInmueble(models.Model):
    nombre = models.CharField(max_length=140, unique=True)
    descripcion = models.TextField(max_length=2000)

    def __unicode__(self):
		return unicode(self.nombre)

    class Meta:
        verbose_name_plural = "14.1. Tipo Inmueble"

ESTADO_REGISTRO_INMUEBLE = ((0, 'Inactivo'),
                (1, 'Activo'))

class Inmueble(models.Model):
    identificacion = models.CharField(max_length=140)
    area_construida = models.FloatField(null=True, blank=True)
    area_privada = models.FloatField(null=True, blank=True)
    fecha_escritura = models.DateField(null=True, blank=True)
    fecha_entrega = models.DateField(null=True, blank=True)
    valor = models.FloatField(default=0)
    lista_precios = models.PositiveSmallIntegerField(null=True, blank=True)
    fecha_entrega_obra = models.DateField(null=True, blank=True) # Fecha de entrega Obra-Ventas
    tipo_inmueble = models.ForeignKey(TipoInmueble)
    seccion_proyecto = models.ForeignKey(SeccionProyecto)
    proyecto = models.ForeignKey(Proyecto)
    item_agrupacion_inmueble = models.OneToOneField('ItemAgrupacionInmueble', related_name='relacion_itemagrupacioninmueble', null=True, blank=True) # Datos de referencia de la agrupación actual a la que pertenece el inmueble

    # Informacion del registro en la BD
    permiso_modificar = models.BooleanField(default=True)
    estado_registro = models.BooleanField(default=True) # Estado del registro: 1-Activo, 0-Inactivo
    usuario_registro = models.ForeignKey(Usuario)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "15.1. Inmueble"

    def __unicode__(self):
		return unicode(self.identificacion)

    def save(self):
        if self.id != None and self.item_agrupacion_inmueble != None:
            if self.proyecto.inmueble_set.get(id=self.id).permiso_modificar:
                self.permiso_modificar = False
        super(Inmueble, self).save()
        ## Codigo para actualizar el contrato donde pertenece el inmueble ##
        
    def str_descripcion(self):
        return self.tipo_inmueble.nombre + ': ' + self.identificacion

    def str_estado_inmueble(self):
        if self.item_agrupacion_inmueble != None:
            return self.item_agrupacion_inmueble.agrupacion_inmueble.str_estado_agrupacion()
        return 'Sin agrupar'

    def str_estado_registro(self):
        estado_registro = ESTADO_REGISTRO_INMUEBLE[self.estado_registro][1]
        return estado_registro

    def str_area_construida(self):
        if self.area_construida != None:
           return  self.area_construida
        return ''

    def str_area_privada(self):
        if self.area_privada != None:
           return  self.area_privada
        return ''

    def str_fecha_escritura(self):
        if self.fecha_escritura != None:
           return  self.fecha_escritura
        return ''

    def str_fecha_entrega(self):
        if self.fecha_entrega != None:
           return  self.fecha_entrega
        return ''

    def str_lista_precios(self):
        if self.lista_precios != None:
           return  self.lista_precios
        return ''

    def str_fecha_entrega_obra(self):
        if self.fecha_entrega_obra != None:
           return  self.fecha_entrega_obra
        return ''

    def str_identificacion(self):
        return self.seccion_proyecto.iniciales + '-' + self.identificacion


ESTADO_REGISTRO_AGRUPACION_INMUEBLE = ((0, 'Inactivo'),
                (1, 'Activo'))

class AgrupacionInmueble(models.Model):
    identificacion = models.CharField(max_length=140)
    inmueble_principal = models.OneToOneField('ItemAgrupacionInmueble', null=True, blank=True)
    agrupacion_contrato_venta = models.OneToOneField('AgrupacionInmuebleContratoVenta', related_name='relacion_agrupacioncontratoventa', null=True, blank=True) # Valor nulo si no hay contrato en ejecución
    proyecto = models.ForeignKey(Proyecto)

    # Informacion del registro en la BD
    estado_registro = models.BooleanField(default=True) # Estado del registro: 1-Activo, 0-Inactivo
    usuario_registro = models.ForeignKey(Usuario)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)

    def save(self):
        if self.inmueble_principal != None:
            self.identificacion = self.inmueble_principal.inmueble.seccion_proyecto.iniciales + '-' + self.inmueble_principal.inmueble.identificacion
        super(AgrupacionInmueble, self).save()

    def str_estado_registro(self):
        estado_registro = ESTADO_REGISTRO_AGRUPACION_INMUEBLE[self.estado_registro][1]
        return estado_registro

    def str_estado_agrupacion(self):
        if self.agrupacion_contrato_venta == None:
            return 'Disponible para venta'
        return self.agrupacion_contrato_venta.contrato_venta.str_estado_contrato_venta()

    def str_valor(self):
        valor_agrupacion = 0
        for item_inmueble in self.itemagrupacioninmueble_set.all():
            valor_agrupacion = round(valor_agrupacion + item_inmueble.inmueble.valor, 2)
        return valor_agrupacion

    def str_descripcion(self):
        str_descripcion = self.inmueble_principal.inmueble.str_descripcion() + '</br>'
        items_inmuebles = self.itemagrupacioninmueble_set.all().exclude(id=self.inmueble_principal.id)
        for item_inmueble in items_inmuebles:
            str_descripcion = str_descripcion + item_inmueble.inmueble.str_descripcion() + '</br>'
        return str_descripcion

    # Validaciones para saber si se puede eliminar el registro
    def eliminar_registro(self):
        eliminar_registro = False
        if self.agrupacion_contrato_venta == None:
            eliminar_registro = True
        return eliminar_registro

    def __unicode__(self):
		return unicode(self.id)

    class Meta:
        verbose_name_plural = "16.1. Agrupacion Inmueble"
    

class ItemAgrupacionInmueble(models.Model):
    inmueble = models.ForeignKey(Inmueble, related_name='relacion_inmueble')
    agrupacion_inmueble = models.ForeignKey(AgrupacionInmueble)

    def __unicode__(self):
		return unicode(self.id)

    class Meta:
        verbose_name_plural = "16.2. Item Agrupacion Inmueble"

# Sistema de encuestas
class Encuesta(models.Model):
    titulo = models.CharField(max_length=240, unique=True)
    descripcion = models.TextField(max_length=1000)
    estado_registro = models.BooleanField(default=True)

    def __unicode__(self):
		return unicode(self.titulo)

    def lista_preguntas(self):
        return self.preguntaencuesta_set.filter(estado_registro=True)

    class Meta:
        verbose_name_plural = "17.1. Encuesta"

class PreguntaEncuesta(models.Model):
    texto = models.TextField(max_length=1000)
    encuesta = models.ForeignKey(Encuesta)
    estado_registro = models.BooleanField(default=True)

    def __unicode__(self):
		return unicode(self.texto)

    def lista_respuestas(self):
        return self.respuestapreguntaencuesta_set.filter(estado_registro=True)

class RespuestaPreguntaEncuesta(models.Model):
    texto = models.TextField(max_length=1000)
    pregunta_encuesta = models.ForeignKey(PreguntaEncuesta)
    estado_registro = models.BooleanField(default=True)

    def __unicode__(self):
		return unicode(self.texto)
        

class EncuestaCliente(models.Model):
    fecha_registro = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True)
    encuesta = models.ForeignKey(Encuesta)
    usuario_registro = models.ForeignKey(Usuario, related_name='relacion_usuarioregistroencuesta')

    def __unicode__(self):
		return unicode(self.id)


class PreguntaEncuestaCliente(models.Model):
    encuesta_cliente = models.ForeignKey(EncuestaCliente)
    pregunta_encuesta = models.ForeignKey(PreguntaEncuesta)
    

class RespuestaClientePreguntaEncuesta(models.Model):
    encuesta_cliente = models.ForeignKey(EncuestaCliente)
    pregunta_encuesta_cliente = models.ForeignKey(PreguntaEncuestaCliente)
    respuesta_pregunta_encuesta = models.ForeignKey(RespuestaPreguntaEncuesta)


class ProspectoVenta(models.Model):
    fecha_registro = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente)
    proyecto = models.ForeignKey(Proyecto)
    usuario_registro = models.ForeignKey(Usuario, related_name='relacion_usuarioregistroprospectoventa')
    usuario_responsable = models.ForeignKey(Usuario, related_name='relacion_usuarioresponsableprospectoventa') # Usuario al que esta asignado el prospecto de venta

    class Meta:
        unique_together = ('cliente', 'proyecto')
        verbose_name_plural = "18.1. Prospecto de Venta"

    def lista_agrupaciones_inmuebles(self):
        ids_agrupaciones_inmueble = self.agrupacionesinmuebleprospectoventa_set.values('agrupacion_inmueble_id')
        return self.proyecto.agrupacioninmueble_set.filter(id__in=ids_agrupaciones_inmueble)

    def lista_agrupaciones_inmuebles_disponibles_venta(self, criterio=''):
        agrupaciones_prospecto_venta = self.lista_agrupaciones_inmuebles()
        ids_agrupaciones_disponibles_venta = []

        for agrupacion_prospecto_venta in agrupaciones_prospecto_venta:
            agrupacion_inmueble = None
            try:
                agrupacion_inmueble = self.proyecto.agrupacioninmueble_set.get(identificacion=agrupacion_prospecto_venta.identificacion, estado_registro=True, agrupacion_contrato_venta=None, identificacion__icontains=criterio)
            except :
                pass
            if agrupacion_inmueble != None:
                ids_agrupaciones_disponibles_venta.append(agrupacion_inmueble.id)
        return self.proyecto.agrupacioninmueble_set.filter(id__in=ids_agrupaciones_disponibles_venta)

    def __unicode__(self):
		return unicode(self.id)

class AgrupacionesInmuebleProspectoVenta(models.Model):
    prospecto_venta = models.ForeignKey(ProspectoVenta)
    agrupacion_inmueble = models.ForeignKey(AgrupacionInmueble)

    def __unicode__(self):
		return self.id

    class Meta:
        verbose_name_plural = "18.2.Agrupacion Inmuebles Prospecto de Venta"

# Modelo Entidad Bancaria
class EntidadBancaria(models.Model) :
    nombre = models.CharField(max_length=140, unique=True)
    estado_registro = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.nombre)

    def cuentas_asociadas(self):
        return self.numerocuenta_set.all()

class NumeroCuenta(models.Model):
    entidad_bancaria = models.ForeignKey(EntidadBancaria)
    numero = models.CharField(max_length=300)
    descripcion = models.CharField(max_length=500,default="",null=True,blank=True)
    estado_registro = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s %s" %(unicode(self.entidad_bancaria),unicode(self.numero))


FORMA_PAGO_CONTRATO_VENTA = ((1, 'Credito'),
            (2, 'Contado'))

ESTADO_CONTRATO_VENTA = ((0, 'No concretado'),
            (1, 'Reservado'),
            (2, 'Separado'),
            (3, 'Vendido'),
            (4, 'Desistido fiducia'),
            (5, 'Desistido directo'))

class EstadoContratoVenta(models.Model):
    estado_contrato = models.SmallIntegerField(choices=ESTADO_CONTRATO_VENTA, default=1) # Estado del contrato
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_limite_estado = models.DateField(null=True, blank=True) # Solo funciona para el estado en reserva
    estado_registro = models.BooleanField(default=True)
    contrato_venta = models.ForeignKey('ContratoVenta')

    class Meta:
        unique_together = ('estado_contrato', 'contrato_venta') # No se bede duplicar el estado de un proyecto
    
    def str_estado_contrato_venta(self):
        return ESTADO_CONTRATO_VENTA[self.estado_contrato][1]

class ContratoVenta(models.Model):
    consecutivo = models.IntegerField()
    identificacion = models.CharField(max_length=140) # Se define de acuerdo al proyecto_identificacion-de-la-agrupación-del-inmueble_consecutivo
    forma_pago = models.SmallIntegerField(choices=FORMA_PAGO_CONTRATO_VENTA, null=True,blank=True) # Forma de pago del contrato
    entidad_bancaria_credito = models.ForeignKey(EntidadBancaria, null=True,blank=True) # Entidad bancaria con la que se solicita el creditontidad bancaria con la que se solicita el credito
    monto_credito = models.FloatField(default=0)
    fecha_registro_desembolso_credito = models.DateField(null=True,blank=True)
    valor_desembolsado_credito = models.FloatField(null=True,blank=True)
    credito_verificado = models.BooleanField(default=False)
    numero_cuenta_fiducia = models.CharField(max_length=40, null=True,blank=True)
    permiso_modificar = models.BooleanField(default=True) # Permiso que permite la modificación del contrato, este cambia a (False) cuando el contrato cambie a estado vendido --
    permiso_imprimir_promesa_compraventa = models.BooleanField(default=True) # Permiso que permite la impresión de la promesa de venta del contrato, este cambia a (False) cuando el contrato cambie a estado vendido
    cliente_principal = models.ForeignKey('ClienteContratoVenta', null=True,blank=True)
    estado_registro = models.BooleanField(default=True) # Estado del registro: 1-Activo, 0-Inactivo
    prospecto_venta = models.ForeignKey(ProspectoVenta)
    proyecto = models.ForeignKey(Proyecto)
    usuario_registro = models.ForeignKey(Usuario, related_name='relacion_usuarioregistrocontratoventa')
    usuario_responsable = models.ForeignKey(Usuario, related_name='relacion_usuarioresponsablecontratoventa') # Usuario al que esta asignado el contrato
    referencia_inmueble = models.CharField(max_length=40, null=True, blank=True)
    
    def save(self):
        if self.consecutivo == None:
            'Get last value of Code and Number from database, and increment before save'
            consecutivo = self.proyecto.contratoventa_set.all().aggregate(Max('consecutivo'))['consecutivo__max']
            if consecutivo == None:
                consecutivo = 1
            else:
                consecutivo = consecutivo + 1
            self.consecutivo = consecutivo
        if self.id != None:
            agrupacion_inmueble = self.agrupacioninmueblecontratoventa_set.get(estado_registro=True)
            self.identificacion = self.proyecto.iniciales + '-' + agrupacion_inmueble.agrupacion_inmueble.identificacion + '-' + str(self.consecutivo)
        super(ContratoVenta, self).save()

    # Fecha en la que el contrato paso a estado (Separado)
    def str_fecha_registro(self):
        estado_contrato = None
        try:
            estado_contrato = self.estadocontratoventa_set.get(estado_contrato=2)
        except :
            pass
        if estado_contrato:
            return estado_contrato.fecha_registro
        return ''

    def str_estado_contrato_venta(self):
        return self.estadocontratoventa_set.get(estado_registro=True).str_estado_contrato_venta()

    def str_forma_pago(self):
        forma_pago = ''
        if self.forma_pago:
            forma_pago = FORMA_PAGO_CONTRATO_VENTA[self.forma_pago-1][1]
        return forma_pago

     # Fecha en la que el contrato pasa a estado (Vendido) (Por default)

    def str_fecha_promesa_compra_venta(self):
        estado_contrato = None
        try:
            estado_contrato = self.estadocontratoventa_set.get(estado_contrato=3)
        except :
            pass
        if estado_contrato:
            return estado_contrato.fecha_registro
        return ''

    def agrupacion_contrato_venta(self):
        return self.agrupacioninmueblecontratoventa_set.get(estado_registro=True).agrupacion_inmueble

    def estado_contrato_venta(self):
        return self.estadocontratoventa_set.get(estado_registro=True)

    def agrupacion_inmueble_contrato_venta(self):
        return self.agrupacioninmueblecontratoventa_set.get(estado_registro=True)

    def calcular_valores(self):
        from views_proyecto.funciones_views import to_word
        self.str_valor_agrupacion_inmueble = self.agrupacion_contrato_venta().str_valor()
        for adicional_agrupacion_contrato_venta in self.adicionalagrupacioncontratoventa_set.all():
            self.str_valor_agrupacion_inmueble = round(self.str_valor_agrupacion_inmueble + adicional_agrupacion_contrato_venta.valor, 2)
        self.str_valor_pagar_entidades_bancarias = 0.0
        self.str_valor_pagado_entidades_bancarias = 0.0
        for pago_entidad_bancaria in self.pagoentidadcontratoventa_set.all():
            self.str_valor_pagar_entidades_bancarias = round(self.str_valor_pagar_entidades_bancarias + pago_entidad_bancaria.valor, 2)
            if pago_entidad_bancaria.verificado:
                self.str_valor_pagado_entidades_bancarias = round(self.str_valor_pagado_entidades_bancarias + pago_entidad_bancaria.valor_desembolsado, 2)

        self.str_valor_pagar_efectivo = 0.0
        for pago_efectivo in self.pagoefectivocontratoventa_set.all():
            self.str_valor_pagar_efectivo = round(self.str_valor_pagar_efectivo + pago_efectivo.valor, 2)

        self.str_valor_pagado_efectivo = 0.0
        for abono_pago_efectivo in self.abonopagoefectivocontratoventa_set.all():
            if abono_pago_efectivo.verificado:
                self.str_valor_pagado_efectivo = round(self.str_valor_pagado_efectivo + abono_pago_efectivo.valor, 2)

        self.str_numero_pagos_efectivo = len(self.pagoefectivocontratoventa_set.all())

        self.str_valor_pagar_cliente = round(self.monto_credito + self.str_valor_pagar_entidades_bancarias + self.str_valor_pagar_efectivo, 2)

        self.str_valor_actual_pagado = round(self.str_valor_pagado_entidades_bancarias + self.str_valor_pagado_efectivo, 2)
                
        valor_inmueble_letras = to_word(int(self.str_valor_agrupacion_inmueble), 'COP')
        self.str_valor_inmueble_letras = valor_inmueble_letras.replace('Colombianos', '') + ' con ' + str(self.str_valor_agrupacion_inmueble).split('.')[1] + ' centavos.'

        valor_pagar_entidades_bancarias_letras = to_word(int(self.str_valor_pagar_entidades_bancarias), 'COP')
        self.str_valor_pagar_entidades_bancarias_letras = valor_pagar_entidades_bancarias_letras.replace('Colombianos', '') + ' con ' + str(self.str_valor_pagar_entidades_bancarias).split('.')[1] + ' centavos.'

        valor_pagar_efectivo_letras = to_word(int(self.str_valor_pagar_efectivo), 'COP')
        self.str_valor_pagar_efectivo_letras = valor_pagar_efectivo_letras.replace('Colombianos', '') + ' con ' + str(self.str_valor_pagar_efectivo).split('.')[1] + ' centavos.'

        monto_credito_letras = to_word(int(self.monto_credito), 'COP')
        self.str_monto_credito_letras = monto_credito_letras.replace('Colombianos', '') + ' con ' + str(self.monto_credito).split('.')[1] + ' centavos.'

    # Consolidado para los detalles de un contrato
    def consolidado_pagos_efectivo(self):
        valor_total_abonos_efectivo = self.abonopagoefectivocontratoventa_set.filter(verificado=True).aggregate(Sum('valor'))['valor__sum']
        if not valor_total_abonos_efectivo:
            valor_total_abonos_efectivo = 0
        suma_cuotas_pagadas = 0

        pagos_efectivo_contrato_venta = self.pagoefectivocontratoventa_set.all().order_by('fecha_desembolso')

        for pago_efectivo_contrato_venta in pagos_efectivo_contrato_venta:
            if suma_cuotas_pagadas < valor_total_abonos_efectivo:
                saldo_pago_efectivo_contrato_venta = round(pago_efectivo_contrato_venta.valor - (valor_total_abonos_efectivo - suma_cuotas_pagadas), 2)
                if saldo_pago_efectivo_contrato_venta < 0:
                    saldo_pago_efectivo_contrato_venta = 0
                pago_efectivo_contrato_venta.saldo_pendiente_pagar = saldo_pago_efectivo_contrato_venta
                suma_cuotas_pagadas = round(suma_cuotas_pagadas + pago_efectivo_contrato_venta.valor, 2)

        return pagos_efectivo_contrato_venta

    def str_documento_apertura_fiducuenta(self, usuario):
        from django.utils.safestring import mark_safe
        from datetime import date
        str_documento_apertura_fiducuenta = ''
        if self.proyecto.apertura_fiducuenta:
            fecha_actual = date.today().strftime('%d de %m de %Y')
            cliente_principal = self.cliente_principal.cliente
            str_documento_apertura_fiducuenta = self.proyecto.str_apertura_fiducuenta()
            str_documento_apertura_fiducuenta = mark_safe(str_documento_apertura_fiducuenta.replace('####FECHA####', fecha_actual))
            str_documento_apertura_fiducuenta = mark_safe(str_documento_apertura_fiducuenta.replace('####NUMERO FIDUCUENTA####', self.numero_cuenta_fiducia))
            str_documento_apertura_fiducuenta = mark_safe(str_documento_apertura_fiducuenta.replace('####NOMBRE CLIENTE PRINCIPAL####', cliente_principal.nombre_1.encode('utf-8') + ' ' + cliente_principal.nombre_2.encode('utf-8') + ' ' + cliente_principal.apellido_1.encode('utf-8') + ' ' + cliente_principal.apellido_2.encode('utf-8') + ' identificado con ' + cliente_principal.str_tipo_identificacion() + ' No. ' + str(cliente_principal.identificacion)))
            str_documento_apertura_fiducuenta = mark_safe(str_documento_apertura_fiducuenta.replace('####FIRMA USUARIO####', '<br/><br/>________________________________ <br />' + usuario.first_name.encode('utf-8') + ' ' + usuario.last_name.encode('utf-8') + ' <br /> Inversiones Boyaca Ltda.'))
        return str_documento_apertura_fiducuenta

    def str_documento_carta_instrucciones(self):
        from django.contrib.humanize.templatetags.humanize import intcomma
        from django.utils.safestring import mark_safe
        str_documento_carta_instrucciones = ''
        if self.proyecto.carta_instrucciones:
            str_documento_carta_instrucciones = self.proyecto.str_carta_instrucciones()
            str_clientes = self.str_html_abrev_descripcion_clientes()
            str_firmas_clientes = self.str_html_firmas_clientes()
            str_cronograma_pagos = self.str_html_cronograma_pagos_efectivo()
            str_documento_carta_instrucciones = mark_safe(str_documento_carta_instrucciones.replace('####ID CONTRATO####', self.identificacion))
            str_documento_carta_instrucciones = mark_safe(str_documento_carta_instrucciones.replace('####PROYECTO####', self.proyecto.nombre))
            str_documento_carta_instrucciones = mark_safe(str_documento_carta_instrucciones.replace('####INMUEBLE####', self.agrupacion_contrato_venta().identificacion))
            str_documento_carta_instrucciones = mark_safe(str_documento_carta_instrucciones.replace('####SECCION INMUEBLE####', self.agrupacion_contrato_venta().inmueble_principal.inmueble.seccion_proyecto.nombre))
            str_documento_carta_instrucciones = mark_safe(str_documento_carta_instrucciones.replace('####AREA INMUEBLE####', str(self.agrupacion_contrato_venta().inmueble_principal.inmueble.area_construida)))
            str_documento_carta_instrucciones = mark_safe(str_documento_carta_instrucciones.replace('####VALOR INMUEBLE####', str(intcomma(self.str_valor_agrupacion_inmueble))))
            str_documento_carta_instrucciones = mark_safe(str_documento_carta_instrucciones.replace('####VALOR INMUEBLE LETRAS####', self.str_valor_inmueble_letras))
            str_documento_carta_instrucciones = mark_safe(str_documento_carta_instrucciones.replace('####NOMBRES CLIENTES####', str_clientes))
            str_documento_carta_instrucciones = mark_safe(str_documento_carta_instrucciones.replace('####CRONOGRAMA PAGOS EFECTIVO####', str_cronograma_pagos))
            if self.monto_credito > 0:
                str_documento_carta_instrucciones = mark_safe(str_documento_carta_instrucciones.replace('####TOTAL FINANCIACION####', str(intcomma(self.monto_credito))))
            else:
                str_documento_carta_instrucciones = mark_safe(str_documento_carta_instrucciones.replace('####TOTAL FINANCIACION####', '-'))
            str_documento_carta_instrucciones = mark_safe(str_documento_carta_instrucciones.replace('####FIRMAS CLIENTES####', str_firmas_clientes))
        return str_documento_carta_instrucciones

    def str_documento_promesa_compraventa(self):
        from django.contrib.humanize.templatetags.humanize import intcomma
        from django.utils.safestring import mark_safe
        str_documento_promesa_compraventa = ''
        if self.proyecto.promesa_compraventa:
            str_documento_promesa_compraventa = self.proyecto.str_promesa_compraventa()
            str_clientes = self.str_html_abrev_descripcion_sociedad_conyugal_clientes()
            str_firmas_clientes = self.str_html_firmas_clientes()
            str_cronograma_pagos_entidades = self.str_html_cronograma_pagos_entidades()
            str_cronograma_pagos_efectivo = self.str_html_cronograma_pagos_efectivo()
            str_documento_promesa_compraventa = mark_safe(str_documento_promesa_compraventa.replace('####NOMBRES CLIENTES####', str_clientes))
            #Info del inmueble
            informacion_inmueble = 'Tipo: '
            agrupacion_contrato_venta = self.agrupacion_contrato_venta()
            for inmueble in agrupacion_contrato_venta.itemagrupacioninmueble_set.all():
                informacion_inmueble += inmueble.inmueble.tipo_inmueble.nombre + ' No.' + inmueble.inmueble.identificacion
                if inmueble == agrupacion_contrato_venta.inmueble_principal:
                    informacion_inmueble += ' Area: ' + str(inmueble.inmueble.area_construida) + ', '
            informacion_inmueble += u' Localización: ' + self.proyecto.direccion
            informacion_inmueble += ' Acabados: '
            for acabado in self.adicionalagrupacioncontratoventa_set.all():
                informacion_inmueble += acabado.nombre + ' '
            str_documento_promesa_compraventa = mark_safe(str_documento_promesa_compraventa.replace('####INFORMACION INMUEBLE####', informacion_inmueble))
            str_documento_promesa_compraventa = mark_safe(str_documento_promesa_compraventa.replace('####VALOR INMUEBLE####', str(intcomma(self.str_valor_agrupacion_inmueble))))
            str_documento_promesa_compraventa = mark_safe(str_documento_promesa_compraventa.replace('####VALOR INMUEBLE LETRAS####', self.str_valor_inmueble_letras))
            str_documento_promesa_compraventa = mark_safe(str_documento_promesa_compraventa.replace('####VALOR PAGOS EFECTIVO CONTRATO####', str(intcomma(self.str_valor_pagar_efectivo))))
            str_documento_promesa_compraventa = mark_safe(str_documento_promesa_compraventa.replace('####VALOR PAGOS EFECTIVO CONTRATO LETRAS####', self.str_valor_pagar_efectivo_letras))
            str_documento_promesa_compraventa = mark_safe(str_documento_promesa_compraventa.replace('####CRONOGRAMA PAGOS EFECTIVO####', str_cronograma_pagos_efectivo))
            str_documento_promesa_compraventa = mark_safe(str_documento_promesa_compraventa.replace('####VALOR PAGOS OTROS RECURSOS CONTRATO####', str(intcomma(self.str_valor_pagar_entidades_bancarias))))
            if self.pagoentidadcontratoventa_set.all():
                str_documento_promesa_compraventa = mark_safe(str_documento_promesa_compraventa.replace('####VALOR PAGOS OTROS RECURSOS CONTRATO LETRAS####', self.str_valor_pagar_entidades_bancarias_letras))
            else:
                str_documento_promesa_compraventa = mark_safe(str_documento_promesa_compraventa.replace('####VALOR PAGOS OTROS RECURSOS CONTRATO LETRAS####', 'Cero'))

            if self.pagoentidadcontratoventa_set.all():
                str_documento_promesa_compraventa = mark_safe(str_documento_promesa_compraventa.replace('####CRONOGRAMA OTROS RECURSOS####', str_cronograma_pagos_entidades))
            else:
                str_documento_promesa_compraventa = mark_safe(str_documento_promesa_compraventa.replace('####CRONOGRAMA OTROS RECURSOS####', 'No aplica, Pago otros recursos: 0 (Cero)'))

            str_documento_promesa_compraventa = mark_safe(str_documento_promesa_compraventa.replace('####MONTO CREDITO####', str(intcomma(self.monto_credito))))

            if self.monto_credito > 0:
                str_documento_promesa_compraventa = mark_safe(str_documento_promesa_compraventa.replace('#####ENTIDAD BANCARIA CREDITO####', self.entidad_bancaria_credito.nombre))
            else:
                str_documento_promesa_compraventa = mark_safe(str_documento_promesa_compraventa.replace('#####ENTIDAD BANCARIA CREDITO####', ''))

            if self.monto_credito > 0:
                str_documento_promesa_compraventa = mark_safe(str_documento_promesa_compraventa.replace('####MONTO CREDITO LETRAS####', self.str_monto_credito_letras))
            else:
                str_documento_promesa_compraventa = mark_safe(str_documento_promesa_compraventa.replace('####MONTO CREDITO LETRAS####', 'Cero'))
            fecha_escritura = self.agrupacion_contrato_venta().inmueble_principal.inmueble.fecha_escritura.strftime('%Y-%m-%d')
            if self.agrupacion_contrato_venta().inmueble_principal.inmueble.fecha_entrega_obra:
                fecha_entrega = self.agrupacion_contrato_venta().inmueble_principal.inmueble.fecha_entrega_obra.strftime('%Y-%m-%d')
                info_fechas = '%s, FECHA DE ENTREGA: %s' % (fecha_escritura,fecha_entrega)
            else:
                info_fechas = fecha_escritura
            str_documento_promesa_compraventa = mark_safe(str_documento_promesa_compraventa.replace('####FECHA ESCRITURA####', info_fechas ))
            str_documento_promesa_compraventa = mark_safe(str_documento_promesa_compraventa.replace('####FIRMAS CLIENTES####', str_firmas_clientes))
            str_documento_promesa_compraventa = mark_safe(str_documento_promesa_compraventa.replace('####PROYECTO####', self.proyecto.nombre))
        return str_documento_promesa_compraventa

    def str_html_abrev_descripcion_clientes(self):
        str_html_abrev_descripcion_clientes = ''
        for cliente in self.clientecontratoventa_set.all():
            str_html_abrev_descripcion_clientes += cliente.cliente.__unicode__() + ' identificado con ' + cliente.cliente.str_tipo_identificacion() + ' No. ' + ' de ' + cliente.cliente.municipio_documento.__unicode__() + ' (' + cliente.cliente.municipio_documento.departamento.__unicode__() + '), '
        return str_html_abrev_descripcion_clientes

    def str_html_abrev_descripcion_sociedad_conyugal_clientes(self):
        str_html_abrev_descripcion_clientes = ''
        for cliente in self.clientecontratoventa_set.all():
            str_html_abrev_descripcion_clientes += cliente.cliente.__unicode__().upper() + ' identificado con ' + cliente.cliente.str_tipo_identificacion() + ' No. ' + str(cliente.cliente.identificacion) + ' de ' + cliente.cliente.municipio_documento.__unicode__() + ' (' + cliente.cliente.municipio_documento.departamento.__unicode__() + ') mayor de edad, con estado civil ' + cliente.cliente.str_estado_civil() + ', '
        return str_html_abrev_descripcion_clientes

    def str_html_cronograma_pagos_efectivo(self):
        from django.contrib.humanize.templatetags.humanize import intcomma
        str_html_cronograma_pagos_efectivo = '<table align="center" class="bordeada tabla_pagos"><tr><th width="20px">N.</th><th width="160px">Concepto</th><th width="160px">Valor</th><th width="120px">Fecha</th></tr>'
        indice = 1
        pagos_efectivo = self.pagoefectivocontratoventa_set.all().order_by('fecha_desembolso')
        for pago_efectivo in pagos_efectivo:
            concepto = 'Cuota'
            if indice == 1:
                concepto = 'Cuota separacion'
            str_html_cronograma_pagos_efectivo += '<tr><th width="40px">' + str(indice) + '</th>' + '<td width="100px">' + concepto + '</td><td width="110px" align="right">'+ str(intcomma(pago_efectivo.valor)) + '</td><td width="75px" align="right">' + pago_efectivo.fecha_desembolso.strftime('%d-%m-%Y') + '</td></tr>'
            indice += 1
        str_html_cronograma_pagos_efectivo += '</table><br /><label>TOTAL RECURSOS PROPIOS $ ' + str(intcomma(self.str_valor_pagar_efectivo))
        return str_html_cronograma_pagos_efectivo

    def str_html_cronograma_pagos_entidades(self):
        from django.contrib.humanize.templatetags.humanize import intcomma
        str_html_cronograma_pagos = '<table align="center" class="bordeada tabla_pagos"><tr><th width="20px">N.</th><th width="160px">Concepto</th><th width="120px">Valor</th><th width="180px">Entidad</th><th width="180px">No. cuenta</th></tr>'
        indice = 1
        for pago_entidad in self.pagoentidadcontratoventa_set.all():
            str_html_cronograma_pagos += '<tr><th  width="40px">' + str(indice) + '</th>' + '<td  width="110px">' + pago_entidad.str_tipo_cuenta() + '</td><td  width="100px" align="right">'+ str(intcomma(pago_entidad.valor)) + '</td><td  width="140px" align="right">' + pago_entidad.entidad.nombre + '</td><td  width="90px" align="right">' + pago_entidad.numero_cuenta + '</td></tr>'
            indice += 1
        str_html_cronograma_pagos += '</table><br /><label>TOTAL OTROS RECURSOS $ ' + str(intcomma(self.str_valor_pagar_entidades_bancarias))
        return str_html_cronograma_pagos

    def str_html_firmas_clientes(self):
        str_html_firmas_clientes = '<table><tr><td>'
        indice = 1
        numero_clientes = len(self.clientecontratoventa_set.all())
        for cliente in self.clientecontratoventa_set.all():
            str_html_firmas_clientes += '<br /><br />________________________________ <br />' + cliente.cliente.nombre_1.upper() + ' ' + cliente.cliente.nombre_2.upper() + ' ' + cliente.cliente.apellido_1.upper() + ' ' + cliente.cliente.apellido_2.upper() + ' <br />' + cliente.cliente.str_abreviatura_tipo_identificacion() + ': ' + str(cliente.cliente.identificacion) + '<br />' + 'Tel.:' + cliente.cliente.telefono_1
            if indice < numero_clientes:
                str_html_firmas_clientes += '</td>'
                if indice % 2 == 0:
                    str_html_firmas_clientes += '</tr><tr><td>'
                else:
                    str_html_firmas_clientes += '<td>'
            indice += 1
        str_html_firmas_clientes += '</td></tr></table>'
        return str_html_firmas_clientes

    def permite_imprimir_carta_apertura_fiducuenta(self):
        """
            Verifica que:
            1- se haya registrado el numero de fiducuenta
            2- Que el proyecto tenga diligenciado el texto de la carta de instrucciones
        """
        permite_imprimir_carta_apertura_fiducuenta = True
        if not self.numero_cuenta_fiducia or self.numero_cuenta_fiducia == '' or not self.proyecto.carta_instrucciones:
            permite_imprimir_carta_apertura_fiducuenta = False
        return permite_imprimir_carta_apertura_fiducuenta

    def permite_imprimir_carta_instrucciones(self):
        """
            Verifica que:
            1- En contrato no se encuentre en estado reservado
            2- Que el proyecto tenga diligenciado el texto de la carta de instrucciones
        """
        permite_imprimir_carta_instrucciones = True
        if self.estado_contrato_venta().estado_contrato < 2 or not self.proyecto.carta_instrucciones:
            permite_imprimir_carta_instrucciones = False
        return permite_imprimir_carta_instrucciones

    def permite_imprimir_promesa_compraventa(self):
        """
            Verifica que:
            1- En contrato tenga activo el permiso de imprimir promesa de compraventa
            2- El inmueble principal tenga fecha de escritura
            3- Si tiene (monto credito) debe tener asignada una entidad bancaria
            4- Los pagos efectuados por medio de entidades bancarias (otros pagos) esten completamente diligenciados
            5- Que el contrato no se encuentre en estado reservado
            6- Que el proyecto tenga diligenciado el texto de la promesa de compraventa
        """
        permite_imprimir_promesa_compraventa = self.permiso_imprimir_promesa_compraventa
        if permite_imprimir_promesa_compraventa:
            if not self.agrupacion_contrato_venta().inmueble_principal.inmueble.fecha_escritura or (self.monto_credito and self.entidad_bancaria_credito == None) or (len(self.pagoentidadcontratoventa_set.filter(Q(entidad=None) | Q(numero_cuenta=None) | Q(numero_cuenta=''))) > 0) or self.estado_contrato_venta().estado_contrato < 2 or not self.proyecto.promesa_compraventa:
                permite_imprimir_promesa_compraventa = False
        return permite_imprimir_promesa_compraventa

    class Meta:
        verbose_name_plural = "19.1. Contrato de Venta"

    def __unicode__(self):
        return "%s %s" %(unicode(self.id), unicode(self.consecutivo))

class AgrupacionInmuebleContratoVenta(models.Model):
    estado_registro = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    agrupacion_inmueble = models.ForeignKey(AgrupacionInmueble)
    contrato_venta = models.ForeignKey(ContratoVenta)

    def __unicode__(self):
        return "%s %s" %(self.id, self.contrato_venta.id)

    class Meta:
        verbose_name_plural = "19.2.Agrupacion Contrato de Venta"

class AdicionalAgrupacionContratoVenta(models.Model):
    nombre = models.CharField(max_length=140) # Item adicional
    descripcion = models.TextField(max_length=2000) # Item adicional
    valor = models.FloatField(default=0) # Item adicional
    contrato_venta = models.ForeignKey(ContratoVenta)

    def __unicode__(self):
        return "%s %s" %(self.id, self.contrato_venta.id)


class ClienteContratoVenta(models.Model):
    cliente = models.ForeignKey(Cliente)
    contrato_venta = models.ForeignKey(ContratoVenta)

    class Meta:
        unique_together = ('cliente', 'contrato_venta')

    def __unicode__(self):
        return "id=%s - contrato_venta=%s - cliente=%s" %(self.id, self.contrato_venta.id, self.cliente.id)

TIPO_CUENTA_PAGO_ENTIDAD_CONTRATO_VENTA = ((1, 'Ahorro programado'),
            (2, 'CDT'),
            (3, 'Cesantias'),
            (4, 'Subsidio'))

class PagoEntidadContratoVenta(models.Model):
    tipo_cuenta = models.SmallIntegerField(choices=TIPO_CUENTA_PAGO_ENTIDAD_CONTRATO_VENTA, default=1) # tipo de notificación
    entidad = models.ForeignKey(EntidadBancaria, null=True, blank=True)
    numero_cuenta = models.CharField(max_length=40, null=True, default=None)
    fecha_desembolso = models.DateField(null=True, blank=True)
    valor = models.FloatField()
    fecha_registro_desembolso = models.DateField(null=True, blank=True)
    valor_desembolsado = models.FloatField(default=0)
    usuario_registro_desembolso = models.ForeignKey(Usuario, null=True, blank=True)
    verificado = models.BooleanField(default=False)
    contrato_venta = models.ForeignKey(ContratoVenta)

    def str_tipo_cuenta(self):
        return TIPO_CUENTA_PAGO_ENTIDAD_CONTRATO_VENTA[int(self.tipo_cuenta) - 1][1]

    def permite_modificacion(self):
        permite_modificacion = False
        if not self.verificado:
            permite_modificacion = True
        return permite_modificacion

    def permite_registrar_abono(self):
        permite_registrar_abono = False
        if not self.verificado:
            permite_registrar_abono = True
        return permite_registrar_abono

    def existe_abono(self):
        existe_abono = False
        if self.usuario_registro_desembolso:
            existe_abono = True
        return existe_abono

    def __unicode__(self):
        return "%s %s" %(self.id, self.contrato_venta.id)


class PagoEfectivoContratoVenta(models.Model):
    fecha_desembolso = models.DateField()
    valor = models.FloatField()
    contrato_venta = models.ForeignKey(ContratoVenta)

    def __unicode__(self):
        return "%s %s" %(self.id, self.contrato_venta.id)


class ModificacionContratoVenta(models.Model):
    fecha_registro = models.DateTimeField(auto_now_add=True)
    texto_legal = models.TextField(max_length=4000)
    contrato_venta = models.ForeignKey(ContratoVenta)
    usuario_registro = models.ForeignKey(Usuario)

    def __unicode__(self):
        return "%s %s" %(self.id, self.contrato_venta.id)

class AbonoPagoEfectivoContratoVenta(models.Model):
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_consignacion = models.DateField()
    numero_consignacion = models.CharField(max_length=20)
    valor = models.FloatField()
    verificado = models.BooleanField(default=False)
    contrato_venta = models.ForeignKey(ContratoVenta)
    usuario_registro = models.ForeignKey(Usuario)
    entidad_bancaria = models.ForeignKey(EntidadBancaria)
    cuenta = models.ForeignKey(NumeroCuenta,null=True,blank=True)

    def __unicode__(self):
        return "%s %s" %(self.id, self.contrato_venta.id)

TIPO_NOTIFICACION_VENTA = ((1, 'LLamada'),
            (2, 'E-mail'),
            (3, 'Videollamada'),
            (4, 'Chat'),
            (5, 'Visita'),
            (6, 'Otro'))

class NotificacionVenta(models.Model):
    fecha_registro = models.DateTimeField(auto_now_add=True)
    tipo_notificacion = models.SmallIntegerField(choices=TIPO_NOTIFICACION_VENTA, default=1) # tipo de notificación
    fecha_limite_notificacion = models.DateTimeField() # Fecha en la que debe finalizar la notificación
    descripcion = models.TextField(max_length=2000) # Observaciones cuando se crea la notificación
    respuesta_oportuna = models.BooleanField(default=False) # Verificar si el usuario dio respuesta a esta notificación
    respuesta_notificacion = models.TextField(max_length=2000) # Observaciones cuando se da respuesta a la notificación
    fecha_registro_respuesta = models.DateTimeField(null=True, blank=True) # Fecha en la que el usuario da respuesta a una notificación
    prospecto_venta = models.ForeignKey(ProspectoVenta, null=True, blank=True)
    contrato_venta = models.ForeignKey(ContratoVenta, null=True, blank=True)
    estado_registro = models.BooleanField(default=True) # Estado del registro: 1-Activo, 0-Inactivo
    usuario_registro = models.ForeignKey(Usuario, related_name='relacion_usuarioregistronotificacioncontratoventa')
    usuario_responsable = models.ForeignKey(Usuario, related_name='relacion_usuarioresponsablenotificacioncontratoventa') # Usuario al que esta asignada la notificación

    def str_tipo_notificacion(self):
        return TIPO_NOTIFICACION_VENTA[int(self.tipo_notificacion)-1][1]

    def permite_contestar(self):
        permite_contestar = False
        if self.fecha_registro_respuesta == None:
            permite_contestar = True
        return permite_contestar

    def __unicode__(self):
        return "%s %s" %(self.id, self.contrato_venta.id)

#### #### MODULO DE VENTAS #### ####



#### #### MODULO PLANES #### ####

def content_file_image_stage_project(instance, filename):
    array_filename = filename.split('.')
    directory_list = ['geo', 'project_' + str(instance.project.id), instance.initials, instance.initials + '.' + array_filename.pop()]
    return '/'.join(directory_list)

class Stage(models.Model):
    name = models.CharField(max_length=140)
    initials = models.CharField(max_length=4)
    description = models.TextField()
    image = models.ImageField(upload_to=content_file_image_stage_project)
    project = models.ForeignKey(Proyecto)

    class Meta:
        unique_together = ('name', 'initials', 'project')

    def save(self):
        super(Stage, self).save()
        if self.image:
            from PIL import Image
            image = Image.open(self.image)
            (width, height) = image.size
            size = ( 38, 34)
            image = image.resize(size, Image.ANTIALIAS)
            image.save(self.image.path)

    def get_image(self):
        import os
        if not self.image:
            return os.path.join('planes', 'img', 'default_icon_stage.jpg')
        return self.image.url

    # Verify if the stage don't have relation phase's
    def can_be_eliminated(self):
        if len(self.phase_set.all()) == 0:
            return True
        else:
            return False


def content_file_image_phase_project(instance, filename):
    array_filename = filename.split('.')
    directory_list = ['geo', 'project_' + str(instance.stage.project.id), instance.stage.initials, instance.initials, instance.initials + '.' + array_filename.pop()]
    return '/'.join(directory_list)

class Phase(models.Model):
    name = models.CharField(max_length=140)
    initials = models.CharField(max_length=4)
    description = models.TextField()
    image = models.ImageField(upload_to=content_file_image_phase_project)
    stage = models.ForeignKey(Stage)

    class Meta:
        unique_together = ('name', 'initials', 'stage')

    def save(self):
        super(Phase, self).save()
        if self.image:
            from PIL import Image
            image = Image.open(self.image)
            (width, height) = image.size
            size = ( 38, 34)
            image = image.resize(size, Image.ANTIALIAS)
            image.save(self.image.path)

    def get_image(self):
        import os
        if not self.image:
            return os.path.join('planes', 'img', 'default_icon_phase.jpg')
        return self.image.url

    # Verify if the stage don't have relation plane image's
    def can_be_eliminated(self):
        if len(self.imageplane_set.all()) == 0:
            return True
        else:
            return False


def content_file_name(instance, filename):
    #return '/'.join(['content', instance.user.username, filename])
    directory_list = ['images', 'planes']
    name_file_parts = filename.split('-')
    for item in name_file_parts:
        directory_list.append(item)
    return '/'.join(directory_list)


def content_file_name2(instance, filename):
    #return '/'.join(['content', instance.user.username, filename])
    directory_list = ['images', 'planes', 'thumb']
    name_file_parts = filename.split('-')
    for item in name_file_parts:
        directory_list.append(item)
    return '/'.join(directory_list)


def content_file_image_plane_project(instance, filename):
    array_filename = filename.split('.')
    directory_list = ['geo', 'project_' + str(instance.phase.stage.project.id), instance.phase.stage.initials, instance.phase.initials, instance.initials, instance.initials + '.' + array_filename.pop()]
    return '/'.join(directory_list)

class ImagePlane(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()
    #image_file = models.ImageField(upload_to=content_file_image_plane_project)
    initials = models.CharField(max_length=4)
    thumb_image_file = ImageWithThumbsField(upload_to=content_file_image_plane_project, sizes=((120, 90), (300, 225), (1024, 768)))
    phase = models.ForeignKey(Phase)

    def save(self):
        #self.docfile.upload_to = 'images/%Y/%m/%d'

        #self.docfile = models.FileField(upload_to='images/%Y/%m/%d')

        #print self.objects.model

        #import locale
        #language, output_encoding = locale.getdefaultlocale()
        #print type(self.docfile.storage)
        directory = ''
        super(ImagePlane, self).save()

    class Meta:
        unique_together = ('name', 'initials', 'phase')

    # Verify if the image plane don't have relation PhotographicZonePlane
    def can_be_eliminated(self):
        if len(self.photographiczoneplane_set.all()) == 0:
            return True
        else:
            return False


class PhotographicZonePlane(models.Model):
    consecutive = models.SmallIntegerField()
    point_x = models.FloatField()
    point_y = models.FloatField()
    marker = models.SmallIntegerField()
    image_plane = models.ForeignKey(ImagePlane)

    class Meta:
        unique_together = ('consecutive', 'image_plane')

    def save(self):
        if self.consecutive == None:
            'Get last value of Code and Number from database, and increment before save'
            consecutive = self.image_plane.photographiczoneplane_set.all().aggregate(Max('consecutive'))['consecutive__max']
            if consecutive == None:
                consecutive = 1
            else:
                consecutive = consecutive + 1
            self.consecutive = consecutive
        super(PhotographicZonePlane, self).save()

    def get_label(self):
        return 'P' + str(self.consecutive)

    def get_url_details(self):
        return '/inverboy/home/cronologicalpicturesreport/' + str(self.id) + '/' + str(self.image_plane.phase.stage.project.id) + '/'

    # Verify if the photographic zone don't have relation ChronologicalPicture
    def can_be_eliminated(self):
        if len(self.chronologicalpicture_set.all()) == 0:
            return True
        else:
            return False


def content_file_cronological_picture(instance, filename):
    array_filename = filename.split('.')
    array_name = array_filename[0].split('-')
    directory_list = ['geo', 'project_' + str(instance.photographic_zone_plane.image_plane.phase.stage.project.id), instance.photographic_zone_plane.image_plane.phase.stage.initials, instance.photographic_zone_plane.image_plane.phase.initials, instance.photographic_zone_plane.image_plane.initials, 'chronological_line', 'P' + str(instance.photographic_zone_plane.consecutive), array_name[5], array_name[6], array_name[7], array_name[5] + filename]
    return '/'.join(directory_list)

class ChronologicalPicture(models.Model):
    code = models.CharField(max_length=140, unique=True)
    date = models.DateField()
    description = models.TextField()
    thumb_image_file = ImageWithThumbsField(upload_to=content_file_cronological_picture, sizes=((120, 90), (300, 225), (1024, 768)))
    photographic_zone_plane = models.ForeignKey(PhotographicZonePlane)

    class Meta:
        unique_together = ('date', 'photographic_zone_plane')

    def save(self):
        super(ChronologicalPicture, self).save()

    def get_label_date(self):
        array_code = self.code.split('-')
        size_array_code = len(array_code)
        return array_code[size_array_code - 1] + '/' + array_code[size_array_code - 2] + '/' + array_code[size_array_code - 3]


def str_date_time(date_time):
    month = date_time.strftime('%m')
    if month == '01':
        month = 'Enero'
    elif month == '02':
        month = 'Febrero'
    elif month == '03':
        month = 'Marzo'
    elif month == '04':
        month = 'Abril'
    elif month == '05':
        month = 'Mayo'
    elif month == '06':
        month = 'Junio'
    elif month == '07':
        month = 'Julio'
    elif month == '08':
        month = 'Agosto'
    elif month == '09':
        month = 'Septiembre'
    elif month == '10':
        month = 'Octubre'
    elif month == '11':
        month = 'Noviembre'
    elif month == '12':
        month = 'Diciembre'

    a = '%s de %s de %s a las %s' %(date_time.strftime('%d'), month, date_time.strftime('%Y'), date_time.strftime('%H:%M'))
    return a

class PublishedProject(models.Model):
    publication_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=4000)
    user = models.ForeignKey(Usuario)
    project = models.ForeignKey(Proyecto)

    def str_publication_date(self):
        return str_date_time(self.publication_date)


class CommentPublishedProject(models.Model):
    publication_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=4000)
    user = models.ForeignKey(Usuario)
    published = models.ForeignKey(PublishedProject)

    def str_publication_date(self):
        return str_date_time(self.publication_date)

#### #### MODULO PLANES #### ####




###### Modulo de sugerencias ######
#Buzon de sugerencias
SUGERENCIAS_MODULOS_CHOICES = (('DOCUMENTOS', 'DOCUMENTOS'),
                                    ('USUARIOS', 'USUARIOS'),
                                    ('PROVEEDORES', 'PROVEEDORES'),
                                    ('SUMINISTROS', 'SUMINISTROS'),
                                    ("APU'S MAESTROS", "APU'S MAESTROS"),
                                    ('PROYECTOS', 'PROYECTOS'),
                                    ("APU'S DE PROYECTO", "APU'S DE PROYECTO"),
                                    ('REQUISICIONES', 'REQUISICIONES'),
                                    ('COTIZACIONES MATERIALES', 'COTIZACIONES MATERIALES'),
                                    ('ORDENES DE COMPRA', 'ORDENES DE COMPRA'),
                                    ('INFORMES DE RECEPCION', 'INFORMES DE RECEPCION'),
                                    ('SALIDAS DE ALMACEN', 'SALIDAS DE ALMACEN'),
                                    ('COTIZACIONES ORDEN DE SERVICIO', 'COTIZACIONES ORDEN DE SERVICIO'),
                                    ('ORDENES DE SERVICIO', 'ORDENES DE SERVICIO'),
                                    ('CORTES DIARIOS DE OBRA', 'CORTES DIARIOS DE OBRA'),
                                    ('ACTAS RECIBO DE OBRA', 'ACTAS RECIBO DE OBRA'))

class BuzonSugerencias(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    modulo = models.CharField(max_length=40, choices=SUGERENCIAS_MODULOS_CHOICES, default='DOCUMENTOS')
    observaciones = models.TextField()
    notificacion = models.BooleanField(default=True)
    estado = models.SmallIntegerField(default=1) #Estado de la segerencia: 1-En estudio, 2-Aprobada, 3-No opera
    usuario = models.ForeignKey(Usuario)