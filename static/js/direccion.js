function validar(form){
    var codigo=form.codigo.value;
    var cadena=evaluarCodigo(codigo);
    var div=document.getElementById("notificaciones");
    if(cadena==''){
        div.innerHTML="";
        return true;
    }
    else{
        div.innerHTML=cadena;
        return false;
    }
}
function evaluarCodigo(cadena){
    var salida="";
    var patron=/[0-9]{5}/;
    var res=patron.test(cadena);
    if(res==false){
        salida="Debes informar un código postal de esta manera ##### \n";
    }
    return salida;
}
