from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from forms.proveedores_form import ProveedorForm
from models.models import Proveedores, db

provedor_bp = Blueprint('provedor_bp', __name__, url_prefix='/proveedores')

@provedor_bp.route("/proveedores")
@login_required
def index():
  
    create_form = ProveedorForm(request.form)
    proveedores = Proveedores.query.all()
    proveedores_ordenados = sorted(proveedores, key=lambda x: x.estatus, reverse=True)
    return render_template("proveedores/proveedores.html", form=create_form, proveedores=proveedores_ordenados)

@provedor_bp.route("/cambiar-estatus", methods=["POST"])
@login_required
def cambiar_estatus():
    proveedor_id = request.form.get("id")
    proveedor = Proveedores.query.get(proveedor_id)

    if not proveedor:
        flash("Proveedor no encontrado", "error")
        return redirect(url_for("provedor_bp.index"))

    nuevo_estatus = int(request.form.get("estatus", proveedor.estatus))
    proveedor.estatus = nuevo_estatus
    db.session.commit()

    if nuevo_estatus == 1:
        flash("¡Proveedor activado correctamente!", "success")
    else:
        flash("¡Proveedor desactivado correctamente!", "warning")
    return redirect(url_for("provedor_bp.index"))

# Unificamos las dos rutas 'register' en una sola
@provedor_bp.route("/register", methods=["GET", "POST"])
@login_required
def register():
    form = ProveedorForm(request.form)
    if form.validate_on_submit():
        try:
            proveedor = Proveedores(
                nombre=form.nombre.data,
                telefono=form.telefono.data,
                email=form.email.data,
                insumo=form.insumo.data,
                estatus=1  # Siempre activo al crear
            )
            db.session.add(proveedor)
            db.session.commit()
            flash("Proveedor agregado correctamente", "success")
            return redirect(url_for('provedor_bp.index'))
        except Exception as e:
            flash(f"Error al agregar proveedor: {str(e)}", "error")
    
    return render_template("proveedores/register.html", form=form)

@provedor_bp.route('/modificar', methods=["GET", "POST"])

def modificar():
    create_form = ProveedorForm(request.form)
    
    if request.method == "GET":
        # Obtener el ID de la URL
        id = request.args.get('id')
        
        # Buscar el proveedor en la base de datos por su ID
        proveedor = db.session.query(Proveedores).filter(Proveedores.id == id).first()
        
        # Si se encuentra el proveedor, completar los datos en el formulario
        if proveedor:
            create_form.id.data = proveedor.id
            create_form.nombre.data = proveedor.nombre
            create_form.telefono.data = proveedor.telefono
            create_form.email.data = proveedor.email
            create_form.insumo.data = proveedor.insumo
        else:
            flash("Proveedor no encontrado", "error")
            return redirect(url_for('provedor_bp.index'))
    
    elif request.method == "POST":
        # Obtener el ID del formulario
        id = create_form.id.data
        
        # Buscar el proveedor en la base de datos
        proveedor = db.session.query(Proveedores).filter(Proveedores.id == id).first()
        
        # Verificar si se encuentra el proveedor
        if proveedor:
            proveedor.nombre = create_form.nombre.data
            proveedor.telefono = create_form.telefono.data
            proveedor.email = create_form.email.data
            proveedor.insumo = create_form.insumo.data
            proveedor.estatus = 1  # Reactivar el proveedor al actualizar

            # Confirmar la actualización en la base de datos
            db.session.commit()
            flash("Proveedor actualizado correctamente", "success")
        else:
            flash("Proveedor no encontrado", "error")
        
        # Redirigir a la vista de listado de proveedores
        return redirect(url_for('provedor_bp.index'))

    # Listar todos los proveedores (aunque no se utiliza en este caso)
    proveedores = Proveedores.query.all()
    return render_template("Proveedores/update.html", form=create_form, proveedores=proveedores, modificar_modal=True)

