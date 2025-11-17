# # 🧩 APP2-atividades/app/routes/nota_routes.py

from flask import Blueprint, request, jsonify
from app.database import db
from app.models.nota_model import Nota
from app.models.atividade_model import Atividade
from app.services.gerenciamento_client import get_aluno_by_id

nota_bp = Blueprint("nota_bp", __name__)

# -----------------------------
# LISTAR TODAS AS NOTAS
# -----------------------------
@nota_bp.route("/", methods=["GET"])
def listar_notas():
    """
    Lista todas as notas
    ---
    tags:
      - Notas
    responses:
      200:
        description: Lista de notas
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
    """
    notas = Nota.query.all()
    return jsonify([n.to_dict() for n in notas]), 200

# -----------------------------
# OBTER NOTA POR ID
# -----------------------------
@nota_bp.route("/<int:id>", methods=["GET"])
def obter_nota(id):
    """
    Obtém uma nota pelo ID
    ---
    tags:
      - Notas
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Nota encontrada
      404:
        description: Nota não encontrada
        content:
          application/json:
            schema:
              type: object
              properties:
                erro:
                  type: string
    """
    nota = Nota.query.get(id)
    if not nota:
        return jsonify({"erro": "Nota não encontrada"}), 404
    return jsonify(nota.to_dict()), 200

# -----------------------------
# CRIAR NOVA NOTA
# -----------------------------
@nota_bp.route("/", methods=["POST"])
def criar_nota():
    """
    Cria uma nova nota
    ---
    tags:
      - Notas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - nota
            - aluno_id
            - atividade_id
          properties:
            nota:
              type: number
              example: 8.5
            aluno_id:
              type: integer
              example: 1
            atividade_id:
              type: integer
              example: 1
    responses:
      201:
        description: Nota criada com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nota:
              type: number
              example: 8.5
            aluno_id:
              type: integer
              example: 1
            atividade_id:
              type: integer
              example: 1
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            erro:
              type: string
    """
    data = request.get_json()
    try:
        # Validação: aluno existe?
        aluno_id = data.get("aluno_id")
        if not aluno_id:
            return jsonify({"erro": "aluno_id é obrigatório"}), 400
        aluno_resp, aluno_status = get_aluno_by_id(aluno_id)
        if aluno_status != 200:
            return jsonify({"erro": f"Aluno com ID {aluno_id} não existe."}), 404
        # Validação: atividade existe?
        atividade_id = data.get("atividade_id")
        if not atividade_id:
            return jsonify({"erro": "atividade_id é obrigatório"}), 400
        if not Atividade.query.get(atividade_id):
            return jsonify({"erro": f"Atividade com ID {atividade_id} não existe."}), 404
        nova_nota = Nota(
            nota=data.get("nota"),
            aluno_id=aluno_id,
            atividade_id=atividade_id
        )
        db.session.add(nova_nota)
        db.session.commit()
        return jsonify(nova_nota.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500

# -----------------------------
# ATUALIZAR NOTA
# -----------------------------
@nota_bp.route("/<int:id>", methods=["PUT"])
def atualizar_nota(id):
    """
    Atualiza uma nota existente
    ---
    tags:
      - Notas
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nota:
              type: number
              example: 9.0
            aluno_id:
              type: integer
              example: 1
            atividade_id:
              type: integer
              example: 1
    responses:
      200:
        description: Nota atualizada com sucesso
        schema:
          type: object
      404:
        description: Nota não encontrada
        schema:
          type: object
          properties:
            erro:
              type: string
    """
    nota = Nota.query.get(id)
    if not nota:
        return jsonify({"erro": "Nota não encontrada"}), 404

    data = request.get_json()
    # Validação: aluno existe se enviado
    if "aluno_id" in data:
        aluno_id = data["aluno_id"]
        aluno_resp, aluno_status = get_aluno_by_id(aluno_id)
        if aluno_status != 200:
            return jsonify({"erro": f"Aluno com ID {aluno_id} não existe."}), 404
        nota.aluno_id = aluno_id
    # Validação: atividade existe se enviada
    if "atividade_id" in data:
        atividade_id = data["atividade_id"]
        if not Atividade.query.get(atividade_id):
            return jsonify({"erro": f"Atividade com ID {atividade_id} não existe."}), 404
        nota.atividade_id = atividade_id
    nota.nota = data.get("nota", nota.nota)

    db.session.commit()
    return jsonify(nota.to_dict()), 200

# -----------------------------
# DELETAR NOTA
# -----------------------------
@nota_bp.route("/<int:id>", methods=["DELETE"])
def deletar_nota(id):
    """
    Deleta uma nota
    ---
    tags:
      - Notas
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Nota excluída com sucesso
        content:
          application/json:
            schema:
              type: object
              properties:
                mensagem:
                  type: string
      404:
        description: Nota não encontrada
        content:
          application/json:
            schema:
              type: object
              properties:
                erro:
                  type: string
    """
    nota = Nota.query.get(id)
    if not nota:
        return jsonify({"erro": "Nota não encontrada"}), 404

    db.session.delete(nota)
    db.session.commit()
    return jsonify({"mensagem": "Nota excluída com sucesso"}), 200
