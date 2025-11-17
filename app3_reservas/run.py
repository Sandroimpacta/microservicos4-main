# /reservas/run.py
import os
from flask import Flask
from app.database import db
from app.routes.reserva_routes import reserva_bp
from flasgger import Swagger

app = Flask(__name__)

# Caminho do banco dentro do container
db_folder = os.path.join(os.path.dirname(__file__), "db")
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, "app.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Registrar blueprint
app.register_blueprint(reserva_bp, url_prefix='/reservas')

# Inicializar Swagger
swagger = Swagger(app)

# Criar tabelas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)






