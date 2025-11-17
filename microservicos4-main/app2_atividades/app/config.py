# atividades/app/config.py
import os

class Config:
    """Configurações do microserviço de atividades"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'chave-atividades')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///atividades.db'  # altere se usar SQL Server ou outro
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False