function traerMedidas(){
    var ajax=new XMLHttpRequest();
    var idTalla = document.getElementById("nombreTalla").value;
    var url='/tallas/medidas/'+idTalla;
    var div=document.getElementById("notificaciones");
    ajax.open('Get',url,true);
    ajax.onreadystatechange= function(){
        if(this.readyState==4 && this.status==200){
           var respuesta=JSON.parse(this.responseText);
           console.log(respuesta)
        }
    };
    ajax.send();
}


