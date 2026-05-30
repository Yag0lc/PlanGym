

let rutinas = [];
let rutinaEditandoId = null;
let ejerciciosParaRutina = cargarEjerciciosParaRutina();
const diasSemana = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"];

function cargarEjerciciosParaRutina() {
    const datos = localStorage.getItem('plangym_ejercicios_rutina');
    const ejercicios = datos ? JSON.parse(datos) : [];
    return ejercicios.map(normalizarEjercicioRutina).filter(ej => ej.nombre);
}

function guardarEjerciciosParaRutina() {
    localStorage.setItem('plangym_ejercicios_rutina', JSON.stringify(ejerciciosParaRutina));
}

function normalizarEjercicioRutina(ejercicio) {
    if (typeof ejercicio === 'string') {
        return {
            nombre: ejercicio,
            dia_semana: 'lunes'
        };
    }

    return {
        nombre: ejercicio.nombre || '',
        dia_semana: diasSemana.includes(ejercicio.dia_semana) ? ejercicio.dia_semana : 'lunes'
    };
}

function ejercicioEstaSeleccionado(nombre) {
    return ejerciciosParaRutina.some(ej => ej.nombre === nombre);
}

function cambiarEjercicioParaRutina(nombre) {
    if (ejercicioEstaSeleccionado(nombre)) {
        ejerciciosParaRutina = ejerciciosParaRutina.filter(ej => ej.nombre !== nombre);
    } else {
        ejerciciosParaRutina.push({
            nombre,
            dia_semana: 'lunes'
        });
    }

    guardarEjerciciosParaRutina();
    renderEjerciciosSelector();

    if (typeof cargarEjercicios === 'function') {
        cargarEjercicios();
    }
}

function cambiarDiaEjercicio(nombre, dia) {
    ejerciciosParaRutina = ejerciciosParaRutina.map(ej => {
        if (ej.nombre === nombre) {
            return {
                nombre: ej.nombre,
                dia_semana: dia
            };
        }

        return ej;
    });

    guardarEjerciciosParaRutina();
}

async function cargarRutinas() {
    const resp = await fetch('/rutinas/');
    if (!resp.ok) {
        rutinas = [];
        renderRutinas();
        return;
    }

    rutinas = await resp.json();
    rutinas = rutinas.map(rutina => {
        rutina.ejercicios = rutina.ejercicios.map(normalizarEjercicioRutina);
        return rutina;
    });

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
    ].map(fila => {
        return {
            nombre: fila.dataset.nombre,
            dia_semana: fila.querySelector('select').value
        };
    });

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
    const opciones = [];

    [...rutina.ejercicios, ...ejerciciosParaRutina].forEach(ejercicio => {
        if (!opciones.some(ej => ej.nombre === ejercicio.nombre)) {
            opciones.push(ejercicio);
        }
    });

    const chips = opciones.map(ej => {
        const ejercicioRutina = rutina.ejercicios.find(item => item.nombre === ej.nombre);
        const selected = ejercicioRutina ? 'selected' : '';
        const dia = ejercicioRutina ? ejercicioRutina.dia_semana : ej.dia_semana;
        const opcionesDias = diasSemana.map(diaSemana => {
            const marcado = diaSemana === dia ? 'selected' : '';
            return `<option value="${diaSemana}" ${marcado}>${diaSemana}</option>`;
        }).join('');

        return `
            <div class="ejercicio-dia-row editar-ejercicio-${rutina.id} ${selected}" data-nombre="${ej.nombre}">
                <button class="secondary" onclick="this.parentElement.classList.toggle('selected')">${ej.nombre}</button>
                <select class="day-select">${opcionesDias}</select>
            </div>
        `;
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
        const ejerciciosTexto = textoRutinaPorDias(rutina.ejercicios);

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

                ${ejerciciosTexto}
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

function textoRutinaPorDias(ejercicios) {
    let hayMas = false;
    const diasConEjercicios = diasSemana.map(dia => {
        const ejerciciosDia = ejercicios
            .filter(ej => ej.dia_semana === dia)
            .map(ej => ej.nombre);

        if (ejerciciosDia.length === 0) return '';

        if (ejerciciosDia.length > 3) {
            hayMas = true;
        }

        return `<p class="rutina-dia"><strong>${dia}:</strong> ${ejerciciosDia.slice(0, 3).join(', ')}${ejerciciosDia.length > 3 ? '...' : ''}</p>`;
    }).filter(linea => linea);

    if (diasConEjercicios.length > 3) {
        hayMas = true;
    }

    const lineasVisibles = diasConEjercicios.slice(0, 3);
    if (hayMas) {
        lineasVisibles.push('<p class="rutina-dia">...</p>');
    }

    return `<div class="rutina-dias">${lineasVisibles.join('')}</div>`;
}

function obtenerDiaHoy() {
    const indice = new Date().getDay();
    const dias = ["domingo", "lunes", "martes", "miercoles", "jueves", "viernes", "sabado"];
    return dias[indice];
}

async function actualizarEstadisticasInicio() {
    const activa = rutinas.find(r => r.activa);

    document.getElementById('rutina-activa-nombre').textContent =
        activa ? activa.nombre : 'Ninguna';

    const totalRutinas = document.getElementById('total-rutinas');
    if (totalRutinas) {
        totalRutinas.textContent = rutinas.length;
    }

    const entrenoHoy = document.getElementById('entreno-hoy');
    const entrenoHoyLista = document.getElementById('entreno-hoy-lista');
    if (entrenoHoy) {
        if (!activa) {
            entrenoHoy.textContent = 'Sin rutina';
            if (entrenoHoyLista) {
                entrenoHoyLista.innerHTML = '<p class="loading-text">No tienes una rutina activa.</p>';
            }
        } else {
            const diaHoy = obtenerDiaHoy();
            const ejerciciosHoy = activa.ejercicios
                .filter(ej => ej.dia_semana === diaHoy)
                .map(ej => ej.nombre);

            entrenoHoy.textContent = ejerciciosHoy.length > 0 ? `${ejerciciosHoy.length} ejercicios` : 'Descanso';

            if (entrenoHoyLista) {
                if (ejerciciosHoy.length === 0) {
                    entrenoHoyLista.innerHTML = '<p class="loading-text">Hoy toca descanso.</p>';
                } else {
                    entrenoHoyLista.innerHTML = ejerciciosHoy.map((nombre, index) => {
                        return `
                            <div class="entreno-hoy-item">
                                <span>${index + 1}</span>
                                <p>${nombre}</p>
                            </div>
                        `;
                    }).join('');
                }
            }
        }
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
        const fila = document.createElement('div');
        const opcionesDias = diasSemana.map(dia => {
            const marcado = dia === ej.dia_semana ? 'selected' : '';
            return `<option value="${dia}" ${marcado}>${dia}</option>`;
        }).join('');

        fila.classList.add('ejercicio-dia-row', 'selected');
        fila.innerHTML = `
            <button class="secondary">${ej.nombre}</button>
            <select class="day-select">${opcionesDias}</select>
        `;

        fila.querySelector('button').onclick = () => {
            cambiarEjercicioParaRutina(ej.nombre);
        };
        fila.querySelector('select').onchange = evento => {
            cambiarDiaEjercicio(ej.nombre, evento.target.value);
        };

        cont.appendChild(fila);
    });
}

renderEjerciciosSelector();
cargarRutinas();
