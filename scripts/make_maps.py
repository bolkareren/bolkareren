"""Generate two mock dungeon maps of the pokemon-training history.

grid_map.svg  - top-down grid map, parchment and ink (old-school module style)
cave_map.svg  - hand-drawn cave, dark stone
"""

import math
import random
from pathlib import Path

OUT = Path(__file__).parent.parent / "assets"
W, H = 900, 700

# name, value, x, y, w, h, kind  (kind: main / trap / side / final)
ROOMS = {
	1: ("ResNet head", "the entrance", 60, 110, 160, 80, "main"),
	2: ("Unfreeze sweeps", "leaky folds", 280, 110, 160, 80, "main"),
	3: ("The mimic", "0.906, discarded", 500, 110, 160, 80, "trap"),
	4: ("Clean restart", "0.596", 280, 270, 160, 80, "main"),
	5: ("Backbone sweeps", "0.677, plus SDT", 500, 270, 160, 80, "main"),
	6: ("LR schedule", "0.716", 720, 270, 160, 80, "main"),
	7: ("Fold bug", "re-baseline 0.759", 720, 430, 160, 80, "trap"),
	8: ("Full unfreeze", "0.760", 500, 430, 160, 80, "main"),
	9: ("6-view TTA", "0.778", 280, 430, 160, 80, "main"),
	10: ("Final ensemble", "0.833 held-out", 250, 570, 220, 90, "final"),
	11: ("Classical floor", "0.285", 60, 270, 160, 80, "side"),
	12: ("DINOv2 heads", "0.618, frozen backbone", 60, 430, 160, 80, "side"),
}

CORRIDORS = [  # main path
	[(220, 150), (280, 150)],
	[(440, 150), (500, 150)],
	[(440, 310), (500, 310)],
	[(660, 310), (720, 310)],
	[(800, 350), (800, 430)],
	[(720, 470), (660, 470)],
	[(500, 470), (440, 470)],
	[(360, 510), (360, 570)],
	[(280, 310), (220, 310)],
]
SECRET = [[(140, 350), (140, 430)]]  # side passage
CHUTE = [(647, 190), (647, 232), (360, 232), (360, 270)]  # mimic trapdoor
# Null experiments, each branching off the room it was tested from.
DEAD_ENDS = [
	[(410, 350), (440, 372), (468, 382)],  # off 4, clean restart
	[(760, 510), (760, 550), (740, 585)],  # off 7, fold bug
	[(840, 510), (840, 545), (858, 580)],  # off 7, fold bug
	[(600, 510), (600, 545), (620, 580)],  # off 8, full unfreeze
]
# label text and anchor for each dead end, in the same order
DEAD_LABELS = [
	("augmentation", 472, 412),
	("pose variants", 740, 612),
	("aspect crop", 858, 607),
	("mono stem", 620, 607),
]


def centre(n):
	_, _, x, y, w, h, _ = ROOMS[n]
	return x + w / 2, y + h / 2


def pts(p):
	return " ".join(f"{x:.1f},{y:.1f}" for x, y in p)


# ---------------------------------------------------------------- grid map

def grid_map():
	ink, paper, room_paper, red = "#3b2a1a", "#efe1bf", "#f8efd8", "#9e2a1f"
	s = []
	s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Georgia, \'Times New Roman\', serif">')
	s.append(f"""<defs>
<pattern id="bg" width="20" height="20" patternUnits="userSpaceOnUse">
<rect width="20" height="20" fill="{paper}"/><path d="M20 0H0V20" fill="none" stroke="#d8c59a" stroke-width="0.6"/></pattern>
<pattern id="rm" width="20" height="20" patternUnits="userSpaceOnUse">
<rect width="20" height="20" fill="{room_paper}"/><path d="M20 0H0V20" fill="none" stroke="#c9b48a" stroke-width="0.8"/></pattern>
<pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<line x1="0" y1="0" x2="0" y2="6" stroke="{ink}" stroke-width="1.4"/></pattern>
</defs>""")
	s.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
	s.append(f'<rect x="8" y="8" width="{W-16}" height="{H-16}" fill="none" stroke="{ink}" stroke-width="2"/>')
	s.append(f'<rect x="14" y="14" width="{W-28}" height="{H-28}" fill="none" stroke="{ink}" stroke-width="0.8"/>')

	# rock hatching around rooms and corridors, the classic module look
	for n, (_, _, x, y, w, h, _) in ROOMS.items():
		s.append(f'<rect x="{x-8}" y="{y-8}" width="{w+16}" height="{h+16}" fill="url(#hatch)" opacity="0.35"/>')

	# rooms
	for n, (name, val, x, y, w, h, kind) in ROOMS.items():
		sw = 4 if kind != "side" else 3
		s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#rm)" stroke="{ink}" stroke-width="{sw}"/>')

	# corridors cut through walls: ink first, then paper on top
	def corridor(p, dash=None):
		d = f' stroke-dasharray="{dash}"' if dash else ""
		s.append(f'<polyline points="{pts(p)}" fill="none" stroke="{ink}" stroke-width="22" stroke-linecap="butt" stroke-linejoin="miter"/>')
		s.append(f'<polyline points="{pts(p)}" fill="none" stroke="{room_paper}" stroke-width="16" stroke-linecap="square" stroke-linejoin="miter"/>')
		s.append(f'<polyline points="{pts(p)}" fill="none" stroke="#c9b48a" stroke-width="0.8"{d}/>')

	for c in CORRIDORS:
		corridor(c)
	for c in DEAD_ENDS:
		(px, py), (ex, ey) = c[-2], c[-1]
		L = math.dist((px, py), (ex, ey))
		ux, uy = (ex - px) / L, (ey - py) / L
		s.append(f'<polyline points="{pts(c)}" fill="none" stroke="{ink}" stroke-width="22" stroke-linecap="butt" stroke-linejoin="miter"/>')
		s.append(f'<line x1="{ex}" y1="{ey}" x2="{ex+ux*4:.1f}" y2="{ey+uy*4:.1f}" stroke="{ink}" stroke-width="22"/>')
		s.append(f'<polyline points="{pts([(c[0][0], c[0][1] - 8)] + c[1:])}" fill="none" stroke="{room_paper}" stroke-width="16" stroke-linecap="butt" stroke-linejoin="miter"/>')
	# secret passage: dotted single line, the old-school "S" door
	for c in SECRET:
		s.append(f'<polyline points="{pts(c)}" fill="none" stroke="{ink}" stroke-width="2.5" stroke-dasharray="3 5"/>')
		mx, my = c[0][0], (c[0][1] + c[1][1]) / 2
		s.append(f'<text x="{mx+10}" y="{my+5}" font-size="15" font-style="italic" fill="{ink}">S</text>')

	# doors: small filled rectangles across each main corridor
	for c in CORRIDORS:
		(x1, y1), (x2, y2) = c[0], c[-1]
		mx, my = (x1 + x2) / 2, (y1 + y2) / 2
		if y1 == y2:
			s.append(f'<rect x="{mx-3}" y="{my-9}" width="6" height="18" fill="{ink}"/>')
		else:
			s.append(f'<rect x="{mx-9}" y="{my-3}" width="18" height="6" fill="{ink}"/>')

	# rubble at the dead ends
	rnd = random.Random(7)
	for c in DEAD_ENDS:
		ex, ey = c[-1]
		px, py = c[-2]
		L = math.dist((px, py), (ex, ey))
		ux, uy = (ex - px) / L, (ey - py) / L
		for k in range(6):
			t = rnd.uniform(0, 14)
			off = rnd.uniform(-5, 5)
			rx, ry = ex - ux * t - uy * off, ey - uy * t + ux * off
			s.append(f'<circle cx="{rx:.1f}" cy="{ry:.1f}" r="{rnd.uniform(1.8, 3.2):.1f}" fill="none" stroke="{ink}" stroke-width="1.2"/>')

	# trapdoor chute from the mimic back to the clean restart
	s.append(f'<polyline points="{pts(CHUTE)}" fill="none" stroke="{red}" stroke-width="2.5" stroke-dasharray="8 5"/>')
	s.append(f'<polygon points="354,258 366,258 360,268" fill="{red}"/>')
	s.append(f'<text x="480" y="226" text-anchor="middle" font-size="13" font-style="italic" fill="{red}">trapdoor, back to the start</text>')
	s.append(f'<rect x="639" y="166" width="16" height="16" fill="none" stroke="{red}" stroke-width="2"/><line x1="639" y1="166" x2="655" y2="182" stroke="{red}" stroke-width="2"/><line x1="655" y1="166" x2="639" y2="182" stroke="{red}" stroke-width="2"/>')

	# labels
	for n, (name, val, x, y, w, h, kind) in ROOMS.items():
		col = red if kind == "trap" else ink
		cx = x + w / 2
		s.append(f'<circle cx="{x+16}" cy="{y+16}" r="10" fill="{room_paper}" stroke="{col}" stroke-width="1.5"/>')
		s.append(f'<text x="{x+16}" y="{y+20.5}" text-anchor="middle" font-size="12" font-weight="bold" fill="{col}">{n}</text>')
		s.append(f'<text x="{cx}" y="{y+h/2+2}" text-anchor="middle" font-size="16" font-weight="bold" fill="{col}">{name}</text>')
		s.append(f'<text x="{cx}" y="{y+h/2+22}" text-anchor="middle" font-size="13" font-style="italic" fill="{col}">{val}</text>')

	for name, lx, ly in DEAD_LABELS:
		s.append(f'<text x="{lx}" y="{ly}" text-anchor="middle" font-size="12" font-style="italic" fill="{ink}">{name}</text>')

	# title cartouche and compass
	s.append(f'<rect x="250" y="30" width="400" height="52" fill="{room_paper}" stroke="{ink}" stroke-width="2"/>')
	s.append(f'<text x="450" y="58" text-anchor="middle" font-size="24" font-weight="bold" letter-spacing="2" fill="{ink}">THE SILHOUETTE TRIAL</text>')
	s.append(f'<text x="450" y="75" text-anchor="middle" font-size="12" font-style="italic" fill="{ink}">151 classes, 17 to 23 July 2026</text>')
	s.append(f'<g transform="translate(830,70)" fill="{ink}"><polygon points="0,-30 6,0 0,30 -6,0"/><polygon points="-30,0 0,-5 30,0 0,5" opacity="0.5"/><text y="-36" text-anchor="middle" font-size="12" font-weight="bold">N</text></g>')
	s.append("</svg>")
	return "\n".join(s)


# ---------------------------------------------------------------- cave map

def blob(x, y, w, h, rnd, n=40, rough=7):
	"""Irregular closed outline around a rounded rectangle."""
	cx, cy = x + w / 2, y + h / 2
	out = []
	for i in range(n):
		a = 2 * math.pi * i / n
		# superellipse gives a squarish cave chamber rather than an oval
		ex = abs(math.cos(a)) ** 0.5 * (1 if math.cos(a) >= 0 else -1)
		ey = abs(math.sin(a)) ** 0.5 * (1 if math.sin(a) >= 0 else -1)
		r = 1 + rnd.uniform(-1, 1) * rough / min(w, h)
		out.append((cx + ex * w / 2 * r, cy + ey * h / 2 * r))
	return out


def smooth_path(p):
	"""Closed Catmull-Rom spline through the points, as cubic beziers."""
	n = len(p)
	d = f"M{p[0][0]:.1f},{p[0][1]:.1f}"
	for i in range(n):
		p0, p1, p2, p3 = p[i - 1], p[i], p[(i + 1) % n], p[(i + 2) % n]
		c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
		c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
		d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
	return d + "Z"


def wobble(p, rnd, step=14, amp=4):
	"""Subdivide a polyline and jitter it so tunnels meander."""
	out = [p[0]]
	for (x1, y1), (x2, y2) in zip(p, p[1:]):
		k = max(1, int(math.dist((x1, y1), (x2, y2)) / step))
		for j in range(1, k + 1):
			t = j / k
			jx = rnd.uniform(-amp, amp) if j < k else 0
			jy = rnd.uniform(-amp, amp) if j < k else 0
			out.append((x1 + (x2 - x1) * t + jx, y1 + (y2 - y1) * t + jy))
	return out


def cave_map():
	rock, floor, wall, text, dim = "#16120f", "#2e2620", "#c8b083", "#ecdcb4", "#b19d74"
	red, gold, violet = "#e0533d", "#e8b34a", "#a99ad8"
	rnd = random.Random(11)
	s = []
	s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Georgia, \'Times New Roman\', serif">')
	s.append(f"""<defs>
<filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="4"/>
<feDisplacementMap in="SourceGraphic" scale="6"/></filter>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" seed="2"/>
<feColorMatrix values="0 0 0 0 0.8  0 0 0 0 0.7  0 0 0 0 0.5  0 0 0 0.06 0"/></filter>
</defs>""")
	s.append(f'<rect width="{W}" height="{H}" fill="{rock}"/>')
	s.append(f'<rect width="{W}" height="{H}" filter="url(#grain)"/>')


	tunnels = [wobble(c, rnd) for c in CORRIDORS]
	deads = [wobble(c, rnd, amp=5) for c in DEAD_ENDS]
	secret = [wobble(c, rnd, amp=3) for c in SECRET]
	chambers = {n: blob(x, y, w, h, rnd) for n, (_, _, x, y, w, h, _) in ROOMS.items()}

	# walls: everything drawn fat in wall colour, then floor drawn slimmer on top,
	# so the walls only remain as an outline. Roughened by the displacement filter.
	s.append('<g filter="url(#rough)">')
	for t in tunnels + deads:
		s.append(f'<polyline points="{pts(t)}" fill="none" stroke="{wall}" stroke-width="27" stroke-linecap="round" stroke-linejoin="round"/>')
	for t in secret:
		s.append(f'<polyline points="{pts(t)}" fill="none" stroke="{wall}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>')
	for n, p in chambers.items():
		s.append(f'<path d="{smooth_path(p)}" fill="{wall}" stroke="{wall}" stroke-width="6"/>')
	for t in tunnels + deads:
		s.append(f'<polyline points="{pts(t)}" fill="none" stroke="{floor}" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>')
	for t in secret:
		s.append(f'<polyline points="{pts(t)}" fill="none" stroke="{floor}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
	for n, p in chambers.items():
		s.append(f'<path d="{smooth_path(p)}" fill="{floor}"/>')
	s.append("</g>")

	# collapsed ends: a few boulders
	for c in DEAD_ENDS:
		ex, ey = c[-1]
		for _ in range(5):
			bx, by, r = ex + rnd.uniform(-8, 8), ey + rnd.uniform(-8, 8), rnd.uniform(3, 6)
			s.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="{r:.1f}" fill="#5a4c3c" stroke="{wall}" stroke-width="0.8"/>')

	# trapdoor chute
	s.append(f'<polyline points="{pts(CHUTE)}" fill="none" stroke="{red}" stroke-width="2.2" stroke-dasharray="7 6" opacity="0.9"/>')
	s.append(f'<polygon points="354,258 366,258 360,268" fill="{red}"/>')
	s.append(f'<text x="480" y="225" text-anchor="middle" font-size="13" font-style="italic" fill="{red}">trapdoor, back to the start</text>')


	colours = {"main": (text, dim), "trap": (red, "#f0a090"), "final": (gold, "#f3d48e"), "side": (violet, "#c9c0ea")}
	for n, (name, val, x, y, w, h, kind) in ROOMS.items():
		tc, vc = colours[kind]
		cx = x + w / 2
		s.append(f'<text x="{x+18}" y="{y+22}" text-anchor="middle" font-size="12" fill="{vc}" opacity="0.8">{n}</text>')
		s.append(f'<text x="{cx}" y="{y+h/2+2}" text-anchor="middle" font-size="16" font-weight="bold" fill="{tc}">{name}</text>')
		s.append(f'<text x="{cx}" y="{y+h/2+22}" text-anchor="middle" font-size="13" font-style="italic" fill="{vc}">{val}</text>')

	for name, lx, ly in DEAD_LABELS:
		s.append(f'<text x="{lx}" y="{ly}" text-anchor="middle" font-size="12" font-style="italic" fill="{dim}">{name}</text>')
	s.append(f'<text x="150" y="395" font-size="11" font-style="italic" fill="{violet}" opacity="0.8">narrow passage</text>')

	s.append(f'<text x="450" y="58" text-anchor="middle" font-size="26" font-weight="bold" letter-spacing="3" fill="{text}">THE SILHOUETTE TRIAL</text>')
	s.append(f'<text x="450" y="78" text-anchor="middle" font-size="12" font-style="italic" fill="{dim}">151 classes, 17 to 23 July 2026</text>')
	s.append("</svg>")
	return "\n".join(s)


if __name__ == "__main__":
	(OUT / "silhouette_map.svg").write_text(cave_map())
	print("wrote", OUT / "silhouette_map.svg")
