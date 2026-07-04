# ⚽ Quiniela de cumpleaños

Una "quiniela" tipo Kahoot para jugar en una fiesta: se proyecta en la tele,
los invitados apuestan desde su celular escaneando un QR, y al final
(sin que ellos lo sepan) el anfitrión se asegura de que ambos terminen
con $100 de saldo para el regalo en efectivo.

## Cómo funciona el guion de la noche

1. Abres `/anfitrion` en el navegador de tu laptop y lo conectas a la tele.
   Ahí aparece un código QR.
2. Arzola y Yivy escanean el QR desde su celular, entran a `/jugar` y
   escriben su nombre (si escriben "Arzola" o "Yivy" el sistema los
   reconoce automáticamente; si escriben otra cosa, se les asigna el
   primer lugar libre).
3. Cuando ambos están dentro, presionas **"Comenzar apuestas"**. A cada
   quien le aparecen sus 3 partidos en el celular con $10 de saldo,
   arman su "parley" (un pronóstico por partido) y confirman.
4. Presionas **"Comenzar partidos"** y vas pasando partido por partido
   con los botones **"Iniciar partido"** / **"Siguiente partido"**. La
   tele anima el marcador, el reloj y los goles; el celular de cada
   quien se va actualizando solo.
5. Los primeros 2 pronósticos de cada quien siempre se cumplen. El
   tercero (el último de su lista) está programado para fallar sin
   importar qué hayan elegido, así que su parley completo se rompe y
   se quedan en $0 — como en un parley real, si una pata pierde, se
   pierde todo.
6. Aparece la pantalla **"La casa nunca pierde… ¿una última
   oportunidad?"**. Presionas **"Dar la última oportunidad"**: a cada
   quien se le regala $1 para apostarlo en Francia 🇫🇷 vs Argentina 🇦🇷,
   a un momio de +9900. No importa qué resultado escojan, están
   programados para ganar esa apuesta.
7. Reproduces ese último partido y presionas **"Revelar premio"**: su
   $1 se convierte automáticamente en $100. Ahí les entregas su premio
   en efectivo. 🎉

Puedes usar el botón **"Reiniciar partida"** al final para ensayar todo
las veces que quieras antes de la fiesta (borra jugadores y resultados,
no borra la configuración).

## Estructura del proyecto

```
Code/
├── app.py            Rutas de Flask (páginas + API)
├── config.py         Nombres de jugadores, partidos, momios, etc.
├── db.py             Acceso a SQLite (sin ORM)
├── game_logic.py      Generador de marcadores y resolución de apuestas
├── requirements.txt
├── static/
│   ├── css/style.css
│   └── js/{host.js, player.js}
└── templates/
    ├── host.html      Pantalla de TV
    └── player.html    Pantalla de celular
```

Todo el "truco" del juego vive en `game_logic.py` y en `config.py`
(`INDICE_PARTIDO_TRUCO`, `PARTIDOS_POR_SLOT`, `MOMIO_BONO`). Si algún
día quieres cambiar los equipos, los nombres de los invitados o el
saldo inicial, solo edita `config.py`.

## Probarlo en tu computadora antes de subirlo

```bash
cd Code
python3 -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abre `http://localhost:5000/anfitrion` en una pestaña (esa es la tele)
y `http://localhost:5000/jugar` en otra o desde tu celular conectado a
la misma red Wi-Fi usando la IP de tu computadora, por ejemplo
`http://192.168.1.50:5000/jugar`.

## Subirlo a PythonAnywhere

1. Sube la carpeta `Code` a un repositorio de GitHub (o cualquier
   método que prefieras para subir archivos).
2. En PythonAnywhere: **Web → Add a new web app → Flask** (elige la
   versión de Python que tengas disponible, cualquier 3.10+ funciona).
3. En la consola de PythonAnywhere (**Bash console**):
   ```bash
   git clone https://github.com/tu-usuario/tu-repo.git
   cd tu-repo
   pip install --user -r requirements.txt
   ```
4. En la pestaña **Web**, en "Code", apunta:
   - **Source code**: la carpeta donde clonaste el repo (donde está `app.py`).
   - **Working directory**: la misma carpeta.
5. Abre el archivo WSGI que te da PythonAnywhere (el link está en la
   misma pestaña Web) y reemplaza su contenido por algo como:
   ```python
   import sys
   path = '/home/tu-usuario/tu-repo'
   if path not in sys.path:
       sys.path.insert(0, path)

   from app import app as application
   ```
6. Presiona **Reload** en la pestaña Web. Tu sitio quedará en
   `https://tu-usuario.pythonanywhere.com`. El QR y las rutas usan URLs
   relativas al dominio actual, así que no necesitas configurar nada
   más: `https://tu-usuario.pythonanywhere.com/anfitrion` para la tele
   y el QR llevará automáticamente a `/jugar`.

> Nota: la cuenta gratuita de PythonAnywhere reinicia la app cada
> cierto tiempo de inactividad, lo cual está bien aquí porque el estado
> vive en SQLite, no en memoria — si la app se reinicia a mitad de la
> partida, el progreso no se pierde.

## Personalizar para otra fiesta

Todo se controla desde `config.py`:

- `JUGADORES_ESPERADOS`: nombres de los dos invitados.
- `PARTIDOS` / `PARTIDO_BONO`: equipos y banderas (usa emojis).
- `SALDO_INICIAL`, `SALDO_BONO`, `MOMIO_BONO`: los montos del "truco".
- `MS_POR_MINUTO`: qué tan rápido corre la animación de cada partido
  (160 ms por minuto ≈ 14 segundos por partido).
