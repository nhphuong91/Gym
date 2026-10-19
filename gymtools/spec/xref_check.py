"""Cross-reference check for CLAUDE.md and the stage docs in gymspec/.

Run from gymspec/: python3 -B ../gymtools/spec/xref_check.py   (or pass the gymspec path)
Prints a summary, then ISSUES and RESULT. Exit code 0 when clean, 1 when issues are listed.

Reads ../CLAUDE.md, every Stage<n>_<Name>.md with its Stage<n>_SupplementInfo.md, and the
"## R#" headings of ../reference.md. A stage is checked as soon as both of its files exist.

How a reference resolves (each Supplement's header states its § convention):
- §x.y by its own prefix: a stage file name or "Policy Definition" -> that doc; "Supplement"
  -> the citing stage's Supplement; §R# -> reference.md. "Stage N", and no prefix in a
  Supplement, follow the Supplements' convention: the normative doc's headings, then the
  Supplement's. No prefix in a normative doc -> its own headings; in CLAUDE.md -> Stage 0.
- §x.y (a): when §x.y is an Accepted limits table, the letter must be one of its rows.
- D-##: by its own "Stage N" prefix or the last one earlier in the same chain
  ("Stage 0 D-47 · D-48"); otherwise the citing stage's log (Stage 0 for CLAUDE.md).
  Ranges such as D-70…D-76 are expanded.
- [W#] and M#: by their own "Stage N" prefix only ("Stage 0 [W64] · [W37]": W37 is the
  citing stage's); otherwise the citing stage's Supplement.
- R#: one numbering across stages. S<n>.<m>: the Steps table of Stage n.
Also checked: R-numbers run on without gaps from stage to stage; every rule not marked
withdrawn has an example row with a pass and a fail; every step row has Input, Action items
and Output; no "should" or "may" in a Rules section; duplicate IDs; each stage's Open items
against its "Open items:" note in CLAUDE.md <stages> and its open round in the Supplement.
Known false positives: none (checked 2026-10-09).
"""
import collections
import pathlib
import re
import sys

GYMSPEC = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('.')
issues = []


def read(path):
    return path.read_text(encoding='utf-8') if path.exists() else None


def issue(where, text, pos, what):
    loc = f'{where}:{text.count(chr(10), 0, pos) + 1}' if text is not None and pos is not None else where
    issues.append(f'{loc}  {what}')


def ranges(nums, fmt=str):
    nums = sorted(set(nums))
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(fmt(nums[i]) if i == j else f'{fmt(nums[i])}–{fmt(nums[j])}')
        i = j + 1
    return ', '.join(out) or 'none'


def section(text, start, end):
    """Text after the first line matching start, up to the next line matching end; and its offset."""
    m = re.search(start, text, re.M)
    if not m:
        return None, None
    rest = text[m.end():]
    e = re.search(end, rest, re.M)
    return (rest[:e.start()] if e else rest), m.end()


def dfmt(x):
    return f'D-{x:02d}'


def cells(row):
    return [c.strip() for c in row.strip().strip('|').split('|')]


def heads(text):
    return set(re.findall(r'^#{2,4} (\d+(?:\.\d+)*)[ .]', text, re.M))


def dupes(seq):
    return sorted(k for k, v in collections.Counter(seq).items() if v > 1)


def expand(tok, prefix):
    m = re.fullmatch(rf'{re.escape(prefix)}(\d+)(?: ?[…–] ?(?:{re.escape(prefix)})?(\d+))?', tok)
    a = int(m.group(1))
    b = int(m.group(2)) if m.group(2) else a
    return list(range(a, b + 1)) if 0 <= b - a <= 200 else [a, b]


# ---- load ------------------------------------------------------------------
P = read(GYMSPEC / '..' / 'CLAUDE.md')
if P is None:
    sys.exit('CLAUDE.md not found: run from gymspec/ or pass the gymspec path')
REFMD = read(GYMSPEC / '..' / 'reference.md') or ''
REF_HEADS = set(re.findall(r'^## (R\d+)\b', REFMD, re.M))

ST = {}
for path in sorted(GYMSPEC.glob('Stage[0-9]*_*.md')):
    m = re.fullmatch(r'Stage(\d+)_(\w+)\.md', path.name)
    if not m:
        continue
    n, part = int(m.group(1)), ('sup' if m.group(2) == 'SupplementInfo' else 'norm')
    st = ST.setdefault(n, {})
    if part in st:
        issue(path.name, None, None, f'a second normative doc for Stage {n} besides {st[part + "_name"]}')
        continue
    st[part], st[part + '_name'] = path.read_text(encoding='utf-8'), path.name
for n in sorted(ST):
    if 'norm' not in ST[n] or 'sup' not in ST[n]:
        print(f'Stage {n}: one of its two files is missing, so it is skipped')
        del ST[n]

# ---- per stage: definitions --------------------------------------------------
defined_R = {}
for n, st in sorted(ST.items()):
    norm, sup, nn, sn = st['norm'], st['sup'], st['norm_name'], st['sup_name']
    st['heads_norm'], st['heads_sup'] = heads(norm), heads(sup)

    rules, off = section(norm, r'^## \d+\. (?:Governing )?[Rr]ules\b.*$',
                         r'^#{2,3} (?:\d+(?:\.\d+)* )?Rule examples\b')
    st['rules'] = []
    if rules is None:
        issue(nn, None, None, 'no Rules section')
    else:
        for m in re.finditer(r'^\| R(\d+) — .*$', rules, re.M):
            r = int(m.group(1))
            st['rules'].append((r, 'withdrawn' in m.group(0).lower()))
            if r in defined_R:
                issue(nn, norm, off + m.start(), f'R{r} is already defined in Stage {defined_R[r]}')
            defined_R[r] = n
        for m in re.finditer(r'\b(should|may)\b', rules, re.I):
            issue(nn, norm, off + m.start(), f'"{m.group(1)}" in the Rules section')

    ex, eoff = section(norm, r'^#{2,3} (?:\d+(?:\.\d+)* )?Rule examples\b.*$', r'^## ')
    have_ex = set()
    if ex is None:
        issue(nn, None, None, 'no Rule examples section')
    else:
        for m in re.finditer(r'^\| R(\d+) — .*$', ex, re.M):
            c = cells(m.group(0))
            if len(c) >= 3 and c[1] not in ('', '—') and c[2] not in ('', '—'):
                have_ex.add(int(m.group(1)))
            else:
                issue(nn, norm, eoff + m.start(), f'the R{m.group(1)} example row lacks a pass or a fail')
    for r, withdrawn in st['rules']:
        if not withdrawn and r not in have_ex:
            issue(nn, None, None, f'R{r} has no example row with a pass and a fail')

    steps, soff = section(norm, r'^## \d+\. Steps\b.*$', r'^## ')
    st['steps'] = set()
    if steps is None:
        if n > 0:
            issue(nn, None, None, 'no Steps table')
    else:
        for m in re.finditer(r'^\| S(\d+)\.(\d+)\b.*$', steps, re.M):
            sid = f'{int(m.group(1))}.{int(m.group(2))}'
            if int(m.group(1)) != n:
                issue(nn, norm, soff + m.start(), f'step S{sid} carries another stage number')
            if sid in st['steps']:
                issue(nn, norm, soff + m.start(), f'S{sid} is defined twice')
            st['steps'].add(sid)
            vals = (cells(m.group(0))[1:4] + ['', '', ''])[:3]
            missing = [k for k, v in zip(('Input', 'Action items', 'Output'), vals) if v in ('', '—')]
            if missing:
                issue(nn, norm, soff + m.start(), f'S{sid} has no {" / ".join(missing)}')

    st['limits'] = {}
    for m in re.finditer(r'^### (\d+\.\d+) Accepted limits\b.*$', norm, re.M):
        body = norm[m.end():]
        e = re.search(r'^(?:#{2,3} |---\s*$)', body, re.M)
        letters = re.findall(r'^\| ([a-z]) \|', body[:e.start()] if e else body, re.M)
        for x in dupes(letters):
            issue(nn, norm, m.start(), f'limit ({x}) is listed twice')
        st['limits'][m.group(1)] = set(letters)

    for key, pat, fmt in (('D', r'^\| D-(\d+) \|', 'D-{:02d}'), ('W', r'^\| W(\d+) \|', 'W{}'),
                          ('M', r'^\| M(\d+) \|', 'M{}')):
        ids = [int(x) for x in re.findall(pat, sup, re.M)]
        for x in dupes(ids):
            issue(sn, None, None, f'{fmt.format(x)} is defined twice')
        st[key] = set(ids)
    st['cited_W'] = set()

order = sorted(defined_R)
if order:
    gaps = sorted(set(range(1, order[-1] + 1)) - set(order))
    if gaps:
        issue('rules', None, None, f'R-numbers missing from the sequence: {ranges(gaps)}')
    for n in sorted(ST):
        mine = [r for r, s in defined_R.items() if s == n]
        later = [r for r, s in defined_R.items() if s > n]
        if mine and later and max(mine) > min(later):
            issue(ST[n]['norm_name'], None, None, 'R-numbers overlap a later stage')

# ---- references ----------------------------------------------------------------
QUAL = r'`?Stage\d+_\w+\.md`?|Stage \d+ Supplement|Stage \d+|Supplement|reference\.md|Policy Definition'
REF = (r'§R?\d+(?:\.\d+)*(?: \([a-z]\))?'
       r'|R\d+(?:–R?\d+)?'
       r'|D-\d+(?: ?[…–] ?D-\d+)?'
       r'|\[W\d+(?:–W?\d+)?(?: · W\d+(?:–W?\d+)?)*\]'
       r'|M\d+'
       r'|S\d+\.\d+(?:–(?:S?\d+\.)?\d+)?')
TOKEN = re.compile(rf'(?:(?P<q>{QUAL}) )?(?P<r>{REF})(?!\w)')
_T = rf'(?:(?:{QUAL}) )?(?:{REF})(?!\w)'
CHAIN = re.compile(rf'(?<![\w§-]){_T}(?:(?: ?· ?|, | and | or ){_T})*')


def stage_of(q):
    if not q:
        return None
    m = re.match(r'`?Stage ?(\d+)', q)
    return int(m.group(1)) if m else (0 if q == 'Policy Definition' else None)


def known(n, where, text, pos, what):
    if n in ST:
        return True
    issue(where, text, pos, f'{what}: no Stage {n} docs in gymspec/')
    return False


def check_section(where, text, pos, kind, own, q, qs, r):
    m = re.fullmatch(r'§(R?\d+(?:\.\d+)*)(?: \(([a-z])\))?', r)
    sec, letter = m.group(1), m.group(2)
    if sec.startswith('R') or q == 'reference.md':
        if sec not in REF_HEADS:
            issue(where, text, pos, f'§{sec} is not a "## R#" heading in reference.md')
        return
    if q is None:
        targets = [(own, 'norm')] if kind == 'norm' else [(own, 'norm'), (own, 'sup')]
    elif q == 'Supplement' or q.endswith('Supplement') or 'SupplementInfo' in q:
        targets = [(own if qs is None else qs, 'sup')]
    elif re.fullmatch(r'Stage \d+', q):
        targets = [(qs, 'norm'), (qs, 'sup')]
    else:
        targets = [(qs, 'norm')]
    for n, part in targets:
        if not known(n, where, text, pos, f'§{sec}'):
            return
        if sec in ST[n]['heads_' + part]:
            lim = ST[n]['limits'].get(sec) if part == 'norm' else None
            if letter and lim is not None and letter not in lim:
                issue(where, text, pos, f'§{sec} ({letter}): Stage {n} §{sec} has no limit ({letter})')
            return
    names = ' or '.join(ST[n][part + '_name'] for n, part in targets)
    issue(where, text, pos, f'§{sec} is not a heading in {names}')


DOCS = [('CLAUDE.md', P, 0, 'prompt')]
for n, st in sorted(ST.items()):
    DOCS += [(st['norm_name'], st['norm'], n, 'norm'), (st['sup_name'], st['sup'], n, 'sup')]
cited_R = {}
for where, text, own, kind in DOCS:
    for cm in CHAIN.finditer(text):
        carry = None
        for tm in TOKEN.finditer(cm.group(0)):
            q, r = tm.group('q'), tm.group('r')
            pos = cm.start() + tm.start('r')
            qs = stage_of(q)
            if r.startswith('§'):
                check_section(where, text, pos, kind, own, q, qs, r)
            elif r.startswith('R'):
                for x in expand(r, 'R'):
                    cited_R.setdefault(x, (where, text, pos))
            elif r.startswith('D-'):
                n = qs if qs is not None else (carry if carry is not None else own)
                if known(n, where, text, pos, r):
                    miss = [x for x in expand(r, 'D-') if x not in ST[n]['D']]
                    if miss:
                        alt = [k for k in sorted(ST) if k != n and set(miss) <= ST[k]['D']]
                        hint = f' (Stage {alt[0]} has it: prefix "Stage {alt[0]}"?)' if alt else ''
                        issue(where, text, pos, f'{ranges(miss, dfmt)} not in the Stage {n} decision log{hint}')
            elif r.startswith('['):
                n = qs if qs is not None else own
                if known(n, where, text, pos, r):
                    ws = [x for item in r[1:-1].split(' · ') for x in expand(item, 'W')]
                    ST[n]['cited_W'] |= set(ws)
                    miss = [x for x in ws if x not in ST[n]['W']]
                    if miss:
                        issue(where, text, pos, f'W{ranges(miss)} not in the Stage {n} references')
            elif r.startswith('M'):
                n = qs if qs is not None else own
                if known(n, where, text, pos, r) and int(r[1:]) not in ST[n]['M']:
                    issue(where, text, pos, f'{r} is not in the Stage {n} measurements')
            elif r.startswith('S'):
                sm = re.fullmatch(r'S(\d+)\.(\d+)(?:–(?:S?(\d+)\.)?(\d+))?', r)
                n, a = int(sm.group(1)), int(sm.group(2))
                b = int(sm.group(4)) if sm.group(4) else a
                if known(n, where, text, pos, r):
                    for x in (range(a, b + 1) if 0 <= b - a <= 50 else (a, b)):
                        if f'{n}.{x}' not in ST[n]['steps']:
                            issue(where, text, pos, f'S{n}.{x} is not a step in {ST[n]["norm_name"]}')
            if qs is not None:
                carry = qs
for x, (where, text, pos) in sorted(cited_R.items()):
    if x not in defined_R:
        issue(where, text, pos, f'R{x} is cited but not defined')

# ---- open items ------------------------------------------------------------------
notes = {}
blk = re.search(r'<stages>(.*?)</stages>', P, re.S)
for m in re.finditer(r'^- Stage (\d+) .*$', blk.group(1) if blk else '', re.M):
    om = re.search(r'Open items: ([^;\n]*)', m.group(0))
    notes[int(m.group(1))] = om.group(1).strip() if om else None
open_summary = []
for n, st in sorted(ST.items()):
    norm, sup, nn = st['norm'], st['sup'], st['norm_name']
    body, boff = section(norm, r'^## \d+\. Open items\s*$', r'^## ')
    if body is None:
        issue(nn, None, None, 'no Open items section')
        continue
    is_none = body.strip().startswith('None')
    defined_O = set(int(x) for x in re.findall(r'^\| O(\d+) \|', body, re.M))
    if is_none and defined_O:
        issue(nn, norm, boff, 'Open items reads "None" but lists O-rows')
    if not is_none and not defined_O:
        issue(nn, norm, boff, 'Open items is neither "None" nor a table of O-rows')
    cited_O = set() if is_none else set(int(x) for x in re.findall(r'\bO(\d+)\b', body))
    cur = re.search(r'Round (\d+), opened', norm)
    if cur:
        for m in re.finditer(r'((?:\bO\d+(?:–O\d+)?(?: · )?)+),? round ' + cur.group(1) + r'\b', sup):
            for a, b in re.findall(r'O(\d+)(?:–O(\d+))?', m.group(1)):
                cited_O |= set(range(int(a), int(b or a) + 1))
    note = notes.get(n)
    if note is not None:
        note_none = note.lower().startswith('none')
        if not note_none:
            cited_O |= set(int(x) for x in re.findall(r'\bO(\d+)\b', note))
        if note_none != is_none:
            issue('CLAUDE.md', None, None, f'<stages> gives Stage {n} "Open items: {note[:30]}", '
                  f'but {nn} {"reads None" if is_none else "lists open items"}')
    for x in sorted(cited_O - defined_O):
        issue(nn, None, None, f'O{x} is cited but is not an open item')
    open_summary.append(f'Stage {n} ' + ('none' if is_none else 'O' + ranges(defined_O))
                        + (f', round {cur.group(1)} open' if cur else ''))
old_oi = sum(len(re.findall(r'\bOI-\d', t)) for _, t, _, _ in DOCS)
if old_oi:
    issue('docs', None, None, f'{old_oi} open-item reference(s) still in the old OI- form')

# ---- report ------------------------------------------------------------------------
print('Docs: CLAUDE.md · ' + ' · '.join(f'{st["norm_name"]} + {st["sup_name"]}' for _, st in sorted(ST.items()))
      + (' · reference.md (## R headings)' if REF_HEADS else ''))
for n, st in sorted(ST.items()):
    rs = [r for r, _ in st['rules']]
    lim = '; '.join(f'§{k} ({"".join(sorted(v))})' for k, v in st['limits'].items()) or 'none'
    print(f'Stage {n}: rules R{min(rs) if rs else "-"}–R{max(rs) if rs else "-"} ({len(rs)}) · '
          f'steps {len(st["steps"])} · log {ranges(st["D"], dfmt)} · W {len(st["W"])} · M {len(st["M"])} · '
          f'accepted limits {lim}')
    print(f'Stage {n}: [W] defined but never cited: {ranges(st["W"] - st["cited_W"])}')
print('Open items: ' + '; '.join(open_summary))
print(f'ISSUES ({len(issues)}):')
for i in issues:
    print('  ' + i)
print('RESULT: clean' if not issues else f'RESULT: {len(issues)} issue(s)')
sys.exit(1 if issues else 0)
