from flask import Blueprint, session, jsonify, request
from services.calendario_service import obtenerDias, marcarDia, desmarcarDia

calendario_bp = Blueprint('calendario_bp', __name__, url_prefix='/calendario')


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario_id' not in session:
            return jsonify({'error': 'No autenticado'}), 401
        return f(*args, **kwargs)
    return decorated


@calendario_bp.route('/', methods=['GET'])
@login_required
def listar():
    mes = request.args.get('mes', type=int)
    anio = request.args.get('anio', type=int)
    dias = obtenerDias(session['usuario_id'], mes, anio)
    return jsonify(dias)


@calendario_bp.route('/marcar', methods=['POST'])
@login_required
def marcar():
    datos = request.get_json()
    dia = datos.get('dia')
    mes = datos.get('mes')
    anio = datos.get('anio')
    marcarDia(session['usuario_id'], dia, mes, anio)
    return jsonify({'ok': True})


@calendario_bp.route('/desmarcar', methods=['POST'])
@login_required
def desmarcar():
    datos = request.get_json()
    dia = datos.get('dia')
    mes = datos.get('mes')
    anio = datos.get('anio')
    desmarcarDia(session['usuario_id'], dia, mes, anio)
    return jsonify({'ok': True})