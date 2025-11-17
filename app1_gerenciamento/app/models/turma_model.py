# gerenciamento/app/models/turma_model.py


from app.database import db

class Turma(db.Model):
    __tablename__ = 'Turma'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('Professor.id'), nullable=False)
    ativo = db.Column(db.Boolean, default=True)

    professor = db.relationship('Professor', back_populates='turmas')
    alunos = db.relationship('Aluno', back_populates='turma', cascade='all, delete')

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "professor_id": self.professor_id,
            "ativo": bool(self.ativo)
        }