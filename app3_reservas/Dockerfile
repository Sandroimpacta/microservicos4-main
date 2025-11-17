# # reserva/app/Dockerfile
# 📗 reservas/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Atualiza pacotes e instala sqlite3
RUN apt-get update && apt-get install -y sqlite3
COPY . .
EXPOSE 5001
CMD ["python", "run.py"]
