
# APP2-atividades/app/models/atividade_model.py

from app.database import db
from datetime import date

class Atividade(db.Model):
    __tablename__ = 'Atividades'  # ⚠️ cuidado com o nome exato da tabela

    id = db.Column(db.Integer, primary_key=True)
    nome_atividade = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.String(500))
    peso_porcento = db.Column(db.Integer, default=100)
    data_entrega = db.Column(db.Date, nullable=False)
    turma_id = db.Column(db.Integer, nullable=False)      # FK para Turma (outro serviço)
    professor_id = db.Column(db.Integer, nullable=False)  # FK para Professor (outro serviço)

    # Relacionamento com Notas
    notas = db.relationship(
        'Nota', 
        back_populates='atividade', 
        cascade='all, delete-orphan'
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome_atividade": self.nome_atividade,
            "descricao": self.descricao,
            "peso_porcento": self.peso_porcento,
            "data_entrega": self.data_entrega.isoformat(),
            "turma_id": self.turma_id,
            "professor_id": self.professor_id,
            "notas": [nota.to_dict() for nota in self.notas]  # inclui as notas relacionadas
        }