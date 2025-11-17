# APP1-gerenciamento/app/controllers/turma_controller.py
from app.database import db
from app.models.turma_model import Turma

def listar_turmas():
    return Turma.query.all()

def obter_turma(id):
    return Turma.query.get(id)

def criar_turma(data):
    nova = Turma(**data)
    db.session.add(nova)
    db.session.commit()
    return nova

def atualizar_turma(id, data):
    turma = Turma.query.get(id)
    if not turma:
        return None
    for key, value in data.items():
        setattr(turma, key, value)
    db.session.commit()
    return turma

def deletar_turma(id):
    turma = Turma.query.get(id)
    if not turma:
        return None
    db.session.delete(turma)
    db.session.commit()
    return True