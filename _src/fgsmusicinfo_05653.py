# -*- coding: utf-8 -*-
"""0.56.53 Music information in the Fused Glass style (user, 2026-11-20, canvas round 2 MusicInfo2: "so good. build
that", the track bars in the gold accent, the record label logo). Other themes / styles keep today's page:
DialogMusicInfo.xml loads MusInfo_PageClassic (today's controls, moved unchanged) when !$EXP[FGS], MusInfo_PageFGS
when $EXP[FGS].

While list 50 has focus Kodi's ListItem.* is the focused row, so the window stores the page's own item at onload
(Window(Home) aeon.mus.type / id / title / artist / year / thumb; cleared at onunload) for the parts that stay on screen.

Screen 1: artist fanart under the gradients (fg/fgs_vi_l / _b); cover 404 at 120,120 with a record sliding out behind it
(albums, songs; round for artists), facts and the record label logo under it; artist (round photo) + title at 720,
the description (9001, OK = full text), the length / end line, one 70 px action row 9000 (8 Play, 9012 Play all,
9011 Shuffle, 12 Info, 6 Refresh, 9013 / 9014 to the artist rows), the track list 50 peeking.
Down (50, -616): the cover and the focused track at the left, ten 70 px rows at 720 (number, title, a gold length bar
in 30 s steps up to 6:00, length) with the style's bar and shadow.
Further: More by the artist 9403 (albums; helper ?info=albums&albumid=) or Top tracks 9401 (artist pages) at -1292,
Similar artists 9402 (round photos) at -1722. Repeatable."""
import io
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import settings_sections as ss  # noqa: E402
import fgsvideoinfo_05653 as vi  # noqa: E402

SKIN = os.path.join(HERE, '..')
INC = os.path.join(SKIN, '1080i', 'Includes_MusicInfo.xml')
WIN = os.path.join(SKIN, '1080i', 'DialogMusicInfo.xml')
A = '<!-- 0.56.53 fgs music info: begin -->'
B = '<!-- 0.56.53 fgs music info: end -->'
ROWS = 'Control.HasFocus(9401) | Control.HasFocus(9402) | Control.HasFocus(9403)'
SCR = '[Control.HasFocus(50) | %s]' % ROWS
SLIDES = (('50', 616), ('9401', 1292), ('9403', 1292), ('9402', 1722))
LINE = vi.LINE
SHADOW = vi.SHADOW
P = 'Window(Home).Property(aeon.mus.%s)'
ALBUM = 'String.IsEqual(%s,album)' % (P % 'type')
ARTIST = 'String.IsEqual(%s,artist)' % (P % 'type')


def textures():
    d = os.path.join(SKIN, 'media', 'fg')
    # the record: grooves, the label in the accent's gold
    n = 512
    im = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    dr.ellipse((0, 0, n - 1, n - 1), fill=(22, 22, 25, 255))
    for r in range(250, 110, -9):
        dr.ellipse((n / 2 - r, n / 2 - r, n / 2 + r, n / 2 + r), outline=(40, 40, 46, 255), width=1)
    dr.ellipse((n / 2 - 96, n / 2 - 96, n / 2 + 96, n / 2 + 96), fill=(232, 176, 75, 255))
    dr.ellipse((n / 2 - 8, n / 2 - 8, n / 2 + 8, n / 2 + 8), fill=(10, 10, 12, 255))
    im.save(os.path.join(d, 'fgs_vinyl.png'))
    # a rounded mask for the 404 cover
    m = Image.new('RGBA', (404, 404), (255, 255, 255, 0))
    ImageDraw.Draw(m).rounded_rectangle((0, 0, 403, 403), radius=12, fill=(255, 255, 255, 255))
    m.save(os.path.join(d, 'm404x404.png'))


def cell(cid, w, label, onclick=(), visible='true'):
    clicks = ''.join('<onclick>%s</onclick>' % c for c in onclick)
    return ('<control type="group"><width>%d</width><height>70</height><visible>%s</visible>'
            '<control type="image"><left>-40</left><top>-34</top><width>%d</width><height>150</height>%s'
            '<visible>Control.HasFocus(%s) + $EXP[FGS_ShadowOn]</visible></control>'
            '<control type="button" id="%s"><left>0</left><top>0</top><width>%d</width><height>70</height>'
            '<font>uc_st_ui_22_bold</font><textcolor>ccffffff</textcolor><focusedcolor>ffffffff</focusedcolor>'
            '<disabledcolor>44ffffff</disabledcolor><align>center</align><aligny>center</aligny><textoffsetx>20</textoffsetx>'
            '<label>%s</label><texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texturefocus><texturenofocus />'
            '<onup>noop</onup><ondown condition="Integer.IsGreater(Container(50).NumItems,0)">50</ondown>'
            '<ondown condition="!Integer.IsGreater(Container(50).NumItems,0) + Control.IsVisible(9001)">9001</ondown>'
            '%s<include>FGS_RowAnim</include></control>'
            '<control type="image"><left>%d</left><top>0</top><width>1</width><height>70</height><texture colordiffuse="%s">common/white.png</texture></control></control>'
            % (w, visible, w + 80, SHADOW, cid, cid, w, label, clicks, w - 1, LINE))


def hero():
    o = []
    a = o.append
    a('<control type="group"><visible>!%s</visible><animation effect="fade" time="200">VisibleChange</animation>' % SCR)
    a('<control type="image"><left>290</left><top>132</top><width>380</width><height>380</height><texture>fg/fgs_vinyl.png</texture>'
      '<visible>!$EXP[Music_InfoIsArtist]</visible><animation effect="slide" start="-170,0" end="0,0" delay="300" time="500" tween="cubic" easing="out">WindowOpen</animation></control>')
    a('<control type="image"><left>80</left><top>86</top><width>484</width><height>484</height>%s</control>' % SHADOW)
    a('<control type="image"><left>120</left><top>120</top><width>404</width><height>404</height><aspectratio scalediffuse="false">scale</aspectratio><fadetime>200</fadetime>'
      '<texture background="true" diffuse="fg/m404x404.png">$VAR[MusInfo_Cover]</texture><visible>!$EXP[Music_InfoIsArtist]</visible></control>')
    a('<control type="image"><left>120</left><top>120</top><width>404</width><height>404</height><aspectratio scalediffuse="false">scale</aspectratio><fadetime>200</fadetime>'
      '<texture background="true" diffuse="aeon/mask_circle.png">$VAR[MusInfo_Cover]</texture><visible>$EXP[Music_InfoIsArtist]</visible></control>')
    a('<control type="grouplist"><left>120</left><top>548</top><width>404</width><height>170</height><orientation>vertical</orientation><itemgap>4</itemgap><usecontrolcoords>true</usecontrolcoords>'
      '<control type="label"><width>404</width><height>40</height><aligny>center</aligny><font>st_ui_24_semibold</font><textcolor>ffffffff</textcolor><label>$VAR[MusInfo_Meta]</label></control>'
      '<control type="label"><width>404</width><height>34</height><aligny>center</aligny><font>st_small_20</font><textcolor>b8ffffff</textcolor><label>[COLOR 73ffffff]$LOCALIZE[31067][/COLOR]  $INFO[ListItem.Property(Album_Label)]</label><visible>!String.IsEmpty(ListItem.Property(Album_Label))</visible></control>'
      '<control type="label"><width>404</width><height>34</height><aligny>center</aligny><font>st_small_20</font><textcolor>b8ffffff</textcolor><label>[COLOR 73ffffff]$LOCALIZE[31536][/COLOR]  $INFO[ListItem.Property(Album_Mood)]</label><visible>!String.IsEmpty(ListItem.Property(Album_Mood))</visible></control>'
      '<control type="label"><width>404</width><height>34</height><aligny>center</aligny><font>st_small_20</font><textcolor>b8ffffff</textcolor><label>[COLOR 73ffffff]$LOCALIZE[31534][/COLOR]  $INFO[ListItem.DateAdded]</label><visible>!String.IsEmpty(ListItem.DateAdded)</visible></control>'
      '</control>')
    # the record label's logo (user note)
    a('<control type="image"><left>120</left><top>730</top><width>300</width><height>80</height><aspectratio align="left" aligny="center">keep</aspectratio>'
      '<texture background="true">resource://resource.images.recordlabels.white/$INFO[ListItem.Property(Album_Label)].png</texture>'
      '<visible>!String.IsEmpty(ListItem.Property(Album_Label))</visible></control>')
    # artist + title
    a('<control type="image"><left>720</left><top>140</top><width>56</width><height>56</height><aspectratio scalediffuse="false">scale</aspectratio>'
      '<texture background="true" diffuse="aeon/mask_circle.png">$INFO[ListItem.Art(artist.thumb)]</texture><visible>!String.IsEmpty(ListItem.Art(artist.thumb))</visible></control>')
    a('<control type="label"><left>792</left><top>140</top><width>1028</width><height>56</height><aligny>center</aligny><font>st_ui_24_semibold</font><textcolor>e6ffffff</textcolor>'
      '<label>$INFO[ListItem.Artist]</label><visible>!$EXP[Music_InfoIsArtist]</visible></control>')
    a('<control type="label"><left>720</left><top>206</top><width>1100</width><height>120</height><aligny>center</aligny><font>st_display_84</font><textcolor>ffffffff</textcolor>'
      '<label>[UPPERCASE]$VAR[Music_InfoTitle][/UPPERCASE]</label></control>')
    # description: OK opens the full text
    a('<control type="image"><left>704</left><top>334</top><width>1132</width><height>150</height><texture border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texture><visible>Control.HasFocus(9001)</visible></control>')
    a('<control type="textbox"><left>720</left><top>342</top><width>1100</width><height>134</height><font>st_body_24</font><textcolor>d9ffffff</textcolor>'
      '<label>$VAR[Music_InfoDescription]</label><autoscroll delay="8000" time="3000" repeat="10000">!Control.HasFocus(9001)</autoscroll><visible>$EXP[Music_InfoHasDescription]</visible></control>')
    a('<control type="button" id="9001"><left>704</left><top>334</top><width>1132</width><height>150</height><label></label><texturefocus /><texturenofocus />'
      '<onup>9000</onup><ondown condition="Integer.IsGreater(Container(50).NumItems,0)">50</ondown><onleft>noop</onleft><onright>noop</onright>'
      '<onclick>SetFocus(61)</onclick><visible>$EXP[Music_InfoHasDescription]</visible></control>')
    a('<control type="label"><left>720</left><top>496</top><width>1100</width><height>40</height><aligny>center</aligny><font>st_ui_24</font><textcolor>b8ffffff</textcolor>'
      '<label>$VAR[MusInfo_EndLine]</label></control>')
    # 0.3.117 helper: the album's tracks as ranges (aeon.alb.*), the first one in the accent
    alb = ('String.IsEqual(Window(Home).Property(aeon.alb.id),Window(Home).Property(aeon.mus.id)) + %s + '
           '!String.IsEmpty(Window(Home).Property(aeon.alb.ranges))' % ALBUM)
    a('<control type="ranges"><left>720</left><top>544</top><width>1100</width><height>10</height><texturebg></texturebg><lefttexture /><righttexture />'
      '<midtexture colordiffuse="47ffffff">common/white.png</midtexture><info>Window(Home).Property(aeon.alb.ranges)</info><visible>%s</visible></control>' % alb)
    a('<control type="ranges"><left>720</left><top>544</top><width>1100</width><height>10</height><texturebg></texturebg><lefttexture /><righttexture />'
      '<midtexture colordiffuse="fg_mark">common/white.png</midtexture><info>Window(Home).Property(aeon.alb.first)</info><visible>%s</visible></control>' % alb)
    # action row
    a('<control type="image"><left>720</left><top>580</top><width>1100</width><height>1</height><texture colordiffuse="%s">common/white.png</texture></control>' % LINE)
    a('<control type="image"><left>720</left><top>650</top><width>1100</width><height>1</height><texture colordiffuse="%s">common/white.png</texture></control>' % LINE)
    a('<control type="image"><left>720</left><top>580</top><width>1</width><height>71</height><texture colordiffuse="%s">common/white.png</texture></control>' % LINE)
    row = [
        cell('8', 150, '$LOCALIZE[31278]', visible='!$EXP[Music_InfoIsArtist]'),
        cell('9012', 200, '$LOCALIZE[31531]', ('PlayMedia(musicdb://artists/$INFO[ListItem.DBID]/,isdir)',), '$EXP[Music_InfoIsArtist] + Integer.IsGreater(ListItem.DBID,0)'),
        cell('9011', 170, '$LOCALIZE[31532]', ('$VAR[Music_InfoShuffleAction]', 'PlayerControl(RandomOn)'), '[$EXP[Music_InfoIsAlbum] | $EXP[Music_InfoIsArtist]] + Integer.IsGreater(ListItem.DBID,0)'),
        cell('12', 270, '$VAR[MusInfo_InfoLabel]', visible='!$EXP[Music_InfoIsArtist]'),
        cell('6', 170, '$LOCALIZE[31533]', visible='!$EXP[Music_InfoIsSong]'),
        cell('9013', 210, '$LOCALIZE[31887]', ('SetFocus(9401)',), '$EXP[Music_InfoIsArtist] + Integer.IsGreater(Container(9401).NumItems,0)'),
        cell('9014', 260, '$LOCALIZE[31888]', ('SetFocus(9402)',), 'Integer.IsGreater(Container(9402).NumItems,0)'),
    ]
    a('<control type="grouplist" id="9000"><left>721</left><top>581</top><width>1099</width><height>70</height><orientation>horizontal</orientation><itemgap>0</itemgap>'
      '<usecontrolcoords>true</usecontrolcoords><onup>noop</onup><onleft>noop</onleft><onright>noop</onright>'
      '<ondown condition="Integer.IsGreater(Container(50).NumItems,0)">50</ondown><ondown condition="!Integer.IsGreater(Container(50).NumItems,0) + Control.IsVisible(9001)">9001</ondown>'
      '%s</control>' % ''.join(row))
    a('</control>')
    return ''.join(o)


def track_row(focused):
    bar = ''.join('<control type="image"><left>%d</left><top>33</top><width>14</width><height>4</height><texture colordiffuse="fg_mark">common/white.png</texture>'
                  '<visible>Integer.IsGreater(ListItem.Duration(secs),%d)</visible></control>' % (840 + 15 * k, 30 * k) for k in range(12))
    sh = ('<control type="image"><left>-40</left><top>-34</top><width>1180</width><height>150</height>%s<visible>Control.HasFocus(50) + $EXP[FGS_ShadowOn]</visible></control>'
          '<control type="image"><left>0</left><top>0</top><width>1100</width><height>70</height><texture border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texture>'
          '<visible>Control.HasFocus(50)</visible></control>' % SHADOW) if focused else ''
    ink = 'ffffffff' if focused else 'ccffffff'
    return (sh +
            '<control type="image"><left>0</left><top>69</top><width>1100</width><height>1</height><texture colordiffuse="14ffffff">common/white.png</texture></control>'
            # songs
            '<control type="label"><left>24</left><top>0</top><width>50</width><height>70</height><aligny>center</aligny><font>st_small_20</font><textcolor>73ffffff</textcolor>'
            '<label>$INFO[ListItem.TrackNumber]</label><visible>String.IsEqual(ListItem.DBType,song)</visible></control>'
            '<control type="label"><left>84</left><top>0</top><width>890</width><height>70</height><aligny>center</aligny><font>st_ui_24_semibold</font><textcolor>%s</textcolor>'
            '<label>$VAR[MusInfo_RowTitle]</label><visible>String.IsEqual(ListItem.DBType,song)</visible></control>'
            # albums (an artist's discography): cover + title
            '<control type="image"><left>14</left><top>9</top><width>52</width><height>52</height><aspectratio>scale</aspectratio><texture background="true">$VAR[MusInfo_RowArt]</texture>'
            '<visible>!String.IsEqual(ListItem.DBType,song)</visible></control>'
            '<control type="label"><left>84</left><top>0</top><width>900</width><height>70</height><aligny>center</aligny><font>st_ui_24_semibold</font><textcolor>%s</textcolor>'
            '<label>$VAR[MusInfo_RowTitle]</label><visible>!String.IsEqual(ListItem.DBType,song)</visible></control>'
            '<control type="label"><left>1000</left><top>0</top><width>76</width><height>70</height><align>right</align><aligny>center</aligny><font>st_small_20</font>'
            '<textcolor>99ffffff</textcolor><label>$VAR[MusInfo_RowRight]</label></control>' % (ink, ink))


def square_item(lid, focused, round_=False):
    f = 'true' if focused else 'false'
    mask = 'aeon/mask_circle.png' if round_ else 'fg/m260x260.png'
    ring = ('<control type="image"><left>-6</left><top>-6</top><width>272</width><height>272</height><texture colordiffuse="ffffffff">aeon/ring_cast.png</texture>'
            if round_ else
            '<control type="image"><left>-3</left><top>-3</top><width>266</width><height>266</height><texture border="19" colordiffuse="ffffffff">fg/ring16.png</texture>')
    return ('<control type="group"><left>14</left><top>10</top><width>260</width><height>260</height>%s'
            '<control type="image"><left>0</left><top>0</top><width>260</width><height>260</height><aspectratio scalediffuse="false">scale</aspectratio>'
            '<texture background="true" diffuse="%s">$INFO[ListItem.Art(thumb)]</texture></control>'
            '<control type="image"><left>0</left><top>0</top><width>260</width><height>260</height><texture diffuse="%s" colordiffuse="b0000000">common/white.png</texture>'
            '<visible>!String.IsEmpty(ListItem.Property(aeon.missing)) + ![%s + Control.HasFocus(%s)]</visible></control>'
            '%s<visible>%s + Control.HasFocus(%s)</visible></control></control>'
            '<control type="label"><left>14</left><top>282</top><width>260</width><height>30</height><aligny>center</aligny><font>st_small_20_semibold</font><textcolor>e6ffffff</textcolor>'
            '<label>$INFO[ListItem.Label]</label>%s</control>'
            '<control type="label"><left>14</left><top>310</top><width>260</width><height>28</height><aligny>center</aligny><font>st_small_20</font><textcolor>8cffffff</textcolor>'
            '<label>$INFO[ListItem.Year]$INFO[ListItem.Album]</label></control>'
            % ('<include>Anim_FocusZoom</include>' if focused else '', mask, mask, f, lid, ring, f, lid,
               '<align>center</align>' if round_ else ''))


def lower():
    o = []
    a = o.append
    fade = '<animation effect="fade" time="200">VisibleChange</animation>'
    # tracks
    a('<control type="group"><visible>Integer.IsGreater(Container(50).NumItems,0) + !Control.HasFocus(50) + ![%s]</visible>%s' % (ROWS, fade))
    a('<control type="label"><left>720</left><top>766</top><width>1100</width><height>40</height><aligny>center</aligny><font>st_ui_28_bold</font><textcolor>ffffffff</textcolor>'
      '<label>[UPPERCASE]$VAR[Music_InfoListCaption][/UPPERCASE]</label></control></control>')
    a('<control type="list" id="50"><left>720</left><top>816</top><width>1100</width><height>700</height><orientation>vertical</orientation>'
      '<scrolltime tween="cubic" easing="out">200</scrolltime><onup>9000</onup>'
      '<ondown condition="Integer.IsGreater(Container(9401).NumItems,0)">9401</ondown>'
      '<ondown condition="!Integer.IsGreater(Container(9401).NumItems,0) + Integer.IsGreater(Container(9403).NumItems,0)">9403</ondown>'
      '<ondown condition="!Integer.IsGreater(Container(9401).NumItems,0) + !Integer.IsGreater(Container(9403).NumItems,0) + Integer.IsGreater(Container(9402).NumItems,0)">9402</ondown>'
      '<onleft>noop</onleft><onright>noop</onright><visible>![%s]</visible>%s'
      '<itemlayout width="1100" height="70">%s</itemlayout><focusedlayout width="1100" height="70">%s</focusedlayout></control>'
      % (ROWS, fade, track_row(False), track_row(True)))
    rows = (('9401', 1560, '$LOCALIZE[31887]', '$VAR[MusInfo_TracksPath]', 'PlayMedia($INFO[ListItem.FileNameAndPath])', False, '!Control.HasFocus(9402)'),
            ('9403', 1560, '$ADDON[skin.aeon.fuse 32798]', '$VAR[FGS_MusAlbumsPath]', 'ActivateWindow(Music,$INFO[ListItem.FolderPath],return)', False, '!Control.HasFocus(9402)'),
            ('9402', 1990, '$LOCALIZE[31888]', '$VAR[FGS_MusSimilarPath]', 'ActivateWindow(Music,$INFO[ListItem.FolderPath],return)', True, 'true'))
    for lid, top, label, path, click, round_, vis in rows:
        a(vi.heading(top, label, '$INFO[Container(%s).NumItems]' % lid, 'Integer.IsGreater(Container(%s).NumItems,0) + %s' % (lid, vis)))
        up = ('<onup condition="Integer.IsGreater(Container(9401).NumItems,0)">9401</onup>'
              '<onup condition="!Integer.IsGreater(Container(9401).NumItems,0) + Integer.IsGreater(Container(9403).NumItems,0)">9403</onup>'
              '<onup condition="!Integer.IsGreater(Container(9401).NumItems,0) + !Integer.IsGreater(Container(9403).NumItems,0) + Integer.IsGreater(Container(50).NumItems,0)">50</onup>'
              '<onup condition="!Integer.IsGreater(Container(9401).NumItems,0) + !Integer.IsGreater(Container(9403).NumItems,0) + !Integer.IsGreater(Container(50).NumItems,0)">9000</onup>'
              '<ondown>noop</ondown>') if lid == '9402' else \
             ('<onup condition="Integer.IsGreater(Container(50).NumItems,0)">50</onup><onup condition="!Integer.IsGreater(Container(50).NumItems,0)">9000</onup>'
              '<ondown condition="Integer.IsGreater(Container(9402).NumItems,0)">9402</ondown>')
        clicks = ('<onclick condition="String.IsEmpty(ListItem.Property(aeon.missing))">%s</onclick>' % click) if lid == '9401' else \
                 ('<onclick condition="String.IsEmpty(ListItem.Property(aeon.missing))">Dialog.Close(musicinformation,true)</onclick>'
                  '<onclick condition="String.IsEmpty(ListItem.Property(aeon.missing))">%s</onclick>' % click)
        a('<control type="list" id="%s"><left>106</left><top>%d</top><width>1728</width><height>350</height><orientation>horizontal</orientation>'
          '<scrolltime tween="cubic" easing="out">200</scrolltime>%s<onleft>noop</onleft><onright>noop</onright>%s<visible>%s</visible>%s'
          '<itemlayout width="288" height="350">%s</itemlayout><focusedlayout width="288" height="350">%s</focusedlayout>'
          '<content target="music" limit="12">%s</content></control>'
          % (lid, top + 50, up, clicks, vis, fade, square_item(lid, False, round_), square_item(lid, True, round_), path))
    return ''.join(o)


def fixed():
    """what stays at the top while the page is down"""
    return (
        # beside the tracks: the cover and the focused track
        '<control type="group"><visible>Control.HasFocus(50)</visible><animation effect="fade" time="250">VisibleChange</animation>'
        '<control type="image"><left>80</left><top>116</top><width>380</width><height>380</height>%s</control>'
        '<control type="image"><left>120</left><top>150</top><width>300</width><height>300</height><aspectratio scalediffuse="false">scale</aspectratio>'
        '<texture background="true" diffuse="fg/m300x300.png">$INFO[%s]</texture></control>'
        '<control type="label"><left>120</left><top>470</top><width>540</width><height>44</height><aligny>center</aligny><font>st_ui_28_bold</font><textcolor>ffffffff</textcolor>'
        '<label>[UPPERCASE]$INFO[%s][/UPPERCASE]</label></control>'
        '<control type="label"><left>120</left><top>512</top><width>540</width><height>32</height><aligny>center</aligny><font>st_small_20</font><textcolor>a6ffffff</textcolor>'
        '<label>$INFO[%s]$INFO[%s,  ·  ,]</label></control>'
        '<control type="label"><left>120</left><top>590</top><width>540</width><height>26</height><aligny>center</aligny><font>st_cap_14</font><textcolor>73ffffff</textcolor>'
        '<label>[UPPERCASE]$VAR[MusInfo_Hint][/UPPERCASE]</label></control>'
        '<control type="label"><left>120</left><top>620</top><width>540</width><height>40</height><aligny>center</aligny><font>st_ui_24_semibold</font><textcolor>ffffffff</textcolor>'
        '<label>$INFO[Container(50).ListItem.Title]</label></control>'
        '<control type="label"><left>120</left><top>660</top><width>540</width><height>32</height><aligny>center</aligny><font>st_small_20</font><textcolor>a6ffffff</textcolor>'
        '<label>$INFO[Container(50).ListItem.Duration]$INFO[Container(50).ListItem.PlayCount,  ·  ,×]</label></control>'
        '<control type="label"><left>720</left><top>130</top><width>1100</width><height>40</height><aligny>center</aligny><font>st_ui_28_bold</font><textcolor>ffffffff</textcolor>'
        '<label>[UPPERCASE]$VAR[Music_InfoListCaption][/UPPERCASE]</label></control>'
        '</control>'
        # the strip over the rows
        '<control type="group"><visible>%s</visible><animation effect="fade" time="250">VisibleChange</animation>'
        '<control type="image"><left>120</left><top>128</top><width>72</width><height>72</height><aspectratio scalediffuse="false">scale</aspectratio>'
        '<texture background="true" diffuse="fg/m72x72.png">$INFO[%s]</texture></control>'
        '<control type="label"><left>212</left><top>126</top><width>1290</width><height>40</height><aligny>center</aligny><font>st_ui_28_bold</font><textcolor>ffffffff</textcolor>'
        '<label>[UPPERCASE]$INFO[%s][/UPPERCASE]</label></control>'
        '<control type="label"><left>212</left><top>164</top><width>1290</width><height>32</height><aligny>center</aligny><font>st_small_20</font><textcolor>a6ffffff</textcolor>'
        '<label>$INFO[%s]$INFO[%s,  ·  ,]</label></control>'
        '<control type="image"><left>1520</left><top>124</top><width>300</width><height>80</height><aspectratio align="right" aligny="center">keep</aspectratio>'
        '<texture background="true">resource://resource.images.recordlabels.white/$INFO[ListItem.Property(Album_Label)].png</texture>'
        '<visible>!String.IsEmpty(ListItem.Property(Album_Label))</visible></control>'
        '<control type="image"><left>120</left><top>226</top><width>1700</width><height>1</height><texture colordiffuse="%s">common/white.png</texture></control>'
        '</control>' % (SHADOW, P % 'thumb', P % 'title', P % 'artist', P % 'year', ROWS, P % 'thumb', P % 'title', P % 'artist', P % 'year', LINE))


VARS = '''	<variable name="FGS_MusTypeName">
		<value condition="String.IsEqual(Window(Home).Property(aeon.mus.type),artist)">$LOCALIZE[133]</value>
		<value condition="String.IsEqual(Window(Home).Property(aeon.mus.type),song)">$LOCALIZE[134]</value>
		<value>$LOCALIZE[132]</value>
	</variable>
	<variable name="FGS_MusAlbumsPath">
		<value condition="String.IsEqual(Window(Home).Property(aeon.mus.type),album) + !String.IsEmpty(Window(Home).Property(aeon.mus.id))">plugin://script.aeon.helper/?info=albums&amp;albumid=$INFO[Window(Home).Property(aeon.mus.id)]</value>
		<value>special://skin/shortcuts/customrows-none.xsp</value>
	</variable>
	<variable name="FGS_MusSimilarPath">
		<value condition="!String.IsEmpty(Window(Home).Property(aeon.artist.id))">plugin://script.aeon.helper/?info=similar&amp;artistid=$INFO[Window(Home).Property(aeon.artist.id)]</value>
		<value condition="String.IsEqual(Window(Home).Property(aeon.mus.type),album) + !String.IsEmpty(Window(Home).Property(aeon.mus.id))">plugin://script.aeon.helper/?info=similar&amp;albumid=$INFO[Window(Home).Property(aeon.mus.id)]</value>
		<value>special://skin/shortcuts/customrows-none.xsp</value>
	</variable>
'''
ONLOAD = ['<onload>SetProperty(aeon.mus.type,$INFO[ListItem.DBType],home)</onload>',
          '<onload>SetProperty(aeon.mus.id,$INFO[ListItem.DBID],home)</onload>',
          '<onload>SetProperty(aeon.mus.title,$ESCINFO[ListItem.Label],home)</onload>',
          '<onload>SetProperty(aeon.mus.artist,$ESCINFO[ListItem.Artist],home)</onload>',
          '<onload>SetProperty(aeon.mus.year,$INFO[ListItem.Year],home)</onload>',
          '<onload>SetProperty(aeon.mus.thumb,$ESCINFO[ListItem.Art(thumb)],home)</onload>']
ONUNLOAD = ['<onunload>ClearProperty(aeon.mus.%s,home)</onunload>' % k for k in ('type', 'id', 'title', 'artist', 'year', 'thumb')]


def page():
    slides = ''.join(
        '<animation type="Conditional" condition="Control.HasFocus(%s) + !Skin.HasSetting(aeon.reducemotion)" reversible="true"><effect type="slide" start="0,0" end="0,-%d" time="340" tween="sine" easing="inout"/></animation>'
        '<animation type="Conditional" condition="Control.HasFocus(%s) + Skin.HasSetting(aeon.reducemotion)" reversible="true"><effect type="slide" start="0,0" end="0,-%d" time="0"/></animation>'
        % (c, d, c, d) for c, d in SLIDES)
    return (
        '<include name="MusInfo_PageFGS">\n'
        '<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture colordiffuse="ff08090c">common/white.png</texture></control>'
        '<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><aspectratio>scale</aspectratio><fadetime>300</fadetime>'
        '<texture background="true">$VAR[MusInfo_Fanart]</texture><visible>!Skin.HasSetting(aeon.nobackdrop)</visible></control>'
        '<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture>fg/fgs_vi_l.png</texture></control>'
        '<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture>fg/fgs_vi_b.png</texture></control>'
        '<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture colordiffuse="b008090c">common/white.png</texture>'
        '<visible>%s</visible><animation effect="fade" time="300">VisibleChange</animation></control>'
        '<include content="FGS_DlgHeader"><param name="lead" value="$VAR[FGS_MusTypeName]"/><param name="leadvis" value="true"/><param name="label" value="$LOCALIZE[31573]"/></include>'
        '<include>Aeon_ClockBox</include>%s'
        '<control type="group">%s%s%s</control>'
        '<include>MusInfo_FullText</include>\n'
        '</include>' % (SCR, fixed(), slides, hero(), lower()))


def main():
    textures()
    for need in ('m300x300.png', 'm260x260.png', 'm72x72.png'):
        if not os.path.exists(os.path.join(SKIN, 'media', 'fg', need)):
            w = int(need[1:].split('x')[0])
            m = Image.new('RGBA', (w, w), (255, 255, 255, 0))
            ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, w - 1), radius=max(6, w // 24), fill=(255, 255, 255, 255))
            m.save(os.path.join(SKIN, 'media', 'fg', need))
            print('  made', need)
    s = io.open(INC, encoding='utf-8').read()
    if A in s:
        s = s[:s.index(A)] + s[s.index(B) + len(B):]
    w = io.open(WIN, encoding='utf-8').read()
    if 'MusInfo_PageClassic' not in w:
        a = w.index('<controls>') + len('<controls>')
        b = w.index('</controls>')
        classic = w[a:b]
        w = (w[:a] + '\n\t\t<include condition="!$EXP[FGS]">MusInfo_PageClassic</include>'
             '\n\t\t<include condition="$EXP[FGS]">MusInfo_PageFGS</include>\n\t' + w[b:])
        k = w.index('<onunload>ClearProperty(aeon.artist.id,home)</onunload>')
        w = w[:k] + '\n\t'.join(ONLOAD + ONUNLOAD) + '\n\t' + w[k:]
        io.open(WIN, 'w', encoding='utf-8', newline='\n').write(w)
        s = s.replace('</includes>', '\t<!-- 0.56.53: today\'s page, moved from DialogMusicInfo.xml unchanged (every theme and style but Fused Glass style) -->\n'
                      '\t<include name="MusInfo_PageClassic">' + classic + '</include>\n</includes>')
    s = s.replace('</includes>', '\t%s\n%s\t%s\n\t%s\n</includes>' % (A, VARS, page(), B))
    io.open(INC, 'w', encoding='utf-8', newline='\n').write(s)
    print('fgs music info: page written')


if __name__ == '__main__':
    main()
