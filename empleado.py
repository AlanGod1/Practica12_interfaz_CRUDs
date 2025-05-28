from conexion import obtener_conexion
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QComboBox
)

class VentanaEmpleados(QWidget):
    def __init__(self, conexion):
        super().__init__()
        self.conexion = conexion
        self.setWindowTitle("Catálogo de Empleados")
        self.setGeometry(100, 100, 700, 400)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID")

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre")

        self.genero_input = QComboBox()
        self.genero_input.addItems(["M", "F"])

        self.puesto_input = QComboBox()
        self.puesto_input.addItems(["encargado", "cajero", "administrador"])

        self.boton_agregar = QPushButton("Agregar")
        self.boton_actualizar = QPushButton("Actualizar")
        self.boton_eliminar = QPushButton("Eliminar")

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Género", "Puesto"])

        self.boton_agregar.clicked.connect(self.agregar)
        self.boton_actualizar.clicked.connect(self.actualizar)
        self.boton_eliminar.clicked.connect(self.eliminar)

        form_layout = QHBoxLayout()
        form_layout.addWidget(self.id_input)
        form_layout.addWidget(self.nombre_input)
        form_layout.addWidget(self.genero_input)
        form_layout.addWidget(self.puesto_input)
        form_layout.addWidget(self.boton_agregar)
        form_layout.addWidget(self.boton_actualizar)
        form_layout.addWidget(self.boton_eliminar)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.tabla)
        self.setLayout(layout)

        self.cargar_datos()

    def crear_empleado(self, id_emp, nombre, genero, puesto):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "INSERT INTO empleado VALUES (%s, %s, %s, %s)"
            values = id_emp, nombre, genero, puesto
            cursor.execute(query, values)
            conexion.commit()
            cursor.close()
            conexion.close()

    def leer_empleados(self):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM empleado")
            datos = cursor.fetchall()
            cursor.close()
            conexion.close()
            return datos
        return []

    def actualizar_empleado(self, id_emp, nombre, genero, puesto):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "UPDATE empleado SET nombre=%s, genero=%s, puesto=%s WHERE id_empleado=%s"
            values = nombre, genero, puesto, id_emp
            cursor.execute(query, values)
            conexion.commit()
            cursor.close()
            conexion.close()

    def eliminar_empleado(self, id_emp):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "DELETE FROM empleado WHERE id_empleado=%s"
            cursor.execute(query, (id_emp,))
            conexion.commit()
            cursor.close()
            conexion.close()

    def cargar_datos(self):
        self.tabla.setRowCount(0)
        datos = self.leer_empleados()
        for fila_idx, (id_empleado, nombre, genero, puesto) in enumerate(datos):
            self.tabla.insertRow(fila_idx)
            self.tabla.setItem(fila_idx, 0, QTableWidgetItem(str(id_empleado)))
            self.tabla.setItem(fila_idx, 1, QTableWidgetItem(nombre))
            self.tabla.setItem(fila_idx, 2, QTableWidgetItem(genero))
            self.tabla.setItem(fila_idx, 3, QTableWidgetItem(puesto))

    def agregar(self):
        id_emp = self.id_input.text()
        nombre = self.nombre_input.text()
        genero = self.genero_input.currentText()
        puesto = self.puesto_input.currentText()
        if id_emp and nombre:
            try:
                self.crear_empleado(id_emp, nombre, genero, puesto)
                self.cargar_datos()
                self.limpiar_campos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo agregar:\n{e}")
        else:
            QMessageBox.warning(self, "Campos vacíos", "Por favor completa todos los campos.")

    def actualizar(self):
        id_emp = self.id_input.text()
        nombre = self.nombre_input.text()
        genero = self.genero_input.currentText()
        puesto = self.puesto_input.currentText()
        if id_emp and nombre:
            try:
                self.actualizar_empleado(id_emp, nombre, genero, puesto)
                self.cargar_datos()
                self.limpiar_campos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo actualizar:\n{e}")
        else:
            QMessageBox.warning(self, "Campos vacíos", "Por favor completa todos los campos.")

    def eliminar(self):
        id_emp = self.id_input.text()
        if id_emp:
            try:
                self.eliminar_empleado(id_emp)
                self.cargar_datos()
                self.limpiar_campos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar:\n{e}")
        else:
            QMessageBox.warning(self, "ID requerido", "Por favor ingresa el ID del empleado.")

    def limpiar_campos(self):
        self.id_input.clear()
        self.nombre_input.clear()
        self.genero_input.setCurrentIndex(0)
        self.puesto_input.setCurrentIndex(0)


