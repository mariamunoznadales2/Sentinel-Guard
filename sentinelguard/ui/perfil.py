from nicegui import app

PERFIL_HOGAR = 'Hogar'
PERFIL_EMPRESA = 'Empresa'
PERFIL_MIXTO = 'Mixto'


def obtener_perfil_actual():
    return app.storage.user.get('perfil')