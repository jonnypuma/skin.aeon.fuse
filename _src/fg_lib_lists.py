# -*- coding: utf-8 -*-
"""0.48.0 Fused Glass library views, phase 3 (after the approved mockups): Flix (528), Circles (536), Combined (529),
Low list (527) and Episode list (511). Imported by fg_lib.py, which writes them into its block; each view's include
loads them in Fused Glass instead of the Aeon views (the Aeon views stay as they were).

Shared parts: the detail block of the item in focus (kicker, clearlogo or name, rating sources and facts, "x of y
watched", media chips, tagline, plot: a vertical grouplist, so what an item lacks takes no room), the art row (poster
with its watched mark beside the landscape art; an episode: its still beside the season poster with the season's
ring), list rows with dark ink on the white focus row, and the season ring of an episode list (from the container's
watched / unwatched counts)."""
from fg_lib import img, lbl, textbox, glass, marks, header, rail, big_chip, meta_label, rounded_mask, mark_exprs, row_chips, row_lead, MARK, TICK, status_line, status_items, panel_chips, row_chips_right, chips_start, studio_text
from fg_lib_walls import focus_vars, tile

VIEWS = (528, 536, 529, 527, 511)
MARKED = (527,)                    # views that draw the watched mark of the item in focus (marks(str(cid)))
SRC = (('imdb', 'ratings/imdb.png'), ('tmdb', 'ratings/tmdb.png'), ('rt', 'ratings/rtfresh.png'))


# ------------------------------------------------------------------------------------------------------------ variables
def view_vars(cid):
    """Art and ink of the item in focus of cid, on top of the walls' facts (focus_vars) and its watched marks."""
    C = 'Container(%d).ListItem' % cid
    d = {'t': cid, 'C': C}
    marks_of = mark_exprs(str(cid), sets=False) if cid in MARKED else ''           # the big percent table only where a view needs it
    return focus_vars(cid) + marks_of + '''	<variable name="FG_L%(t)s_Poster">
		<value condition="String.IsEqual(%(C)s.DBType,episode) + !String.IsEmpty(%(C)s.Art(season.poster))">$INFO[%(C)s.Art(season.poster)]</value>
		<value condition="!String.IsEmpty(%(C)s.Art(poster))">$INFO[%(C)s.Art(poster)]</value>
		<value condition="!String.IsEmpty(%(C)s.Art(tvshow.poster))">$INFO[%(C)s.Art(tvshow.poster)]</value>
		<value>$INFO[%(C)s.Art(thumb)]</value>
	</variable>
	<variable name="FG_L%(t)s_Wide">
		<value condition="String.IsEqual(%(C)s.DBType,episode)">$INFO[%(C)s.Art(thumb)]</value>
		<value condition="!String.IsEmpty(%(C)s.Art(landscape))">$INFO[%(C)s.Art(landscape)]</value>
		<value condition="!String.IsEmpty(%(C)s.Art(tvshow.landscape))">$INFO[%(C)s.Art(tvshow.landscape)]</value>
		<value condition="!String.IsEmpty(%(C)s.Art(fanart))">$INFO[%(C)s.Art(fanart)]</value>
		<value>$INFO[%(C)s.Art(tvshow.fanart)]</value>
	</variable>
	<variable name="FG_L%(t)s_Fanart">
		<value condition="!String.IsEmpty(%(C)s.Art(fanart))">$INFO[%(C)s.Art(fanart)]</value>
		<value condition="!String.IsEmpty(%(C)s.Art(tvshow.fanart))">$INFO[%(C)s.Art(tvshow.fanart)]</value>
		<value>$INFO[%(C)s.Art(landscape)]</value>
	</variable>
	<variable name="FG_L%(t)s_Show">
		<value condition="String.IsEqual(%(C)s.DBType,episode) | String.IsEqual(%(C)s.DBType,season)">$INFO[%(C)s.TVShowTitle]</value>
		<value>$INFO[%(C)s.Label]</value>
	</variable>
	<variable name="FG_L%(t)s_Ink"><value condition="Control.HasFocus(%(t)s)">aeon_onbar</value><value>ffffffff</value></variable>
	<variable name="FG_L%(t)s_Ink2"><value condition="Control.HasFocus(%(t)s)">9e0f1115</value><value>a8ffffff</value></variable>
	<variable name="FG_L%(t)s_ChipEdge"><value condition="Control.HasFocus(%(t)s)">730f1115</value><value>66ffffff</value></variable>
''' % d


def season_vars():
    """The season ring of an episode list: the container's watched / unwatched episodes."""
    w, u = 'Container.TotalWatched', 'Container.TotalUnWatched'
    x = ('\t<expression name="FG_LS_Ring">Integer.IsGreater(%s,0) + Integer.IsGreater(%s,0)</expression>\n'
         '\t<expression name="FG_LS_Tick">Integer.IsGreater(%s,0) + Integer.IsEqual(%s,0)</expression>\n'
         '\t<expression name="FG_LS_Dot">Integer.IsEqual(%s,0) + Integer.IsGreater(%s,0)</expression>\n' % (w, u, w, u, w, u))
    x += '\t<variable name="FG_LS_Pct">\n'
    for t in range(2, 31):
        for k in range(1, t):
            x += '\t\t<value condition="String.IsEqual(%s,%d) + String.IsEqual(%s,%d)">%d</value>\n' % (w, k, u, t - k, round(100 * k / t))
    x += '\t\t<value>50</value>\n\t</variable>\n'
    return x


def season_marks(x, y, size):
    """The season's mark (ring, tick or dot) with a dark disc behind ring and tick, as marks(badge=True)."""
    ring = '$EXP[FG_LS_Ring] + $EXP[FG_L_RingsOn]'
    tick = '$EXP[FG_LS_Tick] + $EXP[FG_L_TicksOn]'
    dot = '$EXP[FG_LS_Dot] + $EXP[FG_L_DotsOn]'
    pad = round(size * 0.18)
    t = round(size * 0.72)
    o = (size - t) // 2
    dsz = max(12, round(size * 0.42))
    return (img(x - pad, y - pad, size + 2 * pad, size + 2 * pad, 'fg/circle.png', 'b3080a0e', vis='[%s] | [%s]' % (ring, tick))
            + img(x, y, size, size, 'fg/ring/t.png', '4dffffff', vis=ring) + img(x, y, size, size, 'fg/ring/a$VAR[FG_LS_Pct].png', MARK, vis=ring)
            + img(x + o, y + o, t, t, 'aeon/icons/check.png', TICK, vis=tick, aspect='keep')
            + img(x + (size - dsz) // 2, y + (size - dsz) // 2, dsz, dsz, 'fg/circle.png', MARK, vis=dot))


# ------------------------------------------------------------------------------------------------------------ parts
def ratings(L):
    """Rating sources (a star and the library rating when none is known) for a horizontal grouplist."""
    out = ''
    for src, tex in SRC:
        v = '$EXP[Aeon_RH_%s] + $EXP[Aeon_VORat]' % src
        out += ('<control type="image"><width>38</width><height>28</height><aspectratio>keep</aspectratio><texture>%s</texture><visible>%s</visible></control>'
                '<control type="label"><width min="10" max="90">auto</width><height>34</height><aligny>center</aligny><font>lb_ui_22_semibold</font><textcolor>ffffffff</textcolor>'
                '<label>$VAR[Aeon_R_%s]</label><visible>%s</visible></control>' % (tex, v, src, v))
    none = '![$EXP[Aeon_RH_imdb] | $EXP[Aeon_RH_tmdb] | $EXP[Aeon_RH_rt]] + !String.IsEmpty(%s.Rating) + $EXP[Aeon_VORat]' % L
    out += ('<control type="image"><width>26</width><height>28</height><aspectratio>keep</aspectratio><texture colordiffuse="fg_mark">aeon/icons/star.png</texture><visible>%s</visible></control>'
            '<control type="label"><width min="10" max="90">auto</width><height>34</height><aligny>center</aligny><font>lb_ui_22_semibold</font><textcolor>ffffffff</textcolor>'
            '<label>$INFO[%s.Rating]</label><visible>%s</visible></control>' % (none, L, none))
    anyr = '[$EXP[Aeon_RH_imdb] | $EXP[Aeon_RH_tmdb] | $EXP[Aeon_RH_rt] | !String.IsEmpty(%s.Rating)] + $EXP[Aeon_VORat]' % L
    return out + meta_label('·', anyr)


def hgroup(w, h, inner, gap=10, vis=None):
    v = '<visible>%s</visible>' % vis if vis else ''
    return ('<control type="grouplist"><width>%d</width><height>%d</height><orientation>horizontal</orientation><itemgap>%d</itemgap><usecontrolcoords>true</usecontrolcoords>%s%s</control>'
            % (w, h, gap, v, inner))


def item_label(w, h, label, font, col, vis=None, align='left'):
    v = '<visible>%s</visible>' % vis if vis else ''
    return ('<control type="label"><width>%d</width><height>%d</height><align>%s</align><aligny>center</aligny><font>%s</font><textcolor>%s</textcolor><label>%s</label>%s</control>'
            % (w, h, align, font, col, label, v))


def detail(cid, x, y, w, h, logo_h=110, title_font='lb_font36_title', title_h=56, plot_h=150, kicker=True, name='all', chips=True, full_audio=True, season_logo=True):
    """The item in focus as a vertical grouplist at (x, y): kicker, clearlogo or name, rating sources and facts,
    "x of y watched", media chips, tagline, plot. name: 'all' (clearlogo or name), 'episode' (an episode's name only),
    'none'."""
    L = 'Container(%d).ListItem' % cid
    ep = 'String.IsEqual(%s.DBType,episode)' % L
    logo_on = '$EXP[FG_L_LogosOn] + !String.IsEmpty(%s.Art(clearlogo)) + !String.IsEqual(%s.DBType,season) + !%s' % (L, L, ep)
    out = ''
    if kicker:
        out += item_label(w, 28, '[UPPERCASE]$VAR[FG_L%d_Kicker][/UPPERCASE]' % cid, 'lb_cap_16', 'a3ffffff')
    if name == 'all' and season_logo:
        # a season: the show's clearlogo over the season's name
        out += ('<control type="image"><width>%d</width><height>%d</height><aspectratio align="left" aligny="center">keep</aspectratio><texture>$INFO[%s.Art(tvshow.clearlogo)]</texture>'
                '<visible>$EXP[FG_L_LogosOn] + String.IsEqual(%s.DBType,season) + !String.IsEmpty(%s.Art(tvshow.clearlogo))</visible></control>'
                % (min(w, 520), min(logo_h, 110), L, L, L))
    if name == 'all':
        out += ('<control type="image"><width>%d</width><height>%d</height><aspectratio align="left" aligny="center">keep</aspectratio><texture>$INFO[%s.Art(clearlogo)]</texture><visible>%s</visible></control>'
                % (min(w, 560), logo_h, L, logo_on))
        out += item_label(w, title_h, '$VAR[FG_L%d_Name]' % cid, title_font, 'ffffffff', '![%s]' % logo_on)
    elif name == 'episode':
        out += item_label(w, title_h, '$INFO[%s.Title]' % L, title_font, 'ffffffff', ep)
    out += hgroup(w, 34, ratings(L) + meta_label('$VAR[FG_L%d_Meta]' % cid))
    # 0.56.9 the info panel rule: the status line (the watched mark and its words), the row's chips
    out += status_line(str(cid), w)
    plot_h -= 42
    if chips:
        out += hgroup(w, 34, panel_chips(str(cid)), 8, '$EXP[Aeon_VOMedia]')
    out += item_label(w, 30, '$INFO[%s.Tagline]' % L, 'lb_tag_22', '8fffffff', '!String.IsEmpty(%s.Tagline) + $EXP[Aeon_VOPlot]' % L)
    out += ('<control type="textbox"><width>%d</width><height>%d</height><font>lb_body_24</font><textcolor>d9ffffff</textcolor><label>$INFO[%s.Plot]</label>'
            '<autoscroll delay="8000" time="2000" repeat="8000">true</autoscroll><visible>$EXP[Aeon_VOPlot]</visible></control>' % (w, plot_h, L))
    return ('<control type="grouplist"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><orientation>vertical</orientation><itemgap>10</itemgap>'
            '<usecontrolcoords>true</usecontrolcoords>%s</control>' % (x, y, w, h, out))


def art(x, y, w, h, tex, r=16, shadow=True, vis=None):
    out = '<control type="group"><left>%d</left><top>%d</top>%s' % (x, y, '<visible>%s</visible>' % vis if vis else '')
    if shadow:
        out += img(-30, -22, w + 60, h + 60, 'fg/sh24.png', '$VAR[FG_PanelSh_8c]', 64)
    out += img(0, 0, w, h, 'fg/r%d.png' % r, 'fg_frost', r) + img(0, 0, w, h, tex, diffuse='fg/m%dx%d.png' % (w, h), aspect='scale', bg=True)
    return out + '</control>'


def art_row(cid, x, y, h, poster_w, wide_w, gap=18, wide_first=False):
    """Poster (with the item's mark; an episode: the season poster with the season's ring) and the wide art (an
    episode: its still with the progress bar)."""
    L = 'Container(%d).ListItem' % cid
    ep = 'String.IsEqual(%s.DBType,episode)' % L
    px, wx = (x + wide_w + gap, x) if wide_first else (x, x + poster_w + gap)
    ms = 30 if poster_w < 200 else 38
    out = art(px, y, poster_w, h, '$VAR[FG_L%d_Poster]' % cid, 14)
    out += '<control type="group"><left>%d</left><top>%d</top><visible>!%s</visible>%s</control>' % (px, y, ep, marks(str(cid), poster_w - ms - 10, 10, ms, badge=True))
    out += '<control type="group"><left>%d</left><top>%d</top><visible>%s</visible>%s</control>' % (px, y, ep, season_marks(poster_w - ms - 10, 10, ms))
    out += art(wx, y, wide_w, h, '$VAR[FG_L%d_Wide]' % cid, 14)
    out += progress(wx + 16, y + h - 18, wide_w - 32, '%s.PercentPlayed' % L, '%s + Integer.IsGreater(%s.PercentPlayed,0)' % (ep, L))
    return out, {(poster_w, h, 14), (wide_w, h, 14)}


def progress(x, y, w, info, vis):
    return ('<control type="progress"><left>%d</left><top>%d</top><width>%d</width><height>6</height><texturebg border="3,0,3,0" colordiffuse="59ffffff">fg/pillh.png</texturebg>'
            '<midtexture border="3,0,3,0" colordiffuse="fg_mark">fg/pillh.png</midtexture><info>%s</info><visible>%s</visible></control>' % (x, y, w, info, vis))


def studio(cid, x, y, w, h, align='left', aligny='center'):
    L = 'Container(%d).ListItem' % cid
    return img(x, y, w, h, 'resource://resource.images.studios.white/$INFO[Window(Home).Property(aeon.studio)].png', 'ebffffff', aspect='keep', align=align, aligny=aligny,
               vis='!Skin.HasSetting(aeon.nostudio) + !String.IsEmpty(Window(Home).Property(aeon.studio)) + String.IsEqual(Window(Home).Property(aeon.studio.of),%s.Studio)' % L) + \
        studio_text(x, y, w, h, L, align, aligny)


def row(cid, w, h, focused, number=False, sub=True, chips=False):
    """A list row (0.56.8, the list row rule): the title (an episode's own title, no "01."), the grey line and after it
    the chips (films and episodes); numbered episode rows: the number, the title, under it the first-aired date and the
    chips (resolution, audio, aspect); at the right the run time (bold), the time left of an item in progress, or
    watched / total; the mark last. Dark ink on the white row in focus."""
    lit = 'Control.HasFocus(%d)' % cid
    out = ''
    if focused:
        out += img(0, 0, w, h, 'fg/r18.png', 'ffffffff', 18, lit) + img(0, 0, w, h, 'fg/r18.png', '1fffffff', 18, '!' + lit) + img(0, 0, w, h, 'fg/e18.png', '38ffffff', 18, '!' + lit)
    ink = '$VAR[FG_L%d_Ink]' % cid if focused else 'ffffffff'
    ink2 = '$VAR[FG_L%d_Ink2]' % cid if focused else 'a8ffffff'
    edge = '$VAR[FG_L%d_ChipEdge]' % cid if focused else '66ffffff'
    ep = 'String.IsEqual(ListItem.DBType,episode)'
    vid = '[%s | String.IsEqual(ListItem.DBType,movie) | String.IsEqual(ListItem.DBType,musicvideo)]' % ep
    x0 = 22
    if number:
        out += lbl(10, 3 if chips else 0, 44, 36 if chips else h, '$INFO[ListItem.Episode]', 'lb_ui_22_semibold', ink2, 'right')
        x0 = 70
    right_w = 116 if number else 126          # "1 h 52 m", "16 min left" (0.56.10: 126, room for four chips)
    tw = w - x0 - right_w - 74
    limit = w - right_w - 60 - 6              # the chips end before the right-hand text's box
    if sub:
        out += lbl(x0, h // 2 - 34, tw, 38, '$INFO[ListItem.Title]', 'lb_ui_24_bold', ink, vis=ep)
        out += lbl(x0, h // 2 - 34, tw, 38, '$INFO[ListItem.Label]', 'lb_ui_24_bold', ink, vis='!' + ep)
        if chips:     # films and episodes: the grey line, then the chips; the rest: the grey line only
            # 0.56.11: the chips right-aligned before the run time, the grey line up to them
            end, shift = w - 60 - 54 - 16, 72
            hdr = '[!String.IsEmpty(ListItem.VideoResolution) + $EXP[Aeon_VOMedia] + !String.IsEmpty(ListItem.HdrType)]'
            for v2, w_end in (('[%s]' % hdr, chips_start(end, shift, x0 + 200)), ('![%s]' % hdr, chips_start(end, shift, x0 + 200, False))):
                out += lbl(x0, h // 2 + 2, w_end - 12 - x0, 30, '$VAR[FG_L_RowSub]', 'lb_small_20', ink2, vis='%s + %s' % (vid, v2))
            out += '<control type="group"><visible>%s</visible>%s</control>' % (vid, row_chips_right(end, h // 2 + 4, 26, ink, edge, x0 + 200, shift))
            out += lbl(x0, h // 2 + 2, tw, 30, '$VAR[FG_L_RowSub]', 'lb_small_20', ink2, vis='!' + vid)
        else:
            out += lbl(x0, h // 2 + 2, tw, 30, '$VAR[FG_L_RowSub]', 'lb_small_20', ink2)
    elif number:      # two lines: the title; the first-aired date and the chips under it
        title_font = 'lb_ui_22_semibold' if not focused else 'lb_ui_24_bold'
        if chips:
            out += lbl(x0, 3, tw, 36, '$INFO[ListItem.Title]', title_font, ink)
            out += lbl(x0, 41, 90, 24, '$INFO[ListItem.Premiered]', 'lb_cap_16', ink2)
            out += row_chips_right(w - 60 - 48 - 14, 41, 23, ink, edge, x0 + 96, 60)      # 0.56.11: right-aligned
        else:
            out += lbl(x0, 0, tw, h, '$INFO[ListItem.Title]', title_font, ink)
    else:
        out += lbl(x0, 0, tw, h, '$INFO[ListItem.Label]', 'lb_ui_22_semibold' if not focused else 'lb_ui_24_bold', ink)
    out += lbl(w - right_w - 60, 0, right_w, h, '$VAR[FG_L_RowRight]', 'lb_ui_22_semibold' if number else 'lb_ui_24_semibold', ink, 'right')
    out += marks('', w - 46, (h - 28) // 2, 28, lit if focused else None)
    return out


def opening(cid, head=True, bg=True):
    return ('\t<include name="FG_V%d_View">\n\t\t<control type="group">\n\t\t\t<visible>Control.IsVisible(%d)</visible>\n\t\t\t<include>Anim_FadeVisible</include>\n%s%s'
            % (cid, cid, '\t\t\t<include>Aeon_V_Bg</include>\n' if bg else '', '\t\t\t%s\n' % header() if head else ''))


def closing(cid, base, az, icon='$VAR[FG_L_ContentIcon]', subs=(), always=False):
    return ('\t\t\t<!-- the rail -->\n\t\t\t' + rail(cid, base * 100 + 1, base * 100 + 50, icon, az.replace('SetFocus(510)', 'SetFocus(%d)' % cid), subs, always) + '\n'
            '\t\t</control>\n\t</include>\n')


def nav(cid, base, extra=''):
    return ('<onback condition="String.IsEqual(Skin.String(aeon.backmode),home)">ActivateWindow(home)</onback>%s' % extra)


# ------------------------------------------------------------------------------------------------------------ views
def v528(az):
    """Flix: the fanart of the item in focus fills the screen; its clearlogo and facts at the top left; at the top right
    the studio / network logo (a set: its films; an episode: its season poster with the season's ring); a row of big
    landscapes (seasons: posters) along the bottom."""
    cid, base = 528, 52800
    L = 'Container(528).ListItem'
    out = opening(cid, head=False, bg=False)
    out += '\t\t\t' + img(0, 0, 1920, 1080, '$VAR[FG_L528_Fanart]', aspect='scale', bg=True, extra='<fadetime>400</fadetime>') + '\n'
    out += ('\t\t\t<control type="videowindow"><width>1920</width><height>1080</height><visible>Player.HasVideo + !String.IsEmpty(Window(Home).Property(aeon.flixtrailer))</visible></control>\n')
    out += '\t\t\t' + img(0, 0, 1560, 1080, 'fg/scrim_l.png', 'f208090c') + img(0, 0, 1080, 1080, 'fg/scrim_l.png', 'b308090c') + img(0, 380, 1920, 700, 'fg/scrim_b.png', 'f708090c') + img(0, 0, 1920, 200, 'fg/scrim_t.png', '9908090c') + '\n'
    out += '\t\t\t' + lbl(96, 30, 1200, 30, '[UPPERCASE]$VAR[FG_L_Kicker]  ›  $VAR[FG_L_Title][/UPPERCASE]', 'lb_cap_16', 'a3ffffff') + '\n'
    out += '\t\t\t' + detail(cid, 96, 84, 840, 560, logo_h=150, title_font='lb_title_50', title_h=70, plot_h=110) + '\n'
    is_set = 'String.IsEqual(%s.DBType,set)' % L
    ep = 'String.IsEqual(%s.DBType,episode)' % L
    film = img(0, 0, 160, 240, '$VAR[Aeon_Poster]', diffuse='fg/m160x240.png', aspect='scale', bg=True) + marks('', 128, 8, 24)
    out += ('\t\t\t<control type="list" id="%d"><left>1106</left><top>84</top><width>712</width><height>240</height><orientation>horizontal</orientation>'
            '<scrolltime tween="cubic" easing="out">400</scrolltime><autoscroll time="5000">Integer.IsGreater(Container(%d).NumItems,4)</autoscroll><visible>%s</visible>'
            '<content>$VAR[FG_L528_Films]</content><itemlayout width="178" height="240">%s</itemlayout><focusedlayout width="178" height="240">%s</focusedlayout></control>\n'
            % (base * 100 + 5, base * 100 + 5, is_set, film, film))
    out += '\t\t\t' + art(1600, 40, 200, 300, '$INFO[%s.Art(season.poster)]' % L, 14, vis=ep + ' + !String.IsEmpty(%s.Art(season.poster))' % L)
    out += '<control type="group"><left>1600</left><top>40</top><visible>%s + !String.IsEmpty(%s.Art(season.poster))</visible>%s</control>' % (ep, L, season_marks(150, 10, 38))
    out += studio(cid, 1600, 360, 200, 64, 'center').replace('<visible>', '<visible>%s + ' % ep)
    out += studio(cid, 1600, 40, 200, 76, 'right', 'top').replace('<visible>', '<visible>!%s + !%s + ' % (ep, is_set)) + '\n'
    # the row: four landscapes (episodes: stills), seasons: posters with their bottoms in line; the list starts 28 px
    # above the tiles so the gold ring and the lift of a season poster are not clipped (0.51.0)
    land = lambda f: '<control type="group"><left>20</left><top>42</top>%s</control>' % tile(cid, 388, 218, f, '$VAR[FG_L_ArtLand]')
    post = lambda f: '<control type="group"><left>20</left><top>20</top>%s</control>' % tile(cid, 160, 240, f, '$VAR[FG_L_ArtPoster]', r=14)
    out += ('\t\t\t<control type="fixedlist" id="528"><left>76</left><top>674</top><width>1716</width><height>318</height><orientation>horizontal</orientation><focusposition>0</focusposition><movement>3</movement>'
            '<viewtype label="Flix">icon</viewtype><visible>Container.Content(movies) | Container.Content(sets) | Container.Content(tvshows) | Container.Content(seasons) | Container.Content(episodes) | Container.Content(musicvideos)</visible>'
            '<scrolltime tween="cubic" easing="out">300</scrolltime>%s<onup condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onup><ondown>%d</ondown>'
            '<itemlayout width="196" height="318" condition="Container.Content(seasons)">%s</itemlayout><focusedlayout width="196" height="318" condition="Container.Content(seasons)">%s</focusedlayout>'
            '<itemlayout width="424" height="318">%s</itemlayout><focusedlayout width="424" height="318">%s</focusedlayout></control>\n'
            % (nav(cid, base), base * 100 + 1, post(False), post(True), land(False), land(True)))
    out += closing(cid, base, az)
    return out, {(160, 240, 14), (200, 300, 14), (388, 218, 16)}


def v536(az):
    """Circles: cast and directors as round photos, seven a row, the name and the role under each."""
    cid, base = 536, 53600
    d = 176
    lit = 'Control.HasFocus(536)'

    def item(f):
        o = '<control type="group"><left>32</left><top>14</top>'
        if f:
            o += '<animation effect="zoom" start="100" end="105" center="auto" time="160" tween="cubic" easing="out" condition="%s">Conditional</animation>' % lit
        o += img(0, 0, d, d, 'fg/circle.png', '14ffffff')
        o += img(0, 0, d, d, '$INFO[ListItem.Art(thumb)]', diffuse='fg/m176x176.png', aspect='scale', bg=True)
        if f:
            o += img(-10, -10, d + 20, d + 20, 'fg/cr4.png', MARK, vis=lit)
        o += lbl(-32, d + 14, d + 64, 30, '$INFO[ListItem.Label]', 'lb_small_20_bold' if f else 'lb_small_20_semibold', 'ffffffff' if f else 'e6ffffff', 'center')
        o += lbl(-32, d + 42, d + 64, 28, '$INFO[ListItem.Label2]', 'lb_small_20', 'a8ffffff', 'center')
        return o + '</control>'
    out = opening(cid)
    out += ('\t\t\t<control type="panel" id="536"><left>104</left><top>166</top><width>1680</width><height>804</height><orientation>vertical</orientation><pagecontrol>%d</pagecontrol>'
            '<viewtype label="31292">icon</viewtype><visible>Container.Content(actors) | Container.Content(directors) | Container.Content(artists)</visible><preloaditems>2</preloaditems>'
            '<scrolltime tween="cubic" easing="out">260</scrolltime>%s<onup>Action(LastPage)</onup><ondown>Action(FirstPage)</ondown>'
            '<onleft condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onleft><onright>%d</onright>'
            '<itemlayout width="240" height="268">%s</itemlayout><focusedlayout width="240" height="268">%s</focusedlayout></control>\n'
            % (base * 100 + 50, nav(cid, base), base * 100 + 1, item(False), item(True)))
    out += closing(cid, base, az, 'common/aeon_film.png')
    return out, {(d, d, d // 2)}


def v529(az):
    """Combined: the posters in a row at the top; under them a card with the children of the one in focus at the left
    (a show's seasons, a set's films) and its facts at the right; seasons: the season's episodes across the card."""
    cid, base = 529, 52900
    L = 'Container(529).ListItem'
    seasons = 'Container.Content(seasons)'
    out = opening(cid)
    t = lambda f: '<control type="group"><left>20</left><top>14</top>%s</control>' % tile(cid, 160, 240, f, '$VAR[FG_L_ArtPoster]', r=14, caption=False)
    out += ('\t\t\t<control type="fixedlist" id="529"><left>76</left><top>152</top><width>1694</width><height>276</height><orientation>horizontal</orientation><focusposition>0</focusposition><movement>6</movement><pagecontrol>%d</pagecontrol>'
            '<viewtype label="31290">icon</viewtype><visible>Container.Content(tvshows) | Container.Content(sets) | Container.Content(seasons)</visible><scrolltime tween="cubic" easing="out">300</scrolltime>'
            '%s<onup condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onup><ondown condition="%s">5292</ondown><ondown condition="!%s">5291</ondown><onright>%d</onright>'
            '<itemlayout width="186" height="276">%s</itemlayout><focusedlayout width="186" height="276">%s</focusedlayout></control>\n'
            % (base * 100 + 50, nav(cid, base), seasons, seasons, base * 100 + 1, t(False), t(True)))
    out += '\t\t\t' + glass(96, 440, 1704, 600) + '\n'
    content = '<content target="videos" sortby="episode" sortorder="ascending">$INFO[Container(529).ListItem.FolderPath]</content>'
    lit1, lit2 = 'Control.HasFocus(5291)', 'Control.HasFocus(5292)'

    def child(f):            # a show's season / a set's film: 130 x 195, its name and a short fact under it
        o = '<control type="group"><left>12</left><top>10</top>'
        o += img(0, 0, 130, 195, 'fg/r12.png', 'fg_frost', 12) + img(0, 0, 130, 195, '$VAR[FG_L_ArtPoster]', diffuse='fg/m130x195.png', aspect='scale', bg=True)
        o += marks('', 96, 8, 26, badge=True)
        if f:
            o += img(-7, -7, 144, 209, 'fg/fr23.png', MARK, 24, lit1)
        o += lbl(0, 205, 136, 28, '$INFO[ListItem.Label]', 'lb_small_20_bold', 'ffffffff' if f else 'e6ffffff')
        o += lbl(0, 231, 136, 24, '$VAR[FG_L_RowRight]', 'lb_cap_14', 'a3ffffff')
        return o + '</control>'

    def episode(f):          # a season's episode: 300 x 169, "E3" and its name under it
        o = '<control type="group"><left>12</left><top>10</top>'
        o += img(0, 0, 300, 169, 'fg/r14.png', 'fg_frost', 14) + img(0, 0, 300, 169, '$INFO[ListItem.Art(thumb)]', diffuse='fg/m300x169.png', aspect='scale', bg=True)
        o += progress(14, 151, 272, 'ListItem.PercentPlayed', 'Integer.IsGreater(ListItem.PercentPlayed,0)')
        o += marks('', 258, 12, 28, badge=True)
        if f:
            o += img(-7, -7, 314, 183, 'fg/fr23.png', MARK, 24, lit2)
        o += lbl(0, 178, 300, 24, '[UPPERCASE]$LOCALIZE[20359] $INFO[ListItem.Episode][/UPPERCASE]', 'lb_cap_14', 'a3ffffff')
        o += lbl(0, 202, 300, 30, '$INFO[ListItem.Title]', 'lb_small_20_bold', 'ffffffff' if f else 'e6ffffff')
        return o + '</control>'
    out += ('\t\t\t<control type="panel" id="5291"><left>112</left><top>458</top><width>628</width><height>560</height><orientation>vertical</orientation>'
            '<scrolltime tween="cubic" easing="out">200</scrolltime><pagecontrol>%d</pagecontrol><onup>529</onup><onleft>529</onleft><onback>529</onback><onright>%d</onright><visible>!%s</visible>'
            '<itemlayout width="154" height="276">%s</itemlayout><focusedlayout width="154" height="276">%s</focusedlayout>%s</control>\n'
            % (base * 100 + 51, base * 100 + 1, seasons, child(False), child(True), content))
    out += ('\t\t\t<control type="panel" id="5292"><left>112</left><top>504</top><width>1652</width><height>524</height><orientation>vertical</orientation>'
            '<scrolltime tween="cubic" easing="out">200</scrolltime><pagecontrol>%d</pagecontrol><onup>529</onup><onleft>529</onleft><onback>529</onback><onright>%d</onright><visible>%s</visible>'
            '<itemlayout width="328" height="262">%s</itemlayout><focusedlayout width="328" height="262">%s</focusedlayout>%s</control>\n'
            % (base * 100 + 52, base * 100 + 1, seasons, episode(False), episode(True), content))
    # shows and sets: the facts at the right of the card
    out += ('\t\t\t<control type="group"><visible>!%s</visible>%s%s</control>\n'
            % (seasons, detail(cid, 788, 468, 984, 560, logo_h=110, title_h=56, plot_h=185), studio(cid, 1572, 950, 200, 70, 'right', 'bottom')))
    # seasons: the season's name and facts over its episodes
    out += ('\t\t\t<control type="grouplist"><left>124</left><top>456</top><width>1640</width><height>40</height><orientation>horizontal</orientation><itemgap>12</itemgap><usecontrolcoords>true</usecontrolcoords>'
            '<visible>%s</visible>%s%s%s%s</control>\n'
            % (seasons, '<control type="label"><width min="10" max="600">auto</width><height>36</height><aligny>center</aligny><font>lb_ui_24_bold</font><textcolor>ffffffff</textcolor><label>$INFO[%s.Label]</label></control>' % L,
               ratings(L), meta_label('$VAR[FG_L529_Meta]'), meta_label('·') + status_items('529', 36)))
    out += closing(cid, base, az, subs=((5291, base * 100 + 51), (5292, base * 100 + 52)), always=True)
    return out, {(160, 240, 14), (130, 195, 12), (300, 169, 14)}


def v527(az):
    """Low list: the show's clearlogo up top; the art and facts start level with the low card of rows at the bottom
    right (episodes: the still beside the season poster with the season's ring); the network logo at the bottom."""
    cid, base = 527, 52700
    L = 'Container(527).ListItem'
    out = opening(cid)
    logo = '$EXP[FG_L_LogosOn] + [!String.IsEmpty(%s.Art(clearlogo)) | !String.IsEmpty(%s.Art(tvshow.clearlogo))]' % (L, L)
    out += '\t\t\t' + img(96, 196, 580, 170, '$VAR[FG_L527_Logo]', aspect='keep', align='left', aligny='bottom', vis=logo)
    out += lbl(96, 196, 580, 170, '$VAR[FG_L527_Show]', 'lb_title_50', 'ffffffff', aligny='bottom', vis='![%s]' % logo) + '\n'
    seasons = 'Container.Content(seasons)'
    row_art, m = art_row(cid, 96, 420, 214, 143, 380, wide_first=True)
    out += '\t\t\t<control type="group"><visible>!%s</visible>%s%s</control>\n' % (
        seasons, row_art, detail(cid, 96, 656, 580, 330, name='episode', title_h=44, title_font='lb_ui_28_semibold', plot_h=142, chips=True))
    # seasons (short rows): the card is narrower and the season's poster with its ring and the facts get the room
    s = art(96, 420, 230, 345, '$VAR[FG_L527_Poster]', 14) + '<control type="group"><left>96</left><top>420</top>%s</control>' % marks('527', 182, 10, 38, badge=True)
    s += detail(cid, 354, 420, 610, 560, title_font='lb_font36_title', title_h=56, plot_h=222, season_logo=False)
    out += '\t\t\t<control type="group"><visible>%s</visible>%s</control>\n' % (seasons, s)
    out += '\t\t\t' + studio(cid, 96, 984, 160, 56) + '\n'
    out += '\t\t\t<control type="group"><visible>!%s</visible>%s</control>' % (seasons, glass(716, 420, 1084, 620))
    out += '<control type="group"><visible>%s</visible>%s</control>\n' % (seasons, glass(1028, 420, 772, 620))
    shift = lambda f: '<control type="group"><left>312</left>%s</control>' % row(cid, 748, 88, f, chips=True)
    out += ('\t\t\t<control type="list" id="527"><left>728</left><top>432</top><width>1060</width><height>596</height><pagecontrol>%d</pagecontrol><orientation>vertical</orientation>'
            '<viewtype label="31148">list</viewtype><visible>Container.Content(seasons) | Container.Content(episodes) | Container.Content(tvshows)</visible><scrolltime tween="cubic" easing="out">200</scrolltime>'
            '%s<onup>Action(LastPage)</onup><ondown>Action(FirstPage)</ondown><onleft condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onleft><onright>%d</onright>'
            '<itemlayout width="1060" height="98" condition="%s">%s</itemlayout><focusedlayout width="1060" height="98" condition="%s">%s</focusedlayout>'
            '<itemlayout width="1060" height="98">%s</itemlayout><focusedlayout width="1060" height="98">%s</focusedlayout></control>\n'
            % (base * 100 + 50, nav(cid, base), base * 100 + 1, seasons, shift(False), seasons, shift(True), row(cid, 1060, 88, False, chips=True), row(cid, 1060, 88, True, chips=True)))
    out += closing(cid, base, az)
    return out, m | {(230, 345, 14)}


def v511(az):
    """Episode list: the season poster (with the season's ring) and the network logo at the left, numbered rows in the
    middle card, the still and facts of the episode in focus at the right."""
    cid, base = 511, 51100
    L = 'Container(511).ListItem'
    out = opening(cid)
    out += '\t\t\t' + art(96, 160, 300, 450, '$VAR[FG_L511_Poster]', 18) + '<control type="group"><left>96</left><top>160</top>%s</control>' % season_marks(246, 14, 40) + '\n'
    out += '\t\t\t' + studio(cid, 96, 640, 300, 70, 'center') + '\n'
    out += '\t\t\t' + glass(432, 160, 640, 880) + '\n'
    out += ('\t\t\t<control type="list" id="511"><left>444</left><top>172</top><width>616</width><height>856</height><pagecontrol>%d</pagecontrol><orientation>vertical</orientation>'
            '<viewtype label="31144">list</viewtype><visible>Container.Content(episodes)</visible><scrolltime tween="cubic" easing="out">200</scrolltime>'
            '%s<onup>Action(LastPage)</onup><ondown>Action(FirstPage)</ondown><onleft condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onleft><onright>%d</onright>'
            '<itemlayout width="616" height="77">%s</itemlayout><focusedlayout width="616" height="77">%s</focusedlayout></control>\n'
            % (base * 100 + 50, nav(cid, base), base * 100 + 1, row(cid, 616, 70, False, number=True, sub=False, chips=True), row(cid, 616, 70, True, number=True, sub=False, chips=True)))
    out += '\t\t\t' + art(1112, 160, 688, 387, '$INFO[%s.Art(thumb)]' % L, 18)
    out += progress(1132, 160 + 387 - 22, 648, '%s.PercentPlayed' % L, 'Integer.IsGreater(%s.PercentPlayed,0)' % L) + '\n'
    out += '\t\t\t' + detail(cid, 1112, 571, 688, 470, name='episode', title_h=52, plot_h=190) + '\n'
    out += closing(cid, base, az)
    return out, {(300, 450, 18), (688, 387, 18)}


def ring_texture():
    """media/fg/cr4.png: a 4 px gold-ring outline for round photos (tinted fg_mark), 196 px."""
    import os
    from PIL import Image, ImageDraw
    S = 196 * 4
    im = Image.new('L', (S, S), 0)
    ImageDraw.Draw(im).ellipse([8, 8, S - 9, S - 9], outline=255, width=16)
    out = Image.new('RGBA', (S, S), (255, 255, 255, 0))
    out.putalpha(im)
    out.resize((196, 196), Image.LANCZOS).save(os.path.join('media', 'fg', 'cr4.png'), optimize=True)


def build(az):
    """The phase 3 variables and views (xml); writes their masks and textures."""
    xml = season_vars()
    for cid in VIEWS:
        xml += view_vars(cid)
    masks = set()
    for fn in (v528, v536, v529, v527, v511):
        v, m = fn(az)
        xml += v
        masks |= m
    for (w, h, r) in masks:
        rounded_mask(w, h, r)
    ring_texture()
    return xml
