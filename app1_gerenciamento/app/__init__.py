# app1_gerenciamento/app/__init__.py


from flask import Flask
from flasgger import Swagger
from app.database import db
from app.routes.professor_routes import professor_bp
from app.routes.aluno_routes import aluno_bp
from app.routes.turma_routes import turma_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Inicializa o banco
    db.init_app(app)

    # Inicializa Swagger
    Swagger(app)

    # Registra os Blueprints
    # Importar e registrar blueprints
    from app.routes.professor_routes import professor_bp
    from app.routes.turma_routes import turma_bp
    from app.routes.aluno_routes import aluno_bp

    app.register_blueprint(professor_bp, url_prefix='/professores')
    app.register_blueprint(turma_bp, url_prefix='/turmas')
    app.register_blueprint(aluno_bp, url_prefix='/alunos')

    # Rota raiz
    @app.route("/")
    def index():
        return "API de Gerenciamento está rodando! 🚀"

    return app
