from nicegui import ui
from sentinelguard.dominio.modo import ModoSeguridad


def crear_pantalla_admin_modos(alarma):

    gestor = alarma.gestor_bd
    modos = gestor.obtener_modos()
    sensores = alarma.listar_sensores()

    ui.label("Administración de Modos de Seguridad").style("font-size:1.5rem; font-weight:bold; margin-bottom:20px;")

    # -----------------------------
    # FORMULARIO CREAR MODO
    # -----------------------------
    with ui.expansion("➕ Crear nuevo modo", value=False):

        nombre_in = ui.input(label="Nombre del modo")
        desc_in = ui.input(label="Descripción")

        sensores_opciones = {str(s.id): f"{s.id} - {s.nombre}" for s in sensores}
        sensores_sel = ui.select(
            sensors_opciones := sensores_opciones,
            multiple=True,
            label="Sensores activos"
        )

        ret_entrada = ui.number(label="Retardo de entrada (segundos)", value=0)
        ret_salida = ui.number(label="Retardo de salida (segundos)", value=0)
        sensibilidad_in = ui.slider(min=1, max=10, value=5, label="Sensibilidad")

        def crear_modo():
            if not nombre_in.value:
                ui.notify("Introduce un nombre", color="red")
                return

            ids = [int(i) for i in sensores_sel.value] if sensores_sel.value else []

            modo = ModoSeguridad(
                nombre_in.value,
                desc_in.value,
                ids,
                int(ret_entrada.value),
                int(ret_salida.value),
                int(sensibilidad_in.value),
                predefinido=False
            )

            gestor.guardar_modo(modo)
            ui.notify("Modo creado")
            ui.navigate.to("/admin/modos")

        ui.button("Crear modo", on_click=crear_modo).style("margin-top: 10px;")

    # -----------------------------
    # LISTA DE MODOS
    # -----------------------------
    ui.separator()
    ui.label("Modos existentes").style("font-size:1.2rem; margin-top:20px;")

    for modo in modos:
        with ui.card().style("width:450px; margin-bottom:15px; padding:20px;"):

            ui.label(f"{modo.nombre}").style("font-weight:bold; font-size:1.1rem;")
            ui.label(modo.descripcion)
            ui.label(f"Sensores activos: {modo.ids_sensores_activos}")
            ui.label(f"Retardo entrada: {modo.retardo_entrada}s")
            ui.label(f"Retardo salida: {modo.retardo_salida}s")
            ui.label(f"Sensibilidad: {modo.sensibilidad}")

            # Eliminar modo
            def eliminar(m=modo):
                import sqlite3
                with gestor._conectar() as conn:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM modos WHERE id = ?", (m.id,))
                    conn.commit()

                ui.notify("Modo eliminado", color="red")
                ui.navigate.to("/admin/modos")

            ui.button("🗑️ Eliminar modo", on_click=eliminar, color="red").style("margin-top:10px;")
