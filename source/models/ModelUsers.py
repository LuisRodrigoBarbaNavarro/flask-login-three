from .entities.users import User

class ModelUsers():
    @classmethod
    def login(self, db, user):
        try:
            # Verificar si el usuario existe.
            cursor = db.connection.cursor()
            cursor.execute("call sp_verifyIdentity(%s, %s)", (user.username, user.password))
            row = cursor.fetchone()

            # Si el usuario existe, se crea un objeto de tipo 'User' y se retorna.
            if row[0] != None:
                user = User(row[0], row[1], row[2], row[4], row[3])
                return user
            else:
                return None
            
        except Exception as error:
            # Si ocurre un error, se imprime en consola y se lanza una excepción.
            raise Exception(error)
        
    @classmethod
    def get_by_id(self, db, id):
        try:
            # Verificar si el usuario existe.
            cursor = db.connection.cursor()
            cursor.execute("SELECT id, username,usertype, fullname FROM users WHERE id = %s", (id))
            row = cursor.fetchone()

            # Si el usuario existe, se crea un objeto de tipo 'User' y se retorna.
            if row != None:
                return User(row[0], row[1], None, row[2], row[3])
            else:
                return None
        except Exception as ex:
            # Si ocurre un error, se imprime en consola y se lanza una excepción.
            raise Exception(ex)