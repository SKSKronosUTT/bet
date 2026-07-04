// ============================================================================
// Pantalla del jugador (celular). Se registra, arma su parley, sigue el
// resultado en vivo y al final apuesta su última oportunidad.
// ============================================================================

const VISTAS = [
  "vista-registro",
  "vista-esperando-inicio",
  "vista-apuesta",
  "vista-siguiendo",
  "vista-bono-espera",
  "vista-bono-apuesta",
  "vista-bono-esperando",
  "vista-fin",
];

const ETIQUETAS_TIPO = {
  equipo1: null, // se llena dinámicamente con el nombre del equipo
  equipo2: null,
  empate: "Empate",
  over: "Más de 2.5 goles",
  under: "Menos de 2.5 goles",
};

let vistaVisible = null;
let formularioApuestaListo = false;
let formularioBonoListo = false;
let seleccionesParley = {};   // { matchId: tipo }
let seleccionBono = null;
let confetiLanzado = false;

function $(id) { return document.getElementById(id); }

function mostrarVista(id) {
  if (id === vistaVisible) return;
  vistaVisible = id;
  VISTAS.forEach((v) => $(v).classList.add("oculto"));
  $(id).classList.remove("oculto");
}

async function post(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body || {}),
  });
  return res.json();
}

function mostrarError(id, mensaje) {
  const el = $(id);
  el.textContent = mensaje;
  el.classList.remove("oculto");
}

function ocultarError(id) {
  $(id).classList.add("oculto");
}

// ---------------------------------------------------------------------------
// Registro
// ---------------------------------------------------------------------------

$("btn-registrar").addEventListener("click", registrar);
$("input-nombre").addEventListener("keydown", (e) => { if (e.key === "Enter") registrar(); });

async function registrar() {
  const nombre = $("input-nombre").value.trim();
  ocultarError("error-registro");
  if (!nombre) {
    mostrarError("error-registro", "Escribe tu nombre para continuar.");
    return;
  }
  $("btn-registrar").disabled = true;
  const r = await post("/api/registro", { username: nombre });
  $("btn-registrar").disabled = false;
  if (r.error) {
    mostrarError("error-registro", r.error);
    return;
  }
  actualizar();
}

// ---------------------------------------------------------------------------
// Construcción del formulario de parley (una sola vez)
// ---------------------------------------------------------------------------

function construirFormularioApuesta(data) {
  const cont = $("contenedor-partidos-apuesta");
  cont.innerHTML = "";
  seleccionesParley = {};

  data.partidos.forEach((partido) => {
    const card = document.createElement("div");
    card.className = "partido-apuesta";

    const opciones = [
      { tipo: "equipo1", texto: `Gana ${partido.equipo1}` },
      { tipo: "empate", texto: "Empate" },
      { tipo: "equipo2", texto: `Gana ${partido.equipo2}` },
    ];
    const opcionesTotal = [
      { tipo: "over", texto: "Más de 2.5 goles" },
      { tipo: "under", texto: "Menos de 2.5 goles" },
    ];

    const versus = document.createElement("div");
    versus.className = "versus";
    versus.innerHTML = `
      <span class="bandera">${partido.bandera1}</span>
      <span>${partido.equipo1}</span>
      <span class="vs">vs</span>
      <span>${partido.equipo2}</span>
      <span class="bandera">${partido.bandera2}</span>`;
    card.appendChild(versus);

    const subt1 = document.createElement("div");
    subt1.className = "subtitulo-opciones";
    subt1.textContent = "Resultado";
    card.appendChild(subt1);

    const grid1 = document.createElement("div");
    grid1.className = "opciones-resultado";
    opciones.forEach((op) => grid1.appendChild(crearBotonOpcion(partido.id, op.tipo, op.texto)));
    card.appendChild(grid1);

    const subt2 = document.createElement("div");
    subt2.className = "subtitulo-opciones";
    subt2.textContent = "Total de goles";
    card.appendChild(subt2);

    const grid2 = document.createElement("div");
    grid2.className = "opciones-total";
    opcionesTotal.forEach((op) => grid2.appendChild(crearBotonOpcion(partido.id, op.tipo, op.texto)));
    card.appendChild(grid2);

    cont.appendChild(card);
  });
}

function crearBotonOpcion(matchId, tipo, texto) {
  const btn = document.createElement("div");
  btn.className = "opcion-apuesta";
  btn.textContent = texto;
  btn.dataset.match = matchId;
  btn.dataset.tipo = tipo;
  btn.addEventListener("click", () => {
    seleccionesParley[matchId] = tipo;
    const hermanos = document.querySelectorAll(`.opcion-apuesta[data-match="${matchId}"]`);
    hermanos.forEach((h) => h.classList.remove("seleccionada"));
    btn.classList.add("seleccionada");
    $("btn-confirmar-parley").disabled = Object.keys(seleccionesParley).length < 3;
  });
  return btn;
}

$("btn-confirmar-parley").addEventListener("click", async () => {
  ocultarError("error-apuesta");
  $("btn-confirmar-parley").disabled = true;
  const r = await post("/api/apostar", { apuestas: seleccionesParley });
  if (r.error) {
    mostrarError("error-apuesta", r.error);
    $("btn-confirmar-parley").disabled = false;
    return;
  }
  actualizar();
});

// ---------------------------------------------------------------------------
// Tabla de seguimiento en vivo
// ---------------------------------------------------------------------------

function badgeEstado(status) {
  const mapa = {
    abierta: '<span class="badge badge--abierta">Abierta</span>',
    ganada: '<span class="badge badge--ganada">Ganada</span>',
    perdida: '<span class="badge badge--perdida">Perdida</span>',
  };
  return mapa[status] || mapa.abierta;
}

function renderSeguimiento(data) {
  const cont = $("contenedor-parley-vivo");
  cont.innerHTML = "";
  data.partidos.forEach((p) => {
    const marcador = (p.marcador1 !== null && p.marcador1 !== undefined)
      ? `${p.marcador1}-${p.marcador2}`
      : "—";
    const row = document.createElement("div");
    row.className = "leg-parley";
    row.innerHTML = `
      <div class="banderas">${p.bandera1}${p.bandera2}</div>
      <div class="info">
        <div class="partido-nombre">${p.equipo1} vs ${p.equipo2}</div>
        <div class="apuesta-nombre">${p.apuesta_label || "—"}</div>
      </div>
      <div class="marcador-mini">${marcador}</div>
      ${badgeEstado(p.apuesta_status)}`;
    cont.appendChild(row);
  });

  const alguienPerdio = data.partidos.some((p) => p.apuesta_status === "perdida");
  const todosGanados = data.partidos.every((p) => p.apuesta_status === "ganada");
  if (alguienPerdio) {
    $("texto-siguiendo").textContent = "Tu parley se rompió. Necesitas que todos tus pronósticos ganen.";
  } else if (todosGanados) {
    $("texto-siguiendo").textContent = "¡Vas perfecto! Sigue mirando la pantalla.";
  } else {
    $("texto-siguiendo").textContent = "Los partidos se están jugando en la pantalla…";
  }
}

// ---------------------------------------------------------------------------
// Apuesta bono
// ---------------------------------------------------------------------------

function construirFormularioBono(data) {
  const cont = $("opciones-bono");
  cont.innerHTML = "";
  seleccionBono = null;
  const opciones = [
    { tipo: "equipo1", texto: `Gana ${data.bono.equipo1}` },
    { tipo: "empate", texto: "Empate" },
    { tipo: "equipo2", texto: `Gana ${data.bono.equipo2}` },
  ];
  opciones.forEach((op) => {
    const btn = document.createElement("div");
    btn.className = "opcion-apuesta";
    btn.textContent = op.texto;
    btn.addEventListener("click", () => {
      seleccionBono = op.tipo;
      cont.querySelectorAll(".opcion-apuesta").forEach((h) => h.classList.remove("seleccionada"));
      btn.classList.add("seleccionada");
      $("btn-confirmar-bono").disabled = false;
    });
    cont.appendChild(btn);
  });
}

$("btn-confirmar-bono").addEventListener("click", async () => {
  if (!seleccionBono) return;
  ocultarError("error-bono");
  $("btn-confirmar-bono").disabled = true;
  const r = await post("/api/apostar-bono", { tipo: seleccionBono });
  if (r.error) {
    mostrarError("error-bono", r.error);
    $("btn-confirmar-bono").disabled = false;
    return;
  }
  actualizar();
});

// ---------------------------------------------------------------------------
// Final + confeti
// ---------------------------------------------------------------------------

function lanzarConfeti() {
  if (confetiLanzado) return;
  confetiLanzado = true;
  const caja = $("confeti-caja");
  const colores = ["#1E8E3E", "#D6A419", "#C93B2C", "#16241A"];
  for (let i = 0; i < 40; i++) {
    const pieza = document.createElement("div");
    pieza.className = "pieza-confeti";
    pieza.style.left = Math.random() * 100 + "%";
    pieza.style.background = colores[i % colores.length];
    pieza.style.animationDelay = (Math.random() * 0.6) + "s";
    caja.appendChild(pieza);
  }
}

// ---------------------------------------------------------------------------
// Bucle principal: decide qué vista mostrar según el estado del servidor
// ---------------------------------------------------------------------------

async function actualizar() {
  let data;
  try {
    const res = await fetch("/api/mi-estado");
    data = await res.json();
  } catch (e) {
    console.error("Error consultando mi-estado", e);
    return;
  }

  if (!data.registrado) {
    mostrarVista("vista-registro");
    return;
  }

  $("saldo-chip").classList.remove("oculto");
  $("saldo-chip").textContent = "$" + Math.round(data.balance);

  if (data.fase === "lobby") {
    $("saludo-espera").textContent = `¡Hola, ${data.username}!`;
    mostrarVista("vista-esperando-inicio");
    return;
  }

  if (data.fase === "betting") {
    if (!data.parlay_submitted) {
      if (!formularioApuestaListo) {
        construirFormularioApuesta(data);
        formularioApuestaListo = true;
      }
      mostrarVista("vista-apuesta");
    } else {
      renderSeguimiento(data);
      mostrarVista("vista-siguiendo");
    }
    return;
  }

  if (data.fase === "playing") {
    renderSeguimiento(data);
    mostrarVista("vista-siguiendo");
    return;
  }

  if (data.fase === "bono_intro") {
    mostrarVista("vista-bono-espera");
    return;
  }

  if (data.fase === "bono_apuestas") {
    if (!data.bonus_bet_submitted) {
      if (!formularioBonoListo) {
        construirFormularioBono(data);
        formularioBonoListo = true;
      }
      mostrarVista("vista-bono-apuesta");
    } else {
      mostrarVista("vista-bono-esperando");
    }
    return;
  }

  if (data.fase === "bono_playing") {
    mostrarVista("vista-bono-esperando");
    return;
  }

  if (data.fase === "end") {
    $("cifra-final").textContent = "$" + Math.round(data.balance);
    mostrarVista("vista-fin");
    lanzarConfeti();
    return;
  }
}

actualizar();
setInterval(actualizar, 1500);
