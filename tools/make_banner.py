#!/usr/bin/env python3
"""
Low-poly Delaunay banner generator for the MIT self-study site.

Produces a wide SVG of flat-shaded triangles whose colours follow a
left-to-right gradient (darkest on the left, where the page title sits, so
white banner text stays legible). One banner per course, written to that
course's folder as `banner.svg` and wired via its `_metadata.yml`:

    title-block-banner: banner.svg
    title-block-banner-color: white

The SVG is a *static* asset committed to the repo — this script is not run
in CI. Deps: numpy, matplotlib (already in requirements.txt).

Add a course = add one line to COURSES below, then run:
    python tools/make_banner.py            # regenerate every course banner
    python tools/make_banner.py --preview  # also drop a PNG in tools/ to eyeball
"""
import argparse
import numpy as np
import matplotlib.tri as mtri

# Colour presets (anchors dark -> light, left -> right). Pick one per course.
PRESETS = {
    "blue":   ["#0b1b34", "#16336b", "#1e40af", "#0891b2"],
    "indigo": ["#120a2b", "#312e81", "#5b21b6", "#7c3aed"],
    "teal":   ["#04211f", "#0f5f5a", "#0d9488", "#22d3ee"],
}

# One entry per course. `seed` just fixes the (otherwise random) triangulation.
COURSES = {
    "18.02": {"preset": "blue", "out": "courses/18.02/banner.svg", "seed": 1802},
    # "8.01SC": {"preset": "teal", "out": "courses/8.01SC/banner.svg", "seed": 801},
}

def hex_to_rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)], dtype=float)

def lerp_palette(anchors, t):
    n = len(anchors) - 1
    t = min(max(t, 0.0), 1.0) * n
    i = min(int(t), n - 1)
    f = t - i
    return anchors[i] * (1 - f) + anchors[i + 1] * f

def build_svg(anchors_hex, W=1600, H=420, cols=20, rows=7,
              jitter=0.42, seed=0, edges=True):
    rng = np.random.default_rng(seed)
    # jittered grid + exact corners so the convex hull covers the whole rect
    xs, ys = [], []
    for j in range(rows + 1):
        for i in range(cols + 1):
            x = i / cols * W
            y = j / rows * H
            if i not in (0, cols):
                x += (rng.random() * 2 - 1) * jitter * (W / cols)
            if j not in (0, rows):
                y += (rng.random() * 2 - 1) * jitter * (H / rows)
            xs.append(min(max(x, 0), W)); ys.append(min(max(y, 0), H))
    x, y = np.array(xs), np.array(ys)
    tri = mtri.Triangulation(x, y)
    anchors = [hex_to_rgb(c) for c in anchors_hex]

    polys = []
    for a, b, c in tri.triangles:
        cx = (x[a] + x[b] + x[c]) / 3.0
        cy = (y[a] + y[b] + y[c]) / 3.0
        t = 0.82 * (cx / W) + 0.18 * (cy / H)          # mostly horizontal
        rgb = lerp_palette(anchors, t) * (1.0 + (rng.random() * 2 - 1) * 0.075)
        rgb = np.clip(rgb, 0, 255).astype(int)
        fill = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        pts = f"{x[a]:.0f},{y[a]:.0f} {x[b]:.0f},{y[b]:.0f} {x[c]:.0f},{y[c]:.0f}"
        polys.append(f'<polygon points="{pts}" fill="{fill}"/>')

    g = ('<g stroke="#ffffff" stroke-opacity="0.05" stroke-width="0.6">'
         if edges else '<g>')
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'preserveAspectRatio="xMidYMid slice" role="img" '
        f'aria-label="Low-poly geometric banner">'
        f'<rect width="{W}" height="{H}" fill="{anchors_hex[0]}"/>'
        f'{g}{"".join(polys)}</g></svg>\n'
    ), (x, y, tri)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true")
    args = ap.parse_args()
    for course, cfg in COURSES.items():
        svg, (x, y, tri) = build_svg(PRESETS[cfg["preset"]], seed=cfg["seed"])
        with open(cfg["out"], "w") as fh:
            fh.write(svg)
        print(f"wrote {cfg['out']}  ({len(svg)//1024+1} KB, "
              f"{len(tri.triangles)} triangles, preset={cfg['preset']})")
        if args.preview:
            import matplotlib; matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            from matplotlib.patches import Polygon
            from matplotlib.collections import PatchCollection
            # re-read fills from the SVG we just built would be overkill;
            # simplest: rebuild colours deterministically is skipped — just
            # rasterize via a quick fill using the same geometry & a flat map.
            fig, ax = plt.subplots(figsize=(16, 4.2), dpi=70)
            ax.triplot(tri, color="#ffffff", lw=0.3, alpha=0.15)
            ax.set_xlim(0, 1600); ax.set_ylim(420, 0); ax.axis("off")
            p = f"tools/preview-{course}.png"
            fig.savefig(p, bbox_inches="tight", pad_inches=0); plt.close(fig)
            print("   wrote", p, "(geometry only; open the .svg for true colours)")

if __name__ == "__main__":
    main()
