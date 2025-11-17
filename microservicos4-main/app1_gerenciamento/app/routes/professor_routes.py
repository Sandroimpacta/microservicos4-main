# app1_gerenciamento/app/routes/professor_routes.py

from flask import Blueprint, jsonify, request
from app.database import db
from app.models.professor_model import Professor

professor_bp = Blueprint("professor_bp", __name__)

# 📘 LISTAR TODOS OS PROFESSORES
@professor_bp.route("/", methods=["GET"])
def listar_professores():
    """
    Lista todos os professores
    ---
    tags:
      - Professores
    responses:
      200:
        description: Lista de professores
    """
    professores = Professor.query.all()
    return jsonify([p.to_dict() for p in professores]), 200


# 📘 OBTER PROFESSOR POR ID
@professor_bp.route("/<int:id>", methods=["GET"])
def obter_professor(id):
    """
    Obtém um professor pelo ID
    ---
    tags:
      - Professores
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Professor encontrado
      404:
        description: Professor não encontrado
    """
    professor = Professor.query.get(id)
    if not professor:
        return jsonify({"erro": "Professor não encontrado"}), 404
    return jsonify(professor.to_dict()), 200


# 📘 CRIAR NOVO PROFESSOR
@professor_bp.route("/", methods=["POST"])
def criar_professor():
    """
    Cadastra um novo professor
    ---
    tags:
      - Professores
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: Ana Paula
            idade:
              type: integer
              example: 35
            materia:
              type: string
              example: Matemática
            observacoes:
              type: string
              example: Professora dedicada e pontual
    responses:
      201:
        description: Professor criado com sucesso
    """
    data = request.get_json()

    novo_professor = Professor(
        nome=data.get("nome"),
        idade=data.get("idade"),
        materia=data.get("materia"),
        observacoes=data.get("observacoes")
    )

    db.session.add(novo_professor)
    db.session.commit()
    return jsonify(novo_professor.to_dict()), 201


# 📘 ATUALIZAR PROFESSOR
@professor_bp.route("/<int:id>", methods=["PUT"])
def atualizar_professor(id):
    """
    Atualiza um professor existente
    ---
    tags:
      - Professores
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
            nome:
              type: string
              example: Ana Paula Souza
            idade:
              type: integer
              example: 36
            materia:
              type: string
              example: Física
            observacoes:
              type: string
              example: Coordenadora do laboratório
    responses:
      200:
        description: Professor atualizado com sucesso
      404:
        description: Professor não encontrado
    """
    professor = Professor.query.get(id)
    if not professor:
        return jsonify({"erro": "Professor não encontrado"}), 404

    data = request.get_json()
    professor.nome = data.get("nome", professor.nome)
    professor.idade = data.get("idade", professor.idade)
    professor.materia = data.get("materia", professor.materia)
    professor.observacoes = data.get("observacoes", professor.observacoes)

    db.session.commit()
    return jsonify(professor.to_dict()), 200


# 📘 DELETAR PROFESSOR
@professor_bp.route("/<int:id>", methods=["DELETE"])
def deletar_professor(id):
    """
    Exclui um professor
    ---
    tags:
      - Professores
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Professor excluído com sucesso
      404:
        description: Professor não encontrado
    """
    professor = Professor.query.get(id)
    if not professor:
        return jsonify({"erro": "Professor não encontrado"}), 404

    db.session.delete(professor)
    db.session.commit()
    return jsonify({"mensagem": "Professor excluído com sucesso"}), 200
