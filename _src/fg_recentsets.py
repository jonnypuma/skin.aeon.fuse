# -*- coding: utf-8 -*-
"""0.45.2 "Home spotlight: recently watched sets" (Skin.HasSetting(aeon.sp.recentsets), off by default).

A Home spotlight whose path is the movie sets (videodb://movies/sets/ or a library://video/movies/sets... node; for a
custom item also its own sets path when no spotlight path is set) lists plugin://script.aeon.helper/?info=recentsets
instead: the sets played last, newest first, sorted by lastplayed descending (the items carry it). The editor (dialog
1163) keeps showing Aeon_SP2Path_* / Aeon_SP2Sort_*: only the four spotlight <content> lines read the new
Aeon_SP2List* wrappers (Aeon_SP2Src_* is taken: the ratings expressions).

- Includes_Aeon_Sub.xml: expressions Aeon_SP2Recent_<sec>, variables Aeon_SP2List_ / ListSort_ / ListOrder_<sec>
- Includes_Aeon_Home.xml: lists 9421 (movies), 9411-9413 (custom 1-3) read the wrappers
- SkinSettings.xml: row 9757 (copy of the switch 9752) after Home spotlight: transition (9754); 9755 / 9756 / 9758
  move down one row (70 px)
- Includes_Settings.xml: help line 32562
Run from the skin folder; runs once."""
import io
import xml.etree.ElementTree as ET

SUB = '1080i/Includes_Aeon_Sub.xml'
HOME = '1080i/Includes_Aeon_Home.xml'
SET = '1080i/SkinSettings.xml'
HELP = '1080i/Includes_Settings.xml'
SECS = ('movies', 'custom1', 'custom2', 'custom3')
PLUGIN = 'plugin://script.aeon.helper/?info=recentsets&amp;limit='


def sets_cond(sec):
    own = ('String.IsEqual(Skin.String(aeon.sp2.%s.path),videodb://movies/sets/) | '
           'String.StartsWith(Skin.String(aeon.sp2.%s.path),library://video/movies/sets)' % (sec, sec))
    if sec.startswith('custom'):
        n = sec[-1]
        own += (' | [String.IsEmpty(Skin.String(aeon.sp2.%s.path)) + '
                'String.StartsWith(Skin.String(CustomMenu.%s.Path),library://video/movies/sets)]' % (sec, n))
    return 'Skin.HasSetting(aeon.sp.recentsets) + [%s]' % own


def wrappers():
    out = ['\t<!-- Skin settings > Spotlight & widgets > Home spotlight: recently watched sets (0.45.2): a spotlight that',
           '\t     shows the movie sets lists the sets played last instead (helper ?info=recentsets, newest first). Only the',
           '\t     spotlight lists read these; the spotlight editor keeps showing the item\'s own path and sort. -->']
    for sec in SECS:
        out += ['\t<expression name="Aeon_SP2Recent_%s">%s</expression>' % (sec, sets_cond(sec)),
                '\t<variable name="Aeon_SP2List_%s">' % sec,
                '\t\t<value condition="$EXP[Aeon_SP2Recent_%s]">%s$VAR[Aeon_SP2Limit_%s]</value>' % (sec, PLUGIN, sec),
                '\t\t<value>$VAR[Aeon_SP2Path_%s]</value>' % sec,
                '\t</variable>',
                '\t<variable name="Aeon_SP2ListSort_%s">' % sec,
                '\t\t<value condition="$EXP[Aeon_SP2Recent_%s]">lastplayed</value>' % sec,
                '\t\t<value>$VAR[Aeon_SP2Sort_%s]</value>' % sec,
                '\t</variable>',
                '\t<variable name="Aeon_SP2ListOrder_%s">' % sec,
                '\t\t<value condition="$EXP[Aeon_SP2Recent_%s]">descending</value>' % sec,
                '\t\t<value>$VAR[Aeon_SP2Order_%s]</value>' % sec,
                '\t</variable>']
    return '\n'.join(out) + '\n'


# 1. wrappers, before the spotlight editor's display variables
s = io.open(SUB, encoding='utf-8').read()
if 'Aeon_SP2Recent_movies' not in s:
    anchor = '\t<variable name="Aeon_SP2E_Path">'
    assert s.count(anchor) == 1
    s = s.replace(anchor, wrappers() + anchor)
    io.open(SUB, 'w', encoding='utf-8', newline='\n').write(s)

# 2. the four spotlight lists
h = io.open(HOME, encoding='utf-8').read()
if '$VAR[Aeon_SP2List_movies]' not in h:
    for sec in SECS:
        old = ('<content sortby="$VAR[Aeon_SP2Sort_%s]" sortorder="$VAR[Aeon_SP2Order_%s]" limit="$VAR[Aeon_SP2Limit_%s]" '
               'browse="never" reload="$INFO[Window(Home).Property(aeon.sp2.reload)]">$VAR[Aeon_SP2Path_%s]</content>'
               % (sec, sec, sec, sec))
        new = ('<content sortby="$VAR[Aeon_SP2ListSort_%s]" sortorder="$VAR[Aeon_SP2ListOrder_%s]" limit="$VAR[Aeon_SP2Limit_%s]" '
               'browse="never" reload="$INFO[Window(Home).Property(aeon.sp2.reload)]">$VAR[Aeon_SP2List_%s]</content>'
               % (sec, sec, sec, sec))
        assert h.count(old) == 1, sec
        h = h.replace(old, new)
    io.open(HOME, 'w', encoding='utf-8', newline='\n').write(h)

# 3. Skin settings row 9757
s = io.open(SET, encoding='utf-8').read()
if 'aeon.sp.recentsets' not in s:
    lines = s.split('\n')

    def block(i):
        while '<control type="group">' not in lines[i]:
            i -= 1
        depth, j = 0, i
        while True:
            depth += lines[j].count('<control') - lines[j].count('</control>')
            if depth == 0 and j > i:
                return i, j
            j += 1

    def find(text):
        # a focus bar's <visible> stands on a line of its own; switch images carry the same condition inline
        # (and only the bar group sits at left -119: the "about" box at the right has the same <visible> line)
        if text.startswith('<visible>'):
            hits = [k for k, l in enumerate(lines) if l.strip() == text and lines[k - 2].strip() == '<left>-119</left>']
        else:
            hits = [k for k, l in enumerate(lines) if text in l]
        assert len(hits) == 1, (text, hits)
        return hits[0]

    # move 9758, 9756, 9755 (focus bar group + row group each) down 70 px, bottom first
    for rid, old, new in (('9758', 681, 751), ('9756', 611, 681), ('9755', 541, 611)):
        for start in (find('<visible>Control.HasFocus(%s)</visible>' % rid), find('<control type="button" id="%s">' % rid)):
            b0, b1 = block(start)
            hits = [k for k in range(b0, b1 + 1) if lines[k].strip() == '<top>%d</top>' % old]
            assert hits and hits[0] <= b0 + 3, (rid, hits)
            lines[hits[0]] = lines[hits[0]].replace('<top>%d</top>' % old, '<top>%d</top>' % new)
    # copy the switch 9752 (Widget screens: studio / network) as 9757 at 541
    b0, b1 = block(find('<visible>Control.HasFocus(9752)</visible>'))
    r0, r1 = block(find('<control type="button" id="9752">'))
    bar = '\n'.join(lines[b0:b1 + 1]).replace('<top>331</top>', '<top>541</top>', 1).replace('9752', '9757')
    row = '\n'.join(lines[r0:r1 + 1]).replace('<top>331</top>', '<top>541</top>', 1)
    assert row.count('aeon.sp.studio') == 23, row.count('aeon.sp.studio')
    row = row.replace('aeon.sp.studio', 'aeon.sp.recentsets').replace('9752', '9757')
    row = row.replace('<param name="label" value="$LOCALIZE[31979]"/>', '<param name="label" value="$ADDON[skin.aeon.fuse 32561]"/>')
    row = row.replace('<param name="icon" value="aeon/icons/tv.png"/>', '<param name="icon" value="aeon/icons/stack.png"/>')
    assert '<onup>9751</onup>' in row and '<ondown>9753</ondown>' in row and '32561' in row and 'stack.png' in row
    row = row.replace('<onup>9751</onup>', '<onup>9754</onup>').replace('<ondown>9753</ondown>', '<ondown>9755</ondown>')
    # bars sit with the bars (before the 9750 rows), rows after the transition row 9754
    _r0, r1_9754 = block(find('<control type="button" id="9754">'))
    lines[r1_9754 + 1:r1_9754 + 1] = [row]
    _b0, b1_9754 = block(find('<visible>Control.HasFocus(9754)</visible>'))
    lines[b1_9754 + 1:b1_9754 + 1] = [bar]
    s = '\n'.join(lines)

    def chain(button, old, new):
        global s
        seg = s.index('<control type="button" id="%s">' % button)
        end = s.index('</control>', seg)
        assert s[seg:end].count(old) == 1, (button, old)
        s = s[:seg] + s[seg:end].replace(old, new) + s[end:]

    chain('9754', '<ondown>9755</ondown>', '<ondown>9757</ondown>')
    chain('9755', '<onup>9754</onup>', '<onup>9757</onup>')
    io.open(SET, 'w', encoding='utf-8', newline='\n').write(s)

# 4. help line
t = io.open(HELP, encoding='utf-8').read()
if 'Control.HasFocus(9757)' not in t:
    a = '\t\t<value condition="Control.HasFocus(9754)">$LOCALIZE[31997]</value>\n'
    assert t.count(a) == 1
    t = t.replace(a, a + '\t\t<value condition="Control.HasFocus(9757)">$ADDON[skin.aeon.fuse 32562]</value>\n')
    io.open(HELP, 'w', encoding='utf-8', newline='\n').write(t)

# checks
for f in (SUB, HOME, SET, HELP):
    ET.parse(f)
root = ET.parse(SET).getroot()
for i in ('9754', '9757', '9755', '9756', '9758', '9750'):
    b = [c for c in root.iter('control') if c.get('id') == i]
    assert len(b) == 1, i
    print(i, 'up', [x.text for x in b[0].findall('onup')], 'down', [x.text for x in b[0].findall('ondown')])
print('ok')
