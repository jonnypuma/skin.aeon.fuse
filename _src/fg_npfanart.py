"""0.46.0 Now playing: no neutral gap between the artist's fanarts. The cycling picture (Aeon_NP_Fanart, a new one every
16 s) showed nothing while the next fanart was still downloading. Now the main fanart lies under it (same zoom and
drift) and the four others are loaded ahead by tiny images off screen, so they are in Kodi's cache when their turn
comes. Both layers are drawn darkened but opaque (ffb0b0b0 on the black page = the old b0ffffff), so they do not blend."""
import io
import xml.etree.ElementTree as ET

P = r'C:\Users\gideo\AppData\Roaming\Kodi\addons\skin.aeon.fuse\1080i\Includes_Aeon_Music.xml'
t = io.open(P, encoding='utf-8').read()
if 'Aeon_NP_FanartBase' not in t:
    var = ('\t<!-- 0.46.0: the main fanart under the cycling one (Aeon_NowPlaying), shown while the next picture loads -->\n'
           '\t<variable name="Aeon_NP_FanartBase">\n'
           '\t\t<value condition="!String.IsEmpty(Player.Art(fanart))">$INFO[Player.Art(fanart)]</value>\n'
           '\t\t<value condition="!String.IsEmpty(Player.Art(artist.fanart))">$INFO[Player.Art(artist.fanart)]</value>\n'
           '\t\t<value>$INFO[Player.Art(thumb)]</value>\n\t</variable>\n')
    a = '\t<variable name="Aeon_NP_Disc">\n'
    assert t.count(a) == 1
    t = t.replace(a, var + a, 1)
    s = t.index('\t<include name="Aeon_NowPlaying">')
    old_start = t.index('\t\t<control type="image">', s)
    old_end = t.index('\t\t</control>\n', old_start) + len('\t\t</control>\n')
    cycling = t[old_start:old_end]
    assert '$VAR[Aeon_NP_Fanart]' in cycling and 'colordiffuse="b0ffffff"' in cycling
    base = (cycling.replace('$VAR[Aeon_NP_Fanart]', '$VAR[Aeon_NP_FanartBase]').replace('colordiffuse="b0ffffff"', 'colordiffuse="ffb0b0b0"')
            .replace('<fadetime>1500</fadetime>', '<fadetime>600</fadetime>'))
    cycling = cycling.replace('colordiffuse="b0ffffff"', 'colordiffuse="ffb0b0b0"')
    pre = ''.join('\t\t<control type="image"><left>-40</left><top>0</top><width>1</width><height>1</height><texture background="true">$INFO[Player.Art(%s%d)]</texture></control>\n'
                  % (kind, k) for k in range(1, 5) for kind in ('artist.fanart', 'fanart'))
    t = (t[:old_start] + '\t\t<!-- 0.46.0: the main fanart under the cycling one, and the artist\'s other fanarts loaded ahead (1 px under the opaque layers) -->\n'
         + pre + base + cycling + t[old_end:])
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
ET.parse(P)
print('ok')
