# -*- coding: utf-8 -*-
"""0.56.5 Fused Glass: the blurred backdrop under every library card, in every view (Material Frost / Raised / Dark;
Clear shows the backdrop sharp).

The user (2026-11-16): "material is not consistently applied everywhere", "the episode combined looks like i expect
glass to look like for all views", "if a user applies another material then the panels shall use those instead, make
it consistent now".
Before: the helper's blurred copy of the backdrop (Window(Home).Property(aeon.blur)) was laid under the cards through
four hand-drawn masks in Aeon_V_Bg (List 510, Episode list 511, Season list combined 3 with episodes open 512, the A-Z
rail), so every other view showed the backdrop sharp through its frosted cards.
Now every card of the library views (FG_V<id>_View, Aeon_V538_View: a picture fg/r24 / r28 / r32 in $VAR[FG_Frost],
at least 200 x 120) gets its own blur layer right under it, in the same group: a full-screen copy of the blurred
backdrop through a mask of that card's shape (fg/bmp_<x>_<y>_<w>_<h>_<r>.png, 960 x 540, stretched to the screen).
So the blur shows, hides and slides with its card, and the cards of other states of the view (seasons / episodes,
sets / films) leave no blur behind. Visible with $EXP[FG_PanelBlur] (fanart backdrop, Material not Clear).
The old 510 / 511 / 512 layers go; the rail keeps its layer (fg/bmrail.png) in every view.
Run after _src/fg_lib*.py / fg_epcomb.py (they rewrite the views), from the skin folder; safe to run again."""
import io
import os
import re
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw

FUSED = os.path.join('1080i', 'Includes_Fused.xml')
VIEWS2 = os.path.join('1080i', 'Includes_Aeon_Views2.xml')
OUT = os.path.join('media', 'fg')
VIEW = re.compile(r'^(FG_V\d+_View|Aeon_V538_View)$')
PANEL = re.compile(r'<control type="image">(?:<left>(-?\d+)</left>)?(?:<top>(-?\d+)</top>)?<width>(\d+)</width>'
                   r'<height>(\d+)</height><texture border="\d+" colordiffuse="\$VAR\[FG_Frost\]">fg/r(\d+)\.png</texture>')
LAYER = re.compile(r'<control type="image"><left>-?\d+</left><top>-?\d+</top><width>1920</width><height>1080</height>'
                   r'<aspectratio>stretch</aspectratio><fadetime>300</fadetime><texture background="true" diffuse="fg/bmp_[^"]+"'
                   r'[^\n]*?</control>')
EXPR = '<expression name="FG_PanelBlur">$EXP[Aeon_GBgFan] + !String.IsEmpty(Window(Home).Property(aeon.blur))</expression>'


def wanted(w, h, r):
    return r >= 24 and w >= 200 and h >= 120


def num(el, tag):
    e = el.find(tag)
    if e is None or e.text is None:
        return 0
    return int(e.text)


def panels_of(inc):
    """the cards of one view include in document order: (abs x, abs y of the parent group, own left, top, w, h, r)"""
    found = []

    def walk(el, x, y):
        for ch in el:
            if ch.tag != 'control':
                continue
            t = ch.get('type')
            if t == 'image':
                tex = ch.find('texture')
                m = re.match(r'fg/r(\d+)\.png', (tex.text or '') if tex is not None else '')
                if m and tex.get('colordiffuse') == '$VAR[FG_Frost]':
                    w, h, r = num(ch, 'width'), num(ch, 'height'), int(m.group(1))
                    found.append((x, y, num(ch, 'left'), num(ch, 'top'), w, h, r))
            elif t == 'group':
                walk(ch, x + num(ch, 'left'), y + num(ch, 'top'))
            else:                       # lists, grouplists: their pictures are not cards at a fixed place
                walk_skip(ch)

    def walk_skip(el):
        for ch in el.iter('control'):
            if ch.get('type') == 'image':
                tex = ch.find('texture')
                if tex is not None and tex.get('colordiffuse') == '$VAR[FG_Frost]' and re.match(r'fg/r\d+\.png', tex.text or ''):
                    found.append(None)  # keeps the order with the text matches; never a card

    d = inc.find('definition')
    walk(d if d is not None else inc, 0, 0)
    return found


def mask(x, y, w, h, r):
    name = 'bmp_%d_%d_%d_%d_%d.png' % (x, y, w, h, r)
    p = os.path.join(OUT, name)
    if not os.path.exists(p):
        ss = 4                          # drawn at 2 x 4 = 8 x the 960 x 540 picture, then down
        im = Image.new('L', (960 * ss, 540 * ss), 0)
        k = ss / 2.0
        ImageDraw.Draw(im).rounded_rectangle([x * k, y * k, (x + w) * k - 1, (y + h) * k - 1], radius=r * k, fill=255)
        a = im.resize((960, 540), Image.LANCZOS)
        out = Image.new('RGBA', (960, 540), (255, 255, 255, 0))
        out.putalpha(a)
        out.save(p, optimize=True)
    return name


def fused():
    t = io.open(FUSED, encoding='utf-8').read()
    t = LAYER.sub('', t)                                    # a second run starts clean
    t = re.sub(r'<expression name="FG_PanelBlur">[^<]*</expression>', EXPR, t)
    root = ET.fromstring(t)
    spans = {}
    for m in re.finditer(r'<include name="([^"]+)">', t):
        if VIEW.match(m.group(1)):
            spans[m.group(1)] = m.start()
    edits = []                                              # (position, text) inserted from the end
    total = 0
    for inc in root.iter('include'):
        name = inc.get('name') or ''
        if name not in spans:
            continue
        tree = panels_of(inc)
        a = spans[name]
        b = t.find('\n\t</include>', a)
        texts = list(PANEL.finditer(t, a, b))
        assert len(texts) == len(tree), (name, len(texts), len(tree))
        n = 0
        for m, p in zip(texts, tree):
            if p is None:
                continue
            gx, gy, L, T, w, h, r = p
            assert (int(m.group(1) or 0), int(m.group(2) or 0), int(m.group(3)), int(m.group(4)), int(m.group(5))) == (L, T, w, h, r), (name, p)
            if not wanted(w, h, r):
                continue
            mk = mask(gx + L, gy + T, w, h, r)
            edits.append((m.start(), '<control type="image"><left>%d</left><top>%d</top><width>1920</width><height>1080</height>'
                                     '<aspectratio>stretch</aspectratio><fadetime>300</fadetime><texture background="true" '
                                     'diffuse="fg/%s" colordiffuse="$VAR[Aeon_VFanAlphaG]">$INFO[Window(Home).Property(aeon.blur)]'
                                     '</texture><visible>$EXP[FG_PanelBlur] + $EXP[FG_PanelBlurMat]</visible></control>'
                                     % (-gx, -gy, mk)))   # the Clear test in the line: fg_material.py leaves the line alone
            n += 1
        total += n
        print('%-16s %d card(s)' % (name, n))
    for pos, text in sorted(edits, reverse=True):
        t = t[:pos] + text + t[pos:]
    if 'name="FG_PanelBlur"' not in t:
        t = t.replace('</includes>', '\t<!-- 0.56.5: the blurred backdrop under every library card (_src/fg_panel_blur.py) -->\n\t%s\n</includes>' % EXPR)
    io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(t)
    print('blur layers', total)


def background():
    """Aeon_V_Bg: the old 510 / 511 / 512 mask layers go; the rail's layer in every Fused Glass view"""
    t = io.open(VIEWS2, encoding='utf-8').read()
    n0 = len(t)
    t = re.sub(r'\t*<control type="image">[^\n]*diffuse="fg/bm51[012]\.png"[^\n]*</control>\n', '', t)
    t = re.sub(r'(diffuse="fg/bmrail\.png"[^\n]*?<visible>)[^<]*(</visible>)',
               r'\1$EXP[Aeon_FGlass] + $EXP[Aeon_GBgFan] + $EXP[FG_PanelBlurMat]\2', t)
    io.open(VIEWS2, 'w', encoding='utf-8', newline='\n').write(t)
    print('Aeon_V_Bg: %s' % ('old card masks removed' if len(t) != n0 else 'already'))


MENU = os.path.join('1080i', 'Includes_Aeon_Menu.xml')
STRIP = ('<control type="image"><left>8</left><top>8</top><width>444</width><height>1064</height><texture border="32" '
         'colordiffuse="$VAR[FG_MenuPanel]">fg/r32.png</texture>')


GROUND = re.compile(r'<control type="image"><left>8</left><top>8</top><width>444</width><height>1064</height><texture border="32" '
                    r'colordiffuse="lib_x_deep">fg/r32\.png</texture>[^\n]*?</control>\n\t\t')


def strip():
    """0.56.6: the left settings strip (1160 / 1166, Aeon_StripFrame / _L at 0,0, sliding in with its window) has the
    clock / A-Z rail's tint (FG_MenuPanel = FG_Strip). It lies over the view's list, whose titles read through a
    see-through strip: so it has a frosted base in every material, the views' ground (lib_x_deep) and the blurred
    backdrop as the view shows it (Aeon_VFanAlphaG), under the tint; nothing of the view reads through, and the strip
    looks like the rail (frosted in Frost / Raised / Dark, the same tint in Clear)."""
    t = io.open(MENU, encoding='utf-8').read()
    t = re.sub(LAYER.pattern + r'\n\t\t', '', t)          # the layers and the line break each was put in with
    t = GROUND.sub('', t)
    mk = mask(8, 8, 444, 1064, 32)
    vis = '$EXP[Aeon_FGlass] + [Window.IsActive(1160) | Window.IsActive(1166)]'
    ground = ('<control type="image"><left>8</left><top>8</top><width>444</width><height>1064</height><texture border="32" '
              'colordiffuse="lib_x_deep">fg/r32.png</texture><visible>%s</visible></control>' % vis)
    layer = ('<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><aspectratio>stretch'
             '</aspectratio><fadetime>300</fadetime><texture background="true" diffuse="fg/%s" colordiffuse="$VAR[Aeon_VFanAlphaG]">'
             '$INFO[Window(Home).Property(aeon.blur)]</texture><visible>%s + $EXP[FG_PanelBlur]</visible></control>' % (mk, vis))
    n = t.count(STRIP)
    t = t.replace(STRIP, ground + '\n\t\t' + layer + '\n\t\t' + STRIP)
    io.open(MENU, 'w', encoding='utf-8', newline='\n').write(t)
    print('left strip: frosted base under it in %d frame(s)' % n)


if __name__ == '__main__':
    fused()
    background()
    strip()
    ET.parse(FUSED)
    ET.parse(VIEWS2)
    ET.parse(MENU)
