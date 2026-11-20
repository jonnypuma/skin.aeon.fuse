"""0.39.9 Busy indicator (DialogBusy: a plugin resolving, e.g. a YouTube trailer, a slow folder), Fused Glass: it was
the Aeon box in the top right corner, half over the clock capsule. Now a capsule like the toast and the background
progress (64 high, r32, frost + edge), docked to the left of the clock capsule where the toast docks (same slides when
the clock sits on the rail or is not there): the spinner in a 40 px disc 12 px inside the round end (concentric,
32 - 12 = 20), "Loading..." (skin string 31952) and Kodi's percentage when it gives one. Below a toast and below the
background progress it drops a row (72) for each. Run in 1080i."""
import io

p = 'DialogBusy.xml'
s = io.open(p, encoding='utf-8').read()
FG = '$EXP[Aeon_FGlass]'


def once(old, new):
    global s
    assert s.count(old) == 1, old[:80]
    s = s.replace(old, new)


once('''	Hidden at start-up and while the player caches (the player shows buffering itself).
-->''', '''	Hidden at start-up and while the player caches (the player shows buffering itself).
	Fused Glass (0.39.9): a capsule beside the clock capsule, like the toast: spinner disc, "Loading...", the percentage.
-->''')
once('''		<control type="group">
			<visible>!Window.IsActive(startup) + !Player.Caching</visible>
			<left>1820</left>''', '''		<control type="group">
			<visible>!Window.IsActive(startup) + !Player.Caching + !%(fg)s</visible>
			<left>1820</left>'''.replace('%(fg)s', FG))
# id 10 lives outside the themed groups (Kodi writes the percentage into it whichever look shows)
once('''			<control type="label" id="10">
				<description>progress % (Kodi)</description>
				<visible>false</visible>
			</control>
		</control>
	</controls>''', '''		</control>
		<control type="label" id="10">
			<description>progress % (Kodi)</description>
			<visible>false</visible>
		</control>

		<!-- ================= Fused Glass (0.39.9) -->
		<control type="group">
			<visible>!Window.IsActive(startup) + !Player.Caching + %(fg)s</visible>
			<left>1288</left>
			<top>40</top>
			<animation effect="slide" end="232,-16" time="0" condition="!$EXP[Aeon_HomeAny] + $EXP[FG_RailClock]">Conditional</animation>
			<animation effect="slide" end="248,0" time="0" condition="!$EXP[Aeon_HomeAny] + !$EXP[Aeon_HasClockBox]">Conditional</animation>
			<animation effect="slide" end="0,72" time="150" tween="cubic" easing="out" condition="Window.IsVisible(notification)">Conditional</animation>
			<animation effect="slide" end="0,72" time="150" tween="cubic" easing="out" condition="Window.IsVisible(extendedprogressdialog)">Conditional</animation>
			<animation type="WindowOpen" condition="!Skin.HasSetting(aeon.reducemotion)">
				<effect type="slide" start="60,0" end="0,0" time="220" tween="cubic" easing="out"/>
			</animation>
			<control type="image"><left>0</left><top>0</top><width>288</width><height>64</height><texture border="32" colordiffuse="fg_panel">fg/r32.png</texture></control>
			<control type="image"><left>0</left><top>0</top><width>288</width><height>64</height><texture border="32" colordiffuse="fg_edge">fg/e32.png</texture></control>
			<control type="image"><left>12</left><top>12</top><width>40</width><height>40</height><texture colordiffuse="1fffffff">fg/circle.png</texture></control>
			<control type="image"><left>18</left><top>18</top><width>28</width><height>28</height><texture colordiffuse="ffffffff">common/aeon_spinner.gif</texture><visible>!Skin.HasSetting(aeon.reducemotion)</visible></control>
			<control type="image"><left>18</left><top>18</top><width>28</width><height>28</height><texture colordiffuse="ffffffff">common/aeon_spinner_still.png</texture><visible>Skin.HasSetting(aeon.reducemotion)</visible></control>
			<control type="label"><left>64</left><top>0</top><width>200</width><height>64</height><aligny>center</aligny><font>ui_22</font><textcolor>ffffffff</textcolor><label>$LOCALIZE[31952][COLOR a3ffffff]$INFO[Control.GetLabel(10),  ,%][/COLOR]</label></control>
		</control>
	</controls>'''.replace('%(fg)s', FG))
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
