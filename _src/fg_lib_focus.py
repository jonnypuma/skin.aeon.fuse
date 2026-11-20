# -*- coding: utf-8 -*-
"""0.56.2 The Fused Glass library views follow Skin settings > Appearance > Focus highlight (Skin.String(aeon.fgfocus):
Pill = default, Flat, Frosted, Outline, Tight), like the menus (the user: "it's pointless just having them for menus and
not library views. please allow them to be used with library views too").

Works on the FG_LIB block (written by _src/fg_lib.py) and the FG_EPCOMB block (_src/fg_epcomb.py) of
1080i/Includes_Fused.xml; both generators call apply() before they save. Run this file on its own to patch them as
they are.
  - Pill, Frosted, Outline, Tight: the row's white focus bar (fg/rNN.png, ffffffff, while the list has the focus)
    draws the style's picture (the menus' fx_*.png, border 16), one image per style switched by visibility (Kodi keeps
    a $VAR picture in a list layout as it was when the rows were made, but it updates visibility).
  - Flat: a square white bar as wide as the card and over the gaps between rows. A list clips its rows to its own
    rectangle (12 px inside the card), so this bar is drawn outside the list, under it: one image per row slot, shown
    while the focused row is in that slot (Container(id).Position). The first slot's bar runs up to the card's top,
    and the last slot's down to the card's bottom when that row ends there, with the card's round corners
    (fg/rtop28.png, fg/rbot28.png); the user: "would look nicer if it was solid white until the top of the card,
    vice versa on the bottom".
  - The rows' focus ink (dark on the white bar: FG_L*/FG_M* Ink, Ink2, ChipEdge, FG_Ec*) stays light with the light
    styles (Frosted, Outline), whose bar is see-through.
Not touched: the season tabs of Episode combined (5381, pills) and the Search window. Safe to run again."""
import io
import os
import re

FUSED = os.path.join('1080i', 'Includes_Fused.xml')
LISTS = (510, 511, 512, 5121, 513, 517, 5171, 518, 524, 527, 532, 533, 538)
S = 'String.IsEqual(Skin.String(aeon.fgfocus),%s)'
FLAT = S % 'flat'
STYLES = (('pill', '!%s + !%s + !%s' % (S % 'frost', S % 'outline', S % 'tight')),
          ('frost', S % 'frost'), ('outline', S % 'outline'), ('tight', S % 'tight'))
BAR = re.compile(r'<control type="image"><left>(-?\d+)</left><top>(-?\d+)</top><width>(\d+)</width><height>(\d+)</height>'
                 r'<texture border="\d+" colordiffuse="ffffffff">fg/r\d+\.png</texture><visible>(Control\.HasFocus\((\d+)\)[^<]*)</visible></control>')
BLOCKS = (('\t<!-- FG_LIB:begin', '<!-- FG_LIB:end -->'), ('\t<!-- FG_EPCOMB:begin', '<!-- FG_EPCOMB:end -->'))
MARK = '<!-- flat focus bar (_src/fg_lib_focus.py) -->'
FLAT_SLOTS = False   # 0.56.3: Flat is gone from Fused Glass (_src/fg_noflat.py)


def edge_textures():
    """white pictures with only the top / only the bottom corners round like the card (r28)"""
    from PIL import Image, ImageDraw
    for name, top in (('rtop28.png', True), ('rbot28.png', False)):
        p = os.path.join('media', 'fg', name)
        if os.path.exists(p):
            continue
        n, r, ss = 64, 28, 4
        a = Image.new('L', (n * ss, n * ss), 0)
        d = ImageDraw.Draw(a)
        d.rounded_rectangle([0, 0, n * ss - 1, n * ss - 1], radius=r * ss, fill=255)
        d.rectangle([0, n * ss // 2, n * ss - 1, n * ss - 1] if top else [0, 0, n * ss - 1, n * ss // 2], fill=255)
        im = Image.new('RGBA', (n, n), (255, 255, 255, 0))
        im.putalpha(a.resize((n, n), Image.LANCZOS))
        im.save(p, optimize=True)


def style_bar(x, y, w, h, cond):
    """the focus bar of a list row in Pill / Frosted / Outline / Tight (Flat is drawn outside the list, flat_slots());
    also used by _src/fg_epcomb.py"""
    return ''.join('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
                   '<texture border="16" colordiffuse="ffffffff">fg/fx_%s.png</texture><visible>%s + %s</visible></control>'
                   % (x, y, w, h, st, cond, sc) for st, sc in STYLES)


def bars(blk):
    out, pos, n = [], 0, 0
    for m in BAR.finditer(blk):
        if int(m.group(6)) not in LISTS:
            continue
        x, y, w, h = map(int, m.group(1, 2, 3, 4))
        out.append(blk[pos:m.start()] + style_bar(x, y, w, h, m.group(5)))
        pos = m.end()
        n += 1
    out.append(blk[pos:])
    return ''.join(out), n


def flat_slots(blk, lid):
    """the flat bars of one list, drawn just before the list control (same parent, under the rows)"""
    m = re.search(r'<control type="(?:fixedlist|list)" id="%d">' % lid, blk)
    if not m:
        return blk, False
    head = blk[m.end():m.end() + 1500]
    head = head[:head.find('<itemlayout')]
    L, T, W, H = (int(re.search(r'<%s>(-?\d+)</%s>' % (k, k), head).group(1)) for k in ('left', 'top', 'width', 'height'))
    fl = blk.find('<focusedlayout', m.end())
    pitch = int(re.search(r'<focusedlayout[^>]*height="(\d+)"', blk[fl:fl + 120]).group(1))
    bar = re.search(r'<control type="image"><left>(-?\d+)</left><top>(-?\d+)</top><width>\d+</width><height>(\d+)</height>'
                    r'<texture border="16" colordiffuse="ffffffff">fg/fx_pill\.png</texture><visible>Control\.HasFocus\(%d\)' % lid, blk[fl:])
    by, bh = int(bar.group(2)), int(bar.group(3))
    gap = max(0, pitch - (by + bh))
    # the card: the smallest r28 picture round the list in the same view (any colour: fg_material.py sets it later)
    inc = blk.rfind('<include name="', 0, m.start())
    view = blk[inc:blk.find('\n\t</include>', inc)]
    cards = [tuple(map(int, c.groups())) for c in re.finditer(
        r'<left>(-?\d+)</left><top>(-?\d+)</top><width>(\d+)</width><height>(\d+)</height><texture border="\d+" colordiffuse="[^"]*">fg/r28\.png', view)]
    cards = [c for c in cards if c[0] <= L and c[0] + c[2] >= L + W and c[1] <= T and c[1] + c[3] >= T + H]
    cx, cy, cw, ch = min(cards, key=lambda c: c[2] * c[3])
    n = H // pitch
    top_edge = T - cy <= 16
    last_top = T + (n - 1) * pitch
    bottom_edge = cy + ch - (last_top + pitch) <= 24
    imgs = [MARK]
    for k in range(n):
        y0 = T + k * pitch + by - gap // 2
        y1 = T + k * pitch + by + bh + (gap - gap // 2)
        tex = 'common/white.png'
        if k == 0 and top_edge:
            y0, tex = cy, 'fg/rtop28.png'
        if k == n - 1 and bottom_edge:
            y1, tex = cy + ch, 'fg/rbot28.png' if tex == 'common/white.png' else tex
        imgs.append('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><texture%s colordiffuse="ffffffff">%s</texture>'
                    '<visible>Control.HasFocus(%d) + %s + Integer.IsEqual(Container(%d).Position,%d)</visible></control>'
                    % (cx, y0, cw, y1 - y0, ' border="28"' if tex != 'common/white.png' else '', tex, lid, FLAT, lid, k))
    blk = blk[:m.start()] + ''.join(imgs) + blk[m.start():]        # inline: the list may sit mid-line
    print('  %d: %d slots, first to the card top: %s, last to the card bottom: %s' % (lid, n, top_edge, bottom_edge))
    return blk, True


def inks(blk):
    """the dark focus ink only on a solid bar"""
    n = 0

    def fix(m):
        nonlocal n
        name, body = m.group(1), m.group(2)
        body2 = re.sub(r'<value condition="(Control\.HasFocus\(\d+\))">', lambda v: '<value condition="%s + !$EXP[FG_FocusLight]">' % v.group(1), body)
        if body2 != body:
            n += 1
        return '<variable name="%s">%s</variable>' % (name, body2)
    blk = re.sub(r'<variable name="(FG_[LM]\d*_(?:Ink|Ink2|ChipEdge)|FG_Ec(?:Ink|Ink2|Pill))">(.*?)</variable>', fix, blk, flags=re.S)
    return blk, n


def apply(f):
    edge_textures()
    for begin, end in BLOCKS:
        a = f.find(begin)
        if a < 0:
            continue
        b = f.find(end, a)
        blk = f[a:b]
        if 'fg/fx_frost.png' in blk:
            continue
        blk, nb = bars(blk)
        ns = 0
        for lid in (LISTS if FLAT_SLOTS else ()):
            blk, done = flat_slots(blk, lid)
            ns += done
        blk, ni = inks(blk)
        print('fg_lib_focus %s: %d bars in the chosen style, flat bars for %d lists, %d ink variables' % (begin.strip()[5:15], nb, ns, ni))
        f = f[:a] + blk + f[b:]
    return f


if __name__ == '__main__':
    f = io.open(FUSED, encoding='utf-8').read()
    g = apply(f)
    if g != f:
        io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(g)
