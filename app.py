from flask import Flask, url_for, render_template, request, redirect 
from flask_sqlalchemy import SQLAlchemy

# Le damos el nombre app, __name__ representa el modulo 
app = Flask(__name__)

# Establecemos las configuraciones basicas de la página 
# Le damos la direccion y en que db se almacenaran los datos 
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Asignamos una secret key a nuestra db 
app.config ['SECRET_KEY'] = 'penguin'

# Le paso el argumento app a la clase AQLAlchemy para establecer una conexión entre Flask y SQLAlchemy lo que nos va a permitir usar la db para acceder a los metodos y atributos de SQLAlchemy 


db = SQLAlchemy(app)

# Creamos la clase usuario y le damos como atributo db.Model
# db.Model es una clase ya existente de SQLAlchemy y nos permite usar funcionalidades para crear la db. 
class User (db.Model):
    id = db.Column(db.Integer, primary_key = True) # db es database, interger es porque va a ser un numero, primary key es porque va a ser un codigo unico 
    nombre = db.Column(db.String(50)) # Asignar cuantos caracteres como max 
    email = db.Column(db.String(50))
    contacto = db.Column(db.String(50))
    descripcion = db.Column(db.String(1000))
    equipo = db.Column(db.String(100))
    funding = db.Column(db.Integer)
    fase = db.Column(db.String(50))
    categoria = db.Column(db.String(50))
    logros = db.Column(db.String(500))
    contraseña = db.Column(db.String(10))

    def __init__(self, nombre, email, contacto, descripcion, equipo, funding, fase, categoria, logros, contraseña):
        self.nombre = nombre 
        self.email = email
        self.contacto = contacto 
        self.descripcion = descripcion
        self.equipo = equipo
        self.funding = funding
        self.fase = fase
        self.categoria = categoria
        self.logros = logros
        self.contraseña = contraseña

    # App context se encarga de que se ejecute create all en el contexto de flask, para evitar errores en la config de la db. 
with app.app_context():
        
        # Se encarga de crear las tablas que establecimos anteriormente 
    db.create_all()

    #Creamos las rutas para nuestra web. 
    @app.route('/') # Esta funcion es para dar inicio a la ruta 
    def inicio():
        return render_template('index.html')
    
    # Ruta de registro 
@app.route('/registro', methods = ['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre_su = request.form['nombre']
        email_su = request.form['email']
        contacto_su = request.form['contacto']
        descripcion_su = request.form['descripcion']
        equipo_su = request.form['equipo']
        funding_su = request.form['funding']
        fase_su = request.form['fase']
        categoria_su = request.form['categoria']
        logros_su = request.form['logros']
        contraseña_su = request.form['contraseña']

            # Le pasamos a la clase usuario los atributos o variables que acabamos de crear

        usuario = User(nombre_su, email_su, contacto_su, descripcion_su, equipo_su, funding_su, fase_su, categoria_su, logros_su, contraseña_su)
        
        # Agregamos el usuario en la base de datos 
        db.session.add(usuario)

        # Para confirmar y aplicar los cambios dentro de la db se usa 
        db.session.commit()

        # Declarar una variable global para que sea accesible desde cualquier parte del codigo y que le daremos el nombre que querramos 
        global usuario_actual 
        usuario_actual = usuario.id 

        return redirect(url_for ('inicio'))
    return render_template('signup.html')
    

    # Ruta para el login 
@app.route('/login')
def login():
    return render_template('login.html')




if __name__ == '__main__':
        app.run(debug=True)
