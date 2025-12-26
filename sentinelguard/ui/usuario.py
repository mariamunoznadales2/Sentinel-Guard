from nicegui import ui


def crear_pantalla_usuario(alarma):
    gestor = alarma.gestor_bd
    usuario = gestor.obtener_usuario()

    ui.label("Perfil de Usuario").style("font-size: 1.6rem; font-weight: bold; margin-bottom: 20px;")

    nombre = ui.input(label="Nombre", value=usuario.nombre)
    email = ui.input(label="Email", value=usuario.email)
    direccion = ui.input(label="Dirección", value=usuario.direccion)

    perfil = ui.select(
        {"hogar": "Hogar", "empresa": "Empresa", "mixto": "Mixto"},
        label="Perfil",
        value=usuario.perfil
    )

    idioma = ui.select(
        {"es": "Español", "en": "Inglés"},
        label="Idioma",
        value=usuario.idioma
    )

    tema = ui.select(
        {"claro": "Claro", "oscuro": "Oscuro"},
        label="Tema",
        value=usuario.tema
    )

    def guardar_cambios():
        usuario.nombre = nombre.value
        usuario.email = email.value
        usuario.direccion = direccion.value
        usuario.perfil = perfil.value
        usuario.idioma = idioma.value
        usuario.tema = tema.value

        gestor.guardar_usuario(usuario)

        ui.notify("Cambios guardados")

        # Aplicar tema visual
        if usuario.tema == "oscuro":
            ui.dark_mode().enable()
        else:
            ui.dark_mode().disable()

    ui.button("Guardar cambios", on_click=guardar_cambios).style("margin-top:15px;")
