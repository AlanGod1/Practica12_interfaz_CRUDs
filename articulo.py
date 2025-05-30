from conexion import obtener_conexion
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QComboBox, QMessageBox
)


class VentanaArticulos(QWidget):
    def __init__(self, conexion):
        super().__init__()
        self.conexion = conexion
        self.setWindowTitle("Catálogo de Productos")
        self.setGeometry(100, 100, 1000, 500)
        
        self.codigo_input = QLineEdit()
        self.codigo_input.setMaxLength(13)
        self.codigo_input.setPlaceholderText("Código de barras")

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre del producto")

        self.precio_input = QLineEdit()
        self.precio_input.setPlaceholderText("Precio de venta")

        self.costo_input = QLineEdit()
        self.costo_input.setPlaceholderText("Costo")

        self.existencias_input = QLineEdit()
        self.existencias_input.setPlaceholderText("Existencias")

        self.reorden_input = QLineEdit()
        self.reorden_input.setPlaceholderText("Nivel de reorden")

        self.categoria_combo = QComboBox()
        self.unidad_combo = QComboBox()
        self.proveedor_combo = QComboBox()

        self.boton_agregar = QPushButton("Agregar")
        self.boton_actualizar = QPushButton("Actualizar")

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(9)
        self.tabla.setHorizontalHeaderLabels([
            "Código", "Nombre", "Precio", "Costo", "Existencias",
            "Reorden", "Categoría", "Proveedor", "Unidad"
        ])

        self.boton_agregar.clicked.connect(self.agregar)
        self.boton_actualizar.clicked.connect(self.cargar_datos)

        form_layout = QHBoxLayout()
        for widget in [self.codigo_input, self.nombre_input, self.precio_input,
                       self.costo_input, self.existencias_input, self.reorden_input,
                       self.categoria_combo, self.proveedor_combo, self.unidad_combo, self.boton_agregar, self.boton_actualizar]:
            form_layout.addWidget(widget)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.tabla)
        self.setLayout(layout)

        self.categorias = {}
        self.proveedores = {}
        self.unidades = {}

        self.cargar_combos()
        self.cargar_datos()

    def cargar_combos(self):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()

            cursor.execute("SELECT id_categoria, nombre FROM categoria")
            for id_cat, nombre in cursor.fetchall():
                self.categoria_combo.addItem(nombre, id_cat)
                self.categorias[nombre] = id_cat

            cursor.execute("SELECT id_proveedor, nombre FROM proveedor")
            for id_prov, nombre in cursor.fetchall():
                self.proveedor_combo.addItem(nombre, id_prov)
                self.proveedores[nombre] = id_prov

            cursor.execute("SELECT id_unidad, nombre FROM unidad")
            for id_uni, nombre in cursor.fetchall():
                self.unidad_combo.addItem(nombre, id_uni)
                self.unidades[nombre] = id_uni

            cursor.close()
            conexion.close()

    def agregar(self):
        try:
            codigo = self.codigo_input.text()
            nombre = self.nombre_input.text()
            precio = float(self.precio_input.text())
            costo = float(self.costo_input.text())
            existencias = int(self.existencias_input.text())
            reorden = self.reorden_input.text()

            id_categoria = self.categoria_combo.currentData()
            id_proveedor = self.proveedor_combo.currentData()
            id_unidad = self.unidad_combo.currentData()

            if not (codigo and nombre and precio and costo and reorden):
                QMessageBox.warning(self, "Campos vacíos", "Llena todos los campos.")
                return

            conexion = obtener_conexion()
            cursor = conexion.cursor()
            query = """
                INSERT INTO articulo 
                (codigo, nombre, precio, costo, existencias, reorden, id_categoria, id_proveedor, id_unidad)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (codigo, nombre, precio, costo, existencias, reorden, id_categoria, id_proveedor, id_unidad)
            cursor.execute(query, valores)
            conexion.commit()
            cursor.close()
            conexion.close()

            self.cargar_datos()
            self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo agregar el producto:\n{e}")

    def cargar_datos(self):
        self.tabla.setRowCount(0)
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT a.codigo, a.nombre, a.precio, a.costo, a.existencias, a.reorden,
                       c.nombre, p.nombre, u.nombre
                FROM articulo a
                JOIN categoria c ON a.id_categoria = c.id_categoria
                JOIN proveedor p ON a.id_proveedor = p.id_proveedor
                JOIN unidad u ON a.id_unidad = u.id_unidad
            """)
            for row_idx, row in enumerate(cursor.fetchall()):
                self.tabla.insertRow(row_idx)
                for col_idx, dato in enumerate(row):
                    self.tabla.setItem(row_idx, col_idx, QTableWidgetItem(str(dato)))
            cursor.close()
            conexion.close()

    def limpiar_campos(self):
        for field in [self.codigo_input, self.nombre_input, self.precio_input,
                      self.costo_input, self.existencias_input, self.reorden_input]:
            field.clear()
        self.categoria_combo.setCurrentIndex(0)
        self.proveedor_combo.setCurrentIndex(0)
        self.unidad_combo.setCurrentIndex(0)
