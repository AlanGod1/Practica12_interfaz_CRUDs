import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.Connect(
        host= "localhost",
        port= "3306",
        user= "root",
        password= "@Pataloca0",
        database= "dunodb",
        )
        return conexion
        
    except Error as e:
        print("Error:", e)
        return None

