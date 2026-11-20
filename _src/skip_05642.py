# -*- coding: utf-8 -*-
"""0.56.42 the segment skip button on the player controls in Aeon Glass, as in Fused Glass (Tab | Glass).
The user: "Doesn't Aeon glass use the same OSD controls panel as Fused Glass? Any reason why it can't use the same
options?" and "Same as Fused Glass if possible."
Aeon Glass (aeon.vglass without aeon.fglass) uses the Aeon player controls (Includes_Aeon_OSD.xml), where the skip
button (id 88) was switched off for it. Now: Up from the seek bar reaches the button in every theme, and Aeon Glass
draws Fused Glass's Tab or Glass button there (Skin.String(aeon.skippy.cardstyle)). Skin settings > Player > Segment skip
button placement (9739) shows in Aeon Glass too, with its own help line (the small seek bar keeps Aeon Glass's skip box).
Repeatable."""
import io
import os
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import settings_rows as sr  # noqa: E402

D = '1080i'
GLASSY = '[$EXP[Aeon_FGlass] | Skin.HasSetting(aeon.vglass)]'


def rd(name):
    return io.open(os.path.join(D, name), encoding='utf-8').read()


def wr(name, text):
    io.open(os.path.join(D, name), 'w', encoding='utf-8', newline='\n').write(text)
    ET.parse(os.path.join(D, name))


def osd():
    t = rd('Includes_Aeon_OSD.xml')
    old_ask = '[$EXP[Aeon_FGlass] | !Skin.HasSetting(aeon.vglass)] + $EXP[FG_SkipAsk]'
    t = t.replace('<onup condition="%s">SetFocus(88)</onup>' % old_ask, '<onup condition="$EXP[FG_SkipAsk]">SetFocus(88)</onup>')
    t = t.replace('<onup condition="![%s]">Action(Info,fullscreenvideo)</onup>' % old_ask, '<onup condition="!$EXP[FG_SkipAsk]">Action(Info,fullscreenvideo)</onup>')
    t = t.replace('<visible>$EXP[FG_SkipAsk] + [$EXP[Aeon_FGlass] | !Skin.HasSetting(aeon.vglass)]</visible>', '<visible>$EXP[FG_SkipAsk]</visible>')
    t = t.replace('<visible>$EXP[Aeon_FGlass] + !$EXP[FG_SkipGlass]</visible>', '<visible>%s + !$EXP[FG_SkipGlass]</visible>' % GLASSY)
    t = t.replace('<visible>$EXP[Aeon_FGlass] + $EXP[FG_SkipGlass]</visible>', '<visible>%s + $EXP[FG_SkipGlass]</visible>' % GLASSY)
    assert old_ask not in t
    assert t.count('<visible>%s + !$EXP[FG_SkipGlass]</visible>' % GLASSY) == 1, 'tab'
    assert t.count('<visible>%s + $EXP[FG_SkipGlass]</visible>' % GLASSY) == 1, 'glass'
    wr('Includes_Aeon_OSD.xml', t)


def settings():
    t = rd('SkinSettings.xml')
    t = sr.set_item_visible(t, 9739, 'Skin.HasSetting(aeon.vglass) + System.AddonIsEnabled(service.skippy)')
    t = sr.renav(t, 9784)
    wr('SkinSettings.xml', t)
    h = rd('Includes_Settings.xml')
    line = '\t\t<value condition="Control.HasFocus(9739) + !$EXP[Aeon_FGlass]">$ADDON[skin.aeon.fuse 32746]</value>\n'
    if line not in h:
        h = h.replace('\t\t<value condition="Control.HasFocus(9739)">', line + '\t\t<value condition="Control.HasFocus(9739)">', 1)
    assert line in h
    wr('Includes_Settings.xml', h)


if __name__ == '__main__':
    osd()
    settings()
    print('ok')
