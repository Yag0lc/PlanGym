

function mostrarPagina(id, boton) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

    document.getElementById(`page-${id}`).classList.add('active');
    boton.classList.add('active');

    document.getElementById('page-title').textContent =
        id.charAt(0).toUpperCase() + id.slice(1);

    if (id === 'ejercicios') {
        cargarCategorias();
        cargarEjercicios();
    }
}


