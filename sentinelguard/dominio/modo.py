from typing import List


class ModoSeguridad:
    def __init__(
        self,
        nombre: str,
        descripcion: str,
        retardo_entrada: int,
        retardo_salida: int,
        sensibilidad: int = 5,
        predefinido: bool = True,
    ):
        self.nombre = nombre
        self.descripcion = descripcion
        self.retardo_entrada = retardo_entrada
        self.retardo_salida = retardo_salida
        self.sensibilidad = sensibilidad
        self.predefinido = predefinido

    def __repr__(self) -> str:
        return f"<ModoSeguridad {self.nombre} (sensibilidad={self.sensibilidad})>"
