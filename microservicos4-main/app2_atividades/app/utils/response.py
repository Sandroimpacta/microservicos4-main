# atividades/app/utils/response.py
from flask import jsonify

def response(data=None, message='', status=200):
    return jsonify({'status': status, 'message': message, 'data': data}), status