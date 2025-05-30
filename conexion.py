import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        print("Intentando conectar a la base de datos...")  # Debug
        conexion = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="@Pataloca0",  # ¡Asegúrate de que sea correcta!
            database="dunodb",
            auth_plugin= 'mysql_native_password'
        )
        print("¡Conexión exitosa!")  # Debug
        return conexion
    except Error as e:
        print("Error al conectar:", e)  # Debug
        return None
