# app3_reservas/app/controllers/reserva_controller.py

from app.database import db
from app.models.reserva_model import Reserva
from app.services import gerenciamento_client as gm

# Campos permitidos para criação/atualização
ALLOWED_FIELDS = {'num_sala', 'lab', 'data', 'turma_id', 'aluno_id', 'professor_id'}


# --------------------------
# Funções de listagem/consulta
# --------------------------
def listar_reservas():
    """Retorna todas as reservas"""
    reservas = Reserva.query.all()
    return [r.to_dict() for r in reservas]  # Assumindo que o modelo tem método to_dict()


def obter_reserva(reserva_id):
    """Retorna uma reserva específica"""
    reserva = Reserva.query.get(reserva_id)
    if not reserva:
        return {"error": "Reserva não encontrada"}, 404
    return reserva.to_dict()


# --------------------------
# Função de criação
# --------------------------
def criar_reserva(data):
    """
    Cria uma nova reserva após validar:
    - Campos obrigatórios
    - Aluno, Turma e Professor via microserviço de gerenciamento
    - Evita duplicidade
    """
    required_fields = ["aluno_id", "turma_id", "professor_id", "num_sala", "data"]
    for field in required_fields:
        if field not in data:
            return {"error": f"Campo '{field}' obrigatório"}, 400

    # Validação externa via microserviço
    try:
        if not gm.check_aluno(data["aluno_id"]):
            return {"error": "Aluno não existe"}, 404
        if not gm.check_turma(data["turma_id"]):
            return {"error": "Turma não existe"}, 404
        if not gm.check_professor(data["professor_id"]):
            return {"error": "Professor não existe"}, 404
    except Exception as e:
        return {"error": "Erro ao verificar dados no gerenciamento", "details": str(e)}, 500

    # Evita duplicidade de reserva (mesmo aluno na mesma turma)
    existing = Reserva.query.filter_by(
        aluno_id=data["aluno_id"], turma_id=data["turma_id"]
    ).first()
    if existing:
        return {"error": "Reserva já existe para este aluno e turma"}, 409

    # Criação da reserva filtrando apenas campos permitidos
    payload = {k: v for k, v in data.items() if k in ALLOWED_FIELDS}
    reserva = Reserva.from_dict(payload)
    db.session.add(reserva)
    db.session.commit()
    return {"id": reserva.id, "message": "Reserva criada com sucesso"}, 201


# --------------------------
# Função de atualização
# --------------------------
def atualizar_reserva(reserva_id, data):
    """Atualiza campos permitidos de uma reserva existente"""
    reserva = Reserva.query.get(reserva_id)
    if not reserva:
        return {"error": "Reserva não encontrada"}, 404

    payload = {k: v for k, v in data.items() if k in ALLOWED_FIELDS}

    # Validação externa via microserviço se campos forem enviados
    try:
        if "aluno_id" in payload and payload["aluno_id"] is not None:
            if not gm.check_aluno(payload["aluno_id"]):
                return {"error": "Aluno não existe"}, 404
        if "turma_id" in payload and payload["turma_id"] is not None:
            if not gm.check_turma(payload["turma_id"]):
                return {"error": "Turma não existe"}, 404
        if "professor_id" in payload and payload["professor_id"] is not None:
            if not gm.check_professor(payload["professor_id"]):
                return {"error": "Professor não existe"}, 404
    except Exception as e:
        return {"error": "Erro ao verificar dados no gerenciamento", "details": str(e)}, 500

    # Garante que 'data' é um objeto date
    if "data" in payload and isinstance(payload["data"], str):
        from datetime import date
        payload["data"] = date.fromisoformat(payload["data"])
    for key, value in payload.items():
        setattr(reserva, key, value)

    db.session.commit()
    return {"id": reserva.id, "message": "Reserva atualizada com sucesso"}


# --------------------------
# Função de deleção
# --------------------------
def deletar_reserva(reserva_id):
    """Deleta uma reserva existente"""
    reserva = Reserva.query.get(reserva_id)
    if not reserva:
        return {"error": "Reserva não encontrada"}, 404

    db.session.delete(reserva)
    db.session.commit()
    return {"message": "Reserva deletada com sucesso"}

