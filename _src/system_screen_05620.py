# -*- coding: utf-8 -*-
"""0.56.20: the Kodi System screen (Custom_1151_SystemMenu.xml) looks the same in every theme as in Fused Glass (the
user, 2026-11-17: "i want all themes to use the Fused Glass Kodi System Settings screen ... It just looks nice on all of
them"). The window was already one design; Aeon drew it on the flat ground, the glass themes on the fanart backdrop
(AG_Background adds Aeon_Backdrop only with Aeon Glass / Fused Glass). Now the backdrop is under it in every theme
(Skin settings > Fanart backdrop still switches it off).

The rows get a landing animation (the user: "there is no navigation animation on that menu though, which should follow
the user settings (default is pop)"): Aeon_LandFocusAll, Fused Glass's landing animations (Skin.String(aeon.fganim): pop
by default, grow, fade, nudge, lift) as Focus animations of the focused row's bar, in every theme; Reduce motion stops
them. Aeon_MenuRow is shared, so the Settings hub and the other screens built from it move the same way. Runs once."""
import io
import os
import re
import xml.etree.ElementTree as ET

MARK = '0.56.20 system_screen'
FUSED = os.path.join('1080i', 'Includes_Fused.xml')
MENU = os.path.join('1080i', 'Includes_Aeon_Menu.xml')
SYS = os.path.join('1080i', 'Custom_1151_SystemMenu.xml')


def main():
    f = io.open(FUSED, encoding='utf-8').read()
    if MARK in f:
        print('already')
        return
    a = f.index('\t<include name="FG_LandVisible">')
    b = f.index('\t</include>', a) + len('\t</include>')
    land = f[a:b]
    anims = re.findall(r'<animation type="Visible" condition="\$EXP\[Aeon_FGlass\] \+ (\$EXP\[FG_Anim\w+\])">(.*?)</animation>', land)
    assert len(anims) == 5, len(anims)
    inc = '\n\t<!-- %s: Fused Glass\'s landing animations on a focused list row, every theme -->\n\t<include name="Aeon_LandFocusAll">\n' % MARK
    for cond, eff in anims:
        inc += '\t\t<animation type="Focus" condition="%s + !Skin.HasSetting(aeon.reducemotion)">%s</animation>\n' % (cond, eff)
    inc += '\t</include>'
    f = f[:b] + inc + f[b:]
    io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(f)
    ET.parse(FUSED)
    m = io.open(MENU, encoding='utf-8').read()
    old = ('\t\t\t<control type="group">\n\t\t\t\t<visible>$PARAM[focused] + Control.HasFocus($PARAM[id])</visible>\n'
           '\t\t\t\t<animation effect="fade" start="0" end="100" time="200">Visible</animation>\n')
    assert m.count(old) == 1, m.count(old)
    m = m.replace(old, old + '\t\t\t\t<include>Aeon_LandFocusAll</include><!-- %s -->\n' % MARK)
    io.open(MENU, 'w', encoding='utf-8', newline='\n').write(m)
    ET.parse(MENU)
    s = io.open(SYS, encoding='utf-8').read()
    old = '\t\t\t<include>AG_Background</include>\n\t\t</control>'
    assert s.count(old) == 1
    s = s.replace(old, '\t\t\t<include>AG_Background</include>\n'
                  '\t\t\t<!-- %s: the dark ground and the fanart backdrop in every theme, as in Fused Glass -->\n'
                  '\t\t\t<control type="group"><visible>!Skin.HasSetting(aeon.fglass)</visible><control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture colordiffuse="ff0b0c10">common/white.png</texture></control><include>Aeon_Backdrop</include></control>\n\t\t</control>' % MARK)
    io.open(SYS, 'w', encoding='utf-8', newline='\n').write(s)
    ET.parse(SYS)
    print('ok')


if __name__ == '__main__':
    main()
