# -*- coding: utf-8 -*-
"""0.46.0 Fused Glass Home: an episode in focus in a strip (TV shows' Recent episodes, Recently played ...: strip 9302;
movies' strip 9301 too, for custom lists) shows its thumb under the show's logo, as the Favourites spotlight does
(232 x 130, frosted frame, yellow line for how far it was watched); the line, chips, ratings and plot under it move
down 140. Run from the skin folder; safe to run again."""
import io
import os
import re
import xml.etree.ElementTree as ET

HOME = os.path.join('1080i', 'Includes_Aeon_Home.xml')
FUSED = os.path.join('1080i', 'Includes_Fused.xml')
STRIPS = (('9302', 'tv'), ('9301', 'movies'))


def exp(cid):
    return ('$EXP[Aeon_FGlass] + String.IsEqual(Container(%s).ListItem.DBType,episode) + !String.IsEmpty(Container(%s).ListItem.Art(thumb))'
            % (cid, cid))


f = io.open(FUSED, encoding='utf-8').read()
f = re.sub(r'\t<!-- FG_STRIPEP:begin.*?<!-- FG_STRIPEP:end -->\n', '', f, flags=re.S)
f = f.replace('</includes>', '\t<!-- FG_STRIPEP:begin (written by _src/fg_stripep.py) ===== an episode in a Home strip shows its thumb (0.46.0) -->\n'
              + ''.join('\t<expression name="FG_StripEp%s">%s</expression>\n' % (cid, exp(cid)) for cid, _ in STRIPS)
              + '\t<!-- FG_STRIPEP:end -->\n</includes>')
io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(f)

h = io.open(HOME, encoding='utf-8').read()
for cid, name in STRIPS:
    if 'FG_StripEp%s]' % cid in h:
        continue
    start = h.index('<!-- info of the focused strip item (%s) -->' % name)
    end = h.index('<!-- info of the focused strip item', start + 10) if '<!-- info of the focused strip item' in h[start + 10:] else len(h)
    part = h[start:end]
    inner = '\t\t\t<control type="group">\n\t\t\t\t<visible>true</visible>\n'
    assert part.count(inner) == 1, (name, part.count(inner))
    slide = '\t\t\t\t<animation effect="slide" end="0,140" time="0" condition="$EXP[FG_StripEp%s]">Conditional</animation>\n' % cid
    thumb = ('\t\t\t<!-- 0.46.0: an episode: its thumb under the logo (Fused Glass) -->\n'
             '\t\t\t<control type="group">\n\t\t\t\t<visible>$EXP[FG_StripEp%(c)s]</visible>\n'
             '\t\t\t\t<control type="image"><left>120</left><top>262</top><width>232</width><height>130</height><texture border="12" colordiffuse="$VAR[FG_Frost]">fg/r12.png</texture></control>\n'
             '\t\t\t\t<control type="image"><left>120</left><top>262</top><width>232</width><height>130</height><aspectratio scalediffuse="false">scale</aspectratio><fadetime>200</fadetime>'
             '<texture background="true" diffuse="fg/m232x130.png">$INFO[Container(%(c)s).ListItem.Art(thumb)]</texture></control>\n'
             '\t\t\t\t<control type="image"><left>120</left><top>262</top><width>232</width><height>130</height><texture border="12" colordiffuse="$VAR[FG_Edge]">fg/e12.png</texture></control>\n'
             '\t\t\t\t<control type="progress"><left>132</left><top>380</top><width>208</width><height>4</height><texturebg border="2" colordiffuse="4d000000">fg/pill4.png</texturebg>'
             '<midtexture border="2" colordiffuse="fg_mark">fg/pill4.png</midtexture><info>Container(%(c)s).ListItem.PercentPlayed</info>'
             '<visible>Integer.IsGreater(Container(%(c)s).ListItem.PercentPlayed,0)</visible></control>\n'
             '\t\t\t</control>\n' % {'c': cid})
    new = part.replace(inner, thumb + inner + slide, 1)
    # the plot textbox of this strip moves too
    plot = re.search(r'\t\t\t<control type="textbox"><left>120</left><top>404</top>[^\n]*\n', new)
    assert plot, name
    line = plot.group(0)
    new = new.replace(line, line.replace('<control type="textbox">', '<control type="textbox"><animation effect="slide" end="0,140" time="0" condition="$EXP[FG_StripEp%s]">Conditional</animation>' % cid, 1), 1)
    h = h[:start] + new + h[end:]
io.open(HOME, 'w', encoding='utf-8', newline='\n').write(h)
for name in (HOME, FUSED):
    ET.parse(name)
print('ok')
