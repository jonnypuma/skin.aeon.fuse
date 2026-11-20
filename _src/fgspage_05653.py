# -*- coding: utf-8 -*-
"""0.56.53 Kodi's settings pages (SettingsCategory: Player, Media, Interface, System, ...) in Fused Glass style, on the
one page spec of the Skin settings window (user, 2026-11-20: "the only thing that's consistent about this skin is how
inconsistent everything is"; standard menus need the gutter, a scroll bar you can reach, the focus bar's dark fill).

The style used SetCat_Classic (the Aeon page) bent by slides and zooms: frame from 100, no title band, the bar inside
the list. It now has FGS_SettingsPage:
- frame 120-1820 x 108-960, title band 108-191 (CATEGORIES | the section, rule at 191), columns split by one line
  (480), the scroll bar gutter 1800-1820 between two lines;
- categories 121-480 as 70 rows from 191, Expert (the level button) the last row, 890-960;
- the settings 481-1800 as 70 rows from 191, ten and a bit in view; Right from a row without values of its own
  reaches the bar 60 (square, in the gutter; accent on focus), Left back;
- the description under the frame, at the list's text column.
The bar textures with the shadow's dark fill baked in (fg/fgs_bar_dk.png): Kodi clones these rows from templates, so
they cannot carry the shadow image the skin's own rows have; FGS_RowTex, FGS_CatTex and the sub-nav cells use it.
Repeatable."""
import io
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', '1080i')
MEDIA = os.path.join(HERE, '..', 'media', 'fg')
L, R, T, B, BAND, ROW, COL, GUT = 120, 1820, 108, 960, 191, 70, 480, 20


def rule(x, y, w, h):
    return ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
            '<texture colordiffuse="$VAR[FGS_FrameCol]">common/white.png</texture></control>' % (x, y, w, h))


def page(addon=False):
    """addon: Add-on settings - the list 481-1499, the gutter 1500-1520, OK / Cancel / Defaults 1521-1820 (as Skin
    settings' right column)"""
    RC = 1500                                   # add-on settings: the list ends where Skin settings' rows end
    end = RC if addon else R - GUT
    lw = end - COL - 1
    out = ['<!-- 0.56.53 fgspage: the Skin settings page spec -->']
    out += [rule(L, T, R - L + 1, 1), rule(L, B, R - L + 1, 1), rule(L + 1, BAND, R - L - 1, 1)]
    out += [rule(x, T, 1, B - T) for x in ((L, COL, RC, RC + GUT, R) if addon else (L, COL, R - GUT, R))]
    if addon:
        out.append(rule(RC + 1, BAND, GUT - 1, 1))
    out.append('<control type="label"><left>%d</left><top>120</top><width>320</width><height>60</height><aligny>center</aligny>'
               '<font>st_ui_30_semibold</font><textcolor>$VAR[AG_Ink]</textcolor><label>[UPPERCASE]$LOCALIZE[31847][/UPPERCASE]</label></control>' % (L + 24))
    out.append('<control type="label"><left>%d</left><top>120</top><width>%d</width><height>60</height><aligny>center</aligny>'
               '<font>st_ui_30_semibold</font><textcolor>$VAR[AG_Ink]</textcolor><label>[UPPERCASE]$INFO[Control.GetLabel(2)][/UPPERCASE]</label></control>'
               % (COL + 25, lw - 48))
    out.append('<control type="grouplist" id="3"><description>categories (Kodi clones template 10 into it)</description>'
               '<left>%d</left><top>%d</top><width>%d</width><height>%d</height><orientation>vertical</orientation>'
               '<onleft>noop</onleft><onright>5</onright><onup>20</onup><ondown>20</ondown></control>'
               % (L + 1, BAND, COL - L - 1, ROW * 9))
    out.append('<include content="Aeon_SettingCategoryTemplate"><param name="width" value="%d"/><param name="roundfirst" value="true"/>'
               '<param name="fgs" value="true"/></include>' % (COL - L - 1))
    out.append('<control type="group"><left>%d</left><top>%d</top><include content="AG_SettingLevelButton">'
               '<param name="width" value="%d"/><param name="onleft" value="noop"/><param name="height" value="70"/>'
               '<param name="round" value="true"/></include></control>' % (L + 1, B - ROW, COL - L - 1))
    out.append('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>1</height>'
               '<texture colordiffuse="$VAR[FGS_FrameCol]">common/white.png</texture></control>' % (L + 1, B - ROW, COL - L - 1))
    out.append('<control type="grouplist" id="5"><description>control area</description><left>%d</left><top>%d</top>'
               '<width>%d</width><height>%d</height><pagecontrol>60</pagecontrol><onleft>3</onleft><onright>60</onright>'
               '<onup>5</onup><ondown>5</ondown></control>' % (COL + 1, BAND, lw, B - BAND - 1))
    out.append('<control type="scrollbar" id="61"><left>-200</left><top>0</top><width>4</width><height>100</height><visible>false</visible></control>')
    out.append('<include content="Aeon_SettingTemplates"><param name="width" value="%d"/><param name="fgs" value="true"/>'
               '<param name="pre" value="FGS_"/><param name="fgswidth" value="%d"/></include>' % (lw, lw))
    out.append('<control type="scrollbar" id="60"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
               '<include>FGS_SBTex</include><textureslidernib /><textureslidernibfocus /><orientation>vertical</orientation>'
               '<showonepage>false</showonepage><onleft>5</onleft><onright>%s</onright><onup>60</onup><ondown>60</ondown></control>'
               % (end + 1, BAND + 1, GUT - 1, B - BAND - 1, '9000' if addon else 'noop'))
    if addon:
        btn = ('<control type="button" id="%s"><width>%d</width><height>70</height><font>uc_st_ui_24_semibold</font>'
               '<textcolor>ccffffff</textcolor><focusedcolor>$VAR[FGS_Aeon_OnBarInk]</focusedcolor><disabledcolor>44ffffff</disabledcolor>'
               '<textoffsetx>24</textoffsetx><aligny>center</aligny><pulseonselect>false</pulseonselect>'
               '<texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texturefocus>'
               '<texturenofocus border="0,2,0,0" colordiffuse="12ffffff">fg/fgs_rule_top.png</texturenofocus></control>')
        out.append('<control type="grouplist" id="9000"><left>%d</left><top>%d</top><width>%d</width><height>210</height>'
                   '<orientation>vertical</orientation><itemgap>0</itemgap><onleft>60</onleft><onright>noop</onright>'
                   '<onup>9000</onup><ondown>9000</ondown>%s</control>'
                   % (RC + GUT + 1, BAND, R - RC - GUT - 1, ''.join(btn % (i, R - RC - GUT - 1) for i in (28, 29, 30))))
    out.append('<control type="textbox" id="6"><description>description (Kodi)</description><left>%d</left><top>975</top>'
               '<width>%d</width><height>90</height><font>st_small_20</font><textcolor>99ffffff</textcolor>'
               '<autoscroll time="3000" delay="6000" repeat="6000">true</autoscroll></control>' % (COL + 25, lw - 48))
    return '\n\t\t'.join(out)


def dark_bar():
    """fgs_bar.png with the shadow's dark fill inside (sh16's middle at FG_ShadowColM: about 34 % black)"""
    src = Image.open(os.path.join(MEDIA, 'fgs_bar.png')).convert('RGBA')
    fill = Image.new('RGBA', src.size, (0, 0, 0, 87))
    Image.alpha_composite(fill, src).save(os.path.join(MEDIA, 'fgs_bar_dk.png'))


def main():
    dark_bar()
    p = os.path.join(D, 'Includes_Fused.xml')
    t = io.open(p, encoding='utf-8').read()
    for name, addon in (('FGS_SettingsPage', False), ('FGS_AddonSettingsPage', True)):
        body = '\t<include name="%s">\n\t\t%s\n\t</include>\n\t<!-- end %s -->\n' % (name, page(addon), name)
        if '<include name="%s">' % name in t:
            i = t.index('\t<include name="%s">' % name)
            j = t.index('<!-- end %s -->' % name, i) + len('<!-- end %s -->\n' % name)
            t = t[:i] + body + t[j:]
        else:
            k = t.index('\t<include name="FGS_RowTex">')
            t = t[:k] + body + t[k:]
    for a, b in (('<texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar.png</texturefocus>\n\t\t<texturenofocus border="0,2,0,0" colordiffuse="12ffffff">fg/fgs_rule_top.png</texturenofocus>',
                  '<texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texturefocus>\n\t\t<texturenofocus border="0,2,0,0" colordiffuse="12ffffff">fg/fgs_rule_top.png</texturenofocus>'),
                 ('<texturefocus border="20" colordiffuse="$VAR[FGS_CatBarCol]">fg/fgs_bar.png</texturefocus>',
                  '<texturefocus border="20" colordiffuse="$VAR[FGS_CatBarCol]">fg/fgs_bar_dk.png</texturefocus>')):
        t = t.replace(a, b)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    c = io.open(os.path.join(D, 'Includes_Common.xml'), encoding='utf-8').read()
    i = c.index('<include name="FGS_SubNavLook">')
    e = c.index('</include>', i)
    c = c[:i] + c[i:e].replace('fg/fgs_bar.png</texturefocus>', 'fg/fgs_bar_dk.png</texturefocus>') + c[e:]
    io.open(os.path.join(D, 'Includes_Common.xml'), 'w', encoding='utf-8', newline='\n').write(c)
    w = os.path.join(D, 'SettingsCategory.xml')
    s = io.open(w, encoding='utf-8').read()
    old = '<include condition="[!Skin.HasSetting(aeon.fglass) + !$EXP[Aeon_MS]] | $EXP[FGS]">SetCat_Classic</include>'
    if old in s:
        s = s.replace(old, '<include condition="!Skin.HasSetting(aeon.fglass) + !$EXP[Aeon_MS]">SetCat_Classic</include>'
                           '<include condition="$EXP[FGS]">FGS_SettingsPage</include><!-- 0.56.53 fgspage -->', 1)
        io.open(w, 'w', encoding='utf-8', newline='\n').write(s)
    w = os.path.join(D, 'DialogAddonSettings.xml')
    s = io.open(w, encoding='utf-8').read()
    old = '<include condition="[!Skin.HasSetting(aeon.fglass) + !$EXP[Aeon_MS]] | $EXP[FGS]">AddonSet_Classic</include>'
    if old in s:
        s = s.replace(old, '<include condition="!Skin.HasSetting(aeon.fglass) + !$EXP[Aeon_MS]">AddonSet_Classic</include>'
                           '<include condition="$EXP[FGS]">FGS_AddonSettingsPage</include><!-- 0.56.53 fgspage -->', 1)
        io.open(w, 'w', encoding='utf-8', newline='\n').write(s)
    print('Kodi settings + add-on settings pages (style) written')


if __name__ == '__main__':
    main()
