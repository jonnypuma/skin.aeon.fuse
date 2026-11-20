"""0.39.8 Background progress (DialogExtendedProgressBar: PVR channel / guide loading after a boot, library scans,
add-on updates), Fused Glass: it had only the Aeon bar and the Glass gradient, so Fused Glass showed the Glass
gradient. Now the Fused toast capsule (576 x 64, r32, beside the clock capsule; docked like the toast in library
windows and without a clock): the spinner in a 40 px disc 12 px inside the round end (concentric, 32 - 12), heading and
percent, the current item under them, the progress revealed from the left inside the capsule (control 32 through a
load-time include: Kodi writes the percentage into id 32). Below a toast it drops under it.
Run in 1080i."""
import io

p = 'DialogExtendedProgressBar.xml'
s = io.open(p, encoding='utf-8').read()
FG = '$EXP[Aeon_FGlass]'


def once(old, new):
    global s
    assert s.count(old) == 1, old[:80]
    s = s.replace(old, new)


SLIDES = ('<animation effect="slide" end="232,-16" time="0" condition="!$EXP[Aeon_HomeAny] + $EXP[FG_RailClock]">Conditional</animation>'
          '<animation effect="slide" end="248,0" time="0" condition="!$EXP[Aeon_HomeAny] + !$EXP[Aeon_HasClockBox]">Conditional</animation>')
once('''			<animation effect="slide" end="100,0" time="0" condition="!$EXP[Aeon_HasClockBox] + !$EXP[Aeon_HomeClock] + ![$EXP[Aeon_VGlass] + Window.IsActive(home)]">Conditional</animation>
			<animation effect="slide" end="0,116" time="150" tween="cubic" easing="out" condition="Window.IsVisible(notification)">Conditional</animation>
			<animation type="WindowOpen" condition="!Skin.HasSetting(aeon.reducemotion)">
				<effect type="slide" start="640,0" end="0,0" time="300" tween="cubic" easing="out"/>
			</animation>
			<animation type="WindowClose" condition="!Skin.HasSetting(aeon.reducemotion)">
				<effect type="slide" start="0,0" end="640,0" time="200" tween="cubic" easing="in"/>
			</animation>''', '''			<animation effect="slide" end="100,0" time="0" condition="!$EXP[Aeon_HasClockBox] + !$EXP[Aeon_HomeClock] + ![$EXP[Aeon_VGlass] + Window.IsActive(home)] + !%(fg)s">Conditional</animation>
			<animation effect="slide" end="0,116" time="150" tween="cubic" easing="out" condition="Window.IsVisible(notification) + !%(fg)s">Conditional</animation>
			<animation effect="slide" end="0,72" time="150" tween="cubic" easing="out" condition="Window.IsVisible(notification) + %(fg)s">Conditional</animation>
			<animation type="WindowOpen" condition="!Skin.HasSetting(aeon.reducemotion) + !%(fg)s">
				<effect type="slide" start="640,0" end="0,0" time="300" tween="cubic" easing="out"/>
			</animation>
			<animation type="WindowClose" condition="!Skin.HasSetting(aeon.reducemotion) + !%(fg)s">
				<effect type="slide" start="0,0" end="640,0" time="200" tween="cubic" easing="in"/>
			</animation>
			<animation type="WindowOpen" condition="!Skin.HasSetting(aeon.reducemotion) + %(fg)s">
				<effect type="slide" start="120,0" end="0,0" time="250" tween="cubic" easing="out"/>
				<effect type="fade" start="0" end="100" time="200"/>
			</animation>
			<animation type="WindowClose" condition="!Skin.HasSetting(aeon.reducemotion) + %(fg)s">
				<effect type="slide" start="0,0" end="120,0" time="180" tween="cubic" easing="in"/>
				<effect type="fade" start="100" end="0" time="160"/>
			</animation>''' % {'fg': FG})
once('''			<!-- ================= Glass -->
			<control type="group">
				<visible>$EXP[Aeon_VGlass]</visible>''', '''			<!-- ================= Fused Glass (0.39.8): the toast capsule, the progress filling it -->
			<control type="group">
				<visible>%(fg)s</visible>
				%(slides)s
				<control type="image"><left>-180</left><top>40</top><width>576</width><height>64</height><texture border="32" colordiffuse="fg_frost2">fg/r32.png</texture></control>
			</control>
			<include>FG_ExtProg32</include>
			<control type="group">
				<visible>%(fg)s</visible>
				%(slides)s
				<control type="image"><left>-180</left><top>40</top><width>576</width><height>64</height><texture border="32" colordiffuse="fg_edge">fg/e32.png</texture></control>
				<control type="image"><left>-168</left><top>52</top><width>40</width><height>40</height><texture colordiffuse="1fffffff">fg/circle.png</texture></control>
				<control type="image"><left>-162</left><top>58</top><width>28</width><height>28</height><texture colordiffuse="ffffffff">common/aeon_spinner.gif</texture><visible>!Skin.HasSetting(aeon.reducemotion)</visible></control>
				<control type="image"><left>-162</left><top>58</top><width>28</width><height>28</height><texture colordiffuse="ffffffff">common/aeon_spinner_still.png</texture><visible>Skin.HasSetting(aeon.reducemotion)</visible></control>
				<control type="label"><left>-112</left><top>45</top><width>400</width><height>24</height><font>cap_20</font><textcolor>a3ffffff</textcolor><label>$INFO[Control.GetLabel(30)]</label></control>
				<control type="label"><left>292</left><top>45</top><width>84</width><height>24</height><align>right</align><font>num_20</font><textcolor>a3ffffff</textcolor><label>$INFO[Control.GetLabel(32),,%%]</label></control>
				<control type="fadelabel"><left>-112</left><top>67</top><width>488</width><height>32</height><font>ui_22</font><textcolor>ffffffff</textcolor><label>$INFO[Control.GetLabel(31)]</label><scrollout>false</scrollout><pauseatend>2000</pauseatend></control>
			</control>

			<!-- ================= Glass -->
			<control type="group">
				<visible>$EXP[Aeon_VGlass] + !%(fg)s</visible>''' % {'fg': FG, 'slides': SLIDES})
# control 32: the old line elsewhere, the capsule fill in Fused Glass (load-time include, one id 32)
a = s.index('\t\t\t<control type="progress" id="32">')
b = s.index('\n\t\t\t</control>', a) + len('\n\t\t\t</control>')
old32 = s[a:b]
s = s[:a] + '\t\t\t<include condition="!Skin.HasSetting(aeon.fglass)">FG_ExtProg32_old</include>' + s[b:]
once('''		<control type="group">
			<visible>$EXP[Aeon_HasClockBox] + !Window.IsVisible(notification)</visible>''', '''		<control type="group">
			<visible>$EXP[Aeon_HasClockBox] + !Window.IsVisible(notification) + !%s</visible>''' % FG)
once('''		<control type="group">
			<visible>!Window.IsVisible(notification)</visible>
			<include>Aeon_HomeClockOver</include>''', '''		<control type="group">
			<visible>!Window.IsVisible(notification) + !%s</visible>
			<include>Aeon_HomeClockOver</include>''' % FG)
io.open(p, 'w', encoding='utf-8', newline='').write(s)

f = 'Includes_Fused.xml'
t = io.open(f, encoding='utf-8').read()
assert 'FG_ExtProg32' not in t
old32_body = '\n'.join(l[1:] if l.startswith('\t') else l for l in old32.split('\n'))
t = t.replace('</includes>', '''	<!-- 0.39.8 background progress (DialogExtendedProgressBar): control 32, the line (old) or the capsule fill (Fused Glass) -->
	<include name="FG_ExtProg32">
		<include condition="Skin.HasSetting(aeon.fglass)">FG_ExtProg32_fg</include>
	</include>
	<include name="FG_ExtProg32_fg">
		<control type="progress" id="32">
			<left>-180</left><top>40</top><width>576</width><height>64</height>
			%s
			<reveal>true</reveal>
			<texturebg border="32" colordiffuse="00ffffff">fg/r32.png</texturebg>
			<midtexture border="32" colordiffuse="1fffffff">fg/r32.png</midtexture>
		</control>
	</include>
	<include name="FG_ExtProg32_old">
%s
	</include>
</includes>''' % (SLIDES, old32_body))
io.open(f, 'w', encoding='utf-8', newline='').write(t)
print('ok')
