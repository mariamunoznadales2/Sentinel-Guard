from nicegui import app, ui


def check_login():
    if not app.storage.user.get("logged_in"):
        ui.navigate.to("/")
        return False
    return True
