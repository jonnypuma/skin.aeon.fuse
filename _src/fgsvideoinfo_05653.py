# -*- coding: utf-8 -*-
"""0.56.53 Video information in the Fused Glass style (user, 2026-11-20, canvas round 2 VideoInfo2: "so good. build
that"; keep the faded gradient over the fanart, round cast photos, Down to similar items). The other themes and styles
keep today's page exactly: DialogVideoInfo.xml now loads VidInfo_PageClassic (today's controls, moved unchanged) when
!$EXP[FGS] and VidInfo_PageFGS when $EXP[FGS] (conditional includes, resolved when the window loads).

The FGS page (screen coordinates, one 1920x1080 screen; the page slides up while a lower row has focus):
- the fanart full screen under two gradients (fg/fgs_vi_l.png dark at the left, fg/fgs_vi_b.png dark at the foot),
  a darker veil while a lower row has focus; the style's header and the clock box;
- screen 1: poster 120,120 300x450 (shadow), facts under it (meta, director, writer, studio); clear logo (else the
  title) at 480, tagline in the accent, rating + genre + ends line, the media chips (today's chip row, unchanged),
  the plot (9001: OK opens the full plot 9200/61), the watched bar, one 70 px action row 9000 (cells line to line,
  fgs_bar_dk focus with the focus shadow): Resume 9 / Play 8 / From start 9013 / Browse 9012 / Trailer 9016 /
  Versions 14 / Extras 15 / More 9010 -> More row 9100 in the same place (443 13 7 10 12 6, Back returns);
- the cast (50) peeks in at the foot; Down slides the page 534 px: a compact strip (logo, meta) stays at the top,
  the cast as round photos with names and roles, the crew (director, writer, studio), the file (video, audio,
  subtitles, runtime) as cells, the Recommended row peeking;
- Recommended 9301 (-1182), Similar 9302 (-1682), Reviews 9303 (-2182): posters 220x330, rounded, white ring.
Repeatable: the includes live between markers; the window is wrapped once."""
import io
import os
import re
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import settings_sections as ss  # noqa: E402

SKIN = os.path.join(HERE, '..')
INC = os.path.join(SKIN, '1080i', 'Includes_VideoInfo.xml')
WIN = os.path.join(SKIN, '1080i', 'DialogVideoInfo.xml')
A = '<!-- 0.56.53 fgs video info: begin -->'
B = '<!-- 0.56.53 fgs video info: end -->'
SCR = '[Control.HasFocus(50) | Control.HasFocus(9301) | Control.HasFocus(9302) | Control.HasFocus(9303)]'
SLIDES = (('50', 608), ('9301', 1256), ('9302', 1756), ('9303', 2256))
LINE = '24ffffff'
SHADOW = '<texture border="56" colordiffuse="$VAR[FG_ShadowColM]">fg/sh16.png</texture>'


def textures():
    """the two gradients over the fanart (alpha only, black)"""
    def ramp(stops, x):
        for (x0, a0), (x1, a1) in zip(stops, stops[1:]):
            if x0 <= x <= x1:
                return a0 + (a1 - a0) * (x - x0) / float(x1 - x0)
        return stops[-1][1]
    w = 512
    im = Image.new('RGBA', (w, 8))
    st = [(0, .97), (.28, .90), (.58, .45), (1, .12)]
    for x in range(w):
        a = int(255 * ramp(st, x / float(w - 1)))
        for y in range(8):
            im.putpixel((x, y), (8, 9, 12, a))
    im.save(os.path.join(SKIN, 'media', 'fg', 'fgs_vi_l.png'))
    im = Image.new('RGBA', (8, w))
    st = [(0, 0), (.55, 0), (.78, .55), (1, .96)]
    for y in range(w):
        a = int(255 * ramp(st, y / float(w - 1)))
        for x in range(8):
            im.putpixel((x, y), (8, 9, 12, a))
    im.save(os.path.join(SKIN, 'media', 'fg', 'fgs_vi_b.png'))


def chips(s):
    """today's chip row from VidInfo_Hero, as it is"""
    a = s.index('<include name="VidInfo_Hero">')
    i = s.index('<!-- media chips: the same as the library bar', a)
    j = s.index('<control type="grouplist">', i)
    m = ss.masked(s)
    e = ss.ctl_end(m, j)
    x = s[j:e]
    x = x.replace('<width>1290</width><height>34</height>', '<left>480</left><top>352</top><width>1340</width><height>34</height>', 1)
    return x


def cell(cid, w, label, onclick=(), visible='true', down=True):
    """one action cell: a group (the shadow is its sibling) with the button and the line at its right"""
    clicks = ''.join('<onclick>%s</onclick>' % c for c in onclick)
    nav = ('<onup>noop</onup><ondown condition="Control.IsVisible(9001)">9001</ondown>'
           '<ondown condition="!Control.IsVisible(9001) + Integer.IsGreater(Container(50).NumItems,0)">50</ondown>') if down else \
          '<onup>9010</onup><ondown>9010</ondown>'
    return ('<control type="group"><width>%d</width><height>70</height><visible>%s</visible>'
            '<control type="image"><left>-40</left><top>-34</top><width>%d</width><height>150</height>%s'
            '<visible>Control.HasFocus(%s) + $EXP[FGS_ShadowOn]</visible></control>'
            '<control type="button" id="%s"><left>0</left><top>0</top><width>%d</width><height>70</height>'
            '<font>uc_st_ui_22_bold</font><textcolor>ccffffff</textcolor><focusedcolor>ffffffff</focusedcolor>'
            '<disabledcolor>44ffffff</disabledcolor><align>center</align><aligny>center</aligny><textoffsetx>20</textoffsetx>'
            '<label>%s</label><texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texturefocus>'
            '<texturenofocus />%s%s<include>FGS_RowAnim</include></control>'
            '<control type="image"><left>%d</left><top>0</top><width>1</width><height>70</height>'
            '<texture colordiffuse="%s">common/white.png</texture></control></control>'
            % (w, visible, w + 80, SHADOW, cid, cid, w, label, nav, clicks, w - 1, LINE))


def hero(s):
    out = []
    o = out.append
    o('<control type="group"><visible>!%s</visible>' % SCR)
    o('<animation effect="fade" time="200">VisibleChange</animation>')
    # poster + facts
    o('<control type="image"><left>80</left><top>86</top><width>380</width><height>530</height>%s</control>' % SHADOW)
    o('<control type="image"><left>120</left><top>120</top><width>300</width><height>450</height><aspectratio scalediffuse="false">scale</aspectratio>'
      '<fadetime>200</fadetime><texture background="true" diffuse="fg/m300x450.png">$VAR[VidInfo_Poster]</texture></control>')
    o('<control type="grouplist"><left>120</left><top>590</top><width>300</width><height>190</height><orientation>vertical</orientation><itemgap>4</itemgap><usecontrolcoords>true</usecontrolcoords>'
      '<control type="label"><width>300</width><height>40</height><aligny>center</aligny><font>st_ui_24_semibold</font><textcolor>ffffffff</textcolor><label>$VAR[VidInfo_MetaLeft]</label></control>'
      '<control type="label"><width>300</width><height>34</height><aligny>center</aligny><font>st_small_20</font><textcolor>b8ffffff</textcolor><label>[COLOR 73ffffff]$LOCALIZE[20339][/COLOR]  $INFO[ListItem.Director]</label><visible>!String.IsEmpty(ListItem.Director)</visible></control>'
      '<control type="label"><width>300</width><height>34</height><aligny>center</aligny><font>st_small_20</font><textcolor>b8ffffff</textcolor><label>[COLOR 73ffffff]$LOCALIZE[20417][/COLOR]  $INFO[ListItem.Writer]</label><visible>!String.IsEmpty(ListItem.Writer)</visible></control>'
      '<control type="label"><width>300</width><height>34</height><aligny>center</aligny><font>st_small_20</font><textcolor>b8ffffff</textcolor><label>[COLOR 73ffffff]$LOCALIZE[572][/COLOR]  $INFO[ListItem.Studio]</label><visible>!String.IsEmpty(ListItem.Studio)</visible></control>'
      '</control>')
    # the studio / network logo under the facts (user note, 2026-11-20), as on today's page
    o('<control type="image"><left>120</left><top>792</top><width>300</width><height>66</height><aspectratio align="left" aligny="center">keep</aspectratio>'
      '<texture background="true">resource://resource.images.studios.white/$INFO[Window(Home).Property(aeon.studio)].png</texture>'
      '<visible>!Skin.HasSetting(aeon.nostudio) + !String.IsEmpty(Window(Home).Property(aeon.studio)) + String.IsEqual(Window(Home).Property(aeon.studio.of),ListItem.Studio)</visible></control>')
    # title column
    o('<control type="image"><left>480</left><top>120</top><width>760</width><height>130</height><aspectratio align="left" aligny="center">keep</aspectratio>'
      '<fadetime>200</fadetime><texture background="true">$INFO[ListItem.Art(clearlogo)]</texture><visible>!String.IsEmpty(ListItem.Art(clearlogo))</visible></control>')
    o('<control type="label"><left>480</left><top>130</top><width>1340</width><height>120</height><aligny>bottom</aligny><wrapmultiline>true</wrapmultiline><font>st_display_52</font>'
      '<textcolor>ffffffff</textcolor><label>[UPPERCASE]$VAR[VidInfo_Title][/UPPERCASE]</label><visible>String.IsEmpty(ListItem.Art(clearlogo))</visible></control>')
    o('<control type="label"><left>480</left><top>258</top><width>1340</width><height>34</height><aligny>center</aligny><font>st_small_20_bold</font>'
      '<textcolor>fg_mark</textcolor><label>[UPPERCASE]$INFO[ListItem.Tagline][/UPPERCASE]</label></control>')
    o('<control type="grouplist"><left>480</left><top>298</top><width>1340</width><height>40</height><orientation>horizontal</orientation><itemgap>14</itemgap><usecontrolcoords>true</usecontrolcoords>'
      '<include content="Aeon_RatingIcons"><param name="place" value="info"/><param name="h" value="40"/><param name="font" value="st_ui_24_semibold"/><param name="ink" value="ffffffff"/></include>'
      '<control type="label"><width>auto</width><height>40</height><aligny>center</aligny><font>st_ui_24</font><textcolor>59ffffff</textcolor><label>·</label><visible>$EXP[VidView_HasRating] + $EXP[Aeon_Rate_info] + !String.IsEmpty(ListItem.Genre)</visible></control>'
      '<control type="label"><width max="700">auto</width><height>40</height><aligny>center</aligny><font>st_ui_24</font><textcolor>e6ffffff</textcolor><label>$INFO[ListItem.Genre]</label></control>'
      '<control type="label"><width>auto</width><height>40</height><aligny>center</aligny><font>st_ui_24</font><textcolor>59ffffff</textcolor><label>·</label><visible>!String.IsEmpty(ListItem.Genre) + !String.IsEmpty(ListItem.Duration)</visible></control>'
      '<control type="label"><width max="500">auto</width><height>40</height><aligny>center</aligny><font>st_ui_24</font><textcolor>e6ffffff</textcolor><label>$VAR[VidInfo_EndLine]</label></control>'
      '</control>')
    o(chips(s))
    # plot: OK = the full plot
    o('<control type="image"><left>464</left><top>400</top><width>892</width><height>136</height><texture border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texture>'
      '<visible>Control.HasFocus(9001)</visible></control>')
    o('<control type="textbox"><left>480</left><top>408</top><width>860</width><height>120</height><font>st_body_24</font><textcolor>e0ffffff</textcolor>'
      '<label>$VAR[VidInfo_Story]</label><autoscroll delay="8000" time="3000" repeat="10000">!Control.HasFocus(9001)</autoscroll></control>')
    o('<control type="button" id="9001"><left>464</left><top>400</top><width>892</width><height>136</height><label></label><texturefocus /><texturenofocus />'
      '<onup>9000</onup><ondown condition="Integer.IsGreater(Container(50).NumItems,0)">50</ondown><onleft>noop</onleft><onright>noop</onright>'
      '<onclick>SetFocus(61)</onclick><visible>!String.IsEmpty(ListItem.Plot)</visible></control>')
    # watched bar
    o('<control type="progress"><left>480</left><top>556</top><width>860</width><height>8</height><texturebg border="2,0,2,0" colordiffuse="2effffff">fg/pillh.png</texturebg>'
      '<midtexture subpixel="true" border="2,0,2,0" colordiffuse="fg_mark">fg/pillh.png</midtexture><info>ListItem.PercentPlayed</info><visible>ListItem.IsResumable</visible></control>')
    o('<control type="label"><left>480</left><top>572</top><width>400</width><height>30</height><aligny>center</aligny><font>st_small_20</font><textcolor>a6ffffff</textcolor>'
      '<label>$INFO[ListItem.PercentPlayed,,%]</label><visible>ListItem.IsResumable</visible></control>')
    o('<control type="label"><left>880</left><top>572</top><width>460</width><height>30</height><align>right</align><aligny>center</aligny><font>st_small_20</font><textcolor>a6ffffff</textcolor>'
      '<label>$VAR[VidInfo_EndLine]</label><visible>ListItem.IsResumable</visible></control>')
    # 0.3.117 helper: the intermission from Skippy's chapters sidecar (aeon.intm.*), a white tick on the bar
    intm = ('String.IsEqual(Window(Home).Property(aeon.intm.path),Window(Home).Property(aeon.vi.path)) + '
            '!String.IsEmpty(Window(Home).Property(aeon.intm.ranges))')
    o('<control type="image"><left>480</left><top>556</top><width>860</width><height>8</height><texture border="2,0,2,0" colordiffuse="2effffff">fg/pillh.png</texture>'
      '<visible>!ListItem.IsResumable + %s</visible></control>' % intm)
    o('<control type="ranges"><left>480</left><top>550</top><width>860</width><height>20</height><texturebg></texturebg><lefttexture /><righttexture />'
      '<midtexture colordiffuse="ffffffff">fg/fgs_offmark.png</midtexture><info>Window(Home).Property(aeon.intm.ranges)</info><visible>%s</visible></control>' % intm)
    o('<control type="label"><left>480</left><top>572</top><width>860</width><height>30</height><align>center</align><aligny>center</aligny><font>st_small_20</font>'
      '<textcolor>a6ffffff</textcolor><label>$ADDON[skin.aeon.fuse 32799] $INFO[Window(Home).Property(aeon.intm.time)]</label><visible>%s</visible></control>' % intm)
    # the action row, line to line, and the More row in its place
    o('<control type="image"><left>480</left><top>660</top><width>1340</width><height>1</height><texture colordiffuse="%s">common/white.png</texture></control>' % LINE)
    o('<control type="image"><left>480</left><top>730</top><width>1340</width><height>1</height><texture colordiffuse="%s">common/white.png</texture></control>' % LINE)
    o('<control type="image"><left>480</left><top>660</top><width>1</width><height>71</height><texture colordiffuse="%s">common/white.png</texture></control>' % LINE)
    row = [
        cell('9', 220, '$LOCALIZE[31618]', visible='$EXP[VidInfo_ShowResume]'),
        cell('8', 180, '$LOCALIZE[31278]', visible='$EXP[VidInfo_ShowPlay]'),
        cell('9013', 240, '$LOCALIZE[31619]', ('SendClick(8)',), '$EXP[VidInfo_ShowResume]'),
        cell('9012', 200, '$LOCALIZE[31620]', ('SendClick(8)',), '$EXP[VidView_IsFolderType]'),
        cell('9016', 200, '$LOCALIZE[31621]', ('RunScript(script.aeon.helper,trailer,play,$ESCINFO[Window(Home).Property(aeon.trailer)])',), '$EXP[VidInfo_ShowTrailer]'),
        cell('14', 230, '$LOCALIZE[31624]', visible='String.IsEqual(ListItem.DBType,movie)'),
        cell('15', 210, '$LOCALIZE[31625]', visible='String.IsEqual(ListItem.DBType,movie)'),
        cell('9010', 160, '$LOCALIZE[31206]', ('SetFocus(9100)',)),
    ]
    o('<control type="grouplist" id="9000"><left>481</left><top>661</top><width>1339</width><height>70</height><orientation>horizontal</orientation>'
      '<itemgap>0</itemgap><usecontrolcoords>true</usecontrolcoords><onup>noop</onup><onleft>noop</onleft><onright>noop</onright>'
      '<ondown condition="Control.IsVisible(9001)">9001</ondown><ondown condition="!Control.IsVisible(9001) + Integer.IsGreater(Container(50).NumItems,0)">50</ondown>'
      '<visible allowhiddenfocus="true">!ControlGroup(9100).HasFocus()</visible>%s</control>' % ''.join(row))
    more = [
        cell('443', 260, '$LOCALIZE[31622]', ('Dialog.Close(all,true)', '$VAR[VidInfo_CollectionAction]'), '!String.IsEmpty(ListItem.SetID)', False),
        cell('13', 260, '$LOCALIZE[31623]', visible='!String.IsEmpty(ListItem.Director)', down=False),
        cell('7', 230, '$LOCALIZE[38018]$INFO[ListItem.UserRating,: ,]', visible='Control.IsEnabled(7)', down=False),
        cell('10', 230, '$LOCALIZE[31626]', visible='Control.IsEnabled(10)', down=False),
        cell('12', 230, '$LOCALIZE[31627]', visible='Control.IsEnabled(12)', down=False),
        cell('6', 200, '$LOCALIZE[31533]', visible='Control.IsEnabled(6)', down=False),
    ]
    o('<control type="grouplist" id="9100"><left>481</left><top>661</top><width>1339</width><height>70</height><orientation>horizontal</orientation>'
      '<itemgap>0</itemgap><usecontrolcoords>true</usecontrolcoords><onup>9010</onup><ondown>9010</ondown><onleft>noop</onleft><onright>noop</onright><onback>9010</onback>'
      '<visible allowhiddenfocus="true">ControlGroup(9100).HasFocus()</visible>%s</control>' % ''.join(more))
    o('</control>')
    return ''.join(out)


def cast_item(focused):
    f = 'true' if focused else 'false'
    ring = ('<control type="image"><left>-6</left><top>-6</top><width>180</width><height>180</height><texture colordiffuse="ffffffff">aeon/ring_cast.png</texture>'
            '<visible>Control.HasFocus(50)</visible></control>') if focused else ''
    zoom = '<include>Anim_FocusZoom</include>' if focused else ''
    ink = 'ffffffff' if focused else 'd9ffffff'
    return (
        # people: round photos
        '<control type="group"><left>19</left><top>10</top><width>168</width><height>168</height><visible>!String.IsEqual(ListItem.DBType,movie)</visible>%s'
        '<control type="image"><left>0</left><top>0</top><width>168</width><height>168</height><texture colordiffuse="1fffffff">aeon/disc_cast.png</texture></control>'
        '<control type="image"><left>59</left><top>59</top><width>50</width><height>50</height><texture colordiffuse="59ffffff">aeon/icons/info.png</texture><visible>String.IsEmpty(ListItem.Art(thumb))</visible></control>'
        '<control type="image"><left>0</left><top>-17</top><width>168</width><height>252</height><aspectratio scalediffuse="false">scale</aspectratio><fadetime>160</fadetime>'
        '<texture background="true" diffuse="aeon/mask_cast.png">$INFO[ListItem.Art(thumb)]</texture></control>%s</control>'
        '<control type="label"><left>0</left><top>192</top><width>206</width><height>30</height><align>center</align><aligny>center</aligny><font>st_small_20_semibold</font>'
        '<textcolor>%s</textcolor><label>$INFO[ListItem.Label]</label><visible>!String.IsEqual(ListItem.DBType,movie)</visible></control>'
        '<control type="label"><left>0</left><top>222</top><width>206</width><height>28</height><align>center</align><aligny>center</aligny><font>st_small_20</font>'
        '<textcolor>8cffffff</textcolor><label>$VAR[VidInfo_CastLine2]</label><visible>!String.IsEqual(ListItem.DBType,movie)</visible></control>'
        # films of a collection: posters
        '<control type="group"><left>26</left><top>0</top><width>154</width><height>231</height><visible>String.IsEqual(ListItem.DBType,movie)</visible>%s'
        '<control type="image"><left>0</left><top>0</top><width>154</width><height>231</height><aspectratio scalediffuse="false">scale</aspectratio>'
        '<texture background="true" diffuse="fg/m154x231.png">$VAR[VidInfo_CastArt]</texture></control>'
        '<control type="image"><left>-3</left><top>-3</top><width>160</width><height>237</height><texture border="19" colordiffuse="ffffffff">fg/ring16.png</texture>'
        '<visible>%s + Control.HasFocus(50)</visible></control></control>'
        '<control type="label"><left>0</left><top>238</top><width>206</width><height>30</height><align>center</align><aligny>center</aligny><font>st_small_20_semibold</font>'
        '<textcolor>%s</textcolor><label>$INFO[ListItem.Label]</label><visible>String.IsEqual(ListItem.DBType,movie)</visible></control>'
        % (zoom, ring, ink, zoom, f, ink))


def online_item(lid, focused):
    f = 'true' if focused else 'false'
    return (
        '<control type="group"><left>14</left><top>10</top><width>220</width><height>330</height>%s'
        '<control type="image"><left>0</left><top>0</top><width>220</width><height>330</height><texture border="16" colordiffuse="14ffffff">fg/r16.png</texture></control>'
        '<control type="image"><left>0</left><top>0</top><width>220</width><height>330</height><aspectratio scalediffuse="false">scale</aspectratio>'
        '<texture background="true" diffuse="fg/m220x330.png">$INFO[ListItem.Art(poster)]</texture></control>'
        '<control type="image"><left>0</left><top>0</top><width>220</width><height>330</height><texture border="16" colordiffuse="b0000000">fg/r16.png</texture>'
        '<visible>!String.IsEmpty(ListItem.Property(aeon.missing)) + ![%s + Control.HasFocus(%s)]</visible></control>'
        '<control type="image"><left>178</left><top>10</top><width>32</width><height>32</height><texture colordiffuse="ffffffff">markers/check.png</texture>'
        '<visible>!String.IsEmpty(ListItem.Property(aeon.owned))</visible></control>'
        '<control type="image"><left>-3</left><top>-3</top><width>226</width><height>336</height><texture border="19" colordiffuse="ffffffff">fg/ring16.png</texture>'
        '<visible>%s + Control.HasFocus(%s)</visible></control></control>'
        '<control type="label"><left>14</left><top>352</top><width>220</width><height>30</height><aligny>center</aligny><font>st_small_20_semibold</font>'
        '<textcolor>e6ffffff</textcolor><label>$INFO[ListItem.Title]</label><visible>!String.IsEmpty(ListItem.Title)</visible></control>'
        '<control type="label"><left>14</left><top>352</top><width>220</width><height>30</height><aligny>center</aligny><font>st_small_20_semibold</font>'
        '<textcolor>e6ffffff</textcolor><label>$INFO[ListItem.Label]</label><visible>String.IsEmpty(ListItem.Title)</visible></control>'
        '<control type="label"><left>14</left><top>380</top><width>220</width><height>28</height><aligny>center</aligny><font>st_small_20</font>'
        '<textcolor>8cffffff</textcolor><label>$INFO[ListItem.Year]$INFO[ListItem.Property(year)]</label></control>'
        % ('<include>Anim_FocusZoom</include>' if focused else '', f, lid, f, lid))


def heading(top, label, count, vis):
    return ('<control type="group"><visible>%s</visible>'
            '<control type="label"><left>120</left><top>%d</top><width>1000</width><height>40</height><aligny>center</aligny><font>st_ui_28_bold</font>'
            '<textcolor>ffffffff</textcolor><label>[UPPERCASE]%s[/UPPERCASE]</label></control>'
            '<control type="label"><left>1120</left><top>%d</top><width>700</width><height>40</height><align>right</align><aligny>center</aligny><font>st_small_20</font>'
            '<textcolor>8cffffff</textcolor><label>%s</label></control></control>' % (vis, top, label, top, count))


def lower(s):
    out = []
    o = out.append
    shown_50 = '![Control.HasFocus(9301) | Control.HasFocus(9302) | Control.HasFocus(9303)]'
    fade = '<animation effect="fade" time="200">VisibleChange</animation>'
    # cast
    o('<control type="group"><visible>Integer.IsGreater(Container(50).NumItems,0) + %s</visible>%s' % (shown_50, fade))
    o(heading(870, '$VAR[VidInfo_CastHeader]', '$VAR[VidInfo_CastCount]', 'true'))
    o('</control>')
    o('<control type="list" id="50"><left>120</left><top>926</top><width>1700</width><height>290</height><orientation>horizontal</orientation><preloaditems>1</preloaditems>'
      '<scrolltime tween="cubic" easing="out">220</scrolltime>'
      '<onup condition="Control.IsVisible(9001)">9001</onup><onup condition="!Control.IsVisible(9001)">9000</onup>'
      '<ondown condition="Integer.IsGreater(Container(9301).NumItems,0)">9301</ondown>'
      '<ondown condition="!Integer.IsGreater(Container(9301).NumItems,0) + Integer.IsGreater(Container(9302).NumItems,0)">9302</ondown>'
      '<ondown condition="!Integer.IsGreater(Container(9301).NumItems,0) + !Integer.IsGreater(Container(9302).NumItems,0) + Integer.IsGreater(Container(9303).NumItems,0)">9303</ondown>'
      '<onleft>noop</onleft><onright>noop</onright><visible>%s</visible>%s'
      '<itemlayout width="206" height="290">%s</itemlayout><focusedlayout width="206" height="290">%s</focusedlayout></control>'
      % (shown_50, fade, cast_item(False), cast_item(True)))
    # crew + the file: only while the page is on screen 1 / 2
    o('<control type="group"><visible>%s</visible>%s' % (shown_50, fade))
    o('<control type="grouplist"><left>120</left><top>1248</top><width>1700</width><height>56</height><orientation>horizontal</orientation><itemgap>16</itemgap><usecontrolcoords>true</usecontrolcoords>')
    for key, info in (('20339', 'ListItem.Director'), ('20417', 'ListItem.Writer'), ('572', 'ListItem.Studio')):
        o('<control type="button"><width min="80" max="700">auto</width><height>56</height><font>st_small_20_semibold</font><textcolor>e6ffffff</textcolor>'
          '<focusedcolor>e6ffffff</focusedcolor><disabledcolor>e6ffffff</disabledcolor><textoffsetx>26</textoffsetx><aligny>center</aligny><enable>false</enable>'
          '<label>[COLOR 8cffffff]$LOCALIZE[%s][/COLOR]   $INFO[%s]</label>'
          '<texturenofocus border="28,0,28,0" colordiffuse="38ffffff">fg/btn56n.png</texturenofocus><texturefocus border="28,0,28,0" colordiffuse="38ffffff">fg/btn56n.png</texturefocus>'
          '<visible>!String.IsEmpty(%s)</visible></control>' % (key, info, info))
    o('</control>')
    o('<control type="image"><left>120</left><top>1344</top><width>1700</width><height>1</height><texture colordiffuse="%s">common/white.png</texture></control>' % LINE)
    o('<control type="image"><left>120</left><top>1414</top><width>1700</width><height>1</height><texture colordiffuse="%s">common/white.png</texture></control>' % LINE)
    cells = (('291', '$VAR[VidInfo_FlagRes]   $VAR[VidInfo_FlagVideo]   $VAR[VidInfo_FlagHDR]'),
             ('292', '$VAR[VidInfo_AudioCodec]$VAR[VidInfo_AudioChannels]$INFO[ListItem.AudioLanguage,   ,]'),
             ('287', '$INFO[ListItem.SubtitleLanguage]'),
             ('180', '$INFO[ListItem.Duration(hh:mm)]$INFO[ListItem.VideoAspect,   ,:1]'))
    for k, (key, val) in enumerate(cells):
        x = 120 + k * 425
        o('<control type="image"><left>%d</left><top>1344</top><width>1</width><height>71</height><texture colordiffuse="%s">common/white.png</texture></control>' % (x, LINE))
        o('<control type="label"><left>%d</left><top>1352</top><width>377</width><height>24</height><aligny>center</aligny><font>st_cap_14</font><textcolor>73ffffff</textcolor>'
          '<label>[UPPERCASE]$LOCALIZE[%s][/UPPERCASE]</label></control>' % (x + 24, key))
        o('<control type="label"><left>%d</left><top>1376</top><width>377</width><height>32</height><aligny>center</aligny><font>st_small_20</font><textcolor>e6ffffff</textcolor>'
          '<label>%s</label></control>' % (x + 24, val))
    o('<control type="image"><left>1819</left><top>1344</top><width>1</width><height>71</height><texture colordiffuse="%s">common/white.png</texture></control>' % LINE)
    o('</control>')
    # online rows
    rows = (('9301', 1524, '$LOCALIZE[31571]', 'recommendations', '50', '9302', '![Control.HasFocus(9302) | Control.HasFocus(9303)]'),
            ('9302', 2024, '$LOCALIZE[31572]', 'similar', '9301', '9303', '!Control.HasFocus(9303)'))
    for lid, top, label, info, up, down, vis in rows:
        o(heading(top, label, '$INFO[Container(%s).NumItems]' % lid, 'Integer.IsGreater(Container(%s).NumItems,0) + %s' % (lid, vis)))
        upnav = ('<onup>50</onup>' if lid == '9301' else
                 '<onup condition="Integer.IsGreater(Container(9301).NumItems,0)">9301</onup><onup condition="!Integer.IsGreater(Container(9301).NumItems,0)">50</onup>')
        o('<control type="list" id="%s"><left>106</left><top>%d</top><width>1728</width><height>420</height><orientation>horizontal</orientation>'
          '<scrolltime tween="cubic" easing="out">200</scrolltime>%s'
          '<ondown condition="Integer.IsGreater(Container(%s).NumItems,0)">%s</ondown>'
          '<ondown condition="!Integer.IsGreater(Container(%s).NumItems,0) + Integer.IsGreater(Container(9303).NumItems,0)">9303</ondown>'
          '<onleft>noop</onleft><onright>noop</onright><onclick condition="!String.IsEmpty(ListItem.Property(aeon.missing))">noop</onclick>'
          '<visible>%s</visible>%s'
          '<itemlayout width="248" height="420">%s</itemlayout><focusedlayout width="248" height="420">%s</focusedlayout>'
          '<content limit="20">plugin://script.aeon.helper/?info=online&amp;bare=1&amp;list=%s&amp;type=$VAR[VidInfo_TMDbType]&amp;year=$VAR[VidInfo_TMDbYear]&amp;query=$VAR[VidInfo_TMDbQuery]</content></control>'
          % (lid, top + 50, upnav, down, down, down, vis, fade, online_item(lid, False), online_item(lid, True), info))
    # reviews: today's list, moved
    a = s.index('<include name="VidInfo_ReviewRow">')
    i = s.index('<control type="list" id="9303">', a)
    m = ss.masked(s)
    e = ss.ctl_end(m, i)
    rev = s[i:e].replace('<left>22</left>\n\t\t\t\t<top>80</top>\n\t\t\t\t<width>1636</width>', '<left>102</left>\n\t\t\t\t<top>2574</top>\n\t\t\t\t<width>1736</width>', 1)
    assert '<top>2574</top>' in rev, 'review list geometry'
    o(heading(2524, '$LOCALIZE[31886]', '$INFO[Container(9303).NumItems]', 'Integer.IsGreater(Container(9303).NumItems,0)'))
    o(rev)
    return ''.join(out)


def page(s):
    slides = ''.join(
        '<animation type="Conditional" condition="Control.HasFocus(%s) + !Skin.HasSetting(aeon.reducemotion)" reversible="true"><effect type="slide" start="0,0" end="0,-%d" time="340" tween="sine" easing="inout"/></animation>'
        '<animation type="Conditional" condition="Control.HasFocus(%s) + Skin.HasSetting(aeon.reducemotion)" reversible="true"><effect type="slide" start="0,0" end="0,-%d" time="0"/></animation>'
        % (c, d, c, d) for c, d in SLIDES)
    return (
        '<include name="VidInfo_PageFGS">\n'
        # the fanart, the gradients, a darker veil below screen 1
        '<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture colordiffuse="ff08090c">common/white.png</texture></control>'
        '<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><aspectratio>scale</aspectratio><fadetime>300</fadetime>'
        '<texture background="true">$VAR[VidInfo_Fanart]</texture><visible>!Skin.HasSetting(aeon.nobackdrop)</visible></control>'
        '<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture>fg/fgs_vi_l.png</texture></control>'
        '<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture>fg/fgs_vi_b.png</texture></control>'
        '<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture colordiffuse="b008090c">common/white.png</texture>'
        '<visible>%s</visible><animation effect="fade" time="300">VisibleChange</animation></control>'
        '<include content="FGS_DlgHeader"><param name="lead" value="$VAR[VidInfo_TypeName]"/><param name="leadvis" value="true"/><param name="label" value="$LOCALIZE[31573]"/></include>'
        '<include>Aeon_ClockBox</include>'
        # the strip that stays while the page is down
        '<control type="group"><visible>%s</visible><animation effect="fade" time="250">VisibleChange</animation>'
        '<control type="image"><left>120</left><top>124</top><width>300</width><height>76</height><aspectratio align="left" aligny="center">keep</aspectratio>'
        '<texture background="true">$INFO[ListItem.Art(clearlogo)]</texture><visible>!String.IsEmpty(ListItem.Art(clearlogo))</visible></control>'
        '<control type="label"><left>120</left><top>124</top><width>300</width><height>76</height><aligny>center</aligny><font>st_ui_28_bold</font><textcolor>ffffffff</textcolor>'
        '<label>[UPPERCASE]$VAR[VidInfo_Title][/UPPERCASE]</label><visible>String.IsEmpty(ListItem.Art(clearlogo))</visible></control>'
        '<control type="label"><left>444</left><top>124</top><width>1376</width><height>76</height><aligny>center</aligny><font>st_small_20</font><textcolor>a6ffffff</textcolor>'
        '<label>$VAR[VidInfo_MetaLeft]$INFO[ListItem.Genre,  ·  ,]</label></control>'
        '<control type="image"><left>120</left><top>226</top><width>1700</width><height>1</height><texture colordiffuse="%s">common/white.png</texture></control>'
        '</control>'
        '<control type="group">%s%s%s</control>'
        '<include>VidInfo_FullPlot</include>\n'
        '</include>' % (SCR, SCR, LINE, slides, hero(s), lower(s)))


def main():
    textures()
    s = io.open(INC, encoding='utf-8').read()
    if A in s:
        a = s.index(A)
        b = s.index(B) + len(B)
        s = s[:a] + s[b:]
    # the classic page: today's window controls, as an include (moved once)
    w = io.open(WIN, encoding='utf-8').read()
    if 'VidInfo_PageClassic' not in w:
        a = w.index('<controls>') + len('<controls>')
        b = w.index('</controls>')
        classic = w[a:b]
        w = (w[:a] + '\n\t\t<include condition="!$EXP[FGS]">VidInfo_PageClassic</include>'
             '\n\t\t<include condition="$EXP[FGS]">VidInfo_PageFGS</include>\n\t' + w[b:])
        io.open(WIN, 'w', encoding='utf-8', newline='\n').write(w)
        s = s.replace('</includes>', '\t<!-- 0.56.53: today\'s page, moved from DialogVideoInfo.xml unchanged (every theme and style but Fused Glass style) -->\n'
                      '\t<include name="VidInfo_PageClassic">' + classic + '</include>\n</includes>')
    s = s.replace('</includes>', '\t%s\n\t%s\n\t%s\n</includes>' % (A, page(s), B))
    io.open(INC, 'w', encoding='utf-8', newline='\n').write(s)
    onload()
    print('fgs video info: page written')


def onload():
    """0.3.117 helper: the film's file and length for the intermission mark (Kodi's ListItem is the cast while 50 has
    focus, so the page keeps its own)"""
    w = io.open(WIN, encoding='utf-8').read()
    if 'aeon.vi.path' in w:
        return
    add = ('<onload>SetProperty(aeon.vi.path,$ESCINFO[ListItem.FileNameAndPath],home)</onload>\n\t'
           '<onload>SetProperty(aeon.vi.secs,$INFO[ListItem.Duration(secs)],home)</onload>\n\t'
           '<onunload>ClearProperty(aeon.vi.path,home)</onunload>\n\t<onunload>ClearProperty(aeon.vi.secs,home)</onunload>\n\t')
    w = w.replace('<include>Anim_DialogOpenClose</include>', add + '<include>Anim_DialogOpenClose</include>', 1)
    io.open(WIN, 'w', encoding='utf-8', newline='\n').write(w)


if __name__ == '__main__':
    main()
