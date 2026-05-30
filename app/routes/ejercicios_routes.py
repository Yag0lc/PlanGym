from flask import Blueprint, jsonify, request, session
from services.ejercicios_service import listarEjercicios, detalleEjercicio, CATEGORIAS

ejercicios_bp = Blueprint('ejercicios_bp', __name__, url_prefix='/ejercicios')


@ejercicios_bp.route('/categorias', methods=['GET'])
def categorias():
    if 'usuario_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401

    return jsonify([
        {'id': k, 'nombre': v} for k, v in CATEGORIAS.items()
    ])


@ejercicios_bp.route('/', methods=['GET'])
def listar():
    if 'usuario_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401

    categoria_id = request.args.get('categoria', type=int)
    pagina = request.args.get('pagina', 1, type=int)
    ejercicios = listarEjercicios(categoria_id=categoria_id, pagina=pagina)
    return jsonify(ejercicios)


@ejercicios_bp.route('/<int:ejercicio_id>', methods=['GET'])
def detalle(ejercicio_id):
    if 'usuario_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401

    ej = detalleEjercicio(ejercicio_id)
    if ej is None:
        return jsonify({'error': 'Ejercicio no encontrado'}), 404
    return jsonify(ej)
