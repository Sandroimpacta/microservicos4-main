# app/utils/response.py
from flask import jsonify

def success_response(data, message="Sucesso"):
    return jsonify({"status": "success", "message": message, "data": data}), 200

def error_response(message, code=400):
    return jsonify({"status": "error", "message": message}), code