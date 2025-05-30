from conexion import obtener_conexion
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QSpinBox, QHeaderView, QComboBox
)
from PyQt6.QtCore import QDate
from datetime import datetime


class VentanaVenta(QWidget):
    def __init__(self, conexion):
        super().__init__()
        self.conexion = conexion
        self.setWindowTitle("Realizar Venta")
        self.setGeometry(100, 100, 1000, 600)

        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("Teléfono del cliente")

        self.boton_buscar_cliente = QPushButton("Buscar cliente")
        self.boton_buscar_cliente.clicked.connect(self.buscar_cliente)

        self.cliente_info_label = QLabel("Cliente: -")
        
        self.id_empleado_input = QLineEdit()
        self.id_empleado_input.setPlaceholderText("ID del empleado")

        self.codigo_input = QLineEdit()
        self.codigo_input.setMaxLength(13)
        self.codigo_input.setPlaceholderText("Código del articulo")
        self.codigo_input.returnPressed.connect(self.buscar_y_agregar_articulo)

        self.forma_pago_combo = QComboBox()
        self.forma_pago_combo.addItems(["Efectivo", "Tarjeta"])


        self.boton_agregar_articulo = QPushButton("Agregar articulo")
        self.boton_agregar_articulo.clicked.connect(self.buscar_y_agregar_articulo)

        self.boton_cancelar_venta = QPushButton("Cancelar venta")
        self.boton_cancelar_venta.clicked.connect(self.limpiar)

        self.tabla_articulos = QTableWidget()
        self.tabla_articulos.setColumnCount(5)
        self.tabla_articulos.setHorizontalHeaderLabels(["Código", "Nombre", "Cantidad", "Subtotal", "Eliminar"])
        self.tabla_articulos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.label_total = QLabel("Total: $0.00")

        self.boton_guardar_venta = QPushButton("Guardar venta")
        self.boton_guardar_venta.clicked.connect(self.guardar_venta)

        layout_form = QHBoxLayout()
        layout_form.addWidget(self.telefono_input)
        layout_form.addWidget(self.boton_buscar_cliente)
        layout_form.addWidget(self.id_empleado_input)
        layout_form.addWidget(self.codigo_input)
        layout_form.addWidget(self.forma_pago_combo)
        layout_form.addWidget(self.boton_agregar_articulo)
        layout_form.addWidget(self.boton_cancelar_venta)

        layout = QVBoxLayout()
        layout.addLayout(layout_form)
        layout.addWidget(self.cliente_info_label)
        layout.addWidget(self.tabla_articulos)
        layout.addWidget(self.label_total)
        layout.addWidget(self.boton_guardar_venta)
        self.setLayout(layout)

        self.articulos_agregados = []

    def buscar_cliente(self):
        telefono = self.telefono_input.text()
        if not telefono:
            QMessageBox.warning(self, "Faltan datos", "Ingresa el teléfono del cliente.")
            return

        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre, direccion FROM cliente WHERE telefono = %s", (telefono,))
            resultado = cursor.fetchone()
            if resultado:
                nombre, direccion = resultado
                self.cliente_info_label.setText(f"Cliente: {nombre} - Dirección: {direccion}")
            else:
                self.cliente_info_label.setText("Cliente no encontrado.")
        finally:
            cursor.close()
            conexion.close()

    def buscar_y_agregar_articulo(self):
        codigo = self.codigo_input.text()
        cantidad = 1

        if not codigo:
            QMessageBox.warning(self, "Código vacío", "Por favor ingresa o escanea un código de barras.")
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
                    self.articulos_agregados.append((codigo, nombre, cantidad, precio))

                    fila = self.tabla_articulos.rowCount()
                    self.tabla_articulos.insertRow(fila)
                    self.tabla_articulos.setItem(fila, 0, QTableWidgetItem(codigo))
                    self.tabla_articulos.setItem(fila, 1, QTableWidgetItem(nombre))

                    spinbox = QSpinBox()
                    spinbox.setRange(1, 1000)
                    spinbox.setValue(cantidad)
                    spinbox.valueChanged.connect(self.actualizar_total)
                    self.tabla_articulos.setCellWidget(fila, 2, spinbox)

                    self.tabla_articulos.setItem(fila, 3, QTableWidgetItem(f"${subtotal:.2f}"))

                    btn_eliminar = QPushButton("Eliminar")
                    btn_eliminar.clicked.connect(lambda _, f=fila: self.eliminar_articulo(f))
                    self.tabla_articulos.setCellWidget(fila, 4, btn_eliminar)

                    self.codigo_input.clear()
                    self.codigo_input.setFocus()
                    self.actualizar_total()
                else:
                    QMessageBox.warning(self, "No encontrado", "El articulo no fue encontrado.")
            finally:
                cursor.close()
                conexion.close()

    def actualizar_total(self):
        total = 0
        for fila in range(self.tabla_articulos.rowCount()):
            spinbox = self.tabla_articulos.cellWidget(fila, 2)
            cantidad = spinbox.value() if spinbox else 0
            precio = self.articulos_agregados[fila][3]
            subtotal = cantidad * precio
            self.tabla_articulos.setItem(fila, 3, QTableWidgetItem(f"${subtotal:.2f}"))
            total += subtotal
            # Actualizar en memoria
            codigo, nombre, _, _ = self.articulos_agregados[fila]
            self.articulos_agregados[fila] = (codigo, nombre, cantidad, precio)
        self.label_total.setText(f"Total: ${total:.2f}")

    def eliminar_articulo(self, fila):
        self.tabla_articulos.removeRow(fila)
        if fila < len(self.articulos_agregados):
            del self.articulos_agregados[fila]
        self.actualizar_total()

    def guardar_venta(self):
        telefono = self.telefono_input.text()
        id_empleado = self.id_empleado_input.text()
        fecha = datetime.now().date()
        total = sum(c * p for _, _, c, p in self.articulos_agregados)
        forma_pago = self.forma_pago_combo.currentText()

        if not telefono or not id_empleado or not self.articulos_agregados:
            QMessageBox.warning(self, "Campos incompletos", "Completa todos los campos y agrega articulos.")
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

                for codigo, _, cantidad, precio in self.articulos_agregados:
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
        self.cliente_info_label.setText("Cliente: -")
        self.tabla_articulos.setRowCount(0)
        self.label_total.setText("Total: $0.00")
        self.articulos_agregados.clear()
        self.codigo_input.setFocus()
