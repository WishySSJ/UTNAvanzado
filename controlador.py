import re

class UsuarioController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.establecer_eventos(self.agregar_usuario, self.buscar_usuarios)

        try:
            self.mostrar_usuarios()
        except Exception as e:
            print(f"Error al cargar usuarios: {e}")

    def agregar_usuario(self):
        nombre, email = self.view.obtener_datos_usuario()

        # Validar entradas
        if not re.match(r"^[A-Za-z\s]+$", nombre):
            self.view.mostrar_mensaje_error("El nombre solo debe contener letras y espacios.")
            return
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            self.view.mostrar_mensaje_error("El correo electrónico no es válido.")
            return

        # Intentar agregar usuario al modelo
        if self.model.agregar_usuario(nombre, email):
            self.view.mostrar_mensaje_info("Usuario agregado exitosamente.")
            self.view.limpiar_campos()
            self.mostrar_usuarios()
        else:
            self.view.mostrar_mensaje_error("El correo electrónico ya está registrado.")

    def buscar_usuarios(self):
        patron = self.view.obtener_patron_busqueda()
        usuarios = self.model.buscar_usuarios(patron)
        self.view.lista_usuarios.delete(*self.view.lista_usuarios.get_children())
        self.view.mostrar_usuarios(usuarios)

    def mostrar_usuarios(self):
        try:
            usuarios = self.model.obtener_todos_los_usuarios()
            if usuarios:
                self.view.lista_usuarios.delete(*self.view.lista_usuarios.get_children())
                self.view.mostrar_usuarios(usuarios)
            else:
                print("No se encontraron usuarios en la base de datos.")
        except Exception as e:
            print(f"Error al mostrar usuarios: {e}")

    def cerrar_conexion(self):
        self.model.cerrar_conexion()