"""0.52.2 Skin settings: "Save lyrics next to the song" moves from Playback to Motion, memory, reset, under "Smooth song
progress" (9579), with a new id 9762.

Why: fg_lyricsave_row.py (0.45.1) put the row (id 9567) at Playback's top 891, where "Clearlogo in Now playing" (9550)
already was: Playback has 12 rows and 11 places, so the two were drawn over each other. 9567 is also the Ratings
category's id in the category list, so SetFocus(9567) (Left / Back on the Ratings rows) could land on the hidden row,
and the row's help line was never added (Includes_Settings.xml already had Control.HasFocus(9567) for the Ratings
category, so it showed the Ratings description). The user chose the move (2026-11-15).

Motion, memory, reset: 9549 -> 9579 -> 9762 -> 9540 (wraps); the row sits at 751 and, like 9548 / 9549 / 9579, moves
up 140 px when the memory rows are hidden (!Aeon_MemTrimRows). Left / Back go to the Motion category (9553).
Playback: 9539 <-> 9550 again. Run from the skin folder; runs once, then run _src/ok_only.py."""
import io
import xml.etree.ElementTree as ET

SET = '1080i/SkinSettings.xml'
HELP = '1080i/Includes_Settings.xml'
OLD, NEW = '9567', '9762'
SLIDE = '\t\t\t\t<animation effect="slide" end="0,-140" time="0" condition="!$EXP[Aeon_MemTrimRows]">Conditional</animation>'


def block(lines, i):
    while lines[i].strip() != '<control type="group">':
        i -= 1
    depth, j = 0, i
    while True:
        depth += lines[j].count('<control') - lines[j].count('</control>')
        if depth == 0 and j > i:
            return i, j
        j += 1


def rechain(s, rid, old, new):
    seg = s.index('<control type="button" id="%s">' % rid)
    end = s.index('</control>', seg)
    assert old in s[seg:end], (rid, old)
    return s[:seg] + s[seg:end].replace(old, new, 1) + s[end:]


s = io.open(SET, encoding='utf-8').read()
if 'id="%s"' % NEW not in s:
    lines = s.split('\n')
    playback = next(k for k, l in enumerate(lines) if 'Property(aeon.skincat),playback)' in l)
    # the row's focus bar on the Playback page (the category column has its own Control.HasFocus(9567) group)
    bar_at = next(k for k, l in enumerate(lines)
                  if k > playback and l.strip() == '<visible>Control.HasFocus(%s)</visible>' % OLD)
    b0, b1 = block(lines, bar_at)
    r0, r1 = block(lines, next(k for k, l in enumerate(lines) if '<control type="button" id="%s">' % OLD in l))
    assert b1 < r0 and r0 > playback
    bar = lines[b0:b1 + 1]
    row = lines[r0:r1 + 1]
    assert bar[2].strip() == '<top>891</top>' and row[1].strip() == '<top>891</top>', (bar[:3], row[:2])
    assert 'type="Visible" delay="160"' in row[2] and 'aeon.lyrics.save' in '\n'.join(row)
    # remove both from Playback (the row first: it comes later in the file)
    del lines[r0:r1 + 1]
    del lines[b0:b1 + 1]
    # focus bar: Playback's had no slide; Motion's lower rows slide up with the hidden memory rows
    bar = '\n'.join([bar[0], bar[1], bar[2].replace('891', '751'), SLIDE] + bar[3:]).replace(OLD, NEW)
    row = '\n'.join([row[0], row[1].replace('891', '751'), SLIDE, row[2].replace('delay="160"', 'delay="140"')] + row[3:])
    row = row.replace(OLD, NEW)
    for old, new in (('<onup>9539</onup>', '<onup>9579</onup>'), ('<ondown>9550</ondown>', '<ondown>9540</ondown>'),
                     ('<onback>9552</onback>', '<onback>9553</onback>'),
                     ('<onleft>SetFocus(9552)</onleft>', '<onleft>SetFocus(9553)</onleft>')):
        assert row.count(old) == 1, old
        row = row.replace(old, new)
    # into Motion: after 9579's focus bar and after 9579's row
    k = next(i for i, l in enumerate(lines) if '<control type="button" id="9579">' in l)
    _e0, e1 = block(lines, k)
    lines[e1 + 1:e1 + 1] = [row]
    f0, f1 = block(lines, next(i for i, l in enumerate(lines) if l.strip() == '<visible>Control.HasFocus(9579)</visible>'))
    lines[f1 + 1:f1 + 1] = [bar]
    s = '\n'.join(lines)
    s = rechain(s, '9539', '<ondown>%s</ondown>' % OLD, '<ondown>9550</ondown>')
    s = rechain(s, '9550', '<onup>%s</onup>' % OLD, '<onup>9539</onup>')
    s = rechain(s, '9579', '<ondown>9540</ondown>', '<ondown>%s</ondown>' % NEW)
    s = rechain(s, '9540', '<onup>9579</onup>', '<onup>%s</onup>' % NEW)
    io.open(SET, 'w', encoding='utf-8', newline='\n').write(s)
h = io.open(HELP, encoding='utf-8').read()
if 'Control.HasFocus(%s)' % NEW not in h:
    a = '\t\t<value condition="Control.HasFocus(9579)">$ADDON[skin.aeon.fuse 32569]</value>\n'
    assert a in h
    h = h.replace(a, a + '\t\t<value condition="Control.HasFocus(%s)">$ADDON[skin.aeon.fuse 32560]</value>\n' % NEW)
    io.open(HELP, 'w', encoding='utf-8', newline='\n').write(h)

root = ET.parse(SET).getroot()
parent = {c: p for p in root.iter() for c in p}
ids = [c.get('id') for c in root.iter('control') if c.get('id')]
assert ids.count(OLD) == 0 and ids.count(NEW) == 1, (ids.count(OLD), ids.count(NEW))
for i in ('9538', '9539', '9550', '9530', '9549', '9579', NEW, '9540'):
    b = [c for c in root.iter('control') if c.get('id') == i][0]
    print(i, 'top', parent[b].findtext('top'), 'up', [x.text for x in b.findall('onup')],
          'down', [x.text for x in b.findall('ondown')], 'left', [x.text for x in b.findall('onleft')],
          'back', [x.text for x in b.findall('onback')])
