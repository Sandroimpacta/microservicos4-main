# 🧩 Sistema Educacional - Microserviços Flask com Swagger e SQLite

Este projeto implementa uma arquitetura de **microserviços Flask**, com três aplicações independentes que se comunicam via rede Docker.  
Cada microserviço possui seu próprio banco **SQLite persistente**, documentação via **Swagger (Flasgger)** e rotas CRUD completas.

---

## 🧱 Estrutura dos Microserviços

| Microserviço | Porta | Descrição | Banco de Dados |
|---------------|--------|------------|----------------|
| **Gerenciamento** | `5000` | Gerencia Professores, Turmas e Alunos | `gerenciamento.db` |
| **Reservas** | `5001` | Gerencia Reservas de Salas e Laboratórios | `reservas.db` |
| **Atividades** | `5002` | Gerencia Atividades e Notas dos Alunos | `atividades.db` |

---

## 🚀 Tecnologias Utilizadas

- **Python 3.10+**
- **Flask**
- **Flask-SQLAlchemy**
- **Flasgger (Swagger UI)**
- **SQLite**
- **Docker / Docker Compose**

---

## 📂 Estrutura de Pastas

microservicos1/
│
├── gerenciamento/
│ ├── app/
│ │ ├── init.py
│ │ ├── main.py
│ │ ├── database.py
│ │ ├── models/
│ │ │ ├── professor_model.py
│ │ │ ├── turma_model.py
│ │ │ └── aluno_model.py
│ │ └── routes/
│ │ ├── professor_routes.py
│ │ ├── turma_routes.py
│ │ └── aluno_routes.py
│ ├── Dockerfile
│ └── requirements.txt
│
├── reservas/
│ ├── app/
│ │ ├── init.py
│ │ ├── main.py
│ │ ├── database.py
│ │ └── routes/
│ │ └── reserva_routes.py
│ ├── Dockerfile
│ └── requirements.txt
│
├── atividades/
│ ├── app/
│ │ ├── init.py
│ │ ├── main.py
│ │ ├── database.py
│ │ ├── models/
│ │ │ ├── atividade_model.py
│ │ │ └── nota_model.py
│ │ └── routes/
│ │ ├── atividade_routes.py
│ │ └── nota_routes.py
│ ├── Dockerfile
│ └── requirements.txt
│
├── docker-compose.yml
└── README.md

---

## ⚙️ Como Executar o Projeto

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/seuusuario/microservicos1.git
cd microservicos1

SWAGGER = docs
http://127.0.0.1:5000/apidocs/ = APP1_Gerenciamento
http://127.0.0.1:5001/apidocs/ = APP3_Reservas
http://127.0.0.1:5002/apidocs/ = APP2_Atividades