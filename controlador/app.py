from flask import Flask,render_template,request
from flask_bootstrap import Bootstrap

app=Flask(__name__, template_folder='../vista', static_folder='../static')
Bootstrap(app)

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
    return render_template('usuarios/consultar.html')

#Sugerencias
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

if __name__ == '__main__':
    app.run(debug=True)