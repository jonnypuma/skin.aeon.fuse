# -*- coding: utf-8 -*-
"""0.52.0 Fused Glass: Season list combined 1 (517) and Season list combined 2 (518), after the boards 5120 / 5121
(A) and 5122 (B) of the library canvas. Fused Glass only (the Aeon themes have no view with these ids). Imported by
fg_lib.py, which writes them into its block; Includes_Views_Video.xml loads FG_V517_View / FG_V518_View.

1 (517): one layout for both pages. The seasons card | the focused season's episodes (5171, always there) | the
facts: the season (the show's fanart with the season's ring, the show's logo over the season's name, facts, genres,
plot, network logo) or, while the episodes have the focus, the episode (its still, facts, chips, plot). Right / Left
only move the focus.
2 (518): the seasons card and one wide glass card: the season poster with its ring, the facts and plot, the network
logo, and the season's episodes as a strip of stills (5181; Right goes into it, the facts then follow the episode)."""
from fg_lib import img, lbl, glass, marks, big_chip, meta_label, mark_exprs, status_line
from fg_lib_walls import tile
from fg_lib_lists import (view_vars, ratings, hgroup, item_label, art, progress, studio, row, opening, closing, nav, detail)

VIEWS = (517, 518)
NAMES = {517: '$ADDON[skin.aeon.fuse 32564]', 518: '$ADDON[skin.aeon.fuse 32566]'}


def ep_path_var(cid):
    C = 'Container(%d).ListItem' % cid
    return ('\t<variable name="FG_L%d_EpPath"><value condition="!String.IsEmpty(%s.TvShowDBID) + !String.IsEmpty(%s.Season)">'
            'videodb://tvshows/titles/$INFO[%s.TvShowDBID]/$INFO[%s.Season]/</value></variable>\n' % (cid, C, C, C, C))


def show_fan_var(cid):
    C = 'Container(%d).ListItem' % cid
    return ('\t<variable name="FG_L%d_ShowFan"><value condition="!String.IsEmpty(%s.Art(tvshow.fanart))">$INFO[%s.Art(tvshow.fanart)]</value>'
            '<value>$INFO[%s.Art(fanart)]</value></variable>\n' % (cid, C, C, C))


def build_vars():
    out = '\t<!-- ===== Season list combined 1 / 2 (0.52.0) -->\n'
    for cid in (517, 5171, 518, 5181):
        out += view_vars(cid)
    out += mark_exprs('517', sets=False) + mark_exprs('518', sets=False)
    out += ep_path_var(517) + ep_path_var(518) + show_fan_var(517)
    return out


def season_list(cid, base, onright):
    """The seasons card at the left: rows with the season's ring and x / y; the season stays lit (soft glass) while
    the focus is on its episodes."""
    return ('\t\t\t' + glass(96, 160, 480, 880) + '\n'
            '\t\t\t<control type="list" id="%d"><left>108</left><top>172</top><width>456</width><height>856</height><pagecontrol>%d</pagecontrol><orientation>vertical</orientation>'
            '<viewtype label="%s">list</viewtype><visible>Container.Content(seasons) + Skin.HasSetting(aeon.fglass)</visible><scrolltime tween="cubic" easing="out">220</scrolltime>'
            '%s<onup>Action(LastPage)</onup><ondown>Action(FirstPage)</ondown>'
            '<onleft condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onleft><onright>%s</onright>'
            '<itemlayout width="456" height="88">%s</itemlayout><focusedlayout width="456" height="88">%s</focusedlayout></control>\n'
            % (cid, base * 100 + 50, NAMES[cid], nav(cid, base), onright, row(cid, 456, 80, False), row(cid, 456, 80, True)))


def season_facts(cid, x, y, w, h, plot_h):
    """The season in focus: the show's logo over the season's name, rating sources and year, x of y watched, the
    genres as one chip, the plot (a vertical grouplist: what a season lacks takes no room)."""
    L = 'Container(%d).ListItem' % cid
    out = ('<control type="image"><width>%d</width><height>90</height><aspectratio align="left" aligny="center">keep</aspectratio><texture>$INFO[%s.Art(tvshow.clearlogo)]</texture>'
           '<visible>$EXP[FG_L_LogosOn] + !String.IsEmpty(%s.Art(tvshow.clearlogo))</visible></control>' % (min(w, 420), L, L))
    out += item_label(w, 64, '$INFO[%s.Label]' % L, 'lb_title_50', 'ffffffff')
    out += hgroup(w, 34, ratings(L) + meta_label('$VAR[FG_L%d_Meta]' % cid))
    out += status_line(str(cid), w)      # 0.56.9 the info panel rule: mark and "x of y episodes watched"; no genre chip
    out += ('<control type="textbox"><width>%d</width><height>%d</height><font>lb_body_24</font><textcolor>d9ffffff</textcolor><label>$INFO[%s.Plot]</label>'
            '<autoscroll delay="8000" time="2000" repeat="8000">true</autoscroll><visible>$EXP[Aeon_VOPlot]</visible></control>' % (w, plot_h, L))
    return ('<control type="grouplist"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><orientation>vertical</orientation><itemgap>10</itemgap>'
            '<usecontrolcoords>true</usecontrolcoords>%s</control>' % (x, y, w, h, out))


def quiet_rows(cid, w, h):
    """Episode rows that show no highlight while the list has no focus (the seasons page shows no episode picked)."""
    lit = 'Control.HasFocus(%d)' % cid
    focused = row(cid, w, h, True, number=True, sub=False, chips=True)
    for tex, col in (('fg/r18.png', '1fffffff'), ('fg/e18.png', '38ffffff')):
        focused = focused.replace(img(0, 0, w, h, tex, col, 18, '!' + lit), '')
    return row(cid, w, h, False, number=True, sub=False, chips=True), focused


def v517(az):
    cid, base = 517, 51700
    E = 'Container(5171).ListItem'
    out = opening(cid)
    out += season_list(cid, base, 'SetFocus(5171)')
    # the season's episodes, always there (no focus on the seasons page)
    it, fo = quiet_rows(5171, 576, 70)
    out += '\t\t\t' + glass(600, 160, 600, 880) + '\n'
    out += ('\t\t\t<control type="list" id="5171"><left>612</left><top>172</top><width>576</width><height>856</height><orientation>vertical</orientation><scrolltime tween="cubic" easing="out">200</scrolltime>'
            '<visible>Control.IsVisible(517)</visible><onleft>SetFocus(517)</onleft><onback>SetFocus(517)</onback><onup>Action(LastPage)</onup><ondown>Action(FirstPage)</ondown><onright>%d</onright><pagecontrol>%d</pagecontrol>'
            '<itemlayout width="576" height="77">%s</itemlayout><focusedlayout width="576" height="77">%s</focusedlayout>'
            '<content sortby="episode" sortorder="ascending">$VAR[FG_L517_EpPath]</content></control>\n' % (base * 100 + 1, base * 100 + 51, it, fo))
    # the season (the seasons page)
    s = art(1240, 160, 560, 315, '$VAR[FG_L517_ShowFan]', 18) + '<control type="group"><left>1240</left><top>160</top>%s</control>' % marks('517', 560 - 52, 14, 38, badge=True)
    s += season_facts(cid, 1240, 499, 560, 450, 190)
    s += studio(cid, 1620, 964, 180, 76, 'right', 'bottom')
    out += '\t\t\t<control type="group"><visible>!Control.HasFocus(5171)</visible><include>Anim_FadeVisible</include>%s</control>\n' % s
    # the episode (the episodes page)
    e = art(1240, 160, 560, 315, '$INFO[%s.Art(thumb)]' % E, 18) + progress(1260, 160 + 315 - 20, 520, '%s.PercentPlayed' % E, 'Integer.IsGreater(%s.PercentPlayed,0)' % E)
    e += detail(5171, 1240, 499, 560, 450, name='episode', title_h=52, plot_h=190, full_audio=False)
    e += studio(cid, 1620, 964, 180, 76, 'right', 'bottom')
    out += '\t\t\t<control type="group"><visible>Control.HasFocus(5171)</visible><include>Anim_FadeVisible</include>%s</control>\n' % e
    out += closing(cid, base, az, subs=((5171, base * 100 + 51),), always=True)
    return out, {(560, 315, 18)}


def strip_item(focused):
    """An episode of the strip: the still (gold ring and lift in focus), EPISODE n and the name under it."""
    lit = 'Control.HasFocus(5181)'
    out = '<control type="group"><left>14</left><top>12</top>%s</control>' % tile(5181, 262, 147, focused, '$INFO[ListItem.Art(thumb)]', 14, caption=False)
    out += lbl(14, 172, 262, 22, '[UPPERCASE]$LOCALIZE[20359] $INFO[ListItem.Episode][/UPPERCASE]', 'lb_cap_14', 'a3ffffff')
    out += lbl(14, 194, 262, 30, '$INFO[ListItem.Title]', 'lb_small_20_bold', 'ffffffff' if focused else 'e6ffffff')
    return out


def v518(az):
    cid, base = 518, 51800
    E = 'Container(5181).ListItem'
    out = opening(cid)
    out += season_list(cid, base, 'SetFocus(5181)')
    out += '\t\t\t' + glass(600, 160, 1200, 880) + '\n'
    # the season poster with its ring
    out += '\t\t\t' + art(632, 192, 300, 450, '$VAR[FG_L518_Poster]', 18) + '<control type="group"><left>632</left><top>192</top>%s</control>\n' % marks('518', 300 - 52, 14, 38, badge=True)
    # the facts: the season, or the episode while the strip has the focus
    out += '\t\t\t<control type="group"><visible>!Control.HasFocus(5181)</visible><include>Anim_FadeVisible</include>%s</control>\n' % season_facts(cid, 964, 192, 804, 450, 160)
    out += ('\t\t\t<control type="group"><visible>Control.HasFocus(5181)</visible><include>Anim_FadeVisible</include>%s</control>\n'
            % detail(5181, 964, 192, 610, 450, name='episode', title_h=52, plot_h=160, full_audio=False))
    out += '\t\t\t' + studio(cid, 1588, 192, 180, 64, 'right', 'top') + '\n'          # top right: clear of the plot
    # the season's episodes as a strip of stills
    out += '\t\t\t' + lbl(632, 668, 600, 26, '[UPPERCASE]$LOCALIZE[20360][/UPPERCASE]', 'lb_cap_16', 'a3ffffff') + '\n'
    out += ('\t\t\t<control type="list" id="5181"><left>610</left><top>694</top><width>1178</width><height>240</height><orientation>horizontal</orientation><scrolltime tween="cubic" easing="out">220</scrolltime>'
            '<visible>Control.IsVisible(518)</visible><onup>SetFocus(518)</onup><onleft>SetFocus(518)</onleft><onback>SetFocus(518)</onback><ondown>noop</ondown><onright>%d</onright><pagecontrol>%d</pagecontrol>'
            '<itemlayout width="284" height="240">%s</itemlayout><focusedlayout width="284" height="240">%s</focusedlayout>'
            '<content sortby="episode" sortorder="ascending">$VAR[FG_L518_EpPath]</content></control>\n' % (base * 100 + 1, base * 100 + 51, strip_item(False), strip_item(True)))
    out += closing(cid, base, az, subs=((5181, base * 100 + 51),), always=True)
    return out, {(300, 450, 18), (262, 147, 14)}


def build(az):
    from fg_lib import rounded_mask
    xml = build_vars()
    masks = set()
    for fn in (v517, v518):
        v, m = fn(az)
        xml += v
        masks |= m
    for (w, h, r) in masks:
        rounded_mask(w, h, r)
    return xml
