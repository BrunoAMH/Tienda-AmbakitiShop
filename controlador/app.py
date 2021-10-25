from flask import Flask,render_template

app=Flask(__name__, template_folder='../vista')

@app.route('/')
def inicio():
    return render_template('comunes/index.html')

if __name__ == '__main__':
    app.run(debug=True)