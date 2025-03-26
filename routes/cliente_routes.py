from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from datetime import datetime
from models.models import Cliente,db
import forms.cliente_form as forms
import os

cliente_bp = Blueprint("cliente", __name__, url_prefix="/cliente")

PRECIOS_PIZZA = {"Chica $40": 40, "Mediana $80": 80, "Grande $120": 120}
PRECIOS_INGREDIENTES = {"Jamon $10": 10, "Piña $10": 10, "Champiñones $10": 10}

@cliente_bp.route("/sistema", methods=["GET", "POST"])
@login_required
def sistema():
    busqueda_form = forms.BusquedaForm(request.form)
    pedido_form = forms.PedidoForm(request.form)
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    pedido_form.fecha_compra.data = fecha_actual

    pedidos = []
    if os.path.exists("pedidos_temp.txt"):
        with open("pedidos_temp.txt", "r") as archivo:
            for linea in archivo:
                datos = linea.strip().split(", ")
                pedido = {
                    "id": int(datos[0]),
                    "nombre": datos[1],
                    "direccion": datos[2],
                    "telefono": datos[3],
                    "fecha_compra": datos[4],
                    "tamanio": datos[5],
                    "ingredientes": datos[6],
                    "num_pizzas": int(datos[7]),
                    "subtotal": float(datos[8])
                }
                pedidos.append(pedido)

    ventas_del_dia = Cliente.query.filter(db.func.date(Cliente.fecha_compra) == fecha_actual).all()
    total_ventas_del_dia = sum(venta.total for venta in ventas_del_dia)

    if request.method == "POST":
        if "Agregar" in request.form and pedido_form.validate():
            nuevo_id = max([p["id"] for p in pedidos], default=0) + 1
            precio_base = PRECIOS_PIZZA[pedido_form.tamanioPizza.data]
            precio_ingrediente = PRECIOS_INGREDIENTES[pedido_form.ingredientes.data]
            subtotal = (precio_base + precio_ingrediente) * pedido_form.numPizzas.data

            with open("pedidos_temp.txt", "a") as archivo:
                archivo.write(f"{nuevo_id}, {pedido_form.nombre.data}, {pedido_form.direccion.data}, "
                              f"{pedido_form.telefono.data}, {pedido_form.fecha_compra.data}, "
                              f"{pedido_form.tamanioPizza.data}, {pedido_form.ingredientes.data}, "
                              f"{pedido_form.numPizzas.data}, {subtotal}\n")

            flash("Pizza agregada correctamente.", "success")
            return redirect(url_for('cliente.sistema'))
        elif "Quitar" in request.form:
            id_quitar = request.form.get("id_quitar")
            pedidos = [p for p in pedidos if str(p["id"]) != id_quitar]

            with open("pedidos_temp.txt", "w") as archivo:
                for p in pedidos:
                    archivo.write(f"{p['id']}, {p['nombre']}, {p['direccion']}, {p['telefono']}, "
                                  f"{p['fecha_compra']}, {p['tamanio']}, {p['ingredientes']}, {p['num_pizzas']}, {p['subtotal']}\n")

            flash("Producto eliminado del pedido", "info")
            return redirect(url_for('cliente.sistema'))  

        elif "Terminar" in request.form and pedidos:
            total = sum(p["subtotal"] for p in pedidos)
            nuevo_cliente = Cliente(
                nombre=pedidos[0]["nombre"], direccion=pedidos[0]["direccion"],
                telefono=pedidos[0]["telefono"], fecha_compra=datetime.strptime(pedidos[0]["fecha_compra"], '%Y-%m-%d'),
                total=total
            )
            db.session.add(nuevo_cliente)
            db.session.commit()
            os.remove("pedidos_temp.txt")
            flash(f"Pedido completado. Total a pagar: ${total}", "success")
            return redirect(url_for('cliente.sistema'))  

        elif "buscar" in request.form and busqueda_form.validate():
            fecha_obj = datetime.strptime(busqueda_form.fecha.data, '%Y-%m-%d')
            resultados_busqueda = Cliente.query.filter(db.func.date(Cliente.fecha_compra) == fecha_obj.date()).all()
            total_busqueda = sum(venta.total for venta in resultados_busqueda)
    return render_template("Cliente/index.html", pedido_form=pedido_form, busqueda_form=busqueda_form,
                           pedidos=pedidos, ventas_del_dia=ventas_del_dia,
                           total_ventas_del_dia=total_ventas_del_dia, fecha_actual=fecha_actual)
