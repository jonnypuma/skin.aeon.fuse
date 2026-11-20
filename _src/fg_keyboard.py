# -*- coding: utf-8 -*-
"""0.53.2 Fused Glass keyboard (DialogKeyboard.xml; the user: "the standard search box is square in Fused Glass and
doesn't fit"): the full-width square slab becomes a rounded frosted card (radius 28, the Fused Glass edge and soft
shadow), 48 px clear of the screen's sides and bottom, and the text sits in a rounded input well. The card keeps
$VAR[FG_KbFill], so Menu theme = Glass and Look > Material still colour it (_src/fg_glassmenus.py). The Aeon and
Glass themes keep the slab. Run from the skin folder; safe to run again; run _src/fg_material.py after it."""
import io
import os

P = os.path.join('1080i', 'Includes_Keyboard.xml')  # 0.55.0: Kb_Classic (was DialogKeyboard.xml)
MARK = '<!-- 0.53.2 Fused Glass card (_src/fg_keyboard.py) -->'
SLAB = '''			<control type="group">
				<left>72</left>
				<top>384</top>
				<width>1776</width>
				<height>672</height>'''
CARD = '''			%s
			<control type="group">
				<visible>Skin.HasSetting(aeon.fglass)</visible>
				<animation effect="fade" start="0" end="100" time="200">WindowOpen</animation>
				<animation effect="fade" start="100" end="0" time="150">WindowClose</animation>
				<control type="image"><left>56</left><top>340</top><width>1808</width><height>732</height><texture border="68" colordiffuse="$VAR[FG_PanelSh_8c]">fg/sh28.png</texture></control>
				<control type="image"><left>96</left><top>380</top><width>1728</width><height>652</height><texture border="28" colordiffuse="$VAR[FG_KbFill]">fg/r28.png</texture></control>
				<control type="image"><left>96</left><top>380</top><width>1728</width><height>652</height><texture border="28" colordiffuse="fg_edge">fg/e28.png</texture></control>
				<!-- the input well: the text being typed sits in a rounded field -->
				<control type="image"><left>120</left><top>446</top><width>1680</width><height>100</height><texture border="24" colordiffuse="1affffff">fg/r24.png</texture></control>
				<control type="image"><left>120</left><top>446</top><width>1680</width><height>100</height><texture border="24" colordiffuse="33ffffff">fg/e24.png</texture></control>
			</control>
''' % MARK


# The keys' focus (keyboard and numeric pad): a square of common/white.png everywhere; on the Fused Glass card it
# becomes a rounded key (radius 14), the other themes keep the square.
PD = os.path.join('1080i', 'Includes_Dialogs.xml')
KEY_OLD = '''	<include name="Dlg_Tex_Key_Round">
		<texturefocus colordiffuse="$VAR[AG_Accent]">common/white.png</texturefocus>
		<texturenofocus colordiffuse="00ffffff">common/white.png</texturenofocus>
	</include>'''
KEY_NEW = '''	<include name="Dlg_Tex_Key_Round">
		<include condition="Skin.HasSetting(aeon.fglass)">Dlg_Tex_Key_FG</include>
		<include condition="!Skin.HasSetting(aeon.fglass)">Dlg_Tex_Key_Plain</include>
	</include>
	<include name="Dlg_Tex_Key_Plain">
		<texturefocus colordiffuse="$VAR[AG_Accent]">common/white.png</texturefocus>
		<texturenofocus colordiffuse="00ffffff">common/white.png</texturenofocus>
	</include>
	<!-- 0.53.2 Fused Glass: rounded keys on the rounded keyboard card (_src/fg_keyboard.py) -->
	<include name="Dlg_Tex_Key_FG">
		<texturefocus border="14" colordiffuse="$VAR[AG_Accent]">fg/r14.png</texturefocus>
		<texturenofocus colordiffuse="00ffffff">common/white.png</texturenofocus>
	</include>'''


def keys():
    t = io.open(PD, encoding='utf-8').read()
    if 'name="Dlg_Tex_Key_FG"' in t:
        print('rounded keys already in place')
        return
    assert t.count(KEY_OLD) == 1, 'key textures'
    io.open(PD, 'w', encoding='utf-8', newline='\n').write(t.replace(KEY_OLD, KEY_NEW))
    print('rounded keys written')


# The number pad (DialogNumeric: PINs, times, the IP address): its input field was a rounded 1 px outline in every
# theme. Fused Glass: the keyboard's rounded input well (radius 20). Aeon menus (square flush boxes): a flush deep box.
# Glass / Fuse keep the outline.
PN = os.path.join('1080i', 'Includes_Keyboard.xml')  # 0.55.0: Num_Classic (was DialogNumeric.xml)
FIELD_OLD = '''				<texture border="10" colordiffuse="$VAR[AG_Line2]">common/rect_outline_1.png</texture>
			</control>
			<control type="label" id="4">'''
FIELD_NEW = '''				<texture border="10" colordiffuse="$VAR[AG_Line2]">common/rect_outline_1.png</texture>
				<visible>!Skin.HasSetting(aeon.fglass) + !$EXP[Aeon_MS]</visible>
			</control>
			<!-- 0.53.2 (_src/fg_keyboard.py): the field in Fused Glass (rounded well) and the Aeon menus (flush deep box) -->
			<control type="image">
				<left>dialog_pad</left><top>dialog_content_top</top><width>560</width><height>76</height>
				<texture border="20" colordiffuse="1affffff">fg/r20.png</texture>
				<visible>Skin.HasSetting(aeon.fglass)</visible>
			</control>
			<control type="image">
				<left>dialog_pad</left><top>dialog_content_top</top><width>560</width><height>76</height>
				<texture border="20" colordiffuse="33ffffff">fg/e20.png</texture>
				<visible>Skin.HasSetting(aeon.fglass)</visible>
			</control>
			<control type="image">
				<left>dialog_pad</left><top>dialog_content_top</top><width>560</width><height>76</height>
				<texture colordiffuse="x_deep">common/white.png</texture>
				<visible>!Skin.HasSetting(aeon.fglass) + $EXP[Aeon_MS]</visible>
			</control>
			<control type="label" id="4">'''


def numpad():
    t = io.open(PN, encoding='utf-8').read()
    if '0.53.2 (_src/fg_keyboard.py)' in t:
        print('number pad field already in place')
        return
    assert t.count(FIELD_OLD) == 1, 'number pad field'
    io.open(PN, 'w', encoding='utf-8', newline='\n').write(t.replace(FIELD_OLD, FIELD_NEW))
    print('number pad field written')


def main():
    keys()
    numpad()
    t = io.open(P, encoding='utf-8').read()
    if MARK in t:
        print('keyboard card already in place')
        return
    assert t.count(SLAB) == 1, 'slab'
    # the slab only outside Fused Glass; the card is drawn before it in Fused Glass
    t = t.replace(SLAB, CARD + SLAB.replace('<height>672</height>', '<height>672</height>\n\t\t\t\t<visible>!Skin.HasSetting(aeon.fglass)</visible>'), 1)
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    print('keyboard card written')


if __name__ == '__main__':
    main()
