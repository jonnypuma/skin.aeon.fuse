"""0.56.31 Fused Glass style, the grid round 3 (the user's notes of 2026-11-17, evening):
- the unfocused rules are fainter: 7 % white (12ffffff), the mockup's value (was 15 %);
- a rule under every section title: the Kodi rows draw their rule at the TOP (fg/fgs_rule_top.png), so the first row
  under a group title draws the title's line; Kodi's group separator (image 11) is a full-width faint line, the line
  under the last row of a group; Skin settings rows get the same faint top rule (they had none) and the three Skin
  settings headings a rule above them, like Kodi's separator;
- Skin settings: the row icons, names, hints and headings move 101 px to the left (the icon starts at 503, 22 px
  from the column line, the inset of the category icons; the page title at 505, 24 px in like CATEGORIES); the names
  keep their right end, so each name gets 101 px more room (param namefgs = namew + 101 on every Dlg_SkinRowChrome
  call; NAVIGATION ANIMATION needs 302 of 306);
- the Skin settings scroll bars (9771, 9773, 9775) sit on the column line at 1500 (they were at 1520, in the preview);
- toggles in the style are gold when on: fg_mark, the skin's one accent (the mark under the Home icon).

Run from the skin folder after fgs_caps_05631 (generator order: ... fgs_round2_05630, fgs_caps_05631, fgs_grid_05631).
Repeatable: every step checks its own mark."""
import io
import os
import re

from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
D = os.path.join(ROOT, '1080i')
SHIFT = 101
FAINT = '12ffffff'


def rd(name):
    return io.open(os.path.join(D, name), encoding='utf-8').read()


def wr(name, text):
    io.open(os.path.join(D, name), 'w', encoding='utf-8', newline='\n').write(text)


def once(text, old, new, count=1):
    assert text.count(old) == count, (old[:90], text.count(old))
    return text.replace(old, new)


def picture():
    path = os.path.join(ROOT, 'media', 'fg', 'fgs_rule_top.png')
    im = Image.new('RGBA', (8, 8), (255, 255, 255, 0))
    for x in range(8):
        im.putpixel((x, 0), (255, 255, 255, 255))
    im.save(path)
    print('picture', path)


SLIDE = '<animation effect="slide" start="0,0" end="-%d,0" time="0" condition="$EXP[FGS]">Conditional</animation>' % SHIFT


def fused():
    t = rd('Includes_Fused.xml')
    if 'fgs_rule_top.png' in t:
        return
    t = once(t, '<texturenofocus border="0,0,0,1" colordiffuse="26ffffff">fg/fgs_rule.png</texturenofocus>\n\t</include>\n\t<include name="FG_RowTex">',
             '<texturenofocus border="0,1,0,0" colordiffuse="%s">fg/fgs_rule_top.png</texturenofocus>\n\t</include>\n\t<include name="FG_RowTex">' % FAINT)
    t = once(t, '<texturenofocus border="0,0,0,1" colordiffuse="26ffffff">fg/fgs_rule.png</texturenofocus>',
             '<texturenofocus border="0,0,0,1" colordiffuse="%s">fg/fgs_rule.png</texturenofocus>' % FAINT)
    # the toggle: gold when on (fg_mark), focused or not
    s = t.index('<include name="FGS_RadioTex">')
    e = t.index('</include>', s)
    block = t[s:e]
    new = block.replace('$VAR[FGS_Aeon_OnBarFill]', 'fg_mark').replace('$VAR[Aeon_Accent]', 'fg_mark')
    assert new != block
    t = t[:s] + new + t[e:]
    extra = '''	<!-- 0.56.31 grid round 3: Kodi's group separator in the style (full width, faint) and the old one -->
	<include name="FGS_SepTex"><texture colordiffuse="%s">common/white.png</texture></include>
	<include name="Aeon_SepTex"><texture colordiffuse="30ffffff">common/white.png</texture></include>
	<!-- Skin settings toggles: gold (fg_mark) when on in the style, the accent elsewhere -->
	<variable name="FGS_ToggleOn">
		<value condition="$EXP[FGS]">fg_mark</value>
		<value>$VAR[Aeon_Accent]</value>
	</variable>
	<variable name="FGS_ToggleOnF">
		<value condition="$EXP[FGS]">fg_mark</value>
		<value>$VAR[FGS_Aeon_OnBarFill]</value>
	</variable>
''' % FAINT
    t = once(t, '\t<include name="FGS_RowTex">', extra + '\t<include name="FGS_RowTex">')
    wr('Includes_Fused.xml', t)
    print('Includes_Fused.xml done')


def kodi_separator():
    t = rd('Includes_Aeon_Menu.xml')
    if 'FGS_SepTex' in t:
        return
    old = '''			<control type="image" id="11">
				<width>$PARAM[width]</width>
				<height>1</height>
				<texture colordiffuse="30ffffff">common/white.png</texture>'''
    new = '''			<control type="image" id="11">
				<include content="Param_W" condition="$PARAM[fgs] + $EXP[FGS]"><param name="w" value="$PARAM[fgswidth]"/></include>
				<include content="Param_W" condition="![$PARAM[fgs] + $EXP[FGS]]"><param name="w" value="$PARAM[width]"/></include>
				<height>1</height>
				<include condition="$PARAM[fgs] + $EXP[FGS]">FGS_SepTex</include>
				<include condition="![$PARAM[fgs] + $EXP[FGS]]">Aeon_SepTex</include>'''
    t = once(t, old, new)
    wr('Includes_Aeon_Menu.xml', t)
    print('Includes_Aeon_Menu.xml done')


def chrome():
    """Dlg_SkinRowChrome: faint top rule in the style; icons, names and hint 87 px to the left, names 87 px wider."""
    t = rd('Includes_Settings.xml')
    if 'name="namefgs"' in t:
        return
    s = t.index('<include name="Dlg_SkinRowChrome">')
    e = t.index('</definition>', s)
    b = t[s:e]
    b = once(b, '<param name="namew">520</param>', '<param name="namew">520</param>\n\t\t<param name="namefgs">%d</param>' % (520 + SHIFT))
    b = once(b, '\t\t<definition>\n', '\t\t<definition>\n\t\t\t<!-- 0.56.31 the style: a faint rule on top of each row (the row under a heading draws its line) -->\n'
             '\t\t\t<control type="image"><left>-119</left><top>0</top><width>1019</width><height>1</height><texture colordiffuse="%s">common/white.png</texture><visible>$EXP[FGS] + !Control.HasFocus($PARAM[id])</visible></control>\n' % FAINT)
    # icons: slide
    b = once(b, '\t\t\t\t<left>2</left><top>20</top><width>30</width><height>30</height>\n',
             '\t\t\t\t<left>2</left><top>20</top><width>30</width><height>30</height>\n\t\t\t\t' + SLIDE + '\n', 2)
    # names: slide + wider
    b = once(b, '\t\t\t\t<width>$PARAM[namew]</width>\n',
             '\t\t\t\t<include content="Param_W" condition="$EXP[FGS]"><param name="w" value="$PARAM[namefgs]"/></include>'
             '<include content="Param_W" condition="!$EXP[FGS]"><param name="w" value="$PARAM[namew]"/></include>\n\t\t\t\t' + SLIDE + '\n', 4)
    # hint: slide
    b = once(b, '\t\t\t\t<width>$PARAM[hintw]</width>\n', '\t\t\t\t<width>$PARAM[hintw]</width>\n\t\t\t\t' + SLIDE + '\n')
    t = t[:s] + b + t[e:]
    wr('Includes_Settings.xml', t)
    print('Includes_Settings.xml done')


def skin():
    t = rd('SkinSettings.xml')
    if 'namefgs' in t:
        return
    n = [0]

    def call(m):
        body = m.group(0)
        w = re.search(r'<param name="namew" value="(\d+)"/>', body)
        width = int(w.group(1)) if w else 520
        n[0] += 1
        return body.replace('<include content="Dlg_SkinRowChrome">',
                            '<include content="Dlg_SkinRowChrome"><param name="namefgs" value="%d"/>' % (width + SHIFT), 1)
    t = re.sub(r'<include content="Dlg_SkinRowChrome">.*?</include>', call, t, flags=re.S)
    assert n[0] == 127, n[0]
    # headings: label 87 px left, a faint rule above (like Kodi's separator)
    head = '<control type="group"><width>1100</width><height>70</height><control type="label"><left>162</left><top>28</top>'
    t = once(t, head, '<control type="group"><width>1100</width><height>70</height>'
             '<control type="image"><left>41</left><top>0</top><width>1019</width><height>1</height><texture colordiffuse="%s">common/white.png</texture><visible>$EXP[FGS]</visible></control>'
             '<control type="label"><left>162</left><top>28</top>%s' % (FAINT, SLIDE), 3)
    # page title
    title = '<control type="label"><left>600</left><top>112</top>'
    i = t.index(title)
    j = t.index('</control>', i)
    t = t[:j] + '<animation effect="slide" start="0,0" end="-95,0" time="0" condition="$EXP[FGS]">Conditional</animation>' + t[j:]
    # scroll bars onto the column line (1520 -> 1496..1500)
    for sid in ('9771', '9773', '9775'):
        i = t.index('<control type="scrollbar" id="%s">' % sid)
        j = t.index('</control>', i)
        t = t[:j] + '\t<animation effect="slide" end="-24,0" time="0" condition="$EXP[FGS]">Conditional</animation>\n' + t[j:]
    wr('SkinSettings.xml', t)
    print('SkinSettings.xml done (%d rows)' % n[0])


def toggles():
    """toggles gold when on (repeatable: skin_previews writes its preview switches with the plain accent again)"""
    t = rd('SkinSettings.xml')
    n = t.count('colordiffuse="$VAR[Aeon_Accent]">$VAR[Aeon_MenuTexSwitch]') + t.count('colordiffuse="$VAR[FGS_Aeon_OnBarFill]">$VAR[Aeon_MenuTexSwitch]')
    if n:
        t = t.replace('colordiffuse="$VAR[Aeon_Accent]">$VAR[Aeon_MenuTexSwitch]', 'colordiffuse="$VAR[FGS_ToggleOn]">$VAR[Aeon_MenuTexSwitch]')
        t = t.replace('colordiffuse="$VAR[FGS_Aeon_OnBarFill]">$VAR[Aeon_MenuTexSwitch]', 'colordiffuse="$VAR[FGS_ToggleOnF]">$VAR[Aeon_MenuTexSwitch]')
        wr('SkinSettings.xml', t)
        print('toggles: %d gold' % n)


def addon_browser():
    t = rd('Includes_Views.xml')
    s = t.index('<include name="FGS_AddonRow">')
    e = t.index('</include>', s)
    b = t[s:e]
    if 'colordiffuse="26ffffff">common/white.png' in b:
        b = b.replace('colordiffuse="26ffffff">common/white.png', 'colordiffuse="%s">common/white.png' % FAINT)
        t = t[:s] + b + t[e:]
        wr('Includes_Views.xml', t)
        print('Includes_Views.xml done')


def categories():
    """Skin settings categories in the style: 22 px capitals (uc_st_ui_22_*, helper 0.3.106 CAPS), the label 4 px to
    the left and 290 wide: MOTION, MEMORY, RESET is 303 px in 24 px bold capitals, 287 in 22 (the room was 284)."""
    t = rd('Includes_Settings.xml')
    s = t.index('<include name="Dlg_SkinCategory">')
    e = t.index('</definition>', s)
    b = t[s:e]
    if 'uc_st_ui_22_' in b:
        return
    b = once(b, 'value="uc_st_ui_24_bold"', 'value="uc_st_ui_22_bold"', 2)
    b = once(b, 'value="uc_st_ui_24_semibold"', 'value="uc_st_ui_22_semibold"', 1)
    b = once(b, '<width>284</width>\n',
             '<include content="Param_W" condition="$EXP[FGS]"><param name="w" value="290"/></include>'
             '<include content="Param_W" condition="!$EXP[FGS]"><param name="w" value="284"/></include>\n'
             '\t\t\t\t\t<animation effect="slide" start="0,0" end="-4,0" time="0" condition="$EXP[FGS]">Conditional</animation>\n', 3)
    t = t[:s] + b + t[e:]
    wr('Includes_Settings.xml', t)
    print('Includes_Settings.xml categories done')


def titles():
    """CATEGORIES and the page title: centred in the title band 108-191 in the style (label 112-172 -> 120-180)."""
    t = rd('SkinSettings.xml')
    mark = '<!-- 0.56.31 title band centre -->'
    if mark in t:
        return
    for left in ('144', '600'):
        i = t.index('<control type="label"><left>%s</left><top>112</top>' % left)
        j = t.index('</control>', i)
        t = t[:j] + '<animation effect="slide" start="0,0" end="0,8" time="0" condition="$EXP[FGS]">Conditional</animation>' + t[j:]
    t = t.replace('<control type="label"><left>144</left><top>112</top>', mark + '\n\t\t<control type="label"><left>144</left><top>112</top>', 1)
    wr('SkinSettings.xml', t)
    print('SkinSettings.xml titles done')


if __name__ == '__main__':
    categories()
    titles()
    picture()
    fused()
    kodi_separator()
    chrome()
    skin()
    toggles()
    addon_browser()
