"""0.39.5 Skin settings > Home menu, Fused Glass:
- The options of the selected item (Disable, Choose type, Move up ... Restore default order) get the same third card
  as the context-menu editor's options (x 1552, 272 x 866, Aeon_Glass): it was drawn for ctxmenu only.
- "Choose icon" (9679, 0.26.0) was nested INSIDE the custom-1 "Set path / content" row group: on a custom item it
  sat on top of that row (the overlap), on any other item it was hidden with it. It is its own row again, between
  Rename and Set path; Set path's Up goes to it.
- The "Fuse" menu theme (aeon.menutheme = fused) no longer overrides Fused Glass: lists and buttons get the Fused
  white highlight (the box had Fuse on, so its highlights were the coloured Fuse bar).
Run in 1080i."""
import io
import re


def block_end(s, i):
    """End index (after '</control>') of the <control ...> element starting at i."""
    depth = 0
    for m in re.compile(r'<control\b|</control>').finditer(s, i):
        if m.group(0) == '</control>':
            depth -= 1
            if depth == 0:
                return m.end()
        else:
            depth += 1
    raise ValueError('unbalanced')


p = 'SkinSettings.xml'
s = io.open(p, encoding='utf-8').read()

# 1. the third card for the Home menu editor too
old = '<visible>$EXP[Aeon_FGlass] + String.IsEqual(Window(Home).Property(aeon.skincat),ctxmenu)</visible><include>Aeon_Glass</include>'
assert s.count(old) == 1
s = s.replace(old, '<visible>$EXP[Aeon_FGlass] + [String.IsEqual(Window(Home).Property(aeon.skincat),ctxmenu) | String.IsEqual(Window(Home).Property(aeon.skincat),homemenu)]</visible><include>Aeon_Glass</include>')

# 2. "Choose icon" out of the custom-1 row, before it
c1 = s.index('<visible>$EXP[Aeon_EditIsCustom1]</visible>')
g1 = s.rindex('<control type="group">', 0, c1)
g1 = s.rindex('\n', 0, g1) + 1                      # start of that line
g1_end = block_end(s, s.index('<control', g1))
cm = s.index('<!-- Choose icon (0.26.0)', g1, g1_end)
cm_line = s.rindex('\n', 0, cm) + 1
ic = s.index('<control type="group">', cm)
ic_end = block_end(s, ic)
assert '<control type="button" id="9679">' in s[ic:ic_end]
icon_block = s[cm_line:ic_end]
after = s[ic_end:]
nl = 1 if after.startswith('\n') else 0
s = s[:cm_line] + s[ic_end + nl:]                   # cut it out of the custom-1 group
# re-indent one level up (it was nested one level deeper) and put it before the custom-1 group
icon_block = '\n'.join(l[1:] if l.startswith('\t') else l for l in icon_block.split('\n')) + '\n'
g1 = s.rindex('<control type="group">', 0, s.index('<visible>$EXP[Aeon_EditIsCustom1]</visible>'))
g1 = s.rindex('\n', 0, g1) + 1
s = s[:g1] + icon_block + s[g1:]

# 3. Set path (custom 1) Up: Choose icon first
b = s.index('<control type="button" id="9668">')
old = '<onup condition="$EXP[Aeon_EditSlotOn]">9663</onup>'
k = s.index(old, b)
assert k - b < 800
s = s[:k] + '<onup condition="$EXP[Aeon_EditSlotOn]">9679</onup>' + s[k:]
io.open(p, 'w', encoding='utf-8', newline='').write(s)

# 4. Fused Glass over the Fuse menu theme
p = 'Includes_Aeon_Glass.xml'
g = io.open(p, encoding='utf-8').read()
F = 'String.IsEqual(Skin.String(aeon.menutheme),fused)'
assert g.count('<expression name="Aeon_Fused">%s</expression>' % F) == 1
g = g.replace('<expression name="Aeon_Fused">%s</expression>' % F,
              '<expression name="Aeon_Fused">%s + !Skin.HasSetting(aeon.fglass)</expression>' % F)
n_pos = g.count('<include condition="%s">' % F)
n_neg = g.count('<include condition="!%s' % F)
g = g.replace('<include condition="%s">' % F, '<include condition="%s + !Skin.HasSetting(aeon.fglass)">' % F)
g = g.replace('<include condition="!%s">' % F, '<include condition="[!%s | Skin.HasSetting(aeon.fglass)]">' % F)
g = g.replace('<include condition="!%s + Skin.HasSetting(aeon.fglass)">' % F, '<include condition="Skin.HasSetting(aeon.fglass)">')
g = g.replace('<include condition="!%s + Skin.HasSetting(aeon.vglass) + !Skin.HasSetting(aeon.fglass)">' % F,
              '<include condition="!%s + Skin.HasSetting(aeon.vglass) + !Skin.HasSetting(aeon.fglass)">' % F)
g = g.replace('<include condition="!%s + !Skin.HasSetting(aeon.vglass)">' % F,
              '<include condition="!%s + !Skin.HasSetting(aeon.vglass) + !Skin.HasSetting(aeon.fglass)">' % F)
io.open(p, 'w', encoding='utf-8', newline='').write(g)
print('ok', n_pos, n_neg)
