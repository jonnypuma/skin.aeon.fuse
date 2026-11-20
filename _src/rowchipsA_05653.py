# -*- coding: utf-8 -*-
"""0.56.53 list rows, option A (user, 2026-11-20: "B is clipping but I think we go for A anyway").
The chip runs (rowchips_05653.py) and the title + version tag (tagrows_05653.py / tagfix_05653.py) were grouplists, and
in a list row Kodi hands a grouplist's children the FOCUSED item: every row showed the focused film's chips / version.
Now nothing on a row flows:
- media chips: fixed slots ending at the same right edge as before, in the order resolution, HDR, audio, aspect,
  rating (the mockup's order); a chip with no value leaves its slot empty. Plain image + label pairs (they read the
  row's own item). The line-2 text stops 10 px before the first slot, the same width on every row of a layout.
- version: Kodi's version name (or, on the focused row, the sidecar edition when Kodi says Standard Edition) as an
  outline chip opening line 2 (VW px, centred); line 2 then starts after it. The inline dimmed version after the title
  and the focused-row tag grouplist are gone. Fused List 510 and the Aeon List row.
Run after rowchips_05653.py, tagrows_05653.py and tagfix_05653.py. Repeatable."""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import settings_sections as ss  # noqa: E402
import tagrows_05653 as tr  # noqa: E402

D = os.path.join(HERE, '..', '1080i')
CHIPS = '<!-- 0.56.53 row chips right -->'
SLOTS = '<!-- 0.56.53 row chips A -->'
VMARK = tr.MARK
VER = '<!-- 0.56.53 version chip A -->'
NEG = '<visible>![%s]</visible>' % tr.TAG
POS = '<visible>%s</visible>' % tr.TAG
LISTS = ('510', '527', '511', '5121', '5171', '5181', '524')
ORDER = ('res', 'hdr', 'audio', 'aspect', 'cert')
GAP = 6
VW = 190                 # version chip width
VG = 12                  # version chip to line-2 text


def kind(label):
    for k, key in (('res', 'ResChip'), ('hdr', 'HdrChip'), ('audio', 'EcAudio'), ('aspect', 'VideoAspect'), ('cert', 'Aeon_Cert')):
        if key in label:
            return k
    return None


def buttons(x):
    """[(kind, width, height, button xml)] of a chip grouplist"""
    out = []
    for b in re.finditer(r'<control type="button"><width>(\d+)</width><height>(\d+)</height><label>(.*?)</label>.*?</control>', x, re.S):
        out.append((kind(b.group(3)), int(b.group(1)), int(b.group(2)), b.group(0)))
    return out


def pair(b, left, top):
    """a chip button as a fixed image + label at left"""
    w, h = re.search(r'<width>(\d+)</width><height>(\d+)</height>', b).groups()
    lab = re.search(r'<label>(.*?)</label>', b, re.S).group(1)
    font = re.search(r'<font>([^<]*)</font>', b).group(1)
    col = re.search(r'<textcolor>([^<]*)</textcolor>', b).group(1)
    tex = re.search(r'<texturenofocus([^>]*)>([^<]*)</texturenofocus>', b)
    vis = ''.join(re.findall(r'<visible>.*?</visible>', b, re.S))
    return ('<control type="image"><left>%d</left><top>%s</top><width>%s</width><height>%s</height><texture%s>%s</texture>%s</control>'
            '<control type="label"><left>%d</left><top>%s</top><width>%s</width><height>%s</height><align>center</align>'
            '<aligny>center</aligny><font>%s</font><textcolor>%s</textcolor><selectedcolor>%s</selectedcolor><label>%s</label>%s</control>'
            % (left, top, w, h, tex.group(1), tex.group(2), vis, left, top, w, h, font, col, col, lab, vis))


def slots_of(x):
    """per edge: {kind: width} union and the slot lefts"""
    edges = {}
    for g in re.finditer(re.escape(CHIPS) + r'<control type="grouplist"><left>(\d+)</left><top>(\d+)</top><width>(\d+)</width>', x):
        m = ss.masked(x)
        a = g.start() + len(CHIPS)
        e = ss.ctl_end(m, a)
        edge = int(g.group(1)) + int(g.group(3))
        u = edges.setdefault(edge, {})
        for k, w, h, _ in buttons(x[a:e]):
            u[k] = max(u.get(k, 0), w)
    lay = {}
    for edge, u in edges.items():
        ks = [k for k in ORDER if k in u]
        total = sum(u[k] for k in ks) + GAP * (len(ks) - 1)
        pos, left = {}, edge - total
        for k in ks:
            pos[k] = left
            left += u[k] + GAP
        lay[edge] = (edge - total, pos, len(ks))
    return lay


def fix_layout(x):
    lay = slots_of(x)
    if not lay:
        return x, None
    n = 0
    while True:
        i = x.find(CHIPS + '<control type="grouplist">')
        if i < 0:
            break
        m = ss.masked(x)
        a = i + len(CHIPS)
        e = ss.ctl_end(m, a)
        g = re.match(r'<control type="grouplist"><left>(\d+)</left><top>(\d+)</top><width>(\d+)</width><height>(\d+)</height>', x[a:])
        edge = int(g.group(1)) + int(g.group(3))
        top = g.group(2)
        body = x[a:e]
        head_end = body.index('<control type="button">')
        vis = ''.join(re.findall(r'<visible>.*?</visible>', body[:head_end], re.S))
        _, pos, _ = lay[edge]
        kids = ''.join(pair(b, pos[k], top) for k, w, h, b in buttons(body))
        new = '%s<control type="group">%s%s</control>' % (SLOTS, vis, kids)
        x = x[:i] + new + x[e:]
        n += 1
    # line 2 stops before the first slot, the same on every row (only where a layout has HDR variants)
    for edge, (start, pos, cnt) in lay.items():
        if 'hdr' not in pos:
            continue

        def sub(mm):
            left = int(mm.group(1))
            w = start - 10 - left
            return mm.group(0).replace('<width>%s</width>' % mm.group(2), '<width>%d</width>' % w, 1)
        x = re.sub(r'<control type="label"><left>(\d+)</left><top>46</top><width>(\d+)</width><height>30</height>'
                   r'(?:(?!</control>).)*?<label>\$VAR\[FG_L_RowSub\]</label>(?:(?!</control>).)*?HdrType(?:(?!</control>).)*?</control>',
                   sub, x, flags=re.S)
    return x, (n, lay)


def unwrap_tags(seg):
    """the focused-row title + tag grouplists: removed, the title label before each shown again"""
    n = 0
    while True:
        i = seg.find(VMARK)
        if i < 0:
            break
        m = ss.masked(seg)
        e = ss.ctl_end(m, i + len(VMARK))
        ls = seg.rfind('<control type="label">', 0, i)
        lab = seg[ls:i]
        if NEG in lab:
            lab = lab.replace(NEG, '', 1)
        else:
            # the Aeon labels carry it on its own line, indented
            lab = re.sub(r'\s*' + re.escape(NEG), '', lab, 1)
        seg = seg[:ls] + lab + seg[e:]
        n += 1
    return seg, n


def chip(left, top, colour, vis):
    return ('%s<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>26</height>'
            '<texture border="8" colordiffuse="%s">fg/e8.png</texture>%s%s</control>'
            '<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>26</height><align>center</align>'
            '<aligny>center</aligny><font>lb_cap_14</font><textcolor>%s</textcolor><selectedcolor>%s</selectedcolor>'
            '<label>[UPPERCASE]$VAR[Aeon_VerStat][/UPPERCASE]</label>%s%s</control>'
            % (VER, left, top, VW, colour, vis, POS, left + 8, top, VW - 16, colour, colour, vis, POS))


def version_line2(seg, pat, ink_of):
    """each matching line-2 label: hidden for rows with a version; a twin after the chip for those rows"""
    out, pos, n = [], 0, 0
    for mm in re.finditer(r'<control type="label">(?:(?!<control).)*?</control>', seg, re.S):
        x = mm.group(0)
        if not re.search(pat, x, re.S) or POS in x or NEG in x:
            continue
        g = re.search(r'<left>(\d+)</left>(\s*)<top>(\d+)</top>(\s*)<width>(\d+)</width>(\s*)<height>(\d+)</height>', x)
        left, top, w, h = int(g.group(1)), int(g.group(3)), int(g.group(5)), int(g.group(7))
        vis = ''.join('<visible>%s</visible>' % v for v in re.findall(r'<visible>(.*?)</visible>', x, re.S))
        old = x[:-len('</control>')] + NEG + '</control>'
        twin = x.replace(g.group(0), '<left>%d</left>%s<top>%d</top>%s<width>%d</width>%s<height>%d</height>'
                         % (left + VW + VG, g.group(2), top, g.group(4), w - VW - VG, g.group(6), h), 1)
        twin = twin[:-len('</control>')] + POS + '</control>'
        ctop = top + (h - 26) // 2
        out.append(seg[pos:mm.start()])
        out.append(old + chip(left, ctop, ink_of(x), vis) + twin)
        pos = mm.end()
        n += 1
    out.append(seg[pos:])
    return ''.join(out), n


def fused():
    p = os.path.join(D, 'Includes_Fused.xml')
    s = io.open(p, encoding='utf-8').read()
    rep = []
    for lid in LISTS:
        for h in re.finditer(r'<control type="(?:list|panel|fixedlist|wraplist)" id="%s"' % lid, s):
            k = h.start()
            while True:
                m = re.compile(r'<(itemlayout|focusedlayout)[^>]*>').search(s, k)
                nxt = re.compile(r'<control type="(?:list|panel|fixedlist|wraplist)" id=').search(s, k + 10)
                if not m or (nxt and nxt.start() < m.start()):
                    break
                e = s.index('</%s>' % m.group(1), m.end())
                x, r = fix_layout(s[m.end():e])
                if lid == '510':
                    x, nv = unwrap_tags(x)
                    x = x.replace('$VAR[Aeon_VerInline]', '')
                    ink = '$VAR[FG_L_Ink]' if m.group(1) == 'focusedlayout' else 'ffffffff'
                    x, nc = version_line2(x, r'<left>22</left><top>46</top>(?:(?!</control>).)*?<label>\$VAR\[FG_L_RowSub\]</label>'
                                             r'(?:(?!</control>).)*?<visible>\[String\.IsEqual\(ListItem\.DBType,movie\)', lambda y, c=ink: c)
                    rep.append('510 %s: tags unwrapped %d, version chips %d' % (m.group(1)[:4], nv, nc))
                if r:
                    rep.append('%s %s: %d chip runs -> slots %s' % (lid, m.group(1)[:4], r[0],
                               {ed: (v[0], v[1]) for ed, v in r[1].items()}))
                s = s[:m.end()] + x + s[e:]
                k = m.end() + len(x)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
    return rep


def aeon():
    p = os.path.join(D, 'Includes_Aeon_Video.xml')
    s = io.open(p, encoding='utf-8').read()
    a = s.index('<include name="Aeon_Row">')
    b = s.find('<include name=', a + 10)
    seg = s[a:b]
    seg, nv = unwrap_tags(seg)
    seg = seg.replace('$VAR[Aeon_VerInline]', '')

    def ink(x):
        return re.search(r'<textcolor>([^<]*)</textcolor>', x).group(1)
    seg, nc = version_line2(seg, r'<left>140</left>\s*<top>58</top>(?:(?!</control>).)*?<label>\$VAR\[Aeon_SubLine\]</label>'
                                 r'(?:(?!</control>).)*?!Container\.Content\(tvshows\)', ink)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s[:a] + seg + s[b:])
    return 'Aeon row: tags unwrapped %d, version chips %d' % (nv, nc)


def main():
    for f in ('Includes_Fused.xml', 'Includes_Aeon_Video.xml'):
        t = io.open(os.path.join(D, f), encoding='utf-8').read()
        if VER in t:
            print('row chips A: already there (%s)' % f)
            return
    for r in fused():
        print(' ', r)
    print(' ', aeon())


if __name__ == '__main__':
    main()
