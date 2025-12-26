from nicegui import ui, app
from sentinelguard.ui.layout import crear_layout
from sentinelguard.ui.perfil import (
    obtener_perfil_actual,
    PERFIL_HOGAR,
    PERFIL_EMPRESA,
    PERFIL_MIXTO,
)
from sentinelguard.persistencia.historial_bd import registrar_evento
from sentinelguard.ui.armado import asegurar_timer_armado


MODOS_POR_PERFIL = {

    PERFIL_HOGAR: [
        {'nombre': 'Modo Casa', 'descripcion': 'Protege el perímetro manteniendo libertad de movimiento en el interior.'},
        {'nombre': 'Modo Noche', 'descripcion': 'Activa sensores estratégicos durante la noche mientras descansas.'},
        {'nombre': 'Modo Total', 'descripcion': 'Activa todos los sensores del sistema sin excepciones.'},
        {'nombre': 'Modo Mascotas', 'descripcion': 'Evita falsas alarmas provocadas por mascotas dentro del hogar.'},
        {'nombre': 'Modo Silencioso', 'descripcion': 'Registra actividad sin activar la sirena audible.'},
    ],

    PERFIL_EMPRESA: [
        {'nombre': 'Modo Perímetro Nocturno', 'descripcion': 'Protege accesos exteriores fuera del horario laboral.'},
        {'nombre': 'Modo Total', 'descripcion': 'Todos los sensores de la instalación activos.'},
        {'nombre': 'Modo Empleados', 'descripcion': 'Permite circulación interior controlada durante la jornada laboral.'},
        {'nombre': 'Modo Almacén', 'descripcion': 'Protege zonas sensibles sin interferir en áreas públicas.'},
        {'nombre': 'Modo Silencioso Profesional', 'descripcion': 'Monitorización discreta sin activación de sirenas.'},
    ],

    PERFIL_MIXTO: [
        {'nombre': 'Modo Total', 'descripcion': 'Combina protección de hogar y empresa según el contexto.'},
        {'nombre': 'Modo Limpieza', 'descripcion': 'Permite movimiento interior limitado por personal autorizado.'},
    ],
}


def crear_pantalla_modos():

    # Motor global de armado 
    asegurar_timer_armado()

    perfil = obtener_perfil_actual()

    if perfil not in (PERFIL_HOGAR, PERFIL_EMPRESA, PERFIL_MIXTO):
        with crear_layout():
            ui.notify('Perfil de usuario no definido. No se pueden cargar los modos.', color='negative')
            ui.label('Perfil no definido').classes('text-xl font-bold text-red-600 mt-6')
        return

    modos = MODOS_POR_PERFIL[perfil]

    with crear_layout():

        ui.label('Modos de Alarma').classes('text-2xl font-semibold mb-6')



        @ui.refreshable
        def render_modos():

            # Notificación final del motor de armado
            msg = app.storage.user.pop('armado_msg_pendiente', None)
            if msg:
                ui.notify(msg, color='positive')

            armando = app.storage.user.get('armando')
            segundos = app.storage.user.get('segundos_armado')
            pendiente = app.storage.user.get('modo_total_pendiente')
            modo_activo = app.storage.user.get('modo_activo')

            with ui.grid().classes('grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 w-full'):
                for modo in modos:

                    activo = (modo['nombre'] == modo_activo)

                    with ui.card().classes('w-full p-6 rounded-xl transition-all duration-300').style(
                        (
                            'background-color:#E5E7EB;'
                            'border: 2px solid #2F7D32;'
                            'box-shadow:none;'
                        )
                        if activo else
                        (
                            'background-color:#E5E7EB;'
                            'border:none;'
                            'box-shadow:none;'
                        )
                    ):

                        with ui.row().classes('items-center justify-between mb-2'):
                            ui.label(modo['nombre']).classes('text-lg font-bold').style(
                                'color:#2F7D32;' if activo else ''
                            )

                            with ui.menu().props(
                                'anchor="top right" self="top left" '
                                'transition-show="scale" transition-hide="scale" '
                                'close-on-content-click="false"'
                            ) as menu:
                                with ui.card().classes('w-72 p-4 rounded-lg').style(
                                    'background-color:#E5E7EB; box-shadow:none;'
                                ):
                                    ui.label(modo['descripcion']).classes('text-sm text-gray-700')
                                    ui.button('Cerrar', on_click=menu.close).props('flat').classes('mt-2')

                            ui.icon('info').classes(
                                'text-blue-600 cursor-pointer hover:text-blue-800'
                            ).on('click', lambda e=None, m=menu: m.open(e))

                        if activo:
                            ui.label('Modo activo').classes('text-sm font-semibold mt-3').style('color:#2F7D32')

                        elif armando and pendiente == modo['nombre']:
                            ui.label(f'Armando sistema ({segundos}s)').classes(
                                'text-sm font-semibold mt-3'
                            ).style('color:#F59E0B')

                        else:
                            ui.button(
                                'ACTIVAR',
                                on_click=lambda m=modo['nombre']: activar_modo(m, render_modos)
                            ).classes('btn-primary w-full mt-3')

        def activar_modo(nombre_modo: str, render_modos):

            # Si ya hay un modo activo, NO se puede activar otro
            if app.storage.user.get('modo_activo'):
                ui.notify('Debes desarmar el sistema antes de activar otro modo', color='warning')
                return

            if app.storage.user.get('armando'):
                ui.notify('El sistema se está armando. Espera unos segundos.', color='warning')
                return

            if app.storage.user.get('alarma_activa'):
                ui.notify('No se puede cambiar de modo mientras la alarma esté activa', color='negative')
                return

            
            app.storage.user['modo_total_pendiente'] = nombre_modo
            app.storage.user['armando'] = True
            app.storage.user['segundos_armado'] = 3

            registrar_evento(
                perfil=obtener_perfil_actual(),
                tipo_evento='Armado',
                descripcion=f'Armado iniciado para el modo {nombre_modo}',
                modo=nombre_modo
            )

            render_modos.refresh()

    
        
        render_modos()
