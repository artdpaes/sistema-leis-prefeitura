from flask import Flask
import os
from dotenv import load_dotenv
from app.routes.lei_routes import lei_bp
from app.routes.auth_routes import auth_bp

def create_app():
    load_dotenv()

    app = Flask(__name__)

    # Chave secreta para sessões (login)
    app.secret_key = os.getenv("SECRET_KEY", "chave-insegura-altere-no-.env")

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(lei_bp)

    return app
