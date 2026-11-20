"""0.39.11 Information page > More > Choose art: Kodi opens the art-type list (DialogSelect, heading "Choose art") and,
after a type is picked, the image picker (FileBrowser, heading "Choose art" again), so the picker did not say which
art it was for. The helper follows the type focused in that list while it is open (Window(Home) aeon.arttype, only for that
list: its items carry ListItem.Property(type)); the picker then shows "Choose art · Poster". Cleared when the picker or the
information page closes. AG_GenericDialog gets an optional header_visible. Run in 1080i."""
import io


def rw(name, pairs):
    s = io.open(name, encoding='utf-8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (name, old[:70])
        s = s.replace(old, new)
    io.open(name, 'w', encoding='utf-8', newline='').write(s)


# DialogSelect's onunload cannot do it: Kodi empties the select list before the window's unload actions run, so
# the helper service follows the focused type while the list is open (service.ArtTypeWatch, helper 0.3.65).
rw('Includes_Dialogs.xml', [
    ('''	<include name="AG_GenericDialog">
		<param name="header_id"></param>
		<param name="header_label"></param>''', '''	<include name="AG_GenericDialog">
		<param name="header_id"></param>
		<param name="header_label"></param>
		<param name="header_visible">true</param>'''),
    ('''				<font>ui_28_bold</font>
				<textcolor>$VAR[AG_Ink]</textcolor>
				<label>$PARAM[header_label]</label>
			</control>''', '''				<font>ui_28_bold</font>
				<textcolor>$VAR[AG_Ink]</textcolor>
				<label>$PARAM[header_label]</label>
				<visible>$PARAM[header_visible]</visible>
			</control>''')])

SHOW = '!String.IsEmpty(Window(Home).Property(aeon.arttype)) + Window.IsVisible(movieinformation)'
rw('FileBrowser.xml', [
    ('''<window>
	<defaultcontrol always="true">450</defaultcontrol>''', '''<window>
	<defaultcontrol always="true">450</defaultcontrol>
	<onunload>ClearProperty(aeon.arttype,home)</onunload>'''),
    ('''				<param name="header_id" value="411"/>
				<param name="kicker" value="$INFO[Container(450).CurrentItem]$INFO[Container(450).NumItems, / ,]"/>
			</include>''', '''				<param name="header_id" value="411"/>
				<param name="header_visible" value="![%(show)s]"/>
				<param name="kicker" value="$INFO[Container(450).CurrentItem]$INFO[Container(450).NumItems, / ,]"/>
			</include>
			<!-- 0.39.11: Choose art's image picker says which art it is for: "Choose art · Poster" -->
			<control type="label">
				<left>dialog_pad</left>
				<top>0</top>
				<right>260</right>
				<height>dialog_header_h</height>
				<font>ui_28_bold</font>
				<textcolor>$VAR[AG_Ink]</textcolor>
				<label>$INFO[Control.GetLabel(411)]  ·  [CAPITALIZE]$INFO[Window(Home).Property(aeon.arttype)][/CAPITALIZE]</label>
				<visible>%(show)s</visible>
			</control>''' % {'show': SHOW})])

rw('DialogVideoInfo.xml', [(
    '''	<onunload>ClearProperty(aeon.trailer,home)</onunload>''',
    '''	<onunload>ClearProperty(aeon.trailer,home)</onunload>
	<onunload>ClearProperty(aeon.arttype,home)</onunload>''')])
print('ok')
