import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)

class VentanaCRUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Catálogo de Categorías")
        self.setGeometry(100, 100, 600, 400)

        self.datos = []  # Simulación en memoria de la "base de datos"

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
        for fila_idx, (id_categoria, nombre) in enumerate(self.datos):
            self.tabla.insertRow(fila_idx)
            self.tabla.setItem(fila_idx, 0, QTableWidgetItem(str(id_categoria)))
            self.tabla.setItem(fila_idx, 1, QTableWidgetItem(nombre))

    def agregar(self):
        idcat = self.id_input.text()
        nombre = self.nombre_input.text()
        if idcat and nombre:
            if any(str(d[0]) == idcat for d in self.datos):
                QMessageBox.warning(self, "ID duplicado", "Ya existe una categoría con ese ID.")
                return
            self.datos.append((idcat, nombre))
            self.cargar_datos()
            self.id_input.clear()
            self.nombre_input.clear()
        else:
            QMessageBox.warning(self, "Campos vacíos", "Por favor completa todos los campos.")

    def actualizar(self):
        idcat = self.id_input.text()
        nombre = self.nombre_input.text()
        if idcat and nombre:
            for idx, (id_existente, _) in enumerate(self.datos):
                if str(id_existente) == idcat:
                    self.datos[idx] = (idcat, nombre)
                    self.cargar_datos()
                    self.id_input.clear()
                    self.nombre_input.clear()
                    return
            QMessageBox.warning(self, "No encontrado", "No existe una categoría con ese ID.")
        else:
            QMessageBox.warning(self, "Campos vacíos", "Por favor completa todos los campos.")

    def eliminar(self):
        idcat = self.id_input.text()
        if idcat:
            for idx, (id_existente, _) in enumerate(self.datos):
                if str(id_existente) == idcat:
                    del self.datos[idx]
                    self.cargar_datos()
                    self.id_input.clear()
                    self.nombre_input.clear()
                    return
            QMessageBox.warning(self, "No encontrado", "No existe una categoría con ese ID.")
        else:
            QMessageBox.warning(self, "ID requerido", "Por favor ingresa el ID a eliminar.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaCRUD()
    ventana.show()
    sys.exit(app.exec())
