/* =====================================================================
   Quiniela de cumpleaños — hoja de estilos
   Concepto: boleto de estadio. Cancha verde, marcador digital, y un
   "stub" de boleto perforado como firma visual (se usa para revelar
   resultados: se "rasga" el boleto para mostrar si ganaste o perdiste).
   ===================================================================== */

@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Share+Tech+Mono&family=Karla:wght@400;500;700&display=swap');

:root {
  --bg: #F3F6ED;
  --ink: #16241A;
  --ink-soft: #4B5A4F;
  --grass: #1E8E3E;
  --grass-dark: #12602B;
  --grass-line: rgba(255, 255, 255, 0.4);
  --gold: #D6A419;
  --gold-dark: #8A6A0F;
  --gold-bg: #FBEECC;
  --red: #C93B2C;
  --red-dark: #7A2116;
  --red-bg: #F9DAD5;
  --green-bg: #DDF0DC;
  --green-dark: #1F6B32;
  --card: #FFFFFF;
  --card-border: #DDE3D2;
  --shadow: 0 10px 30px rgba(22, 36, 26, 0.10);

  --font-display: 'Bebas Neue', sans-serif;
  --font-mono: 'Share Tech Mono', monospace;
  --font-body: 'Karla', sans-serif;
}

* { box-sizing: border-box; }

html, body {
  margin: 0;
  padding: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: var(--font-body);
  -webkit-font-smoothing: antialiased;
}

body {
  background-image:
    radial-gradient(circle at 15% 10%, rgba(30, 142, 62, 0.06), transparent 40%),
    radial-gradient(circle at 85% 90%, rgba(214, 164, 25, 0.08), transparent 40%);
}

h1, h2, h3 { font-family: var(--font-display); letter-spacing: 0.02em; margin: 0; }

button {
  font-family: var(--font-body);
  cursor: pointer;
  border: none;
  border-radius: 10px;
}

button:disabled { cursor: not-allowed; opacity: 0.5; }

button:focus-visible, input:focus-visible, label:focus-within {
  outline: 3px solid var(--gold);
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.001ms !important; transition-duration: 0.001ms !important; }
}

.oculto { display: none !important; }

/* ---------------------------------------------------------------------
   Boton generico (usado tanto en host como jugador)
   --------------------------------------------------------------------- */

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 26px;
  font-size: 17px;
  font-weight: 700;
  border-radius: 12px;
  transition: transform 0.12s ease, box-shadow 0.12s ease;
}

.btn:active:not(:disabled) { transform: scale(0.97); }

.btn-primario {
  background: var(--grass);
  color: #fff;
  box-shadow: 0 6px 0 var(--grass-dark);
}
.btn-primario:hover:not(:disabled) { filter: brightness(1.05); }
.btn-primario:active:not(:disabled) { box-shadow: 0 2px 0 var(--grass-dark); transform: translateY(4px); }

.btn-oro {
  background: var(--gold);
  color: #402F06;
  box-shadow: 0 6px 0 var(--gold-dark);
}
.btn-oro:active:not(:disabled) { box-shadow: 0 2px 0 var(--gold-dark); transform: translateY(4px); }

.btn-fantasma {
  background: transparent;
  color: var(--ink-soft);
  border: 1.5px dashed var(--card-border);
}

/* ---------------------------------------------------------------------
   El "ticket": tarjeta con muesca perforada, firma visual del proyecto
   --------------------------------------------------------------------- */

.ticket {
  position: relative;
  background: var(--card);
  border: 1.5px solid var(--card-border);
  border-radius: 18px;
  box-shadow: var(--shadow);
  overflow: hidden;
}

.ticket__cabeza {
  padding: 18px 22px;
  background: var(--grass);
  color: #fff;
  position: relative;
}

.ticket__perforado {
  position: relative;
  height: 0;
  border-top: 2px dashed var(--card-border);
  margin: 0 18px;
}

.ticket__perforado::before,
.ticket__perforado::after {
  content: "";
  position: absolute;
  top: -10px;
  width: 20px;
  height: 20px;
  background: var(--bg);
  border-radius: 50%;
}
.ticket__perforado::before { left: -28px; }
.ticket__perforado::after { right: -28px; }

.ticket__cuerpo { padding: 18px 22px; }

/* ---------------------------------------------------------------------
   Insignias de estado
   --------------------------------------------------------------------- */

.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.badge--abierta { background: var(--gold-bg); color: var(--gold-dark); }
.badge--ganada  { background: var(--green-bg); color: var(--green-dark); }
.badge--perdida { background: var(--red-bg); color: var(--red-dark); }
.badge--espera  { background: #E7E9E0; color: var(--ink-soft); }

/* =====================================================================
   ANFITRIÓN (pantalla de TV)
   ===================================================================== */

#host-app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px 5vw 60px;
}

.host-header {
  display: flex;
  align-items: baseline;
  gap: 18px;
  margin-bottom: 28px;
}

.host-header h1 {
  font-size: clamp(38px, 5vw, 64px);
  color: var(--grass-dark);
}

.host-header .marca {
  font-family: var(--font-mono);
  font-size: 15px;
  color: var(--ink-soft);
  letter-spacing: 0.08em;
}

/* --- Lobby --- */

.lobby {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  width: 100%;
  max-width: 1100px;
  align-items: start;
}

@media (max-width: 900px) {
  .lobby { grid-template-columns: 1fr; }
}

.qr-caja {
  background: var(--card);
  border: 1.5px solid var(--card-border);
  border-radius: 20px;
  box-shadow: var(--shadow);
  padding: 28px;
  text-align: center;
}

.qr-caja img {
  width: 220px;
  height: 220px;
  border-radius: 12px;
  border: 6px solid var(--grass);
  margin: 12px 0;
}

.qr-caja .url {
  font-family: var(--font-mono);
  font-size: 14px;
  color: var(--grass-dark);
  word-break: break-all;
}

.lista-jugadores { display: flex; flex-direction: column; gap: 16px; }

.jugador-slot {
  display: flex;
  align-items: center;
  gap: 16px;
  background: var(--card);
  border: 1.5px dashed var(--card-border);
  border-radius: 16px;
  padding: 18px 22px;
}

.jugador-slot.ocupado { border-style: solid; border-color: var(--grass); }

.jugador-slot .num-camiseta {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: var(--bg);
  border: 2px solid var(--card-border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-display);
  font-size: 20px;
  color: var(--ink-soft);
  flex-shrink: 0;
}

.jugador-slot.ocupado .num-camiseta { background: var(--grass); color: #fff; border-color: var(--grass-dark); }

.jugador-slot .nombre { font-weight: 700; font-size: 18px; }
.jugador-slot .estado-txt { font-size: 13px; color: var(--ink-soft); }

/* --- Cancha / animacion de partido --- */

.cancha-wrap { width: 100%; max-width: 1000px; }

.marcador-top {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  background: var(--ink);
  color: #fff;
  border-radius: 16px 16px 0 0;
  padding: 20px 30px;
}

.marcador-top .equipo { display: flex; align-items: center; gap: 12px; font-family: var(--font-display); font-size: 30px; }
.marcador-top .bandera { font-size: 40px; }
.marcador-top .goles { font-family: var(--font-mono); font-size: 48px; min-width: 50px; text-align: center; }
.marcador-top .separador { font-family: var(--font-mono); font-size: 30px; opacity: 0.5; }

.marcador-top .reloj {
  font-family: var(--font-mono);
  font-size: 22px;
  background: rgba(255,255,255,0.12);
  padding: 6px 14px;
  border-radius: 8px;
  margin-left: 12px;
}

.cancha {
  position: relative;
  height: 320px;
  background: repeating-linear-gradient(
    90deg,
    var(--grass) 0px, var(--grass) 60px,
    var(--grass-dark) 60px, var(--grass-dark) 120px
  );
  border-radius: 0 0 16px 16px;
  overflow: hidden;
  border: 4px solid var(--ink);
  border-top: none;
}

.cancha .linea-centro {
  position: absolute;
  top: 0; bottom: 0; left: 50%;
  width: 3px;
  background: var(--grass-line);
  transform: translateX(-50%);
}

.cancha .circulo-centro {
  position: absolute;
  top: 50%; left: 50%;
  width: 130px; height: 130px;
  border: 3px solid var(--grass-line);
  border-radius: 50%;
  transform: translate(-50%, -50%);
}

.cancha .porteria {
  position: absolute;
  top: 50%;
  width: 10px; height: 90px;
  background: repeating-linear-gradient(0deg, var(--grass-line) 0 6px, transparent 6px 12px);
  transform: translateY(-50%);
}
.cancha .porteria.izq { left: 0; }
.cancha .porteria.der { right: 0; }

.gol-toast {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%) scale(0.6);
  background: var(--gold);
  color: #402F06;
  font-family: var(--font-display);
  font-size: 46px;
  padding: 14px 36px;
  border-radius: 14px;
  opacity: 0;
  pointer-events: none;
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

.gol-toast.mostrar {
  animation: golPop 2.1s ease forwards;
}

@keyframes golPop {
  0%   { opacity: 0; transform: translate(-50%, -50%) scale(0.5); }
  15%  { opacity: 1; transform: translate(-50%, -50%) scale(1.08); }
  25%  { transform: translate(-50%, -50%) scale(1); }
  85%  { opacity: 1; }
  100% { opacity: 0; transform: translate(-50%, -60%) scale(0.9); }
}

.controles-host {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 26px;
}

/* --- Reveal / bono / final en host --- */

.pantalla-mensaje {
  text-align: center;
  max-width: 720px;
  padding: 40px;
}

.pantalla-mensaje h2 {
  font-size: clamp(34px, 5vw, 56px);
  color: var(--grass-dark);
  margin-bottom: 18px;
}

.pantalla-mensaje p { font-size: 19px; color: var(--ink-soft); line-height: 1.5; }

.momio-grande {
  font-family: var(--font-mono);
  font-size: 64px;
  color: var(--gold-dark);
  margin: 18px 0;
}

.tabla-jugadores-final {
  display: flex;
  gap: 24px;
  justify-content: center;
  margin-top: 30px;
  flex-wrap: wrap;
}

.tarjeta-final {
  background: var(--card);
  border: 2px solid var(--gold);
  border-radius: 18px;
  padding: 26px 34px;
  text-align: center;
  box-shadow: var(--shadow);
}

.tarjeta-final .nombre { font-family: var(--font-display); font-size: 26px; }
.tarjeta-final .cifra { font-family: var(--font-mono); font-size: 44px; color: var(--grass-dark); margin-top: 6px; }

/* =====================================================================
   JUGADOR (celular)
   ===================================================================== */

#player-app {
  min-height: 100vh;
  max-width: 480px;
  margin: 0 auto;
  padding: 22px 16px 60px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.p-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.p-header h1 { font-size: 30px; color: var(--grass-dark); }

.saldo-chip {
  font-family: var(--font-mono);
  background: var(--ink);
  color: var(--gold);
  padding: 8px 16px;
  border-radius: 999px;
  font-size: 18px;
}

.p-card {
  background: var(--card);
  border: 1.5px solid var(--card-border);
  border-radius: 16px;
  padding: 20px;
  box-shadow: var(--shadow);
}

.p-card h2 { font-size: 22px; margin-bottom: 6px; }
.p-card p.sub { color: var(--ink-soft); font-size: 14px; margin: 0 0 14px; }

input.campo-texto {
  width: 100%;
  padding: 14px 16px;
  border-radius: 12px;
  border: 1.5px solid var(--card-border);
  font-size: 17px;
  font-family: var(--font-body);
  background: var(--bg);
}

.error-txt {
  color: var(--red-dark);
  background: var(--red-bg);
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 14px;
  margin-top: 10px;
}

/* --- Boleto de apuesta por partido --- */

.partido-apuesta {
  border: 1.5px solid var(--card-border);
  border-radius: 14px;
  padding: 16px;
  margin-bottom: 14px;
}

.partido-apuesta .versus {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  font-family: var(--font-display);
  font-size: 22px;
  margin-bottom: 12px;
}

.partido-apuesta .versus .bandera { font-size: 30px; }
.partido-apuesta .versus .vs { font-size: 14px; color: var(--ink-soft); font-family: var(--font-body); }

.opciones-apuesta {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.opciones-resultado {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.opciones-total {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-top: 8px;
}

.subtitulo-opciones {
  font-size: 11px;
  text-transform: uppercase;
  color: var(--ink-soft);
  margin: 10px 0 6px;
  letter-spacing: 0.05em;
  font-weight: 700;
}

.opcion-apuesta {
  background: var(--bg);
  border: 1.5px solid var(--card-border);
  border-radius: 10px;
  padding: 10px 8px;
  font-size: 13px;
  font-weight: 700;
  text-align: center;
  color: var(--ink);
  transition: all 0.12s ease;
}

.opcion-apuesta:hover { border-color: var(--grass); }

.opcion-apuesta.seleccionada {
  background: var(--grass);
  border-color: var(--grass-dark);
  color: #fff;
}

/* --- Parley / seguimiento en vivo --- */

.leg-parley {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 0;
  border-bottom: 1px dashed var(--card-border);
}
.leg-parley:last-child { border-bottom: none; }

.leg-parley .banderas { font-size: 26px; white-space: nowrap; }
.leg-parley .info { flex: 1; }
.leg-parley .info .partido-nombre { font-size: 13px; color: var(--ink-soft); }
.leg-parley .info .apuesta-nombre { font-weight: 700; font-size: 15px; }

.leg-parley .marcador-mini {
  font-family: var(--font-mono);
  font-size: 15px;
  color: var(--ink-soft);
  min-width: 34px;
  text-align: center;
}

/* --- Pantalla de espera --- */

.esperando {
  text-align: center;
  padding: 50px 20px;
}

.balon {
  font-size: 54px;
  display: inline-block;
  animation: rebote 1.1s ease-in-out infinite;
}

@keyframes rebote {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-18px); }
}

.esperando h2 { margin: 16px 0 8px; font-size: 24px; }
.esperando p { color: var(--ink-soft); }

/* --- Resultado final / bono --- */

.resultado-grande {
  text-align: center;
  padding: 20px 0;
}

.resultado-grande .cifra {
  font-family: var(--font-mono);
  font-size: 72px;
  color: var(--red-dark);
}

.resultado-grande .cifra.ganaste { color: var(--grass-dark); }

.confeti-caja { position: relative; overflow: hidden; height: 0; }

.pieza-confeti {
  position: absolute;
  top: -20px;
  width: 10px; height: 16px;
  animation: caer 2.6s linear forwards;
}

@keyframes caer {
  to { transform: translateY(420px) rotate(400deg); opacity: 0.2; }
}

.momio-tag {
  display: inline-block;
  font-family: var(--font-mono);
  background: var(--gold);
  color: #402F06;
  padding: 4px 14px;
  border-radius: 999px;
  font-size: 15px;
  margin-top: 4px;
}
