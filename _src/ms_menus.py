# -*- coding: utf-8 -*-
"""Aeon theme menu styles (0.40.0): Mosaic, Ledger, Bridge (default) and Tab slab, the four looks from
skin.glass/mockups/aeon-menus. Writes 1080i/Includes_MenuStyles.xml; the windows pick a look with
<include condition="$EXP[Aeon_MS_<style>]">MS_<window>_<style></include>.

Rules every look keeps: square flush boxes (no gaps, no rounding, no shadows), one row height (R = 72) for every
menu row, rows line up from box to box, box colours from the palette (aeon_box, x_panel, x_raised, x_deep), the
focus bar is aeon_white with aeon_onbar ink, and one artwork tile touches two boxes.

Run from the skin folder: python _src/ms_menus.py"""
import io
import os

R = 72
STYLES = ('mosaic', 'ledger', 'bridge', 'tabslab')
OUT = os.path.join('1080i', 'Includes_MenuStyles.xml')
W1 = 'f0ffffff'          # text on boxes
W2 = 'a0ffffff'          # secondary text
W3 = '6cffffff'          # captions
BOX = '$VAR[Aeon_BoxAccent]'  # the palette's box colour; with the Aeon palette the chosen Aeon accent (0.55.3)
CAP_ON_BOX = 'ccffffff'  # caption on the palette box


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def vis(cond):
    return '<visible>%s</visible>' % esc(cond) if cond else ''


def img(x, y, w, h, color, cond=None, tex='common/white.png', extra=''):
    return ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
            '<texture colordiffuse="%s">%s</texture>%s%s</control>' % (x, y, w, h, color, tex, extra, vis(cond)))


def art(x, y, w, h, info, cond=None, aspect='scale'):
    return ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
            '<aspectratio>%s</aspectratio><fadetime>120</fadetime><texture background="true">%s</texture>%s</control>'
            % (x, y, w, h, aspect, info, vis(cond)))


def icon(x, y, size, tex, color, cond=None):
    return ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
            '<aspectratio>keep</aspectratio><texture colordiffuse="%s">%s</texture>%s</control>' % (x, y, size, size, color, tex, vis(cond)))


def lab(x, y, w, h, text, font, color, align='left', cond=None, scroll=False, extra=''):
    return ('<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><align>%s</align>'
            '<aligny>center</aligny><font>%s</font><textcolor>%s</textcolor><selectedcolor>%s</selectedcolor>%s<label>%s</label>%s%s</control>'
            % (x, y, w, h, align, font, color, color, '<scroll>true</scroll>' if scroll else '', esc(text), extra, vis(cond)))


def textbox(x, y, w, h, text, font, color, cond=None, cid=None):
    return ('<control type="textbox"%s><left>%d</left><top>%d</top><width>%d</width><height>%d</height><font>%s</font>'
            '<textcolor>%s</textcolor><autoscroll time="3000" delay="6000" repeat="6000">true</autoscroll>'
            '<label>%s</label>%s</control>' % (' id="%d"' % cid if cid else '', x, y, w, h, font, color, esc(text), vis(cond)))


def group(x, y, inner, cond=None, extra=''):
    return '<control type="group"><left>%d</left><top>%d</top>%s%s\n%s\n</control>' % (x, y, extra, vis(cond), inner)


def include(name, body):
    return '\t<include name="%s">\n%s\n\t</include>\n' % (name, body)


def expression(name, body):
    return '\t<expression name="%s">%s</expression>\n' % (name, esc(body))


def variable(name, values):
    out = ['\t<variable name="%s">' % name]
    for cond, val in values:
        if cond:
            out.append('\t\t<value condition="%s">%s</value>' % (esc(cond), esc(val)))
        else:
            out.append('\t\t<value>%s</value>' % esc(val))
    out.append('\t</variable>\n')
    return '\n'.join(out)


# ---------------------------------------------------------------------------------------------------------------
# which look: the Aeon theme (not Glass, not Fused Glass) with its own menus (Menu theme not Fuse)
HEAD = []
HEAD.append(expression('Aeon_MS', '!Skin.HasSetting(aeon.vglass) + !String.IsEqual(Skin.String(aeon.menutheme),fused)'))
for s in ('mosaic', 'ledger', 'tabslab'):
    HEAD.append(expression('Aeon_MS_' + s, '$EXP[Aeon_MS] + String.IsEqual(Skin.String(aeon.menutheme),%s)' % s))
HEAD.append(expression('Aeon_MS_bridge', '$EXP[Aeon_MS] + !String.IsEqual(Skin.String(aeon.menutheme),mosaic) + '
                       '!String.IsEqual(Skin.String(aeon.menutheme),ledger) + !String.IsEqual(Skin.String(aeon.menutheme),tabslab)'))

# the item a menu is about: what the window underneath has in focus, or what plays when the menu is over the video
FS = 'Window.IsVisible(fullscreenvideo)'
HEAD.append(expression('MS_HasPoster', '[%s + [!String.IsEmpty(Player.Art(poster)) | !String.IsEmpty(Player.Art(tvshow.poster))]] | '
                       '[!%s + [!String.IsEmpty(ListItem.Art(poster)) | !String.IsEmpty(ListItem.Art(tvshow.poster)) | '
                       '!String.IsEmpty(ListItem.Art(thumb))]]' % (FS, FS)))
HEAD.append(variable('MS_Poster', [
    (FS + ' + !String.IsEmpty(Player.Art(tvshow.poster))', '$INFO[Player.Art(tvshow.poster)]'),
    (FS, '$INFO[Player.Art(poster)]'),
    ('!String.IsEmpty(ListItem.Art(poster))', '$INFO[ListItem.Art(poster)]'),
    ('!String.IsEmpty(ListItem.Art(tvshow.poster))', '$INFO[ListItem.Art(tvshow.poster)]'),
    ('', '$INFO[ListItem.Art(thumb)]')]))
HEAD.append(expression('MS_HasFanart', '[%s + [!String.IsEmpty(Player.Art(fanart)) | !String.IsEmpty(Player.Art(tvshow.fanart))]] | '
                       '[!%s + [!String.IsEmpty(ListItem.Art(fanart)) | !String.IsEmpty(ListItem.Art(tvshow.fanart))]]' % (FS, FS)))
HEAD.append(variable('MS_Fanart', [
    (FS + ' + !String.IsEmpty(Player.Art(fanart))', '$INFO[Player.Art(fanart)]'),
    (FS, '$INFO[Player.Art(tvshow.fanart)]'),
    ('!String.IsEmpty(ListItem.Art(fanart))', '$INFO[ListItem.Art(fanart)]'),
    ('', '$INFO[ListItem.Art(tvshow.fanart)]')]))
HEAD.append(variable('MS_ItemTitle', [(FS, '$INFO[VideoPlayer.Title]'),
                                      ('!String.IsEmpty(ListItem.Label)', '$INFO[ListItem.Label]'), ('', '$LOCALIZE[33063]')]))
HEAD.append(variable('MS_ItemKicker', [
    (FS + ' + !String.IsEmpty(VideoPlayer.TVShowTitle)', '$INFO[VideoPlayer.TVShowTitle]$INFO[VideoPlayer.Season, · S,]$INFO[VideoPlayer.Episode,E,]'),
    (FS, '$INFO[VideoPlayer.Year]'),
    ('String.IsEqual(ListItem.DBType,movie)', '$LOCALIZE[20338]$INFO[ListItem.Year, · ,]'),
    ('String.IsEqual(ListItem.DBType,tvshow)', '$LOCALIZE[20364]$INFO[ListItem.Year, · ,]'),
    ('String.IsEqual(ListItem.DBType,season)', '$INFO[ListItem.TVShowTitle]'),
    ('String.IsEqual(ListItem.DBType,episode)', '$INFO[ListItem.TVShowTitle]$INFO[ListItem.Season, · S,]$INFO[ListItem.Episode,E,]'),
    ('String.IsEqual(ListItem.DBType,musicvideo)', '$LOCALIZE[20391]$INFO[ListItem.Artist, · ,]'),
    ('String.IsEqual(ListItem.DBType,artist)', '$LOCALIZE[557]'),
    ('String.IsEqual(ListItem.DBType,album)', '$LOCALIZE[558]$INFO[ListItem.Artist, · ,]'),
    ('String.IsEqual(ListItem.DBType,song)', '$LOCALIZE[179]$INFO[ListItem.Artist, · ,]'),
    ('', '$LOCALIZE[10106]')]))
# dialogs that are not about an item (exit, skin questions ...): the item shows only over a media window
HEAD.append(expression('MS_MediaUnder', 'Window.IsVisible(videos) | Window.IsVisible(music) | Window.IsVisible(movieinformation) | '
                       'Window.IsVisible(musicinformation) | Window.IsVisible(fullscreenvideo) | Window.IsVisible(home)'))
HEAD.append(variable('MS_ItemPlot', [
    ('!String.IsEmpty(ListItem.Plot)', '$INFO[ListItem.Plot]'),
    ('!String.IsEmpty(ListItem.Property(Album_Description))', '$INFO[ListItem.Property(Album_Description)]'),
    ('', '$INFO[ListItem.Property(Artist_Description)]')]))
# key / value lines about the item, in this order; empty ones drop out (the lines sit in grouplists)
HEAD.append(variable('MS_Runtime', [
    ('Integer.IsGreater(ListItem.Duration(mins),59)', '$INFO[ListItem.Duration(h)]h $INFO[ListItem.Duration(mm)]m'),
    ('', '$INFO[ListItem.Duration(mins)] min')]))
INFO = [('$LOCALIZE[345]', 'ListItem.Year'), ('$LOCALIZE[2050]', 'ListItem.Duration', '$VAR[MS_Runtime]'),
        ('$LOCALIZE[20074]', 'ListItem.MPAA'), ('$LOCALIZE[515]', 'ListItem.Genre'), ('$LOCALIZE[20339]', 'ListItem.Director'),
        ('$LOCALIZE[557]', 'ListItem.Artist'), ('$LOCALIZE[558]', 'ListItem.Album'), ('$LOCALIZE[563]', 'ListItem.Rating')]
INFO = [(e[0], e[1], e[2] if len(e) > 2 else '$INFO[%s]' % e[1]) for e in INFO]
PLOT_LINE = 36                  # body_24 line height: plot textboxes are whole lines tall (Kodi draws a part line otherwise)


def info_stacked(x, y, w, h, info=None):
    """key over value, one row each (Mosaic, Tab slab)"""
    info = info or INFO
    rows = ''.join('<control type="group"><width>%d</width><height>%d</height>%s%s%s</control>' % (
        w, R, lab(0, 8, w, 24, '[UPPERCASE]%s[/UPPERCASE]' % k, 'cap_16', W3), lab(0, 32, w, 32, d, 'ui_24', W1),
        vis('!String.IsEmpty(%s)' % v)) for k, v, d in info)
    return ('<control type="grouplist"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><itemgap>0</itemgap>'
            '<orientation>vertical</orientation><usecontrolcoords>true</usecontrolcoords>%s</control>' % (x, y, w, h, rows))


def info_inline(x, y, w, h, keyw=150, align='left', plot=False, info=None):
    """key and value on one row (Ledger, Bridge); plot: the item's text follows the lines, three lines tall"""
    info = info or INFO
    rows = ''.join('<control type="group"><width>%d</width><height>%d</height>%s%s%s</control>' % (
        w, R, lab(0, 0, keyw, R, '[UPPERCASE]%s[/UPPERCASE]' % k, 'cap_16', W3),
        lab(keyw, 0, w - keyw, R, d, 'ui_24', W1, align=align), vis('!String.IsEmpty(%s)' % v)) for k, v, d in info)
    if plot:
        rows += '<control type="group"><width>%d</width><height>%d</height>%s</control>' % (
            w, 2 * R, textbox(0, (2 * R - 3 * PLOT_LINE) // 2, w, 3 * PLOT_LINE, '$VAR[MS_ItemPlot]', 'body_24', W2))
    return ('<control type="grouplist"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><itemgap>0</itemgap>'
            '<orientation>vertical</orientation><usecontrolcoords>true</usecontrolcoords>%s</control>' % (x, y, w, h, rows))


def poster_tile(x, y, w, h, has='$EXP[MS_HasPoster]', src='$VAR[MS_Poster]', glyph='aeon/icons/lines.png', empty=BOX):
    """the item's poster, or a plain box with a glyph when there is none"""
    return (img(x, y, w, h, 'x_deep') + art(x, y, w, h, src, has) + img(x, y, w, h, empty, '![%s]' % has) +
            icon(x + (w - 56) // 2, y + (h - 56) // 2, 56, glyph, 'ccffffff', '![%s]' % has))


def fanart_band(x, y, w, h):
    return img(x, y, w, h, 'x_deep') + art(x, y, w, h, '$VAR[MS_Fanart]', '$EXP[MS_HasFanart]')


def title_box(x, y, w, color, kicker, title, kicker_color=CAP_ON_BOX, count=None, scroll=False):
    out = img(x, y, w, 2 * R, color)
    out += lab(x + 32, y + 22, w - 64 - (150 if count else 0), 30, '[UPPERCASE]%s[/UPPERCASE]' % kicker, 'cap_20', kicker_color)
    out += lab(x + 32, y + 52, w - 64, 64, title, 'font37', 'ffffffff', scroll=scroll)
    if count:
        out += lab(x + w - 32 - 150, y + 22, 150, 30, count, 'cap_20', kicker_color, align='right')
    return out


def row_button(cid, width, label='', extra='', font='ui_26', offset=32):
    return ('<control type="button" id="%d"><left>0</left><top>0</top><width>%d</width><height>%d</height><font>%s</font>'
            '<textoffsetx>%d</textoffsetx><aligny>center</aligny><textcolor>%s</textcolor><focusedcolor>aeon_onbar</focusedcolor>'
            '<disabledcolor>55ffffff</disabledcolor><texturefocus colordiffuse="aeon_white">common/white.png</texturefocus>'
            '<texturenofocus border="24,0,24,0" colordiffuse="16ffffff">aeon/ms/rowline.png</texturenofocus>'
            '%s%s</control>' % (cid, width, R, font, offset, W1, '<label>%s</label>' % label if label else '', extra))


# ---------------------------------------------------------------------------------------------------------------
# Context menu: Kodi clones button 1000 into grouplist 996; the skin's own row 990 ("View, sort, filter...") comes first.
# n = rows shown: 990 (when visible) + Kodi's buttons 1001..., up to CAP rows on screen (the grouplist scrolls beyond)
CAP = 11
KMAX = 20


def kodi_count(k):
    if k == 0:
        return '!Control.IsVisible(1001)'
    return 'Control.IsVisible(%d) + !Control.IsVisible(%d)' % (1000 + k, 1001 + k)


for n in range(1, KMAX + 1):
    HEAD.append(expression('MS_CtxN%d' % n, '[Control.IsVisible(990) + %s] | [!Control.IsVisible(990) + %s]'
                           % (kodi_count(n - 1), kodi_count(n) if n < KMAX else 'Control.IsVisible(%d)' % (1000 + n))))
for r in range(1, CAP + 1):
    if r < CAP:
        HEAD.append(expression('MS_CtxR%d' % r, '$EXP[MS_CtxN%d]' % r))
    else:
        HEAD.append(expression('MS_CtxR%d' % r, '[Control.IsVisible(990) + Control.IsVisible(%d)] | [!Control.IsVisible(990) + Control.IsVisible(%d)]'
                               % (1000 + CAP - 1, 1000 + CAP)))
# the focused item's place: row i is 990 (i = 0 when 990 shows) or Kodi's button
for i in range(KMAX):
    first = 'Control.HasFocus(990)' if i == 0 else 'Control.HasFocus(%d)' % (1000 + i)
    HEAD.append(expression('MS_CtxF%d' % i, '[Control.IsVisible(990) + %s] | [!Control.IsVisible(990) + Control.HasFocus(%d)]' % (first, 1001 + i)))
HEAD.append(variable('MS_CtxPos', [('$EXP[MS_CtxN%d] + $EXP[MS_CtxF%d]' % (n, i), '%d / %d' % (i + 1, n))
                                   for n in range(1, KMAX + 1) for i in range(n)]))
MIN_ROWS = 4                    # the art and info boxes need four rows; shorter menus keep the empty rows


def m_cond(m):
    """box rows m = max(rows, MIN_ROWS)"""
    if m == MIN_ROWS:
        return ' | '.join('$EXP[MS_CtxR%d]' % r for r in range(1, MIN_ROWS + 1))
    return '$EXP[MS_CtxR%d]' % m


def per_m(fn):
    """one copy of a box for each height"""
    return ''.join(fn(m, m_cond(m)) for m in range(MIN_ROWS, CAP + 1))


def centring(base_rows=2 + MIN_ROWS):
    """the menu group starts centred on base_rows rows (title + MIN_ROWS rows by default) and lifts half a row for each
    row the menu (title + its rows) grows past that"""
    return ''.join('<animation effect="slide" end="0,%d" time="0" condition="%s">Conditional</animation>'
                   % (-(2 + m - base_rows) * R // 2, esc(m_cond(m))) for m in range(MIN_ROWS + 1, CAP + 1)
                   if 2 + m > base_rows)


def ctx_grouplist(x, y, width):
    return ('<control type="grouplist" id="996"><description>context buttons (Kodi clones 1000 here)</description>'
            '<left>%d</left><top>%d</top><width>%d</width><height max="%d">auto</height><itemgap>0</itemgap>'
            '<usecontrolcoords>true</usecontrolcoords><orientation>vertical</orientation>%s</control>'
            % (x, y, width, CAP * R, row_button(990, width, '$LOCALIZE[31342]',
                                                 '<onclick>Dialog.Close(contextmenu)</onclick>'
                                                 '<onclick>AlarmClock(aeonopen,ActivateWindow(1160),00:00,silent)</onclick>'
                                                 '<visible>$EXP[Ctx_ViewRowVis]</visible>')))


def ctx_frame(content_w, content_h_rows, inner, width, centre_rows=2 + MIN_ROWS):
    """dim, the centred group, Kodi's hidden background 999 and the template 1000; centre_rows: see centring()"""
    h0 = content_h_rows * R
    top = (1080 - h0) // 2
    left = (1920 - content_w) // 2
    dim = ('<control type="image"><left>-1920</left><top>-1080</top><width>5760</width><height>3240</height>'
           '<animation effect="fade" start="0" end="100" time="200">WindowOpen</animation>'
           '<animation effect="fade" start="100" end="0" time="150">WindowClose</animation>'
           '<texture colordiffuse="c8000000">common/white.png</texture></control>')
    bg999 = ('<control type="image" id="999"><description>Kodi sizes it; the look is drawn by the boxes</description>'
             '<left>0</left><top>0</top><width>%d</width><height>%d</height><texture>common/white.png</texture>'
             '<visible>false</visible></control>' % (content_w, h0))
    tmpl = row_button(1000, width)
    return dim + '<control type="group"><left>%d</left><top>%d</top>%s\n%s\n%s\n</control>\n%s' % (
        left, top, centring(centre_rows), bg999, inner, tmpl)


def ctx_mosaic():
    LW, IW = 780, 560
    o = title_box(0, 0, LW, BOX, '$VAR[MS_ItemKicker]', '$VAR[MS_ItemTitle]', count='$VAR[MS_CtxPos]')
    o += fanart_band(LW, 0, IW, 2 * R)
    o += per_m(lambda m, c: img(0, 2 * R, LW, m * R, 'x_panel', c) + img(LW, 2 * R, IW, m * R, 'x_raised', c))
    o += poster_tile(LW, 2 * R, 192, 4 * R)
    o += info_stacked(LW + 220, 2 * R, IW - 248, 4 * R)
    o += per_m(lambda m, c: textbox(LW + 32, 6 * R + 16, IW - 64, ((m - 4) * R - 32) // PLOT_LINE * PLOT_LINE, '$VAR[MS_ItemPlot]', 'body_24', W2, c)
               if m > 4 else '')
    o += ctx_grouplist(0, 2 * R, LW)
    return ctx_frame(LW + IW, 2 + MIN_ROWS, o, LW)


def ctx_ledger():
    SP, LW, VW = 96, 600, 420
    W = SP + LW + VW
    o = img(0, 0, SP, 2 * R, 'x_deep') + art(0, 0, SP, 2 * R, '$VAR[MS_Poster]', '$EXP[MS_HasPoster]')
    o += img(0, 0, SP, 2 * R, BOX, '!$EXP[MS_HasPoster]')
    o += title_box(SP, 0, LW + VW, 'x_deep', '$VAR[MS_ItemKicker]', '$VAR[MS_ItemTitle]', kicker_color=W3, count='$VAR[MS_CtxPos]')
    o += per_m(lambda m, c: img(0, 2 * R, SP, m * R, BOX, c) + img(SP, 2 * R, LW, m * R, 'x_panel', c) +
               img(SP + LW, 2 * R, VW, m * R, 'x_raised', c) + img(0, (2 + m) * R, W, R, 'x_deep', c) +
               lab(SP + 32, (2 + m) * R, W - SP - 64, R, '$VAR[MS_ItemPlot]', 'ui_22', W2, cond=c, scroll=True))
    # the spine: row numbers, and the focus bar reaching through it
    for i in range(CAP):
        y = (2 + i) * R
        o += img(0, y, SP, R, 'aeon_white', '$EXP[MS_CtxF%d]' % i)
        num = '[CAPITALIZE]%02d[/CAPITALIZE]' % (i + 1)
        shows = '[%s]' % ' | '.join('$EXP[MS_CtxN%d]' % n for n in range(i + 1, KMAX + 1))
        o += lab(0, y, SP, R, num, 'num_22', 'ffffffff', align='center', cond=shows + ' + !$EXP[MS_CtxF%d]' % i)
        o += lab(0, y, SP, R, num, 'num_22', 'aeon_onbar', align='center', cond='$EXP[MS_CtxF%d]' % i)
    # the values column: the item's facts on the menu's rows
    o += per_m(lambda m, c: info_inline(SP + LW + 24, 2 * R, VW - 48, m * R, keyw=140, align='right').replace(
        '<orientation>', vis(c) + '<orientation>', 1))
    o += ctx_grouplist(SP, 2 * R, LW)
    return ctx_frame(W, 3 + MIN_ROWS, o, LW)


CTX_INFO_ROWS = 8               # Bridge info box: up to six facts plus the two-row plot (a film: year, runtime, rating,
                                # genre, director, score); it reaches below a shorter menu instead of cutting the plot


def ctx_bridge():
    TW, PW, LW, IW = 640, 192, 720, 460
    o = title_box(0, 0, TW, BOX, '$VAR[MS_ItemKicker]', '$VAR[MS_ItemTitle]')
    o += img(0, 2 * R, PW, 4 * R, 'x_deep') + art(0, 2 * R, PW, 4 * R, '$VAR[MS_Poster]', '$EXP[MS_HasPoster]')
    o += img(0, 2 * R, PW, 4 * R, 'x_raised', '!$EXP[MS_HasPoster]')
    o += icon((PW - 56) // 2, 4 * R - 28, 56, 'aeon/icons/lines.png', W2, '!$EXP[MS_HasPoster]')
    ix = PW + LW
    ih = lambda m: max(m - 1, CTX_INFO_ROWS)  # noqa: E731  info box rows for a menu of m rows
    o += per_m(lambda m, c: img(PW, 2 * R, LW, m * R, 'x_panel', c) + img(ix, 3 * R, IW, ih(m) * R, 'x_raised', c))
    # the step: the count on the first row, the info box one row lower
    o += img(ix, 2 * R, 240, R, 'x_deep') + lab(ix + 28, 2 * R, 200, R, '$VAR[MS_CtxPos]', 'num_22', W2)
    # the focused row carried across the info box as a quiet band
    for i in range(1, CAP):
        o += img(ix, (2 + i) * R, IW, R, '28ffffff', '$EXP[MS_CtxF%d] + ![%s]' % (i, ' | '.join('$EXP[MS_CtxN%d]' % n for n in range(CAP + 1, KMAX + 1))))
    o += per_m(lambda m, c: info_inline(ix + 28, 3 * R, IW - 56, ih(m) * R, keyw=152, plot=True).replace('<orientation>', vis(c) + '<orientation>', 1))
    o += ctx_grouplist(PW, 2 * R, LW)
    # centred on the whole height (title, step row, info box); longer menus lift as before
    return ctx_frame(PW + LW + IW, 3 + CTX_INFO_ROWS, o, LW, centre_rows=3 + CTX_INFO_ROWS)


def ctx_tabslab():
    SW, AW, TAB = 820, 400, 260
    o = img(0, 0, TAB, R, BOX) + lab(0, 0, TAB, R, '[UPPERCASE]$VAR[MS_ItemKicker][/UPPERCASE]', 'cap_20', 'ffffffff', align='center')
    o += img(TAB, 0, SW - TAB, R, 'x_deep') + lab(TAB + 24, 0, SW - TAB - 48, R, '$VAR[MS_CtxPos]', 'num_22', W3, align='right')
    o += img(0, R, SW, R, BOX) + lab(32, R, SW - 64, R, '$VAR[MS_ItemTitle]', 'ui_30_semibold', 'ffffffff')
    o += fanart_band(SW, 0, AW, 3 * R)
    o += per_m(lambda m, c: img(0, 2 * R, SW, m * R, 'x_panel', c) + img(SW, 3 * R, AW, (m - 1) * R, 'x_raised', c) +
               img(0, (2 + m) * R, SW + AW, R, 'x_deep', c) +
               lab(32, (2 + m) * R, SW + AW - 64, R, '$VAR[MS_ItemPlot]', 'ui_22', W2, cond=c, scroll=True))
    o += poster_tile(SW + AW - 168, 3 * R, 168, 252)
    o += info_stacked(SW + 28, 3 * R, AW - 168 - 52, 3 * R)
    o += ctx_grouplist(0, 2 * R, SW)
    return ctx_frame(SW + AW, 3 + MIN_ROWS, o, SW)


# ---------------------------------------------------------------------------------------------------------------
# shared by the dialogs below
DIM = ('<control type="image"><left>-1920</left><top>-1080</top><width>5760</width><height>3240</height>'
       '<animation effect="fade" start="0" end="100" time="200">WindowOpen</animation>'
       '<animation effect="fade" start="100" end="0" time="150">WindowClose</animation>'
       '<texture colordiffuse="c8000000">common/white.png</texture></control>')


def heading(x, y, w, h=64, font='font37', cid=1):
    """Kodi writes the dialog's heading into this label"""
    return ('<control type="label" id="%d"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><aligny>center</aligny>'
            '<font>%s</font><textcolor>ffffffff</textcolor></control>' % (cid, x, y, w, h, font))


def cell_button(cid, w, label='', extra=''):
    """a flush square button cell: raised panel colour, the focus bar colour when focused"""
    return ('<control type="button" id="%d"><width>%d</width><height>%d</height><font>ui_26_semibold</font><align>center</align>'
            '<aligny>center</aligny><textcolor>%s</textcolor><focusedcolor>aeon_onbar</focusedcolor><disabledcolor>55ffffff</disabledcolor>'
            '<texturefocus colordiffuse="aeon_white">common/white.png</texturefocus>'
            '<texturenofocus colordiffuse="x_raised">common/white.png</texturenofocus>%s%s</control>'
            % (cid, w, R, W1, '<label>%s</label>' % label if label else '', extra))


def cell_row(gid, x, y, w, ids, cw, nav, labels=None):
    """a horizontal grouplist of button cells, right-aligned in a deep row"""
    labels = labels or {}
    return (img(x, y, w, R, 'x_deep') +
            '<control type="grouplist" id="%d"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><itemgap>0</itemgap>'
            '<orientation>horizontal</orientation><align>right</align><usecontrolcoords>true</usecontrolcoords>%s%s</control>'
            % (gid, x, y, w, R, nav, ''.join(cell_button(i, cw, labels.get(i, '')) for i in ids)))


# ---------------------------------------------------------------------------------------------------------------
# Yes / No, OK and progress (DialogConfirm): heading 1, text 9, progress 20, buttons 11 / 10 / 12 in grouplist 9000.
# Kodi hides the unused buttons and focuses its own default one. The item shows only over a media window.
HEAD.append(expression('MS_DlgHasPoster', '$EXP[MS_MediaUnder] + $EXP[MS_HasPoster]'))
HEAD.append(expression('MS_DlgHasFanart', '$EXP[MS_MediaUnder] + $EXP[MS_HasFanart]'))
HEAD.append(variable('MS_DlgKicker', [('$EXP[MS_MediaUnder] + !String.IsEmpty(ListItem.Label)', '$VAR[MS_ItemTitle]'), ('', 'Kodi')]))
CONF_NAV = '<onleft>9000</onleft><onright>9000</onright><onup>noop</onup><ondown>noop</ondown>'


def conf_message(x, y, w):
    """the message box body: Kodi's text (four whole lines) and its progress bar"""
    return (textbox(x + 36, y + 22, w - 72, 4 * PLOT_LINE, '', 'body_24', W1, cid=9) +
            '<control type="progress" id="20"><left>%d</left><top>%d</top><width>%d</width><height>6</height>'
            '<texturebg colordiffuse="22ffffff">common/white.png</texturebg><midtexture colordiffuse="aeon_white">common/white.png</midtexture>'
            '<info>System.Progressbar</info></control>' % (x + 36, y + 3 * R - 26, w - 72))


def conf_wrap(w, h, inner):
    return DIM + '<control type="group"><left>%d</left><top>%d</top>\n%s\n</control>' % ((1920 - w) // 2, (1080 - h) // 2, inner)


def confirm_mosaic():
    LW, IW = 760, 480
    o = img(0, 0, LW, 2 * R, BOX) + lab(32, 22, LW - 64, 30, '[UPPERCASE]$VAR[MS_DlgKicker][/UPPERCASE]', 'cap_20', CAP_ON_BOX)
    o += heading(32, 52, LW - 64)
    o += img(LW, 0, IW, 2 * R, 'x_deep') + art(LW, 0, IW, 2 * R, '$VAR[MS_Fanart]', '$EXP[MS_DlgHasFanart]')
    o += img(0, 2 * R, LW, 3 * R, 'x_panel') + conf_message(0, 2 * R, LW)
    o += cell_row(9000, 0, 5 * R, LW, (11, 10, 12), LW // 2, CONF_NAV)
    o += poster_tile(LW, 2 * R, 192, 4 * R, has='$EXP[MS_DlgHasPoster]', glyph='aeon/icons/info.png')
    o += img(LW + 192, 2 * R, IW - 192, 4 * R, 'x_raised')
    o += info_stacked(LW + 220, 2 * R, IW - 248, 4 * R).replace('<orientation>', vis('$EXP[MS_MediaUnder]') + '<orientation>', 1)
    return conf_wrap(LW + IW, 6 * R, o)


def confirm_ledger():
    SP, W = 96, 960
    o = poster_tile(0, 0, SP, 2 * R, has='$EXP[MS_DlgHasPoster]', glyph='aeon/icons/info.png')
    o += img(SP, 0, W, 2 * R, 'x_deep') + lab(SP + 32, 22, W - 64, 30, '[UPPERCASE]$VAR[MS_DlgKicker][/UPPERCASE]', 'cap_20', W3)
    o += heading(SP + 32, 52, W - 64)
    o += img(0, 2 * R, SP, 4 * R, BOX) + icon(20, 2 * R + 8, 56, 'aeon/icons/info.png', 'ffffffff')
    o += img(SP, 2 * R, W, 3 * R, 'x_panel') + conf_message(SP, 2 * R, W)
    o += cell_row(9000, SP, 5 * R, W, (11, 10, 12), W // 2, CONF_NAV)
    return conf_wrap(SP + W, 6 * R, o)


def confirm_bridge():
    TW, PW, MW, BW = 640, 192, 760, 520
    o = img(0, 0, TW, 2 * R, BOX) + lab(32, 22, TW - 64, 30, '[UPPERCASE]$VAR[MS_DlgKicker][/UPPERCASE]', 'cap_20', CAP_ON_BOX)
    o += heading(32, 52, TW - 64)
    o += poster_tile(0, 2 * R, PW, 4 * R, has='$EXP[MS_DlgHasPoster]', glyph='aeon/icons/info.png', empty='x_raised')
    o += img(PW, 2 * R, MW, 3 * R, 'x_panel') + conf_message(PW, 2 * R, MW)
    # the buttons step down one row and out past the message: the first button's right edge sits on the message box's
    # right edge (its top-right corner meets the box's bottom-right corner); a lone OK / Cancel ends flush with the box.
    # The grouplist has room for Kodi's third (custom) button.
    bc = BW // 2
    bx = PW + MW - bc
    o += ('<control type="grouplist" id="9000"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><itemgap>0</itemgap>'
          '<orientation>horizontal</orientation><usecontrolcoords>true</usecontrolcoords>%s%s</control>'
          % (bx, 5 * R, 3 * bc, R, CONF_NAV, ''.join(cell_button(i, bc) for i in (11, 10, 12))))
    return conf_wrap(PW + MW + bc, 6 * R, o)


def confirm_tabslab():
    SW, AW, TAB = 820, 400, 260
    o = img(0, 0, TAB, R, BOX) + lab(16, 0, TAB - 32, R, '[UPPERCASE]$VAR[MS_DlgKicker][/UPPERCASE]', 'cap_20', 'ffffffff', align='center')
    o += img(TAB, 0, SW - TAB, R, 'x_deep')
    o += img(0, R, SW, R, BOX) + heading(32, R, SW - 64, R, 'ui_30_semibold')
    o += img(0, 2 * R, SW, 3 * R, 'x_panel') + conf_message(0, 2 * R, SW)
    o += cell_row(9000, 0, 5 * R, SW, (11, 10, 12), SW // 2, CONF_NAV)
    o += img(SW, 0, AW, 3 * R, 'x_deep') + art(SW, 0, AW, 3 * R, '$VAR[MS_Fanart]', '$EXP[MS_DlgHasFanart]')
    o += img(SW, 3 * R, AW, 3 * R, 'x_raised')
    o += poster_tile(SW + AW - 144, 3 * R, 144, 3 * R, has='$EXP[MS_DlgHasPoster]', glyph='aeon/icons/info.png')
    o += info_stacked(SW + 28, 3 * R, AW - 144 - 52, 3 * R).replace('<orientation>', vis('$EXP[MS_MediaUnder]') + '<orientation>', 1)
    return conf_wrap(SW + AW, 6 * R, o)


# ---------------------------------------------------------------------------------------------------------------
# Select (DialogSelect): heading 1, list 3 (simple) / 6 (detailed), scrollbar 61, buttons 5 / 8 / 7 in grouplist 9001.
# Up to SCAP rows show (the list scrolls beyond). Right / Left from the list go to the buttons in the row under it.
SCAP = 9
HEAD.append(expression('MS_SelPlain', 'String.IsEmpty(Window(Home).Property(aeon.palpick)) + String.IsEmpty(Window(Home).Property(aeon.iconpick))'))


def sel_count(n, op='IsEqual'):
    return '[Control.IsVisible(3) + Integer.%s(Container(3).NumItems,%d)] | [Control.IsVisible(6) + Integer.%s(Container(6).NumItems,%d)]' % (op, n, op, n)


for n in range(0, SCAP):
    HEAD.append(expression('MS_SelN%d' % n, sel_count(n)))
HEAD.append(expression('MS_SelN%d' % SCAP, sel_count(SCAP - 1, 'IsGreater')))
for i in range(SCAP):
    HEAD.append(expression('MS_SelF%d' % i, '[Control.HasFocus(3) + Integer.IsEqual(Container(3).Position,%d)] | '
                                            '[Control.HasFocus(6) + Integer.IsEqual(Container(6).Position,%d)]' % (i, i)))
HEAD.append(variable('MS_SelPos', [('Control.IsVisible(6)', '$INFO[Container(6).CurrentItem]$INFO[Container(6).NumItems, / ,]'),
                                   ('', '$INFO[Container(3).CurrentItem]$INFO[Container(3).NumItems, / ,]')]))
# the focused row's own picture (art chooser, versions ...) first, else the item the dialog is about
HEAD.append(expression('MS_SelHasArt', '[Control.IsVisible(6) + [!String.IsEmpty(Container(6).ListItem.Art(thumb)) | '
                       '!String.IsEmpty(Container(6).ListItem.Art(poster))]] | $EXP[MS_DlgHasPoster]'))
HEAD.append(variable('MS_SelArt', [
    ('Control.IsVisible(6) + !String.IsEmpty(Container(6).ListItem.Art(poster))', '$INFO[Container(6).ListItem.Art(poster)]'),
    ('Control.IsVisible(6) + !String.IsEmpty(Container(6).ListItem.Art(thumb))', '$INFO[Container(6).ListItem.Art(thumb)]'),
    ('', '$VAR[MS_Poster]')]))
HEAD.append(variable('MS_SelLabel', [('Control.IsVisible(6)', '$INFO[Container(6).ListItem.Label]'), ('', '$INFO[Container(3).ListItem.Label]')]))
HEAD.append(variable('MS_SelLabel2', [('Control.IsVisible(6)', '$INFO[Container(6).ListItem.Label2]'), ('', '$INFO[Container(3).ListItem.Label2]')]))


def sm_cond(m):
    if m == MIN_ROWS:
        return ' | '.join('$EXP[MS_SelN%d]' % n for n in range(0, MIN_ROWS + 1))
    return '$EXP[MS_SelN%d]' % m


def sel_per_m(fn):
    return ''.join(fn(m, sm_cond(m)) for m in range(MIN_ROWS, SCAP + 1))


def sel_centring():
    return ''.join('<animation effect="slide" end="0,%d" time="0" condition="%s">Conditional</animation>'
                   % (-(m - MIN_ROWS) * R // 2, esc(sm_cond(m))) for m in range(MIN_ROWS + 1, SCAP + 1))


def sel_row(cid, w, focused, spine=0, value_w=0):
    """one list row: label, label2 at the right, a check when selected; detailed rows (list 6) lead with the icon.
    spine: a numbered aeon_box cell at the left (Ledger); value_w: Label2 sits in its own column (Ledger)"""
    fc = 'Control.HasFocus(%d)' % cid
    ink_on = 'aeon_onbar'
    out = []
    if spine:
        out.append(img(0, 0, spine, R, BOX))
    if focused:
        out.append(img(0, 0, w, R, 'aeon_white', fc))
    if not spine:
        out.append('<control type="image"><left>0</left><top>0</top><width>%d</width><height>%d</height>'
                   '<texture border="24,0,24,0" colordiffuse="16ffffff">aeon/ms/rowline.png</texture>%s</control>'
                   % (w, R, vis('!' + fc) if focused else ''))
    if spine:
        out.append(lab(0, 0, spine, R, '$INFO[ListItem.CurrentItem]', 'num_22', 'ffffffff', align='center', cond='!' + fc if focused else None))
        if focused:
            out.append(lab(0, 0, spine, R, '$INFO[ListItem.CurrentItem]', 'num_22', ink_on, align='center', cond=fc))
    x = spine + (24 if cid == 6 else 32)
    if cid == 6:
        # the skin's and Kodi's own icons are white glyphs: they take the bar's ink on the focused row; real pictures keep their colours
        glyph = 'String.Contains(ListItem.Icon,Default) | String.Contains(ListItem.Icon,aeon_mi_) | String.Contains(ListItem.Icon,/icons/)'
        plain = '<control type="image"><left>%d</left><top>12</top><width>48</width><height>48</height><aspectratio>keep</aspectratio>' % x
        if focused:
            out.append(plain + '<texture background="true">$INFO[ListItem.Icon]</texture>%s</control>' % vis('!%s | ![%s]' % (fc, glyph)))
            out.append(plain + '<texture background="true" colordiffuse="aeon_onbar">$INFO[ListItem.Icon]</texture>%s</control>' % vis('%s + [%s]' % (fc, glyph)))
        else:
            out.append(plain + '<texture background="true">$INFO[ListItem.Icon]</texture></control>')
        x += 64
    right = w - 28
    label_w = (w - value_w - x - 24) if value_w else (right - x - 200)
    out.append(lab(x, 0, label_w, R, '$INFO[ListItem.Label]', 'ui_26', W1, cond='!' + fc if focused else None))
    if focused:
        out.append(lab(x, 0, label_w, R, '$INFO[ListItem.Label]', 'ui_26_semibold', ink_on, cond=fc, scroll=True))
    # check for the selected ones, Label2 left of it
    out.append(icon(right - 28, 22, 28, 'markers/check.png', 'aeon_white', 'ListItem.IsSelected' + (' + !' + fc if focused else '')))
    if focused:
        out.append(icon(right - 28, 22, 28, 'markers/check.png', ink_on, 'ListItem.IsSelected + ' + fc))
    l2x = (w - value_w + 24) if value_w else (right - 240)
    l2w = (value_w - 24 - 72) if value_w else 200
    out.append(lab(l2x, 0, l2w, R, '$INFO[ListItem.Label2]', 'ui_22', W2, align='right', cond='!' + fc if focused else None))
    if focused:
        out.append(lab(l2x, 0, l2w, R, '$INFO[ListItem.Label2]', 'ui_22', ink_on, align='right', cond=fc))
    return ''.join(out)


def sel_lists(x, y, w, spine=0, value_w=0):
    out = ''
    for cid in (3, 6):
        out += ('<control type="list" id="%d"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
                '<onup>%d</onup><ondown>%d</ondown><onleft>9001</onleft><onright>9001</onright><pagecontrol>61</pagecontrol>'
                '<scrolltime tween="cubic" easing="out">200</scrolltime>'
                '<itemlayout width="%d" height="%d">%s</itemlayout><focusedlayout width="%d" height="%d">%s</focusedlayout></control>'
                % (cid, x, y, w, SCAP * R, cid, cid, w, R, sel_row(cid, w, False, spine, value_w), w, R, sel_row(cid, w, True, spine, value_w)))
    out += ('<control type="scrollbar" id="61"><left>%d</left><top>%d</top><width>4</width><height>%d</height>'
            '<texturesliderbackground colordiffuse="10ffffff">common/white.png</texturesliderbackground>'
            '<texturesliderbar colordiffuse="44ffffff">common/white.png</texturesliderbar>'
            '<texturesliderbarfocus colordiffuse="aeon_white">common/white.png</texturesliderbarfocus>'
            '<orientation>vertical</orientation><showonepage>false</showonepage><onleft>3</onleft><onright>9001</onright>'
            '<visible>Control.IsVisible(3) | Control.IsVisible(6)</visible></control>' % (x + w - 4, y, SCAP * R))
    # nothing to pick (Kodi then focuses the buttons)
    out += lab(x + 32, y, w - 64, R, '$LOCALIZE[31226]', 'ui_24', W3, cond='$EXP[MS_SelN0]')
    return out


SEL_NAV = ('<onup condition="Control.IsVisible(3)">3</onup><onup condition="Control.IsVisible(6)">6</onup>'
           '<ondown condition="Control.IsVisible(3)">3</ondown><ondown condition="Control.IsVisible(6)">6</ondown>')


TRACK = [False]          # True while the track-panel variant (select over the playing video) is generated


def sel_wrap(w, base_rows, inner):
    h0 = base_rows * R
    return (DIM.replace('c8000000', '55000000') if TRACK[0] else DIM) + '<control type="group"><left>%d</left><top>%d</top>%s\n%s\n</control>' % ((1920 - w) // 2, (1080 - h0) // 2, sel_centring(), inner)


def sel_focus_text(x, y, w, h):
    """what the focused row says, for the info boxes: its label (two lines) over its second label"""
    return (textbox(x, y, w, 2 * PLOT_LINE, '$VAR[MS_SelLabel]', 'body_24', W1) +
            textbox(x, y + 2 * PLOT_LINE + 8, w, max(PLOT_LINE, (h - 2 * PLOT_LINE - 8) // PLOT_LINE * PLOT_LINE), '$VAR[MS_SelLabel2]', 'body_24', W2))


def select_mosaic():
    LW, IW = 780, 480
    o = img(0, 0, LW, 2 * R, BOX) + lab(32, 22, LW - 214, 30, '[UPPERCASE]$VAR[MS_DlgKicker][/UPPERCASE]', 'cap_20', CAP_ON_BOX)
    o += lab(LW - 182, 22, 150, 30, '$VAR[MS_SelPos]', 'cap_20', CAP_ON_BOX, align='right') + heading(32, 52, LW - 64)
    o += img(LW, 0, IW, 2 * R, 'x_deep') + art(LW, 0, IW, 2 * R, '$VAR[MS_Fanart]', '$EXP[MS_DlgHasFanart]')
    o += sel_per_m(lambda m, c: img(0, 2 * R, LW, m * R, 'x_panel', c) + img(LW, 2 * R, IW, m * R, 'x_raised', c))
    o += poster_tile(LW, 2 * R, 192, 4 * R, has='$EXP[MS_SelHasArt]', src='$VAR[MS_SelArt]')
    o += sel_focus_text(LW + 220, 2 * R + 12, IW - 248, 4 * R - 24)
    o += sel_lists(0, 2 * R, LW)
    o += sel_footer(0, LW + IW)
    return sel_wrap(LW + IW, 3 + MIN_ROWS, o)


def sel_footer(x, w, cw=240):
    """the buttons row moves with the list's height: one grouplist per height, only one shows; cw: button width"""
    out = ''
    for m in range(MIN_ROWS, SCAP + 1):
        c = sm_cond(m)
        out += group(x, (2 + m) * R, img(0, 0, w, R, 'x_deep'), c)
    # one grouplist (ids are unique): it slides with the list height
    slides = ''.join('<animation effect="slide" end="0,%d" time="0" condition="%s">Conditional</animation>'
                     % ((m - MIN_ROWS) * R, esc(sm_cond(m))) for m in range(MIN_ROWS + 1, SCAP + 1))
    out += ('<control type="group"><left>%d</left><top>%d</top>%s'
            '<control type="grouplist" id="9001"><left>0</left><top>0</top><width>%d</width><height>%d</height><itemgap>0</itemgap>'
            '<orientation>horizontal</orientation><align>right</align><usecontrolcoords>true</usecontrolcoords>%s%s</control></control>'
            % (x, (2 + MIN_ROWS) * R, slides, w, R, SEL_NAV, sel_buttons(cw)))
    return out


def sel_buttons(cw=240):
    if not TRACK[0]:
        return ''.join(cell_button(i, cw, {7: '$LOCALIZE[222]'}.get(i, '')) for i in (5, 8, 7))
    # over the video, from the subtitle settings: Download subtitles / Subtitle settings instead of Cancel
    sub = '<visible>$EXP[Dlg_FromSubtitleSettings]</visible>'
    return (cell_button(9101, 300, '$LOCALIZE[31510]', '<onclick>Dialog.Close(selectdialog)</onclick><onclick>ActivateWindow(SubtitleSearch)</onclick>' + sub) +
            cell_button(9102, 300, '$LOCALIZE[31511]', '<onclick>Dialog.Close(selectdialog)</onclick>' + sub) +
            cell_button(5, cw) + cell_button(8, cw) +
            cell_button(7, cw, '$LOCALIZE[222]', '<visible>!$EXP[Dlg_FromSubtitleSettings]</visible>'))


def select_ledger():
    SP, LW, VW = 96, 600, 420
    W = SP + LW + VW
    o = poster_tile(0, 0, SP, 2 * R, has='$EXP[MS_SelHasArt]', src='$VAR[MS_SelArt]')
    o += img(SP, 0, LW + VW, 2 * R, 'x_deep') + lab(SP + 32, 22, LW + VW - 214, 30, '[UPPERCASE]$VAR[MS_DlgKicker][/UPPERCASE]', 'cap_20', W3)
    o += lab(W - 182, 22, 150, 30, '$VAR[MS_SelPos]', 'cap_20', W3, align='right') + heading(SP + 32, 52, LW + VW - 64)
    # the columns under the rows, then the rows (each row carries its own spine cell and value column)
    o += sel_per_m(lambda m, c: img(0, 2 * R, SP, m * R, BOX, c) + img(SP, 2 * R, LW, m * R, 'x_panel', c) +
                   img(SP + LW, 2 * R, VW, m * R, 'x_raised', c))
    o += sel_lists(0, 2 * R, W, spine=SP, value_w=VW)
    o += sel_footer(0, W)
    return sel_wrap(W, 3 + MIN_ROWS, o)


def select_bridge():
    TW, PW, LW, IW = 640, 192, 720, 460
    o = img(0, 0, TW, 2 * R, BOX) + lab(32, 22, TW - 64, 30, '[UPPERCASE]$VAR[MS_DlgKicker][/UPPERCASE]', 'cap_20', CAP_ON_BOX)
    o += heading(32, 52, TW - 64)
    o += poster_tile(0, 2 * R, PW, 4 * R, has='$EXP[MS_SelHasArt]', src='$VAR[MS_SelArt]', empty='x_raised')
    ix = PW + LW
    o += sel_per_m(lambda m, c: img(PW, 2 * R, LW, m * R, 'x_panel', c) + img(ix, 3 * R, IW, (m - 1) * R, 'x_raised', c))
    o += img(ix, 2 * R, 240, R, 'x_deep') + lab(ix + 28, 2 * R, 200, R, '$VAR[MS_SelPos]', 'num_22', W2)
    for i in range(1, SCAP):
        o += img(ix, (2 + i) * R, IW, R, '28ffffff', '$EXP[MS_SelF%d]' % i)
    o += sel_focus_text(ix + 28, 3 * R + 12, IW - 56, 3 * R - 24)
    o += sel_lists(PW, 2 * R, LW)
    # buttons half the info column wide: OK + Cancel fill it exactly, flush with the list box on the left
    o += sel_footer(PW, LW + IW, cw=IW // 2)
    return sel_wrap(PW + LW + IW, 3 + MIN_ROWS, o)


def select_tabslab():
    SW, AW, TAB = 820, 400, 260
    o = img(0, 0, TAB, R, BOX) + lab(16, 0, TAB - 32, R, '[UPPERCASE]$VAR[MS_DlgKicker][/UPPERCASE]', 'cap_20', 'ffffffff', align='center')
    o += img(TAB, 0, SW - TAB, R, 'x_deep') + lab(TAB + 24, 0, SW - TAB - 48, R, '$VAR[MS_SelPos]', 'num_22', W3, align='right')
    o += img(0, R, SW, R, BOX) + heading(32, R, SW - 64, R, 'ui_30_semibold')
    o += img(SW, 0, AW, 3 * R, 'x_deep') + art(SW, 0, AW, 3 * R, '$VAR[MS_Fanart]', '$EXP[MS_DlgHasFanart]')
    o += sel_per_m(lambda m, c: img(0, 2 * R, SW, m * R, 'x_panel', c) + img(SW, 3 * R, AW, (m - 1) * R, 'x_raised', c))
    o += poster_tile(SW + AW - 168, 3 * R, 168, 252, has='$EXP[MS_SelHasArt]', src='$VAR[MS_SelArt]')
    o += sel_focus_text(SW + 28, 3 * R + 12, AW - 168 - 52, 3 * R - 24)
    o += sel_lists(0, 2 * R, SW)
    o += sel_footer(0, SW + AW)
    return sel_wrap(SW + AW, 3 + MIN_ROWS, o)


# ---------------------------------------------------------------------------------------------------------------
# Kodi's settings pages (SettingsCategory) and add-on settings (DialogAddonSettings): section label 2, categories
# grouplist 3 (Kodi clones button 10 into it, ids from -200), control area grouplist 5 (templates 7-15), description 6,
# level button 20, scrollbar 60; add-on settings add buttons 28 / 29 / 30 in grouplist 9000.
# The window keeps its background, header caption and clock box; the styles draw the boxes.
SY0 = 112                 # first row of the boxes (the caption sits above)
CATS = 10                 # category rows before the level cell
HEAD.append(variable('MS_OpenCat', [('', '$INFO[Window.Property(ms.cat)]')]))
HEAD.append(variable('MS_CatPos', [('ControlGroup(3).HasFocus(%d)' % (-200 + i), '%d$INFO[Container(3).NumItems, / ,]' % (i + 1)) for i in range(20)]))
# the section's own glyph on the joining tile (Kodi settings), the add-on's icon (add-on settings)
HEAD.append(variable('MS_SetIcon', [
    ('Window.IsActive(playersettings)', 'aeon/icons/play.png'), ('Window.IsActive(mediasettings)', 'aeon/icons/film.png'),
    ('Window.IsActive(interfacesettings)', 'aeon/icons/sparkle.png'), ('Window.IsActive(servicesettings)', 'aeon/icons/cloud.png'),
    ('Window.IsActive(pvrsettings)', 'aeon/icons/tv.png'), ('Window.IsActive(gamesettings)', 'aeon/icons/grid.png'),
    ('', 'aeon/icons/settings.png')]))
HEAD.append(expression('MS_HasAddonIcon', '!String.IsEmpty(ListItem.Icon) + [Window.IsVisible(addonbrowser) | Window.IsVisible(addoninformation)]'))


def set_row(cid, ctype, w, extra=''):
    return ('<control type="%s" id="%d"><width>%d</width><height>%d</height><font>ui_24</font><textcolor>%s</textcolor>'
            '<focusedcolor>aeon_onbar</focusedcolor><disabledcolor>44ffffff</disabledcolor><invalidcolor>ffe5484d</invalidcolor>'
            '<selectedcolor>%s</selectedcolor><textoffsetx>32</textoffsetx><aligny>center</aligny><pulseonselect>false</pulseonselect>'
            '<texturefocus colordiffuse="aeon_white">common/white.png</texturefocus>'
            '<texturenofocus border="24,0,24,0" colordiffuse="16ffffff">aeon/ms/rowline.png</texturenofocus>%s</control>'
            % (ctype, cid, w, R, W1, W1, extra))


def set_templates(w):
    radio = ('<radiowidth>56</radiowidth><radioheight>32</radioheight><radioposx>%d</radioposx>'
             '<textureradioonfocus colordiffuse="aeon_onbar">aeon/ms/radio_on.png</textureradioonfocus>'
             '<textureradioonnofocus colordiffuse="$VAR[Aeon_BoxAccent]">aeon/ms/radio_on.png</textureradioonnofocus>'
             '<textureradiooffocus colordiffuse="aeon_onbar">aeon/ms/radio_off.png</textureradiooffocus>'
             '<textureradiooffnofocus colordiffuse="88ffffff">aeon/ms/radio_off.png</textureradiooffnofocus>' % (w - 88))
    return (set_row(7, 'button', w) + set_row(8, 'radiobutton', w, radio) + set_row(9, 'spincontrolex', w) +
            '<control type="image" id="11"><width>%d</width><height>1</height><texture colordiffuse="22ffffff">common/white.png</texture></control>' % w +
            set_row(12, 'edit', w) + set_row(13, 'sliderex', w, '<sliderwidth>220</sliderwidth><sliderheight>24</sliderheight>') +
            '<control type="label" id="14"><width>%d</width><height>%d</height><textoffsetx>32</textoffsetx><font>ui_22_semibold</font>'
            '<textcolor>%s</textcolor><selectedcolor>%s</selectedcolor><aligny>center</aligny></control>' % (w, R, W3, W3) +
            set_row(15, 'colorbutton', w))


def cat_template(w, tab=False):
    """button 10: one category. Kodi draws the open category with this focus texture, faded, and the focused text colour
    while the highlight is in the settings: a light bar with dark text in Mosaic / Ledger / Bridge. Tab slab: the focus is
    the slab's colour with white text (the open tab fades into the slab colour); a white mark shows the real focus."""
    nofocus = ('<texturenofocus colordiffuse="x_raised">common/white.png</texturenofocus>' if tab else
               '<texturenofocus border="24,0,24,0" colordiffuse="16ffffff">aeon/ms/rowline.png</texturenofocus>')
    return ('<control type="button" id="10"><width>%d</width><height>%d</height><font>ui_24_semibold</font><textcolor>%s</textcolor>'
            '<focusedcolor>%s</focusedcolor><selectedcolor>ffffffff</selectedcolor><disabledcolor>44ffffff</disabledcolor>'
            '<textoffsetx>%d</textoffsetx><aligny>center</aligny><pulseonselect>false</pulseonselect>'
            '<texturefocus colordiffuse="%s">common/white.png</texturefocus>%s'
            '<onfocus>SetProperty(ms.cat,$ESCINFO[System.CurrentControl])</onfocus></control>'
            % (w, R, W2, 'ffffffff' if tab else 'aeon_onbar', 40 if tab else 32, BOX if tab else 'aeon_white', nofocus))


def tab_marks(x, y):
    """Tab slab: a white mark on the focused category tab (not while the column is scrolled)"""
    return ''.join(img(x + 12, y + i * R + 14, 6, R - 28, 'ffffffff',
                       'Control.HasFocus(%d) + !Container(3).HasPrevious' % (-200 + i)) for i in range(CATS))


def cat_list(x, y, w, rows, right):
    return ('<control type="grouplist" id="3"><description>categories (Kodi clones 10 here)</description><left>%d</left><top>%d</top>'
            '<width>%d</width><height>%d</height><itemgap>0</itemgap><orientation>vertical</orientation><pagecontrol>61</pagecontrol>'
            '<onleft>noop</onleft><onright>%s</onright><onup>20</onup><ondown>20</ondown></control>'
            '<control type="scrollbar" id="61"><left>-400</left><top>0</top><width>4</width><height>100</height><visible>false</visible></control>'
            % (x, y, w, rows * R, right))


def level_button(x, y, w, color='x_deep'):
    ups = ''.join('<onup condition="Integer.IsEqual(Container(3).NumItems,%d)">SetFocus(%d)</onup>' % (n, -201 + n) for n in range(1, 21))
    return ('<control type="button" id="20"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><font>ui_22_semibold</font>'
            '<textcolor>%s</textcolor><focusedcolor>aeon_onbar</focusedcolor><textoffsetx>32</textoffsetx><aligny>center</aligny>'
            '<pulseonselect>false</pulseonselect><texturefocus colordiffuse="aeon_white">common/white.png</texturefocus>'
            '<texturenofocus colordiffuse="%s">common/white.png</texturenofocus><onclick>SettingsLevelChange</onclick>%s'
            '<ondown>SetFocus(-200)</ondown><onleft>noop</onleft><onright>5</onright></control>' % (x, y, w, R, W2, color, ups))


def open_cat(x, y, w, color, mark=False):
    """the open category while the highlight is in the settings: a fill (or a mark) behind its cell"""
    out = ''
    for i in range(CATS):
        c = 'ControlGroup(3).HasFocus(%d) + !Control.HasFocus(%d) + !Container(3).HasPrevious' % (-200 + i, -200 + i)
        out += img(x, y + i * R, 6 if mark else w, R, color, c)
    return out


def options(x, y, w, rows, addon):
    right = '9000' if addon else 'noop'
    return ('<control type="grouplist" id="5"><description>settings (Kodi clones 7-15 here)</description><left>%d</left><top>%d</top>'
            '<width>%d</width><height>%d</height><itemgap>0</itemgap><pagecontrol>60</pagecontrol><onleft>3</onleft><onright>%s</onright>'
            '<onup>5</onup><ondown>5</ondown></control>'
            '<control type="scrollbar" id="60"><left>%d</left><top>%d</top><width>4</width><height>%d</height>'
            '<texturesliderbackground colordiffuse="10ffffff">common/white.png</texturesliderbackground>'
            '<texturesliderbar colordiffuse="44ffffff">common/white.png</texturesliderbar>'
            '<texturesliderbarfocus colordiffuse="aeon_white">common/white.png</texturesliderbarfocus>'
            '<orientation>vertical</orientation><showonepage>false</showonepage><onleft>5</onleft><onright>5</onright></control>'
            % (x, y, w, rows * R, right, x + w - 4, y, rows * R))


def help_box(x, y, w):
    return img(x, y, w, 2 * R, 'x_deep') + textbox(x + 32, y + 18, w - 64, 3 * PLOT_LINE, '', 'body_24', W2, cid=6)


def addon_buttons(x, y, w):
    nav = '<onleft>5</onleft><onright>noop</onright><onup>5</onup><ondown>5</ondown>'
    return (img(x, y, w, R, 'x_deep') +
            '<control type="grouplist" id="9000"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><itemgap>0</itemgap>'
            '<orientation>horizontal</orientation><align>right</align><usecontrolcoords>true</usecontrolcoords>%s%s</control>'
            % (x, y, w, R, nav.replace('<onleft>5</onleft>', '<onleft>9000</onleft>').replace('<onright>noop</onright>', '<onright>9000</onright>'),
               ''.join(cell_button(i, 220) for i in (28, 29, 30))))


def set_art(x, y, size, addon):
    if addon:
        return (img(x, y, size, size, 'x_deep') +
                art(x + 12, y + 12, size - 24, size - 24, '$INFO[ListItem.Icon]', '$EXP[MS_HasAddonIcon]', aspect='keep') +
                icon(x + (size - 64) // 2, y + (size - 64) // 2, 64, 'aeon/icons/settings.png', W1, '!$EXP[MS_HasAddonIcon]'))
    return img(x, y, size, size, 'x_deep') + icon(x + (size - 64) // 2, y + (size - 64) // 2, 64, '$VAR[MS_SetIcon]', W1)


def set_titles(addon):
    """kicker / title of the title box, kicker of the category header"""
    if addon:
        return '$LOCALIZE[24000]', '$INFO[Control.GetLabel(2)]'
    return '$LOCALIZE[5]', '$INFO[Control.GetLabel(2)]'


def settings_mosaic(addon):
    CW, OW = 480, 900
    x0, ly = (1920 - CW - OW) // 2, SY0 + 2 * R
    k, t = set_titles(addon)
    rows = 8 if addon else 9
    # the icon tile stands in the title row, at the right end of the title box (it sat over the first two category
    # rows and could cover a long category name); the title scrolls in the room left of it
    o = img(x0, SY0, CW, 2 * R, BOX)
    o += lab(x0 + 32, SY0 + 22, CW - 2 * R - 56, 30, '[UPPERCASE]%s[/UPPERCASE]' % k, 'cap_20', CAP_ON_BOX)
    o += lab(x0 + 32, SY0 + 52, CW - 2 * R - 56, 64, t, 'font37', 'ffffffff', scroll=True)
    o += img(x0 + CW, SY0, OW, 2 * R, 'x_deep') + lab(x0 + CW + 32, SY0 + 22, OW - 64, 30, '$VAR[MS_CatPos]', 'cap_20', W3)
    o += lab(x0 + CW + 32, SY0 + 52, OW - 64, 64, '$VAR[MS_OpenCat]', 'font37', 'ffffffff')
    o += img(x0, ly, CW, (CATS + 1) * R, 'x_panel')
    o += cat_list(x0, ly, CW, CATS, '5') + level_button(x0, ly + CATS * R, CW)
    o += img(x0 + CW, ly, OW, rows * R, 'x_raised') + options(x0 + CW, ly, OW, rows, addon)
    if addon:
        o += addon_buttons(x0 + CW, ly + rows * R, OW)
    o += help_box(x0 + CW, ly + 9 * R, OW)
    o += set_art(x0 + CW - 2 * R, SY0, 2 * R, addon)
    return o + set_templates(OW) + cat_template(CW)


def settings_ledger(addon):
    CW, LC, VC = 440, 560, 440
    OW = LC + VC
    x0, ly = (1920 - CW - OW) // 2, SY0 + 2 * R
    k, t = set_titles(addon)
    rows = 8 if addon else 9
    o = title_box(x0, SY0, CW, BOX, k, t)
    o += img(x0 + CW, SY0, OW - 2 * R, 2 * R, 'x_deep') + lab(x0 + CW + 32, SY0 + 22, OW - 2 * R - 64, 30, '$VAR[MS_CatPos]', 'cap_20', W3)
    o += lab(x0 + CW + 32, SY0 + 52, OW - 2 * R - 64, 64, '$VAR[MS_OpenCat]', 'font37', 'ffffffff')
    o += set_art(x0 + CW + OW - 2 * R, SY0, 2 * R, addon)
    o += img(x0, ly, CW, (CATS + 1) * R, 'x_panel')
    o += cat_list(x0, ly, CW, CATS, '5') + level_button(x0, ly + CATS * R, CW)
    # two columns behind the rows: the label and the value share each row
    o += img(x0 + CW, ly, LC, rows * R, 'x_raised') + img(x0 + CW + LC, ly, VC, rows * R, 'x_panel') + options(x0 + CW, ly, OW, rows, addon)
    if addon:
        o += addon_buttons(x0 + CW, ly + rows * R, OW)
    o += help_box(x0 + CW, ly + 9 * R, OW)
    return o + set_templates(OW) + cat_template(CW)


def settings_bridge(addon):
    CW, OW = 420, 960
    x0, ly = (1920 - CW - OW) // 2, SY0 + 2 * R
    k, t = set_titles(addon)
    rows = 7 if addon else 8
    o = title_box(x0, SY0, CW, BOX, k, t)
    o += img(x0, ly, CW, (CATS + 1) * R, 'x_panel')
    o += cat_list(x0, ly, CW, CATS, '5') + level_button(x0, ly + CATS * R, CW)
    # the step: the count on the title box's first row, the settings box one row lower
    ox = x0 + CW
    o += img(ox, SY0, 240, R, 'x_raised') + lab(ox + 28, SY0, 200, R, '$VAR[MS_CatPos]', 'num_22', W2)
    o += img(ox, SY0 + R, OW - 2 * R, 2 * R, 'x_deep') + lab(ox + 32, SY0 + R + 22, OW - 2 * R - 64, 30, t, 'cap_20', W3)
    o += lab(ox + 32, SY0 + R + 52, OW - 2 * R - 64, 64, '$VAR[MS_OpenCat]', 'font37', 'ffffffff')
    # a second step on the right: the joining tile one row above the header's end
    o += set_art(ox + OW - 2 * R, SY0, 2 * R, addon) + img(ox + OW - 2 * R, SY0 + 2 * R, 2 * R, R, 'x_deep')
    o += img(ox, SY0 + 3 * R, OW, rows * R, 'x_raised') + options(ox, SY0 + 3 * R, OW, rows, addon)
    if addon:
        o += addon_buttons(ox, SY0 + 3 * R + rows * R, OW)
    o += help_box(ox, SY0 + 11 * R, OW)
    return o + set_templates(OW) + cat_template(CW)


def settings_tabslab(addon):
    TW, SW = 400, 960
    x0 = (1920 - TW - SW - 2 * R) // 2
    k, t = set_titles(addon)
    rows = 7 if addon else 8
    o = img(x0, SY0, TW, (CATS + 1) * R, 'x_raised')
    o += cat_list(x0, SY0, TW, CATS, '5') + level_button(x0, SY0 + CATS * R, TW, 'x_panel')
    sx = x0 + TW
    o += img(sx, SY0, SW, 12 * R + 24, BOX)
    o += lab(sx + 32, SY0 + 14, SW - 64, 26, '[UPPERCASE]%s · %s[/UPPERCASE]' % (k, t), 'cap_20', CAP_ON_BOX)
    o += lab(sx + 32, SY0 + 40, SW - 64, 64, '$VAR[MS_OpenCat]', 'font37', 'ffffffff')
    o += set_art(sx + SW, SY0, 2 * R, addon)
    o += img(sx + 24, SY0 + 2 * R, SW - 48, rows * R, 'x_panel') + options(sx + 24, SY0 + 2 * R, SW - 48, rows, addon)
    if addon:
        o += addon_buttons(sx + 24, SY0 + 2 * R + rows * R, SW - 48)
    o += help_box(sx + 24, SY0 + 10 * R, SW - 48)
    return o + set_templates(SW - 48) + cat_template(TW, tab=True) + tab_marks(x0, SY0)


BODY = {'Ctx': {'mosaic': ctx_mosaic, 'ledger': ctx_ledger, 'bridge': ctx_bridge, 'tabslab': ctx_tabslab},
        'Confirm': {'mosaic': confirm_mosaic, 'ledger': confirm_ledger, 'bridge': confirm_bridge, 'tabslab': confirm_tabslab},
        'Select': {'mosaic': select_mosaic, 'ledger': select_ledger, 'bridge': select_bridge, 'tabslab': select_tabslab},
        'SetCat': {s: (lambda f: (lambda: f(False)))(f) for s, f in
                   (('mosaic', settings_mosaic), ('ledger', settings_ledger), ('bridge', settings_bridge), ('tabslab', settings_tabslab))},
        'AddonSet': {s: (lambda f: (lambda: f(True)))(f) for s, f in
                     (('mosaic', settings_mosaic), ('ledger', settings_ledger), ('bridge', settings_bridge), ('tabslab', settings_tabslab))}}


# ---------------------------------------------------------------------------------------------------------------
# DialogSettings: over the video the player's Audio / Subtitles / Video settings (osd*settings) with the skin's tabs
# 9101-9103 that swap the dialogs; elsewhere Kodi's other settings dialogs (lock, content, timers, sources ...).
# Ids: heading 2, control area 5 (templates 7-15), scrollbar 60, buttons 28 / 29 / 30 in grouplist 9000.
# The panel steps aside while the offset slider is up, so the picture stays clear.
DROWS = 8
TABS = ((9101, '$LOCALIZE[31128]', 'osdaudiosettings', 'Window.IsActive(osdaudiosettings)'),
        (9102, '$LOCALIZE[31127]', 'osdsubtitlesettings', 'Window.IsActive(osdsubtitlesettings)'),
        (9103, '$LOCALIZE[31563]', 'osdvideosettings', 'Window.IsActive(osdvideosettings) | Window.IsActive(osdcmssettings)'))
# the playing audio by the skin's own names (as on the library's media flags), channels as 5.1 / 7.1
AC = 'VideoPlayer.AudioCodec'
HEAD.append(variable('MS_PlayerAudio', [
    ('String.Contains(%s,truehd) + String.Contains(%s,atmos)' % (AC, AC), '$LOCALIZE[31420]'),
    ('String.Contains(%s,eac3) + String.Contains(%s,atmos)' % (AC, AC), '$LOCALIZE[31421]'),
    ('String.StartsWith(%s,dtshd_ma_x) | String.IsEqual(%s,dtsx)' % (AC, AC), 'DTS:X'),
    ('String.IsEqual(%s,dtshd_ma)' % AC, '$LOCALIZE[31422]'), ('String.IsEqual(%s,dtshd_hra)' % AC, '$LOCALIZE[31423]'),
    ('String.IsEqual(%s,truehd)' % AC, '$LOCALIZE[31424]'), ('String.IsEqual(%s,eac3)' % AC, '$LOCALIZE[31425]'),
    ('String.IsEqual(%s,ac3)' % AC, '$LOCALIZE[31426]'), ('String.IsEqual(%s,dca) | String.IsEqual(%s,dts)' % (AC, AC), 'DTS'),
    ('String.StartsWith(%s,aac)' % AC, 'AAC'), ('String.IsEqual(%s,flac)' % AC, '$LOCALIZE[31427]'),
    ('String.IsEqual(%s,alac)' % AC, '$LOCALIZE[31428]'), ('String.IsEqual(%s,mp3)' % AC, 'MP3'),
    ('String.IsEqual(%s,opus)' % AC, '$LOCALIZE[31429]'), ('String.StartsWith(%s,pcm) | String.IsEqual(%s,lpcm)' % (AC, AC), 'PCM'),
    ('String.IsEqual(%s,vorbis)' % AC, '$LOCALIZE[31430]'), ('', '[UPPERCASE]$INFO[%s][/UPPERCASE]' % AC)]))
PINFO = [('$LOCALIZE[292]', 'VideoPlayer.AudioCodec', '$VAR[MS_PlayerAudio]$VAR[OSD_AudioChannels, · ,]'),
         ('$LOCALIZE[248]', 'VideoPlayer.AudioLanguage', '$INFO[VideoPlayer.AudioLanguage]'),
         ('$LOCALIZE[291]', 'VideoPlayer.VideoResolution', '$INFO[VideoPlayer.VideoResolution]$INFO[VideoPlayer.VideoCodec, · ,]'),
         ('$LOCALIZE[287]', 'VideoPlayer.SubtitlesLanguage', '$INFO[VideoPlayer.SubtitlesLanguage]')]


def osd_tabs(x, y, cw, current_color=BOX, base='x_deep', width=None):
    """the three tabs as flush cells; the open one in current_color, focus white"""
    out = img(x, y, width or 3 * cw, R, base)
    for i, (cid, label, target, current) in enumerate(TABS):
        left = 'noop' if i == 0 else str(TABS[i - 1][0])
        right = 'noop' if i == 2 else str(TABS[i + 1][0])
        cx = x + i * cw
        out += img(cx, y, cw, R, current_color, current)
        clicks = ''.join('<onclick condition="!Window.IsActive(%s)">%s</onclick>' % (target, a) for a in (
            'SetProperty(aeon.osdtab,1,home)', 'Dialog.Close(osdaudiosettings,true)', 'Dialog.Close(osdsubtitlesettings,true)',
            'Dialog.Close(osdvideosettings,true)', 'Dialog.Close(osdcmssettings,true)', 'ActivateWindow(%s)' % target))
        out += ('<control type="button" id="%d"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><label>[UPPERCASE]%s[/UPPERCASE]</label>'
                '<font>cap_20</font><textcolor>ffffffff</textcolor><focusedcolor>aeon_onbar</focusedcolor><align>center</align><aligny>center</aligny>'
                '<pulseonselect>false</pulseonselect><texturefocus colordiffuse="aeon_white">common/white.png</texturefocus><texturenofocus/>'
                '<onleft>%s</onleft><onright>%s</onright><onup>noop</onup><ondown>5</ondown>%s</control>'
                % (cid, cx, y, cw, R, label, left, right, clicks))
    return out


def dlg_options(x, y, w, osd):
    # 0.56.53 + a fallback that holds only while Kodi builds the rows: with no Up holding then, Kodi links the first
    # row's Up to the last row (GUIControlGroupList::AddControl) and the tabs could not be reached
    up = ((''.join('<onup condition="%s">%d</onup>' % (cur, cid) for cid, _, _, cur in TABS)
           + '<!-- 0.56.53 fallback: Kodi links the first row Up to the last row when no Up holds while it builds the rows -->'
           '<onup condition="!Window.IsActive(osdaudiosettings) + !Window.IsActive(osdsubtitlesettings) + '
           '!Window.IsActive(osdvideosettings) + !Window.IsActive(osdcmssettings)">9101</onup>') if osd else '<onup>5</onup>')
    return ('<control type="grouplist" id="5"><description>settings (Kodi clones 7-15 here)</description><left>%d</left><top>%d</top>'
            '<width>%d</width><height>%d</height><itemgap>0</itemgap><pagecontrol>60</pagecontrol><onleft>noop</onleft><onright>noop</onright>'
            '%s<ondown condition="Control.IsVisible(28) | Control.IsVisible(29) | Control.IsVisible(30)">9000</ondown>'
            '<ondown condition="!Control.IsVisible(28) + !Control.IsVisible(29) + !Control.IsVisible(30)">5</ondown></control>'
            '<control type="scrollbar" id="60"><left>%d</left><top>%d</top><width>4</width><height>%d</height>'
            '<texturesliderbackground colordiffuse="10ffffff">common/white.png</texturesliderbackground>'
            '<texturesliderbar colordiffuse="44ffffff">common/white.png</texturesliderbar>'
            '<texturesliderbarfocus colordiffuse="aeon_white">common/white.png</texturesliderbarfocus>'
            '<orientation>vertical</orientation><showonepage>false</showonepage><onleft>5</onleft><onright>5</onright></control>'
            % (x, y, w, DROWS * R, up, x + w - 4, y, DROWS * R))


def dlg_buttons(x, y, w):
    nav = '<onleft>9000</onleft><onright>9000</onright><onup>5</onup><ondown>5</ondown>'
    return (img(x, y, w, R, 'x_deep') +
            '<control type="grouplist" id="9000"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><itemgap>0</itemgap>'
            '<orientation>horizontal</orientation><align>right</align><usecontrolcoords>true</usecontrolcoords>%s%s</control>'
            % (x, y, w, R, nav, ''.join(cell_button(i, 220) for i in (28, 29, 30))))


def dlg_hint(x, y, w, h):
    """the offset note under the audio and subtitle settings"""
    return textbox(x, y, w, h // PLOT_LINE * PLOT_LINE, '$LOCALIZE[31243]', 'body_24', W2,
                   'Window.IsActive(osdaudiosettings) | Window.IsActive(osdsubtitlesettings)')


def dlg_wrap(w, h, inner, osd):
    dim = DIM.replace('c8000000', '55000000') if osd else DIM
    return ('<control type="group"><visible>!Window.IsVisible(sliderdialog)</visible><include>Anim_FadeVisible</include>%s'
            '<control type="group"><left>%d</left><top>%d</top>\n%s\n</control></control>' % (dim, (1920 - w) // 2, (1080 - h) // 2, inner))


def dlg_art(x, y, w, h, osd, empty=BOX):
    if osd:
        return poster_tile(x, y, w, h, glyph='aeon/icons/settings.png', empty=empty)
    return img(x, y, w, h, empty) + icon(x + (w - 64) // 2, y + (h - 64) // 2, 64, 'aeon/icons/settings.png', 'ccffffff')


def dlg_mosaic(osd):
    LW, IW = 900, 480
    t0 = R if osd else 0
    o = osd_tabs(0, 0, 200, width=LW) if osd else ''
    o += img(0, t0, LW, 2 * R, BOX) + lab(32, t0 + 22, LW - 64, 30, '[UPPERCASE]$VAR[MS_ItemKicker][/UPPERCASE]' if osd else '', 'cap_20', CAP_ON_BOX)
    o += heading(32, t0 + 52, LW - 64, cid=2)
    o += (img(LW, 0, IW, t0 + 2 * R, 'x_deep') + art(LW, 0, IW, t0 + 2 * R, '$VAR[MS_Fanart]', '$EXP[MS_HasFanart]')) if osd else img(LW, 0, IW, 2 * R, 'x_deep')
    ly = t0 + 2 * R
    o += img(0, ly, LW, DROWS * R, 'x_panel') + dlg_options(0, ly, LW, osd)
    o += img(LW, ly, IW, DROWS * R, 'x_raised') + dlg_art(LW, ly, 192, 4 * R, osd)
    if osd:
        o += info_stacked(LW + 220, ly, IW - 248, 4 * R, PINFO) + dlg_hint(LW + 32, ly + 4 * R + 16, IW - 64, 4 * R - 32)
    o += dlg_buttons(0, ly + DROWS * R, LW + IW)
    return dlg_wrap(LW + IW, ly + (DROWS + 1) * R, o, osd) + set_templates(LW)


def dlg_ledger(osd):
    SP, LC, VC = 96, 560, 460
    W = SP + LC + VC
    t0 = R if osd else 0
    o = osd_tabs(SP, 0, 200, width=LC + VC) + img(0, 0, SP, R, 'x_deep') if osd else ''
    o += dlg_art(0, t0, SP, 2 * R, osd)
    o += img(SP, t0, LC + VC, 2 * R, 'x_deep') + lab(SP + 32, t0 + 22, LC + VC - 64, 30, '[UPPERCASE]$VAR[MS_ItemKicker][/UPPERCASE]' if osd else '', 'cap_20', W3)
    o += heading(SP + 32, t0 + 52, LC + VC - 64, cid=2)
    ly = t0 + 2 * R
    # the spine, then the label and value columns behind Kodi's rows
    o += img(0, ly, SP, DROWS * R, BOX) + img(SP, ly, LC, DROWS * R, 'x_raised') + img(SP + LC, ly, VC, DROWS * R, 'x_panel')
    for i, (cid, label, target, current) in enumerate(TABS if osd else ()):
        o += icon(24, ly + 12, 48, ('aeon/icons/audio.png', 'aeon/icons/subtitles.png', 'aeon/icons/film.png')[i], 'ffffffff', current)
    if not osd:
        o += icon(24, ly + 12, 48, 'aeon/icons/settings.png', 'ffffffff')
    o += dlg_options(SP, ly, LC + VC, osd)
    o += dlg_buttons(0, ly + DROWS * R, W)
    return dlg_wrap(W, ly + (DROWS + 1) * R, o, osd) + set_templates(LC + VC)


def dlg_bridge(osd):
    TW, PW, LW, IW = 640, 192, 900, 400
    o = img(0, 0, TW, 2 * R, BOX) + lab(32, 22, TW - 64, 30, '[UPPERCASE]$VAR[MS_ItemKicker][/UPPERCASE]' if osd else '', 'cap_20', CAP_ON_BOX)
    o += heading(32, 52, TW - 64, cid=2)
    if osd:
        # the step: the tabs sit on the title box's second row, out to its right, over the settings box
        o += osd_tabs(TW, R, 150, width=450)
    o += dlg_art(0, 2 * R, PW, 4 * R, osd, empty='x_raised')
    o += img(PW, 2 * R, LW, DROWS * R, 'x_panel') + dlg_options(PW, 2 * R, LW, osd)
    ix = PW + LW
    o += img(ix, 3 * R, IW, (DROWS - 1) * R, 'x_raised')
    if osd:
        o += info_inline(ix + 28, 3 * R, IW - 56, 4 * R, keyw=130, info=PINFO) + dlg_hint(ix + 28, 7 * R + 12, IW - 56, 3 * R - 24)
    o += dlg_buttons(PW, (2 + DROWS) * R, LW)
    return dlg_wrap(PW + LW + IW, (3 + DROWS) * R, o, osd) + set_templates(LW)


def dlg_tabslab(osd):
    SW, AW = 900, 400
    o = osd_tabs(0, 0, 180, width=SW) if osd else img(0, 0, 260, R, BOX) + img(260, 0, SW - 260, R, 'x_deep')
    o += img(0, R, SW, R, BOX) + heading(32, R, SW - 64, R, 'ui_30_semibold', cid=2)
    o += img(0, 2 * R, SW, DROWS * R, 'x_panel') + dlg_options(0, 2 * R, SW, osd)
    if osd:
        o += img(SW, 0, AW, 3 * R, 'x_deep') + art(SW, 0, AW, 3 * R, '$VAR[MS_Fanart]', '$EXP[MS_HasFanart]')
    else:
        o += img(SW, 0, AW, 3 * R, 'x_deep')
    o += img(SW, 3 * R, AW, (DROWS - 1) * R, 'x_raised') + dlg_art(SW + AW - 168, 3 * R, 168, 252, osd)
    if osd:
        o += info_stacked(SW + 28, 3 * R, AW - 168 - 52, 4 * R, PINFO) + dlg_hint(SW + 28, 7 * R + 12, AW - 56, 3 * R - 24)
    o += dlg_buttons(0, (2 + DROWS) * R, SW + AW)
    return dlg_wrap(SW + AW, (3 + DROWS) * R, o, osd) + set_templates(SW)


BODY['OSDSet'] = {s: (lambda f: (lambda: f(True)))(f) for s, f in
                  (('mosaic', dlg_mosaic), ('ledger', dlg_ledger), ('bridge', dlg_bridge), ('tabslab', dlg_tabslab))}
BODY['DlgSet'] = {s: (lambda f: (lambda: f(False)))(f) for s, f in
                  (('mosaic', dlg_mosaic), ('ledger', dlg_ledger), ('bridge', dlg_bridge), ('tabslab', dlg_tabslab))}


# ---------------------------------------------------------------------------------------------------------------
# Aeon Fuse settings (SkinSettings.xml): the window places its own rows on a 70 px grid (categories 120-480, settings
# 481-1500, both from y 191, so their rows already line up); the styles draw the boxes behind them. The open
# category's name sits in the band above the categories, the page's name above the settings.
K = 70
SK_CX, SK_CW, SK_OX, SK_OW, SK_RX, SK_RW = 120, 360, 480, 1020, 1500, 320
SK_TY, SK_TB, SK_ROWS = 108, 191, 11
SK_RE = SK_TB + SK_ROWS * K          # 961
SK_HE = 1045                         # the help line under the settings ends here


def sk_swatches(x, y, s):
    """the palette as the joining tile: four squares, the focus colour as a small inset"""
    h = s // 2
    out = ''.join(img(x + (i % 2) * h, y + (i // 2) * h, h, h, c) for i, c in enumerate(('x_deep', 'x_raised', BOX, 'x_deep')))
    return out + img(x + h + h // 4, y + h + h // 4, h // 2, h // 2, 'aeon_white')


def sk_help(x, w):
    """the help line of the focused row, inside its box (x .. x + w), 24 px in from both ends and centred on the box's
    height: a wrapping label (a textbox cannot centre its lines). The window's own textbox is for the other looks."""
    return lab(x + 24, SK_RE, w - 48, SK_HE - SK_RE, '$VAR[Dlg_SkinHelp]', 'st_small_20', '$VAR[AG_Ink2]',
               cond='!String.IsEqual(Window(Home).Property(aeon.skincat),homemenu)', extra='<wrapmultiline>true</wrapmultiline>')


def skinset_mosaic():
    o = img(SK_CX, SK_TY, SK_CW, SK_TB - SK_TY, BOX) + img(SK_OX, SK_TY, SK_OW + SK_RW, SK_TB - SK_TY, 'x_deep')
    o += img(SK_CX, SK_TB, SK_CW, SK_ROWS * K, 'x_panel') + img(SK_OX, SK_TB, SK_OW, SK_ROWS * K, 'x_raised')
    o += img(SK_RX, SK_TB, SK_RW, SK_ROWS * K, 'x_panel') + img(SK_OX, SK_RE, SK_OW + SK_RW, SK_HE - SK_RE, 'x_deep')
    # the palette tile beside the clock box, on the caption band (0.40.5: it sat over the first two category rows)
    o += sk_swatches(SK_OX + SK_OW + SK_RW - SK_TY, 0, SK_TY)
    return o + sk_help(SK_OX, SK_OW + SK_RW)


def skinset_ledger():
    o = img(SK_CX, SK_TY, SK_CW, SK_TB - SK_TY, BOX) + img(SK_OX, SK_TY, SK_OW + SK_RW - 83, SK_TB - SK_TY, 'x_deep')
    o += sk_swatches(SK_RX + SK_RW - 83, SK_TY, 83)
    # categories, then the label and value columns of the rows, all on one grid
    o += img(SK_CX, SK_TB, SK_CW, SK_ROWS * K, 'x_panel') + img(SK_OX, SK_TB, 440, SK_ROWS * K, 'x_raised')
    o += img(SK_OX + 440, SK_TB, SK_OW - 440, SK_ROWS * K, 'x_panel') + img(SK_RX, SK_TB, SK_RW, SK_ROWS * K, 'x_raised')
    return o + img(SK_OX, SK_RE, SK_OW + SK_RW, SK_HE - SK_RE, 'x_deep') + sk_help(SK_OX, SK_OW + SK_RW)


def skinset_bridge():
    # the title box over the categories, the settings box beside them; on the right the palette tile steps from the band
    # down onto the first row, and the side column starts under it
    o = img(SK_CX, SK_TY, SK_CW, SK_TB - SK_TY, BOX) + img(SK_CX, SK_TB, SK_CW, SK_ROWS * K, 'x_panel')
    o += img(SK_OX, SK_TY, SK_OW, SK_TB - SK_TY, 'x_deep') + img(SK_OX, SK_TB, SK_OW, SK_ROWS * K, 'x_raised')
    # 0.56.16 (the user: "make mosaic box larger so that black box has same height as black strip next to it ... corners
    # meet perpendicularly"): the tile's squares are as tall as the title band (83), so its black square ends where the
    # band ends
    tile = 2 * (SK_TB - SK_TY)
    o += sk_swatches(SK_RX, SK_TY, tile) + img(SK_RX, SK_TY + tile, SK_RW, SK_RE - SK_TY - tile, 'x_deep')
    # the help box runs on under the side column (one deep box): the help line has the whole width
    return o + img(SK_OX, SK_RE, SK_OW + SK_RW, SK_HE - SK_RE, 'x_deep') + sk_help(SK_OX, SK_OW + SK_RW)


def skinset_tabslab():
    # the categories are tabs; the slab (palette box) holds the settings and the help line
    o = img(SK_OX, SK_TY, SK_OW + SK_RW, SK_HE + 24 - SK_TY, BOX)
    o += img(SK_OX + 24, SK_TB, SK_OW - 24, SK_ROWS * K, 'x_panel') + img(SK_RX, SK_TB, SK_RW - 24, SK_ROWS * K, 'x_raised')
    o += img(SK_OX + 24, SK_RE, SK_OW + SK_RW - 48, SK_HE - SK_RE, 'x_deep')
    o += img(SK_CX, SK_TY, SK_CW, SK_TB - SK_TY, 'x_deep')
    return o + sk_swatches(SK_OX - 83, SK_TY, 83) + sk_help(SK_OX + 24, SK_OW + SK_RW - 48)


BODY['SkinSet'] = {'mosaic': skinset_mosaic, 'ledger': skinset_ledger, 'bridge': skinset_bridge, 'tabslab': skinset_tabslab}
# Mosaic's palette tile sits beside the clock box now (skinset_mosaic); nothing is drawn over the category cells
BODY['SkinSetTop'] = {'mosaic': lambda: '', 'ledger': lambda: '', 'bridge': lambda: '', 'tabslab': lambda: ''}



def track(fn):
    def run():
        TRACK[0] = True
        try:
            return fn()
        finally:
            TRACK[0] = False
    return run


BODY['TrackSel'] = {'mosaic': track(select_mosaic), 'ledger': track(select_ledger), 'bridge': track(select_bridge),
                    'tabslab': track(select_tabslab)}



# ---------------------------------------------------------------------------------------------------------------
# Library panel (dialog 1160: View, Sort, Order, Unwatched, Sets, Search, Update / Clean library ...; list 100, the clean
# question list 200, music button 300) and View settings (dialog 1166, list 100). The items stay in
# Includes_LibraryPanel.xml (LibPanel_Items, LibPanel_CleanItems, ViewSet_Items) and the styles lay them out as menus:
# icon, name, current value. The Library panel shows the focused library item beside it; View settings sits at the left
# with a light dim, so the view underneath shows each change at once.
PCAP = 11
CLEAN = '!String.IsEmpty(Window(Home).Property(aeon.libclean))'


def pn_count(kind, n, op='IsEqual'):
    if kind == 'view':
        return 'Integer.%s(Container(100).NumItems,%d)' % (op, n)
    return ('[!%s + Integer.%s(Container(100).NumItems,%d)] | [%s + Integer.%s(Container(200).NumItems,%d)]'
            % (CLEAN, op, n, CLEAN, op, n))


for _k in ('lib', 'view'):
    for _n in range(0, PCAP):
        HEAD.append(expression('MS_%sN%d' % (_k, _n), pn_count(_k, _n)))
    HEAD.append(expression('MS_%sN%d' % (_k, PCAP), pn_count(_k, PCAP - 1, 'IsGreater')))
for _i in range(PCAP):
    HEAD.append(expression('MS_libF%d' % _i, '[!%s + Integer.IsEqual(Container(100).Position,%d)] | [%s + Integer.IsEqual(Container(200).Position,%d)]'
                           % (CLEAN, _i, CLEAN, _i)))
    HEAD.append(expression('MS_viewF%d' % _i, 'Integer.IsEqual(Container(100).Position,%d)' % _i))
HEAD.append(variable('MS_libPos', [(CLEAN, '$INFO[Container(200).CurrentItem]$INFO[Container(200).NumItems, / ,]'),
                                   ('', '$INFO[Container(100).CurrentItem]$INFO[Container(100).NumItems, / ,]')]))
HEAD.append(variable('MS_viewPos', [('', '$INFO[Container(100).CurrentItem]$INFO[Container(100).NumItems, / ,]')]))
# the library item beside the panel: only for the library underneath (not when opened from the System menu)
HEAD.append(expression('MS_LibItem', 'String.IsEmpty(Window(Home).Property(aeon.libmode)) + [Window.IsActive(videos) | Window.IsActive(music)]'))
HEAD.append(expression('MS_LibHasPoster', '$EXP[MS_LibItem] + $EXP[MS_HasPoster]'))
HEAD.append(expression('MS_LibHasFanart', '$EXP[MS_LibItem] + $EXP[MS_HasFanart]'))
PN = {'lib': {'title': '$VAR[LibPanel_Title]', 'kicker': '$VAR[LibPanel_Where]', 'pos': '$VAR[MS_libPos]', 'win': 1160,
              'poster': '$EXP[MS_LibHasPoster]', 'fanart': '$EXP[MS_LibHasFanart]', 'item': '$EXP[MS_LibItem]'},
      'view': {'title': '$LOCALIZE[31540]', 'kicker': '$VAR[Aeon_ViewName]', 'pos': '$VAR[MS_viewPos]', 'win': 1166,
               'poster': '$EXP[MS_LibHasPoster]', 'fanart': '$EXP[MS_LibHasFanart]', 'item': '$EXP[MS_LibItem]'}}


def pn_cond(kind, m):
    if m == MIN_ROWS:
        return ' | '.join('$EXP[MS_%sN%d]' % (kind, n) for n in range(0, MIN_ROWS + 1))
    return '$EXP[MS_%sN%d]' % (kind, m)


def pn_per_m(kind, fn):
    return ''.join(fn(m, pn_cond(kind, m)) for m in range(MIN_ROWS, PCAP + 1))


def pn_row(cid, w, focused, spine=0, value_w=0):
    """one panel row: the item's icon, its name, its current value at the right (Ledger: icon in the spine, value column)"""
    fc = 'Control.HasFocus(%d)' % cid
    out = []
    if spine:
        out.append(img(0, 0, spine, R, BOX))
    if focused:
        out.append(img(0, 0, w, R, 'aeon_white', fc))
    if not spine:
        out.append('<control type="image"><left>0</left><top>0</top><width>%d</width><height>%d</height>'
                   '<texture border="24,0,24,0" colordiffuse="16ffffff">aeon/ms/rowline.png</texture>%s</control>'
                   % (w, R, vis('!' + fc) if focused else ''))
    ix = (spine - 32) // 2 if spine else 28
    out.append(icon(ix, 20, 32, '$INFO[ListItem.Icon]', 'ffffffff', ('!' + fc) if focused else None))
    if focused:
        out.append(icon(ix, 20, 32, '$INFO[ListItem.Icon]', 'aeon_onbar', fc))
    x = spine + 32 if spine else 80
    lw = (w - value_w - x - 16) if value_w else (w - x - 300)
    out.append(lab(x, 0, lw, R, '$INFO[ListItem.Label]', 'ui_26', W1, cond=('!' + fc) if focused else None))
    if focused:
        out.append(lab(x, 0, lw, R, '$INFO[ListItem.Label]', 'ui_26_semibold', 'aeon_onbar', cond=fc, scroll=True))
    vx, vw = ((w - value_w + 24), value_w - 52) if value_w else (w - 300, 272)
    out.append(lab(vx, 0, vw, R, '$INFO[ListItem.Label2]', 'ui_22', W2, align='right', cond=('!' + fc) if focused else None))
    if focused:
        out.append(lab(vx, 0, vw, R, '$INFO[ListItem.Label2]', 'ui_22', 'aeon_onbar', align='right', cond=fc))
    return ''.join(out)


def pn_lists(kind, x, y, w, spine=0, value_w=0):
    def lay(cid):
        return ('<itemlayout width="%d" height="%d">%s</itemlayout><focusedlayout width="%d" height="%d">%s</focusedlayout>'
                % (w, R, pn_row(cid, w, False, spine, value_w), w, R, pn_row(cid, w, True, spine, value_w)))
    if kind == 'view':
        return ('<control type="list" id="100"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
                '<onup>100</onup><ondown>100</ondown><onleft>Dialog.Close(1166)</onleft><onright>Dialog.Close(1166)</onright>'
                '<scrolltime tween="cubic" easing="out">200</scrolltime>%s<content><include>ViewSet_Items</include></content></control>'
                % (x, y, w, PCAP * R, lay(100)))
    return ('<control type="list" id="100"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
            '<onup>100</onup><ondown condition="Player.HasAudio">300</ondown><ondown condition="!Player.HasAudio">100</ondown>'
            '<onleft>Dialog.Close(1160)</onleft><onright>Dialog.Close(1160)</onright><scrolltime tween="cubic" easing="out">200</scrolltime>'
            '<visible allowhiddenfocus="true">!%s</visible>%s<content><include>LibPanel_Items</include></content></control>'
            '<control type="list" id="200"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
            '<onup>200</onup><ondown>200</ondown><onleft>noop</onleft><onright>noop</onright><scrolltime tween="cubic" easing="out">200</scrolltime>'
            '<visible allowhiddenfocus="true">%s</visible>%s<content><include>LibPanel_CleanItems</include></content></control>'
            % (x, y, w, PCAP * R, CLEAN, lay(100), x, y, w, PCAP * R, CLEAN, lay(200)))


def pn_footer(kind, x, w, clean_text=False):
    """the last row moves with the list's height. Library panel: the music playing (button 300), else where it is;
    clean_text: the Clean library question's explanation (Ledger has no side box for it)"""
    out = ''
    for m in range(MIN_ROWS, PCAP + 1):
        c = pn_cond(kind, m)
        inner = img(0, 0, w, R, 'x_deep')
        if kind == 'view':
            inner += lab(32, 0, w - 64, R, '$LOCALIZE[31540] · $VAR[Aeon_ViewName]', 'ui_22', W3)
        else:
            inner += lab(32, 0, w - 64, R, '$VAR[LibPanel_Where]', 'ui_22', W3, cond='!Player.HasAudio + !' + CLEAN)
            if clean_text:
                inner += lab(32, 0, w - 64, R, '$VAR[LibPanel_CleanText]', 'ui_22', W2, cond=CLEAN, scroll=True)
        out += group(x, (2 + m) * R, inner, c)
    if kind == 'lib':
        slides = ''.join('<animation effect="slide" end="0,%d" time="0" condition="%s">Conditional</animation>'
                         % ((m - MIN_ROWS) * R, esc(pn_cond(kind, m))) for m in range(MIN_ROWS + 1, PCAP + 1))
        btn = ('<control type="button" id="300"><left>0</left><top>0</top><width>%d</width><height>%d</height>'
               '<label>$INFO[MusicPlayer.Artist,, · ]$INFO[MusicPlayer.Title]</label><font>ui_24</font><textoffsetx>80</textoffsetx>'
               '<aligny>center</aligny><textcolor>%s</textcolor><focusedcolor>aeon_onbar</focusedcolor>'
               '<texturefocus colordiffuse="aeon_white">common/white.png</texturefocus><texturenofocus/>'
               '<onup>100</onup><ondown>noop</ondown><onleft>Dialog.Close(1160)</onleft><onright>Dialog.Close(1160)</onright>'
               '<onclick>Dialog.Close(1160,true)</onclick><onclick>ActivateWindow(visualisation)</onclick>'
               '<visible>Player.HasAudio + !%s</visible></control>' % (w, R, W1, CLEAN))
        eq = (icon(24, 16, 40, 'common/aeon_eq_still.png', 'ffffffff', 'Player.HasAudio + !Control.HasFocus(300)') +
              icon(24, 16, 40, 'common/aeon_eq_still.png', 'aeon_onbar', 'Player.HasAudio + Control.HasFocus(300)'))
        out += '<control type="group"><left>%d</left><top>%d</top>%s%s%s</control>' % (x, (2 + MIN_ROWS) * R, slides, btn, eq)
    return out


def pn_centring(kind):
    return ''.join('<animation effect="slide" end="0,%d" time="0" condition="%s">Conditional</animation>'
                   % (-(m - MIN_ROWS) * R // 2, esc(pn_cond(kind, m))) for m in range(MIN_ROWS + 1, PCAP + 1))


def pn_wrap(kind, w, inner):
    h0 = (3 + MIN_ROWS) * R
    dim = DIM.replace('c8000000', '66000000') if kind == 'view' else DIM.replace('c8000000', 'b4000000')
    left = 60 if kind == 'view' else (1920 - w) // 2
    return (dim + '<control type="group"><left>%d</left><top>%d</top>%s<include>Anim_FadeVisible</include>\n%s\n</control>'
            % (left, (1080 - h0) // 2, pn_centring(kind), inner))


def pn_info(kind, x, y, w, h, stacked=True):
    """beside the list: the library item's facts, or what Clean library does"""
    item = PN[kind]['item']
    lines = (info_stacked if stacked else info_inline)(x, y, w, h).replace('<orientation>', vis(item + ' + !' + CLEAN) + '<orientation>', 1)
    return lines + textbox(x, y, w, h // PLOT_LINE * PLOT_LINE, '$VAR[LibPanel_CleanText]', 'body_24', W1, CLEAN)


def pn_title(kind, x, y, w, color, kicker_color=CAP_ON_BOX):
    p = PN[kind]
    return (img(x, y, w, 2 * R, color) + lab(x + 32, y + 22, w - 214, 30, '[UPPERCASE]%s[/UPPERCASE]' % p['kicker'], 'cap_20', kicker_color) +
            lab(x + w - 182, y + 22, 150, 30, p['pos'], 'cap_20', kicker_color, align='right') +
            lab(x + 32, y + 52, w - 64, 64, p['title'], 'font37', 'ffffffff'))


def panel_mosaic(kind):
    LW, IW = 780, 480
    p = PN[kind]
    o = pn_title(kind, 0, 0, LW, BOX)
    o += img(LW, 0, IW, 2 * R, 'x_deep') + art(LW, 0, IW, 2 * R, '$VAR[MS_Fanart]', p['fanart'])
    o += pn_per_m(kind, lambda m, c: img(0, 2 * R, LW, m * R, 'x_panel', c) + img(LW, 2 * R, IW, m * R, 'x_raised', c))
    o += poster_tile(LW, 2 * R, 192, 4 * R, has=p['poster'])
    o += pn_info(kind, LW + 220, 2 * R, IW - 248, 4 * R)
    o += pn_lists(kind, 0, 2 * R, LW) + pn_footer(kind, 0, LW + IW)
    return pn_wrap(kind, LW + IW, o)


def panel_ledger(kind):
    SP, LW, VW = 96, 560, 440
    W = SP + LW + VW
    p = PN[kind]
    o = poster_tile(0, 0, SP, 2 * R, has=p['poster']) + pn_title(kind, SP, 0, LW + VW, 'x_deep', W3)
    o += pn_per_m(kind, lambda m, c: img(0, 2 * R, SP, m * R, BOX, c) + img(SP, 2 * R, LW, m * R, 'x_panel', c) +
                  img(SP + LW, 2 * R, VW, m * R, 'x_raised', c))
    o += pn_lists(kind, 0, 2 * R, W, spine=SP, value_w=VW) + pn_footer(kind, 0, W, clean_text=True)
    return pn_wrap(kind, W, o)


def panel_bridge(kind):
    TW, PW, LW, IW = 640, 192, 720, 440
    p = PN[kind]
    o = img(0, 0, TW, 2 * R, BOX) + lab(32, 22, TW - 64, 30, '[UPPERCASE]%s[/UPPERCASE]' % p['kicker'], 'cap_20', CAP_ON_BOX)
    o += lab(32, 52, TW - 64, 64, p['title'], 'font37', 'ffffffff')
    o += poster_tile(0, 2 * R, PW, 4 * R, has=p['poster'], empty='x_raised')
    ix = PW + LW
    o += pn_per_m(kind, lambda m, c: img(PW, 2 * R, LW, m * R, 'x_panel', c) + img(ix, 3 * R, IW, (m - 1) * R, 'x_raised', c))
    o += img(ix, 2 * R, 240, R, 'x_deep') + lab(ix + 28, 2 * R, 200, R, p['pos'], 'num_22', W2)
    for i in range(1, PCAP):
        o += img(ix, (2 + i) * R, IW, R, '28ffffff', '$EXP[MS_%sF%d]' % (kind, i))
    o += pn_info(kind, ix + 28, 3 * R, IW - 56, 3 * R, stacked=False)
    o += pn_lists(kind, PW, 2 * R, LW) + pn_footer(kind, PW, LW + IW)
    return pn_wrap(kind, PW + LW + IW, o)


def panel_tabslab(kind):
    SW, AW, TAB = 820, 400, 300
    p = PN[kind]
    o = img(0, 0, TAB, R, BOX) + lab(16, 0, TAB - 32, R, '[UPPERCASE]%s[/UPPERCASE]' % p['kicker'], 'cap_20', 'ffffffff', align='center')
    o += img(TAB, 0, SW - TAB, R, 'x_deep') + lab(TAB + 24, 0, SW - TAB - 48, R, p['pos'], 'num_22', W3, align='right')
    o += img(0, R, SW, R, BOX) + lab(32, R, SW - 64, R, p['title'], 'ui_30_semibold', 'ffffffff')
    o += img(SW, 0, AW, 3 * R, 'x_deep') + art(SW, 0, AW, 3 * R, '$VAR[MS_Fanart]', p['fanart'])
    o += pn_per_m(kind, lambda m, c: img(0, 2 * R, SW, m * R, 'x_panel', c) + img(SW, 3 * R, AW, (m - 1) * R, 'x_raised', c))
    o += poster_tile(SW + AW - 168, 3 * R, 168, 252, has=p['poster'])
    o += pn_info(kind, SW + 28, 3 * R, AW - 168 - 52, 3 * R)
    o += pn_lists(kind, 0, 2 * R, SW) + pn_footer(kind, 0, SW + AW)
    return pn_wrap(kind, SW + AW, o)


for _k, _name in (('lib', 'LibPanel'), ('view', 'ViewSet')):
    BODY[_name] = {_s: (lambda f, k: (lambda: f(k)))(_f, _k) for _s, _f in
                   (('mosaic', panel_mosaic), ('ledger', panel_ledger), ('bridge', panel_bridge), ('tabslab', panel_tabslab))}



# ---------------------------------------------------------------------------------------------------------------
# Kodi Settings hub (Settings.xml, window "settings"): list 9000 with Aeon_SettingsItems (label, label2 = what it holds,
# properties icon / help); beside it the focused entry and "This box". The window keeps its top bar (caption + clock).
HY0 = 112
HROWS = 11
HUB_FACTS = [('$LOCALIZE[31000]', '$INFO[System.BuildVersionShort]'), ('$LOCALIZE[31649]', 'Aeon Fuse $INFO[System.AddonVersion(skin.aeon.fuse)]'),
             ('$LOCALIZE[31650]', '$INFO[Network.IPAddress]'), ('$LOCALIZE[31651]', '$INFO[System.ScreenResolution]'),
             ('$LOCALIZE[31794]', '$VAR[Aeon_Uptime]')]
HUB_ICON = '$INFO[Container(9000).ListItem.Property(icon)]'


def hub_row(w, focused, spine=0, value_w=0):
    fc = 'Control.HasFocus(9000)'
    out = []
    if spine:
        out.append(img(0, 0, spine, R, BOX))
    if focused:
        out.append(img(0, 0, w, R, 'aeon_white', fc))
    if not spine:
        out.append('<control type="image"><left>0</left><top>0</top><width>%d</width><height>%d</height>'
                   '<texture border="24,0,24,0" colordiffuse="16ffffff">aeon/ms/rowline.png</texture>%s</control>'
                   % (w, R, vis('!' + fc) if focused else ''))
    if spine:
        ix = (spine - 32) // 2
        out.append(icon(ix, 20, 32, '$INFO[ListItem.Property(icon)]', 'ffffffff', ('!' + fc) if focused else None))
        if focused:
            out.append(icon(ix, 20, 32, '$INFO[ListItem.Property(icon)]', 'aeon_onbar', fc))
    x = spine + 32
    lw = (w - value_w - x - 16) if value_w else (w - x - 300)
    out.append(lab(x, 0, lw, R, '$INFO[ListItem.Label]', 'ui_26', W1, cond=('!' + fc) if focused else None))
    if focused:
        out.append(lab(x, 0, lw, R, '$INFO[ListItem.Label]', 'ui_26_semibold', 'aeon_onbar', cond=fc))
    vx, vw = ((w - value_w + 24), value_w - 52) if value_w else (w - 300, 272)
    out.append(lab(vx, 0, vw, R, '$INFO[ListItem.Label2]', 'ui_22', W2, align='right', cond=('!' + fc) if focused else None))
    if focused:
        out.append(lab(vx, 0, vw, R, '$INFO[ListItem.Label2]', 'ui_22', 'aeon_onbar', align='right', cond=fc))
    return ''.join(out)


def hub_list(x, y, w, spine=0, value_w=0):
    return ('<control type="list" id="9000"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
            '<onback>SetProperty(aeon.fromsys,1,home)</onback><onback>ActivateWindow(home)</onback>'
            '<onup>9000</onup><ondown>9000</ondown><onleft>noop</onleft><onright>noop</onright>'
            '<scrolltime tween="cubic" easing="out">200</scrolltime>'
            '<itemlayout width="%d" height="%d">%s</itemlayout><focusedlayout width="%d" height="%d">%s</focusedlayout>'
            '<include>Aeon_SettingsItems</include></control>'
            % (x, y, w, HROWS * R, w, R, hub_row(w, False, spine, value_w), w, R, hub_row(w, True, spine, value_w)))


def hub_tile(x, y, w, h, color='x_deep'):
    """the focused entry's own glyph: the joining tile"""
    return img(x, y, w, h, color) + icon(x + (w - 64) // 2, y + (h - 64) // 2, 64, HUB_ICON, 'ffffffff')


def hub_facts(x, y, w, keyw=170):
    """"This box" on the row grid: a caption row, then one fact a row"""
    out = lab(x, y, w, R, '[UPPERCASE]$LOCALIZE[31269][/UPPERCASE]', 'cap_20', W3)
    for i, (k, v) in enumerate(HUB_FACTS):
        out += lab(x, y + (i + 1) * R, keyw, R, '[UPPERCASE]%s[/UPPERCASE]' % k, 'cap_16', W3)
        out += lab(x + keyw, y + (i + 1) * R, w - keyw, R, v, 'ui_24', W1)
    return out


def hub_help(x, y, w, h):
    return textbox(x, y, w, h // PLOT_LINE * PLOT_LINE, '$INFO[Container(9000).ListItem.Property(help)]', 'body_24', W2)


def hub_pos():
    return '$INFO[Container(9000).CurrentItem]$INFO[Container(9000).NumItems, / ,]'


def hub_mosaic():
    LW, IW = 800, 560
    x0 = (1920 - LW - IW) // 2
    ly = HY0 + 2 * R
    o = title_box(x0, HY0, LW, BOX, '$LOCALIZE[31000]', '$LOCALIZE[5]', count=hub_pos())
    # the band beside the title: what the focused entry holds
    o += img(x0 + LW, HY0, IW, 2 * R, 'x_deep') + lab(x0 + LW + 32, HY0 + 22, IW - 64, 30, '[UPPERCASE]$INFO[Container(9000).ListItem.Label2][/UPPERCASE]', 'cap_20', W3)
    o += lab(x0 + LW + 32, HY0 + 52, IW - 64, 64, '$INFO[Container(9000).ListItem.Label]', 'font37', 'ffffffff')
    o += img(x0, ly, LW, HROWS * R, 'x_panel') + img(x0 + LW, ly, IW, HROWS * R, 'x_raised')
    o += hub_tile(x0 + LW, ly, 3 * R, 3 * R)
    o += hub_help(x0 + LW + 3 * R + 28, ly + 16, IW - 3 * R - 56, 5 * R - 16)
    o += hub_facts(x0 + LW + 32, ly + 5 * R, IW - 64)
    return o + hub_list(x0, ly, LW)


def hub_ledger():
    SP, LC, VC, IW = 96, 520, 340, 460
    x0 = (1920 - SP - LC - VC - IW) // 2
    ly = HY0 + 2 * R
    o = hub_tile(x0, HY0, SP, 2 * R, BOX)
    o += title_box(x0 + SP, HY0, LC + VC, 'x_deep', '$LOCALIZE[31000]', '$LOCALIZE[5]', kicker_color=W3, count=hub_pos())
    o += img(x0 + SP + LC + VC, HY0, IW, 2 * R, 'x_raised') + lab(x0 + SP + LC + VC + 32, HY0, IW - 64, 2 * R, '$INFO[Container(9000).ListItem.Label]', 'ui_30_semibold', 'ffffffff')
    # four columns on one grid: spine, name, what it holds, the entry's help and this box
    o += img(x0, ly, SP, HROWS * R, BOX) + img(x0 + SP, ly, LC, HROWS * R, 'x_panel') + img(x0 + SP + LC, ly, VC, HROWS * R, 'x_raised')
    ix = x0 + SP + LC + VC
    o += img(ix, ly, IW, HROWS * R, 'x_panel')
    o += hub_help(ix + 28, ly + 16, IW - 56, 5 * R - 16)
    o += hub_facts(ix + 28, ly + 5 * R, IW - 56, keyw=150)
    return o + hub_list(x0, ly, SP + LC + VC, spine=SP, value_w=VC)


def hub_bridge():
    TW, PW, LW, IW = 640, 192, 720, 480
    x0 = (1920 - PW - LW - IW) // 2
    ly = HY0 + 2 * R
    o = title_box(x0, HY0, TW, BOX, '$LOCALIZE[31000]', '$LOCALIZE[5]')
    o += hub_tile(x0, ly, PW, 3 * R, 'x_raised')
    o += img(x0 + PW, ly, LW, HROWS * R, 'x_panel')
    ix = x0 + PW + LW
    # the step: the count on the list's first row, the info box one row lower with the focused row carried across
    o += img(ix, ly, 240, R, 'x_deep') + lab(ix + 28, ly, 200, R, hub_pos(), 'num_22', W2)
    o += img(ix, ly + R, IW, (HROWS - 1) * R, 'x_raised')
    for i in range(1, HROWS):
        o += img(ix, ly + i * R, IW, R, '28ffffff', 'Integer.IsEqual(Container(9000).Position,%d)' % i)
    o += lab(ix + 28, ly + R, IW - 56, R, '$INFO[Container(9000).ListItem.Label]', 'ui_30_semibold', 'ffffffff')
    o += hub_help(ix + 28, ly + 2 * R + 8, IW - 56, 3 * R - 8)
    o += hub_facts(ix + 28, ly + 5 * R, IW - 56)
    return o + hub_list(x0 + PW, ly, LW)


def hub_tabslab():
    SW, AW, TAB = 820, 460, 260
    x0 = (1920 - SW - AW) // 2
    o = img(x0, HY0, TAB, R, BOX) + lab(x0, HY0, TAB, R, '[UPPERCASE]$LOCALIZE[31000][/UPPERCASE]', 'cap_20', 'ffffffff', align='center')
    o += img(x0 + TAB, HY0, SW - TAB, R, 'x_deep') + lab(x0 + TAB + 24, HY0, SW - TAB - 48, R, hub_pos(), 'num_22', W3, align='right')
    o += img(x0, HY0 + R, SW, R, BOX) + lab(x0 + 32, HY0 + R, SW - 64, R, '$LOCALIZE[5]', 'ui_30_semibold', 'ffffffff')
    ly = HY0 + 2 * R
    o += img(x0, ly, SW, HROWS * R, 'x_panel')
    # the art panel hangs beside the tabs and the slab: the focused entry's glyph and name, its help, this box
    ax = x0 + SW
    o += hub_tile(ax, HY0, AW, 3 * R)
    o += lab(ax + 28, HY0 + 3 * R - 64, AW - 56, 56, '$INFO[Container(9000).ListItem.Label]', 'ui_30_semibold', 'ffffffff')
    o += img(ax, HY0 + 3 * R, AW, (HROWS - 1) * R, 'x_raised')
    o += hub_help(ax + 28, HY0 + 3 * R + 16, AW - 56, 3 * R - 16)
    o += hub_facts(ax + 28, ly + 5 * R, AW - 56)
    return o + hub_list(x0, ly, SW)


BODY['Hub'] = {'mosaic': hub_mosaic, 'ledger': hub_ledger, 'bridge': hub_bridge, 'tabslab': hub_tabslab}


# ---------------------------------------------------------------------------------------------------------------
# Keyboard (DialogKeyboard) and number pad (DialogNumeric), 0.55.0: the boards "Keyboard and number pad" on the Aeon
# menus page (skin.glass/mockups/aeon-menus). Every key is a flush cell of x_raised on an x_panel ground (1 px of the
# ground shows between cells), the focused key is the white bar with aeon_onbar ink, OK / Done have the palette colour.
# Kodi's ids stay. Keyboard: heading 311, field 312 (edit), Chinese input 313 / 314, letter keys 100 + 20 x row + column
# (Kodi fills each row from the left and hides the keys a layout does not use), Shift 302, Caps 303, Symbols 304 (radio
# buttons: Kodi marks the modes that are on; the skin paints an "on" mode in the palette colour), Space 32, cursor
# 305 / 306, Delete 8, OK 300, Cancel 301, layout 309, IP address 307, show password 310 (password input only).
# Number pad: heading 1, field 4 (Kodi draws the part of a time / date / IP address being typed in textcolor and the
# rest in disabledcolor; it does not say which part it is, so the boards' "Part 4 of 4" note is left out), digits
# 10-19, previous 20, Done 21, next 22, Delete 23.
# Navigation comes from the cells' places (the closest cell that way, wrapping at the edges, as on the boards). A target
# Kodi may hide gets fall-backs: the last key Kodi shows in that row, or the next cell, so focus never lands on a
# hidden key.
KW, KCOLS, KROWS = 96, 13, 4
KGW = KW * KCOLS               # 1248
KSW = 352
PKW, PGW, PSW = 160, 3 * 160, 320
KROW_GROUP = 78510             # + row: the letter rows' groups (Ledger's spine asks ControlGroup(...).HasFocus())
K_HIDEABLE = (307, 309, 310, 20, 22)
K_ROWMIN = {0: 10, 1: 4, 2: 5, 3: 0}   # keys Kodi always shows per letter row (shortest rows of its layouts)
K_FONT = {'key': 'ui_28', 'fn': 'cap_20', 'radio': 'cap_20', 'arrow': 'ui_26', 'side': 'ui_24_semibold', 'on': 'ui_24_bold',
          'digit': 'ui_30_semibold'}
KB_KICKER = '$LOCALIZE[10103]'   # Kodi: Virtual keyboard
PAD_KICKER = '$LOCALIZE[10109]'  # Kodi: Numeric input


def kcell(cid, x, y, w, h, kind, label='', **more):
    d = dict(id=cid, x=x, y=y, w=w, h=h, kind=kind, label=label)
    d.update(more)
    return d


def kb_keys(gx, gy, modes=True):
    """the four letter rows and the row of function keys under them (without the modes when they are tabs)"""
    cells = [kcell(100 + 20 * r + c, gx + c * KW, gy + r * R, KW, R, 'key', row=r, col=c) for r in range(KROWS) for c in range(KCOLS)]
    row = ([(304, 2, 31040), (303, 2, 31041), (302, 2, 31042), (32, 3, 31043)] if modes else [(32, 9, 31043)])
    row += [(305, 1, u'←'), (306, 1, u'→'), (8, 2, 31044)]
    cx = gx
    for cid, u, label in row:
        kind = 'radio' if cid in (302, 303, 304) else 'arrow' if cid in (305, 306) else 'fn'
        cells.append(kcell(cid, cx, gy + KROWS * R, u * KW, R, kind,
                           label if kind == 'arrow' else '[UPPERCASE]$LOCALIZE[%d][/UPPERCASE]' % label))
        cx += u * KW
    return cells


def pad_keys(gx, gy):
    rows = [[(11, 12311), (12, 12312), (13, 12313)], [(14, 12314), (15, 12315), (16, 12316)],
            [(17, 12317), (18, 12318), (19, 12319)], [(20, u'←'), (10, 12310), (22, u'→')]]
    cells = []
    for r, keys in enumerate(rows):
        for c, (cid, label) in enumerate(keys):
            arrow = not isinstance(label, int)
            cells.append(kcell(cid, gx + c * PKW, gy + r * R, PKW, R, 'arrow' if arrow else 'digit',
                               label if arrow else '$LOCALIZE[%d]' % label))
    return cells


def side_cells(x, y, w, rows, pad, spare=False):
    """the dialog's buttons beside the keys, one row each (Done two), from the top; returns (ground, cells).
    The keyboard: OK, Cancel, layout, IP address, show password. The pad: Delete, (a spare deep cell), Done."""
    spec = ([(23, 1, '$LOCALIZE[31044]', 'side')] + ([(None, 1, '', '')] if spare else []) + [(21, 2, '$LOCALIZE[20177]', 'on')]
            if pad else [(300, 1, '$LOCALIZE[12321]', 'on'), (301, 1, '$LOCALIZE[222]', 'side'), (309, 1, '', 'side'),
                         (307, 1, '$LOCALIZE[1006]', 'side'), (310, 1, '', 'side')])
    o, cells, cy = img(x, y, w, rows * R, 'x_deep'), [], y
    for cid, n, label, kind in spec:
        if cid is not None:
            o += img(x, cy, w, n * R, 'x_panel', 'Control.IsVisible(%d)' % cid if cid in K_HIDEABLE else None)
            cells.append(kcell(cid, x, cy, w, n * R, kind, label))
        cy += n * R
    return o, cells


def key_field(x, y, w, h, pad, size):
    """the text being typed in a deep box: the keyboard's edit control, the pad's label (centred)"""
    o = img(x, y, w, h, 'x_deep')
    font = {44: 'hd_display_48', 40: 'hd_display_40', 32: 'ui_30_semibold'}[size]
    if pad:
        return o + ('<control type="label" id="4"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><align>center</align>'
                    '<aligny>center</aligny><font>%s</font><textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor>'
                    '<disabledcolor>%s</disabledcolor></control>' % (x, y, w, h, font, W3))
    o += ('<control type="edit" id="312"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><font>%s</font>'
          '<textcolor>%s</textcolor><align>left</align><aligny>center</aligny><textoffsetx>0</textoffsetx><texturefocus />'
          '<texturenofocus /></control>' % (x + 32, y, w - 64, h, font, W1))
    # Chinese input (code and candidates): small, on the field's right
    for cid, ly in ((313, y + 4), (314, y + h - 30)):
        o += ('<control type="label" id="%d"><left>%d</left><top>%d</top><width>%d</width><height>26</height><align>right</align>'
              '<font>small_20</font><textcolor>%s</textcolor></control>' % (cid, x + w // 2, ly, w // 2 - 32, W2))
    return o


def key_title(x, y, w, color, pad, kicker_color=CAP_ON_BOX):
    o = img(x, y, w, 2 * R, color)
    o += lab(x + 32, y + 22, w - 64, 30, '[UPPERCASE]%s[/UPPERCASE]' % (PAD_KICKER if pad else KB_KICKER), 'cap_20', kicker_color)
    return o + heading(x + 32, y + 52, w - 64, 64, 'font37', 1 if pad else 311)


# -- navigation ---------------------------------------------------------------------------------------------------
def k_candidates(cells, s, d):
    """best first: the cells that way in the same row / column, then (wrapping) the far end of that row / column, then
    the closest cells that way outside it"""
    x, y, w, h = s['x'], s['y'], s['w'], s['h']
    line, off = [], []
    for c in cells:
        if c is s:
            continue
        cx, cy, cw, ch = c['x'], c['y'], c['w'], c['h']
        vo, ho = cy < y + h and cy + ch > y, cx < x + w and cx + cw > x
        dx, dy = abs(cx + cw / 2.0 - x - w / 2.0), abs(cy + ch / 2.0 - y - h / 2.0)
        sc, inline = None, ho
        if d == 'right' and cx >= x + w - 1:
            sc, inline = (cx - x - w) * 10 + dy, vo
        elif d == 'left' and cx + cw <= x + 1:
            sc, inline = (x - cx - cw) * 10 + dy, vo
        elif d == 'down' and cy >= y + h - 1:
            sc = (cy - y - h) * 10 + dx
        elif d == 'up' and cy + ch <= y + 1:
            sc = (y - cy - ch) * 10 + dx
        if sc is not None:
            (line if inline else off).append((sc, c))
    line.sort(key=lambda t: t[0])
    off.sort(key=lambda t: t[0])
    out = [c for _, c in line]
    if d in ('left', 'right'):
        far = [c for c in cells if c is not s and c['y'] < y + h and c['y'] + c['h'] > y]
        far.sort(key=lambda c: c['x'] if d == 'right' else -(c['x'] + c['w']))
    else:
        far = [c for c in cells if c is not s and c['x'] < x + w and c['x'] + c['w'] > x]
        far.sort(key=lambda c: c['y'] if d == 'down' else -(c['y'] + c['h']))
    out += [c for c in far if c not in out]
    return out + [c for _, c in off if c not in out]


def k_nav(cells, s, d):
    """[(condition, id)]: the first one that holds is where focus goes. Kodi's layouts fill each letter row from the
    left; K_ROWMIN keys of a row are always there (every layout in Kodi 22 has them), the rest may be hidden and the
    fourth row may be empty (Italian symbols)."""
    by_id = dict((c['id'], c) for c in cells)
    out, neg, done_rows = [], [], set()
    for c in k_candidates(cells, s, d):
        if c['kind'] == 'key':
            r = c['row']
            if r in done_rows:
                continue
            same = s['kind'] == 'key' and r == s['row']
            if same and c['col'] < s['col']:
                return out + [(' + '.join(neg), c['id'])]          # keys to the left are always there
            if same and d == 'right':
                if c['col'] != s['col'] + 1:
                    continue                                       # past a hidden key the rest of the row is hidden too
                if c['col'] < K_ROWMIN[r]:
                    return out + [(' + '.join(neg), c['id'])]
                out.append((' + '.join(neg + ['Control.IsVisible(%d)' % c['id']]), c['id']))
                neg.append('!Control.IsVisible(%d)' % c['id'])
                continue                                           # then the side, or round to the row's first key
            # the key in that column, else the last key Kodi shows in that row (Left wrapping round: the row's last
            # key, at worst the source itself), else past the row
            floor = s['col'] if same else -1
            row = [by_id[100 + 20 * r + k] for k in range(c['col'], -1, -1)]
            for i, k in enumerate(row):
                cond = neg + (['!Control.IsVisible(%d)' % row[i - 1]['id']] if i else [])
                if k['col'] < K_ROWMIN[r] or k['col'] <= floor:
                    return out + [(' + '.join(cond), k['id'])]
                out.append((' + '.join(cond + ['Control.IsVisible(%d)' % k['id']]), k['id']))
            neg = neg + ['!Control.IsVisible(%d)' % row[-1]['id']]
            done_rows.add(r)
            continue
        if c['id'] in K_HIDEABLE:
            out.append((' + '.join(neg + ['Control.IsVisible(%d)' % c['id']]), c['id']))
            neg.append('!Control.IsVisible(%d)' % c['id'])
            continue
        return out + [(' + '.join(neg), c['id'])]
    return out


def k_navxml(cells, s):
    o = ''
    for d in ('left', 'right', 'up', 'down'):
        nav = k_nav(cells, s, d)
        if not nav:
            o += '<on%s>noop</on%s>' % (d, d)
        for cond, cid in nav:
            o += ('<on%s condition="%s">%d</on%s>' % (d, esc(cond), cid, d)) if cond else '<on%s>%d</on%s>' % (d, cid, d)
    return o


def radio_fill(w, h):
    name = 'aeon/ms/fill_%dx%d.png' % (w, h)
    path = os.path.join('media', *name.split('/'))
    if not os.path.exists(path):
        from PIL import Image
        Image.new('RGBA', (w, h), (255, 255, 255, 255)).save(path)
        print('wrote', path)
    return name


def k_button(c, nav):
    """one flush cell: x_raised (OK / Done: the palette colour), the white bar when focused. A mode key is a radio button
    whose "on" picture fills the cell in the palette colour; its name is a label on top (the picture covers the button's)."""
    kind, w, h = c['kind'], c['w'] - 1, c['h'] - (0 if c.get('tab') else 1)
    radio = kind == 'radio'
    ink = W2 if kind in ('fn', 'radio') else 'ffffffff' if kind == 'on' else W1
    o = ('<control type="%s" id="%d"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><font>%s</font>'
         '<align>center</align><aligny>center</aligny><textoffsetx>0</textoffsetx><textcolor>%s</textcolor>'
         '<focusedcolor>aeon_onbar</focusedcolor><disabledcolor>55ffffff</disabledcolor><pulseonselect>false</pulseonselect>'
         '<texturefocus colordiffuse="aeon_white">common/white.png</texturefocus>'
         '<texturenofocus colordiffuse="%s">common/white.png</texturenofocus>'
         % ('radiobutton' if radio else 'button', c['id'], c['x'], c['y'], w, h, K_FONT[kind], ink,
            BOX if kind == 'on' else 'x_raised'))
    if radio:
        # radioposx 0 would put the picture at Kodi's default place (the right end), so a hair past 0. Kodi keeps a radio
        # picture's aspect ratio, so the "on" fill is a white picture of the cell's own size (written here when missing).
        tex = radio_fill(w, h)
        o += ('<radiowidth>%d</radiowidth><radioheight>%d</radioheight><radioposx>0.01</radioposx>'
              '<textureradioonfocus colordiffuse="aeon_white">%s</textureradioonfocus>'
              '<textureradioonnofocus colordiffuse="$VAR[Aeon_BoxAccent]">%s</textureradioonnofocus>'
              '<textureradioofffocus /><textureradiooffnofocus />' % (w, h, tex, tex))
    elif c['label']:
        o += '<label>%s</label>' % esc(c['label'])
    o += nav + '</control>'
    if radio:
        o += lab(c['x'], c['y'], w, h, c['label'], K_FONT[kind], 'aeon_onbar', 'center', 'Control.HasFocus(%d)' % c['id'])
        o += lab(c['x'], c['y'], w, h, c['label'], K_FONT[kind], ink, 'center', '!Control.HasFocus(%d)' % c['id'])
    return o


def k_emit(cells):
    """the cells as Kodi controls (the letter rows in groups, one per row), each with its navigation"""
    o, rows = '', {}
    for c in cells:
        x = k_button(c, k_navxml(cells, c))
        if c['kind'] == 'key':
            rows.setdefault(c['row'], []).append(x)
        else:
            o += x
    for r in sorted(rows):
        o = '<control type="group" id="%d">%s</control>' % (KROW_GROUP + r, ''.join(rows[r])) + o
    return o


def k_ground(x, y, w, rows):
    return img(x, y, w, rows * R, 'x_panel')


def k_wrap(w, h, inner, pad, top=None):
    """the dim and the menu centred on the screen; the keyboard steps aside while the IP address pad is up"""
    g = '<control type="group"><left>%d</left><top>%d</top>\n%s\n</control>' % ((1920 - w) // 2, (1080 - h) // 2 if top is None else top, inner)
    return DIM + g if pad else '<control type="group">%s%s%s</control>' % (vis('!Window.IsVisible(numericinput)'), DIM, g)


def spine_marks(x, w, cells, y0, y1):
    """Ledger: the spine cell of the focused row turns white and points at the row"""
    o = ''
    for y in sorted(set(c['y'] for c in cells if y0 <= c['y'] < y1)):
        conds = []
        for c in cells:
            if c['y'] != y:
                continue
            cond = 'ControlGroup(%d).HasFocus()' % (KROW_GROUP + c['row']) if c['kind'] == 'key' else 'Control.HasFocus(%d)' % c['id']
            if cond not in conds:
                conds.append(cond)
        cond = ' | '.join(conds)
        o += img(x, y, w, R, 'aeon_white', cond) + lab(x, y, w, R, u'›', 'font37', 'aeon_onbar', 'center', cond)
    return o


# A: the title box and the field are the top band; the keys and the buttons meet under them
def keys_mosaic(pad):
    gw, sw, rows = (PGW, PSW, 4) if pad else (KGW, KSW, KROWS + 1)
    tw = gw if pad else 5 * KW
    o = key_title(0, 0, tw, BOX, pad)
    o += key_field(tw, 0, gw + sw - tw, 2 * R, pad, 40 if pad else 44)
    cells = pad_keys(0, 2 * R) if pad else kb_keys(0, 2 * R)
    g, side = side_cells(gw, 2 * R, sw, rows, pad, spare=True)
    o += k_ground(0, 2 * R, gw, rows) + g + k_emit(cells + side)
    return k_wrap(gw + sw, (2 + rows) * R, o, pad)


# B: a spine in the palette colour runs down the field row and every key row; the focused row's spine cell starts the bar
def keys_ledger(pad):
    gw, sw, rows = (PGW, PSW, 4) if pad else (KGW, KSW, KROWS + 1)
    sp = 96
    o = img(0, 0, sp, 2 * R, 'x_raised') + icon(26, 50, 44, 'aeon/icons/%s.png' % ('grid' if pad else 'search'), W1)
    o += key_title(sp, 0, gw + sw, 'x_deep', pad, W3)
    o += img(0, 2 * R, sp, (1 + rows) * R, BOX)
    o += key_field(sp, 2 * R, gw + sw, R, pad, 32)
    cells = pad_keys(sp, 3 * R) if pad else kb_keys(sp, 3 * R)
    g, side = side_cells(sp + gw, 3 * R, sw, rows, pad, spare=True)
    o += k_ground(sp, 3 * R, gw, rows) + g + k_emit(cells + side)
    o += spine_marks(0, sp, cells + side, 3 * R, (3 + rows) * R)
    return k_wrap(sp + gw + sw, (3 + rows) * R, o, pad)


# C: stairs. Title, then the field one row down and across, the keys under the title, the buttons one more row down
# and out past the keys. The row the field leaves under the title names the keyboard layout (the pad leaves it plain).
def keys_bridge(pad):
    gw, sw, rows = (PGW, PSW, 4) if pad else (KGW, KSW, KROWS + 1)
    tw = gw if pad else 640
    o = key_title(0, 0, tw, BOX, pad)
    o += key_field(tw, R, gw + sw - tw, 2 * R, pad, 40 if pad else 44)
    o += img(0, 2 * R, tw, R, 'x_deep')
    if not pad:
        o += lab(32, 2 * R, tw - 64, R, '[UPPERCASE]$INFO[Control.GetLabel(309)][/UPPERCASE]', 'cap_20', W3)
    cells = pad_keys(0, 3 * R) if pad else kb_keys(0, 3 * R)
    g, side = side_cells(gw, 4 * R, sw, rows - 1, pad)
    o += k_ground(0, 3 * R, gw, rows) + g + k_emit(cells + side)
    return k_wrap(gw + sw, (3 + rows) * R, o, pad)


# D: the dialog's name is the first tab and flows into the slab; on the keyboard the modes (Symbols, Caps, Shift) are
# tabs beside it and a mode that is on takes the slab's colour. The field and the keys sit in the slab 24 px in; the
# buttons hang beside the tabs and the slab, touching both.
def keys_tabslab(pad):
    gw, sw, rows = (PGW, PSW, 4) if pad else (KGW, KSW, KROWS + 1)
    slw, kt = gw + 48, 320
    tabs = [] if pad else [kcell(cid, kt + i * 192, 0, 192, R, 'radio', '[UPPERCASE]$LOCALIZE[%d][/UPPERCASE]' % s, tab=True)
                           for i, (cid, s) in enumerate(((304, 31040), (303, 31041), (302, 31042)))]
    tx = kt + 192 * len(tabs)
    o = img(0, 0, tx, R, 'x_panel') + img(0, 0, kt - (1 if tabs else 0), R, BOX)
    o += lab(16, 0, kt - 32, R, '[UPPERCASE]%s[/UPPERCASE]' % (PAD_KICKER if pad else KB_KICKER), 'cap_20', 'ffffffff', 'center')
    o += img(tx, 0, slw - tx, R, 'x_deep')
    o += img(0, R, slw, (2 + rows) * R + 24, BOX)
    o += heading(32, R, slw - 64, R, 'ui_30_semibold', 1 if pad else 311)
    o += key_field(24, 2 * R, gw, R, pad, 32)
    cells = pad_keys(24, 3 * R) if pad else kb_keys(24, 3 * R, modes=False)
    g, side = side_cells(slw, 0, sw, 3 + rows, pad)
    o += k_ground(24, 3 * R, gw, rows) + g + img(slw, (3 + rows) * R, sw, 24, 'x_deep')
    o += k_emit(tabs + cells + side)
    return k_wrap(slw + sw, (3 + rows) * R + 24, o, pad)


BODY['Kb'] = {s: (lambda f: (lambda: f(False)))(f) for s, f in
              (('mosaic', keys_mosaic), ('ledger', keys_ledger), ('bridge', keys_bridge), ('tabslab', keys_tabslab))}
BODY['Num'] = {s: (lambda f: (lambda: f(True)))(f) for s, f in
               (('mosaic', keys_mosaic), ('ledger', keys_ledger), ('bridge', keys_bridge), ('tabslab', keys_tabslab))}


def main():
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<!-- GENERATED by _src/ms_menus.py: the Aeon theme\'s menu styles (Menu theme Mosaic / Ledger / Bridge / Tab slab).',
           '     Do not edit by hand; change the script and run it again. -->',
           '<includes>']
    out.extend(HEAD)
    for win, styles in BODY.items():
        for s in STYLES:
            out.append(include('MS_%s_%s' % (win, s), styles[s]()))
    out.append('</includes>\n')
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
    print(OUT, os.path.getsize(OUT))


if __name__ == '__main__':
    main()
