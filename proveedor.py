from conexion import obtener_conexion
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)

def crear_proveedor(id_proveedor, nombre, telefono):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        query = "INSERT INTO proveedores (id_proveedor, nombre, telefono) VALUES (%s, %s, %s)"
        values = id_proveedor, nombre, telefono
        cursor.execute(query, values)
        conexion.commit()
        cursor.close()
        conexion.close()

def leer_proveedores():
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_proveedor, nombre, telefono FROM proveedores")
        datos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return datos
    return []

def actualizar_proveedor(id_proveedor, nombre, telefono):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        query = "UPDATE proveedores SET nombre=%s, telefono=%s WHERE id_proveedor=%s"
        values = nombre, telefono, id_proveedor
        cursor.execute(query, values)
        conexion.commit()
        cursor.close()
        conexion.close()

def eliminar_proveedor(id_proveedor):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        query = "DELETE FROM proveedores WHERE id_proveedor=%s"
        values = (id_proveedor,)
        cursor.execute(query, values)
        conexion.commit()
        cursor.close()
        conexion.close()

class VentanaProveedores(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Catálogo de Proveedores")
        self.setGeometry(100, 100, 700, 400)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID Proveedor")

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre")

        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("Teléfono")

        self.boton_agregar = QPushButton("Agregar")
        self.boton_actualizar = QPushButton("Actualizar")
        self.boton_eliminar = QPushButton("Eliminar")

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Teléfono"])

        self.boton_agregar.clicked.connect(self.agregar)
        self.boton_actualizar.clicked.connect(self.actualizar)
        self.boton_eliminar.clicked.connect(self.eliminar)

        form_layout = QHBoxLayout()
        form_layout.addWidget(self.id_input)
        form_layout.addWidget(self.nombre_input)
        form_layout.addWidget(self.telefono_input)
        form_layout.addWidget(self.boton_agregar)
        form_layout.addWidget(self.boton_actualizar)
        form_layout.addWidget(self.boton_eliminar)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.tabla)
        self.setLayout(layout)

        self.cargar_datos()

    def cargar_datos(self):
        self.tabla.setRowCount(0)
        datos = leer_proveedores()
        for fila_idx, (id_proveedor, nombre, telefono) in enumerate(datos):
            self.tabla.insertRow(fila_idx)
            self.tabla.setItem(fila_idx, 0, QTableWidgetItem(str(id_proveedor)))
            self.tabla.setItem(fila_idx, 1, QTableWidgetItem(nombre))
            self.tabla.setItem(fila_idx, 2, QTableWidgetItem(telefono))

    def agregar(self):
        try:
            id_proveedor = int(self.id_input.text())
            nombre = self.nombre_input.text()
            telefono = self.telefono_input.text()
            if nombre and telefono:
                crear_proveedor(id_proveedor, nombre, telefono)
                self.cargar_datos()
                self.limpiar_campos()
            else:
                QMessageBox.warning(self, "Campos vacíos", "Completa todos los campos.")
        except ValueError:
            QMessageBox.warning(self, "ID inválido", "El ID debe ser un número entero.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo agregar:\n{e}")

    def actualizar(self):
        try:
            id_proveedor = int(self.id_input.text())
            nombre = self.nombre_input.text()
            telefono = self.telefono_input.text()
            if nombre and telefono:
                actualizar_proveedor(id_proveedor, nombre, telefono)
                self.cargar_datos()
                self.limpiar_campos()
            else:
                QMessageBox.warning(self, "Campos vacíos", "Completa todos los campos.")
        except ValueError:
            QMessageBox.warning(self, "ID inválido", "El ID debe ser un número entero.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar:\n{e}")

    def eliminar(self):
        try:
            id_proveedor = int(self.id_input.text())
            eliminar_proveedor(id_proveedor)
            self.cargar_datos()
            self.limpiar_campos()
        except ValueError:
            QMessageBox.warning(self, "ID inválido", "El ID debe ser un número entero.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar:\n{e}")

    def limpiar_campos(self):
        self.id_input.clear()
        self.nombre_input.clear()
        self.telefono_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaProveedores()
    ventana.show()
    sys.exit(app.exec())
