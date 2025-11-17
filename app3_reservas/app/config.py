# app3_reservas/app/config.py
import os

class Config:
    """Configurações do microserviço de reservas"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'chave-reservas')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///reservas.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False