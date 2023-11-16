from flask_login import UserMixin
# Creación de la clase User que funge como entidad para la tabla users de la base de datos.
class User(UserMixin):
    def __init__(self, id, username, password, usertype, fullname="") -> None:
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname
        self.usertype = usertype