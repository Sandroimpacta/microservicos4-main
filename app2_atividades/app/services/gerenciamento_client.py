# 🧠 1️⃣ Serviço de Validação – APP2 (Atividades)

# 📁 app2_atividades/app/services/gerenciamento_client.py

import requests

GERENCIAMENTO_URL = "http://app1_gerenciamento:5000"  # nome do serviço no docker-compose

def get_aluno_by_id(aluno_id):
    """
    Valida se um aluno existe no microserviço de Gerenciamento.
    """
    try:
        response = requests.get(f"{GERENCIAMENTO_URL}/alunos/{aluno_id}", timeout=5)
        response.raise_for_status()
        return response.json(), 200

    except requests.exceptions.Timeout:
        return {"erro": "Serviço de gerenciamento demorou para responder."}, 504
    except requests.exceptions.ConnectionError:
        return {"erro": "Falha ao conectar ao serviço de gerenciamento."}, 503
    except requests.exceptions.HTTPError:
        return {"erro": f"Aluno não encontrado (HTTP {response.status_code})."}, response.status_code
    except Exception as e:
        return {"erro": f"Erro inesperado: {str(e)}"}, 500


def get_professor_by_id(professor_id):
    """
    Valida se um professor existe no microserviço de Gerenciamento.
    """
    try:
        response = requests.get(f"{GERENCIAMENTO_URL}/professores/{professor_id}", timeout=5)
        response.raise_for_status()
        return response.json(), 200

    except requests.exceptions.Timeout:
        return {"erro": "Serviço de gerenciamento demorou para responder."}, 504
    except requests.exceptions.ConnectionError:
        return {"erro": "Falha ao conectar ao serviço de gerenciamento."}, 503
    except requests.exceptions.HTTPError:
        return {"erro": f"Professor não encontrado (HTTP {response.status_code})."}, response.status_code
    except Exception as e:
        return {"erro": f"Erro inesperado: {str(e)}"}, 500
