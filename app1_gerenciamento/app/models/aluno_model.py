# app1_gerenciamento/app/models/aluno_model.py

from app.database import db
from datetime import date

class Aluno(db.Model):
    __tablename__ = 'Aluno'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    turma_id = db.Column(db.Integer, db.ForeignKey('Turma.id'), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)

    # Campos de notas e média final
    nota_primeiro_semestre = db.Column(db.Float, nullable=True)
    nota_segundo_semestre = db.Column(db.Float, nullable=True)
    media_final = db.Column(db.Float, nullable=True)

    # Relacionamento com a tabela Turma
    turma = db.relationship('Turma', back_populates='alunos')

    def calcular_media(self):
        """Calcula automaticamente a média final do aluno."""
        if self.nota_primeiro_semestre is not None and self.nota_segundo_semestre is not None:
            self.media_final = (self.nota_primeiro_semestre + self.nota_segundo_semestre) / 2
        else:
            self.media_final = None

    def to_dict(self):
        """Converte o objeto Aluno em dicionário para retorno JSON."""
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "turma_id": self.turma_id,
            "data_nascimento": self.data_nascimento.isoformat() if self.data_nascimento else None,
            "nota_primeiro_semestre": self.nota_primeiro_semestre,
            "nota_segundo_semestre": self.nota_segundo_semestre,
            "media_final": self.media_final
        }

    def __repr__(self):
        return f"<Aluno {self.nome} (Média: {self.media_final})>"
