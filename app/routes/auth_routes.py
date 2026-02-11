from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from app.services.auth_service import autenticar_usuario, criar_usuario


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
            session["is_admin"] = bool(usuario.get("is_admin"))
            flash("Login realizado com sucesso.", "sucesso")
            return redirect(url_for("lei.nova_lei"))

        flash("Usuário ou senha inválidos.", "erro")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Você saiu do sistema.", "info")
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


def admin_obrigatorio(view_func):
    """
    Decorator para exigir que o usuário seja administrador.
    """
    from functools import wraps

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Você não tem permissão para acessar esta página.", "erro")
            return redirect(url_for("lei.nova_lei"))
        return view_func(*args, **kwargs)

    return wrapper


@auth_bp.route("/usuarios/novo", methods=["GET", "POST"])
@login_obrigatorio
@admin_obrigatorio
def novo_usuario():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        senha = request.form.get("password", "")
        confirmar = request.form.get("confirm_password", "")
        is_admin = request.form.get("is_admin") == "on"

        if senha != confirmar:
            flash("As senhas não conferem.", "erro")
            return render_template("novo_usuario.html")

        ok, mensagem = criar_usuario(username, senha, is_admin=is_admin)
        categoria = "sucesso" if ok else "erro"
        flash(mensagem, categoria)

        if ok:
            return redirect(url_for("auth.novo_usuario"))

    return render_template("novo_usuario.html")

