"""Moving pictures (SMIL) for the upper-body evaluation routine, v3.

Each picture is drawn in a local 156 x 132 box and returned as SVG markup.
Shapes are sampled from a pose function at evenly spaced frames and animated
with <animate> (points, cx/cy, d). The base attributes are the start pose, and
a faint ghost shows the end pose, so viewers without SMIL show both.
"""
import math

W, H = 156, 132
BODY = "#555555"
GHOST = "#d4d4d4"
FURN = "#e4e4e4"
FURN_STROKE = "#b8b8b8"
CAPTION = "#6f6f6f"
FRAMES = 30


def rad(d):
    return d * math.pi / 180.0


def pt(o, length, ang):
    """Point at `length` from o. ang: 0 = down, 90 = forward (+x), 180 = up, -90 = back."""
    return (o[0] + length * math.sin(rad(ang)), o[1] + length * math.cos(rad(ang)))


def rot(p, c, deg):
    """Rotate p about c; positive deg = clockwise on screen."""
    a = rad(deg)
    dx, dy = p[0] - c[0], p[1] - c[1]
    return (c[0] + dx * math.cos(a) - dy * math.sin(a), c[1] + dx * math.sin(a) + dy * math.cos(a))


def mid(a, b, u=0.5):
    return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)


def n1(v):
    s = f"{v:.1f}"
    if s == "-0.0":
        s = "0.0"
    return s[:-2] if s.endswith(".0") else s


def fp(p):
    return f"{n1(p[0])},{n1(p[1])}"


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def tl(t, segs):
    """Value at time t over segments [(duration, start, end), ...], eased."""
    for d, a, b in segs:
        if t <= d:
            return a + (b - a) * (ease(t / d) if d > 0 else 1.0)
        t -= d
    return segs[-1][2]


def total(segs):
    return sum(s[0] for s in segs)


def ik(a, b, l1, l2, bend_sign):
    """Middle joint of a two-link chain a->j->b; bend_sign picks the side."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy)
    d = max(min(d, l1 + l2 - 1e-6), abs(l1 - l2) + 1e-6)
    x = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    hgt = math.sqrt(max(l1 * l1 - x * x, 0.0))
    ux, uy = dx / d, dy / d
    px, py = a[0] + ux * x, a[1] + uy * x
    return (px - uy * hgt * bend_sign, py + ux * hgt * bend_sign)


def circle_meet(c1, r1, c2, r2, upper=True):
    """Intersection of two circles; upper = smaller y."""
    dx, dy = c2[0] - c1[0], c2[1] - c1[1]
    d = math.hypot(dx, dy)
    d = max(min(d, r1 + r2 - 1e-6), abs(r1 - r2) + 1e-6)
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    hgt = math.sqrt(max(r1 * r1 - a * a, 0.0))
    px, py = c1[0] + a * dx / d, c1[1] + a * dy / d
    p1 = (px + hgt * dy / d, py - hgt * dx / d)
    p2 = (px - hgt * dy / d, py + hgt * dx / d)
    if upper:
        return p1 if p1[1] < p2[1] else p2
    return p1 if p1[1] >= p2[1] else p2


def wedge(c, r, a_lo, a_hi):
    """Pie slice from angle a_lo to a_hi (a_lo <= a_hi), drawn the same way every frame."""
    p1, p2 = pt(c, r, a_lo), pt(c, r, a_hi)
    return f"M{fp(c)} L{fp(p1)} A{n1(r)} {n1(r)} 0 0 0 {fp(p2)} Z"


class Scene:
    """Collects animated shapes; render() emits ghosts, then animated shapes, then overlays."""

    def __init__(self, dur, ghost_ts=()):
        self.dur = dur
        self.ghost_ts = list(ghost_ts)
        self.under = []
        self.items = []
        self.over = []

    def poly(self, fn, stroke=BODY, width=3.4, ghost=True, fill="none", dash=None, closed=False, opacity=None):
        self.items.append(("poly", fn, dict(stroke=stroke, width=width, ghost=ghost, fill=fill,
                                            dash=dash, closed=closed, opacity=opacity)))

    def circle(self, fn, r, stroke=BODY, width=1.6, fill="#ffffff", ghost=True):
        self.items.append(("circle", fn, dict(r=r, stroke=stroke, width=width, fill=fill, ghost=ghost)))

    def path(self, fn, stroke="none", width=1.2, fill="none", ghost=False, fill_opacity=None):
        self.items.append(("path", fn, dict(stroke=stroke, width=width, fill=fill, ghost=ghost,
                                            fill_opacity=fill_opacity)))

    def _times(self):
        return [self.dur * i / FRAMES for i in range(FRAMES + 1)]

    def _anim(self, attr, vals):
        if all(v == vals[0] for v in vals):
            return ""
        return (f'<animate attributeName="{attr}" dur="{n1(self.dur)}s" repeatCount="indefinite" '
                f'values="{";".join(vals)}"/>')

    @staticmethod
    def _style(st, ghost):
        stroke = GHOST if ghost else st["stroke"]
        s = f'stroke="{stroke}" stroke-width="{n1(st["width"])}"'
        if st.get("dash") and not ghost:
            s += f' stroke-dasharray="{st["dash"]}"'
        if st.get("opacity") is not None and not ghost:
            s += f' stroke-opacity="{st["opacity"]}"'
        return s

    def render(self):
        ts = self._times()
        out = list(self.under)
        for g in self.ghost_ts:
            for kind, fn, st in self.items:
                if not st.get("ghost"):
                    continue
                if kind == "poly":
                    tag = "polygon" if st["closed"] else "polyline"
                    pts = " ".join(fp(p) for p in fn(g))
                    out.append(f'<{tag} points="{pts}" fill="none" {self._style(st, True)} '
                               f'stroke-linecap="round" stroke-linejoin="round"/>')
                elif kind == "circle":
                    c = fn(g)
                    out.append(f'<circle cx="{n1(c[0])}" cy="{n1(c[1])}" r="{n1(st["r"])}" fill="none" '
                               f'stroke="{GHOST}" stroke-width="{n1(st["width"])}"/>')
        for kind, fn, st in self.items:
            if kind == "poly":
                tag = "polygon" if st["closed"] else "polyline"
                frames = [" ".join(fp(p) for p in fn(t)) for t in ts]
                fill = st["fill"]
                out.append(f'<{tag} points="{frames[0]}" fill="{fill}" {self._style(st, False)} '
                           f'stroke-linecap="round" stroke-linejoin="round">'
                           f'{self._anim("points", frames)}</{tag}>')
            elif kind == "circle":
                cs = [fn(t) for t in ts]
                ax = self._anim("cx", [n1(c[0]) for c in cs])
                ay = self._anim("cy", [n1(c[1]) for c in cs])
                out.append(f'<circle cx="{n1(cs[0][0])}" cy="{n1(cs[0][1])}" r="{n1(st["r"])}" '
                           f'fill="{st["fill"]}" stroke="{st["stroke"]}" stroke-width="{n1(st["width"])}">'
                           f'{ax}{ay}</circle>')
            elif kind == "path":
                ds = [fn(t) for t in ts]
                fo = f' fill-opacity="{st["fill_opacity"]}"' if st.get("fill_opacity") is not None else ""
                out.append(f'<path d="{ds[0]}" fill="{st["fill"]}"{fo} stroke="{st["stroke"]}" '
                           f'stroke-width="{n1(st["width"])}">{self._anim("d", ds)}</path>')
        out.extend(self.over)
        return "\n".join(out)


# ─── shared static bits ────────────────────────────────────────────────────

def caption(text, icon=True):
    s = []
    x = 6
    if icon:
        s.append(f'<rect x="6" y="119" width="11" height="8" rx="1.5" fill="none" stroke="{CAPTION}" stroke-width="1"/>'
                 f'<circle cx="11.5" cy="123" r="2.2" fill="none" stroke="{CAPTION}" stroke-width="1"/>'
                 f'<rect x="8" y="117.5" width="4" height="1.8" fill="{CAPTION}"/>')
        x = 21
    s.append(f'<text font-size="9" fill="{CAPTION}" x="{x}" y="126">{text}</text>')
    return "\n".join(s)


def floor(y, x0=4, x1=152):
    return f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{FURN_STROKE}" stroke-width="1"/>'


def label(x, y, text, fill=CAPTION, anchor=None):
    a = f' text-anchor="{anchor}"' if anchor else ""
    return f'<text font-size="9" fill="{fill}" x="{n1(x)}" y="{n1(y)}"{a}>{text}</text>'


def beat_dots(dur, n, color, x0=8, y=108, step=8, text=""):
    """n beat dots lighting in turn over `dur` seconds; text sits to the right."""
    out = []
    for i in range(n):
        lo, hi = i / n, (i + 1) / n
        if i == 0:
            vals, kts = "1;0.2", f"0;{n1(hi) if hi < 1 else 1}"
        elif hi >= 1:
            vals, kts = "0.2;1", f"0;{lo:.4g}"
        else:
            vals, kts = "0.2;1;0.2", f"0;{lo:.4g};{hi:.4g}"
        out.append(f'<circle cx="{x0 + i * step}" cy="{y}" r="2.8" fill="{color}" fill-opacity="0.45">'
                   f'<animate attributeName="fill-opacity" dur="{n1(dur)}s" repeatCount="indefinite" '
                   f'calcMode="discrete" values="{vals}" keyTimes="{kts}"/></circle>')
    if text:
        out.append(label(x0 + n * step + 2, y + 3, text))
    return "\n".join(out)


def dot(p, color, r=2.4):
    return f'<circle cx="{n1(p[0])}" cy="{n1(p[1])}" r="{r}" fill="{color}"/>'


# ─── standing side figure (faces right) ────────────────────────────────────

def stand(x, base=100, s=1.0, knee=0.0):
    a = (x, base)
    k = pt(a, 20 * s, 180 - knee)
    h = pt(k, 21 * s, 180 + knee)
    return a, k, h


# ─── 1 shoulder raise range ────────────────────────────────────────────────

def pic_shoulder_raise(col):
    segs = [(1.0, 0, 0), (3.0, 0, 170), (2.0, 170, 170), (3.0, 170, 0)]
    sc = Scene(total(segs), ghost_ts=[5.0])
    s = 0.85
    a, k, h = stand(52, s=s)
    lum = pt(h, 13 * s, 180)
    sh = pt(lum, 17 * s, 180)
    head = pt(sh, 9 * s, 180)
    ang = lambda t: tl(t, segs)
    elbow = lambda t: pt(sh, 14, ang(t))
    tip = lambda t: pt(sh, 31, ang(t))
    sc.under.append(floor(100))
    sc.poly(lambda t: [(a[0] + 6, a[1]), a, k, h, lum, sh], ghost=False)
    sc.circle(lambda t: head, 5.5, ghost=False)
    sc.path(lambda t: wedge(sh, 11, 0, max(ang(t), 0.01)), fill=col, fill_opacity="0.18", stroke=col, width=1)
    sc.poly(lambda t: [sh, elbow(t), tip(t)])
    sc.poly(lambda t: [sh, h], stroke=col, width=1.4, ghost=False, dash="3 2")
    sc.poly(lambda t: [sh, elbow(t)], stroke=col, width=1.6, ghost=False)
    sc.circle(lambda t: elbow(t), 2.4, stroke=col, fill=col, width=0.5, ghost=False)
    sc.over += [dot(sh, col), dot(h, col), label(8, 112, "dots: hip · shoulder · elbow"),
                caption("side view · lens at shoulder")]
    return sc.render()


# ─── 2 shoulder turn-out range (lying, camera at the feet) ─────────────────

def pic_shoulder_turnout(col):
    segs = [(1.0, 0, 0), (2.5, 0, 75), (2.0, 75, 75), (2.5, 75, 0)]
    sc = Scene(total(segs), ghost_ts=[4.5])
    e = (108.0, 87.0)
    ang = lambda t: tl(t, segs)
    tip = lambda t: pt(e, 30, 180 - ang(t))
    sc.under += [f'<rect x="10" y="96" width="136" height="4" rx="1" fill="{FURN}" stroke="{FURN_STROKE}" stroke-width="0.8"/>',
                 f'<circle cx="70" cy="66" r="9" fill="#ffffff" stroke="{BODY}" stroke-width="1.6"/>',
                 f'<ellipse cx="70" cy="84" rx="30" ry="11" fill="#f2f2f2" stroke="{BODY}" stroke-width="1.6"/>',
                 f'<circle cx="34" cy="88" r="4.5" fill="#ffffff" stroke="{BODY}" stroke-width="1.6"/>',
                 f'<line x1="{n1(e[0])}" y1="{n1(e[1])}" x2="{n1(e[0])}" y2="{n1(e[1] - 36)}" stroke="{col}" '
                 f'stroke-width="1.4" stroke-dasharray="3 2"/>']
    sc.path(lambda t: wedge(e, 14, 180 - max(ang(t), 0.01), 180), fill=col, fill_opacity="0.18", stroke=col, width=1)
    sc.poly(lambda t: [e, tip(t)])
    sc.circle(lambda t: tip(t), 3.4)
    sc.over += [f'<circle cx="{n1(e[0])}" cy="{n1(e[1])}" r="4.5" fill="#ffffff" stroke="{BODY}" stroke-width="1.6"/>',
                dot(e, col, 2), label(8, 112, "elbow at your side, bent 90°"),
                caption("from the feet · elbow height")]
    return sc.render()


# ─── 3 elbow range ─────────────────────────────────────────────────────────

def pic_elbow_range(col):
    segs = [(2.0, 0, 0), (2.0, 0, 145), (2.0, 145, 145), (2.0, 145, 0)]
    sc = Scene(total(segs), ghost_ts=[5.0])
    s = 0.95
    a, k, h = stand(50, s=s)
    lum = pt(h, 13 * s, 180)
    sh = pt(lum, 17 * s, 180)
    head = pt(sh, 9 * s, 180)
    sa = (sh[0] + 4, sh[1] + 2)
    el = pt(sa, 17, 6)
    f = lambda t: tl(t, segs)
    wr = lambda t: pt(el, 16, f(t))
    tip = lambda t: pt(el, 20, f(t))
    sc.under.append(floor(100))
    sc.poly(lambda t: [(a[0] + 6, a[1]), a, k, h, lum, sh], ghost=False)
    sc.circle(lambda t: head, 6, ghost=False)
    sc.path(lambda t: wedge(el, 9, f(t), 180), fill=col, fill_opacity="0.18", stroke=col, width=1)
    sc.poly(lambda t: [sa, el, tip(t)])
    sc.circle(lambda t: wr(t), 2.4, stroke=col, fill=col, width=0.5, ghost=False)
    sc.over += [dot(sa, col), dot(el, col), label(8, 112, "dots: shoulder · elbow · wrist"),
                caption("side view · lens at elbow")]
    return sc.render()


# ─── forearm on a table (4, 16, 19) ────────────────────────────────────────

WRIST = (88.0, 64.0)


def table_under():
    return [f'<rect x="6" y="68" width="86" height="6" rx="1" fill="{FURN}" stroke="{FURN_STROKE}" stroke-width="0.8"/>',
            f'<line x1="12" y1="74" x2="12" y2="104" stroke="{FURN_STROKE}" stroke-width="1.2"/>',
            f'<line x1="86" y1="74" x2="86" y2="104" stroke="{FURN_STROKE}" stroke-width="1.2"/>',
            floor(104)]


def forearm_over():
    return f'<line x1="16" y1="64" x2="{n1(WRIST[0])}" y2="{n1(WRIST[1])}" stroke="{BODY}" stroke-width="7" stroke-linecap="round"/>'


def pic_wrist_range(col):
    segs = [(1.0, 0, 0), (1.5, 0, 70), (1.5, 70, 70), (1.5, 70, 0), (1.5, 0, -75), (1.5, -75, -75), (1.5, -75, 0)]
    sc = Scene(total(segs), ghost_ts=[3.2, 7.7])
    b = lambda t: tl(t, segs)
    knuckle = lambda t: pt(WRIST, 18, 90 + b(t))
    finger = lambda t: pt(WRIST, 28, 90 + b(t))
    sc.under += table_under() + [forearm_over(),
                                 f'<line x1="{n1(WRIST[0])}" y1="{n1(WRIST[1])}" x2="{n1(WRIST[0] + 30)}" y2="{n1(WRIST[1])}" '
                                 f'stroke="{col}" stroke-width="1.4" stroke-dasharray="3 2"/>']
    sc.path(lambda t: wedge(WRIST, 13, min(90, 90 + b(t)) - 0.01, max(90, 90 + b(t))),
            fill=col, fill_opacity="0.18", stroke=col, width=1)
    sc.poly(lambda t: [WRIST, knuckle(t)], width=5)
    sc.poly(lambda t: [knuckle(t), finger(t)], width=3)
    sc.circle(lambda t: knuckle(t), 2.4, stroke=col, fill=col, width=0.5, ghost=False)
    sc.over += [dot((50, 64), col), dot(WRIST, col), label(8, 112, "up, then down"),
                caption("thumb side · lens at table")]
    return sc.render()


# ─── 5 low-back bend range (pens) ──────────────────────────────────────────

def pic_lowback_range(col):
    fwd = [(1.0, 0, 0), (2.5, 0, 1), (2.0, 1, 1), (2.5, 1, 0), (1.0, 0, 0)]
    back = [(2.0, 0, 1), (1.5, 1, 1), (1.5, 1, 0)]
    d1 = total(fwd)
    dur = d1 + total(back)

    def angles(t):
        if t <= d1:
            u = tl(t, fwd)
            return 50 * u, 40 * u, 12 * u
        u = tl(t - d1, back)
        return -8 * u, -16 * u, -4 * u

    sc = Scene(dur, ghost_ts=[4.5])
    a, k, h = stand(56, s=0.95)

    def chain(t):
        p, l, th = angles(t)
        d0 = 180 - p
        p2 = pt(h, 6, d0)
        lu = pt(p2, 12, d0 - l)
        sh = pt(lu, 16, d0 - l - th)
        hd = pt(sh, 8.5, d0 - l - th - 6)
        return p2, lu, sh, hd, d0, d0 - l, d0 - l - th

    def arm(t):
        p2, lu, sh, hd, *_ = chain(t)
        el = pt(sh, 15, 6)
        return [sh, el, pt(el, 14, 10)]

    def pen_low(t):
        p2, lu, sh, hd, d0, dl, dt = chain(t)
        c = pt(mid(h, p2), 3.6, d0 + 90)
        return [pt(c, 5.5, d0 + 180), pt(c, 5.5, d0)]

    def pen_up(t):
        p2, lu, sh, hd, d0, dl, dt = chain(t)
        c = pt(pt(lu, 3, dt), 3.6, dt + 90)
        return [pt(c, 5.5, dt + 180), pt(c, 5.5, dt)]

    sc.under.append(floor(100))
    sc.poly(lambda t: [(a[0] + 6, a[1]), a, k, h])
    sc.poly(lambda t: [h] + list(chain(t)[:3]))
    sc.circle(lambda t: chain(t)[3], 5.8)
    sc.poly(arm)
    sc.poly(pen_low, stroke=col, width=2.6, ghost=False)
    sc.poly(pen_up, stroke=col, width=2.6, ghost=False)
    sc.over += [label(8, 112, "pens: dimples and 15 cm up"), caption("side view · lens at waist")]
    return sc.render()


# ─── 6 side-bend (front view, no camera) ───────────────────────────────────

def pic_sidebend(col):
    segs = [(1.5, 0, 0), (2.5, 0, 30), (2.0, 30, 30), (2.5, 30, 0)]
    sc = Scene(total(segs), ghost_ts=[5.0])
    pc = (78.0, 60.0)
    hl, hr = (69.0, 62.0), (87.0, 62.0)
    b = lambda t: tl(t, segs)

    def top(t):
        return pt(pc, 30, 180 - b(t))

    def shoulders(t):
        tp = top(t)
        return pt(tp, 14, 270 - b(t)), pt(tp, 14, 90 - b(t))

    def finger(t):
        return pt(shoulders(t)[1], 34, -b(t))

    sc.under += [floor(100)]
    sc.poly(lambda t: [(67, 100), hl, hr, (89, 100)])
    sc.poly(lambda t: [shoulders(t)[0], shoulders(t)[1], hr, hl], closed=True)
    sc.circle(lambda t: pt(top(t), 9.5, 180 - 1.3 * b(t)), 6.5)
    sc.poly(lambda t: [shoulders(t)[0], (shoulders(t)[0][0], shoulders(t)[0][1] + 33)])
    sc.poly(lambda t: [shoulders(t)[1], finger(t)])
    y0, y1 = finger(0)[1], finger(4.5)[1]
    sc.over += [f'<line x1="97" y1="{n1(y0)}" x2="105" y2="{n1(y0)}" stroke="{col}" stroke-width="1.6"/>',
                f'<line x1="97" y1="{n1(y1)}" x2="105" y2="{n1(y1)}" stroke="{col}" stroke-width="1.6"/>',
                f'<line x1="103" y1="{n1(y0)}" x2="103" y2="{n1(y1)}" stroke="{col}" stroke-width="1" stroke-dasharray="2 2"/>',
                label(108, (y0 + y1) / 2 + 3, "gap, cm", fill=col),
                label(8, 112, "fingertip slides down the thigh"),
                caption("no camera · mark twice", icon=False)]
    return sc.render()


# ─── 7 hip hinge (waiter's bow) ────────────────────────────────────────────

def pic_hip_hinge(col):
    segs = [(1.0, 0, 0), (2.5, 0, 60), (1.5, 60, 60), (2.5, 60, 0)]
    sc = Scene(total(segs), ghost_ts=[4.2])
    a, k, h = stand(50, knee=8)
    T = lambda t: tl(t, segs)
    lum = lambda t: pt(h, 13, 180 - T(t))
    sh = lambda t: pt(lum(t), 17, 180 - T(t))
    head = lambda t: pt(sh(t), 9, 172 - T(t))
    hand = lambda t: rot((h[0] + 3, h[1] - 4), h, T(t))
    elbow = lambda t: ik(sh(t), hand(t), 13, 13, 1)
    sc.under.append(floor(100))
    sc.path(lambda t: wedge(h, 11, 180 - max(T(t), 0.01), 180), fill=col, fill_opacity="0.18", stroke=col, width=1)
    sc.poly(lambda t: [(a[0] + 6, a[1]), a, k, h, lum(t), sh(t)])
    sc.circle(head, 6)
    sc.poly(lambda t: [sh(t), elbow(t), hand(t)], width=3)
    sc.poly(lambda t: [h, lum(t)], stroke=col, width=3.6, ghost=False)
    sc.over += [label(70, 76, "hips 50–70°", fill=col), label(8, 112, "low back stays flat"),
                caption("side view · lens at hip")]
    return sc.render()


# ─── 8 pelvic tuck ─────────────────────────────────────────────────────────

def pic_pelvic_tuck(col):
    segs = [(1.5, 0, 0), (1.5, 0, 1), (1.5, 1, 1), (1.5, 1, 0)]
    sc = Scene(total(segs), ghost_ts=[3.7])
    a, k, h = stand(62)
    u = lambda t: tl(t, segs)
    tilt = lambda t: -26 * u(t)
    shape = [(h[0] - 7, h[1] - 8), (h[0] + 6, h[1] - 9), (h[0] + 8, h[1] + 4), (h[0] - 6, h[1] + 5)]
    pelvis = lambda t: [rot(p, h, tilt(t)) for p in shape]
    ptop = lambda t: rot((h[0] - 0.5, h[1] - 8.5), h, tilt(t))
    lu = (62.0, 38.0)
    sh = (62.0, 23.0)

    def spine(t):
        p0 = ptop(t)
        c = (p0[0] + 10 * (1 - u(t)) + 1, (p0[1] + lu[1]) / 2)
        return f"M{fp(p0)} Q{fp(c)} {fp(lu)}"

    glute = lambda t: [rot(p, h, tilt(t)) for p in [(h[0] - 8, h[1] - 5), (h[0] - 14, h[1] + 1), (h[0] - 8, h[1] + 8)]]
    sc.under.append(floor(100))
    sc.poly(lambda t: [(a[0] + 6, a[1]), a, k, h], ghost=False)
    sc.poly(pelvis, width=1.8, closed=True, fill="#ffffff")
    sc.path(spine, stroke=BODY, width=3.4)
    sc.poly(glute, stroke=col, width=2.6, ghost=False)
    sc.under.append(f'<line x1="{n1(lu[0])}" y1="{n1(lu[1])}" x2="{n1(sh[0])}" y2="{n1(sh[1])}" stroke="{BODY}" '
                    f'stroke-width="3.4" stroke-linecap="round"/>'
                    f'<circle cx="62.5" cy="14.5" r="6" fill="#ffffff" stroke="{BODY}" stroke-width="1.6"/>'
                    f'<polyline points="63,24 64.5,40 66,55" fill="none" stroke="{BODY}" stroke-width="3" stroke-linecap="round"/>')
    sc.over += [label(14, 70, "glutes on", fill=col), label(78, 28, "upper back still"),
                label(8, 112, "low back flattens"), caption("side view · lens at hip")]
    return sc.render()


# ─── 9 seated knee straighten ──────────────────────────────────────────────

def pic_seated_knee(col):
    segs = [(1.0, 0, 0), (1.5, 0, 50), (1.5, 50, 50), (1.5, 50, 0), (0.5, 0, 0)]
    sc = Scene(total(segs), ghost_ts=[3.0])
    hp, kn = (40.0, 66.0), (64.0, 66.0)
    lu, sh = (40.0, 53.0), (40.0, 37.0)
    e = lambda t: tl(t, segs)
    ank = lambda t: pt(kn, 22, e(t))
    toe = lambda t: pt(ank(t), 6, e(t) + 90)
    sc.under += [f'<rect x="20" y="68" width="52" height="5" rx="1" fill="{FURN}" stroke="{FURN_STROKE}" stroke-width="0.8"/>',
                 f'<line x1="24" y1="73" x2="24" y2="100" stroke="{FURN_STROKE}" stroke-width="1.2"/>',
                 f'<line x1="68" y1="73" x2="68" y2="100" stroke="{FURN_STROKE}" stroke-width="1.2"/>',
                 floor(100),
                 f'<polyline points="{fp(kn)} {fp(hp)} {fp(lu)} {fp(sh)}" fill="none" stroke="{BODY}" stroke-width="3.4" '
                 f'stroke-linecap="round" stroke-linejoin="round"/>',
                 f'<circle cx="41" cy="28" r="6" fill="#ffffff" stroke="{BODY}" stroke-width="1.6"/>',
                 f'<polyline points="41,38 46,51 56,62" fill="none" stroke="{BODY}" stroke-width="3" stroke-linecap="round"/>',
                 f'<line x1="{n1(hp[0])}" y1="{n1(hp[1])}" x2="{n1(lu[0])}" y2="{n1(lu[1])}" stroke="{col}" stroke-width="3.6" stroke-linecap="round"/>']
    sc.poly(lambda t: [kn, ank(t), toe(t)])
    sc.over += [label(52, 22, "low back still", fill=col),
                label(92, 50, "30–50° short", fill=col), label(92, 59, "of straight", fill=col),
                caption("side view · lens at seat")]
    return sc.render()


# ─── all fours (10, 11, 15) ────────────────────────────────────────────────

KNEE4 = (46.0, 98.0)
HAND4 = (112.0, 98.0)


def quad(theta):
    hp = pt(KNEE4, 24, 180 - theta)
    sh = circle_meet(hp, 50, HAND4, 30, upper=True)
    trunk_ang = math.degrees(math.atan2(sh[0] - hp[0], sh[1] - hp[1]))
    head = pt(sh, 10, trunk_ang - 12)
    el = ik(sh, HAND4, 15.5, 15.5, 1)
    low = pt(hp, 22, trunk_ang)
    return hp, sh, head, el, low


def quad_scene(col, segs, ghost_t, note):
    sc = Scene(total(segs), ghost_ts=[ghost_t])
    th = lambda t: tl(t, segs)
    sc.under += [floor(101), f'<line x1="{n1(KNEE4[0])}" y1="{n1(KNEE4[1])}" x2="20" y2="98" stroke="{BODY}" '
                             f'stroke-width="3.4" stroke-linecap="round"/>']
    sc.poly(lambda t: [KNEE4, quad(th(t))[0], quad(th(t))[1]])
    sc.circle(lambda t: quad(th(t))[2], 6)
    sc.poly(lambda t: [quad(th(t))[1], quad(th(t))[3], HAND4], width=3.2)
    sc.poly(lambda t: [quad(th(t))[0], quad(th(t))[4]], stroke=col, width=3.6, ghost=False)
    sc.over += [f'<circle cx="{n1(HAND4[0])}" cy="{n1(HAND4[1] - 1)}" r="3.4" fill="{BODY}"/>',
                label(8, 112, note), caption("side view · lens ~30 cm up")]
    return sc


def pic_rock_forward(col):
    segs = [(1.0, 0, 0), (2.0, 0, 18), (1.0, 18, 18), (2.0, 18, 0)]
    return quad_scene(col, segs, 3.5, "low back stays level, no sag").render()


def pic_rock_back(col):
    segs = [(1.0, 0, 0), (2.0, 0, -25), (1.0, -25, -25), (2.0, -25, 0)]
    sc = quad_scene(col, segs, 3.5, "hips back to ~120°, back flat")
    return sc.render()


def pic_one_arm_hold(col):
    segs = [(1.0, 0, 0), (1.0, 0, 1), (3.0, 1, 1), (1.0, 1, 0)]
    sc = Scene(total(segs), ghost_ts=[])
    hp, sh, head, el, low = quad(0)
    u = lambda t: tl(t, segs)
    free = lambda t: [sh, pt(sh, 30, 10 + 80 * u(t))]
    sc.under += [floor(101), f'<line x1="{n1(KNEE4[0])}" y1="{n1(KNEE4[1])}" x2="20" y2="98" stroke="{BODY}" '
                             f'stroke-width="3.4" stroke-linecap="round"/>']
    sc.poly(free, stroke="#a8a8a8", width=3.2, ghost=False)
    sc.under.append(f'<polyline points="{fp(KNEE4)} {fp(hp)} {fp(sh)}" fill="none" stroke="{BODY}" stroke-width="3.4" '
                    f'stroke-linecap="round" stroke-linejoin="round"/>'
                    f'<circle cx="{n1(head[0])}" cy="{n1(head[1])}" r="6" fill="#ffffff" stroke="{BODY}" stroke-width="1.6"/>')
    sc.over += [f'<polyline points="{fp(sh)} {fp(el)} {fp(HAND4)}" fill="none" stroke="{BODY}" stroke-width="3.2" '
                f'stroke-linecap="round" stroke-linejoin="round"/>',
                f'<circle cx="{n1(HAND4[0])}" cy="{n1(HAND4[1] - 1)}" r="3.4" fill="{BODY}"/>',
                dot(el, col, 3), label(48, 52, "hold 30 s", fill=col), label(8, 112, "this elbow stays slightly bent"),
                caption("side view · lens ~30 cm up")]
    return sc.render()


# ─── 12 face-down knee bend ────────────────────────────────────────────────

def pic_prone_knee(col):
    segs = [(1.0, 0, 0), (2.0, 0, 100), (1.0, 100, 100), (2.0, 100, 0)]
    sc = Scene(total(segs), ghost_ts=[3.5])
    hp, kn = (62.0, 92.0), (38.0, 94.0)
    f = lambda t: tl(t, segs)
    ank = lambda t: pt(kn, 21, -90 - f(t))
    foot = lambda t: pt(ank(t), 5, -f(t))
    sc.under += [floor(100),
                 f'<polyline points="{fp(hp)} 14,96" fill="none" stroke="#b0b0b0" stroke-width="3" stroke-linecap="round"/>',
                 f'<polyline points="{fp(kn)} {fp(hp)} 110,91" fill="none" stroke="{BODY}" stroke-width="3.4" '
                 f'stroke-linecap="round" stroke-linejoin="round"/>',
                 f'<polyline points="110,91 120,97 138,97" fill="none" stroke="{BODY}" stroke-width="3" stroke-linecap="round"/>',
                 f'<circle cx="128" cy="88" r="6" fill="#ffffff" stroke="{BODY}" stroke-width="1.6"/>',
                 f'<line x1="{n1(hp[0])}" y1="{n1(hp[1])}" x2="84" y2="91.5" stroke="{col}" stroke-width="3.6" stroke-linecap="round"/>']
    sc.poly(lambda t: [kn, ank(t), foot(t)])
    sc.over += [label(66, 82, "pelvis still", fill=col), label(8, 112, "shin to upright (90°) or more"),
                caption("side view · lens at floor")]
    return sc.render()


# ─── 13 shoulder-blade check (back view) ───────────────────────────────────

def pic_blade_check(col):
    segs = [(2.0, 0, 160), (2.0, 160, 0)]
    sc = Scene(total(segs), ghost_ts=[2.0])
    sl, sr = (56.0, 46.0), (100.0, 46.0)
    a = lambda t: tl(t, segs)
    phi = lambda t: 0.0 if a(t) < 30 else (a(t) - 30) * 0.38
    blade_l = [(70, 49), (69, 74), (59, 51)]
    blade_r = [(86, 49), (87, 74), (97, 51)]

    def arm(side):
        def f(t):
            s0 = sl if side < 0 else sr
            ang = -a(t) if side < 0 else a(t)
            return [s0, pt(s0, 34, ang)]
        return f

    def bell(side):
        def f(t):
            s0 = sl if side < 0 else sr
            ang = -a(t) if side < 0 else a(t)
            hnd = pt(s0, 34, ang)
            return [pt(hnd, 5, ang + 90), pt(hnd, 5, ang - 90)]
        return f

    sc.under += [f'<polygon points="56,42 100,42 93,90 63,90" fill="#ffffff" stroke="{BODY}" stroke-width="1.6" stroke-linejoin="round"/>',
                 f'<line x1="78" y1="46" x2="78" y2="86" stroke="#9a9a9a" stroke-width="1" stroke-dasharray="2 3"/>']
    sc.poly(lambda t: [rot(p, (67, 57), phi(t)) for p in blade_l], stroke=col, width=1.6, fill=col, closed=True,
            ghost=False, opacity=None)
    sc.poly(lambda t: [rot(p, (89, 57), -phi(t)) for p in blade_r], stroke=col, width=1.6, fill=col, closed=True,
            ghost=False, opacity=None)
    for side in (-1, 1):
        sc.poly(arm(side), width=3.6)
        sc.poly(bell(side), stroke="#333333", width=4.2)
    sc.over += [f'<circle cx="78" cy="31" r="7" fill="#ffffff" stroke="{BODY}" stroke-width="1.6"/>',
                beat_dots(4.0, 4, col, text="2 beats up · 2 down"),
                caption("2 m behind · shoulder height")]
    out = sc.render()
    return out.replace(f'fill="{col}" stroke="{col}" stroke-width="1.6"', f'fill="{col}" fill-opacity="0.3" stroke="{col}" stroke-width="1.6"')


# ─── 14 kneeling push-ups on handles ───────────────────────────────────────

def pic_kneeling_pushup(col):
    segs = [(3.0, 40.8, 18.0), (2.0, 18.0, 40.8), (2.0, 40.8, 40.8)]
    sc = Scene(total(segs), ghost_ts=[3.0])
    kn, hh = (34.0, 97.0), (92.0, 93.0)
    beta = lambda t: tl(t, segs)
    sh = lambda t: (kn[0] + 72 * math.cos(rad(beta(t))), kn[1] - 72 * math.sin(rad(beta(t))))
    el = lambda t: ik(sh(t), hh, 22.5, 22.5, 1)
    head = lambda t: (sh(t)[0] + 10 * math.cos(rad(beta(t) - 14)), sh(t)[1] - 10 * math.sin(rad(beta(t) - 14)))
    sc.under += [floor(101), f'<line x1="{n1(kn[0])}" y1="{n1(kn[1])}" x2="12" y2="96" stroke="{BODY}" stroke-width="3.4" stroke-linecap="round"/>',
                 f'<polygon points="86,101 86,95 89,93 95,93 98,95 98,101" fill="#8a8a8a" stroke="#666666" stroke-width="0.8"/>']
    sc.poly(lambda t: [kn, sh(t)])
    sc.circle(head, 6)
    sc.poly(lambda t: [sh(t), el(t), hh], width=3.2)
    sc.circle(lambda t: el(t), 2.8, stroke=col, fill=col, width=0.5, ghost=False)
    sc.over += [beat_dots(7.0, 7, col, step=6, text="3 down · 2 up · 2 hold"),
                label(8, 24, "elbows never straight", fill=col),
                caption("side view · lens at floor")]
    return sc.render()


# ─── 16 wrist control set (1 kg) ───────────────────────────────────────────

def pic_wrist_control(col):
    segs = [(1.0, 0, 55), (1.0, 55, 0)]
    sc = Scene(total(segs), ghost_ts=[])
    b = lambda t: tl(t, segs)
    hand = lambda t: pt(WRIST, 18, 90 + b(t))
    bell = lambda t: [pt(hand(t), 7, 180 + b(t)), pt(hand(t), 7, b(t))]
    stop_c = pt(WRIST, 24, 90 + 63)
    sc.under += table_under() + [forearm_over(),
                                 f'<rect x="{n1(stop_c[0] - 4)}" y="{n1(stop_c[1] - 4)}" width="9" height="7" rx="1" fill="#bdbdbd" '
                                 f'stroke="#8f8f8f" stroke-width="0.8" transform="rotate(-27 {n1(stop_c[0])} {n1(stop_c[1])})"/>']
    sc.poly(lambda t: [WRIST, hand(t)], width=5)
    sc.poly(bell, stroke="#333333", width=5)
    sc.over += [label(108, 40, "block at", fill=col), label(108, 49, "your limit", fill=col),
                beat_dots(2.0, 2, col, y=14, text="1 beat up · 1 down"),
                caption("side view, then from above")]
    return sc.render()


# ─── 17 side-raise endurance (front view, wall) ────────────────────────────

def pic_side_raise(col):
    segs = [(2.0, 0, 90), (2.0, 90, 0)]
    sc = Scene(total(segs), ghost_ts=[2.0])
    sr = (92.0, 38.0)
    a = lambda t: tl(t, segs)
    hand = lambda t: (sr[0] + 34 * math.sin(rad(a(t))) * 0.87, sr[1] + 34 * math.cos(rad(a(t))))
    el = lambda t: mid(sr, hand(t))
    bell = lambda t: [(hand(t)[0], hand(t)[1] - 5), (hand(t)[0], hand(t)[1] + 5)]
    sc.under += [f'<rect x="38" y="6" width="80" height="94" fill="#f1f1f1"/>', floor(100),
                 f'<polygon points="64,38 92,38 88,68 68,68" fill="#ffffff" stroke="{BODY}" stroke-width="1.6" stroke-linejoin="round"/>',
                 f'<polyline points="70,100 71,68 85,68 86,100" fill="none" stroke="{BODY}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>',
                 f'<line x1="64" y1="40" x2="62" y2="72" stroke="{BODY}" stroke-width="3.4" stroke-linecap="round"/>',
                 f'<circle cx="78" cy="25" r="7" fill="#ffffff" stroke="{BODY}" stroke-width="1.6"/>',
                 f'<line x1="96" y1="38" x2="150" y2="38" stroke="{col}" stroke-width="1.2" stroke-dasharray="3 2"/>']
    sc.poly(lambda t: [sr, el(t), hand(t)], width=3.6)
    sc.poly(bell, stroke="#333333", width=4.2)
    sc.over += [label(126, 33, "90°", fill=col), label(8, 34, "back on", fill="#8a8a8a"),
                label(8, 43, "the wall", fill="#8a8a8a"),
                beat_dots(4.0, 2, col, step=8, text="metronome 30: 1 up · 1 down"),
                caption("in front · lens at shoulder")]
    return sc.render()


# ─── 18 curl endurance (seated) ────────────────────────────────────────────

def pic_curl(col):
    segs = [(2.0, 15, 140), (2.0, 140, 15)]
    sc = Scene(total(segs), ghost_ts=[2.0])
    sh, el = (34.0, 40.0), (36.0, 58.0)
    f = lambda t: tl(t, segs)
    hand = lambda t: pt(el, 17, f(t))
    bell = lambda t: [pt(hand(t), 6, f(t) + 90), pt(hand(t), 6, f(t) - 90)]
    sc.under += [f'<line x1="22" y1="30" x2="22" y2="72" stroke="{FURN_STROKE}" stroke-width="2"/>',
                 f'<rect x="20" y="70" width="44" height="5" rx="1" fill="{FURN}" stroke="{FURN_STROKE}" stroke-width="0.8"/>',
                 f'<line x1="24" y1="75" x2="24" y2="100" stroke="{FURN_STROKE}" stroke-width="1.2"/>',
                 f'<line x1="60" y1="75" x2="60" y2="100" stroke="{FURN_STROKE}" stroke-width="1.2"/>', floor(100),
                 f'<polyline points="66,98 60,98 60,68 32,68 33,54 34,40" fill="none" stroke="{BODY}" stroke-width="3.4" '
                 f'stroke-linecap="round" stroke-linejoin="round"/>',
                 f'<circle cx="35" cy="31" r="6" fill="#ffffff" stroke="{BODY}" stroke-width="1.6"/>']
    sc.poly(lambda t: [sh, el, hand(t)], width=3.4)
    sc.poly(bell, stroke="#333333", width=4.4)
    sc.over += [dot(el, col, 2.8), label(76, 80, "bottom stops", fill=col), label(76, 89, "short of straight", fill=col),
                beat_dots(4.0, 4, col, text="2 beats up · 2 down"), caption("side view · lens at elbow")]
    return sc.render()


# ─── 19 band wrist-lift endurance ──────────────────────────────────────────

def pic_band_wrist(col):
    segs = [(2.0, 0, 45), (2.0, 45, 0)]
    sc = Scene(total(segs), ghost_ts=[2.0])
    b = lambda t: tl(t, segs)
    hand = lambda t: pt(WRIST, 18, 90 + b(t))
    grip = lambda t: pt(WRIST, 14, 90 + b(t))
    sc.under += table_under() + [forearm_over(),
                                 f'<polyline points="92,104 110,104" fill="none" stroke="{BODY}" stroke-width="4" stroke-linecap="round"/>']
    sc.poly(lambda t: [(101, 102), grip(t)], stroke=col, width=2, ghost=False)
    sc.poly(lambda t: [WRIST, hand(t)], width=5)
    sc.over += [label(106, 84, "band under", fill=col), label(106, 93, "your foot", fill=col),
                beat_dots(4.0, 4, col, y=14, text="2 beats up · 2 down"), caption("side view · lens at table")]
    return sc.render()


# ─── 20 session-2 score example (static) ───────────────────────────────────

def pic_score(col):
    lw, rw = 17.5 * 4.4, 21.5 * 4.4
    thr = rw * 0.80
    return "\n".join([
        label(8, 22, "Side raise, mean of 2 sessions"),
        label(8, 44, "Left"), f'<rect x="34" y="36" width="{n1(lw)}" height="10" rx="1.5" fill="{col}" fill-opacity="0.55"/>',
        label(38 + lw, 44, "17.5"),
        label(8, 66, "Right"), f'<rect x="34" y="58" width="{n1(rw)}" height="10" rx="1.5" fill="{col}"/>',
        label(38 + rw, 66, "21.5"),
        f'<line x1="{n1(34 + thr)}" y1="30" x2="{n1(34 + thr)}" y2="74" stroke="#333333" stroke-width="1" stroke-dasharray="3 2"/>',
        label(34 + thr, 84, "80% line", anchor="middle"),
        label(8, 102, "17.5 ÷ 21.5 = 81% → pass", fill=col),
        caption("weaker ÷ stronger", icon=False),
    ])


PICTURES = {
    "shoulder_raise": pic_shoulder_raise,
    "shoulder_turnout": pic_shoulder_turnout,
    "elbow_range": pic_elbow_range,
    "wrist_range": pic_wrist_range,
    "lowback_range": pic_lowback_range,
    "sidebend": pic_sidebend,
    "hip_hinge": pic_hip_hinge,
    "pelvic_tuck": pic_pelvic_tuck,
    "seated_knee": pic_seated_knee,
    "rock_forward": pic_rock_forward,
    "rock_back": pic_rock_back,
    "prone_knee": pic_prone_knee,
    "blade_check": pic_blade_check,
    "kneeling_pushup": pic_kneeling_pushup,
    "one_arm_hold": pic_one_arm_hold,
    "wrist_control": pic_wrist_control,
    "side_raise": pic_side_raise,
    "curl": pic_curl,
    "band_wrist": pic_band_wrist,
    "score": pic_score,
}
