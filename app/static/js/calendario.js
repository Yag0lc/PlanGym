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
let anoActual = hoy.getFullYear();


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
    const resp = await fetch(`/calendario/?mes=${mesActual}&anio=${anoActual}`);
    diasCompletados = await resp.json();
    generateCalendar();
}

async function marcarDiaCompletado() {
    if (!diaSeleccionado) return;

    if (diasCompletados.includes(diaSeleccionado)) {
        await fetch('/calendario/desmarcar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ dia: diaSeleccionado, mes: mesActual, anio: anoActual })
        });
    } else {
        await fetch('/calendario/marcar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ dia: diaSeleccionado, mes: mesActual, anio: anoActual })
        });
    }

    await cargarDiasCompletados();
}

async function cambiarMes(direccion) {
    mesActual += direccion;
    if (mesActual > 12) { mesActual = 1; anoActual++; }
    if (mesActual < 1) { mesActual = 12; anoActual--; }
    diaSeleccionado = null;
    await cargarDiasCompletados();
}

function generateCalendar() {
    const grid = document.getElementById('calendar-grid');
    grid.innerHTML = '';

    document.getElementById('mes-anio').textContent =
        `${nombresMeses[mesActual - 1]} ${anoActual}`;

    const diasSemana = ["Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"];
    diasSemana.forEach(d => {
        const header = document.createElement('div');
        header.classList.add('day-header');
        header.textContent = d;
        grid.appendChild(header);
    });

    const primerDia = new Date(anoActual, mesActual - 1, 1).getDay();
    const offset = primerDia === 0 ? 6 : primerDia - 1;
    const diasEnMes = new Date(anoActual, mesActual, 0).getDate();

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

async function actualizarEstadisticasInicio() {
    const activa = rutinas.find(r => r.activa);
    document.getElementById('rutina-activa-nombre').textContent =
        activa ? activa.nombre : 'Ninguna';

    const totalRutinas = document.getElementById('total-rutinas');
    if (totalRutinas) totalRutinas.textContent = rutinas.length;

    const resp = await fetch(`/calendario/?mes=${mesActual}&anio=${anoActual}`);
    const dias = await resp.json();

    const totalDias = document.getElementById('total-dias');
    if (totalDias) totalDias.textContent = dias.length;
}

function actualizarRutinaActivaInicio() {
    actualizarEstadisticasInicio();
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

    const catalogo = document.getElementById('catalogo-ejercicios');
    if (catalogo) {
        catalogo.innerHTML =
            ejerciciosDisponibles.map(ej => `<div class="ej-chip">${ej}</div>`).join('');
    }
}
// ===== EJERCICIOS API =====

let categoriaActual = null;

async function cargarCategorias() {
    const resp = await fetch('/ejercicios/categorias');
    const cats = await resp.json();
    const cont = document.getElementById('filtros-categorias');
    cats.forEach(cat => {
        const btn = document.createElement('button');
        btn.className = 'filtro-btn';
        btn.textContent = cat.nombre;
        btn.onclick = () => filtrarEjercicios(cat.id, btn);
        cont.appendChild(btn);
    });
}

async function filtrarEjercicios(categoriaId, btn) {
    categoriaActual = categoriaId;
    document.querySelectorAll('.filtro-btn').forEach(b => b.classList.remove('active'));
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
    const lista = await resp.json();
    grid.innerHTML = '';
    if (!lista.length) {
        grid.innerHTML = '<p class="loading-text">No hay ejercicios.</p>';
        return;
    }
    lista.forEach(ej => {
        const card = document.createElement('div');
        card.className = 'ej-card';
        card.innerHTML = `
            <span class="ej-badge">${ej.categoria}</span>
            <h4>${ej.nombre}</h4>
            <p>${ej.descripcion ? ej.descripcion.substring(0, 80) + '...' : 'Sin descripción'}</p>
        `;
        card.onclick = () => abrirDetalle(ej.id);
        grid.appendChild(card);
    });
}

async function abrirDetalle(id) {
    document.getElementById('modal-overlay').classList.add('open');
    document.getElementById('modal-content').innerHTML = '<button class="modal-close" onclick="cerrarModal()">✕</button><p class="loading-text">Cargando...</p>';
    const resp = await fetch(`/ejercicios/${id}`);
    const ej = await resp.json();
    document.getElementById('modal-content').innerHTML = `
        <button class="modal-close" onclick="cerrarModal()">✕</button>
        ${ej.imagen_url ? `<img src="${ej.imagen_url}" alt="${ej.nombre}">` : ''}
        <h2>${ej.nombre}</h2>
        <p class="modal-cat">${ej.categoria}</p>
        <p class="modal-desc">${ej.descripcion || 'Sin descripción disponible.'}</p>
        ${ej.musculos && ej.musculos.length ? `
            <div class="modal-musculos">
                ${ej.musculos.map(m => `<span class="ej-badge">${m}</span>`).join('')}
            </div>` : ''}
    `;
}

function cerrarModal(e) {
    if (!e || e.target === document.getElementById('modal-overlay')) {
        document.getElementById('modal-overlay').classList.remove('open');
    }
}

// Cargar ejercicios al entrar a la página
const originalShowPage = showPage;
window.showPageEjercicios = function(id, el) {
    originalShowPage(id, el);
    if (id === 'ejercicios') {
        const grid = document.getElementById('ejercicios-grid');
        if (grid.querySelector('.loading-text')) {
            cargarCategorias();
            cargarEjercicios();
        }
    }
}
// ===== INICIO =====

generateCalendar();
renderEjerciciosSelector();
cargarRutinas();
cargarDiasCompletados();
