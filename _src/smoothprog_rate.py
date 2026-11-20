"""0.52.3 Smooth song progress on by default, and how often it moves (the user's wish, 2026-11-15).

- The switch (row 9579) now stores the opposite: Skin.HasSetting(aeon.smoothprogress.off), so nothing set = on. OK
  toggles it (one Skin.ToggleSetting). The card's expression Aeon_SmoothProgress (Includes_Aeon_Music.xml) and the
  helper (smoothprog.py ACTIVE) read the same.
- New row 9763 "Updates per second" under it at 751: Screen | 10 | 25 | 30 | 60, Skin.String(aeon.smoothprogress.rate)
  '' (Screen: as often as Kodi draws the GUI, the default), 10, 25, 30, 60; OK steps through them, Left / Back go to
  the Motion category (9553). Pills: track x 454-860, Screen 140 px (Czech "Obrazovka" is the widest at 112 px),
  numbers 64 px; row labels end left of 454 in every language (_src/smoothprog_rate_strings.py).
- "Save lyrics next to the song" (9762) moves down to 821. All three slide up 140 px with the other lower Motion rows
  when the memory rows are hidden (!Aeon_MemTrimRows). Chain: 9549 -> 9579 -> 9763 -> 9762 -> 9540.
Run from the skin folder; runs once, then run _src/ok_only.py."""
import io
import xml.etree.ElementTree as ET

SET = '1080i/SkinSettings.xml'
HELP = '1080i/Includes_Settings.xml'
MUSIC = '1080i/Includes_Aeon_Music.xml'
ID = '9763'
SLIDE = '\t\t\t\t<animation effect="slide" end="0,-140" time="0" condition="!$EXP[Aeon_MemTrimRows]">Conditional</animation>'
RATE = 'Skin.String(aeon.smoothprogress.rate)'
IS = dict((v, 'String.IsEqual(%s,%s)' % (RATE, v)) for v in ('10', '25', '30', '60'))
SCREEN = '![%s]' % ' | '.join(IS[v] for v in ('10', '25', '30', '60'))
# (condition, label, left, width, value OK sets next)
OPTIONS = [(SCREEN, '$ADDON[skin.aeon.fuse 32571]', 458, 140, 'Skin.SetString(%s,10)' % RATE[12:-1]),
           (IS['10'], '$NUMBER[10]', 598, 64, 'Skin.SetString(%s,25)' % RATE[12:-1]),
           (IS['25'], '$NUMBER[25]', 662, 64, 'Skin.SetString(%s,30)' % RATE[12:-1]),
           (IS['30'], '$NUMBER[30]', 726, 64, 'Skin.SetString(%s,60)' % RATE[12:-1]),
           (IS['60'], '$NUMBER[60]', 790, 64, 'Skin.Reset(%s)' % RATE[12:-1])]


def block(lines, i):
    while lines[i].strip() != '<control type="group">':
        i -= 1
    depth, j = 0, i
    while True:
        depth += lines[j].count('<control') - lines[j].count('</control>')
        if depth == 0 and j > i:
            return i, j
        j += 1


def find(lines, text):
    # a <visible> anchor must be the whole line (the switch images carry the same condition inside their own tags)
    hits = [k for k, l in enumerate(lines) if (l.strip() == text if text.startswith('<visible>') else text in l)]
    assert len(hits) == 1, (text, len(hits))
    return hits[0]


def rechain(s, rid, old, new):
    seg = s.index('<control type="button" id="%s">' % rid)
    end = s.index('</control>', seg)
    assert old in s[seg:end], (rid, old)
    return s[:seg] + s[seg:end].replace(old, new, 1) + s[end:]


def pills():
    t = '\t\t\t\t'
    out = [t + '<control type="image"><left>454</left><top>13</top><width>406</width><height>44</height><texture border="22,0,22,0" colordiffuse="22ffffff">$VAR[Aeon_MenuTexPill]</texture><visible>!Control.HasFocus(%s)</visible></control>' % ID,
           t + '<control type="image"><left>454</left><top>13</top><width>406</width><height>44</height><texture border="22,0,22,0" colordiffuse="26000000">$VAR[Aeon_MenuTexPill]</texture><visible>Control.HasFocus(%s)</visible></control>' % ID]
    for cond, label, x, w, _next in OPTIONS:
        box = '<left>%d</left><top>13</top><width>%d</width><height>44</height>' % (x, w)
        for colour, focus in (('$VAR[Aeon_Accent]', '!'), ('$VAR[Aeon_OnBarFill]', '')):
            out.append(t + '<control type="image">%s<texture border="22,0,22,0" colordiffuse="%s">$VAR[Aeon_MenuTexPill]</texture><visible>[%s] + %sControl.HasFocus(%s)</visible></control>' % (box, colour, cond, focus, ID))
        for font, colour, sel, focus in (('st_ui_22_bold', '$VAR[Aeon_AccentText]', '', '!'),
                                         ('st_ui_22_bold', '$VAR[Aeon_SegSelTxt]', '', ''),
                                         ('st_ui_22', '99ffffff', '!', '!'),
                                         ('st_ui_22', '$VAR[Aeon_SegUnselF]', '!', '')):
            out.append(t + '<control type="label">%s<align>center</align><font>%s</font><textcolor>%s</textcolor><label>%s</label><visible>%s[%s] + %sControl.HasFocus(%s)</visible></control>' % (box, font, colour, label, sel, cond, focus, ID))
    return out


s = io.open(SET, encoding='utf-8').read()
if RATE not in s:
    lines = s.split('\n')
    # 1. the switch: on unless aeon.smoothprogress.off is set
    r0, r1 = block(lines, find(lines, '<control type="button" id="9579">'))
    row = '\n'.join(lines[r0:r1 + 1])
    on = '<onclick condition="!Skin.HasSetting(aeon.smoothprogress)">Skin.SetBool(aeon.smoothprogress)</onclick>'
    off = '<onclick condition="Skin.HasSetting(aeon.smoothprogress)">Skin.Reset(aeon.smoothprogress)</onclick>'
    assert row.count(on) == 1 and row.count(off) == 1
    row = row.replace(on, '<onclick>Skin.ToggleSetting(aeon.smoothprogress.off)</onclick>')
    row = row.replace('\t\t\t\t\t' + off + '\n', '')
    row = row.replace('Skin.HasSetting(aeon.smoothprogress)', '!Skin.HasSetting(aeon.smoothprogress.off)')
    assert 'aeon.smoothprogress)' not in row and row.count('aeon.smoothprogress.off') == 15, row.count('aeon.smoothprogress.off')
    head = row.split('\n')[:4]
    lines[r0:r1 + 1] = row.split('\n')
    # 2. Save lyrics (9762) down to 821: its row and its focus bar
    for anchor in ('<control type="button" id="9762">', '<visible>Control.HasFocus(9762)</visible>'):
        g0, _g1 = block(lines, find(lines, anchor))
        top = next(k for k in range(g0, g0 + 4) if lines[k].strip().startswith('<top>'))
        assert lines[top].strip() == '<top>751</top>', lines[top]
        lines[top] = lines[top].replace('751', '821')
    # 3. the new row after 9579's row
    assert head[1].strip() == '<top>681</top>' and head[2] == SLIDE and 'delay="120"' in head[3], head
    new_row = [head[0], head[1].replace('681', '751'), SLIDE, head[3].replace('delay="120"', 'delay="140"'),
               '\t\t\t\t<include content="Dlg_SkinRowChrome">',
               '\t\t\t\t\t<param name="id" value="%s"/><param name="label" value="$ADDON[skin.aeon.fuse 32570]"/><param name="hint" value=""/><param name="labelTop" value="0"/><param name="labelH" value="70"/><param name="icon" value="aeon/icons/motion.png"/><param name="labelx" value="46"/>' % ID,
               '\t\t\t\t</include>',
               '\t\t\t\t<control type="button" id="%s">' % ID,
               '\t\t\t\t\t<include>Dlg_SkinRowButton</include>',
               '\t\t\t\t\t<onup>9579</onup>',
               '\t\t\t\t\t<ondown>9762</ondown>',
               '\t\t\t\t\t<onback>9553</onback>',
               '\t\t\t\t\t<onleft>SetFocus(9553)</onleft>']
    new_row += ['\t\t\t\t\t<onclick condition="%s">%s</onclick>' % (cond, nxt) for cond, _l, _x, _w, nxt in OPTIONS]
    new_row += ['\t\t\t\t</control>'] + pills() + ['\t\t\t</control>']
    _r0, r1 = block(lines, find(lines, '<control type="button" id="9579">'))
    lines[r1 + 1:r1 + 1] = new_row
    # 4. its focus bar after 9579's
    f0, f1 = block(lines, find(lines, '<visible>Control.HasFocus(9579)</visible>'))
    bar = '\n'.join(lines[f0:f1 + 1])
    assert bar.count('<top>681</top>') == 1
    lines[f1 + 1:f1 + 1] = bar.replace('<top>681</top>', '<top>751</top>').replace('9579', ID).split('\n')
    s = '\n'.join(lines)
    s = rechain(s, '9579', '<ondown>9762</ondown>', '<ondown>%s</ondown>' % ID)
    s = rechain(s, '9762', '<onup>9579</onup>', '<onup>%s</onup>' % ID)
    io.open(SET, 'w', encoding='utf-8', newline='\n').write(s)

h = io.open(HELP, encoding='utf-8').read()
if 'Control.HasFocus(%s)' % ID not in h:
    a = '\t\t<value condition="Control.HasFocus(9579)">$ADDON[skin.aeon.fuse 32569]</value>\n'
    assert a in h
    h = h.replace(a, a + '\t\t<value condition="Control.HasFocus(%s)">$ADDON[skin.aeon.fuse 32572]</value>\n' % ID)
    io.open(HELP, 'w', encoding='utf-8', newline='\n').write(h)

m = io.open(MUSIC, encoding='utf-8').read()
old = '<expression name="Aeon_SmoothProgress">Skin.HasSetting(aeon.smoothprogress) + '
if old in m:
    m = m.replace(old, '<expression name="Aeon_SmoothProgress">!Skin.HasSetting(aeon.smoothprogress.off) + ')
    m = m.replace('<!-- 0.52.1 Smooth song progress: the helper (script.aeon.helper smoothprog.py) is driving the card\'s fill 4801 -->',
                  '<!-- 0.52.1 Smooth song progress (on by default since 0.52.3): the helper (script.aeon.helper smoothprog.py) is\n'
                  '\t     driving the card\'s fill 4801 -->')
    m = m.replace('the helper sets its percent as a fraction about twice per\n'
                  '\t\t\t     pixel of travel (up to 60 times a second)',
                  'the helper sets its percent as a fraction (as often as Kodi\n'
                  '\t\t\t     draws the screen, or 10 / 25 / 30 / 60 times a second)')
    assert 'about twice per' not in m
    io.open(MUSIC, 'w', encoding='utf-8', newline='\n').write(m)

root = ET.parse(SET).getroot()
ET.parse(MUSIC)
parent = {c: p for p in root.iter() for c in p}
for i in ('9549', '9579', ID, '9762', '9540'):
    b = [c for c in root.iter('control') if c.get('id') == i]
    assert len(b) == 1, i
    b = b[0]
    print(i, 'top', parent[b].findtext('top'), 'up', [x.text for x in b.findall('onup')],
          'down', [x.text for x in b.findall('ondown')], 'left', [x.text for x in b.findall('onleft')],
          'click', [x.text for x in b.findall('onclick')])
