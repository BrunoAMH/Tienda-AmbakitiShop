import datetime

from flask import Flask,render_template,request,flash,redirect,url_for,abort
from flask_bootstrap import Bootstrap
from flask_login import current_user,login_user,logout_user,login_manager,login_required,LoginManager
from modelo.DAO import db,Usuario,direcciones,Producto,Prenda,Talla,fotos,Sabores,Comestible,Suvenir,Sugerencia,Tarjetas,Descuento, Comentario, Carrito
import json
app=Flask(__name__, template_folder='../vista', static_folder='../static')
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='cl4v3'

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))

@app.route('/')
def inicio():
    return render_template('comunes/index.html')

#---------------------------------------USUARIOS---------------------------------------
@app.route('/usuarios/registrarNuevo')
def nuevoUsuario():
    return render_template('usuarios/nuevo.html')

@app.route('/usuarios/creacionCuenta', methods=['post'])
def registrarUsuario():
    try:
        u = Usuario()
        u.nombre = request.form['nombrecompleto']
        u.telefono = request.form['telefono']
        u.estatus = 1
        u.tipo = "Cliente"
        u.correo = request.form['email']
        u.contrasena = request.form['password']
        u.insertar()
        flash('Usuario registrado con exito')
        return redirect(url_for('login'))
    except:
        flash('!Error al guardar el usuario!')
        return redirect(url_for('nuevoUsuario'))

@app.route('/usuarios/editarUsuario')
def editarUsuario():
    return render_template('usuarios/editar.html')

@app.route('/usuarios/guardarCambios', methods=['post'])
def guardarCambios():
    #try:
        u = Usuario()
        u.idUsuario = current_user.idUsuario
        u.nombre = request.form['nombre']
        u.telefono = request.form['telefono']
        u.estatus = 1
        u.tipo = "Cliente"
        u.correo = request.form['correo']
        u.contrasena = request.form['password']
        u.actualizar()
        login_user(u.consultaIndividual(u.idUsuario))
        flash('Cambios guardados con exito')
    #except:
        #flash('!Error al modificar el usuario!')
        return redirect(url_for('editarUsuario'))

@app.route('/usuarios/login')
def login():
    return render_template('usuarios/login.html')

@app.route('/usuarios/iniciandoSesion', methods=['post'])
def iniciandoSesion():
    correo=request.form['correo']
    password=request.form['contrasena']
    user=Usuario()
    user=user.validar(correo, password)
    if user!= None:
        #estatus = user.tipo
        #if estatus == 1:
        login_user(user)
        return render_template('comunes/index.html')
        #else:
        #    return render_template('usuarios/login.html')
    else:
        #flash('Datos incorrectos')
        return render_template('usuarios/login.html')
    return "iniciando sesion con " + correo + " y " + password

@app.route('/usuarios/consultarUsuarios')
@login_required
def consultarUsuarios():
    u = Usuario()
    return render_template('usuarios/consultar.html',usuarios = u.consultaGeneral())
@app.route('/cerrarSesion')
def cerrarSesion():
    logout_user()
    return redirect(url_for('login'))
@app.route('/usuarios/editar/<int:id>')
@login_required
def editarUsuarioUnico(id):
    u = Usuario();
    return render_template('/usuarios/editarUnico.html', usuario = u.consultaIndividual(id))

@app.route('/usuarios/editandoUsuarioUnico',methods=['post'])
@login_required
def editandoUsuarioUnico():
    try:
        u = Usuario()
        u.idUsuario = request.form['idUsuario']
        u.nombre = request.form['nombrecompleto']
        u.telefono = request.form['telefono']
        u.estatus = 1
        u.tipo=request.form['tipo']
        u.correo = request.form['email']
        u.contrasena = request.form['password']
        u.actualizar()
        #login_user(u.consultaIndividual(u.idUsuario))
        flash('Cambios guardados con exito')
    except:
        flash('!Error al modificar el usuario!')
    return redirect(url_for('consultarUsuarios'))

@app.route('/usuarios/eliminar/<int:id>')
def eliminarUsuario(id):
    try:
        u = Usuario()
        u.eliminar(id)
        flash('Usuario eliminado')
    except:
        flash('No se puede eliminar el usuario')
    return redirect(url_for('consultarUsuarios'))

@app.route('/usuarios/email/<string:email>',methods=['Get'])
def consultarPorEmail(email):
    usuario=Usuario()
    return json.dumps(usuario.consultarPorEmail(email))

@app.route('/usuarios/telefono/<string:telefono>',methods=['Get'])
def consultarPorTelefono(telefono):
    usuario=Usuario()
    return json.dumps(usuario.consultarPorTelefono(telefono))

#---------------------------------------DIRECCION---------------------------------------
@app.route('/usuarios/editarDireccion')
def editarDireccion():
    d = direcciones()
    return render_template('/direcciones/editar.html',direccion = d.consultaIndividualIdUsuario(current_user.idUsuario))
@app.route('/usuarios/ValidarDireccion', methods =['post'])
def nuevaDireccion():
    d = direcciones()
    d.calle = request.form['calle']
    d.codigoPostal = request.form['codigo']
    d.descripcion = request.form['descripcion']
    d.ciudad = request.form['ciudad']
    d.colonia = request.form['colonia']
    d.instruccionEntrega = request.form['instruccion']
    d.insertar()
@app.route('/usuarios/guardarDireccion', methods=['post'])
def guardarDireccion():
    try:
        d = direcciones()
        id = request.form['idDireccion']
        if (id == ""):
            d.idUsuario = current_user.idUsuario
            d.calle = request.form['calle']
            d.codigoPostal = request.form['codigo']
            d.descripcion = request.form['descripcion']
            d.ciudad = request.form['ciudad']
            d.colonia = request.form['colonia']
            d.instruccionEntrega = request.form['instruccion']
            d.insertar()
            flash('Cambios guardados con exito')
        else:
            d.idDireccion = request.form['idDireccion']
            d.idUsuario = current_user.idUsuario
            d.calle = request.form['calle']
            d.codigoPostal = request.form['codigo']
            d.descripcion = request.form['descripcion']
            d.ciudad = request.form['ciudad']
            d.colonia = request.form['colonia']
            d.instruccionEntrega = request.form['instruccion']
            d.actualizar()
            #login_user(u.consultaIndividual(u.idUsuario))
            flash('Cambios guardados con exito')
    except:
        flash('!Error al modificar la direccion!')
    return redirect(url_for('editarDireccion'))

#---------------------------------------SUGERENCIAS---------------------------------------
@app.route('/sugerencias/nuevaSugerencia')
@login_required
def nuevaSugerencia():
    return render_template('/sugerencias/nueva.html')
@app.route('/sugerencias/validarSugerencia',methods=['post'])
@login_required
def validandoSugerencia():
    try:
        s = Sugerencia()
        u = Usuario()
        u.idUsuario = current_user.idUsuario
        s.Usuarios_idUsuario = u.idUsuario
        s.comentario = request.form['comentario']
        s.fecha = '2021-11-25'
        s.insertar()
        flash('Sugerencia mandada con exito')
    except:
        flash('Fallo al mandar la sugerencia')
    return redirect(url_for('nuevaSugerencia'))
@app.route('/sugerencias/consultarSugerencias')
@login_required
def consultarSugerencia():
    s = Sugerencia();
    return render_template('/sugerencias/consultar.html', sugerencias=s.consultaGeneral())
@app.route('/sugerencia/eliminar/<int:id>')
@login_required
def eliminarSugerencia(id):
    s = Sugerencia()
    s.eliminar(id)
    flash('Sugerencia eliminada')
    return redirect(url_for('consultarSugerencia'))
#---------------------------------------PRODUCTOS---------------------------------------
@app.route('/productos/consultarPrendas')
def consultarProductosPrendas():
    prod = Producto()
    return render_template('/productos/consultarPrendas.html', productos = prod.consultaGeneral())

@app.route('/productos/consultarSuvenirs')
def consultarProductosSuvenirs():
    prod = Producto()
    return render_template('/productos/consultarSuvenirs.html', productos = prod.consultaGeneral())

@app.route('/productos/consultarConsumibles')
def consultarProductosComestibles():
    prod = Producto()
    return render_template('/productos/consultarComestibles.html', productos = prod.consultaGeneral())

@app.route('/productos/agregarProductoConsumible')
@login_required
def agregarProductoConsumible():
    s = Sabores()
    if current_user.is_authenticated() and current_user.is_admin:
        return render_template('/productos/nuevoConsumible.html', sabor = s.consultaGeneral())
    else:
        abort(404)
@app.route('/productos/guardandoProductoConsumible',methods=['post'])
def guardandoProductoConsumible():
    p = Producto()
    f = fotos()
    s = Sabores()
    c = Comestible()
    p.nombre = request.form['nombre']
    p.descripcion = request.form['descripcion']
    p.precioVenta = request.form['precioVenta']
    p.estatus = 'D'
    p.categoria = 'C'
    f.fotografia =request.files['foto'].read()
    f.insertar()
    p.idFoto = f.idFoto
    p.insertar()
    c.Productos_idProducto = p.idProducto
    c.Sabores_idSabor = 1
    c.unidadesExistencia = request.form['unidades']
    c.insertar()
    flash('Producto guardado con exito')
    return redirect(url_for('agregarProductoConsumible'))
@app.route('/productos/agregarProductoSuvenir')
@login_required
def agregarProductoSuvenir():
    if current_user.is_authenticated() and current_user.is_admin:
        return render_template('/productos/nuevoSuvenir.html')
    else:
        abort(404)
@app.route('/productos/guardandoProductoSuvenir',methods=['post'])
def guardandoProductoSuvenir():
    p = Producto()
    f = fotos()
    su = Suvenir()
    p.nombre = request.form['nombre']
    p.descripcion = request.form['descripcion']
    p.precioVenta = request.form['precioVenta']
    p.estatus = 'D'
    p.categoria = 'S'
    f.fotografia =request.files['foto'].read()
    f.insertar()
    p.idFoto = f.idFoto
    p.insertar()
    su.unidadesExistencia = request.form['unidades']
    su.Productos_idProducto = p.idProducto
    su.insertar()
    flash('Producto guardado con exito')
    return redirect(url_for('agregarProductoSuvenir'))


@app.route('/productos/guardandoProductoRopa',methods=['post'])
def guardandoProductoRopa():
    p = Producto()
    f = fotos()
    r = Prenda()
    p.nombre = request.form['nombre']
    p.descripcion = request.form['descripcion']
    p.precioVenta = request.form['precioVenta']
    p.estatus = 'D'
    p.categoria = 'R'
    f.fotografia =request.files['foto'].read()
    f.insertar()
    p.idFoto=f.idFoto
    p.insertar()
    r.Productos_idProducto = p.idProducto
    r.Tallas_idTalla = 1
    r.unidadesExistencia = request.form['unidades']
    r.color = request.form['color']
    genero = request.form['genero']
    if genero == 'Hombre':
        r.genero='H'
    elif genero == 'Mujer':
        r.genero = 'M'
    elif genero == 'Ambos':
        r.genero = 'A'
    r.insertar()
    flash('Producto guardado con exito')
    return redirect(url_for('agregarProductoRopa'))

@app.route('/productos/imagen/<int:id>')
def consultarImagenProducto(id):
    f = fotos()
    return f.consultaIndividual(id).fotografia

@app.route('/productos/editar/<int:id>')
def editarProducto(id):
    t = Talla()
    return render_template('/tallas/editar.html', t = t.consultaIndividual(id))
@app.route('/producto/verProducto/<int:id>')

def verProducto(id):
    p = Producto()
    c = Comentario()
    pre = Prenda()
    return render_template('/productos/verProducto.html', producto=p.consultaIndividual(id), comentario = c.consultaGeneral(), prenda = pre.consultaGeneral())
#---------------------------------------SUVENIRS---------------------------------------
@app.route('/suvenirs/consultar')
def consultarSuvenir():
    su = Suvenir()
    return render_template('/suvenirs/consultar.html', suvenirs=su.consultaGeneral())

@app.route('/suvenirs/ver/<int:id>')
def editarSuvenir(id):
    s = Suvenir()
    return render_template('/suvenirs/editar.html', s=s.consultaIndividual(id))

@app.route('/suvenirs/editandoSuvenir',methods=['post'])
def editandoSuvenir():
    try:
        s = Suvenir()
        s.idSuvenir = request.form['id']
        s.Productos_idProducto = request.form['Productos_idProducto']
        s.unidadesExistencia = request.form['Stock']
        s.actualizar()
        flash('Datos actualizados con exito')
    except:
        flash('!Error al actualizar!')
    return render_template('/suvenirs/editar.html', s=s)

@app.route('/suvenirs/eliminar/<int:id>')
def eliminarSuvenir(id):
    s = Suvenir()
    s.eliminar(id)
    flash('Suvenir eliminado')
    return redirect(url_for('consultarSuvenirs'))

#---------------------------------------PRENDAS---------------------------------------
@app.route('/prendas/consultar')
def consultarPrendas():
    pren = Prenda()
    return render_template('/prendas/consultar.html', prendas=pren.consultaGeneral())

@app.route('/prendas/nueva')
@login_required
def agregarProductoRopa():
    if current_user.is_authenticated() and current_user.is_admin:
        t = Talla()
        return render_template('/productos/nuevoRopa.html', tallas=t.consultaGeneral())
    else:
        abort(404)
@app.route('/prendas/eliminar/<int:id>')
def eliminarPrenda(id):
    p = Prenda()
    p.eliminar(id)
    flash('Prenda eliminada')
    return redirect(url_for('consultarPrendas'))

@app.route('/prendas/ver/<int:id>')
def editarPrenda(id):
    p = Prenda()
    return render_template('/prendas/editar.html', p=p.consultaIndividual(id))

@app.route('/prendas/editandoPrenda',methods=['post'])
def editandoPrenda():
    try:
        p = Prenda()
        p.idPrenda = request.form['id']
        p.Productos_idProducto = request.form['Productos_idProducto']
        p.Tallas_idTalla = request.form['Tallas_idTalla']
        p.unidadesExistencia = request.form['unidadesExistencia']
        p.color = request.form['color']
        genero = request.form['genero']
        if genero == 'Hombre':
            p.genero = 'H'
        elif genero == 'Mujer':
            p.genero = 'M'
        elif genero == 'Ambos':
            p.genero = 'A'
        p.actualizar()
        flash('Datos de la prenda actualizados con exito')
    except:
        flash('!Error al actualizar datos de la prenda!')
    return render_template('/prendas/editar.html', p=p)
#---------------------------------------TALLAS---------------------------------------
@app.route('/tallas/consultar')
def consultarTallas():
    tall = Talla()
    return render_template('/tallas/consultar.html', tallas=tall.consultaGeneral())
@app.route('/tallas/nuevo')
def agregarTalla():
    return render_template('/tallas/nuevo.html')
@app.route('/tallas/validarTalla',methods=['post'])
def guardandoTalla():
    try:
        t = Talla()
        t.nombreTalla = request.form['nombreTalla']
        t.medidas = request.form['medidas']
        t.insertar()
        flash('Talla guardada con exito')
    except:
        flash('Fallo al guardar')
    return redirect(url_for('agregarTalla'))
@app.route('/tallas/eliminar/<int:id>')
def eliminarTalla(id):
    t = Talla()
    t.eliminar(id)
    flash('Eliminada')
    return redirect(url_for('consultarTallas'))

@app.route('/tallas/ver/<int:id>')
def editarTalla(id):
    t = Talla()
    return render_template('/tallas/editar.html', t=t.consultaIndividual(id))

@app.route('/tallas/editandoTalla',methods=['post'])
def editandoTalla():
    try:
        t = Talla()
        t.idTalla = request.form['idTalla']
        t.nombreTalla = request.form['nombreTalla']
        t.medidas = request.form['medidas']
        t.actualizar()
        flash('Datos de la talla actualizados con exito')
    except:
        flash('!Error al actualizar datos de la talla!')
    return render_template('/tallas/editar.html', t=t)

#---------------------------------------PEDIDOS---------------------------------------
@app.route('/pedidos/MisPedidos')
def misPedidos():
    return render_template('/pedidos/consultar.html')
#---------------------------------------CARRITO---------------------------------------
@app.route('/carrito/nuevo', methods=['post'])
@login_required
def nuevoCarrito():
    c= Carrito()
    c.fecha = '2021-11-29'
    c.cantidad=1
    c.precio=request.form['precio']
    print(c.precio)
@app.route('/carrito/consultar')
@login_required
def miCarrito():
    carr = Carrito()
    return render_template('/carrito/consultar.html', carrito=carr.consultaGeneral())
#TARJETAS
@app.route('/tarjeta/nuevaTarjeta')
@login_required
def agregarTarjeta():
    return render_template('/tarjetas/nueva.html')

@app.route('/tarjetas/validarTarjeta', methods=['post'])
@login_required
def validarTarjeta():
    try:
        t = Tarjetas()
        u = Usuario()
        u.idUsuario = current_user.idUsuario
        t.Usuarios_idUsuario = u.idUsuario
        t.numTarjeta = request.form['tarjeta']
        t.emisora = request.form['emisora']
        mes = request.form['mes']
        anio = request.form['anio']
        t.fechaVigencia = anio + '-' + mes + '-' +'01'
        tipo = request.form['tipo']
        if tipo == 'Credito':
            t.tipo = 'C'
        elif tipo == 'Debito':
            t.tipo = 'D'
        t.cvc = request.form['cvc']
        t.insertar()
        flash('Tarjeta guardada con exito')
    except:
        flash('Fallo al guardar la tarjeta')
    return redirect(url_for('agregarTarjeta'))

#---------------------------------------DESCUENTOS---------------------------------------
@app.route('/descuentos/consultar')
def consultarDescuentos():
    d = Descuento()
    return render_template('/descuentos/consultar.html', descuento = d.consultaGeneral())
@app.route('/descuentos/nuevo')
@login_required
def nuevoDescuento():
    p = Producto()
    return render_template('/descuentos/nuevo.html', productos = p.consultaGeneral())
@app.route('/descuento/validandoDescuento', methods=['post'])

@login_required
def validarDescuento():
    try:
        d = Descuento()
        fechaInicio = request.form['fechaInicio'].split('-')
        fechaFin = request.form['fechaFin'].split('-')

        d.fechaInicio = fechaInicio[0]+'-'+fechaInicio[1]+'-'+fechaInicio[2]
        d.fechaFin = fechaFin[0]+'-'+fechaFin[1]+'-'+fechaFin[2]
    
        d.descuento = request.form['descuentoPorcentaje']
        d.Productos_idProducto = request.form['producto']
        d.insertar()
        flash('Descuento guardado con exito')
    except:
        flash('Fallo al guardar el descuento')
    return redirect(url_for('consultarDescuentos'))

@app.route('/descuentos/eliminar/<int:id>')
def eliminarDescuento(id):
    d = Descuento()
    d.eliminar(id)
    flash('¡Descuento Eliminado!')
    return redirect(url_for('consultarDescuentos'))

@app.route('/descuentos/ver/<int:id>')
def editarDescuento(id):
    d = Descuento()
    return render_template('/descuentos/editar.html', d=d.consultaIndividual(id))

@app.route('/descuento/editandoDescuento',methods=['post'])
def editandoDescuento():
    try:
        d = Descuento()
        d.idDescuento = request.form['idDescuento']
        #d.fechaInicio = request.form['fechaInicio']
        d.fechaInicio = '2021-10-01'
        #d.fechaFin = request.form['fechaFin']
        d.fechaFin = '2021-11-01'
        d.descuento = request.form['descuento']
        d.Productos_idProducto = request.form['producto']
        d.actualizar()
        flash('!Datos actualizados!')
    except:
        flash('!Error al actualizar el descuento!')
    return  redirect(url_for('consultarDescuentos'))

#----------------------------------------COMENTARIOS---------------------------------------
@app.route('/comentarios/nuevo/<int:id>')
@login_required
def nuevoComentario(id):
    p = Producto()
    return render_template('/comentarios/nuevo.html', producto = p.consultaIndividual(id))
@app.route('/comentario/validandoComentario', methods=['post'])
@login_required
def validandoComentario():
        c = Comentario()
        u = Usuario()
        c.comentario = request.form['comentario']
        c.calificacion = request.form['calificacion']
        u.idUsuario = current_user.idUsuario
        c.Usuarios_idUsuario = u.idUsuario
        c.Productos_idProducto = request.form['id']
        c.compraConfirmada='Y'
        c.insertar()
        #flash('Descuento guardado con exito')
        #flash('Fallo al guardar el descuento')
        return redirect(url_for('consultarProductos'))

#---------------------------------------SABORES---------------------------------------
@app.route('/sabores/nuevo')
@login_required
def nuevoSabor():
    return render_template('/sabores/nuevo.html')

@app.route('/sabores/consultar')
@login_required
def consultarSabores():
    s=Sabores()
    return render_template('/sabores/consultar.html', sabores=s.consultaGeneral())

@app.route('/sabores/eliminar/<int:id>')
@login_required
def eliminarSabor(id):
    s = Sabores()
    s.eliminar(id)
    flash('Sabor eliminado')
    return redirect(url_for('consultarSabores'))

@app.route('/sabores/ver/<int:id>')
@login_required
def consultarSabor(id):
    s = Sabores()
    return render_template('sabores/editar.html', sab=s.consultaIndividual(id))


@app.route('/sabores/modificar', methods=['post'])
def modificarSabor():
    s = Sabores()
    s.idSabor=request.form['id']
    s.nombreSabor=request.form['nombre']
    s.actualizar()
    flash('El nombre ha sido actualizado')
    return render_template('sabores/editar.html', sab=s)


@app.route('/sabores/validarSabor', methods=['post'])
@login_required
def validarSabor():
        s = Sabores()
        s.nombreSabor = request.form['sabor']
        s.insertar()
        flash('Sabor guardado con exito')
        return redirect(url_for('nuevoSabor'))

#---------------------------------------COMESTIBLES---------------------------------------

@app.route('/comestibles/consultar')
@login_required
def consultarComestibles():
    c = Comestible()
    return render_template('/comestibles/consultar.html', comestibles=c.consultaGeneral())

@app.route('/comestibles/eliminar/<int:id>')
@login_required
def eliminarComestible(id):
    c = Comestible()
    c.eliminar(id)
    flash('Eliminado')
    return redirect(url_for('consultarComestibles'))

@app.route('/comestibles/ver/<int:id>')
@login_required
def consultarComestible(id):
    c = Comestible()
    return render_template('comestibles/editar.html', c=c.consultaIndividual(id))


@app.route('/comestibles/modificar', methods=['post'])
def modificarComestible():
    c = Comestible()
    c.idComestible=request.form['id']
    c.Productos_idProducto=request.form['idProd']
    c.Sabores_idSabor = request.form['idSab']
    c.unidadesExistencia = request.form['Stock']
    c.actualizar()
    flash('Se ha actualizado correctamente')
    return render_template('comestibles/editar.html', com=c)



#---------------------------------------PAGINAS DE ERROR---------------------------------------
@app.errorhandler(404)
def error_404(e):
    return render_template('comunes/error_404.html'),404

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)