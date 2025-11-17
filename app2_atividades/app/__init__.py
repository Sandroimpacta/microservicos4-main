# app2_atividades/app/__init__.py
from flask import Flask
from flasgger import Swagger
from app.database import db

# Importa os Blueprints
from app.routes.atividade_routes import atividade_bp
from app.routes.nota_routes import nota_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Inicializa banco
    db.init_app(app)

    # Inicializa Swagger
    Swagger(app)

    # Registra os Blueprints
    app.register_blueprint(atividade_bp, url_prefix='/atividades')
    app.register_blueprint(nota_bp, url_prefix='/notas')

    # Rota raiz
    @app.route("/")
    def index():
        return "API de Atividades está rodando! ✅"

    return app
