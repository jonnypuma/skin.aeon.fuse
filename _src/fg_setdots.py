"""0.39.3 Home spotlight of a movie set (custom Home items): the row of dots sat at its fixed place after the
Play / More information buttons (x 782), but a set shows its films instead of those buttons, so the dots floated in
the middle of the screen. Now they follow the film strip: level with the posters, 28 px after the last one
(strip 9441: left 112, items 96 wide, posters 88). Right past the last film already moves the highlight to them.
More than 12 films: the strip runs to the right edge, the dots keep their old place.
Run in 1080i."""
import io

p = 'Includes_Aeon_Home.xml'
s = io.open(p, encoding='utf-8').read()
assert 'fg_setdots' not in s
anims = ''.join('\t\t\t\t<animation effect="slide" end="%d,-94" time="0" condition="$EXP[Aeon_SetShown] + Integer.IsEqual(Container(9441).NumItems,%d)">Conditional</animation>\n'
                % (n * 96 - 650, n) for n in range(1, 13))
for c in ('custom1', 'custom2', 'custom3'):
    old = '\t\t\t<control type="group"><left>60</left><visible>$EXP[Aeon_SP2Show_%s]</visible>\n' % c
    assert s.count(old) == 1, c
    s = s.replace(old, old + '\t\t\t\t<!-- a set: the dots follow its film strip (0.39.3, _src/fg_setdots.py) -->\n' + anims, 1)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
