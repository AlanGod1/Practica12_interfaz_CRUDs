from conexion import obtener_conexion
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QSpinBox, QComboBox
)
from PyQt6.QtCore import QDate, Qt
from datetime import datetime

class VentanaVenta(QWidget):
    def __init__(self, conexion):
        super().__init__()
        self.conexion = conexion
        self.setWindowTitle("Realizar Venta")
        self.setGeometry(100, 100, 1000, 500)

        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("Teléfono del cliente")

        self.id_empleado_input = QLineEdit()
        self.id_empleado_input.setPlaceholderText("ID del empleado")

        self.forma_pago_combo = QComboBox()
        self.forma_pago_combo.addItems(["Efectivo", "Targeta"])

        self.codigo_input = QLineEdit()
        self.codigo_input.setMaxLength(13)
        self.codigo_input.setPlaceholderText("Código del producto")
        self.codigo_input.returnPressed.connect(self.buscar_y_agregar_producto)

        self.boton_agregar_producto = QPushButton("Agregar producto")
        self.boton_agregar_producto.clicked.connect(self.buscar_y_agregar_producto)

        self.boton_cancelar_venta = QPushButton("Cancelar venta")
        self.boton_cancelar_venta.clicked.connect(self.limpiar)

        self.tabla_productos = QTableWidget()
        self.tabla_productos.setColumnCount(5)
        self.tabla_productos.setHorizontalHeaderLabels(["Código", "Nombre", "Cantidad", "Subtotal", "Eliminar"])

        self.label_total = QLabel("Total: $0.00")

        self.boton_guardar_venta = QPushButton("Guardar venta")
        self.boton_guardar_venta.clicked.connect(self.guardar_venta)

        layout_form = QHBoxLayout()
        layout_form.addWidget(self.telefono_input)
        layout_form.addWidget(self.id_empleado_input)
        layout_form.addWidget(self.forma_pago_combo)
        layout_form.addWidget(self.codigo_input)
        layout_form.addWidget(self.boton_agregar_producto)
        layout_form.addWidget(self.boton_cancelar_venta)

        layout = QVBoxLayout()
        layout.addLayout(layout_form)
        layout.addWidget(self.tabla_productos)
        layout.addWidget(self.label_total)
        layout.addWidget(self.boton_guardar_venta)
        self.setLayout(layout)

        self.productos_agregados = []

    def buscar_y_agregar_producto(self):
        codigo = self.codigo_input.text()
        cantidad = 1

        if not codigo:
            QMessageBox.warning(self, "Código vacío", "Por favor ingresa o escanea un código de barras.")
            return

        # Verifica si el producto ya fue agregado
        if any(p[0] == codigo for p in self.productos_agregados):
            QMessageBox.information(self, "Ya agregado", "Este producto ya está en el carrito.")
            return

        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT nombre, precio FROM articulo WHERE codigo = %s", (codigo,))
                resultado = cursor.fetchone()

                if resultado:
                    nombre, precio = resultado
                    subtotal = cantidad * precio
                    self.productos_agregados.append((codigo, nombre, cantidad, precio))

                    fila = self.tabla_productos.rowCount()
                    self.tabla_productos.insertRow(fila)

                    self.tabla_productos.setItem(fila, 0, QTableWidgetItem(codigo))
                    self.tabla_productos.setItem(fila, 1, QTableWidgetItem(nombre))

                    spinbox = QSpinBox()
                    spinbox.setRange(1, 1000)
                    spinbox.setValue(cantidad)
                    spinbox.valueChanged.connect(self.actualizar_subtotal)
                    self.tabla_productos.setCellWidget(fila, 2, spinbox)

                    subtotal_item = QTableWidgetItem(f"${subtotal:.2f}")
                    subtotal_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    self.tabla_productos.setItem(fila, 3, subtotal_item)

                    boton_eliminar = QPushButton("Eliminar")
                    boton_eliminar.clicked.connect(lambda _, fila=fila: self.eliminar_producto(fila))
                    self.tabla_productos.setCellWidget(fila, 4, boton_eliminar)

                    self.actualizar_subtotal()
                    self.codigo_input.clear()
                    self.codigo_input.setFocus()
                else:
                    QMessageBox.warning(self, "No encontrado", "El producto no fue encontrado.")
            finally:
                cursor.close()
                conexion.close()

    def actualizar_subtotal(self):
        total = 0.0
        for fila in range(self.tabla_productos.rowCount()):
            cantidad_widget = self.tabla_productos.cellWidget(fila, 2)
            cantidad = cantidad_widget.value()
            codigo = self.tabla_productos.item(fila, 0).text()

            for i, (c, n, _, p) in enumerate(self.productos_agregados):
                if c == codigo:
                    self.productos_agregados[i] = (c, n, cantidad, p)
                    subtotal = cantidad * p
                    self.tabla_productos.item(fila, 3).setText(f"${subtotal:.2f}")
                    total += subtotal
                    break

        self.label_total.setText(f"Total: ${total:.2f}")

    def eliminar_producto(self, fila):
        codigo = self.tabla_productos.item(fila, 0).text()
        self.productos_agregados = [p for p in self.productos_agregados if p[0] != codigo]
        self.tabla_productos.removeRow(fila)

        # Reasignar botones eliminar
        for f in range(self.tabla_productos.rowCount()):
            boton = self.tabla_productos.cellWidget(f, 4)
            boton.clicked.disconnect()
            boton.clicked.connect(lambda _, fila=f: self.eliminar_producto(fila))

        self.actualizar_subtotal()

    def guardar_venta(self):
        telefono = self.telefono_input.text()
        id_empleado = self.id_empleado_input.text()
        forma_pago = self.forma_pago_combo.currentText()
        fecha = datetime.now().date()
        total = sum(c * p for _, _, c, p in self.productos_agregados)

        if not telefono or not id_empleado or not self.productos_agregados:
            QMessageBox.warning(self, "Campos incompletos", "Por favor completa todos los campos y agrega productos.")
            return

        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT IFNULL(MAX(id_venta), 0) + 1 FROM venta")
                id_venta = cursor.fetchone()[0]

                cursor.execute(
                    "INSERT INTO venta (id_venta, fecha, importe, forma_pago, telefono, id_empleado) VALUES (%s, %s, %s, %s, %s, %s)",
                    (id_venta, fecha, total, forma_pago, telefono, id_empleado)
                )

                for codigo, _, cantidad, precio in self.productos_agregados:
                    cursor.execute(
                        "INSERT INTO detalles_venta (id_venta, codigo, cantidad, precio) VALUES (%s, %s, %s, %s)",
                        (id_venta, codigo, cantidad, precio)
                    )
                    cursor.execute(
                        "UPDATE articulo SET existencias = existencias - %s WHERE codigo = %s",
                        (cantidad, codigo)
                    )

                conexion.commit()
                QMessageBox.information(self, "Éxito", "Venta registrada correctamente.")
                self.limpiar()

            except Exception as e:
                conexion.rollback()
                QMessageBox.critical(self, "Error", f"Error al guardar la venta:\n{e}")
            finally:
                cursor.close()
                conexion.close()

    def limpiar(self):
        self.telefono_input.clear()
        self.id_empleado_input.clear()
        self.codigo_input.clear()
        self.tabla_productos.setRowCount(0)
        self.label_total.setText("Total: $0.00")
        self.productos_agregados.clear()
        self.codigo_input.setFocus()
