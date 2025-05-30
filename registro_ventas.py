from conexion import obtener_conexion   
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QSplitter, QMessageBox, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt


class VentanaRegistroVentas(QWidget):
    def __init__(self, conexion):
        super().__init__()
        self.setWindowTitle("Registro de Ventas")
        self.setGeometry(150, 150, 900, 600)
        self.conexion = conexion

        layout = QVBoxLayout(self)

        # Botón de actualizar
        self.boton_actualizar = QPushButton("Actualizar")
        self.boton_actualizar.clicked.connect(self.cargar_ventas)

        # Tabla de ventas
        self.tabla_ventas = QTableWidget()
        self.tabla_ventas.setColumnCount(6)
        self.tabla_ventas.setHorizontalHeaderLabels([
            "ID Venta", "Fecha", "Importe", "Forma de Pago", "Teléfono", "ID Empleado"
        ])
        self.tabla_ventas.horizontalHeader().setStretchLastSection(True)
        self.tabla_ventas.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_ventas.itemSelectionChanged.connect(self.mostrar_detalles_venta)

        # Tabla de detalles
        self.tabla_detalles = QTableWidget()
        self.tabla_detalles.setColumnCount(4)
        self.tabla_detalles.setHorizontalHeaderLabels([
            "Código", "Nombre", "Cantidad", "Precio"
        ])
        self.tabla_detalles.horizontalHeader().setStretchLastSection(True)

        self.label_info = QLabel("Seleccione una venta para ver los detalles.")

        # Distribución
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self.tabla_ventas)
        splitter.addWidget(self.tabla_detalles)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        # Layout de botones
        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.boton_actualizar)
        layout_botones.addStretch()

        layout.addLayout(layout_botones)
        layout.addWidget(splitter)
        layout.addWidget(self.label_info)

        self.setLayout(layout)

        # Cargar ventas al iniciar
        self.cargar_ventas()

    def cargar_ventas(self):
        try:
            conexion = obtener_conexion()
            cursor= conexion.cursor()
            cursor.execute("SELECT id_venta, fecha, importe, forma_pago, telefono, id_empleado FROM venta ORDER BY fecha DESC")
            ventas = cursor.fetchall()

            self.tabla_ventas.setRowCount(0)
            for fila_idx, fila_datos in enumerate(ventas):
                self.tabla_ventas.insertRow(fila_idx)
                for col_idx, dato in enumerate(fila_datos):
                    item = QTableWidgetItem(str(dato))
                    item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                    self.tabla_ventas.setItem(fila_idx, col_idx, item)
            cursor.close()
            conexion.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las ventas:\n{e}")

    def mostrar_detalles_venta(self):
        seleccion = self.tabla_ventas.selectedItems()
        if not seleccion:
            return

        id_venta = seleccion[0].text()

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT d.codigo, a.nombre, d.cantidad, d.precio
                FROM detalles_venta d
                JOIN articulo a ON d.codigo = a.codigo
                WHERE d.id_venta = %s
            """, (id_venta,))
            detalles = cursor.fetchall()

            self.tabla_detalles.setRowCount(0)
            for fila_idx, fila_datos in enumerate(detalles):
                self.tabla_detalles.insertRow(fila_idx)
                for col_idx, dato in enumerate(fila_datos):
                    item = QTableWidgetItem(str(dato))
                    item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                    self.tabla_detalles.setItem(fila_idx, col_idx, item)

            self.label_info.setText(f"Detalles de la venta #{id_venta}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los detalles:\n{e}")
