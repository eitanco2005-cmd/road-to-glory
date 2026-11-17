"""Deterministic puzzle generators (seeded): mazes with solutions, word searches with answer keys."""
import random
from collections import deque

INK = "#1b1b1b"


# ------------------------------------------------------------------ maze
def maze(cols, rows, seed):
    """Perfect maze by randomized DFS. Returns walls: set of (cell, dir) open passages and the solution path."""
    rnd = random.Random(seed)
    opened = {(c, r): set() for c in range(cols) for r in range(rows)}
    stack = [(0, 0)]
    seen = {(0, 0)}
    D = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
    OPP = {"N": "S", "S": "N", "E": "W", "W": "E"}
    while stack:
        c, r = stack[-1]
        nb = [(d, (c + dx, r + dy)) for d, (dx, dy) in D.items()
              if 0 <= c + dx < cols and 0 <= r + dy < rows and (c + dx, r + dy) not in seen]
        if not nb:
            stack.pop()
            continue
        d, n = rnd.choice(nb)
        opened[(c, r)].add(d)
        opened[n].add(OPP[d])
        seen.add(n)
        stack.append(n)
    start, end = (0, 0), (cols - 1, rows - 1)
    prev = {start: None}
    q = deque([start])
    while q:
        cur = q.popleft()
        if cur == end:
            break
        for d in opened[cur]:
            dx, dy = D[d]
            n = (cur[0] + dx, cur[1] + dy)
            if n not in prev:
                prev[n] = cur
                q.append(n)
    path, cur = [], end
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    return opened, path[::-1]


def maze_svg(cols, rows, seed, cell=24, solution=False, sw=3.0):
    """SVG fragment + size. Entry: gap in the top wall of the top-left cell; exit: gap in the bottom wall of the bottom-right cell."""
    opened, path = maze(cols, rows, seed)
    W, H = cols * cell, rows * cell
    lines = []
    for (c, r), ds in opened.items():
        x, y = c * cell, r * cell
        if "N" not in ds and not (r == 0 and c == 0):
            lines.append(f"M{x},{y}h{cell}")
        if "W" not in ds:
            lines.append(f"M{x},{y}v{cell}")
        if r == rows - 1 and c != cols - 1:
            lines.append(f"M{x},{y + cell}h{cell}")
        if c == cols - 1 and r != rows - 1:
            lines.append(f"M{x + cell},{y}v{cell}")
    out = []
    if solution:
        pts = " ".join(f"{(c + .5) * cell:.1f},{(r + .5) * cell:.1f}" for c, r in path)
        pts = f"{cell * .5:.1f},{-cell * .7:.1f} " + pts + f" {W - cell * .5:.1f},{H + cell * .7:.1f}"
        out.append(f'<polyline points="{pts}" fill="none" stroke="#e0533d" stroke-width="{cell * .32:.1f}" stroke-linejoin="round" stroke-linecap="round" opacity=".85"/>')
    out.append(f'<path d="{"".join(lines)}" fill="none" stroke="{INK}" stroke-width="{sw}" stroke-linecap="square"/>')
    return "".join(out), W, H, path


# ------------------------------------------------------------------ word search
HE_FINALS = {"כ": "ך", "מ": "ם", "נ": "ן", "פ": "ף", "צ": "ץ"}


def word_search(words, size, seed, dirs, alphabet, filler_weights=None):
    """Place words (list of letter lists) into size x size grid. dirs = list of (dx, dy).
    Returns grid (rows of letters) and placements [(word, [(x,y)...])]."""
    rnd = random.Random(seed)
    for attempt in range(400):
        grid = [[None] * size for _ in range(size)]
        placed = []
        ok = True
        for w in sorted(words, key=len, reverse=True):
            cands = []
            for (dx, dy) in dirs:
                for y in range(size):
                    for x in range(size):
                        cells = [(x + dx * i, y + dy * i) for i in range(len(w))]
                        if not all(0 <= cx < size and 0 <= cy < size for cx, cy in cells):
                            continue
                        clash = [grid[cy][cx] not in (None, ch) for (cx, cy), ch in zip(cells, w)]
                        if any(clash):
                            continue
                        overlap = sum(grid[cy][cx] == ch for (cx, cy), ch in zip(cells, w))
                        cands.append((overlap, rnd.random(), cells))
            if not cands:
                ok = False
                break
            # prefer some overlap but keep it random
            cands.sort(key=lambda t: (-min(t[0], 1), t[1]))
            pick = cands[0] if rnd.random() < 0.35 else rnd.choice(cands)
            for (cx, cy), ch in zip(pick[2], w):
                grid[cy][cx] = ch
            placed.append((w, pick[2]))
        if not ok:
            continue
        letters = list(alphabet)
        weights = [filler_weights.get(ch, 1) for ch in letters] if filler_weights else None
        for y in range(size):
            for x in range(size):
                if grid[y][x] is None:
                    grid[y][x] = rnd.choices(letters, weights=weights)[0]
        # every word must occur exactly once (avoid accidental duplicates)
        if all(_count(grid, w, dirs) == 1 for w in words):
            return grid, placed
    raise RuntimeError("could not build word search")


def _count(grid, w, dirs):
    n = len(grid)
    c = 0
    for (dx, dy) in dirs:
        for y in range(n):
            for x in range(n):
                cells = [(x + dx * i, y + dy * i) for i in range(len(w))]
                if all(0 <= cx < n and 0 <= cy < n for cx, cy in cells) and all(grid[cy][cx] == ch for (cx, cy), ch in zip(cells, w)):
                    c += 1
    return c


def word_search_svg(grid, placed, cell=34, rtl=False, answers=False, font="Fredoka", fs=None):
    n = len(grid)
    fs = fs or cell * 0.62
    out = [f'<rect x="1" y="1" width="{n * cell - 2}" height="{n * cell - 2}" rx="10" fill="#fff" stroke="{INK}" stroke-width="2.5"/>']
    def pos(x, y):
        xx = (n - 1 - x) if rtl else x  # grid x=0 is the reading start (right edge in Hebrew)
        return (xx + .5) * cell, (y + .5) * cell
    if answers:
        for w, cells in placed:
            (x0, y0), (x1, y1) = pos(*cells[0]), pos(*cells[-1])
            out.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#f2b632" stroke-width="{cell * .7:.1f}" stroke-linecap="round" opacity=".55"/>')
    for y in range(n):
        for x in range(n):
            px, py = pos(x, y)
            out.append(f'<text x="{px:.1f}" y="{py + fs * .36:.1f}" text-anchor="middle" font-family="{font}" font-size="{fs:.1f}" font-weight="600" fill="{INK}">{grid[y][x]}</text>')
    return "".join(out), n * cell


# ------------------------------------------------------------------ color by number
# 0 = background (colour 1), others map to legend numbers. 16 x 18 pixel dreidel.
DREIDEL_PIXELS = [
    "0000000330000000",
    "0000000330000000",
    "0000000330000000",
    "0000000330000000",
    "0011111111111100",
    "0012222222222100",
    "0012244444422100",
    "0012244224422100",
    "0012222224422100",
    "0012222224422100",
    "0012222224422100",
    "0012244444444100",
    "0012222222222100",
    "0001222222221000",
    "0000122222210000",
    "0000012222100000",
    "0000001221000000",
    "0000000110000000",
]
# letter shape in the middle approximates ג in colour 4.

CANDLE_PIXELS = [
    "000000050000000",
    "000000555000000",
    "000005565500000",
    "000005666500000",
    "000000565000000",
    "000000030000000",
    "000002222200000",
    "000002444200000",
    "000002222200000",
    "000002444200000",
    "000002222200000",
    "000002444200000",
    "000002222200000",
    "000002444200000",
    "000002222200000",
    "000033333330000",
    "000333333333000",
    "000000000000000",
]
