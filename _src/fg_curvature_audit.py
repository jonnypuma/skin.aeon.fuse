"""Curvature audit (0.39.6): rounded textures and how the skin draws them. Run in 1080i:  python ../_src/fg_curvature_audit.py [-v]
For each texture used with a 9-slice border (anywhere: controls and include bodies) it measures every side's corner
arc from the shape's body (alpha >= 50 %: where a column's / row's coverage reaches the straight edge's plateau) and
reports:
  KINK      a border smaller than the corner arc on a sliced side: the corner meets the straight edge with a kink
  OVAL      a corner whose horizontal and vertical extents differ by more than 2 px (not a circular arc)
  SCALED    a control smaller than the border sum (Kodi rescales the corner), or, on an axis without border, drawn at
            another size than the texture (the rounded ends are stretched into ovals)
  NEARPILL  a rounded texture drawn a little taller than 2r (meant as a pill, ends not semicircles)
Soft shadows / glows (sh*, *shadow*, *glow*, fade*) are left out: they have no edge to kink.
Rule: [[feedback-curvature]] - border >= arc, pills r = h/2, nested shapes concentric."""
import glob
import io
import os
import re
import sys
import xml.etree.ElementTree as ET

from PIL import Image

MEDIA = os.path.join('..', 'media')
TEXTAGS = ('texture', 'texturefocus', 'texturenofocus', 'texturebg', 'midtexture', 'lefttexture', 'righttexture',
           'alttexturefocus', 'alttexturenofocus', 'overlaytexture', 'texturesliderbar', 'texturesliderbackground',
           'texturesliderbarfocus', 'textureleft', 'textureright', 'texturefocusleft', 'texturefocusright')
# checked by hand: the measure is thrown by a baked shadow (row / column profiles of the body are circular)
CHECKED = {'dialogs/panel_fx.png': 'r30, top-left profile identical by row and column (2026-11-13)'}
SOFT = re.compile(r'(^|/)(sh\d+|[^/]*shadow[^/]*|[^/]*glow[^/]*|fade[^/]*)\.png$')


def constants():
    return dict((m.group(1), int(m.group(2))) for m in
                re.finditer(r'<constant name="([^"]+)">(-?\d+)</constant>', io.open('Constants.xml', encoding='utf-8').read()))


def variables():
    out = {}
    for f in glob.glob('*.xml'):
        for m in re.finditer(r'<variable name="([^"]+)">(.*?)</variable>', io.open(f, encoding='utf-8').read(), re.S):
            out[m.group(1)] = [v.strip() for v in re.findall(r'<value[^>]*>([^<]*)</value>', m.group(2))]
    return out


CONST = constants()
VARS = variables()


def num(v):
    if v is None:
        return None
    v = v.strip()
    return int(v) if re.fullmatch(r'-?\d+', v) else CONST.get(v)


def border4(b):
    p = [int(x) for x in b.split(',')]
    return (p[0],) * 4 if len(p) == 1 else tuple(p) if len(p) == 4 else None


_cache = {}


def arcs(path):
    if path in _cache:
        return _cache[path]
    full = os.path.join(MEDIA, path)
    res = None
    if os.path.isfile(full):
        im = Image.open(full).convert('RGBA')
        w, h = im.size
        # the shape's body (alpha >= 50 %), so a soft drop shadow round it does not count as corner; a white shape with
        # a dark shadow baked under it (fxb_*): the white pixels only
        px = im.load()
        opaque = [[px[x, y][3] >= 128 for x in range(w)] for y in range(h)]
        light = [[opaque[y][x] and max(px[x, y][:3]) >= 128 for x in range(w)] for y in range(h)]
        n_op = sum(map(sum, opaque))
        mask = light if sum(map(sum, light)) >= 0.25 * max(1, n_op) else opaque
        img = Image.new('L', (w, h))
        img.putdata([255 if mask[y][x] else 0 for y in range(h) for x in range(w)])
        a = img.load()
        col = [sum(a[x, y] for y in range(h)) / 255.0 for x in range(w)]
        row = [sum(a[x, y] for x in range(w)) / 255.0 for y in range(h)]
        cm, rm = col[w // 2], row[h // 2]

        def extent(seq, plateau):
            for i in range(len(seq) // 2):
                if seq[i] >= plateau - 0.5:
                    return i
            return len(seq) // 2
        if cm > 0 and rm > 0:
            res = {'size': (w, h), 'l': extent(col, cm), 'r': extent(col[::-1], cm), 't': extent(row, rm), 'b': extent(row[::-1], rm)}
            # margins round the body (a shadow's room): the corner radius is the extent minus the margin
            first = lambda seq: next((i for i, v in enumerate(seq) if v > 0), 0)
            res['m'] = {'l': first(col), 'r': first(col[::-1]), 't': first(row), 'b': first(row[::-1])}
    _cache[path] = res
    return res


def resolve(path):
    m = re.search(r'\$VAR\[([^\]]+)\]', path)
    if m:
        return [v for v in VARS.get(m.group(1), []) if v.endswith('.png')]
    return [] if '$' in path else [path]


def main():
    issues, uses = {}, {}

    def add(kind, path, bd, msg):
        issues.setdefault((kind, path, bd), set()).add(msg)

    for f in sorted(glob.glob('*.xml')):
        try:
            root = ET.parse(f).getroot()
        except ET.ParseError:
            continue
        parent = {c: p for p in root.iter() for c in p}
        for tag in TEXTAGS:
            for el in root.iter(tag):
                b, text = el.get('border'), (el.text or '').strip()
                if not b or not text:
                    continue
                bd = border4(b)
                if not bd:
                    continue
                ctl = parent.get(el)
                w = h = None
                if ctl is not None and ctl.tag == 'control':
                    w, h = num(ctl.findtext('width')), num(ctl.findtext('height'))
                for path in resolve(text):
                    uses.setdefault((path, bd), set()).add(f)
                    g = arcs(path)
                    if not g or SOFT.search(path):
                        continue
                    bl, bt, br, bb = bd
                    tw, th = g['size']
                    sliced_h, sliced_v = (bl or br), (bt or bb)
                    bad = []
                    if sliced_h and (bl + 1 < g['l'] or br + 1 < g['r']):
                        bad.append('horizontal')
                    if sliced_v and (bt + 1 < g['t'] or bb + 1 < g['b']):
                        bad.append('vertical')
                    if bad:
                        add('KINK', path, bd, '%s  arcs l%d t%d r%d b%d (%s)' % (f, g['l'], g['t'], g['r'], g['b'], '/'.join(bad)))
                    if w and w > 0 and sliced_h and w < bl + br:
                        add('SCALED', path, bd, '%s  %s width %d < border %d+%d' % (f, ctl.get('type'), w, bl, br))
                    if h and h > 0 and sliced_v and h < bt + bb:
                        add('SCALED', path, bd, '%s  %s height %d < border %d+%d' % (f, ctl.get('type'), h, bt, bb))
                    if h and h > 0 and not sliced_v and (g['t'] or g['b']) and h != th:
                        add('SCALED', path, bd, '%s  %s height %d, texture %d, no vertical border: ends stretched' % (f, ctl.get('type'), h, th))
                    if w and w > 0 and not sliced_h and (g['l'] or g['r']) and w != tw:
                        add('SCALED', path, bd, '%s  %s width %d, texture %d, no horizontal border: ends stretched' % (f, ctl.get('type'), w, tw))
                    m = re.fullmatch(r'fg/r(\d+)\.png', path)
                    if m and h:
                        r = int(m.group(1))
                        if 2 * r < h <= 2 * r + 10:
                            add('NEARPILL', path, bd, '%s  height %d (2r = %d)' % (f, h, 2 * r))
    for (path, bd) in list(uses):
        g = arcs(path)
        if not g or SOFT.search(path) or path in CHECKED:
            continue
        if re.search(r'/(e\d+|[^/]*outline[^/]*|sepline)\.png$', path):
            continue                     # thin rings / lines: no filled corner to measure
        rad = dict((k, g[k] - g['m'][k]) for k in 'ltrb')
        pairs = [(rad[a], rad[b]) for a, b in (('l', 't'), ('r', 't'), ('l', 'b'), ('r', 'b')) if rad[a] > 0 and rad[b] > 0]
        if any(abs(x - y) > 2 for x, y in pairs):
            add('OVAL', path, bd, 'arcs l%d t%d r%d b%d size %s' % (g['l'], g['t'], g['r'], g['b'], g['size']))
    order = {'KINK': 0, 'OVAL': 1, 'SCALED': 2, 'NEARPILL': 3}
    for (kind, path, bd), where in sorted(issues.items(), key=lambda kv: (order[kv[0][0]], kv[0][1], kv[0][2])):
        print('%-8s %-30s border %-14s %d' % (kind, path, ','.join(map(str, bd)), len(where)))
        for w in sorted(where)[:4]:
            print('           ', w)
        if len(where) > 4:
            print('            ... %d more' % (len(where) - 4))
    print('\n%d bordered texture/border pairs, %d issue groups' % (len(uses), len(issues)))
    if '-v' in sys.argv:
        for (path, bd) in sorted(uses):
            g = arcs(path)
            print('  %-32s %-14s %s' % (path, ','.join(map(str, bd)), g and 'arcs l%d t%d r%d b%d %s' % (g['l'], g['t'], g['r'], g['b'], g['size'])))


main()
