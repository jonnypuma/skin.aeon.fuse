# -*- coding: utf-8 -*-
"""0.47.0+ Fused Glass library views, redrawn after the approved mockups (canvas "Fused Glass library views",
skin.glass/mockups/fused-library-views). Run from the skin folder; safe to run again (rewrites its own block).

One language for every view: a header (kicker + title at x 96 / y 40, the view and sort order in a quiet capsule at the
right), a 64-wide glass rail at the right edge (the clock at the top, the A-Z jump list, the item count at the bottom),
glass cards, white focus rows with dark ink, the gold ring on art in focus, and one rule for watched marks on every
media type: nothing watched = gold dot, part watched = progress ring (a film or episode: how far it is played; a show
or season: its episodes; a set: its films), all watched = tick.

Watched marks and clearlogo titles follow View settings per view and media type (aeon.vo.watched / rings / logos:
'' = the global setting, on, off): the dots and ticks the global Watched indicators (aeon.watchedmarkers), the rings
are on unless a view turns them off, the clearlogo the global Logos instead of titles (aeon.nologos).

Phase 1 (0.47.0): the shared parts and the List view (510) for films, sets, TV shows, seasons and episodes. Each
redrawn view is a complete Fused Glass include (FG_V<id>_View) that the view's include loads instead of its Aeon one
when the skin starts in Fused Glass (a theme change reloads the skin); the Aeon views are left as they were."""
import io
import os
import re

from PIL import Image, ImageDraw

FUSED = '1080i/Includes_Fused.xml'
VIDEO = '1080i/Includes_Aeon_Video.xml'
VIEWS2 = '1080i/Includes_Aeon_Views2.xml'
VIEWS3 = '1080i/Includes_Aeon_Views3.xml'
MUSICLIB = '1080i/Includes_Aeon_MusicLib.xml'
FONT = '1080i/Font.xml'
FG = '$EXP[Aeon_FGlass]'
A = '$ADDON[skin.aeon.fuse %d]'
INK = 'aeon_onbar'                 # the dark ink on white
MARK = 'fg_mark'                   # the gold accent
TICK = 'e6ffffff'                  # 0.56.8 the watched tick is white (the user: "white is better" than green)
TICK_ON_WHITE = 'ff0f1115'


# ------------------------------------------------------------------------------------------------------------ textures
def rounded_mask(w, h, r):
    p = os.path.join('media', 'fg', 'm%dx%d.png' % (w, h))
    im = Image.new('L', (w * 4, h * 4), 0)
    ImageDraw.Draw(im).rounded_rectangle([0, 0, w * 4 - 1, h * 4 - 1], r * 4, fill=255)
    out = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    out.putalpha(im.resize((w, h), Image.LANCZOS))
    out.save(p, optimize=True)


def ring_textures():
    """media/fg/ring: t.png (the full track) and a0..a100.png (the arc of that many percent from 12 o'clock, round
    ends), white, 80 x 80 with a 7 px stroke; the skin tints them (track grey, arc gold)."""
    d = os.path.join('media', 'fg', 'ring')
    os.makedirs(d, exist_ok=True)
    S, sw = 320, 28                                   # 4x
    box = [sw // 2, sw // 2, S - sw // 2 - 1, S - sw // 2 - 1]
    track = Image.new('L', (S, S), 0)
    ImageDraw.Draw(track).ellipse(box, outline=255, width=sw)
    save_white(track, os.path.join(d, 't.png'))
    import math
    for pct in range(0, 101):
        im = Image.new('L', (S, S), 0)
        if pct:
            dr = ImageDraw.Draw(im)
            start, end = -90, -90 + 360 * pct / 100
            dr.arc(box, start, end, fill=255, width=sw)
            rr = (S - sw) / 2 - 0.5
            for ang in (start, end):
                cx = S / 2 + rr * math.cos(math.radians(ang))
                cy = S / 2 + rr * math.sin(math.radians(ang))
                dr.ellipse([cx - sw / 2, cy - sw / 2, cx + sw / 2, cy + sw / 2], fill=255)
        save_white(im, os.path.join(d, 'a%d.png' % pct))


def save_white(mask, path):
    out = Image.new('RGBA', mask.size, (255, 255, 255, 0))
    out.putalpha(mask)
    out.resize((80, 80), Image.LANCZOS).save(path, optimize=True)


# ------------------------------------------------------------------------------------------------------------ xml parts
def img(x, y, w, h, tex, col=None, border=None, vis=None, diffuse=None, aspect=None, extra='', bg=False, align=None, aligny=None):
    t = '<texture%s%s%s%s>%s</texture>' % (' border="%s"' % border if border is not None else '', ' colordiffuse="%s"' % col if col else '',
                                           ' diffuse="%s"' % diffuse if diffuse else '', ' background="true"' if bg else '', tex)
    at = (' scalediffuse="false"' if diffuse else '') + (' align="%s"' % align if align else '') + (' aligny="%s"' % aligny if aligny else '')
    a = '<aspectratio%s>%s</aspectratio>' % (at, aspect) if aspect else ''
    v = '<visible>%s</visible>' % vis if vis else ''
    return '<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>%s%s%s%s</control>' % (x, y, w, h, a, t, v, extra)


def lbl(x, y, w, h, label, font, col='ffffffff', align='left', vis=None, extra='', sel=True, aligny='center'):
    s = '<selectedcolor>%s</selectedcolor>' % col if sel else ''
    v = '<visible>%s</visible>' % vis if vis else ''
    return ('<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><align>%s</align><aligny>%s</aligny>'
            '<font>%s</font><textcolor>%s</textcolor>%s<label>%s</label>%s%s</control>' % (x, y, w, h, align, aligny, font, col, s, label, v, extra))


def textbox(x, y, w, h, label, font, col='d9ffffff', vis=None, scroll=True):
    v = '<visible>%s</visible>' % vis if vis else ''
    a = '<autoscroll delay="8000" time="2000" repeat="8000">true</autoscroll>' if scroll else ''
    return '<control type="textbox"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><font>%s</font><textcolor>%s</textcolor><label>%s</label>%s%s</control>' % (
        x, y, w, h, font, col, label, a, v)


def glass(x, y, w, h, r=28, shadow=True):
    """A frosted card: drop shadow, tint, hairline edge (fg_material.py turns fg_frost / fg_edge into its $VARs)."""
    out = ''
    if shadow:
        out += img(x - 40, y - 40, w + 80, h + 80, 'fg/sh28.png', '$VAR[FG_PanelSh_8c]', 68)
    out += img(x, y, w, h, 'fg/r%d.png' % r, 'fg_frost', r) + img(x, y, w, h, 'fg/e%d.png' % r, 'fg_edge', r)
    return out


CHIP_PAD = 6          # 0.56.10: the label 6 px inside the chip's outline (the user: "some labels inside chips clip the outline")


def chip(x, y, w, label, vis, ink='ffffffff', edge='66ffffff', h=26, font='lb_cap_14'):
    return (img(x, y, w, h, 'fg/e8.png', edge, 8, vis) + lbl(x + CHIP_PAD, y, w - 2 * CHIP_PAD, h, label, font, ink, 'center', vis))


CHIP_SETS = (((52, 112, 66, 64, 100), 6), ((48, 112, 60, 56, 88), 4), ((48, 112, 60, 56), 4), ((48, 112, 60), 4), ((48, 112), 4))


def chip_set(room):
    """the widest chip set (widths, gap) that fits in room px: all five, smaller, then without HDR, the certificate..."""
    for widths, gap in CHIP_SETS:
        if sum(widths) + gap * (len(widths) - 1) <= room:
            return widths, gap
    return CHIP_SETS[-1]


def row_chips(x, y, h=26, ink='ffffffff', edge='66ffffff', ep_only=False, widths=(52, 112, 66, 64, 72), gap=6, font='lb_cap_14', limit=None):
    """The media chips of a list row's item at (x, y): resolution, audio, aspect ratio, certificate, HDR (0.56.8, the list
    row rule: films and episodes alike, in this order; HDR last, so an item without it leaves no gap). Kodi takes no
    buttons or grouplists in list rows, so the chips have fixed widths and places. limit: the x the chips must end
    before; the row gets as many as fit (chip_set), the aspect ratio in every row. ep_only is kept for the callers."""
    if limit is not None:
        widths, gap = chip_set(limit - x)
    vid ='[String.IsEqual(ListItem.DBType,episode) | String.IsEqual(ListItem.DBType,movie) | String.IsEqual(ListItem.DBType,musicvideo)]'
    media = '!String.IsEmpty(ListItem.VideoResolution) + $EXP[Aeon_VOMedia]'
    parts = (('$VAR[Aeon_ResChip]', media),
             ('$VAR[FG_EcAudio]', media + ' + !String.IsEmpty(ListItem.AudioCodec)'),
             ('$INFO[ListItem.VideoAspect]:1', '%s + !String.IsEmpty(ListItem.VideoAspect) + $EXP[Aeon_VOMedia]' % vid),
             ('$VAR[Aeon_Cert]', '%s + $EXP[Aeon_CertKnown]' % vid),
             ('$VAR[FG_L_HdrChip]', media + ' + !String.IsEmpty(ListItem.HdrType)'))
    out, cx = '', 0
    for (label, vis), w in zip(parts, widths):
        out += chip(cx, 0, w, label, vis, ink, edge, h, font)
        cx += w + gap
    return '<control type="group"><left>%d</left><top>%d</top>%s</control>' % (x, y, out)


def row_chips_right(end, y, h=26, ink='ffffffff', edge='66ffffff', start_min=0, shift=0, font='lb_cap_14'):
    """0.56.11 (the user: "move all chips towards duration and right align them, to give space for genres", "this is a
    general comment"): the row's chips right-aligned, ending at end, just before the run time. A row in progress, whose
    "16 min left" is wider, slides them shift px left. The set is the widest that fits from start_min; a variant per
    HDR / certificate presence keeps them flush right when an item has no HDR or no known certificate."""
    widths, gap = chip_set(end - shift - start_min)
    vid = '[String.IsEqual(ListItem.DBType,episode) | String.IsEqual(ListItem.DBType,movie) | String.IsEqual(ListItem.DBType,musicvideo)]'
    media = '!String.IsEmpty(ListItem.VideoResolution) + $EXP[Aeon_VOMedia]'
    parts = (('$VAR[Aeon_ResChip]', media),
             ('$VAR[FG_EcAudio]', media + ' + !String.IsEmpty(ListItem.AudioCodec)'),
             ('$INFO[ListItem.VideoAspect]:1', '%s + !String.IsEmpty(ListItem.VideoAspect) + $EXP[Aeon_VOMedia]' % vid),
             ('$VAR[Aeon_Cert]', '%s + $EXP[Aeon_CertKnown]' % vid),
             ('$VAR[FG_L_HdrChip]', media + ' + !String.IsEmpty(ListItem.HdrType)'))
    n = len(widths)
    hdr_c, cert_c = parts[4][1], parts[3][1]
    combos = [(None, None)]
    if n >= 4:
        combos = [(None, True), (None, False)]
    if n >= 5:
        combos = [(True, True), (True, False), (False, True), (False, False)]
    anim = ('<animation effect="slide" start="0,0" end="-%d,0" time="0" condition="Integer.IsGreater(ListItem.PercentPlayed,0)">Conditional</animation>' % shift) if shift else ''
    out = ''
    for has_hdr, has_cert in combos:
        idx = [0, 1, 2] + ([3] if has_cert else []) + ([4] if has_hdr else [])
        idx = [i for i in idx if i < n]
        conds = []
        if has_hdr is not None:
            conds.append('[%s]' % hdr_c if has_hdr else '![%s]' % hdr_c)
        if has_cert is not None:
            conds.append('[%s]' % cert_c if has_cert else '![%s]' % cert_c)
        total = sum(widths[i] for i in idx) + gap * (len(idx) - 1)
        inner, cx = '', 0
        for i in idx:
            inner += chip(cx, 0, widths[i], parts[i][0], parts[i][1], ink, edge, h, font)
            cx += widths[i] + gap
        vis = '<visible>%s</visible>' % ' + '.join(conds) if conds else ''
        out += '<control type="group"><left>%d</left><top>%d</top>%s%s%s</control>' % (end - total, y, vis, anim, inner)
    return out


def chips_start(end, shift, start_min, with_hdr=True):
    """where right-aligned chips start at most (the grey line ends before it): all of the set, a row in progress"""
    widths, gap = chip_set(end - shift - start_min)
    if not with_hdr and len(widths) == 5:
        widths = widths[:4]
    return end - shift - (sum(widths) + gap * (len(widths) - 1))


def studio_text(x, y, w, h, L, align='left', aligny='center'):
    """0.56.11 (the user: "STUDIO LOGO!!!!!! just use one if this movie doesn't have one", "just put a text label then"):
    the studio's name where its logo would be, when none of the item's studios has a logo in the studio pack (the helper
    publishes aeon.studio.text then, and no aeon.studio)"""
    vis = ('!Skin.HasSetting(aeon.nostudio) + String.IsEmpty(Window(Home).Property(aeon.studio)) + !String.IsEmpty(Window(Home).Property(aeon.studio.text)) + '
           'String.IsEqual(Window(Home).Property(aeon.studio.of),%s.Studio)' % L)
    return lbl(x, y, w, h, '[UPPERCASE]$INFO[Window(Home).Property(aeon.studio.text)][/UPPERCASE]', 'lb_ui_22_bold', 'd9ffffff', align, vis=vis,
               extra='<wrapmultiline>true</wrapmultiline>', aligny=aligny)


def row_lead(label, font, col, h=30):
    """A label as wide as its text, to lead row_chips on a row's second line."""
    return ('<control type="label"><width min="1" max="420">auto</width><height>%d</height><aligny>center</aligny><font>%s</font><textcolor>%s</textcolor>'
            '<selectedcolor>%s</selectedcolor><label>%s</label></control>' % (h, font, col, col, label))


# ------------------------------------------------------------------------------------------------------------ marks
def p_of(tag):
    return 'Container(%s).ListItem' % tag if tag else 'ListItem'


def mark_exprs(tag, sets=True):
    """dot / ring / tick for the items of one prefix (ListItem in layouts, Container(id).ListItem for the item in
    focus), and the ring's percent."""
    P = p_of(tag)
    prog = '[String.IsEqual(%(P)s.DBType,movie) | String.IsEqual(%(P)s.DBType,episode) | String.IsEqual(%(P)s.DBType,musicvideo)]' % {'P': P}
    eps = '[String.IsEqual(%(P)s.DBType,tvshow) | String.IsEqual(%(P)s.DBType,season)]' % {'P': P}
    st = 'String.IsEqual(%s.DBType,set)' % P
    d = {'P': P, 'prog': prog, 'eps': eps, 'set': st, 't': tag}
    x = '''	<expression name="FG_L%(t)s_Ring">[%(prog)s + Integer.IsGreater(%(P)s.PercentPlayed,0)] | [%(eps)s + Integer.IsGreater(%(P)s.Property(WatchedEpisodes),0) + Integer.IsGreater(%(P)s.Property(UnWatchedEpisodes),0)] | [%(set)s + Integer.IsGreater(%(P)s.Property(Watched),0) + !String.IsEqual(%(P)s.Property(Watched),%(P)s.Property(Total))]</expression>
	<expression name="FG_L%(t)s_Tick">[%(prog)s + Integer.IsGreater(%(P)s.PlayCount,0) + !Integer.IsGreater(%(P)s.PercentPlayed,0)] | [%(eps)s + Integer.IsGreater(%(P)s.Property(TotalEpisodes),0) + Integer.IsEqual(%(P)s.Property(UnWatchedEpisodes),0)] | [%(set)s + Integer.IsGreater(%(P)s.Property(Total),0) + String.IsEqual(%(P)s.Property(Watched),%(P)s.Property(Total))]</expression>
	<expression name="FG_L%(t)s_Dot">[%(prog)s + !Integer.IsGreater(%(P)s.PlayCount,0) + !Integer.IsGreater(%(P)s.PercentPlayed,0)] | [%(eps)s + Integer.IsGreater(%(P)s.Property(TotalEpisodes),0) + Integer.IsEqual(%(P)s.Property(WatchedEpisodes),0)] | [%(set)s + Integer.IsGreater(%(P)s.Property(Total),0) + Integer.IsEqual(%(P)s.Property(Watched),0)]</expression>
''' % d
    x += '\t<variable name="FG_L%s_Pct">\n' % tag
    x += '\t\t<value condition="%s">$INFO[%s.PercentPlayed]</value>\n' % (prog, P)
    x += '\t\t<value condition="%s">$INFO[%s.Property(WatchedEpisodePercent)]</value>\n' % (eps, P)
    for t in range(2, 31 if sets else 2):           # sets: the ring's percent of watched films (a view without sets skips the table)
        for w in range(1, t):
            x += '\t\t<value condition="String.IsEqual(%s.Property(Total),%d) + String.IsEqual(%s.Property(Watched),%d)">%d</value>\n' % (P, t, P, w, round(100 * w / t))
    x += '\t\t<value>50</value>\n\t</variable>\n'
    return x


def marks(tag, x, y, size, on_white=None, badge=False):
    """The item's watched mark in a size x size box at (x, y): ring, tick or dot. on_white: a condition under which the
    mark sits on a white row (darker track and tick). badge: a dark disc behind ring and tick (on pictures)."""
    out = ''
    if on_white:
        on_white = '[%s + !$EXP[FG_FocusLight]]' % on_white
    ring_vis = '$EXP[FG_L%s_Ring] + $EXP[FG_L_RingsOn]' % tag
    tick_vis = '$EXP[FG_L%s_Tick] + $EXP[FG_L_TicksOn]' % tag
    dot_vis = '$EXP[FG_L%s_Dot] + $EXP[FG_L_DotsOn]' % tag
    if badge:
        pad = round(size * 0.18)
        out += img(x - pad, y - pad, size + 2 * pad, size + 2 * pad, 'fg/circle.png', 'b3080a0e', vis='[%s] | [%s]' % (ring_vis, tick_vis))
    if on_white:
        out += img(x, y, size, size, 'fg/ring/t.png', '66000000', vis='%s + %s' % (ring_vis, on_white))
        out += img(x, y, size, size, 'fg/ring/t.png', '4dffffff', vis='%s + !%s' % (ring_vis, on_white))
    else:
        out += img(x, y, size, size, 'fg/ring/t.png', '4dffffff', vis=ring_vis)
    out += img(x, y, size, size, 'fg/ring/a$VAR[FG_L%s_Pct].png' % tag, MARK, vis=ring_vis)
    t = round(size * 0.72)
    o = (size - t) // 2
    if on_white:
        out += img(x + o, y + o, t, t, 'aeon/icons/check.png', TICK_ON_WHITE, vis='%s + %s' % (tick_vis, on_white), aspect='keep')
        out += img(x + o, y + o, t, t, 'aeon/icons/check.png', TICK, vis='%s + !%s' % (tick_vis, on_white), aspect='keep')
    else:
        out += img(x + o, y + o, t, t, 'aeon/icons/check.png', TICK, vis=tick_vis, aspect='keep')
    dsz = max(12, round(size * 0.42))
    out += img(x + (size - dsz) // 2, y + (size - dsz) // 2, dsz, dsz, 'fg/circle.png', MARK, vis=dot_vis)
    return out


COMMON = '''	<!-- ===== watched marks and titles: View settings per view and media type (aeon.vo.*), else the global settings -->
	<expression name="FG_L_DotsOn">String.IsEqual(Window(Home).Property(aeon.vo.watched),on) | [String.IsEmpty(Window(Home).Property(aeon.vo.watched)) + !String.IsEqual(Skin.String(aeon.watchedmarkers),off) + !String.IsEqual(Skin.String(aeon.watchedmarkers),watched)]</expression>
	<expression name="FG_L_TicksOn">String.IsEqual(Window(Home).Property(aeon.vo.watched),on) | [String.IsEmpty(Window(Home).Property(aeon.vo.watched)) + !String.IsEqual(Skin.String(aeon.watchedmarkers),off) + !String.IsEqual(Skin.String(aeon.watchedmarkers),unwatched)]</expression>
	<expression name="FG_L_RingsOn">!String.IsEqual(Window(Home).Property(aeon.vo.rings),off)</expression>
	<expression name="FG_L_LogosOn">String.IsEqual(Window(Home).Property(aeon.vo.logos),on) | [String.IsEmpty(Window(Home).Property(aeon.vo.logos)) + !Skin.HasSetting(aeon.nologos)]</expression>
	<!-- ===== the header: where you are (kicker) and the title -->
	<!-- 0.52.5: the view's name as the picker gives it, where one view id has a name per content -->
	<variable name="FG_L_ViewName">
		<value condition="Control.IsVisible(529) + Container.Content(seasons)">$ADDON[skin.aeon.fuse 32590]</value>
		<value condition="Control.IsVisible(520) + Container.Content(seasons)">$LOCALIZE[31119]</value>
		<value condition="Control.IsVisible(520) + Container.Content(tvshows)">$LOCALIZE[31117]</value>
		<value condition="Control.IsVisible(521) + Container.Content(episodes)">$LOCALIZE[31131]</value>
		<value>$INFO[Container.Viewmode]</value>
	</variable>
	<variable name="FG_L_Kicker">
		<value condition="Container.Content(movies) | Container.Content(tvshows) | Container.Content(musicvideos)">$LOCALIZE[14022]</value>
		<value condition="Container.Content(sets)">$LOCALIZE[342]</value>
		<value condition="Container.Content(seasons)">$LOCALIZE[20343]</value>
		<value condition="Container.Content(episodes)">$LOCALIZE[20343]$INFO[Container.ShowTitle,  ›  ,]</value>
		<value>$LOCALIZE[14022]</value>
	</variable>
	<variable name="FG_L_Title">
		<value condition="Container.Content(movies) + String.EndsWith(Container.FolderPath,/titles/)">$LOCALIZE[342]</value>
		<value condition="Container.Content(tvshows) + String.EndsWith(Container.FolderPath,/titles/)">$LOCALIZE[20343]</value>
		<value condition="Container.Content(sets) + String.EndsWith(Container.FolderPath,/sets/)">$LOCALIZE[20434]</value>
		<value condition="Container.Content(seasons) + !String.IsEmpty(Container.ShowTitle)">$INFO[Container.ShowTitle]</value>
		<value>$INFO[Container.FolderName]</value>
	</variable>
	<variable name="FG_L_SortDir">
		<value condition="Container.SortDirection(descending)">↓</value>
		<value>↑</value>
	</variable>
	<!-- ===== a set's films -->
	<variable name="FG_L_FilmCount">
		<value condition="Integer.IsEqual(ListItem.Property(Total),1)">1 $ADDON[skin.aeon.fuse 32315]</value>
		<value condition="!String.IsEmpty(ListItem.Property(Total))">$INFO[ListItem.Property(Total)] $LOCALIZE[31114]</value>
	</variable>
'''


def header():
    """Kicker + title at the top left, the view and sort order in a quiet capsule at the top right."""
    return (lbl(96, 36, 1100, 30, '[UPPERCASE]$VAR[FG_L_Kicker][/UPPERCASE]', 'lb_cap_16', 'a3ffffff') +
            lbl(94, 60, 1200, 72, '$VAR[FG_L_Title]', 'lb_title_50', 'ffffffff') +
            '<control type="grouplist"><left>1000</left><top>52</top><width>800</width><height>40</height><orientation>horizontal</orientation><align>right</align><usecontrolcoords>true</usecontrolcoords>'
            '<control type="button"><width min="60" max="800">auto</width><height>40</height><label>$VAR[FG_L_ViewName]  ·  $INFO[Container.SortMethod] $VAR[FG_L_SortDir]</label>'
            '<font>lb_small_20_semibold</font><textoffsetx>18</textoffsetx><aligny>center</aligny><textcolor>ccffffff</textcolor><focusedcolor>ccffffff</focusedcolor><disabledcolor>ccffffff</disabledcolor>'
            '<texturenofocus border="20" colordiffuse="14ffffff">fg/r20.png</texturenofocus><texturefocus border="20" colordiffuse="14ffffff">fg/r20.png</texturefocus><enable>false</enable></control></control>')


def rail(cid, az, sb, icon, az_content, subs=(), always=False):
    """The glass rail at the right edge: the clock, the A-Z jump list (az) with its scroll bar (sb), the content icon
    and the number of items of container cid. subs (0.52.5): ((list, scrollbar), ...) second lists of the view (a
    season's episodes): while one has the focus the rail shows its scroll bar and its number of items. always: the
    scroll bar shows even when everything fits on one page."""
    in_sub = '[%s]' % ' | '.join('Control.HasFocus(%d) | Control.HasFocus(%d)' % (s, ssb) for s, ssb in subs) if subs else ''
    out = glass(1836, 24, 64, 1032, 32, shadow=False)
    out += lbl(1836, 40, 64, 32, '$INFO[System.Time(HH)]', 'lb_ui_28_semibold', 'ffffffff', 'center')
    out += lbl(1836, 72, 64, 32, '$INFO[System.Time(mm)]', 'lb_ui_28', 'b8ffffff', 'center')
    out += ('<include content="FG_AZBubble"><param name="vis" value="Control.HasFocus(%d)"/><param name="label" value="$INFO[Container(%d).ListItem.Label]"/></include>' % (az, az))
    # 0.56.6 the focus circle (36) is taller than a letter row (26) and a list cuts its rows at its edges: one circle per
    # letter slot outside the list, shown for the focused letter's slot; # jumps to the view's own list
    out += ''.join(img(1850, 211 + 26 * k, 36, 36, 'fg/circle.png', 'ffffffff',
                       vis='Control.HasFocus(%d) + Integer.IsEqual(Container(%d).Position,%d)' % (az, az, k)) for k in range(27))
    az_content = az_content.replace('<onclick>SetFocus(510,0,absolute)</onclick>', '<onclick>SetFocus(%d,0,absolute)</onclick>' % cid)
    out += ('<control type="list" id="%d"><left>1836</left><top>216</top><width>64</width><height>702</height><orientation>vertical</orientation><scrolltime>0</scrolltime>'
            '<onleft>SetFocus(%d)</onleft><onright>%d</onright><onback>SetFocus(%d)</onback>'
            '<itemlayout width="64" height="26">%s</itemlayout><focusedlayout width="64" height="26">%s%s%s</focusedlayout>%s</control>'
            % (az, cid, sb, cid,
               lbl(0, 0, 64, 26, '$INFO[ListItem.Label]', 'lb_cap_16', '80ffffff', 'center'),
               '',
               lbl(0, 0, 64, 26, '$INFO[ListItem.Label]', 'lb_cap_16', INK, 'center', vis='Control.HasFocus(%d)' % az),
               lbl(0, 0, 64, 26, '$INFO[ListItem.Label]', 'lb_cap_16', '80ffffff', 'center', vis='!Control.HasFocus(%d)' % az),
               az_content))
    out += ('<control type="scrollbar" id="%d"><left>1891</left><top>216</top><width>5</width><height>702</height>'
            '<texturesliderbackground colordiffuse="00ffffff">common/white.png</texturesliderbackground>'
            '<texturesliderbar border="2" colordiffuse="66ffffff">fg/r8.png</texturesliderbar><texturesliderbarfocus border="2" colordiffuse="fg_mark">fg/r8.png</texturesliderbarfocus>'
            '<orientation>vertical</orientation><showonepage>%s</showonepage><onleft>%d</onleft><onright>noop</onright><onback>SetFocus(%d)</onback>%s</control>'
            % (sb, 'true' if always else 'false', az, cid, '<visible>!%s</visible>' % in_sub if subs else ''))
    for s, ssb in subs:
        out += ('<control type="scrollbar" id="%d"><left>1891</left><top>216</top><width>5</width><height>702</height>'
                '<texturesliderbackground colordiffuse="00ffffff">common/white.png</texturesliderbackground>'
                '<texturesliderbar border="2" colordiffuse="66ffffff">fg/r8.png</texturesliderbar><texturesliderbarfocus border="2" colordiffuse="fg_mark">fg/r8.png</texturesliderbarfocus>'
                '<orientation>vertical</orientation><showonepage>%s</showonepage><onleft>%d</onleft><onright>noop</onright><onback>SetFocus(%d)</onback>'
                '<visible>Control.HasFocus(%d) | Control.HasFocus(%d)</visible></control>' % (ssb, 'true' if always else 'false', s, s, s, ssb))
    out += img(1855, 966, 26, 26, icon, 'ffffffff', aspect='keep')
    for c, vis in [(cid, '!%s' % in_sub if subs else '')] + [(s, 'Control.HasFocus(%d)' % s) for s, _ in subs]:
        big = 'Integer.IsGreater(Container(%d).NumItems,9999)' % c      # five digits: a smaller font so they fit the rail
        pre = (vis + ' + ') if vis else ''
        out += lbl(1836, 998, 64, 32, '$INFO[Container(%d).NumItems]' % c, 'lb_small_20_bold', 'ffffffff', 'center', pre + '!' + big)
        out += lbl(1836, 998, 64, 32, '$INFO[Container(%d).NumItems]' % c, 'lb_cap_16', 'ffffffff', 'center', pre + big)
    return out


def media_vars(tag):
    """Resolution / HDR / audio / aspect names of the item in focus of container tag (as Episode combined)."""
    L = p_of(tag)
    return '''	<variable name="FG_L%(t)s_Res">
		<value condition="String.IsEqual(%(L)s.VideoResolution,8K)">8K</value>
		<value condition="String.IsEqual(%(L)s.VideoResolution,4K) | String.IsEqual(%(L)s.VideoResolution,2160)">4K</value>
		<value condition="String.IsEqual(%(L)s.VideoResolution,1080)">1080</value>
		<value condition="String.IsEqual(%(L)s.VideoResolution,720)">720</value>
		<value condition="!String.IsEmpty(%(L)s.VideoResolution)">SD</value>
	</variable>
	<!-- 0.56.9 the info panel rule: the row's names; Dolby Vision with its profile (the helper reads it from the .nfo or
	     the media manager's mediainfo file: aeon.dvp for aeon.dvp.path); no SDR chip -->
	<variable name="FG_L%(t)s_Hdr">
		<value condition="String.IsEqual(%(L)s.HdrType,dolbyvision) + !String.IsEmpty(Window(Home).Property(aeon.dvp)) + String.IsEqual(%(L)s.FileNameAndPath,Window(Home).Property(aeon.dvp.path))">DV $INFO[Window(Home).Property(aeon.dvp)]</value>
		<value condition="String.IsEqual(%(L)s.HdrType,dolbyvision)">DV</value>
		<value condition="String.IsEqual(%(L)s.HdrType,hdr10plus)">HDR10+</value>
		<value condition="String.IsEqual(%(L)s.HdrType,hdr10)">HDR10</value>
		<value condition="String.IsEqual(%(L)s.HdrType,hlg)">HLG</value>
	</variable>
	<variable name="FG_L%(t)s_Chan">
		<value condition="Integer.IsEqual(%(L)s.AudioChannels,8)"> 7.1</value>
		<value condition="Integer.IsEqual(%(L)s.AudioChannels,6)"> 5.1</value>
		<value condition="Integer.IsEqual(%(L)s.AudioChannels,2)"> 2.0</value>
	</variable>
	<variable name="FG_L%(t)s_Audio">
		<value condition="String.StartsWith(%(L)s.AudioCodec,truehd) + String.Contains(%(L)s.AudioCodec,atmos)">TrueHD Atmos</value>
		<value condition="String.StartsWith(%(L)s.AudioCodec,eac3) + String.Contains(%(L)s.AudioCodec,atmos)">DD+ Atmos</value>
		<value condition="String.IsEqual(%(L)s.AudioCodec,truehd)">TrueHD$VAR[FG_L%(t)s_Chan]</value>
		<value condition="String.IsEqual(%(L)s.AudioCodec,eac3)">DD+$VAR[FG_L%(t)s_Chan]</value>
		<value condition="String.IsEqual(%(L)s.AudioCodec,ac3) | String.IsEqual(%(L)s.AudioCodec,dolbydigital)">DD$VAR[FG_L%(t)s_Chan]</value>
		<value condition="String.IsEqual(%(L)s.AudioCodec,dtshd_ma_x) | String.IsEqual(%(L)s.AudioCodec,dts-x)">DTS:X$VAR[FG_L%(t)s_Chan]</value>
		<value condition="String.IsEqual(%(L)s.AudioCodec,dtshd_ma) | String.IsEqual(%(L)s.AudioCodec,dtsma)">DTS-HD MA$VAR[FG_L%(t)s_Chan]</value>
		<value condition="String.StartsWith(%(L)s.AudioCodec,dts) | String.IsEqual(%(L)s.AudioCodec,dca)">DTS$VAR[FG_L%(t)s_Chan]</value>
		<value condition="String.StartsWith(%(L)s.AudioCodec,aac)">AAC$VAR[FG_L%(t)s_Chan]</value>
		<value condition="!String.IsEmpty(%(L)s.AudioCodec)">[UPPERCASE]$INFO[%(L)s.AudioCodec][/UPPERCASE]$VAR[FG_L%(t)s_Chan]</value>
	</variable>
	<variable name="FG_L%(t)s_AudioS">
		<value condition="String.StartsWith(%(L)s.AudioCodec,truehd) + String.Contains(%(L)s.AudioCodec,atmos)">TrueHD Atmos</value>
		<value condition="String.StartsWith(%(L)s.AudioCodec,eac3) + String.Contains(%(L)s.AudioCodec,atmos)">DD+ Atmos</value>
		<value condition="String.IsEqual(%(L)s.AudioCodec,truehd)">TrueHD$VAR[FG_L%(t)s_Chan]</value>
		<value condition="String.IsEqual(%(L)s.AudioCodec,eac3)">DD+$VAR[FG_L%(t)s_Chan]</value>
		<value condition="String.IsEqual(%(L)s.AudioCodec,ac3) | String.IsEqual(%(L)s.AudioCodec,dolbydigital)">DD$VAR[FG_L%(t)s_Chan]</value>
		<value condition="String.IsEqual(%(L)s.AudioCodec,dtshd_ma_x) | String.IsEqual(%(L)s.AudioCodec,dts-x)">DTS:X$VAR[FG_L%(t)s_Chan]</value>
		<value condition="String.IsEqual(%(L)s.AudioCodec,dtshd_ma) | String.IsEqual(%(L)s.AudioCodec,dtsma)">DTS-HD MA$VAR[FG_L%(t)s_Chan]</value>
		<value condition="String.StartsWith(%(L)s.AudioCodec,dts) | String.IsEqual(%(L)s.AudioCodec,dca)">DTS$VAR[FG_L%(t)s_Chan]</value>
		<value condition="String.StartsWith(%(L)s.AudioCodec,aac)">AAC$VAR[FG_L%(t)s_Chan]</value>
		<value condition="!String.IsEmpty(%(L)s.AudioCodec)">[UPPERCASE]$INFO[%(L)s.AudioCodec][/UPPERCASE]$VAR[FG_L%(t)s_Chan]</value>
	</variable>
	<variable name="FG_L%(t)s_Logo">
		<value condition="!String.IsEmpty(%(L)s.Art(clearlogo))">$INFO[%(L)s.Art(clearlogo)]</value>
		<value>$INFO[%(L)s.Art(tvshow.clearlogo)]</value>
	</variable>
''' % {'t': tag, 'L': L}


PROG = '[String.IsEqual(%(L)s.DBType,movie) | String.IsEqual(%(L)s.DBType,episode) | String.IsEqual(%(L)s.DBType,musicvideo)]'
GROUPS = '[String.IsEqual(%(L)s.DBType,tvshow) | String.IsEqual(%(L)s.DBType,season) | String.IsEqual(%(L)s.DBType,set)]'
HAS_MARKS = {'510', '512', '517', '518', '522', '523', '524', '527'}     # views whose mark expressions exist already


def status_vars(tag, resume=None):
    """0.56.9 the info panel rule, the status line's words for the item in focus of container tag: an item in progress
    its time left (the helper's aeon.left slots, as the rows; resume: a view's own "58:18 of 1:13:33 · 15 min left"),
    watched / unwatched (Kodi's words), shows and seasons x of y episodes, sets x of y films. Also the mark expressions
    of views that had none."""
    L = p_of(tag)
    d = {'L': L, 't': tag}
    prog = PROG % d
    x = '\t<variable name="FG_L%s_Status">\n' % tag
    if resume:
        x += '\t\t<value condition="Integer.IsGreater(%s.PercentPlayed,0) + !String.IsEmpty(%s)">$INFO[%s]</value>\n' % (L, resume, resume)
    for k in range(1, 41):
        x += ('\t\t<value condition="Integer.IsGreater(%(L)s.PercentPlayed,0) + String.IsEqual(%(L)s.DBID,Window(Home).Property(aeon.left.%(k)d.id)) + '
              'String.IsEqual(%(L)s.DBType,Window(Home).Property(aeon.left.%(k)d.type))">$INFO[Window(Home).Property(aeon.left.%(k)d.hmb)]</value>\n' % {'L': L, 'k': k})
    x += '\t\t<value condition="%s + Integer.IsGreater(%s.PercentPlayed,0)">$INFO[%s.PercentPlayed]%%</value>\n' % (prog, L, L)
    x += '\t\t<value condition="%s + Integer.IsGreater(%s.PlayCount,0)">$LOCALIZE[16102]</value>\n' % (prog, L)
    x += '\t\t<value condition="%s">$LOCALIZE[16101]</value>\n' % prog
    x += ('\t\t<value condition="String.IsEqual(%(L)s.DBType,tvshow) | String.IsEqual(%(L)s.DBType,season)">$INFO[%(L)s.Property(WatchedEpisodes)] $ADDON[skin.aeon.fuse 32285] '
          '$INFO[%(L)s.Property(TotalEpisodes)] $ADDON[skin.aeon.fuse 32323]</value>\n' % d)
    x += ('\t\t<value condition="String.IsEqual(%(L)s.DBType,set)">$INFO[%(L)s.Property(Watched)] $ADDON[skin.aeon.fuse 32285] $INFO[%(L)s.Property(Total)] '
          '$ADDON[skin.aeon.fuse 32321]</value>\n' % d)
    x += '\t</variable>\n'
    if tag not in HAS_MARKS:
        HAS_MARKS.add(tag)
        x += mark_exprs(tag, sets=False)
    return x


def status_items(tag, h=32, w=600, font='lb_ui_22'):
    """the mark (ring, tick, dot as the rows; the view settings decide which show) and the status words, as items of
    a horizontal grouplist"""
    anym = '[$EXP[FG_L%(t)s_Ring] + $EXP[FG_L_RingsOn]] | [$EXP[FG_L%(t)s_Tick] + $EXP[FG_L_TicksOn]] | [$EXP[FG_L%(t)s_Dot] + $EXP[FG_L_DotsOn]]' % {'t': tag}
    return ('<control type="group"><width>28</width><height>%d</height><visible>%s</visible>%s</control>'
            '<control type="label"><width min="10" max="%d">auto</width><height>%d</height><aligny>center</aligny><font>%s</font><textcolor>ccffffff</textcolor>'
            '<label>$VAR[FG_L%s_Status]</label></control>' % (h, anym, marks(tag, 0, (h - 28) // 2, 28), w, h, font, tag))


def status_line(tag, w, h=32, x=None, y=None):
    """0.56.9 the info panel rule: the status line (mark and words) of the item in focus of container tag; with x / y
    at that place, else as an item of a vertical grouplist. Films, episodes, music videos, shows, seasons, sets."""
    d = {'L': p_of(tag)}
    pos = '<left>%d</left><top>%d</top>' % (x, y) if x is not None else ''
    return ('<control type="grouplist">%s<width>%d</width><height>%d</height><orientation>horizontal</orientation><itemgap>10</itemgap><usecontrolcoords>true</usecontrolcoords>'
            '<visible>%s | %s</visible>%s</control>' % (pos, w, h, PROG % d, GROUPS % d, status_items(tag, h, w - 40)))


def panel_chips(tag):
    """0.56.9 the info panel rule: the row's media chips at panel size, in the row's order: resolution, audio, aspect
    ratio, HDR (with the Dolby Vision profile; nothing for SDR)"""
    L = p_of(tag)
    media = '$EXP[Aeon_VOMedia]'
    return ''.join(big_chip(a, b) for a, b in (
        ('$VAR[FG_L%s_Res]' % tag, '!String.IsEmpty(%s.VideoResolution) + %s' % (L, media)),
        ('$VAR[FG_L%s_Audio]' % tag, '!String.IsEmpty(%s.AudioCodec) + %s' % (L, media)),
        ('$INFO[%s.VideoAspect]:1' % L, '!String.IsEmpty(%s.VideoAspect) + %s' % (L, media)),
        ('$VAR[FG_L%s_Hdr]' % tag, '!String.IsEmpty(%s.HdrType) + %s' % (L, media))))


def big_chip(label, vis):
    return ('<control type="button"><width min="40" max="420">auto</width><height>34</height><label>%s</label><font>lb_small_20_bold</font>'
            '<textoffsetx>14</textoffsetx><align>center</align><aligny>center</aligny><textcolor>ffffffff</textcolor><focusedcolor>ffffffff</focusedcolor><disabledcolor>ffffffff</disabledcolor>'
            '<texturenofocus border="10" colordiffuse="66ffffff">fg/e12.png</texturenofocus><texturefocus border="10" colordiffuse="66ffffff">fg/e12.png</texturefocus><enable>false</enable>'
            '<visible>%s</visible></control>' % (label, vis))


def meta_label(label, vis=None):
    v = '<visible>%s</visible>' % vis if vis else ''
    return ('<control type="label"><width min="10" max="600">auto</width><height>36</height><aligny>center</aligny><font>lb_ui_22</font>'
            '<textcolor>ccffffff</textcolor><label>%s</label>%s</control>' % (label, v))


# ------------------------------------------------------------------------------------------------------------ List 510
def row510(focused):
    """One row of the List view: 1053 x 92 (an 86-high row and a 6 px gap). 0.56.8, the list row rule: the title, the
    grey line and after it the chips (films and episodes), at the right the run time (bold, as before), the time left of
    an item in progress, or watched / total, and the mark last."""
    lit = 'Control.HasFocus(510)'
    on_white = lit if focused else None
    out = ''
    if focused:
        out += img(0, 0, 1053, 86, 'fg/r18.png', 'ffffffff', 18, lit)
        out += img(0, 0, 1053, 86, 'fg/r18.png', '1fffffff', 18, '!' + lit)
        out += img(0, 0, 1053, 86, 'fg/e18.png', '38ffffff', 18, '!' + lit)
    ink = ('$VAR[FG_L_Ink]' if focused else 'ffffffff')
    ink2 = ('$VAR[FG_L_Ink2]' if focused else 'a8ffffff')
    edge = ('$VAR[FG_L_ChipEdge]' if focused else '66ffffff')
    ep = 'String.IsEqual(ListItem.DBType,episode)'
    film = '[String.IsEqual(ListItem.DBType,movie) | String.IsEqual(ListItem.DBType,musicvideo)]'
    # episodes: their still at the left, with its bar
    out += img(10, 7, 128, 72, '$INFO[ListItem.Art(thumb)]', diffuse='fg/m128x72.png', aspect='scale', vis=ep, bg=True)
    out += ('<control type="progress"><left>18</left><top>71</top><width>112</width><height>4</height><texturebg border="2,0,2,0" colordiffuse="59ffffff">fg/pillh.png</texturebg>'
            '<midtexture border="2,0,2,0" colordiffuse="fg_mark">fg/pillh.png</midtexture><info>ListItem.PercentPlayed</info><visible>%s + Integer.IsGreater(ListItem.PercentPlayed,0)</visible></control>' % ep)
    out += lbl(156, 10, 680, 38, '$INFO[ListItem.Title]', 'lb_ui_24_bold', ink, vis=ep)
    end, shift = 1053 - 46 - 14 - 54 - 16, 72          # 0.56.11: the chips end just before the run time ("1·44")
    hdr = '[!String.IsEmpty(ListItem.VideoResolution) + $EXP[Aeon_VOMedia] + !String.IsEmpty(ListItem.HdrType)]'
    for vis, w_end in (('[%s]' % hdr, chips_start(end, shift, 282)), ('![%s]' % hdr, chips_start(end, shift, 282, False))):
        out += lbl(156, 46, w_end - 12 - 156, 30, '$VAR[FG_L_RowSub]', 'lb_small_20', ink2, vis='%s + %s' % (ep, vis))
    out += '<control type="group"><visible>%s</visible>%s</control>' % (ep, row_chips_right(end, 48, 26, ink, edge, 282, shift))
    out += lbl(22, 10, 820, 38, '$INFO[ListItem.Label]', 'lb_ui_24_bold', ink, vis='!' + ep)
    for vis, w_end in (('[%s]' % hdr, chips_start(end, shift, 282)), ('![%s]' % hdr, chips_start(end, shift, 282, False))):
        out += lbl(22, 46, w_end - 12 - 22, 30, '$VAR[FG_L_RowSub]', 'lb_small_20', ink2, vis='%s + %s' % (film, vis))
    out += '<control type="group"><visible>%s</visible>%s</control>' % (film, row_chips_right(end, 48, 26, ink, edge, 282, shift))
    out += lbl(22, 46, 820, 30, '$VAR[FG_L_RowSub]', 'lb_small_20', ink2, vis='!%s + !%s' % (ep, film))
    out += lbl(1053 - 46 - 14 - 150, 24, 150, 38, '$VAR[FG_L_RowRight]', 'lb_ui_24_semibold', ink, 'right')
    out += marks('', 1053 - 46, 28, 30, on_white)
    return out


def view510():
    L = 'Container(510).ListItem'
    out = '\t<include name="FG_V510_View">\n\t\t<control type="group">\n\t\t\t<visible>Control.IsVisible(510)</visible>\n\t\t\t<include>Anim_FadeVisible</include>\n'
    out += '\t\t\t<include>Aeon_V_Bg</include>\n'
    out += '\t\t\t<!-- header -->\n\t\t\t' + header() + '\n'
    # the poster (an episode: its season's) as tall as the list, its watched mark
    out += '\t\t\t<!-- the poster, as tall as the list (episodes: the season poster), with its watched mark -->\n'
    out += ('\t\t\t<control type="group"><visible>!Control.HasFocus(5101) + !Control.HasFocus(5104)</visible><include>Anim_FadeVisible</include>'
            + img(56, 120, 667, 960, 'fg/sh24.png', '$VAR[FG_PanelSh_8c]', 64)
            + img(96, 160, 587, 880, 'fg/r18.png', 'fg_frost', 18)
            + img(96, 160, 587, 880, '$VAR[FG_L510_Poster]', diffuse='fg/m587x880.png', aspect='scale', bg=True, extra='<fadetime>300</fadetime>')
            + marks('510', 627, 176, 40, badge=True) + '</control>\n')
    # the left panes: a film's versions (one at a time) or a set's films (two by two)
    out += '\t\t\t<!-- the left panes (Left from the list): a film\'s versions, one at a time, or a set\'s films, two by two -->\n'
    out += ('\t\t\t<control type="panel" id="5101"><left>96</left><top>160</top><width>587</width><height>880</height><orientation>vertical</orientation>'
            '<scrolltime tween="cubic" easing="out">320</scrolltime><onright>SetFocus(510)</onright><onleft condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onleft><onback>SetFocus(510)</onback>'
            '<visible>$EXP[Aeon_C_One]</visible><animation effect="fade" start="100" end="0" time="0" condition="!Control.HasFocus(5101)">Conditional</animation><content>$VAR[Aeon_LeftPaneContent]</content>'
            '<itemlayout width="587" height="880">%s</itemlayout><focusedlayout width="587" height="880">%s</focusedlayout></control>\n'
            % (img(0, 0, 587, 880, '$VAR[Aeon_Poster]', diffuse='fg/m587x880.png', aspect='scale', bg=True),
               img(0, 0, 587, 880, '$VAR[Aeon_Poster]', diffuse='fg/m587x880.png', aspect='scale', bg=True)
               + img(0, 0, 587, 880, 'fg/r18.png', '99080a0e', 18)
               + lbl(30, 300, 527, 110, '$INFO[ListItem.Title]', 'lb_font36_title', 'ffffffff', 'center', aligny='bottom')
               + lbl(30, 418, 527, 34, '[UPPERCASE]$INFO[ListItem.VideoVersionName][/UPPERCASE]', 'lb_cap_16', 'b3ffffff', 'center')
               + img(251, 470, 84, 84, 'aeon/ring_circle.png', 'd9ffffff') + img(277, 496, 32, 32, 'aeon/icons/play.png', 'ffffffff')
               + lbl(30, 580, 527, 34, '$VAR[Aeon_TileMeta]', 'lb_small_20_bold', 'ccffffff', 'center')
               + marks('', 531, 16, 40, badge=True)))
    # two by two: the panel is 8 px bigger all round (two columns need 588 px, and the gold ring must not be clipped)
    out += ('\t\t\t<control type="panel" id="5104"><left>88</left><top>152</top><width>604</width><height>896</height><orientation>vertical</orientation>'
            '<scrolltime tween="cubic" easing="out">260</scrolltime><onright>SetFocus(510)</onright><onleft condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onleft><onback>SetFocus(510)</onback>'
            '<visible>$EXP[Aeon_C_Grid]</visible><animation effect="fade" start="100" end="0" time="0" condition="!Control.HasFocus(5104)">Conditional</animation><content>$VAR[Aeon_LeftPaneContent]</content>'
            '<itemlayout width="294" height="440"><control type="group"><left>8</left><top>8</top>%s</control></itemlayout>'
            '<focusedlayout width="294" height="440"><control type="group"><left>8</left><top>8</top>%s</control></focusedlayout></control>\n'
            % (img(0, 0, 274, 420, '$VAR[Aeon_Poster]', diffuse='fg/m274x420.png', aspect='scale', bg=True) + marks('', 228, 12, 30, badge=True),
               img(0, 0, 274, 420, '$VAR[Aeon_Poster]', diffuse='fg/m274x420.png', aspect='scale', bg=True)
               + img(0, 0, 274, 420, 'fg/r16.png', '94080a0e', 16)
               + lbl(14, 110, 246, 120, '$INFO[ListItem.Title]', 'lb_ui_26_semibold', 'ffffffff', 'center', aligny='bottom')
               + img(109, 244, 56, 56, 'aeon/ring_circle.png', 'd9ffffff') + img(127, 262, 20, 20, 'aeon/icons/play.png', 'ffffffff')
               + lbl(10, 318, 254, 30, '$VAR[Aeon_TileMeta]', 'lb_small_20_bold', 'ccffffff', 'center')
               + img(-7, -7, 288, 434, 'fg/e24.png', 'fg_mark', 24)
               + marks('', 228, 12, 30, badge=True)))
    out += ('\t\t\t<control type="group"><visible>Control.HasFocus(5101) | Control.HasFocus(5104)</visible><include>Anim_FadeVisible</include>'
            + img(89, 153, 601, 894, 'fg/e24.png', 'fg_mark', 24, 'Control.HasFocus(5101)')
            + lbl(96, 1044, 587, 30, '$INFO[Container(5101).CurrentItem] / $INFO[Container(5101).NumItems]', 'lb_small_20_semibold', 'b3ffffff', 'center', 'Control.HasFocus(5101) + Integer.IsGreater(Container(5101).NumItems,1)')
            + lbl(96, 1044, 587, 30, '$INFO[Container(5104).CurrentItem] / $INFO[Container(5104).NumItems]', 'lb_small_20_semibold', 'b3ffffff', 'center', 'Control.HasFocus(5104) + Integer.IsGreater(Container(5104).NumItems,4)')
            + '</control>\n')
    # 0.56.48: a chevron on the poster's right edge while Left opens a pane (a set's films, a film's versions)
    out += ("\t\t\t<!-- 0.56.48 sets_05648: Left opens the pane (a set's films, a film's versions) -->\n"
            '\t\t\t<control type="group"><visible>Control.HasFocus(510) + $EXP[Aeon_HasLeftPane]</visible><include>Anim_FadeVisible</include>'
            '<control type="image"><left>623</left><top>576</top><width>48</width><height>48</height><texture colordiffuse="b3080a0e">fg/circle.png</texture></control>'
            '<control type="image"><left>635</left><top>588</top><width>24</width><height>24</height><aspectratio>keep</aspectratio>'
            '<texture colordiffuse="ffffffff">aeon/icons/chevron_left.png</texture></control></control>\n')
    # the list card: six rows, the item in focus under them
    out += '\t\t\t<!-- the list card: six rows; the item in focus under them -->\n\t\t\t' + glass(723, 160, 1077, 880) + '\n'
    out += ('\t\t\t<control type="fixedlist" id="510"><onback condition="String.IsEqual(Skin.String(aeon.backmode),home)">ActivateWindow(home)</onback>'
            '<left>735</left><top>172</top><width>1053</width><height>552</height><orientation>vertical</orientation><pagecontrol>5103</pagecontrol><movement>2</movement>'
            '<viewtype label="535">list</viewtype><visible>$EXP[Aeon_IsView]</visible><scrolltime tween="cubic" easing="out">220</scrolltime>'
            '<onup>Action(LastPage)</onup><ondown>Action(FirstPage)</ondown>'
            '<onleft condition="$EXP[Aeon_HasGridPane]">SetFocus(5104)</onleft><onleft condition="$EXP[Aeon_HasOnePane]">SetFocus(5101)</onleft>'
            '<onleft condition="[!$EXP[Aeon_HasLeftPane]] + !Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onleft><onright>SetFocus(5102)</onright>'
            '<itemlayout width="1053" height="92">%s</itemlayout><focusedlayout width="1053" height="92">%s</focusedlayout></control>\n' % (row510(False), row510(True)))
    # the item in focus
    foot = img(747, 734, 1029, 1, 'common/white.png', '24ffffff')
    # the rating sources first (when the view shows ratings), then the facts
    ratings = ''
    for src, tex in (('imdb', 'ratings/imdb.png'), ('tmdb', 'ratings/tmdb.png'), ('rt', 'ratings/rtfresh.png')):     # as the mockups (and the walls)
        ratings += ('<control type="image"><width>40</width><height>30</height><aspectratio>keep</aspectratio><texture>%s</texture><visible>$EXP[Aeon_RH_%s]</visible></control>'
                    '<control type="label"><width min="10" max="90">auto</width><height>36</height><aligny>center</aligny><font>lb_ui_22_semibold</font><textcolor>ffffffff</textcolor>'
                    '<label>$VAR[Aeon_R_%s]</label><visible>$EXP[Aeon_RH_%s]</visible></control>' % (tex, src, src, src))
    none = '![$EXP[Aeon_RH_imdb] | $EXP[Aeon_RH_tmdb] | $EXP[Aeon_RH_rt]]'
    ratings += ('<control type="image"><width>28</width><height>30</height><aspectratio>keep</aspectratio><texture colordiffuse="fg_mark">aeon/icons/star.png</texture>'
                '<visible>%(n)s + !String.IsEmpty(%(L)s.Rating)</visible></control><control type="label"><width min="10" max="90">auto</width><height>36</height><aligny>center</aligny>'
                '<font>lb_ui_22_semibold</font><textcolor>ffffffff</textcolor><label>$INFO[%(L)s.Rating]</label><visible>%(n)s + !String.IsEmpty(%(L)s.Rating)</visible></control>' % {'n': none, 'L': L})
    anyr = '[$EXP[Aeon_RH_imdb] | $EXP[Aeon_RH_tmdb] | $EXP[Aeon_RH_rt] | !String.IsEmpty(%s.Rating)]' % L
    for vis, inner in (('$EXP[Aeon_VORat]', ratings + meta_label('·', anyr)), ('!$EXP[Aeon_VORat]', '')):
        foot += ('<control type="grouplist"><left>747</left><top>748</top><width>776</width><height>36</height><orientation>horizontal</orientation><itemgap>9</itemgap>'
                 '<usecontrolcoords>true</usecontrolcoords><visible>%s</visible>%s%s</control>' % (vis, inner, meta_label('$VAR[FG_L510_Meta]')))
    # 0.56.9 the info panel rule: the status line (the watched mark and its words) under the facts
    foot += status_line('510', 760, 32, 747, 788)
    tag_vis = '!String.IsEmpty(%s.Tagline) + $EXP[Aeon_VOPlot]' % L
    foot += lbl(747, 824, 760, 32, '$INFO[%s.Tagline]' % L, 'lb_tag_22', '8fffffff', vis=tag_vis)
    is_set = 'String.IsEqual(%s.DBType,set)' % L
    foot += textbox(747, 858, 760, 118, '$INFO[%s.Plot]' % L, 'lb_body_24', 'd9ffffff', '!String.IsEmpty(%s.Tagline) + $EXP[Aeon_VOPlot]' % L)
    foot += textbox(747, 826, 760, 150, '$INFO[%s.Plot]' % L, 'lb_body_24', 'd9ffffff', 'String.IsEmpty(%s.Tagline) + $EXP[Aeon_VOPlot] + !%s' % (L, is_set))
    foot += textbox(747, 826, 590, 150, '$INFO[%s.Plot]' % L, 'lb_body_24', 'd9ffffff', 'String.IsEmpty(%s.Tagline) + $EXP[Aeon_VOPlot] + %s' % (L, is_set))
    film = img(0, 0, 96, 144, '$VAR[Aeon_Poster]', diffuse='fg/m96x144.png', aspect='scale', bg=True) + marks('', 70, 6, 20)
    foot += ('<control type="list" id="5105"><left>1356</left><top>752</top><width>420</width><height>150</height><orientation>horizontal</orientation>'
             '<animation effect="slide" end="0,96" time="0" condition="$EXP[FG_L_LogosOn] + !String.IsEmpty(Container(510).ListItem.Art(clearlogo))">Conditional</animation>'   # 0.56.48: under the clearlogo
             '<scrolltime tween="cubic" easing="out">400</scrolltime><autoscroll time="5000">Integer.IsGreater(Container(5105).NumItems,4)</autoscroll>'
             '<visible>%s</visible><content>$VAR[Aeon_LeftPaneContent]</content><itemlayout width="108" height="150">%s</itemlayout><focusedlayout width="108" height="150">%s</focusedlayout></control>'
             % (is_set, film, film))
    chips = panel_chips('510')      # 0.56.9: resolution, audio, aspect ratio, HDR; the genres stay in the row's grey line
    foot += ('<control type="grouplist"><left>747</left><top>988</top><width>760</width><height>36</height><orientation>horizontal</orientation><itemgap>8</itemgap><usecontrolcoords>true</usecontrolcoords>'
             '<visible>$EXP[Aeon_VOMedia]</visible>%s</control>' % chips)
    # the clearlogo (a setting) and the studio / network logo at the right
    foot += img(1528, 750, 250, 84, '$VAR[FG_L510_Logo]', aspect='keep', vis='$EXP[FG_L_LogosOn]', align='right', aligny='top')
    foot += img(1608, 954, 170, 70, 'resource://resource.images.studios.white/$INFO[Window(Home).Property(aeon.studio)].png', 'ebffffff', aspect='keep',
                vis='!Skin.HasSetting(aeon.nostudio) + !String.IsEmpty(Window(Home).Property(aeon.studio)) + String.IsEqual(Window(Home).Property(aeon.studio.of),%s.Studio) + !%s' % (L, is_set),
                align='right', aligny='bottom')
    foot += studio_text(1528, 954, 250, 70, L, 'right', 'bottom').replace('.Studio)</visible>', '.Studio) + !%s</visible>' % is_set)     # 0.56.48: a set's film strip sits there
    out += '\t\t\t<!-- the item in focus: rating sources, facts, tagline, plot, media chips; clearlogo and studio logo -->\n\t\t\t<control type="group"><visible>!Control.HasFocus(5101) + !Control.HasFocus(5104)</visible>' + foot + '</control>\n'
    out += '\t\t\t<!-- the rail -->\n\t\t\t' + rail(510, 5102, 5103, '$VAR[FG_L_ContentIcon]', AZ510) + '\n'
    out += '\t\t</control>\n\t</include>\n'
    return out


LIST_VARS = '''	<!-- ===== List view (510) -->
	<variable name="FG_L_Ink"><value condition="Control.HasFocus(510)">aeon_onbar</value><value>ffffffff</value></variable>
	<variable name="FG_L_Ink2"><value condition="Control.HasFocus(510)">9e0f1115</value><value>a8ffffff</value></variable>
	<variable name="FG_L_ChipEdge"><value condition="Control.HasFocus(510)">730f1115</value><value>66ffffff</value></variable>
	<variable name="FG_L_RowSub">
		<value condition="String.IsEqual(ListItem.DBType,episode)">$LOCALIZE[20359] $INFO[ListItem.Episode]$INFO[ListItem.Premiered,  ·  ,]</value>
		<value condition="String.IsEqual(ListItem.DBType,season)">$INFO[ListItem.Property(TotalEpisodes),, $LOCALIZE[20360]]$INFO[ListItem.Year,  ·  ,]</value>
		<value condition="String.IsEqual(ListItem.DBType,tvshow) + Integer.IsEqual(ListItem.Property(TotalSeasons),1)">$INFO[ListItem.Year]  ·  1 $LOCALIZE[20373]$INFO[ListItem.Genre,  ·  ,]</value>
		<value condition="String.IsEqual(ListItem.DBType,tvshow)">$INFO[ListItem.Year]$INFO[ListItem.Property(TotalSeasons),  ·  , $LOCALIZE[33054]]$INFO[ListItem.Genre,  ·  ,]</value>
		<value condition="String.IsEqual(ListItem.DBType,set)">$VAR[FG_L_FilmCount]</value>
		<value>$INFO[ListItem.Year]$INFO[ListItem.Genre,  ·  ,]</value>
	</variable>
	<!-- 0.56.8 the list row rule: the HDR chip; the time left of a film / episode in progress (the helper's timeleft.py
	     keeps it per item in aeon.left.<k>; a condition compares two info labels written bare, $INFO[] is not
	     read there), else the run time; shows, seasons and sets watched / total -->
	<variable name="FG_L_HdrChip">
		<value condition="String.IsEqual(ListItem.HdrType,dolbyvision) + !String.IsEmpty(Window(Home).Property(aeon.dvp)) + String.IsEqual(ListItem.FileNameAndPath,Window(Home).Property(aeon.dvp.path))">DV $INFO[Window(Home).Property(aeon.dvp)]</value>
		<value condition="String.IsEqual(ListItem.HdrType,dolbyvision)">DV</value>
		<value condition="String.IsEqual(ListItem.HdrType,hdr10plus)">HDR10+</value>
		<value condition="String.IsEqual(ListItem.HdrType,hdr10)">HDR10</value>
		<value condition="String.IsEqual(ListItem.HdrType,hlg)">HLG</value>
	</variable>
	<variable name="FG_L_RowRight">
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.1.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.1.type))">$INFO[Window(Home).Property(aeon.left.1.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.2.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.2.type))">$INFO[Window(Home).Property(aeon.left.2.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.3.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.3.type))">$INFO[Window(Home).Property(aeon.left.3.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.4.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.4.type))">$INFO[Window(Home).Property(aeon.left.4.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.5.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.5.type))">$INFO[Window(Home).Property(aeon.left.5.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.6.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.6.type))">$INFO[Window(Home).Property(aeon.left.6.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.7.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.7.type))">$INFO[Window(Home).Property(aeon.left.7.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.8.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.8.type))">$INFO[Window(Home).Property(aeon.left.8.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.9.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.9.type))">$INFO[Window(Home).Property(aeon.left.9.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.10.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.10.type))">$INFO[Window(Home).Property(aeon.left.10.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.11.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.11.type))">$INFO[Window(Home).Property(aeon.left.11.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.12.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.12.type))">$INFO[Window(Home).Property(aeon.left.12.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.13.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.13.type))">$INFO[Window(Home).Property(aeon.left.13.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.14.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.14.type))">$INFO[Window(Home).Property(aeon.left.14.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.15.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.15.type))">$INFO[Window(Home).Property(aeon.left.15.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.16.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.16.type))">$INFO[Window(Home).Property(aeon.left.16.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.17.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.17.type))">$INFO[Window(Home).Property(aeon.left.17.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.18.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.18.type))">$INFO[Window(Home).Property(aeon.left.18.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.19.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.19.type))">$INFO[Window(Home).Property(aeon.left.19.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.20.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.20.type))">$INFO[Window(Home).Property(aeon.left.20.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.21.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.21.type))">$INFO[Window(Home).Property(aeon.left.21.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.22.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.22.type))">$INFO[Window(Home).Property(aeon.left.22.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.23.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.23.type))">$INFO[Window(Home).Property(aeon.left.23.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.24.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.24.type))">$INFO[Window(Home).Property(aeon.left.24.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.25.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.25.type))">$INFO[Window(Home).Property(aeon.left.25.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.26.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.26.type))">$INFO[Window(Home).Property(aeon.left.26.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.27.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.27.type))">$INFO[Window(Home).Property(aeon.left.27.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.28.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.28.type))">$INFO[Window(Home).Property(aeon.left.28.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.29.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.29.type))">$INFO[Window(Home).Property(aeon.left.29.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.30.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.30.type))">$INFO[Window(Home).Property(aeon.left.30.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.31.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.31.type))">$INFO[Window(Home).Property(aeon.left.31.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.32.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.32.type))">$INFO[Window(Home).Property(aeon.left.32.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.33.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.33.type))">$INFO[Window(Home).Property(aeon.left.33.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.34.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.34.type))">$INFO[Window(Home).Property(aeon.left.34.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.35.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.35.type))">$INFO[Window(Home).Property(aeon.left.35.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.36.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.36.type))">$INFO[Window(Home).Property(aeon.left.36.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.37.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.37.type))">$INFO[Window(Home).Property(aeon.left.37.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.38.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.38.type))">$INFO[Window(Home).Property(aeon.left.38.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.39.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.39.type))">$INFO[Window(Home).Property(aeon.left.39.hmb)]</value>
		<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.40.id)) + String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.40.type))">$INFO[Window(Home).Property(aeon.left.40.hmb)]</value>
		<value condition="String.IsEqual(ListItem.DBType,tvshow) | String.IsEqual(ListItem.DBType,season)">$INFO[ListItem.Property(WatchedEpisodes)] / $INFO[ListItem.Property(TotalEpisodes)]</value>
		<value condition="String.IsEqual(ListItem.DBType,set)">$INFO[ListItem.Property(Watched)] / $INFO[ListItem.Property(Total)]</value>
		<value>$VAR[Aeon_DurHM]</value>
	</variable>
	<variable name="FG_L510_Poster">
		<value condition="String.IsEqual(Container(510).ListItem.DBType,episode) + !String.IsEmpty(Container(510).ListItem.Art(season.poster))">$INFO[Container(510).ListItem.Art(season.poster)]</value>
		<value condition="String.IsEqual(Container(510).ListItem.DBType,episode)">$INFO[Container(510).ListItem.Art(tvshow.poster)]</value>
		<value condition="!String.IsEmpty(Container(510).ListItem.Art(poster))">$INFO[Container(510).ListItem.Art(poster)]</value>
		<value condition="!String.IsEmpty(Container(510).ListItem.Art(tvshow.poster))">$INFO[Container(510).ListItem.Art(tvshow.poster)]</value>
		<value>$INFO[Container(510).ListItem.Art(thumb)]</value>
	</variable>
	<variable name="FG_L510_Meta">
		<value condition="String.IsEqual(Container(510).ListItem.DBType,tvshow)">$INFO[Container(510).ListItem.Year]$VAR[FG_L510_Cert]$VAR[FG_L510_Seasons]</value>
		<value condition="String.IsEqual(Container(510).ListItem.DBType,season)">$INFO[Container(510).ListItem.Year,,  ·  ]$INFO[Container(510).ListItem.Property(TotalEpisodes),, $LOCALIZE[20360]]</value>
		<value condition="String.IsEqual(Container(510).ListItem.DBType,set)">$INFO[Container(510).ListItem.Property(Total),, $LOCALIZE[31114]]</value>
		<value condition="String.IsEqual(Container(510).ListItem.DBType,episode) + !String.IsEmpty(Container(510).ListItem.Premiered)">$INFO[Container(510).ListItem.Premiered]$VAR[FG_L510_Cert]$VAR[FG_L510_Run2]$INFO[Container(510).ListItem.EndTimeResume,  ·  $LOCALIZE[31030] ,]</value>
		<value condition="String.IsEqual(Container(510).ListItem.DBType,episode)">$VAR[FG_L510_Run]$INFO[Container(510).ListItem.EndTimeResume,  ·  $LOCALIZE[31030] ,]</value>
		<value>$INFO[Container(510).ListItem.Year]$VAR[FG_L510_Cert]$VAR[FG_L510_Run2]$INFO[Container(510).ListItem.EndTimeResume,  ·  $LOCALIZE[31030] ,]</value>
	</variable>
	<variable name="FG_L510_Cert">
		<value condition="$EXP[Aeon_CertKnown] + Control.HasFocus(510)">  ·  $VAR[Aeon_Cert]</value>
		<value condition="!String.IsEmpty(Container(510).ListItem.MPAA) + !String.Contains(Container(510).ListItem.MPAA,:)">$INFO[Container(510).ListItem.MPAA,  ·  ,]</value>
	</variable>
	<variable name="FG_L510_Seasons">
		<value condition="Integer.IsEqual(Container(510).ListItem.Property(TotalSeasons),1)">  ·  1 $LOCALIZE[20373]</value>
		<value>$INFO[Container(510).ListItem.Property(TotalSeasons),  ·  , $LOCALIZE[33054]]</value>
	</variable>
	<variable name="FG_L510_Run">
		<value condition="Integer.IsGreater(Container(510).ListItem.Duration(mins),59)">$INFO[Container(510).ListItem.Duration(h)]h $INFO[Container(510).ListItem.Duration(mm)]m</value>
		<value>$INFO[Container(510).ListItem.Duration(mins),, min]</value>
	</variable>
	<variable name="FG_L510_Run2">
		<value condition="Integer.IsGreater(Container(510).ListItem.Duration(mins),59)">  ·  $INFO[Container(510).ListItem.Duration(h)]h $INFO[Container(510).ListItem.Duration(mm)]m</value>
		<value>$INFO[Container(510).ListItem.Duration(mins),  ·  , min]</value>
	</variable>
	<variable name="FG_L_ContentIcon">
		<value condition="Container.Content(tvshows) | Container.Content(seasons) | Container.Content(episodes)">aeon/icons/tv.png</value>
		<value>common/aeon_film.png</value>
	</variable>
'''

AZ510 = ''


def main():
    global AZ510
    for (w, h, r) in ((587, 880, 18), (128, 72, 12), (274, 420, 16), (96, 144, 10)):
        rounded_mask(w, h, r)
    ring_textures()
    v = io.open(VIDEO, encoding='utf-8').read()
    # the A-Z jump list's content (letters and their jumps) as the Aeon List view has it
    m = re.search(r'<control type="list" id="5102">.*?(<content>.*?</content>)', v, re.S)
    AZ510 = re.sub(r'\s*\n\s*', '', m.group(1))
    import fg_lib_walls
    import fg_lib_lists
    import fg_lib_lists2
    import fg_lib_music
    import fg_lib_seasons
    body = ('\t<!-- FG_LIB:begin (written by _src/fg_lib.py) ===================== Fused Glass library views (0.47.0+) -->\n'
            + COMMON + mark_exprs('') + mark_exprs('510') + media_vars('510') + status_vars('510') + LIST_VARS + view510()
            + fg_lib_walls.build(AZ510) + fg_lib_lists.build(AZ510) + fg_lib_lists2.build(AZ510) + fg_lib_music.build(AZ510) + fg_lib_seasons.build(AZ510) + '\t<!-- FG_LIB:end -->\n')
    f = io.open(FUSED, encoding='utf-8').read()
    f = re.sub(r'\t<!-- FG_LIB:begin.*?<!-- FG_LIB:end -->\n', '', f, flags=re.S)
    f = f.replace('</includes>', body + '</includes>')
    import fg_lib_focus                 # 0.56.2: the views follow Focus highlight (Pill, Flat, Frosted, Outline, Tight)
    f = fg_lib_focus.apply(f)
    io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(f)
    # the List view loads the Fused Glass include instead of the Aeon one in Fused Glass
    if 'name="Aeon_510_ViewAeon"' not in v:
        a = '\t<include name="Aeon_510_View">\n'
        assert v.count(a) == 1
        v = v.replace(a, '\t<!-- 0.47.0: Fused Glass loads its own List view (FG_V510_View, _src/fg_lib.py) -->\n'
                         '\t<include name="Aeon_510_View">\n\t\t<include condition="Skin.HasSetting(aeon.fglass)">FG_V510_View</include>\n'
                         '\t\t<include condition="!Skin.HasSetting(aeon.fglass)">Aeon_510_ViewAeon</include>\n\t</include>\n'
                         '\t<include name="Aeon_510_ViewAeon">\n', 1)
        io.open(VIDEO, 'w', encoding='utf-8', newline='\n').write(v)
    # 0.47.0: the walls load their Fused Glass includes the same way
    w2 = io.open(VIEWS2, encoding='utf-8').read()
    for cid in fg_lib_walls.WALLS:
        if 'name="Aeon_V%d_ViewAeon"' % cid in w2:
            continue
        a = '\t<include name="Aeon_V%d_View">\n' % cid
        assert w2.count(a) == 1, cid
        w2 = w2.replace(a, '\t<!-- 0.47.0: Fused Glass loads its own view (FG_V%(c)d_View, _src/fg_lib_walls.py) -->\n'
                           '\t<include name="Aeon_V%(c)d_View">\n\t\t<include condition="Skin.HasSetting(aeon.fglass)">FG_V%(c)d_View</include>\n'
                           '\t\t<include condition="!Skin.HasSetting(aeon.fglass)">Aeon_V%(c)d_ViewAeon</include>\n\t</include>\n'
                           '\t<include name="Aeon_V%(c)d_ViewAeon">\n' % {'c': cid}, 1)
    io.open(VIEWS2, 'w', encoding='utf-8', newline='\n').write(w2)
    # 0.48.0: Flix, Circles, Combined, Low list, Episode list, Banner list, Compact list and Season list the same way
    for path, name, cid in ((VIDEO, 'Aeon_511_View', 511), (VIDEO, 'Aeon_V527_View', 527), (VIEWS3, 'Aeon_V528_View', 528),
                            (VIEWS3, 'Aeon_V529_View', 529), (VIEWS3, 'Aeon_V536_View', 536),
                            (VIEWS2, 'Aeon_V522_View', 522), (VIEWS2, 'Aeon_V524_View', 524), (VIDEO, 'Aeon_512_View', 512),
                            (MUSICLIB, 'Aeon_513_View', 513), (VIEWS2, 'Aeon_V530_View', 530), (VIEWS2, 'Aeon_V531_View', 531),
                            (VIEWS2, 'Aeon_V532_View', 532), (VIEWS2, 'Aeon_V533_View', 533), (VIEWS2, 'Aeon_V534_View', 534)):
        s = io.open(path, encoding='utf-8').read()
        if 'name="%sAeon"' % name in s:
            continue
        a = '\t<include name="%s">\n' % name
        assert s.count(a) == 1, name
        s = s.replace(a, '\t<!-- 0.48.0: Fused Glass loads its own view (FG_V%(c)d_View, _src/fg_lib_lists.py) -->\n'
                         '\t<include name="%(n)s">\n\t\t<include condition="Skin.HasSetting(aeon.fglass)">FG_V%(c)d_View</include>\n'
                         '\t\t<include condition="!Skin.HasSetting(aeon.fglass)">%(n)sAeon</include>\n\t</include>\n'
                         '\t<include name="%(n)sAeon">\n' % {'c': cid, 'n': name}, 1)
        io.open(path, 'w', encoding='utf-8', newline='\n').write(s)
    # the title font (the title face at 50) and the tagline font (the body font slanted) as plain fonts in every font
    # set: the helper (fonts.py) makes the section copies (lb_title_50, lb_tag_22 ...) from the plain fonts each time
    # it writes its block, so section copies written here would be lost on the box
    fx = io.open(FONT, encoding='utf-8').read()
    if '<name>title_50</name>' not in fx:
        fx, n = re.subn(r'(\t\t<font><name>aeon_title_66</name><filename>([^<]+)</filename>[^\n]*\n)',
                        lambda m: m.group(1) + '\t\t<font><name>title_50</name><filename>%s</filename><size>50</size><linespacing>0.95</linespacing></font>\n' % m.group(2), fx)
        assert n == 7, n
    if '<name>tag_22</name>' not in fx:
        fx, n = re.subn(r'(\t\t<font><name>ui_22</name><filename>([^<]+)</filename><size>22</size></font>\n)',
                        lambda m: m.group(1) + '\t\t<font><name>tag_22</name><filename>%s</filename><size>22</size><style>italics</style></font>\n' % m.group(2), fx)
        assert n == 7, n
    io.open(FONT, 'w', encoding='utf-8', newline='\n').write(fx)
    import xml.etree.ElementTree as ET
    for name in (FUSED, VIDEO, VIEWS2, VIEWS3, MUSICLIB, FONT):
        ET.parse(name)
    print('ok')


if __name__ == '__main__':
    main()
