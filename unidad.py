from conexion import obtener_conexion
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)


class VentanaUnidad(QWidget):
    def __init__(self, conexion):
        super().__init__()
        self.conexion = conexion
        self.setWindowTitle("Catálogo de Unidades")
        self.setGeometry(100, 100, 600, 400)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID")

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre")

        self.boton_agregar = QPushButton("Agregar")
        self.boton_actualizar = QPushButton("Actualizar")
        self.boton_eliminar = QPushButton("Eliminar")

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(2)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre"])

        self.boton_agregar.clicked.connect(self.agregar)
        self.boton_actualizar.clicked.connect(self.actualizar)
        self.boton_eliminar.clicked.connect(self.eliminar)

        form_layout = QHBoxLayout()
        form_layout.addWidget(self.id_input)
        form_layout.addWidget(self.nombre_input)
        form_layout.addWidget(self.boton_agregar)
        form_layout.addWidget(self.boton_actualizar)
        form_layout.addWidget(self.boton_eliminar)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.tabla)
        self.setLayout(layout)

        self.cargar_datos()

    def crear_unidad(self, id, nombre):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "INSERT INTO unidad VALUES (%s, %s)"
            values = id, nombre
            cursor.execute(query, values)
            conexion.commit()
            cursor.close()
            conexion.close()

    def leer_unidad(self):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM unidad")
            datos = cursor.fetchall()
            cursor.close()
            conexion.close()
            return datos
        return []

    def actualizar_unidad(self, id_unidad, nombre):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "UPDATE unidad SET nombre=%s WHERE id_unidad=%s"
            values = nombre, id_unidad
            cursor.execute(query, values)
            conexion.commit()
            cursor.close()
            conexion.close()

    def eliminar_unidad(self, id_unidad):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "DELETE FROM unidad WHERE id_unidad=%s"
            values = id_unidad,
            cursor.execute(query, values)
            conexion.commit()
            cursor.close()
            conexion.close()


    def cargar_datos(self):
        self.tabla.setRowCount(0)
        datos = self.leer_unidad()
        for fila_idx, (id_unidad, nombre) in enumerate(datos):
            self.tabla.insertRow(fila_idx)
            self.tabla.setItem(fila_idx, 0, QTableWidgetItem(str(id_unidad)))
            self.tabla.setItem(fila_idx, 1, QTableWidgetItem(nombre))

    def agregar(self):
        idunidad = self.id_input.text()
        nombre = self.nombre_input.text()
        if idunidad and nombre:
            try:
                self.crear_unidad(idunidad, nombre)
                self.cargar_datos()
                self.id_input.clear()
                self.nombre_input.clear()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo agregar:\n{e}")
        else:
            QMessageBox.warning(self, "Campos vacíos", "Por favor completa todos los campos.")

    def actualizar(self):
        idunidad = self.id_input.text()
        nombre = self.nombre_input.text()
        if idunidad and nombre:
            try:
                self.actualizar_unidad(int(idunidad), nombre)
                self.cargar_datos()
                self.id_input.clear()
                self.nombre_input.clear()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo actualizar:\n{e}")
        else:
            QMessageBox.warning(self, "Campos vacíos", "Por favor completa todos los campos.")


    def eliminar(self):
        idunidad = self.id_input.text()
        if idunidad:
            try:
                self.eliminar_unidad(int(idunidad))
                self.cargar_datos()
                self.id_input.clear()
                self.nombre_input.clear()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar:\n{e}")
        else:
            QMessageBox.warning(self, "ID requerido", "Por favor ingresa el ID a eliminar.")

