# -*- coding: utf-8 -*-
"""0.56.53 round 5 of the Fused Glass style windows (canvas F6xQV7p6NWvcxZxy5NR18C, boards Login5, Keyboard5, Slider5,
Overlays5 - the ones the user left without a note; Guide controls / System menu: "don't build", View picker: "wait",
Bookmarks + Library panel: questions answered in chat).

- LoginScreen: profiles as round pictures, the focused one large with a white ring, its last login under it; Power / Exit /
  Restart as cells on a line at the foot. Kodi ids 52 (profiles) and 20 (power) kept.
- DialogKeyboard: the keys as cells on the frame line to line (13 per row as Kodi has them), a big input line, under it
  what you type already matches in the library (helper aeon.kb.h1-3, 0.3.120) and the recent searches (aeon.search.1-3,
  searchhist.py); OK on one types it into the field (RunScript(script.aeon.helper,kbset,h1|s1)). Id contract
  (GUIDialogKeyboardGeneric): 311 heading, 312 edit, 313/314 extra lines, keys 100-112 120-132 140-152 160-172,
  304 symbols, 303 caps, 302 shift, 32 space, 305/306 cursor, 8 delete, 300 done, 301 cancel, 309 layout, 310 reveal,
  307 IP address.
- DialogSlider: the offset card of the OSD panel alone at the top (bottom with aeon.offsetbar = bottom), a ruler, the value
  in the accent, a gold marker (ids 10 / 11 / 12).
- Notification / volume / busy / background progress as pills in the style's glass (ids 400-402; 29999; 10; 30-32).
Repeatable: wrap() moves today's controls once, put() rewrites the FGS pages; the keyboard window gets its own include."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fgswin_05653 as fw  # noqa: E402

PANEL = 'e6080a0c'
EDGE = '29ffffff'


def tex(t, border):
    return t.replace('<texture colordiffuse', '<texture border="%d" colordiffuse' % border)


def pill(x, y, w, h, r, fill=PANEL):
    return (tex(fw.img(x, y, w, h, 'fg/r%d.png' % r, fill), r) + tex(fw.img(x, y, w, h, 'fg/e%d.png' % r, EDGE), r))


# ---------------------------------------------------------------- login
def login_item(focused):
    s, x, y = (240, 30, 60) if focused else (150, 75, 105)
    out = ''
    if focused:
        out += fw.img(x - 11, y - 11, s + 22, s + 22, 'fg/circle.png', 'ffffffff', 'Control.HasFocus(52)')
        out += fw.img(x - 6, y - 6, s + 12, s + 12, 'fg/circle.png', 'ff0b0d11', 'Control.HasFocus(52)')
    out += fw.img(x, y, s, s, 'fg/circle.png', '33ffffff' if focused else '24ffffff')
    out += fw.img(x + s // 2 - s // 5, y + s // 2 - s // 5, s * 2 // 5, s * 2 // 5, 'common/aeon_mi_person.png', '99ffffff' if focused else '66ffffff')
    out += ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><aspectratio scalediffuse="false">scale</aspectratio>'
            '<texture background="true" diffuse="fg/circle.png"%s>$INFO[ListItem.Icon]</texture></control>' % (x, y, s, s, '' if focused else ' colordiffuse="b3ffffff"'))
    ny = y + s + 22
    out += fw.label(0, ny, 300, 40, '$INFO[ListItem.Label]', 'st_ui_28_bold' if focused else 'st_ui_22_semibold', 'ffffffff' if focused else 'b3ffffff', 'center')
    out += fw.label(0, ny + 42, 300, 30, '$INFO[ListItem.Label2]', 'st_small_20', '8cffffff', 'center')
    return out


def login_page():
    cells = (fw.cell('20', 200, '$LOCALIZE[31022]', '<onup>52</onup>', ('ActivateWindow(ShutdownMenu)',), font='st_cap_16')
             + fw.cell('9371', 200, '$LOCALIZE[13012]', '<onup>52</onup>', ('Quit',), font='st_cap_16')
             + fw.cell('9372', 200, '$LOCALIZE[13313]', '<onup>52</onup>', ('RestartApp',), font='st_cap_16'))
    return (
        '<include name="Login_PageFGS">'
        '<include>AG_Background</include>'
        + fw.img(0, 0, 1920, 1080, 'common/white.png', 'c70b0d11') +
        fw.header('$LOCALIZE[31000]', '$LOCALIZE[31286]') +
        '<control type="fixedlist" id="52"><left>-90</left><top>220</top><width>2100</width><height>520</height><orientation>horizontal</orientation>'
        '<focusposition>3</focusposition><movement>3</movement><onup>noop</onup><ondown>20</ondown><scrolltime tween="cubic" easing="out">300</scrolltime>'
        '<itemlayout width="300" height="520">%s</itemlayout><focusedlayout width="300" height="520">%s</focusedlayout></control>' % (login_item(False), login_item(True)) +
        fw.line(660, 899, 600) + fw.line(660, 970, 600) + fw.line(660, 900, 1, 70) +
        '<control type="grouplist" id="9370"><left>660</left><top>900</top><width>600</width><height>70</height><orientation>horizontal</orientation>'
        '<itemgap>0</itemgap><onleft>9372</onleft><onright>20</onright><onup>52</onup>%s</control>' % cells +
        '</include>')


# ---------------------------------------------------------------- keyboard
KX, KW = 120, 1700
ROWS = [331 + r * 105 for r in range(6)]
KH = 104


def key_rows():
    rows = []
    for base in (100, 120, 140, 160):
        rows.append([(str(base + i), 130 if i < 12 else 140) for i in range(13)])
    rows.append([('304', 220), ('303', 220), ('302', 220), ('32', 500), ('305', 140), ('306', 140), ('8', 260)])
    rows.append([('300', 425), ('301', 425), ('309', 425), ('307', 425)])
    out = []
    for r, row in enumerate(rows):
        x, cells = KX, []
        for cid, w in row:
            cells.append((cid, x, w))
            x += w
        out.append(cells)
    return out


def nearest(row, cx):
    return min(row, key=lambda c: abs(c[1] + c[2] / 2.0 - cx))[0]


def kb_page():
    rows = key_rows()
    has_sugg = '[!String.IsEmpty(Window(Home).Property(aeon.kb.h1.label)) | !String.IsEmpty(Window(Home).Property(aeon.search.1))]'
    keys = ''
    labels = {'304': '$LOCALIZE[31040]', '303': '$LOCALIZE[31041]', '302': '$LOCALIZE[31042]', '32': '$LOCALIZE[31043]', '305': '←', '306': '→',
              '8': '$LOCALIZE[31044]', '300': '$LOCALIZE[12321]', '301': '$LOCALIZE[222]', '307': '$LOCALIZE[1006]'}
    for r, row in enumerate(rows):
        for i, (cid, x, w) in enumerate(row):
            cx = x + w / 2.0
            up = nearest(rows[r - 1], cx) if r else None
            down = nearest(rows[r + 1], cx) if r < len(rows) - 1 else nearest(rows[0], cx)
            nav = '<onleft>%s</onleft><onright>%s</onright>' % (row[i - 1][0], row[(i + 1) % len(row)][0])
            if up:
                nav += '<onup>%s</onup>' % up
            else:
                nav += '<onup condition="%s">9361</onup><onup condition="!%s">%s</onup>' % (has_sugg, has_sugg, nearest(rows[-1], cx))
            nav += '<ondown>%s</ondown>' % down
            radio = cid in ('304', '303', '302')
            big = r < 4
            keys += ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>%s<visible>Control.HasFocus(%s) + $EXP[FGS_ShadowOn]</visible></control>'
                     % (x - 40, ROWS[r] - 34, w + 80, KH + 80, fw.SHADOW, cid))
            keys += ('<control type="%s" id="%s"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><font>%s</font>'
                     '<textcolor>%s</textcolor><focusedcolor>ffffffff</focusedcolor><disabledcolor>44ffffff</disabledcolor><align>center</align><aligny>center</aligny>'
                     '<textoffsetx>0</textoffsetx><pulseonselect>false</pulseonselect>%s'
                     '<texturefocus colordiffuse="66000000">common/white.png</texturefocus><texturenofocus />%s%s</control>'
                     % ('radiobutton' if radio else 'button', cid, x, ROWS[r], w, KH, 'st_ui_30_semibold' if big else 'st_small_20_bold',
                        'd9ffffff' if big else 'a6ffffff', ('<label>%s</label>' % (labels[cid] if big else '[UPPERCASE]%s[/UPPERCASE]' % labels[cid])) if cid in labels else '',
                        ('<radiowidth>16</radiowidth><radioheight>16</radioheight><radioposx>%d</radioposx><textureradioonfocus colordiffuse="fg_mark">fg/circle.png</textureradioonfocus>'
                         '<textureradioonnofocus colordiffuse="fg_mark">fg/circle.png</textureradioonnofocus><textureradioofffocus colordiffuse="33ffffff">fg/circle.png</textureradioofffocus>'
                         '<textureradiooffnofocus colordiffuse="33ffffff">fg/circle.png</textureradiooffnofocus>' % (w - 40)) if radio else '',
                        nav))
    rings = ''
    for r, row in enumerate(rows):
        for cid, x, w in row:
            rings += tex(fw.img(x, ROWS[r], w, KH, 'common/aeon_outline_sq.png', '99ffffff', 'Control.HasFocus(%s)' % cid), 8)
            rings += fw.img(x, ROWS[r] + KH - 5, w, 5, 'common/white.png', 'fg_mark', 'Control.HasFocus(%s)' % cid)
    grid = ''
    for r, row in enumerate(rows):
        grid += fw.line(121, ROWS[r] + KH, 1699)
        for cid, x, w in row[1:]:
            grid += fw.line(x, ROWS[r], 1, KH)
    # suggestions: library hits, then the recent searches
    sugg = ''
    for n in (1, 2, 3):
        p = 'Window(Home).Property(aeon.kb.h%d.%%s)' % n
        sugg += ('<control type="group"><width>380</width><height>84</height><visible>!String.IsEmpty(%s)</visible>'
                 '%s<control type="button" id="%d"><left>0</left><top>0</top><width>380</width><height>84</height><label></label>'
                 '<texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texturefocus><texturenofocus border="12" colordiffuse="0fffffff">fg/r12.png</texturenofocus>'
                 '<onclick>RunScript(script.aeon.helper,kbset,h%d)</onclick></control>'
                 '<control type="image"><left>10</left><top>10</top><width>43</width><height>64</height><aspectratio>scale</aspectratio><texture background="true">$INFO[%s]</texture></control>'
                 '%s%s</control>'
                 % (p % 'label', '', 9361 + n, n, p % 'art',
                    fw.label(66, 12, 300, 34, '$INFO[%s]' % (p % 'label'), 'st_ui_22_bold', 'ffffffff', extra='<scroll>false</scroll>'),
                    fw.label(66, 44, 300, 28, '$INFO[%s]' % (p % 'year'), 'st_small_20', '8cffffff')))
    sugg += ('<control type="group"><width>1</width><height>84</height>'
             '<visible>!String.IsEmpty(Window(Home).Property(aeon.kb.h1.label)) + !String.IsEmpty(Window(Home).Property(aeon.search.1))</visible>'
             + fw.img(0, 17, 1, 50, 'common/white.png', '26ffffff') + '</control>')
    for n in (1, 2, 3):
        sugg += ('<control type="button" id="%d"><width>auto</width><height>56</height><font>st_small_20_semibold</font><textcolor>bfffffff</textcolor><focusedcolor>ffffffff</focusedcolor>'
                 '<textoffsetx>24</textoffsetx><aligny>center</aligny><label>$INFO[Window(Home).Property(aeon.search.%d)]</label>'
                 '<texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texturefocus><texturenofocus border="28" colordiffuse="33ffffff">fg/e28.png</texturenofocus>'
                 '<onclick>RunScript(script.aeon.helper,kbset,s%d)</onclick><visible>!String.IsEmpty(Window(Home).Property(aeon.search.%d))</visible></control>'
                 % (9364 + n, n, n, n))
    hidden = ''.join('<control type="label" id="%s"><left>-3000</left><top>0</top><width>600</width><height>30</height><font>st_small_20</font></control>' % i for i in ('311',))
    return (
        '<include name="Kb_FGS"><control type="group"><visible>!Window.IsVisible(numericinput)</visible>'
        + fw.img(0, 0, 1920, 1080, 'common/white.png', 'ff0b0d11') +
        fw.img(0, 0, 1920, 1080, 'common/aeon_fade_left.png', '661c2230') +
        hidden +
        '<control type="grouplist"><left>60</left><top>44</top><width>1500</width><height>48</height><orientation>horizontal</orientation><itemgap>14</itemgap><usecontrolcoords>true</usecontrolcoords>'
        '<control type="label"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28_bold</font><textcolor>ffffffff</textcolor><label>[UPPERCASE]$INFO[Control.GetLabel(311)][/UPPERCASE]</label></control>'
        '</control><include>Aeon_ClockBox</include>'
        + fw.line(120, 108, 1701) + fw.line(120, 960, 1701) + fw.line(120, 108, 1, 852) + fw.line(1820, 108, 1, 852) +
        fw.line(121, 219, 1699) + fw.line(121, 330, 1699) +
        # the input line
        fw.img(150, 146, 36, 36, 'icons/af3/magnifying-glass.png', '99ffffff') +
        '<control type="edit" id="312"><left>210</left><top>116</top><width>1000</width><height>96</height><font>st_display_52</font><textcolor>ffffffff</textcolor>'
        '<align>left</align><aligny>center</aligny><textoffsetx>0</textoffsetx><texturefocus /><texturenofocus /></control>'
        + fw.label(1220, 109, 380, 110, '$INFO[Window(Home).Property(aeon.kb.found)]  [COLOR 80ffffff]$ADDON[skin.aeon.fuse 32802][/COLOR]', 'st_small_20_semibold', 'ffffffff', 'right',
                   '!String.IsEmpty(Window(Home).Property(aeon.kb.found)) + String.IsEmpty(Control.GetLabel(313))') +
        '<control type="label" id="313"><left>1220</left><top>124</top><width>380</width><height>36</height><align>right</align><aligny>center</aligny><font>st_small_20</font><textcolor>8cffffff</textcolor></control>'
        '<control type="label" id="314"><left>1220</left><top>164</top><width>380</width><height>36</height><align>right</align><aligny>center</aligny><font>st_small_20</font><textcolor>8cffffff</textcolor></control>'
        '<control type="button" id="310"><left>1620</left><top>109</top><width>200</width><height>110</height><font>st_cap_16</font><textcolor>b3ffffff</textcolor><focusedcolor>ffffffff</focusedcolor>'
        '<align>center</align><aligny>center</aligny><texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texturefocus><texturenofocus />'
        '<onup>noop</onup><ondown>100</ondown><onleft>noop</onleft><onright>noop</onright></control>'
        + fw.img(1620, 109, 1, 110, 'common/white.png', fw.LINE, 'Control.IsVisible(310)') +
        # what you meant: the library first, then the recent searches (from the frame, as the board)
        '<control type="grouplist" id="9361"><left>146</left><top>233</top><width>1654</width><height>84</height><orientation>horizontal</orientation><itemgap>14</itemgap>'
        '<align>left</align><onup>310</onup><ondown>100</ondown><onleft>noop</onleft><onright>noop</onright>%s</control>' % sugg +
        grid + keys + rings +
        '</control></include>')


def keyboard():
    fw.put('Kb', kb_page())
    p = os.path.join(fw.D, 'DialogKeyboard.xml')
    w = io.open(p, encoding='utf-8').read()
    if 'Kb_FGS' not in w:
        w = w.replace('<include condition="!$EXP[Aeon_MS]">Kb_Classic</include>',
                      '<include condition="!$EXP[Aeon_MS] + !$EXP[FGS]">Kb_Classic</include>\n\t\t<include condition="$EXP[FGS]">Kb_FGS</include>', 1)
        assert 'Kb_FGS' in w
        io.open(p, 'w', encoding='utf-8', newline='\n').write(w)


# ---------------------------------------------------------------- slider
def slider_page():
    ticks = ''
    for i in range(41):
        big, mid = i % 10 == 0, i % 5 == 0
        h = 36 if big else (22 if mid else 12)
        ticks += fw.img(520 + i * 22, 181 - h // 2, 2, h, 'common/white.png', 'bfffffff' if big else ('73ffffff' if mid else '38ffffff'))
    return (
        '<include name="Slider_PageFGS"><control type="group">'
        '<include>Anim_TopStrip</include><animation effect="slide" end="0,760" time="0" condition="$EXP[OSD_OffsetBarBottom]">Conditional</animation>'
        + tex(fw.img(440, 20, 1040, 280, 'fg/sh16.png', '$VAR[FG_ShadowColM]'), 56) +
        pill(480, 60, 960, 200, 24, 'eb080a0c') +
        '<control type="label" id="10"><left>-3000</left><top>0</top><width>600</width><height>30</height><font>st_small_20</font></control>'
        '<control type="label" id="12"><left>-3000</left><top>0</top><width>300</width><height>30</height><font>st_small_20</font></control>'
        + fw.label(520, 78, 560, 56, '[UPPERCASE]$INFO[Control.GetLabel(10)][/UPPERCASE]', 'st_ui_24_bold', 'ffffffff') +
        fw.label(1060, 72, 340, 64, '$INFO[Control.GetLabel(12)]', 'st_display_40', 'fg_mark', 'right') +
        fw.img(520, 180, 880, 2, 'common/white.png', '4dffffff') + ticks +
        fw.img(959, 146, 3, 70, 'common/white.png', 'ffffffff', 'String.Contains(Control.GetLabel(10),offset) | String.Contains(Control.GetLabel(10),delay)') +
        '<control type="slider" id="11"><left>516</left><top>140</top><width>888</width><height>82</height>'
        '<texturesliderbar colordiffuse="00ffffff">fg/fgs_offmark.png</texturesliderbar>'
        '<textureslidernib colordiffuse="fg_mark">fg/fgs_offmark.png</textureslidernib><textureslidernibfocus colordiffuse="fg_mark">fg/fgs_offmark.png</textureslidernibfocus>'
        '<onup>11</onup><ondown>11</ondown><onleft>11</onleft><onright>11</onright></control>'
        '</control></include>')


# ---------------------------------------------------------------- overlays
OPEN = ('<animation type="WindowOpen" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="slide" start="%s" end="0,0" time="250" tween="cubic" easing="out"/>'
        '<effect type="fade" start="0" end="100" time="200"/></animation>'
        '<animation type="WindowClose" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="slide" start="0,0" end="%s" time="180" tween="cubic" easing="in"/>'
        '<effect type="fade" start="100" end="0" time="160"/></animation>'
        '<animation type="WindowOpen" condition="Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" time="150"/></animation>'
        '<animation type="WindowClose" condition="Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="100" end="0" time="150"/></animation>')


def notif_page():
    return (
        '<include name="Notif_PageFGS"><control type="group">' + OPEN % ('120,0', '120,0') +
        tex(fw.img(1210, 0, 652, 176, 'fg/sh16.png', '$VAR[FG_ShadowColM]'), 56) +
        pill(1250, 40, 572, 96, 48) +
        fw.img(1266, 56, 64, 64, 'fg/circle.png', '1fffffff') +
        '<control type="image" id="400"><left>1274</left><top>64</top><width>48</width><height>48</height><aspectratio scalediffuse="false">scale</aspectratio><texture diffuse="fg/circle.png"/></control>'
        '<control type="label" id="401"><left>-3000</left><top>0</top><width>400</width><height>22</height><font>st_small_20</font></control>'
        '<control type="label" id="402"><left>-3000</left><top>0</top><width>400</width><height>22</height><font>st_small_20</font></control>'
        '<control type="fadelabel"><left>1346</left><top>50</top><width>440</width><height>38</height><font>st_ui_22_bold</font><textcolor>ffffffff</textcolor>'
        '<label>$INFO[Control.GetLabel(401)]</label><scrollout>false</scrollout><pauseatend>2000</pauseatend></control>'
        '<control type="fadelabel"><left>1346</left><top>86</top><width>440</width><height>34</height><font>st_small_20</font><textcolor>a6ffffff</textcolor>'
        '<label>$INFO[Control.GetLabel(402)]</label><scrollout>false</scrollout><pauseatend>2000</pauseatend></control>'
        '</control></include>')


def vol_page():
    fills = ''
    for v in range(5, 101, 5):
        h = max(48, int(round(404 * v / 100.0)))
        cond = 'Integer.IsGreaterOrEqual(Control.GetLabel(29999),%d)' % v + ('' if v == 100 else ' + !Integer.IsGreaterOrEqual(Control.GetLabel(29999),%d)' % (v + 5))
        fills += tex(fw.img(1764, 712 - h, 48, h, 'fg/r24.png', 'ffffffff', '!Player.Muted + ' + cond), 24)
    return (
        '<include name="Vol_PageFGS"><control type="group"><visible>!Window.IsActive(startup) + !Window.IsActive(GameVolume)</visible>' + OPEN % ('100,0', '100,0') +
        '<control type="progress" id="29999"><left>-3000</left><top>-3000</top><width>1</width><height>1</height><info>Player.Volume</info></control>'
        + tex(fw.img(1716, 260, 144, 500, 'fg/sh16.png', '$VAR[FG_ShadowColM]'), 56) +
        pill(1756, 300, 64, 420, 32) + fills +
        fw.label(1520, 480, 220, 60, '$INFO[Control.GetLabel(29999)]', 'st_display_40', 'ffffffff', 'right', '!Player.Muted', '<shadowcolor>a0000000</shadowcolor>') +
        fw.label(1440, 480, 300, 60, '[UPPERCASE]$LOCALIZE[31015][/UPPERCASE]', 'st_ui_24_bold', 'fg_mark', 'right', 'Player.Muted', '<shadowcolor>a0000000</shadowcolor>') +
        fw.img(1770, 736, 36, 36, 'icons/af3/volume-high.png', 'e6ffffff', '!Player.Muted') +
        fw.img(1770, 736, 36, 36, 'icons/af3/volume-xmark.png', 'fg_mark', 'Player.Muted') +
        '</control></include>')


def busy_page():
    return (
        '<include name="Busy_PageFGS"><control type="group"><visible>!Window.IsActive(startup) + !Player.Caching</visible>'
        '<animation type="WindowOpen"><effect type="fade" start="0" end="100" time="150"/></animation>'
        '<animation type="WindowClose"><effect type="fade" start="100" end="0" time="150"/></animation>'
        + fw.img(900, 420, 120, 120, 'fg/circle.png', 'bf080a0c') +
        fw.img(920, 440, 80, 80, 'common/aeon_spinner_ring.png', '2effffff') +
        fw.img(920, 440, 80, 80, 'common/aeon_spinner.gif', 'fg_mark', '!Skin.HasSetting(aeon.reducemotion)') +
        fw.img(920, 440, 80, 80, 'common/aeon_spinner_still.png', 'fg_mark', 'Skin.HasSetting(aeon.reducemotion)') +
        fw.label(860, 550, 200, 36, '$INFO[Control.GetLabel(10),,%]', 'st_ui_22_bold', 'ffffffff', 'center', extra='<shadowcolor>a0000000</shadowcolor>') +
        '<control type="label" id="10"><visible>false</visible></control>'
        '</control></include>')


def extprog_page():
    """the toast capsule beside the clock as today (same place, same moves: under a notification, docked in library
    windows), in the round-5 glass: spinner well, heading over the line, the percentage in the accent, a gold bar inside"""
    slides = ('<animation effect="slide" end="232,-16" time="0" condition="!$EXP[Aeon_HomeAny] + $EXP[FG_RailClock]">Conditional</animation>'
              '<animation effect="slide" end="248,0" time="0" condition="$EXP[FG_NoClock]">Conditional</animation>'
              '<animation effect="slide" end="92,0" time="0" condition="$EXP[FG_ClockNarrow]">Conditional</animation>'
              '<animation effect="slide" end="0,72" time="150" tween="cubic" easing="out" condition="Window.IsVisible(notification)">Conditional</animation>')
    return (
        '<include name="ExtProg_PageFGS"><control type="group"><left>1180</left><top>0</top>' + OPEN % ('120,0', '120,0') + slides +
        pill(-180, 40, 576, 64, 32) +
        fw.img(-168, 52, 40, 40, 'fg/circle.png', '1fffffff') +
        fw.img(-162, 58, 28, 28, 'common/aeon_spinner.gif', 'fg_mark', '!Skin.HasSetting(aeon.reducemotion)') +
        fw.img(-162, 58, 28, 28, 'common/aeon_spinner_still.png', 'fg_mark', 'Skin.HasSetting(aeon.reducemotion)') +
        '<control type="label" id="30"><left>-3000</left><top>0</top><width>400</width><height>20</height><font>st_small_20</font></control>'
        '<control type="label" id="31"><left>-3000</left><top>0</top><width>400</width><height>20</height><font>st_small_20</font></control>'
        + fw.label(-112, 44, 340, 26, '$INFO[Control.GetLabel(30)]', 'st_small_20_bold', 'ffffffff') +
        fw.label(232, 40, 140, 64, '$INFO[Control.GetLabel(32),,%]', 'st_ui_22_bold', 'fg_mark', 'right') +
        '<control type="fadelabel"><left>-112</left><top>68</top><width>340</width><height>26</height><font>st_small_20</font><textcolor>a6ffffff</textcolor>'
        '<label>$INFO[Control.GetLabel(31)]</label><scrollout>false</scrollout><pauseatend>2000</pauseatend></control>'
        '<control type="progress" id="32"><left>-120</left><top>94</top><width>456</width><height>4</height>'
        '<texturebg border="2" colordiffuse="1fffffff">fg/pill4.png</texturebg><lefttexture /><midtexture border="2" colordiffuse="fg_mark">fg/pill4.png</midtexture><righttexture /></control>'
        '</control></include>')


def main():
    for window, name, page in (('LoginScreen.xml', 'Login', login_page), ('DialogSlider.xml', 'Slider', slider_page),
                               ('DialogNotification.xml', 'Notif', notif_page), ('DialogVolumeBar.xml', 'Vol', vol_page),
                               ('DialogBusy.xml', 'Busy', busy_page), ('DialogExtendedProgressBar.xml', 'ExtProg', extprog_page)):
        fw.wrap(window, name)
        fw.put(name, page())
    keyboard()
    print('fgs round 5: login, keyboard, slider, notification, volume, busy, progress written')


if __name__ == '__main__':
    main()
