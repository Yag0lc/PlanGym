from flask import Blueprint, request, session, redirect, url_for, flash
from services.usuario_service import registrarUsuario, comprobarUsuario

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    nombre = request.form.get('nombre', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')

    if not nombre or not email or not password:
        flash('Todos los campos son obligatorios.', 'error')
        return redirect(url_for('home'))

    if len(password) < 6:
        flash('La contraseña debe tener al menos 6 caracteres.', 'error')
        return redirect(url_for('home'))

    usuario = registrarUsuario(nombre, email, password)

    if usuario is None:
        flash('Este email ya está registrado.', 'error')
        return redirect(url_for('home'))

    session['usuario_id'] = usuario.id
    session['usuario_nombre'] = usuario.nombre

    return redirect(url_for('dashboard'))


@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')

    if not email or not password:
        flash('Introduce email y contraseña.', 'error')
        return redirect(url_for('home'))

    usuario = comprobarUsuario(email, password)

    if not usuario:
        flash('Email o contraseña incorrectos.', 'error')
        return redirect(url_for('home'))

    session['usuario_id'] = usuario.id
    session['usuario_nombre'] = usuario.nombre

    return redirect(url_for('dashboard'))


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))