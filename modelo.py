import sqlite3
import re

class UsuarioModel:
    def __init__(self, db_name="usuarios.db"):
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            self.crear_tabla()
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            raise

    def crear_tabla(self):
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}")
            raise

    def agregar_usuario(self, nombre, email):
        try:
            self.cursor.execute("INSERT INTO usuarios (nombre, email) VALUES (?, ?)", (nombre, email))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except sqlite3.Error as e:
            print(f"Error al agregar usuario: {e}")
            return False

    def buscar_usuarios(self, patron):
        try:
            self.cursor.execute("SELECT * FROM usuarios")
            usuarios = self.cursor.fetchall()
            return [usuario for usuario in usuarios if re.search(patron, usuario[1]) or re.search(patron, usuario[2])]
        except sqlite3.Error as e:
            print(f"Error al buscar usuarios: {e}")
            return []

    def obtener_todos_los_usuarios(self):
        try:
            self.cursor.execute("SELECT * FROM usuarios")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener usuarios: {e}")
            return []

    def cerrar_conexion(self):
        try:
            self.conn.close()
        except sqlite3.Error as e:
            print(f"Error al cerrar la conexión: {e}")
