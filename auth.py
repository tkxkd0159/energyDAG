import functools
import re
from flask import Blueprint, render_template, abort, redirect, url_for, \
                  g, request, session, flash
from jinja2 import TemplateNotFound
from werkzeug.security import check_password_hash, generate_password_hash

from rdb import get_db

auth = Blueprint('auth', __name__, template_folder='templates', url_prefix='/auth')

def login_required(f):

    @functools.wraps(f)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.signin"))
        return f(**kwargs)
    return wrapped_view

@auth.before_app_request
def load_logged_in_user():

    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE idx = ?", (user_id,)).fetchone()
        )


@auth.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username: str = request.form["walletid"]
        username = username.lower()
        password: str = request.form["walletpw"]
        db = get_db()
        error = None

        id_pattern = re.compile(r"^[a-zA-Z]+")
        anti_id_pattern = re.compile(r"[^a-zA-Z0-9]+")
        if id_pattern.match(username) is None:
            error = "Username must begin with plain characters"
        elif anti_id_pattern.findall(username) != []:
            error = "You must use only alphabets and numbers"
        elif len(username) < 6:
            error = "Username must be at least 6 characters long"
        elif len(password) < 10:
            error = "Password must be at least 10 characters long"
        elif (
            db.execute("SELECT idx FROM user WHERE username = ?", (username,)).fetchone()
            is not None
        ):
            error = f"User {username} is already registered"

        if error is None:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/register.html")


@auth.route("/signin", methods=("GET", "POST"))
def signin():
    if request.method == "POST":
        username = request.form["walletid"]
        username = username.lower()
        password = request.form["walletpw"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username!"
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password!"

        if error is None:
            session.clear()
            session["user_id"] = user["idx"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/signin.html")


@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))