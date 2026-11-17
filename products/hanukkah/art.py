"""Original vector art for the Hanukkah packs (hand-written SVG, no third-party artwork).

Every function returns an SVG fragment (no <svg> wrapper) drawn in its own coordinate box so pages can
place it with transform. `color=False` gives coloring-page line art (white fills, thick black outline);
`color=True` gives the flat palette used on covers, charts and the web previews.
"""
import math

INK = "#1b1b1b"
PAL = {
    "blue": "#2f6db5", "sky": "#cfe2f7", "gold": "#f2b632", "flame": "#f59e0b", "flame_in": "#fde68a",
    "orange": "#ef7d31", "jam": "#c2334d", "dough": "#e9b872", "sugar": "#fff8e7", "silver": "#c9d3df",
    "teal": "#0e6b63", "cream": "#fff7e6", "red": "#d64545", "green": "#3f9b5a", "purple": "#7b5cc4",
}


def _f(color, c, white="#fff"):
    return PAL[c] if color else white


def flame(x, y, h=26, color=True, sw=2.2):
    """Teardrop flame standing on (x, y)."""
    w = h * 0.42
    d = (f"M{x:.1f},{y - h:.1f} C{x + w:.1f},{y - h * 0.5:.1f} {x + w * 0.95:.1f},{y:.1f} {x:.1f},{y:.1f} "
         f"C{x - w * 0.95:.1f},{y:.1f} {x - w:.1f},{y - h * 0.5:.1f} {x:.1f},{y - h:.1f}Z")
    inner = h * 0.5
    wi = inner * 0.42
    di = (f"M{x:.1f},{y - inner:.1f} C{x + wi:.1f},{y - inner * 0.5:.1f} {x + wi * 0.9:.1f},{y - 1:.1f} {x:.1f},{y - 1:.1f} "
          f"C{x - wi * 0.9:.1f},{y - 1:.1f} {x - wi:.1f},{y - inner * 0.5:.1f} {x:.1f},{y - inner:.1f}Z")
    return (f'<path d="{d}" fill="{_f(color, "flame")}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
            f'<path d="{di}" fill="{_f(color, "flame_in")}" stroke="{INK if not color else "none"}" stroke-width="{sw * 0.6}"/>')


def candle(x, y, w=14, h=46, color=True, c="blue", lit=True, stripes=True, sw=2.4):
    """Candle standing on (x, y) (bottom centre)."""
    out = [f'<rect x="{x - w / 2:.1f}" y="{y - h:.1f}" width="{w}" height="{h}" rx="2" fill="{_f(color, c)}" stroke="{INK}" stroke-width="{sw}"/>']
    if stripes:
        for i in range(1, 4):
            yy = y - h + i * h / 4
            out.append(f'<path d="M{x - w / 2:.1f},{yy + 3:.1f} L{x + w / 2:.1f},{yy - 3:.1f}" stroke="{INK}" stroke-width="{sw * 0.6}" fill="none"/>')
    out.append(f'<path d="M{x:.1f},{y - h:.1f} v-5" stroke="{INK}" stroke-width="{sw * 0.8}" stroke-linecap="round"/>')
    if lit:
        out.append(flame(x, y - h - 4, h=h * 0.55, color=color, sw=sw * 0.85))
    return "".join(out)


def hanukkiah(color=True, lit=9, candles=True, sw=3.2, count=8):
    """Hanukkiah in a 400x330 box: 8 cups on a bar + raised shamash in the middle.
    lit = how many flames (0..9; the shamash is lit first when lit>0, then cups right-to-left)."""
    g = []
    gold = _f(color, "gold")
    # base + stem
    g.append(f'<path d="M140,322 L260,322 L240,298 L160,298 Z" fill="{gold}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>')
    g.append(f'<rect x="188" y="196" width="24" height="104" rx="4" fill="{gold}" stroke="{INK}" stroke-width="{sw}"/>')
    g.append(f'<ellipse cx="200" cy="246" rx="22" ry="9" fill="{gold}" stroke="{INK}" stroke-width="{sw}"/>')
    # bar
    g.append(f'<rect x="28" y="184" width="344" height="18" rx="9" fill="{gold}" stroke="{INK}" stroke-width="{sw}"/>')
    xs = [44, 82, 120, 158, 242, 280, 318, 356]
    for x in xs:
        g.append(f'<rect x="{x - 4}" y="160" width="8" height="26" fill="{gold}" stroke="{INK}" stroke-width="{sw * 0.8}"/>')
        g.append(f'<path d="M{x - 14},152 L{x + 14},152 L{x + 9},164 L{x - 9},164 Z" fill="{gold}" stroke="{INK}" stroke-width="{sw * 0.8}" stroke-linejoin="round"/>')
    # shamash post
    g.append(f'<rect x="194" y="112" width="12" height="74" fill="{gold}" stroke="{INK}" stroke-width="{sw * 0.8}"/>')
    g.append(f'<path d="M184,104 L216,104 L210,116 L190,116 Z" fill="{gold}" stroke="{INK}" stroke-width="{sw * 0.8}" stroke-linejoin="round"/>')
    if candles:
        cols = ["blue", "sky", "blue", "sky", "sky", "blue", "sky", "blue"]
        order = list(reversed(xs))  # night 1 candle on the right
        lit_set = set(order[:max(0, lit - 1)])
        have = set(order[:count])
        for x, c in zip(xs, cols):
            if x not in have:
                continue
            g.append(candle(x, 152, w=13, h=48, color=color, c=c, lit=x in lit_set, sw=sw * 0.75))
        g.append(candle(200, 104, w=14, h=50, color=color, c="orange", lit=lit > 0, sw=sw * 0.75))
    return "".join(g)


DREIDEL_LETTERS = {"he": ["נ", "ג", "ה", "פ"], "en": ["נ", "ג", "ה", "ש"]}


def dreidel(color=True, letter="ג", side_letter="ה", sw=3.2, c1="blue", c2="sky"):
    """3/4-view dreidel in a 240x320 box."""
    a, b = _f(color, c1), _f(color, c2)
    g = []
    # handle
    g.append(f'<rect x="108" y="10" width="26" height="62" rx="9" fill="{_f(color, "gold")}" stroke="{INK}" stroke-width="{sw}"/>')
    # top face
    g.append(f'<path d="M40,84 L146,84 L196,62 L92,62 Z" fill="{b}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>')
    g.append(f'<ellipse cx="121" cy="73" rx="15" ry="6" fill="{_f(color, "gold")}" stroke="{INK}" stroke-width="{sw * 0.8}"/>')
    # front face
    g.append(f'<path d="M40,84 L146,84 L146,196 L40,196 Z" fill="{a}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>')
    # side face
    g.append(f'<path d="M146,84 L196,62 L196,170 L146,196 Z" fill="{b}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>')
    # point
    g.append(f'<path d="M40,196 L146,196 L104,290 Z" fill="{a}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>')
    g.append(f'<path d="M146,196 L196,170 L104,290 Z" fill="{b}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>')
    # letters (hollow so kids can colour them)
    lf = "#fff" if color else "#fff"
    g.append(f'<text x="93" y="170" text-anchor="middle" font-family="Fredoka, \'Noto Sans Hebrew\', sans-serif" font-weight="700" '
             f'font-size="88" fill="{lf}" stroke="{INK}" stroke-width="{sw * 0.9}" paint-order="stroke">{letter}</text>')
    if side_letter:
        g.append(f'<text x="0" y="0" transform="translate(172,152) skewY(-24) scale(0.62,1)" text-anchor="middle" '
                 f'font-family="Fredoka, \'Noto Sans Hebrew\', sans-serif" font-weight="700" font-size="70" fill="{lf}" '
                 f'stroke="{INK}" stroke-width="{sw * 0.9}" paint-order="stroke">{side_letter}</text>')
    return "".join(g)


def sufganiyah(color=True, sw=3.2):
    """Side view jam doughnut in a 260x190 box."""
    g = []
    g.append(f'<path d="M20,130 C20,50 240,50 240,130 C240,170 20,170 20,130 Z" fill="{_f(color, "dough")}" stroke="{INK}" stroke-width="{sw}"/>')
    # pale band around the middle (typical of fried doughnuts)
    g.append(f'<path d="M24,138 C70,156 190,156 236,138" fill="none" stroke="{INK}" stroke-width="{sw * 0.7}"/>')
    # sugar dots
    import random
    r = random.Random(7)
    n = 0
    while n < 24:
        x = r.uniform(40, 220); y = r.uniform(70, 124)
        top = 130 - 78 * math.sqrt(max(0.0, 1 - ((x - 130) / 110) ** 2))
        if y < top + 9 or (96 < x < 166 and y < 82):
            continue
        n += 1
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r.uniform(2.2, 3.6):.1f}" fill="#fff" stroke="{INK}" stroke-width="{sw * 0.35}"/>')
    # jam blob on top
    g.append(f'<path d="M110,64 C104,46 122,34 132,44 C140,30 162,40 152,56 C162,62 150,76 138,70 C128,78 108,76 110,64 Z" '
             f'fill="{_f(color, "jam")}" stroke="{INK}" stroke-width="{sw * 0.9}" stroke-linejoin="round"/>')
    return "".join(g)


def oil_jug(color=True, sw=3.2):
    """Small clay oil jug (pach shemen) in a 200x260 box."""
    c = _f(color, "orange")
    g = []
    g.append(f'<path d="M70,40 L130,40 L124,70 C176,92 186,170 160,212 C150,228 140,238 100,240 C60,238 50,228 40,212 C14,170 24,92 76,70 Z" '
             f'fill="{c}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>')
    g.append(f'<rect x="62" y="28" width="76" height="16" rx="6" fill="{c}" stroke="{INK}" stroke-width="{sw}"/>')
    g.append(f'<path d="M126,78 C170,60 186,96 158,118" fill="none" stroke="{INK}" stroke-width="{sw * 2.6}" stroke-linecap="round"/>')
    g.append(f'<path d="M126,78 C170,60 186,96 158,118" fill="none" stroke="{c}" stroke-width="{sw * 1.1}" stroke-linecap="round"/>')
    g.append(f'<path d="M40,150 C80,168 120,168 160,150" fill="none" stroke="{INK}" stroke-width="{sw * 0.7}"/>')
    g.append(f'<path d="M46,178 C80,194 120,194 154,178" fill="none" stroke="{INK}" stroke-width="{sw * 0.7}"/>')
    for x in (70, 100, 130):
        g.append(f'<circle cx="{x}" cy="164" r="4" fill="{_f(color, "cream")}" stroke="{INK}" stroke-width="{sw * 0.5}"/>')
    # single oil drop
    g.append(f'<path d="M100,4 C108,16 112,22 100,26 C88,22 92,16 100,4 Z" fill="{_f(color, "gold")}" stroke="{INK}" stroke-width="{sw * 0.6}"/>')
    return "".join(g)


def coin(cx, cy, r=34, color=True, sw=3, mark="candle"):
    """Chocolate gelt coin."""
    g = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{_f(color, "gold")}" stroke="{INK}" stroke-width="{sw}"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r * 0.78:.1f}" fill="none" stroke="{INK}" stroke-width="{sw * 0.6}" stroke-dasharray="3 4"/>']
    if mark == "candle":
        g.append(candle(cx, cy + r * 0.45, w=r * 0.28, h=r * 0.6, color=color, c="gold", stripes=False, sw=sw * 0.6))
    return "".join(g)


def gift(x, y, w=110, h=90, color=True, c="red", sw=3):
    g = [f'<rect x="{x}" y="{y + 18}" width="{w}" height="{h - 18}" rx="4" fill="{_f(color, c)}" stroke="{INK}" stroke-width="{sw}"/>',
         f'<rect x="{x - 6}" y="{y}" width="{w + 12}" height="22" rx="4" fill="{_f(color, c)}" stroke="{INK}" stroke-width="{sw}"/>',
         f'<rect x="{x + w / 2 - 9}" y="{y}" width="18" height="{h}" fill="{_f(color, "gold")}" stroke="{INK}" stroke-width="{sw * 0.8}"/>',
         f'<path d="M{x + w / 2},{y} C{x + w / 2 - 40},{y - 34} {x + w / 2 - 44},{y + 2} {x + w / 2},{y} C{x + w / 2 + 44},{y + 2} {x + w / 2 + 40},{y - 34} {x + w / 2},{y} Z" '
         f'fill="{_f(color, "gold")}" stroke="{INK}" stroke-width="{sw * 0.8}" stroke-linejoin="round"/>']
    return "".join(g)


def star(cx, cy, r=30, color=True, sw=3, c="blue"):
    """Six-pointed star drawn as one 12-point outline (points + inner corners)."""
    pts = []
    ri = r / math.sqrt(3)
    for k in range(12):
        a = math.radians(k * 30)
        rr = r if k % 2 == 0 else ri
        pts.append(f"{cx + rr * math.sin(a):.1f},{cy - rr * math.cos(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{_f(color, c)}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'


def latkes(color=True, sw=3.2):
    """Plate with three potato pancakes, 300x170 box."""
    g = [f'<ellipse cx="150" cy="120" rx="140" ry="42" fill="{_f(color, "sky")}" stroke="{INK}" stroke-width="{sw}"/>',
         f'<ellipse cx="150" cy="116" rx="108" ry="28" fill="#fff" stroke="{INK}" stroke-width="{sw * 0.7}"/>']
    for (x, y) in [(110, 104), (190, 104), (150, 84)]:
        g.append(f'<path d="M{x - 46},{y} C{x - 48},{y - 22} {x + 48},{y - 22} {x + 46},{y} C{x + 44},{y + 18} {x - 44},{y + 18} {x - 46},{y} Z" '
                 f'fill="{_f(color, "dough")}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>')
        for dx in (-22, 0, 20):
            g.append(f'<path d="M{x + dx - 8},{y - 4} q8,-6 16,0" fill="none" stroke="{INK}" stroke-width="{sw * 0.5}" stroke-linecap="round"/>')
    return "".join(g)


def window_scene(color=True, sw=3.4):
    """Window with a lit hanukkiah on the sill, 420x420 box (classic 'pirsumei nisa' image)."""
    g = [f'<rect x="20" y="20" width="380" height="330" rx="10" fill="{_f(color, "blue")}" stroke="{INK}" stroke-width="{sw}"/>',
         f'<rect x="40" y="40" width="340" height="290" fill="{"#173a66" if color else "#fff"}" stroke="{INK}" stroke-width="{sw * 0.8}"/>',
         f'<path d="M210,40 V330 M40,150 H380" stroke="{INK}" stroke-width="{sw}"/>',
         f'<path d="M300,70 a26,26 0 1 0 22,40 a20,20 0 1 1 -22,-40 Z" fill="{_f(color, "flame_in")}" stroke="{INK}" stroke-width="{sw * 0.7}"/>']
    for (x, y) in [(90, 80), (150, 110), (360, 200), (70, 240)]:
        g.append(star(x, y, r=11, color=color, sw=sw * 0.5, c="flame_in"))
    g.append(f'<rect x="0" y="350" width="420" height="34" rx="6" fill="{_f(color, "dough")}" stroke="{INK}" stroke-width="{sw}"/>')
    g.append(f'<g transform="translate(110,190) scale(0.5)">{hanukkiah(color=color, lit=9, sw=sw * 1.1)}</g>')
    return "".join(g)


def svg(inner, vb, cls="", style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" class="{cls}" style="{style}" '
            f'stroke-linecap="round">{inner}</svg>')
