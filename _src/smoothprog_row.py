"""0.52.1 Skin settings > Motion, memory, reset: "Smooth song progress" (row 9579, Skin.HasSetting(aeon.smoothprogress),
off by default), a copy of the switch row "Reduce motion" (9540) placed last, under "Check library art now" (9549) at
681. Like 9548 / 9549 it moves up 140 px when the memory rows are hidden (!Aeon_MemTrimRows). The Playback page has
no free row (11 places, 12 rows: 9567 and 9550 already share 891). OK toggles; Left goes back to the category list
(SetFocus(9553)), as ok_only.py wants. Help line: 32569 (Includes_Settings.xml). Run from the skin folder; runs once,
then run _src/ok_only.py."""
import io
import xml.etree.ElementTree as ET

SET = '1080i/SkinSettings.xml'
HELP = '1080i/Includes_Settings.xml'
SLIDE = '\t\t\t\t<animation effect="slide" end="0,-140" time="0" condition="!$EXP[Aeon_MemTrimRows]">Conditional</animation>'
s = io.open(SET, encoding='utf-8').read()
if 'aeon.smoothprogress' not in s:
    lines = s.split('\n')

    def block(i):
        while lines[i].strip() != '<control type="group">':
            i -= 1
        depth, j = 0, i
        while True:
            depth += lines[j].count('<control') - lines[j].count('</control>')
            if depth == 0 and j > i:
                return i, j
            j += 1

    # focus bar: a copy of 9549's (top 611, with the slide) at 681
    b0, b1 = block(next(k for k, l in enumerate(lines) if l.strip() == '<visible>Control.HasFocus(9549)</visible>'))
    bar = '\n'.join(lines[b0:b1 + 1])
    assert bar.count('<top>611</top>') == 1 and SLIDE in bar
    bar = bar.replace('<top>611</top>', '<top>681</top>').replace('9549', '9579')
    # row: a copy of Reduce motion (9540, top 191) at 681 with the slide; the Visible animation keeps aeon.reducemotion
    r0, r1 = block(next(k for k, l in enumerate(lines) if '<control type="button" id="9540">' in l))
    head, body = lines[r0:r0 + 3], lines[r0 + 3:r1 + 1]
    assert head[1].strip() == '<top>191</top>' and 'type="Visible" delay="0"' in head[2], head
    head = [head[0], head[1].replace('191', '681'), SLIDE, head[2].replace('delay="0"', 'delay="120"')]
    row = '\n'.join(body)
    assert row.count('aeon.reducemotion') == 18, row.count('aeon.reducemotion')
    row = row.replace('aeon.reducemotion', 'aeon.smoothprogress').replace('9540', '9579')
    row = row.replace('<param name="label" value="$LOCALIZE[31058]"/>', '<param name="label" value="$ADDON[skin.aeon.fuse 32568]"/>')
    row = row.replace('<param name="icon" value="aeon/icons/pause.png"/>', '<param name="icon" value="aeon/icons/music.png"/>')
    assert '<onup>9549</onup>' in row and '<ondown>9545</ondown>' in row
    row = row.replace('<ondown>9545</ondown>', '<ondown>9540</ondown>')
    assert '32568' in row and 'music.png' in row
    row = '\n'.join(head) + '\n' + row
    # after 9549's focus bar and after 9549's row
    k = next(i for i, l in enumerate(lines) if '<control type="button" id="9549">' in l)
    _e0, e1 = block(k)
    lines[e1 + 1:e1 + 1] = [row]
    lines[b1 + 1:b1 + 1] = [bar]
    s = '\n'.join(lines)
    # chain: 9549 down -> 9579, 9540 up -> 9579
    for rid, old, new in (('9549', '<ondown>9540</ondown>', '<ondown>9579</ondown>'),
                          ('9540', '<onup>9549</onup>', '<onup>9579</onup>')):
        seg = s.index('<control type="button" id="%s">' % rid)
        end = s.index('</control>', seg)
        assert old in s[seg:end], (rid, old)
        s = s[:seg] + s[seg:end].replace(old, new, 1) + s[end:]
    io.open(SET, 'w', encoding='utf-8', newline='\n').write(s)
h = io.open(HELP, encoding='utf-8').read()
if 'Control.HasFocus(9579)' not in h:
    a = '\t\t<value condition="Control.HasFocus(9549)">$ADDON[skin.aeon.fuse 32449]</value>\n'
    assert a in h
    h = h.replace(a, a + '\t\t<value condition="Control.HasFocus(9579)">$ADDON[skin.aeon.fuse 32569]</value>\n')
    io.open(HELP, 'w', encoding='utf-8', newline='\n').write(h)
root = ET.parse(SET).getroot()
for i in ('9549', '9579', '9540'):
    b = [c for c in root.iter('control') if c.get('id') == i]
    assert len(b) == 1, (i, len(b))
    b = b[0]
    print(i, 'up', [x.text for x in b.findall('onup')], 'down', [x.text for x in b.findall('ondown')],
          'left', [x.text for x in b.findall('onleft')], 'click', [x.text for x in b.findall('onclick')])
