// ===== RUTINAS =====

let rutinas = [];
let rutinaEditandoId = null;
let ejerciciosParaRutina = cargarEjerciciosParaRutina();

function cargarEjerciciosParaRutina() {
    const datos = localStorage.getItem('plangym_ejercicios_rutina');
    return datos ? JSON.parse(datos) : [];
}

function guardarEjerciciosParaRutina() {
    localStorage.setItem('plangym_ejercicios_rutina', JSON.stringify(ejerciciosParaRutina));
}

function ejercicioEstaSeleccionado(nombre) {
    return ejerciciosParaRutina.includes(nombre);
}

function cambiarEjercicioParaRutina(nombre) {
    if (ejercicioEstaSeleccionado(nombre)) {
        ejerciciosParaRutina = ejerciciosParaRutina.filter(ej => ej !== nombre);
    } else {
        ejerciciosParaRutina.push(nombre);
    }

    guardarEjerciciosParaRutina();
    renderEjerciciosSelector();

    if (typeof cargarEjercicios === 'function') {
        cargarEjercicios();
    }
}

async function cargarRutinas() {
    const resp = await fetch('/rutinas/');
    rutinas = await resp.json();

    renderRutinas();
    actualizarEstadisticasInicio();
}

async function crearRutina() {
    const nombreInput = document.getElementById('nombre-rutina');
    const nombre = nombreInput.value.trim();

    if (!nombre) return;

    const ejerciciosSeleccionados = [...ejerciciosParaRutina];

    if (ejerciciosSeleccionados.length === 0) return;

    const resp = await fetch('/rutinas/crear', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nombre,
            ejercicios: ejerciciosSeleccionados
        })
    });

    if (resp.ok) {
        nombreInput.value = '';
        ejerciciosParaRutina = [];
        guardarEjerciciosParaRutina();
        renderEjerciciosSelector();
        await cargarRutinas();
    }
}

async function activarRutina(id) {
    await fetch(`/rutinas/activar/${id}`, {
        method: 'POST'
    });

    await cargarRutinas();
}

async function eliminarRutina(id) {
    await fetch(`/rutinas/eliminar/${id}`, {
        method: 'POST'
    });

    await cargarRutinas();
}

function editarRutina(id) {
    rutinaEditandoId = id;
    renderRutinas();
}

function cancelarEdicionRutina() {
    rutinaEditandoId = null;
    renderRutinas();
}

async function guardarRutina(id) {
    const nombreInput = document.getElementById(`editar-rutina-nombre-${id}`);
    const nombre = nombreInput.value.trim();
    const ejercicios = [
        ...document.querySelectorAll(`.editar-ejercicio-${id}.selected`)
    ].map(chip => chip.textContent);

    if (!nombre || ejercicios.length === 0) return;

    const resp = await fetch(`/rutinas/actualizar/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nombre,
            ejercicios
        })
    });

    if (resp.ok) {
        rutinaEditandoId = null;
        await cargarRutinas();
    }
}

function renderEditorRutina(rutina) {
    const opciones = [...new Set([...ejerciciosParaRutina, ...rutina.ejercicios])];

    const chips = opciones.map(ej => {
        const selected = rutina.ejercicios.includes(ej) ? 'selected' : '';
        return `<div class="ej-chip editar-ejercicio-${rutina.id} ${selected}" onclick="this.classList.toggle('selected')">${ej}</div>`;
    }).join('');

    return `
        <div class="rutina-editor">
            <input type="text" id="editar-rutina-nombre-${rutina.id}" value="${rutina.nombre}">
            <div class="chips">${chips}</div>
            <div class="actions">
                <button onclick="guardarRutina(${rutina.id})">Guardar</button>
                <button class="secondary" onclick="cancelarEdicionRutina()">Cancelar</button>
            </div>
        </div>
    `;
}

function renderRutinas() {
    const cont = document.getElementById('rutinas-container');

    cont.innerHTML = '';

    rutinas.forEach(rutina => {
        const div = document.createElement('div');

        div.classList.add('rutina-card');

        if (rutina.activa) {
            div.classList.add('active-rutina');
        }

        if (rutinaEditandoId === rutina.id) {
            div.innerHTML = renderEditorRutina(rutina);
        } else {
            div.innerHTML = `
            <div>
                <h4>
                    ${rutina.nombre}
                    ${rutina.activa ? '<span>ACTIVA</span>' : ''}
                </h4>

                <p>${rutina.ejercicios.join(', ')}</p>
            </div>

            <div class="actions">
                ${
                    !rutina.activa
                        ? `<button onclick="activarRutina(${rutina.id})">Activar</button>`
                        : ''
                }

                <button class="secondary" onclick="editarRutina(${rutina.id})">
                    Editar
                </button>

                <button class="danger" onclick="eliminarRutina(${rutina.id})">
                    Eliminar
                </button>
            </div>
        `;
        }

        cont.appendChild(div);
    });
}

async function actualizarEstadisticasInicio() {
    const activa = rutinas.find(r => r.activa);

    document.getElementById('rutina-activa-nombre').textContent =
        activa ? activa.nombre : 'Ninguna';

    const totalRutinas = document.getElementById('total-rutinas');
    if (totalRutinas) {
        totalRutinas.textContent = rutinas.length;
    }

    const resp = await fetch(`/calendario/?mes=${mesActual}&anio=${anoActual}`);
    const dias = await resp.json();

    document.getElementById('total-dias').textContent = dias.length;
}

function renderEjerciciosSelector() {
    const cont = document.getElementById('ejercicios-selector');

    cont.innerHTML = '';

    if (ejerciciosParaRutina.length === 0) {
        cont.innerHTML = '<p class="loading-text">Selecciona ejercicios desde el catalogo.</p>';
        return;
    }

    ejerciciosParaRutina.forEach(ej => {
        const chip = document.createElement('div');

        chip.classList.add('ej-chip', 'selected');
        chip.textContent = ej;

        chip.onclick = () => {
            cambiarEjercicioParaRutina(ej);
        };

        cont.appendChild(chip);
    });
}

renderEjerciciosSelector();
cargarRutinas();
