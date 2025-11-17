# app1_gerenciamento/app/controllers/aluno_controller.py
from app.database import db
from app.models.aluno_model import Aluno

def listar_alunos():
    alunos = Aluno.query.all()
    return [a.to_dict() for a in alunos]

def obter_aluno(id):
    aluno = Aluno.query.get(id)
    return aluno.to_dict() if aluno else None

def criar_aluno(data):
    novo = Aluno(**data)
    db.session.add(novo)
    db.session.commit()
    return novo.to_dict()

def atualizar_aluno(id, data):
    aluno = Aluno.query.get(id)
    if not aluno:
        return None

    for key, value in data.items():
        setattr(aluno, key, value)
    db.session.commit()
    return aluno.to_dict()

def deletar_aluno(id):
    aluno = Aluno.query.get(id)
    if not aluno:
        return None
    db.session.delete(aluno)
    db.session.commit()
    return True
