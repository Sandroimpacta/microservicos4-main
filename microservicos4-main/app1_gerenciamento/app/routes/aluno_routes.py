# app1_gerenciamento/app/routes/aluno_routes.py
from flask import Blueprint, jsonify, request
from datetime import datetime
from app.database import db
from app.models.aluno_model import Aluno
from app.models.turma_model import Turma

aluno_bp = Blueprint("aluno_bp", __name__)

# -----------------------------
# 📘 LISTAR TODOS OS ALUNOS
# -----------------------------
@aluno_bp.route("/", methods=["GET"])
def listar_alunos():
    """
    Lista todos os alunos com notas e média final calculada automaticamente
    ---
    tags:
      - Alunos
    responses:
      200:
        description: Lista de alunos cadastrados com média final
        schema:
          type: array
          items:
            type: object
            properties:
              id: {type: integer, example: 1}
              nome: {type: string, example: "Maria Oliveira"}
              idade: {type: integer, example: 15}
              turma_id: {type: integer, example: 2}
              data_nascimento: {type: string, format: date, example: "2010-04-12"}
              nota_primeiro_semestre: {type: number, format: float, example: 8.5}
              nota_segundo_semestre: {type: number, format: float, example: 9.0}
              media_final: {type: number, format: float, example: 8.75}
    """
    alunos = Aluno.query.all()

    resultado = []
    for aluno in alunos:
        aluno.calcular_media()  # 🔹 garante que a média está atualizada
        resultado.append(aluno.to_dict())

    return jsonify(resultado), 200


# -----------------------------
# 📘 OBTER ALUNO POR ID
# -----------------------------
@aluno_bp.route("/<int:id>", methods=["GET"])
def obter_aluno(id):
    """
    Obtém um aluno pelo ID
    ---
    tags:
      - Alunos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Aluno encontrado
      404:
        description: Aluno não encontrado
    """
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404
    return jsonify(aluno.to_dict()), 200


# -----------------------------
# 📘 CRIAR NOVO ALUNO
# -----------------------------
@aluno_bp.route("/", methods=["POST"])
def criar_aluno():
    """
    Cria um novo aluno (média calculada automaticamente)
    ---
    tags:
      - Alunos
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome: {type: string, example: "João Silva"}
            idade: {type: integer, example: 17}
            turma_id: {type: integer, example: 1}
            data_nascimento: {type: string, format: date, example: "2008-05-10"}
            nota_primeiro_semestre: {type: number, format: float, example: 7.5}
            nota_segundo_semestre: {type: number, format: float, example: 8.0}
    responses:
      201:
        description: Aluno criado com sucesso (média calculada)
        examples:
          application/json: {
              "id": 3,
              "nome": "João Silva",
              "idade": 17,
              "turma_id": 1,
              "data_nascimento": "2008-05-10",
              "nota_primeiro_semestre": 7.5,
              "nota_segundo_semestre": 8.0,
              "media_final": 7.75
          }
    """
    data = request.get_json()
    try:
        # Verifica se a turma existe antes de criar o aluno
        turma_id = data.get("turma_id")
        if not turma_id or not Turma.query.get(turma_id):
            return jsonify({"erro": "Turma não encontrada"}), 404

        data_nascimento = None
        if data.get("data_nascimento"):
            data_nascimento = datetime.strptime(data["data_nascimento"], "%Y-%m-%d").date()

        novo_aluno = Aluno(
            nome=data.get("nome"),
            idade=data.get("idade"),
            turma_id=turma_id,
            data_nascimento=data_nascimento,
            nota_primeiro_semestre=data.get("nota_primeiro_semestre"),
            nota_segundo_semestre=data.get("nota_segundo_semestre")
        )

        # ✅ Calcula automaticamente a média antes de salvar
        novo_aluno.calcular_media()

        db.session.add(novo_aluno)
        db.session.commit()
        return jsonify(novo_aluno.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500


# -----------------------------
# 📘 ATUALIZAR ALUNO
# -----------------------------
@aluno_bp.route("/<int:id>", methods=["PUT"])
def atualizar_aluno(id):
    """
    Atualiza um aluno existente (média recalculada automaticamente)
    ---
    tags:
      - Alunos
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
            nome: {type: string, example: "João Atualizado"}
            idade: {type: integer, example: 18}
            turma_id: {type: integer, example: 2}
            data_nascimento: {type: string, format: date, example: "2007-04-12"}
            nota_primeiro_semestre: {type: number, format: float, example: 8.5}
            nota_segundo_semestre: {type: number, format: float, example: 9.0}
    responses:
      200:
        description: Aluno atualizado com sucesso
    """
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    data = request.get_json()

    # Verifica se a turma existe antes de atualizar o aluno
    turma_id = data.get("turma_id", aluno.turma_id)
    if not Turma.query.get(turma_id):
        return jsonify({"erro": "Turma não encontrada"}), 404

    aluno.nome = data.get("nome", aluno.nome)
    aluno.idade = data.get("idade", aluno.idade)
    aluno.turma_id = turma_id

    if data.get("data_nascimento"):
        aluno.data_nascimento = datetime.strptime(data["data_nascimento"], "%Y-%m-%d").date()

    aluno.nota_primeiro_semestre = data.get("nota_primeiro_semestre", aluno.nota_primeiro_semestre)
    aluno.nota_segundo_semestre = data.get("nota_segundo_semestre", aluno.nota_segundo_semestre)

    # ✅ Recalcula a média automaticamente após atualização
    aluno.calcular_media()

    db.session.commit()
    return jsonify(aluno.to_dict()), 200


# -----------------------------
# 📘 DELETAR ALUNO
# -----------------------------
@aluno_bp.route("/<int:id>", methods=["DELETE"])
def deletar_aluno(id):
    """
    Deleta um aluno
    ---
    tags:
      - Alunos
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Aluno excluído com sucesso
        examples:
          application/json: { "mensagem": "Aluno excluído com sucesso" }
      404:
        description: Aluno não encontrado
    """
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    db.session.delete(aluno)
    db.session.commit()
    return jsonify({"mensagem": "Aluno excluído com sucesso"}), 200