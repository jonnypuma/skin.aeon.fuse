# -*- coding: utf-8 -*-
"""0.48.0 Fused Glass library views, phase 3 second part (after the approved mockups): Banner list (522), Compact list
(524) and Season list (512). Imported by fg_lib.py like fg_lib_lists.py, whose parts it uses.

Banner and Compact keep their panes: Right from a film with versions or from a set enters them (one at a time on the
poster's place, or the strip of films under the facts, as the View settings choose: aeon.versions.grid /
aeon.sets.single). The Season list keeps Right to the season's episodes: the poster and facts make way for the
episode rows and the episode in focus, as the Aeon view swaps its info for them."""
from fg_lib import img, lbl, glass, marks, chip, mark_exprs, row_chips, MARK
from fg_lib_walls import focus_vars, tile
from fg_lib_lists import view_vars, detail, art, art_row, studio, row, opening, closing, nav, progress

VIEWS = (522, 524, 512, 5121)


def extra_vars():
    out = '''	<!-- ===== Banner list: the banner, else the landscape art -->
	<variable name="FG_L_ArtBanner">
		<value condition="!String.IsEmpty(ListItem.Art(banner))">$INFO[ListItem.Art(banner)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(tvshow.banner))">$INFO[ListItem.Art(tvshow.banner)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(landscape))">$INFO[ListItem.Art(landscape)]</value>
		<value>$INFO[ListItem.Art(fanart)]</value>
	</variable>
'''
    for cid in VIEWS:
        out += view_vars(cid)
    out += mark_exprs('522') + mark_exprs('524') + mark_exprs('512', sets=False)
    return out


def side(cid, one, grid, x, y, w, h, wide_w, text_logo=False):
    """The facts of the item in focus of a Banner / Compact list: art row, clearlogo or name, facts, chips, tagline and
    plot, the studio / network logo at the bottom; a set: its poster with the facts beside it and its films under
    them. one / grid: the panes' ids (a film's versions or a set's films, one at a time / the strip)."""
    L = 'Container(%d).ListItem' % cid
    is_set = 'String.IsEqual(%s.DBType,set)' % L
    exp1, exp2 = '$EXP[Aeon_C_One%d]' % cid, '$EXP[Aeon_C_Grid%d]' % cid
    pane = 'Container(%d)' % cid
    out = ''
    # not a set
    row_art, masks = art_row(cid, x, y, 340, 227, wide_w)
    g = row_art + detail(cid, x, y + 364, w, h - 364 - 90, logo_h=90, title_h=50, plot_h=150, full_audio=w >= 700) + studio(cid, x, y + h - 70, 200, 70)
    if text_logo:      # text titles: the clearlogo at the bottom right
        g += img(x + w - 280, y + h - 76, 280, 76, '$INFO[%s.Art(clearlogo)]' % L, aspect='keep', align='right', aligny='bottom',
                 vis='!$EXP[FG_L_LogosOn] + !String.IsEmpty(%s.Art(clearlogo))' % L)
    out += '<control type="group"><visible>!%s</visible>%s</control>' % (is_set, g)
    # a set: the poster, the facts beside it, its films under them
    s = art(x, y, 227, 340, '$VAR[FG_L%d_Poster]' % cid, 14) + '<control type="group"><left>%d</left><top>%d</top>%s</control>' % (x, y, marks(str(cid), 179, 10, 38, badge=True))
    s += detail(cid, x + 255, y, w - 255, 360, logo_h=96, title_h=50, plot_h=170, kicker=True, chips=False)     # 0.56.9: "Movie set" kicker
    s += studio(cid, x, y + h - 64, 200, 64)
    out += '<control type="group"><visible>%s</visible>%s</control>' % (is_set, s)
    # the strip (a set's films; a film's versions when the View settings show them as a grid): Right enters it
    film = lambda f: (img(0, 0, 140, 210, '$VAR[Aeon_Poster]', diffuse='fg/m140x210.png', aspect='scale', bg=True) + marks('', 108, 8, 24, badge=True)
                      + (img(-7, -7, 154, 224, 'fg/fr23.png', MARK, 24, 'Control.HasFocus(%d)' % grid) if f else ''))
    out += ('<control type="list" id="%d"><left>%d</left><top>%d</top><width>%d</width><height>224</height><orientation>horizontal</orientation>'
            '<scrolltime tween="cubic" easing="out">320</scrolltime><autoscroll time="5000">!Control.HasFocus(%d) + Integer.IsGreater(Container(%d).NumItems,5)</autoscroll>'
            '<onleft>%d</onleft><onup>%d</onup><onback>%d</onback><visible>%s</visible><content>$VAR[Aeon_LeftPane%d]</content>'
            '<itemlayout width="156" height="224"><control type="group"><left>7</left><top>7</top>%s</control></itemlayout>'
            '<focusedlayout width="156" height="224"><control type="group"><left>7</left><top>7</top>%s</control></focusedlayout></control>'
            % (grid, x - 7, y + 388 - 7, w + 14, grid, grid, cid, cid, cid, exp2, cid, film(False), film(True)))
    out += lbl(x, y + 610, w, 32, '$INFO[Container(%d).ListItem.Label]$INFO[Container(%d).ListItem.Year,  ·  ,]' % (grid, grid), 'lb_small_20_bold', 'ffffffff',
               vis='Control.HasFocus(%d)' % grid)
    # one at a time on the poster's place (a film's versions; a set's films when the View settings say so)
    one_item = (img(0, 0, 227, 340, '$VAR[Aeon_Poster]', diffuse='fg/m227x340.png', aspect='scale', bg=True) + img(0, 0, 227, 340, 'fg/r14.png', '99080a0e', 14)
                + lbl(12, 96, 203, 90, '$INFO[ListItem.Title]', 'lb_ui_24_bold', 'ffffffff', 'center', aligny='bottom')
                + lbl(12, 190, 203, 28, '[UPPERCASE]$INFO[ListItem.VideoVersionName][/UPPERCASE]', 'lb_cap_14', 'b3ffffff', 'center')
                + img(86, 228, 56, 56, 'aeon/ring_circle.png', 'd9ffffff') + img(104, 246, 20, 20, 'aeon/icons/play.png', 'ffffffff')
                + marks('', 189, 10, 28, badge=True))
    out += ('<control type="panel" id="%d"><left>%d</left><top>%d</top><width>227</width><height>340</height><orientation>vertical</orientation>'
            '<scrolltime tween="cubic" easing="out">320</scrolltime><onleft>%d</onleft><onright>noop</onright><onback>%d</onback><visible>%s</visible>'
            '<animation effect="fade" start="100" end="0" time="0" condition="!Control.HasFocus(%d)">Conditional</animation><content>$VAR[Aeon_LeftPane%d]</content>'
            '<itemlayout width="227" height="340">%s</itemlayout><focusedlayout width="227" height="340">%s</focusedlayout></control>'
            % (one, x, y, cid, cid, exp1, one, cid, one_item, one_item))
    out += img(x - 7, y - 7, 241, 354, 'fg/fr23.png', MARK, 24, 'Control.HasFocus(%d)' % one)
    out += lbl(x, y + 346, 227, 30, '$INFO[Container(%d).CurrentItem] / $INFO[Container(%d).NumItems]' % (one, one), 'lb_small_20_semibold', 'b3ffffff', 'center',
               'Control.HasFocus(%d) + Integer.IsGreater(Container(%d).NumItems,1)' % (one, one))
    return out, masks | {(227, 340, 14), (140, 210, 12)}


def list_nav(cid, one, grid, base):
    return ('<onright condition="$EXP[Aeon_C_One%(c)d]">SetFocus(%(o)d)</onright><onright condition="$EXP[Aeon_C_Grid%(c)d]">SetFocus(%(g)d)</onright>'
            '<onright condition="![$EXP[Aeon_C_Version%(c)d] | $EXP[Aeon_C_Set%(c)d]]">%(a)d</onright>' % {'c': cid, 'o': one, 'g': grid, 'a': base * 100 + 1})


def v522(az):
    """Banner list: the banners down the left, the item in focus in a card at the right."""
    cid, base = 522, 52200
    t = lambda f: '<control type="group"><left>20</left><top>7</top>%s</control>' % tile(cid, 612, 113, f, '$VAR[FG_L_ArtBanner]', r=14, caption=False, lift=False)
    out = opening(cid)
    out += ('\t\t\t<control type="list" id="522"><left>76</left><top>153</top><width>652</width><height>889</height><pagecontrol>%d</pagecontrol><orientation>vertical</orientation>'
            '<viewtype label="31140">list</viewtype><visible>Container.Content(tvshows) | Container.Content(movies) | Container.Content(seasons)</visible>'
            '<scrolltime tween="cubic" easing="out">240</scrolltime>%s<onup>Action(LastPage)</onup><ondown>Action(FirstPage)</ondown>'
            '<onleft condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onleft>%s'
            '<itemlayout width="652" height="127">%s</itemlayout><focusedlayout width="652" height="127">%s</focusedlayout></control>\n'
            % (base * 100 + 50, nav(cid, base), list_nav(cid, 5221, 5224, base), t(False), t(True)))
    out += '\t\t\t' + glass(748, 160, 1052, 880) + '\n'
    s, masks = side(cid, 5221, 5224, 776, 188, 996, 824, 680)
    out += '\t\t\t' + s + '\n' + closing(cid, base, az)
    return out, masks | {(612, 113, 14)}


def row_compact(cid, w, h, focused):
    """A Compact list row (0.56.8, the list row rule, one line): episodes their number in front; the title; the chips
    resolution, audio, aspect (films and episodes); the run time (bold), the time left of an item in progress, or
    watched / total; the mark last. The year has no column any more: the side panel shows it."""
    lit = 'Control.HasFocus(%d)' % cid
    out = ''
    if focused:
        out += img(0, 0, w, h, 'fg/r16.png', 'ffffffff', 16, lit) + img(0, 0, w, h, 'fg/r16.png', '1fffffff', 16, '!' + lit) + img(0, 0, w, h, 'fg/e16.png', '38ffffff', 16, '!' + lit)
    ink = '$VAR[FG_L%d_Ink]' % cid if focused else 'ffffffff'
    ink2 = '$VAR[FG_L%d_Ink2]' % cid if focused else 'a8ffffff'
    edge = '$VAR[FG_L%d_ChipEdge]' % cid if focused else '66ffffff'
    ep = 'String.IsEqual(ListItem.DBType,episode)'
    font = 'lb_ui_22_bold' if focused else 'lb_ui_22_semibold'
    # 0.56.10 (the user: "move chips to the right, closer to duration to provide more space for titles"): the chips end
    # 14 px before the run time; an item in progress ("16 min left", wider) has them further left
    prog = 'Integer.IsGreater(ListItem.PercentPlayed,0)'
    widths, gap = (48, 112, 60), 4
    span = sum(widths) + gap * (len(widths) - 1)
    for vis, end in (('!' + prog, w - 38 - 10 - 50 - 14), (prog, w - 38 - 10 - 108 - 12)):
        x = end - span
        out += lbl(18, 0, x - 12 - 18, h, '$INFO[ListItem.Label]', font, ink, vis='!%s + %s' % (ep, vis))
        out += lbl(54, 0, x - 12 - 54, h, '$INFO[ListItem.Title]', font, ink, vis='%s + %s' % (ep, vis))
        out += '<control type="group"><visible>%s</visible>%s</control>' % (vis, row_chips(x, (h - 24) // 2, 24, ink, edge, widths=widths, gap=gap))
    out += lbl(10, 0, 34, h, '$INFO[ListItem.Episode]', 'lb_small_20_semibold', ink2, 'right', vis=ep)
    out += lbl(w - 38 - 10 - 116, 0, 116, h, '$VAR[FG_L_RowRight]', 'lb_small_20_bold', ink, 'right')
    out += marks('', w - 38, (h - 22) // 2, 22, lit if focused else None)
    return out


def v524(az):
    """Compact list: many short rows in a card at the left, the item in focus at the right (text titles: the clearlogo
    at the bottom right)."""
    cid, base = 524, 52400
    out = opening(cid)
    out += '\t\t\t' + glass(96, 160, 740, 880) + '\n'
    out += ('\t\t\t<control type="list" id="524"><left>108</left><top>172</top><width>716</width><height>832</height><pagecontrol>%d</pagecontrol><orientation>vertical</orientation>'
            '<viewtype label="31142">list</viewtype><visible>Container.Content(movies) | Container.Content(sets) | Container.Content(tvshows) | Container.Content(seasons) | Container.Content(episodes) | Container.Content(musicvideos)</visible>'
            '<scrolltime tween="cubic" easing="out">200</scrolltime>%s<onup>Action(LastPage)</onup><ondown>Action(FirstPage)</ondown>'
            '<onleft condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onleft>%s'
            '<itemlayout width="716" height="64">%s</itemlayout><focusedlayout width="716" height="64">%s</focusedlayout></control>\n'
            % (base * 100 + 50, nav(cid, base), list_nav(cid, 5241, 5244, base), row_compact(cid, 716, 58, False), row_compact(cid, 716, 58, True)))
    s, masks = side(cid, 5241, 5244, 876, 160, 924, 880, 640, text_logo=True)
    out += '\t\t\t' + s + '\n' + closing(cid, base, az)
    return out, masks


def v512(az):
    """Season list: the seasons (with their rings) in a narrow card at the left, the season poster, the show's logo and
    the season's facts. Right opens the season's episodes in place of the poster and facts."""
    cid, base = 512, 51200
    L = 'Container(512).ListItem'
    out = opening(cid)
    out += '\t\t\t' + glass(96, 160, 540, 880) + '\n'
    out += ('\t\t\t<control type="list" id="512"><left>108</left><top>172</top><width>516</width><height>856</height><pagecontrol>%d</pagecontrol><orientation>vertical</orientation>'
            '<viewtype label="31146">list</viewtype><visible>Container.Content(seasons)</visible><scrolltime tween="cubic" easing="out">220</scrolltime>'
            '%s<onfocus>ClearProperty(aeon.info)</onfocus><onup>Action(LastPage)</onup><ondown>Action(FirstPage)</ondown>'
            '<onleft condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onleft><onright>SetProperty(aeon.info,1)</onright><onright>SetFocus(5121)</onright>'
            '<itemlayout width="516" height="88">%s</itemlayout><focusedlayout width="516" height="88">%s</focusedlayout></control>\n'
            % (base * 100 + 50, nav(cid, base), row(cid, 516, 80, False), row(cid, 516, 80, True)))
    # 0.53.3 hint B (board 5126 of the library canvas, the user's pick): the season's episodes peek in as a slim glass
    # strip beside the seasons card (the number of episodes, the word, a tick per episode: bright = watched), and a white
    # disc with a dark chevron rides on it at the season in focus: Right opens the episodes
    SX, SW = 652, 64
    g = glass(SX, 160, SW, 880)
    g += lbl(SX, 182, SW, 36, '$INFO[%s.Property(TotalEpisodes)]' % L, 'lb_ui_24_bold', 'ffffffff', 'center')
    # the word turned on its side: a centred label turns round its own centre (Kodi rotates at the aligned point)
    g += lbl(SX + SW // 2 - 80, 306 - 12, 160, 24, '[UPPERCASE]$LOCALIZE[20360][/UPPERCASE]', 'lb_cap_14', 'b3ffffff', 'center', extra='<angle>90</angle>')
    g += ('<control type="list" id="51290"><left>%d</left><top>396</top><width>26</width><height>168</height><orientation>vertical</orientation>'
          '<visible>!String.IsEmpty(%s.Property(TotalEpisodes))</visible>'
          '<itemlayout width="26" height="14"><control type="image"><left>0</left><top>0</top><width>26</width><height>5</height>'
          '<texture border="2" colordiffuse="d9ffffff">fg/pillh.png</texture><visible>Integer.IsGreater(ListItem.PlayCount,0)</visible></control>'
          '<control type="image"><left>0</left><top>0</top><width>26</width><height>5</height>'
          '<texture border="2" colordiffuse="4dffffff">fg/pillh.png</texture><visible>!Integer.IsGreater(ListItem.PlayCount,0)</visible></control></itemlayout>'
          '<focusedlayout width="26" height="14"/>'
          '<content sortby="episode" sortorder="ascending">$VAR[Aeon_SeasonEpPath]</content></control>' % (SX + (SW - 26) // 2, L))
    for k in range(10):            # the list shows ten rows of 88 from y 172; the row's bar is 80 high
        cy = 172 + k * 88 + 40
        g += ('<control type="group"><left>%d</left><top>%d</top><visible>Control.HasFocus(512) + Integer.IsEqual(Container(512).Position,%d)</visible>'
              '<animation effect="fade" start="0" end="100" time="120">Visible</animation>%s%s</control>'
              % (SX + SW // 2 - 18, cy - 18, k, img(0, 0, 36, 36, 'fg/circle.png', 'ffffffff'),
                 img(8, 8, 20, 20, 'aeon/icons/chevron_right.png', 'ff0f1115')))
    # the season: poster with its ring, the show's logo, the facts (moved over for the strip)
    PX, PW, PH = SX + SW + 40, 340, 510
    FX = PX + PW + 40
    FW = 1800 - FX
    logo = '$EXP[FG_L_LogosOn] + !String.IsEmpty(%s.Art(tvshow.clearlogo))' % L
    g += art(PX, 160, PW, PH, '$VAR[FG_L512_Poster]', 18) + '<control type="group"><left>%d</left><top>160</top>%s</control>' % (PX, marks('512', PW - 54, 14, 40, badge=True))
    g += img(FX, 160, FW, 96, '$INFO[%s.Art(tvshow.clearlogo)]' % L, aspect='keep', align='left', aligny='center', vis=logo)
    g += lbl(FX, 160, FW, 96, '$INFO[%s.TVShowTitle]' % L, 'lb_ui_28_semibold', 'ccffffff', vis='![%s]' % logo)
    g += detail(cid, FX, 272, FW, 470, kicker=False, title_font='lb_title_50', title_h=64, plot_h=222, season_logo=False)
    g += img(FX, 770, FW, 1, 'common/white.png', '24ffffff')
    g += lbl(FX, 788, 160, 34, '$LOCALIZE[515]', 'lb_ui_22', '99ffffff') + lbl(FX + 170, 788, FW - 170, 34, '$INFO[%s.Genre]' % L, 'lb_ui_22_semibold', 'ffffffff')
    g += lbl(FX, 834, 160, 56, '$LOCALIZE[572]', 'lb_ui_22', '99ffffff') + studio(cid, FX + 170, 834, 180, 56)
    out += '\t\t\t<control type="group"><visible>!$EXP[Aeon_EpOpen]</visible><include>Anim_FadeVisible</include>%s</control>\n' % g
    # the season's episodes (Right): rows in a card, the episode in focus beside them
    E = 'Container(5121).ListItem'
    e = glass(676, 160, 600, 880)
    e += ('<control type="list" id="5121"><left>688</left><top>172</top><width>576</width><height>856</height><orientation>vertical</orientation><scrolltime tween="cubic" easing="out">200</scrolltime>'
          '<onleft>ClearProperty(aeon.info)</onleft><onleft>SetFocus(512)</onleft><onback>ClearProperty(aeon.info)</onback><onback>SetFocus(512)</onback>'
          '<onup>Action(LastPage)</onup><ondown>Action(FirstPage)</ondown><onright>%d</onright><pagecontrol>%d</pagecontrol>'
          '<itemlayout width="576" height="77">%s</itemlayout><focusedlayout width="576" height="77">%s</focusedlayout>'
          '<content sortby="episode" sortorder="ascending">$VAR[Aeon_SeasonEpPath]</content></control>'
          % (base * 100 + 1, base * 100 + 51, row(5121, 576, 70, False, number=True, sub=False, chips=True), row(5121, 576, 70, True, number=True, sub=False, chips=True)))
    e += art(1316, 160, 484, 272, '$INFO[%s.Art(thumb)]' % E, 18) + progress(1334, 160 + 272 - 20, 448, '%s.PercentPlayed' % E, 'Integer.IsGreater(%s.PercentPlayed,0)' % E)
    e += detail(5121, 1316, 456, 484, 516, name='episode', title_h=52, plot_h=310, full_audio=False)     # 0.56.10: a longer plot
    e += studio(5121, 1316 + 484 - 200, 456 + 580 - 64, 200, 64, 'right', 'bottom')      # and the studio logo
    # faded out, not hidden: Right from the seasons must be able to give the episode list the focus
    out += ('\t\t\t<control type="group"><animation effect="fade" start="100" end="0" time="200" condition="!$EXP[Aeon_EpOpen]">Conditional</animation>%s</control>\n' % e)
    out += closing(cid, base, az, subs=((5121, base * 100 + 51),), always=True)
    return out, {(380, 570, 18), (340, 510, 18), (484, 272, 18)}


def build(az):
    from fg_lib import rounded_mask
    xml = extra_vars()
    masks = set()
    for fn in (v522, v524, v512):
        v, m = fn(az)
        xml += v
        masks |= m
    for (w, h, r) in masks:
        rounded_mask(w, h, r)
    return xml
