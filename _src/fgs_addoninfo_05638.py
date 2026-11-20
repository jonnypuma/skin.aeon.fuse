"""0.56.38 Fused Glass style: the add-on information page (DialogAddonInfo) in the System grid.

The page today (hero card, button row, Description card, Details card) moves unchanged into AddonInfo_Classic
(Includes_Dialogs.xml) for every other theme / style; the style gets FGS_AddonInfo (Includes_Fused.xml):
- header: the add-on's type (light) and name (bold); the clock;
- one grid 360-1560: the icon column holds the add-on's icon (rounded) and its facts under it (version, type,
  installed, updated, status: small capitals and the value, right-aligned to the divider);
- right of the divider: the summary, creator / origin, the lifecycle notice, the description (or What's new) as a
  scrolling text, then the actions as rows (Kodi's ids 12 open, 9 configure, 13 auto-update as the switch, 10
  dependencies, 7 enable / disable, 8 versions, 14 update, 6 install / uninstall, and 9202 What's new) in grouplist 9000,
  70 high with the white bar on the divider; Kodi shows only the ones it enables; Back closes;
- the screenshots panel 50 stays (Kodi fills it) but out of the way (hidden in the style).
Run from the skin folder after fgs_dialogs_05632. Repeatable."""
import io
import os

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
MARK = '<!-- 0.56.38 fgs_addoninfo -->'


def rd(name):
    return io.open(os.path.join(D, name), encoding='utf-8').read()


def wr(name, text):
    io.open(os.path.join(D, name), 'w', encoding='utf-8', newline='\n').write(text)


def fact(label, value):
    """one fact in the facts grouplist: hidden (and closed up) without a value"""
    return ('<control type="group"><width>374</width><height>58</height><visible>!String.IsEmpty(%s)</visible>'
            '<control type="label"><left>0</left><top>0</top><width>374</width><height>24</height><align>right</align><font>st_cap_14</font><textcolor>66ffffff</textcolor><label>[UPPERCASE]%s[/UPPERCASE]</label></control>'
            '<control type="label"><left>0</left><top>22</top><width>374</width><height>30</height><align>right</align><font>st_small_20</font><textcolor>ccffffff</textcolor><label>$INFO[%s]</label></control></control>'
            % (value, label, value))


FGS = '''	%(mark)s
	<include name="FGS_AddonInfo">
		<include content="FGS_DlgHeader"><param name="lead" value="$INFO[ListItem.AddonType]"/><param name="leadvis" value="!String.IsEmpty(ListItem.AddonType)"/><param name="label" value="$INFO[ListItem.AddonName]"/></include>
		<!-- the grid -->
		<control type="image"><left>360</left><top>180</top><width>1200</width><height>1</height><texture colordiffuse="1affffff">common/white.png</texture></control>
		<control type="image"><left>810</left><top>181</top><width>1</width><height>770</height><texture colordiffuse="1affffff">common/white.png</texture></control>
		<!-- the icon column: the icon, its facts under it -->
		<control type="image"><left>594</left><top>212</top><width>180</width><height>180</height><aspectratio align="right" aligny="top">keep</aspectratio><fadetime>150</fadetime><texture background="true" diffuse="fg/m180x180.png">$INFO[ListItem.Art(thumb)]</texture></control>
		<control type="grouplist"><left>400</left><top>410</top><width>374</width><height>540</height><orientation>vertical</orientation><itemgap>0</itemgap><usecontrolcoords>true</usecontrolcoords>
		%(facts)s
		</control>
		<!-- right of the divider: summary, creator, lifecycle, the text -->
		<control type="textbox"><left>846</left><top>200</top><width>678</width><height>72</height><font>st_ui_24_semibold</font><textcolor>eeffffff</textcolor><label>$INFO[ListItem.AddonSummary]</label></control>
		<control type="label"><left>846</left><top>276</top><width>678</width><height>30</height><font>st_small_20</font><textcolor>80ffffff</textcolor><label>$INFO[ListItem.AddonCreator,$ADDON[skin.aeon.fuse 32149] ,]$INFO[ListItem.AddonOrigin,  ·  ,]</label></control>
		<control type="label"><left>846</left><top>306</top><width>678</width><height>30</height><font>st_small_20_bold</font><textcolor>fg_mark</textcolor><label>$INFO[ListItem.AddonLifecycleType]$INFO[ListItem.AddonLifecycleDesc,  ·  ,]</label><visible>String.IsEqual(ListItem.AddonLifecycleType,$LOCALIZE[24170]) | String.IsEqual(ListItem.AddonLifecycleType,$LOCALIZE[24171])</visible></control>
		<control type="label"><left>846</left><top>344</top><width>678</width><height>26</height><font>st_cap_14</font><textcolor>66ffffff</textcolor><label>[UPPERCASE]$VAR[AddonInfo_TextTitle][/UPPERCASE]</label></control>
		<control type="textbox"><left>846</left><top>372</top><width>678</width><height>120</height><font>st_small_20</font><textcolor>b3ffffff</textcolor><label>$VAR[AddonInfo_Text]</label><autoscroll time="3000" delay="6000" repeat="6000">true</autoscroll></control>
		<!-- the actions: rows in the grid -->
		<control type="image"><left>810</left><top>520</top><width>750</width><height>1</height><texture colordiffuse="12ffffff">common/white.png</texture></control>
		<control type="grouplist" id="9000">
			<left>810</left><top>521</top><width>750</width><height>430</height>
			<orientation>vertical</orientation><itemgap>0</itemgap><usecontrolcoords>true</usecontrolcoords>
			<onup>9000</onup><ondown>9000</ondown><onleft>noop</onleft><onright>noop</onright>
			<control type="button" id="12"><include>FGS_DlgRow</include><label>$LOCALIZE[518]</label><visible>Control.IsEnabled(12)</visible></control>
			<control type="button" id="9"><include>FGS_DlgRow</include><label>$LOCALIZE[24020]</label><visible>Control.IsEnabled(9)</visible></control>
			<control type="radiobutton" id="13">
				<description>auto-update (Kodi labels it)</description>
				<include>FGS_DlgRow</include>
				<radiowidth>64</radiowidth><radioheight>32</radioheight><radioposx>650</radioposx>
				<textureradioonfocus colordiffuse="fg_mark">fg/fgs_toggle_on.png</textureradioonfocus>
				<textureradioonnofocus colordiffuse="b3e8b04b">fg/fgs_toggle_on.png</textureradioonnofocus>
				<textureradioofffocus colordiffuse="ffffffff">fg/fgs_toggle_off.png</textureradioofffocus>
				<textureradiooffnofocus colordiffuse="80ffffff">fg/fgs_toggle_off.png</textureradiooffnofocus>
				<visible>Control.IsEnabled(13)</visible>
			</control>
			<control type="button" id="10"><include>FGS_DlgRow</include><label>$LOCALIZE[39024]</label><visible>Control.IsEnabled(10)</visible></control>
			<control type="button" id="7"><include>FGS_DlgRow</include><visible>Control.IsEnabled(7)</visible></control>
			<control type="button" id="8"><include>FGS_DlgRow</include><label>$LOCALIZE[24138]</label><visible>Control.IsEnabled(8)</visible></control>
			<control type="button" id="14"><include>FGS_DlgRow</include><label>$LOCALIZE[24069]</label><visible>Control.IsEnabled(14)</visible></control>
			<control type="button" id="6"><include>FGS_DlgRow</include><visible>Control.IsEnabled(6)</visible></control>
			<control type="button" id="9202">
				<include>FGS_DlgRow</include>
				<label>$VAR[Dlg_AddonNewsLabel]</label>
				<onclick condition="String.IsEmpty(Window(Home).Property(aeon.addonnews))">SetProperty(aeon.addonnews,1,home)</onclick>
				<onclick condition="!String.IsEmpty(Window(Home).Property(aeon.addonnews))">ClearProperty(aeon.addonnews,home)</onclick>
				<visible>!String.IsEmpty(ListItem.AddonNews)</visible>
			</control>
		</control>
		<!-- Kodi fills the screenshots panel; the style does not show it -->
		<control type="panel" id="50"><left>-4000</left><top>0</top><width>10</width><height>10</height><itemlayout width="10" height="10"/><focusedlayout width="10" height="10"/><visible>false</visible></control>
		<include content="FGS_DlgHint"><param name="label" value="$ADDON[skin.aeon.fuse 32692]"/></include>
	</include>
'''


def main():
    t = rd('DialogAddonInfo.xml')
    if 'AddonInfo_Classic' not in t:
        s = t.index('\t\t<!-- ====== hero card -->')
        e = t.index('\t</controls>')
        body = t[s:e]
        t = t[:s] + '\t\t<include condition="!$EXP[FGS]">AddonInfo_Classic</include>\n\t\t<include condition="$EXP[FGS]">FGS_AddonInfo</include>' + MARK + '\n' + t[e:]
        wr('DialogAddonInfo.xml', t)
        d = rd('Includes_Dialogs.xml')
        assert 'name="AddonInfo_Classic"' not in d
        inc = '\t<!-- 0.56.38: DialogAddonInfo outside the Fused Glass style (moved from the window file unchanged) -->\n\t<include name="AddonInfo_Classic">\n' + body + '\t</include>\n'
        k = d.rindex('</includes>')
        d = d[:k] + inc + d[k:]
        wr('Includes_Dialogs.xml', d)
        print('classic moved')
    t = rd('DialogAddonInfo.xml')
    if '<include condition="!$EXP[FGS]">AG_MoodLine</include>' not in t:
        assert t.count('<include>AG_MoodLine</include>') == 1
        t = t.replace('<include>AG_MoodLine</include>', '<include condition="!$EXP[FGS]">AG_MoodLine</include>')
        wr('DialogAddonInfo.xml', t)
    f = rd('Includes_Fused.xml')
    if MARK in f:
        s = f.index('\t' + MARK)
        e = f.index('\t</include>\n', f.index('<include name="FGS_AddonInfo">', s)) + len('\t</include>\n')
        f = f[:s] + f[e:]
    if True:
        facts = ''.join(fact(lab, val) for lab, val in (
            ('$LOCALIZE[31150]', 'ListItem.AddonVersion'), ('$LOCALIZE[31151]', 'ListItem.AddonType'),
            ('$LOCALIZE[31152]', 'ListItem.AddonInstallDate'), ('$LOCALIZE[31153]', 'ListItem.AddonLastUpdated'),
            ('$LOCALIZE[31219]', 'ListItem.Property(Addon.Status)')))
        block = FGS % {'mark': MARK, 'facts': facts}
        f = f.replace('\t<include name="FGS_RowTex">', block + '\t<include name="FGS_RowTex">', 1)
        wr('Includes_Fused.xml', f)
        print('FGS_AddonInfo written')


if __name__ == '__main__':
    main()
