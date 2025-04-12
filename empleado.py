import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QComboBox
)

class VentanaEmpleados(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Catálogo de Empleados")
        self.setGeometry(100, 100, 700, 400)

        self.empleados = []  # Simulación de base de datos en memoria

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

    def cargar_datos(self):
        self.tabla.setRowCount(0)
        for fila_idx, (id_emp, nombre, genero, puesto) in enumerate(self.empleados):
            self.tabla.insertRow(fila_idx)
            self.tabla.setItem(fila_idx, 0, QTableWidgetItem(str(id_emp)))
            self.tabla.setItem(fila_idx, 1, QTableWidgetItem(nombre))
            self.tabla.setItem(fila_idx, 2, QTableWidgetItem(genero))
            self.tabla.setItem(fila_idx, 3, QTableWidgetItem(puesto))

    def agregar(self):
        id_emp = self.id_input.text()
        nombre = self.nombre_input.text()
        genero = self.genero_input.currentText()
        puesto = self.puesto_input.currentText()

        if id_emp and nombre:
            if any(emp[0] == id_emp for emp in self.empleados):
                QMessageBox.warning(self, "Duplicado", "Ya existe un empleado con ese ID.")
                return
            self.empleados.append((id_emp, nombre, genero, puesto))
            self.cargar_datos()
            self.limpiar_campos()
        else:
            QMessageBox.warning(self, "Campos vacíos", "Por favor completa todos los campos.")

    def actualizar(self):
        id_emp = self.id_input.text()
        nombre = self.nombre_input.text()
        genero = self.genero_input.currentText()
        puesto = self.puesto_input.currentText()

        if id_emp and nombre:
            for i, (id_existente, _, _, _) in enumerate(self.empleados):
                if id_existente == id_emp:
                    self.empleados[i] = (id_emp, nombre, genero, puesto)
                    self.cargar_datos()
                    self.limpiar_campos()
                    return
            QMessageBox.warning(self, "No encontrado", "No se encontró un empleado con ese ID.")
        else:
            QMessageBox.warning(self, "Campos vacíos", "Por favor completa todos los campos.")

    def eliminar(self):
        id_emp = self.id_input.text()
        if id_emp:
            for i, (id_existente, _, _, _) in enumerate(self.empleados):
                if id_existente == id_emp:
                    del self.empleados[i]
                    self.cargar_datos()
                    self.limpiar_campos()
                    return
            QMessageBox.warning(self, "No encontrado", "No se encontró un empleado con ese ID.")
        else:
            QMessageBox.warning(self, "ID requerido", "Por favor ingresa el ID del empleado.")

    def limpiar_campos(self):
        self.id_input.clear()
        self.nombre_input.clear()
        self.genero_input.setCurrentIndex(0)
        self.puesto_input.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaEmpleados()
    ventana.show()
    sys.exit(app.exec())
