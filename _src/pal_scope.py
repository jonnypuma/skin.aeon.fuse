# -*- coding: utf-8 -*-
"""0.40.4: a palette for the menus only, for the library views only, or for both (default).

Kodi has one colour theme at a time, so the library windows (MyVideoNav, MyMusicNav, MyPics) get colour names of their
own: every palette colour they draw (directly or through includes / variables) is renamed lib_<name>. Includes and
variables the library shares with other windows get a library copy, <name>_L; the copies and the library-only ones use
lib_ names, the others keep theirs, so menus are untouched.

Colour files:
  - defaults.xml and every palette file also define lib_<name> = their own <name> (so "both" looks as before);
  - "<palette> (menus).xml": the palette without lib_ names (library views keep the Aeon colours of defaults.xml);
  - "<palette> (library).xml": only the lib_ names (menus keep the Aeon colours).
The helper's palette picker asks which one (script.aeon.helper palette.py), Skin.String(aeon.palette) holds the file.

Run once from the skin folder; it refuses to run twice."""
import glob
import io
import os
import re
import sys
import xml.etree.ElementTree as ET

NAMES = ['aeon_accent', 'aeon_box', 'aeon_onaccent', 'aeon_onbar', 'aeon_onbar_99', 'aeon_onbar_aa', 'aeon_onbar_bb', 'aeon_onbar_cc',
         'aeon_sbbar', 'aeon_white', 'x_accent', 'x_accenttext', 'x_column', 'x_deep', 'x_deep_8c', 'x_deep_cc', 'x_deep_e6',
         'x_deep_f0', 'x_ground', 'x_line', 'x_line2', 'x_onaccent', 'x_panel', 'x_raised', 'x_surface']
PAL = re.compile(r'(?<![\w.\[/-])(' + '|'.join(sorted(NAMES, key=len, reverse=True)) + r')(?![\w.])')
LIBWIN = ('MyVideoNav.xml', 'MyMusicNav.xml', 'MyPics.xml')
SUFFIX = '_L'
TAG = re.compile(r'<!--.*?-->|<(/?)([A-Za-z_][\w.-]*)((?:\s+[\w:.-]+\s*=\s*"[^"]*")*)\s*(/?)>', re.S)
NAME_ATTR = re.compile(r'\bname="([^"]+)"')

files = {os.path.basename(f): io.open(f, encoding='utf-8').read() for f in glob.glob('1080i/*.xml')}
if any('lib_aeon_white' in t for t in files.values()):
    sys.exit('already applied')


def top_defs(fname, text):
    """depth-1 <include name> / <variable name> elements of an Includes file: [(kind, name, start, end)]"""
    out, depth, start, cur = [], 0, None, None
    for m in TAG.finditer(text):
        if m.group(0).startswith('<!--'):
            continue
        closing, tag, attrs, selfclose = m.group(1), m.group(2), m.group(3) or '', m.group(4)
        if closing:
            depth -= 1
            if depth == 1 and cur:
                out.append((cur[0], cur[1], start, m.end()))
                cur = None
            continue
        if depth == 1 and tag in ('include', 'variable'):
            nm = NAME_ATTR.search(attrs)
            if nm:
                if selfclose:
                    out.append((tag[0], nm.group(1), m.start(), m.end()))
                else:
                    cur, start = (tag[0], nm.group(1)), m.start()
        if not selfclose:
            depth += 1
    return out


def root_tag(text):
    for m in TAG.finditer(text):
        if not m.group(0).startswith('<!--'):
            return m.group(2)


defs = {}          # (kind, name) -> (file, start, end)
for fn, t in files.items():
    if root_tag(t) == 'includes':
        for kind, name, a, b in top_defs(fn, t):
            assert (kind, name) not in defs, ('twice', kind, name)
            defs[(kind, name)] = (fn, a, b)


def body(k):
    fn, a, b = defs[k]
    return files[fn][a:b]


INC_REF = re.compile(r'(<include(?:\s+condition="[^"]*")?\s*>)([A-Za-z0-9_]+)(</include>)|(<include\s+content=")([A-Za-z0-9_]+)(")')
VAR_REF = re.compile(r'(\$(?:ESC)?VAR\[)([A-Za-z0-9_]+)(\])')
PARAM_REF = re.compile(r'(<param\s+name="[^"]+"\s+value=")([A-Za-z0-9_]+)("\s*/?>)')


def refs(text):
    out = set()
    for m in INC_REF.finditer(text):
        out.add(('i', m.group(2) or m.group(5)))
    for m in VAR_REF.finditer(text):
        out.add(('v', m.group(2)))
    for m in PARAM_REF.finditer(text):      # include / variable names handed on as a parameter ($PARAM[extra])
        for kind in ('i', 'v'):
            if (kind, m.group(2)) in defs:
                out.add((kind, m.group(2)))
    return {k for k in out if k in defs}


def window_text(fn):
    return files[fn]


closure = {}
for fn, t in files.items():
    if root_tag(t) != 'window':
        continue
    seen, todo = set(), list(refs(t))
    while todo:
        k = todo.pop()
        if k in seen:
            continue
        seen.add(k)
        todo.extend(refs(body(k)))
    closure[fn] = seen
used_by = {}
for fn, s in closure.items():
    for k in s:
        used_by.setdefault(k, set()).add(fn)

tainted = set()
changed = True
while changed:
    changed = False
    for k in defs:
        if k not in tainted and (PAL.search(body(k)) or refs(body(k)) & tainted):
            tainted.add(k)
            changed = True
lib = set()
for fn in LIBWIN:
    lib |= closure[fn]
lib_t = lib & tainted
shared = {k for k in lib_t if used_by[k] - set(LIBWIN)}
only = lib_t - shared
print('library: %d tainted (%d library-only rewritten in place, %d shared copied as %s)' % (len(lib_t), len(only), len(shared), SUFFIX))
for k in shared:
    assert (k[0], k[1] + SUFFIX) not in defs, k


def rename(name, kind):
    return name + SUFFIX if (kind, name) in shared else name


def rewrite(text):
    text = PAL.sub(lambda m: 'lib_' + m.group(1), text)

    def inc(m):
        if m.group(2):
            return m.group(1) + rename(m.group(2), 'i') + m.group(3)
        return m.group(4) + rename(m.group(5), 'i') + m.group(6)
    text = INC_REF.sub(inc, text)
    text = VAR_REF.sub(lambda m: m.group(1) + rename(m.group(2), 'v') + m.group(3), text)

    def par(m):
        n = m.group(2)
        for kind in ('i', 'v'):
            if (kind, n) in shared:
                return m.group(1) + n + SUFFIX + m.group(3)
        return m.group(0)
    return PARAM_REF.sub(par, text)


# edits per file, applied from the end so offsets stay valid
edits = {}
for k in only:
    fn, a, b = defs[k]
    edits.setdefault(fn, []).append((a, b, rewrite(files[fn][a:b])))
for k in shared:
    fn, a, b = defs[k]
    orig = files[fn][a:b]
    twin = rewrite(orig)
    twin = re.sub(r'(<%s\s+name=")%s(")' % ('include' if k[0] == 'i' else 'variable', re.escape(k[1])), r'\g<1>%s%s\2' % (k[1], SUFFIX), twin, count=1)
    note = '<!-- %s%s: the library windows\' copy of %s (lib_ colours: palette for menus / library / both, 0.40.4) -->\n\t' % (k[1], SUFFIX, k[1])
    edits.setdefault(fn, []).append((a, b, orig + '\n\t' + note + twin))
for fn in LIBWIN:
    t = files[fn]
    edits.setdefault(fn, []).append((0, len(t), rewrite(t)))
for fn, lst in edits.items():
    t = files[fn]
    lst.sort(key=lambda e: e[0], reverse=True)
    if any(e[0] == 0 and e[1] == len(t) for e in lst):
        assert len(lst) == 1, fn
    last = None
    for a, b, new in lst:
        assert last is None or b <= last, ('overlap', fn)
        t = t[:a] + new + t[b:]
        last = a
    io.open(os.path.join('1080i', fn), 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(os.path.join('1080i', fn))
print('files changed:', ', '.join(sorted(edits)))

# colour files
COLOR = re.compile(r'(\s*)<color name="([^"]+)">([0-9A-Fa-f]{8})</color>')
for path in sorted(glob.glob('colors/*.xml')):
    base = os.path.basename(path)
    t = io.open(path, encoding='utf-8').read()
    found = [(m.group(2), m.group(3)) for m in COLOR.finditer(t) if m.group(2) in NAMES]
    if not found:
        continue
    lines = ''.join('\n    <color name="lib_%s">%s</color>' % (n, v) for n, v in found)
    block = ('\n    <!-- 0.40.4: the library windows\' names (lib_<name>), the same colours; "<palette> (menus).xml" leaves them out,'
             '\n         "<palette> (library).xml" has only these -->' + lines + '\n')
    full = t.replace('</colors>', block + '</colors>', 1)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(full)
    if base in ('defaults.xml', 'Fused Glass.xml'):
        continue
    stem = base[:-4]
    menus = t.replace('<colors>', '<colors>\n    <!-- 0.40.4: palette "%s" for the menus only: library views keep the Aeon colours (lib_ names of defaults.xml) -->' % stem, 1)
    io.open('colors/%s (menus).xml' % stem, 'w', encoding='utf-8', newline='\n').write(menus)
    libonly = ('<?xml version="1.0" encoding="UTF-8"?>\n<!-- 0.40.4: palette "%s" for the library views only: the menus keep the Aeon colours -->\n<colors>%s\n</colors>\n'
               % (stem, lines))
    io.open('colors/%s (library).xml' % stem, 'w', encoding='utf-8', newline='\n').write(libonly)
for path in glob.glob('colors/*.xml'):
    ET.parse(path)
print('colour files:', len(glob.glob('colors/*.xml')))
