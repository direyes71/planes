/**
 * Created by PyCharm.
 * User: Administrador
 * Date: 10/08/12
 * Time: 11:58 AM
 * To change this template use File | Settings | File Templates.
 */
    ///////////////////////////////////////////////////////////////////////// CAMPOS VACIOS //////////////////////////////////////////////////////////////////////////////////////
    function trim (myString){
        return myString.replace(/^\s+/g,'').replace(/\s+$/g,'');
    }
    function validar_campo_vacio(val) {
        val.setCustomValidity('');
        if (val.value.length == 0) {
            val.setCustomValidity('Valor no valido');
        }
    }
    function validar_vacio_solo_espacios(val){              // AGREGAR USUARIO nombres,apellidos, direccion AGREGAR PROVEEDOR razon_social
        val.setCustomValidity('');
        if (trim(val.value)==''){
            val.setCustomValidity('Valor no valido');
        }
    }
    function validar_solo_espacios(val){
        val.setCustomValidity('');
        if (val.value.length > 0) {
            if (trim(val.value) == ''){
                val.setCustomValidity('Valor no valido');
            }
        }
    }
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    function validar_teclado_numeros(e) {                            // AGREGAR USUARIO identificacion AGREGAR PROVEEDOR identificacion
       tecla = (document.all) ? e.keyCode : e.which;
       if (tecla==8) return true;
       patron =/\d/;
       te = String.fromCharCode(tecla);
       return patron.test(te);
    }
    function validar_teclado_numerosLetrasNomUser(e){                // AGREGAR USUARIO nombre_usuario
       tecla = (document.all) ? e.keyCode : e.which;
       if (tecla==8) return true;
       patron = /^[A-Za-z0-9\Á\É\Í\Ó\Ú\Ñ\á\é\í\ó\ú\ñ]+$/;
       te = String.fromCharCode(tecla);
       return patron.test(te);
    }
    function validar_contrasenia(p1,p2){                                 // AGREGAR USUARIO comparar contraseñas
       p2.setCustomValidity('');
       if (p1.value != p2.value || p1.value == '' || p2.value == '') {
           p2.setCustomValidity('Contraseña no corresponde');
       }
    }
    function validar_teclado_numerosLetrasEspacios(e) {                 // AGREGAR USUARIO nombres,apellidos
       tecla = (document.all) ? e.keyCode : e.which;
       if (tecla==8) return true;
       patron = /^[A-Za-z0-9\s\xF1\xD1\Á\É\Í\Ó\Ú\Ñ\á\é\í\ó\ú\ñ]+$/;
       te = String.fromCharCode(tecla);
       return patron.test(te);
    }
    function validar_teclado_MayusculasNumerosEspacios_CE(e) {          // AGREGAR PROVEEDOR razon_social
       tecla = (document.all) ? e.keyCode : e.which;
       if (tecla==8) return true;
       patron = /^[A-Z0-9\s\xF1\xD1\Á\É\Í\Ó\Ú\Ñ\á\é\í\ó\ú\ñ]+$/;
       te = String.fromCharCode(tecla);
       return patron.test(te);
    }
    function validar_teclado_numerosLetrasEspaciosCe(e) {                 
       tecla = (document.all) ? e.keyCode : e.which;
       if (tecla==8) return true;
       patron = /^[A-Za-z0-9\s\xF1\xD1\Á\É\Í\Ó\Ú\Ñ\á\é\í\ó\ú\ñ\"\/]+$/;
       te = String.fromCharCode(tecla);
       return patron.test(te);
    }
    function validar_teclado_numerosLetras(e) {
       tecla = (document.all) ? e.keyCode : e.which;
       if (tecla==8) return true;
       patron = /^[A-Za-z0-9\xF1\xD1\Á\É\Í\Ó\Ú\Ñ\á\é\í\ó\ú\ñ]+$/;
       te = String.fromCharCode(tecla);
       return patron.test(te);
    }
    function validar_teclado_MayusculasNumerosEspacios(e) {
       tecla = (document.all) ? e.keyCode : e.which;
       if (tecla==8) return true;
       patron = /^[A-Z0-9\s\xF1\xD1\Á\É\Í\Ó\Ú\Ñ\.\/]+$/;
       te = String.fromCharCode(tecla);
       return patron.test(te);
    }
    function validar_teclado_telefonoIndicativo(e){
       tecla = (document.all) ? e.keyCode : e.which;
       if (tecla==8) return true;
       patron = /^[\)\(0-9]+$/;
       te = String.fromCharCode(tecla);
       return patron.test(te);
    }
    function validar_teclado_fecha(e){                  // AGREGAR USUARIO fecha_nacimiento
       tecla = (document.all) ? e.keyCode : e.which;
       if (tecla==8) return true;
       patron = /^[0-9\-]+$/;
       te = String.fromCharCode(tecla);
       return patron.test(te);
    }
    function validar_fecha(val){                        //AGREGAR USUARIO fecha_nacimiento
        fecha = val.value.replace(/\-/g,'/');
        fecha = fecha.split('/');
        anio = parseInt(fecha[0]);
        mes = parseInt(fecha[1],10);
        dia = parseInt(fecha[2],10);
        val.setCustomValidity('');

        //////////////////////////////////////////////// fecha mayor que fecha actual //////////////////////////////
        fechaActual = new Date();
        anioA = fechaActual.getFullYear();
        mesA = fechaActual.getMonth();
        mesA = mesA + 1;
        diaA = fechaActual.getDate();

        if (anio > anioA){
            val.setCustomValidity('La fecha no debe ser mayor a la fecha actual');
        }
          else{
                if(anio == anioA){
                    if(mes > mesA){
                        val.setCustomValidity('La fecha no debe ser mayor a la fecha actual');
                    }
                        else{
                            if(mes == mesA){
                                if(dia >= diaA){
                                    val.setCustomValidity('La fecha no debe ser mayor a la fecha actual');
                                }
                            }
                        }
                }
          }

        switch(mes){
            case 1:
            case 3:
            case 5:
            case 7:
            case 8:
            case 10:
            case 12:
                numDias=31;
                break;
            case 4: case 6: case 9: case 11:
                numDias=30;
                break;
            case 2:
                if (comprobarSiBisisesto(anio)){ numDias=29 }else{ numDias=28};
                break;
            default:
                val.setCustomValidity('Fecha no valida');
                break;
        }

        if (dia>numDias || dia==0){
            val.setCustomValidity('Fecha no valida');
        }
    }
    function comprobarSiBisisesto(anio){
        if (( anio % 100 != 0) && (anio % 4 == 0) || (anio % 400 == 0)) {
            return true;
        }
        else {
            return false;
        }
    }
    function validar_selects_vacios(val){
        val.setCustomValidity('');
        if (val.value == '0' || val.value == ""){
            val.setCustomValidity('Seleccionar un elemento de la lista');
        }
    }
    function validar_celular_telefono(val){
        //telefonoCelular =/(^\(?[0-9]{1}\)??[0-9]{7})|(\d{10})/;
        telefonoCelular =/(^\({1}[0-9]{1}\){1}?[0-9]{7})|(\d{10})/;
        val.setCustomValidity('');
        if(telefonoCelular.test(val.value)== false){
            val.setCustomValidity('Telefono/Celular no valido');
        }
    }
    function validar_celular(){
        telefonoCelular =/\d{10}/;
        val.setCustomValidity('');
        if(telefonoCelular.test(val.value)== false){
            val.setCustomValidity('Numero de celular no valido');
        }
    }
    function validar_telefono_indicativo(val){
        telefono =/(^\({1}[0-9]{1}\){1}?[0-9]{7})/;
        val.setCustomValidity('');
        if(telefono.test(val.value)== false){
            val.setCustomValidity('Telefono/Celular no valido');
        }
    }
    function validar_email(val){
        mail =/^(.+\@.+\..+)$/;
        val.setCustomValidity('');
        if(mail.test(val.value)== false){
            val.setCustomValidity('Email no valido');
        }
    }
    function validar_teclado_decimal(e,obj){
        tecla = (document.all) ? e.keyCode : e.which;
        if (tecla==8) return true;
        numero = obj.value;
        patron =/[0-9.]/;
        if(validaFloat(numero)) {
            punto = numero.split('.');
            if (punto.length==2){
                if (punto[1].length<2)
                    patron = /\d/;
                else
                    patron = /''/;
            }
        }
        te = String.fromCharCode(tecla);
        return patron.test(te);
    }
    function validaFloat(numero){
      if (!/^([0-9])*[.]?[0-9]*$/.test(numero))
        return false;
        return true
    }