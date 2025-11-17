
# app2_atividades/app/controllers/atividade_controller.py
from app.database import db
from app.models.atividade_model import Atividade

def listar_atividades():
    return Atividade.query.all()

def obter_atividade(id):
    return Atividade.query.get(id)

def criar_atividade(data):
    nova = Atividade(**data)
    db.session.add(nova)
    db.session.commit()
    return nova

def atualizar_atividade(id, data):
    atividade = Atividade.query.get(id)
    if not atividade:
        return None
    for key, value in data.items():
        setattr(atividade, key, value)
    db.session.commit()
    return atividade

def deletar_atividade(id):
    atividade = Atividade.query.get(id)
    if not atividade:
        return None
    db.session.delete(atividade)
    db.session.commit()
    return True