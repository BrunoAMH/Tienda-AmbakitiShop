
import urllib

from flask import Flask,render_template,request,flash,redirect,url_for,abort
from flask_bootstrap import Bootstrap
from flask_login import current_user,login_user,logout_user,login_manager,login_required,LoginManager
from modelo.DAO import db,Usuario

app=Flask(__name__, template_folder='../vista', static_folder='../static')
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='cl4v3'



@app.route('/')
def inicio():
    return render_template('comunes/index.html')


#USUARIOS
@app.route('/usuarios/registrarNuevo')
def nuevoUsuario():
    return render_template('usuarios/nuevo.html')

@app.route('/usuarios/creacionCuenta', methods=['post'])
def registrarUsuario():
    nombre=request.form['nombre']
    return "usuario registrado de nombre: " + nombre

@app.route('/usuarios/editarUsuario')
def editarUsuario():
    return render_template('usuarios/editar.html')

@app.route('/usuarios/login')
def login():
    return render_template('usuarios/login.html')

@app.route('/usuarios/iniciandoSesion', methods=['post'])
def iniciandoSesion():
    correo=request.form['correo']
    return "iniciando sesion con " + correo

@app.route('/usuarios/consultarUsuarios')
def consultarUsuarios():
    u = Usuario()
    return render_template('usuarios/consultar.html',usuarios = u.consultaGeneral())

@app.route('/usuarios/guardarCambios', methods=['post'])
def guardarCambios():
    nombre=request.form['nombre']
    return "cambios guardados del usuarios " + nombre



#DIRECCION
@app.route('/usuarios/editarDireccion')
def editarDireccion():
    return render_template('/direcciones/editar.html')

#SUGERENCIAS
@app.route('/sugerencias/nuevaSugerencia')
def nuevaSugerencia():
    return render_template('/sugerencias/nueva.html')

@app.route('/sugerencias/consultarSugerencias')
def consultarSugerencia():
    return render_template('/sugerencias/consultar.html')

#PRODUCTOS
@app.route('/productos/consultarProductos')
def consultarProductos():
    return render_template('/productos/consultar.html')

@app.route('/productos/agregarProducto')
def agregarProducto():
    return render_template('/productos/nuevo.html')
#PEDIDOS
@app.route('/pedidos/MisPedidos')
def misPedidos():
    return render_template('/pedidos/consultar.html')

#CARRITO
@app.route('/carrito/consultar')
def miCarrito():
    return render_template('/carrito/consultar.html')

#TARJETAS
@app.route('/tarjeta/anadir')
def agregarTarjeta():
    return render_template('/tarjetas/nueva.html')

@app.route('/comunes/prueba')
def comun():
    return render_template('/comunes/prueba.html')

@app.route('/tarjetas/confirmaCompra', methods=['post'])
def confirmarCompra():
    return "Compra confirmada"

#DESCUENTOS
@app.route('/descuentos/consultar')
def consultarDescuentos():
    return render_template('/descuentos/consultar.html')


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)