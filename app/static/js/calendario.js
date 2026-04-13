const ejerciciosDisponibles = [
    "Press banca",
    "Dominadas",
    "Sentadilla",
    "Peso muerto",
    "Remo barra",
    "Press militar",
    "Curl bíceps",
    "Plancha"
];

let rutinas = [
    {
        id:1,
        nombre:"Push Pull Legs",
        ejercicios:["Press banca","Dominadas","Sentadilla"],
        activa:true
    },
    {
        id:2,
        nombre:"Full Body",
        ejercicios:["Peso muerto","Remo barra"],
        activa:false
    }
];

let diasCompletados = [];
let diaSeleccionado = null;



function showPage(id, el){
    document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));

    document.getElementById(`page-${id}`).classList.add('active');
    el.classList.add('active');

    document.getElementById('page-title').textContent =
        id.charAt(0).toUpperCase()+id.slice(1);
}



function generateCalendar(){
    const grid = document.getElementById('calendar-grid');
    grid.innerHTML = '';

    const diasSemana = ["Lu","Ma","Mi","Ju","Vi","Sa","Do"];

    diasSemana.forEach(d=>{
        const header = document.createElement('div');
        header.classList.add('day-header');
        header.textContent = d;
        grid.appendChild(header);
    });

    for(let i=1;i<=30;i++){
        const day = document.createElement('div');
        day.classList.add('day');

        if(diasCompletados.includes(i)){
            day.classList.add('completed');
        }

        day.textContent = i;

        day.onclick = ()=>seleccionarDia(i);

        grid.appendChild(day);
    }
}

function seleccionarDia(dia){
    diaSeleccionado = dia;

    generateCalendar();

    const dias = document.querySelectorAll('.day');

    dias.forEach(d=>{
        if(parseInt(d.textContent)===dia){
            d.classList.add('active');
        }
    });
}

function marcarDiaCompletado(){
    if(!diaSeleccionado) return;

    if(!diasCompletados.includes(diaSeleccionado)){
        diasCompletados.push(diaSeleccionado);
    }

    generateCalendar();
}



function renderEjerciciosSelector(){
    const cont = document.getElementById('ejercicios-selector');
    cont.innerHTML = '';

    ejerciciosDisponibles.forEach(ej=>{
        const chip = document.createElement('div');
        chip.classList.add('ej-chip');
        chip.textContent = ej;

        chip.onclick = ()=>{
            chip.classList.toggle('selected');
        };

        cont.appendChild(chip);
    });

    document.getElementById('catalogo-ejercicios').innerHTML =
        ejerciciosDisponibles.map(ej=>`<div class="ej-chip">${ej}</div>`).join('');
}



function renderRutinas(){
    const cont = document.getElementById('rutinas-container');
    cont.innerHTML = '';

    rutinas.forEach(rutina=>{

        const div = document.createElement('div');
        div.classList.add('rutina-card');

        if(rutina.activa){
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

    actualizarRutinaActivaInicio();
}



function crearRutina(){
    const nombreInput = document.getElementById('nombre-rutina');
    const nombre = nombreInput.value.trim();

    if(!nombre) return;

    const ejerciciosSeleccionados = [
        ...document.querySelectorAll('.ej-chip.selected')
    ].map(chip=>chip.textContent);

    if(ejerciciosSeleccionados.length===0) return;

    rutinas.push({
        id:Date.now(),
        nombre,
        ejercicios:ejerciciosSeleccionados,
        activa:false
    });

    nombreInput.value='';

    renderRutinas();
    renderEjerciciosSelector();
}



function activarRutina(id){
    rutinas.forEach(r=>{
        r.activa = r.id===id;
    });

    renderRutinas();
}



function eliminarRutina(id){
    rutinas = rutinas.filter(r=>r.id!==id);

    renderRutinas();
}



function actualizarRutinaActivaInicio(){
    const activa = rutinas.find(r=>r.activa);

    document.getElementById('rutina-activa-nombre').textContent =
        activa ? activa.nombre : 'Ninguna';
}



generateCalendar();
renderEjerciciosSelector();
renderRutinas();