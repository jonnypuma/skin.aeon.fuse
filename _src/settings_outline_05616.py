# -*- coding: utf-8 -*-
"""0.56.16 Skin settings, Aeon and Glass themes (not Fuse, not Fused Glass): one outline language (the user: "why are the
dividing lines blue here? and why does this box have a brighter outline color? ... maybe they should change based on
where the highlight bar is? at least we need a more cohesive design for the outlines"):
- the category cells' rules are the settings rows' rule (1 px white 19 %), not a slate blue;
- the light frame (ff8a8f99) is drawn round the box the highlight bar is in: the categories while a category has the
  focus, the settings box (Aeon menu styles) while a setting has it. Runs once."""
import io
import os
import re
import xml.etree.ElementTree as ET

SS = os.path.join('1080i', 'SkinSettings.xml')
IS = os.path.join('1080i', 'Includes_Settings.xml')
MARK = '0.56.16 settings_outline'
CATS = ('9600', '9551', '9566', '9567', '9552', '9568', '9569', '9601', '9553', '9558', '9559')


def main():
    s = io.open(SS, encoding='utf-8').read()
    if MARK in s:
        print('already done')
        return
    ids = re.findall(r'<include content="Dlg_SkinCategory">\s*<param name="id" value="(\d+)"', s)
    assert tuple(ids) == CATS, ids
    cat = ' | '.join('Control.HasFocus(%s)' % i for i in CATS)
    # the category frame: only while a category has the focus
    old = '<texture colordiffuse="ff8a8f99">common/white.png</texture><visible>!$EXP[Aeon_Fused] + !$EXP[Aeon_FGlass]</visible></control>'
    assert s.count(old) == 4, s.count(old)
    s = s.replace(old, '<texture colordiffuse="ff8a8f99">common/white.png</texture><visible>!$EXP[Aeon_Fused] + !$EXP[Aeon_FGlass] + $EXP[Aeon_SkinCatFocus]</visible></control>')
    # the settings box frame (Aeon menu styles), in the same group (left 120): while a setting has the focus
    last = s.index('<control type="image"><left>359</left><top>191</top><width>1</width><height>770</height><texture colordiffuse="ff8a8f99">')
    e = s.index('</control>', last) + len('</control>')
    frame = ''
    for cond, x0, w in (('[$EXP[Aeon_MS_mosaic] | $EXP[Aeon_MS_ledger] | $EXP[Aeon_MS_bridge]]', 360, 1020), ('$EXP[Aeon_MS_tabslab]', 384, 996)):
        v = '<visible>%s + !$EXP[Aeon_SkinCatFocus]</visible>' % cond
        for x, y, ww, hh in ((x0, 191, w, 1), (x0, 191, 1, 770), (x0, 960, w, 1), (x0 + w - 1, 191, 1, 770)):
            frame += ('\n\t\t\t<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
                      '<texture colordiffuse="ff8a8f99">common/white.png</texture>%s</control>' % (x, y, ww, hh, v))
    s = s[:e] + '\n\t\t\t<!-- %s: the settings box framed while a setting has the focus (the categories while one of them has it) -->' % MARK + frame + s[e:]
    io.open(SS, 'w', encoding='utf-8', newline='\n').write(s)
    ET.parse(SS)
    t = io.open(IS, encoding='utf-8').read()
    old = '<control type="image"><left>0</left><top>-9</top><width>360</width><height>2</height><texture colordiffuse="ff2e3440">common/white.png</texture>'
    assert t.count(old) == 1
    t = t.replace(old, '<control type="image"><left>0</left><top>-8</top><width>360</width><height>1</height><texture colordiffuse="30ffffff">common/white.png</texture>')
    assert t.count('</includes>') == 1
    t = t.replace('</includes>', '\t<!-- %s: a category has the focus -->\n\t<expression name="Aeon_SkinCatFocus">%s</expression>\n</includes>' % (MARK, cat))
    io.open(IS, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(IS)
    print('ok')


if __name__ == '__main__':
    main()
