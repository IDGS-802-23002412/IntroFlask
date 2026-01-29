from flask import Flask, render_template, request
from math import sqrt
from flask import flash
from flask_wtf.csrf import CSRFProtect
import forms

app = Flask(__name__)
app.secret_key = 'Clave secreta'
csrf = CSRFProtect()

@app.route('/')
def index():
    titulo="IDGS-802-Flask"
    lista={'Juan', 'Karla', 'Miguel', 'Ana'}
    return render_template('index.html', titulo=titulo, lista=lista)

@app.route("/usuarios" , methods=["GET", "POST"])
def usuarios():
    mat = 0
    nom = ''
    apa = ''
    ama = ''
    email = ''
    usuarios_class = forms.UserForm(request.form)
    
    if request.method == 'POST' and usuarios_class.validate():
        mat = usuarios_class.matricula.data 
        nom = usuarios_class.nombre.data 
        apa = usuarios_class.apaterno.data
        ama = usuarios_class.amaterno.data 
        email = usuarios_class.correo.data

        mensaje = 'Bienvenido {}'.format(nom)
        flash(mensaje)

    return render_template("usuarios.html", form=usuarios_class, 
                           mat=mat, nom=nom, apa=apa,ama=ama, email=email)

@app.route ("/formularios")
def formularios():
    return render_template("formularios.html")

@app.route ("/reportes")
def reportes():
    return render_template("reportes.html")

@app.route('/hola')
def hola():
    return "¡Hola, hola!"

@app.route('/user/<string:user>')
def user(user):
    return f"Hello, {user}!"

@app.route("/numero/<int:n>")
def numero(n):
    return "Numero: {}".format(n)

@app.route("/user/<int:id>/<string:username>")
def user_info(id, username):
    return "ID: {} nombre: {}".format(id, username)

@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1, n2):
    return "La suma es: {}".format(n1 + n2)

@app.route("/default")
@app.route("/default/<string:param>")
def default(param="juan"):
    return f"<h1>¡Hola, {param}!</h1>"

@app.route("/opera")
def opera():
    return '''
    <form>
        <label for="name"> Name: </label>
        <input type="text" id="name" name="name" required>

        <label for="name"> apaterno: </label>
        <input type="text" id="name" name="name" required>
    <form>
    '''

@app.route("/operasBas" , methods=["GET","POST"])
def operasBas():
    n1=0
    n2=0
    res=0
    if request.method == "POST":
        n1=request.form.get("n1")
        n2=request.form.get("n2")
        res=float(n1)+float(n2)
    
    return render_template("operasBas.html",n1=n1, n2=n2, res=res)

@app.route("/resultado", methods=["GET","POST"])
def resultado():
    n1 = request.form.get("n1")
    n2 = request.form.get("n2")
    operacion = request.form.get("operacion")

    if operacion == "suma":     
        return f"La suma es: {float(n1)+float(n2)}"
    elif operacion == "restar":
        return f"La resta es: {float(n1)-float(n2)}"
    elif operacion == "multiplicacion":
        return f"La multiplicacion es: {float(n1)*float(n2)}"
    else: 
        return f"La division es: {float(n1)/float(n2)}"

@app.route("/alumnos")
def alumnos():

    return render_template("alumnos.html")

@app.route("/distancia", methods=["GET","POST"])
def distancia():
    x1=0
    y1=0
    x2=0
    y2=0
    res=0
    if request.method == "POST":
        x1=float(request.form.get("x1"))
        y1=float(request.form.get("y1"))
        x2=float(request.form.get("x2"))
        y2=float(request.form.get("y2"))
        res= sqrt((x2 - x1)**2 + (y2 - y1)**2)

    return render_template("distancia.html",x1=x1, y1=y1, x2=x2, y2=y2, res=res)

@app.route("/cinepolis", methods=["GET", "POST"])
def cinepolis():
    precioBoleta = 12
    total = 0
    mensaje = ""

    if request.method == "POST":
        nombre = request.form.get("nombre")
        cantidadCompradores = int(request.form.get("cantidadCompradores"))
        cantidadBoletas = int(request.form.get("cantidadBoletas"))
        tarjetaCineco = request.form.get("opcion")

        maxBoletos = cantidadCompradores * 7

        if cantidadBoletas > maxBoletos:
            mensaje = (
                f"{nombre}"
                f"No puedes comprar más de "
                f"{maxBoletos} boletas por cantidad de compradores "
            )   
            return render_template("cinepolis.html", mensaje=mensaje)

        subtotal = cantidadBoletas * precioBoleta

        if cantidadBoletas > 5:
            subtotal *= 0.85
        elif cantidadBoletas >= 3:
            subtotal *= 0.90

        if tarjetaCineco == "Si":
            total = subtotal * 0.90
        else:
            total = subtotal

        return render_template("cinepolis.html",total=total,mensaje=mensaje)

    return render_template("cinepolis.html")

if __name__ == '__main__':
    csrf.init_app(app)
    app.run(debug=True)
