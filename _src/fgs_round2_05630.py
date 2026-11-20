# -*- coding: utf-8 -*-
"""0.56.30 the Fused Glass style, round 2 (the user, 2026-11-17: "there are no grids inside the lines in the deeper
menus ... only the highlight bar has lines"; the scroll bar "should sit flush with the right outline" and only when
needed; "why not make them [row heights] uniform"; "pill around the adjustment levers"; reuse the skin's toggle;
"addon menus are not done in this style yet"). Idempotent; run after fgs_flush_05629.py.

- The rule under every unfocused row shows (fg/fgs_rule.png, full white bottom line at 15 %; the old texture's own 24 %
  line tinted to 12 % was invisible); the focused row keeps its brighter rules above and below (fg/fgs_bar.png).
- Rows 70 high everywhere in the style (Skin settings already, now the Kodi settings pages, add-on settings, their
  categories, section titles and the level button, which sits flush with the bottom of the frame).
- The settings rows reach the right outline (Kodi settings 481-1814, add-on settings 481-1546); the scroll bar is
  6 px inside the outline (1814 / 1546) and shows only when the list is longer than the frame (all themes).
- Spin values: a pill split in two around the arrows (fg/fgs_spin_down.png / fgs_spin_up.png); on / off: the skin's
  own toggle (the Skin settings switch: the track in the accent colour with the dark knob on the right when on, a dim
  track with the knob on the left when off; fg/fgs_toggle_on.png / fgs_toggle_off.png, coloured like the switch).
- Add-on browser: the list in the System grid (frame, a rule under each row, the icon column and its divider, names in
  capitals, the version at the end, the bar on the divider), no card, the scroll bar on the outline.
"""
import io
import os
import re

D = '1080i'
MARK = '0.56.30 fgs_round2'
C = '$PARAM[fgs] + $EXP[FGS]'


def rd(p):
    return io.open(os.path.join(D, p), encoding='utf-8').read()


def wr(p, t):
    io.open(os.path.join(D, p), 'w', encoding='utf-8', newline='\n').write(t)


def once(t, old, new, tag):
    if new in t:
        return t
    assert t.count(old) == 1, (tag, t.count(old))
    return t.replace(old, new)


# ------------------------------------------------------------------------------------------------ pictures
def pictures():
    from PIL import Image, ImageDraw
    fg = os.path.join('media', 'fg')
    # the rule: 8 x 8, the bottom row white
    img = Image.new('RGBA', (8, 8), (255, 255, 255, 0))
    for x in range(8):
        img.putpixel((x, 7), (255, 255, 255, 255))
    img.save(os.path.join(fg, 'fgs_rule.png'))
    S = 4                                             # supersampling
    W, H = 40, 32

    def half(side, up):
        big = Image.new('RGBA', (W * S, H * S), (255, 255, 255, 0))
        d = ImageDraw.Draw(big)
        lw = int(1.5 * S)
        r = H * S // 2
        # the pill's half: rounded on the outer side, straight on the inner one (the two halves meet in a line)
        if side == 'left':
            d.rounded_rectangle((0, 0, W * S * 2, H * S - 1), radius=r, outline=(255, 255, 255, 255), width=lw)
            d.rectangle((W * S - lw, 0, W * S - 1, H * S - 1), fill=(255, 255, 255, 255))      # the line between the halves
        else:
            d.rounded_rectangle((-W * S, 0, W * S - 1, H * S - 1), radius=r, outline=(255, 255, 255, 255), width=lw)
        cx, cy, k = W * S // 2 + (S if side == 'left' else -S), H * S // 2, 6 * S
        pts = [(cx - k, cy - k // 2), (cx, cy + k // 2), (cx + k, cy - k // 2)] if not up else [(cx - k, cy + k // 2), (cx, cy - k // 2), (cx + k, cy + k // 2)]
        d.line(pts, fill=(255, 255, 255, 255), width=int(2.2 * S), joint='curve')
        return big.resize((W * 2, H * 2), Image.LANCZOS)
    half('left', False).save(os.path.join(fg, 'fgs_spin_down.png'))
    half('right', True).save(os.path.join(fg, 'fgs_spin_up.png'))
    # the toggle, from the skin's own switch pictures (64 x 32 track, 24 x 24 knob 4 px in)
    track = Image.open(os.path.join('media', 'common', 'aeon_switch.png')).convert('RGBA').resize((128, 64), Image.LANCZOS)
    knob = Image.open(os.path.join('media', 'aeon', 'circle_24.png')).convert('RGBA').resize((48, 48), Image.LANCZOS)
    on = track.copy()
    dark = Image.new('RGBA', knob.size, (15, 17, 21, 255))
    dark.putalpha(knob.split()[3])
    on.alpha_composite(dark, (128 - 8 - 48, 8))       # knob on the right, dark (the accent tints the track)
    on.save(os.path.join(fg, 'fgs_toggle_on.png'))
    off = Image.new('RGBA', track.size, (255, 255, 255, 0))
    t2 = track.copy()
    t2.putalpha(t2.split()[3].point(lambda a: a * 0x33 // 255))
    off.alpha_composite(t2)
    k2 = Image.new('RGBA', knob.size, (255, 255, 255, 255))
    k2.putalpha(knob.split()[3].point(lambda a: a * 0xcc // 255))
    off.alpha_composite(k2, (8, 8))                    # knob on the left, white
    off.save(os.path.join(fg, 'fgs_toggle_off.png'))
    print('pictures written')


# ------------------------------------------------------------------------------------------------ includes
NEW_INCLUDES = '''	<!-- %(m)s: the Fused Glass style's settings rows: 70 high, a rule under each row, the spin pill, the toggle -->
	<include name="FGS_RowH"><height>70</height></include>
	<include name="FGS_CatTex">
		<texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar.png</texturefocus>
		<texturenofocus border="0,0,0,1" colordiffuse="26ffffff">fg/fgs_rule.png</texturenofocus>
	</include>
	<include name="FGS_SpinTex">
		<spinwidth>40</spinwidth>
		<spinheight>32</spinheight>
		<textureup colordiffuse="8cffffff">fg/fgs_spin_up.png</textureup>
		<texturedown colordiffuse="8cffffff">fg/fgs_spin_down.png</texturedown>
		<textureupfocus colordiffuse="ffffffff">fg/fgs_spin_up.png</textureupfocus>
		<texturedownfocus colordiffuse="ffffffff">fg/fgs_spin_down.png</texturedownfocus>
		<textureupdisabled colordiffuse="33ffffff">fg/fgs_spin_up.png</textureupdisabled>
		<texturedowndisabled colordiffuse="33ffffff">fg/fgs_spin_down.png</texturedowndisabled>
	</include>
	<include name="FGS_RadioTex">
		<radiowidth>64</radiowidth>
		<radioheight>32</radioheight>
		<textureradioonfocus colordiffuse="$VAR[FGS_Aeon_OnBarFill]">fg/fgs_toggle_on.png</textureradioonfocus>
		<textureradioonnofocus colordiffuse="$VAR[Aeon_Accent]">fg/fgs_toggle_on.png</textureradioonnofocus>
		<textureradioofffocus colordiffuse="ffffffff">fg/fgs_toggle_off.png</textureradioofffocus>
		<textureradiooffnofocus colordiffuse="ccffffff">fg/fgs_toggle_off.png</textureradiooffnofocus>
		<textureradioondisabled colordiffuse="44ffffff">fg/fgs_toggle_on.png</textureradioondisabled>
		<textureradiooffdisabled colordiffuse="44ffffff">fg/fgs_toggle_off.png</textureradiooffdisabled>
	</include>
	<include name="Aeon_RadioSize24">
		<radiowidth>24</radiowidth>
		<radioheight>24</radioheight>
	</include>
	<include name="FGS_W1333"><width>1333</width></include>
	<include name="FGS_W1065"><width>1065</width></include>
	<include name="Aeon_W1296"><width>1296</width></include>
	<include name="Aeon_W1058"><width>1058</width></include>
'''


def includes():
    f = rd('Includes_Fused.xml')
    if 'name="FGS_SpinTex"' not in f:
        f = f.replace('</includes>', NEW_INCLUDES % {'m': MARK} + '</includes>')
    # the rule under the rows
    f = f.replace('<texturenofocus border="0,0,0,1" colordiffuse="1fffffff">common/aeon_rule_h.png</texturenofocus>',
                  '<texturenofocus border="0,0,0,1" colordiffuse="26ffffff">fg/fgs_rule.png</texturenofocus>')
    wr('Includes_Fused.xml', f)
    print('includes written')


def templates():
    t = rd('Includes_Aeon_Menu.xml')
    # the setting row: 70 high, its width param under the style
    i = t.index('<include name="Aeon_SettingRow">')
    j = t.index('\n\t</include>', i)
    blk = t[i:j]
    if 'FGS_RowH' not in blk:
        blk = blk.replace('<param name="fgs">false</param>', '<param name="fgs">false</param>\n\t\t<param name="fgswidth">$PARAM[width]</param>', 1)
        blk = blk.replace('<width>$PARAM[width]</width>\n\t\t\t<height>$PARAM[height]</height>',
                          '<include content="Param_W" condition="%s"><param name="w" value="$PARAM[fgswidth]"/></include>\n'
                          '\t\t\t<include content="Param_W" condition="![%s]"><param name="w" value="$PARAM[width]"/></include>\n'
                          '\t\t\t<include condition="%s">FGS_RowH</include>\n'
                          '\t\t\t<include content="Param_H" condition="![%s]"><param name="h" value="$PARAM[height]"/></include>' % (C, C, C, C))
        assert 'FGS_RowH' in blk
        t = t[:i] + blk + t[j:]
        t = t.replace('\t<include name="Aeon_SettingRow">',
                      '\t<include name="Param_W"><param name="w">100</param><definition><width>$PARAM[w]</width></definition></include>\n'
                      '\t<include name="Param_H"><param name="h">70</param><definition><height>$PARAM[h]</height></definition></include>\n'
                      '\t<include name="Aeon_SettingRow">', 1)
    # the templates: fgswidth on to the rows; the spin pill, the toggle, 70-high titles
    i = t.index('<include name="Aeon_SettingTemplates">')
    j = t.index('\n\t</include>', i)
    blk = t[i:j]
    if 'FGS_SpinTex' not in blk:
        blk = blk.replace('<param name="pre"></param>', '<param name="pre"></param>\n\t\t<param name="fgswidth">1058</param>', 1)
        blk = blk.replace('<param name="pre" value="$PARAM[pre]"/></include>', '<param name="pre" value="$PARAM[pre]"/><param name="fgswidth" value="$PARAM[fgswidth]"/></include>')
        old = '\t\t\t\t<radiowidth>24</radiowidth>\n\t\t\t\t<radioheight>24</radioheight>'
        assert blk.count(old) == 1
        blk = blk.replace(old, '\t\t\t\t<include condition="%s">FGS_RadioTex</include>\n\t\t\t\t<include condition="![%s]">Aeon_RadioSize24</include>' % (C, C))
        old = '''			<control type="spincontrolex" id="9">
				<include content="Aeon_SettingRow">'''
        assert blk.count(old) == 1
        blk = blk.replace(old, '''			<control type="spincontrolex" id="9">
				<include condition="%s">FGS_SpinTex</include>
				<include content="Aeon_SettingRow">''' % C)
        old = '''			<control type="label" id="14">
				<width>$PARAM[width]</width>
				<height>settings_row_h</height>'''
        assert blk.count(old) == 1
        blk = blk.replace(old, '''			<control type="label" id="14">
				<width>$PARAM[width]</width>
				<include condition="%s">FGS_RowH</include>
				<include condition="![%s]">Aeon_RowHConst</include>''' % (C, C))
        t = t[:i] + blk + t[j:]
        t = t.replace('\t<include name="Aeon_SettingRow">', '\t<include name="Aeon_RowHConst"><height>settings_row_h</height></include>\n\t<include name="Aeon_SettingRow">', 1)
    # the category template: 70 high, the rule under it
    i = t.index('<include name="Aeon_SettingCategoryTemplate">')
    j = t.index('\n\t</include>', i)
    blk = t[i:j]
    if 'FGS_CatTex' not in blk:
        old = '\t\t\t\t<height>settings_row_h</height>'
        assert blk.count(old) == 1
        blk = blk.replace(old, '\t\t\t\t<include condition="%s">FGS_RowH</include>\n\t\t\t\t<include condition="![%s]">Aeon_RowHConst</include>' % (C, C))
        blk = blk.replace('<include condition="$PARAM[fgs] + $EXP[FGS]">FGS_RowTex</include>', '<include condition="$PARAM[fgs] + $EXP[FGS]">FGS_CatTex</include>')
        assert 'FGS_CatTex' in blk
        t = t[:i] + blk + t[j:]
    # the two classic pages: the list to the outline, the scroll bar on it and only when needed, the level button 70 high
    for inc, w_old, w_new, sb_old, sb_new, fgsw in (('SetCat_Classic', 'Aeon_W1296', 'FGS_W1333', '1790', '1814', 1333),
                                                     ('AddonSet_Classic', 'Aeon_W1058', 'FGS_W1065', '1540', '1546', 1065)):
        i = t.index('<include name="%s">' % inc)
        j = t.index('\n\t</include>', i)
        blk = t[i:j]
        if MARK in blk:
            continue
        w = w_old.replace('Aeon_W', '')
        m = re.search(r'(<control type="grouplist" id="5">.*?)<width>%s</width>' % w, blk, re.S)
        assert m, inc
        blk = blk[:m.end(1)] + '<include condition="!$EXP[FGS]">%s</include><include condition="$EXP[FGS]">%s</include><!-- %s -->' % (w_old, w_new, MARK) + blk[m.end():]
        blk = re.sub(r'(<param name="fgs" value="true"/><param name="pre" value="FGS_"/>)', r'\1<param name="fgswidth" value="%d"/>' % fgsw, blk, 1)
        old = '<include content="AG_Scrollbar">\n\t\t\t\t<param name="id" value="60"/>\n\t\t\t\t<param name="left" value="%s"/>' % sb_old
        assert blk.count(old) == 1, inc
        k = blk.index(old)
        e = blk.index('</include>', k) + len('</include>')
        sb = blk[k:e]
        sb2 = sb.replace('</include>', '\t<param name="showonepage" value="false"/>\n\t\t\t</include>')
        blk = blk[:k] + ('<control type="group"><animation effect="slide" start="0,0" end="%d,0" time="0" condition="$EXP[FGS]">Conditional</animation>\n\t\t\t'
                         % (int(sb_new) - int(sb_old))) + sb2 + '\n\t\t\t</control>' + blk[e:]
        old = '<param name="height" value="76"/>\n\t\t\t\t\t<param name="round" value="true"/>'
        assert blk.count(old) == 1, inc
        blk = blk.replace(old, '<param name="height" value="76"/>\n\t\t\t\t\t<param name="round" value="true"/>')
        # the level button's group: 6 px down under the style, so its 70-px button meets the frame's bottom
        m = re.search(r'<control type="group">\s*<left>100</left>\s*<top>789</top>', blk)
        assert m, inc
        blk = blk[:m.end()] + '\n\t\t\t\t<animation effect="slide" start="0,0" end="0,5" time="0" condition="$EXP[FGS]">Conditional</animation>' + blk[m.end():]
        t = t[:i] + blk + t[j:]
    wr('Includes_Aeon_Menu.xml', t)
    # the level button: 70 high under the style
    s = rd('Includes_Settings.xml')
    i = s.index('<include name="AG_SettingLevelButton">')
    j = s.index('\n\t</include>', i)
    blk = s[i:j]
    if 'FGS_RowH' not in blk:
        old = '<height>$PARAM[height]</height>'
        assert blk.count(old) == 1
        blk = blk.replace(old, '<include condition="$PARAM[round] + $EXP[FGS]">FGS_RowH</include>\n'
                          '\t\t\t\t<include content="Param_H" condition="![$PARAM[round] + $EXP[FGS]]"><param name="h" value="$PARAM[height]"/></include>')
        s = s[:i] + blk + s[j:]
        wr('Includes_Settings.xml', s)
    print('templates written')


# ------------------------------------------------------------------------------------------------ add-on browser
ROW = '''	<include name="FGS_AddonRow">
		<param name="focused">false</param>
		<definition>
			<control type="image"><left>0</left><top>69</top><width>1134</width><height>1</height><texture colordiffuse="26ffffff">common/white.png</texture></control>
			<control type="image"><left>110</left><top>0</top><width>1</width><height>70</height><texture colordiffuse="30ffffff">common/white.png</texture></control>
			<control type="group">
				<visible>$PARAM[focused] + Control.HasFocus(50)</visible>
				<include>Aeon_LandFocusAll</include>
				<control type="image"><left>0</left><top>0</top><width>1134</width><height>1</height><texture colordiffuse="55ffffff">common/white.png</texture></control>
				<control type="image"><left>0</left><top>69</top><width>1134</width><height>1</height><texture colordiffuse="55ffffff">common/white.png</texture></control>
				<control type="image"><left>108</left><top>0</top><width>5</width><height>70</height><texture colordiffuse="ffffffff">common/white.png</texture></control>
			</control>
			<control type="image"><left>33</left><top>13</top><width>44</width><height>44</height><aspectratio>keep</aspectratio><texture background="true">$INFO[ListItem.Icon]</texture></control>
			<control type="label"><left>146</left><top>0</top><width>700</width><height>70</height><aligny>center</aligny><font>st_ui_24</font>
				<textcolor>9effffff</textcolor><selectedcolor>9effffff</selectedcolor><label>[UPPERCASE]$INFO[ListItem.Label][/UPPERCASE]</label>
				<visible>!$PARAM[focused] | !Control.HasFocus(50)</visible></control>
			<control type="label"><left>146</left><top>0</top><width>700</width><height>70</height><aligny>center</aligny><font>st_ui_24_bold</font>
				<textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><label>[UPPERCASE]$INFO[ListItem.Label][/UPPERCASE]</label>
				<visible>$PARAM[focused] + Control.HasFocus(50)</visible></control>
			<control type="label"><left>860</left><top>0</top><width>244</width><height>70</height><align>right</align><aligny>center</aligny><font>st_small_20</font>
				<textcolor>8cffffff</textcolor><selectedcolor>8cffffff</selectedcolor><label>$INFO[ListItem.Label2]</label></control>
		</definition>
	</include>
	<include name="FGS_View50">
		<!-- the frame of the grid: around the sort / filter row and the list -->
		<control type="image"><left>666</left><top>168</top><width>1134</width><height>1</height><texture colordiffuse="30ffffff">common/white.png</texture></control>
		<control type="image"><left>666</left><top>1016</top><width>1134</width><height>1</height><texture colordiffuse="30ffffff">common/white.png</texture></control>
		<control type="image"><left>666</left><top>168</top><width>1</width><height>848</height><texture colordiffuse="30ffffff">common/white.png</texture></control>
		<control type="image"><left>1800</left><top>168</top><width>1</width><height>849</height><texture colordiffuse="30ffffff">common/white.png</texture></control>
		<control type="image"><left>666</left><top>246</top><width>1134</width><height>1</height><texture colordiffuse="30ffffff">common/white.png</texture></control>
		<control type="group">
			<visible>Control.IsVisible(50)</visible>
			<include>Anim_VisibleFade</include>
			<control type="list" id="50">
				<left>666</left>
				<top>246</top>
				<width>1134</width>
				<height>770</height>
				<onup>9000</onup>
				<ondown>noop</ondown>
				<onleft condition="Window.IsActive(addonbrowser) + $EXP[Aeon_FGlass] + Control.IsVisible(7700)">7700</onleft>
				<onleft>noop</onleft>
				<onright>60</onright>
				<pagecontrol>60</pagecontrol>
				<scrolltime tween="cubic" easing="out">200</scrolltime>
				<viewtype label="535">list</viewtype>
				<itemlayout width="1134" height="70">
					<include>FGS_AddonRow</include>
				</itemlayout>
				<focusedlayout width="1134" height="70">
					<include content="FGS_AddonRow"><param name="focused" value="true"/></include>
				</focusedlayout>
			</control>
			<control type="scrollbar" id="60">
				<left>1794</left>
				<top>247</top>
				<width>6</width>
				<height>769</height>
				<texturesliderbackground colordiffuse="1affffff">common/white.png</texturesliderbackground>
				<texturesliderbar colordiffuse="66ffffff">common/white.png</texturesliderbar>
				<texturesliderbarfocus colordiffuse="ffffffff">common/white.png</texturesliderbarfocus>
				<orientation>vertical</orientation>
				<showonepage>false</showonepage>
				<onleft>50</onleft>
				<onright>noop</onright>
				<onup>9000</onup>
				<ondown>noop</ondown>
				<onback>50</onback>
			</control>
		</control>
	</include>
'''


def addon_browser():
    v = rd('Includes_Views.xml')
    if 'name="FGS_View50"' not in v:
        v = v.replace('\t<include name="View_50_List">', '\t<!-- %s: the add-on browser\'s list in the Fused Glass style -->\n' % MARK + ROW + '\t<include name="View_50_List">', 1)
        wr('Includes_Views.xml', v)
    a = rd('AddonBrowser.xml')
    a = once(a, '\t\t<include>View_50_List</include>',
             '\t\t<include condition="!$EXP[FGS]">View_50_List</include>\n\t\t<include condition="$EXP[FGS]">FGS_View50</include><!-- %s -->' % MARK, 'view')
    old = '''			<height>848</height>
			<include>AG_Card</include>
		</control>'''
    if '<include condition="!$EXP[FGS]">AG_Card</include>' not in a:
        assert a.count(old) == 1
        a = a.replace(old, '''			<height>848</height>
			<include condition="!$EXP[FGS]">AG_Card</include>
		</control>''')
    wr('AddonBrowser.xml', a)
    print('add-on browser written')


# ------------------------------------------------------------------------------------------------ the frame: ten rows
def frame700():
    """the classic pages' frame is 684 high (9 rows of 76); under the style the rows are 70, so the frame, the list and
    the scroll bar become 700 (10 rows), the level button flush with its bottom"""
    t = rd('Includes_Aeon_Menu.xml')
    tag = '<!-- 700 -->'
    for inc in ('SetCat_Classic', 'AddonSet_Classic'):
        i = t.index('<include name="%s">' % inc)
        j = t.index('\n\t</include>', i)
        blk = t[i:j]
        if tag in blk:
            continue
        cond = '[!$EXP[Aeon_Fused] + !$EXP[Aeon_VGlass]] | $EXP[FGS]</visible>'
        # the bottom line 16 px down, the vertical lines 16 px longer
        def frame(m):
            line = m.group(0)
            if '<top>864</top>' in line:
                return line.replace('</control>', '<animation effect="slide" start="0,0" end="0,16" time="0" condition="$EXP[FGS]">Conditional</animation>%s</control>' % tag, 1)
            if '<height>684</height>' in line:
                return line.replace('</control>', '<animation effect="zoom" start="100,100" end="100,102.339" center="0,180" time="0" condition="$EXP[FGS]">Conditional</animation>%s</control>' % tag, 1)
            return line
        blk = re.sub(r'<control type="image">(?:(?!</control>).)*?' + re.escape(cond) + r'\s*</control>', frame, blk, flags=re.S)
        # the list
        m = re.search(r'(<control type="grouplist" id="5">.*?)<height>684</height>', blk, re.S)
        assert m, inc
        blk = blk[:m.end(1)] + '<include condition="!$EXP[FGS]">Aeon_H684</include><include condition="$EXP[FGS]">FGS_H700</include>' + tag + blk[m.end():]
        # the scroll bar (inside its slid group): 700 high
        blk = blk.replace('<animation effect="slide" start="0,0" end="24,0" time="0" condition="$EXP[FGS]">Conditional</animation>',
                          '<animation effect="slide" start="0,0" end="24,0" time="0" condition="$EXP[FGS]">Conditional</animation>'
                          '<animation effect="zoom" start="100,100" end="100,102.339" center="0,181" time="0" condition="$EXP[FGS]">Conditional</animation>', 1)
        blk = blk.replace('<animation effect="slide" start="0,0" end="6,0" time="0" condition="$EXP[FGS]">Conditional</animation>',
                          '<animation effect="slide" start="0,0" end="6,0" time="0" condition="$EXP[FGS]">Conditional</animation>'
                          '<animation effect="zoom" start="100,100" end="100,102.339" center="0,181" time="0" condition="$EXP[FGS]">Conditional</animation>', 1)
        # the level button: flush with the frame's new bottom (880 - 70 = 810; its group is at 789)
        blk = blk.replace('<animation effect="slide" start="0,0" end="0,5" time="0" condition="$EXP[FGS]">Conditional</animation>',
                          '<animation effect="slide" start="0,0" end="0,21" time="0" condition="$EXP[FGS]">Conditional</animation>', 1)
        t = t[:i] + blk + t[j:]
    if 'name="FGS_H700"' not in t:
        t = t.replace('\t<include name="Aeon_SettingRow">', '\t<include name="FGS_H700"><height>700</height></include>\n'
                      '\t<include name="Aeon_H684"><height>684</height></include>\n\t<include name="Aeon_SettingRow">', 1)
    wr('Includes_Aeon_Menu.xml', t)
    print('frame 700')


if __name__ == '__main__':
    pictures()
    includes()
    templates()
    addon_browser()
    frame700()
