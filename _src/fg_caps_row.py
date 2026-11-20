"""0.45.1 Skin settings > Menu names: "Menu names in capitals" (row 9566, Skin setting aeon.hm.caps, Fused Glass), a copy
of the Look category's switch row 9528 placed under 9565 at 611. Run from the skin folder; runs once."""
import io
import xml.etree.ElementTree as ET

SET = '1080i/SkinSettings.xml'
HELP = '1080i/Includes_Settings.xml'
s = io.open(SET, encoding='utf-8').read()
if 'aeon.hm.caps' not in s:
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

    bar_at = next(k for k, l in enumerate(lines) if l.strip() == '<visible>Control.HasFocus(9528) + $EXP[Aeon_FGlass]</visible>')
    b0, b1 = block(bar_at)
    r0, r1 = block(next(k for k, l in enumerate(lines) if '<control type="button" id="9528">' in l))
    bar = '\n'.join(lines[b0:b1 + 1]).replace('<top>821</top>', '<top>611</top>').replace('9528', '9566')
    row = '\n'.join(lines[r0:r1 + 1]).replace('<top>821</top>', '<top>611</top>', 1)
    assert row.count('aeon.toastpill') >= 2
    row = row.replace('aeon.toastpill', 'aeon.hm.caps').replace('9528', '9566')
    row = row.replace('<param name="label" value="$ADDON[skin.aeon.fuse 32474]"/>', '<param name="label" value="$ADDON[skin.aeon.fuse 32554]"/>')
    row = row.replace('<param name="icon" value="aeon/icons/clock.png"/>', '<param name="icon" value="aeon/icons/home.png"/>')
    row = row.replace('<onup>9546</onup>', '<onup>9565</onup>').replace('<ondown>9529</ondown>', '<ondown>9560</ondown>')
    # after the 9565 row of the menu-names category
    k = next(i for i, l in enumerate(lines) if '<control type="button" id="9565">' in l)
    _e0, e1 = block(k)
    lines[e1 + 1:e1 + 1] = [bar, row]
    s = '\n'.join(lines)
    # chain: 9565 down -> 9566, 9560 up -> 9566
    seg = s.index('<control type="button" id="9565">')
    end = s.index('</control>', s.index('<ondown>9560</ondown>', seg))
    s = s[:seg] + s[seg:end].replace('<ondown>9560</ondown>', '<ondown>9566</ondown>', 1) + s[end:]
    seg = s.index('<control type="button" id="9560">')
    end = s.index('</control>', s.index('<onup>9565</onup>', seg))
    s = s[:seg] + s[seg:end].replace('<onup>9565</onup>', '<onup>9566</onup>', 1) + s[end:]
    io.open(SET, 'w', encoding='utf-8', newline='\n').write(s)
h = io.open(HELP, encoding='utf-8').read()
if 'Control.HasFocus(9566)' not in h:
    a = '\t\t<value condition="Control.HasFocus(9529)">$ADDON[skin.aeon.fuse 32551]</value>\n'
    assert a in h
    h = h.replace(a, a + '\t\t<value condition="Control.HasFocus(9566)">$ADDON[skin.aeon.fuse 32555]</value>\n')
    io.open(HELP, 'w', encoding='utf-8', newline='\n').write(h)
root = ET.parse(SET).getroot()
for i in ('9565', '9566', '9560'):
    b = [c for c in root.iter('control') if c.get('id') == i][0]
    print(i, 'up', [x.text for x in b.findall('onup')], 'down', [x.text for x in b.findall('ondown')])
ET.parse(HELP)
print('ok')
