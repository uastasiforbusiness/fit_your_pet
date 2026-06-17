# Caballo — Proyecto Frontend

Archivo único `index.html` con mockup de teléfono, fondo de paisaje y caballo animado.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `index.html` | Página principal. Mockup de teléfono centrado, paisaje de fondo, caballo SVG superpuesto |
| `horse.svg` | Caballo en SVG generado desde imagen JPG. Contiene la animación CSS interna |
| `background.jpg` | Imagen de paisaje de fondo (teléfono) |

## Animación

El caballo se dibuja progresivamente en **4 segundos** al cargar la página:

- Animación CSS por `stroke-dasharray` + `stroke-dashoffset` con `pathLength="1"`
- Colores: blanco sobre paisaje (`fill: none` → `fill: #ffffff`, `stroke: #ffffff`)
- Sombra: `drop-shadow` para visibilidad en fondos claros
- Se reproduce **una sola vez** al cargar, deja el caballo visible al final

## Cómo ajustar el caballo

Todo el control está en `index.html` en la clase `.horse-container object`:

### Tamaño

Cambiar el valor `scale(X)`:

```css
transform: translateX(-50%) translateY(-35px) scale(0.625);
```

- `0.625` = tamaño actual
- Más grande: `0.78` (25% más grande)
- Más pequeño: `0.47` (25% más pequeño)

### Posición vertical

Ajustar `translateY(-35px)`:

- Valor **negativo** = sube el caballo
- Valor **positivo** = baja el caballo
- `0` = pegado a la base del teléfono

### Color / sombra

Dentro de `horse.svg` en la clase `.draw-path`:

```css
stroke: #ffffff;              /* color del trazo */
fill: #ffffff;                /* color del relleno final */
filter: drop-shadow(...);     /* sombra */
```

## Origen del SVG

El `horse.svg` se generó a partir de un JPG mediante trazado de contornos con `scikit-image` + `measure.find_contours()`. El viewBox está recortado al bounding box exacto del caballo (`82 10 858 1644`) para eliminar espacio vacío y facilitar el posicionamiento.

## Notas técnicas

- Sin JavaScript
- Sin dependencias externas
- Funciona abriendo `index.html` directamente en el navegador
- Animación dentro del SVG: no requiere CSS externo
- El `<object>` carga el SVG externo manteniendo la animación interna
