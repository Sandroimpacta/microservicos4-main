# app3_reservas/app/__init__.py
from flask import Flask
from flasgger import Swagger
from app.database import db

# Importa Blueprint
from app.routes.reserva_routes import reserva_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Inicializa banco
    db.init_app(app)

    # Inicializa Swagger
    Swagger(app)

    # Registra Blueprint
    app.register_blueprint(reserva_bp, url_prefix='/reservas')

    # Rota raiz
    @app.route("/")
    def index():
        return "API de Reservas está rodando! ✅"

    return app
