# -*- coding: utf-8 -*-
"""0.56.53 DialogSettings in the Fused Glass style (canvas round 2: SettingsCentred2 "yees! build this" + note "can
upload custom picture"; SettingsPanel2 "yes, build this").

Centred (profile, lock, sources, PVR timer ... ): the page spec (frame 120-1820 x 108-960, title band, 70 px rows from
191, gutter 1500-1520 with bar 60, OK / Cancel / Defaults (28 / 29 / 30) as rows at 1521-1820, the style's setting
templates). Profile settings add the avatar column 121-480: the profile's picture in a circle (Kodi's own Profile
picture row picks any picture, the upload), the name under it; other dialogs give the rows the whole width.
Side panel (OSD audio / subtitles / video): the film stays visible at the left; the panel 1160-1820 on the frame lines,
the three tabs (9101-9103, same actions as today) as cells in the title band, the current one underlined in the
accent, rows 1161-1799, bar 60 in the gutter, the buttons as one row of cells at the foot, the play time at the left.
Not built: the offset ruler (Kodi hands the offset only as text). Repeatable."""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import settings_sections as ss  # noqa: E402
import fgswin_05653 as fw  # noqa: E402

PROFILE = 'Window.IsActive(profilesettings)'


def buttons_rows():
    s = io.open(os.path.join(fw.D, 'Includes_Fused.xml'), encoding='utf-8').read()
    a = s.index('<include name="FGS_AddonSettingsPage">')
    i = s.index('<control type="grouplist" id="9000">', a)
    e = ss.ctl_end(ss.masked(s), i)
    return s[i:e]


def centred():
    def area(x, w):
        return ('<control type="grouplist" id="5"><description>control area</description><left>%d</left><top>191</top><width>%d</width><height>768</height>'
                '<itemgap>0</itemgap><pagecontrol>60</pagecontrol><onleft>noop</onleft><onright>60</onright><onup>5</onup><ondown>5</ondown></control>'
                '<include content="Aeon_SettingTemplates"><param name="width" value="%d"/><param name="fgs" value="true"/><param name="pre" value="FGS_"/><param name="fgswidth" value="%d"/></include>'
                % (x, w, w, w))
    avatar = (
        '<control type="group"><visible>%s</visible>' % PROFILE +
        fw.img(171, 230, 260, 260, 'common/white.png', '14ffffff').replace('<texture colordiffuse', '<texture diffuse="aeon/mask_circle.png" colordiffuse') +
        fw.img(246, 305, 110, 110, 'fg/pw_user.png', '99ffffff', 'String.IsEmpty(System.ProfileThumb)') +
        '<control type="image"><left>171</left><top>230</top><width>260</width><height>260</height><aspectratio scalediffuse="false">scale</aspectratio>'
        '<texture background="true" diffuse="aeon/mask_circle.png">$INFO[System.ProfileThumb]</texture></control>'
        + fw.img(165, 224, 272, 272, 'aeon/ring_cast.png', 'ffffffff') +
        fw.label(121, 520, 359, 50, '$INFO[System.ProfileName]', 'st_ui_30_semibold', 'ffffffff', 'center') +
        '</control>')
    return (
        '<include name="FGS_SettingsCentred">'
        '<include content="FGS_DlgBack"/>'
        '<control type="grouplist"><left>60</left><top>44</top><width>1500</width><height>48</height><orientation>horizontal</orientation><itemgap>14</itemgap><usecontrolcoords>true</usecontrolcoords>'
        '<control type="label"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28</font><textcolor>$VAR[Aeon_MenuLeadCol]</textcolor><label>[UPPERCASE]$LOCALIZE[5][/UPPERCASE]</label></control>'
        '<control type="label" id="2"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28_bold</font><textcolor>ffffffff</textcolor></control>'
        '</control><include>Aeon_ClockBox</include>'
        + fw.line(120, 108, 1701) + fw.line(120, 960, 1701) + fw.line(121, 191, 1699) +
        ''.join(fw.line(x, 108, 1, 852) for x in (120, 1500, 1520, 1820)) +
        fw.line(480, 108, 1, 852).replace('</control>', '<visible>%s</visible></control>' % PROFILE) +
        '<control type="group"><visible>%s</visible>%s</control>' % (PROFILE, fw.label(144, 120, 320, 60, '[UPPERCASE]$LOCALIZE[13200][/UPPERCASE]', 'st_ui_30_semibold', 'ffffffff')) +
        fw.label(505, 120, 971, 60, '[UPPERCASE]$INFO[Control.GetLabel(2)][/UPPERCASE]', 'st_ui_30_semibold', 'ffffffff', vis=PROFILE) +
        fw.label(144, 120, 1332, 60, '[UPPERCASE]$INFO[Control.GetLabel(2)][/UPPERCASE]', 'st_ui_30_semibold', 'ffffffff', vis='!' + PROFILE) +
        avatar +
        '<include condition="%s">FGS_SetArea_Profile</include><include condition="!%s">FGS_SetArea_Wide</include>' % (PROFILE, PROFILE) +
        '<control type="scrollbar" id="60"><left>1501</left><top>192</top><width>19</width><height>768</height><include>FGS_SBTex</include><textureslidernib /><textureslidernibfocus />'
        '<orientation>vertical</orientation><showonepage>false</showonepage><onleft>5</onleft><onright>9000</onright><onup>60</onup><ondown>60</ondown></control>'
        + buttons_rows() +
        '</include>'
        '<include name="FGS_SetArea_Profile">%s</include>'
        '<include name="FGS_SetArea_Wide">%s</include>' % (area(481, 1019), area(121, 1379)))


def tab(i, cid, label, target, current, left, right):
    return ('<control type="group"><left>%d</left><top>109</top><width>253</width><height>82</height>'
            '<control type="button" id="%d"><left>0</left><top>0</top><width>253</width><height>82</height><label>%s</label><font>uc_st_ui_22_bold</font>'
            '<textcolor>8cffffff</textcolor><focusedcolor>ffffffff</focusedcolor><align>center</align><aligny>center</aligny><pulseonselect>false</pulseonselect>'
            '<texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texturefocus><texturenofocus />'
            '<onleft>%s</onleft><onright>%s</onright><onup>noop</onup><ondown>5</ondown>'
            '<onclick condition="!Window.IsActive(%s)">SetProperty(aeon.osdtab,1,home)</onclick>'
            '<onclick condition="!Window.IsActive(%s)">Dialog.Close(osdaudiosettings,true)</onclick>'
            '<onclick condition="!Window.IsActive(%s)">Dialog.Close(osdsubtitlesettings,true)</onclick>'
            '<onclick condition="!Window.IsActive(%s)">Dialog.Close(osdvideosettings,true)</onclick>'
            '<onclick condition="!Window.IsActive(%s)">Dialog.Close(osdcmssettings,true)</onclick>'
            '<onclick condition="!Window.IsActive(%s)">ActivateWindow(%s)</onclick></control>'
            '<control type="label"><left>0</left><top>0</top><width>253</width><height>82</height><align>center</align><aligny>center</aligny><font>uc_st_ui_22_bold</font>'
            '<textcolor>ffffffff</textcolor><label>%s</label><visible>[%s] + !Control.HasFocus(%d)</visible></control>'
            '%s%s</control>'
            % (1041 + i * 253, cid, label, left, right, target, target, target, target, target, target, target, label, current, cid,
               fw.img(30, 76, 193, 4, 'common/white.png', 'fg_mark', '[%s] + !Control.HasFocus(%d)' % (current, cid)),
               fw.img(252, 0, 1, 82, 'common/white.png', fw.LINE)))


OFFW = 'Window.IsActive(osdaudiosettings) | Window.IsActive(osdsubtitlesettings)'


def panel():
    nav = '<onup>5</onup><ondown>noop</ondown>'
    return (
        '<include name="FGS_SettingsPanel">'
        '<control type="group"><visible>!Window.IsVisible(sliderdialog)</visible><include>Anim_FadeVisible</include>'
        '<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture flipx="true">fg/fgs_vi_l.png</texture>'
        '<animation effect="fade" start="0" end="100" time="200">WindowOpen</animation><animation effect="fade" start="100" end="0" time="150">WindowClose</animation></control>'
        '<control type="group"><include content="Anim_SidePanel" condition="String.IsEmpty(Window(Home).Property(aeon.osdtab))"><param name="offset" value="80"/></include>'
        + fw.img(1040, 108, 781, 853, 'common/white.png', 'c708090c') +
        fw.line(1040, 108, 781) + fw.line(1040, 960, 781) + fw.line(1041, 191, 779) +
        ''.join(fw.line(x, 108, 1, 852) for x in (1040, 1800, 1820)) +
        tab(0, 9101, '$LOCALIZE[31128]', 'osdaudiosettings', 'Window.IsActive(osdaudiosettings)', 'noop', '9102') +
        tab(1, 9102, '$LOCALIZE[31127]', 'osdsubtitlesettings', 'Window.IsActive(osdsubtitlesettings)', '9101', '9103') +
        tab(2, 9103, '$LOCALIZE[31563]', 'osdvideosettings', 'Window.IsActive(osdvideosettings) | Window.IsActive(osdcmssettings)', '9102', 'noop') +
        '<control type="grouplist" id="5"><description>control area</description><left>1041</left><include condition="%s">FGS_OsdAreaOffset</include><include condition="!%s">FGS_OsdAreaFull</include><width>759</width>' % (OFFW, OFFW) +
        '<itemgap>0</itemgap><pagecontrol>60</pagecontrol><onleft>noop</onleft><onright>60</onright>'
        '<onup condition="Window.IsActive(osdaudiosettings)">9101</onup><onup condition="Window.IsActive(osdsubtitlesettings)">9102</onup>'
        '<onup condition="Window.IsActive(osdvideosettings) | Window.IsActive(osdcmssettings)">9103</onup>'
        '<onup condition="!Window.IsActive(osdaudiosettings) + !Window.IsActive(osdsubtitlesettings) + !Window.IsActive(osdvideosettings) + !Window.IsActive(osdcmssettings)">5</onup>'
        '<ondown>9000</ondown></control>'
        '<include content="Aeon_SettingTemplates"><param name="width" value="759"/><param name="fgs" value="true"/><param name="pre" value="FGS_"/><param name="fgswidth" value="759"/></include>'
        '<control type="scrollbar" id="60"><left>1801</left><top>192</top><width>19</width><height>698</height><include>FGS_SBTex</include><textureslidernib /><textureslidernibfocus />'
        '<orientation>vertical</orientation><showonepage>false</showonepage><onleft>5</onleft><onright>noop</onright><onup>60</onup><ondown>60</ondown></control>'
        # 0.3.117 helper: the offset as the mockup draws it (SettingsPanel2): its own card at the top of the audio /
        # subtitle panel, the name and the value big in the accent, a tall ruler -0.5 .. +0.5 s, the white centre line,
        # the marker in the accent (aeon.off.*)
        '<control type="group"><visible>%s</visible>' % OFFW +
        fw.img(1041, 192, 759, 250, 'common/white.png', '0affffff') + fw.line(1041, 442, 759) +
        fw.label(1065, 206, 400, 50, '[UPPERCASE]$LOCALIZE[297][/UPPERCASE]', 'st_ui_24_bold', 'ffffffff', vis='Window.IsActive(osdaudiosettings)') +
        fw.label(1065, 206, 400, 50, '[UPPERCASE]$LOCALIZE[22006][/UPPERCASE]', 'st_ui_24_bold', 'ffffffff', vis='Window.IsActive(osdsubtitlesettings)') +
        fw.label(1465, 200, 311, 60, '$INFO[Window(Home).Property(aeon.off.val)]', 'st_display_40', 'fg_mark', 'right') +
        fw.img(1065, 318, 711, 2, 'common/white.png', '4dffffff') +
        ''.join(fw.img(1065 + int(k * 7.1), 318 - (17 if k % 25 == 0 else (11 if k % 5 == 0 else 6)), 2, 34 if k % 25 == 0 else (22 if k % 5 == 0 else 12),
                       'common/white.png', '99ffffff' if k % 25 == 0 else ('59ffffff' if k % 5 == 0 else '2effffff')) for k in range(0, 101, 5) ) +
        fw.img(1420, 284, 3, 70, 'common/white.png', 'ffffffff') +
        '<control type="ranges"><left>1065</left><top>233</top><width>711</width><height>86</height><texturebg></texturebg><lefttexture /><righttexture />'
        '<midtexture colordiffuse="fg_mark">fg/fgs_offmark.png</midtexture><info>Window(Home).Property(aeon.off.ranges)</info></control>' +
        fw.label(1065, 366, 200, 30, '-0.5 s', 'st_small_20', '8cffffff') + fw.label(1576, 366, 200, 30, '+0.5 s', 'st_small_20', '8cffffff', 'right') +
        fw.label(1065, 390, 711, 50, '$LOCALIZE[31243]', 'st_cap_14', '8cffffff', extra='<wrapmultiline>true</wrapmultiline>') +
        '</control>'
        + fw.line(1040, 890, 781) +
        '<control type="grouplist" id="9000"><left>1041</left><top>891</top><width>779</width><height>70</height><orientation>horizontal</orientation><itemgap>0</itemgap>'
        '<usecontrolcoords>true</usecontrolcoords><onleft>noop</onleft><onright>noop</onright><onup>5</onup><ondown>noop</ondown>%s</control>'
        % (fw.cell('28', 260, '', nav, vis='!String.IsEmpty(Control.GetLabel(28))') + fw.cell('29', 260, '', nav, vis='!String.IsEmpty(Control.GetLabel(29))') + fw.cell('30', 259, '', nav, vis='!String.IsEmpty(Control.GetLabel(30))')) +
        '</control>'
        '<control type="group"><left>60</left><top>990</top>'
        + fw.img(0, 0, 330, 56, 'fg/btn56n.png', 'b30a0c10').replace('<texture colordiffuse', '<texture border="28,0,28,0" colordiffuse') +
        fw.img(24, 22, 12, 12, 'fg/circle.png', 'fg_mark') +
        fw.label(48, 0, 270, 56, '$INFO[Player.Time]$INFO[Player.Duration, / ,]', 'st_small_20_semibold', 'ffffffff') +
        '</control></control>'
        '</include>')


def main():
    p = os.path.join(fw.D, 'DialogSettings.xml')
    w = io.open(p, encoding='utf-8').read()
    a = '<include condition="!$EXP[Dlg_IsOSDSettings] + !$EXP[Aeon_MS]">Dlg_SettingsCentred</include>'
    b = '<include condition="$EXP[Dlg_IsOSDSettings] + !$EXP[Aeon_MS]">Dlg_SettingsPanel</include>'
    if a in w:
        w = w.replace(a, '<include condition="!$EXP[Dlg_IsOSDSettings] + !$EXP[Aeon_MS] + !$EXP[FGS]">Dlg_SettingsCentred</include>\n\t\t'
                         '<include condition="!$EXP[Dlg_IsOSDSettings] + !$EXP[Aeon_MS] + $EXP[FGS]">FGS_SettingsCentred</include>')
        w = w.replace(b, '<include condition="$EXP[Dlg_IsOSDSettings] + !$EXP[Aeon_MS] + !$EXP[FGS]">Dlg_SettingsPanel</include>\n\t\t'
                         '<include condition="$EXP[Dlg_IsOSDSettings] + !$EXP[Aeon_MS] + $EXP[FGS]">FGS_SettingsPanel</include>')
        io.open(p, 'w', encoding='utf-8', newline='\n').write(w)
    fw.put('SettingsDlg', centred() + panel() +
           '<include name="FGS_OsdAreaOffset"><top>442</top><height>448</height></include>'
           '<include name="FGS_OsdAreaFull"><top>191</top><height>699</height></include>')
    print('fgs settings dialogs: pages written')


if __name__ == '__main__':
    main()
