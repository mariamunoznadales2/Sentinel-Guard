import asyncio
from nicegui import app, background_tasks


_TASK_ARMADO = None


def asegurar_timer_armado():
    """Arranca (una sola vez) el motor de armado en segundo plano, independiente de la UI."""
    global _TASK_ARMADO
    if _TASK_ARMADO is not None:
        return

    async def loop_armado():
        while True:
            await asyncio.sleep(1)

            if not app.storage.user.get('armando'):
                continue

            segundos = int(app.storage.user.get('segundos_armado') or 0)

            if segundos > 1:
                app.storage.user['segundos_armado'] = segundos - 1
                continue

            # Finaliza armado
            modo = app.storage.user.get('modo_total_pendiente')
            if not modo:
                # Si falta el modo pendiente, cancelamos armado por seguridad
                app.storage.user.pop('armando', None)
                app.storage.user.pop('segundos_armado', None)
                continue

            app.storage.user.pop('armando', None)
            app.storage.user.pop('segundos_armado', None)
            app.storage.user.pop('modo_total_pendiente', None)
            app.storage.user['modo_activo'] = modo

            # Flag para que la UI muestre notificación una sola vez
            app.storage.user['armado_msg_pendiente'] = f'Sistema armado en {modo}'

    _TASK_ARMADO = background_tasks.create(loop_armado())
