# reservas/app/models/reserva_model.py

from app.database import db

class Reserva(db.Model):
    __tablename__ = 'Reservas'
    
    id = db.Column(db.Integer, primary_key=True)
    num_sala = db.Column(db.Integer, nullable=False)
    lab = db.Column(db.Boolean, default=False)
    data = db.Column(db.Date, nullable=False)
    turma_id = db.Column(db.Integer, nullable=False)  # FK to Turma in gerenciamento - stored as integer
    aluno_id = db.Column(db.Integer)  # FK to Aluno in gerenciamento (não obrigatório persistir)
    professor_id = db.Column(db.Integer)  # FK to Professor em gerenciamento (não obrigatório persistir)

    def to_dict(self):
        return {
            "id": self.id,
            "num_sala": self.num_sala,
            "lab": bool(self.lab),
            "data": self.data.isoformat(),
            "turma_id": self.turma_id
            # Não retorna aluno_id e professor_id, pois não persiste
        }

    @staticmethod
    def from_dict(data):
        # Garante que 'data' é um objeto date
        from datetime import date
        data_value = data.get('data')
        if isinstance(data_value, str):
            data_value = date.fromisoformat(data_value)
        return Reserva(
            num_sala=data.get('num_sala'),
            lab=data.get('lab', False),
            data=data_value,
            turma_id=data.get('turma_id'),
            aluno_id=data.get('aluno_id'),
            professor_id=data.get('professor_id')
        )