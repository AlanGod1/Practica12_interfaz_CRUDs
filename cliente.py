import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)

class VentanaClientes(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Catálogo de Clientes")
        self.setGeometry(100, 100, 800, 400)

        self.clientes = []  # Lista para simular base de datos

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

    def cargar_datos(self):
        self.tabla.setRowCount(0)
        for fila_idx, (telefono, nombre, direccion, rfc) in enumerate(self.clientes):
            self.tabla.insertRow(fila_idx)
            self.tabla.setItem(fila_idx, 0, QTableWidgetItem(telefono))
            self.tabla.setItem(fila_idx, 1, QTableWidgetItem(nombre))
            self.tabla.setItem(fila_idx, 2, QTableWidgetItem(direccion))
            self.tabla.setItem(fila_idx, 3, QTableWidgetItem(rfc if rfc else ""))

    def agregar(self):
        telefono = self.telefono_input.text()
        nombre = self.nombre_input.text()
        direccion = self.direccion_input.text()
        rfc = self.rfc_input.text()

        if telefono and nombre and direccion:
            if any(cliente[0] == telefono for cliente in self.clientes):
                QMessageBox.warning(self, "Duplicado", "Ya existe un cliente con ese teléfono.")
                return
            self.clientes.append((telefono, nombre, direccion, rfc))
            self.cargar_datos()
            self.limpiar_campos()
        else:
            QMessageBox.warning(self, "Campos vacíos", "Por favor completa todos los campos obligatorios.")

    def actualizar(self):
        telefono = self.telefono_input.text()
        nombre = self.nombre_input.text()
        direccion = self.direccion_input.text()
        rfc = self.rfc_input.text()

        if telefono and nombre and direccion:
            for i, (tel, _, _, _) in enumerate(self.clientes):
                if tel == telefono:
                    self.clientes[i] = (telefono, nombre, direccion, rfc)
                    self.cargar_datos()
                    self.limpiar_campos()
                    return
            QMessageBox.warning(self, "No encontrado", "No se encontró un cliente con ese teléfono.")
        else:
            QMessageBox.warning(self, "Campos vacíos", "Por favor completa todos los campos obligatorios.")

    def eliminar(self):
        telefono = self.telefono_input.text()
        if telefono:
            for i, (tel, _, _, _) in enumerate(self.clientes):
                if tel == telefono:
                    del self.clientes[i]
                    self.cargar_datos()
                    self.limpiar_campos()
                    return
            QMessageBox.warning(self, "No encontrado", "No se encontró un cliente con ese teléfono.")
        else:
            QMessageBox.warning(self, "Teléfono requerido", "Por favor ingresa el teléfono del cliente a eliminar.")

    def limpiar_campos(self):
        self.telefono_input.clear()
        self.nombre_input.clear()
        self.direccion_input.clear()
        self.rfc_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaClientes()
    ventana.show()
    sys.exit(app.exec())
