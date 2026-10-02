"""Minimal character sheet for the profile introduction, in the cave-map palette."""

from pathlib import Path

OUT = Path(__file__).parent.parent / "assets"
W, H = 900, 560

ROCK, PANEL, WALL = "#16120f", "#221c18", "#c8b083"
TEXT, DIM, GOLD = "#ecdcb4", "#b19d74", "#e8b34a"

ABILITIES = [("STR", 13), ("DEX", 16), ("CON", 13), ("INT", 18), ("WIS", 8), ("CHA", 10)]

# (name, expertise)  expertise = two gold dots, proficient = one dot. Currently all proficient.
SKILLS = [
	("Code", [("Python", False), ("SQL", False), ("C/C++", False)]),
	("Libraries", [
		("PyTorch", False), ("scikit-learn", False), ("NumPy", False), ("SciPy", False),
		("pandas", False), ("Matplotlib", False), ("OpenCV", False), ("CVXPY/MOSEK", False),
	]),
	("Tools", [("Git", False), ("MLflow", False), ("Jupyter", False), ("Linux", False), ("Claude Code", False)]),
]

BACKGROUND = [
	("MSc Mathematics", "Freie Universität Berlin, 2024 to present"),
	("BSc (Hons) Computer Science and Physics", "University of Toronto, 2018 to 2023"),
]
LANGUAGES = "Turkish (native), English (C1), German (A2)"


def mod(score):
	m = (score - 10) // 2
	return f"+{m}" if m >= 0 else f"−{-m}"


def panel(s, x, y, w, h):
	s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PANEL}" stroke="{WALL}" stroke-width="2.5" filter="url(#rough)"/>')


def sheet():
	s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Georgia, \'Times New Roman\', serif">']
	s.append("""<defs>
<filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="4"/>
<feDisplacementMap in="SourceGraphic" scale="4"/></filter>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" seed="2"/>
<feColorMatrix values="0 0 0 0 0.8  0 0 0 0 0.7  0 0 0 0 0.5  0 0 0 0.06 0"/></filter>
</defs>""")
	s.append(f'<rect width="{W}" height="{H}" fill="{ROCK}"/>')
	s.append(f'<rect width="{W}" height="{H}" filter="url(#grain)"/>')

	# header
	s.append(f'<text x="40" y="66" font-size="34" font-weight="bold" letter-spacing="2" fill="{TEXT}">BOLKAR EREN</text>')
	s.append(f'<text x="40" y="96" font-size="16" font-style="italic" fill="{DIM}">Wizard stuck in the wrong timeline</text>')
	s.append(f'<line x1="40" y1="114" x2="{W-40}" y2="114" stroke="{WALL}" stroke-width="1.5" filter="url(#rough)"/>')

	# ability scores
	bw, gap, y0 = 120, 20, 136
	for i, (ab, sc) in enumerate(ABILITIES):
		x = 40 + i * (bw + gap)
		panel(s, x, y0, bw, 104)
		cx = x + bw / 2
		col = GOLD if ab == "INT" else TEXT
		s.append(f'<text x="{cx}" y="{y0+24}" text-anchor="middle" font-size="13" letter-spacing="2" fill="{DIM}">{ab}</text>')
		s.append(f'<text x="{cx}" y="{y0+64}" text-anchor="middle" font-size="32" font-weight="bold" fill="{col}">{mod(sc)}</text>')
		s.append(f'<ellipse cx="{cx}" cy="{y0+88}" rx="20" ry="11" fill="{ROCK}" stroke="{WALL}" stroke-width="1.5"/>')
		s.append(f'<text x="{cx}" y="{y0+93}" text-anchor="middle" font-size="13" fill="{TEXT}">{sc}</text>')

	# skills
	px, py, pw, ph = 40, 264, 400, 266
	panel(s, px, py, pw, ph)
	s.append(f'<text x="{px+20}" y="{py+32}" font-size="18" font-weight="bold" fill="{TEXT}">Skills</text>')
	cols = [SKILLS[0:1] + SKILLS[2:3], SKILLS[1:2]]
	for ci, groups in enumerate(cols):
		x = px + 20 + ci * 190
		y = py + 62
		for gname, items in groups:
			s.append(f'<text x="{x}" y="{y}" font-size="12" letter-spacing="1.5" fill="{DIM}">{gname.upper()}</text>')
			y += 20
			for name, expert in items:
				if expert:
					s.append(f'<circle cx="{x+5}" cy="{y-4.5}" r="4" fill="{GOLD}"/><circle cx="{x+16}" cy="{y-4.5}" r="4" fill="{GOLD}"/>')
				else:
					s.append(f'<circle cx="{x+5}" cy="{y-4.5}" r="4" fill="{WALL}"/>')
				s.append(f'<text x="{x + (28 if expert else 18)}" y="{y}" font-size="14" fill="{TEXT}">{name}</text>')
				y += 19
			y += 10

	# background
	px, py, pw, ph = 460, 264, 400, 266
	panel(s, px, py, pw, ph)
	s.append(f'<text x="{px+20}" y="{py+32}" font-size="18" font-weight="bold" fill="{TEXT}">Background</text>')
	y = py + 62
	for title, sub in BACKGROUND:
		if title:
			s.append(f'<text x="{px+20}" y="{y}" font-size="15" font-weight="bold" fill="{TEXT}">{title}</text>')
			y += 19
		s.append(f'<text x="{px+20}" y="{y}" font-size="13" font-style="italic" fill="{DIM}">{sub}</text>')
		y += 27 if title is None or sub.startswith(("Freie", "University")) else 19
	y += 4
	s.append(f'<line x1="{px+20}" y1="{y-10}" x2="{px+pw-20}" y2="{y-10}" stroke="{WALL}" stroke-width="0.8" opacity="0.5"/>')
	s.append(f'<text x="{px+20}" y="{y+12}" font-size="12" letter-spacing="1.5" fill="{DIM}">LANGUAGES</text>')
	s.append(f'<text x="{px+20}" y="{y+32}" font-size="14" fill="{TEXT}">{LANGUAGES}</text>')

	s.append("</svg>")
	return "\n".join(s)


if __name__ == "__main__":
	(OUT / "character_sheet.svg").write_text(sheet())
	print("wrote", OUT / "character_sheet.svg")
