import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from config import DevelopmentConfig
from models.models import *
# Inicializar la aplicación Flask
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.secret_key = "clavesecretapizzeria"

# Inicializar extensiones
csrf = CSRFProtect(app)
db.init_app(app)

 
# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.login_message = "Debes iniciar sesión para acceder a esta página."
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registrar Blueprints
from routes.auth_routes import auth_bp
from routes.cliente_routes import cliente_bp
from routes.proveedor_routes import provedor_bp

app.register_blueprint(auth_bp, url_prefix='/')
app.register_blueprint(cliente_bp)
app.register_blueprint(provedor_bp)
@app.route('/')
def index():
    return redirect(url_for('auth.login'))
# Crear la base de datos si no existe
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
