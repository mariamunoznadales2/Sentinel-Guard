from nicegui import ui, app
from sentinelguard.ui.perfil import (
    PERFIL_HOGAR,
    PERFIL_EMPRESA,
    PERFIL_MIXTO,
)


# Credenciales simuladas (estado estable)
USUARIOS = {
    'hogar': {'password': 'hogar123', 'perfil': PERFIL_HOGAR},
    'empresa': {'password': 'empresa123', 'perfil': PERFIL_EMPRESA},
    'mixto': {'password': 'mixto123', 'perfil': PERFIL_MIXTO},
}


def crear_pantalla_login():

    with ui.column().classes(
        'min-h-screen w-full items-center justify-center'
    ).style('background-color: #D1D5DB'):

        with ui.card().classes(
            'w-full max-w-md p-8 sm:p-8 p-5'
        ).style(
            'background-color: #E6E8EB; '
            'border: 1px solid #E2E8F0; '
            'border-radius: 14px;'
        ):

            # -------- CABECERA --------
            with ui.row().classes('gap-2 sm:gap-4 items-center flex-nowrap overflow-x-auto no-scrollbar'):
                ui.image('/static/logo.png').classes('w-10 h-10')
                ui.label('SentinelGuard').classes('text-2xl font-bold')

            ui.label('Security Control Panel').classes(
                'text-sm text-center mt-0'
            ).style('color: #64748B')

            ui.label(
                'Accede para gestionar tu sistema'
            ).classes(
                'text-sm text-center mt-3 mb-4 hidden sm:block'
            ).style('color: #475569')

            # -------- FORMULARIO --------
            usuario = ui.input('Usuario').props('autofocus').classes('w-full mb-4')

            contrasena = ui.input(
                'Contraseña',
                password=True,
                password_toggle_button=True
            ).classes('w-full')

            error_label = ui.label('').classes(
                'text-sm mt-2'
            ).style('color: #B3261E')

            # -------- BOTÓN --------
            boton_entrar = ui.button(
                'ENTRAR'
            ).classes(
                'w-full text-lg mt-5 py-3 sm:py-4'
            ).style(
                'background-color: #3154A6; color: white;'
            )
            boton_entrar.disable()

            # -------- UX --------
            def actualizar_estado_boton():
                if contrasena.value and len(contrasena.value) >= 1:
                    boton_entrar.enable()
                else:
                    boton_entrar.disable()

            actualizar_estado_boton()

            usuario.on('update:model-value', actualizar_estado_boton)
            contrasena.on('update:model-value', actualizar_estado_boton)

            def entrar():
                error_label.text = ''
                boton_entrar.disable()
                boton_entrar.text = 'Comprobando credenciales…'

                u = (usuario.value or '').strip()
                p = (contrasena.value or '')

                info = USUARIOS.get(u)
                if info is None or info['password'] != p:
                    boton_entrar.text = 'ENTRAR'
                    boton_entrar.enable()
                    error_label.text = 'Usuario o contraseña incorrectos'
                    return

                app.storage.user.clear()
                app.storage.user['usuario'] = u
                app.storage.user['perfil'] = info['perfil']
                ui.navigate.to('/inicio')

            boton_entrar.on_click(entrar)

            # Enter para enviar
            contrasena.on('keydown.enter', entrar)

            # -------- OLVIDÉ CONTRASEÑA (UX REALISTA) --------
            ui.link(
                '¿Has olvidado la contraseña?',
                '#'
            ).classes(
                'text-sm text-center mt-4'
            ).style(
                'color: #3154A6'
            ).on(
                'click',
                lambda: ui.notify(
                    'Recuperación de contraseña no disponible en esta demo',
                    color='warning'
                )
            )

            # -------- CONFIANZA --------
            ui.label(
                'Conexión cifrada · Acceso restringido a usuarios autorizados'
            ).classes(
                'text-xs text-center mt-6'
            ).style('color: #94A3B8')
