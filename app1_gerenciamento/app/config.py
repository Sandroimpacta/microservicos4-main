# gerenciamento/app/config.py

import os

class Config:
    """Configurações principais do Flask"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'chave-secreta-padrao')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///gerenciamento.db'  # substitua pelo seu banco real, se quiser
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
