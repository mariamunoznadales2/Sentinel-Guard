import sqlite3
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Iterator


class GestorBD:
    def __init__(self, ruta_bd: str = 'sentinelguard.db') -> None:
        self.ruta_bd = ruta_bd

    @contextmanager
    def _conectar(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.ruta_bd)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    # ───────────────── UTILIDADES ─────────────────

    def _tabla_existe(self, conn: sqlite3.Connection, nombre: str) -> bool:
        cur = conn.cursor()
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
            (nombre,),
        )
        return cur.fetchone() is not None

    def _columnas(self, conn: sqlite3.Connection, tabla: str) -> List[str]:
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({tabla});")
        return [row[1] for row in cur.fetchall()]

    # ───────────────── INICIALIZACIÓN ─────────────────

    def inicializar(self) -> None:
        with self._conectar() as conn:
            self._asegurar_tabla_usuarios(conn)
            self._asegurar_tabla_modos(conn)
            self._seed_usuarios(conn)
            self._seed_modos(conn)

    def _asegurar_tabla_usuarios(self, conn: sqlite3.Connection) -> None:
        if not self._tabla_existe(conn, 'usuarios'):
            conn.execute(
                """
                CREATE TABLE usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT UNIQUE,
                    contrasena TEXT,
                    nombre TEXT,
                    email TEXT,
                    telefono TEXT,
                    direccion TEXT,
                    perfil TEXT
                );
                """
            )

        cols = self._columnas(conn, 'usuarios')

        def add(col_def: str) -> None:
            conn.execute(f"ALTER TABLE usuarios ADD COLUMN {col_def};")

        if 'nombre' not in cols:
            add("nombre TEXT")
        if 'email' not in cols:
            add("email TEXT")
        if 'telefono' not in cols:
            add("telefono TEXT")
        if 'direccion' not in cols:
            add("direccion TEXT")
        if 'perfil' not in cols:
            add("perfil TEXT")

    def _asegurar_tabla_modos(self, conn: sqlite3.Connection) -> None:
        if not self._tabla_existe(conn, 'modos'):
            conn.execute(
                """
                CREATE TABLE modos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT,
                    descripcion TEXT,
                    perfil TEXT
                );
                """
            )

    # ───────────────── SEED ─────────────────

    def _seed_usuarios(self, conn: sqlite3.Connection) -> None:
        cur = conn.cursor()
        usuarios = [
            (
                'carlos',
                '1234',
                'Carlos Fernández López',
                'carlos@sentinelguard.com',
                '600123123',
                'Calle Mayor 12, Córdoba',
                'Hogar',
            ),
            (
                'atlas',
                '1234',
                'Grupo Atlas S.A.',
                'contacto@atlas.com',
                '957000111',
                'Polígono Industrial Las Quemadas',
                'Empresa',
            ),
            (
                'laura',
                '1234',
                'Laura García',
                'laura@sentinelguard.com',
                '655987987',
                'Av. República Argentina 8',
                'Mixto',
            ),
        ]

        for u in usuarios:
            cur.execute(
                """
                INSERT OR IGNORE INTO usuarios
                (usuario, contrasena, nombre, email, telefono, direccion, perfil)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                u,
            )

    def _seed_modos(self, conn: sqlite3.Connection) -> None:
        cur = conn.cursor()
        modos = [
            ('Modo Casa', 'Protege el perímetro manteniendo libertad interior.', 'Hogar'),
            ('Modo Noche', 'Protección nocturna interior y exterior.', 'Hogar'),
            ('Modo Vacaciones', 'Protección total del inmueble.', 'Hogar'),
            ('Modo Mascotas', 'Evita falsas alarmas por mascotas.', 'Hogar'),
            ('Modo Silencioso', 'Registra eventos sin sirena.', 'Hogar'),
            ('Modo Total Empresa', 'Todos los sensores activos.', 'Empresa'),
            ('Modo Empleados', 'Movimiento interior controlado.', 'Empresa'),
            ('Modo Almacén', 'Protege zonas sensibles.', 'Empresa'),
            ('Modo Mixto Configurable', 'Configuración avanzada por zonas.', 'Mixto'),
            ('Modo Limpieza', 'Movimiento interior limitado.', 'Mixto'),
        ]

        for m in modos:
            cur.execute(
                """
                INSERT OR IGNORE INTO modos (nombre, descripcion, perfil)
                VALUES (?, ?, ?);
                """,
                m,
            )

    # ───────────────── CONSULTAS ─────────────────

    def verificar_credenciales(self, usuario: str, contrasena: str) -> bool:
        with self._conectar() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT 1
                FROM usuarios
                WHERE usuario = ? AND contrasena = ?
                LIMIT 1;
                """,
                (usuario, contrasena),
            )
            return cur.fetchone() is not None

    def obtener_perfil_usuario(self, usuario: str) -> Optional[str]:
        with self._conectar() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT perfil
                FROM usuarios
                WHERE usuario = ?
                LIMIT 1;
                """,
                (usuario,),
            )
            row = cur.fetchone()
            return row['perfil'] if row else None

    # ⭐ CLAVE: DATOS PERSONALES POR USUARIO
    def obtener_datos_usuario(self, usuario: str) -> Optional[Dict[str, Any]]:
        with self._conectar() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT nombre, email, telefono, direccion, perfil, usuario
                FROM usuarios
                WHERE usuario = ?
                LIMIT 1;
                """,
                (usuario,),
            )
            row = cur.fetchone()
            return dict(row) if row else None

    # Compatibilidad (no se rompe nada viejo)
    def obtener_datos_perfil(self, perfil: str) -> Optional[Dict[str, Any]]:
        with self._conectar() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT nombre, email, telefono, direccion, perfil, usuario
                FROM usuarios
                WHERE LOWER(perfil) = LOWER(?)
                ORDER BY id ASC
                LIMIT 1;
                """,
                (perfil,),
            )
            row = cur.fetchone()
            return dict(row) if row else None

    def obtener_modos(self, perfil: str) -> List[Dict[str, Any]]:
        with self._conectar() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT nombre, descripcion
                FROM modos
                WHERE LOWER(perfil) = LOWER(?)
                ORDER BY nombre;
                """,
                (perfil,),
            )
            return [dict(r) for r in cur.fetchall()] 