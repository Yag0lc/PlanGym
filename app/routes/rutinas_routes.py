from flask import Blueprint, request, session, jsonify
from services.rutina_service import (
    crearRutina,
    obtenerRutinas,
    actualizarRutina,
    activarRutina,
    eliminarRutina,
)

rutinas_bp = Blueprint('rutinas_bp', __name__, url_prefix='/rutinas')


def rutinaAJson(rutina):
    return {
        'id': rutina.id,
        'nombre': rutina.nombre,
        'activa': rutina.activa,
        'ejercicios': [
            {
                'nombre': e.nombre,
                'dia_semana': e.dia_semana
            }
            for e in rutina.ejercicios
        ]
    }


@rutinas_bp.route('/', methods=['GET'])
def listar():
    if 'usuario_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401

    rutinas = obtenerRutinas(session['usuario_id'])
    resultado = []
    for r in rutinas:
        resultado.append(rutinaAJson(r))
    return jsonify(resultado)


@rutinas_bp.route('/crear', methods=['POST'])
def crear():
    if 'usuario_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401

    datos = request.get_json(silent=True) or {}
    nombre = datos.get('nombre', '').strip()
    ejercicios = datos.get('ejercicios', [])

    rutina = crearRutina(nombre, session['usuario_id'], ejercicios)

    if rutina is None:
        return jsonify({'error': 'Datos inválidos'}), 400

    return jsonify(rutinaAJson(rutina)), 201


@rutinas_bp.route('/actualizar/<int:id_rutina>', methods=['PUT'])
def actualizar(id_rutina):
    if 'usuario_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401

    datos = request.get_json(silent=True) or {}
    nombre = datos.get('nombre', '').strip()
    ejercicios = datos.get('ejercicios', [])

    rutina = actualizarRutina(id_rutina, session['usuario_id'], nombre, ejercicios)

    if rutina is None:
        return jsonify({'error': 'Rutina no encontrada o datos invalidos'}), 400

    return jsonify(rutinaAJson(rutina))


@rutinas_bp.route('/activar/<int:id_rutina>', methods=['POST'])
def activar(id_rutina):
    if 'usuario_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401

    resultado = activarRutina(id_rutina, session['usuario_id'])
    if resultado:
        return jsonify({'ok': True})
    return jsonify({'error': 'Rutina no encontrada'}), 404


@rutinas_bp.route('/eliminar/<int:id_rutina>', methods=['POST'])
def eliminar(id_rutina):
    if 'usuario_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401

    resultado = eliminarRutina(id_rutina, session['usuario_id'])
    if resultado:
        return jsonify({'ok': True})
    return jsonify({'error': 'Rutina no encontrada'}), 404
