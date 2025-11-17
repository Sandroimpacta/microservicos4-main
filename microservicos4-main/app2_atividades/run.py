# app2_atividades/run.py
import os
from flask import Flask
from app.database import db
from app.routes.atividade_routes import atividade_bp
from app.routes.nota_routes import nota_bp
from flasgger import Swagger

app = Flask(__name__)

# Pasta e banco dentro do container
db_folder = os.path.join(os.path.dirname(__file__), "db")
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, "app.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Registrar blueprints
app.register_blueprint(atividade_bp, url_prefix='/atividades')
app.register_blueprint(nota_bp, url_prefix='/notas')

# Inicializar Swagger
swagger = Swagger(app)

# Criar tabelas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)









