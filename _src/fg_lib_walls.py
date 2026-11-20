# -*- coding: utf-8 -*-
"""0.47.0 Fused Glass walls, after the approved mockups: Poster wall (520), Landscape wall (521), Square wall (525),
Cards (526) and Showcase (523). Imported by fg_lib.py (which writes them into its block and loads them in Fused
Glass instead of the Aeon views).

Every wall: the header, the rail, the tiles (rounded art, the gold ring and a small lift on the tile in focus, the
watched mark in the corner, the name under it) and one info band for the item in focus: a narrow name column (genres,
clearlogo or title, the facts, the rating sources with "16 of 52 episodes watched", media chips or genres), the
tagline and plot as wide as they can be, a set's films (moving on every 5 s when more than four) and the studio /
network logo at the far right. Cards show the fanart with the clearlogo over it."""
import os

from PIL import Image, ImageDraw

from fg_lib import img, lbl, textbox, glass, marks, mark_exprs, header, rail, big_chip, meta_label, rounded_mask, media_vars, MARK, status_vars, status_line, panel_chips, studio_text

WALLS = (520, 521, 525, 526, 523)


def focus_ring_texture():
    """media/fg/fr23.png: a 4 px rounded ring (radius 23, the tile's 16 + 7) for 9-slice (border 24)."""
    S = 96 * 4
    im = Image.new('L', (S, S), 0)
    ImageDraw.Draw(im).rounded_rectangle([8, 8, S - 9, S - 9], 23 * 4, outline=255, width=4 * 4)
    out = Image.new('RGBA', (S, S), (255, 255, 255, 0))
    out.putalpha(im)
    out.resize((96, 96), Image.LANCZOS).save(os.path.join('media', 'fg', 'fr23.png'), optimize=True)


def focus_vars(cid):
    """The facts of the item in focus of container cid (as the List view's FG_L510_*)."""
    C = 'Container(%d).ListItem' % cid
    return '''	<!-- ===== the item in focus of %(t)s -->
	<variable name="FG_L%(t)s_Meta">
		<value condition="String.IsEqual(%(C)s.DBType,tvshow)">$INFO[%(C)s.Year]$VAR[FG_L%(t)s_Cert]$VAR[FG_L%(t)s_Seasons]</value>
		<value condition="String.IsEqual(%(C)s.DBType,season)">$INFO[%(C)s.Year,,  ·  ]$INFO[%(C)s.Property(TotalEpisodes),, $LOCALIZE[20360]]</value>
		<value condition="String.IsEqual(%(C)s.DBType,set)">$INFO[%(C)s.Property(Total),, $LOCALIZE[31114]]</value>
		<value condition="String.IsEqual(%(C)s.DBType,episode) + !String.IsEmpty(%(C)s.Premiered)">$INFO[%(C)s.Premiered]$VAR[FG_L%(t)s_Cert]$VAR[FG_L%(t)s_Run2]$INFO[%(C)s.EndTimeResume,  ·  $LOCALIZE[31030] ,]</value>
		<value condition="String.IsEqual(%(C)s.DBType,episode)">$VAR[FG_L%(t)s_Run]$INFO[%(C)s.EndTimeResume,  ·  $LOCALIZE[31030] ,]</value>
		<value>$INFO[%(C)s.Year]$VAR[FG_L%(t)s_Cert]$VAR[FG_L%(t)s_Run2]$INFO[%(C)s.EndTimeResume,  ·  $LOCALIZE[31030] ,]</value>
	</variable>
	<variable name="FG_L%(t)s_Watch">
		<value condition="String.IsEqual(%(C)s.DBType,tvshow) | String.IsEqual(%(C)s.DBType,season)">$INFO[%(C)s.Property(WatchedEpisodes)] $ADDON[skin.aeon.fuse 32285] $INFO[%(C)s.Property(TotalEpisodes)] $ADDON[skin.aeon.fuse 32323]</value>
		<value condition="String.IsEqual(%(C)s.DBType,set)">$INFO[%(C)s.Property(Watched)] $ADDON[skin.aeon.fuse 32285] $INFO[%(C)s.Property(Total)] $ADDON[skin.aeon.fuse 32321]</value>
	</variable>
	<variable name="FG_L%(t)s_Cert">
		<value condition="$EXP[Aeon_CertKnown] + Control.HasFocus(%(t)s)">  ·  $VAR[Aeon_Cert]</value>
		<value condition="!String.IsEmpty(%(C)s.MPAA) + !String.Contains(%(C)s.MPAA,:)">$INFO[%(C)s.MPAA,  ·  ,]</value>
	</variable>
	<variable name="FG_L%(t)s_Seasons">
		<value condition="Integer.IsEqual(%(C)s.Property(TotalSeasons),1)">  ·  1 $LOCALIZE[20373]</value>
		<value>$INFO[%(C)s.Property(TotalSeasons),  ·  , $LOCALIZE[33054]]</value>
	</variable>
	<variable name="FG_L%(t)s_Run">
		<value condition="Integer.IsGreater(%(C)s.Duration(mins),59)">$INFO[%(C)s.Duration(h)]h $INFO[%(C)s.Duration(mm)]m</value>
		<value>$INFO[%(C)s.Duration(mins),, min]</value>
	</variable>
	<variable name="FG_L%(t)s_Run2">
		<value condition="Integer.IsGreater(%(C)s.Duration(mins),59)">  ·  $INFO[%(C)s.Duration(h)]h $INFO[%(C)s.Duration(mm)]m</value>
		<value>$INFO[%(C)s.Duration(mins),  ·  , min]</value>
	</variable>
	<variable name="FG_L%(t)s_Kicker">
		<value condition="String.IsEqual(%(C)s.DBType,episode) + Integer.IsEqual(%(C)s.Season,1) + Integer.IsEqual(%(C)s.Episode,1)">S1 E1  ·  $LOCALIZE[31394]</value>
		<value condition="String.IsEqual(%(C)s.DBType,episode) + Integer.IsEqual(%(C)s.Episode,1) + Integer.IsGreater(%(C)s.Season,0)">S$INFO[%(C)s.Season] E1  ·  $LOCALIZE[31395]</value>
		<value condition="String.IsEqual(%(C)s.DBType,episode)">S$INFO[%(C)s.Season] E$INFO[%(C)s.Episode]</value>
		<value condition="String.IsEqual(%(C)s.DBType,season)">$INFO[%(C)s.TVShowTitle]</value>
		<value condition="String.IsEqual(%(C)s.DBType,set)">$LOCALIZE[20457]</value>
		<value>$INFO[%(C)s.Genre]</value>
	</variable>
	<variable name="FG_L%(t)s_Name">
		<value condition="String.IsEqual(%(C)s.DBType,episode)">$INFO[%(C)s.Title]</value>
		<value>$INFO[%(C)s.Label]</value>
	</variable>
	<variable name="FG_L%(t)s_Films">
		<value condition="String.IsEqual(%(C)s.DBType,set) + !String.IsEmpty(%(C)s.FolderPath)">$INFO[%(C)s.FolderPath]</value>
		<value condition="String.IsEqual(%(C)s.DBType,set)">videodb://movies/sets/$INFO[%(C)s.DBID]/</value>
	</variable>
''' % {'t': cid, 'C': C} + media_vars(str(cid)) + status_vars(str(cid))


ART_VARS = '''	<!-- ===== wall art by shape (ListItem in the tiles) -->
	<variable name="FG_L_ArtPoster">
		<value condition="!String.IsEmpty(ListItem.Art(poster))">$INFO[ListItem.Art(poster)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(tvshow.poster))">$INFO[ListItem.Art(tvshow.poster)]</value>
		<value>$INFO[ListItem.Art(thumb)]</value>
	</variable>
	<variable name="FG_L_ArtLand">
		<value condition="String.IsEqual(ListItem.DBType,episode) + !String.IsEmpty(ListItem.Art(thumb))">$INFO[ListItem.Art(thumb)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(landscape))">$INFO[ListItem.Art(landscape)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(tvshow.landscape))">$INFO[ListItem.Art(tvshow.landscape)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(fanart))">$INFO[ListItem.Art(fanart)]</value>
		<value>$INFO[ListItem.Art(thumb)]</value>
	</variable>
	<variable name="FG_L_ArtFanart">
		<value condition="!String.IsEmpty(ListItem.Art(fanart))">$INFO[ListItem.Art(fanart)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(tvshow.fanart))">$INFO[ListItem.Art(tvshow.fanart)]</value>
		<value>$INFO[ListItem.Art(landscape)]</value>
	</variable>
	<variable name="FG_L_ArtLogo">
		<value condition="!String.IsEmpty(ListItem.Art(clearlogo))">$INFO[ListItem.Art(clearlogo)]</value>
		<value>$INFO[ListItem.Art(tvshow.clearlogo)]</value>
	</variable>
'''


def tile(cid, w, h, focused, art, r=16, caption=True, logo=False, lift=True):
    """A wall tile at (0, 0): the art (rounded), the clearlogo over a shade (Cards), the watched mark, the name under
    it; in focus the gold ring around it and a small lift."""
    mask = 'fg/m%dx%d.png' % (w, h)
    lit = 'Control.HasFocus(%d)' % cid
    out = ''
    if focused:
        out += img(-28, -20, w + 56, h + 56, 'fg/sh16.png', '$VAR[FG_ShadowCol]', 56, lit)
    out += img(0, 0, w, h, 'fg/r%d.png' % r, 'fg_frost', r)
    out += img(0, 0, w, h, art, diffuse=mask, aspect='scale', bg=True)
    if logo:
        out += img(0, 0, w, h, 'fg/scrim_b.png', 'b3080a0e', diffuse=mask)
        out += img(round(w * 0.12), round(h * 0.6), round(w * 0.76), round(h * 0.34), '$VAR[FG_L_ArtLogo]', aspect='keep', align='center', aligny='bottom')
    ms = 36 if w >= 300 else 28
    out += marks('', w - ms - 12, 12, ms, badge=True)
    if focused:
        out += img(-7, -7, w + 14, h + 14, 'fg/fr23.png', 'fg_mark', 24, lit)
    if caption:
        out += lbl(-10, h + 12, w + 20, 32, '$INFO[ListItem.Label]', 'lb_small_20_bold' if focused else 'lb_small_20', 'ffffffff' if focused else 'a8ffffff', 'center')
    if focused and lift:
        out = ('<control type="group"><animation effect="zoom" start="100" end="105" center="auto" time="160" tween="cubic" easing="out" condition="%s">Conditional</animation>%s</control>'
               % (lit, out))
    return out


LEAD_W, LEAD_H = 154, 231           # the season poster that leads the Showcase band (seasons)


COL_W = 560        # the name column of the walls' info band (0.56.10)


def info_band(cid, y, h, films_id, lead=False):
    """The info band of the walls: a glass card from x 96 to 1800. lead: a season leads it with its poster and ring
    (Showcase); the name column and the plot then move right."""
    L = 'Container(%d).ListItem' % cid
    pad = 24
    inner_h = h - 2 * pad
    out = glass(96, y, 1704, h)
    # the name column (0.56.10: COL_W wide, was 380; the user: "way too cramped, make plot narrower"), its block centred
    col = 96 + pad
    season = 'String.IsEqual(%s.DBType,season)' % L
    shift = LEAD_W + 36 if lead else 0
    if lead:
        from fg_lib_lists import art as art_card
        out += ('<control type="group"><visible>%s</visible>%s<control type="group"><left>%d</left><top>%d</top>%s</control></control>'
                % (season, art_card(col, y + pad, LEAD_W, LEAD_H, '$VAR[FG_L%d_LPoster]' % cid, 12, shadow=False),
                   col, y + pad, marks(str(cid), LEAD_W - 36, 10, 26, badge=True)))
        out += ('<control type="group"><animation effect="slide" start="0,0" end="%d,0" time="0" condition="%s">Conditional</animation>' % (shift, season))
    logo_h = max(44, min(90, inner_h - 178))      # 0.56.9: the status line adds 34
    top = y + pad + max(0, (inner_h - logo_h - 178) // 2)
    # the clearlogo stands in for the name of a film, set or show (a season or an episode keeps its own name). 0.56.11 (the
    # user: "Put clearlogo here instead to give more space for the mediainfo etc."): it stands at the right of the name
    # column, beside the kicker, ratings and facts; the lines under them move up into the row it took
    logo_on = ('$EXP[FG_L_LogosOn] + !String.IsEmpty(%s.Art(clearlogo)) + !String.IsEqual(%s.DBType,season) + !String.IsEqual(%s.DBType,episode)' % (L, L, L))
    up = logo_h + 6
    d = up // 2
    lw = COL_W - 240
    kick = '[UPPERCASE]$VAR[FG_L%d_Kicker][/UPPERCASE]' % cid
    out += lbl(col, top, COL_W, 26, kick, 'lb_cap_16', 'a3ffffff', vis='![%s]' % logo_on)
    out += lbl(col, top + d, lw, 26, kick, 'lb_cap_16', 'a3ffffff', vis=logo_on)
    out += img(col + COL_W - 230, top + d, 230, 100, '$INFO[%s.Art(clearlogo)]' % L, aspect='keep', align='right', aligny='center', vis=logo_on)
    out += lbl(col, top + 30, COL_W, logo_h, '$VAR[FG_L%d_Name]' % cid, 'lb_font36_title', 'ffffffff', vis='![%s]' % logo_on)
    yy = top + 30 + logo_h + 6
    stack = lbl(col, yy + 34, COL_W, 32, '$VAR[FG_L%d_Meta]' % cid, 'lb_ui_22', 'ccffffff', vis='![%s]' % logo_on)
    stack += lbl(col, yy + 34, lw, 32, '$VAR[FG_L%d_Meta]' % cid, 'lb_ui_22', 'ccffffff', vis=logo_on)
    # the rating sources (a star and the library rating when none is known)
    rat = ''
    for src, tex in (('imdb', 'ratings/imdb.png'), ('tmdb', 'ratings/tmdb.png'), ('rt', 'ratings/rtfresh.png')):
        rat += ('<control type="image"><width>38</width><height>28</height><aspectratio>keep</aspectratio><texture>%s</texture><visible>$EXP[Aeon_RH_%s] + $EXP[Aeon_VORat]</visible></control>'
                '<control type="label"><width min="10" max="90">auto</width><height>32</height><aligny>center</aligny><font>lb_ui_22_semibold</font><textcolor>ffffffff</textcolor>'
                '<label>$VAR[Aeon_R_%s]</label><visible>$EXP[Aeon_RH_%s] + $EXP[Aeon_VORat]</visible></control>' % (tex, src, src, src))
    none = '![$EXP[Aeon_RH_imdb] | $EXP[Aeon_RH_tmdb] | $EXP[Aeon_RH_rt]] + !String.IsEmpty(%s.Rating) + $EXP[Aeon_VORat]' % L
    rat += ('<control type="image"><width>26</width><height>28</height><aspectratio>keep</aspectratio><texture colordiffuse="fg_mark">aeon/icons/star.png</texture><visible>%s</visible></control>'
            '<control type="label"><width min="10" max="90">auto</width><height>32</height><aligny>center</aligny><font>lb_ui_22_semibold</font><textcolor>ffffffff</textcolor>'
            '<label>$INFO[%s.Rating]</label><visible>%s</visible></control>' % (none, L, none))
    stack += ('<control type="grouplist"><left>%d</left><top>%d</top><width>%d</width><height>32</height><orientation>horizontal</orientation><itemgap>10</itemgap>'
              '<usecontrolcoords>true</usecontrolcoords>%s</control>' % (col, yy, COL_W, rat))
    stack += status_line(str(cid), COL_W, 32, col, yy + 68)
    chips = panel_chips(str(cid))      # resolution, audio, aspect ratio, HDR; the watched count is on the status line
    stack += ('<control type="grouplist"><left>%d</left><top>%d</top><width>%d</width><height>36</height><orientation>horizontal</orientation><itemgap>8</itemgap>'
              '<usecontrolcoords>true</usecontrolcoords>%s</control>' % (col, yy + 104, COL_W, chips))
    out += ('<control type="group"><animation effect="slide" start="0,0" end="0,-%d" time="0" condition="%s">Conditional</animation>%s</control>'
            % (up - d, logo_on, stack))
    if lead:
        out += '</control>'
    # tagline and plot, as wide as the band allows
    is_set = 'String.IsEqual(%s.DBType,set)' % L
    has_logo = ('[!String.IsEmpty(Window(Home).Property(aeon.studio)) | !String.IsEmpty(Window(Home).Property(aeon.studio.text))] + '      # 0.56.11: or its name
                'String.IsEqual(Window(Home).Property(aeon.studio.of),%s.Studio) + !Skin.HasSetting(aeon.nostudio)' % L)
    px = col + COL_W + 36
    ptop = y + pad
    right = 96 + 1704 - pad
    pw_full = right - px
    tag = '!String.IsEmpty(%s.Tagline)' % L
    variants = [('!%s + ![%s]' % (is_set, has_logo), 0, pw_full), ('!%s + %s' % (is_set, has_logo), 0, pw_full - 216), (is_set, 0, pw_full - 216 - 460)]
    if lead:                             # a season: the plot starts after the moved name column
        variants = [('!%s + %s' % (season, v), 0, pw) for v, _, pw in variants[:2]] + variants[2:] + [
            ('%s + ![%s]' % (season, has_logo), shift, pw_full - shift), ('%s + %s' % (season, has_logo), shift, pw_full - shift - 216)]
    lines = lambda H: int(int(H / 36.2) * 36.2)          # whole lines of lb_body_24 (36.2 px), so no half line shows
    for vis, dx, pw in variants:
        out += lbl(px + dx, ptop, pw, 30, '$INFO[%s.Tagline]' % L, 'lb_tag_22', '8fffffff', vis='%s + %s + $EXP[Aeon_VOPlot]' % (vis, tag))
        out += textbox(px + dx, ptop + 36, pw, lines(inner_h - 36), '$INFO[%s.Plot]' % L, 'lb_body_24', 'd9ffffff', '%s + %s + $EXP[Aeon_VOPlot]' % (vis, tag))
        out += textbox(px + dx, ptop, pw, lines(inner_h), '$INFO[%s.Plot]' % L, 'lb_body_24', 'd9ffffff', '%s + !%s + $EXP[Aeon_VOPlot]' % (vis, tag))
    # a set's films (moving on every 5 s when more than four)
    fh = min(150, inner_h - 6)
    fw = round(fh * 2 / 3)
    film = img(0, 0, fw, fh, '$VAR[Aeon_Poster]', diffuse='fg/m%dx%d.png' % (fw, fh), aspect='scale', bg=True) + marks('', fw - 24, 4, 20)
    out += ('<control type="list" id="%d"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><orientation>horizontal</orientation>'
            '<scrolltime tween="cubic" easing="out">400</scrolltime><autoscroll time="5000">Integer.IsGreater(Container(%d).NumItems,4)</autoscroll>'
            '<visible>%s</visible><content>$VAR[FG_L%d_Films]</content><itemlayout width="%d" height="%d">%s</itemlayout><focusedlayout width="%d" height="%d">%s</focusedlayout></control>'
            % (films_id, right - 216 - 440, ptop + (inner_h - fh) // 2, 440, fh, films_id, is_set, cid, fw + 12, fh, film, fw + 12, fh, film))
    # the studio / network logo at the far right
    out += img(right - 180, y + (h - 84) // 2, 180, 84, 'resource://resource.images.studios.white/$INFO[Window(Home).Property(aeon.studio)].png', 'ebffffff',
               aspect='keep', vis=has_logo, align='right', aligny='center')
    out += studio_text(right - 200, y + (h - 84) // 2, 200, 84, L, 'right', 'center')
    return out, (fw, fh)


def opening(cid):
    return ('\t<include name="FG_V%d_View">\n\t\t<control type="group">\n\t\t\t<visible>Control.IsVisible(%d)</visible>\n'
            '\t\t\t<include>Anim_FadeVisible</include>\n\t\t\t<include>Aeon_V_Bg</include>\n\t\t\t%s\n' % (cid, cid, header()))


def closing(cid, base, band, az):
    return ('\t\t\t<!-- the item in focus -->\n\t\t\t' + band + '\n'
            '\t\t\t<!-- the rail -->\n\t\t\t' + rail(cid, base * 100 + 1, base * 100 + 50, '$VAR[FG_L_ContentIcon]', az.replace('SetFocus(510)', 'SetFocus(%d)' % cid)) + '\n'
            '\t\t</control>\n\t</include>\n')


def wall(cid, base, shape, cols, w, h, y, gapy, band_y, band_h, caption=True, logo=False, viewlabel=None, visible=None, panel_h=None, az='', episodes=False):
    """A wall view: panel cid with cols columns of w x h tiles; the info band under it."""
    art = {'poster': '$VAR[FG_L_ArtPoster]', 'land': '$VAR[FG_L_ArtLand]', 'square': '$VAR[FG_L_ArtPoster]', 'fanart': '$VAR[FG_L_ArtFanart]'}[shape]
    r = 14 if shape == 'square' else 16
    # the tiles from x 96 to 1800 as the mockup (edge to edge); the panel starts 20 px further left and 14 px higher so
    # the gold ring and the lift of the tile in focus are not clipped
    gapx = (1704 - cols * w) // (cols - 1)
    iw, ih = w + gapx, h + gapy
    if panel_h is None:
        panel_h = min(14 + ih + h + (48 if caption else 14), band_y - (y - 14))
    item = '<control type="group"><left>20</left><top>14</top>%s</control>'
    band, film_size = info_band(cid, band_y, band_h, base * 100 + 5)
    out = opening(cid)
    ep_layouts, extra_masks = '', set()
    if episodes:
        # the Episode wall (episodes): the season poster with the season's ring and the show's logo at the left, the
        # stills three a row beside them (layouts that switch on the content; their tiles start 360 px further right)
        from fg_lib_lists import art as art_card, season_marks
        E = 'Container.Content(episodes)'
        L = 'Container(%d).ListItem' % cid
        ep = lambda f: '<control type="group"><left>360</left><top>14</top>%s</control>' % tile(cid, 420, 236, f, '$VAR[FG_L_ArtLand]', 16, caption)
        ep_layouts = ('<itemlayout width="472" height="294" condition="%s">%s</itemlayout><focusedlayout width="472" height="294" condition="%s">%s</focusedlayout>'
                      % (E, ep(False), E, ep(True)))
        out += ('\t\t\t<control type="group"><visible>%s</visible>%s<control type="group"><left>96</left><top>174</top>%s</control>%s</control>\n'
                % (E, art_card(96, 174, 300, 450, '$VAR[FG_L%d_SPoster]' % cid, 18), season_marks(246, 14, 40),
                   img(96, 648, 300, 96, '$INFO[%s.Art(tvshow.clearlogo)]' % L, aspect='keep', align='center', aligny='center')))
        extra_masks = {(420, 236, 16), (300, 450, 18)}
    out += ('\t\t\t<control type="panel" id="%d"><left>76</left><top>%d</top><width>%d</width><height>%d</height><pagecontrol>%d</pagecontrol><orientation>vertical</orientation>'
            '<viewtype label="%s">icon</viewtype><visible>%s</visible><preloaditems>2</preloaditems><scrolltime tween="cubic" easing="out">260</scrolltime>'
            '<onback condition="String.IsEqual(Skin.String(aeon.backmode),home)">ActivateWindow(home)</onback><onup>Action(LastPage)</onup><ondown>Action(FirstPage)</ondown>'
            '<onleft condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onleft><onright>%d</onright>'
            '%s<itemlayout width="%d" height="%d">%s</itemlayout><focusedlayout width="%d" height="%d">%s</focusedlayout></control>\n'
            % (cid, y - 14, cols * iw + 20, panel_h, base * 100 + 50, viewlabel, visible, base * 100 + 1, ep_layouts,
               iw, ih, item % tile(cid, w, h, False, art, r, caption, logo),
               iw, ih, item % tile(cid, w, h, True, art, r, caption, logo)))
    out += closing(cid, base, band, az)
    return out, {(w, h, r), film_size + (10,)} | extra_masks


def pill_textures():
    """media/fg/pill_l.png / pill_r.png (+ _e edges): the left and right halves of a radius-22 pill (r22 / e22 cut in
    two), so a pill can grow with its text (a fixed left part with a ring, a button of auto width)."""
    for src, l_name, r_name in (('r22.png', 'pill_l.png', 'pill_r.png'), ('e22.png', 'pill_le.png', 'pill_re.png')):
        im = Image.open(os.path.join('media', 'fg', src))
        w, h = im.size
        im.crop((0, 0, w // 2, h)).save(os.path.join('media', 'fg', l_name), optimize=True)
        im.crop((w // 2, 0, w, h)).save(os.path.join('media', 'fg', r_name), optimize=True)


def show_pill(cx, y):
    """Seasons: the progress of the season in focus in a glass pill centred at cx under the big poster (0.52.0, the
    user's call: a season view shows the season's numbers, the show's belong on the show views): the season's ring,
    tick or dot, "Season 3  ·  2 of 8 episodes watched". Three grouplists centred alike: the tint, the edge, the
    mark and text."""
    L = 'Container(523).ListItem'
    text = ('$INFO[%s.Label]  ·  $INFO[%s.Property(WatchedEpisodes)] $ADDON[skin.aeon.fuse 32285] $INFO[%s.Property(TotalEpisodes)] $ADDON[skin.aeon.fuse 32323]'
            % (L, L, L))
    vis = 'Container.Content(seasons) + String.IsEqual(%s.DBType,season) + !String.IsEmpty(%s.Property(TotalEpisodes))' % (L, L)

    def button(tex, col, ink):
        t = ('<texturenofocus border="0,22,22,22" colordiffuse="%s">%s</texturenofocus><texturefocus border="0,22,22,22" colordiffuse="%s">%s</texturefocus>'
             % (col, tex, col, tex)) if tex else '<texturenofocus/><texturefocus/>'
        return ('<control type="button"><width min="40" max="900">auto</width><height>44</height><label>%s</label><font>lb_small_20_bold</font>'
                '<textoffsetx>14</textoffsetx><aligny>center</aligny><textcolor>%s</textcolor><focusedcolor>%s</focusedcolor><disabledcolor>%s</disabledcolor>'
                '%s<enable>false</enable></control>' % (text, ink, ink, ink, t))

    def row(first, second):
        return ('<control type="grouplist"><left>%d</left><top>%d</top><width>1000</width><height>44</height><orientation>horizontal</orientation>'
                '<align>center</align><itemgap>0</itemgap>%s%s</control>' % (cx - 500, y, first, second))

    left_part = lambda tex, col: '<control type="image"><width>40</width><height>44</height><texture border="22,22,0,22" colordiffuse="%s">%s</texture></control>' % (col, tex)
    ring = '<control type="group"><width>40</width><height>44</height>' + marks('523', 16, 10, 24) + '</control>'
    return ('<control type="group"><visible>%s</visible>' % vis
            + row(left_part('fg/pill_l.png', 'fg_frost'), button('fg/pill_r.png', 'fg_frost', '00ffffff'))
            + row(left_part('fg/pill_le.png', 'fg_edge'), button('fg/pill_re.png', 'fg_edge', '00ffffff'))
            + row(ring, button(None, None, 'ffffffff')) + '</control>')


def showcase(cid, base, az):
    """Showcase (523): a cover flow of posters, the one in focus big in the middle, the info band. Seasons: the season
    poster with its ring leads the band, and the season's progress sits under the big poster."""
    sw, sh, bw, bh, gap = 220, 330, 330, 495, 36
    band, film_size = info_band(cid, 760, 280, base * 100 + 5, lead=True)
    lit = 'Control.HasFocus(%d)' % cid
    top = 160
    side = ('<control type="group"><left>%d</left><top>%d</top>' % (gap // 2, 190 + (bh - sh) // 2 - top)
            + img(0, 0, sw, sh, 'fg/r16.png', 'fg_frost', 16) + img(0, 0, sw, sh, '$VAR[FG_L_ArtPoster]', diffuse='fg/m%dx%d.png' % (sw, sh), aspect='scale', bg=True)
            + img(0, 0, sw, sh, 'fg/r16.png', '66080a0e', 16) + marks('', sw - 40, 12, 28, badge=True) + '</control>')
    big = ('<control type="group"><left>%d</left><top>%d</top>' % (gap // 2, 190 - top)
           + img(-30, -22, bw + 60, bh + 60, 'fg/sh24.png', '$VAR[FG_PanelSh_8c]', 64)
           + img(0, 0, bw, bh, 'fg/r18.png', 'fg_frost', 18) + img(0, 0, bw, bh, '$VAR[FG_L_ArtPoster]', diffuse='fg/m%dx%d.png' % (bw, bh), aspect='scale', bg=True)
           + marks('', bw - 52, 14, 38, badge=True) + img(-7, -7, bw + 14, bh + 14, 'fg/fr23.png', 'fg_mark', 24, lit) + '</control>')
    iw, bigw = sw + gap, bw + gap
    left = (96 + 1800) // 2 - bigw // 2 - 3 * iw          # three posters left of the big one, as the Aeon Showcase
    out = opening(cid)
    out += ('\t\t\t<control type="wraplist" id="%d"><left>%d</left><top>%d</top><width>%d</width><height>560</height><orientation>horizontal</orientation><focusposition>3</focusposition>'
            '<movement>2</movement><viewtype label="31138">icon</viewtype><visible>Container.Content(movies) | Container.Content(sets) | Container.Content(tvshows) | Container.Content(seasons)</visible>'
            '<scrolltime tween="cubic" easing="out">300</scrolltime><onback condition="String.IsEqual(Skin.String(aeon.backmode),home)">ActivateWindow(home)</onback>'
            '<onup condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onup><ondown>%d</ondown>'
            '<itemlayout width="%d" height="560">%s</itemlayout><focusedlayout width="%d" height="560">%s</focusedlayout></control>\n'
            % (cid, left, top, 1810 - left, base * 100 + 1, iw, side, bigw, big))       # clipped short of the rail
    out += '\t\t\t<!-- seasons: the show\'s own progress under the big poster -->\n\t\t\t' + show_pill((96 + 1800) // 2, 190 + bh + 18) + '\n'
    out += closing(cid, base, band, az)
    return out, {(sw, sh, 16), (bw, bh, 18), film_size + (10,), (LEAD_W, LEAD_H, 12)}


SPECS = (
    (520, dict(base=52000, shape='poster', cols=8, w=168, h=252, y=174, gapy=60, band_y=782, band_h=258, viewlabel='31130',
               visible='Container.Content(movies) | Container.Content(sets) | Container.Content(tvshows) | Container.Content(seasons)')),
    (521, dict(base=52100, shape='land', cols=4, w=396, h=223, y=174, gapy=66, band_y=760, band_h=280, viewlabel='31133', episodes=True, panel_h=586,
               visible='Container.Content(movies) | Container.Content(sets) | Container.Content(tvshows) | Container.Content(episodes) | Container.Content(musicvideos)')),
    (525, dict(base=52500, shape='square', cols=6, w=240, h=240, y=174, gapy=56, band_y=760, band_h=280, viewlabel='31134',
               visible='Container.Content(movies) | Container.Content(sets) | Container.Content(tvshows) | Container.Content(musicvideos) | Container.Content(seasons)')),
    (526, dict(base=52600, shape='fanart', cols=3, w=510, h=287, y=174, gapy=24, band_y=792, band_h=248, viewlabel='31136', caption=False, logo=True,
               visible='Container.Content(movies) | Container.Content(sets) | Container.Content(tvshows)')),
)


def build(az):
    """The walls' variables and views (xml); writes their masks and the focus ring."""
    xml, masks = ART_VARS, set()
    xml += ('\t<variable name="FG_L521_SPoster"><value condition="!String.IsEmpty(Container(521).ListItem.Art(season.poster))">$INFO[Container(521).ListItem.Art(season.poster)]</value>'
            '<value>$INFO[Container(521).ListItem.Art(tvshow.poster)]</value></variable>\n')
    xml += ('\t<variable name="FG_L523_LPoster"><value condition="!String.IsEmpty(Container(523).ListItem.Art(poster))">$INFO[Container(523).ListItem.Art(poster)]</value>'
            '<value>$INFO[Container(523).ListItem.Art(tvshow.poster)]</value></variable>\n')
    xml += mark_exprs('523', sets=False)            # the lead poster's ring (seasons only, so no set table)
    for cid in WALLS:
        xml += focus_vars(cid)
    for cid, args in SPECS:
        v, m = wall(cid, az=az, **args)
        xml += v
        masks |= m
    v, m = showcase(523, 52300, az)
    xml += v
    masks |= m
    for (w, h, r) in masks:
        rounded_mask(w, h, r)
    focus_ring_texture()
    pill_textures()
    return xml
