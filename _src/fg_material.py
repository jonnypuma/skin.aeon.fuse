"""0.45.0 Fused Glass material (mockup board Materials): Skin settings > Look > Material = Frost / Raised / Clear /
Today (Skin.String(aeon.fgmat): frost, raised, clear, '' = Today, the look so far and the default). Run from the skin
folder; safe to run again, and run it again after any generator that writes colordiffuse="fg_frost" / "fg_edge".

- every frosted panel's tint (fg_frost) and edge (fg_edge) follows $VAR[FG_Frost] / $VAR[FG_Edge]:
  Today b814161c / 1fffffff (tint 72 %), Frost 8c2a2e38 / 33ffffff (a lighter frost the picture's colours glow
  through), Raised the same frost with a lit rim 66ffffff, Clear 4d14161c / 26ffffff (tint 30 %)
- panel drop shadows (fg/sh24, sh28, sh32) follow $VAR[FG_PanelSh_xx]: deeper (e6000000) with Raised
- the artwork / focus shadow (FG_ShadowCol) is stronger with Frost and Raised
- Clear draws no blurred copy of the backdrop under the panels (library views, Planner)
- dialogs and the context menu (the baked dialogs/panel_fg.png) get a copy per material (0.45.1)
- 0.53.0, Menu theme Glass (aeon.fgmenu = glass, FG_GlassMenus from _src/fg_glassmenus.py): FG_MenuFill (the shared
  card, was fg_frost2) and FG_KbFill (keyboard) take the material's frost, and dialogs/panel_fgg*.png are the dialog
  panel in each material's frost
- 0.56.6: FG_Strip (the clock / A-Z rail) and FG_MenuPanel (library options strip, View settings, Skin settings
  rail) are one strip material, a step denser than the cards: b32a2e38 Frost / Raised, 9914161c Clear, cc14161c Dark
- 0.56.5 (replaced by 0.56.6): FG_MenuPanel (the side strips: library options strip, View settings, Skin settings rail) is dark in every
  material and menu theme (fa2a2e38 with Frost / Raised, else fa14161c: 98 %, so the list behind does not read through)
- 0.56.24: menus no longer follow the Library view theme (aeon.fgmat). FG_MenuFill / FG_KbFill / AG_PanelTex follow the
  Menu theme only (the Today values), FG_MenuPanel (left strips, Skin settings rail) is one dark strip (cc14161c), and
  the menu files (MENU_FILES: settings, dialogs, keyboard, context menu, information pages, toasts) draw edges, frost,
  panel fill, focus and panel shadows from fixed twins (FG_EdgeM, FG_FrostM, FG_PanelM, FG_ShadowColM, xx000000).
  The library copy of the shared card (Aeon_Glass_L) and the A-Z bubble keep the old fill (FG_LibCardFill); the
  Library view theme and Home bar preview cards in Skin settings keep the material (they show it)."""
import io
import os
import re
import xml.etree.ElementTree as ET

D = '1080i'
FUSED = os.path.join(D, 'Includes_Fused.xml')
SET = os.path.join(D, 'SkinSettings.xml')
HELP = os.path.join(D, 'Includes_Settings.xml')
A = '$ADDON[skin.aeon.fuse %d]'
M = 'Skin.String(aeon.fgmat)'
IS = lambda v: 'String.IsEqual(%s,%s)' % (M, v)
SH = 'String.IsEqual(Skin.String(aeon.fgshadow),%s)'        # 0.56.28 Panel shadow
ALPHAS = ('59', '66', '73', '80', '8c', '99', 'a6')

VARS = ('\t<!-- FG_MATERIAL:begin (written by _src/fg_material.py) ==================== Skin settings > Look > Material (0.45.0) -->\n'
        '\t<variable name="FG_Frost">\n'
        '\t\t<value condition="%s | %s">8c2a2e38</value>\n'
        '\t\t<value condition="%s">4d14161c</value>\n'
        '\t\t<value>b814161c</value>\n\t</variable>\n' % (IS('frost'), IS('raised'), IS('clear')) +
        '\t<variable name="FG_Edge">\n'
        '\t\t<value condition="%s">33ffffff</value>\n'
        '\t\t<value condition="%s">26ffffff</value>\n'
        '\t\t<value>1fffffff</value>\n\t</variable>\n' % (IS('frost'), IS('clear')) +      # 0.56.39: no rim (shadow_lift_05639)
        '\t<variable name="FG_Panel">\n'
        '\t\t<value condition="%s | %s">c22a2e38</value>\n'
        '\t\t<value condition="%s">8c14161c</value>\n'
        '\t\t<value>f514161c</value>\n\t</variable>\n' % (IS('frost'), IS('raised'), IS('clear')) +
        # 0.53.0: Menu theme Glass (Fused Glass, Skin.String(aeon.fgmenu) = glass): settings menus, dialogs and
        # information pages draw their cards in the material's frost instead of the dark fills
        # 0.56.12 (the user on the menu-tint mockups: "A. Darker will be the new Glass theme, and you will add B. Frost
        # as a third option"): Glass halfway from the old Glass to the Dark fill; Frost (FG_FrostMenus, first) the old
        # Glass with 30 % of a cool grey (40, 44, 54) over it, laid on the blurred backdrop (_src/fg_frostmenus.py)
        ''.join('\t<variable name="%s">\n'
                '\t\t<value condition="$EXP[FG_FrostMenus] + [%s | %s]">ae292d37</value>\n'
                '\t\t<value condition="$EXP[FG_FrostMenus] + %s">82202329</value>\n'
                '\t\t<value condition="$EXP[FG_FrostMenus]">b31e2129</value>\n'
                '\t\t<value condition="$EXP[FG_GlassMenus] + [%s | %s]">b222262e</value>\n'
                '\t\t<value condition="$EXP[FG_GlassMenus] + %s">93171a20</value>\n'
                '\t\t<value condition="$EXP[FG_GlassMenus]">c8171a20</value>\n'
                '%s\t</variable>\n' % (name, IS('frost'), IS('raised'), IS('clear'), IS('frost'), IS('raised'), IS('clear'), dark)
                for name, dark in (
                    ('FG_LibCardFill', '\t\t<value>d91a1d24</value>\n'),)) +       # 0.56.24: the library card (Aeon_Glass_L) and A-Z bubble
        # 0.56.24 (the user: the Library view theme "is only supposed to affect library view panels, not the menu, that's
        # why we have a Menu theme right above it"): the menus' fills follow the Menu theme only (the Today values)
        ''.join('\t<variable name="%s">\n'
                '\t\t<value condition="$EXP[FG_FrostMenus]">b31e2129</value>\n'
                '\t\t<value condition="$EXP[FG_GlassMenus]">c8171a20</value>\n'
                '%s\t</variable>\n' % (name, dark)
                for name, dark in (
                    ('FG_MenuFill', '\t\t<value>d91a1d24</value>\n'),              # Aeon_Glass cards (was fg_frost2)
                    ('FG_KbFill', '\t\t<value>f2101010</value>\n'))) +             # the keyboard's card
        # and fixed twins of the material variables for the menu files (MENU_FILES below)
        '\t<variable name="FG_FrostM">\n\t\t<value>b814161c</value>\n\t</variable>\n'
        '\t<variable name="FG_EdgeM">\n\t\t<value>1fffffff</value>\n\t</variable>\n' +
        ''
        '\t<variable name="FG_PanelM">\n\t\t<value>f514161c</value>\n\t</variable>\n'
        '\t<variable name="FG_ShadowColM">\n\t\t<value condition="String.IsEqual(Skin.String(aeon.fganim),glow)">66ffffff</value>\n'
        '\t\t<value>6b000000</value>\n\t</variable>\n'
        # 0.56.24: the left strips (library options 1160 / View settings 1166) and the Skin settings rail: one dark strip
        '\t<variable name="FG_MenuPanel">\n\t\t<value>cc14161c</value>\n\t</variable>\n' +
        # 0.56.5: the side strips (library options strip 1160 / View settings 1166, the Skin settings rail) are dark in
        # every material and menu theme, in the material's tone (the user: "glass shall be glass, except for the side
        # strips, they can be dark"; with Glass + Clear the strip was a 30 % tint and too see-through)
        # 0.56.6: one strip material for the side strips on both sides (the user: "does the settings side strip have the
        # same material as the clock/A-Z strip does now? it looks much darker? they should be the same"): FG_Strip is
        # the clock / A-Z rail of the views and FG_MenuPanel the left strip (1160 / 1166) and the Skin settings rail, a
        # step denser than the cards (FG_Frost) in each material; the blurred backdrop is under both in Frost /
        # Raised / Dark (fg/bmrail.png; the left strip's own layer, _src/fg_panel_blur.py)
        ''.join('\t<variable name="%s">\n'
                '\t\t<value condition="%s | %s">b32a2e38</value>\n'
                '\t\t<value condition="%s">9914161c</value>\n'
                '\t\t<value>cc14161c</value>\n\t</variable>\n' % (name, IS('frost'), IS('raised'), IS('clear'))
                for name in ('FG_Strip',)) +                                     # 0.56.24: FG_MenuPanel is fixed (above)
        # 0.56.28 Panel shadow (Skin.String(aeon.fgshadow), the user: "Instead of Raised as a style, we could have 'Panel
        # shadow' ... Mild, Medium (Default), Strong, Heavy ... Applies universally to menus, library views"): Medium is
        # the old shadow, Mild half of it, Strong 1.6 times, Heavy the old Raised (e6, with the lit rim of FG_Edge / FG_EdgeM)
        ''.join('\t<variable name="FG_PanelSh_%s">\n\t\t<value condition="%s">%02x000000</value>\n'
                '\t\t<value condition="%s">%02x000000</value>\n\t\t<value condition="%s">%02x000000</value>\n'
                '\t\t<value>%s000000</value>\n\t</variable>\n'
                % (a, SH % 'heavy', min(0xe6, int(round(int(a, 16) * 1.75))), SH % 'strong', min(0xe6, int(round(int(a, 16) * 1.4))), SH % 'mild', min(0xe6, int(round(int(a, 16) * 0.8))), a)
                for a in ALPHAS) +
        '\t<!-- FG_MATERIAL:end -->\n')

# 0.56.28 Expert settings: Panel opacity (aeon.x.pop) and Panel tint (aeon.x.ptint) at five steps each (_src/fg_expert.py)
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fg_expert
_exps, _combos = fg_expert.expressions('FGX', 'aeon.x.pop', 'aeon.x.ptint')
VARS, _twins = fg_expert.expand(VARS, ('FG_Frost', 'FG_Panel', 'FG_Strip', 'FG_LibCardFill', 'FG_MenuFill', 'FG_KbFill', 'FG_FrostM',
                                       'FG_PanelM', 'FG_MenuPanel'), 'FGX', _combos)
VARS = VARS.replace('\t<!-- FG_MATERIAL:end -->\n', _exps + _twins + '\t<!-- FG_MATERIAL:end -->\n')
f = io.open(FUSED, encoding='utf-8').read()
f = re.sub(r'\t<!-- FG_MATERIAL:begin.*?<!-- FG_MATERIAL:end -->\n', '', f, flags=re.S)
f = f.replace('</includes>', VARS + '</includes>')
# the artwork / focus shadow: stronger with Frost and Raised
old = '''	<variable name="FG_ShadowCol">
		<value condition="String.IsEqual(Skin.String(aeon.fganim),glow)">66ffffff</value>
		<value>8c000000</value>'''
if old in f:
    f = f.replace(old, '''	<variable name="FG_ShadowCol">
		<value condition="String.IsEqual(Skin.String(aeon.fganim),glow)">66ffffff</value>
		<value condition="%s | %s">b3000000</value>
		<value>6b000000</value>''' % (IS('frost'), IS('raised')))
io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(f)

# every XML file: frost, edge, panel shadows; Clear: no blurred backdrop under the panels
counts = {'frost': 0, 'edge': 0, 'shadow': 0, 'blur': 0}
for name in sorted(os.listdir(D)):
    if not name.endswith('.xml'):
        continue
    p = os.path.join(D, name)
    t = io.open(p, encoding='utf-8').read()
    n = t
    counts['frost'] += n.count('colordiffuse="fg_frost"')
    counts['edge'] += n.count('colordiffuse="fg_edge"')
    n = n.replace('colordiffuse="fg_frost"', 'colordiffuse="$VAR[FG_Frost]"').replace('colordiffuse="fg_edge"', 'colordiffuse="$VAR[FG_Edge]"')
    n = n.replace('colordiffuse="fg_panel"', 'colordiffuse="$VAR[FG_Panel]"')       # the open settings rail and the like (0.45.1)
    n = n.replace('colordiffuse="fg_frost2"', 'colordiffuse="$VAR[FG_MenuFill]"')  # dialog / settings cards (0.53.0)
    # the clock / A-Z rail of the views (64 x 1032, r32) takes the strip material (0.56.6)
    n = n.replace('<width>64</width><height>1032</height><texture border="32" colordiffuse="$VAR[FG_Frost]">fg/r32.png',
                  '<width>64</width><height>1032</height><texture border="32" colordiffuse="$VAR[FG_Strip]">fg/r32.png')
    def shadow(m):
        counts['shadow'] += 1
        return 'colordiffuse="$VAR[FG_PanelSh_%s]">fg/sh%s.png' % (m.group(1), m.group(2))
    n = re.sub(r'colordiffuse="(%s)000000">fg/sh(24|28|32)\.png' % '|'.join(ALPHAS), shadow, n)
    def blur(m):
        line = m.group(0)
        if 'aeon.fgmat' in line or 'FG_PanelBlurMat' in line or 'diffuse="fg/bmp_' in line:      # fg_panel_blur.py's layers set their own (0.56.6)
            return line
        counts['blur'] += 1
        return line.replace('</visible>', ' + !%s</visible>' % IS('clear'), 1)
    n = re.sub(r'[^\n]*\$INFO\[Window\(Home\)\.Property\(aeon\.blur\)\][^\n]*', blur, n)
    if n != t:
        io.open(p, 'w', encoding='utf-8', newline='\n').write(n)
print('frost %(frost)d, edge %(edge)d, panel shadows %(shadow)d, blur layers %(blur)d' % counts)

# Skin settings > Look: the Material row (9529, Fused Glass, under 9528 at 891), a copy of 9521 (four choices)
s = io.open(SET, encoding='utf-8').read()
if 'aeon.fgmat' not in s:
    lines = s.split('\n')
    # the focus-bar group of 9521 and its row group, by text: each starts at '<control type="group">'
    def block(start_marker_index):
        """the group that encloses the line index (walks back to its <control type="group"> and on to its end)"""
        i = start_marker_index
        while '<control type="group">' not in lines[i]:
            i -= 1
        depth, j = 0, i
        while True:
            depth += lines[j].count('<control') - lines[j].count('</control>')
            if depth == 0 and j > i:
                return i, j
            j += 1
    bar_at = next(k for k, l in enumerate(lines) if l.strip() == '<visible>Control.HasFocus(9521)</visible>')
    b0, b1 = block(bar_at)
    btn_at = next(k for k, l in enumerate(lines) if '<control type="button" id="9521">' in l)
    r0, r1 = block(btn_at)
    bar = '\n'.join(lines[b0:b1 + 1]).replace('<top>191</top>', '<top>891</top>').replace('Control.HasFocus(9521)', 'Control.HasFocus(9529)')
    row = '\n'.join(lines[r0:r1 + 1])
    row = row.replace('<top>191</top>', '<top>891</top>', 1)
    X = 'aeon.watchedmarkers'
    pairs = [('[String.IsEmpty(Skin.String(%s)) | String.IsEqual(Skin.String(%s),both)]' % (X, X), '@@SEG3@@'),
             ('String.IsEqual(Skin.String(%s),off)' % X, '@@SEG4@@'),
             ('Skin.SetString(%s,off)' % X, 'Skin.Reset(aeon.fgmat)'),
             ('Skin.SetString(%s,both)' % X, 'Skin.SetString(aeon.fgmat,clear)'),
             ('String.IsEqual(Skin.String(%s),unwatched)' % X, IS('frost')),
             ('Skin.SetString(%s,unwatched)' % X, 'Skin.SetString(aeon.fgmat,frost)'),
             ('String.IsEqual(Skin.String(%s),watched)' % X, IS('raised')),
             ('Skin.SetString(%s,watched)' % X, 'Skin.SetString(aeon.fgmat,raised)'),
             ('@@SEG3@@', IS('clear')),
             ('@@SEG4@@', '[String.IsEmpty(%s) | %s]' % (M, IS('today'))),
             ('$LOCALIZE[31744]', A % 32547), ('$LOCALIZE[31301]', A % 32548), ('$LOCALIZE[31080]', A % 32549),
             ('$LOCALIZE[31072]', '$ADDON[skin.aeon.fuse 32573]'), ('9521', '9529')]
    for a, b in pairs:
        row = row.replace(a, b)
    assert X not in row, 'a watched-markers condition was left'
    # navigation: up 9528, down 9521 (one each)
    row = re.sub(r'<onup[^>]*>[^<]*</onup>', '', row)
    row = row.replace('<ondown>9522</ondown>', '<onup>9528</onup><ondown>9521</ondown>', 1)
    # the row's title and icon (Dlg_SkinRowChrome) and Fused Glass only
    assert '<param name="label" value="$LOCALIZE[31055]"/>' in row and '<param name="icon" value="aeon/icons/check.png"/>' in row
    row = row.replace('<param name="label" value="$LOCALIZE[31055]"/>', '<param name="label" value="%s"/>' % (A % 32550))
    row = row.replace('<param name="icon" value="aeon/icons/check.png"/>', '<param name="icon" value="aeon/icons/layers.png"/>')
    row = row.replace('<control type="group">', '<control type="group">\n\t\t\t\t<visible>$EXP[Aeon_FGlass]</visible>', 1)
    # insert after the 9528 row group
    s2 = '\n'.join(lines)
    at = s2.index('<control type="button" id="9528">')
    k = s2[:at].count('\n')
    _, e1 = block(k)
    lines.insert(e1 + 1, row)
    lines.insert(b0, bar)              # the focus bar next to 9521's own (it is drawn under the rows)
    s = '\n'.join(lines)
    # chain: 9528 down -> 9529, 9521 up (Fused) -> 9529
    seg = s.index('<control type="button" id="9528">')
    end = s.index('</control>', s.index('<ondown>9521</ondown>', seg))
    s = s[:seg] + s[seg:end].replace('<ondown>9521</ondown>', '<ondown>9529</ondown>', 1) + s[end:]
    s = s.replace('<onup condition="$EXP[Aeon_FGlass]">9528</onup>', '<onup condition="$EXP[Aeon_FGlass]">9529</onup>', 1)
    io.open(SET, 'w', encoding='utf-8', newline='\n').write(s)
h = io.open(HELP, encoding='utf-8').read()
if 'Control.HasFocus(9529)' not in h:
    a = '\t\t<value condition="Control.HasFocus(9521)">$LOCALIZE[31611]</value>\n'
    assert a in h
    h = h.replace(a, a + '\t\t<value condition="Control.HasFocus(9529)">%s</value>\n' % (A % 32551))
    io.open(HELP, 'w', encoding='utf-8', newline='\n').write(h)
# the dialog / context menu panel (0.45.1): one baked picture (shadow, fill and edge in one, since Kodi resizes only
# the context menu's image 999), so each material gets its own copy of media/dialogs/panel_fg.png, made by fg_panel.py
from PIL import Image
MATS = {'frost': ((42, 46, 56), 0xc2 / 255.0, 0.20, 1.0), 'raised': ((42, 46, 56), 0xc2 / 255.0, 0.40, 1.4),
        'clear': ((20, 22, 28), 0x8c / 255.0, 0.15, 1.0)}
base = Image.open(os.path.join('media', 'dialogs', 'panel_fg.png')).convert('RGBA')
bp = base.load()
for mat, (fill, alpha, edge, shade) in MATS.items():
    out = Image.new('RGBA', base.size)
    op = out.load()
    for y in range(base.size[1]):
        for x in range(base.size[0]):
            r, g, b, a = bp[x, y]
            if (r, g, b) == (0, 0, 0):                   # shadow
                op[x, y] = (0, 0, 0, min(255, int(round(a * shade))))
            elif (r, g, b) == (26, 29, 36):              # fill (its rim keeps its antialiased alpha)
                op[x, y] = fill + (int(round(a / 0.94 * alpha)),)
            else:                                        # the hairline edge
                lit = tuple(int(round(c + (255 - c) * edge)) for c in fill)
                op[x, y] = lit + (int(round(a / 0.94 * max(alpha, 0.6))),)
    out.save(os.path.join('media', 'dialogs', 'panel_fg_%s.png' % mat), optimize=True)
# 0.53.0, Menu theme Glass: the same picture in the material's own frost (FG_Frost tint, FG_Edge rim): panel_fgg*.png
# 0.56.12: Glass a step darker (halfway to the Dark fill); Frost its light cool tint (panel_fgf*.png)
GLASS = {'': ((23, 26, 32), 0xc8 / 255.0, 0.20, 1.0), 'frost': ((34, 38, 46), 0xb2 / 255.0, 0.30, 1.0),
         'raised': ((34, 38, 46), 0xb2 / 255.0, 0.55, 1.4), 'clear': ((23, 26, 32), 0x93 / 255.0, 0.25, 1.0)}
FROST = {'': ((30, 33, 41), 0xb3 / 255.0, 0.30, 1.0), 'frost': ((41, 45, 55), 0xae / 255.0, 0.35, 1.0),
         'raised': ((41, 45, 55), 0xae / 255.0, 0.55, 1.4), 'clear': ((32, 35, 41), 0x82 / 255.0, 0.30, 1.0)}
for prefix, table in (('panel_fgg', GLASS), ('panel_fgf', FROST)):
    for mat, (fill, alpha, edge, shade) in table.items():
        out = Image.new('RGBA', base.size)
        op = out.load()
        for y in range(base.size[1]):
            for x in range(base.size[0]):
                r, g, b, a = bp[x, y]
                if (r, g, b) == (0, 0, 0):
                    op[x, y] = (0, 0, 0, min(255, int(round(a * shade))))
                elif (r, g, b) == (26, 29, 36):
                    op[x, y] = fill + (int(round(a / 0.94 * alpha)),)
                else:
                    lit = tuple(int(round(c + (255 - c) * edge)) for c in fill)
                    op[x, y] = lit + (int(round(a / 0.94 * max(alpha, 0.5))),)
        out.save(os.path.join('media', 'dialogs', '%s%s.png' % (prefix, '_' + mat if mat else '')), optimize=True)
aeon = os.path.join(D, 'Includes_Aeon.xml')
a = io.open(aeon, encoding='utf-8').read()
first = '\t\t<value condition="Skin.HasSetting(aeon.fglass)">dialogs/panel_fg.png</value>\n'
if 'panel_fg_frost.png' not in a:
    assert a.count(first) == 1
    a = a.replace(first, ''.join('\t\t<value condition="Skin.HasSetting(aeon.fglass) + %s">dialogs/panel_fg_%s.png</value>\n' % (IS(m), m)
                                 for m in ('frost', 'raised', 'clear')) + first)
if 'panel_fgf' not in a:                    # 0.56.12 Menu theme Frost: its own panels, before Glass's
    top = '\t\t<value condition="$EXP[FG_GlassMenus] + %s">dialogs/panel_fgg_frost.png</value>\n' % IS('frost')
    if top in a:
        a = a.replace(top, ''.join('\t\t<value condition="$EXP[FG_FrostMenus] + %s">dialogs/panel_fgf_%s.png</value>\n' % (IS(m), m)
                                   for m in ('frost', 'raised', 'clear')) +
                      '\t\t<value condition="$EXP[FG_FrostMenus]">dialogs/panel_fgf.png</value>\n' + top)
if 'panel_fgg' not in a:
    top = '\t\t<value condition="Skin.HasSetting(aeon.fglass) + %s">dialogs/panel_fg_frost.png</value>\n' % IS('frost')
    assert a.count(top) == 1
    a = a.replace(top, ''.join('\t\t<value condition="$EXP[FG_GlassMenus] + %s">dialogs/panel_fgg_%s.png</value>\n' % (IS(m), m)
                               for m in ('frost', 'raised', 'clear')) +
                  '\t\t<value condition="$EXP[FG_GlassMenus]">dialogs/panel_fgg.png</value>\n' + top)
# 0.56.24: the dialog panel follows the menu theme only (panel_fgf.png / panel_fgg.png / panel_fg.png); the material
# copies above stay on disk, unused
a = re.sub(r'\t\t<value condition="[^"]*aeon\.fgmat[^"]*">dialogs/panel_fg[fg]?_(?:frost|raised|clear)\.png</value>\n', '', a)
io.open(aeon, 'w', encoding='utf-8', newline='\n').write(a)

# 0.56.24: the menu files draw from the fixed twins (the Library view theme is for library view panels only)
MENU_FILES = ('SkinSettings.xml', 'Includes_Settings.xml', 'Includes_Aeon_Menu.xml', 'Includes_Keyboard.xml', 'Includes_Dialogs.xml',
              'DialogContextMenu.xml', 'DialogPVRGuideControls.xml', 'SettingsProfile.xml', 'EventLog.xml', 'script-aeon-fonts.xml',
              'Includes_VideoInfo.xml', 'DialogBusy.xml', 'DialogExtendedProgressBar.xml', 'DialogNotification.xml')
KEEP = ('Control.HasFocus(9529)', 'Control.HasFocus(9764)')       # the Skin settings previews of the material / Home bar


def to_menu(line):
    if any(k in line for k in KEEP):
        return line
    for v in ('FG_Edge', 'FG_Frost', 'FG_Panel', 'FG_ShadowCol'):
        line = line.replace('$VAR[%s]' % v, '$VAR[%sM]' % v)
    return line          # 0.56.28: the panel shadows follow Panel shadow everywhere, so the menus keep $VAR[FG_PanelSh_xx]


menu_lines = 0
for name in MENU_FILES:
    p = os.path.join(D, name)
    t = io.open(p, encoding='utf-8').read()
    n = '\n'.join(to_menu(x) for x in t.split('\n'))
    if n != t:
        menu_lines += sum(1 for x, y in zip(t.split('\n'), n.split('\n')) if x != y)
        io.open(p, 'w', encoding='utf-8', newline='\n').write(n)
# the shared card: Aeon_Glass (menus) on the twins, Aeon_Glass_L (library) and the A-Z bubble on the library fill
g = os.path.join(D, 'Includes_Aeon_Glass.xml')
t = io.open(g, encoding='utf-8').read()
i, j, k = t.index('\t<include name="Aeon_Glass">'), t.index('\t<include name="Aeon_Glass_L">'), t.index('\t<include name="Aeon_PageIn">')
n = t[:i] + '\n'.join(to_menu(x) for x in t[i:j].split('\n')) + t[j:k].replace('$VAR[FG_MenuFill]', '$VAR[FG_LibCardFill]') + t[k:]
if n != t:
    io.open(g, 'w', encoding='utf-8', newline='\n').write(n)
f = io.open(FUSED, encoding='utf-8').read()
i = f.index('\t<include name="FG_AZBubble">')
j = f.index('</include>', i)
n = f[:i] + f[i:j].replace('$VAR[FG_MenuFill]', '$VAR[FG_LibCardFill]') + f[j:]
if n != f:
    io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(n)
# the clock capsule: its frost and edge as params; the menus' copy of the clock box (Aeon_ClockBox: settings, dialogs,
# information pages) passes the fixed twins, the library copy (Aeon_ClockBox_L), Home and the screensaver the material
i = f.index('\t<include name="FG_ClockCapsule">')
j = f.index('\t</include>', i)
cap = f[i:j]
if '$PARAM[frost]' not in cap:
    new = cap.replace('<param name="wx">$EXP[AG_HasWeather]</param>\n',
                      '<param name="wx">$EXP[AG_HasWeather]</param>\n\t\t<param name="frost">$VAR[FG_Frost]</param>\n'
                      '\t\t<param name="edge">$VAR[FG_Edge]</param>\n', 1)
    new = new.replace('colordiffuse="$VAR[FG_Frost]"', 'colordiffuse="$PARAM[frost]"').replace('colordiffuse="$VAR[FG_Edge]"', 'colordiffuse="$PARAM[edge]"')
    assert new.count('$PARAM[frost]') == 2 and new.count('$PARAM[edge]') == 2 and new.count('<param name="frost">') == 1, cap[:200]
    f = f[:i] + new + f[j:]
    io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(f)
t = io.open(g, encoding='utf-8').read()
i = t.index('\t<include name="Aeon_ClockBox">')
j = t.index('\t</include>', i)
new = t[i:j].replace('<include>FG_ClockCapsule</include>', '<include content="FG_ClockCapsule"><param name="frost" value="$VAR[FG_FrostM]"/>'
                     '<param name="edge" value="$VAR[FG_EdgeM]"/></include>')
if new != t[i:j]:
    io.open(g, 'w', encoding='utf-8', newline='\n').write(t[:i] + new + t[j:])
print('menu lines on the fixed twins', menu_lines)
for name in [FUSED, SET, HELP, aeon, g] + [os.path.join(D, x) for x in MENU_FILES]:
    ET.parse(name)
print('ok')
