
# app2_atividades/app/controllers/nota_controller.py
from app.database import db
from app.models.nota_model import Nota

def listar_notas():
    return Nota.query.all()

def obter_nota(id):
    return Nota.query.get(id)

def criar_nota(data):
    nova = Nota(**data)
    db.session.add(nova)
    db.session.commit()
    return nova

def atualizar_nota(id, data):
    nota = Nota.query.get(id)
    if not nota:
        return None
    for key, value in data.items():
        setattr(nota, key, value)
    db.session.commit()
    return nota

def deletar_nota(id):
    nota = Nota.query.get(id)
    if not nota:
        return None
    db.session.delete(nota)
    db.session.commit()
    return True