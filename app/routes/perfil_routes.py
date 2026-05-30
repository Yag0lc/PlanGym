from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from services.perfil_service import obtenerPerfil, actualizarPassword, actualizarNombre

perfil_bp = Blueprint('perfil_bp', __name__, url_prefix='/perfil') 



@perfil_bp.route('/')
def perfil():
    if 'usuario_id' not in session:
        return redirect(url_for('home'))

    usuario, stats = obtenerPerfil(session['usuario_id'])
    return render_template('perfil.html', usuario=usuario, stats=stats)


@perfil_bp.route('/cambiar-nombre', methods=['POST'])
def cambiar_nombre():
    if 'usuario_id' not in session:
        return redirect(url_for('home'))

    nuevo_nombre = request.form.get('nombre', '').strip()
    if actualizarNombre(session['usuario_id'], nuevo_nombre):
        session['usuario_nombre'] = nuevo_nombre
        flash('Nombre actualizado correctamente.', 'success')
    else:
        flash('El nombre debe tener al menos 3 caracteres.', 'error')
    return redirect(url_for('perfil_bp.perfil'))


@perfil_bp.route('/cambiar-password', methods=['POST'])
def cambiar_password():
    if 'usuario_id' not in session:
        return redirect(url_for('home'))

    nueva_password = request.form.get('password', '')
    if actualizarPassword(session['usuario_id'], nueva_password):
        flash('Contraseña actualizada correctamente.', 'success')
    else:
        flash('La contraseña debe tener al menos 6 caracteres.', 'error')
    return redirect(url_for('perfil_bp.perfil'))
