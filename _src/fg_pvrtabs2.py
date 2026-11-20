"""0.39.3 TV / Radio area tabs, second pass:
- Left / Right did not switch areas: the tabs sat in a grouplist, which links its children left / right itself, and the
  per-area navigation came in through an include named with $PARAM. The tabs now sit in a plain group (id 9000, still
  Kodi's menucontrol) at fixed places, and each tab gets its own Left / Right actions through plain params.
- The white focus pill was smaller than the grey pill of the open area: the focus textures (fxb_*.png) carry a shadow
  margin (4 px left / right, 2 px top, 8 px bottom). In Fused Glass the tab draws no focus texture itself; the card
  draws the pill in the focus style the user picked, placed so its body covers exactly the 196 x 44 tab, so the label
  sits in its middle. Other themes keep the row focus texture.
Run in 1080i."""
import io

AREAS = (('Channels', 100, 19019, '$LOCALIZE'), ('Guide', 101, 19069, '$LOCALIZE'), ('Recordings', 102, 19017, '$LOCALIZE'),
         ('Timers', 103, 19040, '$LOCALIZE'), ('TimerRules', 104, 19138, '$LOCALIZE'), ('Search', 105, 137, '$LOCALIZE'))
TAB_W, GAP, TAB_H = 196, 8, 44
SET = 'SetProperty(aeon.pvrnav,1,home)'

p = 'Includes_Misc.xml'
s = io.open(p, encoding='utf-8').read()

# 1. the tab button: fixed place, its own Left / Right
a = s.index('\t<include name="Misc_PVRAreaButton">')
b = s.index('\t<include name="Misc_PVRNav_Search">')
b = s.index('\n\t</include>', b) + len('\n\t</include>')
s = s[:a] + '''	<include name="Misc_PVRAreaButton">
		<definition>
			<control type="button" id="$PARAM[id]">
				<left>$PARAM[x]</left>
				<top>8</top>
				<width>%(w)d</width>
				<height>%(h)d</height>
				<align>center</align>
				<aligny>center</aligny>
				<font>cap_20</font>
				<textcolor>$VAR[AG_Ink2]</textcolor>
				<focusedcolor>$VAR[Aeon_OnBarInk]</focusedcolor>
				<include>FG_PVRTabFocus</include>
				<texturenofocus />
				<label>$PARAM[label]</label>
				<onclick condition="String.IsEmpty(Window.Property(IsRadio)) + !Window.IsActive(TV$PARAM[area])">ActivateWindow(TV$PARAM[area])</onclick>
				<onclick condition="!String.IsEmpty(Window.Property(IsRadio)) + !Window.IsActive(Radio$PARAM[area])">ActivateWindow(Radio$PARAM[area])</onclick>
				<onclick condition="Window.IsActive(TV$PARAM[area]) | Window.IsActive(Radio$PARAM[area])">SetFocus(9100)</onclick>
				<!-- 0.39.3: Left / Right go straight to the next area, the focus stays on the tabs there -->
				<onleft>$PARAM[left_set]</onleft>
				<onleft condition="String.IsEmpty(Window.Property(IsRadio))">$PARAM[left_tv]</onleft>
				<onleft condition="!String.IsEmpty(Window.Property(IsRadio))">$PARAM[left_radio]</onleft>
				<onright>$PARAM[right_set]</onright>
				<onright condition="String.IsEmpty(Window.Property(IsRadio))">$PARAM[right_tv]</onright>
				<onright condition="!String.IsEmpty(Window.Property(IsRadio))">$PARAM[right_radio]</onright>
				<onup>noop</onup>
				<ondown>9001</ondown>
				<onback>$PARAM[back]</onback>
			</control>
		</definition>
	</include>''' % {'w': TAB_W, 'h': TAB_H} + s[b:]

# 2. the row: one group (id 9000) with the card, the open area's pill, the focus pill and the tabs
a = s.index('\t\t\t<!-- 0.39.3: the areas as tabs on a card')
b = s.index('\t\t\t<control type="grouplist" id="9001">', a)
card_w = len(AREAS) * TAB_W + (len(AREAS) - 1) * GAP + 16
rows = []
for i, (area, cid, _n, _l) in enumerate(AREAS):
    x = 8 + i * (TAB_W + GAP)
    rows.append('\t\t\t\t<control type="image"><left>%d</left><top>8</top><width>%d</width><height>%d</height><texture border="22" colordiffuse="$VAR[Misc_PVRTabSel]">fg/r22.png</texture><visible>[Window.IsActive(TV%s) | Window.IsActive(Radio%s)] + !Control.HasFocus(%d)</visible></control>'
                % (x, TAB_W, TAB_H, area, area, cid))
for i, (area, cid, _n, _l) in enumerate(AREAS):
    x = 8 + i * (TAB_W + GAP)
    rows.append('\t\t\t\t<control type="image"><left>%d</left><top>6</top><width>%d</width><height>%d</height><texture border="20,18,20,24">$VAR[Misc_PVRTabFocusTex]</texture><visible>$EXP[Aeon_FGlass] + Control.HasFocus(%d) + !String.IsEqual(Skin.String(aeon.fgfocus),flat)</visible><include>FG_LandVisible</include></control>'
                % (x - 4, TAB_W + 8, TAB_H + 10, cid))
    rows.append('\t\t\t\t<control type="image"><left>%d</left><top>8</top><width>%d</width><height>%d</height><texture>fg/fxb_flat.png</texture><visible>$EXP[Aeon_FGlass] + Control.HasFocus(%d) + String.IsEqual(Skin.String(aeon.fgfocus),flat)</visible><include>FG_LandVisible</include></control>'
                % (x, TAB_W, TAB_H, cid))
tabs = []
for i, (area, cid, num, loc) in enumerate(AREAS):
    x = 8 + i * (TAB_W + GAP)
    prev = AREAS[i - 1][0] if i else None
    nxt = AREAS[i + 1][0] if i + 1 < len(AREAS) else None
    params = [('id', str(cid)), ('area', area), ('label', '%s[%d]' % (loc, num)), ('x', str(x)),
              ('left_set', SET if prev else 'noop'), ('left_tv', 'ReplaceWindow(TV%s)' % prev if prev else 'noop'),
              ('left_radio', 'ReplaceWindow(Radio%s)' % prev if prev else 'noop'),
              ('right_set', SET if nxt else 'noop'), ('right_tv', 'ReplaceWindow(TV%s)' % nxt if nxt else 'noop'),
              ('right_radio', 'ReplaceWindow(Radio%s)' % nxt if nxt else 'noop'), ('back', '$PARAM[content_id]')]
    tabs.append('\t\t\t\t<include content="Misc_PVRAreaButton">\n' + ''.join(
        '\t\t\t\t\t<param name="%s" value="%s"/>\n' % kv for kv in params) + '\t\t\t\t</include>')
block = '''			<!-- 0.39.3: the areas as tabs on a card (Fused Glass; flat elsewhere). A plain group, not a grouplist: a grouplist
			     links its children left / right itself, and here Left / Right switch areas. The open area has a light pill
			     while the focus is elsewhere; in Fused Glass the focus pill is drawn here too, its body exactly on the tab. -->
			<control type="group" id="9000">
				<left>102</left><top>128</top>
				<width>%(cw)d</width><height>60</height>
				<control type="image"><left>-32</left><top>-24</top><width>%(cw64)d</width><height>124</height><texture border="56" colordiffuse="66000000">fg/sh16.png</texture><visible>$EXP[Aeon_FGlass]</visible></control>
				<control type="image"><width>%(cw)d</width><height>60</height><texture border="28" colordiffuse="fg_frost">fg/r28.png</texture><visible>$EXP[Aeon_FGlass]</visible></control>
				<control type="image"><width>%(cw)d</width><height>60</height><texture border="28" colordiffuse="fg_edge">fg/e28.png</texture><visible>$EXP[Aeon_FGlass]</visible></control>
%(rows)s
%(tabs)s
			</control>
''' % {'cw': card_w, 'cw64': card_w + 64, 'rows': '\n'.join(rows), 'tabs': '\n'.join(tabs)}
s = s[:a] + block + s[b:]
io.open(p, 'w', encoding='utf-8', newline='').write(s)

p = 'Includes_Fused.xml'
t = io.open(p, encoding='utf-8').read()
assert 'FG_PVRTabFocus' not in t
t = t.replace('''	<include name="FG_SubNavNoFocus_old"><texturenofocus /></include>''', '''	<include name="FG_SubNavNoFocus_old"><texturenofocus /></include>
	<!-- the area tabs: in Fused Glass the card draws the focus pill (exactly on the tab), so the tab itself draws none -->
	<include name="FG_PVRTabFocus">
		<include condition="Skin.HasSetting(aeon.fglass)">FG_PVRTabFocus_fg</include>
		<include condition="!Skin.HasSetting(aeon.fglass)">Aeon_TexRowFocus</include>
	</include>
	<include name="FG_PVRTabFocus_fg"><texturefocus /></include>
	<variable name="Misc_PVRTabFocusTex">
		<value condition="String.IsEqual(Skin.String(aeon.fgfocus),tight)">fg/fxb_tight.png</value>
		<value condition="String.IsEqual(Skin.String(aeon.fgfocus),frost)">fg/fxb_frost.png</value>
		<value condition="String.IsEqual(Skin.String(aeon.fgfocus),outline)">fg/fxb_outline.png</value>
		<value>fg/fxb_pill.png</value>
	</variable>''', 1)
assert 'FG_PVRTabFocus' in t
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('ok', card_w)
