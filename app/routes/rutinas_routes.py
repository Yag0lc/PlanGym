from flask import Blueprint, request, session, redirect, url_for, jsonify
from services.rutina_service import crearRutina, obtenerRutinas, activarRutina, eliminarRutina

rutinas_bp = Blueprint('rutinas_bp', __name__, url_prefix='/rutinas')


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario_id' not in session:
            return jsonify({'error': 'No autenticado'}), 401
        return f(*args, **kwargs)
    return decorated


@rutinas_bp.route('/', methods=['GET'])
@login_required
def listar():
    rutinas = obtenerRutinas(session['usuario_id'])
    resultado = []
    for r in rutinas:
        resultado.append({
            'id': r.id,
            'nombre': r.nombre,
            'activa': r.activa,
            'ejercicios': [e.nombre for e in r.ejercicios]
        })
    return jsonify(resultado)


@rutinas_bp.route('/crear', methods=['POST'])
@login_required
def crear():
    datos = request.get_json()
    nombre = datos.get('nombre', '').strip()
    ejercicios = datos.get('ejercicios', [])

    rutina = crearRutina(nombre, session['usuario_id'], ejercicios)

    if rutina is None:
        return jsonify({'error': 'Datos inválidos'}), 400

    return jsonify({
        'id': rutina.id,
        'nombre': rutina.nombre,
        'activa': rutina.activa,
        'ejercicios': [e.nombre for e in rutina.ejercicios]
    }), 201


@rutinas_bp.route('/activar/<int:id_rutina>', methods=['POST'])
@login_required
def activar(id_rutina):
    activarRutina(id_rutina, session['usuario_id'])
    return jsonify({'ok': True})


@rutinas_bp.route('/eliminar/<int:id_rutina>', methods=['POST'])
@login_required
def eliminar(id_rutina):
    resultado = eliminarRutina(id_rutina, session['usuario_id'])
    if resultado:
        return jsonify({'ok': True})
    return jsonify({'error': 'Rutina no encontrada'}), 404