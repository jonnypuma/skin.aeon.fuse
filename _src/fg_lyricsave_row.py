"""0.45.1 Skin settings > Player: "Save lyrics next to the song" (row 9567, under Cinema mode 9539 at 891), a copy of the
switch row "Lyrics take focus" (9535). The switch shows Skin.HasSetting(aeon.lyrics.save); OK / left / right run
RunScript(script.aeon.helper,lyricsave), which turns CU LRC Lyrics' save_lyrics2_lrc / _txt on or off and the setting
with it (the helper also matches the setting to the lyrics add-on at start-up). Run from the skin folder; runs once."""
import io
import xml.etree.ElementTree as ET

SET = '1080i/SkinSettings.xml'
HELP = '1080i/Includes_Settings.xml'
s = io.open(SET, encoding='utf-8').read()
if 'aeon.lyrics.save' not in s:
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

    bar_at = next(k for k, l in enumerate(lines) if l.strip() == '<visible>Control.HasFocus(9535)</visible>')
    b0, b1 = block(bar_at)
    r0, r1 = block(next(k for k, l in enumerate(lines) if '<control type="button" id="9535">' in l))
    bar = '\n'.join(lines[b0:b1 + 1]).replace('<top>541</top>', '<top>891</top>').replace('9535', '9567')
    row = '\n'.join(lines[r0:r1 + 1]).replace('<top>541</top>', '<top>891</top>', 1)
    assert row.count('Skin.ToggleSetting(aeon.lyrics.focus)') == 3, row.count('Skin.ToggleSetting(aeon.lyrics.focus)')
    row = row.replace('Skin.ToggleSetting(aeon.lyrics.focus)', 'RunScript(script.aeon.helper,lyricsave)')
    row = row.replace('aeon.lyrics.focus', 'aeon.lyrics.save').replace('9535', '9567')
    row = row.replace('<param name="label" value="$LOCALIZE[31814]"/>', '<param name="label" value="$ADDON[skin.aeon.fuse 32559]"/>')
    row = row.replace('<param name="icon" value="aeon/icons/lines.png"/>', '<param name="icon" value="aeon/icons/music.png"/>')
    assert '<onup>9534</onup>' in row and '<ondown>9536</ondown>' in row
    row = row.replace('<onup>9534</onup>', '<onup>9539</onup>').replace('<ondown>9536</ondown>', '<ondown>9550</ondown>')
    assert '32559' in row and 'music.png' in row
    # after the Cinema mode row (9539), the last of the Player category
    k = next(i for i, l in enumerate(lines) if '<control type="button" id="9539">' in l)
    _e0, e1 = block(k)
    lines[e1 + 1:e1 + 1] = [bar, row]
    s = '\n'.join(lines)
    # chain: 9539 down -> 9567, 9550 up -> 9567
    seg = s.index('<control type="button" id="9539">')
    end = s.index('</control>', s.index('<ondown>9550</ondown>', seg))
    s = s[:seg] + s[seg:end].replace('<ondown>9550</ondown>', '<ondown>9567</ondown>', 1) + s[end:]
    seg = s.index('<control type="button" id="9550">')
    end = s.index('</control>', s.index('<onup>9539</onup>', seg))
    s = s[:seg] + s[seg:end].replace('<onup>9539</onup>', '<onup>9567</onup>', 1) + s[end:]
    io.open(SET, 'w', encoding='utf-8', newline='\n').write(s)
h = io.open(HELP, encoding='utf-8').read()
if 'Control.HasFocus(9567)' not in h:
    a = '\t\t<value condition="Control.HasFocus(9539)">$LOCALIZE[31930]</value>\n'
    assert a in h
    h = h.replace(a, a + '\t\t<value condition="Control.HasFocus(9567)">$ADDON[skin.aeon.fuse 32560]</value>\n')
    io.open(HELP, 'w', encoding='utf-8', newline='\n').write(h)
root = ET.parse(SET).getroot()
for i in ('9539', '9567', '9550'):
    b = [c for c in root.iter('control') if c.get('id') == i][0]
    print(i, 'up', [x.text for x in b.findall('onup')], 'down', [x.text for x in b.findall('ondown')],
          'click', [x.text for x in b.findall('onclick')])
ET.parse(HELP)
print('ok')
