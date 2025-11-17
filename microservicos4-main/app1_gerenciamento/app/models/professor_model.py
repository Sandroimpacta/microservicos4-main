# gerenciamento/app/models/professor_model.py

from app.database import db

class Professor(db.Model):
    __tablename__ = 'Professor'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    materia = db.Column(db.String(100))
    observacoes = db.Column(db.Text)

    turmas = db.relationship('Turma', back_populates='professor', cascade='all, delete')

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "materia": self.materia,
            "observacoes": self.observacoes
        }