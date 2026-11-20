# -*- coding: utf-8 -*-
"""0.53.0: two Fused Glass options. Run from the skin folder, then python _src/fg_material.py, then python
_src/ok_only.py. Safe to run again (every change is checked before it is made).

1. Skin settings > Appearance > Menu theme in Fused Glass: Dark (Skin.String(aeon.fgmenu) empty, the look so far and
   the default) | Glass (aeon.fgmenu = glass, expression FG_GlassMenus). Glass draws the settings menus, dialogs and
   information pages in the material chosen under Look > Material instead of the dark fills:
   - the shared card Aeon_Glass / Aeon_Glass_L (was fg_frost2) -> $VAR[FG_MenuFill] (written by fg_material.py)
   - the baked dialog / context menu panel AG_PanelTex -> dialogs/panel_fgg*.png (fg_material.py)
   - the library options strip and the open settings rail (FG_Panel there) -> $VAR[FG_MenuPanel]
   - the keyboard's card -> $VAR[FG_KbFill]
   - the dim behind dialogs (AG_DimDialog) lighter, and the settings backdrop (Aeon_Backdrop) brighter with a lighter
     dim, so the glass has a picture to show
   Aeon and Glass keep aeon.menutheme as before; the row in Fused Glass no longer offers Glass | Fuse (Fuse never did
   anything in Fused Glass). No restart: everything switches with visibility and variables.
2. Skin settings > Backgrounds > Home bar (row 9764, Fused Glass): Off (default) | Bar | Keys | Shelf
   (Skin.String(aeon.homebar): '' / bar / keys / shelf), frosted glass behind the Home menu row from the mockup canvas
   https://claude.ai/artifact/Me64YpHgSLfR9w7xkLCRvH (skin.glass/mockups/fg-glass-menu). It follows Look > Material
   (FG_Frost, FG_Edge, FG_PanelSh_80). Bar / Keys size to the focused item's name with the growing-pill trick: three
   grouplists (shadow, fill, edge) laid out like the icons row, the name's width taken by a disabled button with the
   same text in transparent ink.
"""
import io
import os
import re
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFilter, ImageFont

D = '1080i'
A = '$ADDON[skin.aeon.fuse %d]'
FG = 'Skin.HasSetting(aeon.fglass)'
GM = 'String.IsEqual(Skin.String(aeon.fgmenu),glass)'


def rd(name):
    return io.open(os.path.join(D, name), encoding='utf-8').read()


def wr(name, text):
    io.open(os.path.join(D, name), 'w', encoding='utf-8', newline='\n').write(text)
    ET.parse(os.path.join(D, name))


# ------------------------------------------------------------------------------------------------ textures (media/fg)
SS = 4
H, R = 106, 53          # the Home row's box: 106 high, a full pill (r = h / 2)
SHM, SHT, SHB = 40, 26, 46   # shadow margins: sides, top, bottom (as the panels' fg/sh* use)


def capsule_mask(w, h, r, ss=SS):
    im = Image.new('L', (w * ss, h * ss), 0)
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w * ss - 1, h * ss - 1), r * ss, fill=255)
    return im.resize((w, h), Image.LANCZOS)


def ring_mask(w, h, r, ss=SS):
    im = Image.new('L', (w * ss, h * ss), 0)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w * ss - 1, h * ss - 1), r * ss, fill=237)
    d.rounded_rectangle((ss, ss, w * ss - 1 - ss, h * ss - 1 - ss), (r - 1) * ss, fill=20)
    d.rounded_rectangle((2 * ss, 2 * ss, w * ss - 1 - 2 * ss, h * ss - 1 - 2 * ss), (r - 2) * ss, fill=0)
    return im.resize((w, h), Image.LANCZOS)


def white(alpha):
    out = Image.new('RGBA', alpha.size, (255, 255, 255, 0))
    out.putalpha(alpha)
    return out


def black(alpha):
    out = Image.new('RGBA', alpha.size, (0, 0, 0, 0))
    out.putalpha(alpha)
    return out


def save(im, name):
    im.save(os.path.join('media', 'fg', name), optimize=True)


# capsule halves (fill and edge) and the edge's middle column
W2 = 4 * R
cap = capsule_mask(W2, H, R)
ring = ring_mask(W2, H, R)
save(white(cap.crop((0, 0, R, H))), 'hb_fl.png')
save(white(cap.crop((W2 - R, 0, W2, H))), 'hb_fr.png')
save(white(ring.crop((0, 0, R, H))), 'hb_el.png')
save(white(ring.crop((W2 - R, 0, W2, H))), 'hb_er.png')
save(white(ring.crop((W2 // 2 - 2, 0, W2 // 2 + 2, H))), 'hb_em.png')
# the capsule's shadow: a blurred capsule 10 px lower, sliced into left part / middle column / right part
SW, SH = W2 + 2 * SHM, H + SHT + SHB
sh = Image.new('L', (SW, SH), 0)
sh.paste(capsule_mask(W2, H, R), (SHM, SHT + 10))
sh = sh.filter(ImageFilter.GaussianBlur(14))
save(black(sh.crop((0, 0, R + SHM, SH))), 'hb_sl.png')
save(black(sh.crop((SW - R - SHM, 0, SW, SH))), 'hb_sr.png')
save(black(sh.crop((SW // 2 - 2, 0, SW // 2 + 2, SH))), 'hb_sm.png')
# Keys: a 72 px glass circle, its 1 px rim, its shadow (112 square, the circle 8 px low)
save(white(capsule_mask(72, 72, 36)), 'hb_c72.png')
save(white(ring_mask(72, 72, 36)), 'hb_ce72.png')
cs = Image.new('L', (112, 112), 0)
cs.paste(capsule_mask(72, 72, 36), (20, 28))
save(black(cs.filter(ImageFilter.GaussianBlur(9))), 'hb_csh.png')
# Shelf: the soft shadow under the band, and a half-strength line
g = Image.new('L', (4, 60), 0)
for y in range(60):
    ImageDraw.Draw(g).line((0, y, 3, y), fill=int(150 * (1 - y / 60.0) ** 2))
save(black(g), 'hb_shelfsh.png')
save(white(Image.new('L', (4, 1), 128)), 'hb_half.png')

# ------------------------------------------------------------------------------------------- Includes_Fused.xml block
SH_COL = '$VAR[FG_PanelSh_80]'
FILL = '$VAR[FG_Frost]'
EDGE = '$VAR[FG_Edge]'
NAME = '$VAR[FG_HmNameC]'


def namebtn(tex, col, h, maxw=760):
    """the focused name's width, taken by a disabled button with the same text in transparent ink"""
    return ('<control type="button"><width max="%d">auto</width><height>%d</height><font>hm_display_60</font>'
            '<textoffsetx>0</textoffsetx><textcolor>00ffffff</textcolor><focusedcolor>00ffffff</focusedcolor>'
            '<disabledcolor>00ffffff</disabledcolor><label>%s</label>'
            '<texturefocus colordiffuse="%s">%s</texturefocus><texturenofocus colordiffuse="%s">%s</texturenofocus>'
            '<enable>false</enable></control>' % (maxw, h, NAME, col, tex, col, tex))


def img(w, h, tex, col=None, left=None, top=None):
    pos = ('<left>%d</left>' % left if left is not None else '') + ('<top>%d</top>' % top if top is not None else '')
    c = ' colordiffuse="%s"' % col if col else ''
    return '<control type="image">%s<width>%d</width><height>%d</height><texture%s>%s</texture></control>' % (pos, w, h, c, tex)


def grp(w, h, inner, vis=None):
    v = '<visible>%s</visible>' % vis if vis else ''
    return '<control type="group"><width>%d</width><height>%d</height>%s%s</control>' % (w, h, v, inner)


def glist(top, h, items, left=0, align='center'):
    a = '<align>center</align>' if align == 'center' else ''
    return ('<control type="grouplist"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
            '<orientation>horizontal</orientation><itemgap>0</itemgap><usecontrolcoords>true</usecontrolcoords>%s\n\t\t\t\t%s\n\t\t\t</control>'
            % (left, top, 1920 - left, h, a, '\n\t\t\t\t'.join(items)))


SH_TOP = 653 - SHT
SH_H = H + SHT + SHB
# side slots of the icons row (0.39.1): three each side, 150 px; the outer pair shows from 7 items on, and so on
SIDE_VIS = {3: 'Integer.IsGreater(Container(9000).NumItems,6)', 2: 'Integer.IsGreater(Container(9000).NumItems,4)',
            1: 'Integer.IsGreater(Container(9000).NumItems,2)'}
LEFT_SLOTS = (3, 2, 1)
RIGHT_SLOTS = (1, 2, 3)

# A Bar, icons mode: the capsule is the icons row itself (3 x 150 + 95 + 20 + name + 55 + 3 x 150)
bar_sh = [grp(53, SH_H, img(93, SH_H, 'fg/hb_sl.png', SH_COL, left=-40)), img(512, SH_H, 'fg/hb_sm.png', SH_COL),
          namebtn('fg/hb_sm.png', SH_COL, SH_H), img(452, SH_H, 'fg/hb_sm.png', SH_COL),
          grp(53, SH_H, img(93, SH_H, 'fg/hb_sr.png', SH_COL))]
bar_fill = [img(53, H, 'fg/hb_fl.png', FILL), img(512, H, 'common/white.png', FILL), namebtn('common/white.png', FILL, H),
            img(452, H, 'common/white.png', FILL), img(53, H, 'fg/hb_fr.png', FILL)]
bar_edge = [img(53, H, 'fg/hb_el.png', EDGE), img(512, H, 'fg/hb_em.png', EDGE), namebtn('fg/hb_em.png', EDGE, H),
            img(452, H, 'fg/hb_em.png', EDGE), img(53, H, 'fg/hb_er.png', EDGE)]


# B Keys, icons mode: a circle under each side icon, a capsule round the focused icon and its name
def side(slots, kind):
    out = []
    for n in slots:
        if kind == 'sh':
            out.append(grp(150, SH_H, img(112, 112, 'fg/hb_csh.png', SH_COL, left=19, top=SHT + 17 - 20), SIDE_VIS[n]))
        else:
            tex, col = ('fg/hb_c72.png', FILL) if kind == 'fill' else ('fg/hb_ce72.png', EDGE)
            out.append(grp(150, H, img(72, 72, tex, col, left=39, top=17), SIDE_VIS[n]))
    return out


keys_sh = (side(LEFT_SLOTS, 'sh') + [grp(75, SH_H, img(93, SH_H, 'fg/hb_sl.png', SH_COL, left=-18)),
                                     img(40, SH_H, 'fg/hb_sm.png', SH_COL), namebtn('fg/hb_sm.png', SH_COL, SH_H),
                                     grp(55, SH_H, img(93, SH_H, 'fg/hb_sr.png', SH_COL))] + side(RIGHT_SLOTS, 'sh'))
keys_fill = (side(LEFT_SLOTS, 'fill') + [img(22, H, 'fg/clear.png'), img(53, H, 'fg/hb_fl.png', FILL),
                                         img(40, H, 'common/white.png', FILL), namebtn('common/white.png', FILL, H),
                                         img(53, H, 'fg/hb_fr.png', FILL), img(2, H, 'fg/clear.png')] + side(RIGHT_SLOTS, 'fill'))
keys_edge = (side(LEFT_SLOTS, 'edge') + [img(22, H, 'fg/clear.png'), img(53, H, 'fg/hb_el.png', EDGE),
                                         img(40, H, 'fg/hb_em.png', EDGE), namebtn('fg/hb_em.png', EDGE, H),
                                         img(53, H, 'fg/hb_er.png', EDGE), img(2, H, 'fg/clear.png')] + side(RIGHT_SLOTS, 'edge'))

# titles mode (Home icons option off): the wraplist's focused item sits in slot 1 (x 620): icon at 660, name at 720
T_CAP = 660 - 33
# (a grouplist clips to its own box, so the shadow's list starts 40 px further left and its first piece is 93 wide)
keys_t_sh = [img(93, SH_H, 'fg/hb_sl.png', SH_COL), img(40, SH_H, 'fg/hb_sm.png', SH_COL),
             namebtn('fg/hb_sm.png', SH_COL, SH_H, 520), grp(53, SH_H, img(93, SH_H, 'fg/hb_sr.png', SH_COL))]
keys_t_fill = [img(53, H, 'fg/hb_fl.png', FILL), img(40, H, 'common/white.png', FILL), namebtn('common/white.png', FILL, H, 520),
               img(53, H, 'fg/hb_fr.png', FILL)]
keys_t_edge = [img(53, H, 'fg/hb_el.png', EDGE), img(40, H, 'fg/hb_em.png', EDGE), namebtn('fg/hb_em.png', EDGE, H, 520),
               img(53, H, 'fg/hb_er.png', EDGE)]


def fixed_capsule(x0, x1):
    mid = x1 - x0 - 2 * R
    return '\n\t\t\t'.join([
        img(93, SH_H, 'fg/hb_sl.png', SH_COL, left=x0 - 40, top=SH_TOP), img(mid, SH_H, 'fg/hb_sm.png', SH_COL, left=x0 + R, top=SH_TOP),
        img(93, SH_H, 'fg/hb_sr.png', SH_COL, left=x1 - R, top=SH_TOP),
        img(R, H, 'fg/hb_fl.png', FILL, left=x0, top=653), img(mid, H, 'common/white.png', FILL, left=x0 + R, top=653),
        img(R, H, 'fg/hb_fr.png', FILL, left=x1 - R, top=653),
        img(R, H, 'fg/hb_el.png', EDGE, left=x0, top=653), img(mid, H, 'fg/hb_em.png', EDGE, left=x0 + R, top=653),
        img(R, H, 'fg/hb_er.png', EDGE, left=x1 - R, top=653)])


SHELF = '\n\t\t\t'.join([
    img(1920, 60, 'fg/hb_shelfsh.png', SH_COL, left=0, top=653 + H),
    img(1920, H, 'common/white.png', FILL, left=0, top=653),
    img(1920, 1, 'common/white.png', EDGE, left=0, top=653),
    img(1920, 1, 'fg/hb_half.png', EDGE, left=0, top=653 + H - 1)])

ICONS = '$EXP[FG_HmIcons] + Control.IsVisible(9000)'
TITLES = '!$EXP[FG_HmIcons] + $EXP[Aeon_FGlass] + Control.IsVisible(9000)'


def group(vis, body, comment):
    return ('\t\t<!-- %s -->\n\t\t<control type="group">\n\t\t\t<include>Aeon_LowBand</include>\n\t\t\t<visible>%s</visible>\n'
            '\t\t\t%s\n\t\t</control>\n' % (comment, vis, body))


BLOCK = (
    '\t<!-- FG_GLASSMENU:begin (written by _src/fg_glassmenus.py) ============ Menu theme Glass and the Home bar (0.53.0)\n'
    '\t     Menu theme in Fused Glass: Dark (aeon.fgmenu empty, default) | Glass: settings menus, dialogs and information\n'
    '\t     pages in the material of Look > Material (FG_MenuFill, FG_MenuPanel, FG_KbFill, AG_PanelTex: fg_material.py).\n'
    '\t     Home bar (Backgrounds, aeon.homebar): Off | Bar | Keys | Shelf, frosted glass behind the Home menu row. -->\n'
    '\t<expression name="FG_GlassMenus">%s + %s</expression>\n'
    '\t<expression name="FG_HomeBarA">$EXP[Aeon_FGlass] + String.IsEqual(Skin.String(aeon.homebar),bar)</expression>\n'
    '\t<expression name="FG_HomeBarB">$EXP[Aeon_FGlass] + String.IsEqual(Skin.String(aeon.homebar),keys)</expression>\n'
    '\t<expression name="FG_HomeBarC">$EXP[Aeon_FGlass] + String.IsEqual(Skin.String(aeon.homebar),shelf)</expression>\n'
    '\t<!-- Glass: the settings backdrop shows more of its picture, under a lighter dim -->\n'
    '\t<variable name="FG_BackdropDim">\n\t\t<value condition="$EXP[FG_GlassMenus]">40000000</value>\n\t\t<value>66000000</value>\n\t</variable>\n'
    '\t<!-- under the menu row on Home (icons mode): drawn just before the icons row -->\n'
    '\t<include name="FG_HomeBarIcons">\n' % (FG, GM) +
    group(ICONS + ' + $EXP[FG_HomeBarA]', glist(SH_TOP, SH_H, bar_sh) + '\n\t\t\t' + glist(653, H, bar_fill) + '\n\t\t\t' + glist(653, H, bar_edge),
          'Bar: one capsule as wide as the row') +
    group(ICONS + ' + $EXP[FG_HomeBarB]', glist(SH_TOP, SH_H, keys_sh) + '\n\t\t\t' + glist(653, H, keys_fill) + '\n\t\t\t' + glist(653, H, keys_edge),
          'Keys: a circle under each side icon, a capsule round the focused icon and name') +
    group('Control.IsVisible(9000) + $EXP[FG_HomeBarC]', SHELF, 'Shelf: a band across the screen (both modes)') +
    '\t</include>\n'
    '\t<!-- titles mode: drawn just before the wraplist 9000 -->\n'
    '\t<include name="FG_HomeBarTitles">\n' +
    group(TITLES + ' + $EXP[FG_HomeBarA]', fixed_capsule(24, 1896), 'Bar: the titles run to the screen edges, so one capsule 24..1896') +
    group(TITLES + ' + $EXP[FG_HomeBarB]', glist(SH_TOP, SH_H, keys_t_sh, left=T_CAP - 40, align='left') + '\n\t\t\t' +
          glist(653, H, keys_t_fill, left=T_CAP, align='left') + '\n\t\t\t' + glist(653, H, keys_t_edge, left=T_CAP, align='left'),
          'Keys: a capsule round the focused title') +
    '\t</include>\n'
    '\t<!-- FG_GLASSMENU:end -->\n')

f = rd('Includes_Fused.xml')
f = re.sub(r'\t<!-- FG_GLASSMENU:begin.*?<!-- FG_GLASSMENU:end -->\n', '', f, flags=re.S)
f = f.replace('</includes>', BLOCK + '</includes>')
wr('Includes_Fused.xml', f)

# ------------------------------------------------------------------------------------------------- Home: the two hooks
h = rd('Includes_Aeon_Home.xml')
if '<include>FG_HomeBarTitles</include>' not in h:
    a = '\t\t<control type="wraplist" id="9000">\n'
    assert h.count(a) == 1
    h = h.replace(a, '\t\t<include>FG_HomeBarTitles</include>\n' + a)
    b = '\t\t<!-- Fused Glass, "only the focused item\'s name" (0.39.1)'
    assert h.count(b) == 1
    h = h.replace(b, '\t\t<include>FG_HomeBarIcons</include>\n' + b)
    wr('Includes_Aeon_Home.xml', h)

# Live TV page: the Watched last card ends 6 px above the row; with a Home bar it shrinks to 96 % from its top edge,
# so its foot clears the bar by the bar's own shadow margin (26 px) and its top stays clear of the clock pill
h = rd('Includes_Aeon_Home.xml')
ZOOM = ('<animation effect="zoom" end="96" center="960,112" time="0" condition="[$EXP[FG_HomeBarA] | $EXP[FG_HomeBarB] | '
        '$EXP[FG_HomeBarC]]">Conditional</animation>')
if ZOOM not in h:
    a = ('\t\t\t<include>Aeon_LowBand</include>\n\t\t\t<left>120</left>\n\t\t\t<top>120</top>\n'
         '\t\t\t<visible>$EXP[Aeon_H_LiveTV]</visible>\n')
    assert h.count(a) == 1
    h = h.replace(a, a + '\t\t\t' + ZOOM + '\n')
    wr('Includes_Aeon_Home.xml', h)

# ------------------------------------------------------------------- settings backdrop, dialog dim (Glass menus only)
g = rd('Includes_Aeon_Glass.xml')
if 'FG_BackdropDim' not in g:
    a = '\t<variable name="Aeon_BackdropAlpha">\n'
    assert g.count(a) == 1
    g = g.replace(a, a +
                  '\t\t<value condition="$EXP[FG_GlassMenus] + String.IsEqual(Skin.String(aeon.backdrop.dim),light)">4dffffff</value>\n'
                  '\t\t<value condition="$EXP[FG_GlassMenus] + String.IsEqual(Skin.String(aeon.backdrop.dim),strong)">b3ffffff</value>\n'
                  '\t\t<value condition="$EXP[FG_GlassMenus]">80ffffff</value>\n')
    i = g.index('<include name="Aeon_Backdrop">')
    j = g.index('</include>', i)
    part = g[i:j]
    assert part.count('<texture colordiffuse="66000000">common/white.png</texture>') == 1
    g = g[:i] + part.replace('<texture colordiffuse="66000000">common/white.png</texture>',
                             '<texture colordiffuse="$VAR[FG_BackdropDim]">common/white.png</texture>') + g[j:]
    wr('Includes_Aeon_Glass.xml', g)
a_ = rd('Includes_Aeon.xml')
if 'FG_GlassMenus]">5908090c' not in a_:
    a = '\t<variable name="AG_DimDialog">\n'
    assert a_.count(a) == 1
    a_ = a_.replace(a, a + '\t\t<value condition="$EXP[FG_GlassMenus]">5908090c</value>\n')
    wr('Includes_Aeon.xml', a_)
# the library options strip / view settings (1160 / 1166) and the open settings rail: FG_MenuPanel
for name, n in (('Includes_Aeon_Menu.xml', 2), ('Includes_Settings.xml', 1)):
    t = rd(name)
    old = 'colordiffuse="$VAR[FG_Panel]">fg/r32.png'
    if t.count(old) == n:
        wr(name, t.replace(old, 'colordiffuse="$VAR[FG_MenuPanel]">fg/r32.png'))
    else:
        assert t.count('$VAR[FG_MenuPanel]') == n, name
k = rd('Includes_Keyboard.xml')
if '<texture colordiffuse="f2101010">common/white.png</texture>' in k:
    assert k.count('<texture colordiffuse="f2101010">common/white.png</texture>') == 1
    wr('Includes_Keyboard.xml', k.replace('<texture colordiffuse="f2101010">common/white.png</texture>',
                                       '<texture colordiffuse="$VAR[FG_KbFill]">common/white.png</texture>'))

# ------------------------------------------------------------------------------------------------ Skin settings rows
FB = ImageFont.truetype(os.path.join('fonts', 'Figtree-Bold.ttf'), 22)


def po(lang_dir, ident):
    t = io.open(os.path.join('language', lang_dir, 'strings.po'), encoding='utf-8').read()
    m = re.search(r'msgctxt "#%d"\nmsgid "(.*)"\nmsgstr "(.*)"' % ident, t)
    return (m.group(2) or m.group(1)) if m else ''


LANGS = sorted(os.listdir('language'))


def cell_width(ident=None, localize=None, literal=None, minimum=92):
    """widest translation (Figtree Bold 22) + 40, at least the minimum"""
    if literal:
        texts = [literal]
    else:
        texts = [po(l, ident) for l in LANGS]
    return max(minimum, max(int(FB.getlength(t)) for t in texts) + 40)


def pills(row_id, cells, right, vis):
    """cells: [(condition, label, width)] -> track + per cell fill / label, focused and not (ms_settings_row style)"""
    total = sum(w for _, _, w in cells)
    x = right - total
    on = lambda c: '%s + [%s]' % (vis, c)
    off = lambda c: '%s + ![%s]' % (vis, c)
    out = ['<control type="image"><left>%d</left><top>13</top><width>%d</width><height>44</height><texture border="22,0,22,0" colordiffuse="22ffffff">$VAR[Aeon_MenuTexPill]</texture><visible>%s + !Control.HasFocus(%d)</visible></control>' % (x - 4, total + 8, vis, row_id),
           '<control type="image"><left>%d</left><top>13</top><width>%d</width><height>44</height><texture border="22,0,22,0" colordiffuse="26000000">$VAR[Aeon_MenuTexPill]</texture><visible>%s + Control.HasFocus(%d)</visible></control>' % (x - 4, total + 8, vis, row_id)]
    for cond, label, w in cells:
        geo = '<left>%d</left><top>13</top><width>%d</width><height>44</height>' % (x, w)
        out += ['<control type="image">%s<texture border="22,0,22,0" colordiffuse="$VAR[Aeon_Accent]">$VAR[Aeon_MenuTexPill]</texture><visible>%s + !Control.HasFocus(%d)</visible></control>' % (geo, on(cond), row_id),
                '<control type="image">%s<texture border="22,0,22,0" colordiffuse="$VAR[Aeon_OnBarFill]">$VAR[Aeon_MenuTexPill]</texture><visible>%s + Control.HasFocus(%d)</visible></control>' % (geo, on(cond), row_id),
                '<control type="label">%s<align>center</align><font>st_ui_22_bold</font><textcolor>$VAR[Aeon_AccentText]</textcolor><label>%s</label><visible>%s + !Control.HasFocus(%d)</visible></control>' % (geo, label, on(cond), row_id),
                '<control type="label">%s<align>center</align><font>st_ui_22_bold</font><textcolor>$VAR[Aeon_SegSelTxt]</textcolor><label>%s</label><visible>%s + Control.HasFocus(%d)</visible></control>' % (geo, label, on(cond), row_id),
                '<control type="label">%s<align>center</align><font>st_ui_22</font><textcolor>99ffffff</textcolor><label>%s</label><visible>%s + !Control.HasFocus(%d)</visible></control>' % (geo, label, off(cond), row_id),
                '<control type="label">%s<align>center</align><font>st_ui_22</font><textcolor>$VAR[Aeon_SegUnselF]</textcolor><label>%s</label><visible>%s + Control.HasFocus(%d)</visible></control>' % (geo, label, off(cond), row_id)]
        x += w
    return '\n\t\t\t\t'.join(out)


s = rd('SkinSettings.xml')
# 1. Menu theme (9748) in Fused Glass: Dark | Glass, set with OK on the row
start = s.index('<param name="id" value="9748"/>')
gs = s.rindex('<control type="group">', 0, start)
ge = s.index('\n\t\t\t</control>\n', start) + 1
row = s[gs:ge]
if 'aeon.fgmenu' not in row:
    old = '<onclick>RunScript(script.aeon.helper,menutheme)</onclick>'
    assert row.count(old) == 1
    row = row.replace(old, '<onclick condition="!%s">RunScript(script.aeon.helper,menutheme)</onclick>\n'
                           '\t\t\t\t\t<onclick condition="%s + %s">Skin.Reset(aeon.fgmenu)</onclick>\n'
                           '\t\t\t\t\t<onclick condition="%s + !%s">Skin.SetString(aeon.fgmenu,glass)</onclick>' % (FG, FG, GM, FG, GM))
    n = row.count('<visible>Skin.HasSetting(aeon.vglass) + [')
    assert n == 14, n
    row = row.replace('<visible>Skin.HasSetting(aeon.vglass) + [', '<visible>Skin.HasSetting(aeon.vglass) + !%s + [' % FG)
    cells = [('!' + GM, A % 32573, cell_width(32573, minimum=110)), (GM, 'Glass', 122)]
    # row = the group up to its closing tag (s[ge:] starts with it): the Fused Glass pills go last
    assert row.endswith('</control>\n')
    row = row + '\t\t\t\t<!-- Fused Glass (0.53.0): Dark (default) | Glass, aeon.fgmenu -->\n\t\t\t\t' + pills(9748, cells, 860, FG) + '\n'
    s = s[:gs] + row + s[ge:]

# 2. Backgrounds > Home bar (9764, Fused Glass) in the place of the Aeon / Glass Home band row (681)
if 'id="9764"' not in s:
    i = s.index('<control type="button" id="9737">')
    rg = s.rindex('\t\t\t<control type="group">\n', 0, i)
    re_ = s.index('\n\t\t\t</control>\n', i) + len('\n\t\t\t</control>\n')
    fb_end = rg
    fb = s.rindex('\t\t\t<control type="group">\n', 0, fb_end - 1)
    focus = s[fb:rg]
    assert 'Control.HasFocus(9737) + !$EXP[Aeon_FGlass]' in focus
    focus = focus.replace('Control.HasFocus(9737) + !$EXP[Aeon_FGlass]', 'Control.HasFocus(9764) + $EXP[Aeon_FGlass]')
    HB = 'Skin.String(aeon.homebar)'
    isv = lambda v: 'String.IsEqual(%s,%s)' % (HB, v)
    none = '![%s | %s | %s]' % (isv('bar'), isv('keys'), isv('shelf'))
    cells = [(none, '$LOCALIZE[31072]', cell_width(localize=31072, literal=None, ident=31072)),
             (isv('bar'), A % 32576, cell_width(32576)), (isv('keys'), A % 32577, cell_width(32577)),
             (isv('shelf'), A % 32578, cell_width(32578))]
    row = ('\t\t\t<!-- 0.53.0: Home bar (aeon.homebar, Fused Glass, off): frosted glass behind the Home menu row -->\n'
           '\t\t\t<control type="group">\n'
           '\t\t\t\t<top>681</top>\n'
           '\t\t\t\t<visible>$EXP[Aeon_FGlass]</visible>\n'
           '\t\t\t\t<include content="Dlg_SkinRowChrome">\n'
           '\t\t\t\t\t<param name="id" value="9764"/><param name="label" value="%s"/><param name="hint" value=""/><param name="labelTop" value="0"/><param name="labelH" value="70"/><param name="icon" value="aeon/icons/home.png"/><param name="labelx" value="46"/>\n'
           '\t\t\t\t</include>\n'
           '\t\t\t\t<control type="button" id="9764">\n'
           '\t\t\t\t\t<include>Dlg_SkinRowButton</include>\n'
           '\t\t\t\t\t<onup>9736</onup>\n'
           '\t\t\t\t\t<ondown>9730</ondown>\n'
           '\t\t\t\t\t<onback>9569</onback>\n'
           '\t\t\t\t\t<onleft>SetFocus(9569)</onleft>\n'
           '\t\t\t\t\t<onclick condition="%s">Skin.SetString(aeon.homebar,bar)</onclick>\n'
           '\t\t\t\t\t<onclick condition="%s">Skin.SetString(aeon.homebar,keys)</onclick>\n'
           '\t\t\t\t\t<onclick condition="%s">Skin.SetString(aeon.homebar,shelf)</onclick>\n'
           '\t\t\t\t\t<onclick condition="%s">Skin.Reset(aeon.homebar)</onclick>\n'
           '\t\t\t\t</control>\n'
           '\t\t\t\t%s\n'
           '\t\t\t</control>\n' % (A % 32575, none, isv('bar'), isv('keys'), isv('shelf'), pills(9764, cells, 856, '$EXP[Aeon_FGlass]')))
    s = s[:re_] + focus + row + s[re_:]
    # navigation in Fused Glass: 9736 -> 9764 -> 9730 (wraps to the top)
    a = '<ondown condition="!$EXP[Aeon_FGlass]">9737</ondown><ondown condition="$EXP[Aeon_FGlass]">9730</ondown>'
    assert s.count(a) == 1
    s = s.replace(a, '<ondown condition="!$EXP[Aeon_FGlass]">9737</ondown><ondown condition="$EXP[Aeon_FGlass]">9764</ondown>')
    a = '<onup condition="!$EXP[Aeon_FGlass]">9737</onup><onup condition="$EXP[Aeon_FGlass]">9736</onup>'
    assert s.count(a) == 1
    s = s.replace(a, '<onup condition="!$EXP[Aeon_FGlass]">9737</onup><onup condition="$EXP[Aeon_FGlass]">9764</onup>')
wr('SkinSettings.xml', s)

# 3. help lines
t = rd('Includes_Settings.xml')
if 'Control.HasFocus(9764)' not in t:
    a = '\t\t<value condition="Control.HasFocus(9748) + !Skin.HasSetting(aeon.vglass)">$ADDON[skin.aeon.fuse 32456]</value>\n'
    assert t.count(a) == 1
    t = t.replace(a, '\t\t<value condition="Control.HasFocus(9748) + %s">%s</value>\n' % (FG, A % 32574) + a)
    a = '\t\t<value condition="Control.HasFocus(9744)">$LOCALIZE[31579]</value>\n'
    assert t.count(a) == 1
    t = t.replace(a, a + '\t\t<value condition="Control.HasFocus(9764)">%s</value>\n' % (A % 32579))
    wr('Includes_Settings.xml', t)
print('ok')
