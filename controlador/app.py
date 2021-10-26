from flask import Flask,render_template,request

app=Flask(__name__, template_folder='../vista', static_folder='../static')

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

@app.route('/usuarios/consultarUsuarios')
def consultarUsuarios():
    return render_template('usuarios/consultar.html')

if __name__ == '__main__':
    app.run(debug=True)