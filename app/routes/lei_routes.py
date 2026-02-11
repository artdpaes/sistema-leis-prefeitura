from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.lei_service import gerar_proximo_numero, salvar_lei
from app.routes.auth_routes import login_obrigatorio

lei_bp = Blueprint("lei", __name__)

@lei_bp.route("/nova-lei", methods=["GET", "POST"])
@login_obrigatorio
def nova_lei():
    numero = gerar_proximo_numero()
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        data_lei = request.form.get("data_lei", "").strip()

        if not titulo or not data_lei:
            flash("Título e data da lei são obrigatórios.", "erro")
            return render_template("nova_lei.html", numero_lei=numero)

        salvar_lei(numero, titulo, descricao, data_lei)
        flash("Lei cadastrada com sucesso.", "sucesso")
        return redirect(url_for("lei.sucesso", numero=numero))
    return render_template("nova_lei.html", numero_lei=numero)

@lei_bp.route("/sucesso")
@login_obrigatorio
def sucesso():
    numero = request.args.get("numero")
    return render_template("sucesso.html", numero_lei=numero)
