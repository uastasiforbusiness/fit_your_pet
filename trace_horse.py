import numpy as np
from PIL import Image
from skimage import measure

img = Image.open(r"C:\Users\gabri\Downloads\d63dc172af2d7c1e65a9f9e6234997d2.jpg").convert('L')
arr = np.array(img)
h, w = arr.shape
print(f"Image size: {w}x{h}")

# Invert: black lines become bright
arr_inv = 255 - arr

# Trace contours at threshold - lower for anti-aliased lines
thresh = 40
contours = measure.find_contours(arr_inv, level=thresh)
print(f"Found {len(contours)} contour segments at level {thresh}")

# Filter small noise - keep more for details
min_len = 8
contours = [c for c in contours if len(c) >= min_len]
print(f"After filtering (min_len={min_len}): {len(contours)} segments")

# Generate SVG paths
lines = []
for i, contour in enumerate(contours):
    pts = contour.tolist()
    path_d = "M " + " L ".join([f"{p[1]:.1f},{p[0]:.1f}" for p in pts])
    lines.append(f'<path class="draw-path" pathLength="1" d="{path_d}"/>')

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%">
<style>
  .draw-path {{
    fill: none;
    stroke: #ffffff;
    stroke-width: 3;
    stroke-linecap: round;
    stroke-linejoin: round;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
    stroke-dasharray: 1;
    stroke-dashoffset: 1;
    animation: drawHorse 4s cubic-bezier(0.22,1,0.36,1) forwards;
  }}
  @keyframes drawHorse {{
    0% {{ stroke-dashoffset: 1; opacity: 0; }}
    15% {{ opacity: 1; }}
    100% {{ stroke-dashoffset: 0; opacity: 1; }}
  }}
</style>
<g>
{chr(10).join(lines)}
</g>
</svg>'''

with open("horse.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print(f"Done: {len(lines)} paths -> horse.svg")