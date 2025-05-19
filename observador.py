import re


class LogObserver:
    def update(self, mensaje):
        raise NotImplementedError("Debe implementar el método update()")


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
        for observador in self._observadores:
            observador.update(mensaje)
