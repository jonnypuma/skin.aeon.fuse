# -*- coding: utf-8 -*-
"""0.56.6 Fused Glass information screen: the buttons of the More row (More by this director, My rating, Versions ...,
grouplist 9100) look like Play / Trailer / More (the user, 2026-11-16: "the buttons when pressing More ... need to be
the same style as the Play, Trailer and More button").
Play / Trailer / More (VidInfo_Button): a 56 px pill, white when focused (AG_Accent) with the gold ring 5 px round it
(AG_PillHalo, ring fg_mark) and zoomed to 105 %, a line pill (AG_Line2) otherwise, bold 22 text. The More row's buttons
size to their words in a grouplist, where no separate halo can follow a button, so the ring is in the button's own
focus picture: fg/btn56f.png (white pill + gold ring, 122 x 66 with the 5 px ring margin) and fg/btn56n.png (the line
pill with the same margin, so a button keeps its size), border 33. The grouplist is 66 tall (11 up) in Fused Glass.
Aeon and Glass keep their look. Run from the skin folder; safe to run again."""
import io
import os

from PIL import Image

INFO = os.path.join('1080i', 'Includes_VideoInfo.xml')
GOLD = (0xe8, 0xb0, 0x4b)
OLD = ('\t\t\t\t<include>VidView_PillLook</include>\n\t\t\t\t<height>44</height>\n\t\t\t\t<font>lb_ui_22_semibold</font>\n'
       '\t\t\t\t<include>Aeon_T_7d6586af</include>\n\t\t\t\t<include>Aeon_T_e6a0379c</include>\n')
NEW = ('\t\t\t\t<include condition="Skin.HasSetting(aeon.fglass)">VidInfo_MoreLook_fg</include>\n'
       '\t\t\t\t<include condition="!Skin.HasSetting(aeon.fglass)">VidInfo_MoreLook_aeon</include>\n')
LOOKS = ('\t<!-- 0.56.6 the More row\'s buttons: like Play / Trailer / More in Fused Glass (_src/fg_morebuttons.py) -->\n'
         '\t<include name="VidInfo_MoreLook_fg">\n'
         '\t\t<width>auto</width>\n\t\t<height>66</height>\n\t\t<font>lb_ui_22_bold</font>\n'
         '\t\t<textcolor>$VAR[AG_Ink]</textcolor>\n\t\t<focusedcolor>$VAR[AG_OnAccent]</focusedcolor>\n\t\t<textoffsetx>33</textoffsetx>\n'
         '\t\t<texturefocus border="33,0,33,0" colordiffuse="ffffffff">fg/btn56f.png</texturefocus>\n'
         '\t\t<texturenofocus border="33,0,33,0" colordiffuse="$VAR[AG_Line2]">fg/btn56n.png</texturenofocus>\n'
         '\t\t<animation type="Focus" condition="!$EXP[ReduceMotion]"><effect type="zoom" start="100" end="105" center="auto" time="150" tween="cubic" easing="out"/></animation>\n'
         '\t\t<animation type="Unfocus" condition="!$EXP[ReduceMotion]"><effect type="zoom" start="105" end="100" center="auto" time="150" tween="cubic" easing="out"/></animation>\n'
         '\t</include>\n'
         '\t<include name="VidInfo_MoreLook_aeon">\n'
         '\t\t<include>VidView_PillLook</include>\n\t\t<height>44</height>\n\t\t<font>lb_ui_22_semibold</font>\n'
         '\t\t<include>Aeon_T_7d6586af</include>\n\t\t<include>Aeon_T_e6a0379c</include>\n'
         '\t</include>\n'
         '\t<include name="VidInfo_MoreRowBox_fg"><top>789</top><height>66</height></include>\n'
         '\t<include name="VidInfo_MoreRowBox_aeon"><top>800</top><height>44</height></include>\n')


def textures():
    pill = Image.open(os.path.join('media', 'aeon', 'pill_56.png')).convert('RGBA')
    line = Image.open(os.path.join('media', 'aeon', 'pill_56_line.png')).convert('RGBA')
    ring = Image.open(os.path.join('media', 'aeon', 'pill_56_ring.png')).convert('RGBA')
    assert pill.size == (112, 56) and ring.size == (122, 66)
    f = Image.new('RGBA', (122, 66), (255, 255, 255, 0))
    gold = Image.new('RGBA', ring.size, GOLD + (0,))
    gold.putalpha(ring.getchannel('A'))
    f.alpha_composite(gold)
    white = Image.new('RGBA', pill.size, (255, 255, 255, 0))
    white.putalpha(pill.getchannel('A'))
    f.alpha_composite(white, (5, 5))
    f.save(os.path.join('media', 'fg', 'btn56f.png'), optimize=True)
    n = Image.new('RGBA', (122, 66), (255, 255, 255, 0))
    n.alpha_composite(line, (5, 5))
    n.save(os.path.join('media', 'fg', 'btn56n.png'), optimize=True)
    print('fg/btn56f.png, fg/btn56n.png')


def info():
    t = io.open(INFO, encoding='utf-8').read()
    if 'VidInfo_MoreLook_fg' in t:
        print('More row already done')
        return
    assert t.count(OLD) == 1, 'VidInfo_MoreButton'
    t = t.replace(OLD, NEW)
    old_box = ('<control type="grouplist" id="9100">\n\t\t\t<left>160</left>\n\t\t\t<top>800</top>\n\t\t\t<width>1600</width>\n\t\t\t<height>44</height>\n')
    assert t.count(old_box) == 1, 'grouplist 9100'
    t = t.replace(old_box, '<control type="grouplist" id="9100">\n\t\t\t<left>160</left>\n'
                          '\t\t\t<include condition="Skin.HasSetting(aeon.fglass)">VidInfo_MoreRowBox_fg</include>\n'
                          '\t\t\t<include condition="!Skin.HasSetting(aeon.fglass)">VidInfo_MoreRowBox_aeon</include>\n'
                          '\t\t\t<width>1600</width>\n')
    a = t.find('\t<include name="VidInfo_MoreButton">')
    t = t[:a] + LOOKS + t[a:]
    io.open(INFO, 'w', encoding='utf-8', newline='\n').write(t)
    print('More row: buttons like Play / Trailer / More in Fused Glass')


if __name__ == '__main__':
    textures()
    info()
