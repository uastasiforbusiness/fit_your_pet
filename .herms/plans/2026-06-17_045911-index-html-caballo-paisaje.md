# Plan: Ajustar index.html para fondo full-screen y caballo centrado

Status: DRAFT

Fecha: 2026-06-17 04:59

## Goal

Convertir el workspace actual `C:\Users\gabri\Desktop\cavallo` en una demo frontend estática de un solo archivo donde:

- `background.png` o, si no existe, `background.jpg`, cubra toda la ventana del navegador.
- `horse.svg`, ubicado en el mismo workspace, se cargue desde `index.html`.
- El caballo quede centrado de forma responsiva sobre el paisaje.
- La animación dure 4 segundos, se reproduzca una vez al cargar y deje el dibujo visible al final.
- No haya barras de desplazamiento.

## Current context / assumptions

Workspace inspeccionado:

- Ruta activa: `/c/Users/gabri/Desktop/cavallo`
- Archivos presentes:
  - `index.html`
  - `horse.svg`
  - `background.jpg`
- No existe `background.png` en el workspace.
- `index.html` actual renderiza un mockup de teléfono, no una escena full-screen.
- `horse.svg` contiene 18 paths con `fill="#000000"` y `stroke="none"`.
- El workspace no es un repositorio Git: `git remote -v` falla con `fatal: not a git repository`.
- GitNexus está instalado, pero no puede indexar este workspace porque no es repositorio Git.

Assumptions:

- El usuario quiere mantener un único `index.html` con CSS inline.
- Los assets externos deben seguir siendo `background.jpg` y `horse.svg`.
- No se deben modificar ni convertir `horse.svg` ni `background.jpg` en esta fase.
- No se requiere servidor local: debe funcionar abriendo `index.html` directamente en navegador.

## Proposed approach

Reemplazar únicamente `index.html` por una versión limpia de escena full-screen:

1. Usar `html, body` con `width: 100%`, `height: 100%`, `margin: 0`.
2. Aplicar al `body`:
   - `width: 100vw`
   - `height: 100vh`
   - `overflow: hidden`
   - `background-image` en capas:
     - primero `url("background.png")`
     - después `url("background.jpg")` como fallback
   - `background-position: center`
   - `background-size: cover`
   - `background-repeat: no-repeat`
3. Crear un contenedor `.stage` con:
   - `position: fixed`
   - `inset: 0`
   - `display: grid`
   - `place-items: center`
   - `overflow: hidden`
4. Cargar el caballo con una etiqueta HTML externa:
   - Preferencia: `<object data="horse.svg" type="image/svg+xml">`
   - Fallback interno: `<img src="horse.svg" alt="Caballo vectorial" />`
5. Centrar y escalar el caballo de forma responsiva:
   - `max-width: min(72vw, 820px)`
   - `max-height: 78vh`
   - `width: auto`
   - `height: auto`
   - `display: block`
6. Aplicar animación CSS única de 4 segundos:
   - `animation: drawHorse 4s cubic-bezier(...) forwards`
   - usar `clip-path: inset(0 100% 0 0)` a `clip-path: inset(0 0 0 0)` para simular dibujo/revelado fluido.
   - combinar con `opacity`, `transform: scale/translateY` y `filter: blur` para una entrada elegante.
7. No usar JavaScript.
8. No instalar dependencias.
9. No modificar assets.

Nota de diseño: como `horse.svg` es un SVG relleno y no un SVG de trazos con `stroke`, una animación real basada en `stroke-dasharray` no es fiable sin modificar el SVG. La solución más robusta sin tocar `horse.svg` es un reveal CSS tipo dibujo con `clip-path`.

## Step-by-step plan

1. Revisar `index.html` actual y confirmar que solo se cambiará ese archivo.
2. Reescribir `index.html` con:
   - estructura HTML mínima.
   - CSS inline dentro de `<style>`.
   - fondo full-screen con fallback `background.png` / `background.jpg`.
   - contenedor centrado.
   - carga de `horse.svg` mediante `<object>`.
   - animación CSS `drawHorse` de 4 segundos.
3. Verificar que el archivo resultante:
   - no tiene dependencias JS.
   - no modifica `horse.svg`.
   - no modifica `background.jpg`.
   - mantiene los assets en rutas relativas.
4. Validar manualmente en navegador:
   - abrir `index.html`.
   - confirmar que no hay scroll.
   - confirmar que el fondo cubre toda la pantalla.
   - confirmar que el caballo está centrado.
   - confirmar que la animación dura 4 segundos, se ejecuta una vez y deja el caballo visible.
5. Si se detecta un problema visual, ajustar solo CSS de `index.html`.

## Files likely to change

- `C:\Users\gabri\Desktop\cavallo\index.html`

Files that should not change:

- `C:\Users\gabri\Desktop\cavallo\horse.svg`
- `C:\Users\gabri\Desktop\cavallo\background.jpg`
- No se creará `background.png` en esta fase.

## Tests / validation

Validación estática:

- `read_file index.html`
  - confirmar que el CSS está dentro de `<style>`.
  - confirmar que el fondo usa `background-size: cover`, `background-position: center` y `overflow: hidden`.
  - confirmar que `horse.svg` se carga con `<object data="horse.svg">`.
  - confirmar que la animación usa `4s` y `forwards`.

Validación visual:

- Abrir `file:///C:/Users/gabri/Desktop/cavallo/index.html` en Chrome/Edge.
- Confirmar visualmente:
  - sin barras de desplazamiento.
  - fondo cubriendo toda la ventana.
  - caballo centrado.
  - animación de 4 segundos.
  - estado final visible.

Validación opcional con herramientas del navegador:

- Navegar a `file:///C:/Users/gabri/Desktop/cavallo/index.html`.
- Inspeccionar estilos aplicados al `body`, `.stage` y `.horse`.
- Confirmar que no hay errores de carga de assets en consola.

## DRY-RUN VERIFICATION

| Check | Command | Result | Impact |
|---|---|---|---|
| Workspace activo | `pwd` | `/c/Users/gabri/Desktop/cavallo` | Plan apunta al workspace correcto. |
| Archivos del workspace | `search_files(target="files", pattern="*")` | `index.html`, `horse.svg`, `background.jpg` | No existe `background.png`; se usará fallback a `.jpg`. |
| Estado actual de index.html | `read_file index.html` | Renderiza mockup de teléfono, no full-screen | Se debe reescribir `index.html`. |
| Estado de horse.svg | `read_file horse.svg` | SVG con 18 paths rellenos, sin strokes | `stroke-dasharray` no es fiable; usar `clip-path` reveal. |
| Tamaño de assets | `stat -c '%n %s bytes' index.html horse.svg background.jpg` | Archivos presentes; `background.jpg` pesa 97888 bytes | Assets válidos para validación local. |
| Git instalado | `which git && git --version` | `git version 2.54.0.windows.1` | Git disponible, pero no hay repo. |
| Remote Git | `git remote -v` | `fatal: not a git repository` | No se planifica commit, diff Git ni push. |
| GitNexus instalado | `which gitnexus` | `/c/Users/gabri/AppData/Roaming/npm/gitnexus` | Herramienta disponible. |
| GitNexus status | `gitnexus status` | `Not a git repository.` | No se puede usar indexado porque no es repo Git. |
| Help git status | `git status -h` | Muestra opciones de `git status` | Comando validado si luego se necesita estado local. |
| Help git remote | `git remote -h` | Muestra opciones de `git remote` | Comando validado, aunque no hay remote. |
| Help gitnexus status | `gitnexus status --help` | Muestra `Usage: gitnexus status [options]` | Comando validado. |
| Help stat | `stat --help` | Muestra opciones de `stat` | Comando validado para inspección de archivos. |

## Web research

No aplica. Es un plan de diseño frontend estático sin dependencias externas, frameworks ni CLIs de terceros.

## Risks, tradeoffs, and open questions

Riesgos:

- Si `horse.svg` tiene fondo blanco incrustado, puede tapar parte del paisaje.
- Si `background.jpg` no es landscape, `background-size: cover` puede recortar zonas.
- `clip-path` puede no estar disponible en navegadores muy antiguos.

Tradeoffs:

- `clip-path` reveal funciona con cualquier SVG cargado externamente.
- `stroke-dasharray` sería más literal, pero requiere modificar o convertir `horse.svg` a trazos.

Open questions:

- Si el usuario exige una animación estrictamente de trazos, habrá que convertir `horse.svg` a paths con stroke o incrustar una versión preparada para `stroke-dasharray`.
- Si aparece `background.png`, el CSS lo usará primero automáticamente.
