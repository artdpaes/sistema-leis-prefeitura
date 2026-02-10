from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from app.services.auth_service import autenticar_usuario


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        senha = request.form.get("password")

        usuario = autenticar_usuario(username, senha)
        if usuario:
            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["username"]
            return redirect(url_for("lei.nova_lei"))

        flash("Usuário ou senha inválidos.", "erro")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


def login_obrigatorio(view_func):
    """
    Decorator simples para exigir login em rotas protegidas.
    """
    from functools import wraps

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)

    return wrapper

