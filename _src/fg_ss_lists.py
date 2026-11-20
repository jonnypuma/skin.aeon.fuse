"""0.45.1: the screensaver's new slides (screensaver.aeon.fuse 1.2.0) - In cinemas now, Airing today, Airing tomorrow.

- a small label over the title says which list it is ("AIRING TODAY - NETFLIX"), in the accent colour on Fused Glass
- the credits line shows the helper's aeon.ss.line1 ("S3 E5 - Title", an album's artist) when there is one
- the ULTRA HD tag is left out on these slides (it would sit on the label)
- the pager shows as many dots as the list has items (a day may have only two or three)
Run from the skin folder; runs once."""
import io
import re
import xml.etree.ElementTree as ET

WIN = '1080i/Custom_1156_Screensaver.xml'
SUB = '1080i/Includes_Aeon_Sub.xml'
KIND = 'Window(Home).Property(aeon.ss.kind)'
LISTS = '[String.IsEqual(%s,cinema) | String.IsEqual(%s,today) | String.IsEqual(%s,tomorrow)]' % (KIND, KIND, KIND)
LINE2 = '$INFO[Container(9701).ListItem.Property(aeon.ss.line2), · ,]'

s = io.open(SUB, encoding='utf-8').read()
if 'Aeon_SSKindWord' not in s:
    a = '\t<variable name="Aeon_SSCredit">\n'
    assert s.count(a) == 1
    s = s.replace(a, '''	<!-- the screensaver's helper lists (0.45.1): which list a slide comes from -->
	<variable name="Aeon_SSKindWord">
		<value condition="String.IsEqual(%(k)s,cinema)">$ADDON[skin.aeon.fuse 32556]</value>
		<value condition="String.IsEqual(%(k)s,today)">$ADDON[skin.aeon.fuse 32557]%(l2)s</value>
		<value condition="String.IsEqual(%(k)s,tomorrow)">$ADDON[skin.aeon.fuse 32558]%(l2)s</value>
	</variable>
''' % {'k': KIND, 'l2': LINE2} + a + '''		<value condition="!String.IsEmpty(Container(9701).ListItem.Property(aeon.ss.line1))">$INFO[Container(9701).ListItem.Property(aeon.ss.line1)]</value>
''', 1)
    io.open(SUB, 'w', encoding='utf-8', newline='\n').write(s)

w = io.open(WIN, encoding='utf-8').read()
if 'Aeon_SSKindWord' not in w:
    # the ULTRA HD tag: not on the list slides
    tag = '<visible>String.IsEqual(Container(9701).ListItem.VideoResolution,4K) | String.IsEqual(Container(9701).ListItem.VideoResolution,2160)</visible>'
    assert w.count(tag) == 2, w.count(tag)
    w = w.replace(tag, '<visible>[String.IsEqual(Container(9701).ListItem.VideoResolution,4K) | String.IsEqual(Container(9701).ListItem.VideoResolution,2160)] + !%s</visible>' % LISTS)
    # the list's label, above the title (where the ULTRA HD tag sits on the other slides)
    at = '\t\t\t<!-- ULTRA HD tag -->\n'
    assert w.count(at) == 1
    label = ('\t\t\t<!-- which list (0.45.1): In cinemas now / Airing today / Airing tomorrow, with the network -->\n'
             '\t\t\t<control type="label"><left>1000</left><top>426</top><width>820</width><height>32</height><align>right</align><aligny>center</aligny>'
             '<font>cap_20</font><textcolor>%s</textcolor><label>[UPPERCASE]$VAR[Aeon_SSKindWord][/UPPERCASE]</label><visible>%s + %s</visible></control>\n')
    w = w.replace(at, label % ('fg_mark', LISTS, 'Skin.HasSetting(aeon.fglass)') + label % ('ccffffff', LISTS, '!Skin.HasSetting(aeon.fglass)') + at, 1)
    # pager: a dot / ring only for the items there are
    count = [0]

    def dots(m):
        line = m.group(0)
        if not re.search(r'aeon_ring\.png|aeon_dot\.png|fg/circle\.png|fg/bar\.png', line):
            return line
        k = re.search(r'Integer\.IsEqual\(Container\(9701\)\.CurrentItem,(\d+)\)', line).group(1)
        count[0] += 1
        return re.sub(r'</visible>', ' + Integer.IsGreaterOrEqual(Container(9701).NumItems,%s)</visible>' % k, line, count=1)
    w = re.sub(r'[^\n]*Integer\.IsEqual\(Container\(9701\)\.CurrentItem,\d+\)[^\n]*', dots, w)
    print('pager dots', count[0])
    io.open(WIN, 'w', encoding='utf-8', newline='\n').write(w)
for name in (WIN, SUB):
    ET.parse(name)
print('ok')
