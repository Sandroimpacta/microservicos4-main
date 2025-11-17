# app3_reservas/app/routes/reserva_routes.py
from flask import Blueprint, jsonify, request
from app.database import db
from app.models.reserva_model import Reserva
from datetime import date
import requests
import time
from app.controllers.reserva_controller import criar_reserva as criar_reserva_controller

reserva_bp = Blueprint("reserva_bp", __name__)

# URL base do app1-gerenciamento
GERENCIAMENTO_URL = "http://app1-gerenciamento:5000"

# Função de verificação de turma
def verificar_turma(turma_id, retries=3, delay=1):
    """
    Verifica se a turma existe no microserviço de gerenciamento.
    Retorna tuple (resposta_json, status_code)
    Tenta algumas vezes antes de desistir.
    """
    url = f"{GERENCIAMENTO_URL}/turmas/{turma_id}"
    for attempt in range(1, retries + 1):
        try:
            print(f"[verificar_turma] Tentando acessar {url} (tentativa {attempt})")
            response = requests.get(url, timeout=3)
            print(f"[verificar_turma] Status: {response.status_code}, Body: {response.text}")
            if response.status_code == 404:
                return {"erro": f"Turma com ID {turma_id} não encontrada."}, 404
            response.raise_for_status()
            return response.json(), 200
        except requests.exceptions.Timeout:
            print(f"[verificar_turma] Timeout ao acessar {url} (tentativa {attempt})")
            if attempt == retries:
                return {"erro": "Tempo de resposta excedido no serviço de gerenciamento."}, 504
            time.sleep(delay)
        except requests.exceptions.ConnectionError as e:
            print(f"[verificar_turma] ConnectionError ao acessar {url}: {e} (tentativa {attempt})")
            if attempt == retries:
                return {"erro": "Serviço de gerenciamento indisponível."}, 503
            time.sleep(delay)
        except requests.exceptions.HTTPError as e:
            print(f"[verificar_turma] HTTPError ao acessar {url}: {e} (tentativa {attempt})")
            return {"erro": f"Erro ao buscar turma: {str(e)}"}, response.status_code
        except Exception as e:
            print(f"[verificar_turma] Erro inesperado ao acessar {url}: {e} (tentativa {attempt})")
            if attempt == retries:
                return {"erro": f"Erro interno: {str(e)}"}, 500
            time.sleep(delay)

# Funções de verificação para aluno e professor

def verificar_aluno(aluno_id):
    url = f"{GERENCIAMENTO_URL}/alunos/{aluno_id}"
    try:
        print(f"[verificar_aluno] GET {url}")
        response = requests.get(url, timeout=3)
        print(f"[verificar_aluno] Response: {response.status_code} {response.text}")
        if response.status_code == 404:
            return {"erro": f"Aluno com ID {aluno_id} não encontrado."}, 404
        response.raise_for_status()
        return response.json(), 200
    except requests.exceptions.Timeout as e:
        print(f"[verificar_aluno] Timeout: {e}")
        return {"erro": "Tempo de resposta excedido no serviço de gerenciamento."}, 504
    except requests.exceptions.ConnectionError as e:
        print(f"[verificar_aluno] ConnectionError: {e}")
        return {"erro": "Serviço de gerenciamento indisponível."}, 503
    except requests.exceptions.HTTPError as e:
        print(f"[verificar_aluno] HTTPError: {e}")
        return {"erro": f"Erro ao buscar aluno: {str(e)}"}, response.status_code
    except Exception as e:
        print(f"[verificar_aluno] Exception: {e}")
        return {"erro": f"Erro interno: {str(e)}"}, 500

def verificar_professor(professor_id):
    url = f"{GERENCIAMENTO_URL}/professores/{professor_id}"
    try:
        print(f"[verificar_professor] GET {url}")
        response = requests.get(url, timeout=3)
        print(f"[verificar_professor] Response: {response.status_code} {response.text}")
        if response.status_code == 404:
            return {"erro": f"Professor com ID {professor_id} não encontrado."}, 404
        response.raise_for_status()
        return response.json(), 200
    except requests.exceptions.Timeout as e:
        print(f"[verificar_professor] Timeout: {e}")
        return {"erro": "Tempo de resposta excedido no serviço de gerenciamento."}, 504
    except requests.exceptions.ConnectionError as e:
        print(f"[verificar_professor] ConnectionError: {e}")
        return {"erro": "Serviço de gerenciamento indisponível."}, 503
    except requests.exceptions.HTTPError as e:
        print(f"[verificar_professor] HTTPError: {e}")
        return {"erro": f"Erro ao buscar professor: {str(e)}"}, response.status_code
    except Exception as e:
        print(f"[verificar_professor] Exception: {e}")
        return {"erro": f"Erro interno: {str(e)}"}, 500


# 📘 LISTAR TODAS AS RESERVAS
@reserva_bp.route("/", methods=["GET"])
def listar_reservas():
    """
    Lista todas as reservas
    ---
    tags:
      - Reservas
    responses:
      200:
        description: Lista de reservas
        schema:
          type: array
          items:
            type: object
    """
    reservas = Reserva.query.all()
    return jsonify([r.to_dict() for r in reservas]), 200


# 📘 OBTER RESERVA POR ID
@reserva_bp.route("/<int:id>", methods=["GET"])
def obter_reserva(id):
    """
    Obtém uma reserva pelo ID
    ---
    tags:
      - Reservas
    parameters:
      - name: id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Reserva encontrada
      404:
        description: Reserva não encontrada
    """
    reserva = Reserva.query.get(id)
    if not reserva:
        return jsonify({"erro": "Reserva não encontrada"}), 404
    return jsonify(reserva.to_dict()), 200


# 📘 CRIAR NOVA RESERVA
@reserva_bp.route("/", methods=["POST"])
def criar_reserva():
    """
    Cria uma nova reserva
    ---
    tags:
      - Reservas
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            aluno_id: {type: integer}
            turma_id: {type: integer}
            professor_id: {type: integer}
            num_sala: {type: integer}
            lab: {type: boolean}
            data: {type: string, format: date}
    responses:
      201:
        description: Reserva criada com sucesso
      404:
        description: Aluno, Turma ou Professor não existe
    """
    try:
        data_json = request.get_json()
        result = criar_reserva_controller(data_json)
        # Se o controller retornar tuple (dict, status), repasse
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
        # Se retornar só dict, assuma sucesso
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500


# 📘 ATUALIZAR RESERVA
@reserva_bp.route("/<int:id>", methods=["PUT"])
def atualizar_reserva(id):
    """
    Atualiza uma reserva existente
    ---
    tags:
      - Reservas
    parameters:
      - name: id
        in: path
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            aluno_id: {type: integer}
            turma_id: {type: integer}
            professor_id: {type: integer}
            num_sala: {type: integer}
            lab: {type: boolean}
            data: {type: string, format: date}
    responses:
      200:
        description: Reserva atualizada com sucesso
      404:
        description: Reserva, aluno, turma ou professor não encontrada
    """
    reserva = Reserva.query.get(id)
    if not reserva:
        return jsonify({"erro": "Reserva não encontrada"}), 404

    try:
        data_json = request.get_json()
        reserva.num_sala = data_json.get("num_sala", reserva.num_sala)
        reserva.lab = data_json.get("lab", reserva.lab)

        if "data" in data_json and data_json["data"]:
            reserva.data = date.fromisoformat(data_json["data"])

        # ✅ Verifica turma se enviada
        if "turma_id" in data_json:
            turma_id = data_json["turma_id"]
            turma_resp, status = verificar_turma(turma_id)
            if status != 200:
                return jsonify(turma_resp), status
            reserva.turma_id = turma_id

        # ✅ Verifica aluno se enviado
        if "aluno_id" in data_json:
            aluno_id = data_json["aluno_id"]
            aluno_resp, status = verificar_aluno(aluno_id)
            if status != 200:
                return jsonify(aluno_resp), status
            reserva.aluno_id = aluno_id

        # ✅ Verifica professor se enviado
        if "professor_id" in data_json:
            professor_id = data_json["professor_id"]
            prof_resp, status = verificar_professor(professor_id)
            if status != 200:
                return jsonify(prof_resp), status
            reserva.professor_id = professor_id

        db.session.commit()
        return jsonify(reserva.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        print(f"[atualizar_reserva] Exception: {e}")
        return jsonify({"erro": str(e)}), 500


# 📘 DELETAR RESERVA
@reserva_bp.route("/<int:id>", methods=["DELETE"])
def deletar_reserva(id):
    """
    Deleta uma reserva existente
    ---
    tags:
      - Reservas
    parameters:
      - name: id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Reserva excluída com sucesso
      404:
        description: Reserva não encontrada
    """
    reserva = Reserva.query.get(id)
    if not reserva:
        return jsonify({"erro": "Reserva não encontrada"}), 404

    db.session.delete(reserva)
    db.session.commit()
    return jsonify({"mensagem": "Reserva excluída com sucesso"}), 200
