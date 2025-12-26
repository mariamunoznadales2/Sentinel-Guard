from nicegui import ui
from sentinelguard.dominio.sensor import Sensor, TipoSensor, EstadoSensor


def crear_pantalla_admin_sensores(alarma):

    ui.label("Administración de Sensores").style("font-size: 1.5rem; font-weight: bold; margin-bottom: 20px;")

    gestor = alarma.gestor_bd
    sensores = gestor.obtener_sensores()

    # -------------------------
    # FORMULARIO CREAR SENSOR
    # -------------------------
    with ui.expansion("➕ Crear nuevo sensor", value=False):

        nombre_input = ui.input(label="Nombre del sensor")
        zona_input = ui.input(label="Zona")
        tipo_input = ui.select(
            {t.name: t.name for t in TipoSensor},
            label="Tipo de sensor"
        )

        def crear_sensor():
            if not nombre_input.value or not tipo_input.value:
                ui.notify("Completa todos los campos", color="red")
                return

            nuevo = Sensor(
                identificador=0,
                nombre=nombre_input.value,
                tipo=TipoSensor[tipo_input.value],
                zona=zona_input.value
            )

            gestor.guardar_sensor(nuevo)

            ui.notify("Sensor creado")
            ui.navigate.to("/admin/sensores")

        ui.button("Crear sensor", on_click=crear_sensor).style("margin-top: 10px;")


    # -------------------------
    # LISTADO DE SENSORES
    # -------------------------
    ui.separator()

    ui.label("Sensores existentes").style("font-size: 1.2rem; margin-top: 20px;")

    for sensor in sensores:
        with ui.card().style("width: 420px; margin-bottom: 15px; padding:20px;"):

            ui.label(f"ID {sensor.id} — {sensor.nombre}").style("font-weight: bold;")
            ui.label(f"Tipo: {sensor.tipo.name}")
            ui.label(f"Zona: {sensor.zona}")
            ui.label(f"Estado: {sensor.estado.name}")

            # FORMULARIO EDICIÓN --------------------
            with ui.expansion("✏️ Editar sensor", value=False):

                nombre_ed = ui.input(label="Nombre", value=sensor.nombre)
                zona_ed = ui.input(label="Zona", value=sensor.zona)
                tipo_ed = ui.select(
                    {t.name: t.name for t in TipoSensor},
                    label="Tipo",
                    value=sensor.tipo.name
                )

                estado_ed = ui.select(
                    {e.name: e.name for e in EstadoSensor},
                    label="Estado",
                    value=sensor.estado.name
                )

                def guardar_cambios(s=sensor):
                    s.nombre = nombre_ed.value
                    s.zona = zona_ed.value
                    s.tipo = TipoSensor[tipo_ed.value]
                    s.estado = EstadoSensor[estado_ed.value]

                    gestor.actualizar_sensor(s)

                    ui.notify("Cambios guardados")
                    ui.navigate.to("/admin/sensores")

                ui.button("Guardar cambios", on_click=guardar_cambios).style("margin-top:10px;")

            # BOTÓN ELIMINAR ------------------------
            def eliminar(s_id=sensor.id):
                gestor.eliminar_sensor(s_id)
                ui.notify("Sensor eliminado", color="red")
                ui.navigate.to("/admin/sensores")

            ui.button("🗑️ Eliminar", on_click=eliminar, color="red").style("margin-top:10px;")
