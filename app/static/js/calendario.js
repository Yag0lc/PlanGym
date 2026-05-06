// ===== DATOS =====
const ejerciciosDisponibles = [
    "Press banca", "Dominadas", "Sentadilla", "Peso muerto",
    "Remo barra", "Press militar", "Curl bíceps", "Plancha"
];

const nombresMeses = [
    "Enero","Febrero","Marzo","Abril","Mayo","Junio",
    "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
];

let rutinas = [];
let diasCompletados = [];
let diaSeleccionado = null;

const hoy = new Date();
let mesActual = hoy.getMonth() + 1;
let anioActual = hoy.getFullYear();


// ===== NAVEGACIÓN =====

function showPage(id, el) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.getElementById(`page-${id}`).classList.add('active');
    el.classList.add('active');
    document.getElementById('page-title').textContent =
        id.charAt(0).toUpperCase() + id.slice(1);
}


// ===== CALENDARIO =====

async function cargarDiasCompletados() {
    const resp = await fetch(`/calendario/?mes=${mesActual}&anio=${anioActual}`);
    diasCompletados = await resp.json();
    generateCalendar();
}

async function marcarDiaCompletado() {
    if (!diaSeleccionado) return;

    if (diasCompletados.includes(diaSeleccionado)) {
        await fetch('/calendario/desmarcar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ dia: diaSeleccionado, mes: mesActual, anio: anioActual })
        });
    } else {
        await fetch('/calendario/marcar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ dia: diaSeleccionado, mes: mesActual, anio: anioActual })
        });
    }

    await cargarDiasCompletados();
}

async function cambiarMes(direccion) {
    mesActual += direccion;
    if (mesActual > 12) { mesActual = 1; anioActual++; }
    if (mesActual < 1) { mesActual = 12; anioActual--; }
    diaSeleccionado = null;
    await cargarDiasCompletados();
}

function generateCalendar() {
    const grid = document.getElementById('calendar-grid');
    grid.innerHTML = '';

    document.getElementById('mes-anio').textContent =
        `${nombresMeses[mesActual - 1]} ${anioActual}`;

    const diasSemana = ["Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"];
    diasSemana.forEach(d => {
        const header = document.createElement('div');
        header.classList.add('day-header');
        header.textContent = d;
        grid.appendChild(header);
    });

    const primerDia = new Date(anioActual, mesActual - 1, 1).getDay();
    const offset = primerDia === 0 ? 6 : primerDia - 1;
    const diasEnMes = new Date(anioActual, mesActual, 0).getDate();

    for (let i = 0; i < offset; i++) {
        const empty = document.createElement('div');
        grid.appendChild(empty);
    }

    for (let i = 1; i <= diasEnMes; i++) {
        const day = document.createElement('div');
        day.classList.add('day');
        if (diasCompletados.includes(i)) day.classList.add('completed');
        if (i === diaSeleccionado) day.classList.add('active');
        day.textContent = i;
        day.onclick = () => seleccionarDia(i);
        grid.appendChild(day);
    }
}

function seleccionarDia(dia) {
    diaSeleccionado = dia;
    generateCalendar();
}


// ===== RUTINAS =====

async function cargarRutinas() {
    const resp = await fetch('/rutinas/');
    rutinas = await resp.json();
    renderRutinas();
    actualizarRutinaActivaInicio();
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
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre, ejercicios: ejerciciosSeleccionados })
    });

    if (resp.ok) {
        nombreInput.value = '';
        renderEjerciciosSelector();
        await cargarRutinas();
    }
}

async function activarRutina(id) {
    await fetch(`/rutinas/activar/${id}`, { method: 'POST' });
    await cargarRutinas();
}

async function eliminarRutina(id) {
    await fetch(`/rutinas/eliminar/${id}`, { method: 'POST' });
    await cargarRutinas();
}

function renderRutinas() {
    const cont = document.getElementById('rutinas-container');
    cont.innerHTML = '';

    rutinas.forEach(rutina => {
        const div = document.createElement('div');
        div.classList.add('rutina-card');
        if (rutina.activa) div.classList.add('active-rutina');

        div.innerHTML = `
            <div>
                <h4>
                    ${rutina.nombre}
                    ${rutina.activa ? '<span>ACTIVA</span>' : ''}
                </h4>
                <p>${rutina.ejercicios.join(', ')}</p>
            </div>
            <div class="actions">
                ${!rutina.activa
                    ? `<button onclick="activarRutina(${rutina.id})">Activar</button>`
                    : ''}
                <button class="danger" onclick="eliminarRutina(${rutina.id})">Eliminar</button>
            </div>
        `;

        cont.appendChild(div);
    });

    actualizarRutinaActivaInicio();
}

function actualizarRutinaActivaInicio() {
    const activa = rutinas.find(r => r.activa);
    document.getElementById('rutina-activa-nombre').textContent =
        activa ? activa.nombre : 'Ninguna';
}


// ===== EJERCICIOS =====

function renderEjerciciosSelector() {
    const cont = document.getElementById('ejercicios-selector');
    cont.innerHTML = '';

    ejerciciosDisponibles.forEach(ej => {
        const chip = document.createElement('div');
        chip.classList.add('ej-chip');
        chip.textContent = ej;
        chip.onclick = () => chip.classList.toggle('selected');
        cont.appendChild(chip);
    });

    document.getElementById('catalogo-ejercicios').innerHTML =
        ejerciciosDisponibles.map(ej => `<div class="ej-chip">${ej}</div>`).join('');
}


// ===== INICIO =====

generateCalendar();
renderEjerciciosSelector();
cargarRutinas();
cargarDiasCompletados();