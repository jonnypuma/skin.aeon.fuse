# -*- coding: utf-8 -*-
"""0.56.22 Episode code: three more ways to write it (the user: "you were supposed to add more Episode codes in the
settings as well S1 E1, S1 | E1, S1 <bullet point> E1"). Skin.String(aeon.epcode): '' = 1x01, sxe = S01E01, sp = S1 E1,
bar = S1 | E1, dot = S1 • E1. Every Aeon_EpCode* variable gets the three; Skin settings row 9709 becomes five pills
(track 422-860), OK steps through them (Left / Back as before). Runs once; then run _src/ok_only.py."""
import io
import os
import re
import xml.etree.ElementTree as ET

SUB = os.path.join('1080i', 'Includes_Aeon_Sub.xml')
SET = os.path.join('1080i', 'SkinSettings.xml')
MARK = '0.56.22 epcode'
EP = 'Skin.String(aeon.epcode)'
IS = lambda v: 'String.IsEqual(%s,%s)' % (EP, v)
NEW = (('sp', 'S%(s)s E%(e)s'), ('bar', 'S%(s)s | E%(e)s'), ('dot', 'S%(s)s • E%(e)s'))
# (value, label, left, width): 1x01 | S01E01 | S1 E1 | S1 | E1 | S1 • E1
PILLS = [('', '1x01', 426, 76), ('sxe', 'S01E01', 502, 100), ('sp', 'S1 E1', 602, 80), ('bar', 'S1 | E1', 682, 88),
         ('dot', 'S1 • E1', 770, 86)]
ID = '9709'


def cond(value):
    if value:
        return IS(value)
    return '![%s]' % ' | '.join(IS(v) for v, _l, _x, _w in PILLS if v)


def variables():
    t = io.open(SUB, encoding='utf-8').read()
    n = 0
    for m in list(re.finditer(r'<variable name="Aeon_EpCode\w*">', t)):
        a = t.index(m.group(0))
        b = t.index('</variable>', a)
        block = t[a:b]
        if IS('sp') in block:
            continue
        prefix = re.search(r'String\.IsEmpty\(([^)]*(?:\([^)]*\))?[^)]*)\.Episode\)', block).group(1)
        fall = '<value condition="Integer.IsGreater(%s.Episode,9)">' % prefix
        assert block.count(fall) == 1, (m.group(0), fall)
        ins = ''.join('<value condition="%s">%s</value>\n\t\t' % (IS(v), f % {'s': '$INFO[%s.Season]' % prefix, 'e': '$INFO[%s.Episode]' % prefix})
                      for v, f in NEW)
        block = block.replace(fall, ins + fall)
        t = t[:a] + block + t[b:]
        n += 1
    io.open(SUB, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(SUB)
    return n


def row():
    t = io.open(SET, encoding='utf-8').read()
    if MARK in t:
        return False
    a = t.index('<control type="button" id="%s">' % ID)
    b = t.index('</control>', a) + len('</control>')
    button = t[a:b]
    clicks = re.findall(r'[ \t]*<onclick[^\n]*\n', button)
    assert len(clicks) == 2, clicks
    indent = clicks[0][:len(clicks[0]) - len(clicks[0].lstrip())]
    order = [v for v, _l, _x, _w in PILLS]
    new_clicks = ''.join('%s<onclick condition="%s">%s</onclick>\n' % (indent, cond(v), ('Skin.SetString(aeon.epcode,%s)' % order[(i + 1) % len(order)]) if order[(i + 1) % len(order)] else 'Skin.Reset(aeon.epcode)')
                         for i, v in enumerate(order))
    new_button = button.replace(''.join(clicks), new_clicks)
    assert new_button != button
    t = t[:a] + new_button + t[b:]
    # the pills: every image / label of this row at left 608 or 734
    b = t.index('</control>', a) + len('</control>')
    end = t.index('\n\t\t\t</control>', b)
    tail = t[b:end]
    olds = re.findall(r'\n[ \t]*<control type="(?:image|label)"><left>(?:608|734)</left>[^\n]*', tail)
    assert len(olds) == 14, len(olds)
    for line in olds:
        tail = tail.replace(line, '', 1)
    tab = '\t\t\t'
    pills = [tab + '<control type="image"><left>422</left><top>13</top><width>438</width><height>44</height><texture border="22,0,22,0" colordiffuse="22ffffff">$VAR[Aeon_MenuTexPill]</texture><visible>!Control.HasFocus(%s)</visible></control><!-- %s -->' % (ID, MARK),
             tab + '<control type="image"><left>422</left><top>13</top><width>438</width><height>44</height><texture border="22,0,22,0" colordiffuse="26000000">$VAR[Aeon_MenuTexPill]</texture><visible>Control.HasFocus(%s)</visible></control>' % ID]
    for v, label, x, w in PILLS:
        box = '<left>%d</left><top>13</top><width>%d</width><height>44</height>' % (x, w)
        c = cond(v)
        for colour, focus in (('$VAR[Aeon_Accent]', '!'), ('$VAR[Aeon_OnBarFill]', '')):
            pills.append(tab + '<control type="image">%s<texture border="22,0,22,0" colordiffuse="%s">$VAR[Aeon_MenuTexPill]</texture><visible>[%s] + %sControl.HasFocus(%s)</visible></control>' % (box, colour, c, focus, ID))
        for font, colour, sel, focus in (('st_ui_22_bold', '$VAR[Aeon_AccentText]', '', '!'), ('st_ui_22_bold', '$VAR[Aeon_SegSelTxt]', '', ''),
                                         ('st_ui_22', '99ffffff', '!', '!'), ('st_ui_22', '$VAR[Aeon_SegUnselF]', '!', '')):
            pills.append(tab + '<control type="label">%s<align>center</align><font>%s</font><textcolor>%s</textcolor><label>%s</label><visible>%s[%s] + %sControl.HasFocus(%s)</visible></control>' % (box, font, colour, label, sel, c, focus, ID))
    tail = tail.rstrip() + '\n' + '\n'.join(pills)
    t = t[:b] + tail + t[end:]
    io.open(SET, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(SET)
    return True


def main():
    print('variables', variables(), 'row', row())


if __name__ == '__main__':
    main()
