from nicegui import ui
from contextlib import contextmanager
from sentinelguard.ui.perfil import (
    obtener_perfil_actual,
    PERFIL_HOGAR,
    PERFIL_EMPRESA,
    PERFIL_MIXTO,
)


@contextmanager
def crear_layout():
    perfil = obtener_perfil_actual()

    # ================= NAVBAR =================
    with ui.row().classes(
        # En móvil: permite wrap (2 filas)
        # En desktop: forzamos una sola línea
        'w-full px-4 py-3 items-center justify-between '
        'flex-wrap md:flex-nowrap'
    ).style(
        'background-color:#E6E8EB'
    ):

        # ---------- LOGO ----------
        with ui.row().classes(
            'items-center gap-2'
        ):
            ui.image('/static/logo.png').classes(
                'h-5 w-5 md:h-6 md:w-6'
            )
            ui.label('SentinelGuard').classes(
                'text-base md:text-xl font-bold'
            )

        # ---------- MENÚ ----------
        with ui.row().classes(
            # En móvil más compacto
            'items-center gap-3 md:gap-6 mt-2 md:mt-0'
        ):

            ui.button(
                'Inicio',
                on_click=lambda: ui.navigate.to('/inicio')
            ).props('flat').classes(
                'text-sm md:text-base'
            ).style('color:#005C99')

            ui.button(
                'Modos',
                on_click=lambda: ui.navigate.to('/modos')
            ).props('flat').classes(
                'text-sm md:text-base'
            ).style('color:#005C99')

            if perfil in (PERFIL_HOGAR, PERFIL_EMPRESA, PERFIL_MIXTO):
                ui.button(
                    'Sensores',
                    on_click=lambda: ui.navigate.to('/sensores')
                ).props('flat').classes(
                    'text-sm md:text-base'
                ).style('color:#005C99')

            ui.button(
                'Historial',
                on_click=lambda: ui.navigate.to('/historial')
            ).props('flat').classes(
                'text-sm md:text-base'
            ).style('color:#005C99')

            ui.icon('account_circle').classes(
                'text-blue-600 cursor-pointer text-2xl md:text-3xl'
            ).on(
                'click',
                lambda: ui.navigate.to('/perfil')
            )

    # ================= CONTENIDO =================
    with ui.column().classes(
        'w-full min-h-screen px-4 py-6 md:p-6'
    ).style(
        'background-color:#D1D5DB'
    ):
        yield
