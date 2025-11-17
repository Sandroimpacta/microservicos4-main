import requests
import logging

BASE_URL = "http://app1_gerenciamento:5000"  # Ajuste conforme Docker Compose
TIMEOUT = 3  # segundos

def check_aluno(aluno_id):
    try:
        r = requests.get(f"{BASE_URL}/alunos/{aluno_id}", timeout=TIMEOUT)
        return r.status_code == 200
    except requests.RequestException:
        return False

def check_turma(turma_id):
    try:
        r = requests.get(f"{BASE_URL}/turmas/{turma_id}", timeout=TIMEOUT)
        if r.status_code == 200:
            return True
        else:
            logging.warning(f"Turma {turma_id} não encontrada ou erro: status {r.status_code}")
            return False
    except requests.RequestException as e:
        logging.error(f"Erro ao verificar turma {turma_id}: {e}")
        return False

def check_professor(professor_id):
    try:
        r = requests.get(f"{BASE_URL}/professores/{professor_id}", timeout=TIMEOUT)
        if r.status_code == 200:
            return True
        else:
            logging.warning(f"Professor {professor_id} não encontrado ou erro: status {r.status_code}")
            return False
    except requests.RequestException as e:
        logging.error(f"Erro ao verificar professor {professor_id}: {e}")
        return False