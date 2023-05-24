from flask import Flask, url_for, render_template, request, redirect 
import boto3 # Libreria de amazonws que te permite adjuntar videos sin subir 
import uuid # unique universal id 
from flask_sqlalchemy import SQLAlchemy

# Le damos el nombre app, __name__ representa el modulo 
app = Flask(__name__)

# Las extensiones que permitimos que se carguen 
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'mp4'} 

# Creamos una funcion en donde le indicamos desde donde empieza a leer para saber si es que se deja o no subir un archivo 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    filename = db.Column(db.String(100))
    file_url = db.Column(db.String(200))
    

    def __init__(self, nombre, email, contacto, descripcion, equipo, funding, fase, categoria, logros, contraseña, filename, file_url):
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
        self.filename = filename
        self.file_url = file_url 


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
        uploaded_file = request.files['new-file']

        if not allowed_file(uploaded_file.filename):
            return 'FILE NOT ALLOWED'
        
        # Crear un nuevo nombre para el archivo que se sube
        new_filename = uuid.uuid4().hex + '.' + uploaded_file.filename.rsplit('.', 1)[1].lower()
        bucket_name = '4myachubucket'
        s3 = boto3.resource('s3')
        s3.Bucket(bucket_name).upload_fileobj(uploaded_file, new_filename)
        file_url = 'https://4myachubucket.s3.us-east-2.amazonaws.com/{}'.format(new_filename)
        new_file = User(new_filename, file_url, nombre_su, email_su,contacto_su, descripcion_su, equipo_su, funding_su, fase_su, categoria_su, logros_su, contraseña_su)

        db.session.add(new_file)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('signup.html')


@app.route('/profile/<id>', methods = ['GET'])
def profile(id):
    files = User.query.filter_by(id=id).first()
    return render_template('profile.html', files=files)


    # Ruta para el login 
@app.route('/login', methods = ['GET', 'POST'])
def login():
    # Si el metodo es POST hace esto para pedir la info 
    if request.method == 'POST':
        nombre_usuario = request.form ['nombre']
        contraseña_usuario = request.form['contraseña']

        #Buscamos el usuario en la base de datos 
        usuario_existente = User.query.filter_by(nombre = nombre_usuario). first()
    
        # Si el usuario existe 
        if usuario_existente is not None: 

            #checkeamos que la contraseña ingresada sea la correcta 
            if usuario_existente.contraseña == contraseña_usuario:

                global usuario_actual 
                usuario_actual = usuario_existente.id 

                return redirect(url_for('inicio'))

            else: 
                return "Contraseña invalida"
        else: 
            return "El usuario no existe"

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
