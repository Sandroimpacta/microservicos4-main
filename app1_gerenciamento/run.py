# gerenciamento/run.py

import os
from flask import Flask
from app.database import db
from app.routes.professor_routes import professor_bp
from app.routes.turma_routes import turma_bp
from app.routes.aluno_routes import aluno_bp
from flasgger import Swagger

app = Flask(__name__)

# Padroniza caminho do banco para sempre /app/db/app.db
DB_FOLDER = os.path.join(os.path.dirname(__file__), "db")
os.makedirs(DB_FOLDER, exist_ok=True)
DB_PATH = os.path.join(DB_FOLDER, "app.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Registrar blueprints
app.register_blueprint(professor_bp, url_prefix='/professores')
app.register_blueprint(turma_bp, url_prefix='/turmas')
app.register_blueprint(aluno_bp, url_prefix='/alunos')

# Inicializar Swagger
swagger = Swagger(app)

# Criar tabelas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)








