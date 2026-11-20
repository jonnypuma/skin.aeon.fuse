# -*- coding: utf-8 -*-
"""0.49.0 Fused Glass music library views, after the approved mockups: Fanart list (513), Wall (530: artists and
albums; songs dropped as the user decided), Showcase (531), Rows / Album list (532), Song list (533) and Fanart wall
(534: artists; albums dropped). Imported by fg_lib.py like the video views; each view's include loads them in Fused
Glass instead of the Aeon views.

The music menu (Artists, Albums, Songs, Genres: buttons 9801-9804) sits as glass pills at the top right before the
view capsule, which is button 9805 (it opens the view picker, as the Aeon menu's View button). Up from the first row
goes to the pill of what the list shows. One music info band under the walls and the showcase: a narrow name column
(an artist's clearlogo; for albums the artist's clearlogo over the album's name), the bio or the review as wide as it
fits, then for artists the album count with its icon and their album covers, moving on every 5 s; for albums the
record label logo. The info follows ListItem, as the Aeon music views do."""
from fg_lib import img, lbl, glass, rail, rounded_mask, INK
from fg_lib_walls import tile

VIEWS = (513, 530, 531, 532, 533, 534)
CYC = {513: 5131, 530: 5300005, 531: 5310005, 532: 5320005, 534: 5340005}     # each view's album cover cycler
LABEL_LOGO = 'resource://resource.images.recordlabels.white/$INFO[ListItem.Property(Album_Label)].png'
HAS_LABEL = '!String.IsEmpty(ListItem.Property(Album_Label)) + [Container.Content(albums) | Container.Content(songs)]'
ART_LOGO = ('$EXP[FG_L_LogosOn] + [!String.IsEmpty(ListItem.Art(clearlogo)) | !String.IsEmpty(ListItem.Art(artist.clearlogo)) | '
            '!String.IsEmpty(ListItem.Art(albumartist.clearlogo))]')


VARS = '''	<!-- ===== music views (0.49.0, _src/fg_lib_music.py) -->
	<variable name="FG_M_Square">
		<value condition="!String.IsEmpty(ListItem.Art(thumb))">$INFO[ListItem.Art(thumb)]</value>
		<value>$INFO[ListItem.Art(album.thumb)]</value>
	</variable>
	<variable name="FG_M_Fanart">
		<value condition="!String.IsEmpty(ListItem.Art(fanart))">$INFO[ListItem.Art(fanart)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(artist.fanart))">$INFO[ListItem.Art(artist.fanart)]</value>
		<value>$INFO[ListItem.Art(thumb)]</value>
	</variable>
	<variable name="FG_M_ArtistLogo">
		<value condition="!String.IsEmpty(ListItem.Art(clearlogo))">$INFO[ListItem.Art(clearlogo)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(artist.clearlogo))">$INFO[ListItem.Art(artist.clearlogo)]</value>
		<value>$INFO[ListItem.Art(albumartist.clearlogo)]</value>
	</variable>
	<variable name="FG_M_ArtistName">
		<value condition="Container.Content(artists)">$INFO[ListItem.Label]</value>
		<value condition="!String.IsEmpty(ListItem.AlbumArtist)">$INFO[ListItem.AlbumArtist]</value>
		<value>$INFO[ListItem.Artist]</value>
	</variable>
	<variable name="FG_M_Name">
		<value condition="String.IsEqual(ListItem.DBType,song) + !String.IsEmpty(ListItem.Title)">$INFO[ListItem.Title]</value>
		<value>$INFO[ListItem.Label]</value>
	</variable>
	<variable name="FG_M_Meta">
		<value condition="Container.Content(artists)">$INFO[ListItem.Genre]$INFO[ListItem.Property(Artist_YearsActive),  ·  ,]</value>
		<!-- 0.56.9 the info panel rule: year · tracks · length · genres; a release type only when it is not an album -->
		<value condition="Container.Content(albums) + Integer.IsEqual(Window(Home).Property(aeon.tc.focus),1)">$INFO[ListItem.Year,,  ·  ]1 $ADDON[skin.aeon.fuse 32308]$VAR[FG_M_Len]$VAR[FG_M_Type]$INFO[ListItem.Genre,  ·  ,]</value>
		<value condition="Container.Content(albums)">$INFO[ListItem.Year]$INFO[Window(Home).Property(aeon.tc.focus),  ·  , $ADDON[skin.aeon.fuse 32309]]$VAR[FG_M_Len]$VAR[FG_M_Type]$INFO[ListItem.Genre,  ·  ,]</value>
		<value condition="Container.Content(songs)">$INFO[ListItem.Album]$INFO[ListItem.Year,  ·  ,]$INFO[ListItem.Genre,  ·  ,]</value>
		<value>$INFO[ListItem.Genre]</value>
	</variable>
	<variable name="FG_M_Len">
		<value condition="Integer.IsGreater(ListItem.Duration(mins),59)">  ·  $INFO[ListItem.Duration(h)]h $INFO[ListItem.Duration(mm)]m</value>
		<value condition="Integer.IsGreater(ListItem.Duration(mins),0)">$INFO[ListItem.Duration(mins),  ·  , min]</value>
	</variable>
	<variable name="FG_M_Type">
		<value condition="!String.IsEmpty(ListItem.Property(Album_Type)) + !String.StartsWith(ListItem.Property(Album_Type),album)">$INFO[ListItem.Property(Album_Type),  ·  ,]</value>
	</variable>
	<variable name="FG_M_RowSub">
		<value condition="String.IsEqual(ListItem.DBType,artist)">$INFO[ListItem.Genre]</value>
		<value condition="String.IsEqual(ListItem.DBType,album)">$INFO[ListItem.Artist]$INFO[ListItem.Year,  ·  ,]</value>
		<value>$INFO[ListItem.Artist]</value>
	</variable>
	<variable name="FG_M_HKicker">
		<value condition="Container.Content(albums) + String.StartsWith(Container.FolderPath,musicdb://artists/)">$LOCALIZE[2]  ›  $LOCALIZE[31298]</value>
		<value condition="Container.Content(songs) + String.StartsWith(Container.FolderPath,musicdb://albums/)">$LOCALIZE[2]  ›  $LOCALIZE[31299]</value>
		<value>$LOCALIZE[2]</value>
	</variable>
	<variable name="FG_M_HTitle">
		<value condition="[Container.Content(albums) | Container.Content(songs)] + !String.IsEmpty(Container.FolderName) + !String.EndsWith(Container.FolderPath,musicdb://albums/) + !String.EndsWith(Container.FolderPath,musicdb://songs/)">$INFO[Container.FolderName]</value>
		<value condition="Container.Content(artists)">$LOCALIZE[31298]</value>
		<value condition="Container.Content(albums)">$LOCALIZE[31299]</value>
		<value condition="Container.Content(songs)">$LOCALIZE[31343]</value>
		<value condition="Container.Content(genres)">$LOCALIZE[31344]</value>
		<value>$INFO[Container.FolderName]</value>
	</variable>
'''
# 0.56.8: the track count of a row ("1 track", "11 tracks"; Includes_Plural.xml's way), List view (513) and Album list (532)
VARS += ''.join('\t<variable name="FG_M_Tc%s">\n\t\t<value condition="Integer.IsEqual(Window(Home).Property(%s),1)">1 $ADDON[skin.aeon.fuse 32308]</value>\n'
                '\t\t<value>$INFO[Window(Home).Property(%s),, $ADDON[skin.aeon.fuse 32309]]</value>\n\t</variable>\n' % (n, prop, prop)
                for n, prop in [(str(k), 'aeon.tc.%d' % k) for k in range(5)] + [('532_%d' % k, 'aeon.tc532.%d' % k) for k in range(10)])
for _t, _c in ((9801, 'Container.Content(artists)'), (9802, 'Container.Content(albums)'), (9803, 'Container.Content(songs)'), (9804, 'Container.Content(genres)')):
    VARS += '\t<variable name="FG_M_Tab%d"><value condition="%s">40ffffff</value><value>14ffffff</value></variable>\n' % (_t, _c)
for _cid, _cyc in CYC.items():
    VARS += ('\t<variable name="FG_M%d_Albums"><value condition="Container.Content(artists) + !String.IsEmpty(Container(%d).ListItem.DBID)">musicdb://albums/?artistid=$INFO[Container(%d).ListItem.DBID]</value></variable>\n'
             % (_cid, _cid, _cid))


# ------------------------------------------------------------------------------------------------------------ parts
def m_header():
    """Kicker and title at the top left; at the top right the music menu as glass pills and the view capsule (9805)."""
    downs = ''.join('<ondown condition="Control.IsVisible(%d)">SetFocus(%d)</ondown>' % (v, v) for v in VIEWS)
    common = ('<height>40</height><font>lb_small_20_semibold</font><textoffsetx>18</textoffsetx><aligny>center</aligny><textcolor>e6ffffff</textcolor>'
              '<focusedcolor>aeon_onbar</focusedcolor><onup condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onup>' + downs)
    out = lbl(96, 36, 1100, 30, '[UPPERCASE]$VAR[FG_M_HKicker][/UPPERCASE]', 'lb_cap_16', 'a3ffffff')
    out += lbl(94, 60, 900, 72, '$VAR[FG_M_HTitle]', 'lb_title_50', 'ffffffff')
    tabs = ''
    for bid, label, target in ((9801, 31298, 'artists'), (9802, 31299, 'albums'), (9803, 31343, 'songs'), (9804, 31344, 'genres')):
        left = '<onleft condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onleft>' if bid == 9801 else '<onleft>%d</onleft>' % (bid - 1)
        tabs += ('<control type="button" id="%d"><width min="60" max="300">auto</width><label>$LOCALIZE[%d]</label>%s'
                 '<texturenofocus border="20" colordiffuse="$VAR[FG_M_Tab%d]">fg/r20.png</texturenofocus><texturefocus border="20" colordiffuse="ffffffff">fg/r20.png</texturefocus>'
                 '%s<onright>%d</onright><onclick>Container.Update(musicdb://%s/)</onclick></control>' % (bid, label, common, bid, left, bid + 1, target))
    # 0.56.14: the view's name per content (Album wall showing artists is the Artist wall), as Aeon names it
    tabs += ('<control type="button" id="9805"><width min="60" max="700">auto</width><label>$VAR[Aeon_ViewName]  ·  $INFO[Container.SortMethod] $VAR[FG_L_SortDir]</label>%s'
             '<texturenofocus border="20" colordiffuse="14ffffff">fg/r20.png</texturenofocus><texturefocus border="20" colordiffuse="ffffffff">fg/r20.png</texturefocus>'
             '<onleft>9804</onleft><onright>noop</onright><onclick>SetProperty(aeon.curview,$INFO[Container.Viewmode],home)</onclick><onclick>ActivateWindow(1164)</onclick></control>' % common)
    out += ('<control type="grouplist"><left>700</left><top>52</top><width>1100</width><height>40</height><orientation>horizontal</orientation><align>right</align>'
            '<itemgap>10</itemgap><usecontrolcoords>true</usecontrolcoords>%s</control>' % tabs)
    return out


def m_up(first_row):
    """Up from the first row: the pill of what the list shows."""
    c = 'Window.IsActive(music) + %s' % first_row
    return ('<onup condition="%(c)s + Container.Content(albums)">9802</onup><onup condition="%(c)s + Container.Content(songs)">9803</onup>'
            '<onup condition="%(c)s + Container.Content(genres)">9804</onup><onup condition="%(c)s + !Container.Content(albums) + !Container.Content(songs) + !Container.Content(genres)">9801</onup>'
            '<onup condition="![%(f)s]">Action(LastPage)</onup>' % {'c': c, 'f': c})


def opening(cid):
    return ('\t<include name="FG_V%d_View">\n\t\t<control type="group">\n\t\t\t<visible>Control.IsVisible(%d)</visible>\n\t\t\t<include>Anim_FadeVisible</include>\n'
            '\t\t\t<include>Aeon_V_Bg</include>\n\t\t\t%s\n' % (cid, cid, m_header()))


def closing(cid, base, az):
    return ('\t\t\t' + rail(cid, base * 100 + 1, base * 100 + 50, 'aeon/icons/music.png', az.replace('SetFocus(510)', 'SetFocus(%d)' % cid)) + '\n'
            '\t\t</control>\n\t</include>\n')


def cycler(cid, x, y, size, vis='Container.Content(artists)'):
    """The artist's album covers, one at a time, moving on every 5 s (a list with one visible item)."""
    cyc = CYC[cid]
    cover = (img(0, 0, size, size, 'fg/r14.png', 'fg_frost', 14)
             + img(0, 0, size, size, '$INFO[ListItem.Art(thumb)]', diffuse='fg/m%dx%d.png' % (size, size), aspect='scale', bg=True))
    return ('<control type="list" id="%d"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><orientation>horizontal</orientation>'
            '<scrolltime tween="cubic" easing="inout">500</scrolltime>'   # 0.56.6: moved on by Timers.xml aeoncycler, not autoscroll
            '<visible>%s</visible><content browse="never">$VAR[FG_M%d_Albums]</content>'        # never hidden by its own count: a hidden list loads nothing
            '<itemlayout width="%d" height="%d">%s</itemlayout><focusedlayout width="%d" height="%d">%s</focusedlayout></control>'
            % (cyc, x, y, size, size, vis, cid, size, size, cover, size, size, cover)), {(size, size, 14)}


def count_block(cid, x, y, vis='Container.Content(artists)'):
    """The album count under its stack icon."""
    cyc = CYC[cid]
    v = '%s + Integer.IsGreater(Container(%d).NumItems,0)' % (vis, cyc)
    return (img(x + 15, y, 40, 40, 'common/aeon_layers.png', 'ffffffff', aspect='keep', vis=v)
            + lbl(x - 10, y + 44, 90, 36, '$INFO[Container(%d).NumItems]' % cyc, 'lb_ui_24_bold', 'ffffffff', 'center', v))


def name_block(x, y, w, logo_h, artist_font='lb_font36_title'):
    """An artist: the clearlogo or the name. An album or song: the artist's clearlogo (or name) over its own name."""
    art_ = 'Container.Content(artists)'
    out = img(x, y, w, logo_h, '$VAR[FG_M_ArtistLogo]', aspect='keep', align='left', aligny='center', vis='%s + %s' % (art_, ART_LOGO))
    out += lbl(x, y, w, logo_h, '$INFO[ListItem.Label]', artist_font, 'ffffffff', vis='%s + ![%s]' % (art_, ART_LOGO))
    out += img(x, y, w, 60, '$VAR[FG_M_ArtistLogo]', aspect='keep', align='left', aligny='center', vis='!%s + %s' % (art_, ART_LOGO))
    out += lbl(x, y, w, 60, '$VAR[FG_M_ArtistName]', 'lb_ui_28_semibold', 'ccffffff', vis='!%s + ![%s]' % (art_, ART_LOGO))
    out += lbl(x, y + 64, w, 46, '$VAR[FG_M_Name]', 'lb_ui_28_bold', 'ffffffff', vis='!' + art_)
    return out


def info_band(cid, y=760, h=280):
    """The music info band of the walls and the showcase."""
    pad = 24
    inner = h - 2 * pad
    right = 1800 - pad
    x = 96 + pad
    out = glass(96, y, 1704, h)
    lh = min(110, inner - 70)
    out += name_block(x, y + pad, 360, lh)
    out += lbl(x, y + pad + 118, 360, 34, '$VAR[FG_M_Meta]', 'lb_ui_22', 'ccffffff')
    tx = x + 360 + 36
    cov = inner
    bio = lambda w, vis: ('<control type="textbox"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><font>lb_body_24</font><textcolor>d9ffffff</textcolor>'
                          '<label>$VAR[Aeon_M_Bio]</label><autoscroll delay="8000" time="2000" repeat="8000">true</autoscroll><visible>%s + $EXP[Aeon_VOBio]</visible></control>'
                          % (tx, y + pad, w, inner, vis))
    # artists: the album count between the text and the covers
    cx = right - cov
    out += bio(cx - 36 - 90 - 36 - tx, 'Container.Content(artists)')
    out += count_block(cid, cx - 36 - 70, y + (h - 80) // 2)
    c, m = cycler(cid, cx, y + pad, cov)
    out += c
    # albums: the record label logo at the right
    out += bio(right - 190 - 36 - tx, '!Container.Content(artists) + %s' % HAS_LABEL)
    out += bio(right - tx, '!Container.Content(artists) + ![%s]' % HAS_LABEL)
    out += img(right - 190, y + (h - 90) // 2, 190, 90, LABEL_LOGO, 'ebffffff', aspect='keep', align='right', aligny='center', vis=HAS_LABEL)
    return out, m


def grid_view(cid, base, cols, w, h, gapy, art, label, visible, az, r=14, caption=True):
    gapx = (1704 - cols * w) // (cols - 1)
    iw, ih = w + gapx, h + gapy
    y, band_y = 174, 760
    ph = min(14 + ih + h + (48 if caption else 14), band_y - (y - 14))
    item = '<control type="group"><left>20</left><top>14</top>%s</control>'
    band, m = info_band(cid)
    out = opening(cid)
    out += ('\t\t\t<control type="panel" id="%d"><left>76</left><top>%d</top><width>%d</width><height>%d</height><pagecontrol>%d</pagecontrol><orientation>vertical</orientation>'
            '<viewtype label="%s">icon</viewtype><visible>%s</visible><preloaditems>2</preloaditems><scrolltime tween="cubic" easing="out">260</scrolltime>'
            '<onback condition="String.IsEqual(Skin.String(aeon.backmode),home)">ActivateWindow(home)</onback>%s<ondown>Action(FirstPage)</ondown>'
            '<onleft condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onleft><onright>%d</onright>'
            '<itemlayout width="%d" height="%d">%s</itemlayout><focusedlayout width="%d" height="%d">%s</focusedlayout></control>\n'
            % (cid, y - 14, cols * iw + 20, ph, base * 100 + 50, label, visible, m_up('Integer.IsLessOrEqual(Container.CurrentItem,%d)' % cols), base * 100 + 1,
               iw, ih, item % tile(cid, w, h, False, art, r, caption), iw, ih, item % tile(cid, w, h, True, art, r, caption)))
    out += '\t\t\t' + band + '\n' + closing(cid, base, az)
    return out, m | {(w, h, r)}


# ------------------------------------------------------------------------------------------------------------ views
def v530(az):
    """Wall: two rows of square pictures with their names, the music info band (artists, albums)."""
    return grid_view(530, 53000, 6, 240, 240, 56, '$VAR[FG_M_Square]', '31090', 'Container.Content(albums) | Container.Content(artists)', az)


def v534(az):
    """Fanart wall: two rows of the artists' fanart with their names, the music info band (artists)."""
    return grid_view(534, 53400, 4, 396, 223, 66, '$VAR[FG_M_Fanart]', '31088', 'Container.Content(artists)', az, r=16)


def v531(az):
    """Showcase: a cover flow of square pictures, the one in focus big in the middle, the music info band."""
    cid, base = 531, 53100
    sm, big, gap = 250, 420, 34
    lit = 'Control.HasFocus(531)'
    top = 160
    side = ('<control type="group"><left>%d</left><top>%d</top>' % (gap // 2, 190 + (big - sm) // 2 - top)
            + img(0, 0, sm, sm, 'fg/r16.png', 'fg_frost', 16) + img(0, 0, sm, sm, '$VAR[FG_M_Square]', diffuse='fg/m%dx%d.png' % (sm, sm), aspect='scale', bg=True)
            + img(0, 0, sm, sm, 'fg/r16.png', '66080a0e', 16) + '</control>')
    bigt = ('<control type="group"><left>%d</left><top>%d</top>' % (gap // 2, 190 - top)
            + img(-30, -22, big + 60, big + 60, 'fg/sh24.png', '$VAR[FG_PanelSh_8c]', 64)
            + img(0, 0, big, big, 'fg/r20.png', 'fg_frost', 20) + img(0, 0, big, big, '$VAR[FG_M_Square]', diffuse='fg/m%dx%d.png' % (big, big), aspect='scale', bg=True)
            + img(-7, -7, big + 14, big + 14, 'fg/fr23.png', 'fg_mark', 24, lit) + '</control>')
    iw, bigw = sm + gap, big + gap
    left = (96 + 1800) // 2 - bigw // 2 - 3 * iw
    band, m = info_band(cid)
    out = opening(cid)
    out += ('\t\t\t<control type="wraplist" id="531"><left>%d</left><top>%d</top><width>%d</width><height>560</height><orientation>horizontal</orientation><focusposition>3</focusposition>'
            '<movement>2</movement><viewtype label="31046">icon</viewtype><visible>Container.Content(albums) | Container.Content(artists)</visible>'
            '<scrolltime tween="cubic" easing="out">300</scrolltime><onback condition="String.IsEqual(Skin.String(aeon.backmode),home)">ActivateWindow(home)</onback>'
            '<onup condition="Window.IsActive(music) + Container.Content(albums)">9802</onup><onup condition="Window.IsActive(music) + !Container.Content(albums)">9801</onup>'
            '<onup condition="!Window.IsActive(music) + !Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onup><ondown>%d</ondown>'
            '<itemlayout width="%d" height="560">%s</itemlayout><focusedlayout width="%d" height="560">%s</focusedlayout></control>\n'
            % (left, top, 1810 - left, base * 100 + 1, iw, side, bigw, bigt))
    out += '\t\t\t' + band + '\n' + closing(cid, base, az)
    return out, m | {(sm, sm, 16), (big, big, 20)}


def row532(focused, w=936, h=79):
    lit = 'Control.HasFocus(532)'
    out = ''
    if focused:
        out += img(0, 0, w, h, 'fg/r18.png', 'ffffffff', 18, lit) + img(0, 0, w, h, 'fg/r18.png', '1fffffff', 18, '!' + lit) + img(0, 0, w, h, 'fg/e18.png', '38ffffff', 18, '!' + lit)
    ink = '$VAR[FG_M532_Ink]' if focused else 'ffffffff'
    ink2 = '$VAR[FG_M532_Ink2]' if focused else 'a8ffffff'
    out += img(10, (h - 62) // 2, 62, 62, 'fg/r12.png', '1fffffff', 12)      # a quiet square where there is no picture
    out += img(10, (h - 62) // 2, 62, 62, '$VAR[FG_M_Square]', diffuse='fg/m62x62.png', aspect='scale', bg=True)
    out += lbl(90, h // 2 - 32, w - 250, 36, '$INFO[ListItem.Label]', 'lb_ui_24_bold', ink)
    out += lbl(90, h // 2 + 2, w - 250, 30, '$VAR[FG_M_RowSub]', 'lb_small_20', ink2)
    # 0.56.8 the list row rule: an album's track count at the right (an overlay per screen row, v532), not the year again
    return out


def v532(az):
    """Rows (artists) / Album list (albums): rows with a small picture, a second line and the album count; at the right
    the picture with the name and facts beside it, the bio or review under them and (artists) the album covers."""
    cid, base = 532, 53200
    out = opening(cid)
    out += '\t\t\t' + glass(96, 160, 960, 880) + '\n'
    out += ('\t\t\t<control type="list" id="532"><left>108</left><top>172</top><width>936</width><height>850</height><pagecontrol>%d</pagecontrol><orientation>vertical</orientation>'
            '<viewtype label="31098">list</viewtype><visible>Container.Content(albums) | Container.Content(artists)</visible><scrolltime tween="cubic" easing="out">200</scrolltime>'
            '<onback condition="String.IsEqual(Skin.String(aeon.backmode),home)">ActivateWindow(home)</onback>%s<ondown>Action(FirstPage)</ondown>'
            '<onleft condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onleft><onright>%d</onright>'
            '<itemlayout width="936" height="85">%s</itemlayout><focusedlayout width="936" height="85">%s</focusedlayout></control>\n'
            % (base * 100 + 50, m_up('Integer.IsEqual(Container.CurrentItem,1)'), base * 100 + 1, row532(False), row532(True)))
    # the album count of each artist row (the helper publishes Window(Home).Property(aeon.ac.<row>))
    rows = ''
    for k in range(10):
        p = 'Window(Home).Property(aeon.ac.%d)' % k
        y = 172 + k * 85
        on = 'Integer.IsEqual(Container(532).Position,%d) + Control.HasFocus(532)' % k
        v = '!String.IsEmpty(%s)' % p
        rows += lbl(108 + 936 - 110, y, 50, 79, '$INFO[%s]' % p, 'lb_ui_22_semibold', INK, 'right', vis='%s + %s' % (v, on))
        rows += lbl(108 + 936 - 110, y, 50, 79, '$INFO[%s]' % p, 'lb_ui_22_semibold', 'ffffffff', 'right', vis='%s + ![%s]' % (v, on))
        rows += img(108 + 936 - 50, y + 27, 26, 26, 'common/aeon_layers.png', INK, aspect='keep', vis='%s + %s' % (v, on))
        rows += img(108 + 936 - 50, y + 27, 26, 26, 'common/aeon_layers.png', 'b3ffffff', aspect='keep', vis='%s + ![%s]' % (v, on))
    out += '\t\t\t<control type="group"><visible>Container.Content(artists) + !Container(532).Scrolling</visible>%s</control>\n' % rows
    # 0.56.8 albums: the track count of each row at the right (the helper publishes aeon.tc532.<row>), like 513
    rows = ''
    for k in range(10):
        p = 'Window(Home).Property(aeon.tc532.%d)' % k
        y = 172 + k * 85
        on = 'Integer.IsEqual(Container(532).Position,%d) + Control.HasFocus(532)' % k
        v = '!String.IsEmpty(%s)' % p
        lab = '$INFO[%s]' % p        # 0.56.10: the number and the song icon (the user: "use the song icon instead of tracks label")
        rows += lbl(108 + 936 - 260, y, 200, 79, lab, 'lb_ui_22_semibold', INK, 'right', vis='%s + %s' % (v, on))
        rows += lbl(108 + 936 - 260, y, 200, 79, lab, 'lb_ui_22_semibold', 'ffffffff', 'right', vis='%s + ![%s]' % (v, on))
        rows += img(108 + 936 - 50, y + 27, 26, 26, 'aeon/icons/music.png', INK, aspect='keep', vis='%s + %s' % (v, on))
        rows += img(108 + 936 - 50, y + 27, 26, 26, 'aeon/icons/music.png', 'b3ffffff', aspect='keep', vis='%s + ![%s]' % (v, on))
    out += '\t\t\t<control type="group"><visible>Container.Content(albums) + !Container(532).Scrolling</visible>%s</control>\n' % rows
    # the item in focus
    x, w = 1096, 704
    g = img(x - 30, 138, 360, 360, 'fg/sh24.png', '$VAR[FG_PanelSh_8c]', 64) + img(x, 160, 300, 300, 'fg/r18.png', 'fg_frost', 18)
    g += img(x, 160, 300, 300, '$VAR[FG_M_Square]', diffuse='fg/m300x300.png', aspect='scale', bg=True)
    sx = x + 328
    art_ = 'Container.Content(artists)'
    g += name_block(sx, 160, w - 328, 100, 'lb_ui_28_bold').replace('<label>$VAR[FG_M_Name]</label>', '<label>$VAR[FG_M_Name]</label><wrapmultiline>true</wrapmultiline>')
    g = g.replace('<left>%d</left><top>224</top><width>%d</width><height>46</height>' % (sx, w - 328), '<left>%d</left><top>224</top><width>%d</width><height>84</height>' % (sx, w - 328))
    g += lbl(sx, 276, w - 328, 34, '$VAR[FG_M_Meta]', 'lb_ui_22', 'ccffffff', vis=art_)
    g += lbl(sx, 314, w - 328, 34, '$VAR[FG_M_Meta]', 'lb_ui_22', 'ccffffff', vis='!' + art_)      # under an album name of two lines
    g += img(sx, 380, 170, 60, LABEL_LOGO, 'ebffffff', aspect='keep', align='left', aligny='center', vis=HAS_LABEL)
    bio = ('<control type="textbox"><left>%d</left><top>486</top><width>%d</width><height>%%d</height><font>lb_body_24</font><textcolor>d9ffffff</textcolor>'
           '<label>$VAR[Aeon_M_Bio]</label><autoscroll delay="8000" time="2000" repeat="8000">true</autoscroll><visible>%%s + $EXP[Aeon_VOBio]</visible></control>' % (x, w))
    g += bio % (360, 'Container.Content(artists)') + bio % (554, '!Container.Content(artists)')
    # artists: the album count, the covers moving on, the album's name and year
    g += count_block(cid, x, 900)
    c, m = cycler(cid, x + 100, 880, 150)
    g += c + lbl(x + 274, 900, w - 274, 36, '$INFO[Container(%d).ListItem.Label]' % CYC[cid], 'lb_ui_24_bold', 'ffffffff', vis='Container.Content(artists)')
    g += lbl(x + 274, 938, w - 274, 30, '$INFO[Container(%d).ListItem.Year]' % CYC[cid], 'lb_small_20_semibold', '99ffffff', vis='Container.Content(artists)')
    out += '\t\t\t' + g + '\n' + closing(cid, base, az)
    return out, m | {(300, 300, 18), (62, 62, 10)}


def row533(focused, w=696, h=62):
    lit = 'Control.HasFocus(533)'
    out = ''
    if focused:
        out += img(0, 0, w, h, 'fg/r16.png', 'ffffffff', 16, lit) + img(0, 0, w, h, 'fg/r16.png', '1fffffff', 16, '!' + lit) + img(0, 0, w, h, 'fg/e16.png', '38ffffff', 16, '!' + lit)
        out += img(56, (h - 18) // 2, 18, 18, 'aeon/icons/play.png', INK, aspect='keep', vis=lit)
    ink = '$VAR[FG_M533_Ink]' if focused else 'ffffffff'
    ink2 = '$VAR[FG_M533_Ink2]' if focused else 'a8ffffff'
    out += lbl(6, 0, 40, h, '$INFO[ListItem.TrackNumber]', 'lb_ui_22_semibold', ink2, 'right')
    out += lbl(86, 0, w - 86 - 112, h, '$INFO[ListItem.Title]', 'lb_ui_24_bold' if focused else 'lb_ui_22_semibold', ink)
    # 0.56.8 the list row rule: the length at the right; the play count is not in the row any more
    out += lbl(w - 98, 0, 80, h, '$INFO[ListItem.Duration]', 'lb_ui_22_semibold', ink, 'right')
    return out


def v533(az):
    """Song list: the album at the left (cover; the artist's clearlogo, the album's name, facts, record label logo beside
    it; the review under them), the tracks in a narrower card at the right."""
    cid, base = 533, 53300
    out = opening(cid)
    cov = 380
    g = img(66, 138, cov + 60, cov + 60, 'fg/sh24.png', '$VAR[FG_PanelSh_8c]', 64) + img(96, 160, cov, cov, 'fg/r20.png', 'fg_frost', 20)
    g += img(96, 160, cov, cov, '$VAR[FG_M_Square]', diffuse='fg/m380x380.png', aspect='scale', bg=True)
    ix, iw = 96 + cov + 28, 1040 - 96 - cov - 28 - 40
    g += img(ix, 160, iw, 80, '$VAR[FG_M_ArtistLogo]', aspect='keep', align='left', aligny='center', vis=ART_LOGO)
    g += lbl(ix, 160, iw, 80, '$VAR[FG_M_ArtistName]', 'lb_ui_28_semibold', 'ccffffff', vis='![%s]' % ART_LOGO)
    g += lbl(ix, 250, iw, 100, '$INFO[ListItem.Album]', 'lb_font36_title', 'ffffffff', aligny='top', extra='<wrapmultiline>true</wrapmultiline>')
    g += lbl(ix, 356, iw, 34, '$INFO[ListItem.Year]$INFO[ListItem.Genre,  ·  ,]', 'lb_ui_22', 'ccffffff')
    g += img(ix, 470, 170, 60, LABEL_LOGO, 'ebffffff', aspect='keep', align='left', aligny='center', vis='!String.IsEmpty(ListItem.Property(Album_Label))')
    g += ('<control type="textbox"><left>96</left><top>566</top><width>904</width><height>474</height><font>lb_body_24</font><textcolor>d9ffffff</textcolor>'
          '<label>$VAR[Aeon_M_Bio]</label><autoscroll delay="8000" time="2000" repeat="8000">true</autoscroll><visible>$EXP[Aeon_VOBio]</visible></control>')
    out += '\t\t\t' + g + '\n\t\t\t' + glass(1080, 160, 720, 880) + '\n'
    out += ('\t\t\t<control type="list" id="533"><left>1092</left><top>172</top><width>696</width><height>858</height><pagecontrol>%d</pagecontrol><orientation>vertical</orientation>'
            '<viewtype label="31099">list</viewtype><visible>Container.Content(songs)</visible><scrolltime tween="cubic" easing="out">200</scrolltime>'
            '<onback condition="String.IsEqual(Skin.String(aeon.backmode),home)">ActivateWindow(home)</onback>%s<ondown>Action(FirstPage)</ondown>'
            '<onleft condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onleft><onright>%d</onright>'
            '<itemlayout width="696" height="66">%s</itemlayout><focusedlayout width="696" height="66">%s</focusedlayout></control>\n'
            % (base * 100 + 50, m_up('Integer.IsEqual(Container.CurrentItem,1)'), base * 100 + 1, row533(False), row533(True)))
    out += closing(cid, base, az)
    return out, {(cov, cov, 20)}


def row513(focused, w=980, h=92):
    lit = 'Control.HasFocus(513)'
    out = ''
    if focused:
        out += img(0, 0, w, h, 'fg/r18.png', 'ffffffff', 18, lit) + img(0, 0, w, h, 'fg/r18.png', '1fffffff', 18, '!' + lit) + img(0, 0, w, h, 'fg/e18.png', '38ffffff', 18, '!' + lit)
    ink = '$VAR[FG_M513_Ink]' if focused else 'ffffffff'
    ink2 = '$VAR[FG_M513_Ink2]' if focused else 'a8ffffff'
    song = 'String.IsEqual(ListItem.DBType,song)'
    out += img(12, 14, 64, 64, 'fg/r12.png', '1fffffff', 12, '!' + song)
    out += img(12, 14, 64, 64, '$VAR[FG_M_Square]', diffuse='fg/m64x64.png', aspect='scale', bg=True, vis='!' + song)
    out += lbl(12, 0, 52, h, '$INFO[ListItem.TrackNumber]', 'lb_ui_24_bold', ink2, 'right', vis=song)
    out += lbl(96, 12, w - 380, 38, '$VAR[FG_M_Name]', 'lb_ui_24_bold', ink)
    out += lbl(96, 50, w - 380, 30, '$VAR[FG_M_RowSub]', 'lb_small_20', ink2)
    out += lbl(w - 130, 0, 110, h, '$INFO[ListItem.Duration]', 'lb_ui_22_semibold', ink, 'right', vis=song)
    return out


def v513(az):
    """Fanart list: the list in a card at the left (the library line with position / count, five rows; under them the
    bio, or the artist's clearlogo with the album review, the album count and the moving album cover or the artist's
    photo); at the right the big picture in a card with the clearlogo or the album's facts under it."""
    cid, base = 513, 51300
    out = opening(cid)
    out += '\t\t\t' + glass(96, 160, 1004, 880) + glass(1136, 160, 664, 880) + '\n'
    out += '\t\t\t' + img(122, 182, 24, 24, 'aeon/icons/music.png', 'bfffffff', aspect='keep')
    out += lbl(162, 172, 600, 44, '[UPPERCASE]$VAR[AeonM_Header][/UPPERCASE]', 'lb_cap_16', 'a8ffffff')
    out += lbl(780, 172, 296, 44, '$INFO[Container(513).CurrentItem] / $INFO[Container(513).NumItems]', 'lb_small_20_semibold', 'a8ffffff', 'right') + '\n'
    out += ('\t\t\t<control type="list" id="513"><left>108</left><top>228</top><width>980</width><height>490</height><pagecontrol>%d</pagecontrol><orientation>vertical</orientation>'
            '<viewtype label="535">list</viewtype><visible>Container.Content(artists) | Container.Content(albums) | Container.Content(songs) | Container.Content(genres)</visible>'
            '<scrolltime tween="cubic" easing="out">220</scrolltime><onback condition="String.IsEqual(Skin.String(aeon.backmode),home)">ActivateWindow(home)</onback>'
            '%s<ondown>Action(FirstPage)</ondown><onleft condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onleft><onright>%d</onright>'
            '<itemlayout width="980" height="98">%s</itemlayout><focusedlayout width="980" height="98">%s</focusedlayout></control>\n'
            % (base * 100 + 50, m_up('Integer.IsEqual(Container.CurrentItem,1)'), base * 100 + 1, row513(False), row513(True)))
    # albums: the track count of each row (the helper publishes aeon.tc.<row>) and the run time column
    rows = ''
    for k in range(5):
        p = 'Window(Home).Property(aeon.tc.%d)' % k
        on = 'Integer.IsEqual(Container(513).Position,%d) + Control.HasFocus(513)' % k
        lab = '$INFO[%s]' % p      # 0.56.10: the number and the song icon
        v = '!String.IsEmpty(%s)' % p
        y = 228 + k * 98
        rows += lbl(108 + 980 - 296, y, 236, 92, lab, 'lb_ui_22_semibold', INK, 'right', vis='%s + %s' % (v, on))
        rows += lbl(108 + 980 - 296, y, 236, 92, lab, 'lb_ui_22_semibold', 'ffffffff', 'right', vis='%s + ![%s]' % (v, on))
        rows += img(108 + 980 - 50, y + 33, 26, 26, 'aeon/icons/music.png', INK, aspect='keep', vis='%s + %s' % (v, on))
        rows += img(108 + 980 - 50, y + 33, 26, 26, 'aeon/icons/music.png', 'b3ffffff', aspect='keep', vis='%s + ![%s]' % (v, on))
    out += '\t\t\t<control type="group"><visible>Container.Content(albums) + !Container(513).Scrolling</visible>%s</control>\n' % rows
    # under the rows: the bio (artists) or the artist's clearlogo with the review, the album count and the cover
    g = img(120, 742, 956, 1, 'common/white.png', '24ffffff')
    bio = ('<control type="textbox"><left>124</left><top>%d</top><width>620</width><height>%d</height><font>lb_body_24</font><textcolor>d9ffffff</textcolor>'
           '<label>$VAR[Aeon_M_Bio]</label><autoscroll delay="8000" time="2000" repeat="8000">true</autoscroll><visible>%s + $EXP[Aeon_VOBio]</visible></control>')
    g += bio % (762, 260, 'Container.Content(artists)')
    g += img(124, 760, 360, 56, '$VAR[FG_M_ArtistLogo]', aspect='keep', align='left', aligny='center', vis='!Container.Content(artists) + %s' % ART_LOGO)
    g += lbl(124, 760, 620, 56, '$VAR[FG_M_ArtistName]', 'lb_ui_28_semibold', 'ccffffff', vis='!Container.Content(artists) + ![%s]' % ART_LOGO)
    g += bio % (826, 196, '!Container.Content(artists)')
    g += count_block(cid, 780, 870)
    c, m = cycler(cid, 876, 790, 200)
    g += c
    g += img(876, 790, 200, 200, 'fg/r14.png', 'fg_frost', 14, '!Container.Content(artists)')
    g += img(876, 790, 200, 200, '$VAR[Aeon_M_ArtistThumb]', diffuse='fg/m200x200.png', aspect='scale', bg=True, vis='!Container.Content(artists)')
    out += '\t\t\t' + g + '\n'
    # the right card: the big picture, the clearlogo or the album's facts under it
    r = img(1160, 184, 616, 616, '$VAR[FG_M_Square]', diffuse='fg/m616x616.png', aspect='scale', bg=True)
    r += img(1180, 820, 576, 110, '$VAR[FG_M_ArtistLogo]', aspect='keep', align='center', aligny='center', vis='Container.Content(artists) + ' + ART_LOGO)
    r += lbl(1160, 820, 616, 110, '$INFO[ListItem.Label]', 'lb_font36_title', 'ffffffff', 'center', vis='Container.Content(artists) + ![%s]' % ART_LOGO)
    r += lbl(1160, 940, 616, 34, '$VAR[FG_M_Meta]', 'lb_ui_22', 'ccffffff', 'center', vis='Container.Content(artists)')
    r += lbl(1184, 820, 568, 30, '[UPPERCASE]$INFO[ListItem.Album][/UPPERCASE]', 'lb_cap_16', 'a3ffffff', vis='Container.Content(songs)')
    r += lbl(1184, 848, 568, 50, '$VAR[FG_M_Name]', 'lb_ui_28_bold', 'ffffffff', vis='!Container.Content(artists)')
    r += lbl(1184, 900, 568, 34, '$VAR[FG_M_Meta]', 'lb_ui_22', 'ccffffff', vis='!Container.Content(artists)')
    r += img(1584, 950, 170, 64, LABEL_LOGO, 'ebffffff', aspect='keep', align='right', aligny='center', vis=HAS_LABEL)
    out += '\t\t\t' + r + '\n' + closing(cid, base, az)
    return out, m | {(64, 64, 10), (200, 200, 14), (616, 616, 18)}


def build(az):
    xml = VARS
    for cid in (513, 532, 533):
        xml += ('\t<variable name="FG_M%(c)d_Ink"><value condition="Control.HasFocus(%(c)d)">aeon_onbar</value><value>ffffffff</value></variable>\n'
                '\t<variable name="FG_M%(c)d_Ink2"><value condition="Control.HasFocus(%(c)d)">9e0f1115</value><value>a8ffffff</value></variable>\n' % {'c': cid})
    masks = set()
    for fn in (v513, v530, v531, v532, v533, v534):
        v, m = fn(az)
        xml += v
        masks |= m
    for (w, h, r) in masks:
        rounded_mask(w, h, r)
    return xml
