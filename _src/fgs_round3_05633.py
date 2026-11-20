"""0.56.33 Fused Glass style, round 3 (the user's notes of 2026-11-17, evening):
- no smeared lines: a row's rule / divider picture was 8 px and Kodi stretched its transparent middle with linear
  filtering, so the line bled into a fade across the row (the "frosted gradient" in the dialogs, faintly under every
  Kodi settings rule): the pictures get a transparent margin inside their border (fgs_rowdiv 16 px, border 2;
  fgs_rule_top / fgs_rule border 2);
- everything but the focused row dims, like the System screen: unfocused labels, icons and values 40 % (66), frame
  outlines and dividers 10 % (1a, were 19 %), rules 7 %; the open category (focus in the list) dims; the focused row
  gets a full outline (fgs_bar: top, bottom AND right edge at 27 %, the white bar left); unfocused pills 70 %, toggles
  gold at 70 %;
- the navigation animation (Skin.String(aeon.fganim)) plays in the style: Kodi's rows and categories, the dialogs'
  rows and the select lists animate on focus (FGS_RowAnim), Skin settings rows animate their name with the bar; Glow
  (which only zoomed a shadow, and the style has none) brightens the row in;
- the System screen: the focused option's icon grows (40 -> 56) with a small pop;
- Home > System > Shortcuts: Files (Kodi's video sources, 744) after File manager;
- the grid list's icon (favourites, add-on browser, media windows): a rounded 96 x 54 frame (fg/m96x54.png).
Run from the skin folder after fgs_dialogs_05632. Repeatable."""
import io
import os
import re

from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
D = os.path.join(ROOT, '1080i')
FG = os.path.join(ROOT, 'media', 'fg')
MARK = '<!-- 0.56.33 fgs_round3 -->'


def rd(name):
    return io.open(os.path.join(D, name), encoding='utf-8').read()


def wr(name, text):
    io.open(os.path.join(D, name), 'w', encoding='utf-8', newline='\n').write(text)


def once(text, old, new, count=1):
    assert text.count(old) == count, (old[:100], text.count(old))
    return text.replace(old, new)


def block(text, start, end='</definition>'):
    s = text.index(start)
    return s, text.index(end, s)


def pictures():
    im = Image.new('RGBA', (16, 16), (255, 255, 255, 0))
    for x in range(1, 16):
        im.putpixel((x, 15), (255, 255, 255, 0x12))
    for y in range(16):
        im.putpixel((0, y), (255, 255, 255, 0x1a))
    im.save(os.path.join(FG, 'fgs_rowdiv.png'))
    bar = Image.open(os.path.join(FG, 'fgs_bar.png')).convert('RGBA')
    w, h = bar.size
    for y in range(h):
        if bar.getpixel((w - 1, y))[3] < 0x44:
            bar.putpixel((w - 1, y), (255, 255, 255, 0x44))
    bar.save(os.path.join(FG, 'fgs_bar.png'))
    mask = Image.open(os.path.join(FG, 'm128x72.png')).convert('RGBA').resize((96, 54), Image.LANCZOS)
    mask.save(os.path.join(FG, 'm96x54.png'))


ANIM = '''	<!-- 0.56.33 the navigation animation in the style, for rows that are buttons or list items (Focus) -->
	<include name="FGS_RowAnim">
		<animation type="Focus" condition="$EXP[FGS] + $EXP[FG_AnimPop] + !Skin.HasSetting(aeon.reducemotion)"><effect type="zoom" start="100" end="101.2" center="auto" time="110" tween="cubic" easing="out"/><effect type="zoom" start="100" end="98.814" center="auto" delay="110" time="160" tween="cubic" easing="in"/></animation>
		<animation type="Focus" condition="$EXP[FGS] + $EXP[FG_AnimGrow] + !Skin.HasSetting(aeon.reducemotion)"><effect type="zoom" start="97,100" end="100,100" center="auto" time="200" tween="cubic" easing="out"/></animation>
		<animation type="Focus" condition="$EXP[FGS] + $EXP[FG_AnimFade] + !Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="30" end="100" time="200" tween="sine" easing="out"/></animation>
		<animation type="Focus" condition="$EXP[FGS] + $EXP[FG_AnimGlow] + !Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="40" end="100" time="420" tween="sine" easing="out"/></animation>
		<animation type="Focus" condition="$EXP[FGS] + $EXP[FG_AnimNudge] + !Skin.HasSetting(aeon.reducemotion)"><effect type="slide" start="0,0" end="9,0" time="100" tween="cubic" easing="out"/><effect type="slide" start="0,0" end="-9,0" delay="100" time="160" tween="cubic" easing="in"/></animation>
		<animation type="Focus" condition="$EXP[FGS] + $EXP[FG_AnimLift] + !Skin.HasSetting(aeon.reducemotion)"><effect type="slide" start="0,0" end="0,-4" time="110" tween="cubic" easing="out"/><effect type="slide" start="0,0" end="0,4" delay="110" time="160" tween="cubic" easing="in"/></animation>
	</include>
	<!-- Glow in the style (the bar groups and names of Skin settings rows, Visible) -->
	<include name="FGS_LandGlow">
		<animation type="Visible" condition="$EXP[FGS] + $EXP[FG_AnimGlow] + !Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="40" end="100" time="420" tween="sine" easing="out"/></animation>
	</include>
	<!-- the dim of everything but the focused row (the System screen's 40 %) -->
	<variable name="FGS_RowText"><value condition="$EXP[FGS]">66ffffff</value><value>99ffffff</value></variable>
	<variable name="FGS_TitleText"><value condition="$EXP[FGS]">8cffffff</value><value>ccffffff</value></variable>
	<variable name="FGS_CatText"><value condition="$EXP[FGS]">66ffffff</value><value>ccffffff</value></variable>
	<variable name="FGS_CatIcon"><value condition="$EXP[FGS]">66ffffff</value><value>bbffffff</value></variable>
	<variable name="FGS_RowIcon"><value condition="$EXP[FGS]">66ffffff</value><value>$VAR[Aeon_Accent]</value></variable>
	<variable name="FGS_FrameCol"><value condition="$EXP[FGS]">1affffff</value><value>30ffffff</value></variable>
	<variable name="FGS_CatBarCol"><value condition="ControlGroup(5).HasFocus">59ffffff</value><value>ffffffff</value></variable>
	<variable name="FGS_PillOn"><value condition="$EXP[FGS]">b3ffffff</value><value>$VAR[Aeon_Accent]</value></variable>
	<variable name="FGS_Dim99"><value condition="$EXP[FGS]">66ffffff</value><value>99ffffff</value></variable>
'''


def fused():
    t = rd('Includes_Fused.xml')
    if MARK not in t:
        t = once(t, '\t<include name="FGS_RowTex">', '\t' + MARK + '\n' + ANIM + '\t<include name="FGS_RowTex">')
    t = t.replace('<texturenofocus border="0,1,0,0" colordiffuse="12ffffff">fg/fgs_rule_top.png</texturenofocus>',
                  '<texturenofocus border="0,2,0,0" colordiffuse="12ffffff">fg/fgs_rule_top.png</texturenofocus>')
    t = t.replace('<texturenofocus border="0,0,0,1" colordiffuse="12ffffff">fg/fgs_rule.png</texturenofocus>',
                  '<texturenofocus border="0,0,0,2" colordiffuse="12ffffff">fg/fgs_rule.png</texturenofocus>')
    s, e = block(t, '<include name="FGS_CatTex">', '</include>')
    b = t[s:e].replace('<texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar.png</texturefocus>',
                       '<texturefocus border="20" colordiffuse="$VAR[FGS_CatBarCol]">fg/fgs_bar.png</texturefocus>')
    t = t[:s] + b + t[e:]
    s, e = block(t, '<include name="FGS_RadioTex">', '</include>')
    b = t[s:e].replace('<textureradioonnofocus colordiffuse="fg_mark">', '<textureradioonnofocus colordiffuse="b3e8b04b">')
    b = b.replace('<textureradiooffnofocus colordiffuse="ccffffff">', '<textureradiooffnofocus colordiffuse="80ffffff">')
    t = t[:s] + b + t[e:]
    t = t.replace('<variable name="FGS_ToggleOn">\n\t\t<value condition="$EXP[FGS]">fg_mark</value>',
                  '<variable name="FGS_ToggleOn">\n\t\t<value condition="$EXP[FGS]">b3e8b04b</value>')
    old = '<variable name="FGS_Aeon_CatFocInk">\n\t\t<value condition="$EXP[FGS]">ffffffff</value>'
    if old in t:
        t = t.replace(old, '<variable name="FGS_Aeon_CatFocInk">\n\t\t<value condition="$EXP[FGS] + ControlGroup(5).HasFocus">80ffffff</value>\n\t\t<value condition="$EXP[FGS]">ffffffff</value>')
    t = t.replace('<variable name="FGS_Aeon_ParentInk">\n\t\t<value condition="$EXP[FGS]">ffffffff</value>',
                  '<variable name="FGS_Aeon_ParentInk">\n\t\t<value condition="$EXP[FGS]">99ffffff</value>')
    # Home > System > Shortcuts: Files after File manager
    fm = '<item><label>$LOCALIZE[7]</label><icon>common/aeon_mi_folder.png</icon><onclick>ActivateWindow(filemanager)</onclick></item>'
    if 'ActivateWindow(Videos,Files,return)' not in t:
        t = once(t, fm, fm + '\n\t\t\t\t\t\t<item><label>$LOCALIZE[744]</label><icon>common/aeon_mi_film.png</icon><onclick>ActivateWindow(Videos,Files,return)</onclick></item>')
    var = '\t<variable name="FGS_OnText"><value condition="$EXP[FGS]">99ffffff</value><value>ffffffff</value></variable>\n'
    if 'name="FGS_OnText"' not in t:
        t = once(t, '\t<variable name="FGS_Dim99">', var + '\t<variable name="FGS_Dim99">')
    wr('Includes_Fused.xml', t)
    print('Includes_Fused.xml done')


FRAME = re.compile(r'colordiffuse="30ffffff">common/white\.png</texture><visible>([^<]*FGS[^<]*)</visible>')


def frames(t):
    return FRAME.sub(lambda m: 'colordiffuse="$VAR[FGS_FrameCol]">common/white.png</texture><visible>%s</visible>' % m.group(1), t)


def menu():
    t = rd('Includes_Aeon_Menu.xml')
    s, e = block(t, '<include name="Aeon_SettingRow">')
    b = t[s:e]
    if 'FGS_RowAnim' not in b:
        b = once(b, '<textcolor>99ffffff</textcolor>', '<textcolor>$VAR[FGS_RowText]</textcolor>')
        b = once(b, '<selectedcolor>99ffffff</selectedcolor>', '<selectedcolor>$VAR[FGS_RowText]</selectedcolor>')
        b = once(b, '<include condition="$PARAM[fgs] + $EXP[FGS]">FGS_RowTex</include>',
                 '<include condition="$PARAM[fgs] + $EXP[FGS]">FGS_RowTex</include>\n\t\t\t<include condition="$PARAM[fgs] + $EXP[FGS]">FGS_RowAnim</include>')
        t = t[:s] + b + t[e:]
    s, e = block(t, '<include name="Aeon_SettingTemplates">')
    b = t[s:e]
    if 'FGS_TitleText' not in b:
        b = once(b, '<textcolor>ccffffff</textcolor><selectedcolor>ccffffff</selectedcolor>',
                 '<textcolor>$VAR[FGS_TitleText]</textcolor><selectedcolor>$VAR[FGS_TitleText]</selectedcolor>')
        t = t[:s] + b + t[e:]
    s, e = block(t, '<include name="Aeon_SettingCategoryTemplate">')
    b = t[s:e]
    if 'FGS_CatText' not in b:
        b = once(b, '<textcolor>ccffffff</textcolor>', '<textcolor>$VAR[FGS_CatText]</textcolor>')
        b = once(b, '<include condition="$PARAM[fgs] + $EXP[FGS]">FGS_CatTex</include>',
                 '<include condition="$PARAM[fgs] + $EXP[FGS]">FGS_CatTex</include>\n\t\t\t\t<include condition="$PARAM[fgs] + $EXP[FGS]">FGS_RowAnim</include>')
        t = t[:s] + b + t[e:]
    t = frames(t)
    # the System screen: the focused option's icon grows with a small pop
    s, e = block(t, '<include name="Aeon_MenuRow">')
    b = t[s:e]
    if '0.56.33 icon pop' not in b:
        i = b.index('<!-- the focused option nudges to the left -->')
        j = b.index('<control type="image">', i)
        k = b.index('</control>', j)
        img = b[j:k]
        new = img.replace('<left>698</left>', '<left>690</left>').replace('<top>30</top>', '<top>22</top>')
        new = new.replace('<width>40</width>', '<width>56</width>').replace('<height>40</height>', '<height>56</height>')
        assert new != img, img
        new = new.replace('<control type="image">', '<control type="image"><!-- 0.56.33 icon pop -->\n\t\t\t\t\t<animation type="Visible" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="zoom" start="71" end="100" center="auto" time="240" tween="back" easing="out"/></animation>', 1)
        b = b[:j] + new + b[k:]
        t = t[:s] + b + t[e:]
    wr('Includes_Aeon_Menu.xml', t)
    print('Includes_Aeon_Menu.xml done')


def settings():
    t = rd('Includes_Settings.xml')
    s, e = block(t, '<include name="Dlg_SkinRowChrome">')
    b = t[s:e]
    if 'FGS_RowIcon' not in b:
        b = once(b, '<texture colordiffuse="$VAR[Aeon_Accent]">$PARAM[icon]</texture>', '<texture colordiffuse="$VAR[FGS_RowIcon]">$PARAM[icon]</texture>')
        # the focused name animates with the bar (FG_LandVisible + the style's glow)
        i = b.index('<textcolor>$VAR[FGS_Aeon_OnBarInk]</textcolor>')
        j = b.index('<visible>[$PARAM[enable]] + Control.HasFocus($PARAM[id])</visible>', i)
        b = b[:j] + '<include>FG_LandVisible</include><include>FGS_LandGlow</include>\n\t\t\t\t' + b[j:]
        t = t[:s] + b + t[e:]
    t = t.replace('<variable name="FG_SkinRowInk">\n\t\t<value condition="Skin.HasSetting(aeon.fglass)">e0ffffff</value>',
                  '<variable name="FG_SkinRowInk">\n\t\t<value condition="$EXP[FGS]">66ffffff</value>\n\t\t<value condition="Skin.HasSetting(aeon.fglass)">e0ffffff</value>')
    s, e = block(t, '<include name="Dlg_SkinCategory">')
    b = t[s:e]
    if 'FGS_CatIcon' not in b:
        b = once(b, '<texture colordiffuse="bbffffff">$PARAM[icon]</texture>', '<texture colordiffuse="$VAR[FGS_CatIcon]">$PARAM[icon]</texture>')
        b = once(b, '<texture border="20" colordiffuse="80ffffff">fg/fgs_bar.png</texture>', '<texture border="20" colordiffuse="40ffffff">fg/fgs_bar.png</texture>')
        k = b.rindex('<textcolor>ccffffff</textcolor>')
        b = b[:k] + '<textcolor>$VAR[FGS_CatText]</textcolor>' + b[k + len('<textcolor>ccffffff</textcolor>'):]
        t = t[:s] + b + t[e:]
    t = frames(t)
    wr('Includes_Settings.xml', t)
    print('Includes_Settings.xml done')


def skin():
    t = rd('SkinSettings.xml')
    t = frames(t)
    t = t.replace('colordiffuse="$VAR[Aeon_Accent]">$VAR[Aeon_MenuTexPill]', 'colordiffuse="$VAR[FGS_PillOn]">$VAR[Aeon_MenuTexPill]')
    t = t.replace('<font>st_ui_22</font><textcolor>99ffffff</textcolor>', '<font>st_ui_22</font><textcolor>$VAR[FGS_Dim99]</textcolor>')
    # the On beside an unfocused switch
    t = t.replace('<align>right</align><font>st_ui_22_bold</font><textcolor>ffffffff</textcolor>', '<align>right</align><font>st_ui_22_bold</font><textcolor>$VAR[FGS_OnText]</textcolor>')
    t = re.sub(r'<include>FG_LandVisible</include>(?!<include>FGS_LandGlow</include>)', '<include>FG_LandVisible</include><include>FGS_LandGlow</include>', t)
    wr('SkinSettings.xml', t)
    print('SkinSettings.xml done')


def views():
    t = rd('Includes_Views.xml')
    for name in ('FGS_AddonRow', 'FGS_View50'):
        s, e = block(t, '<include name="%s">' % name, '\n\t</include>')
        b = t[s:e].replace('colordiffuse="30ffffff">common/white.png', 'colordiffuse="$VAR[FGS_FrameCol]">common/white.png')
        b = b.replace('<textcolor>9effffff</textcolor><selectedcolor>9effffff</selectedcolor>', '<textcolor>66ffffff</textcolor><selectedcolor>66ffffff</selectedcolor>')
        b = b.replace('<left>7</left><top>7</top><width>96</width><height>56</height><aspectratio>keep</aspectratio><texture background="true">',
                      '<left>7</left><top>8</top><width>96</width><height>54</height><aspectratio>keep</aspectratio><texture background="true" diffuse="fg/m96x54.png">')
        t = t[:s] + b + t[e:]
    wr('Includes_Views.xml', t)
    print('Includes_Views.xml done')


if __name__ == '__main__':
    pictures()
    fused()
    menu()
    settings()
    skin()
    views()
