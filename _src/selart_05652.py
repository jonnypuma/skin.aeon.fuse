"""0.56.52 the picture in Kodi's select list with pictures (list 6). The user, 2026-11-19: clicking an actress on the
information page found a film and a TV show; the film showed landscape art, the show nothing. Kodi's actor search
(CGUIDialogVideoInfo::OnSearch) loads every item's art, but the rows drew only ListItem.Icon, and a show without a
thumb has no icon. Now the landscape slot of the Fused Glass style rows picks: landscape -> episode still -> the show's
landscape -> fanart with the clear logo on it -> poster -> icon. The classic Aeon icon grid (square slot) picks the
poster before the icon. The Aeon menu styles' select already starts at the poster. Patches the XML and the generator
(fgs_dialogs_05632.py) so a rerun keeps it. Run from the skin folder. Repeatable."""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FUSED = os.path.join(HERE, '..', '1080i', 'Includes_Fused.xml')
DLGS = os.path.join(HERE, '..', '1080i', 'Includes_Dialogs.xml')
GEN = os.path.join(HERE, 'fgs_dialogs_05632.py')

OLD = ('<control type="image"><left>300</left><top>6</top><width>130</width><height>58</height><aspectratio align="right">'
       'keep</aspectratio><texture background="true">$INFO[ListItem.Icon]</texture><visible>$PARAM[pic]</visible></control>')
LOGO_COND = ('String.IsEmpty(ListItem.Art(landscape)) + ![String.IsEqual(ListItem.DBType,episode) + '
             '[!String.IsEmpty(ListItem.Art(thumb)) | !String.IsEmpty(ListItem.Art(tvshow.landscape))]] + '
             '!String.IsEmpty(ListItem.Art(fanart))')
NEW = ('<control type="image"><left>300</left><top>6</top><width>130</width><height>58</height><aspectratio align="right">'
       'keep</aspectratio><texture background="true">$VAR[FGS_SelArt]</texture><visible>$PARAM[pic]</visible></control>'
       # 0.56.52 fanart stands in for landscape: the clear logo (else the show's) on it, like a landscape poster
       '<control type="image"><left>333</left><top>12</top><width>91</width><height>46</height><aspectratio>keep</aspectratio>'
       '<texture background="true">$VAR[FGS_SelLogo]</texture><visible>$PARAM[pic] + ' + LOGO_COND + '</visible></control>')
VARS = '''	<!-- 0.56.52 the select list's picture (actor search etc.): landscape, else fanart + clear logo, else poster -->
	<variable name="FGS_SelArt">
		<value condition="!String.IsEmpty(ListItem.Art(landscape))">$INFO[ListItem.Art(landscape)]</value>
		<value condition="String.IsEqual(ListItem.DBType,episode) + !String.IsEmpty(ListItem.Art(thumb))">$INFO[ListItem.Art(thumb)]</value>
		<value condition="String.IsEqual(ListItem.DBType,episode) + !String.IsEmpty(ListItem.Art(tvshow.landscape))">$INFO[ListItem.Art(tvshow.landscape)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(fanart))">$INFO[ListItem.Art(fanart)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(poster))">$INFO[ListItem.Art(poster)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(tvshow.poster))">$INFO[ListItem.Art(tvshow.poster)]</value>
		<value>$INFO[ListItem.Icon]</value>
	</variable>
	<variable name="FGS_SelLogo">
		<value condition="!String.IsEmpty(ListItem.Art(clearlogo))">$INFO[ListItem.Art(clearlogo)]</value>
		<value>$INFO[ListItem.Art(tvshow.clearlogo)]</value>
	</variable>
	<variable name="Dlg_SelIcon">
		<value condition="!String.IsEmpty(ListItem.Art(poster))">$INFO[ListItem.Art(poster)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(tvshow.poster))">$INFO[ListItem.Art(tvshow.poster)]</value>
		<value>$INFO[ListItem.Icon]</value>
	</variable>
'''


def main():
    t = io.open(FUSED, encoding='utf-8').read()
    if 'name="FGS_SelArt"' not in t:
        t = t.replace('\t<include name="FGS_SelRow">', VARS + '\t<include name="FGS_SelRow">', 1)
    if OLD in t:
        t = t.replace(OLD, NEW, 1)
    assert NEW in t and 'name="FGS_SelArt"' in t
    io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(t)

    g = io.open(GEN, encoding='utf-8').read()
    if OLD in g:
        g = g.replace(OLD, NEW, 1)
        io.open(GEN, 'w', encoding='utf-8', newline='\n').write(g)
    assert NEW in g

    # the classic icon grid (Dlg_SelectIconGrid, panel 6): poster before the icon
    d = io.open(DLGS, encoding='utf-8').read()
    s = d.index('<include name="Dlg_SelectIconGrid">')
    e = d.index('</include>', s)
    blk = d[s:e].replace('$INFO[ListItem.Icon]', '$VAR[Dlg_SelIcon]')
    d = d[:s] + blk + d[e:]
    io.open(DLGS, 'w', encoding='utf-8', newline='\n').write(d)
    print('selart: FGS select picture fallback + logo; icon grid posters (%d)' % blk.count('Dlg_SelIcon'))


if __name__ == '__main__':
    main()
