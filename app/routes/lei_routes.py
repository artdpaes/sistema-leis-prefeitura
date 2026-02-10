from flask import Blueprint, render_template, request, redirect
from app.services.lei_service import gerar_proximo_numero, salvar_lei
from app.routes.auth_routes import login_obrigatorio

lei_bp = Blueprint("lei", __name__)

@lei_bp.route("/nova-lei", methods=["GET", "POST"])
@login_obrigatorio
def nova_lei():
    numero = gerar_proximo_numero()
    if request.method == "POST":
        salvar_lei(
            numero,
            request.form["titulo"],
            request.form["descricao"],
            request.form["data_lei"]
        )
        return redirect("/sucesso")
    return render_template("nova_lei.html", numero_lei=numero)

@lei_bp.route("/sucesso")
@login_obrigatorio
def sucesso():
    return render_template("sucesso.html")
