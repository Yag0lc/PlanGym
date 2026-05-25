// ===== NAVEGACION =====

function mostrarPagina(id, el) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

    document.getElementById(`page-${id}`).classList.add('active');
    el.classList.add('active');

    document.getElementById('page-title').textContent =
        id.charAt(0).toUpperCase() + id.slice(1);

    if (id === 'ejercicios') {
        cargarCategorias();
        cargarEjercicios();
    }
}
