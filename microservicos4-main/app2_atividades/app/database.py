# app2_atividades/app/database.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar modelos para que o db.create_all() os reconheça
from app.models.atividade_model import Atividade
from app.models.nota_model import Nota
