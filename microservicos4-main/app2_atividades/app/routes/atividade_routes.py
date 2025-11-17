# app2_atividades/app/routes/atividade_routes.py

from flask import Blueprint, request, jsonify
from app.database import db
from app.models.atividade_model import Atividade
from datetime import date
from app.services.gerenciamento_client import get_professor_by_id, get_aluno_by_id
import requests

atividade_bp = Blueprint("atividade_bp", __name__)

# -----------------------------
# LISTAR TODAS AS ATIVIDADES
# -----------------------------
@atividade_bp.route("/", methods=["GET"])
def listar_atividades():
    """
    Lista todas as atividades
    ---
    tags:
      - Atividades
    responses:
      200:
        description: Lista de atividades
        schema:
          type: array
          items:
            type: object
    """
    atividades = Atividade.query.all()
    return jsonify([a.to_dict() for a in atividades]), 200

# -----------------------------
# OBTER ATIVIDADE POR ID
# -----------------------------
@atividade_bp.route("/<int:id>", methods=["GET"])
def obter_atividade(id):
    """
    Obtém uma atividade pelo ID
    ---
    tags:
      - Atividades
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Atividade encontrada
        schema:
          type: object
      404:
        description: Atividade não encontrada
        schema:
          type: object
          properties:
            erro:
              type: string
    """
    atividade = Atividade.query.get(id)
    if not atividade:
        return jsonify({"erro": "Atividade não encontrada"}), 404
    return jsonify(atividade.to_dict()), 200

# -----------------------------
# CRIAR NOVA ATIVIDADE
# -----------------------------
@atividade_bp.route("/", methods=["POST"])
def criar_atividade():
    """
    Cria uma nova atividade
    ---
    tags:
      - Atividades
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - nome_atividade
            - data_entrega
            - turma_id
            - professor_id
          properties:
            nome_atividade:
              type: string
              example: "Prova de Matemática"
            descricao:
              type: string
              example: "Conteúdo de álgebra"
            peso_porcento:
              type: integer
              example: 10
            data_entrega:
              type: string
              format: date
              example: "2025-11-10"
            turma_id:
              type: integer
              example: 1
            professor_id:
              type: integer
              example: 1
    responses:
      201:
        description: Atividade criada com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome_atividade:
              type: string
              example: "Prova de Matemática"
            descricao:
              type: string
              example: "Conteúdo de álgebra"
            peso_porcento:
              type: integer
              example: 10
            data_entrega:
              type: string
              format: date
              example: "2025-11-10"
            turma_id:
              type: integer
              example: 1
            professor_id:
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
        # Validação: turma existe?
        turma_id = data.get("turma_id")
        if not turma_id:
            return jsonify({"erro": "turma_id é obrigatório"}), 400
        turma_resp = requests.get(f"http://app1_gerenciamento:5000/turmas/{turma_id}")
        if turma_resp.status_code != 200:
            return jsonify({"erro": f"Turma com ID {turma_id} não existe."}), 404
        # Validação: professor existe?
        professor_id = data.get("professor_id")
        if not professor_id:
            return jsonify({"erro": "professor_id é obrigatório"}), 400
        prof_resp, prof_status = get_professor_by_id(professor_id)
        if prof_status != 200:
            return jsonify({"erro": f"Professor com ID {professor_id} não existe."}), 404
        data_entrega = date.fromisoformat(data["data_entrega"])

        nova = Atividade(
            nome_atividade=data.get("nome_atividade"),
            descricao=data.get("descricao"),
            peso_porcento=data.get("peso_porcento", 100),
            data_entrega=data_entrega,
            turma_id=turma_id,
            professor_id=professor_id
        )
        db.session.add(nova)
        db.session.commit()
        return jsonify(nova.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500

# -----------------------------
# ATUALIZAR ATIVIDADE
# -----------------------------
@atividade_bp.route("/<int:id>", methods=["PUT"])
def atualizar_atividade(id):
    """
    Atualiza uma atividade existente
    ---
    tags:
      - Atividades
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
            nome_atividade:
              type: string
              example: "Prova Atualizada"
            descricao:
              type: string
              example: "Conteúdo atualizado"
            peso_porcento:
              type: integer
              example: 15
            data_entrega:
              type: string
              format: date
              example: "2025-11-12"
            turma_id:
              type: integer
              example: 2
            professor_id:
              type: integer
              example: 2
    responses:
      200:
        description: Atividade atualizada com sucesso
        schema:
          type: object
      404:
        description: Atividade não encontrada
        schema:
          type: object
          properties:
            erro:
              type: string
    """
    atividade = Atividade.query.get(id)
    if not atividade:
        return jsonify({"erro": "Atividade não encontrada"}), 404

    data = request.get_json()
    # Validação: turma existe se enviada
    if "turma_id" in data:
        turma_id = data["turma_id"]
        turma_resp = requests.get(f"http://app1_gerenciamento:5000/turmas/{turma_id}")
        if turma_resp.status_code != 200:
            return jsonify({"erro": f"Turma com ID {turma_id} não existe."}), 404
        atividade.turma_id = turma_id
    # Validação: professor existe se enviado
    if "professor_id" in data:
        professor_id = data["professor_id"]
        prof_resp, prof_status = get_professor_by_id(professor_id)
        if prof_status != 200:
            return jsonify({"erro": f"Professor com ID {professor_id} não existe."}), 404
        atividade.professor_id = professor_id
    atividade.nome_atividade = data.get("nome_atividade", atividade.nome_atividade)
    atividade.descricao = data.get("descricao", atividade.descricao)
    atividade.peso_porcento = data.get("peso_porcento", atividade.peso_porcento)
    if "data_entrega" in data and data["data_entrega"]:
        atividade.data_entrega = date.fromisoformat(data["data_entrega"])
    db.session.commit()
    return jsonify(atividade.to_dict()), 200

# -----------------------------
# DELETAR ATIVIDADE
# -----------------------------
@atividade_bp.route("/<int:id>", methods=["DELETE"])
def deletar_atividade(id):
    """
    Deleta uma atividade
    ---
    tags:
      - Atividades
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Atividade excluída com sucesso
        schema:
          type: object
          properties:
            mensagem:
              type: string
      404:
        description: Atividade não encontrada
        schema:
          type: object
          properties:
            erro:
              type: string
    """
    atividade = Atividade.query.get(id)
    if not atividade:
        return jsonify({"erro": "Atividade não encontrada"}), 404

    db.session.delete(atividade)
    db.session.commit()
    return jsonify({"mensagem": "Atividade excluída com sucesso"}), 200
