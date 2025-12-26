import sqlite3
from datetime import datetime

RUTA_BD = 'sentinelguard.db'


def inicializar_bd_historial():
    with sqlite3.connect(RUTA_BD) as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                perfil TEXT NOT NULL,
                fecha_hora TEXT NOT NULL,
                tipo_evento TEXT NOT NULL,
                sensor TEXT,
                modo TEXT,
                descripcion TEXT
            )
            '''
        )
        conn.commit()


def registrar_evento(
    perfil: str,
    tipo_evento: str,
    descripcion: str,
    modo: str | None = None,
    sensor: str | None = None,
):
    fecha_hora = datetime.now().isoformat(timespec='seconds')

    with sqlite3.connect(RUTA_BD) as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO eventos (perfil, fecha_hora, tipo_evento, sensor, modo, descripcion)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (perfil, fecha_hora, tipo_evento, sensor, modo, descripcion)
        )
        conn.commit()


def obtener_eventos_por_perfil(perfil: str):
    with sqlite3.connect(RUTA_BD) as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT fecha_hora, tipo_evento, sensor, modo, descripcion
            FROM eventos
            WHERE perfil = ?
            ORDER BY fecha_hora DESC
            ''',
            (perfil,)
        )
        return cursor.fetchall()
