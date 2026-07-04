<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Quiniela de cumpleaños — Anfitrión</title>
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
<div id="host-app">

  <div class="host-header">
    <h1>⚽ Quiniela del cumpleaños</h1>
    <span class="marca">MODO ANFITRIÓN</span>
  </div>

  <!-- ============ LOBBY ============ -->
  <section id="vista-lobby">
    <div class="lobby">
      <div class="qr-caja">
        <h2>Escanea para entrar</h2>
        <img id="qr-img" src="" alt="Código QR para unirse a la quiniela">
        <p class="url">{{ join_url }}</p>
      </div>
      <div class="lista-jugadores" id="lista-jugadores">
        <!-- se llena por JS -->
      </div>
    </div>
    <div class="controles-host">
      <button class="btn btn-primario" id="btn-iniciar-apuestas" disabled>Comenzar apuestas</button>
    </div>
  </section>

  <!-- ============ BETTING (esperando a que apuesten) ============ -->
  <section id="vista-apostando" class="oculto">
    <div class="pantalla-mensaje">
      <h2>Armando su parley…</h2>
      <p>Cada quien está eligiendo sus 3 pronósticos en su celular.</p>
    </div>
    <div class="lista-jugadores" id="lista-jugadores-apostando"></div>
    <div class="controles-host">
      <button class="btn btn-primario" id="btn-comenzar-partidos" disabled>Comenzar partidos</button>
    </div>
  </section>

  <!-- ============ PARTIDO EN VIVO ============ -->
  <section id="vista-jugando" class="oculto">
    <div class="cancha-wrap">
      <div class="marcador-top">
        <div class="equipo"><span class="bandera" id="j-bandera1"></span><span id="j-nombre1"></span></div>
        <div class="goles" id="j-goles1">0</div>
        <div class="separador">:</div>
        <div class="goles" id="j-goles2">0</div>
        <div class="equipo"><span id="j-nombre2"></span><span class="bandera" id="j-bandera2"></span></div>
        <div class="reloj" id="j-reloj">00:00</div>
      </div>
      <div class="cancha" id="cancha">
        <div class="linea-centro"></div>
        <div class="circulo-centro"></div>
        <div class="porteria izq"></div>
        <div class="porteria der"></div>
        <div class="gol-toast" id="gol-toast">¡GOOOL!</div>
      </div>
    </div>
    <div class="controles-host">
      <button class="btn btn-primario" id="btn-reproducir">Iniciar partido</button>
      <button class="btn btn-oro oculto" id="btn-siguiente">Siguiente partido</button>
    </div>
  </section>

  <!-- ============ ANUNCIO "LA CASA NUNCA PIERDE" ============ -->
  <section id="vista-bono-intro" class="oculto">
    <div class="pantalla-mensaje">
      <h2>La casa nunca pierde…</h2>
      <p>pero, ¿una última oportunidad?</p>
    </div>
    <div class="controles-host">
      <button class="btn btn-oro" id="btn-revelar-bono">Dar la última oportunidad</button>
    </div>
  </section>

  <!-- ============ ESPERANDO APUESTA BONO ============ -->
  <section id="vista-bono-apuestas" class="oculto">
    <div class="pantalla-mensaje">
      <h2 style="color:var(--gold-dark)">Francia 🇫🇷 vs Argentina 🇦🇷</h2>
      <p>Un peso, momio +9900. Cualquier resultado paga igual.</p>
    </div>
    <div class="lista-jugadores" id="lista-jugadores-bono"></div>
    <div class="controles-host">
      <button class="btn btn-primario" id="btn-comenzar-bono" disabled>Jugar el partido final</button>
    </div>
  </section>

  <!-- ============ PARTIDO BONO EN VIVO ============ -->
  <section id="vista-bono-jugando" class="oculto">
    <div class="cancha-wrap">
      <div class="marcador-top">
        <div class="equipo"><span class="bandera" id="b-bandera1"></span><span id="b-nombre1"></span></div>
        <div class="goles" id="b-goles1">0</div>
        <div class="separador">:</div>
        <div class="goles" id="b-goles2">0</div>
        <div class="equipo"><span id="b-nombre2"></span><span class="bandera" id="b-bandera2"></span></div>
        <div class="reloj" id="b-reloj">00:00</div>
      </div>
      <div class="cancha" id="cancha-bono">
        <div class="linea-centro"></div>
        <div class="circulo-centro"></div>
        <div class="porteria izq"></div>
        <div class="porteria der"></div>
        <div class="gol-toast" id="gol-toast-bono">¡GOOOL!</div>
      </div>
    </div>
    <div class="controles-host">
      <button class="btn btn-primario" id="btn-reproducir-bono">Iniciar partido final</button>
      <button class="btn btn-oro oculto" id="btn-finalizar-bono">Revelar premio</button>
    </div>
  </section>

  <!-- ============ FINAL ============ -->
  <section id="vista-final" class="oculto">
    <div class="pantalla-mensaje">
      <h2>¡Feliz cumpleaños! 🎉</h2>
      <p>Que empiece la entrega de premios.</p>
    </div>
    <div class="tabla-jugadores-final" id="tabla-final"></div>
    <div class="controles-host" style="margin-top:40px;">
      <button class="btn btn-fantasma" id="btn-reiniciar">Reiniciar partida (nueva ronda)</button>
    </div>
  </section>

</div>

<script id="config-datos" type="application/json">{{ nombres_esperados | tojson }}</script>
<script>
  document.getElementById('qr-img').src =
    "https://api.qrserver.com/v1/create-qr-code/?size=260x260&data=" + encodeURIComponent("{{ join_url }}");
</script>
<script src="{{ url_for('static', filename='js/host.js') }}"></script>
</body>
</html>
