# -*- coding: utf-8 -*-
"""0.56.0 Skin settings preview cards (SkinSettings.xml), one generator for all of them.

The user (2026-11-15): "fix the existing cards but also make more previews for options which genuinely can have them".
Each settings page gets one preview container in the right column, shown while a row with a preview has the focus:
  - Glass and the Aeon theme with Menu theme Fuse: the card (Aeon_Glass) beside the settings, 280 x 470 from the first row;
  - Aeon menu styles (Mosaic, Ledger, Bridge, Tab slab): no card of its own, the styles' side column (1500..1820) is it;
  - Fused Glass: a full-height third card 1552..1824 x 108..974, like the Home menu page's side card, the content 12 px
    in from both of its edges.
Inside: PREVIEW, a caption, a 248 x 140 drawing (a small screen) and, for some rows, a few lines of text (now 196 px
tall in a readable font; it was 46 px and cut long texts off).
The drawings of the older previews are kept (_src/skin_previews_legacy.json, taken from the window once); the new ones
are drawn here on a "small screen" (1920 x 1080 scaled into 248 x 140). Many follow the current choice live: they use the
skin's own pictures and colour variables (vignette, Material, focus highlight) or switch with the setting.
Run from the skin folder: python _src/skin_previews.py  (safe to run again)."""
import io
import json
import os
import re

P = os.path.join('1080i', 'SkinSettings.xml')
LEGACY = os.path.join('_src', 'skin_previews_legacy.json')
BEGIN, END = '<!-- PREVIEW CARD %s (_src/skin_previews.py) -->', '<!-- /PREVIEW CARD %s -->'
W1, W2, W3 = 'f0ffffff', 'a0ffffff', '6cffffff'
CARD_H = 470                 # Glass / Aeon card height
X0, Y0, MW, MH = 16, 96, 248, 140
KX, KY = MW / 1920.0, MH / 1080.0


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def vis(c):
    return '<visible>%s</visible>' % esc(c) if c else ''


# ---------------------------------------------------------------------------------------------------- small screen
def R(x, y, w, h, col, cond=None, tex='common/white.png', border=None, aspect=None):
    """a rectangle given in screen coordinates (1920 x 1080), drawn into the 248 x 140 small screen"""
    L, T = X0 + int(round(x * KX)), Y0 + int(round(y * KY))
    W = max(1, int(round((x + w) * KX)) - int(round(x * KX)))
    H = max(1, int(round((y + h) * KY)) - int(round(y * KY)))
    return ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>%s'
            '<texture%s colordiffuse="%s">%s</texture>%s</control>'
            % (L, T, W, H, '<aspectratio>%s</aspectratio>' % aspect if aspect else '',
               ' border="%s"' % border if border else '', col, tex, vis(cond)))


def A(x, y, w, h, col, cond=None, tex='common/white.png', border=None):
    """a rectangle in card coordinates (for the larger, not-to-scale samples)"""
    return ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
            '<texture%s colordiffuse="%s">%s</texture>%s</control>'
            % (x, y, w, h, ' border="%s"' % border if border else '', col, tex, vis(cond)))


def T(x, y, w, h, text, col=W1, font='st_cap_10', align='left', cond=None, card=False):
    if not card:
        x, y = X0 + int(round(x * KX)), Y0 + int(round(y * KY))
        w, h = max(8, int(round(w * KX))), max(8, int(round(h * KY)))
    return ('<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><align>%s</align>'
            '<aligny>center</aligny><font>%s</font><textcolor>%s</textcolor><label>%s</label>%s</control>'
            % (x, y, w, h, align, font, col, esc(text), vis(cond)))


# 0.56.20 (the user: the previews should show "real fanart from the skin backgrounds clear design add-on, real panels,
# and a description of tint / opacity per option"): the picture behind every card is real fanart: Skin Backgrounds -
# Clear Design (resource.images.skinbackgrounds.clear, optional) for the card's subject, else the library fanart the
# helper keeps for the settings backdrop (Window(Home) aeon.bgfan), else the skin's own picture.
PICS = ('movies', 'tvshows', 'music', 'video')
PIC_FOR = {'music': 'music', 'player': 'video', 'screensaver': 'tvshows'}
PIC_BEGIN, PIC_END = '\t<!-- PREVIEW PICTURES (_src/skin_previews.py) -->', '\t<!-- /PREVIEW PICTURES -->'
CTX = ['movies']


def pic(ctx=None):
    return '$VAR[Aeon_PrevPic_%s]' % (ctx or CTX[0])


def pic_vars():
    # 0.56.22 (the user: "can't we just take one of the images from that addon ... without having users redownload the
    # entire addon"): the four pictures are bundled (media/previews/clear_<subject>.jpg, 960 px, CC BY-SA 3.0 US like the
    # pack, see media/previews/LICENSE.txt), so the skin no longer imports the add-on.
    o = [PIC_BEGIN]
    for p in PICS:
        o.append('\t<variable name="Aeon_PrevPic_%s">\n\t\t<value>previews/clear_%s.jpg</value>\n\t</variable>' % (p, p))
    return '\n'.join(o + [PIC_END])


def ground(fan=True, dim='99000000'):
    """the small screen's ground: the dark page, a picture over it, a little darker"""
    o = R(0, 0, 1920, 1080, 'ff0e0e0e')
    if fan:
        o += R(0, 0, 1920, 1080, 'ffffffff', tex=pic(), aspect='scale')
        if dim[:2] != '00':          # Kodi takes colordiffuse 00000000 as "not set" and draws it white
            o += R(0, 0, 1920, 1080, dim)
    return o


# ---------------------------------------------------------------------------------------------------- the option table
# 0.56.20: under the sample, one line per option: a swatch (that option drawn over the same picture), its name and its
# number (how dark the tint is, or how much of the picture shows); the option in use bright. Card coordinates.
TINT, PICTURE, BLURRED = '$ADDON[skin.aeon.fuse 32626]', '$ADDON[skin.aeon.fuse 32627]', '$ADDON[skin.aeon.fuse 32628]'


def blur_mark(x, y, cond=None):
    """the picture behind is blurred: a soft dot before the number (the legend under the table says it in words)"""
    return A(x, y, 20, 20, 'b3ffffff', cond, tex='aeon/icons/blur.png')


def option_table(head, rows, top=248, cond=None, legend=False):
    """rows: (name label, condition of the option in use, swatch drawer (x, y) -> controls, value label, value
    condition or None, blurred). head: the column's word (Tint / Picture). legend: the blur mark's line under it."""
    o = '<control type="group"><top>%d</top>%s' % (top, vis(cond))
    o += T(150, 0, 114, 24, '[UPPERCASE]%s[/UPPERCASE]' % head, '66ffffff', 'st_cap_14', 'right', card=True)
    for i, row in enumerate(rows):
        name, now, swatch, value, vcond = row[:5]
        y = 28 + i * 34
        o += swatch(16, y + 2)
        o += T(70, y, 120, 30, name, W1, 'st_small_20_semibold', 'left', now, card=True)
        o += T(70, y, 120, 30, name, '8cffffff', 'st_small_20', 'left', '!' + now, card=True)
        # a value can depend on other settings (the theme, the backdrop strength, the material): a list of
        # (number, condition, blurred), one shows
        values = value if isinstance(value, list) else [(value, vcond, len(row) > 5 and row[5])]
        for text, c, blurred in values:
            o += T(190, y, 74, 30, text, W2, 'st_small_20', 'right', c, card=True)
            if blurred:
                o += blur_mark(170, y + 5, c)
    if legend:
        y = 28 + len(rows) * 34 + 8
        o += blur_mark(16, y + 5) + T(44, y, 220, 30, BLURRED, '8cffffff', 'st_small_20', card=True)
    return o + '</control>'


def sw_panel(fill, edge):
    """a swatch: the picture, then a panel in that fill with that edge"""
    def draw(x, y):
        return (A(x, y, 44, 26, 'ffffffff', tex=pic()) + A(x, y, 44, 26, fill, tex='fg/r8.png', border='4') +
                A(x, y, 44, 26, edge, tex='fg/e28.png', border='6'))
    return draw


def sample_panel(fill, edge, top=96):
    """the real panel at its real size: the picture, a card in the fill in use, and real text on it"""
    return (A(16, top, 248, 140, 'ffffffff', tex=pic()) + A(28, top + 50, 224, 80, fill, tex='fg/r8.png', border='8') +
            A(28, top + 50, 224, 80, edge, tex='fg/e28.png', border='14') +
            T(42, top + 58, 200, 32, 'Lawrence of Arabia', W1, 'st_ui_22_bold', card=True) +
            T(42, top + 90, 200, 28, '1962  ·  3h 47m', 'b3ffffff', 'st_small_20', card=True))


def lines(x, y, widths, gap=44, h=18, col='66ffffff'):
    return ''.join(R(x, y + i * gap, w, h, col) for i, w in enumerate(widths))


def spotlight(y=140):
    """Home: the spotlight's title, chips and plot at the top left"""
    return (R(96, y, 620, 80, 'e6ffffff') +
            ''.join(R(96 + i * 110, y + 120, 96, 30, '55ffffff') for i in range(4)) + lines(96, y + 190, (700, 620)))


def menu_row(y, names=True, caps=False):
    """Home: the menu row (Movies, TV shows, Music) with the focused item bright, and the tiles under it"""
    o = ''
    for i, w in enumerate((300, 340, 260)):
        x = 96 + sum((300, 340, 260)[:i]) + i * 70
        o += R(x, y, w, 56, 'f0ffffff' if i == 1 else '55ffffff')
    o += R(96 + 300 + 70, y + 74, 80, 8, 'fg_mark')
    return o


def tiles(y, n=6, w=260, h=150, col='88ffffff'):
    return ''.join(R(96 + i * (w + 24), y, w, h, col) for i in range(n))


def osd_card(y=760, h=260, col='cc0e0e0e'):
    """the player controls: a card at the bottom with the title, the seek line and the buttons"""
    return (R(96, y, 1728, h, col) + R(140, y + 40, 520, 44, 'e6ffffff') + R(140, y + 110, 1640, 8, '44ffffff') +
            R(140, y + 110, 900, 8, 'fg_mark') + ''.join(R(140 + i * 90, y + 160, 56, 56, '88ffffff') for i in range(5)))


def posters(y=200, n=6, w=250, h=375, gap=28, x0=96, col='77ffffff'):
    return ''.join(R(x0 + i * (w + gap), y, w, h, col) for i in range(n))


# ---------------------------------------------------------------------------------------------------- the new previews
# caption ids: the skin's own captions where there is one, else Kodi's names in capitals
CAP = {'home': '[UPPERCASE]$LOCALIZE[10000][/UPPERCASE]', 'library': '$LOCALIZE[31824]', 'screensaver': '$LOCALIZE[31688]',
       'info': '[UPPERCASE]$LOCALIZE[19033][/UPPERCASE]', 'player': '[UPPERCASE]$LOCALIZE[14200][/UPPERCASE]',
       'music': '$LOCALIZE[31685]', 'boxes': '$LOCALIZE[31826]', 'sample': '$LOCALIZE[31686]', 'skin': '[UPPERCASE]$LOCALIZE[166][/UPPERCASE]',
       'menu': '[UPPERCASE]$LOCALIZE[33061][/UPPERCASE]', 'toasts': '[UPPERCASE]$LOCALIZE[25000][/UPPERCASE]',
       'cast': '[UPPERCASE]$LOCALIZE[206][/UPPERCASE]', 'movies': '[UPPERCASE]$LOCALIZE[342][/UPPERCASE]', 'ratings': '$LOCALIZE[31450]'}


def S(name):
    return 'Skin.String(%s)' % name


def eq(name, v):
    return 'String.IsEqual(Skin.String(%s),%s)' % (name, v)


def empty_or(name, v):
    return '[String.IsEmpty(Skin.String(%s)) | String.IsEqual(Skin.String(%s),%s)]' % (name, name, v)


def p_watched():
    on_u = '[%s | %s | %s]' % (eq('aeon.watchedmarkers', 'unwatched'), eq('aeon.watchedmarkers', 'both'), 'String.IsEmpty(Skin.String(aeon.watchedmarkers))')
    on_w = '[%s | %s | %s]' % (eq('aeon.watchedmarkers', 'watched'), eq('aeon.watchedmarkers', 'both'), 'String.IsEmpty(Skin.String(aeon.watchedmarkers))')
    o = ground(dim='cc000000') + posters(240, 6, 260, 390, 30)
    for i in range(6):
        x = 96 + i * 290
        if i in (0, 2, 5):         # unwatched: the gold dot
            o += R(x + 200, 260, 40, 40, 'fg_mark', on_u, tex='fg/circle.png')
        elif i in (1, 4):          # watched: the tick
            o += R(x + 190, 254, 56, 56, 'ffffffff', on_w, tex='aeon/icons/check.png')
        else:                      # part watched: the progress ring
            o += R(x + 192, 254, 52, 52, 'ffffffff', on_u, tex='aeon/ring_circle.png')
    return o


def p_trailer():
    hide = 'Skin.HasSetting(aeon.hidetrailer)'
    o = ground() + R(96, 160, 400, 600, '88ffffff') + R(560, 180, 800, 80, 'e6ffffff') + lines(560, 300, (1100, 1000, 900))
    # Play, then Trailer (gold play mark) unless it is hidden, then More
    o += R(560, 700, 220, 80, 'f0ffffff') + R(810, 700, 220, 80, '66ffffff', '!' + hide)
    o += R(895, 715, 50, 50, 'fg_mark', '!' + hide, tex='aeon/icons/play.png')
    return o + R(1060, 700, 220, 80, '66ffffff', '!' + hide) + R(810, 700, 220, 80, '66ffffff', hide)


def p_logos():
    o = ground() + R(96, 160, 380, 570, '88ffffff')
    o += T(540, 150, 1200, 200, 'MATRIX', 'f0ffffff', 'st_font25_title', 'left', '!Skin.HasSetting(aeon.nologos)')
    o += R(540, 200, 760, 70, 'e6ffffff', 'Skin.HasSetting(aeon.nologos)')
    return o + lines(540, 400, (1100, 1000, 820))


def p_sidestrip():
    o = ground(dim='cc000000')
    o += R(0, 0, 100, 1080, 'ffffffff', 'Skin.HasSetting(aeon.vsbwhite)') + R(0, 0, 100, 1080, 'ff1c1c1c', '!Skin.HasSetting(aeon.vsbwhite)')
    o += ''.join(R(30, 300 + i * 90, 40, 40, 'ff0e0e0e', 'Skin.HasSetting(aeon.vsbwhite)', tex='aeon/icons/%s.png' % ic)
                 + R(30, 300 + i * 90, 40, 40, 'ccffffff', '!Skin.HasSetting(aeon.vsbwhite)', tex='aeon/icons/%s.png' % ic)
                 for i, ic in enumerate(('grid', 'search', 'settings')))
    return o + posters(200, 5, 290, 435, 40, 180)


def p_progress():
    o = ground(dim='cc000000') + posters(240, 6, 260, 390, 30)
    for i, f in ((0, 0.6), (2, 0.3), (3, 0.85)):
        x = 96 + i * 290
        o += R(x + 16, 600, 228, 10, '44ffffff', 'Skin.HasSetting(aeon.progressline)')
        o += R(x + 16, 600, int(228 * f), 10, 'fg_mark', 'Skin.HasSetting(aeon.progressline)')
    return o


def p_hmicons():
    o = ground() + spotlight()
    for i, ic in enumerate(('film', 'tv', 'music', 'search', 'power')):
        x = 600 + i * 150
        o += R(x, 780, 90, 90, 'f0ffffff' if i == 1 else '77ffffff', tex='aeon/icons/%s.png' % ic)
        o += R(x - 20, 900, 130, 26, 'f0ffffff' if i == 1 else '66ffffff', None if i == 1 else '!Skin.HasSetting(aeon.hm.icons)')
    return o


def p_toastpill():
    on = 'Skin.HasSetting(aeon.toastpill)'
    o = ground() + spotlight()
    # the clock capsule; with toasts in it, it grows to the left and holds the message
    o += R(1590, 40, 230, 64, 'cc1a1d24', '!' + on, tex='fg/r8.png', border='4') + R(1620, 58, 90, 28, 'e6ffffff', '!' + on)
    o += R(1160, 40, 400, 64, 'cc1a1d24', '!' + on, tex='fg/r8.png', border='4') + R(1190, 58, 320, 28, '99ffffff', '!' + on)
    o += R(1100, 40, 720, 64, 'cc1a1d24', on, tex='fg/r8.png', border='4') + R(1130, 58, 380, 28, '99ffffff', on) + R(1620, 58, 90, 28, 'e6ffffff', on)
    return o


def mat(v):
    if v == 'dark':
        return '[String.IsEmpty(Skin.String(aeon.fgmat)) | %s]' % eq('aeon.fgmat', 'today')
    return eq('aeon.fgmat', v)


def p_material():
    """0.56.20 Library view theme (Skin.String(aeon.fgmat)): the library panel at its real size in the material in use
    (FG_Frost / FG_Edge), then each material: Dark tint 72 %, Frost 55 % over the blurred picture, Raised the same with
    a lit edge, Clear 30 % over the sharp picture (values from _src/fg_material.py)"""
    rows = (('$ADDON[skin.aeon.fuse 32573]', mat('dark'), sw_panel('b814161c', '1fffffff'), '72 %', None),
            ('$ADDON[skin.aeon.fuse 32547]', mat('frost'), sw_panel('8c2a2e38', '33ffffff'), '55 %', None, True),
            ('$ADDON[skin.aeon.fuse 32548]', mat('raised'), sw_panel('8c2a2e38', '66ffffff'), '55 %', None, True),
            ('$ADDON[skin.aeon.fuse 32549]', mat('clear'), sw_panel('4d14161c', '26ffffff'), '30 %', None))
    return sample_panel('$VAR[FG_Frost]', '$VAR[FG_Edge]') + option_table(TINT, rows, legend=True)


def p_shadow():
    """0.56.39 Panel shadow (Skin.String(aeon.fgshadow)) = how high the panels float (the user: "increasing the size of
    the shadow underneath a panel so it seems it is raised higher, nothing to do with outline"). A black shadow only
    shows on a picture, so: the picture, then the shadow in use (shadow_lift_05639 grows and drops it with the
    strength), then the card on top; each strength's swatch is a small card on the picture with its own shadow,
    tighter for Mild, bigger and lower for Strong and Heavy; the outline never changes"""
    top = 96

    def sw(g, d, shadow):
        def draw(x, y):
            return (A(x, y, 44, 26, 'ffffffff', tex=pic()) +
                    A(x + 9 - g, y + 4 - g + d, 26 + 2 * g, 14 + 2 * g, shadow, tex='fg/sho14.png', border='7') +
                    A(x + 10, y + 4, 24, 12, 'd9e8eaf0', tex='fg/r8.png', border='4'))
        return draw
    rows = (('$ADDON[skin.aeon.fuse 32670]', eq('aeon.fgshadow', 'mild'), sw(-1, 0, 'cc000000'), '', None),
            ('$LOCALIZE[31071]', empty_or('aeon.fgshadow', 'medium'), sw(1, 2, 'e6000000'), '', None),
            ('$LOCALIZE[31673]', eq('aeon.fgshadow', 'strong'), sw(3, 4, 'f2000000'), '', None),
            ('$ADDON[skin.aeon.fuse 32671]', eq('aeon.fgshadow', 'heavy'), sw(5, 6, 'ff000000'), '', None))
    o = A(16, top, 248, 140, 'ffffffff', tex=pic())
    # the card high on the picture, so the shadow under it has picture to fall on
    o += A(0, top - 22, 280, 140, '$VAR[FG_PanelSh_80]', tex='fg/sho28.png', border='68')      # 40 px round the card, as the library's cards
    o += (A(40, top + 18, 200, 60, '$VAR[FG_Frost]', tex='fg/r8.png', border='8') + A(40, top + 18, 200, 60, '$VAR[FG_Edge]', tex='fg/e28.png', border='14') +
          T(52, top + 22, 180, 30, 'Lawrence of Arabia', W1, 'st_ui_22_bold', card=True) +
          T(52, top + 48, 180, 26, '1962  ·  3h 47m', 'b3ffffff', 'st_small_20', card=True))
    return o + option_table('$ADDON[skin.aeon.fuse 32668]', rows)


def p_xpanel():
    """0.56.28 Expert settings > Panel opacity / blur / tint: the panel at its real size in the glass in use"""
    fg = sample_panel('$VAR[FG_Frost]', '$VAR[FG_Edge]')
    ag = (A(16, 96, 248, 140, 'ffffffff', tex=pic()) + A(28, 146, 224, 80, '$VAR[AG_FillD]', tex='fg/r8.png', border='8') +
          A(28, 146, 224, 80, '$VAR[AG_FillL]', tex='fg/r8.png', border='8') + A(28, 146, 224, 80, '38ffffff', tex='fg/e28.png', border='14') +
          T(42, 154, 200, 32, 'Lawrence of Arabia', W1, 'st_ui_22_bold', card=True) +
          T(42, 186, 200, 28, '1962  \u00b7  3h 47m', 'b3ffffff', 'st_small_20', card=True))
    # 0.56.44: Aeon Glass's cards too
    return ('<control type="group"><visible>Skin.HasSetting(aeon.fglass)</visible>%s</control>'
            '<control type="group"><visible>!Skin.HasSetting(aeon.fglass)</visible>%s</control>' % (fg, ag))


def p_xfan():
    """0.56.28 Expert settings > Fanart opacity / blur / tint: the picture at the library views' fanart alpha, under the
    Frosted tint in use"""
    o = A(16, 96, 248, 140, 'ff08090c') + A(16, 96, 248, 140, '$VAR[Aeon_VFanAlphaG]', tex=pic())
    for name, a in (('', '24'), ('light', '12'), ('strong', '48')):
        o += A(16, 96, 248, 140, a + 'b0c4de', empty_or('aeon.x.ftint', 'default') if not name else eq('aeon.x.ftint', name))
    return o


def p_lyricscover():
    on = 'Skin.HasSetting(aeon.lyrics.cover)'
    o = ground() + R(140, 260, 520, 520, 'aaffffff') + lines(140, 830, (420, 300), 50, 26, '99ffffff')
    o += R(760, 380, 980, 90, 'f0ffffff', '!' + on) + R(760, 500, 760, 70, '77ffffff', '!' + on)
    o += R(180, 430, 440, 64, 'f0ffffff', on) + R(220, 520, 360, 50, 'bbffffff', on)
    return o


def p_pausebar():
    o = ground() + R(900, 440, 120, 200, 'e6ffffff', tex='aeon/icons/pause.png')
    bar = R(140, 900, 1640, 10, '55ffffff') + R(140, 900, 1000, 10, 'fg_mark') + R(140, 940, 160, 30, '99ffffff') + R(1620, 940, 160, 30, '99ffffff')
    o += bar.replace('</control>', vis('!' + eq('aeon.pausebar', 'never')) + '</control>')
    o += T(1500, 980, 300, 70, '5 s', W2, 'st_cap_10', 'right', eq('aeon.pausebar', '5'))
    return o


def p_flags():
    o = ground() + osd_card()
    for i in range(3):
        o += R(1300 + i * 130, 800, 100, 64, 'ccffffff', '!Skin.HasSetting(aeon.osd.noflags)', tex='aeon/icons/flag.png')
    return o


def p_cinema():
    o = R(0, 0, 1920, 1080, 'ff0e0e0e')
    n = {'1': 1, '2': 2, '3': 3}
    for k, cnt in n.items():
        for i in range(cnt):
            o += R(120 + i * 400, 380, 360, 220, '66ffffff', eq('aeon.cinema', k))
            o += R(250 + i * 400, 450, 90, 80, 'ccffffff', eq('aeon.cinema', k), tex='aeon/icons/play.png')
        o += R(120 + cnt * 400, 330, 520, 320, 'e6ffffff', eq('aeon.cinema', k)) + R(330 + cnt * 400, 450, 100, 90, 'ff0e0e0e', eq('aeon.cinema', k), tex='aeon/icons/film.png')
    o += R(700, 330, 520, 320, 'e6ffffff', 'String.IsEmpty(Skin.String(aeon.cinema))') + R(910, 450, 100, 90, 'ff0e0e0e', 'String.IsEmpty(Skin.String(aeon.cinema))', tex='aeon/icons/film.png')
    return o


def p_nplogo():
    on = 'Skin.HasSetting(aeon.osd.nplogo)'
    o = ground() + R(140, 300, 460, 460, 'aaffffff')
    o += T(680, 300, 1100, 160, 'ARTIST', 'f0ffffff', 'st_font25_title', 'left', on) + R(680, 340, 700, 80, 'e6ffffff', '!' + on)
    return o + lines(680, 520, (900, 600), 60, 30, '99ffffff') + R(680, 700, 1100, 10, '44ffffff') + R(680, 700, 600, 10, 'fg_mark')


def p_theme():
    """the skin theme in use: Aeon (square boxes), Glass (clear panels), Fused Glass (rounded frosted cards)"""
    aeon, glass, fg = '!Skin.HasSetting(aeon.vglass)', 'Skin.HasSetting(aeon.vglass) + !Skin.HasSetting(aeon.fglass)', 'Skin.HasSetting(aeon.fglass)'
    o = ground()
    o += R(160, 160, 520, 140, 'aeon_box', aeon) + R(160, 300, 520, 620, 'x_panel', aeon) + R(680, 160, 1080, 760, 'x_raised', aeon)
    o += R(700, 340, 1040, 90, 'aeon_white', aeon)
    o += R(160, 160, 1600, 760, '3a101010', glass) + R(160, 160, 1600, 2, '77ffffff', glass) + R(700, 340, 1040, 90, 'aeon_white', glass)
    o += R(160, 160, 480, 760, 'cc1a1d24', fg, tex='fg/r8.png', border='8') + R(680, 160, 1080, 760, 'cc1a1d24', fg, tex='fg/r8.png', border='8')
    o += R(700, 340, 1040, 90, 'ffffffff', fg, tex='fg/r8.png', border='4')
    return o + lines(720, 500, (700, 600, 760), 110, 30, '77ffffff')


def p_menutheme():
    """Fused Glass: the dialogs' card in the menu theme in use (Dark / Glass); Aeon: the menu style's boxes"""
    fg = 'Skin.HasSetting(aeon.fglass)'
    aeon = '!Skin.HasSetting(aeon.vglass)'
    o = ground(dim='22000000')
    o += R(420, 180, 1080, 720, '$VAR[FG_MenuFill]', fg, tex='fg/r8.png', border='4') + R(420, 180, 1080, 720, '$VAR[FG_Edge]', fg, tex='fg/e28.png', border='6')
    o += R(460, 400, 1000, 100, 'ffffffff', fg, tex='fg/r8.png', border='4')
    ms = {'mosaic': [(420, 180, 600, 160, 'aeon_box'), (1020, 180, 480, 160, 'x_deep'), (420, 340, 1080, 560, 'x_panel')],
          'ledger': [(420, 180, 120, 720, 'aeon_box'), (540, 180, 960, 160, 'x_deep'), (540, 340, 960, 560, 'x_panel')],
          'tabslab': [(420, 180, 300, 90, 'aeon_box'), (720, 180, 780, 90, 'x_deep'), (420, 270, 1080, 630, 'aeon_box'), (450, 400, 1020, 470, 'x_panel')],
          'bridge': [(420, 180, 600, 160, 'aeon_box'), (420, 340, 1080, 560, 'x_panel'), (1020, 260, 480, 160, 'x_deep')]}
    for st, boxes in ms.items():
        cond = aeon + ' + ' + (eq('aeon.menutheme', st) if st != 'bridge' else
                                '!%s + !%s + !%s + !%s' % (eq('aeon.menutheme', 'mosaic'), eq('aeon.menutheme', 'ledger'), eq('aeon.menutheme', 'tabslab'), eq('aeon.menutheme', 'fused')))
        o += ''.join(R(x, y, w, h, c, cond) for x, y, w, h, c in boxes) + R(450 if st != 'ledger' else 560, 520, 1020 if st != 'ledger' else 910, 90, 'aeon_white', cond)
    fuse = aeon + ' + ' + eq('aeon.menutheme', 'fused')
    o += R(420, 180, 1080, 720, 'x_panel', fuse, tex='aeon/card_panel.png', border='4') + R(460, 400, 1000, 100, 'aeon_white', fuse, tex='fg/r8.png', border='4')
    # 0.56.20 Aeon Glass had no sample here (an empty card): its glass card, with Aeon Glass's accent bar flush to the
    # card (menu theme Aeon Glass) or Fused Glass's inset white pill (menu theme Fuse)
    vg = 'Skin.HasSetting(aeon.vglass) + !' + fg
    o += R(420, 180, 1080, 720, '3a101010', vg, tex='fg/r28.png', border='6') + R(420, 180, 1080, 720, '38ffffff', vg, tex='fg/e28.png', border='6')
    o += R(420, 400, 1080, 100, '$VAR[Aeon_Accent]', vg + ' + !' + eq('aeon.menutheme', 'fused'), tex='common/aeon_row_glass.png')
    o += R(460, 400, 1000, 100, 'aeon_white', vg + ' + ' + eq('aeon.menutheme', 'fused'), tex='fg/r8.png', border='4')
    # 0.56.20 Fused Glass: the menu card at its real size in the menu theme in use (FG_MenuFill), then Dark / Glass /
    # Frost with their tint for the material in use (FG_MenuFill in _src/fg_glassmenus.py, Frost 0.56.12)
    # 0.56.24: the menus follow the Menu theme only, no longer the Library view theme (_src/fg_material.py): one tint
    # per theme, the menus' fixed edge
    fill = {'dark': ('d91a1d24', '85 %'), 'glass': ('c8171a20', '78 %'), 'frost': ('b31e2129', '70 %'), 'system': ('00000000', '')}

    def sw_menu(theme):
        def draw(x, y):
            return (A(x, y, 44, 26, 'ffffffff', tex=pic()) + A(x, y, 44, 26, fill[theme][0], tex='fg/r8.png', border='4') +
                    A(x, y, 44, 26, '$VAR[FG_EdgeM]', tex='fg/e28.png', border='6'))
        return draw
    lines_ = [('$ADDON[skin.aeon.fuse 32573]', '[String.IsEmpty(Skin.String(aeon.fgmenu)) | %s]' % eq('aeon.fgmenu', 'dark'), sw_menu('dark'),
               fill['dark'][1], None)]
    for theme, name in (('glass', 32549), ('frost', 32547), ('system', 32402)):   # 0.56.27 Clear; 0.56.29 Fused Glass
        lines_.append(('$ADDON[skin.aeon.fuse %d]' % name, eq('aeon.fgmenu', theme), sw_menu(theme), fill[theme][1], None, theme == 'frost'))
    table = option_table(TINT, lines_, legend=True)
    return ('<control type="group">%s%s</control>' % (vis('!' + fg), o) +
            '<control type="group">%s%s%s</control>' % (vis(fg), sample_panel('$VAR[FG_MenuFill]', '$VAR[FG_EdgeM]'), table))


def p_libbg():
    o = R(0, 0, 1920, 1080, 'ff141518', empty_or('aeon.vbg', 'neutral')) + R(0, 0, 1920, 1080, 'ffffffff', empty_or('aeon.vbg', 'neutral'), tex='aeon/glow_soft.png')
    o += R(0, 0, 1920, 1080, 'ffffffff', eq('aeon.vbg', 'fanart'), tex='common/aeon_bg_default.png', aspect='scale') + R(0, 0, 1920, 1080, 'aa000000', eq('aeon.vbg', 'fanart'))
    o += R(0, 0, 1920, 1080, 'ff3a2a18', eq('aeon.vbg', 'color')) + R(0, 0, 1920, 1080, '66000000', eq('aeon.vbg', 'color'), tex='common/aeon_vignette.png')
    return o + posters(240, 6, 260, 390, 30)


def p_lowmenu():
    low = 'Skin.HasSetting(aeon.lowmenu)'
    o = ground() + spotlight()
    o += menu_row(620).replace('</control>', vis('!' + low) + '</control>') + tiles(760).replace('</control>', vis('!' + low) + '</control>')
    o += menu_row(800).replace('</control>', vis(low) + '</control>') + tiles(930, 7, 210, 120).replace('</control>', vis(low) + '</control>')
    return o


def p_boxes():
    o = ground() + spotlight()
    box = (1712, 0, 208, 108)
    o += R(*box, col='aeon_box', cond=empty_or('aeon.boxbg', 'colors')) + R(*box, col='ff3a3a3c', cond=eq('aeon.boxbg', 'neutral'))
    o += R(*box, col='ffffffff', cond=eq('aeon.boxbg', 'fanart'), tex='common/aeon_bg_default.png', aspect='scale')
    o += R(*box, col='33ffffff', cond=eq('aeon.boxbg', 'follow'))
    return o + R(1740, 20, 150, 70, 'f0ffffff') + menu_row(620) + tiles(760)


def p_focus():
    """the focus highlight in use, on a list in a card (not to scale: three rows of 36)"""
    o = A(16, 96, 248, 140, 'cc1a1d24', tex='fg/r8.png', border='8') + A(16, 96, 248, 140, '$VAR[FG_Edge]', tex='fg/e28.png', border='14')
    o += A(28, 108, 224, 36, 'ffffffff', tex='$VAR[FG_FocusTex]', border='12')       # 0.56.3: no Flat
    o += T(44, 108, 190, 36, '$LOCALIZE[31683]', '$VAR[Aeon_OnBarInk]', 'st_ui_22_bold', card=True)
    o += T(44, 150, 190, 36, '$LOCALIZE[31684]', W1, 'st_ui_22', card=True) + T(44, 190, 190, 36, '$LOCALIZE[31684]', W2, 'st_ui_22', card=True)
    return o


def p_spoilers():
    on = 'Skin.HasSetting(aeon.spoilers)'
    o = ground(dim='cc000000')
    for i in range(3):
        y = 160 + i * 300
        o += R(120, y, 440, 248, '88ffffff') + R(600, y + 20, 700, 50, 'e6ffffff')
        if i == 0:
            o += lines(600, y + 110, (1100, 900), 50, 24, '77ffffff')
        else:
            o += R(120, y, 440, 248, 'ee3a3a3c', on) + R(300, y + 80, 80, 80, 'ccffffff', on, tex='aeon/icons/lock.png')
            o += lines(600, y + 110, (1100, 900), 50, 24, '77ffffff').replace('</control>', vis('!' + on) + '</control>')
    return o


def p_epcode():
    # 0.56.22: five ways (1x01, S01E01, S1 E1, S1 | E1, S1 • E1)
    forms = (('sxe', 'S01E01'), ('sp', 'S1 E1'), ('bar', 'S1 | E1'), ('dot', 'S1 • E1'))
    o = ground(dim='cc000000') + R(120, 260, 520, 292, '88ffffff') + R(700, 290, 900, 70, 'e6ffffff') + lines(700, 420, (1000, 820), 60, 28, '77ffffff')
    o += T(120, 600, 900, 180, '1x01', W1, 'st_ui_22_bold', 'left', '!' + '[%s]' % ' | '.join(eq('aeon.epcode', v) for v, _ in forms))
    for v, text in forms:
        o += T(120, 600, 900, 180, text, W1, 'st_ui_22_bold', 'left', eq('aeon.epcode', v))
    return o


def p_castphotos():
    on = 'Skin.HasSetting(aeon.osd.castphotos)'
    o = ground() + R(96, 160, 380, 570, '88ffffff') + R(540, 180, 900, 80, 'e6ffffff') + lines(540, 300, (1100, 1000), 50, 26)
    for i in range(6):
        x = 540 + i * 210
        o += R(x, 560, 170, 170, 'aaffffff', on, tex='fg/circle.png') + R(x, 760, 170, 26, '88ffffff')
    return o


def p_skipbtn():
    on = 'Skin.HasSetting(aeon.skippy.button)'
    o = ground(dim='33000000')
    return o + R(1460, 880, 360, 100, 'f0ffffff', on, tex='fg/r8.png', border='8') + R(1500, 912, 220, 36, 'ff0e0e0e', on)


def p_segline():
    on = '!Skin.HasSetting(aeon.skippy.noline)'
    o = ground() + osd_card()
    for x, w in ((140, 160), (1500, 280)):
        o += R(x, 870, w, 8, 'ff2f6fa8', on)
    return o


def p_aeonskip():
    clock = eq('aeon.skippy.aeonstyle', 'clock')
    o = ground(dim='33000000') + R(1712, 0, 208, 108, 'aeon_box')
    o += R(1412, 940, 300, 108, 'aeon_white', '!' + clock) + R(1712, 940, 208, 108, 'aeon_box', '!' + clock)
    o += R(1412, 0, 300, 108, 'aeon_white', clock)
    return o


def p_upnext():
    on = '!Skin.HasSetting(aeon.skippy.nonext)'
    o = ground(dim='33000000')
    return (o + R(1180, 700, 640, 300, 'cc1a1d24', on, tex='fg/r8.png', border='8') + R(1210, 730, 300, 170, 'aaffffff', on) +
            R(1540, 740, 250, 40, 'e6ffffff', on) + R(1540, 810, 200, 26, '88ffffff', on) + R(1210, 930, 580, 8, 'fg_mark', on))


def p_cardskip():
    glass = eq('aeon.skippy.cardstyle', 'glass')
    o = ground() + osd_card()
    o += R(1500, 690, 300, 70, 'f0ffffff', '!' + glass, tex='fg/r8.png', border='8')
    o += R(1500, 940, 280, 60, '66ffffff', glass, tex='fg/r8.png', border='8')
    return o


def p_vignette():
    """Home with the vignette in use: the skin's own picture and strength"""
    o = ground(dim='00000000')
    side = 'Skin.HasSetting(aeon.vignette.side)'
    o += R(0, 0, 1920, 1080, '$VAR[Aeon_VignetteCol]', '!%s + !%s' % (eq('aeon.vignette', 'a'), side), tex='common/aeon_vignette.png')
    o += R(0, 0, 1920, 1080, '$VAR[Aeon_VignetteCol]', '!%s + %s' % (eq('aeon.vignette', 'a'), side), tex='common/aeon_vignette_side.png')
    return o + spotlight() + menu_row(620)


def p_vignette_strength():
    """0.56.20 Home vignette: the picture with the vignette in use, then each strength: how dark the edges get
    (Aeon_VignetteCol: Light 55, Medium 99, Strong cc, Heavy ff), in the shape in use (Round / Side)"""
    side = 'Skin.HasSetting(aeon.vignette.side)'

    def sw(alpha):
        def draw(x, y):
            out = A(x, y, 44, 26, 'ffffffff', tex=pic())
            if alpha:
                out += A(x, y, 44, 26, alpha + 'ffffff', '!' + side, tex='common/aeon_vignette.png')
                out += A(x, y, 44, 26, alpha + 'ffffff', side, tex='common/aeon_vignette_side.png')
            return out
        return draw
    off = '[String.IsEmpty(Skin.String(aeon.vignette)) | %s]' % eq('aeon.vignette', 'a')
    rows = (('$LOCALIZE[31548]', off, sw(None), '0 %', None),
            ('$LOCALIZE[31672]', eq('aeon.vignette', 'b'), sw('55'), '33 %', None),
            ('$LOCALIZE[31071]', eq('aeon.vignette', 'c'), sw('99'), '60 %', None),
            ('$LOCALIZE[31673]', eq('aeon.vignette', 'e'), sw('cc'), '80 %', None),
            ('$ADDON[skin.aeon.fuse 32603]', eq('aeon.vignette', 'd'), sw('ff'), '100 %', None))
    return p_vignette() + option_table(TINT, rows)


def p_backdrop():
    """0.56.20 Backdrop strength (Skin.String(aeon.backdrop.dim)): the settings page's ground with the backdrop picture at
    the strength in use (Aeon_BackdropAlpha, FG_BackdropDim), then each strength: how much of the picture shows
    (Light 11 / Medium 24 / Strong 44 %, with Fused Glass's Glass menus 30 / 50 / 70 %)"""
    glass = '$EXP[FG_GlassMenus]'

    def sw(a1, a2):
        def draw(x, y):
            return (A(x, y, 44, 26, 'ff0b0c10') + A(x, y, 44, 26, a1 + 'ffffff', '!' + glass, tex=pic()) +
                    A(x, y, 44, 26, a2 + 'ffffff', glass, tex=pic()))
        return draw
    light, medium, strong = (eq('aeon.backdrop.dim', 'light'), '[String.IsEmpty(Skin.String(aeon.backdrop.dim)) | %s]' % eq('aeon.backdrop.dim', 'medium'),
                             eq('aeon.backdrop.dim', 'strong'))
    rows = (('$LOCALIZE[31672]', light, sw('1c', '4d'), '11 %', '!' + glass),
            ('$LOCALIZE[31071]', medium, sw('3c', '80'), '24 %', '!' + glass),
            ('$LOCALIZE[31673]', strong, sw('70', 'b3'), '44 %', '!' + glass))
    o = (A(16, 96, 248, 140, 'ff0b0c10') + A(16, 96, 248, 140, '$VAR[Aeon_BackdropAlpha]', tex=pic()) +
         A(16, 96, 248, 140, '$VAR[FG_BackdropDim]') +
         A(40, 126, 200, 1, '44ffffff') + T(40, 130, 200, 34, '[UPPERCASE]$LOCALIZE[5][/UPPERCASE]', W1, 'st_ui_22_bold', card=True) +
         A(40, 166, 200, 1, '22ffffff') + T(40, 170, 200, 34, '$LOCALIZE[31200]', W2, 'st_small_20', card=True))
    o += option_table(PICTURE, rows)
    # Fused Glass's Glass menus: the same lines, their numbers
    for i, value in enumerate(('30 %', '50 %', '70 %')):
        o += T(190, 248 + 28 + i * 34, 74, 30, value, W2, 'st_small_20', 'right', glass, card=True)
    return o


def p_ssweather(which):
    o = ground(dim='55000000') + R(140, 760, 560, 60, 'e6ffffff') + R(140, 840, 400, 30, '88ffffff')
    if which == 'weather':
        o += R(1712, 108, 208, 108, 'aeon_box', 'Skin.HasSetting(aeon.ss.weather)') + R(1760, 128, 110, 70, 'e6ffffff', 'Skin.HasSetting(aeon.ss.weather)', tex='aeon/icons/cloud.png')
    else:
        o += R(1712, 0, 208, 108, 'aeon_box', 'Skin.HasSetting(aeon.ss.clock)') + R(1740, 20, 150, 70, 'f0ffffff', 'Skin.HasSetting(aeon.ss.clock)')
    return o


def p_ssbg():
    o = R(0, 0, 1920, 1080, 'ff141518', empty_or('aeon.ssbg', 'neutral')) + R(0, 0, 1920, 1080, 'ffffffff', empty_or('aeon.ssbg', 'neutral'), tex='aeon/glow_soft.png')
    o += R(0, 0, 1920, 1080, 'ffffffff', eq('aeon.ssbg', 'fanart'), tex='common/aeon_bg_default.png', aspect='scale')
    o += R(0, 0, 1920, 1080, 'ff3a2a18', eq('aeon.ssbg', 'color')) + R(0, 0, 1920, 1080, '88000000', eq('aeon.ssbg', 'color'), tex='common/aeon_vignette.png')
    return o + R(140, 300, 420, 420, 'aaffffff') + R(620, 420, 700, 60, 'e6ffffff') + R(620, 510, 480, 30, '88ffffff')


def p_homeband():
    on = 'Skin.HasSetting(aeon.homeband)'
    return ground() + spotlight() + R(0, 600, 1920, 110, '88000000', on) + menu_row(620) + tiles(760)


def p_homebar():
    bar, keys, shelf = eq('aeon.homebar', 'bar'), eq('aeon.homebar', 'keys'), eq('aeon.homebar', 'shelf')
    o = ground() + spotlight()
    o += R(560, 760, 820, 130, '55ffffff', bar, tex='fg/r8.png', border='8')
    o += R(0, 750, 1920, 150, '44ffffff', shelf)
    for i, ic in enumerate(('film', 'tv', 'music', 'search', 'power')):
        x = 600 + i * 150
        o += R(x - 15, 765, 120, 120, '44ffffff', keys, tex='fg/circle.png')
        o += R(x, 780, 90, 90, 'f0ffffff' if i == 1 else '99ffffff', tex='aeon/icons/%s.png' % ic)
    return o


def p_stack():
    """0.56.41 (the user: "the preview makes it seem it's for home item submenus"): a set focused in the row under the
    Home menu (ringed), and under the plot the small posters of the films in it (Includes_Aeon_Home Aeon_H_Stack:
    x 120, y 528, 62 x 93 posters)"""
    on = '!Skin.HasSetting(aeon.nostack)'
    o = ground() + spotlight(110) + menu_row(690) + tiles(800, 6, 260, 150, '66ffffff')
    o += R(90, 794, 272, 162, 'f0ffffff', tex='fg/e8.png', border='4')          # the focused set, ringed
    o += ''.join(R(120 + i * 72, 528, 62, 93, 'ccffffff', on) for i in range(10))
    return o


def p_wsbg():
    o = R(0, 0, 1920, 1080, 'ff141518', eq('aeon.wsbg', 'neutral')) + R(0, 0, 1920, 1080, 'ffffffff', eq('aeon.wsbg', 'neutral'), tex='aeon/glow_soft.png')
    o += R(0, 0, 1920, 1080, 'ffffffff', empty_or('aeon.wsbg', 'fanart'), tex='common/aeon_bg_default.png', aspect='scale') + R(0, 0, 1920, 1080, '88000000', empty_or('aeon.wsbg', 'fanart'))
    o += R(0, 0, 1920, 1080, 'ff3a2a18', eq('aeon.wsbg', 'color'))
    return o + R(140, 200, 900, 90, 'e6ffffff') + lines(140, 340, (1000, 860, 920), 60, 30, '99ffffff') + tiles(820, 6)


def p_weather():
    on = '!Skin.HasSetting(aeon.noweather)'
    o = ground() + spotlight()
    for i in range(14):
        o += R(200 + i * 120, 80 + (i * 37) % 300, 3, 90, '55ffffff', on)
    o += ''.join(R(1100 + i * 140, 40, 110, 110, 'cc1a1d24', on, tex='fg/r8.png', border='8') +
                 R(1125 + i * 140, 60, 60, 60, 'ccffffff', on, tex='aeon/icons/%s.png' % ic) for i, ic in enumerate(('sun', 'cloud', 'rain', 'cloud', 'sun')))
    return o + menu_row(620) + tiles(760)


def p_capsnames():
    on = 'Skin.HasSetting(aeon.hm.caps)'
    o = ground() + spotlight()
    o += T(96, 600, 900, 140, '$LOCALIZE[20343]', W1, 'st_ui_22_bold', 'left', '!' + on)
    o += T(96, 600, 900, 140, '[UPPERCASE]$LOCALIZE[20343][/UPPERCASE]', W1, 'st_ui_22_bold', 'left', on)
    return o + tiles(760)


RT_LOW_ICON = 'ratings/rtrotten.png'          # the rotten tomato for a low score


def p_ratings():
    """0.56.15 (the user: "show them in vertical order ... it gets cut off after two rating suppliers, just list them
    vertically instead. should be an option to use icons or text labels too. an the color and on/off previews respond
    to that setting too. so if icons are on ... then only the number gets colored"): one line per provider that is on,
    its icon or its name (Ratings shown as), the number in the rating colour when Colour is on (the name too as text)"""
    text = 'Skin.HasSetting(aeon.rating.text)'
    col = '$VAR[Aeon_PrevRatingColor]'
    # 0.56.22 (the user: "put the ratings in lower numbers too so you can show off all the colors"): high (green),
    # middle (amber) and low (red) samples, each in its own colour while Colour is on
    rows = (('imdb', 'IMDb', 'ratings/imdb.png', '7.8', '$VAR[Aeon_PrevRatingColor]'),
            ('tmdb', 'TMDb', 'ratings/tmdb.png', '5.6', '$VAR[Aeon_PrevRatingColorMid]'),
            ('rt', 'RT', RT_LOW_ICON, '38%', '$VAR[Aeon_PrevRatingColorLow]'),
            ('trakt', 'Trakt', 'ratings/trakt.png', '8.1', '$VAR[Aeon_PrevRatingColor]'))
    anyon = ' | '.join('Skin.HasSetting(aeon.rating.%s)' % k for k, _, _, _, _ in rows)
    o = '<control type="grouplist"><left>16</left><top>96</top><width>248</width><height>236</height><orientation>vertical</orientation><itemgap>6</itemgap>'
    for key, name, icon, num, col in rows:
        o += ('<control type="grouplist"><width>248</width><height>48</height><orientation>horizontal</orientation><itemgap>12</itemgap>%s'
              '<control type="image"><width>44</width><height>48</height><aspectratio>keep</aspectratio><texture>%s</texture>%s</control>'
              '<control type="label"><width min="10" max="140">auto</width><height>48</height><aligny>center</aligny><font>st_ui_24_bold</font><textcolor>%s</textcolor><label>%s</label>%s</control>'
              '<control type="label"><width min="10" max="140">auto</width><height>48</height><aligny>center</aligny><font>st_ui_24_bold</font><textcolor>%s</textcolor><label>%s</label></control>'
              '</control>' % (vis('Skin.HasSetting(aeon.rating.%s)' % key), icon, vis('!' + text), col, name, vis(text), col, num))
    col = '$VAR[Aeon_PrevRatingColor]'
    o += ('<control type="grouplist"><width>248</width><height>48</height><orientation>horizontal</orientation><itemgap>12</itemgap>%s'
          '<control type="image"><width>40</width><height>48</height><aspectratio>keep</aspectratio><texture colordiffuse="fff2c94c">aeon/icons/star.png</texture></control>'
          '<control type="label"><width min="10" max="140">auto</width><height>48</height><aligny>center</aligny><font>st_ui_24_bold</font><textcolor>%s</textcolor><label>7.8</label></control>'
          '</control>' % (vis('![%s]' % anyon), col))
    return o + '</control>'


def p_chips():
    """0.56.22 Media info chips (row 9780): sample chips in rows, each shown while its switch has it on (a film with a
    sidecar: Lawrence of Arabia's UHD remux), so the card follows the picker."""
    hide = lambda k: '!Skin.HasSetting(aeon.hide.%s)' % k
    show = lambda k: 'Skin.HasSetting(aeon.chip.%s)' % k
    rows = ((('4K', hide('res')), ('2.20:1', hide('aspect')), ('DOLBY VISION', hide('hdr'))),
            (('P7 FEL', hide('dvp')), ('TRUEHD ATMOS', hide('audio')), ('7.1', hide('channels'))),
            (('UHD REMUX', hide('source')), ('MKV', show('container')), ('62.4 MB/S', show('bitrate'))),
            (('61.2 GB', show('size')), ('30 SUBS', show('subs')), ('3D', show('3d'))),
            (('38 CHAPTERS', show('chapters')), ('COMMENTARY', show('commentary'))))
    o = ('<control type="grouplist"><left>16</left><top>84</top><width>248</width><height>250</height><orientation>vertical</orientation>'
         '<itemgap>6</itemgap>')
    for row in rows:
        o += '<control type="grouplist"><width>248</width><height>30</height><orientation>horizontal</orientation><itemgap>6</itemgap>'
        for label, cond in row:
            o += ('<control type="button"><width min="20" max="200">auto</width><height>30</height><label>%s</label><font>st_cap_10</font>'
                  '<textcolor>ffffffff</textcolor><focusedcolor>ffffffff</focusedcolor><disabledcolor>ffffffff</disabledcolor><align>center</align><aligny>center</aligny>'
                  '<textoffsetx>8</textoffsetx><enable>false</enable><texturenofocus border="8" colordiffuse="33ffffff">fg/r8.png</texturenofocus>'
                  '<texturefocus border="8" colordiffuse="33ffffff">fg/r8.png</texturefocus>%s</control>' % (label, vis(cond)))
        o += '</control>'
    return ground(dim='aa000000') + o + '</control>'


def p_epjoin():
    """0.56.23 Episodes in one file as one row (row 9781): Lost season 6 as Kodi lists it (1 LA X, 2 LA X) or joined
    (1-2 LA X), then the next episodes."""
    on = 'Skin.HasSetting(aeon.ep.join)'
    o = ground(dim='cc000000')
    rows_off = (('1', 'LA X (1)', '0:42'), ('2', 'LA X (1)', '0:42'), ('3', 'What Kate Does', '0:43'), ('4', 'The Substitute', '0:43'))
    rows_on = ((u'1–2', 'LA X', '0:42'), ('3', 'What Kate Does', '0:43'), ('4', 'The Substitute', '0:43'), ('5', 'Lighthouse', '0:44'))
    for rows, cond in ((rows_off, '!' + on), (rows_on, on)):
        for i, (num, title, time) in enumerate(rows):
            y = 200 + i * 190
            if i == 0:
                o += R(120, y - 20, 1680, 150, 'e6ffffff', cond)
            ink = 'ff111111' if i == 0 else W1
            o += T(150, y, 220, 110, ('$NUMBER[%s]' % num) if num.isdigit() else num, ink, 'st_cap_12', 'left', cond)   # a bare number is a string id
            o += T(400, y, 1000, 110, title.upper(), ink, 'st_cap_12', 'left', cond)
            o += T(1500, y, 260, 110, time, ink, 'st_cap_12', 'right', cond)
    return o


# ---------------------------------------------------------------------------------------------------- 0.56.20 more tables
# the background rows, Corner boxes, Home bar and Focus highlight get the option table too (the user: "Yes, all rows").
# Picture = how much of the picture shows: the layer's opacity times what the dark layer over it leaves (values from
# Aeon_V_Bg, Aeon_VFanAlpha(G), Aeon_VWashAlpha, Custom_1156_Screensaver.xml, Includes_Aeon_Sub.xml, Aeon_BoxFan).
STRENGTH = (eq('aeon.backdrop.dim', 'light'), empty_or('aeon.backdrop.dim', 'medium'), eq('aeon.backdrop.dim', 'strong'))
FROSTED = '$EXP[Aeon_FanFrosted]'
FG_BLUR = '[$EXP[Aeon_FGlass] + !%s]' % eq('aeon.fgmat', 'clear')


def by_strength(vals, extra=None, blurred=False):
    """[(number, condition, blurred)] for the backdrop strengths Light / Medium / Strong"""
    return [(v, c if not extra else '%s + %s' % (extra, c), blurred) for v, c in zip(vals, STRENGTH)]


def lib_picture(extra=None):
    """the library background's picture share for the background, strength and look in use"""
    def x(c):
        return c if not extra else '%s + %s' % (extra, c)
    fan, col, neu = eq('aeon.vbg', 'fanart'), eq('aeon.vbg', 'color'), empty_or('aeon.vbg', 'neutral')
    return ([('0 %', x(neu), False)] +
            by_strength(('13 %', '27 %', '47 %'), x('%s + %s + %s' % (fan, FROSTED, FG_BLUR)), True) +
            by_strength(('13 %', '27 %', '47 %'), x('%s + %s + !%s' % (fan, FROSTED, FG_BLUR)), False) +
            by_strength(('31 %', '49 %', '69 %'), x('%s + !%s' % (fan, FROSTED))) +
            by_strength(('28 %', '48 %', '60 %'), x(col), True))


def sw_bg(kind, alpha='ff'):
    def draw(x, y):
        if kind == 'neutral':
            return A(x, y, 44, 26, 'ff141518') + A(x, y, 44, 26, '55ffffff', tex='aeon/glow_soft.png')
        if kind == 'color':
            return A(x, y, 44, 26, 'ff3a2a18') + A(x, y, 44, 26, alpha + 'ffffff', tex=pic()) + A(x, y, 44, 26, '88ffffff', tex='common/aeon_vignette.png')
        return A(x, y, 44, 26, 'ff0a0a0c') + A(x, y, 44, 26, alpha + 'ffffff', tex=pic())
    return draw


def bg_rows(key, neutral_default, fanart, colour):
    neu = empty_or(key, 'neutral') if neutral_default else eq(key, 'neutral')
    fan = eq(key, 'fanart') if neutral_default else empty_or(key, 'fanart')
    return [('$LOCALIZE[31549]', neu, sw_bg('neutral'), '0 %', None),
            ('$LOCALIZE[31550]', fan, sw_bg('fanart', fanart[1]), fanart[0], None),
            ('$LOCALIZE[31680]', eq(key, 'color'), sw_bg('color', colour[1]), colour[0], None, True)]


def p_libbg_t():
    rows = [('$LOCALIZE[31549]', empty_or('aeon.vbg', 'neutral'), sw_bg('neutral'), '0 %', None),
            ('$LOCALIZE[31550]', eq('aeon.vbg', 'fanart'), sw_bg('fanart', '7d'),
             by_strength(('13 %', '27 %', '47 %'), '%s + %s' % (FROSTED, FG_BLUR), True) +
             by_strength(('13 %', '27 %', '47 %'), '%s + !%s' % (FROSTED, FG_BLUR)) +
             by_strength(('31 %', '49 %', '69 %'), '!' + FROSTED), None),
            ('$LOCALIZE[31680]', eq('aeon.vbg', 'color'), sw_bg('color', '7a'), by_strength(('28 %', '48 %', '60 %'), None, True), None)]
    return p_libbg() + option_table(PICTURE, rows, legend=True)


def p_ssbg_t():
    return p_ssbg() + option_table(PICTURE, bg_rows('aeon.ssbg', True, ('22 %', '38'), ('67 %', 'ab')), legend=True)


def p_wsbg_t():
    return p_wsbg() + option_table(PICTURE, bg_rows('aeon.wsbg', False, ('100 %', 'ff'), ('67 %', 'ab')), legend=True)


def p_boxes_t():
    def sw(kind):
        def draw(x, y):
            out = A(x, y, 44, 26, 'ffffffff', tex=pic())
            box = (x + 22, y, 22, 13)
            if kind == 'colors':
                return out + A(*box, col='aeon_box')
            if kind == 'neutral':
                return out + A(*box, col='ff3a3a3c')
            if kind == 'fanart':
                return out + A(*box, col='88000000')
            return out + A(*box, col='5c000000')
        return draw
    rows = [('$LOCALIZE[31551]', empty_or('aeon.boxbg', 'colors'), sw('colors'), '0 %', None),
            ('$LOCALIZE[31549]', eq('aeon.boxbg', 'neutral'), sw('neutral'), '0 %', None),
            ('$LOCALIZE[31550]', eq('aeon.boxbg', 'fanart'), sw('fanart'), '47 %', None),
            ('$LOCALIZE[31543]', eq('aeon.boxbg', 'follow'), sw('follow'), lib_picture(), None)]
    return p_boxes() + option_table(PICTURE, rows, legend=True)


def p_homebar_t():
    """Fused Glass Home bar: the frosted glass is the Library view theme's material (FG_Frost), so the number follows it"""
    def sw(kind):
        def draw(x, y):
            out = A(x, y, 44, 26, 'ffffffff', tex=pic())
            if kind == 'bar':
                return out + A(x + 6, y + 9, 32, 10, '$VAR[FG_Frost]', tex='fg/pill10.png', border='5,0,5,0')
            if kind == 'keys':
                return out + ''.join(A(x + 5 + i * 12, y + 8, 10, 10, '$VAR[FG_Frost]', tex='fg/circle.png') for i in range(3))
            if kind == 'shelf':
                return out + A(x, y + 8, 44, 11, '$VAR[FG_Frost]')
            return out
        return draw
    mats = [('72 %', mat('dark'), False), ('55 %', mat('frost'), False), ('55 %', mat('raised'), False), ('30 %', mat('clear'), False)]
    rows = [('$LOCALIZE[31548]', '[String.IsEmpty(Skin.String(aeon.homebar)) | %s]' % eq('aeon.homebar', 'off'), sw('off'), '0 %', None)]
    for key, sid in (('bar', 32576), ('keys', 32577), ('shelf', 32578)):
        rows.append(('$ADDON[skin.aeon.fuse %d]' % sid, eq('aeon.homebar', key), sw(key), mats, None))
    return p_homebar() + option_table(TINT, rows)


def p_homegrad_t():
    """0.56.42 Home gradient: Home with the fade from the bottom in use (Soft = the lower gradient as strong as Home
    vignette makes it, Strong = a second, taller one over it), then Off / Soft / Strong"""
    off, strong = eq('aeon.homegrad', 'off'), eq('aeon.homegrad', 'strong')
    o = ground(dim='00000000') + spotlight()
    o += R(0, 540, 1920, 540, '$VAR[Aeon_VignetteLow]', '!' + off, tex='aeon/osd_scrim_bottom.png')
    o += R(0, 360, 1920, 720, 'b3000000', strong, tex='aeon/osd_scrim_bottom.png')
    o += menu_row(620) + tiles(760)

    def sw(alphas):
        def draw(x, y):
            out = A(x, y, 44, 26, 'ffffffff', tex=pic())
            for a in alphas:
                out += A(x, y, 44, 26, a + '000000', tex='aeon/osd_scrim_bottom.png')
            return out
        return draw
    rows = (('$LOCALIZE[31548]', off, sw(()), '', None),
            ('$ADDON[skin.aeon.fuse 32740]', '[String.IsEmpty(Skin.String(aeon.homegrad)) | %s]' % eq('aeon.homegrad', 'soft'), sw(('a0',)), '', None),
            ('$LOCALIZE[31673]', strong, sw(('a0', 'b3')), '', None))
    return o + option_table(PICTURE, rows)


def p_focus_t():
    """Fused Glass Focus highlight: the white of the focused row (fg/fx_*.png: Pill and Tight solid, Frosted a wash
    of about 18 % with a lit rim, Outline a ring with a 5 % fill)"""
    def sw(tex):
        def draw(x, y):
            return A(x, y, 44, 26, 'cc1a1d24', tex='fg/r8.png', border='4') + A(x + 3, y + 5, 38, 16, 'ffffffff', tex=tex, border='8')
        return draw
    rows = [('$ADDON[skin.aeon.fuse 32409]', empty_or('aeon.fgfocus', 'pill'), sw('fg/fx_pill.png'), '100 %', None),
            ('$ADDON[skin.aeon.fuse 32411]', eq('aeon.fgfocus', 'frost'), sw('fg/fx_frost.png'), '18 %', None),
            ('$ADDON[skin.aeon.fuse 32412]', eq('aeon.fgfocus', 'outline'), sw('fg/fx_outline.png'), '5 %', None),
            ('$ADDON[skin.aeon.fuse 32413]', eq('aeon.fgfocus', 'tight'), sw('fg/fx_tight.png'), '100 %', None)]
    return p_focus() + option_table(TINT, rows)


def p_focus_ag():
    """0.56.44 Aeon Glass Focus highlight (Skin.String(aeon.agfocus)): Glass, the accent bar (default), or Fused Glass's
    pictures (Pill and Tight white with dark text, Frosted a wash, Outline a ring)"""
    def sw(tex, col='ffffffff'):
        def draw(x, y):
            return A(x, y, 44, 26, 'cc1a1d24', tex='fg/r8.png', border='4') + A(x + 3, y + 5, 38, 16, col, tex=tex, border='8')
        return draw
    o = A(16, 96, 248, 140, 'ffffffff', tex=pic()) + A(16, 96, 248, 140, '$VAR[AG_FillD]', tex='fg/r8.png', border='8')
    o += A(16, 96, 248, 140, '$VAR[AG_FillL]', tex='fg/r8.png', border='8') + A(16, 96, 248, 140, '38ffffff', tex='fg/e28.png', border='14')
    o += A(28, 108, 224, 36, '$VAR[Aeon_MenuFocusColR]', tex='$VAR[Aeon_MenuFocusTex]', border='12')
    o += T(44, 108, 190, 36, '$LOCALIZE[31683]', '$VAR[Aeon_OnBarInk]', 'st_ui_22_bold', card=True)
    o += T(44, 150, 190, 36, '$LOCALIZE[31684]', W1, 'st_ui_22', card=True) + T(44, 190, 190, 36, '$LOCALIZE[31684]', W2, 'st_ui_22', card=True)
    rows = [('$ADDON[skin.aeon.fuse 32429]', 'String.IsEmpty(Skin.String(aeon.agfocus))', sw('common/aeon_row_glass64.png', '$VAR[Aeon_Accent]'), '', None),
            ('$ADDON[skin.aeon.fuse 32409]', eq('aeon.agfocus', 'pill'), sw('fg/fx_pill.png'), '100 %', None),
            ('$ADDON[skin.aeon.fuse 32411]', eq('aeon.agfocus', 'frost'), sw('fg/fx_frost.png'), '18 %', None),
            ('$ADDON[skin.aeon.fuse 32412]', eq('aeon.agfocus', 'outline'), sw('fg/fx_outline.png'), '5 %', None),
            ('$ADDON[skin.aeon.fuse 32413]', eq('aeon.agfocus', 'tight'), sw('fg/fx_tight.png'), '100 %', None)]
    return o + option_table(TINT, rows)


def p_agblur():
    """0.56.44 Aeon Glass Panel blur (Skin.String(aeon.agblur)): the menus' backdrop sharp (Off, as before) or blurred"""
    def sw(blurred):
        def draw(x, y):
            return A(x, y, 44, 26, 'ffffffff', tex=pic()) + (A(x, y, 44, 26, '66b0c4de', tex='fg/r8.png', border='4') if blurred else '')
        return draw
    o = A(16, 96, 248, 140, 'ffffffff', tex=pic()) + A(16, 96, 248, 140, '55b0c4de', 'Skin.HasSetting(aeon.vglass) + !String.IsEmpty(Skin.String(aeon.agblur))')
    o += A(28, 146, 224, 80, '$VAR[AG_FillD]', tex='fg/r8.png', border='8') + A(28, 146, 224, 80, '38ffffff', tex='fg/e28.png', border='14')
    o += T(42, 154, 200, 32, 'Lawrence of Arabia', W1, 'st_ui_22_bold', card=True)
    rows = [('$LOCALIZE[31072]', 'String.IsEmpty(Skin.String(aeon.agblur))', sw(False), '', None),
            ('$LOCALIZE[31672]', eq('aeon.agblur', 'light'), sw(True), '', None, True),
            ('$LOCALIZE[31071]', eq('aeon.agblur', 'medium'), sw(True), '', None, True),
            ('$LOCALIZE[31673]', eq('aeon.agblur', 'strong'), sw(True), '', None, True)]
    return o + option_table(PICTURE, rows, legend=True)


def p_dlgbg():
    """0.56.32 Menu background (Skin.String(aeon.fgsdlgbg)), the Fused Glass style's menus and dialogs: a menu at
    screen scale over the item's fanart (Fanart) or over the window it opened on, dimmed (Screen), then the options"""
    scr = eq('aeon.fgsdlgbg', 'screen')
    o = ground(dim='8c06070a')
    # Screen: a library wall behind the menu, under the dim
    o += R(0, 0, 1920, 1080, 'ff12141a', scr)
    for i in range(6):
        for j in range(2):
            o += R(100 + i * 300, 200 + j * 420, 260, 380, '33ffffff', scr, tex='fg/r8.png', border='4')
    o += R(0, 0, 1920, 1080, 'c706070a', scr)
    # the menu: the grid, the divider, the bar on the focused row
    o += R(810, 180, 1, 490, '40ffffff')
    for k in range(8):
        o += R(360, 180 + k * 70, 1200, 2, '2effffff' if k not in (1, 2) else '70ffffff')
    o += R(806, 250, 6, 70, 'ffffffff')
    for k in range(7):
        o += R(846, 205 + k * 70, 260 if k != 1 else 320, 20, 'ccffffff' if k == 1 else '66ffffff')
    o += R(504, 180, 270, 405, 'ffffffff', tex=pic(), aspect='scale')
    rows = (('$LOCALIZE[31550]', 'String.IsEmpty(Skin.String(aeon.fgsdlgbg))',
             lambda x, y: A(x, y, 44, 26, 'ffffffff', tex=pic()) + A(x, y, 44, 26, '8c06070a'), '', None),
            ('$ADDON[skin.aeon.fuse 32690]', scr,
             lambda x, y: A(x, y, 44, 26, 'ff12141a') + A(x + 4, y + 4, 10, 18, '55ffffff') + A(x + 17, y + 4, 10, 18, '55ffffff') + A(x + 30, y + 4, 10, 18, '55ffffff') + A(x, y, 44, 26, 'c706070a'), '', None))
    return o + option_table('$ADDON[skin.aeon.fuse 32527]', rows)


NEW = {
    'look': [(9521, 'library', p_watched), (9522, 'info', p_trailer), (9523, 'info', p_logos), (9524, 'library', p_sidestrip),
             (9527, 'library', p_progress), (9546, 'home', p_hmicons), (9528, 'toasts', p_toastpill), (9529, 'sample', p_shadow)],     # 0.56.28: 9529 is Panel shadow
    'playback': [(9536, 'music', p_lyricscover), (9537, 'player', p_pausebar), (9538, 'player', p_flags), (9539, 'movies', p_cinema),
                 (9550, 'music', p_nplogo)],
    'appearance': [(9744, 'skin', p_theme), (9748, 'menu', p_menutheme), (9745, 'library', p_libbg_t), (9746, 'home', p_lowmenu),
                   (9747, 'boxes', p_boxes_t), (9749, 'sample', p_focus_t), (9742, 'menu', p_backdrop),
                   (9798, 'menu', p_dlgbg), (9791, 'sample', p_xpanel), (9792, 'sample', p_xpanel), (9793, 'sample', p_xpanel),
                   (9515, 'sample', p_focus_ag), (9518, 'sample', p_agblur),     # 0.56.44 Aeon Glass
                   (9794, 'library', p_xfan), (9795, 'library', p_xfan), (9796, 'library', p_xfan)],
    'details': [(9707, 'info', p_spoilers), (9709, 'info', p_epcode), (9761, 'cast', p_castphotos), (9780, 'info', p_chips), (9781, 'library', p_epjoin)],
    'behaviour': [(9727, 'player', p_skipbtn), (9728, 'player', p_segline), (9738, 'player', p_aeonskip), (9729, 'player', p_upnext),
                  (9739, 'player', p_cardskip)],
    'backgrounds': [(9733, 'home', p_vignette_strength), (9765, 'home', p_vignette), (9734, 'screensaver', lambda: p_ssweather('weather')),
                    (9735, 'screensaver', lambda: p_ssweather('clock')), (9736, 'screensaver', p_ssbg_t), (9737, 'home', p_homeband),
                    (9764, 'home', p_homebar_t)],
    'widgets': [(9755, 'home', p_stack), (9756, 'home', p_wsbg_t), (9516, 'home', p_homegrad_t)],     # 0.56.42: 9516 Home gradient
    'time': [(9512, 'home', p_weather)],
    'menu': [(9566, 'home', p_capsnames)],
    'ratings': [(9710, 'ratings', p_ratings), (9711, 'ratings', p_ratings), (9712, 'ratings', p_ratings), (9713, 'ratings', p_ratings),
                (9714, 'ratings', p_ratings), (9768, 'ratings', p_ratings)],
}
# the old drawings that are wrong for their row now (9744 was the accent sample before Skin theme took the id) or off
DROP = {9744, 9710, 9711, 9712, 9713, 9714,   # 0.56.15: the ratings rows' old one-line sample (cut off after two)
        9742}                                  # 0.56.20: Backdrop strength gets the option table (p_backdrop)
# 0.56.12 (_src/settings_sections.py): the theme's own rows moved from Look to Appearance, their previews with them
MOVED = dict((r, 'appearance') for r in (9524, 9525, 9528, 9529, 9546, 9547))
# 0.56.42 (_src/regroup_05642.py): the rows in the new categories; a row's card goes to its page
try:
    from regroup_05642 import PAGES as _RG
    MOVED.update((r, key) for key, _c, _g, _s, order in _RG for r in order if isinstance(r, int))
except ImportError:
    pass
MOVED[9516] = 'home'                   # 0.56.42 Home gradient (_src/rows_05642.py)


# ---------------------------------------------------------------------------------------------------- the window
def ctl_end(t, start):
    depth = 0
    for m in re.finditer(r'<control[ >]|</control>', t[start:]):
        depth += -1 if m.group(0) == '</control>' else 1
        if depth == 0:
            return start + m.end()
    raise ValueError('unbalanced at %d' % start)


def take_legacy(t):
    """the old containers (groups at left 920, top 199): their per-row drawings, then the window without them"""
    rows = {}
    while True:
        m = re.search(r'<control type="group">\s*<left>920</left>\s*<top>199</top>', t)
        if not m:
            break
        s, e = m.start(), ctl_end(t, m.start())
        c = t[s:e]
        page = re.findall(r'<visible>String.IsEqual\(Window\(Home\).Property\(aeon.skincat\),(\w+)\)</visible>', t[:s])[-1]
        for g in re.finditer(r'<control type="group">\s*<visible>Control.HasFocus\((\d+)\)</visible>', c):
            gs = g.start()
            ge = ctl_end(c, gs)
            rid = int(g.group(1))
            inner = c[g.end():ge - len('</control>')]
            rows.setdefault(page, []).append((rid, inner.strip()))
        ls = t.rfind('\n', 0, s)
        t = t[:ls] + t[e:]
    return rows, t


def fix_text(x):
    """the old 46 px text boxes cut long texts off: 196 px, a readable font"""
    return re.sub(r'(<control type="textbox"><left>16</left><top>2[45]\d</top><width>248</width>)<height>\d+</height><font>st_cap_14</font>',
                  r'\1<height>196</height><font>st_small_20</font>', x)


def container(page, rows):
    ids = [r for r, _ in rows]
    cond = ' | '.join('Control.HasFocus(%d)' % r for r in ids)
    o = [BEGIN % page,
         '<control type="group"><left>920</left><top>199</top><width>280</width><height>%d</height>%s' % (CARD_H, vis(cond)),
         '<animation type="Visible" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" time="200"/>'
         '<effect type="slide" start="0,16" end="0,0" time="200" tween="cubic" easing="out"/></animation>',
         # the card: Glass / Aeon with Menu theme Fuse beside the settings; Fused Glass a full-height third card; the Aeon
         # menu styles draw their own side column
         '<control type="group"><width>280</width><height>%d</height><visible>!$EXP[Aeon_FGlass] + !$EXP[Aeon_MS]</visible><include>Aeon_Glass</include></control>' % CARD_H,
         '<control type="group"><left>12</left><top>-91</top><width>272</width><height>866</height><visible>$EXP[Aeon_FGlass]</visible><include>Aeon_Glass</include></control>',
         # Fused Glass: the content 12 px in from the card's sides and 24 px under its top
         # Aeon Bridge: the palette tile stands at the top of the side column (108..274 since 0.56.16), the content starts under it
         '<control type="group"><animation effect="slide" start="0,0" end="8,-80" time="0" condition="$EXP[Aeon_FGlass]">Conditional</animation>'
         '<animation effect="slide" start="0,0" end="0,86" time="0" condition="$EXP[Aeon_MS_bridge]">Conditional</animation>',
         '<control type="label"><left>16</left><top>14</top><width>248</width><height>30</height><font>st_cap_20</font>'
         '<textcolor>$VAR[Aeon_Accent]</textcolor><label>$LOCALIZE[31681]</label></control>']
    for rid, inner in rows:
        o.append('<!-- preview:%d -->' % rid)
        o.append('<control type="group"><visible>Control.HasFocus(%d)</visible>%s</control>' % (rid, inner))
    o.append('</control></control>')
    o.append(END % page)
    return '\n'.join(o)


def real_pictures(x, ctx='movies'):
    """0.56.20: the skin's stand-in picture becomes the card's real fanart (pic_vars)"""
    return x.replace('common/aeon_bg_default.png', pic(ctx))


def new_inner(cap, fn):
    CTX[0] = PIC_FOR.get(cap, 'movies')
    return real_pictures('<control type="label"><left>16</left><top>54</top><width>248</width><height>30</height><align>left</align>'
                         '<aligny>center</aligny><font>st_cap_20</font><textcolor>66ffffff</textcolor><label>%s</label></control>'
                         % esc(CAP[cap]) + '<control type="group">%s</control>' % fn(), CTX[0])


def main():
    t = io.open(P, encoding='utf-8').read()
    # a run before this one: take its containers out
    t = re.sub(r'\n?<!-- PREVIEW CARD (\w+) \(_src/skin_previews.py\) -->.*?<!-- /PREVIEW CARD \1 -->', '', t, flags=re.S)
    if os.path.exists(LEGACY):
        legacy = json.load(io.open(LEGACY, encoding='utf-8'))
        legacy = dict((k, [tuple(r) for r in v]) for k, v in legacy.items())
        assert not re.search(r'<control type="group">\s*<left>920</left>\s*<top>199</top>', t), 'old containers still in the window'
    else:
        legacy, t = take_legacy(t)
        io.open(LEGACY, 'w', encoding='utf-8', newline='\n').write(json.dumps(legacy, indent=1, ensure_ascii=False))
        print('legacy previews saved:', dict((k, len(v)) for k, v in legacy.items()))
    pages = sorted(set(legacy) | set(NEW))
    per_page = {}
    for page in pages:
        rows = [(r, real_pictures(fix_text(x))) for r, x in legacy.get(page, []) if r not in DROP]
        have = set(r for r, _ in rows)
        rows += [(r, new_inner(cap, fn)) for r, cap, fn in NEW.get(page, []) if r not in have]
        for r, x in rows:
            per_page.setdefault(MOVED.get(r, page), []).append((r, x))
    for page in sorted(per_page):
        rows = per_page.get(page, [])
        m = re.search(r'(<control type="group">\s*<left>600</left>\s*<animation[^\n]*?</animation>\s*<visible>String.IsEqual\(Window\(Home\).Property\(aeon.skincat\),%s\)</visible>)' % page, t)
        assert m, page
        t = t[:m.end()] + '\n' + container(page, rows) + t[m.end():]
        print(page, len(rows), 'previews')
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    # the cards' pictures (Includes_Settings.xml, a marked block: replaced on every run)
    inc = os.path.join('1080i', 'Includes_Settings.xml')
    s = io.open(inc, encoding='utf-8').read()
    s = re.sub(r'\n?' + re.escape(PIC_BEGIN) + r'.*?' + re.escape(PIC_END), '', s, flags=re.S)
    i = s.index('<includes>') + len('<includes>')
    s = s[:i] + '\n' + pic_vars() + s[i:]
    io.open(inc, 'w', encoding='utf-8', newline='\n').write(s)


if __name__ == '__main__':
    main()
