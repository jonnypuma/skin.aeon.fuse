"""0.42.0 Fused Glass Home > Power (mockup board Power): writes include FG_H_PowerPage into 1080i/Includes_Fused.xml
(between FG_POWER markers), turns Aeon_H_PowerPage into load-time variants (classic = Aeon_H_PowerPage_Classic) and
points Down from the Power item at the new row in Fused Glass. Run from the skin folder."""
import io
import re

FUSED = '1080i/Includes_Fused.xml'
HOME = '1080i/Includes_Aeon_Home.xml'
CE = 'System.HasAddon(service.coreelec.settings)'
ARMED = 'String.IsEqual(Window(Home).Property(aeon.pw.arm),1)'
A = '$ADDON[skin.aeon.fuse %d]'

PILLS = [  # id, label, actions, visible
    (93411, '$LOCALIZE[351]', ['CancelAlarm(shutdowntimer,true)'], 'true'),
    (93412, '30 ' + A % 32501, ['CancelAlarm(shutdowntimer,true)', 'AlarmClock(shutdowntimer,Shutdown(),30,true)'], 'true'),
    (93413, '60 ' + A % 32501, ['CancelAlarm(shutdowntimer,true)', 'AlarmClock(shutdowntimer,Shutdown(),60,true)'], 'true'),
    (93414, '90 ' + A % 32501, ['CancelAlarm(shutdowntimer,true)', 'AlarmClock(shutdowntimer,Shutdown(),90,true)'], 'true'),
    (93415, '120 ' + A % 32501, ['CancelAlarm(shutdowntimer,true)', 'AlarmClock(shutdowntimer,Shutdown(),120,true)'], 'true'),
    (93416, A % 32500, ['CancelAlarm(shutdowntimer,true)', 'AlarmClock(shutdowntimer,Shutdown(),$INFO[Player.TimeRemaining(mins)],true)'], 'Player.HasVideo + !Pvr.IsPlayingTv'),
]
BUTTONS = [  # id, icon, label, sub, actions, visible
    (93421, 'aeon/icons/clock.png', '$LOCALIZE[20144]', '$VAR[FG_PwTimerSub]', ['SetFocus(9341)'], 'true'),
    (93422, 'aeon/icons/moon.png', A % 32492, '', ['Suspend()'], 'true'),
    (93423, 'fg/pw_refresh.png', A % 32493, '', ['RestartApp()'], 'true'),
    (93424, 'fg/pw_restart.png', '$LOCALIZE[13013]', '', ['Reboot()'], 'true'),
    (93425, 'fg/pw_android.png', A % 32495, 'CoreELEC', ['RunScript(script.aeon.helper,android)'], CE),
    (93426, 'aeon/icons/power.png', A % 32496, '$VAR[FG_PwOffSub]', None, 'true'),
    (93427, 'fg/pw_logout.png', A % 32498, A % 32499, ['Quit()'], 'true'),
    (93428, 'fg/pw_screen.png', '$LOCALIZE[360]', '', ['ActivateScreensaver'], 'true'),
]


def pill(ident, label, actions, visible):
    acts = ''.join('<onclick>%s</onclick>' % a for a in actions)
    return ('\t\t\t\t\t<control type="button" id="%d"><width min="96" max="420">auto</width><height>56</height><label>%s</label>'
            '<font>hm_ui_24</font><align>center</align><aligny>center</aligny><textoffsetx>28</textoffsetx>'
            '<textcolor>ffffffff</textcolor><focusedcolor>aeon_onbar</focusedcolor><include>FG_PillBtnTex</include>%s'
            '<onup>noop</onup><ondown>93421</ondown><onback>93421</onback><visible>%s</visible></control>\n'
            % (ident, label, acts, visible))


def button(ident, icon, label, sub, actions, visible):
    off = ident == 93426
    if off:
        acts = ('<onclick condition="%s">Shutdown()</onclick>'
                '<onclick condition="!%s">SetProperty(aeon.pw.arm,1,home)</onclick>'
                '<onclick condition="!%s">AlarmClock(aeonpwarm,ClearProperty(aeon.pw.arm,home),00:06,silent)</onclick>' % (ARMED, ARMED, ARMED))
        focus = ''
    else:
        acts = ''.join('<onclick>%s</onclick>' % a for a in actions)
        focus = '<onfocus>ClearProperty(aeon.pw.arm,home)</onfocus>'
    ids = [b[0] for b in BUTTONS]
    k = ids.index(ident)
    def nav(tag, other):
        if other == 93425:                      # Reboot to Android: CoreELEC only, else skip it
            alt = ids[(ids.index(93425) + (1 if tag == 'onright' else -1)) % len(ids)]
            return '<%s condition="%s">%d</%s><%s condition="!%s">%d</%s>' % (tag, CE, other, tag, tag, CE, alt, tag)
        return '<%s>%d</%s>' % (tag, other, tag)
    focus += nav('onleft', ids[(k - 1) % len(ids)]) + nav('onright', ids[(k + 1) % len(ids)])
    ink = 'ffc4373c' if off else 'aeon_onbar'
    # 0.46.0: a solid ring in the accent (red for Shut down) round the white focus disc; the 35 % glow read brown
    glow = ('<control type="image"><left>29</left><top>5</top><width>154</width><height>154</height><texture colordiffuse="%s">fg/circle.png</texture>'
            '<visible>Control.HasFocus(%d)</visible></control>' % ('ffe5484d' if off else 'fg_mark', ident))
    return '''				<control type="group">
					<width>212</width><height>250</height>
					<visible>%(vis)s</visible>
					%(glow)s<control type="image"><left>42</left><top>18</top><width>128</width><height>128</height><texture colordiffuse="fg_frost">fg/circle.png</texture><visible>!Control.HasFocus(%(id)d)</visible></control>
					<control type="image"><left>42</left><top>18</top><width>128</width><height>128</height><texture colordiffuse="fg_edge">fg/circle_edge.png</texture><visible>!Control.HasFocus(%(id)d)</visible></control>
					<control type="button" id="%(id)d">
						<left>36</left><top>12</top><width>140</width><height>140</height><label></label>
						<texturefocus colordiffuse="ffffffff">fg/circle.png</texturefocus><texturenofocus />
						%(acts)s%(focus)s
						<onup>ClearProperty(aeon.pw.arm,home)</onup><onup>9000</onup>
						<ondown>noop</ondown>
						<onback>ClearProperty(aeon.pw.arm,home)</onback><onback>9000</onback>
					</control>
					<control type="image"><left>82</left><top>58</top><width>48</width><height>48</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">%(icon)s</texture><visible>!Control.HasFocus(%(id)d)</visible></control>
					<control type="image"><left>82</left><top>58</top><width>48</width><height>48</height><aspectratio>keep</aspectratio><texture colordiffuse="%(ink)s">%(icon)s</texture><visible>Control.HasFocus(%(id)d)</visible></control>
					<control type="label"><left>0</left><top>166</top><width>212</width><height>32</height><align>center</align><aligny>center</aligny><font>hm_ui_22_semibold</font><textcolor>ffffffff</textcolor><label>%(label)s</label></control>
					<control type="label"><left>0</left><top>198</top><width>212</width><height>28</height><align>center</align><aligny>center</aligny><font>hm_small_20</font><textcolor>9effffff</textcolor><label>%(sub)s</label></control>
				</control>
''' % {'id': ident, 'icon': icon, 'label': label, 'sub': sub, 'acts': acts, 'focus': focus, 'vis': visible, 'ink': ink, 'glow': glow}


BODY = '''	<!-- FG_POWER:begin (written by _src/fg_home_power.py) ======================= Home > Power, Fused Glass (0.42.0)
	     Over the Power picture: the date, a big clock, how long Kodi and the machine have been running and what plays,
	     and the shutdown timer (pills, 9341). Under the menu round actions (9342; Down from the Power item): Shutdown
	     timer (goes up to the pills), Sleep, Restart Kodi, Reboot, Reboot to Android (CoreELEC), Shut down (OK twice),
	     Log off (exits Kodi), Screensaver. Up from the Power item still opens the Power card (9339). -->
	<variable name="FG_PwTimerSub">
		<value condition="System.HasAlarm(shutdowntimer)">$INFO[System.Alarmpos]</value>
		<value>$LOCALIZE[351]</value>
	</variable>
	<variable name="FG_PwOffSub">
		<value condition="%(armed)s">$ADDON[skin.aeon.fuse 32497]</value>
	</variable>
	<variable name="FG_PwPlaying">
		<value condition="Player.HasMedia">$INFO[Player.Title]</value>
		<value>$ADDON[skin.aeon.fuse 32491]</value>
	</variable>
	<include name="FG_H_PowerPage">
		<control type="group">
			<include>Aeon_LowBand</include>
			<visible>$EXP[Aeon_H_PowerSec] + [Control.HasFocus(9000) | ControlGroup(9341).HasFocus() | ControlGroup(9342).HasFocus() | Control.HasFocus(9339)]</visible>
			<animation type="Visible" tween="cubic" easing="out" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" delay="200" time="300"/><effect type="slide" start="0,24" end="0,0" delay="200" time="300"/></animation>
			<animation type="Hidden"><effect type="fade" start="100" end="0" time="150"/></animation>
			<control type="label"><left>120</left><top>106</top><width>900</width><height>32</height><aligny>center</aligny><font>hm_cap_20</font><textcolor>b3ffffff</textcolor><label>[UPPERCASE]$INFO[System.Date(DDDD d MMMM)][/UPPERCASE]</label></control>
			<control type="label"><left>110</left><top>128</top><width>1100</width><height>196</height><aligny>center</aligny><font>hm_display_160</font><textcolor>ffffffff</textcolor><label>$INFO[System.Time(HH:mm)]</label></control>
			<control type="label"><left>120</left><top>318</top><width>1240</width><height>36</height><aligny>center</aligny><font>hm_ui_24</font><textcolor>dbffffff</textcolor>
				<label>$ADDON[skin.aeon.fuse 32489] $VAR[Aeon_Uptime]$INFO[Window(Home).Property(aeon.boxuptime),  ·  $ADDON[skin.aeon.fuse 32490] ,]  ·  $VAR[FG_PwPlaying]</label></control>
			<control type="label"><left>120</left><top>392</top><width>1100</width><height>28</height><aligny>center</aligny><font>hm_cap_20</font><textcolor>b3ffffff</textcolor><label>[UPPERCASE]$LOCALIZE[20144]$INFO[System.Alarmpos,  ·  ,][/UPPERCASE]</label></control>
			<control type="grouplist" id="9341">
				<left>112</left><top>428</top><width>1300</width><height>60</height>
				<orientation>horizontal</orientation><itemgap>12</itemgap>
				<onup>noop</onup><ondown>93421</ondown>
%(pills)s			</control>
		</control>
		<control type="group">
			<include>Aeon_LowSubSlide</include>
			<visible>$EXP[Aeon_H_PowerSec] + [Control.HasFocus(9000) | ControlGroup(9341).HasFocus() | ControlGroup(9342).HasFocus()]</visible>
			<animation type="Visible" tween="cubic" easing="out" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" delay="200" time="300"/></animation>
			<animation type="Hidden"><effect type="fade" start="100" end="0" time="150"/></animation>
			<control type="group">
				<include>Aeon_LowSubZoom</include>
				<control type="grouplist" id="9342">
					<left>0</left><top>780</top><width>1920</width><height>250</height>
					<orientation>horizontal</orientation><align>center</align><itemgap>0</itemgap><usecontrolcoords>true</usecontrolcoords>
					<onup>9000</onup>
%(buttons)s				</control>
			</control>
		</control>
	</include>
	<!-- FG_POWER:end -->
''' % {'armed': ARMED, 'pills': ''.join(pill(*p) for p in PILLS), 'buttons': ''.join(button(*b) for b in BUTTONS)}

t = io.open(FUSED, encoding='utf-8').read()
t = re.sub(r'\t<!-- FG_POWER:begin.*?<!-- FG_POWER:end -->\n', '', t, flags=re.S)
if 'Aeon_H_PowerPage_Classic' not in t:
    a = '\t<include name="Aeon_H_PowerPage">\n'
    assert t.count(a) == 1
    t = t.replace(a, '\t<include name="Aeon_H_PowerPage">\n'
                     '\t\t<include condition="Skin.HasSetting(aeon.fglass)">FG_H_PowerPage</include>\n'
                     '\t\t<include condition="!Skin.HasSetting(aeon.fglass)">Aeon_H_PowerPage_Classic</include>\n'
                     '\t</include>\n'
                     '\t<include name="Aeon_H_PowerPage_Classic">\n')
t = t.replace('</includes>', BODY + '</includes>')
io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(t)

h = io.open(HOME, encoding='utf-8').read()
old = '<ondown condition="$EXP[Aeon_H_PowerSec] + !$EXP[Aeon_H_SpotAny]">SetFocus(93081)</ondown>'
if old in h:
    h = h.replace(old, '<ondown condition="$EXP[Aeon_H_PowerSec] + !$EXP[Aeon_H_SpotAny] + !Skin.HasSetting(aeon.fglass)">SetFocus(93081)</ondown>'
                       '<ondown condition="$EXP[Aeon_H_PowerSec] + !$EXP[Aeon_H_SpotAny] + Skin.HasSetting(aeon.fglass)">SetFocus(93421)</ondown>')
    io.open(HOME, 'w', encoding='utf-8', newline='\n').write(h)
import xml.etree.ElementTree as ET
ET.parse(FUSED); ET.parse(HOME)
print('ok')
