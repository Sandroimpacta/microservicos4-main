# app3_reservas/app/database.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar modelos para criar tabelas
from app.models.reserva_model import Reserva
