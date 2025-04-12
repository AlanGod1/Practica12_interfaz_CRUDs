import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)

class VentanaCRUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Catálogo de Unidades")
        self.setGeometry(100, 100, 600, 400)

        self.unidades = []  # Lista para simular la base de datos

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

    def cargar_datos(self):
        self.tabla.setRowCount(0)
        for fila_idx, (id_unidad, nombre) in enumerate(self.unidades):
            self.tabla.insertRow(fila_idx)
            self.tabla.setItem(fila_idx, 0, QTableWidgetItem(str(id_unidad)))
            self.tabla.setItem(fila_idx, 1, QTableWidgetItem(nombre))

    def agregar(self):
        idunidad = self.id_input.text()
        nombre = self.nombre_input.text()
        if idunidad and nombre:
            if any(u[0] == idunidad for u in self.unidades):
                QMessageBox.warning(self, "Duplicado", "Ya existe una unidad con ese ID.")
                return
            self.unidades.append((idunidad, nombre))
            self.cargar_datos()
            self.limpiar()
        else:
            QMessageBox.warning(self, "Campos vacíos", "Por favor completa todos los campos.")

    def actualizar(self):
        idunidad = self.id_input.text()
        nombre = self.nombre_input.text()
        if idunidad and nombre:
            for i, (id_actual, _) in enumerate(self.unidades):
                if id_actual == idunidad:
                    self.unidades[i] = (idunidad, nombre)
                    self.cargar_datos()
                    self.limpiar()
                    return
            QMessageBox.warning(self, "No encontrado", "No se encontró una unidad con ese ID.")
        else:
            QMessageBox.warning(self, "Campos vacíos", "Por favor completa todos los campos.")

    def eliminar(self):
        idunidad = self.id_input.text()
        if idunidad:
            for i, (id_actual, _) in enumerate(self.unidades):
                if id_actual == idunidad:
                    del self.unidades[i]
                    self.cargar_datos()
                    self.limpiar()
                    return
            QMessageBox.warning(self, "No encontrado", "No se encontró una unidad con ese ID.")
        else:
            QMessageBox.warning(self, "ID requerido", "Por favor ingresa el ID a eliminar.")

    def limpiar(self):
        self.id_input.clear()
        self.nombre_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaCRUD()
    ventana.show()
    sys.exit(app.exec())
