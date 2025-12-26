
import os
from nicegui import ui,app
from sentinelguard.ui.perfil_usuario import crear_pantalla_perfil_usuario
from sentinelguard.persistencia.historial_bd import inicializar_bd_historial
from sentinelguard.ui.historial import crear_pantalla_historial
from sentinelguard.ui.login import crear_pantalla_login
from sentinelguard.ui.inicio import crear_pantalla_inicio
from sentinelguard.ui.modos import crear_pantalla_modos
from sentinelguard.ui.admin_modos import crear_pantalla_admin_modos
from sentinelguard.ui.sensores import crear_pantalla_sensores
from sentinelguard.ui.perfil import (
    obtener_perfil_actual,
    PERFIL_HOGAR,
    PERFIL_EMPRESA,
    PERFIL_MIXTO,
)
from sentinelguard.persistencia.basedatos import GestorBD

gestor_bd = GestorBD()
gestor_bd.inicializar()


# --------------------------------------------------
ui.add_head_html('''
<style>
    html, body {
        margin: 0;
        padding: 0;
        background-color: #D1D5DB;
    }

    .nicegui-content {
        padding: 0 !important;
        margin: 0 !important;
        background-color: #D1D5DB;
    }
</style>
''', shared=True)

print("CWD:", os.getcwd())


app.add_static_files('/static', 'static')

inicializar_bd_historial()

# --------------------------------------------------
# OBJETO ALARMA MINIMALISTA (STUB SEGURO)
# --------------------------------------------------
class AlarmaStub:
    def __init__(self, gestor_bd):
        self.gestor_bd = gestor_bd

    def listar_sensores(self):
        return []


def obtener_alarma_stub():
    from sentinelguard.persistencia.basedatos import GestorBD
    gestor = GestorBD()
    return AlarmaStub(gestor)




# --------------------------------------------------
# RUTAS
# --------------------------------------------------
@ui.page('/')
def root():
    ui.navigate.to('/login')


@ui.page('/login')
def login_page():
    crear_pantalla_login()


@ui.page('/inicio')
def inicio_page():
    crear_pantalla_inicio()


@ui.page('/modos')
def modos_page():
    crear_pantalla_modos()


@ui.page('/admin/modos')
def admin_modos_page():
    perfil = obtener_perfil_actual()

    if perfil not in (PERFIL_EMPRESA, PERFIL_MIXTO,):
        ui.notify(
            'No tienes permisos para acceder a la administración de modos',
            color='negative'
        )
        ui.navigate.to('/modos')
        return

    alarma = obtener_alarma_stub()
    crear_pantalla_admin_modos(alarma)


@ui.page('/sensores')
def sensores_page():
    crear_pantalla_sensores()


@ui.page('/historial')
def historial_page():
    crear_pantalla_historial()

@ui.page('/perfil')
def perfil_page():
    crear_pantalla_perfil_usuario()




# --------------------------------------------------
# ESTILOS (ROBUSTOS PARA QUASAR/NICEGUI)
# --------------------------------------------------

ui.add_head_html("""
<style>
/* ====== Botones: COLORES EXACTOS PEDIDOS ======
   - Normal: #3154A6
   - ARMAR:  #2F7D32
   - SOS:    #B3261E
   - ADMIN:  #223663
*/

/* 1) Variables Quasar (cuando Quasar pinta por tema) */
.btn-primary { --q-primary: #3154A6; }
.btn-armar   { --q-primary: #2F7D32; }
.btn-admin   { --q-primary: #223663; }
.btn-danger  { --q-negative: #B3261E; --q-primary: #B3261E; }

/* 2) Fuerza de fondo (cuando la clase queda fuera del .q-btn) */
.btn-primary.q-btn, .q-btn.btn-primary, .btn-primary .q-btn {
    background-color: #3154A6 !important;
    color: white !important;
    background-image: none !important;
    box-shadow: none !important;
}

.btn-armar.q-btn, .q-btn.btn-armar, .btn-armar .q-btn {
    background-color: #2F7D32 !important;
    color: white !important;
    background-image: none !important;
    box-shadow: none !important;
}

.btn-admin.q-btn, .q-btn.btn-admin, .btn-admin .q-btn {
    background-color: #223663 !important;
    color: white !important;
    background-image: none !important;
    box-shadow: none !important;
}

.btn-danger.q-btn, .q-btn.btn-danger, .btn-danger .q-btn {
    background-color: #B3261E !important;
    color: white !important;
    background-image: none !important;
    box-shadow: none !important;
}

/* asegura texto blanco dentro */
.btn-primary .q-btn__content,
.btn-armar .q-btn__content,
.btn-admin .q-btn__content,
.btn-danger .q-btn__content {
    color: white !important;
}
</style>
""", shared=True)


ui.run(
    host='0.0.0.0',
    port=8080,
    storage_secret='sentinelguard_secret'
)

