from nicegui import ui
from sentinelguard.ui.layout import crear_layout
from sentinelguard.ui.perfil import obtener_perfil_actual
from sentinelguard.persistencia.historial_bd import obtener_eventos_por_perfil


def crear_pantalla_historial():

    perfil = obtener_perfil_actual()

    with crear_layout():

        ui.label('Historial de eventos').classes(
            'text-2xl font-semibold mb-6'
        )

        eventos = obtener_eventos_por_perfil(perfil)

        if not eventos:
            ui.label(
                'No hay eventos registrados para este perfil.'
            ).classes(
                'text-sm text-gray-600'
            )
            return

        with ui.column().classes('w-full gap-4'):

            for fecha_hora, tipo, sensor, modo, descripcion in eventos:

                es_sos = (tipo == 'SOS')

                with ui.card().classes(
                    'w-full p-4 rounded-xl border-l-4'
                ).style(
                    (
                        'background-color:#E5E7EB;'
                        'border-color:#B3261E;'
                        'box-shadow:none;'
                    )
                    if es_sos else
                    (
                        'background-color:#E5E7EB;'
                        'border-color:#3154A6;'
                        'box-shadow:none;'
                    )
                ):

                    with ui.row().classes(
                        'justify-between items-start w-full'
                    ):

                        # ─── INFORMACIÓN PRINCIPAL ───
                        with ui.column().classes('gap-1'):

                            if es_sos:
                                ui.label('🚨 EMERGENCIA SOS').classes(
                                    'font-bold'
                                ).style(
                                    'color:#B3261E;'
                                )
                            else:
                                ui.label(tipo).classes(
                                    'font-semibold text-gray-700'
                                )

                            ui.label(descripcion).classes(
                                'text-sm'
                            ).style(
                                'color:#B3261E;' if es_sos else 'color:#374151;'
                            )

                            detalles = []

                            if modo:
                                detalles.append(f'Modo: {modo}')

                            if sensor:
                                detalles.append(f'Sensor: {sensor}')

                            if detalles:
                                ui.label(
                                    ' · '.join(detalles)
                                ).classes(
                                    'text-xs text-gray-500'
                                )

                        # ─── FECHA / HORA ───
                        ui.label(fecha_hora).classes(
                            'text-xs text-gray-500'
                        )
