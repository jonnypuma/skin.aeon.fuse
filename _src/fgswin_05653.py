# -*- coding: utf-8 -*-
"""0.56.53 shared plumbing for the round-2 Fused Glass style windows (canvas F6xQV7p6NWvcxZxy5NR18C).
Each window keeps today's controls for every other theme / style: wrap() moves them once into <Name>_PageClassic and
loads <Name>_PageFGS when $EXP[FGS]. The FGS pages live in 1080i/Includes_FGSWin.xml between per-window markers
(put()), so every window generator stays repeatable on its own.
Also the pieces the pages share: the style's header, clock, 70 px action cells with the focus shadow, lines."""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SKIN = os.path.join(HERE, '..')
D = os.path.join(SKIN, '1080i')
FILE = os.path.join(D, 'Includes_FGSWin.xml')
LINE = '24ffffff'
SHADOW = '<texture border="56" colordiffuse="$VAR[FG_ShadowColM]">fg/sh16.png</texture>'
BAR = '<texture border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texture>'


def ensure_file():
    if not os.path.exists(FILE):
        io.open(FILE, 'w', encoding='utf-8', newline='\n').write(
            '<?xml version="1.0" encoding="UTF-8"?>\n<!-- 0.56.53 Fused Glass style pages of Kodi\'s standard windows (canvas round 2);\n'
            '     written by _src/fgs*_05653.py through _src/fgswin_05653.py. Today\'s pages: <Name>_PageClassic. -->\n<includes>\n</includes>\n')
    inc = os.path.join(D, 'Includes.xml')
    s = io.open(inc, encoding='utf-8').read()
    if 'Includes_FGSWin.xml' not in s:
        s = s.replace('\t<include file="Expressions.xml"/>', '\t<include file="Expressions.xml"/>\n\t<include file="Includes_FGSWin.xml"/>', 1)
        assert 'Includes_FGSWin.xml' in s
        io.open(inc, 'w', encoding='utf-8', newline='\n').write(s)


def wrap(window, name):
    """the window's <controls> -> <name>_PageClassic (once) + conditional includes"""
    ensure_file()
    p = os.path.join(D, window)
    w = io.open(p, encoding='utf-8').read()
    if '%s_PageClassic' % name in w:
        return
    a = w.index('<controls>') + len('<controls>')
    b = w.rindex('</controls>')
    classic = w[a:b]
    w = (w[:a] + '\n\t\t<include condition="!$EXP[FGS]">%s_PageClassic</include>\n\t\t<include condition="$EXP[FGS]">%s_PageFGS</include>\n\t' % (name, name) + w[b:])
    io.open(p, 'w', encoding='utf-8', newline='\n').write(w)
    s = io.open(FILE, encoding='utf-8').read()
    s = s.replace('</includes>', '\t<!-- today\'s %s controls, moved unchanged -->\n\t<include name="%s_PageClassic">%s</include>\n</includes>' % (window, name, classic))
    io.open(FILE, 'w', encoding='utf-8', newline='\n').write(s)


def put(name, xml):
    """the FGS page (and anything else) between this window's markers"""
    ensure_file()
    a, b = '<!-- %s fgs: begin -->' % name, '<!-- %s fgs: end -->' % name
    s = io.open(FILE, encoding='utf-8').read()
    if a in s:
        s = s[:s.index(a)] + s[s.index(b) + len(b):]
    s = s.replace('</includes>', '\t%s\n%s\n\t%s\n</includes>' % (a, xml, b))
    io.open(FILE, 'w', encoding='utf-8', newline='\n').write(s)


def header(lead, label):
    return ('<include content="FGS_DlgHeader"><param name="lead" value="%s"/><param name="leadvis" value="true"/><param name="label" value="%s"/></include>'
            '<include>Aeon_ClockBox</include>' % (lead, label))


def img(x, y, w, h, tex, diffuse='', vis='', extra=''):
    return ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>%s<texture%s>%s</texture>%s</control>'
            % (x, y, w, h, extra, (' colordiffuse="%s"' % diffuse) if diffuse else '', tex, ('<visible>%s</visible>' % vis) if vis else ''))


def line(x, y, w, h=1):
    return img(x, y, w, h, 'common/white.png', LINE)


def label(x, y, w, h, text, font='st_small_20', col='e6ffffff', align='left', vis='', extra=''):
    return ('<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><align>%s</align><aligny>center</aligny>'
            '<font>%s</font><textcolor>%s</textcolor><label>%s</label>%s%s</control>'
            % (x, y, w, h, align, font, col, text, extra, ('<visible>%s</visible>' % vis) if vis else ''))


def cell(cid, w, text, nav='', clicks=(), vis='true', h=70, font='uc_st_ui_22_bold', align='center'):
    """one action cell for a horizontal grouplist: shadow, button, the line at its right"""
    return ('<control type="group"><width>%d</width><height>%d</height><visible>%s</visible>'
            '<control type="image"><left>-40</left><top>-34</top><width>%d</width><height>%d</height>%s<visible>Control.HasFocus(%s) + $EXP[FGS_ShadowOn]</visible></control>'
            '<control type="button" id="%s"><left>0</left><top>0</top><width>%d</width><height>%d</height><font>%s</font><textcolor>ccffffff</textcolor>'
            '<focusedcolor>ffffffff</focusedcolor><disabledcolor>44ffffff</disabledcolor><align>%s</align><aligny>center</aligny><textoffsetx>24</textoffsetx>'
            '<label>%s</label><texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texturefocus><texturenofocus />%s%s<include>FGS_RowAnim</include></control>'
            '%s</control>'
            % (w, h, vis, w + 80, h + 80, SHADOW, cid, cid, w, h, font, align, ('[UPPERCASE]%s[/UPPERCASE]' % text) if font.startswith('st_cap') else text, nav, ''.join('<onclick>%s</onclick>' % c for c in clicks),
               img(w - 1, 0, 1, h, 'common/white.png', LINE)))


def gutter_bar(sid, x, y, h, onleft, onright='noop'):
    """the style's square scroll bar in a 20 px gutter (accent when focused)"""
    return ('<control type="scrollbar" id="%s"><left>%d</left><top>%d</top><width>19</width><height>%d</height>'
            '<texturesliderbackground colordiffuse="0dffffff">common/white.png</texturesliderbackground>'
            '<texturesliderbar colordiffuse="59ffffff">common/white.png</texturesliderbar>'
            '<texturesliderbarfocus colordiffuse="$VAR[Aeon_SBFocus]">common/white.png</texturesliderbarfocus>'
            '<orientation>vertical</orientation><showonepage>false</showonepage><onleft>%s</onleft><onright>%s</onright></control>'
            % (sid, x, y, h, onleft, onright))
