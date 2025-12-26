from nicegui import ui, app
from sentinelguard.ui.layout import crear_layout
from sentinelguard.ui.perfil import (
    obtener_perfil_actual,
    PERFIL_HOGAR,
    PERFIL_EMPRESA,
    PERFIL_MIXTO,
)
from sentinelguard.persistencia.historial_bd import registrar_evento


SENSORES_POR_PERFIL = {

    PERFIL_HOGAR: [
        {'nombre': 'Movimiento Salón', 'tipo': 'Movimiento'},
        {'nombre': 'Puerta Principal', 'tipo': 'Apertura'},
        {'nombre': 'Ventana Dormitorio', 'tipo': 'Apertura'},
        {'nombre': 'Humo Cocina', 'tipo': 'Humo'},
    ],

    PERFIL_EMPRESA: [
        {'nombre': 'Acceso Principal', 'tipo': 'Apertura'},
        {'nombre': 'Movimiento Oficina', 'tipo': 'Movimiento'},
        {'nombre': 'Movimiento Almacén', 'tipo': 'Movimiento'},
        {'nombre': 'Humo Zona Técnica', 'tipo': 'Humo'},
    ],

    PERFIL_MIXTO: [
        {'nombre': 'Acceso Vivienda', 'tipo': 'Apertura'},
        {'nombre': 'Movimiento Zona Mixta', 'tipo': 'Movimiento'},
    ],
}


def crear_pantalla_sensores():

    perfil = obtener_perfil_actual()
    sensores = SENSORES_POR_PERFIL.get(perfil, [])

    with crear_layout():

        ui.label('Sensores').classes(
            'text-2xl font-semibold mb-2'
        )

        # ✅ MENSAJE GLOBAL (una sola vez, arriba)
        if not app.storage.user.get('modo_activo'):
            ui.label(
                'Arma el sistema para simular eventos'
            ).classes(
                'text-sm text-gray-600 mb-6'
            )

        if not sensores:
            ui.label(
                'No hay sensores definidos para este perfil.'
            ).classes(
                'text-sm text-gray-600'
            )
            return

        with ui.grid().classes(
            'grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 w-full'
        ):
            for sensor in sensores:
                crear_tarjeta_sensor(sensor)


def crear_tarjeta_sensor(sensor):

    modo_activo = app.storage.user.get('modo_activo')

    with ui.card().classes(
        'w-full p-6 rounded-xl'
    ).style(
        'background-color:#E5E7EB;border:none;box-shadow:none;'
    ):

        ui.label(sensor['nombre']).classes(
            'text-lg font-bold mb-1'
        )

        ui.label(sensor['tipo']).classes(
            'text-sm text-gray-600 mb-4'
        )

        if modo_activo:
            ui.button(
                'SIMULAR EVENTO',
                on_click=lambda s=sensor: disparar_sensor(s)
            ).classes('btn-danger w-full')
        else:
            ui.button(
                'SISTEMA DESARMADO',
                on_click=lambda: None
            ).props('disable').classes(
                'w-full'
            )


def disparar_sensor(sensor):

    modo_activo = app.storage.user.get('modo_activo')
    perfil = obtener_perfil_actual()

    # 🔒 Seguridad extra (por si se llama desde otro sitio)
    if not modo_activo:
        return

    # Simulación realista del evento
    app.storage.user['alarma_activa'] = True

    descripcion = (
        f'{sensor["tipo"]} '
        f'detectado por el sensor {sensor["nombre"]}, con el {modo_activo} activado.'
    )

    ui.notify(
        f'🚨 Evento detectado: {sensor["nombre"]}',
        color='negative'
    )

    registrar_evento(
        perfil=perfil,
        tipo_evento='Actividad detectada',
        descripcion=descripcion,
        sensor=sensor['nombre'],
        modo=modo_activo
    )
