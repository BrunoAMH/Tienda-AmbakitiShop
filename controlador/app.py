import datetime

from flask import Flask,render_template,request,flash,redirect,url_for,abort
from flask_bootstrap import Bootstrap
from flask_login import current_user,login_user,logout_user,login_manager,login_required,LoginManager
from modelo.DAO import db,Usuario,direcciones,Producto,Prenda,Talla,fotos,Sabores,Comestible,Suvenir,Sugerencia,Tarjetas,Descuento, Comentario

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

#USUARIOS
@app.route('/usuarios/registrarNuevo')
def nuevoUsuario():
    return render_template('usuarios/nuevo.html')

@app.route('/usuarios/creacionCuenta', methods=['post'])
def registrarUsuario():
    u = Usuario()
    u.nombre = request.form['nombre']
    u.telefono = request.form['telefono']
    u.estatus = 1
    u.tipo = "Admin"
    u.correo = request.form['correo']
    u.contrasena = request.form['contrasena']
    d = direcciones()
    d.calle = request.form['calle']
    d.codigoPostal = request.form['codigo']
    d.descripcion = request.form['descripcion']
    d.ciudad = request.form['ciudad']
    d.colonia = request.form['colonia']
    d.instruccionEntrega = request.form['instruccion']
    d.insertar()
    u.idDireccion = d.idDireccion
    u.insertar()
    flash('Usuario registrado con exito')
    return render_template('usuarios/nuevo.html')

@app.route('/usuarios/editarUsuario')
def editarUsuario():
    return render_template('usuarios/editar.html')

@app.route('/usuarios/guardarCambios', methods=['post'])
def guardarCambios():
    try:
        u = Usuario()
        u.idUsuario = current_user.idUsuario
        u.nombre = request.form['nombre']
        u.telefono = request.form['telefono']
        u.estatus = 1
        u.tipo = "Admin"
        u.correo = request.form['correo']
        u.contrasena = request.form['contrasena']
        u.actualizar()
        login_user(u.consultaIndividual(u.idUsuario))
        flash('Cambios guardados con exito')
    except:
        flash('!Error al modificar el usuario!')
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
def consultarUsuarios():
    u = Usuario()
    return render_template('usuarios/consultar.html',usuarios = u.consultaGeneral())
@app.route('/cerrarSesion')
def cerrarSesion():
    logout_user()
    return redirect(url_for('login'))
#DIRECCION
@app.route('/usuarios/editarDireccion')
def editarDireccion():
    d = direcciones()
    return render_template('/direcciones/editar.html',direccion = d.consultaIndividual(current_user.idDireccion))
@app.route('/usuarios/guardarDireccion', methods=['post'])
def guardarDireccion():
    try:
        d = direcciones()
        u = Usuario()
        u.idUsuario = current_user.idUsuario
        d.idDireccion = current_user.idDireccion
        d.calle = request.form['calle']
        d.codigoPostal = request.form['codigo']
        d.descripcion = request.form['descripcion']
        d.ciudad = request.form['ciudad']
        d.colonia = request.form['colonia']
        d.instruccionEntrega = request.form['instruccion']
        d.actualizar()
        login_user(u.consultaIndividual(u.idUsuario))
        flash('Cambios guardados con exito')
    except:
        flash('!Error al modificar la direccion!')

    return redirect(url_for('editarDireccion'))

#SUGERENCIAS
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
    flash('Eliminada')
    return redirect(url_for('consultarSugerencia'))
#PRODUCTOS
@app.route('/productos/consultarProductos')
def consultarProductos():
    prod = Producto()
    return render_template('/productos/consultar.html', productos = prod.consultaGeneral())
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

@app.route('/productos/agregarProductoRopa')
@login_required
def agregarProductoRopa():
    if current_user.is_authenticated() and current_user.is_admin:
        t = Talla()
        return render_template('/productos/nuevoRopa.html', tallas=t.consultaGeneral())
    else:
        abort(404)
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
@app.route('/productos/ver/<int:id>')
def editarProducto(id):
    t = Talla()
    return render_template('/tallas/editar.html', t = t.consultaIndividual(id))
#PRENDAS
@app.route('/prendas/consultar')
def consultarPrendas():
    pren = Prenda()
    return render_template('/prendas/consultar.html', prendas=pren.consultaGeneral())
@app.route('/prendas/nueva')
def agregarPrenda():
    return render_template('/prendas/nueva.html')
@app.route('/eliminar/<int:id>')
def eliminarProducto(id):
    flash('Eliminada')
    return redirect(url_for('consultarProductos'))
#TALLAS
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
    return render_template('/tallas/editar.html', t = t.consultaIndividual(id))
@app.route('/tallas/editandoTalla',methods=['post'])
def editandoTalla():
    try:
        t = Talla()
        t.nombreTalla = request.form['nombreTalla']
        t.medidas = request.form['medidas']
        t.actualizar()
        flash('Cambios guardados con exito')
    except:
        flash('!Error al modificar la direccion!')
    return redirect(url_for('consultarTallas'))
#PEDIDOS
@app.route('/pedidos/MisPedidos')
def misPedidos():
    return render_template('/pedidos/consultar.html')
#CARRITO
@app.route('/carrito/consultar')
def miCarrito():
    return render_template('/carrito/consultar.html')
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

#DESCUENTOS
@app.route('/descuentos/consultar')
def consultarDescuentos():
    d = Descuento()
    return render_template('/descuentos/consultar.html', descuento = d.consultaGeneral())
@app.route('/descuentos/nuevo')
def nuevoDescuento():
    p = Producto()
    return render_template('/descuentos/nuevo.html', productos = p.consultaGeneral())
@app.route('/descuento/validandoDescuento', methods=['post'])
@login_required
def validarDescuento():
    #try:
        d = Descuento()
        d.fechaInicio = '2021-01-01'
        d.fechaFin = '2021-01-10'
        d.descuento = request.form['descuentoPorcentaje']
        d.Productos_idProducto = request.form['tipo']
        d.insertar()
        flash('Descuento guardado con exito')
    #except:
        flash('Fallo al guardar el descuento')


        return render_template('/comentarios/nuevo.html')
    #return redirect(url_for('nuevoDescuento'))
#COMENTARIOS
@app.route('/comentarios/nuevo')
@login_required
def nuevoComentario():
    return render_template('/comentarios/nuevo.html')
@app.route('/comentario/validandoComentario/<int:id>', methods=['post'])
@login_required
def validandoComentario():
    try:

        flash('Descuento guardado con exito')
    except:
        flash('Fallo al guardar el descuento')
    return redirect(url_for('nuevoDescuento'))
#SABORES
@app.route('/sabores/nuevo')
@login_required
def nuevoSabor():
    return render_template('/sabores/nuevo.html')
@app.route('/sabores/validarSabor', methods=['post'])
@login_required
def validarSabor():

        s = Sabores()
        s.nombreSabor = request.form['sabor']
        s.insertar()
        flash('Sabor guardado con exito')
        return redirect(url_for('nuevoSabor'))
#PAGINAS DE ERROR
@app.errorhandler(404)
def error_404(e):
    return render_template('comunes/error_404.html'),404

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)