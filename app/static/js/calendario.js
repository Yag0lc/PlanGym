// ===== CALENDARIO =====

const nombresMeses = [
    "Enero", "Febrero", "Marzo", "Abril",
    "Mayo", "Junio", "Julio", "Agosto",
    "Septiembre", "Octubre", "Noviembre", "Diciembre"
];

const nombresDias = [
    "domingo", "lunes", "martes", "miercoles", "jueves", "viernes", "sabado"
];

let diasCompletados = [];
let diaSeleccionado = null;

const hoy = new Date();
let mesActual = hoy.getMonth() + 1;
let anoActual = hoy.getFullYear();

function mostrarFechaActual() {
    const fecha = new Date();
    const diaSemana = nombresDias[fecha.getDay()];
    const dia = fecha.getDate();
    const mes = nombresMeses[fecha.getMonth()].toLowerCase();
    const ano = fecha.getFullYear();

    document.getElementById('fecha-actual').textContent =
        `${diaSemana}, ${dia} de ${mes} de ${ano}`;
}

async function cargarDiasCompletados() {
    const resp = await fetch(`/calendario/?mes=${mesActual}&anio=${anoActual}`);
    diasCompletados = await resp.json();

    generarCalendario();
    await actualizarRacha();
}

async function marcarDiaCompletado() {
    if (!diaSeleccionado) return;

    const endpoint = diasCompletados.includes(diaSeleccionado)
        ? '/calendario/desmarcar'
        : '/calendario/marcar';

    await fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            dia: diaSeleccionado,
            mes: mesActual,
            anio: anoActual
        })
    });

    await cargarDiasCompletados();
}

async function cambiarMes(direccion) {
    mesActual += direccion;

    if (mesActual > 12) {
        mesActual = 1;
        anoActual++;
    }

    if (mesActual < 1) {
        mesActual = 12;
        anoActual--;
    }

    diaSeleccionado = null;

    await cargarDiasCompletados();
}

async function obtenerDiasCompletadosMes(mes, ano) {
    const resp = await fetch(`/calendario/?mes=${mes}&anio=${ano}`);

    if (!resp.ok) {
        return [];
    }

    return await resp.json();
}

async function actualizarRacha() {
    const rachaElemento = document.getElementById('racha-dias');
    if (!rachaElemento) return;

    let fecha = new Date();
    let racha = 0;
    const cacheMeses = {};

    for (let i = 0; i < 365; i++) {
        const mes = fecha.getMonth() + 1;
        const ano = fecha.getFullYear();
        const clave = `${mes}-${ano}`;

        if (!cacheMeses[clave]) {
            cacheMeses[clave] = await obtenerDiasCompletadosMes(mes, ano);
        }

        const dia = fecha.getDate();
        const completado = cacheMeses[clave].includes(dia);

        if (!completado && racha === 0 && i === 0) {
            fecha.setDate(fecha.getDate() - 1);
            continue;
        }

        if (!completado) {
            break;
        }

        racha++;
        fecha.setDate(fecha.getDate() - 1);
    }

    rachaElemento.textContent = racha;
}

function generarCalendario() {
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

        if (diasCompletados.includes(i)) {
            day.classList.add('completed');
        }

        if (i === diaSeleccionado) {
            day.classList.add('active');
        }

        day.textContent = i;
        day.onclick = () => seleccionarDia(i);

        grid.appendChild(day);
    }
}

function seleccionarDia(dia) {
    diaSeleccionado = dia;
    generarCalendario();
}

mostrarFechaActual();
cargarDiasCompletados();
