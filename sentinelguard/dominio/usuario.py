class Usuario:
    def __init__(self,
                 identificador: int,
                 nombre: str,
                 email: str,
                 direccion: str,
                 perfil: str = "hogar",
                 idioma: str = "es",
                 tema: str = "claro",
                 password: str = ""):

        self.id = identificador
        self.nombre = nombre
        self.email = email
        self.direccion = direccion
        self.perfil = perfil          # hogar | empresa | mixto | admin
        self.idioma = idioma
        self.tema = tema              # claro | oscuro
        self.password = password      # contraseña para login
