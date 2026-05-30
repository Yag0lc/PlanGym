

let categoriaActual = null;

async function cargarCategorias() {
    const cont = document.getElementById('filtros-categorias');

    if (!cont || cont.children.length > 1) return;

    const resp = await fetch('/ejercicios/categorias');
    if (!resp.ok) return;

    const cats = await resp.json();

    cats.forEach(cat => {
        const btn = document.createElement('button');

        btn.className = 'filtro-btn';
        btn.textContent = cat.nombre;

        btn.onclick = () => {
            filtrarEjercicios(cat.id, btn);
        };

        cont.appendChild(btn);
    });
}

async function filtrarEjercicios(categoriaId, btn) {
    categoriaActual = categoriaId;

    document
        .querySelectorAll('.filtro-btn')
        .forEach(b => b.classList.remove('active'));

    btn.classList.add('active');

    await cargarEjercicios();
}

async function cargarEjercicios() {
    const grid = document.getElementById('ejercicios-grid');

    grid.innerHTML = '<p class="loading-text">Cargando...</p>';

    const url = categoriaActual
        ? `/ejercicios/?categoria=${categoriaActual}`
        : '/ejercicios/';

    const resp = await fetch(url);
    if (!resp.ok) {
        grid.innerHTML = '<p class="loading-text">No se pudieron cargar los ejercicios.</p>';
        return;
    }

    const lista = await resp.json();

    grid.innerHTML = '';

    if (!lista.length) {
        grid.innerHTML = '<p class="loading-text">No hay ejercicios.</p>';
        return;
    }

    lista.forEach(ej => {
        const card = document.createElement('div');
        const seleccionado = ejercicioEstaSeleccionado(ej.nombre);

        card.className = seleccionado ? 'ej-card selected' : 'ej-card';

        card.innerHTML = `
            <span class="ej-badge">${ej.categoria}</span>

            <h4>${ej.nombre}</h4>

            <p>
                ${
                    ej.descripcion
                        ? ej.descripcion.substring(0, 80) + '...'
                        : 'Sin descripcion'
                }
            </p>

            <button class="select-exercise-btn">
                ${seleccionado ? 'Quitar de rutina' : 'Anadir a rutina'}
            </button>
        `;

        card.onclick = () => abrirDetalle(ej.id);
        card.querySelector('.select-exercise-btn').onclick = (event) => {
            event.stopPropagation();
            cambiarEjercicioParaRutina(ej.nombre);
        };

        grid.appendChild(card);
    });
}

async function abrirDetalle(id) {
    const overlay = document.getElementById('modal-overlay');
    const content = document.getElementById('modal-content');

    overlay.classList.add('open');

    content.innerHTML = `
        <button class="modal-close" onclick="cerrarModal()">x</button>
        <p class="loading-text">Cargando...</p>
    `;

    const resp = await fetch(`/ejercicios/${id}`);
    const ej = await resp.json();
    const seleccionado = ejercicioEstaSeleccionado(ej.nombre);

    content.innerHTML = `
        <button class="modal-close" onclick="cerrarModal()">x</button>

        ${ej.imagen_url ? `<img src="${ej.imagen_url}" alt="${ej.nombre}">` : ''}

        <h2>${ej.nombre}</h2>

        <p class="modal-cat">${ej.categoria}</p>

        <p class="modal-desc">
            ${ej.descripcion || 'Sin descripcion disponible.'}
        </p>

        ${
            ej.musculos && ej.musculos.length
                ? `
                <div class="modal-musculos">
                    ${ej.musculos.map(m => `<span class="ej-badge">${m}</span>`).join('')}
                </div>
            `
                : ''
        }

        <button onclick='cambiarEjercicioParaRutina(${JSON.stringify(ej.nombre)}); cerrarModal();'>
            ${seleccionado ? 'Quitar de rutina' : 'Anadir a rutina'}
        </button>
    `;
}

function cerrarModal(e) {
    const overlay = document.getElementById('modal-overlay');

    if (!e || e.target === overlay) {
        overlay.classList.remove('open');
    }
}
