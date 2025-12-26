from nicegui import ui
from sentinelguard.ui.layout import crear_layout
from sentinelguard.ui.perfil import obtener_perfil_actual
from sentinelguard.persistencia.basedatos import GestorBD


def crear_pantalla_perfil_usuario():

    perfil = obtener_perfil_actual()   # ← CLAVE
    gestor = GestorBD()
    datos = gestor.obtener_datos_perfil(perfil)

    if not datos:
        ui.notify('Perfil no encontrado', color='negative')
        return

    with crear_layout():

        ui.label('Perfil de usuario').classes(
            'text-2xl font-semibold mb-6'
        )

        with ui.row().classes('w-full gap-8'):

            # ───── COLUMNA IZQUIERDA ─────
            with ui.card().classes('p-6 w-72').style(
                'background-color:#E5E7EB;border:none;box-shadow:none;'
            ):
                ui.icon('account_circle').classes(
                    'text-blue-600 text-7xl mb-4'
                )

                ui.label(datos['nombre']).classes(
                    'text-lg font-semibold'
                )

                ui.label(datos['email']).classes(
                    'text-sm text-gray-600'
                )

                ui.label(f"Perfil: {datos['perfil']}").classes(
                    'text-xs text-gray-500 mt-2'
                )

            # ───── COLUMNA DERECHA ─────
            with ui.card().classes('p-6 flex-1').style(
                'background-color:#E5E7EB;border:none;box-shadow:none;'
            ):
                ui.label('Información personal').classes(
                    'text-sm font-semibold mb-4'
                )

                def fila(label, valor):
                    with ui.row().classes('justify-between py-1'):
                        ui.label(label).classes('text-sm text-gray-600')
                        ui.label(valor).classes('text-sm font-medium')

                fila('Nombre completo', datos['nombre'])
                fila('Correo electrónico', datos['email'])
                fila('Teléfono', datos.get('telefono', '—'))
                fila('Dirección', datos.get('direccion', '—'))

                ui.separator().classes('my-4')

                ui.button(
                    'Cerrar sesión',
                    on_click=lambda: ui.navigate.to('/login')
                ).classes('btn-primary w-48')
