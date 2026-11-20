# -*- coding: utf-8 -*-
"""0.56.53 Fused Glass: the Home menu's submenu editor (dialog 1159) and widget editor (dialog 1158) in the Fused Glass
design (user, 2026-11-19: "these submenus have to be rebuilt for Fused Glass"; then, on the box: "No horizontal line
above Sets ... the items should be numbered. the lines above and below them shall connect to the vertical lines",
"highlight bar is not sitting flush with vertical lines", "what is choose type? We are under Movies - so that IS the
chosen type", "what is Add list... ? is it the same as + Add item???").

Each window's controls become includes picked when the window loads (theme and style are fixed while the skin runs):
- Ed<id>_Classic: the controls as they were (Aeon, Aeon Glass);
- Ed<id>_FGS (Fused Glass style) and Ed<id>_FG (Fused Glass, glass cards): the same controls laid out like Skin
  settings: backdrop, "Aeon Fuse  Submenu / Widgets" header, clock pill; the list in its own frame / card with a title
  band (the Home item, what the list is for) and a rule under it and above the first row; numbered rows whose rules
  and focus bar meet the frame's vertical lines (style) or sit 12 px inside the card (glass cards); the row you work on
  stays marked while the options have focus (the style's dimmed bar, as the selected category);
- the options in a frame / card of their own: the title band says "Selected item:" and the row in focus (it said
  "Item: Movies"); then the options, one after another. Gone: Choose type (it changed the Home item's type: an editor
  of Movies' submenu is not the place) and Add list... (the same action as + Add item, only placed after the row in
  focus). The widget editor's Widget screen options (9640, above the panel before) is the first option.
Repeatable (the controls are taken from Ed<id>_Classic once it exists)."""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import settings_sections as ss  # noqa: E402

D = os.path.join(HERE, '..', '1080i')
WINDOWS = {1159: ('Custom_1159_HomeSubmenu.xml', '$LOCALIZE[1034]'),
           1158: ('Custom_1158_HomeLists.xml', '$ADDON[skin.aeon.fuse 32025]')}
FRAME = 'FGS_FrameCol'
L, T, W, H = 120, 108, 1380, 852          # list frame / card
OL, OW = 1520, 300                        # options frame / card
BAND = 191                                # title band 108-191, as Skin settings
LIST_TOP = 276
GONE = ('9630', '9623')                   # Choose type, Add list...


def card(left, width):
    return ('<control type="group"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
            '<include content="Aeon_Glass"><param name="fgs" value="true"/></include></control>' % (left, T, width, H))


def rule(x, y, w, h=1):
    return ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
            '<texture colordiffuse="$VAR[%s]">common/white.png</texture></control>' % (x, y, w, h, FRAME))


def options(b, first_x, width, style):
    """the options group rebuilt: (group xml, id of the first option)"""
    m = ss.masked(b)
    g = b.index('<control type="group" id="9612">')
    e = ss.ctl_end(m, g)
    kids = ss.children(m, g, e)
    rows = []                                  # [(id, button xml, [label xml])]
    for a, c in kids:
        x = b[a:c]
        bid = re.match(r'<control type="button" id="(\d+)">', x)
        if bid:
            rows.append([bid.group(1), x, []])
        elif rows and x.startswith('<control type="label">'):
            rows[-1][2].append(x)
    extra = re.search(r'<control type="button" id="9640">.*?</control>', b, re.S)
    if extra:                                  # widget editor: Widget screen options becomes the first option
        labs = re.findall(r'<control type="label"><left>1464</left><top>130</top>.*?</control>', b, re.S)
        rows.insert(0, ['9640', extra.group(0), labs])
        for x in [extra.group(0)] + labs:
            b = b.replace(x, '', 1)
        m = ss.masked(b)
        g = b.index('<control type="group" id="9612">')
        e = ss.ctl_end(m, g)
    rows = [r for r in rows if r[0] not in GONE]
    ids = [r[0] for r in rows]
    if style:
        return grid_options(b, g, e, rows, ids, first_x, width), ids[0]
    pitch = min(54, (T + H - 8 - 200) // len(rows))
    out = []
    for k, (bid, btn, labs) in enumerate(rows):
        top = k * pitch
        btn = re.sub(r'<left>-?\d+</left><top>-?\d+</top><width>\d+</width><height>\d+</height>',
                     '<left>0</left><top>%d</top><width>%d</width><height>%d</height>' % (top, width, pitch - 2), btn, count=1)
        btn = re.sub(r'<onup>[^<]*</onup>', '', btn)
        btn = re.sub(r'<ondown[^>]*>[^<]*</ondown>', '', btn)
        btn = re.sub(r'<onleft>[^<]*</onleft>', '<onleft>9611</onleft>', btn)
        nav = '<onup>%s</onup><ondown>%s</ondown>' % (ids[k - 1], ids[(k + 1) % len(ids)])
        i = btn.index('<label></label>')
        btn = btn[:i] + nav + btn[i:]
        btn = btn.replace('<include>Aeon_TexRowFocus</include>', '<include>%s</include>' % ('FGS_BtnFocus' if style else 'Aeon_TexRowFocus'))
        out.append(btn)
        for lab in labs:
            lab = re.sub(r'<left>\d+</left>(\s*)<top>-?\d+</top>(\s*)<width>\d+</width>(\s*)<height>\d+</height>',
                         r'<left>24</left>\g<1><top>%d</top>\g<2><width>%d</width>\g<3><height>%d</height>' % (top, width - 40, pitch - 2), lab, count=1)
            out.append(lab)
    group = ('<control type="group" id="9612"><left>%d</left><top>200</top>%s</control>' % (first_x, ''.join(out)))
    return b[:g] + group + b[e:], ids[0]


PITCH = 70                                 # Fused Glass style: the Skin settings row grid (Categories)
SBAR = '9688'                              # the options' scroll bar (style)
LBAR = '9689'                              # the list's scroll bar (style)
GUT = 20                                   # the scroll bar gutter between two lines (style)


def grid_options(b, g, e, rows, ids, x, width):
    """Fused Glass style (user, 2026-11-19: "uniform heights on highlight bar in the same window, flush with it's
    neighbor cell(s)", "missing horizontal lines"): the options as rows of the Skin settings grid, 70 high from the
    title band's rule (191), each with the settings rows' line at its top, flush with the frame (x .. 1820); a
    grouplist that scrolls when they do not fit (the widget editor's 14), its scroll bar on the right line"""
    out = []
    for k, (bid, btn, labs) in enumerate(rows):
        btn = re.sub(r'<left>-?\d+</left><top>-?\d+</top><width>\d+</width><height>\d+</height>',
                     '<left>0</left><top>0</top><width>%d</width><height>%d</height>' % (width, PITCH), btn, count=1)
        btn = re.sub(r'<onup>[^<]*</onup>', '', btn)
        btn = re.sub(r'<ondown[^>]*>[^<]*</ondown>', '', btn)
        btn = re.sub(r'<onleft>[^<]*</onleft>', '<onleft>9611</onleft>', btn)
        nav = '<onup>%s</onup><ondown>%s</ondown>' % (ids[k - 1], ids[(k + 1) % len(ids)])
        i = btn.index('<label></label>')
        btn = btn[:i] + nav + btn[i:]
        btn = btn.replace('<include>Aeon_TexRowFocus</include>', '<include>FGS_BtnFocus</include>')
        line = ('<control type="image"><left>0</left><top>0</top><width>%d</width><height>1</height>'
                '<texture colordiffuse="12ffffff">common/white.png</texture><visible>!Control.HasFocus(%s)</visible></control>' % (width, bid))
        cell = [line, btn]
        for lab in labs:
            cell.append(re.sub(r'<left>\d+</left>(\s*)<top>-?\d+</top>(\s*)<width>\d+</width>(\s*)<height>\d+</height>',
                               r'<left>24</left>\g<1><top>0</top>\g<2><width>%d</width>\g<3><height>%d</height>' % (width - 40, PITCH), lab, count=1))
        out.append('<control type="group"><width>%d</width><height>%d</height>%s</control>' % (width, PITCH, ''.join(cell)))
    group = ('<control type="grouplist" id="9612"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
             '<orientation>vertical</orientation><itemgap>0</itemgap><usecontrolcoords>true</usecontrolcoords>'
             '<scrolltime tween="cubic" easing="out">200</scrolltime><pagecontrol>%s</pagecontrol>%s</control>'
             '<control type="scrollbar" id="%s"><left>%d</left><top>%d</top><width>19</width><height>%d</height>'
             '<include>FGS_SBTex</include>'
             '<textureslidernib /><textureslidernibfocus /><orientation>vertical</orientation><showonepage>false</showonepage>'
             '<onleft>9612</onleft></control>'
             % (x, BAND, width, T + H - BAND, SBAR, ''.join(out), SBAR, x + width + 1, BAND + 1, T + H - BAND - 1))
    return b[:g] + group + b[e:]


def grid_rows(b):
    """Fused Glass style: the list rows 70 high (were 84), the two lines moved up to fit"""
    for lay in ('itemlayout', 'focusedlayout'):
        i = b.index('<%s width' % lay)
        j = b.index('</%s>' % lay, i)
        seg = b[i:j].replace('height="84"', 'height="%d"' % PITCH).replace('<height>84</height>', '<height>%d</height>' % PITCH)
        seg = seg.replace('<top>83</top>', '<top>%d</top>' % (PITCH - 1)).replace('<height>164</height>', '<height>150</height>')
        seg = re.sub(r'<top>8</top>(<width>\d+</width>)<height>38</height>', r'<top>5</top>\1<height>34</height>', seg)
        seg = re.sub(r'<top>44</top>(<width>\d+</width>)<height>30</height>', r'<top>37</top>\1<height>26</height>', seg)
        b = b[:i] + seg + b[j:]
    return b


def fg(body, wid, head, style):
    """style: True = Fused Glass style (frame lines, bars flush with them), False = glass cards (12 px inside)"""
    inset = 1 if style else 12
    b = body
    title = re.search(r'<control type="label"><left>140</left><top>70</top>.*?<label>(.*?)</label></control>', b, re.S)
    desc = re.search(r'<control type="label"><left>140</left><top>126</top>.*?<label>(.*?)</label></control>', b, re.S)
    b = b.replace(title.group(0), '').replace(desc.group(0), '')
    b = re.sub(r'<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height>'
               r'<texture colordiffuse="\$VAR\[AG_Ground\]">common/white.png</texture></control>', '', b, count=1)
    for a, c in (('hm_ui_24_bold', 'st_ui_24_bold'), ('hm_ui_24_semibold', 'st_ui_24_semibold'),
                 ('hm_small_20_semibold', 'st_small_20_semibold'), ('hm_small_20', 'st_small_20')):
        b = b.replace('<font>%s</font>' % a, '<font>%s</font>' % c)
    if style:
        b = b.replace('$VAR[Aeon_MenuFocusTex]', '$VAR[FGS_Aeon_MenuFocusTex]').replace('$VAR[Aeon_OnBarInk]', '$VAR[FGS_Aeon_OnBarInk]')
    b = b.replace('colordiffuse="30ffffff">common/white.png', 'colordiffuse="$VAR[%s]">common/white.png' % FRAME)
    x, w = L + inset, W - inset - (0 if style else inset)
    ox, ow = OL + inset, OW - inset - (0 if style else inset)
    lt = BAND + PITCH if style else LIST_TOP           # style: Add item is one 70 row
    if style:                                          # style: the options share the list's right line (1500)
        ox, ow = L + W + GUT + 1, 1820 - GUT - (L + W + GUT) - 1   # 0.56.53 gutters: list | 1500-1520 | options | 1800-1820
    # + Add item and the list
    b = re.sub(r'(<control type="button" id="9650">\s*<left>)140(</left><top>)200(</top><width>)1240(</width><height>)60(</height>)',
               r'\g<1>%d\g<2>%d\g<3>%d\g<4>%d\g<5>' % (x, BAND + 1, w, lt - BAND - 2), b)
    b = b.replace('<include>Aeon_TexRowFocus</include><texturenofocus />\n\t\t\t<onup>noop</onup><ondown>9611</ondown>',
                  '<include>%s</include><texturenofocus />\n\t\t\t<onup>noop</onup><ondown>9611</ondown>' % ('FGS_BtnFocus' if style else 'Aeon_TexRowFocus'), 1)
    b = re.sub(r'(<control type="label"><left>)164(</left><top>)200(</top><width>\d+</width><height>)60(</height>)',
               r'\g<1>%d\g<2>%d\g<3>%d\g<4>' % (x + 24, BAND + 1, lt - BAND - 2), b)
    b = re.sub(r'(<control type="list" id="9611">\s*<left>)140(</left><top>)270(</top><width>)1240(</width><height>)740(</height>)',
               r'\g<1>%d\g<2>%d\g<3>%d\g<4>%d\g<5>' % (x, lt, w, T + H - lt), b)
    b = b.replace('<itemlayout width="1240"', '<itemlayout width="%d"' % w).replace('<focusedlayout width="1240"', '<focusedlayout width="%d"' % w)
    b = b.replace('<width>1240</width>', '<width>%d</width>' % w).replace('<width>1320</width>', '<width>%d</width>' % (w + 80))
    # numbers, labels after them
    num = ('<control type="label"><left>16</left><top>8</top><width>44</width><height>38</height><align>right</align><aligny>center</aligny>'
           '<font>st_ui_24_semibold</font><textcolor>%s</textcolor><label>$INFO[ListItem.CurrentItem]</label>%s</control>')
    for lay in ('itemlayout', 'focusedlayout'):
        i = b.index('<%s width' % lay)
        j = b.index('</%s>' % lay, i)
        seg = b[i:j].replace('<left>24</left>', '<left>80</left>')
        k = seg.index('>') + 1
        if lay == 'itemlayout':
            add = num % ('99ffffff', '')
        else:
            mark = ('<control type="image"><left>0</left><top>0</top><width>%d</width><height>84</height>'
                    '<texture border="%s" colordiffuse="%s">%s</texture><visible>!Control.HasFocus(9611)</visible></control>'
                    % (w, '20' if style else '16', '40ffffff' if style else '80ffffff', 'fg/fgs_bar.png' if style else 'fg/selrow16.png'))
            add = mark + num % ('ffffffff', '<visible>!Control.HasFocus(9611)</visible>') + num % (
                '$VAR[FGS_Aeon_OnBarInk]' if style else '$VAR[Aeon_OnBarInk]', '<visible>Control.HasFocus(9611)</visible>')
        b = b[:i] + seg[:k] + add + seg[k:] + b[j:]
    if style:
        b = grid_rows(b)
        b = b.replace('<control type="list" id="9611">', '<control type="list" id="9611"><pagecontrol>%s</pagecontrol>' % LBAR, 1)
        b += ('<control type="scrollbar" id="%s"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
              '<include>FGS_SBTex</include><textureslidernib /><textureslidernibfocus /><orientation>vertical</orientation>'
              '<showonepage>false</showonepage><onleft>9611</onleft><onright>9611</onright></control>'
              % (LBAR, L + W + 1, lt, GUT - 1, T + H - lt))
    b, first = options(b, ox, ow, style)
    b = re.sub(r'(<control type="list" id="9611">.*?<onright>)9630(</onright>)', r'\g<1>%s\g<2>' % first, b, count=1, flags=re.S)
    top = ('<control type="image"><width>1920</width><height>1080</height><texture colordiffuse="$VAR[AG_Ground]">common/white.png</texture></control>'
           '<control type="group"><visible>$EXP[Aeon_VGlass]</visible><include>Aeon_Backdrop</include></control>')
    if style:
        top += ''.join(rule(*r) for r in ((L, T, 1820 - L + 1), (L, T + H, 1820 - L + 1)))
        top += ''.join(rule(xx, T, 1, H) for xx in (L, L + W, L + W + GUT, 1820 - GUT, 1820))
        top += rule(L + W + 1, BAND, GUT - 1) + rule(1820 - GUT + 1, BAND, GUT - 1)
    else:
        top += card(L, W) + card(OL, OW)
    top += rule(x, BAND, w) + rule(ox, BAND, ow) + rule(x, lt - 1, w)
    top += ('<include content="Aeon_MenuHeader"><param name="lead" value="Aeon Fuse"/><param name="label" value="%s"/></include>'
            '<include>Aeon_ClockBox</include>' % head)
    top += ('<control type="label"><left>%d</left><top>116</top><width>%d</width><height>40</height><aligny>center</aligny>'
            '<font>st_ui_30_semibold</font><textcolor>$VAR[AG_Ink]</textcolor><label>[UPPERCASE]$VAR[Aeon_EditTitle][/UPPERCASE]</label></control>'
            '<control type="label"><left>%d</left><top>154</top><width>%d</width><height>30</height><aligny>center</aligny>'
            '<font>st_small_20</font><textcolor>99ffffff</textcolor><label>%s</label></control>' % (x + 24, w - 48, x + 24, w - 48, desc.group(1)))
    top += ('<control type="label"><left>%d</left><top>116</top><width>%d</width><height>30</height><aligny>center</aligny>'
            '<font>st_small_20</font><textcolor>66ffffff</textcolor><label>$LOCALIZE[31719]</label></control>'
            '<control type="label"><left>%d</left><top>146</top><width>%d</width><height>40</height><aligny>center</aligny>'
            '<font>st_ui_24_bold</font><textcolor>ffffffff</textcolor><label>$INFO[Container(9611).ListItem.Label]</label></control>'
            % (ox + 24, ow - 48, ox + 24, ow - 48))
    return '<!-- 0.56.53 fgeditors -->' + top + b


def put(t, name, content):
    if '<include name="%s">' % name in t:
        i = t.index('<include name="%s">' % name)
        j = t.index('<!-- end %s -->' % name, i) + len('<!-- end %s -->' % name)
        return t[:i] + '<include name="%s">%s</include>\n\t<!-- end %s -->' % (name, content, name) + t[j:]
    k = t.rindex('</includes>')
    return t[:k] + '\t<include name="%s">%s</include>\n\t<!-- end %s -->\n' % (name, content, name) + t[k:]


def main():
    inc = os.path.join(D, 'Includes_Fused.xml')
    t = io.open(inc, encoding='utf-8').read()
    for wid, (name, head) in WINDOWS.items():
        p = os.path.join(D, name)
        s = io.open(p, encoding='utf-8').read()
        a = s.index('<controls>') + len('<controls>')
        e = s.rindex('</controls>')
        cn = 'Ed%d_Classic' % wid
        if '<include name="%s">' % cn in t:
            i = t.index('<include name="%s">' % cn)
            body = t[i + len('<include name="%s">' % cn):t.index('</include>\n\t<!-- end %s -->' % cn, i)]
        else:
            body = s[a:e]
        t = put(t, cn, body)
        t = put(t, 'Ed%d_FGS' % wid, fg(body, wid, head, True))
        t = put(t, 'Ed%d_FG' % wid, fg(body, wid, head, False))
        s = (s[:a] + '\n\t\t<include condition="$EXP[Aeon_FGlass] + $EXP[FGS]">Ed%d_FGS</include>'
             '\n\t\t<include condition="$EXP[Aeon_FGlass] + !$EXP[FGS]">Ed%d_FG</include>'
             '\n\t\t<include condition="!$EXP[Aeon_FGlass]">%s</include>\n\t' % (wid, wid, cn) + s[e:])
        io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
        print('window %d: Fused Glass layouts written' % wid)
    io.open(inc, 'w', encoding='utf-8', newline='\n').write(t)


if __name__ == '__main__':
    main()
