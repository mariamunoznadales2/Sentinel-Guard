from nicegui import ui, app
from sentinelguard.ui.layout import crear_layout
from sentinelguard.ui.modos import MODOS_POR_PERFIL
from sentinelguard.ui.perfil import (
    obtener_perfil_actual,
    PERFIL_HOGAR,
    PERFIL_EMPRESA,
    PERFIL_MIXTO,
)
from sentinelguard.persistencia.historial_bd import registrar_evento
from sentinelguard.ui.armado import asegurar_timer_armado


def llamar_emergencias_sos():
    if app.storage.user.get('sos_enviado'):
        return

    app.storage.user['sos_enviado'] = True
    perfil = obtener_perfil_actual()

    registrar_evento(
        perfil=perfil,
        tipo_evento='SOS',
        sensor=None,
        modo='N/A',
        descripcion='Botón SOS pulsado: llamada a emergencias'
    )

    ui.notify('🚨 Llamada a emergencias realizada', color='negative')

    ui.timer(
        5,
        lambda: app.storage.user.pop('sos_enviado', None),
        once=True
    )


def crear_pantalla_inicio():

    # Aseguramos motor de armado global (independiente de UI)
    asegurar_timer_armado()

    perfil = obtener_perfil_actual()

    if perfil == PERFIL_HOGAR:
        saludo = 'Hola, Carlos'
    elif perfil == PERFIL_EMPRESA:
        saludo = 'Hola, Grupo Atlas S.A.'
    elif perfil == PERFIL_MIXTO:
        saludo = 'Hola, Laura'
    else:
        saludo = 'Hola'

    with crear_layout():

        ui.label(saludo).classes('text-xl md:text-2xl font-semibold mb-2')

        @ui.refreshable
        def render_inicio():

            # Notificación final (una vez)
            msg = app.storage.user.pop('armado_msg_pendiente', None)
            if msg:
                ui.notify(msg, color='positive')

            modo_activo = app.storage.user.get('modo_activo')
            armando = app.storage.user.get('armando')
            segundos = app.storage.user.get('segundos_armado')

            # Validación por perfil
            modos_validos = [m['nombre'] for m in MODOS_POR_PERFIL.get(perfil, [])]
            if modo_activo and modo_activo not in modos_validos:
                app.storage.user.pop('modo_activo', None)
                modo_activo = None

            if armando:
                estado = f'Armando sistema ({segundos}s)'
            elif modo_activo:
                estado = 'Tu sistema está actualmente protegido'
            else:
                estado = 'Tu sistema está desarmado'

            ui.label(estado).classes('text-sm text-gray-600 mb-6')

            with ui.grid().classes('grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 w-full'):

                with ui.card().style('background-color:#E5E7EB;border:none;box-shadow:none;').classes('p-6'):
                    ui.label('Estado del sistema').classes('text-sm text-gray-500 mb-3')

                    if app.storage.user.get('alarma_activa'):
                        ui.label('ALARMA ACTIVADA').classes('text-xl font-bold').style('color:#B3261E')
                    elif armando:
                        ui.label('ARMANDO SISTEMA').classes('text-xl font-bold').style('color:#F59E0B')
                        ui.label(f'Activación en {segundos}s').classes('text-sm').style('color:#F59E0B')
                    elif modo_activo:
                        ui.label('SISTEMA ARMADO').classes('text-xl font-bold').style('color:#2F7D32')
                        ui.label(f'Modo activo: {modo_activo}').classes('text-sm').style('color:#2F7D32')
                    else:
                        ui.label('SISTEMA DESARMADO').classes('text-xl font-bold').style('color:#B3261E')

                with ui.card().style('background-color:#E5E7EB;border:none;box-shadow:none;').classes('p-6'):
                    ui.label('Acciones rápidas').classes('text-sm font-semibold mb-4')

                    if not modo_activo and not armando:
                        ui.button(
                            'ARMAR (MODO TOTAL)',
                            on_click=lambda: armar_modo_total(perfil, render_inicio)
                        ).classes('btn-armar w-full mb-3')
                    else:
                        ui.button(
                            'ARMANDO...' if armando else 'SISTEMA ARMADO',
                            on_click=lambda: None
                        ).props('disable').classes('w-full mb-3')

                    ui.button(
                        'DESARMAR',
                        on_click=lambda: desarmar_sistema(render_inicio)
                    ).classes('btn-primary w-full')

                with ui.card().style('background-color:#E5E7EB;border:2px solid #B3261E;box-shadow:none;').classes('p-6'):
                    ui.label('Emergencia').classes('text-sm font-semibold mb-4').style('color:#B3261E')
                    ui.button('SOS', on_click=llamar_emergencias_sos).classes('btn-danger w-full text-lg')

        # Refresco suave estable (no rompe slots porque NO está dentro del refreshable)
        ui.timer(0.5, render_inicio.refresh)

        render_inicio()


def armar_modo_total(perfil, render_inicio):

    if app.storage.user.get('armando'):
        return

    if app.storage.user.get('alarma_activa'):
        ui.notify('No se puede armar el sistema mientras la alarma esté activa', color='negative')
        return

    if app.storage.user.get('modo_activo'):
        ui.notify('El sistema ya está armado', color='warning')
        return

    modo_total = next(
        (m['nombre'] for m in MODOS_POR_PERFIL.get(perfil, []) if 'Total' in m['nombre']),
        None
    )

    if not modo_total:
        ui.notify('Este perfil no dispone de Modo Total', color='warning')
        return

    app.storage.user['modo_total_pendiente'] = modo_total
    app.storage.user['armando'] = True
    app.storage.user['segundos_armado'] = 3

    render_inicio.refresh()


def desarmar_sistema(render_inicio):

    modo_anterior = app.storage.user.get('modo_activo')

    if not modo_anterior and not app.storage.user.get('armando'):
        ui.notify('El sistema ya está desarmado', color='warning')
        return

    app.storage.user.pop('modo_activo', None)
    app.storage.user.pop('alarma_activa', None)
    app.storage.user.pop('armando', None)
    app.storage.user.pop('segundos_armado', None)
    app.storage.user.pop('modo_total_pendiente', None)
    app.storage.user.pop('armado_msg_pendiente', None)

    if modo_anterior:
        registrar_evento(
            perfil=obtener_perfil_actual(),
            tipo_evento='Desarmado',
            descripcion='Sistema desarmado por el usuario',
            modo=modo_anterior
        )
        ui.notify('Sistema desarmado', color='positive')
    else:
        ui.notify('Armado cancelado', color='warning')

    render_inicio.refresh()
