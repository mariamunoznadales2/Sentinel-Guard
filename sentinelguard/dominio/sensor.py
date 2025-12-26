from enum import Enum, auto


class TipoSensor(Enum):
    MOVIMIENTO = auto()
    PUERTA = auto()
    HUMO = auto()
    ROTURA_CRISTAL = auto()


class EstadoSensor(Enum):
    NORMAL = auto()
    DISPARADO = auto()
    DESCONECTADO = auto()


class Sensor:
    def __init__(self, identificador: int, nombre: str, tipo: TipoSensor, zona: str):
        self.id = identificador
        self.nombre = nombre
        self.tipo = tipo
        self.zona = zona
        self.estado = EstadoSensor.NORMAL

    def disparar(self) -> None:
        """Marca el sensor como disparado (simula una intrusión o evento)."""
        self.estado = EstadoSensor.DISPARADO

    def resetear(self) -> None:
        """Vuelve el sensor a estado normal."""
        self.estado = EstadoSensor.NORMAL

    def desconectar(self) -> None:
        """Simula que el sensor está desconectado o con fallo."""
        self.estado = EstadoSensor.DESCONECTADO
