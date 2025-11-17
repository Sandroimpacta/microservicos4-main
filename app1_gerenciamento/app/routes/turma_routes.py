# app1_gerenciamento/app/routes/turma_routes.py

from flask import Blueprint, jsonify, request
from app.database import db
from app.models.turma_model import Turma
from app.models.professor_model import Professor

turma_bp = Blueprint("turma_bp", __name__)

# 📘 LISTAR TODAS AS TURMAS
@turma_bp.route("/", methods=["GET"])
def listar_turmas():
    """
    Lista todas as turmas
    ---
    tags:
      - Turmas
    responses:
      200:
        description: Lista de turmas
    """
    turmas = Turma.query.all()
    return jsonify([t.to_dict() for t in turmas]), 200


# 📘 OBTER TURMA POR ID
@turma_bp.route("/<int:id>", methods=["GET"])
def obter_turma(id):
    """
    Obtém uma turma pelo ID
    ---
    tags:
      - Turmas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Turma encontrada
      404:
        description: Turma não encontrada
    """
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({"erro": "Turma não encontrada"}), 404
    return jsonify(turma.to_dict()), 200


# 📘 CRIAR NOVA TURMA
@turma_bp.route("/", methods=["POST"])
def criar_turma():
    """
    Cadastra uma nova turma
    ---
    tags:
      - Turmas
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            descricao:
              type: string
              example: Turma A - Matemática
            professor_id:
              type: integer
              example: 1
            ativo:
              type: boolean
              example: true
    responses:
      201:
        description: Turma criada com sucesso
      400:
        description: Professor não encontrado
    """
    data = request.get_json()

    professor_id = data.get("professor_id")
    if not Professor.query.get(professor_id):
        return jsonify({"erro": "Professor não encontrado"}), 400

    nova_turma = Turma(
        descricao=data.get("descricao"),
        professor_id=professor_id,
        ativo=data.get("ativo", True)
    )

    db.session.add(nova_turma)
    db.session.commit()
    return jsonify(nova_turma.to_dict()), 201


# 📘 ATUALIZAR TURMA
@turma_bp.route("/<int:id>", methods=["PUT"])
def atualizar_turma(id):
    """
    Atualiza uma turma existente
    ---
    tags:
      - Turmas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            descricao:
              type: string
              example: Turma B - Física
            professor_id:
              type: integer
              example: 2
            ativo:
              type: boolean
              example: false
    responses:
      200:
        description: Turma atualizada com sucesso
      404:
        description: Turma não encontrada
      400:
        description: Professor não encontrado
    """
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({"erro": "Turma não encontrada"}), 404

    data = request.get_json()

    # Se o professor for alterado, validar existência
    professor_id = data.get("professor_id", turma.professor_id)
    if not Professor.query.get(professor_id):
        return jsonify({"erro": "Professor não encontrado"}), 400

    turma.descricao = data.get("descricao", turma.descricao)
    turma.professor_id = professor_id
    turma.ativo = data.get("ativo", turma.ativo)

    db.session.commit()
    return jsonify(turma.to_dict()), 200


# 📘 DELETAR TURMA
@turma_bp.route("/<int:id>", methods=["DELETE"])
def deletar_turma(id):
    """
    Exclui uma turma
    ---
    tags:
      - Turmas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Turma excluída com sucesso
      404:
        description: Turma não encontrada
    """
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({"erro": "Turma não encontrada"}), 404

    db.session.delete(turma)
    db.session.commit()
    return jsonify({"mensagem": "Turma excluída com sucesso"}), 200