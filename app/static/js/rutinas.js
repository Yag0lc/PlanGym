// ===== RUTINAS =====

const ejerciciosDisponibles = [
    "Press banca",
    "Dominadas",
    "Sentadilla",
    "Peso muerto",
    "Remo barra",
    "Press militar",
    "Curl biceps",
    "Plancha"
];

let rutinas = [];

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

    const ejerciciosSeleccionados = [
        ...document.querySelectorAll('.ej-chip.selected')
    ].map(chip => chip.textContent);

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

function renderRutinas() {
    const cont = document.getElementById('rutinas-container');

    cont.innerHTML = '';

    rutinas.forEach(rutina => {
        const div = document.createElement('div');

        div.classList.add('rutina-card');

        if (rutina.activa) {
            div.classList.add('active-rutina');
        }

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

                <button class="danger" onclick="eliminarRutina(${rutina.id})">
                    Eliminar
                </button>
            </div>
        `;

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

    ejerciciosDisponibles.forEach(ej => {
        const chip = document.createElement('div');

        chip.classList.add('ej-chip');
        chip.textContent = ej;

        chip.onclick = () => {
            chip.classList.toggle('selected');
        };

        cont.appendChild(chip);
    });
}

renderEjerciciosSelector();
cargarRutinas();
