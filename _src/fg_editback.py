"""0.39.5 Skin settings > Home menu / Context menu editors: Back on an option row (Disable, Choose type ...) closed
Skin settings: its <onback>SetFocus($INFO[..editrow])</onback> runs the builtin and then lets Back fall through
(an onback needs a control id). Now one conditional plain id per slot row (the row the options belong to), the
category button when none is set. Fused Glass: both option columns sit 20 px further right, inside their card
(they started 16 px left of it).
Run in 1080i."""
import io
import re

p = 'SkinSettings.xml'
s = io.open(p, encoding='utf-8').read()
for prop, fallback in (('editrow', '9558'), ('ctxrow', '9559')):
    ids = sorted(set(re.findall(r'SetProperty\(aeon\.%s,(\d+),home\)' % prop, s)))
    old = '<onback>SetFocus($INFO[Window(Home).Property(aeon.%s)])</onback>' % prop
    new = ''.join('<onback condition="String.IsEqual(Window(Home).Property(aeon.%s),%s)">%s</onback>' % (prop, i, i) for i in ids) + '<onback>%s</onback>' % fallback
    n = s.count(old)
    s = s.replace(old, new)
    print(prop, n, ids)
# Fused Glass: the option columns inside their card
for cat in ('ctxmenu', 'homemenu'):
    T = '\t'
    old = T * 3 + '<left>1536</left><top>168</top>\n' + T * 3 + '<visible>String.IsEqual(Window(Home).Property(aeon.skincat),%s)</visible>\n' % cat
    assert s.count(old) == 1, cat
    s = s.replace(old, old + T * 3 + '<animation effect="slide" end="20,0" time="0" condition="$EXP[Aeon_FGlass]">Conditional</animation>\n')
io.open(p, 'w', encoding='utf-8', newline='').write(s)
