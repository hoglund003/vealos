# Victor og Pelle
from datetime import date
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_manager, login_user, logout_user, login_required, LoginManager, UserMixin
from werkzeug.exceptions import abort
from flask import current_app
from application.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_user
from application import login_manager

class User(UserMixin):
    @staticmethod
    def get(user_id):
        user = User()
        user_row = get_user(user_id)
        user.id = user_row['id']
        return user

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

bp = Blueprint("auth", __name__)


@bp.route("/auth/", methods =["GET", "POST"])
def login():
    if request.method == 'POST':
        user_email = request.form.get("email")
        user_password = request.form.get("password")
        correct_email = 0
        correct_password = 0
        db = get_db()

        user = db.execute("SELECT * FROM users WHERE email = ?", (user_email,)).fetchone()

        if not user:
            correct_email = 0
        else:
            correct_email = 1
        if not user:
            correct_password = 0
        elif check_password_hash(user['password'], user_password) == True:
            correct_password = 1

        if (correct_email == 1) and (correct_password == 1):
            flash('Du er logget inn')
            return redirect(url_for('index.index'))
        else:
            flash('Du skrevet feil passord eller email')

    return render_template("auth.html")


@bp.route("/forgot_password", methods =["GET", "POST"])
def forgot_password():
    if request.method == 'POST':
        user_email = request.form.get('email_f')
        pass_code = request.form.get('pass_code')
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (user_email,)).fetchone()
        if not user:
            flash('Denne mailen er ikke registert på en bruker')
        else:
            flash('Vi sender deg en mail med en kode du skriver inn under')
    return render_template("glemt_passord.html")

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index.index"))



