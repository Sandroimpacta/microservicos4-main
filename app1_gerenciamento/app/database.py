# app1_gerenciamento/app/database.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar modelos para que o db.create_all() os reconheça
from app.models.aluno_model import Aluno
from app.models.professor_model import Professor
from app.models.turma_model import Turma
