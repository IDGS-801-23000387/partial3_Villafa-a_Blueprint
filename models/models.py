import datetime
from flask_sqlalchemy import SQLAlchemy  
from flask_login import UserMixin 
from werkzeug.security import generate_password_hash, check_password_hash  

db = SQLAlchemy()

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    fecha_compra = db.Column(db.Date, nullable=False)
    total = db.Column(db.Float, nullable=False)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)
class Proveedores(db.Model):  # Cambiamos de Alumnos a Proveedores
    __tablename__ = 'proveedores'  # Cambiamos el nombre de la tabla
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    telefono = db.Column(db.String(15))  # Nuevo campo para el teléfono
    email = db.Column(db.String(100))
    insumo = db.Column(db.String(50))
    estatus = db.Column(db.Integer, default=1)  # Estatus (0 o 1, por defecto 1)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now, server_default=db.func.now())
    
 