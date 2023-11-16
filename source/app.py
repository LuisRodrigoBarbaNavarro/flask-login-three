# Importamos las librerías necesarias.
from flask_login import LoginManager, login_user, logout_user, login_required
from flask import Flask, flash, redirect, render_template, request, url_for
from models.ModelUsers import ModelUsers
from models.entities.users import User
from flask_mysqldb import MySQL
from functools import wraps
from config import config

# Establecemos la configuración de la aplicación.
app = Flask(__name__)
db = MySQL(app)
login_manager_app = LoginManager(app)

# Definimos las rutas de la aplicación.
# Ruta principal.
@app.route("/")
def index():
    return redirect("login")

# Ruta para el registro de usuarios.
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User(0, request.form['username-input'], request.form['password-input'],0)
        logged_user = ModelUsers.login(db, user)
        if logged_user != None:
            if logged_user.usertype == 1:
                login_user(logged_user)
                return redirect(url_for("admin"))
            else:
                login_user(logged_user)
                return redirect(url_for("home"))
        else:
            flash("Usuario o contraseña incorrectos.")
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")

# Ruta de menú principal para usuarios normales.
@app.route("/home")
@login_required
def home():
    return render_template("public/home.html")

# Ruta de menú principal para usuarios administradores.
@app.route("/admin")
@login_required
def admin():
    return render_template("public/admin.html")

@login_manager_app.user_loader
def load_user(id):
    return ModelUsers.get_by_id(db, id)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # Verificar si el usuario está autenticado y es un administrador
            if not current_user.is_authenticated or current_user.usertype != 1:
                abort(403) # Acceso prohibido
                return func(*args, **kwargs)
            return decorated_view

# Ruta para cerrar sesión.
if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.run()