
function validar(form){
    var fechaInicio = form.fechaInicio.value;
    var fechaFin = form.fechaFin.value;
    var producto = form.producto.value;

    var cadena = validarFechas(fechaInicio,fechaFin)
    cadena+=verificarProducto(producto);

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


function verificarProducto(producto){
    var salida = "";
    if(producto=="Selecciona una opcion"){
        salida = "Debes elegir un producto válido \n";
    }
    return salida;
}
function validarFechas(fechaInicio, fechaFin){
    var salida ="";
    if (fechaInicio<=fechaFin){
        salida=""
    }else{
        salida="Debes establecer las fechas correctamente \n"
    }
    return salida;
}
