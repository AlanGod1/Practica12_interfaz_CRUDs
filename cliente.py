from conexion import obtener_conexion
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)



class VentanaClientes(QWidget):
    def __init__(self, conexion):
        super().__init__()
        self.conexion = conexion
        self.setWindowTitle("Catálogo de Clientes")
        self.setGeometry(100, 100, 800, 400)

        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("Teléfono")

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre")

        self.direccion_input = QLineEdit()
        self.direccion_input.setPlaceholderText("Dirección")

        self.rfc_input = QLineEdit()
        self.rfc_input.setPlaceholderText("RFC (opcional)")

        self.boton_agregar = QPushButton("Agregar")
        self.boton_actualizar = QPushButton("Actualizar")
        self.boton_eliminar = QPushButton("Eliminar")

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Teléfono", "Nombre", "Dirección", "RFC"])

        self.boton_agregar.clicked.connect(self.agregar)
        self.boton_actualizar.clicked.connect(self.actualizar)
        self.boton_eliminar.clicked.connect(self.eliminar)

        form_layout = QHBoxLayout()
        form_layout.addWidget(self.telefono_input)
        form_layout.addWidget(self.nombre_input)
        form_layout.addWidget(self.direccion_input)
        form_layout.addWidget(self.rfc_input)
        form_layout.addWidget(self.boton_agregar)
        form_layout.addWidget(self.boton_actualizar)
        form_layout.addWidget(self.boton_eliminar)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.tabla)
        self.setLayout(layout)

        self.cargar_datos()

    def crear_cliente(self, telefono, nombre, direccion, rfc):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "INSERT INTO cliente VALUES (%s, %s, %s, %s)"
            values = telefono, nombre, direccion, rfc
            cursor.execute(query, values)
            conexion.commit()
            cursor.close()
            conexion.close()

    def leer_clientes(self):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM cliente")
            datos = cursor.fetchall()
            cursor.close()
            conexion.close()
            return datos
        return []

    def actualizar_cliente(self, telefono, nombre, direccion, rfc):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "UPDATE cliente SET nombre=%s, direccion=%s, rfc=%s WHERE telefono=%s"
            values = nombre, direccion, rfc, telefono
            cursor.execute(query, values)
            conexion.commit()
            cursor.close()
            conexion.close()

    def eliminar_cliente(self, telefono):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "DELETE FROM cliente WHERE telefono=%s"
            values = (telefono,)
            cursor.execute(query, values)
            conexion.commit()
            cursor.close()
            conexion.close()

    def cargar_datos(self):
        self.tabla.setRowCount(0)
        datos = self.leer_clientes()
        for fila_idx, (telefono, nombre, direccion, rfc) in enumerate(datos):
            self.tabla.insertRow(fila_idx)
            self.tabla.setItem(fila_idx, 0, QTableWidgetItem(telefono))
            self.tabla.setItem(fila_idx, 1, QTableWidgetItem(nombre))
            self.tabla.setItem(fila_idx, 2, QTableWidgetItem(direccion))
            self.tabla.setItem(fila_idx, 3, QTableWidgetItem(rfc if rfc else ""))

    def agregar(self):
        telefono = self.telefono_input.text()
        nombre = self.nombre_input.text()
        direccion = self.direccion_input.text()
        rfc = self.rfc_input.text() or None
        if telefono and nombre and direccion:
            try:
                self.crear_cliente(telefono, nombre, direccion, rfc)
                self.cargar_datos()
                self.limpiar_campos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo agregar:\n{e}")
        else:
            QMessageBox.warning(self, "Campos vacíos", "Por favor completa todos los campos obligatorios.")

    def actualizar(self):
        telefono = self.telefono_input.text()
        nombre = self.nombre_input.text()
        direccion = self.direccion_input.text()
        rfc = self.rfc_input.text() or None
        if telefono and nombre and direccion:
            try:
                self.actualizar_cliente(telefono, nombre, direccion, rfc)
                self.cargar_datos()
                self.limpiar_campos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo actualizar:\n{e}")
        else:
            QMessageBox.warning(self, "Campos vacíos", "Por favor completa todos los campos obligatorios.")

    def eliminar(self):
        telefono = self.telefono_input.text()
        if telefono:
            try:
                self.eliminar_cliente(telefono)
                self.cargar_datos()
                self.limpiar_campos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar:\n{e}")
        else:
            QMessageBox.warning(self, "Teléfono requerido", "Por favor ingresa el teléfono del cliente a eliminar.")

    def limpiar_campos(self):
        self.telefono_input.clear()
        self.nombre_input.clear()
        self.direccion_input.clear()
        self.rfc_input.clear()

