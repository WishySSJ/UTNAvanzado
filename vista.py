import tkinter as tk
from tkinter import ttk, messagebox
from modelo import UsuarioModel
from controlador import UsuarioController
import re
from functools import wraps



class LogObserver:
    def update(self, mensaje):
        raise NotImplementedError

class ConsoleLogger(LogObserver):
    def update(self, mensaje):
        print(f"[ConsoleLogger] {mensaje}")

class FileLogger(LogObserver):
    def __init__(self, archivo):
        self.archivo = archivo

    def update(self, mensaje):
        with open(self.archivo, "a") as f:
            f.write(f"{mensaje}\n")

class LogSubject:
    def __init__(self):
        self._observadores = []

    def agregar_observador(self, observador: LogObserver):
        self._observadores.append(observador)

    def notificar(self, mensaje):
        for obs in self._observadores:
            obs.update(mensaje)

# Instancia global del sujeto
log_subject = LogSubject()
log_subject.agregar_observador(ConsoleLogger())
log_subject.agregar_observador(FileLogger("app.log"))

# Decorador con logging usando el patrón observador
def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        mensaje_inicio = f"Llamada a: {func.__name__} | args: {args[1:]}, kwargs: {kwargs}"
        log_subject.notificar(mensaje_inicio)
        try:
            result = func(*args, **kwargs)
            log_subject.notificar(f"Resultado de {func.__name__}: {result}")
            return result
        except Exception as e:
            log_subject.notificar(f"Error en {func.__name__}: {e}")
            raise
    return wrapper




class UsuarioView:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Usuarios")
        
        # Frame para agregar usuarios
        self.frame_agregar = ttk.LabelFrame(self.root, text="Agregar Usuario")
        self.frame_agregar.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(self.frame_agregar, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(self.frame_agregar)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame_agregar, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_email = ttk.Entry(self.frame_agregar)
        self.entry_email.grid(row=1, column=1, padx=5, pady=5)

        self.btn_agregar = ttk.Button(self.frame_agregar, text="Agregar")
        self.btn_agregar.grid(row=2, column=0, columnspan=2, pady=10)

        # Frame para buscar usuarios
        self.frame_buscar = ttk.LabelFrame(self.root, text="Buscar Usuarios")
        self.frame_buscar.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(self.frame_buscar, text="Buscar (regex):").grid(row=0, column=0, padx=5, pady=5)
        self.entry_buscar = ttk.Entry(self.frame_buscar)
        self.entry_buscar.grid(row=0, column=1, padx=5, pady=5)

        self.btn_buscar = ttk.Button(self.frame_buscar, text="Buscar")
        self.btn_buscar.grid(row=1, column=0, columnspan=2, pady=10)

        # Lista de usuarios
        self.frame_lista = ttk.LabelFrame(self.root, text="Lista de Usuarios")
        self.frame_lista.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.columnas = ("ID", "Nombre", "Email")
        self.lista_usuarios = ttk.Treeview(self.frame_lista, columns=self.columnas, show="headings")
        for col in self.columnas:
            self.lista_usuarios.heading(col, text=col)
            self.lista_usuarios.column(col, width=150)

        self.lista_usuarios.grid(row=0, column=0, padx=5, pady=5)

    @log_action
    def mostrar_usuarios(self, usuarios):
        for usuario in usuarios:
            self.lista_usuarios.insert("", tk.END, values=usuario)

    @log_action
    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)

    @log_action
    def mostrar_mensaje_error(self, mensaje):
        messagebox.showerror("Error", mensaje)

    @log_action
    def mostrar_mensaje_info(self, mensaje):
        messagebox.showinfo("Éxito", mensaje)

    @log_action
    def obtener_datos_usuario(self):
        return self.entry_nombre.get(), self.entry_email.get()

    @log_action
    def obtener_patron_busqueda(self):
        return self.entry_buscar.get()

    @log_action
    def establecer_eventos(self, agregar_usuario, buscar_usuarios):
        self.btn_agregar.config(command=agregar_usuario)
        self.btn_buscar.config(command=buscar_usuarios)


# === INICIO DE LA APLICACIÓN ===

if __name__ == "__main__":
    log_subject.notificar("Aplicación iniciada.")

    root = tk.Tk()
    model = UsuarioModel()
    view = UsuarioView(root)
    controller = UsuarioController(model, view)

    try:
        root.mainloop()
    except Exception as e:
        log_subject.notificar(f"Error en el loop principal de Tkinter: {e}")
    finally:
        controller.cerrar_conexion()
        log_subject.notificar("Conexión con la base de datos cerrada.")
        log_subject.notificar("Aplicación finalizada.")
