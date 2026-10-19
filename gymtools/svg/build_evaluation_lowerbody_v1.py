#!/usr/bin/env python3
"""Build script for gymplan/evaluation_lowerbody.svg v1 (chat, 2026-10-08).

Layout copies evaluation_upperbody v3: one-test cards, a moving picture per card
(SMIL, D-78), info boxes, rules, unlock box, send-back box and version note.
Usage:  python3 -B build_evaluation_lowerbody_v1.py <out.svg>
Write to a scratch path, never straight into gymplan/ (gymtools/README); then copy
the SVG into gymplan/ and cp it to gymtxt/evaluation_lowerbody.txt, comparing hashes.
"""
import math
import sys

N = 31  # animation keyframes per picture, as in upper v3


# ── formatting ───────────────────────────────────────────────────────────────
def f(v):
    s = '%.1f' % v
    if s.endswith('.0'):
        s = s[:-2]
    if s == '-0':
        s = '0'
    return s


def r4(v):
    return ('%.4f' % v).rstrip('0').rstrip('.')


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# ── colours: theme.py glutes / quads / calves; session 2 grey as upper v3 ──
COL = {
    'hip':   dict(stripe='#085041', fill='#e1f5ee', stroke='#0f6e56', title='#085041', detail='#0f6e56'),
    'knee':  dict(stripe='#26215c', fill='#eeedfe', stroke='#534ab7', title='#26215c', detail='#3c3489'),
    'ankle': dict(stripe='#185fa5', fill='#e6f1fb', stroke='#378add', title='#042c53', detail='#185fa5'),
    'grey':  dict(stripe='#666666', fill='#f2f2f2', stroke='#aaaaaa', title='#333333', detail='#555555'),
}
BODY, FAINT, CAP = '#555555', '#d4d4d4', '#6f6f6f'


# ── geometry ─────────────────────────────────────────────────────────────────
def rad(a):
    return a * math.pi / 180


def pt(p, length, a):
    """Point at `length` from p in screen direction a (degrees, 0 = right, 90 = down)."""
    return (p[0] + length * math.cos(rad(a)), p[1] + length * math.sin(rad(a)))


def ang(p, q):
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))


def dist(p, q):
    return math.hypot(q[0] - p[0], q[1] - p[1])


def ik(a, b, l1, l2, pick):
    """Middle joint between a and b (segment l1 from a, l2 from b); pick chooses of two."""
    d0 = dist(a, b)
    d = min(d0, l1 + l2 - 1e-6)
    x = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    h = math.sqrt(max(l1 * l1 - x * x, 0.0))
    ux, uy = (b[0] - a[0]) / d0, (b[1] - a[1]) / d0
    mx, my = a[0] + ux * x, a[1] + uy * x
    return pick((mx - uy * h, my + ux * h), (mx + uy * h, my - ux * h))


def lower(c1, c2):
    return c1 if c1[1] > c2[1] else c2


def upper(c1, c2):
    return c1 if c1[1] < c2[1] else c2


def front(c1, c2):
    return c1 if c1[0] > c2[0] else c2


# ── timing: cosine-eased keyframes ──────────────────────────────────────────
def sched(pattern, start=0.0):
    vals, cur = [start], start
    for target, steps in pattern:
        for k in range(1, steps + 1):
            vals.append(cur + (target - cur) * (1 - math.cos(math.pi * k / steps)) / 2)
        cur = target
    assert len(vals) == N, len(vals)
    return vals


HOLD_MOVE = [(0, 3), (1, 10), (1, 7), (0, 10)]  # rest · move · hold ~2 s · return
BEAT = [(1, 15), (0, 15)]                       # one way, then back, on the beat


# ── picture builder ──────────────────────────────────────────────────────────
class Pic:
    def __init__(self, accent, dur, box_stroke=None):
        self.a, self.dur, self.els = accent, dur, []
        self.add('<rect x="0" y="0" width="156" height="132" rx="4" fill="#ffffff" '
                 f'stroke="{box_stroke or accent}" stroke-width="0.8"/>')

    def add(self, s):
        self.els.append(s)

    def an(self, attr, vals):
        return (f'<animate attributeName="{attr}" dur="{self.dur}" repeatCount="indefinite" '
                f'values="{";".join(vals)}"/>')

    def poly(self, frames, stroke=BODY, sw=3.4, dash=None, tag='polyline'):
        if isinstance(frames[0], tuple):
            frames = [frames]
        P = [' '.join(f'{f(x)},{f(y)}' for x, y in fr) for fr in frames]
        d = f' stroke-dasharray="{dash}"' if dash else ''
        head = (f'<{tag} points="{P[0]}" fill="none" stroke="{stroke}" stroke-width="{sw}"{d} '
                'stroke-linecap="round" stroke-linejoin="round"')
        if len(set(P)) == 1:
            self.add(head + '/>')
        else:
            self.add(head + '>' + self.an('points', P) + f'</{tag}>')

    def circ(self, frames, r, fill, stroke=None, sw=None):
        if isinstance(frames, tuple):
            frames = [frames]
        cx, cy = [f(p[0]) for p in frames], [f(p[1]) for p in frames]
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
        head = f'<circle cx="{cx[0]}" cy="{cy[0]}" r="{r}" fill="{fill}"{st}'
        an = ''
        if len(set(cx)) > 1:
            an += self.an('cx', cx)
        if len(set(cy)) > 1:
            an += self.an('cy', cy)
        self.add(head + ('>' + an + '</circle>' if an else '/>'))

    def head(self, frames, r=5.5):
        self.circ(frames, r, '#ffffff', BODY, 1.6)

    def faint_head(self, p, r=5.5):
        self.add(f'<circle cx="{f(p[0])}" cy="{f(p[1])}" r="{r}" fill="none" stroke="{FAINT}" stroke-width="1.6"/>')

    def dot(self, frames):
        if isinstance(frames, tuple):
            frames = [frames]
        if len({(f(p[0]), f(p[1])) for p in frames}) == 1:
            p = frames[0]
            self.add(f'<circle cx="{f(p[0])}" cy="{f(p[1])}" r="2.4" fill="{self.a}"/>')
        else:
            self.circ(frames, 2.4, self.a, self.a, 0.5)

    def wedge(self, frames):
        """frames: (vertex, start angle, end angle, radius, sweep flag) per keyframe."""
        D = []
        for v, a1, a2, r, sweep in frames:
            p1, p2 = pt(v, r, a1), pt(v, r, a2)
            D.append(f'M{f(v[0])},{f(v[1])} L{f(p1[0])},{f(p1[1])} '
                     f'A{r} {r} 0 0 {sweep} {f(p2[0])},{f(p2[1])} Z')
        head = (f'<path d="{D[0]}" fill="{self.a}" fill-opacity="0.18" '
                f'stroke="{self.a}" stroke-width="1"')
        self.add(head + ('>' + self.an('d', D) + '</path>' if len(set(D)) > 1 else '/>'))

    def text(self, x, y, t, col=None, anchor=None):
        a = f' text-anchor="{anchor}"' if anchor else ''
        self.add(f'<text font-size="9" fill="{col or self.a}" x="{f(x)}" y="{f(y)}"{a}>{esc(t)}</text>')

    def floor(self):
        self.add('<line x1="4" y1="100" x2="152" y2="100" stroke="#b8b8b8" stroke-width="1"/>')

    def mat(self):
        self.add('<rect x="10" y="96" width="136" height="4" rx="1" fill="#e4e4e4" '
                 'stroke="#b8b8b8" stroke-width="0.8"/>')

    def prop(self, x, y, w, h):
        self.add(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="1" '
                 'fill="#e4e4e4" stroke="#b8b8b8" stroke-width="0.8"/>')

    def line(self, x1, y1, x2, y2, sw=1.2):
        self.add(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" '
                 f'stroke="#b8b8b8" stroke-width="{sw}"/>')

    def aline(self, x1, y1, x2, y2, sw=1.6, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.add(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" '
                 f'stroke="{self.a}" stroke-width="{sw}"{d}/>')

    def beats(self, n, caption, x0=8, y=108, step=8):
        for k in range(n):
            if k == 0:
                v, kt = '1;0.2', f'0;{r4(1 / n)}'
            elif k == n - 1:
                v, kt = '0.2;1', f'0;{r4((n - 1) / n)}'
            else:
                v, kt = '0.2;1;0.2', f'0;{r4(k / n)};{r4((k + 1) / n)}'
            self.add(f'<circle cx="{x0 + k * step}" cy="{y}" r="2.8" fill="{self.a}" fill-opacity="0.45">'
                     f'<animate attributeName="fill-opacity" dur="{self.dur}" repeatCount="indefinite" '
                     f'calcMode="discrete" values="{v}" keyTimes="{kt}"/></circle>')
        self.text(x0 + (n - 1) * step + 10, y + 3, caption, CAP)

    def camera(self, caption):
        self.add('<rect x="6" y="119" width="11" height="8" rx="1.5" fill="none" stroke="#6f6f6f" '
                 'stroke-width="1"/><circle cx="11.5" cy="123" r="2.2" fill="none" stroke="#6f6f6f" '
                 'stroke-width="1"/><rect x="8" y="117.5" width="4" height="1.8" fill="#6f6f6f"/>')
        self.text(21, 126, caption, CAP)

    def svg(self, num, label, x, y):
        return '\n'.join([f'<!-- PIC {num} — {label} -->', f'<g transform="translate({x},{y})">']
                         + self.els + ['</g>'])


# ── pictures ─────────────────────────────────────────────────────────────────
SH, HP = (31, 92), (57, 92)          # supine: shoulder, hip on the mat
FAR_LEG = [SH, HP, (78, 92), (98, 92), (98, 84)]


def pic_hip_bend(acc):
    p = Pic(acc, '8s')
    p.mat()
    u = sched(HOLD_MOVE)

    def leg(x):
        phi, kap = 120 * x, 115 * x
        k = pt(HP, 21, -phi)
        sd = -phi + kap
        a = pt(k, 20, sd)
        return k, a, pt(a, 8, sd - 90)

    p.poly([HP, *leg(1)], FAINT)
    p.poly(FAR_LEG)
    p.head((21, 89.5))
    p.wedge([(HP, 0, -120 * x, 11, 0) for x in u])
    p.poly([[HP, *leg(x)] for x in u])
    p.poly([HP, (HP[0] + 28, 92)], acc, 1.4, dash='3 2')
    p.dot(HP)
    p.dot([leg(x)[0] for x in u])
    p.text(84, 34, 'knee to chest,')
    p.text(84, 43, 'no hands')
    p.text(8, 112, 'dots: hip · knee · mat line', CAP)
    p.camera('side view · lens at floor')
    return p


def pic_slr(acc):
    p = Pic(acc, '8s')
    p.mat()
    u = sched(HOLD_MOVE)

    def leg(x):
        phi = 95 * x
        k = pt(HP, 21, -phi)
        a = pt(HP, 41, -phi)
        return k, a, pt(a, 8, -phi - 90)

    p.poly([HP, *leg(1)], FAINT)
    p.poly(FAR_LEG)
    p.head((21, 89.5))
    p.wedge([(HP, 0, -95 * x, 11, 0) for x in u])
    p.poly([[HP, *leg(x)] for x in u])
    p.poly([HP, (HP[0] + 28, 92)], acc, 1.4, dash='3 2')
    p.dot(HP)
    p.dot([leg(x)[1] for x in u])
    p.text(86, 34, 'knee straight,')
    p.text(86, 43, 'not forced')
    p.text(8, 112, 'dots: hip · ankle · mat line', CAP)
    p.camera('side view · lens at floor')
    return p


def pic_side_lift(acc):
    p = Pic(acc, '8s')
    p.floor()
    p.line(36, 24, 36, 100, 2.4)                        # frame upright
    u = sched(HOLD_MOVE)
    hip = (74, 62)

    def leg(x):
        th = rad(40 * x)
        return ((hip[0] + 19 * math.sin(th), hip[1] + 19 * math.cos(th)),
                (hip[0] + 38 * math.sin(th), hip[1] + 38 * math.cos(th)))

    p.poly([hip, *leg(1)], FAINT)
    p.poly([(66, 100), (66, 81), (66, 62)])
    p.poly([(61, 35), (79, 35), (75, 62), (65, 62)], tag='polygon')
    p.head((70, 27), 6)
    p.poly([(62, 37), (49, 47), (37, 52)], sw=3)          # hand on the frame
    p.poly([(78, 37), (81, 49), (82, 60)], sw=3)
    p.poly([hip, (74, 100)], acc, 1.4, dash='3 2')
    p.wedge([(hip, 90, 90 - 40 * x, 12, 0) for x in u])
    p.poly([[hip, *leg(x)] for x in u])
    p.dot(hip)
    p.dot([leg(x)[1] for x in u])
    p.text(92, 40, 'belt line')
    p.text(92, 49, 'stays level')
    p.text(8, 112, 'angle: vertical → leg', CAP)
    p.camera('front view · lens at hip')
    return p


def pic_knee_range(acc):
    p = Pic(acc, '10s')
    p.mat()
    kap = sched([(-5, 3), (-5, 2), (0, 3), (140, 9), (140, 6), (0, 7)])

    def leg(k):
        if k <= 0:
            kn = (78, 92)
            sd = k
            a = pt(kn, 20, sd)
        else:
            d = math.sqrt(21 ** 2 + 20 ** 2 - 2 * 21 * 20 * math.cos(math.pi - rad(k)))
            al = math.degrees(math.acos((21 ** 2 + d * d - 20 ** 2) / (2 * 21 * d)))
            kn = pt(HP, 21, -al)
            a = (HP[0] + d, 92)
            sd = ang(kn, a)
        return kn, a, pt(a, 8, sd - 90)

    def wd(k):
        kn, a, _ = leg(max(k, 0))
        return (kn, ang(kn, HP), ang(kn, a), 7, 0)

    p.poly([HP, *leg(140)], FAINT)
    p.poly(FAR_LEG)
    p.head((21, 89.5))
    p.wedge([wd(k) for k in kap])
    p.poly([[HP, *leg(k)] for k in kap])
    p.dot(HP)
    p.dot([leg(k)[0] for k in kap])
    p.dot([leg(k)[1] for k in kap])
    p.text(92, 60, 'heel lifts =')
    p.text(92, 69, 'past straight')
    p.text(8, 112, 'dots: hip · knee · ankle', CAP)
    p.camera('side view · lens at floor')
    return p


def pic_knee_to_wall(acc):
    p = Pic(acc, '8s')
    p.floor()
    p.line(114, 10, 114, 100, 2.4)                      # wall
    u = sched(HOLD_MOVE)
    ank, toe = (100, 100), (107, 100)
    btoe, bank = (72, 100), (66, 96)

    def pose(x):
        th, g, tau = rad(8 + 30 * x), rad(40 + 15 * x), rad(8 + 6 * x)
        kn = (ank[0] + 20 * math.sin(th), ank[1] - 20 * math.cos(th))
        hp = (kn[0] - 21 * math.sin(g), kn[1] - 21 * math.cos(g))
        bk = ik(bank, hp, 20, 21, lower)
        sh = (hp[0] + 26 * math.sin(tau), hp[1] - 26 * math.cos(tau))
        hd = (sh[0] + 7.7 * math.sin(tau), sh[1] - 7.7 * math.cos(tau))
        hand = (112.5, sh[1] + 6)
        el = ik(sh, hand, 14, 13, lower)
        return dict(K=kn, H=hp, BK=bk, S=sh, Hd=hd, arm=[sh, el, hand])

    e = pose(1)
    p.poly([btoe, bank, e['BK'], e['H']], FAINT)
    p.poly([toe, ank, e['K'], e['H'], e['S']], FAINT)
    F = [pose(x) for x in u]
    p.poly([[btoe, bank, fr['BK'], fr['H']] for fr in F])
    p.poly([[toe, ank, fr['K'], fr['H'], fr['S']] for fr in F])
    p.head([fr['Hd'] for fr in F])
    p.poly([fr['arm'] for fr in F], sw=3)
    p.poly([ank, (100, 76)], acc, 1.4, dash='3 2')
    p.wedge([(ank, -90, ang(ank, fr['K']), 10, 1) for fr in F])
    p.dot(ank)
    p.dot([fr['K'] for fr in F])
    p.aline(107, 102, 107, 106)
    p.aline(114, 102, 114, 106)
    p.aline(107, 104, 114, 104, 1, '2 2')
    p.text(118, 107, 'gap, cm')
    p.text(8, 24, 'heel down,')
    p.text(8, 33, 'knee to wall')
    p.text(8, 112, 'dots: ankle · knee', CAP)
    p.camera('side view · lens at shin')
    return p


def pic_step_down(acc):
    p = Pic(acc, '4s')
    p.floor()
    p.prop(44, 88, 30, 12)                              # 20 cm box
    u = sched(BEAT)

    def pose(x):
        d = 12 * x
        return dict(st=[(64, 88), (64, 68 + d / 2), (64, 48 + d)],
                    fr=[(76, 48 + d), (76.5, 68 + d), (77, 88 + d)],
                    to=[(59, 22 + d), (81, 22 + d), (77, 48 + d), (63, 48 + d)],
                    hd=(70, 14 + d),
                    al=[(60, 24 + d), (54, 36 + d), (63, 46 + d)],
                    ar=[(80, 24 + d), (86, 36 + d), (77, 46 + d)],
                    pv=[(56, 48 + d), (84, 48 + d)])

    e = pose(1)
    p.poly(e['fr'], FAINT)
    p.poly(e['to'], FAINT, tag='polygon')
    p.faint_head(e['hd'], 6)
    F = [pose(x) for x in u]
    p.poly([fr['st'] for fr in F])
    p.poly([fr['fr'] for fr in F])
    p.poly([fr['to'] for fr in F], tag='polygon')
    p.head([fr['hd'] for fr in F], 6)
    p.poly([fr['al'] for fr in F], sw=3)
    p.poly([fr['ar'] for fr in F], sw=3)
    p.poly([(64, 44), (64, 92)], acc, 1.4, dash='3 2')
    p.poly([fr['pv'] for fr in F], acc, 1.4, dash='3 2')
    p.dot([fr['st'][1] for fr in F])
    p.text(94, 58, 'pelvis level')
    p.text(94, 76, 'knee over')
    p.text(94, 85, '2nd toe')
    p.beats(4, '2 beats down · 2 up')
    p.camera('in front · lens at knee')
    return p


def pic_heel_behind(acc):
    p = Pic(acc, '2s')
    p.floor()
    u = sched(BEAT)

    def pose(x):
        r = 7 * x
        return dict(st=[(64, 100 - r), (64, 95 - r), (64, 76 - r), (64, 56 - r)],
                    fr=[(74, 56 - r), (75, 70 - r), (73, 79 - r)],
                    to=[(59, 30 - r), (79, 30 - r), (75, 56 - r), (63, 56 - r)],
                    hd=(69, 22 - r),
                    al=[(60, 32 - r), (53, 38 - r), (52, 31 - r)],
                    ar=[(78, 32 - r), (85, 38 - r), (86, 31 - r)],
                    ach=[(64, 100 - r), (64, 80 - r)])

    e = pose(1)
    p.poly(e['st'], FAINT)
    p.poly(e['to'], FAINT, tag='polygon')
    F = [pose(x) for x in u]
    p.poly([fr['fr'] for fr in F])
    p.poly([fr['st'] for fr in F])
    p.poly([fr['to'] for fr in F], tag='polygon')
    p.head([fr['hd'] for fr in F], 6)
    p.poly([fr['al'] for fr in F], sw=3)
    p.poly([fr['ar'] for fr in F], sw=3)
    p.poly([fr['ach'] for fr in F], acc, 1.4, dash='3 2')
    p.aline(67, 93, 71, 93)
    p.text(75, 96, 'full height')
    p.text(94, 62, 'heel stays')
    p.text(94, 71, 'straight')
    p.beats(2, '1 beat up · 1 down')
    p.camera('behind · lens at ankle')
    return p


def pie(c, r, a):
    """Clock-face pie from 12 o'clock, a degrees clockwise; two arcs keep the flags fixed."""
    top = (c[0], c[1] - r)
    a1 = min(a, 180)
    p1 = (c[0] + r * math.sin(rad(a1)), c[1] - r * math.cos(rad(a1)))
    p2 = (c[0] + r * math.sin(rad(a)), c[1] - r * math.cos(rad(a)))
    return (f'M{f(c[0])},{f(c[1])} L{f(top[0])},{f(top[1])} A{r} {r} 0 0 1 {f(p1[0])},{f(p1[1])} '
            f'A{r} {r} 0 0 1 {f(p2[0])},{f(p2[1])} Z')


def pic_stance(acc):
    p = Pic(acc, '10s')
    p.floor()
    u = sched([(0, 3), (1, 4), (1, 17), (0, 6)])

    def free(x):
        return [(64, 60), (66 - x, 80 - 3 * x), (64 - 2 * x, 100 - 7 * x)]

    p.poly(free(1), FAINT)
    p.poly([(56, 100), (56, 80), (56, 60)])
    p.poly([free(x) for x in u])
    p.poly([(51, 34), (69, 34), (65, 60), (55, 60)], tag='polygon')
    p.head((60, 26), 6)
    p.poly([(52, 37), (55, 45), (67, 43)], sw=3)          # arms crossed
    p.poly([(68, 37), (65, 45), (53, 43)], sw=3)
    c = (118, 42)
    p.add(f'<circle cx="{c[0]}" cy="{c[1]}" r="13" fill="none" stroke="{FAINT}" stroke-width="2"/>')
    angles = [0.0 if i <= 7 else (359.9 * (i - 7) / 17 if i <= 24 else 0.0) for i in range(N)]
    D = [pie(c, 13, a) for a in angles]
    p.add(f'<path d="{D[0]}" fill="{acc}" fill-opacity="0.35" stroke="{acc}" stroke-width="1">'
          + p.an('d', D) + '</path>')
    p.text(118, 66, '30 s', anchor='middle')
    p.text(92, 82, 'eyes open,')
    p.text(92, 91, 'arms crossed')
    p.text(8, 112, 'no touchdown · no wobble', CAP)
    p.camera('in front · lens at ankle')
    return p


def pic_sl_squat(acc):
    p = Pic(acc, '2s')
    p.floor()
    u = sched(BEAT)

    def pose(x):
        d = 9 * x
        return dict(st=[(62, 100), (62, 80 + d / 2), (62, 60 + d)],
                    fr=[(72, 60 + d), (74, 73 + d), (73, 84 + d)],
                    to=[(57, 34 + d), (77, 34 + d), (73, 60 + d), (61, 60 + d)],
                    hd=(67, 26 + d),
                    a1=[(58, 37 + d), (61, 45 + d), (73, 43 + d)],
                    a2=[(76, 37 + d), (73, 45 + d), (61, 43 + d)],
                    pv=[(54, 60 + d), (80, 60 + d)])

    e = pose(1)
    p.poly(e['fr'], FAINT)
    p.poly(e['to'], FAINT, tag='polygon')
    p.faint_head(e['hd'], 6)
    F = [pose(x) for x in u]
    p.poly([fr['st'] for fr in F])
    p.poly([fr['fr'] for fr in F])
    p.poly([fr['to'] for fr in F], tag='polygon')
    p.head([fr['hd'] for fr in F], 6)
    p.poly([fr['a1'] for fr in F], sw=3)
    p.poly([fr['a2'] for fr in F], sw=3)
    p.poly([(62, 56), (62, 100)], acc, 1.4, dash='3 2')
    p.poly([fr['pv'] for fr in F], acc, 1.4, dash='3 2')
    p.dot([fr['st'][1] for fr in F])
    p.text(88, 56, 'pelvis level')
    p.text(88, 78, 'knee over')
    p.text(88, 87, 'the foot')
    p.beats(2, '1 beat down · 1 up')
    p.camera('in front · lens at hip')
    return p


def pic_sit_to_stand(acc):
    p = Pic(acc, '4s')
    p.floor()
    p.prop(12, 88, 40, 4)                               # bench
    p.line(16, 92, 16, 100)
    p.line(48, 92, 48, 100)
    p.prop(16, 81, 32, 7)                               # low box = raised seat
    u = [1 - x for x in sched(BEAT)]                    # 1 standing, 0 touching the seat
    ank, toe = (62, 100), (69, 100)

    def pose(x):
        hp = (41 + 22.5 * (1 - (1 - x) ** 2), 78 - 18 * x * x)
        kn = ik(ank, hp, 20, 21, front)
        t = rad(15 + 30 * math.sin(math.pi * x) - 11 * x)
        sh = (hp[0] + 26 * math.sin(t), hp[1] - 26 * math.cos(t))
        hd = (sh[0] + 7.7 * math.sin(t), sh[1] - 7.7 * math.cos(t))

        def rot(dx, dy):
            return (sh[0] + dx * math.cos(t) - dy * math.sin(t), sh[1] + dx * math.sin(t) + dy * math.cos(t))

        psi = rad(72 - 38 * x)
        fk = (hp[0] + 21 * math.sin(psi), hp[1] + 21 * math.cos(psi))
        fa = (fk[0] + 20 * math.sin(psi + rad(5)), fk[1] + 20 * math.cos(psi + rad(5)))
        return dict(K=kn, H=hp, S=sh, Hd=hd, arm=[sh, rot(6, 8), rot(-1, 11)], fr=[hp, fk, fa])

    e = pose(0)
    p.poly(e['fr'], FAINT)
    p.poly([toe, ank, e['K'], e['H'], e['S']], FAINT)
    p.faint_head(e['Hd'])
    F = [pose(x) for x in u]
    p.poly([fr['fr'] for fr in F], sw=3)
    p.poly([[toe, ank, fr['K'], fr['H'], fr['S']] for fr in F])
    p.head([fr['Hd'] for fr in F])
    p.poly([fr['arm'] for fr in F], sw=3)
    p.dot([fr['K'] for fr in F])
    p.text(94, 38, 'thigh above')
    p.text(94, 47, 'parallel;')
    p.text(94, 56, 'touch, no sit')
    p.beats(4, '2 beats down · 2 up')
    p.camera('side view · lens at seat')
    return p


def pic_bridge(acc):
    p = Pic(acc, '2s')
    p.mat()
    p.prop(82, 73, 56, 4)                               # bench top
    p.line(86, 77, 86, 96)
    p.line(134, 77, 134, 96)
    heel = (91.5, 71)

    def hip(ps):
        return (SH[0] + 26 * math.cos(rad(ps)), SH[1] - 26 * math.sin(rad(ps)))

    def knee(hp):
        return ik(hp, heel, 21, 20, upper)

    lo, hi = 2.0, 60.0                                  # top: shoulder, hip and knee in line
    for _ in range(60):
        mid = (lo + hi) / 2
        hp = hip(mid)
        if ang(hp, knee(hp)) - ang(SH, hp) < 0:
            lo = mid
        else:
            hi = mid
    top = (lo + hi) / 2
    u = sched(BEAT)

    def pose(x):
        ps = top * x
        hp = hip(ps)
        kn = knee(hp)
        t = (math.cos(rad(ps)), -math.sin(rad(ps)))
        n = (-math.sin(rad(ps)), -math.cos(rad(ps)))
        el = (SH[0] + 10 * t[0] + 6 * n[0], SH[1] + 10 * t[1] + 6 * n[1])
        hd = (SH[0] + 3 * t[0] + 9 * n[0], SH[1] + 3 * t[1] + 9 * n[1])
        return dict(H=hp, K=kn, T=pt(heel, 8, ang(kn, heel) - 90),
                    up=[hp, (hp[0], hp[1] - 21), (hp[0], hp[1] - 41)], arm=[SH, el, hd])

    e = pose(1)
    p.poly(e['up'], FAINT)
    p.poly([SH, e['H'], e['K'], heel, e['T']], FAINT)
    F = [pose(x) for x in u]
    p.poly([fr['up'] for fr in F], sw=3)
    p.poly([[SH, fr['H'], fr['K'], heel, fr['T']] for fr in F])
    p.head((21, 89.5))
    p.poly([fr['arm'] for fr in F], sw=3)
    p.dot([fr['K'] for fr in F])
    p.text(96, 52, 'knee ~20°,')
    p.text(96, 61, 'heel fixed')
    p.beats(2, '1 beat up · 1 down')
    p.camera('side view · lens at bench')
    return p


def pic_heel_side(acc):
    p = Pic(acc, '2s')
    p.floor()
    p.line(26, 10, 26, 100, 2.4)                        # wall
    u = sched(BEAT)
    toe = (46, 100)

    def pose(x):
        b = rad(50 * x)
        a = (toe[0] + 8 * math.cos(b), toe[1] - 8 * math.sin(b))
        kn = (a[0] - 0.6, a[1] - 20)
        hp = (kn[0] + 0.6, kn[1] - 21)
        sh = (hp[0] - 1.5, hp[1] - 26)
        hd = (sh[0] - 0.5, sh[1] - 7.7)
        hand = (27.5, sh[1] + 2)
        el = ik(sh, hand, 14, 13, lower)
        fk = (hp[0] - 2, hp[1] + 21)
        return dict(A=a, K=kn, H=hp, S=sh, Hd=hd, arm=[sh, el, hand],
                    fr=[hp, fk, (fk[0] + 17.3, fk[1] - 10)])

    e = pose(1)
    p.poly([toe, e['A'], e['K'], e['H'], e['S']], FAINT)
    F = [pose(x) for x in u]
    p.poly([fr['fr'] for fr in F], sw=3)
    p.poly([[toe, fr['A'], fr['K'], fr['H'], fr['S']] for fr in F])
    p.head([fr['Hd'] for fr in F])
    p.poly([fr['arm'] for fr in F], sw=3)
    ty = e['A'][1]
    p.aline(58, ty, 82, ty, 1.4, '3 2')
    p.dot([fr['A'] for fr in F])
    p.text(86, ty + 3, 'full height')
    p.beats(2, '1 beat up · 1 down')
    p.camera('side view · lens at ankle')
    return p


def pic_bars():
    p = Pic('#185fa5', '1s', box_stroke='#aaaaaa')
    bar = '#185fa5'
    w = 94.6
    sc = w / 30
    p.text(8, 22, 'Heel raises, mean of 2 sessions', CAP)
    p.text(8, 44, 'Left', CAP)
    p.add(f'<rect x="34" y="36" width="{f(27.5 * sc)}" height="10" rx="1.5" fill="{bar}" fill-opacity="0.55"/>')
    p.text(34 + 27.5 * sc + 4, 44, '27.5', CAP)
    p.text(8, 66, 'Right', CAP)
    p.add(f'<rect x="34" y="58" width="{f(w)}" height="10" rx="1.5" fill="{bar}"/>')
    p.text(34 + w + 4, 66, '30', CAP)
    lx = 34 + 0.9 * w
    p.add(f'<line x1="{f(lx)}" y1="30" x2="{f(lx)}" y2="74" stroke="#333333" stroke-width="1" '
          'stroke-dasharray="3 2"/>')
    p.text(lx, 84, '90% line', CAP, 'middle')
    p.text(8, 102, '27.5 ÷ 30 = 92% → pass', bar)
    p.text(6, 126, 'weaker ÷ stronger', CAP)
    return p


# ── card text ────────────────────────────────────────────────────────────────
KIN = ('How to: Kinovea angle tools ↗', 'https://kinovea.readthedocs.io/en/stable/measurement/angle.html')
V_WALL = ('Video: Physiotutors, wall test ↗', 'https://www.youtube.com/watch?v=U7woPNLUT3Q')
V_STEP = ('Video: Professional Seminars, lateral step-down ↗', 'https://www.youtube.com/watch?v=0XplbMnHcOs')
V_HEEL = ('Video: Missy Fraser PhD, single-leg heel raise ↗', 'https://www.youtube.com/watch?v=O4XF2njh7NA')
V_STANCE = ('Video: AAOP, timed single-leg stance ↗', 'https://www.youtube.com/watch?v=OQuUxUZQjQ0')
V_SQUAT = ('Video: USC Athletic Training, single-leg squat ↗', 'https://www.youtube.com/watch?v=5bzEI_yrr4o')
V_STS = ('Video: Physiotherapy UC Copenhagen, one-leg sit to stand ↗',
         'https://www.youtube.com/watch?v=a1zcZND3q2w')
V_BRIDGE = ('Video: Sport Rehab Guide, single-leg hamstring bridge ↗',
            'https://www.youtube.com/watch?v=9pjW1AoEI58')

SECTIONS = [
    ('A', 'A RANGES',
     'A — Session 1: Ranges  (~15 min · no weights · your own effort only; card 5 leans body weight)', [
        dict(n=1, g='hip', label='Hip bend range', title='Hip bend range, knee bent — each leg',
             rows=[('Set-up', 'Lie on your back on the mat, legs straight, side-on to the camera, 2 m '
                              'away, lens at floor level, the tested leg nearest the camera.'),
                   ('Do', 'Bring the knee toward your chest as far as it goes by itself: hip muscles '
                          'only, no hands; the knee bends freely, the other leg stays flat. Hold 2 s; '
                          'lower. 3 tries per leg.'),
                   ('Read', "Kinovea, end frame: Angle tool, centre on the hip, one leg along the mat "
                            "toward your feet, the other to the knee."),
                   ('Write down', 'The best of 3, per leg. Training limit: 70–80% of it (squat and '
                                  'hip-thrust depth).')],
             links=[KIN], dose='3 tries per leg', kit='Mat · tripod · phone', pic=pic_hip_bend),
        dict(n=2, g='hip', label='Straight-leg raise range', title='Straight-leg raise range — each leg',
             rows=[('Set-up', 'As card 1: on your back, legs straight, the tested leg nearest the '
                              'camera, lens at floor level.'),
                   ('Do', "Raise the straight leg as far as it goes by itself, the other leg flat on the "
                          "mat; don't force the knee straight. Hold 2 s; lower. 3 tries per leg."),
                   ('Read', 'Kinovea, top frame: Angle tool, centre on the hip, one leg along the mat '
                            'toward your feet, the other to the ankle.'),
                   ('Write down', 'The best of 3, per leg. RDL depth stops at 70–80% of it.')],
             links=[KIN], dose='3 tries per leg', kit='Mat · tripod · phone', pic=pic_slr),
        dict(n=3, g='hip', label='Hip side-lift range', title='Hip side-lift range, standing — each leg',
             rows=[('Set-up', 'Stand facing the camera, 2 m away, lens at hip height, one hand on the '
                              'frame, feet together, belt line level.'),
                   ('Do', "Lift the straight leg out to the side as far as it goes by itself, toes "
                          "forward, pelvis and trunk still. Hold 2 s; lower. A try whose belt line "
                          "tilts doesn't count. 3 tries per leg."),
                   ('Read', 'Kinovea, top frame: Angle-to-vertical tool along the lifted leg, hip to '
                            'ankle.'),
                   ('Write down', 'The best of 3, per leg. Training limit: 70–80% of it (hip machine, '
                                  'banded hip work).')],
             links=[KIN], dose='3 tries per leg', kit='Frame · tripod · phone', pic=pic_side_lift),
        dict(n=4, g='knee', label='Knee range', title='Knee range — each leg',
             rows=[('Set-up', 'Lie on your back, legs straight, side-on, lens at floor level, the '
                              'tested leg nearest the camera.'),
                   ('Do', 'Tighten the thigh to straighten the knee fully; hold 2 s. Then slide the '
                          'heel along the mat toward your buttock as far as it goes by itself; hold '
                          '2 s. 3 tries per leg.'),
                   ('Read', 'Kinovea, both end frames: Angle tool, centre on the knee, legs to the hip '
                            'and the ankle.'),
                   ('Write down', 'Both numbers per leg, and whether the heel lifts off the mat as you '
                                  'straighten (= the knee bows past straight: yes/no).')],
             links=[KIN], dose='3 tries per leg', kit='Mat · tripod · phone', pic=pic_knee_range),
        dict(n=5, g='ankle', label='Knee-to-wall lunge', title='Knee-to-wall lunge (ankle range) — each leg',
             rows=[('Set-up', 'Barefoot, face the wall, tested foot pointing straight at it, toes '
                              '~10 cm away, the other foot a step behind, hands on the wall. Lens '
                              'side-on at shin height, tested leg nearest the camera.'),
                   ('Do', 'Bend the front knee slowly to touch the wall, heel flat, knee over the '
                          'second toe; hold 2 s. If it touches, move the foot back 1 cm and repeat; '
                          'stop at the last touch with the heel down. No bounce.'),
                   ('Read', 'Kinovea, the last clean touch: Angle-to-vertical tool along the shin, '
                            'ankle to knee.'),
                   ('Write down', 'That angle and the toe-to-wall gap (cm), per leg. Training limit: '
                                  '70–80% of the angle.')],
             links=[KIN, V_WALL], dose='1 cm steps, per leg', kit='Wall · tape measure · tripod',
             pic=pic_knee_to_wall),
    ]),
    ('B', 'B CONTROL TESTS',
     'B — Session 1: Control tests  (~15 min · each clean or not · film every one)', [
        dict(n=6, g='knee', label='Step-down', title='Step-down — each leg',
             rows=[('Set-up', 'Barefoot on the 20 cm box, tested foot near its edge, the other leg '
                              'hanging beside it, hands on hips. Camera in front, 2 m, lens at knee '
                              'height. Metronome 60: 2 beats down, 2 up.'),
                   ('Do', 'Bend the standing knee slowly until the other heel just touches the '
                          'floor, no weight on it, then straighten, knee soft at the top. 10 reps '
                          'per leg.'),
                   ('Fail if', 'On any rep the knee drifts inside the second toe (valgus) or the '
                               'pelvis drops on the free side; any pain.'),
                   ('Write down', 'Clean or not, per leg.')],
             links=[V_STEP], dose='10 reps per leg', kit='20 cm box · tripod', pic=pic_step_down),
        dict(n=7, g='ankle', label='Heel-raise control set', title='Heel-raise control set — each leg',
             rows=[('Set-up', 'Barefoot on one leg on a flat floor, fingertips on the wall at shoulder '
                              'height, knee straight but soft. Camera behind you, 2 m, lens at ankle '
                              'height. Metronome 60: up on one beat, down on the next.'),
                   ('Do', 'Rise onto the ball of the foot as high as it goes, then lower to the floor. '
                          '10 reps per leg, on the beat.'),
                   ('Fail if', "A rep stops short of your first reps' height, the heel wobbles in or "
                               "out, a beat is missed, or any pain."),
                   ('Write down', 'Clean or not, per leg. Then card 8.')],
             links=[V_HEEL], dose='10 reps per leg', kit='Wall · tripod', pic=pic_heel_behind),
        dict(n=8, g='ankle', label='Single-leg stance', title='Single-leg stance, 30 s — each leg',
             rows=[('Set-up', 'Barefoot on one leg, arms crossed on the chest, eyes open, the other '
                              'foot just off the floor beside the ankle. Camera in front, lens at '
                              'ankle height.'),
                   ('Do', 'Hold 30 s per leg.'),
                   ('Fail if', 'The lifted foot touches down, the standing foot wobbles or shifts, the '
                               'arms uncross, or any pain.'),
                   ('Write down', "Clean or not, per leg. Cards 7 and 8 together are the ankle's "
                                  "control test: both clean.")],
             links=[V_STANCE], dose='30 s per leg', kit='Tripod · phone', pic=pic_stance),
        dict(n=9, g='hip', label='Single-leg squat', title='Single-leg squat — each leg',
             rows=[('Set-up', 'Barefoot on one leg, arms crossed on the chest, the other leg held a '
                              'little forward. Camera in front, 2 m, lens at hip height. Metronome 60: '
                              '1 beat down, 1 up.'),
                   ('Do', 'Squat until the knee is bent about 60° (two-thirds of a right angle, thigh '
                          'well above parallel), then stand. 5 reps per leg, on the beat.'),
                   ('Fail if', "Any of Crossley's five is not good: overall (balance, smooth, on the "
                               "beat), trunk (leans or turns), pelvis (drops or turns), hip (thigh "
                               "drifts in), knee (moves inside the foot); any pain."),
                   ('Write down', 'Good or not, per criterion, per leg.')],
             links=[V_SQUAT], dose='5 reps per leg', kit='Tripod · phone', pic=pic_sl_squat),
    ]),
    ('C', 'C SYMMETRY TESTS',
     'C — Session 1: Symmetry tests  (~20 min · each leg to technical failure · ≥3 min between sides)', [
        dict(n=10, g='knee', label='Single-leg sit-to-stand', title='Single-leg sit-to-stand — each leg',
             rows=[('Set-up', 'Seat: the low box on the bench, thighs just above parallel when '
                              'seated. Sit on its front half, foot on a tape mark, the other leg held '
                              'forward off the floor, arms crossed. Lens side-on at seat height. '
                              'Metronome 60: 2 beats down, 2 up.'),
                   ('Do', 'Stand up on one leg, knee soft at the top; lower for 2 beats to touch the '
                          'seat without sitting; stand again. Keep going.'),
                   ('Stop when', 'A rep misses the beat, the free foot touches down, the arms uncross, '
                                 'the trunk lurches or rocks to get up, the knee caves in or snaps '
                                 'straight, or the seat takes your weight.'),
                   ('Write down', 'Reps before the first miss, per leg; seat height in cm.')],
             links=[V_STS], dose='1 set per leg', kit='Bench · low box · tripod', pic=pic_sit_to_stand),
        dict(n=11, g='hip', label='Single-leg bridge', title='Single-leg bridge — each leg',
             rows=[('Set-up', 'On your back on the mat, the tested heel on the bench, knee bent ~20°, '
                              'the other leg held straight up, arms crossed on the chest; mark the '
                              'heel spot. Lens side-on at bench height. Metronome 60: up on one beat, '
                              'down on the next.'),
                   ('Do', 'Push the heel down to lift the hips until shoulder, hip and knee line up; '
                          'lower to a light touch on the mat. Keep going.'),
                   ('Stop when', 'The hips miss the top line, a beat is missed, the heel slides, the '
                                 'pelvis twists, or you rest at the bottom.'),
                   ('Write down', 'Reps before the first miss, per leg.')],
             links=[V_BRIDGE], dose='1 set per leg', kit='Bench · mat · tripod', pic=pic_bridge),
        dict(n=12, g='ankle', label='Single-leg heel raises', title='Single-leg heel raises — each leg',
             rows=[('Set-up', 'As card 7: barefoot, flat floor, fingertips on the wall at '
                              'shoulder height, same spot every time. Lens side-on at ankle '
                              'height. Metronome 60: up on one beat, down on the next.'),
                   ('Do', 'Heel raises as high as they go, knee straight but soft; keep going, on '
                          'the beat.'),
                   ('Stop when', 'A rep misses full height (against your first reps), misses the beat, '
                                 'the knee bends, or you lean on the wall.'),
                   ('Write down', 'Reps before the first miss, per leg.')],
             links=[V_HEEL], dose='1 set per leg', kit='Wall · tripod', pic=pic_heel_side),
    ]),
    ('D', 'D SESSION 2',
     'D — Session 2: 2–7 days later  (~20 min · symmetry tests only)', [
        dict(n=13, g='grey', label='Repeat symmetry tests', title='Repeat 10–12 — other side first',
             rows=[('Set-up', '2–7 days after session 1: the same warm-up, seat, heel spot, wall '
                              'spot, beat and set-up. Start with the other side.'),
                   ('Do', 'Tests 10, 11 and 12 once more.'),
                   ('Score', 'Mean of both sessions, weaker ÷ stronger: ≥90% passes.'),
                   ('Example', 'Heel raises left 27 and 28, right 30 and 30: 27.5 ÷ 30 = 92%, a '
                               'pass.')],
             links=[], dose='1 set per leg', kit='As session 1', pic=lambda acc: pic_bars()),
    ]),
]

PRE_LINES = [
    'What: tests that decide when each lower-body joint may move up one loading stage. Order: A, B, C, then D.',
    'When: a rested day, no lower-body training or badminton the day before. Warm up 5 min (walk or bike).',
    'Day after: no badminton — the symmetry tests take calves, quads and glutes to technical failure.',
    'Phone = camera only: on the tripod ~2 m away, level, lens at the height the card names; never in your hand.',
    'Beat: a metronome on a second device (PC, tablet or speaker), loud enough for the video to record it.',
    'iPhone (iOS 18 or later): turn on Settings → Camera → Record Sound → Allow Audio Playback.',
    "Angles: later, on the PC, in Kinovea (free): open the video, pause on the frame, pick the card's tool,",
    'drag its centre onto the joint, note the number (over 180°: 360 minus it), snip the frame (Win+Shift+S).',
    'Pictures move when this file opens in Edge or Chrome; elsewhere they show the start (dark) and end (faint).',
    'Kit: the 20 cm box · bench · wall · frame or rack to hold · mat · tape measure · tape · tripod and phone',
    'a second device for the beat · Kinovea on the PC · barefoot for every test',
]
POST_LINES = [
    'Per joint: pain ≤5/10 during and after · back to normal the next morning · no swelling or warmth',
    'within 24 h · no “loose joint” feeling that day.',
    'Two clean weeks in a row are needed; a fail is a flare and restarts the count.',
]
RULES = [
    "These are tests, not training sets: follow each card's set-up exactly",
    'Stop at pain, a clunk, or a slipping or giving-way feeling — that test is not clean this round',
    'Same seat, box, spots, set-up and beat every time; barefoot; write down the seat height',
    'Film every test and judge it on the paused video, not by feel',
    "Ranges: your own effort only, nothing pushes further — except card 5's slow lean, heel flat",
    'No stretching before the range tests',
]
UNLOCK = [
    'A joint moves up one loading stage when all three hold: 2 clean step-gate weeks, a clean control test',
    'and a symmetry score of ≥90% over both sessions. Passing now opens stage 2 only.',
    'Knee at stage 2: squats may go below parallel, within 70–80% of your card-4 bend (R1 · R3).',
    'For 2→3: train ≥2 clean weeks at stage 2, then run this file again; the same for 3→4.',
    'The ranges (A) set your training limits at every stage; redo them after a flare.',
    'A flare drops a joint back one stage · court work (cardio routine) needs ankle, knee and hip at stage 4.',
    'Rules behind this file: Stage 0 §2.5–2.6 · R1 · R3 · R14 · D-61 · D-62 · D-67…D-69 · D-77…D-82 (gymspec).',
]
SEND = [
    ('#085041', 'Hip: bend ° L/R · leg-raise ° L/R · side-lift ° L/R · test 9 per criterion L/R · bridge reps L/R ×2'),
    ('#26215c', 'Knee: straight and bent ° L/R · heel lifts? L/R · test 6 clean? L/R · sit-to-stand reps L/R ×2 · seat cm'),
    ('#185fa5', 'Ankle: shin ° and gap cm L/R · tests 7–8 clean? L/R · heel-raise reps L/R ×2'),
    ('#666666', 'All: the Kinovea snips · step-gate clean weeks so far, per joint'),
]
VERSION = ('v1 — new file: hip, knee and ankle loading-gate tests as one-test cards with moving '
           'pictures and video links (D-80…D-82)')


# ── page builder ─────────────────────────────────────────────────────────────
def wrap(text, width=60):
    lines, cur = [], ''
    for w in text.split(' '):
        t = f'{cur} {w}' if cur else w
        if len(t) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def card(sec, c, y):
    col = COL[c['g']]
    body = []
    ty = y + 34
    for lab, txt in c['rows']:
        lines = wrap(txt)
        body.append(f'<text font-size="11" font-weight="500" fill="{col["title"]}" x="72" y="{ty}">{lab}</text>')
        for i, ln in enumerate(lines):
            body.append(f'<text font-size="11" fill="{col["detail"]}" x="136" y="{ty + 14 * i}">{esc(ln)}</text>')
        ty += 14 * len(lines)
    last = ty - 14
    if c['links']:
        ly, lx = last + 15, 72
        for lab, url in c['links']:
            body.append(f'<a href="{url}" target="_blank"><text font-size="10" fill="#185fa5" '
                        f'x="{lx}" y="{ly}">{esc(lab)}</text></a>')
            lx += round(len(lab) * 5.0) + 16
        last = ly
    h = max(178, last - y + 14)
    out = [f'<!-- {sec}{c["n"]} — {c["label"]} -->',
           f'<rect x="30" y="{y}" width="8" height="{h}" rx="2" fill="{col["stripe"]}"/>',
           f'<rect x="38" y="{y}" width="612" height="{h}" rx="4" fill="{col["fill"]}" '
           f'stroke="{col["stroke"]}" stroke-width="0.8"/>',
           f'<text font-size="11" font-weight="500" fill="#555" x="54" y="{y + 16}">{c["n"]}</text>',
           f'<text font-size="12" font-weight="500" fill="{col["title"]}" x="72" y="{y + 16}">{esc(c["title"])}</text>']
    out += body
    out += [f'<text font-size="12" font-weight="500" fill="{col["title"]}" x="490" y="{y + 16}">{esc(c["dose"])}</text>',
            f'<text font-size="11" fill="{col["detail"]}" x="490" y="{y + 31}">{esc(c["kit"])}</text>']
    out.append(c['pic'](col['stroke']).svg(c['n'], c['label'], 486, y + 38))
    return '\n'.join(out), h


def info_box(comment, y, title, lines, step, first, title_dy, pad, link_line=None):
    h = first + step * (len(lines) - 1) + pad
    out = [f'<!-- {comment} -->',
           f'<rect x="30" y="{y}" width="620" height="{h}" rx="8" fill="#e8f4fd" stroke="#5aabf0" stroke-width="1"/>',
           f'<text font-size="12" font-weight="500" fill="#1a5c8a" x="50" y="{y + title_dy}">{esc(title)}</text>']
    for i, ln in enumerate(lines):
        t = f'<text font-size="11" fill="#2272a8" x="50" y="{y + first + step * i}">{esc(ln)}</text>'
        if link_line is not None and i == link_line[0]:
            t = f'<a href="{link_line[1]}" target="_blank">{t}</a>'
        out.append(t)
    return '\n'.join(out), h


def build():
    blocks = []
    blocks.append('<text font-size="15" font-weight="500" fill="#1a1a1a" x="340" y="28" text-anchor="middle">'
                  'Lower-body evaluation — loading-gate tests</text>\n'
                  '<text font-size="11" fill="#666" x="340" y="44" text-anchor="middle">'
                  'Hip · knee · ankle — ranges, control and symmetry · 2 sessions (~50 + ~20 min)</text>')
    blocks.append('\n'.join([
        '<!-- LEGEND -->',
        '<rect x="30" y="54" width="620" height="56" rx="6" fill="#f7f7f7" stroke="#ccc" stroke-width="0.8"/>',
        '<text font-size="11" font-weight="500" fill="#1a1a1a" x="50" y="72">Muscle group</text>',
        '<rect x="50" y="89" width="10" height="10" rx="2" fill="#085041"/>',
        '<text font-size="11" fill="#333" x="66" y="98">Hip / glutes</text>',
        '<rect x="208" y="89" width="10" height="10" rx="2" fill="#26215c"/>',
        '<text font-size="11" fill="#333" x="224" y="98">Knee (quads, hamstrings)</text>',
        '<rect x="366" y="89" width="10" height="10" rx="2" fill="#185fa5"/>',
        '<text font-size="11" fill="#333" x="382" y="98">Ankle / calf</text>']))
    y = 122
    pre, h = info_box('PRE-WORKOUT NOTE', y, 'Before you start — what this is, and how the phone is used',
                      PRE_LINES, 13, 30, 17, 6, (6, KIN[1]))
    blocks.append(pre)
    y += h + 12
    for si, (sec, comment, header, cards) in enumerate(SECTIONS):
        blocks.append('\n'.join([
            f'<!-- ── {comment} ── -->',
            f'<rect x="30" y="{y}" width="620" height="24" rx="4" fill="#e8e8e8" stroke="#bbb" stroke-width="0.5"/>',
            f'<text font-size="12" font-weight="500" fill="#1a1a1a" x="50" y="{y + 16}">{esc(header)}</text>']))
        y += 34
        for ci, c in enumerate(cards):
            s, h = card(sec, c, y)
            blocks.append(s)
            y += h + (6 if ci < len(cards) - 1 else 0)
        y += 14 if si < len(SECTIONS) - 1 else 12
    post, h = info_box('POST-WORKOUT NOTE', y, 'Step-gate log — after every training session (exit criterion 1)',
                       POST_LINES, 13, 30, 17, 6)
    blocks.append(post)
    y += h + 12
    hr = 20 * len(RULES) + 32
    rl = ['<!-- GLOBAL RULES -->',
          f'<rect x="30" y="{y}" width="620" height="{hr}" rx="6" fill="#f7f7f7" stroke="#ccc" stroke-width="0.8"/>',
          f'<text font-size="12" font-weight="500" fill="#1a1a1a" x="50" y="{y + 22}">Every test — rules</text>']
    for i, r in enumerate(RULES):
        rl.append(f'<rect x="50" y="{y + 32 + 20 * i}" width="7" height="7" rx="1" fill="#e8a020"/>')
        rl.append(f'<text font-size="11" fill="#444" x="64" y="{y + 40 + 20 * i}">{esc(r)}</text>')
    blocks.append('\n'.join(rl))
    y += hr + 12
    tim, h = info_box('TIMING SUMMARY', y, 'What the results unlock — the same tests at every stage step',
                      UNLOCK, 17, 37, 20, 13)
    blocks.append(tim)
    y += h + 12
    hs = 18 * len(SEND) + 38
    sl = ['<!-- SET COUNT -->',
          f'<rect x="30" y="{y}" width="620" height="{hs}" rx="6" fill="#f7f7f7" stroke="#ccc" stroke-width="0.8"/>',
          f'<text font-size="12" font-weight="500" fill="#1a1a1a" x="50" y="{y + 22}">Send back to Claude — results per joint</text>']
    for i, (cl, t) in enumerate(SEND):
        sl.append(f'<text font-size="11" fill="{cl}" x="50" y="{y + 42 + 18 * i}">{esc(t)}</text>')
    blocks.append('\n'.join(sl))
    y += hs + 20
    blocks.append('<!-- VERSION NOTE -->\n'
                  f'<text font-size="9" fill="#aaa" x="340" y="{y}" text-anchor="middle">{esc(VERSION)}</text>')
    head = (f'<svg width="100%" viewBox="0 0 680 {y + 32}" xmlns="http://www.w3.org/2000/svg" '
            'style="font-family: sans-serif;">')
    return head + '\n\n' + '\n\n'.join(blocks) + '\n\n</svg>'


def main():
    out = sys.argv[1]
    svg = build()
    with open(out, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(svg)
    print(out, len(svg.encode('utf-8')), 'bytes')


if __name__ == '__main__':
    main()
