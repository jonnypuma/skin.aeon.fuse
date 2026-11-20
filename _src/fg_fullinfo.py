"""0.41.0 Fused Glass information screen (DialogFullScreenInfo): writes include FG_FullInfo into
1080i/Includes_FusedPlayer.xml (between the FG_FULLINFO markers) and switches DialogFullScreenInfo.xml to load-time
variants (FG_FullInfo / FullInfo_Classic). Mockups: PlayerInfo, PlayerInfoCast, PlayerInfoMore.
Run from the skin folder: python _src/fg_fullinfo.py"""
import io
import re

INC = '1080i/Includes_FusedPlayer.xml'
DLG = '1080i/DialogFullScreenInfo.xml'
PAGE = 'Window(fullscreeninfo).Property(fgpage)'
PHOTOS = 'Skin.HasSetting(aeon.osd.castphotos)'
CAP = '<font>pl_cap_16</font><textcolor>99ffffff</textcolor>'
KEY = ('<control type="button"><width min="40" max="200">auto</width><height>26</height><label>[B]%s[/B]</label><font>pl_cap_12</font>'
       '<textoffsetx>9</textoffsetx><align>center</align><aligny>center</aligny><textcolor>ffffffff</textcolor><disabledcolor>ffffffff</disabledcolor>'
       '<texturenofocus border="8" colordiffuse="59ffffff">fg/e8.png</texturenofocus><texturefocus border="8" colordiffuse="59ffffff">fg/e8.png</texturefocus><enable>false</enable></control>'
       '<control type="label"><width max="400">auto</width><height>26</height><aligny>center</aligny><font>pl_small_20</font><textcolor>99ffffff</textcolor><label>%s</label></control>')


def card(top, height):
    return ('\t\t\t<control type="image"><left>56</left><top>%d</top><width>1808</width><height>%d</height><texture border="72" colordiffuse="99000000">fg/sh32.png</texture></control>\n'
            '\t\t\t<control type="image"><left>96</left><top>%d</top><width>1728</width><height>%d</height><texture border="32" colordiffuse="fg_frost">fg/r32.png</texture></control>\n'
            '\t\t\t<control type="image"><left>96</left><top>%d</top><width>1728</width><height>%d</height><texture border="32" colordiffuse="fg_edge">fg/e32.png</texture></control>\n'
            % (top - 28, height + 80, top, height, top, height))


def hints(top, *pairs):
    return ('\t\t\t<control type="grouplist"><left>136</left><top>%d</top><width>1400</width><height>26</height><orientation>horizontal</orientation><itemgap>10</itemgap>%s</control>\n'
            % (top, ''.join(KEY % p for p in pairs)))


def overview(top, h, poster_w, poster_h, mask, col, plot_lines, photos):
    """The overview page: poster with progress, kicker / title / meta / ratings / plot, media + up next on the right,
    then the cast (chips in the middle column, or photos across the card)."""
    x = 136 + poster_w + 40          # text column
    tw = 1380 - x                    # up to the right column
    o = []
    o.append(card(top, h))
    o.append('\t\t\t<control type="image"><left>136</left><top>%d</top><width>%d</width><height>%d</height><aspectratio scalediffuse="false">scale</aspectratio>'
             '<texture background="true" diffuse="fg/%s">$VAR[Aeon_OSD_Poster]</texture><visible>!$EXP[FG_OSDLive]</visible></control>\n' % (top + 36, poster_w, poster_h, mask))
    py = top + 36 + poster_h + 18
    o.append('\t\t\t<control type="image"><left>136</left><top>%d</top><width>%d</width><height>6</height><texture border="3" colordiffuse="38ffffff">fg/pill4.png</texture></control>\n' % (py, poster_w))
    o.append('\t\t\t<control type="progress"><left>136</left><top>%d</top><width>%d</width><height>6</height><texturebg border="3" colordiffuse="00ffffff">fg/pill4.png</texturebg>'
             '<midtexture border="3" colordiffuse="ffffffff">fg/pill4.png</midtexture><info>Player.Progress</info></control>\n' % (py, poster_w))
    # chapters as gaps, as on the seek bar (0.45.1); Kodi draws the range ends half their height lower: -3
    o.append('\t\t\t<control type="ranges"><left>136</left><top>%d</top><width>%d</width><height>6</height><texturebg></texturebg><lefttexture /><midtexture />'
             '<righttexture colordiffuse="fg_gapcol">fg/chgap6.png</righttexture><info>Player.Chapters</info><visible>$EXP[OSD_HasChapters]</visible></control>\n' % (py - 3, poster_w))
    o.append('\t\t\t<control type="label"><left>136</left><top>%d</top><width>%d</width><height>28</height><aligny>center</aligny><font>pl_small_20</font><textcolor>b3ffffff</textcolor>'
             '<label>$INFO[Player.Time]$INFO[Player.Duration, / ,]</label></control>\n' % (py + 12, poster_w))
    o.append('\t\t\t<control type="label"><left>136</left><top>%d</top><width>%d</width><height>28</height><aligny>center</aligny><font>pl_small_20</font><textcolor>99ffffff</textcolor>'
             '<label>$INFO[Player.TimeRemaining,−,]</label></control>\n' % (py + 40, poster_w))
    y = top + 36
    o.append('\t\t\t<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>24</height><aligny>center</aligny>%s<label>$VAR[FG_OSDKick]</label></control>\n' % (x, y, tw, CAP))
    o.append('\t\t\t<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>66</height><aligny>center</aligny><font>pl_display_52</font><textcolor>ffffffff</textcolor><scroll>true</scroll>'
             '<label>$VAR[FG_OSDCardTitle]</label></control>\n' % (x, y + 24, tw))
    o.append('\t\t\t<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>34</height><aligny>center</aligny><font>pl_ui_22</font><textcolor>d0ffffff</textcolor><scroll>true</scroll>'
             '<label>$VAR[FG_InfoMeta]</label></control>\n' % (x, y + 96, tw))
    o.append('\t\t\t<control type="grouplist"><left>%d</left><top>%d</top><width>%d</width><height>34</height><orientation>horizontal</orientation><itemgap>12</itemgap>'
             '<include content="Aeon_InfoRating"><param name="src" value="imdb"/><param name="icon" value="imdb"/></include>'
             '<include content="Aeon_InfoRating"><param name="src" value="tmdb"/><param name="icon" value="tmdb"/></include>'
             '<include content="Aeon_InfoRating"><param name="src" value="rt"/><param name="icon" value="rtfresh"/></include>'
             '<include content="Aeon_InfoRating"><param name="src" value="trakt"/><param name="icon" value="trakt"/></include>'
             '<control type="label"><width>auto</width><height>34</height><aligny>center</aligny><font>pl_ui_24_bold</font><textcolor>ffffffff</textcolor><label>$INFO[VideoPlayer.Rating]</label>'
             '<visible>String.IsEmpty(Window(Home).Property(aeon.r.player.imdb)) + String.IsEmpty(Window(Home).Property(aeon.r.player.tmdb)) + String.IsEmpty(Window(Home).Property(aeon.r.player.rt)) + String.IsEmpty(Window(Home).Property(aeon.r.player.trakt))</visible></control>'
             '</control>\n' % (x, y + 138, tw))
    o.append('\t\t\t<control type="textbox"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><font>pl_body_24</font><textcolor>ebffffff</textcolor>'
             '<label>$INFO[VideoPlayer.Plot]</label><autoscroll delay="8000" time="3000" repeat="10000">!Skin.HasSetting(aeon.noautoscroll)</autoscroll></control>\n' % (x, y + 188, tw, plot_lines * 36))
    # right column: media chips, facts, up next
    rx, rw = 1420, 364
    o.append('\t\t\t<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>24</height><aligny>center</aligny>%s<label>[UPPERCASE]$LOCALIZE[31449][/UPPERCASE]</label></control>\n' % (rx, y, rw, CAP))
    o.append('\t\t\t<control type="grouplist"><left>%d</left><top>%d</top><width>%d</width><height>34</height><orientation>horizontal</orientation><itemgap>8</itemgap>'
             '<include content="Aeon_InfoChip"><param name="label" value="$VAR[OSD_FlagResolution]"/><param name="visible" value="!String.IsEmpty(VideoPlayer.VideoResolution)"/></include>'
             '<include content="Aeon_InfoChip"><param name="label" value="$VAR[FG_ChipHDR]"/><param name="visible" value="!String.IsEmpty(VideoPlayer.HdrType)"/></include>'
             '<include content="Aeon_InfoChip"><param name="label" value="$VAR[OSD_FlagVideoCodec]"/><param name="visible" value="!String.IsEmpty(VideoPlayer.VideoCodec)"/></include>'
             '</control>\n' % (rx, y + 32, rw))
    o.append('\t\t\t<control type="grouplist"><left>%d</left><top>%d</top><width>%d</width><height>34</height><orientation>horizontal</orientation><itemgap>8</itemgap>'
             '<include content="Aeon_InfoChip"><param name="label" value="$VAR[OSD_FlagAudio]"/><param name="visible" value="!String.IsEmpty(VideoPlayer.AudioCodec)"/></include>'
             '<include content="Aeon_InfoChip"><param name="label" value="$INFO[VideoPlayer.VideoAspect,,:1]"/><param name="visible" value="!String.IsEmpty(VideoPlayer.VideoAspect)"/></include>'
             '</control>\n' % (rx, y + 74, rw))
    o.append('\t\t\t<control type="label"><left>%d</left><top>%d</top><width>150</width><height>30</height><aligny>center</aligny><font>pl_small_20</font><textcolor>8cffffff</textcolor><label>$LOCALIZE[292]</label></control>\n' % (rx, y + 126))
    o.append('\t\t\t<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>30</height><align>right</align><aligny>center</aligny><font>pl_small_20</font><textcolor>d0ffffff</textcolor><label>$INFO[Window(Home).Property(aeon.pf.audio)]</label></control>\n' % (rx + 150, y + 126, rw - 150))
    uy = y + (210 if photos else 236)
    th = 160 if photos else 205
    o.append('\t\t\t<control type="group"><visible>$EXP[FG_OSDUpNext]</visible>'
             '<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>24</height><aligny>center</aligny>%s<label>[UPPERCASE]$LOCALIZE[31235][/UPPERCASE]</label></control>'
             '<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><aspectratio scalediffuse="false">scale</aspectratio><texture background="true" diffuse="fg/m400x225.png">$INFO[Window(Home).Property(Skippy.NextEpisode.Thumb)]</texture></control>'
             '<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>32</height><aligny>center</aligny><font>pl_ui_22_bold</font><textcolor>ffffffff</textcolor><label>$INFO[Window(Home).Property(Skippy.NextEpisode.Label)]</label><visible>!String.IsEmpty(Window(Home).Property(Skippy.NextEpisode.Thumb))</visible></control>'
             '<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>32</height><aligny>center</aligny><font>pl_ui_22_bold</font><textcolor>ffffffff</textcolor><label>$INFO[Window(Home).Property(Skippy.NextEpisode.Label)]</label><visible>String.IsEmpty(Window(Home).Property(Skippy.NextEpisode.Thumb))</visible></control>'
             '</control>\n' % (rx, uy, rw, CAP, rx, uy + 32, int(th * 16 / 9) if photos else rw, th, rx, uy + 40 + th, rw, rx, uy + 30, rw))
    # cast
    if photos:
        cy = top + h - 330
        o.append('\t\t\t<control type="label"><left>136</left><top>%d</top><width>800</width><height>36</height><aligny>center</aligny><font>pl_ui_26_semibold</font><textcolor>ffffffff</textcolor><label>$LOCALIZE[206]</label></control>\n' % cy)
        o.append('\t\t\t<control type="label"><left>984</left><top>%d</top><width>800</width><height>36</height><align>right</align><aligny>center</aligny><font>pl_small_20_semibold</font><textcolor>9effffff</textcolor>'
                 '<label>$INFO[Container(9504).CurrentItem]$INFO[Container(9504).NumItems, / ,]</label><visible>Integer.IsGreater(Container(9504).NumItems,0)</visible></control>\n' % cy)
        o.append('''			<control type="list" id="9504">
				<left>118</left><top>%d</top><width>1666</width><height>240</height>
				<orientation>horizontal</orientation><preloaditems>1</preloaditems>
				<scrolltime tween="cubic" easing="out">220</scrolltime>
				<onup>999</onup>
				<ondown>SetProperty(fgpage,2,fullscreeninfo)</ondown>
				<ondown condition="!String.IsEmpty(Window(Home).Property(aeon.pf.seasonpath))">SetFocus(9502)</ondown>
				<ondown condition="!!String.IsEmpty(Window(Home).Property(aeon.pf.seasonpath))">SetFocus(9503)</ondown>
				<onleft>noop</onleft><onright>noop</onright>
				<onclick>noop</onclick>
				<content>$VAR[FG_InfoCastPath]</content>
				<itemlayout width="182" height="240"><include>FG_CastItem</include></itemlayout>
				<focusedlayout width="182" height="240"><include content="FG_CastItem"><param name="focused" value="true"/></include></focusedlayout>
			</control>
''' % (cy + 42))
        o.append(hints(top + h - 46, ('$LOCALIZE[31234]', '$ADDON[skin.aeon.fuse 32479]'), ('[UPPERCASE]$LOCALIZE[31347][/UPPERCASE]', '')) if False else
                 hints(top + h - 46, ('[UPPERCASE]$LOCALIZE[31245][/UPPERCASE]', '$LOCALIZE[15067]'), ('[UPPERCASE]$ADDON[skin.aeon.fuse 32488][/UPPERCASE]', '$ADDON[skin.aeon.fuse 32480]')))
    else:
        cy = y + 188 + plot_lines * 36 + 18
        o.append('\t\t\t<control type="label"><left>%d</left><top>%d</top><width>400</width><height>24</height><aligny>center</aligny>%s<label>[UPPERCASE]$LOCALIZE[206][/UPPERCASE]</label><visible>Integer.IsGreater(Container(9501).NumItems,0)</visible></control>\n' % (x, cy, CAP))
        o.append('''			<control type="panel" id="9501">
				<left>%d</left><top>%d</top><width>%d</width><height>104</height>
				<orientation>vertical</orientation><preloaditems>0</preloaditems>
				<content>$VAR[FG_InfoCastPath]</content>
				<itemlayout width="%d" height="52"><include>FG_CastChip</include></itemlayout>
				<focusedlayout width="%d" height="52"><include>FG_CastChip</include></focusedlayout>
			</control>
''' % (x, cy + 30, tw, tw // 3, tw // 3))
        o.append(hints(top + h - 46, ('[UPPERCASE]$LOCALIZE[31245][/UPPERCASE]', '$LOCALIZE[15067]'), ('[UPPERCASE]$ADDON[skin.aeon.fuse 32488][/UPPERCASE]', '$ADDON[skin.aeon.fuse 32480]')))
    return ''.join(o)


def page2():
    top, h = 140, 902
    o = [card(top, h)]
    o.append('\t\t\t<control type="label"><left>136</left><top>176</top><width>1100</width><height>24</height><aligny>center</aligny>%s<label>$VAR[FG_OSDKick]</label></control>\n' % CAP)
    o.append('\t\t\t<control type="label"><left>136</left><top>200</top><width>1100</width><height>52</height><aligny>center</aligny><font>pl_display_40</font><textcolor>ffffffff</textcolor><scroll>true</scroll><label>$VAR[FG_OSDCardTitle]</label></control>\n')
    # page tabs: Overview (dim) | File and season (pill)
    o.append('\t\t\t<control type="grouplist"><left>984</left><top>190</top><width>800</width><height>44</height><orientation>horizontal</orientation><align>right</align><itemgap>8</itemgap>'
             '<control type="button"><width min="80" max="400">auto</width><height>44</height><label>$ADDON[skin.aeon.fuse 32479]</label><font>pl_ui_22</font><textoffsetx>20</textoffsetx><aligny>center</aligny><textcolor>9effffff</textcolor><disabledcolor>9effffff</disabledcolor><texturenofocus /><texturefocus /><enable>false</enable></control>'
             '<control type="button"><width min="80" max="400">auto</width><height>44</height><label>[B]$ADDON[skin.aeon.fuse 32480][/B]</label><font>pl_ui_22</font><textoffsetx>20</textoffsetx><aligny>center</aligny><textcolor>ffffffff</textcolor><disabledcolor>ffffffff</disabledcolor>'
             '<texturenofocus border="22" colordiffuse="29ffffff">fg/r22.png</texturenofocus><texturefocus border="22" colordiffuse="29ffffff">fg/r22.png</texturefocus><enable>false</enable></control>'
             '</control>\n')
    # left: in this file
    o.append('\t\t\t<control type="label"><left>136</left><top>292</top><width>900</width><height>24</height><aligny>center</aligny>%s<label>[UPPERCASE]$ADDON[skin.aeon.fuse 32481][/UPPERCASE]</label></control>\n' % CAP)
    rows = [
        ('$LOCALIZE[291]', '$VAR[OSD_FlagVideoCodec]$VAR[OSD_FlagResolution,  ·  ,]$INFO[VideoPlayer.VideoAspect,  ·  ,:1]$VAR[FG_ChipHDR,  ·  ,]', 1),
        ('$LOCALIZE[292]', '$VAR[OSD_FlagAudio]$INFO[Window(Home).Property(aeon.pf.audio),  ·  ,]', 1),
        ('$LOCALIZE[287]', '$INFO[Window(Home).Property(aeon.pf.subcount),,:  ]$INFO[Window(Home).Property(aeon.pf.subs)]', 4),
        ('$ADDON[skin.aeon.fuse 32482]', '$INFO[Window(Home).Property(aeon.pf.file)]', 2),
        ('$ADDON[skin.aeon.fuse 32483]', '$INFO[Window(Home).Property(aeon.pf.size)]', 1),
        ('$ADDON[skin.aeon.fuse 32484]', '$INFO[System.ScreenResolution]', 1),
    ]
    y = 330
    for label, value, lines in rows:
        o.append('\t\t\t<control type="label"><left>136</left><top>%d</top><width>150</width><height>32</height><font>pl_ui_22</font><textcolor>8cffffff</textcolor><label>%s</label></control>\n' % (y, label))
        o.append('\t\t\t<control type="textbox"><left>300</left><top>%d</top><width>836</width><height>%d</height><font>pl_ui_22</font><textcolor>ebffffff</textcolor><label>%s</label></control>\n' % (y, lines * 32, value))
        y += lines * 32 + 16
    # right: the season (episodes only)
    o.append('''			<control type="group">
				<visible>!String.IsEmpty(Window(Home).Property(aeon.pf.seasonpath))</visible>
				<control type="label"><left>1184</left><top>292</top><width>600</width><height>24</height><aligny>center</aligny>%s<label>[UPPERCASE]$LOCALIZE[20373] $INFO[VideoPlayer.Season][/UPPERCASE]</label></control>
				<control type="list" id="9502">
					<left>1176</left><top>326</top><width>616</width><height>640</height>
					<orientation>vertical</orientation><preloaditems>1</preloaditems>
					<scrolltime tween="cubic" easing="out">200</scrolltime>
					<onup>ClearProperty(fgpage,fullscreeninfo)</onup><onup condition="Skin.HasSetting(aeon.osd.castphotos) + Integer.IsGreater(Container(9504).NumItems,0)">SetFocus(9504)</onup><onup condition="![Skin.HasSetting(aeon.osd.castphotos) + Integer.IsGreater(Container(9504).NumItems,0)]">SetFocus(999)</onup>
					<onleft>noop</onleft><onright>noop</onright>
					<onclick>noop</onclick>
					<content target="videos">$VAR[FG_InfoSeasonPath]</content>
					<itemlayout width="616" height="96"><include>FG_SeasonRow</include></itemlayout>
					<focusedlayout width="616" height="96"><include content="FG_SeasonRow"><param name="focused" value="true"/></include></focusedlayout>
				</control>
			</control>
''' % CAP)
    o.append(hints(top + h - 46, ('[UPPERCASE]$ADDON[skin.aeon.fuse 32487][/UPPERCASE]', '$ADDON[skin.aeon.fuse 32479]'), ('[UPPERCASE]$LOCALIZE[31245][/UPPERCASE]', '$LOCALIZE[15067]')))
    return ''.join(o)


def live_card():
    """0.46.1 Live TV: a compact card at the bottom instead of the film / episode overview (which had an empty poster
    slot): the channel's logo tile with its number, channel and genre, the programme with LIVE, two lines of plot, Next
    on the right; under it a bar the width of the card, with the start, the time left and the scheduled end."""
    top, h = 676, 366
    o = [card(top, h)]
    o.append('\t\t\t<control type="image"><left>136</left><top>%d</top><width>176</width><height>200</height><texture border="18" colordiffuse="14ffffff">fg/r18.png</texture></control>\n'
             '\t\t\t<control type="image"><left>136</left><top>%d</top><width>176</width><height>200</height><texture border="18" colordiffuse="24ffffff">fg/e18.png</texture></control>\n'
             '\t\t\t<control type="image"><left>152</left><top>%d</top><width>144</width><height>110</height><aspectratio>keep</aspectratio><texture background="true">$INFO[VideoPlayer.Cover]</texture></control>\n'
             '\t\t\t<control type="label"><left>136</left><top>%d</top><width>176</width><height>44</height><align>center</align><aligny>center</aligny><font>pl_display_40</font><textcolor>ffffffff</textcolor>'
             '<label>$INFO[VideoPlayer.ChannelNumberLabel]</label></control>\n' % (top + 36, top + 36, top + 52, top + 176))
    x, tw = 352, 1000
    o.append('\t\t\t<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>26</height><aligny>center</aligny>%s'
             '<label>[UPPERCASE]$INFO[VideoPlayer.ChannelName]$INFO[VideoPlayer.Genre,  ·  ,][/UPPERCASE]</label></control>\n' % (x, top + 36, tw, CAP))
    o.append('\t\t\t<control type="grouplist"><left>%d</left><top>%d</top><width>%d</width><height>64</height><orientation>horizontal</orientation><itemgap>16</itemgap><usecontrolcoords>true</usecontrolcoords>'
             '<control type="label"><width max="%d">auto</width><height>64</height><aligny>center</aligny><font>pl_display_48</font><textcolor>ffffffff</textcolor><label>$INFO[VideoPlayer.Title]</label></control>'
             '<control type="group"><top>17</top><width>78</width><height>30</height>'
             '<control type="image"><width>78</width><height>30</height><texture border="15" colordiffuse="ffe5484d">fg/r16.png</texture></control>'
             '<control type="label"><width>78</width><height>30</height><align>center</align><aligny>center</aligny><font>pl_cap_14</font><textcolor>ffffffff</textcolor><label>● $ADDON[skin.aeon.fuse 32477]</label></control></control>'
             '</control>\n' % (x, top + 64, tw, tw - 110))
    o.append('\t\t\t<control type="textbox"><left>%d</left><top>%d</top><width>%d</width><height>66</height><font>pl_body_24</font><textcolor>c8ffffff</textcolor>'
             '<label>$INFO[VideoPlayer.Plot]</label><autoscroll delay="6000" time="3000" repeat="10000">true</autoscroll></control>\n' % (x, top + 134, tw))
    # next, on the right
    o.append('\t\t\t<control type="group"><left>1420</left><top>%d</top><visible>!String.IsEmpty(VideoPlayer.NextTitle)</visible>'
             '<control type="label"><width>364</width><height>26</height><align>right</align><aligny>center</aligny>%s<label>[UPPERCASE]$LOCALIZE[19031]$INFO[VideoPlayer.NextStartTime,  ·  ,][/UPPERCASE]</label></control>'
             '<control type="label"><top>30</top><width>364</width><height>34</height><align>right</align><aligny>center</aligny><font>pl_ui_22_bold</font><textcolor>ffffffff</textcolor><label>$INFO[VideoPlayer.NextTitle]</label></control>'
             '</control>\n' % (top + 36, CAP))
    # the bar across the card: start | time left | ends
    by = top + 244
    o.append('\t\t\t<control type="image"><left>136</left><top>%d</top><width>1648</width><height>12</height><texture border="6" colordiffuse="3dffffff">fg/pill12.png</texture></control>\n'
             '\t\t\t<control type="progress"><left>136</left><top>%d</top><width>1648</width><height>12</height><texturebg border="6" colordiffuse="00ffffff">fg/pill12.png</texturebg>'
             '<midtexture border="6" colordiffuse="ffffffff">fg/pill12.png</midtexture><info>PVR.EpgEventProgress</info></control>\n' % (by, by))
    o.append('\t\t\t<control type="label"><left>136</left><top>%d</top><width>400</width><height>30</height><aligny>center</aligny><font>pl_ui_22_bold</font><textcolor>ffffffff</textcolor><label>$INFO[VideoPlayer.StartTime]</label></control>\n'
             '\t\t\t<control type="label"><left>560</left><top>%d</top><width>800</width><height>30</height><align>center</align><aligny>center</aligny><font>pl_small_20</font><textcolor>c8ffffff</textcolor>'
             '<label>$INFO[PVR.EpgEventRemainingTime,, $LOCALIZE[31965]]</label></control>\n'
             '\t\t\t<control type="label"><left>1384</left><top>%d</top><width>400</width><height>30</height><align>right</align><aligny>center</aligny><font>pl_ui_22_bold</font><textcolor>ffffffff</textcolor>'
             '<label>$LOCALIZE[31030] $INFO[VideoPlayer.EndTime]</label></control>\n' % (by + 22, by + 22, by + 22))
    o.append(hints(top + h - 46, ('[UPPERCASE]$LOCALIZE[31245][/UPPERCASE]', '$LOCALIZE[15067]')))
    return ''.join(o)


BODY = '''	<!-- FG_FULLINFO:begin (written by _src/fg_fullinfo.py) ============================== information screen (0.41.0) -->
	<variable name="FG_InfoCastPath">
		<value condition="Player.HasVideo + !$EXP[FG_OSDLive]">plugin://script.aeon.helper/?info=playercast&amp;s=$INFO[VideoPlayer.Season]&amp;e=$INFO[VideoPlayer.Episode]&amp;y=$INFO[VideoPlayer.Year]</value>
		<value>special://skin/shortcuts/customrows-none.xsp</value>
	</variable>
	<variable name="FG_InfoSeasonPath">
		<value condition="!String.IsEmpty(Window(Home).Property(aeon.pf.seasonpath))">$INFO[Window(Home).Property(aeon.pf.seasonpath)]</value>
		<value>special://skin/shortcuts/customrows-none.xsp</value>
	</variable>
	<variable name="FG_InfoFileW">
		<value condition="!String.IsEmpty(Window(Home).Property(aeon.pf.seasonpath))">836</value>
		<value>1484</value>
	</variable>
	<!-- Down from the overview: the cast row (photos), else the second page -->
	<variable name="FG_InfoToPage2">
		<value condition="!String.IsEmpty(Window(Home).Property(aeon.pf.seasonpath))">SetFocus(9502)</value>
		<value>SetFocus(9503)</value>
	</variable>
	<variable name="FG_InfoBackTo">
		<value condition="Skin.HasSetting(aeon.osd.castphotos) + Integer.IsGreater(Container(9504).NumItems,0)">SetFocus(9504)</value>
		<value>SetFocus(999)</value>
	</variable>
	<variable name="FG_InfoMeta">
		<value condition="!String.IsEmpty(VideoPlayer.TVShowTitle)">$INFO[VideoPlayer.Premiered]$INFO[Player.Duration(mins),  ·  , min]$INFO[VideoPlayer.mpaa,  ·  ]$INFO[VideoPlayer.Genre,  ·  ]$INFO[VideoPlayer.Studio,  ·  ]</value>
		<value>$VAR[AGOSD_Sub]</value>
	</variable>
	<variable name="FG_ChipHDR">
		<value condition="String.IsEqual(VideoPlayer.HdrType,dolbyvision)">DV</value>
		<value>$VAR[OSD_FlagHDR]</value>
	</variable>
	<!-- a cast member as a chip: name and character (the overview's default) -->
	<include name="FG_CastChip">
		<control type="image"><left>0</left><top>4</top><width>$PARAM[w]</width><height>44</height><texture border="22" colordiffuse="1cffffff">fg/r22.png</texture></control>
		<control type="label"><left>18</left><top>4</top><width>270</width><height>44</height><aligny>center</aligny><font>pl_small_20</font><textcolor>ffffffff</textcolor>
			<label>[B]$INFO[ListItem.Label][/B]$INFO[ListItem.Label2,  [COLOR 9effffff],[/COLOR]]</label></control>
	</include>
	<!-- a cast member as a photo (as on the item information view, VidInfo_CastItem) -->
	<include name="FG_CastItem">
		<param name="focused">false</param>
		<definition>
			<control type="group">
				<left>18</left><top>14</top><width>146</width><height>146</height>
				<animation type="Conditional" condition="$PARAM[focused] + Control.HasFocus(9504) + !Skin.HasSetting(aeon.reducemotion)" reversible="true"><effect type="zoom" start="100" end="108" center="auto" time="160" tween="cubic" easing="out"/></animation>
				<control type="image"><left>-6</left><top>-6</top><width>158</width><height>158</height><texture colordiffuse="$VAR[Aeon_Accent]">aeon/ring_cast.png</texture><visible>$PARAM[focused] + Control.HasFocus(9504)</visible></control>
				<control type="image"><width>146</width><height>146</height><texture colordiffuse="1fffffff">fg/circle.png</texture></control>
				<control type="image"><left>48</left><top>48</top><width>50</width><height>50</height><texture colordiffuse="66ffffff">aeon/icons/info.png</texture><visible>String.IsEmpty(ListItem.Art(thumb))</visible></control>
				<control type="image"><left>0</left><top>-15</top><width>146</width><height>219</height><aspectratio scalediffuse="false">scale</aspectratio><fadetime>160</fadetime><texture background="true" diffuse="aeon/mask_cast.png">$INFO[ListItem.Art(thumb)]</texture></control>
			</control>
			<control type="label"><left>8</left><top>177</top><width>166</width><height>28</height><align>center</align><font>pl_small_20_semibold</font><textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><label>$INFO[ListItem.Label]</label></control>
			<control type="label"><left>8</left><top>205</top><width>166</width><height>26</height><align>center</align><font>pl_small_20</font><textcolor>9effffff</textcolor><label>$INFO[ListItem.Label2]</label></control>
		</definition>
	</include>
	<!-- an episode of the season on the second page; the one playing has a light pill, the focused row is white -->
	<include name="FG_SeasonRow">
		<param name="focused">false</param>
		<definition>
			<control type="image"><left>0</left><top>4</top><width>616</width><height>88</height><texture border="16" colordiffuse="1affffff">fg/r16.png</texture><visible>ListItem.IsPlaying + !$PARAM[focused]</visible></control>
			<control type="image"><left>0</left><top>4</top><width>616</width><height>88</height><texture border="16" colordiffuse="ffffffff">fg/r16.png</texture><visible>$PARAM[focused] + Control.HasFocus(9502)</visible></control>
			<control type="image"><left>8</left><top>12</top><width>128</width><height>72</height><aspectratio scalediffuse="false">scale</aspectratio><texture background="true" diffuse="fg/m128x72.png">$INFO[ListItem.Art(thumb)]</texture></control>
			<control type="label"><left>152</left><top>14</top><width>450</width><height>32</height><aligny>center</aligny><font>pl_ui_22_bold</font><textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><label>$INFO[ListItem.Episode,E, · ]$INFO[ListItem.Title]</label><visible>!$PARAM[focused] | !Control.HasFocus(9502)</visible></control>
			<control type="label"><left>152</left><top>14</top><width>450</width><height>32</height><aligny>center</aligny><font>pl_ui_22_bold</font><textcolor>aeon_onbar</textcolor><selectedcolor>aeon_onbar</selectedcolor><label>$INFO[ListItem.Episode,E, · ]$INFO[ListItem.Title]</label><visible>$PARAM[focused] + Control.HasFocus(9502)</visible></control>
			<control type="label"><left>152</left><top>48</top><width>450</width><height>28</height><aligny>center</aligny><font>pl_small_20</font><textcolor>9effffff</textcolor><selectedcolor>9effffff</selectedcolor><label>$INFO[ListItem.Duration(mins),, min]</label><visible>!$PARAM[focused] | !Control.HasFocus(9502)</visible></control>
			<control type="label"><left>152</left><top>48</top><width>450</width><height>28</height><aligny>center</aligny><font>pl_small_20</font><textcolor>aeon_onbar</textcolor><selectedcolor>aeon_onbar</selectedcolor><label>$INFO[ListItem.Duration(mins),, min]</label><visible>$PARAM[focused] + Control.HasFocus(9502)</visible></control>
		</definition>
	</include>
	<include name="FG_FullInfo">
		<control type="button" id="999">
			<left>0</left><top>0</top><width>screen_w</width><height>screen_h</height>
			<label></label><texturefocus /><texturenofocus />
			<onright>StepForward</onright>
			<onleft>StepBack</onleft>
			<onup>ChapterOrBigStepForward</onup>
			<ondown condition="Skin.HasSetting(aeon.osd.castphotos) + Integer.IsGreater(Container(9504).NumItems,0)">SetFocus(9504)</ondown>
			<ondown condition="![Skin.HasSetting(aeon.osd.castphotos) + Integer.IsGreater(Container(9504).NumItems,0)]">SetProperty(fgpage,2,fullscreeninfo)</ondown>
			<ondown condition="![Skin.HasSetting(aeon.osd.castphotos) + Integer.IsGreater(Container(9504).NumItems,0)] + !String.IsEmpty(Window(Home).Property(aeon.pf.seasonpath))">SetFocus(9502)</ondown>
			<ondown condition="![Skin.HasSetting(aeon.osd.castphotos) + Integer.IsGreater(Container(9504).NumItems,0)] + !!String.IsEmpty(Window(Home).Property(aeon.pf.seasonpath))">SetFocus(9503)</ondown>
			<onclick>OSD</onclick>
		</control>
		<!-- the second page's focus when there is no season list (films) -->
		<control type="button" id="9503">
			<left>-200</left><top>-200</top><width>10</width><height>10</height><label></label><texturefocus /><texturenofocus />
			<onup>ClearProperty(fgpage,fullscreeninfo)</onup><onup condition="Skin.HasSetting(aeon.osd.castphotos) + Integer.IsGreater(Container(9504).NumItems,0)">SetFocus(9504)</onup><onup condition="![Skin.HasSetting(aeon.osd.castphotos) + Integer.IsGreater(Container(9504).NumItems,0)]">SetFocus(999)</onup>
			<onleft>noop</onleft><onright>noop</onright><ondown>noop</ondown>
		</control>
		<control type="group">
			<visible>!Window.IsVisible(sliderdialog) + !Window.IsVisible(selectdialog) + !Window.IsVisible(osdsubtitlesettings) + !Window.IsVisible(osdaudiosettings) + !Window.IsVisible(osdvideosettings)</visible>
			<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture colordiffuse="66000000">common/white.png</texture></control>
			<control type="image"><left>0</left><top>0</top><width>1920</width><height>260</height><texture colordiffuse="cc000000">fg/scrim_t.png</texture></control>
			<include>FG_NowPill</include>
			<control type="group">
				<visible>!Skin.HasSetting(aeon.osd.noclock)</visible>
				<include>FG_ClockCapsuleEnds</include>
			</control>
			<!-- overview: cast as chips (default) -->
			<control type="group">
				<visible>String.IsEmpty(%(page)s) + !%(photos)s + !$EXP[FG_OSDLive]</visible>
				<animation type="Visible" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" time="200"/><effect type="slide" start="0,-24" end="0,0" time="260" tween="cubic" easing="out"/></animation>
%(chips)s			</control>
			<!-- overview: cast as photos (Skin settings > ... > Cast photos in the information screen) -->
			<control type="group">
				<visible>String.IsEmpty(%(page)s) + %(photos)s + !$EXP[FG_OSDLive]</visible>
				<animation type="Visible" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" time="200"/><effect type="slide" start="0,-24" end="0,0" time="260" tween="cubic" easing="out"/></animation>
%(photo)s			</control>
			<!-- Live TV (0.46.1): the compact card -->
			<control type="group">
				<visible>String.IsEmpty(%(page)s) + $EXP[FG_OSDLive]</visible>
				<animation type="Visible" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" time="200"/><effect type="slide" start="0,24" end="0,0" time="260" tween="cubic" easing="out"/></animation>
%(live)s			</control>
			<!-- second page: file and season -->
			<control type="group">
				<visible>String.IsEqual(%(page)s,2)</visible>
				<animation type="Visible" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" time="200"/><effect type="slide" start="0,24" end="0,0" time="260" tween="cubic" easing="out"/></animation>
%(page2)s			</control>
		</control>
	</include>
	<!-- FG_FULLINFO:end -->
''' % {'page': PAGE, 'photos': PHOTOS,
       'chips': overview(320, 722, 270, 405, 'm270x405.png', 446, 4, False),
       'photo': overview(170, 872, 230, 345, 'm230x345.png', 406, 3, True),
       'page2': page2(), 'live': live_card()}
BODY = BODY.replace('<width>$PARAM[w]</width><height>44</height><texture border="22" colordiffuse="1cffffff">fg/r22.png', '<width>300</width><height>44</height><texture border="22" colordiffuse="1cffffff">fg/r22.png')

t = io.open(INC, encoding='utf-8').read()
t = re.sub(r'\t<!-- FG_FULLINFO:begin.*?<!-- FG_FULLINFO:end -->\n', '', t, flags=re.S)
t = t.replace('</includes>', BODY + '</includes>')
io.open(INC, 'w', encoding='utf-8', newline='\n').write(t)

d = io.open(DLG, encoding='utf-8').read()
if 'FG_FullInfo' not in d:
    a = d.index('\t<controls>\n') + len('\t<controls>\n')
    b = d.index('\t</controls>')
    classic = d[a:b]
    d = (d[:a] + '\t\t<include condition="Skin.HasSetting(aeon.fglass)">FG_FullInfo</include>\n'
         '\t\t<include condition="!Skin.HasSetting(aeon.fglass)">FullInfo_Classic</include>\n' + d[b:])
    d = d.replace('\t<defaultcontrol always="true">999</defaultcontrol>\n',
                  '\t<defaultcontrol always="true">999</defaultcontrol>\n'
                  '\t<onload condition="Skin.HasSetting(aeon.fglass)">ClearProperty(fgpage,fullscreeninfo)</onload>\n'
                  '\t<onload condition="Skin.HasSetting(aeon.fglass)">RunScript(script.aeon.helper,playerfacts)</onload>\n')
    io.open(DLG, 'w', encoding='utf-8', newline='\n').write(d)
    t = io.open(INC, encoding='utf-8').read()
    t = t.replace('</includes>', '\t<!-- the information screen of the Aeon / Glass themes (DialogFullScreenInfo.xml, 0.28.1 / 0.38.0) -->\n'
                  '\t<include name="FullInfo_Classic">\n' + classic + '\t</include>\n</includes>')
    io.open(INC, 'w', encoding='utf-8', newline='\n').write(t)
import xml.etree.ElementTree as ET
ET.parse(INC); ET.parse(DLG)
print('ok')
