from enum import Enum, auto
from typing import Dict, Optional, List
import threading
import time
from datetime import datetime

from .sensor import Sensor
from .modo import ModoSeguridad


class EstadoAlarma(Enum):
    DESARMADO = auto()
    RETARDO_SALIDA = auto()
    ARMADO = auto()
    RETARDO_ENTRADA = auto()
    ALARMA_DISPARADA = auto()


class Alarma:
    def __init__(self, gestor_bd=None):
        self.gestor_bd = gestor_bd

        self.estado = EstadoAlarma.DESARMADO
        self.modo_activo: Optional[ModoSeguridad] = None
        self.sensores: Dict[int, Sensor] = {}
        self.tiempo_restante = 0

    def registrar_sensor(self, sensor: Sensor) -> None:
        self.sensores[sensor.id] = sensor

    def listar_sensores(self) -> List[Sensor]:
        return list(self.sensores.values())

    def armar(self, modo: ModoSeguridad) -> None:
        self.modo_activo = modo

        if modo.retardo_salida > 0:
            self.estado = EstadoAlarma.RETARDO_SALIDA
            self.tiempo_restante = modo.retardo_salida
            threading.Thread(target=self._temporizador_salida, daemon=True).start()
        else:
            self.estado = EstadoAlarma.ARMADO

        if self.gestor_bd:
            self.gestor_bd.registrar_evento(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ARMAR",
                f"Modo: {modo.nombre}"
            )

    def _temporizador_salida(self):
        while self.tiempo_restante > 0 and self.estado == EstadoAlarma.RETARDO_SALIDA:
            time.sleep(1)
            self.tiempo_restante -= 1

        if self.estado == EstadoAlarma.RETARDO_SALIDA:
            self.estado = EstadoAlarma.ARMADO

    def desarmar(self) -> None:
        self.estado = EstadoAlarma.DESARMADO
        self.modo_activo = None
        self.tiempo_restante = 0

        if self.gestor_bd:
            self.gestor_bd.registrar_evento(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "DESARMAR",
                ""
            )

    def procesar_disparo_sensor(self, id_sensor: int) -> None:
        sensor = self.sensores.get(id_sensor)
        if not sensor:
            return

        if self.estado == EstadoAlarma.ARMADO:
            if self.modo_activo.retardo_entrada > 0:
                self.estado = EstadoAlarma.RETARDO_ENTRADA
                self.tiempo_restante = self.modo_activo.retardo_entrada
                threading.Thread(target=self._temporizador_entrada, daemon=True).start()

                if self.gestor_bd:
                    self.gestor_bd.registrar_evento(
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "RETARDO_ENTRADA",
                        f"Disparo sensor {sensor.nombre}"
                    )
            else:
                self._activar_alarma(sensor)

    def _temporizador_entrada(self):
        while self.tiempo_restante > 0 and self.estado == EstadoAlarma.RETARDO_ENTRADA:
            time.sleep(1)
            self.tiempo_restante -= 1

        if self.estado == EstadoAlarma.RETARDO_ENTRADA:
            self._activar_alarma()

    def _activar_alarma(self, sensor: Optional[Sensor] = None):
        self.estado = EstadoAlarma.ALARMA_DISPARADA
        desc = f"Sensor: {sensor.nombre}" if sensor else "Disparo finalizado"

        if self.gestor_bd:
            self.gestor_bd.registrar_evento(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ALARMA_DISPARADA",
                desc
            )
