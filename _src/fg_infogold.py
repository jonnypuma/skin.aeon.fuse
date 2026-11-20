# -*- coding: utf-8 -*-
"""0.56.3 the information screen's buttons (Resume, From start, Play, Trailer, More: VidInfo_Button) show the gold
accent when focused in Fused Glass: the thin ring round the focused pill (AG_PillHalo) is gold (fg_mark), like the
gold ring round a focused poster in the library walls (the user: "the item play information window should have the
yellow accent when Resume, From start or More button are highlighted"). AG_PillHalo takes the ring colour as a param
(default the grey halo, as before for every other button). Run from the skin folder; safe to run again."""
import io
import os

C = os.path.join('1080i', 'Includes_Common.xml')
V = os.path.join('1080i', 'Includes_VideoInfo.xml')
c = io.open(C, encoding='utf-8').read()
if '<param name="ring">' not in c:
    old = '\t<include name="AG_PillHalo">\n\t\t<param name="h">56</param>\n'
    assert c.count(old) == 1
    c = c.replace(old, old + '\t\t<param name="ring">$VAR[AG_Halo]</param>\n', 1)
    old2 = '<texture border="33,0,33,0" colordiffuse="$VAR[AG_Halo]">aeon/pill_$PARAM[h]_ring.png</texture>'
    assert c.count(old2) == 1
    c = c.replace(old2, '<texture border="33,0,33,0" colordiffuse="$PARAM[ring]">aeon/pill_$PARAM[h]_ring.png</texture>')
    io.open(C, 'w', encoding='utf-8', newline='\n').write(c)
    print('AG_PillHalo: ring colour param')
v = io.open(V, encoding='utf-8').read()
if 'VidInfo_HaloRing' not in v:
    old = '\t\t\t\t<control type="group">\n\t\t\t\t\t<visible>Control.HasFocus($PARAM[id])</visible>\n\t\t\t\t\t<include>AG_PillHalo</include>\n\t\t\t\t</control>'
    assert v.count(old) == 1, v.count(old)
    v = v.replace(old, old.replace('<include>AG_PillHalo</include>',
                                   '<include content="AG_PillHalo"><param name="ring" value="$VAR[VidInfo_HaloRing]"/></include>'))
    a = '\t<include name="VidInfo_Button">'
    v = v.replace(a, '\t<!-- 0.56.3: the gold accent round the focused button in Fused Glass (_src/fg_infogold.py) -->\n'
                     '\t<variable name="VidInfo_HaloRing">\n\t\t<value condition="Skin.HasSetting(aeon.fglass)">fg_mark</value>\n'
                     '\t\t<value>$VAR[AG_Halo]</value>\n\t</variable>\n' + a, 1)
    io.open(V, 'w', encoding='utf-8', newline='\n').write(v)
    print('VidInfo_Button: gold ring in Fused Glass')
