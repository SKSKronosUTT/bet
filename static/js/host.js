// ============================================================================
// Pantalla del anfitrión (TV). Controla el flujo del juego consultando
// /api/estado cada cierto tiempo, y dispara las animaciones de partido
// localmente en el navegador (el servidor solo guarda pending/live/finished).
// ============================================================================

const NOMBRES_ESPERADOS = JSON.parse(document.getElementById("config-datos").textContent);

const VISTAS = {
  lobby: "vista-lobby",
  betting: "vista-apostando",
  playing: "vista-jugando",
  bono_intro: "vista-bono-intro",
  bono_apuestas: "vista-bono-apuestas",
  bono_playing: "vista-bono-jugando",
  end: "vista-final",
};

let faseActual = null;
let matchEtiquetadoId = null;   // ultimo id de partido cuyas banderas/nombres ya pintamos
let matchAnimadoId = null;      // evita relanzar la animación en cada poll
let bonoEtiquetadoId = null;
let bonoAnimadoId = null;

function $(id) { return document.getElementById(id); }

function mostrarVista(fase) {
  if (fase === faseActual) return;
  faseActual = fase;
  Object.values(VISTAS).forEach((id) => $(id).classList.add("oculto"));
  const destino = VISTAS[fase];
  if (destino) $(destino).classList.remove("oculto");
}

async function post(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body || {}),
  });
  return res.json();
}

// ---------------------------------------------------------------------------
// Animación de partido (reutilizable para partidos normales y el bono)
// ---------------------------------------------------------------------------

function animarPartido(prefijo, partido, alTerminar) {
  const golesEl1 = $(`${prefijo}-goles1`);
  const golesEl2 = $(`${prefijo}-goles2`);
  const relojEl = $(`${prefijo}-reloj`);
  const toast = prefijo === "j" ? $("gol-toast") : $("gol-toast-bono");

  let restantes = (partido.goles || []).slice().sort((a, b) => a.minuto - b.minuto);
  let m1 = 0, m2 = 0, minuto = 0;
  golesEl1.textContent = "0";
  golesEl2.textContent = "0";
  relojEl.textContent = "00:00";

  const intervaloMs = Math.max(30, partido.duracion_ms / 90);

  const timer = setInterval(() => {
    minuto++;
    relojEl.textContent = String(minuto).padStart(2, "0") + ":00";

    while (restantes.length && restantes[0].minuto <= minuto) {
      const gol = restantes.shift();
      if (gol.equipo === 1) {
        m1++;
        golesEl1.textContent = m1;
      } else {
        m2++;
        golesEl2.textContent = m2;
      }
      lanzarToast(toast, gol.jugador);
    }

    if (minuto >= 90) {
      clearInterval(timer);
      relojEl.textContent = "90:00";
      alTerminar();
    }
  }, intervaloMs);
}

function lanzarToast(toast, nombreGoleador) {
  toast.textContent = `¡GOOOL de ${nombreGoleador}!`;
  toast.classList.remove("mostrar");
  void toast.offsetWidth; // fuerza reflow para poder relanzar la animación
  toast.classList.add("mostrar");
}

// ---------------------------------------------------------------------------
// Render por fase
// ---------------------------------------------------------------------------

function tarjetaJugadorLobby(nombreEsperado, jugador) {
  const div = document.createElement("div");
  div.className = "jugador-slot" + (jugador ? " ocupado" : "");
  const inicial = jugador ? jugador.username.charAt(0).toUpperCase() : "?";
  div.innerHTML = `
    <div class="num-camiseta">${inicial}</div>
    <div>
      <div class="nombre">${jugador ? jugador.username : nombreEsperado}</div>
      <div class="estado-txt">${jugador ? "Conectado, listo para jugar" : "Esperando a que se una…"}</div>
    </div>`;
  return div;
}

function renderLobby(estado) {
  const cont = $("lista-jugadores");
  cont.innerHTML = "";
  NOMBRES_ESPERADOS.forEach((nombre, slot) => {
    const jugador = estado.jugadores.find((j) => j.slot === slot) || null;
    cont.appendChild(tarjetaJugadorLobby(nombre, jugador));
  });
  const listos = estado.jugadores.length === NOMBRES_ESPERADOS.length;
  $("btn-iniciar-apuestas").disabled = !listos;
}

function renderApostando(estado) {
  const cont = $("lista-jugadores-apostando");
  cont.innerHTML = "";
  estado.jugadores.forEach((j) => {
    const div = document.createElement("div");
    div.className = "jugador-slot ocupado";
    const estadoBadge = j.parlay_submitted
      ? '<span class="badge badge--ganada">Parley listo</span>'
      : '<span class="badge badge--espera">Eligiendo…</span>';
    div.innerHTML = `
      <div class="num-camiseta">${j.username.charAt(0).toUpperCase()}</div>
      <div style="flex:1;">
        <div class="nombre">${j.username}</div>
      </div>
      ${estadoBadge}`;
    cont.appendChild(div);
  });
  const todosListos = estado.jugadores.length > 0 && estado.jugadores.every((j) => j.parlay_submitted);
  $("btn-comenzar-partidos").disabled = !todosListos;
}

function renderJugando(estado) {
  const p = estado.partido_actual;
  if (!p) return;

  if (p.id !== matchEtiquetadoId) {
    matchEtiquetadoId = p.id;
    $("j-bandera1").textContent = p.bandera1;
    $("j-nombre1").textContent = p.equipo1;
    $("j-bandera2").textContent = p.bandera2;
    $("j-nombre2").textContent = p.equipo2;
    $("j-goles1").textContent = "0";
    $("j-goles2").textContent = "0";
    $("j-reloj").textContent = "00:00";
    $("btn-siguiente").classList.add("oculto");
  }

  if (p.status === "pending") {
    $("btn-reproducir").classList.remove("oculto");
    $("btn-reproducir").disabled = false;
  } else if (p.status === "live") {
    $("btn-reproducir").classList.add("oculto");
    if (matchAnimadoId !== p.id) {
      matchAnimadoId = p.id;
      animarPartido("j", p, () => {
        $("btn-siguiente").disabled = false;
        $("btn-siguiente").classList.remove("oculto");
      });
    }
  }
}

function renderBonoApuestas(estado) {
  const cont = $("lista-jugadores-bono");
  cont.innerHTML = "";
  estado.jugadores.forEach((j) => {
    const div = document.createElement("div");
    div.className = "jugador-slot ocupado";
    const badge = j.bonus_bet_submitted
      ? '<span class="badge badge--ganada">Apostó su $1</span>'
      : '<span class="badge badge--espera">Pensando…</span>';
    div.innerHTML = `
      <div class="num-camiseta">${j.username.charAt(0).toUpperCase()}</div>
      <div style="flex:1;"><div class="nombre">${j.username}</div></div>
      ${badge}`;
    cont.appendChild(div);
  });
  const todosListos = estado.jugadores.length > 0 && estado.jugadores.every((j) => j.bonus_bet_submitted);
  $("btn-comenzar-bono").disabled = !todosListos;
}

function renderBonoJugando(estado) {
  const p = estado.partido_actual;
  if (!p) return;

  if (p.id !== bonoEtiquetadoId) {
    bonoEtiquetadoId = p.id;
    $("b-bandera1").textContent = p.bandera1;
    $("b-nombre1").textContent = p.equipo1;
    $("b-bandera2").textContent = p.bandera2;
    $("b-nombre2").textContent = p.equipo2;
    $("b-goles1").textContent = "0";
    $("b-goles2").textContent = "0";
    $("b-reloj").textContent = "00:00";
    $("btn-finalizar-bono").classList.add("oculto");
  }

  if (p.status === "pending") {
    $("btn-reproducir-bono").classList.remove("oculto");
    $("btn-reproducir-bono").disabled = false;
  } else if (p.status === "live") {
    $("btn-reproducir-bono").classList.add("oculto");
    if (bonoAnimadoId !== p.id) {
      bonoAnimadoId = p.id;
      animarPartido("b", p, () => {
        $("btn-finalizar-bono").disabled = false;
        $("btn-finalizar-bono").classList.remove("oculto");
      });
    }
  }
}

function renderFinal(estado) {
  const cont = $("tabla-final");
  cont.innerHTML = "";
  estado.jugadores.forEach((j) => {
    const div = document.createElement("div");
    div.className = "tarjeta-final";
    div.innerHTML = `
      <div class="nombre">${j.username}</div>
      <div class="cifra">$${Math.round(j.balance)}</div>`;
    cont.appendChild(div);
  });
}

// ---------------------------------------------------------------------------
// Bucle principal
// ---------------------------------------------------------------------------

async function actualizar() {
  try {
    const res = await fetch("/api/estado");
    const estado = await res.json();
    mostrarVista(estado.fase);
    if (estado.fase === "lobby") renderLobby(estado);
    else if (estado.fase === "betting") renderApostando(estado);
    else if (estado.fase === "playing") renderJugando(estado);
    else if (estado.fase === "bono_apuestas") renderBonoApuestas(estado);
    else if (estado.fase === "bono_playing") renderBonoJugando(estado);
    else if (estado.fase === "end") renderFinal(estado);
    if (window.twemoji) twemoji.parse(document.getElementById("host-app"));
  } catch (e) {
    console.error("Error consultando /api/estado", e);
  }
}

// ---------------------------------------------------------------------------
// Botones
// ---------------------------------------------------------------------------

$("btn-iniciar-apuestas").addEventListener("click", async () => {
  $("btn-iniciar-apuestas").disabled = true;
  const r = await post("/api/host/iniciar-apuestas");
  if (r.error) { alert(r.error); $("btn-iniciar-apuestas").disabled = false; }
});

$("btn-comenzar-partidos").addEventListener("click", async () => {
  $("btn-comenzar-partidos").disabled = true;
  const r = await post("/api/host/comenzar-partidos");
  if (r.error) { alert(r.error); $("btn-comenzar-partidos").disabled = false; }
});

$("btn-reproducir").addEventListener("click", async () => {
  $("btn-reproducir").disabled = true;
  await post("/api/host/reproducir-partido");
});

$("btn-siguiente").addEventListener("click", async () => {
  $("btn-siguiente").disabled = true;
  matchAnimadoId = null;
  await post("/api/host/finalizar-partido");
});

$("btn-revelar-bono").addEventListener("click", async () => {
  $("btn-revelar-bono").disabled = true;
  await post("/api/host/revelar-bono");
});

$("btn-comenzar-bono").addEventListener("click", async () => {
  $("btn-comenzar-bono").disabled = true;
  await post("/api/host/comenzar-bono");
});

$("btn-reproducir-bono").addEventListener("click", async () => {
  $("btn-reproducir-bono").disabled = true;
  await post("/api/host/reproducir-bono");
});

$("btn-finalizar-bono").addEventListener("click", async () => {
  $("btn-finalizar-bono").disabled = true;
  await post("/api/host/finalizar-bono");
});

$("btn-reiniciar").addEventListener("click", async () => {
  if (!confirm("¿Reiniciar toda la partida? Se borrarán los jugadores y resultados.")) return;
  await post("/api/host/reiniciar");
  matchEtiquetadoId = matchAnimadoId = bonoEtiquetadoId = bonoAnimadoId = null;
  faseActual = null;
  actualizar();
});

actualizar();
setInterval(actualizar, 1500);
