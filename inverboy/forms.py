# -*- encoding: utf-8 -*-

from inverboy.models import *
from django import forms
from django.contrib.admin import widgets
from django.forms.widgets import *

# FECHA
import datetime
import time
from datetime import date

# VALIDACIONES PERSONALIZADAS
from django.core.exceptions import ValidationError

# EXPRESIONES REGULARES
import re

#VALIDACIONES
from inverboy.validaciones.validaciones import *

#from validator.core import Validator, Field
#from validator.rules import *

## VALIDACIONES
def validate_trim(value):
    if normaliza(value.lower()).strip() == '':
        raise ValidationError(u'Este campo es obligatorio.')
        #return True


def normaliza(cadena):
    from unicodedata import normalize
    decomposed = normalize("NFKD", cadena)
    return ''.join(c for c in decomposed if ord(c)<0x7f)


class LoginForm(forms.Form):
    user = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Usuario'}),)
    clave = forms.CharField(widget=widgets.forms.PasswordInput(attrs={'placeholder': '********'}), max_length=30,)


class BusquedaForm(forms.Form):
    criterio = forms.CharField()


CARGO_USUARIO_CHOICES = (('0', '----'),
                         ('ADMINISTRADOR AGENCIA', 'ADMINISTRADOR AGENCIA'),
                         ('ALMACENISTA', 'ALMACENISTA'),
                         ('ANALISTAS DE DESARROLLO', 'ANALISTAS DE DESARROLLO'),
                         ('ARQUITECTO EXPERTO', 'ARQUITECTO EXPERTO'),
                         ('ARQUITECTO CREATIVO', 'ARQUITECTO CREATIVO'),
                         ('ASESOR COMERCIAL', 'ASESOR COMERCIAL'),
                         ('ASESOR JURIDICO', 'ASESOR JURIDICO'),
                         ('ASISTENTE DE COMPRAS', 'ASISTENTE DE COMPRAS'),
                         ('AUDITOR COMERCIAL', 'AUDITOR COMERCIAL'),
                         ('AUDITOR DE CALIDAD', 'AUDITOR DE CALIDAD'),
                         ('AUDITOR DE RECURSOS', 'AUDITOR DE RECURSOS'),
                         ('AUXILIAR ADMINISTRATIVA', 'AUXILIAR ADMINISTRATIVA'),
                         ('AUXILIAR DE CONTABILIDAD', 'AUXILIAR DE CONTABILIDAD'),
                         ('CONTADOR', 'CONTADOR'),
                         ('COORDINADOR SISOMA', 'COORDINADOR SISOMA'),
                         ('DIRECTOR COMERCIAL', 'DIRECTOR COMERCIAL'),
                         ('DIRECTOR DE COMPRAS Y CONTRATACION', 'DIRECTOR DE COMPRAS Y CONTRATACION'),
                         ('DIRECTOR DE CONCRETOS', 'DIRECTOR DE CONCRETOS'),
                         ('DIRECTOR DE DESARROLLO', 'DIRECTOR DE DESARROLLO'),
                         ('DIRECTOR DE DISEÑO Y DESARROLLO', 'DIRECTOR DE DISEÑO Y DESARROLLO'),
                         ('DIRECTOR DE OBRA', 'DIRECTOR DE OBRA'),
                         ('DIRECTOR DE TICS', 'DIRECTOR DE TICS'),
                         ('DIRECTOR RRHH', 'DIRECTOR RRHH'),
                         ('GERENTE ADMINISTRATIVO', 'GERENTE ADMINISTRATIVO'),
                         ('GERENTE COMERCIAL', 'GERENTE COMERCIAL'),
                         ('GERENTE DE PLANEACION Y CONTRALORIA', 'GERENTE DE PLANEACION Y CONTRALORIA'),
                         ('GERENTE FINANCIERO', 'GERENTE FINANCIERO'),
                         ('GERENTE GENERAL', 'GERENTE GENERAL'),
                         ('GESTOR DE CALIDAD', 'GESTOR DE CALIDAD'),
                         ('RESIDENTE ADMINISTRATIVA', 'RESIDENTE ADMINISTRATIVA'),
                         ('RESIDENTE DE CONTRALORIA', 'RESIDENTE DE CONTRALORIA'),
                         ('RESIDENTE DE OBRA', 'RESIDENTE DE OBRA'),
                         ('SOPORTE TECNICO', 'SOPORTE TECNICO'),
                         ('TALENTO HUMANO', 'TALENTO HUMANO'),
                         ('TESORERIA', 'TESORERIA'),
                         ('DIRECTOR DE COSTOS DE PRESUPUESTO','DIRECTOR DE COSTOS DE PRESUPUESTO'))


#### Formularios Base ####
# Formulario base
class BaseForm(forms.Form):

    # Elimina los espacios en blanco del formulario (trim)
    def _clean_fields(self):
        from django.db.models import FileField

        for name, field in self.fields.items():
            # value_from_datadict() gets the data from the data dictionaries.
            # Each widget type knows how to retrieve its own data, because some
            # widgets split data over several HTML fields.
            value = field.widget.value_from_datadict(self.data, self.files,
                self.add_prefix(name))

            try:
                if isinstance(field, FileField):
                    initial = self.initial.get(name, field.initial)
                    value = field.clean(value, initial)
                else:
                    if isinstance(value, basestring):
                        value = field.clean(value.strip())
                    else:
                        value = field.clean(value)
                self.cleaned_data[name] = value
                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value
            except ValidationError, e:
                self._errors[name] = self.error_class(e.messages)
                if name in self.cleaned_data:
                    del self.cleaned_data[name]


# Formulario base (ModelForm)
class BaseModelForm(forms.ModelForm):

    # Elimina los espacios en blanco del formulario (trim)
    def _clean_fields(self):
        from django.db.models import FileField

        for name, field in self.fields.items():
            # value_from_datadict() gets the data from the data dictionaries.
            # Each widget type knows how to retrieve its own data, because some
            # widgets split data over several HTML fields.
            value = field.widget.value_from_datadict(self.data, self.files,
                self.add_prefix(name))

            try:
                if isinstance(field, FileField):
                    initial = self.initial.get(name, field.initial)
                    value = field.clean(value, initial)
                else:
                    if isinstance(value, basestring):
                        value = field.clean(value.strip())
                    else:
                        value = field.clean(value)
                self.cleaned_data[name] = value
                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value
            except ValidationError, e:
                self._errors[name] = self.error_class(e.messages)
                if name in self.cleaned_data:
                    del self.cleaned_data[name]
#### Formularios Base ####



class UsuarioForm(forms.Form):
    identificacion = forms.IntegerField()
    nombre_usuario = forms.CharField(max_length=30, validators=[validate_trim], )
    nombres = forms.CharField(max_length=30)
    apellidos = forms.CharField(max_length=30)
    fecha_nacimiento = forms.CharField()
    departamento = forms.ModelChoiceField(Departamento.objects.all())
    municipio = forms.ModelChoiceField(Municipio.objects.all())
    direccion = forms.CharField(max_length=30)
    cargo = forms.ChoiceField(widget=Select, choices=CARGO_USUARIO_CHOICES) # Cargo
    telefono = forms.CharField(required=False)
    celular = forms.IntegerField()
    grupo_usuario = forms.ModelChoiceField(Group.objects.all())
    estado = forms.BooleanField(initial=1, required=False)
    conservar_contrasena = forms.BooleanField(required=False)
    contrasena = forms.CharField(widget=widgets.forms.PasswordInput, max_length=30, required=False)
    confirmar_contrasena = forms.CharField(widget=widgets.forms.PasswordInput, max_length=30, required=False)
    def clean(self):
        cleaned_data = super(UsuarioForm, self).clean()
        # Validación de digitos de identificación
        identificacion = None
        try:
            identificacion = self.cleaned_data['identificacion']
        except:
            pass
        if identificacion != None:
            error_identificacion = validar_identificacion(str(identificacion))
            if error_identificacion != '':
                self._errors['identificacion'] = self.error_class([error_identificacion])
        # Validación nombre de usuario
        nombre_usuario = None
        try:
            nombre_usuario = self.cleaned_data['nombre_usuario'].strip()
        except:
            pass
        if nombre_usuario != None:
            error_nombre_usuario = validar_cadena_caracteres_especiales_acentos_espacios(nombre_usuario)
            if error_nombre_usuario != '':
                self._errors['nombre_usuario'] = self.error_class([error_nombre_usuario])
        # Validación nombres
        nombres = None
        try:
            nombres = self.cleaned_data['nombres'].strip()
        except:
            pass
        if nombres != None:
            error_nombres = validar_cadena_caracteres_especiales(nombres)
            if error_nombres != '':
                self._errors['nombres'] = self.error_class([error_nombres])
        # Validación apellidos
        apellidos = None
        try:
            apellidos = self.cleaned_data['apellidos'].strip()
        except:
            pass
        if apellidos != None:
            error_apellidos = validar_cadena_caracteres_especiales(apellidos)
            if error_apellidos != '':
                self._errors['apellidos'] = self.error_class([error_apellidos])
        # Validación de digitos de celular
        celular = None
        try:
            celular = self.cleaned_data['celular']
        except:
            pass
        if celular != None:
            error_celular = validar_celular(str(celular))
            if error_celular != '':
                self._errors['celular'] = self.error_class([error_celular])
        # Validación de digitos de telefono
        telefono = None
        try:
            telefono = self.cleaned_data['telefono'].strip()
        except:
            pass
        if telefono != None:
            if telefono != '':
                error_telefono = validar_telefono(telefono)
                if error_telefono != '':
                    self._errors['telefono'] = self.error_class([error_telefono])
        # Validación fecha de nacimiento
        fecha_nacimiento = None
        try:
            fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        except:
            pass
        if fecha_nacimiento != None:
            error_fecha = validar_fecha(unicode((fecha_nacimiento)))
            if error_fecha == '':
                fecha_nacimiento = time.strptime(fecha_nacimiento, '%Y-%m-%d')
                hoy = date.today()
                hoy = time.strptime(hoy.strftime('%Y-%m-%d'), '%Y-%m-%d')
                if fecha_nacimiento > hoy:
                    error_fecha = 'La fecha de nacimiento no debe ser mayor a la fecha actual'
            if error_fecha != '':
                self._errors['fecha_nacimiento'] = self.error_class([error_fecha])
        # Validación dirección
        direccion = None
        try:
            direccion = self.cleaned_data['direccion'].strip()
        except:
            pass
        if direccion != None:
            error_direccion = validar_cadena(direccion)
            if error_direccion == '':
                error_direccion = validar_cadena_caracteres_especiales(direccion)
            if error_direccion != '':
                self._errors['direccion'] = self.error_class([error_direccion])
        # Validación de digitos de cargo
        if self.cleaned_data['cargo'] == '0':
            msg = u'Este campo es obligatorio.'
            self._errors['cargo'] = self.error_class([msg])
        # Validación de contraseñas
        conservar_contrasena = None
        try:
            conservar_contrasena = self.cleaned_data["conservar_contrasena"]
        except :
            pass
            
        if conservar_contrasena == None or conservar_contrasena == False:
            contrasena = cleaned_data.get("contrasena")
            confirmar_contrasena = cleaned_data.get("confirmar_contrasena")
            if contrasena != confirmar_contrasena:
                msg = u"Las contraseñas no coinciden."
                self._errors["contrasena"] = self.error_class([msg])
            else:
                try:
                    if not re.search('(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$', contrasena):
                        msg = u"Digite una contraseña segura, que contenga minimo 8 caracteres: que contenga por lo menos una letra Mayuscula, una Minuscula, un Numero ó un caracter especial."
                        self._errors["contrasena"] = self.error_class([msg])
                except:
                    pass
        return cleaned_data
    

## Modificar informacion del usuario
class ModificarUsuarioForm(forms.Form):
    contrasena_anterior = forms.CharField(widget=widgets.forms.PasswordInput, max_length=30, )
    contrasena = forms.CharField(widget=widgets.forms.PasswordInput, max_length=30, )
    confirmar_contrasena = forms.CharField(widget=widgets.forms.PasswordInput, max_length=30)
    def clean(self):
        cleaned_data = super(ModificarUsuarioForm, self).clean()
        # VALIDACION CONTRASEÑAS
        contrasena = cleaned_data.get("contrasena")
        confirmar_contrasena = cleaned_data.get("confirmar_contrasena")
        if contrasena != confirmar_contrasena:
            msg = u"Las contraseñas no coinciden."
            self._errors["contrasena"] = self.error_class([msg])
        else:
            try:
                if not re.search('(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$', contrasena):
                    msg = u"Digite una contraseña segura, que contenga minimo 8 caracteres: que contenga por lo menos una letra Mayuscula, una Minuscula, un Numero ó un caracter especial."
                    self._errors["contrasena"] = self.error_class([msg])
            except:
                pass
        return cleaned_data


# PERMISOS MODULOS SEGUN BD
PERMISOS_MODULO_USUARIOS_CHOICES = (('add_usuario', 'Crear'),
                            ('change_usuario', 'Modificar'),
                            ('view_usuario', 'Lectura'))

PERMISOS_MODULO_GRUPOS_CHOICES = (('add_group', 'Crear'),
                            ('change_group', 'Modificar'),
                            ('view_group', 'Lectura'))

PERMISOS_MODULO_PROVEEDORES_CHOICES = (('add_proveedor', 'Crear'),
                            ('change_proveedor', 'Modificar'),
                            ('view_proveedor', 'Lectura'))

PERMISOS_MODULO_CATEGORIAS_CHOICES = (('add_categoria', 'Crear'),
                            ('change_categoria', 'Modificar'),
                            ('view_categoria', 'Lectura'))

PERMISOS_MODULO_SUMINISTROS_CHOICES = (('add_suministro', 'Crear'),
                            ('change_suministro', 'Modificar'),
                            ('view_suministro', 'Lectura'))

PERMISOS_MODULO_CAPITULOS_CHOICES = (('add_capitulo', 'Crear'),
                            ('change_capitulo', 'Modificar'),
                            ('view_capitulo', 'Lectura'))

PERMISOS_MODULO_APU_CHOICES = (('add_apu', 'Crear'),
                            ('change_apu', 'Modificar'),
                            ('view_apu', 'Lectura'))

PERMISOS_MODULO_PROYECTOS_CHOICES = (('add_proyecto', 'Crear'),
                            ('change_proyecto', 'Modificar'),
                            ('view_proyecto', 'Lectura'))

PERMISOS_MODULO_PERSONAL_ADMINISTRATIVO_PROYECTO_CHOICES = (('add_personaadministrativoproyecto', 'Crear'),
                            ('change_personaadministrativoproyecto', 'Desvincular'),
                            ('view_personaadministrativoproyecto', 'Lectura'))

PERMISOS_MODULO_PERSONAL_ANEXO_PROYECTO_CHOICES = (('add_personaproyecto', 'Crear'),
                            ('change_personaproyecto', 'Eliminar'),
                            ('view_personaproyecto', 'Lectura'))

PERMISOS_MODULO_CAPITULO_APU_PROYECTO_CHOICES = (('add_capituloapuproyecto', 'Crear'),
                            ('change_capituloapuproyecto', 'Modificar'),
                            ('view_capituloapuproyecto', 'Lectura'))

PERMISOS_MODULO_APU_PROYECTO_CHOICES = (('add_apuproyecto', 'Crear'),
                            ('change_apuproyecto', 'Modificar'),
                            ('view_apuproyecto', 'Lectura'))

PERMISOS_MODULO_REQUISICION_PROYECTO_CHOICES = (('add_requisicion', 'Crear'),
                            ('change_requisicion', 'Crear'),
                            ('view_requisicion', 'Lectura'),
                            ('approve_requisicion', 'Aprobar'))

PERMISOS_MODULO_COTIZACION_PROYECTO_CHOICES = (('add_cotizacion', 'Crear'),
                            ('change_cotizacion', 'Modificar'),
                            ('view_cotizacion', 'Lectura'))

PERMISOS_MODULO_ORDEN_COMPRA_PROYECTO_CHOICES = (('add_ordencompra', 'Crear'),
                            ('change_ordencompra', 'Modificar'),
                            ('view_ordencompra', 'Lectura'),
                            ('assignchangepermission_ordencompra', 'Asignar permiso para modificar'))

PERMISOS_MODULO_INFORME_RECEPCION_PROYECTO_CHOICES = (('add_informerecepcion', 'Crear'),
                            ('view_informerecepcion', 'Lectura'))

PERMISOS_MODULO_ALMACEN_PROYECTO_CHOICES = (('add_almacen', 'Crear'), ('view_suministroalmacen', 'Lectura'))

PERMISOS_MODULO_INFORME_SALIDA_PROYECTO_CHOICES = (('add_informesalida', 'Crear'),
                            ('view_informesalida', 'Lectura'))

PERMISOS_MODULO_ORDEN_SERVICIO_PROYECTO_CHOICES = (('add_ordenservicio', 'Crear'),
                            ('change_ordenservicio', 'Crear'),
                            ('view_ordenservicio', 'Lectura'),
                            ('assignchangepermission_ordenservicio', 'Asignar permiso para modificar'))

PERMISOS_MODULO_CORTE_DIARIO_OBRA_PROYECTO_CHOICES = (('add_cortediarioobra', 'Crear'),
                            ('view_cortediarioobra', 'Lectura'))

PERMISOS_MODULO_ACTA_RECIBO_OBRA_PROYECTO_CHOICES = (('add_actareciboobra', 'Crear'),
                            ('change_actareciboobra', 'Crear'),
                            ('view_actareciboobra', 'Lectura'),
                            ('approve_actareciboobra', 'Aprobar acta'),
                            ('approve_cooperativaactareciboobra', 'Aprobar'))

PERMISOS_MODULO_REQUISICION_INDIRECTOS_PROYECTO_CHOICES = (('add_requisicionindirectos', 'Crear'),
                            ('view_requisicionindirectos', 'Lectura'))

PERMISOS_MODULO_ORDEN_GIRO_PROYECTO_CHOICES = (('add_ordengiro', 'Crear'),
                            ('view_ordengiro', 'Lectura'))

PERMISOS_MODULO_ACTA_CONFORMIDAD_PROYECTO_CHOICES = (('add_actaconformidad', 'Crear'),
                            ('view_actaconformidad', 'Lectura'))

PERMISOS_MODULO_FACTURA_ORDEN_COMPRA_PROYECTO_CHOICES = (('add_facturaordencompra', 'Crear'),
                            ('view_facturaordencompra', 'Lectura'))

PERMISOS_MODULO_SECCION_PROYECTO_CHOICES = (('add_seccionproyecto', 'Crear'),
                            ('change_seccionproyecto', 'Modificar'),
                            ('view_seccionproyecto', 'Lectura'))

PERMISOS_MODULO_TIPO_INMUEBLE_CHOICES = (('add_tipoinmueble', 'Crear'),
                            ('change_tipoinmueble', 'Modificar'),
                            ('view_tipoinmueble', 'Lectura'))

PERMISOS_MODULO_INMUEBLES_CHOICES = (('add_inmueble', 'Crear'),
                            ('change_inmueble', 'Modificar'),
                            ('view_inmueble', 'Lectura'))

PERMISOS_MODULO_AGRUPACION_INMUEBLES_CHOICES = (('add_agrupacioninmueble', 'Crear'),
                            ('change_agrupacioninmueble', 'Modificar'),
                            ('view_agrupacioninmueble', 'Lectura'))

PERMISOS_MODULO_ENCUESTAS_CHOICES = (('add_encuesta', 'Crear'),
                            ('change_encuesta', 'Modificar'),
                            ('view_encuesta', 'Lectura'))

PERMISOS_MODULO_ENTIDAD_BANCARIA_CHOICES = (('add_entidadbancaria', 'Crear'),
                            ('change_entidadbancaria', 'Modificar'),
                            ('view_entidadbancaria', 'Lectura'))

PERMISOS_MODULO_ADICIONALES_AGRUPACION_INMUEBLE_CHOICES = (('add_adicionalagrupacion', 'Crear'),
                            ('change_adicionalagrupacion', 'Modificar'),
                            ('view_adicionalagrupacion', 'Lectura'))

PERMISOS_MODULO_CLIENTES_CHOICES = (('add_cliente', 'Crear'),
                            ('change_cliente', 'Modificar'),
                            ('view_cliente', 'Lectura'))

PERMISOS_MODULO_CONTRATO_VENTA_CHOICES = (('add_contratoventa', 'Crear'),
                            ('change_contratoventa', 'Modificar'),
                            ('view_contratoventa', 'Lectura'),
                            ('validate_paymentcontratoventa', 'Validar pagos contrato venta'),
                            ('assignchangepermission_contratoventa', 'Asignar permiso para modificar'))

PERMISOS_MODULO_DOCUMENTOS_VENTA_CHOICES = (('add_documentoventa', 'Editar documento venta'),
                            ('view_documentoventa', 'Lectura documento venta'))

PERMISOS_MODULO_REPORTE_FOTOGRAFICO_PROYECTO_CHOICES = (('create_setup', 'Crear setup'),
                            ('upload_chronologicalpicture', 'Actualizar fotografias'),
                            ('delete_chronologicalpicture', 'Eliminar fotografias'),
                            ('view_stage', 'Visualizar reporte'))

#Permisos Juridico
PERMISOS_MODULO_JURIDICO_CHOICES = (('juridico', 'Juridico'),
                                    ('modificar_juridico', 'Modificar'))

class GrupoForm(forms.Form):
    nombre_grupo = forms.CharField()
    modulo_usuarios = forms.MultipleChoiceField(choices=PERMISOS_MODULO_USUARIOS_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_grupos = forms.MultipleChoiceField(choices=PERMISOS_MODULO_GRUPOS_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_proveedores = forms.MultipleChoiceField(choices=PERMISOS_MODULO_PROVEEDORES_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_categorias = forms.MultipleChoiceField(choices=PERMISOS_MODULO_CATEGORIAS_CHOICES, widget=forms.CheckboxSelectMultiple, required=False, label='Modulo clasificación de suministros')
    modulo_suministros = forms.MultipleChoiceField(choices=PERMISOS_MODULO_SUMINISTROS_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_capitulos = forms.MultipleChoiceField(choices=PERMISOS_MODULO_CAPITULOS_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_apu = forms.MultipleChoiceField(choices=PERMISOS_MODULO_APU_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_proyectos = forms.MultipleChoiceField(choices=PERMISOS_MODULO_PROYECTOS_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_personal_administrativo_proyecto = forms.MultipleChoiceField(choices=PERMISOS_MODULO_PERSONAL_ADMINISTRATIVO_PROYECTO_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_personal_anexo_proyecto = forms.MultipleChoiceField(choices=PERMISOS_MODULO_PERSONAL_ANEXO_PROYECTO_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_capitulos_apu_proyecto = forms.MultipleChoiceField(choices=PERMISOS_MODULO_CAPITULO_APU_PROYECTO_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_apu_proyecto = forms.MultipleChoiceField(choices=PERMISOS_MODULO_APU_PROYECTO_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_requisiciones = forms.MultipleChoiceField(choices=PERMISOS_MODULO_REQUISICION_PROYECTO_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_cotizaciones = forms.MultipleChoiceField(choices=PERMISOS_MODULO_COTIZACION_PROYECTO_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_orden_compra = forms.MultipleChoiceField(choices=PERMISOS_MODULO_ORDEN_COMPRA_PROYECTO_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_informe_recepcion = forms.MultipleChoiceField(choices=PERMISOS_MODULO_INFORME_RECEPCION_PROYECTO_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_almacen = forms.MultipleChoiceField(choices=PERMISOS_MODULO_ALMACEN_PROYECTO_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_informe_salida = forms.MultipleChoiceField(choices=PERMISOS_MODULO_INFORME_SALIDA_PROYECTO_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_orden_servicio = forms.MultipleChoiceField(choices=PERMISOS_MODULO_ORDEN_SERVICIO_PROYECTO_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_corte_diario_obra = forms.MultipleChoiceField(choices=PERMISOS_MODULO_CORTE_DIARIO_OBRA_PROYECTO_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_acta_recibo_obra = forms.MultipleChoiceField(choices=PERMISOS_MODULO_ACTA_RECIBO_OBRA_PROYECTO_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_requisiciones_indirectos = forms.MultipleChoiceField(choices=PERMISOS_MODULO_REQUISICION_INDIRECTOS_PROYECTO_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_orden_giro = forms.MultipleChoiceField(choices=PERMISOS_MODULO_ORDEN_GIRO_PROYECTO_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_acta_conformidad = forms.MultipleChoiceField(choices=PERMISOS_MODULO_ACTA_CONFORMIDAD_PROYECTO_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_factura_orden_compra = forms.MultipleChoiceField(choices=PERMISOS_MODULO_FACTURA_ORDEN_COMPRA_PROYECTO_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_encuestas = forms.MultipleChoiceField(choices=PERMISOS_MODULO_ENCUESTAS_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_entidad_bancaria = forms.MultipleChoiceField(choices=PERMISOS_MODULO_ENTIDAD_BANCARIA_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_seccion_proyecto = forms.MultipleChoiceField(choices=PERMISOS_MODULO_SECCION_PROYECTO_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_tipo_inmueble = forms.MultipleChoiceField(choices=PERMISOS_MODULO_TIPO_INMUEBLE_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_inmuebles = forms.MultipleChoiceField(choices=PERMISOS_MODULO_INMUEBLES_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_agrupacion_inmuebles = forms.MultipleChoiceField(choices=PERMISOS_MODULO_AGRUPACION_INMUEBLES_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_adicionales_agrupacion_inmueble = forms.MultipleChoiceField(choices=PERMISOS_MODULO_ADICIONALES_AGRUPACION_INMUEBLE_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_clientes = forms.MultipleChoiceField(choices=PERMISOS_MODULO_CLIENTES_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_contrato_venta = forms.MultipleChoiceField(choices=PERMISOS_MODULO_CONTRATO_VENTA_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_documentos_venta = forms.MultipleChoiceField(choices=PERMISOS_MODULO_DOCUMENTOS_VENTA_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    modulo_reporte_fotografico = forms.MultipleChoiceField(choices=PERMISOS_MODULO_REPORTE_FOTOGRAFICO_PROYECTO_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    #permiso juridico
    modulo_juridico = forms.MultipleChoiceField(choices=PERMISOS_MODULO_JURIDICO_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)

    def clean(self):
        cleaned_data = super(GrupoForm, self).clean()
        # Validación nombre_grupo
        nombre_grupo = None
        try:
            nombre_grupo = self.cleaned_data['nombre_grupo'].strip()
        except:
            pass
        if nombre_grupo != None:
            error_nombre_grupo = validar_cadena(nombre_grupo)
            if error_nombre_grupo == '':
                error_nombre_grupo = validar_cadena_caracteres_especiales(nombre_grupo)
            if error_nombre_grupo != '':
                self._errors['nombre_grupo'] = self.error_class([error_nombre_grupo])
        return cleaned_data


TIPO_PROVEEDOR_CHOICES = (('1', 'Persona Natural'),
                            ('2', 'Persona Juridica'))

REGIMEN_TRIBUTARIO_CHOICES = (('1', 'Común'),
                                ('2', 'Simplificado'))

class ProveedorForm(forms.Form):
    identificacion = forms.IntegerField()
    razon_social = forms.CharField(max_length=80)
    nombre_comercial = forms.CharField(max_length=40, required=False)
    tipo = forms.ChoiceField(widget=RadioSelect, choices=TIPO_PROVEEDOR_CHOICES) # Persona Natural ó Juridica
    regimen_tributario = forms.ChoiceField(widget=RadioSelect, choices=REGIMEN_TRIBUTARIO_CHOICES) # Persona Natural ó Juridica
    telefono_1 = forms.CharField()
    telefono_2 = forms.CharField(required=False)
    fax = forms.CharField(required=False)
    web_site = forms.URLField(max_length=40, required=False)
    email = forms.EmailField(max_length=40, required=False)
    observaciones = forms.CharField(widget=forms.Textarea, required=False)
    municipio = forms.ModelChoiceField(Municipio.objects.all())
    direccion = forms.CharField(max_length=30)
    estado = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super(ProveedorForm, self).clean()
        # Validación de digitos de identificación
        identificacion = None
        try:
            identificacion = self.cleaned_data['identificacion']
        except:
            pass
        if identificacion != None:
            error_identificacion = validar_identificacion(str(identificacion))
            if error_identificacion != '':
                self._errors['identificacion'] = self.error_class([error_identificacion])
        # Validación razon_social
        razon_social = None
        try:
            razon_social = self.cleaned_data['razon_social'].strip()
        except:
            pass
        if razon_social != None:
            error_razon_social = validar_cadena(razon_social)
            if error_razon_social == '':
                error_razon_social = validar_cadena_caracteres_especiales(razon_social)
            if error_razon_social != '':
                self._errors['razon_social'] = self.error_class([error_razon_social])
        # Validación nombre_comercial
        nombre_comercial = None
        try:
            nombre_comercial = self.cleaned_data['nombre_comercial'].strip()
        except:
            pass
        if nombre_comercial != None:
            if nombre_comercial.strip() != '':
                error_nombre_comercial = validar_cadena_caracteres_especiales(nombre_comercial)
                if error_nombre_comercial != '':
                    self._errors['nombre_comercial'] = self.error_class([error_nombre_comercial])
        # Validación dirección
        direccion = None
        try:
            direccion = self.cleaned_data['direccion'].strip()
        except:
            pass
        if direccion != None:
            error_direccion = validar_cadena(direccion)
            if error_direccion == '':
                error_direccion = validar_cadena_caracteres_especiales(direccion)
            if error_direccion != '':
                self._errors['direccion'] = self.error_class([error_direccion])
        # Validación de digitos de telefono_1
        telefono1 = None
        try:
            telefono1 = self.cleaned_data['telefono_1']
        except:
            pass
        if telefono1 != None:
            error_telefono1 = validar_telefono(telefono1)
            if error_telefono1 != '':
                self._errors['telefono_1'] = self.error_class([error_telefono1])
        # Validación de digitos de telefono_2
        telefono2 = None
        try:
            telefono2 = self.cleaned_data['telefono_2']
        except:
            pass
        if telefono2 != None:
            if telefono2.strip() != '':
                error_telefono2 = validar_telefono(telefono2)
                if error_telefono2 != '':
                    self._errors['telefono_2'] = self.error_class([error_telefono2])
        # Validaciòn digitos de fax
        fax = None
        try:
            fax = self.cleaned_data['fax']
        except:
            pass
        if fax != None:
            if fax != '':
                error_fax = validar_telefono(str(fax))
                if error_fax != '':
                    self._errors['fax'] = self.error_class([error_fax])
        return cleaned_data


CARGO_CONTACTO_CHOICES = (('0', '----'),
                            ('1', 'Gerente'),
                            ('2', 'Operador'),
                            ('3', 'Vendedor'))

class ContactoForm(forms.Form):
    nombre_contacto = forms.CharField(max_length=80)
    cargo_contacto = forms.ChoiceField(widget=Select, choices=CARGO_CONTACTO_CHOICES)
    telefono_contacto = forms.CharField(max_length=10)
    ext_contacto = forms.CharField(max_length=4, required=False)
    celular_contacto = forms.CharField(max_length=10, required=False)
    email_contacto = forms.EmailField(max_length=40, required=False)


class CategoriaForm(forms.Form):
    nombre = forms.CharField(max_length=40)
    estado = forms.BooleanField(required=False)
    def clean(self):
        cleaned_data = super(CategoriaForm, self).clean()
        # Validación nombre
        nombre = None
        try:
            nombre = self.cleaned_data['nombre'].strip()
        except:
            pass
        if nombre != None:
            error_nombre = validar_cadena(nombre)
            if error_nombre == '':
                error_nombre = validar_cadena_caracteres_especiales(nombre)
            if error_nombre != '':
                self._errors['nombre'] = self.error_class([error_nombre])
        return cleaned_data

class EspecificacionForm(forms.Form):
    categoria_asociada = forms.ModelChoiceField(Categoria.objects.filter(tipo=1, estado=1))
    nombre = forms.CharField(max_length=40)
    estado = forms.BooleanField(required=False)
    def clean(self):
        cleaned_data = super(EspecificacionForm, self).clean()
        # Validación nombre
        nombre = None
        try:
            nombre = self.cleaned_data['nombre'].strip()
        except:
            pass
        if nombre != None:
            error_nombre = validar_cadena(nombre)
            if error_nombre == '':
                error_nombre = validar_cadena_caracteres_especiales(nombre)
            if error_nombre != '':
                self._errors['nombre'] = self.error_class([error_nombre])
        return cleaned_data

class TipoForm(forms.Form):
    categoria = forms.ModelChoiceField(Categoria.objects.filter(tipo=1, estado=1))
    especificacion = forms.ModelChoiceField(Categoria.objects.filter(tipo=2, estado=1))
    nombre = forms.CharField(max_length=40)
    estado = forms.BooleanField(required=False)
    def clean(self):
        cleaned_data = super(TipoForm, self).clean()
        # Validación nombre
        nombre = None
        try:
            nombre = self.cleaned_data['nombre'].strip()
        except:
            pass
        if nombre != None:
            error_nombre = validar_cadena(nombre)
            if error_nombre == '':
                error_nombre = validar_cadena_caracteres_especiales(nombre)
            if error_nombre != '':
                self._errors['nombre'] = self.error_class([error_nombre])
        return cleaned_data

    
REPRESENTATIVO_SUMINISTRO_CHOICES = (('1', 'Si'),
                            ('0', 'No'))


UNIDAD_MEDIDA_SUMINISTRO_CHOICES = (('0', '----'),
                                    ('Bulto', 'Bulto'),
                                    ('Caja', 'Caja'),
                                    ('DD', 'DD'),
                                    ('Gl', 'Gl'),
                                    ('Glb', 'Glb'),
                                    ('HH', 'HH'),
                                    ('Kg', 'Kg'),
                                    ('Lb', 'Lb'),
                                    ('Lt', 'Lt'),
                                    ('m2', 'm2'),
                                    ('m3', 'm3'),
                                    ('mL', 'mL'),
                                    ('MS', 'MS'),
                                    ('Pliego', 'Pliego'),
                                    ('Quintal', 'Quintal'),
                                    ('Tn', 'Tn'),
                                    ('Tira', 'Tira'),
                                    ('Un', 'Un'))


CLASIFICACION_GENERAL_SUMINISTRO_CHOICES = (('0', '----'),
                                    ('Equipo', 'Equipo'),
                                    ('Mano de obra', 'Mano de obra'),
                                    ('Material', 'Material'),
                                    ('Transporte', 'Transporte'),
                                    ('Indirectos', 'Indirectos'),
                                    ('Plenitareas', 'Plenitareas'))


class SuministroForm(forms.Form):
    categoria = forms.ModelChoiceField(Categoria.objects.filter(tipo=1, estado=1))
    especificacion = forms.ModelChoiceField(Categoria.objects.filter(tipo=2, estado=1))
    #tipo = forms.ModelChoiceField(Categoria.objects.filter(tipo=3), required=False)
    clasificacion_general = forms.ChoiceField(widget=Select, choices=CLASIFICACION_GENERAL_SUMINISTRO_CHOICES)
    nombre = forms.CharField(max_length=80)
    sinonimos = forms.CharField(widget=forms.Textarea, required=False)
    representativo = forms.ChoiceField(widget=RadioSelect, choices=REPRESENTATIVO_SUMINISTRO_CHOICES, initial=1)
    unidad_embalaje = forms.DecimalField(decimal_places=2, min_value=0.001)
    unidad_medida = forms.ChoiceField(choices=UNIDAD_MEDIDA_SUMINISTRO_CHOICES)
    dias_compra = forms.IntegerField(min_value=1)
    requiere_cartilla = forms.BooleanField(required=False)
    peso = forms.DecimalField(required=False, decimal_places=2, min_value=0.1)
    largo = forms.DecimalField(required=False, decimal_places=2, min_value=0.1)
    alto = forms.DecimalField(required=False, decimal_places=2, min_value=0.1)
    ancho = forms.DecimalField(required=False, decimal_places=2, min_value=0.1)
    estado = forms.BooleanField(required=False)
    def clean(self):
        cleaned_data = super(SuministroForm, self).clean()
        # Validación nombre
        nombre = None
        try:
            nombre = self.cleaned_data['nombre'].strip()
        except:
            pass
        if nombre != None:
            error_nombre = validar_cadena(nombre)
            if error_nombre == '':
                error_nombre = validar_cadena_nombre_suministro(nombre)
            if error_nombre != '':
                self._errors['nombre'] = self.error_class([error_nombre])
        # Validacion de clasificacion general de suministro
        if self.cleaned_data['clasificacion_general'] == '0':
            msg = u"Este campo es obligatorio."
            self._errors["clasificacion_general"] = self.error_class([msg])
        # Validación de unidad_embalaje
        unidad_embalaje = None
        try:
            unidad_embalaje = self.cleaned_data['unidad_embalaje']
        except:
            pass
        if unidad_embalaje != None:
            error_unidad_embalaje = validar_cantidad_float_digitos(str(unidad_embalaje))
            if error_unidad_embalaje != '':
                self._errors['unidad_embalaje'] = self.error_class([error_unidad_embalaje])
        # Validación dias_compra
        dias_compra = None
        try:
            dias_compra = self.cleaned_data['dias_compra']
        except:
            pass
        if dias_compra != None:
            error_dias_compra = validar_int_digitos(dias_compra, 9)
            if error_dias_compra != '':
                self._errors['dias_compra'] = self.error_class([error_dias_compra])
        # Validación de unidad de medida de suministro
        if self.cleaned_data['unidad_medida'] == '0':
            msg = u"Este campo es obligatorio."
            self._errors["unidad_medida"] = self.error_class([msg])
        # Validación de peso
        peso = None
        try:
            peso = self.cleaned_data['peso']
        except:
            pass
        if peso != None:
            error_peso = validar_cantidad_float_digitos(str(peso))
            if error_peso != '':
                self._errors['peso'] = self.error_class([error_peso])
        # Validación de largo
        largo = None
        try:
            largo = self.cleaned_data['largo']
        except:
            pass
        if largo != None:
            error_largo = validar_cantidad_float_digitos(str(largo))
            if error_largo != '':
                self._errors['largo'] = self.error_class([error_largo])
        # Validación de alto
        alto = None
        try:
            alto = self.cleaned_data['alto']
        except:
            pass
        if alto != None:
            error_alto = validar_cantidad_float_digitos(str(alto))
            if error_alto != '':
                self._errors['alto'] = self.error_class([error_alto])
        # Validación de ancho
        ancho = None
        try:
            ancho = self.cleaned_data['ancho']
        except:
            pass
        if ancho != None:
            error_ancho = validar_cantidad_float_digitos(str(ancho))
            if error_ancho != '':
                self._errors['ancho'] = self.error_class([error_ancho])
        return cleaned_data


class CapituloForm(forms.Form):
    nombre = forms.CharField(max_length=40)
    estado = forms.BooleanField(required=False)
    def clean(self):
        cleaned_data = super(CapituloForm, self).clean()
        # Validación nombre
        nombre = None
        try:
            nombre = self.cleaned_data['nombre'].strip()
        except:
            pass
        if nombre != None:
            error_nombre = validar_cadena(nombre)
            if error_nombre == '':
                error_nombre = validar_cadena_caracteres_especiales(nombre)
            if error_nombre != '':
                self._errors['nombre'] = self.error_class([error_nombre])
        return cleaned_data


class SubCapituloForm(forms.Form):
    capitulo_asociado = forms.ModelChoiceField(Capitulo.objects.filter(tipo_capitulo=1, estado_capitulo=1))
    codigo = forms.IntegerField(required=False)
    nombre = forms.CharField(max_length=40)
    estado = forms.BooleanField(required=False)
    def clean(self):
        cleaned_data = super(SubCapituloForm, self).clean()
        # Validación nombre
        nombre = None
        try:
            nombre = self.cleaned_data['nombre'].strip()
        except:
            pass
        if nombre != None:
            error_nombre = validar_cadena(nombre)
            if error_nombre == '':
                error_nombre = validar_cadena_caracteres_especiales(nombre)
            if error_nombre != '':
                self._errors['nombre'] = self.error_class([error_nombre])
        return cleaned_data


UNIDAD_MEDIDA_APU_CHOICES = (('0', '----'),
                                    ('Glb', 'Glb'),
                                    ('Kg', 'Kg'),
                                    ('m2', 'm2'),
                                    ('m3', 'm3'),
                                    ('mL', 'mL'),
                                    ('Un', 'Un'))


class ApuForm(forms.Form):
    capitulo = forms.ModelChoiceField(Capitulo.objects.filter(tipo_capitulo=1, estado_capitulo=1))
    #subcapitulo = forms.ModelChoiceField(Capitulo.objects.filter(tipo_capitulo=2, estado_capitulo=1), required=False)
    nombre = forms.CharField(max_length=60)
    unidad_medida = forms.ChoiceField(choices=UNIDAD_MEDIDA_APU_CHOICES)
    estado = forms.BooleanField(required=False)
    def clean(self):
        cleaned_data = super(ApuForm, self).clean()
        # Validación nombre
        nombre = None
        try:
            nombre = self.cleaned_data['nombre'].strip()
        except:
            pass
        if nombre != None:
            error_nombre = validar_cadena(nombre)
            if error_nombre == '':
                error_nombre = validar_cadena_nombre_apu(nombre)
            if error_nombre != '':
                self._errors['nombre'] = self.error_class([error_nombre])

        # Validación unidad_medida
        if self.cleaned_data['unidad_medida'] == '0':
            msg = u"Este campo es obligatorio."
            self._errors["unidad_medida"] = self.error_class([msg])
        return cleaned_data


class BusquedaApuform(forms.Form):
    #capitulo = forms.ModelChoiceField(Capitulo.objects.filter(tipo_capitulo=1, estado_capitulo=1), required=False)
    #subcapitulo = forms.ModelChoiceField(Capitulo.objects.filter(tipo_capitulo=2, estado_capitulo=1), required=False)
    criterio = forms.CharField(max_length=60, required=False)
    def clean(self):
        cleaned_data = super(BusquedaApuform, self).clean()
        #Validación del criterio en la busqueda, si son espacios en blanco deja el campo vacio
        if self.cleaned_data['criterio'].strip() == '':
            self.criterio = ''
        return cleaned_data


class ProyectoForm(BaseModelForm):
    departamento = forms.ModelChoiceField(Departamento.objects.all(), widget=forms.Select(attrs={'onchange': "Dajaxice.aplicacion.inverboy.cargar_municipios('Dajax.process',{'option':this.value, 'elemento': 'id_municipio'})"}), required=False)

    class Meta:
        model = Proyecto
        fields = ('nombre', 'iniciales', 'direccion', 'ext', 'tipo_proyecto', 'rete_ica', 'rete_fuente', 'municipio')

    def __init__(self, *args, **kwargs):
        super(ProyectoForm, self).__init__(*args, **kwargs)

        self.fields['rete_ica'] = forms.DecimalField(max_digits=5, decimal_places=2, min_value=0.0, max_value=100, required=False)
        self.fields['rete_fuente'] = forms.DecimalField(max_digits=5, decimal_places=2, min_value=0.0, max_value=100, required=False)

        # Carga los municipios de acuerdo al departamento seleccionado
        if args or kwargs:
            if args:
                departamento = args[0]['departamento']
            else:
                try:
                    departamento = kwargs['data']['departamento']
                except:
                    departamento = kwargs['initial']['departamento']

            if departamento == '':
                self.fields['municipio'].queryset = Municipio.objects.filter(id=0)
            else:
                self.fields['municipio'].queryset = Municipio.objects.filter(departamento=departamento)
        else:
            self.fields['municipio'].queryset = Municipio.objects.filter(id=0)

        # Chosen
        self.fields['departamento'].widget.attrs['data-placeholder'] = 'Seleccione..'
        self.fields['departamento'].widget.attrs['class'] = 'chosen-select'
        self.fields['departamento'].widget.attrs['style'] = 'width:350px;'

        # Chosen
        self.fields['municipio'].widget.attrs['data-placeholder'] = 'Seleccione..'
        self.fields['municipio'].widget.attrs['class'] = 'chosen-select'
        self.fields['municipio'].widget.attrs['style'] = 'width:350px;'

    def clean(self):
        cleaned_data = super(ProyectoForm, self).clean()

        fields = []

        # Validación nombre
        nombre = None
        try:
            nombre = self.cleaned_data['nombre'].strip()
        except:
            pass
        if nombre != None:
            """
            fields.append(Field('nombre', nombre).append([
                IsRequired(error='Este campo es obligatorio.'), Regex(u"^[áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))"""
            pass

        # Validación iniciales
        iniciales = None
        try:
            iniciales = self.cleaned_data['iniciales'].strip()
        except:
            pass
        if iniciales != None:
            """
            fields.append(Field('iniciales', iniciales).append([
                IsRequired('Este campo es obligatorio.'), Regex(u"^[áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))"""
            pass

        # Validación tipo_proyecto
        tipo_proyecto = None
        try:
            tipo_proyecto = self.cleaned_data['tipo_proyecto'].strip()
        except:
            pass
        if tipo_proyecto != None:

            #fields.append(Field('tipo_proyecto', tipo_proyecto).append([
            #    IsRequired('Este campo es obligatorio.'), Regex(u"^[áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            #]))
            pass

        # Validación direccion
        direccion = None
        try:
            direccion = self.cleaned_data['direccion'].strip()
        except:
            pass
        if direccion != None:
            #fields.append(Field('direccion', direccion).append([
            #    IsRequired('Este campo es obligatorio.'), Regex(u"^[ A-Za-z0-9]+$", error='El campo no tiene el formato correcto.'),
            #]))
            pass

        # Validación ext
        ext = None
        try:
            ext = self.cleaned_data['ext']
        except:
            pass
        if ext != None:
            #fields.append(Field('ext', str(ext)).append([
            #    IsRequired('Este campo es obligatorio.'), Regex(u"^[0-9]{1,3}$", error='El campo no tiene el formato correcto.'),
            #]))
            pass

        #validations = Validator().append(fields).run(True)

        """for validation in validations:
            if validation['passed'] == False:
                self._errors[validation['field']] = self.error_class(validation['errors'])
        """

        return cleaned_data


class BusquedaApuProyectoform(forms.Form):
    #capitulo = forms.ModelChoiceField(CapituloApuProyecto.objects.filter(tipo_capitulo=1, estado_capitulo=1), required=False)
    #subcapitulo = forms.ModelChoiceField(Capitulo.objects.filter(tipo_capitulo=2, estado_capitulo=1), required=False)
    criterio = forms.CharField(max_length=200, required=False)
    def clean(self):
        cleaned_data = super(BusquedaApuProyectoform, self).clean()
        # VALIDACION DE VALOR CRITERIO EN LA BUSQUEDA SI SON ESPACIOS DEJA EL CAMPO VACIO
        if self.cleaned_data['criterio'].strip() == '':
            self.criterio = ''
        return cleaned_data


class CapituloApuProyectoForm(forms.Form):
    codigo = forms.IntegerField(min_value=1)
    nombre = forms.CharField(max_length=40)
    estado = forms.BooleanField(required=False)
    def clean(self):
        cleaned_data = super(CapituloApuProyectoForm, self).clean()
        # Validación codigo
        codigo = None
        try:
            codigo = self.cleaned_data['codigo']
        except:
            pass
        if codigo != None:
            error_codigo = validar_int_4digitos(str(codigo))
            if error_codigo != '':
                self._errors['codigo'] = self.error_class([error_codigo])
        # Validación nombre
        nombre = None
        try:
            nombre = self.cleaned_data['nombre'].strip()
        except:
            pass
        if nombre != None:
            error_nombre = validar_cadena(nombre)
            if error_nombre == '':
                error_nombre = validar_cadena_caracteres_especiales(nombre)
            if error_nombre != '':
                self._errors['nombre'] = self.error_class([error_nombre])
        return cleaned_data


class ApuProyectoForm(forms.Form):
    capitulo = forms.ModelChoiceField(CapituloApuProyecto.objects.filter(tipo_capitulo=1, estado_capitulo=1))
    #subcapitulo = forms.ModelChoiceField(CapituloApuProyecto.objects.filter(tipo_capitulo=2, estado_capitulo=1), required=False)
    nombre = forms.CharField(max_length=60)
    #unidad_medida = forms.CharField(required=False)
    cantidad_proyecto = forms.DecimalField(required=True, initial=1, min_value=0.1, decimal_places=2)
    cantidad_apu = forms.DecimalField(required=True, min_value=0.1, decimal_places=2)
    cantidad_total = forms.FloatField(min_value=0.1, required=False)
    valor_unitario = forms.FloatField(min_value=1, required=False)
    valor_total = forms.FloatField(min_value=1, required=False)
    apu_manejo_estandar = forms.BooleanField(required=False)
    estado = forms.BooleanField(required=False)
    
    def clean(self):
        cleaned_data = super(ApuProyectoForm, self).clean()
        # Validación nombre
        nombre = None
        try:
            nombre = self.cleaned_data['nombre'].strip()
        except:
            pass
        if nombre != None:
            error_nombre = validar_cadena(nombre)
            if error_nombre == '':
                error_nombre = validar_cadena_nombre_apu(nombre)
            if error_nombre != '':
                self._errors['nombre'] = self.error_class([error_nombre])
        # Validación de cantidad_proyecto
        cantidad_proyecto = None
        try:
            cantidad_proyecto = self.cleaned_data['cantidad_proyecto']
        except:
            pass
        if cantidad_proyecto != None:
            error_cantidad_proyecto = validar_cantidad_float_digitos(str(cantidad_proyecto))
            if error_cantidad_proyecto != '':
                self._errors['cantidad_proyecto'] = self.error_class([error_cantidad_proyecto])
        # Validación de cantidad_apu
        cantidad_apu = None
        try:
            cantidad_apu = self.cleaned_data['cantidad_apu']
        except:
            pass
        if cantidad_apu != None:
            error_cantidad_apu = validar_cantidad_float_digitos(str(cantidad_apu))
            if error_cantidad_apu != '':
                self._errors['cantidad_apu'] = self.error_class([error_cantidad_apu])
        return cleaned_data


FORMA_PAGO_ORDEN_SERVICIO = (('2', 'Contra-entrega'),
                                    ('3', 'Cortes de obra'),
                                    ('4', 'Otro'))

TIPO_IVA_ORDEN_SERVICIO = (('1', 'IVA/Utilidad'),
                                    ('2', 'Porcentaje iva'),
                                    ('3', 'IVA/AIU'))

class OrdenServicioForm(forms.Form):
    fecha_entrega = forms.DateField(input_formats=['%Y-%m-%d'])
    amortizacion_anticipo = forms.FloatField(min_value=0.0, max_value=100)
    retencion_garantia = forms.FloatField(min_value=0.0, max_value=100)
    rete_ica = forms.FloatField(min_value=0.0, max_value=100)
    rete_fuente = forms.FloatField(min_value=0.0, max_value=100)
    forma_pago = forms.ChoiceField(choices=FORMA_PAGO_ORDEN_SERVICIO) # Formas de pago: 2-Contra-entrega, 3-Cortes de obra, 4-Otro
    parametro_pago = forms.CharField(widget=forms.Textarea, required=False)
    observaciones = forms.CharField(widget=forms.Textarea, required=False)
    tipo_iva = forms.ChoiceField(choices=TIPO_IVA_ORDEN_SERVICIO, required=False) # Tipo_iva: Null - No aplica, 1 - IVA/Utilidad, 2 - porcentaje iva, 3 - IVA/AIU
    porcentaje_a_i_u = forms.FloatField(min_value=0.0, max_value=100, required=False)
    porcentaje_utilidad = forms.FloatField(min_value=0.0, max_value=100, required=False)
    porcentaje_iva = forms.FloatField(min_value=0.0, max_value=100, required=False)
    aplica_tercero = forms.BooleanField(required=False)
    tercero = forms.ModelChoiceField(Proveedor.objects.filter(estado_proveedor=True), required=False)
    aplica_cooperativa = forms.BooleanField(required=False)
    base_gravable_cooperativa = forms.FloatField(min_value=0.0, max_value=100, required=False)
    porcentaje_iva_cooperativa = forms.FloatField(min_value=0.0, max_value=100, required=False)

    def clean(self):
        import datetime

        cleaned_data = super(OrdenServicioForm, self).clean()

        campos = []

        # Validación fecha_entrega
        fecha_entrega = None
        try:
            fecha_entrega = self.cleaned_data['fecha_entrega']
        except:
            pass
        if fecha_entrega != None:
            fecha_entrega = datetime.datetime(fecha_entrega.year, fecha_entrega.month, fecha_entrega.day)
            fecha_actual = datetime.datetime.today()
            if fecha_entrega < fecha_actual:
                self._errors['fecha_entrega'] = self.error_class(['La fecha debe ser mayor o igual a la actual'])

        # Validación amortizacion_anticipo
        amortizacion_anticipo = None
        try:
            amortizacion_anticipo = self.cleaned_data['amortizacion_anticipo']
        except:
            pass
        if amortizacion_anticipo != None:
            """
            campos.append(Field('amortizacion_anticipo', str(amortizacion_anticipo)).append([
                IsRequired(error='Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
            ]))"""
            pass

        # Validación retencion_garantia
        retencion_garantia = None
        try:
            retencion_garantia = self.cleaned_data['retencion_garantia']
        except:
            pass
        if retencion_garantia != None:
            """
            campos.append(Field('retencion_garantia', str(retencion_garantia)).append([
                IsRequired(error='Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
            ]))"""
            pass

        # Validación rete_ica
        rete_ica = None
        try:
            rete_ica = self.cleaned_data['rete_ica']
        except:
            pass
        if rete_ica != None:
            """
            campos.append(Field('rete_ica', str(rete_ica)).append([
                IsRequired(error='Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
            ]))"""
            pass

        # Validación rete_fuente
        rete_fuente = None
        try:
            rete_fuente = self.cleaned_data['rete_fuente']
        except:
            pass
        if rete_fuente != None:
            """
            campos.append(Field('rete_fuente', str(rete_fuente)).append([
                IsRequired(error='Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
            ]))"""
            pass

        tipo_iva = None
        try:
            tipo_iva = self.cleaned_data['tipo_iva']
        except:
            pass

        if tipo_iva != None:
            if tipo_iva == '1':
                # Validación porcentaje_a_i_u
                porcentaje_a_i_u = ''
                try:
                    porcentaje_a_i_u = self.cleaned_data['porcentaje_a_i_u']
                except:
                    pass
                """
                campos.append(Field('porcentaje_a_i_u', str(porcentaje_a_i_u)).append([
                    IsRequired(error='Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
                ]))"""

                # Validación porcentaje_utilidad
                porcentaje_utilidad = ''
                try:
                    porcentaje_utilidad = self.cleaned_data['porcentaje_utilidad']
                except:
                    pass

                """
                campos.append(Field('porcentaje_utilidad', str(porcentaje_utilidad)).append([
                    IsRequired(error='Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
                ]))"""

                # Validación porcentaje_iva
                porcentaje_iva = ''
                try:
                    porcentaje_iva = self.cleaned_data['porcentaje_iva']
                except:
                    pass

                """
                campos.append(Field('porcentaje_iva', str(porcentaje_iva)).append([
                    IsRequired(error='Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
                ]))"""

            elif tipo_iva == '2':
                # Validación porcentaje_iva
                porcentaje_iva = ''
                try:
                    porcentaje_iva = self.cleaned_data['porcentaje_iva']
                except:
                    pass

                """
                campos.append(Field('porcentaje_iva', str(porcentaje_iva)).append([
                    IsRequired(error='Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
                ]))"""

            if tipo_iva == '3':
                # Validación porcentaje_a_i_u
                porcentaje_a_i_u = ''
                try:
                    porcentaje_a_i_u = self.cleaned_data['porcentaje_a_i_u']
                except:
                    pass

                """
                campos.append(Field('porcentaje_a_i_u', str(porcentaje_a_i_u)).append([
                    IsRequired(error='Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
                ]))"""

                # Validación porcentaje_iva
                porcentaje_iva = ''
                try:
                    porcentaje_iva = self.cleaned_data['porcentaje_iva']
                except:
                    pass

                """
                campos.append(Field('porcentaje_iva', str(porcentaje_iva)).append([
                    IsRequired(error='Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
                ]))"""

        # Validación tercero
        aplica_tercero = self.cleaned_data['aplica_tercero']
        if aplica_tercero:
            tercero = None
            try:
                tercero = self.cleaned_data['tercero']
            except :
                pass
            if tercero == None or tercero == 0:
                self._errors['tercero'] = self.error_class(['Debe seleccionar un tercero'])


        # Validación aplica_cooperativa
        aplica_cooperativa = self.cleaned_data['aplica_cooperativa']
        if aplica_cooperativa:
            # Validación base_gravable_cooperativa
            base_gravable_cooperativa = None
            try:
                base_gravable_cooperativa = self.cleaned_data['base_gravable_cooperativa']
            except:
                pass
            if base_gravable_cooperativa != None:
                """
                campos.append(Field('base_gravable_cooperativa', str(base_gravable_cooperativa)).append([
                    IsRequired(error='Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
                ]))"""
            else:
                self._errors['base_gravable_cooperativa'] = self.error_class(['Este campo es obligatorio'])

            # Validación porcentaje_iva_cooperativa
            porcentaje_iva_cooperativa = None
            try:
                porcentaje_iva_cooperativa = self.cleaned_data['porcentaje_iva_cooperativa']
            except:
                pass
            if porcentaje_iva_cooperativa != None:
                """
                campos.append(Field('porcentaje_iva_cooperativa', str(porcentaje_iva_cooperativa)).append([
                    IsRequired(error='Este campo es obligatorio.'), Regex("^[0-9]{1,10}(\.[0-9]{0,2})?$", error='La cantidad no tiene el formato correcto'),
                ]))"""
                pass
            else:
                self._errors['porcentaje_iva_cooperativa'] = self.error_class(['Este campo es obligatorio'])

        """validaciones = Validator().append(campos).run(True)

        for validacion in validaciones:
            if validacion['passed'] == False:
                self._errors[validacion['field']] = self.error_class(validacion['errors'])
        """
        return cleaned_data



#### #### MODULO DE VENTAS #### ####

# Formulario para el texto
class DocumentoVentaForm(BaseForm):
    texto = forms.CharField(widget=forms.Textarea(attrs={'rows':'40', 'cols':'100'}), required=False)

# Formulario encuesta
class EncuestaForm(BaseModelForm):

    class Meta:
        model = Encuesta
        fields = ('titulo', 'descripcion')

    def clean(self):
        cleaned_data = super(EncuestaForm, self).clean()

        fields = []

        # Validacion titulo
        titulo = None
        try:
            titulo = self.cleaned_data['titulo'].strip()
        except:
            pass
        if titulo != None:
            fields.append(Field('titulo', titulo).append([
                IsRequired(error='Este campo es obligatorio.'), Regex(u"^[áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))
            
        validations = Validator().append(fields).run(True)

        for validation in validations:
            if validation['passed'] == False:
                self._errors[validation['field']] = self.error_class(validation['errors'])

        return cleaned_data


class PreguntaEncuestaForm(BaseForm):

    texto_pregunta = forms.CharField(widget=forms.Textarea(attrs={'rows':'2', 'cols':'20'}), max_length=1000)

    def __init__(self, *args, **kwargs):
        super(PreguntaEncuestaForm, self).__init__(*args, **kwargs)
        # Campos para las respuestas de la pregunta
        if args != None:
            numero_respuestas = len(dict(args[0].iterlists())) - 1
            for consecutivo_respuestas in range(1, numero_respuestas):
                self.fields.update({'texto_respuesta_' + str(consecutivo_respuestas): forms.CharField(widget=forms.Textarea(attrs={'rows':'2', 'cols':'20'}), max_length=1000, label='Respuesta ' + str(consecutivo_respuestas))})


# Formulario encuesta
class EncuestaClienteForm(BaseForm):

    def __init__(self, encuesta=None, *args, **kwargs):
        super(EncuestaClienteForm, self).__init__(*args, **kwargs)

        # Campos para las respuestas de la pregunta
        if encuesta != None:
            for pregunta_encuesta in encuesta.lista_preguntas():
                self.fields.update({str(pregunta_encuesta.id): forms.ModelChoiceField(pregunta_encuesta.lista_respuestas(), label=pregunta_encuesta.texto, widget=forms.Select(attrs={'class':'chosen-select', 'style': 'width:350px;', }), )})


# Formulario Bancaria
class EntidadBancariaForm(BaseModelForm):

    class Meta:
        model = EntidadBancaria
        fields = ('nombre', 'estado_registro')

    def __init__(self, *args, **kwargs):
        super(EntidadBancariaForm, self).__init__(*args, **kwargs)
        if not kwargs:
            self.fields.pop('estado_registro')

    def clean(self):
        cleaned_data = super(EntidadBancariaForm, self).clean()

        fields = []

        # Validacion nombre
        nombre = None
        try:
            nombre = self.cleaned_data['nombre'].strip()
        except:
            pass
        if nombre != None:
            fields.append(Field('nombre', nombre).append([
                IsRequired(error='Este campo es obligatorio.'), Regex(u"^[áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))

        validations = Validator().append(fields).run(True)

        for validation in validations:
            if validation['passed'] == False:
                self._errors[validation['field']] = self.error_class(validation['errors'])

        return cleaned_data

    
class TipoAdicionalAgrupacionForm(BaseModelForm):

    class Meta:
        model = AdicionalAgrupacion
        fields = ('nombre',)

    def clean(self):
        cleaned_data = super(TipoAdicionalAgrupacionForm, self).clean()

        fields = []

        # Validacion nombre
        nombre = None
        try:
            nombre = self.cleaned_data['nombre'].strip()
        except:
            pass
        if nombre != None:
            fields.append(Field('nombre', nombre).append([
                IsRequired(error='Este campo es obligatorio.'), Regex(u"^[áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))

        validations = Validator().append(fields).run(True)

        for validation in validations:
            if validation['passed'] == False:
                self._errors[validation['field']] = self.error_class(validation['errors'])

        return cleaned_data

class AdicionalAgrupacionForm(BaseModelForm):

    class Meta:
        model = AdicionalAgrupacion
        fields = ('tipo_adicional', 'nombre', 'descripcion', 'valor',)

    def __init__(self, proyecto_id=None, *args, **kwargs):
        super(AdicionalAgrupacionForm, self).__init__(*args, **kwargs)

        self.fields['valor'] = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.0, initial=0)

        proyecto = Proyecto.objects.get(id=proyecto_id)

        self.fields['tipo_adicional'].required = False
        self.fields['tipo_adicional'].queryset = proyecto.lista_tipos_adicionales_agrupaciones_inmueble()

        # Chosen
        self.fields['tipo_adicional'].widget.attrs['data-placeholder'] = 'Seleccione..'
        self.fields['tipo_adicional'].widget.attrs['class'] = 'chosen-select'
        self.fields['tipo_adicional'].widget.attrs['style'] = 'width:350px;'

    def clean(self):
        cleaned_data = super(AdicionalAgrupacionForm, self).clean()

        fields = []

        # Validacion nombre
        nombre = None
        try:
            nombre = self.cleaned_data['nombre'].strip()
        except:
            pass
        if nombre != None:
            fields.append(Field('nombre', nombre).append([
                IsRequired(error='Este campo es obligatorio.'), Regex(u"^[áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))

        validations = Validator().append(fields).run(True)

        for validation in validations:
            if validation['passed'] == False:
                self._errors[validation['field']] = self.error_class(validation['errors'])

        return cleaned_data


TIPO_IDENTIFICACION_CLIENTE = (('', '-----'),
                (1, 'Cedula de ciudadania'),
                (2, 'Cedula extranjera'),
                (3, 'Nit'))

ESTADO_CIVIL = (
                (2, 'Casado - Con sociedad conyugal vigente'),
                (3, 'Casado - Con sociedad conyugal disuelta y liquidada'),
                (1, 'Soltero (a) - Sin sociedad marital'),
                (4, 'Soltero (a) - Por estado de viudez'),
                (5, 'Soltero (a) - Con sociedad marital de hecho'))

INGRESOS_MENSUALES = ((0, '----'),
                (1, 'Menos de un salario minimo'),
                (2, 'Entre 1 salario minimo y menos de 2'),
                (3, 'Entre 2 salarios minimos y menos de 4'),
                (4, 'Entre 4 salarios minimos y menos de 6'),
                (5, 'Mas de 6 salarios minimos'))

class ClienteForm(forms.Form):
    tipo_identificacion = forms.ChoiceField(choices=TIPO_IDENTIFICACION_CLIENTE) # Tipo identificacion
    identificacion = forms.IntegerField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    nombre_1 = forms.CharField(max_length=20)
    nombre_2 = forms.CharField(max_length=50, required=False)
    apellido_1 = forms.CharField(max_length=20)
    apellido_2 = forms.CharField(max_length=20, required=False)
    departamento_documento = forms.ModelChoiceField(Departamento.objects.all(), widget=forms.Select(attrs={'onchange': "Dajaxice.aplicacion.inverboy.cargar_municipios('Dajax.process',{'option':this.value, 'elemento': 'id_municipio_documento'})"}), required=False)
    municipio_documento = forms.ModelChoiceField(Municipio.objects.all())
    estado_civil = forms.ChoiceField(choices=ESTADO_CIVIL) # Estado civil
    departamento_residencia = forms.ModelChoiceField(Departamento.objects.all(), widget=forms.Select(attrs={'onchange': "Dajaxice.aplicacion.inverboy.cargar_municipios('Dajax.process',{'option':this.value, 'elemento': 'id_municipio_residencia'})"}), required=False)
    municipio_residencia = forms.ModelChoiceField(Municipio.objects.all())
    direccion_residencia = forms.CharField(max_length=30)
    telefono_1 = forms.CharField(max_length=10) # Telefono ó celular
    telefono_2 = forms.CharField(max_length=10, required=False)
    email = forms.EmailField(required=False)

    # Información laboral
    empresa = forms.CharField(max_length=40, required=False)
    telefono_empresa = forms.CharField(max_length=10, required=False) # Telefono ó celular
    extension_telefono_empresa = forms.CharField(max_length=6,required=False)
    direccion_empresa = forms.CharField(max_length=30, required=False)
    ingresos_mensuales = forms.ChoiceField(choices=INGRESOS_MENSUALES, required=False)

    observaciones = forms.CharField(widget=forms.Textarea, required=False)
    # Informacion del registro en la BD
    estado = forms.BooleanField(required=False, label='Activo')

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)

        # Carga los municipios de acuerdo al departamento seleccionado (documento, residencia)
        if args or kwargs:
            if args:
                departamento_documento = args[0]['departamento_documento']
                departamento_residencia = args[0]['departamento_residencia']
            else:
                departamento_documento = kwargs['initial']['departamento_documento']
                departamento_residencia = kwargs['initial']['departamento_residencia']

            if departamento_documento == '':
                self.fields['municipio_documento'].queryset = Municipio.objects.filter(id=0)
            else:
                self.fields['municipio_documento'].queryset = Municipio.objects.filter(departamento=departamento_documento)

            if departamento_residencia == '':
                self.fields['municipio_residencia'].queryset = Municipio.objects.filter(id=0)
            else:
                self.fields['municipio_residencia'].queryset = Municipio.objects.filter(departamento=departamento_residencia)
        else:
            self.fields['municipio_documento'].queryset = Municipio.objects.filter(id=0)
            self.fields['municipio_residencia'].queryset = Municipio.objects.filter(id=0)

        # Chosen
        self.fields['tipo_identificacion'].widget.attrs['data-placeholder'] = 'Seleccione..'
        self.fields['tipo_identificacion'].widget.attrs['class'] = 'chosen-select'
        self.fields['tipo_identificacion'].widget.attrs['style'] = 'width:350px;'

        # Chosen
        self.fields['departamento_documento'].widget.attrs['data-placeholder'] = 'Seleccione..'
        self.fields['departamento_documento'].widget.attrs['class'] = 'chosen-select'
        self.fields['departamento_documento'].widget.attrs['style'] = 'width:350px;'

        # Chosen
        self.fields['municipio_documento'].widget.attrs['data-placeholder'] = 'Seleccione..'
        self.fields['municipio_documento'].widget.attrs['class'] = 'chosen-select'
        self.fields['municipio_documento'].widget.attrs['style'] = 'width:350px;'

        # Chosen
        self.fields['departamento_residencia'].widget.attrs['data-placeholder'] = 'Seleccione..'
        self.fields['departamento_residencia'].widget.attrs['class'] = 'chosen-select'
        self.fields['departamento_residencia'].widget.attrs['style'] = 'width:350px;'

        # Chosen
        self.fields['municipio_residencia'].widget.attrs['data-placeholder'] = 'Seleccione..'
        self.fields['municipio_residencia'].widget.attrs['class'] = 'chosen-select'
        self.fields['municipio_residencia'].widget.attrs['style'] = 'width:350px;'

        # Chosen
        self.fields['estado_civil'].widget.attrs['data-placeholder'] = 'Seleccione..'
        self.fields['estado_civil'].widget.attrs['class'] = 'chosen-select'
        self.fields['estado_civil'].widget.attrs['style'] = 'width:350px;'

        # Chosen
        self.fields['ingresos_mensuales'].widget.attrs['data-placeholder'] = 'Seleccione..'
        self.fields['ingresos_mensuales'].widget.attrs['class'] = 'chosen-select'
        self.fields['ingresos_mensuales'].widget.attrs['style'] = 'width:350px;'

    def clean(self):
        cleaned_data = super(ClienteForm, self).clean()

        fields = []

        # Validacion identificacion
        identificacion = None
        try:
            identificacion = str(self.cleaned_data['identificacion']).strip()
        except:
            pass
        if identificacion != None:
            fields.append(Field('identificacion', identificacion).append([
                IsRequired(error='Este campo es obligatorio.'), Regex("^[1-9]{1}[0-9]{6,9}$", error='El campo no tiene el formato correcto.'),
            ]))

        # Validacion nombre_1
        nombre_1 = None
        try:
            nombre_1 = self.cleaned_data['nombre_1'].strip()
        except:
            pass
        if nombre_1 != None:
            fields.append(Field('nombre_1', nombre_1).append([
                IsRequired(error='Este campo es obligatorio.'), Regex(u"^[áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))

        # Validacion nombre_2
        nombre_2 = None
        try:
            nombre_2 = self.cleaned_data['nombre_2'].strip()
        except:
            pass
        if nombre_2 != None:
            if nombre_2 != '':
                fields.append(Field('nombre_2', nombre_2).append([
                    IsRequired(error='Este campo es obligatorio.'), Regex(u"^[áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
                ]))

        # Validacion apellido_1
        apellido_1 = None
        try:
            apellido_1 = self.cleaned_data['apellido_1'].strip()
        except:
            pass
        if apellido_1 != None:
            fields.append(Field('apellido_1', apellido_1).append([
                IsRequired(error='Este campo es obligatorio.'), Regex(u"^[áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))

        # Validacion apellido_2
        apellido_2 = None
        try:
            apellido_2 = self.cleaned_data['apellido_2'].strip()
        except:
            pass
        if apellido_2 != '':
            fields.append(Field('apellido_2', apellido_2).append([
                IsRequired(error='Este campo es obligatorio.'), Regex(u"^[áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))

        # Validacion direccion_residencia
        direccion_residencia = None
        try:
            direccion_residencia = self.cleaned_data['direccion_residencia'].strip()
        except:
            pass
        if direccion_residencia != None:
            fields.append(Field('direccion_residencia', direccion_residencia).append([
                IsRequired(error='Este campo es obligatorio.'), Regex("^[ A-Za-z0-9]+$", error='El campo no tiene el formato correcto.'),
            ]))

        # Validacion telefono_1
        telefono_1 = None
        try:
            telefono_1 = self.cleaned_data['telefono_1'].strip()
        except:
            pass
        if telefono_1 != None:
            fields.append(Field('telefono_1', telefono_1).append([
                IsRequired(error='Este campo es obligatorio.'), Regex("(^\({1}[0-9]{1}\){1}?[0-9]{7})|(\d{10})", error='El campo no tiene el formato correcto.'),
            ]))

        # Validacion telefono_2
        telefono_2 = None
        try:
            telefono_2 = self.cleaned_data['telefono_2'].strip()
        except:
            pass
        if telefono_2 != None:
            if telefono_2 != '':
                fields.append(Field('telefono_2', telefono_2).append([
                    IsRequired(error='Este campo es obligatorio.'), Regex("(^\({1}[0-9]{1}\){1}?[0-9]{7})|(\d{10})", error='El campo no tiene el formato correcto.'),
                ]))

        # Validacion empresa
        empresa = None
        try:
            empresa = self.cleaned_data['empresa'].strip()
        except:
            pass
        if empresa != None:
            if empresa != '':
                fields.append(Field('empresa', empresa).append([
                    IsRequired(error='Este campo es obligatorio.'), Regex(u"^[&.áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
                ]))

        # Validacion telefono_empresa
        telefono_empresa = None
        try:
            telefono_empresa = self.cleaned_data['telefono_empresa'].strip()
        except:
            pass
        if telefono_empresa != None:
            if telefono_empresa != '':
                fields.append(Field('telefono_empresa', telefono_empresa).append([
                    IsRequired(error='Este campo es obligatorio.'), Regex("(^\({1}[0-9]{1}\){1}?[0-9]{7})|(\d{10})", error='El campo no tiene el formato correcto.'),
                ]))

        # Validacion direccion_empresa
        direccion_empresa = None
        try:
            direccion_empresa = self.cleaned_data['direccion_empresa'].strip()
        except:
            pass
        if direccion_empresa != None:
            if direccion_empresa != '':
                fields.append(Field('direccion_empresa', direccion_empresa).append([
                    IsRequired(error='Este campo es obligatorio.'), Regex("^[ A-Za-z0-9]+$", error='El campo no tiene el formato correcto.'),
                ]))

        validations = Validator().append(fields).run(True)

        for validation in validations:
            if validation['passed'] == False:
                self._errors[validation['field']] = self.error_class(validation['errors'])

        return cleaned_data

class ContactoClienteForm(forms.Form):
    nombre_contacto = forms.CharField(max_length=140)
    telefono_contacto = forms.CharField(max_length=10)
    departamento_contacto = forms.ModelChoiceField(Departamento.objects.all(), widget=forms.Select(attrs={'onchange': "Dajaxice.aplicacion.inverboy.cargar_municipios('Dajax.process',{'option':this.value, 'elemento': 'id_municipio_contacto'})"}), required=False)
    municipio_contacto = forms.ModelChoiceField(Municipio.objects.all())
    email_contacto = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        super(ContactoClienteForm, self).__init__(*args, **kwargs)
        # Carga los municipios de acuerdo al departamento seleccionado
        if args or kwargs:
            if args:
                departamento_contacto = args[0]['departamento_contacto']
            else:
                departamento_contacto = kwargs['initial']['departamento_contacto']                

            if departamento_contacto == '':
                self.fields['municipio_contacto'].queryset = Municipio.objects.filter(id=0)
            else:
                self.fields['municipio_contacto'].queryset = Municipio.objects.filter(departamento=departamento_contacto)
        else:
            self.fields['municipio_contacto'].queryset = Municipio.objects.filter(id=0)
        # Chosen
        self.fields['departamento_contacto'].widget.attrs['data-placeholder'] = 'Seleccione..'
        self.fields['departamento_contacto'].widget.attrs['class'] = 'chosen-select'
        self.fields['departamento_contacto'].widget.attrs['style'] = 'width:350px;'

        # Chosen
        self.fields['municipio_contacto'].widget.attrs['data-placeholder'] = 'Seleccione..'
        self.fields['municipio_contacto'].widget.attrs['class'] = 'chosen-select'
        self.fields['municipio_contacto'].widget.attrs['style'] = 'width:350px;'

    def clean(self):
        cleaned_data = super(ContactoClienteForm, self).clean()

        fields = []

        # Validacion nombre_contacto
        nombre_contacto = None
        try:
            nombre_contacto = self.cleaned_data['nombre_contacto'].strip()
        except:
            pass
        if nombre_contacto != None:
            fields.append(Field('nombre_contacto', nombre_contacto).append([
                IsRequired(error='Este campo es obligatorio.'), Regex(u"^[áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))

        # Validacion telefono_contacto
        telefono_contacto = None
        try:
            telefono_contacto = self.cleaned_data['telefono_contacto'].strip()
        except:
            pass
        if telefono_contacto != None:
            fields.append(Field('telefono_contacto', telefono_contacto).append([
                IsRequired(error='Este campo es obligatorio.'), Regex("(^\({1}[0-9]{1}\){1}?[0-9]{7})|(\d{10})", error='El campo no tiene el formato correcto.'),
            ]))

        validations = Validator().append(fields).run(True)

        for validation in validations:
            if validation['passed'] == False:
                self._errors[validation['field']] = self.error_class(validation['errors'])

        return cleaned_data


class SeccionProyectoForm(BaseModelForm):

    class Meta:
        model = SeccionProyecto
        fields = ('nombre', 'iniciales')

    def clean(self):
        cleaned_data = super(SeccionProyectoForm, self).clean()

        fields = []

        # Validacion nombre
        nombre = None
        try:
            nombre = self.cleaned_data['nombre'].strip()
        except:
            pass
        if nombre != None:
            fields.append(Field('nombre', nombre).append([
                IsRequired(error='Este campo es obligatorio.'), Regex(u"^[áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))

        # Validacion iniciales
        iniciales = None
        try:
            iniciales = self.cleaned_data['iniciales'].strip()
        except:
            pass
        if iniciales != None:
            fields.append(Field('iniciales', iniciales).append([
                IsRequired(error='Este campo es obligatorio.'), Regex(u"^[áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))

        validations = Validator().append(fields).run(True)

        for validation in validations:
            if validation['passed'] == False:
                self._errors[validation['field']] = self.error_class(validation['errors'])

        return cleaned_data


class TipoInmuebleForm(BaseModelForm):

    class Meta:
        model = TipoInmueble

    def clean(self):
        cleaned_data = super(TipoInmuebleForm, self).clean()

        fields = []

        # Validacion nombre
        nombre = None
        try:
            nombre = self.cleaned_data['nombre'].strip()
        except:
            pass
        if nombre != None:
            fields.append(Field('nombre', nombre).append([
                IsRequired(error='Este campo es obligatorio.'), Regex(u"^[áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))

        # Validacion descripcion
        descripcion = None
        try:
            descripcion = self.cleaned_data['descripcion'].strip()
        except:
            pass
        if descripcion != None:
            fields.append(Field('descripcion', descripcion).append([
                IsRequired(error='Este campo es obligatorio.'),
            ]))

        validations = Validator().append(fields).run(True)

        for validation in validations:
            if validation['passed'] == False:
                self._errors[validation['field']] = self.error_class(validation['errors'])

        return cleaned_data

                    
class InmuebleForm(BaseModelForm):

    class Meta:
        model = Inmueble
        fields = ('identificacion', 'tipo_inmueble', 'seccion_proyecto', 'area_construida', 'area_privada', 'fecha_entrega_obra', 'valor', 'lista_precios', 'estado_registro')

    def __init__(self, *args, **kwargs):
        from django.forms.extras.widgets import SelectDateWidget
        super(InmuebleForm, self).__init__(*args, **kwargs)
        self.fields['area_construida'] = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.1, required=False)
        self.fields['area_privada'] = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.1, required=False)
        # Selector de fecha
        self.fields['fecha_entrega_obra'].widget = SelectDateWidget()
        self.fields['fecha_entrega_obra'].required = False
        
        self.fields['valor'] = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.0, initial=0)
        self.fields['lista_precios'].required = False
        self.fields['lista_precios'] = forms.IntegerField(min_value=1, required=False)

        # Campo (estado) para modificacion del registro
        self.fields['estado_registro'].required = False
        self.fields['estado_registro'].label = 'Activo'

        # Chosen
        self.fields['tipo_inmueble'].widget.attrs['data-placeholder'] = 'Seleccione..'
        self.fields['tipo_inmueble'].widget.attrs['class'] = 'chosen-select'
        self.fields['tipo_inmueble'].widget.attrs['style'] = 'width:350px;'


        # Chosen
        self.fields['seccion_proyecto'].widget.attrs['data-placeholder'] = 'Seleccione..'
        self.fields['seccion_proyecto'].widget.attrs['class'] = 'chosen-select'
        self.fields['seccion_proyecto'].widget.attrs['style'] = 'width:350px;'

        if self.instance.id:
            #Actualiza el estado del registro en el formulario
            self.instance.estado_registro = Inmueble.objects.get(id=self.instance.id).estado_registro
            # Valida si el inmueble se encuentra comprometido
            if self.instance.item_agrupacion_inmueble != None:
                # Remueve el campo de estado
                self.fields.pop('estado_registro')
                if self.instance.item_agrupacion_inmueble.agrupacion_inmueble.agrupacion_contrato_venta != None:
                    if self.instance.permiso_modificar == False:
                        # Remueve el campo de estado
                        self.fields.pop('valor')
                        self.fields.pop('lista_precios')


    def clean(self):

        cleaned_data = super(InmuebleForm, self).clean()

        fields = []

        # Validacion identificacion
        identificacion = None
        try:
            identificacion = self.cleaned_data['identificacion'].strip()
        except:
            pass
        if identificacion != None:
            fields.append(Field('identificacion', identificacion).append([
                IsRequired(error='Este campo es obligatorio.'), Regex("^[ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))

        # Validacion lista_precios
        lista_precios = None
        try:
            lista_precios = self.cleaned_data['lista_precios']
        except:
            pass
        if lista_precios != None:
            fields.append(Field('lista_precios', str(lista_precios)).append([
                IsRequired(error='Este campo es obligatorio.'), Regex("^[0-9]{1,6}$", error='El campo no tiene el formato correcto.'),
            ]))
            
        validations = Validator().append(fields).run(True)

        for validation in validations:
            if validation['passed'] == False:
                self._errors[validation['field']] = self.error_class(validation['errors'])

        return cleaned_data


class AgrupacionInmuebleForm(BaseModelForm):

    class Meta:
        model = AgrupacionInmueble
        fields = ('identificacion',)

    def __init__(self, *args, **kwargs):
        super(AgrupacionInmuebleForm, self).__init__(*args, **kwargs)
        self.fields['valor'] = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.1)

    def clean(self):

        cleaned_data = super(AgrupacionInmuebleForm, self).clean()

        fields = []

        # Validacion identificacion
        identificacion = None
        try:
            identificacion = self.cleaned_data['identificacion'].strip()
        except:
            pass
        if identificacion != None:
            fields.append(Field('identificacion', identificacion).append([
                IsRequired(error='Este campo es obligatorio.'), Regex("^[ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))

        validations = Validator().append(fields).run(True)

        for validation in validations:
            if validation['passed'] == False:
                self._errors[validation['field']] = self.error_class(validation['errors'])

        return cleaned_data


TIPO_NOTIFICACION_VENTA = (('', '----'),
            (1, 'LLamada'),
            (2, 'E-mail'),
            (3, 'Videollamada'),
            (4, 'Chat'),
            (5, 'Visita'),
            (6, 'Otro'))

class NotificacionVentaForm(BaseModelForm):

    fecha_limite_notificacion = forms.DateField(input_formats=['%Y-%m-%d'])
    hora_limite_notificacion = forms.TimeField(input_formats=['%H:%M'])

    class Meta:
        model = NotificacionVenta
        fields = ('tipo_notificacion', 'descripcion')

    def __init__(self, *args, **kwargs):
        super(NotificacionVentaForm, self).__init__(*args, **kwargs)
        self.fields['tipo_notificacion'] = forms.ChoiceField(choices=TIPO_NOTIFICACION_VENTA)

        #self.fields['fecha_limite_notificacion'] = forms.DateTimeField(input_formats=['%y-%m-%d %H:%M'])

        # Chosen
        self.fields['tipo_notificacion'].widget.attrs['data-placeholder'] = 'Seleccione..'
        self.fields['tipo_notificacion'].widget.attrs['class'] = 'chosen-select'
        self.fields['tipo_notificacion'].widget.attrs['style'] = 'width:350px;'

    def clean(self):
        from datetime import datetime, timedelta

        cleaned_data = super(NotificacionVentaForm, self).clean()

        # Validacion fecha_limite_notificacion
        fecha_limite_notificacion = None
        try:
            fecha_limite_notificacion = self.cleaned_data['fecha_limite_notificacion']
        except:
            pass
        hora_limite_notificacion = None
        try:
            hora_limite_notificacion = self.cleaned_data['hora_limite_notificacion']
        except:
            pass
        if fecha_limite_notificacion != None and hora_limite_notificacion != None:
            fecha_limite = datetime.combine(fecha_limite_notificacion, hora_limite_notificacion)
            fecha_minima = datetime.now() + timedelta(minutes=15)
            if fecha_limite < fecha_minima:
                self._errors['fecha_limite_notificacion'] = self.error_class(['La fecha/hora debe ser mayor a 15 minutos de la fecha/hora actual.'])
        return cleaned_data


class RespuestaNotificacionVentaForm(BaseForm):
    observaciones = forms.CharField(widget=forms.Textarea)


FORMA_PAGO_CONTRATO_VENTA = (('', '-----'),
            (1, 'Credito'),
            (2, 'Contado'))

NUMERO_CUOTAS_EFECTIVO_CONTRATO_VENTA = (('', '-----'),
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
            (6, '6'),
            (7, '7'),
            (8, '8'),
            (9, '9'),
            (10, '10'),
            (11, '11'),
            (12, '12'),
            (13, '13'),
            (14, '14'),
            (15, '15'),
            (16, '16'),
            (17, '17'),
            (18, '18'),
            (19, '19'),
            (20, '20'),
            (21, '21'),
            (22, '22'),
            (23, '23'),
            (24, '24'),
            (25, '25'),
            (26, '26'),
            (27, '27'),
            (28, '29'),
            (30, '30'),
            (31, '31'),
            (32, '32'),
            (33, '33'),
            (34, '34'),
            (35, '35'),
            (36, '36'),
            (37, '37'),
            (38, '38'),
            (39, '39'),
            (40, '40'),
            (41, '41'),
            (42, '42'),
            (43, '43'),
            (44, '44'),
            (45, '45'),
            (46, '46'),
            (47, '47'),
            (48, '48'),
            (49, '49'),
            (50, '50'),
            (51, '51'),
            (52, '52'),
            (53, '53'),
            (54, '54'),
            (55, '55'),
            (56, '56'),
            (57, '57'),
            (58, '58'),
            (59, '59'),
            (60, '60'),
            (61, '61'),
            (62, '62'),
            (63, '63'),
            (64, '64'),
            (65, '65'),
            (66, '66'),
            (67, '67'),
            (68, '68'),
            (69, '69'),
            (70, '70'),
            (71, '71'),
            (72, '72'))

class ContratoVentaForm(BaseModelForm):
    fecha_maxima_separacion = forms.DateField(input_formats=['%Y-%m-%d'])
    numero_cuotas = forms.ChoiceField(choices=NUMERO_CUOTAS_EFECTIVO_CONTRATO_VENTA, required=False)
    texto_legal = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = ContratoVenta
        fields = ('forma_pago', 'entidad_bancaria_credito', 'monto_credito')

    def __init__(self, *args, **kwargs):
        super(ContratoVentaForm, self).__init__(*args, **kwargs)
        self.fields['forma_pago'] = forms.ChoiceField(choices=FORMA_PAGO_CONTRATO_VENTA, required=False)

        self.fields['entidad_bancaria_credito'] = forms.ModelChoiceField(EntidadBancaria.objects.filter(estado_registro=True), required=False)

        self.fields['monto_credito'] = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.1, required=False)

        if not self.instance.id or (self.instance.id and self.instance.estado_contrato_venta().estado_contrato < 3):
            self.fields.pop('texto_legal')

        # Chosen
        self.fields['forma_pago'].widget.attrs['data-placeholder'] = 'Seleccione..'
        self.fields['forma_pago'].widget.attrs['class'] = 'chosen-select'
        self.fields['forma_pago'].widget.attrs['style'] = 'width:350px;'

        # Chosen
        self.fields['entidad_bancaria_credito'].widget.attrs['data-placeholder'] = 'Seleccione..'
        self.fields['entidad_bancaria_credito'].widget.attrs['class'] = 'chosen-select'
        self.fields['entidad_bancaria_credito'].widget.attrs['style'] = 'width:350px;'

        # Chosen
        self.fields['numero_cuotas'].widget.attrs['data-placeholder'] = 'Seleccione..'
        self.fields['numero_cuotas'].widget.attrs['class'] = 'chosen-select'
        self.fields['numero_cuotas'].widget.attrs['style'] = 'width:80px;'

    def clean(self):
        from datetime import datetime

        cleaned_data = super(ContratoVentaForm, self).clean()

        # Validacion fecha_maxima_separacion
        fecha_maxima_separacion = None
        try:
            fecha_maxima_separacion = self.cleaned_data['fecha_maxima_separacion']
        except:
            pass
        if fecha_maxima_separacion != None:
            # Valida que sea un nuevo registro, ó si es la modificación de un registro valida la fecha si esta es diferente a la fecha con la que fue registrado inicialmente
            contrato_venta = self.instance
            if not contrato_venta.id or (contrato_venta.id and contrato_venta.estado_contrato_venta().estado_contrato == 1 and contrato_venta.estado_contrato_venta().fecha_limite_estado != fecha_maxima_separacion):
                if fecha_maxima_separacion < date.today():
                    self._errors['fecha_maxima_separacion'] = self.error_class(['La fecha no debe ser menor la fecha actual.'])

        # Validacion forma_pago
        forma_pago = None
        try:
            forma_pago = self.cleaned_data['forma_pago']
        except:
            pass
        if forma_pago != None and forma_pago != '':
            forma_pago = int(forma_pago)
            if forma_pago == 1:
                monto_credito = None
                try:
                    monto_credito = self.cleaned_data['monto_credito']
                except:
                    pass
                if monto_credito == None:
                    self._errors['monto_credito'] = self.error_class(['Este campo es obligatorio.'])
        return cleaned_data


TIPO_CUENTA_PAGO_ENTIDAD_CONTRATO_VENTA = (('', '-----'),
            (1, 'Ahorro programado'),
            (2, 'CDT'),
            (3, 'Cesantias'),
            (4, 'Subsidio'))
        
class PagoEntidadContratoVentaForm(BaseModelForm):

    class Meta:
        model = PagoEntidadContratoVenta
        fields = ('tipo_cuenta', 'entidad', 'numero_cuenta', 'fecha_desembolso', 'valor')

    def __init__(self, contrato_venta=None, *args, **kwargs):
        super(PagoEntidadContratoVentaForm, self).__init__(*args, **kwargs)
        self.fields['tipo_cuenta'] = forms.ChoiceField(choices=TIPO_CUENTA_PAGO_ENTIDAD_CONTRATO_VENTA)

        # Valida si el contrato ya esta en estado (3-Vendido), si es asi hace obligatorios los campos entidad y numero de cuenta
        if contrato_venta and contrato_venta.estado_contrato_venta().estado_contrato >= 3:
            self.fields['entidad'] = forms.ModelChoiceField(EntidadBancaria.objects.filter(estado_registro=True))
            self.fields['numero_cuenta'] = forms.CharField(max_length=40)
        else:
            self.fields['entidad'] = forms.ModelChoiceField(EntidadBancaria.objects.filter(estado_registro=True), required=False)
            self.fields['numero_cuenta'] = forms.CharField(max_length=40, required=False)

        self.fields['fecha_desembolso'] = forms.DateField(input_formats=['%Y-%m-%d'], required=False)

        self.fields['valor'] = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.1)

        # Chosen
        self.fields['tipo_cuenta'].widget.attrs['data-placeholder'] = 'Seleccione..'
        self.fields['tipo_cuenta'].widget.attrs['class'] = 'chosen-select'
        self.fields['tipo_cuenta'].widget.attrs['style'] = 'width:350px;'

        # Chosen
        self.fields['entidad'].widget.attrs['data-placeholder'] = 'Seleccione..'
        self.fields['entidad'].widget.attrs['class'] = 'chosen-select'
        self.fields['entidad'].widget.attrs['style'] = 'width:350px;'

    def clean(self):
        cleaned_data = super(PagoEntidadContratoVentaForm, self).clean()

        fields = []

        # Validacion numero_cuenta
        numero_cuenta = None
        try:
            numero_cuenta = self.cleaned_data['numero_cuenta'].strip()
        except:
            pass
        if numero_cuenta != None and numero_cuenta != '':
            fields.append(Field('numero_cuenta', numero_cuenta).append([
                IsRequired(error='Este campo es obligatorio.'), Regex("^[ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))

        validations = Validator().append(fields).run(True)

        for validation in validations:
            if validation['passed'] == False:
                self._errors[validation['field']] = self.error_class(validation['errors'])

        # Validacion fecha_desembolso
        fecha_desembolso = None
        try:
            fecha_desembolso = self.cleaned_data['fecha_desembolso']
        except:
            pass
        #if fecha_desembolso != None:                
        #    if not self.instance.id or (self.instance.id and self.instance.fecha_desembolso != fecha_desembolso):
        #        if fecha_desembolso < datetime.date.today():
        #            self._errors['fecha_desembolso'] = self.error_class(['La fecha debe ser mayor a la fecha actual.'])
        return cleaned_data


class PagoEfectivoContratoVentaForm(BaseModelForm):

    class Meta:
        model = PagoEfectivoContratoVenta
        fields = ('fecha_desembolso', 'valor')

    def __init__(self, *args, **kwargs):
        super(PagoEfectivoContratoVentaForm, self).__init__(*args, **kwargs)

        self.fields['fecha_desembolso'] = forms.DateField(input_formats=['%Y-%m-%d'])
        self.fields['valor'] = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.1)

    def clean(self):
        cleaned_data = super(PagoEfectivoContratoVentaForm, self).clean()

        # Validacion fecha_desembolso
        fecha_desembolso = None
        try:
            fecha_desembolso = self.cleaned_data['fecha_desembolso']
        except:
            pass
        #if fecha_desembolso != None:
        #    if fecha_desembolso < datetime.date.today():
        #        self._errors['fecha_desembolso'] = self.error_class(['La fecha debe ser mayor a la fecha actual.'])

        return cleaned_data


class AbonoPagoEntidadContratoVentaForm(BaseForm):
    valor = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.1)


class AbonoPagoEfectivoContratoVentaForm(BaseModelForm):
    
    class Meta:
        model = AbonoPagoEfectivoContratoVenta
        fields = ('fecha_consignacion', 'numero_consignacion', 'valor')

    def __init__(self, *args, **kwargs):
        super(AbonoPagoEfectivoContratoVentaForm, self).__init__(*args, **kwargs)

        self.fields['fecha_consignacion'] = forms.DateField(input_formats=['%Y-%m-%d'])
        self.fields['valor'] = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.1)

    def clean(self):
        cleaned_data = super(AbonoPagoEfectivoContratoVentaForm, self).clean()

        fields = []

        # Validacion numero_consignacion
        numero_consignacion = None
        try:
            numero_consignacion = self.cleaned_data['numero_consignacion'].strip()
        except:
            pass
        if numero_consignacion != None and numero_consignacion != '':
            fields.append(Field('numero_consignacion', numero_consignacion).append([
                IsRequired(error='Este campo es obligatorio.'), Regex("^[ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))

        validations = Validator().append(fields).run(True)

        for validation in validations:
            if validation['passed'] == False:
                self._errors[validation['field']] = self.error_class(validation['errors'])

        return cleaned_data


#### #### MODULO DE VENTAS #### ####



###### Modulo de sugerencias ######

SUGERENCIAS_MODULOS_CHOICES = (('', '----'),
                                    ('DOCUMENTOS', 'DOCUMENTOS'),
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

class BuzonSugerenciaForm(forms.Form):
    modulo = forms.ChoiceField(choices=SUGERENCIAS_MODULOS_CHOICES, required=True)
    observaciones = forms.CharField(widget=forms.Textarea)
    def clean(self):
        cleaned_data = super(BuzonSugerenciaForm, self).clean()
        #Validación nombre
        observaciones = None
        try:
            observaciones = self.cleaned_data['observaciones']
        except:
            pass
        if observaciones != None:
            error_observaciones = validar_cadena(observaciones)
            if error_observaciones != '':
                self._errors['observaciones'] = self.error_class([error_observaciones])
        return cleaned_data


#class ReporteVentasForm(forms.ModelForm):
#    def __init__(self, *args, **kwargs):
#        super(ReporteVentasForm, self).__init__(*args, **kwargs)
#        self.fields['opciones'].widget = forms.CheckboxSelectMultiple()

REPORTE_VENTAS_OPCIONES = (('nombre_cliente', 'Nombre Cliente'),
                            ('identificacion_cliente', 'Identificacion Cliente'),
                            ('ciudad_cliente', 'Ciudad Cliente'),
                            ('entidad_bancaria', 'Entidad Bancaria'),
                            ('fecha_escrtura', 'Fecha de escritura'),
                            ('valor_pagos_entidad', 'Valor pagos entidad'),
                            ('valor_pagos_efectivo', 'Valor pagos efectivo'),
                            ('inmueble_contrato', 'Inmueble del contrato'),
                            ('valor_inmueble_contrato', 'Valor del inmueble del contrato'),
                            ('valor_adicionales_contrato', 'Valor de los adicionales del contrato'),
    )

class ReporteVentasForm(forms.Form):
    reporte_ventas_opciones = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=REPORTE_VENTAS_OPCIONES)

#### #### MODULO PLANES #### ####


# -*- coding: utf-8 -*-
from django import forms

#VALIDACIONES
#from validator.core import Validator, Field
#from validator.rules import *

class StageForm(forms.Form):
    name = forms.CharField(max_length=140, label='Nombre')
    initials = forms.CharField(max_length=3, label='Siglas')
    description = forms.CharField(widget=forms.Textarea, required=False, label='Descripción')
    image_file = forms.ImageField(
        label='Seleccione una imagen',
        help_text='(icono)',
        required=False
    )

    def clean(self):
        cleaned_data = super(StageForm, self).clean()

        fields = []

        # Validation name
        name = None
        try:
            name = self.cleaned_data['name'].strip()
        except:
            pass
        if name != None:
            """
            fields.append(Field('name', name).append([
                IsRequired(error='Este campo es obligatorio.'), Regex("^[áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))"""
            pass

        # Validation initials
        initials = None
        try:
            initials = self.cleaned_data['initials'].strip()
        except:
            pass
        if initials != None:
            """
            fields.append(Field('initials', initials).append([
                IsRequired('Este campo es obligatorio.'), Regex("^[áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))"""
            pass

        """
        validations = Validator().append(fields).run(True)

        for validation in validations:
            if validation['passed'] == False:
                self._errors[validation['field']] = self.error_class(validation['errors'])
        """
        return cleaned_data


class ImagePlaneForm(forms.Form):
    name = forms.CharField(max_length=140, label='Nombre')
    initials = forms.CharField(max_length=3, label='Siglas')
    description = forms.CharField(widget=forms.Textarea, required=False, label='Descripción')
    image_file = forms.ImageField(
        label='Seleccione una imagen (Plano)',
        help_text='max. 42 megabytes'
    )

    def clean(self):
        cleaned_data = super(ImagePlaneForm, self).clean()

        fields = []

        # Validation name
        name = None
        try:
            name = self.cleaned_data['name'].strip()
        except:
            pass
        if name != None:
            """
            fields.append(Field('name', name).append([
                IsRequired(error='Este campo es obligatorio.'), Regex("^[áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))"""
            pass

        # Validation initials
        initials = None
        try:
            initials = self.cleaned_data['initials'].strip()
        except:
            pass
        if initials != None:
            """
            fields.append(Field('initials', initials).append([
                IsRequired('Este campo es obligatorio.'), Regex("^[áéíóúÁÉÍÓÚñÑ A-Za-z0-9_-]+$", error='El campo no tiene el formato correcto.'),
            ]))"""
            pass

        """
        validations = Validator().append(fields).run(True)

        for validation in validations:
            if validation['passed'] == False:
                self._errors[validation['field']] = self.error_class(validation['errors'])
        """

        return cleaned_data


class MultipleUploadChronologicalPicturesForm(forms.Form):
    image_file = forms.ImageField(
        label='Seleccione uno o varios archivos (Fotos).',
        help_text='max. 42 megabytes'
    )


class PublishedProjectForm(BaseModelForm):

    class Meta:
        model = PublishedProject
        fields = ('text',)


class CommentPublishedProjectForm(BaseModelForm):

    class Meta:
        model = CommentPublishedProject
        fields = ('text',)


#### #### MODULO PLANES #### ####




# Uload de archivos
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()


class PlaneForm(forms.ModelForm):

    class Meta:
        model = ImagePlane