# app1_gerenciamento/app/controllers/professor_controller.py
from app.database import db
from app.models.professor_model import Professor

def listar_professores():
    return Professor.query.all()

def obter_professor(id):
    return Professor.query.get(id)

def criar_professor(data):
    novo = Professor(**data)
    db.session.add(novo)
    db.session.commit()
    return novo

def atualizar_professor(id, data):
    professor = Professor.query.get(id)
    if not professor:
        return None
    for key, value in data.items():
        setattr(professor, key, value)
    db.session.commit()
    return professor

def deletar_professor(id):
    professor = Professor.query.get(id)
    if not professor:
        return None
    db.session.delete(professor)
    db.session.commit()
    return True