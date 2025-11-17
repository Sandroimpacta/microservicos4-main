# 🧩 APP2-atividades/app/models/nota_model.py

from app.database import db

class Nota(db.Model):
    __tablename__ = "notas"

    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Float, nullable=False)
    aluno_id = db.Column(db.Integer, nullable=False)  # FK -> Aluno.id (outro serviço)
    
    # 🔹 FK para Atividade
    atividade_id = db.Column(db.Integer, db.ForeignKey("Atividades.id"), nullable=False)

    # Relacionamento de volta
    atividade = db.relationship(
        "Atividade", 
        back_populates="notas"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nota": self.nota,
            "aluno_id": self.aluno_id,
            "atividade_id": self.atividade_id
        }