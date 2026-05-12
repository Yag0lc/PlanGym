from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from services.perfil_service import obtenerPerfil, actualizarPassword, actualizarNombre

perfil_bp = Blueprint('perfil_bp', __name__, url_prefix='/perfil') 



def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated


@perfil_bp.route('/')
@login_required
def perfil():
    usuario, stats = obtenerPerfil(session['usuario_id'])
    return render_template('perfil.html', usuario=usuario, stats=stats)


@perfil_bp.route('/cambiar-nombre', methods=['POST'])
@login_required
def cambiar_nombre():
    nuevo_nombre = request.form.get('nombre', '').strip()
    if actualizarNombre(session['usuario_id'], nuevo_nombre):
        session['usuario_nombre'] = nuevo_nombre
        flash('Nombre actualizado correctamente.', 'success')
    else:
        flash('El nombre debe tener al menos 3 caracteres.', 'error')
    return redirect(url_for('perfil_bp.perfil'))


@perfil_bp.route('/cambiar-password', methods=['POST'])
@login_required
def cambiar_password():
    nueva_password = request.form.get('password', '')
    if actualizarPassword(session['usuario_id'], nueva_password):
        flash('Contraseña actualizada correctamente.', 'success')
    else:
        flash('La contraseña debe tener al menos 6 caracteres.', 'error')
    return redirect(url_for('perfil_bp.perfil'))