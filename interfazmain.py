import sys
from conexion import obtener_conexion
from PyQt6.QtWidgets import QApplication, QTabWidget, QWidget, QVBoxLayout
from empleado import VentanaEmpleados  
from categoria import Ventanacatego
from cliente import VentanaClientes
from proveedor import VentanaProveedores
from unidad import VentanaUnidad
from articulo import VentanaArticulos
from venta import VentanaVenta
class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        
        try:
            self.conexion = obtener_conexion()
        except Exception as e:
            self.mostrar_error(f"No se pudo conectar a la base de datos:\n{str(e)}")
            sys.exit(1)

        self.tabs = QTabWidget()
        self.tabs.addTab(VentanaEmpleados(self.conexion), "Empleados")  # Instancia aquí
        self.tabs.addTab(Ventanacatego(self.conexion), "Categorias")
        self.tabs.addTab(VentanaClientes(self.conexion), "Clientes")
        self.tabs.addTab(VentanaProveedores(self.conexion), "Proveedores")
        self.tabs.addTab(VentanaUnidad(self.conexion), "Unidad")
        self.tabs.addTab(VentanaArticulos(self.conexion), "Articulos")
        self.tabs.addTab(VentanaVenta(self.conexion), "Venta")
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())