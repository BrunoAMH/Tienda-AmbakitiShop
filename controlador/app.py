from flask import Flask,render_template,request

app=Flask(__name__, template_folder='../vista')

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

if __name__ == '__main__':
    app.run(debug=True)