"""0.56.45 Skin settings > Home menu > Start on (the user, 2026-11-18: "an option to set a home item as default landing
after splash screen goes away. so a user can pick for instance System as starting point after a reboot"): row 9519
after Add item; OK lists the shown Home menu items (helper startitem: Skin.String(aeon.startitem) = the key,
aeon.startitem.label = its name), Default = Home as Kodi opens it. The helper's service moves the menu there once per
start, when the splash has gone (service.StartItem). Run from the skin folder. Repeatable."""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import settings_sections as ss  # noqa: E402

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'SkinSettings.xml')
SUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'Includes_Aeon_Sub.xml')
RID = 9519
ROW = '''
				<control type="group"><!-- 0.56.45 startitem: Start on -->
					<width>1100</width><height>54</height>
					<control type="image"><left>41</left><top>53</top><width>1019</width><height>1</height><texture colordiffuse="30ffffff">common/white.png</texture><visible>[!$EXP[Aeon_Fused]] + !$EXP[Aeon_FGlass] + !$EXP[Aeon_MS]</visible></control>
					<control type="image"><left>1</left><top>-34</top><width>1099</width><height>134</height><texture border="56" colordiffuse="$VAR[FG_ShadowColM]">fg/sh16.png</texture><visible>[Control.HasFocus(9519)] + $EXP[Aeon_FGlass] + $EXP[FGS_ShadowOn]</visible><include>FG_LandShadowVisible</include></control>
					<control type="image"><left>41</left><top>0</top><width>1019</width><height>54</height><texture border="20" colordiffuse="$VAR[Aeon_MenuFocusColR]">$VAR[FGS_Aeon_MenuFocusTex]</texture><visible>Control.HasFocus(9519)</visible><animation effect="zoom" start="100,100" end="102.355,100.000" center="auto" time="0" condition="$EXP[Aeon_FGlass] + $EXP[FG_FocusFlat]">Conditional</animation></control>
					<control type="button" id="9519">
						<left>41</left><top>0</top><width>1019</width><height>54</height>
						<label></label><texturefocus /><texturenofocus />
						<onup>9639</onup>
						<ondown condition="$EXP[Aeon_MenuTail1]">9590</ondown><ondown>noop</ondown>
						<onback>9558</onback><onleft>SetFocus(9558)</onleft><onright>noop</onright>
						<onfocus>SetProperty(aeon.editrow,9519,home)</onfocus>
						<onclick>RunScript(script.aeon.helper,startitem)</onclick>
					</control>
					<control type="image"><left>163</left><top>3</top><width>48</width><height>48</height><texture colordiffuse="99ffffff">aeon/icons/home.png</texture><visible>!Control.HasFocus(9519)</visible></control>
					<control type="image"><left>163</left><top>3</top><width>48</width><height>48</height><texture colordiffuse="$VAR[FGS_Aeon_OnBarInk]">aeon/icons/home.png</texture><visible>Control.HasFocus(9519)</visible></control>
					<control type="label"><left>210</left><top>0</top><width>400</width><height>54</height><aligny>center</aligny><font>st_ui_24_semibold</font><textcolor>99ffffff</textcolor><label>$ADDON[skin.aeon.fuse 32749]</label><visible>!Control.HasFocus(9519)</visible></control>
					<control type="label"><left>210</left><top>0</top><width>400</width><height>54</height><aligny>center</aligny><font>st_ui_24_bold</font><textcolor>$VAR[FGS_Aeon_OnBarInk]</textcolor><label>$ADDON[skin.aeon.fuse 32749]</label><visible>Control.HasFocus(9519)</visible></control>
					<control type="label"><left>560</left><top>0</top><width>440</width><height>54</height><align>right</align><aligny>center</aligny><font>st_small_20_semibold</font><textcolor>ccffffff</textcolor><label>$VAR[Aeon_StartItemName]</label><visible>!Control.HasFocus(9519)</visible></control>
					<control type="label"><left>560</left><top>0</top><width>440</width><height>54</height><align>right</align><aligny>center</aligny><font>st_small_20_semibold</font><textcolor>$VAR[FGS_Aeon_OnBarInk]</textcolor><label>$VAR[Aeon_StartItemName]</label><visible>Control.HasFocus(9519)</visible></control>
				</control>'''
VARS = '''	<!-- 0.56.45 startitem: Skin settings > Home menu > Start on -->
	<variable name="Aeon_StartItemName">
		<value condition="!String.IsEmpty(Skin.String(aeon.startitem.label))">$INFO[Skin.String(aeon.startitem.label)]</value>
		<value>$LOCALIZE[31546]</value>
	</variable>
	<variable name="Aeon_HomeMenuHint">
		<value condition="Control.HasFocus(9519)">$ADDON[skin.aeon.fuse 32750]</value>
		<value>$LOCALIZE[31671]</value>
	</variable>
'''


def main():
    t = io.open(P, encoding='utf-8').read()
    if 'id="9519"' in t:
        print('startitem: already there')
        return
    m = ss.masked(t)
    s = t.index('<control type="grouplist" id="9641">')
    e = ss.ctl_end(m, s)
    a, b = ss.children(m, s, e)[-1]
    assert 'id="9639"' in t[a:b]
    t = t[:b] + ROW + t[b:]
    old = '<ondown condition="$EXP[Aeon_MenuTail1]">9590</ondown><ondown>noop</ondown>\n\t\t\t\t\t\t<onback>9558</onback><onleft>SetFocus(9558)</onleft><onright>noop</onright>\n\t\t\t\t\t\t<onfocus>SetProperty(aeon.editrow,9639,home)</onfocus>'
    assert t.count(old) == 1
    t = t.replace(old, old.replace('<ondown condition="$EXP[Aeon_MenuTail1]">9590</ondown><ondown>noop</ondown>', '<ondown>9519</ondown>'))
    hint = '<font>st_small_20</font><textcolor>66ffffff</textcolor><label>$LOCALIZE[31671]</label>'
    assert t.count(hint) == 1, t.count(hint)
    t = t.replace(hint, hint.replace('$LOCALIZE[31671]', '$VAR[Aeon_HomeMenuHint]'))
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    x = io.open(SUB, encoding='utf-8').read()
    if 'Aeon_StartItemName' not in x:
        i = x.index('\t<variable name="Aeon_VOS_ratings">')
        x = x[:i] + VARS + x[i:]
        io.open(SUB, 'w', encoding='utf-8', newline='\n').write(x)
    print('startitem: row 9519 after Add item')


if __name__ == '__main__':
    main()
