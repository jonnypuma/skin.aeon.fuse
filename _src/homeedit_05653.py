# -*- coding: utf-8 -*-
"""0.56.53 Skin settings > Home menu (and Context menu) in Fused Glass (user, 2026-11-19, box):
1. "the font color in the Selected item when in focus is white, same as focus highlight bar": the editor buttons drew
   the plain white bar (Aeon_TexRowFocus) while their focused labels use FGS_Aeon_OnBarInk, white in Fused Glass
   style. In that style they now draw the style's own grey glass bar (FGS_BtnFocus, fg/fgs_bar.png, as the rows);
   the other styles keep theirs. audit_focus.py (memory) flags this case since.
2. "the scrollbar is misaligned and showing inside the selected item box": the rows' bars ran to the list card's edge
   (1500) and the bar 9642 sat at 1520, in the Selected item column. The rows are 995 wide (were 1019) and, in Fused
   Glass, the bar moves 30 left to 1490: in the gap at the card's right edge, clear of the rows.
3. "missing a delete button for custom items (presets cannot be deleted so the delete button should be unavailable
   for those)": Delete (9687, Kodi's string 117) as the last button. Custom items: RunScript(...swap.py,delete,<pos>)
   asks, clears the item and moves the ones below up. Presets: shown dimmed with "Custom items only" (32796).
Repeatable."""
import io
import os
import re

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
P = os.path.join(D, 'SkinSettings.xml')
SUB = os.path.join(D, 'Includes_Aeon_Sub.xml')
FUSED = os.path.join(D, 'Includes_Fused.xml')
BTNS = ['9676', '9677', '9678', '9662', '9671', '9660', '9661', '9663', '9679', '9668', '9669', '9670', '9680', '9681',
        '9682', '9683', '9684', '9685', '9686', '9664', '9666', '9667', '9665']
FOCUS = '<include condition="$EXP[FGS]">FGS_BtnFocus</include><include condition="!$EXP[FGS]">Aeon_TexRowFocus</include>'
ANY = 'Aeon_EditIsCustomAny'


def focus(s):
    n = 0
    for b in BTNS:
        i = s.index('<control type="button" id="%s">' % b)
        e = s.index('</control>', i)
        x = s[i:e]
        if '<include>Aeon_TexRowFocus</include>' in x:
            s = s[:i] + x.replace('<include>Aeon_TexRowFocus</include>', FOCUS, 1) + s[e:]
            n += 1
    return s, n


def rows(s):
    i = s.index('<control type="grouplist" id="9641">')
    e = s.index('<control type="scrollbar" id="9642">', i)
    seg = s[i:e]
    k = 0
    if 'FGS_W1019' not in seg:                         # only before step 7 (it widens the rows again in the style)
        k = seg.count('<width>1019</width>')
        seg = seg.replace('<width>1019</width>', '<width>995</width>')
    s = s[:i] + seg + s[e:]
    j = s.index('<control type="scrollbar" id="9642">')
    end = s.index('</control>', j)
    bar = s[j:end]
    if 'end="-30,0"' not in bar:
        bar = bar.replace('<orientation>vertical</orientation>',
                          '<animation effect="slide" end="-30,0" time="0" condition="$EXP[Aeon_FGlass]">Conditional</animation><orientation>vertical</orientation>', 1)
        s = s[:j] + bar + s[end:]
    return s, k


def delete_button(s):
    if 'id="9687"' in s:
        return s, 'delete: already there'
    # Restore default order: Down goes to Delete while a custom item is chosen; the first button's Up comes back to it
    i = s.index('<control type="button" id="9665">')
    e = s.index('</control>', i)
    x = s[i:e].replace('<ondown>9662</ondown>', '<ondown condition="$EXP[%s]">9687</ondown><ondown>9662</ondown>' % ANY, 1)
    s = s[:i] + x + s[e:]
    i = s.index('<control type="button" id="9662">')
    e = s.index('</control>', i)
    x = s[i:e].replace('<onup>9665</onup>', '<onup condition="$EXP[%s]">9687</onup><onup>9665</onup>' % ANY, 1)
    s = s[:i] + x + s[e:]
    # the new group after Restore default order's group
    i = s.index('<control type="button" id="9665">')
    g = s.rfind('<control type="group">', 0, i)
    depth, k = 0, g
    for mm in re.finditer(r'<control[ >]|</control>', s[g:]):
        depth += 1 if mm.group(0) != '</control>' else -1
        if depth == 0:
            k = g + mm.end()
            break
    on = '$EXP[%s]' % ANY
    lab = ('<control type="label"><left>24</left><top>%s</top><width>228</width><height>%s</height><aligny>center</aligny>'
           '<font>%s</font><textcolor>%s</textcolor><label>%s</label><visible>%s</visible></control>')
    new = ('\n\t\t\t\t\t\t<!-- 0.56.53 Delete: custom items only; presets see it dimmed, with why -->'
           '\n\t\t\t\t\t\t<control type="group"><width>256</width><height>60</height>'
           '<control type="button" id="9687"><left>0</left><top>0</top><width>256</width><height>60</height><label></label>'
           + FOCUS + '<texturenofocus />'
           '<onup>9665</onup><ondown>9662</ondown><onright>noop</onright><onleft>9558</onleft>'
           '<onclick>RunScript(special://home/addons/script.aeon.helper/swap.py,delete,$INFO[Window(Home).Property(aeon.editslot)])</onclick>'
           '<enable>%s</enable></control>' % on
           + lab % (0, 60, 'st_ui_22_semibold', 'ccffffff', '$LOCALIZE[117]', '!Control.HasFocus(9687) + %s' % on)
           + lab % (0, 60, 'st_ui_22_semibold', '$VAR[FGS_Aeon_OnBarInk]', '$LOCALIZE[117]', 'Control.HasFocus(9687)')
           + lab % (2, 34, 'st_ui_22_semibold', '44ffffff', '$LOCALIZE[117]', '!%s' % on)
           + lab % (32, 22, 'st_cap_14', '44ffffff', '[UPPERCASE]$ADDON[skin.aeon.fuse 32796][/UPPERCASE]', '!%s' % on)
           + '</control>')
    s = s[:k] + new + s[k:]
    return s, 'delete: button 9687 added'


def selrow(s):
    """5. "the unfocused highlight on the home menu has a Fuse style non-focus bar": in Fused Glass style the row you
    work on (focus on its buttons) is marked as the selected category is, the style's grey bar dimmed (fg/fgs_bar.png
    at 40); the glass cards keep fg/selrow16.png"""
    old = '<texture border="16" colordiffuse="80ffffff">fg/selrow16.png</texture>'
    n = 0
    out = []
    pos = 0
    for m in re.finditer(r'<control type="image"><left>41</left><top>0</top><width>(\d+)</width><height>54</height>' + re.escape(old) +
                         r'<visible>(.*?) \+ \$EXP\[Aeon_FGlass\]</visible></control>', s):
        w, cond = m.group(1), m.group(2)
        new = ('<control type="image"><left>41</left><top>0</top><width>%s</width><height>54</height>%s'
               '<visible>%s + $EXP[Aeon_FGlass] + !$EXP[FGS]</visible></control>'
               '<control type="image"><left>41</left><top>0</top><width>%s</width><height>54</height>'
               '<texture border="20" colordiffuse="40ffffff">fg/fgs_bar.png</texture><visible>%s + $EXP[FGS]</visible></control>'
               % (w, old, cond, w, cond))
        out.append(s[pos:m.start()] + new)
        pos = m.end()
        n += 1
    return ''.join(out) + s[pos:], n


def scrollstop(s):
    """6. "Right from the Home menu list should land on the scroll bar before the options" (user, 2026-11-19): every
    row's Right goes to the bar 9642 while it shows (more rows than fit), else straight to the options as before. On the
    bar Up/Down scroll, Left goes back to the row you came from, Right on to the options; focused it turns the accent."""
    if '<!-- 0.56.53 scroll stop -->' in s:
        return s, 0
    i = s.index('<control type="grouplist" id="9641">')
    e = s.index('<control type="scrollbar" id="9642">', i)
    seg = s[i:e]
    k = seg.count('<onright>SetFocus(9662)</onright>')
    seg = seg.replace('<onright>SetFocus(9662)</onright>',
                      '<onright condition="Control.IsVisible(9642)">9642</onright>'
                      '<onright condition="!Control.IsVisible(9642)">SetFocus(9662)</onright>')
    s = s[:i] + seg + s[e:]
    j = s.index('<control type="scrollbar" id="9642">')
    end = s.index('</control>', j)
    bar = s[j:end]
    bar = bar.replace('<texturesliderbarfocus border="2" colordiffuse="99ffffff">',
                      '<texturesliderbarfocus border="2" colordiffuse="fg_mark">', 1)
    bar = bar.replace('<showonepage>false</showonepage>',
                      '<showonepage>false</showonepage><!-- 0.56.53 scroll stop -->'
                      '<onleft>SetFocus($INFO[Window(Home).Property(aeon.editrow)])</onleft>'
                      '<onright>SetFocus(9662)</onright><onback>9558</onback>', 1)
    return s[:j] + bar + s[end:], k


def column(s, cat):
    """the options column group of a page (ctxmenu / homemenu): (start, end)"""
    k = s.index('<left>1536</left><top>168</top>\n\t\t\t<visible>String.IsEqual(Window(Home).Property(aeon.skincat),%s)' % cat)
    g = s.rfind('<control type="group">', 0, k)
    depth = 0
    for mm in re.finditer(r'<control[ >]|</control>', s[g:]):
        depth += 1 if mm.group(0) != '</control>' else -1
        if depth == 0:
            return g, g + mm.end()


W = '<include condition="$EXP[FGS]">FGS_W%d</include><include condition="!$EXP[FGS]">FGS_W%d_Else</include>'


def flush(s):
    """7. "the highlight bar is again not flush with the vertical lines on either side" (user, 2026-11-19, Fused Glass
    style): the option buttons drew 1536-1792 in a column whose lines are 1500 and 1820, and the rows' marker stopped at
    1476 (995 wide for the scroll bar). In Fused Glass style the option columns (Home menu, Context menu) move 35 left
    (text 24 px in from the line) and the buttons are 319 wide, 1501-1820; the Home menu rows are 1019 wide (481-1500) as
    on every other settings page and the scroll bar sits where theirs does (-24, on the line). Other looks unchanged."""
    if 'FGS_W319' in s:
        return s, 0
    n = 0
    for cat in ('ctxmenu', 'homemenu'):
        g, e = column(s, cat)
        seg = s[g:e]
        n += seg.count('<width>256</width><height>60</height><label></label>')
        seg = seg.replace('<width>256</width><height>60</height><label></label>',
                          W % (319, 256) + '<height>60</height><label></label>')
        vis = '<visible>String.IsEqual(Window(Home).Property(aeon.skincat),%s)</visible>' % cat
        seg = seg.replace(vis, vis + '<animation effect="slide" end="-35,0" time="0" condition="$EXP[FGS]">Conditional</animation>', 1)
        s = s[:g] + seg + s[e:]
    i = s.index('<control type="grouplist" id="9641">')
    e = s.index('<control type="scrollbar" id="9642">', i)
    seg = s[i:e]
    n += seg.count('<width>995</width>')
    seg = seg.replace('<width>995</width>', W % (1019, 995))
    s = s[:i] + seg + s[e:]
    j = s.index('<control type="scrollbar" id="9642">')
    end = s.index('</control>', j)
    bar = s[j:end].replace('<animation effect="slide" end="-30,0" time="0" condition="$EXP[Aeon_FGlass]">',
                           '<animation effect="slide" end="-24,0" time="0" condition="$EXP[FGS]">Conditional</animation>'
                           '<animation effect="slide" end="-30,0" time="0" condition="$EXP[Aeon_FGlass] + !$EXP[FGS]">', 1)
    return s[:j] + bar + s[end:], n


HT = {}


def cond(tag, fgs, other):
    """a <tag> that is fgs in Fused Glass style and other elsewhere (two includes, written to Includes_Fused.xml)"""
    a, b = 'FGS_%s%s' % (tag[0].upper(), fgs), 'FGS_%s%s_Else' % (tag[0].upper(), other)
    HT[a] = '<%s>%s</%s>' % (tag, fgs, tag)
    HT[b] = '<%s>%s</%s>' % (tag, other, tag)
    return '<include condition="$EXP[FGS]">%s</include><include condition="!$EXP[FGS]">%s</include>' % (a, b)


def heights(s):
    """8. "the focus bar does not have the same height as the Categories options on the left ... Shall have uniform
    heights on highlight bar in the same window, flush with it's neighbor cell(s)" (user, 2026-11-19): in Fused Glass
    style the Home menu rows (54) and the option buttons of Home menu / Context menu (60) are 70 high, the Categories'
    height, and the option buttons start on the Categories' grid (261 = 191 + 70); the options' scroll bar 9643 sits on
    the frame's right line. Other looks unchanged."""
    if '<!-- 0.56.53 grid 70 -->' in s:
        return s, 0
    n = 0
    i = s.index('<control type="grouplist" id="9641">')
    e = s.index('<control type="scrollbar" id="9642">', i)
    seg = s[i:e]
    for old, new in (('<height>54</height>', cond('height', 70, 54)), ('<top>53</top>', cond('top', 69, 53)),
                     ('<height>134</height>', cond('height', 150, 134)),
                     ('<top>3</top><width>', None)):
        if new is None:
            continue
        n += seg.count(old)
        seg = seg.replace(old, new)
    seg = re.sub(r'<top>3</top>(.{0,80}?)<height>48</height>', lambda m: cond('top', 11, 3) + m.group(1) + '<height>48</height>', seg)
    seg = seg.replace('<height>702</height>', cond('height', 700, 702), 1)
    s = s[:i] + seg + '<!-- 0.56.53 grid 70 -->' + s[e:]
    for cat, shift in (('ctxmenu', -73), ('homemenu', -33)):
        g, e = column(s, cat)
        seg = s[g:e]
        n += seg.count('<height>60</height>')
        seg = seg.replace('<height>60</height>', cond('height', 70, 60))
        seg = seg.replace('<top>60</top>', cond('top', 70, 60)).replace('<top>120</top>', cond('top', 140, 120))
        seg = seg.replace('<top>2</top><width>228</width><height>34</height>', cond('top', 7, 2) + '<width>228</width><height>34</height>')
        seg = seg.replace('<top>32</top><width>228</width><height>22</height>', cond('top', 37, 32) + '<width>228</width><height>22</height>')
        anim = '<animation effect="slide" end="0,%d" time="0" condition="$EXP[FGS]">Conditional</animation>' % shift
        seg = seg.replace('<control type="group"><top>96</top>', '<control type="group"><top>96</top>' + anim, 1)
        bar = '<left>268</left><top>96</top><width>4</width><height>600</height>'
        if bar in seg:
            seg = seg.replace(bar, bar + '<animation effect="slide" end="47,%d" time="0" condition="$EXP[FGS]">Conditional</animation>' % shift, 1)
        s = s[:g] + seg + s[e:]
    return s, n


def grid191(s):
    """8b. with 70 px buttons the eleventh (Delete, dimmed for presets with its reason) fell below the panel and a
    disabled button cannot be scrolled to: the buttons start one row up, on 191 (level with the first category), all
    eleven fit to the frame's bottom (961), and Selected item / its name move up into the title band (-24)."""
    if '<!-- 0.56.53 grid 191 -->' in s:
        return s
    for a, b in (('end="0,37" time="0" condition="$EXP[FGS]"', 'end="0,-33" time="0" condition="$EXP[FGS]"'),
                 ('end="47,37" time="0" condition="$EXP[FGS]"', 'end="47,-33" time="0" condition="$EXP[FGS]"'),
                 ('end="0,-3" time="0" condition="$EXP[FGS]"', 'end="0,-73" time="0" condition="$EXP[FGS]"')):
        s = s.replace(a, b)
    up = '<animation effect="slide" end="0,-24" time="0" condition="$EXP[FGS]">Conditional</animation>'
    for cat in ('ctxmenu', 'homemenu'):
        g, e = column(s, cat)
        seg = s[g:e]
        seg = seg.replace('<label>$LOCALIZE[31719]</label>', '<label>$LOCALIZE[31719]</label>' + up)
        seg = seg.replace('<label>$VAR[Aeon_EditTitle]</label>', '<label>$VAR[Aeon_EditTitle]</label>' + up)
        seg = seg.replace('<label>$VAR[Aeon_CtxSelName]</label>', '<label>$VAR[Aeon_CtxSelName]</label>' + up)
        seg = seg.replace('<include condition="!$EXP[Aeon_MS]">Dlg_HmPanelH</include>',
                          '<include condition="!$EXP[Aeon_MS] + !$EXP[FGS]">Dlg_HmPanelH</include>'
                          '<include condition="$EXP[FGS]">FGS_H770</include>')
        s = s[:g] + seg + s[e:]
    return s.replace('<!-- 0.56.53 grid 70 -->', '<!-- 0.56.53 grid 70 --><!-- 0.56.53 grid 191 -->', 1)


LINE = ('<control type="image"><left>%d</left><top>0</top><width>%d</width><height>1</height>'
        '<texture colordiffuse="12ffffff">common/white.png</texture><visible>$EXP[FGS] + !Control.HasFocus(%s)</visible></control>')


def rowlines(s):
    """9. "some menus and menu items are missing horizontal lines for the options" (user, 2026-11-19): in Fused Glass
    style every Home menu row and every option button gets the settings rows' line at its top (12ffffff, hidden on the
    focused row, as Dlg_SkinRowChrome)."""
    if '<!-- 0.56.53 row lines -->' in s:
        return s, 0
    n = 0
    i = s.index('<control type="grouplist" id="9641">')
    e = s.index('<control type="scrollbar" id="9642">', i)
    seg = s[i:e]

    def row(m):
        return (LINE % (41, 1019, m.group(1))).replace('<width>1019</width>', W % (1019, 995)) + m.group(0)
    seg, k = re.subn(r'<control type="button" id="(\d+)">(?=\s*<left>41</left>)', row, seg)
    n += k
    s = s[:i] + seg + s[e:]
    for cat in ('ctxmenu', 'homemenu'):
        g, e = column(s, cat)
        seg = s[g:e]
        seg, k = re.subn(r'<control type="button" id="(\d+)">(?=\s*<left>0</left>)', lambda m: LINE % (0, 319, m.group(1)) + m.group(0), seg)
        n += k
        s = s[:g] + seg + s[e:]
    return s.replace('<!-- 0.56.53 grid 70 -->', '<!-- 0.56.53 grid 70 --><!-- 0.56.53 row lines -->', 1), n


def ctxrows(s):
    """10. the Context menu page as the Home menu page in Fused Glass style: a line at the top of each row (9672-9675),
    the row being edited marked with the style's dimmed bar (it had the Fuse outline), and Selected item / its name at
    the Home menu page's height (that column has no 40 lift: 40 more up)"""
    if '<!-- 0.56.53 ctx rows -->' in s:
        return s, 0
    n = 0
    for rid in ('9672', '9673', '9674', '9675'):
        b = '<control type="button" id="%s">' % rid
        s = s.replace(b, LINE % (-119, 1019, rid) + b, 1)
        n += 1
    sel = re.compile(r'<control type="image"><left>-119</left><top>0</top><width>1019</width><height>70</height>'
                     r'<texture border="16" colordiffuse="80ffffff">fg/selrow16.png</texture><visible>(.*?) \+ \$EXP\[Aeon_FGlass\]</visible></control>')

    def mark(m):
        return (m.group(0).replace('$EXP[Aeon_FGlass]</visible>', '$EXP[Aeon_FGlass] + !$EXP[FGS]</visible>') +
                '<control type="image"><left>-119</left><top>0</top><width>1019</width><height>70</height>'
                '<texture border="20" colordiffuse="40ffffff">fg/fgs_bar.png</texture><visible>%s + $EXP[FGS]</visible></control>' % m.group(1))
    s, k = sel.subn(mark, s)
    n += k
    g, e = column(s, 'ctxmenu')
    seg = s[g:e]
    up = '<animation effect="slide" end="0,-40" time="0" condition="$EXP[FGS]">Conditional</animation>'
    for lab in ('<label>$LOCALIZE[31719]</label>', '<label>$VAR[Aeon_CtxSelName]</label>'):
        seg = seg.replace(lab, lab + up, 1)
    s = s[:g] + seg + s[e:]
    return s.replace('<!-- 0.56.53 grid 70 -->', '<!-- 0.56.53 grid 70 --><!-- 0.56.53 ctx rows -->', 1), n


def main():
    s = io.open(P, encoding='utf-8').read()
    s, nh = heights(s)
    print('grid 70 (style): %d' % nh)
    s = grid191(s)
    s, nl = rowlines(s)
    print('row lines (style): %d' % nl)
    s, nc = ctxrows(s)
    print('ctx rows (style): %d' % nc)
    # 9b. the row lines' width as the rows' (an earlier run had them 995)
    s = s.replace('<left>41</left><top>0</top><width>995</width><height>1</height><texture colordiffuse="12ffffff">',
                  '<left>41</left><top>0</top>' + W % (1019, 995) + '<height>1</height><texture colordiffuse="12ffffff">')
    s, nflush = flush(s)
    print('flush (style): %d widths' % nflush)
    # 7b. the option list (a grouplist, it clips) widens with its buttons; one shift for the bar (an earlier run doubled it)
    for cat in ('ctxmenu', 'homemenu'):
        g, e = column(s, cat)
        seg = s[g:e]
        old = '<control type="grouplist">\n\t\t\t\t<left>0</left><top>0</top><width>256</width>'
        if old in seg:
            seg = seg.replace(old, '<control type="grouplist">\n\t\t\t\t<left>0</left><top>0</top>' + W % (319, 256))
            print('option grouplist widened: %s' % cat)
        s = s[:g] + seg + s[e:]
    dup = '<animation effect="slide" end="-30,0" time="0" condition="$EXP[Aeon_FGlass]">Conditional</animation>'
    j = s.index('<control type="scrollbar" id="9642">')
    end = s.index('</control>', j)
    if dup in s[j:end]:
        s = s[:j] + s[j:end].replace(dup, '', 1) + s[end:]
        print('scroll bar: doubled shift removed')
    s, nstop = scrollstop(s)
    # 6b. the row being edited stays marked while the scroll bar has the focus (it is below 9650)
    i = s.index('<control type="grouplist" id="9641">')
    e = s.index('<control type="scrollbar" id="9642">', i)
    seg = s[i:e]
    old = 'Integer.IsGreater(System.CurrentControlId,9650)'
    if 'Control.HasFocus(9642)]' not in seg:
        print('marker on the bar: %d' % seg.count(old))
        seg = seg.replace(old, '[Integer.IsGreater(System.CurrentControlId,9650) | Control.HasFocus(9642)]')
        s = s[:i] + seg + s[e:]
    print('scroll stop: %d rows' % nstop)
    s, n = focus(s)
    s, k = rows(s)
    s, msg = delete_button(s)
    if 'fg/fgs_bar.png</texture><visible>[String.IsEqual(Window(Home).Property(aeon.editrow)' not in s:
        s, nsel = selrow(s)
        print('selected-row marker (style): %d rows' % nsel)
    # 4. "the new Delete button clips the bottom part of the box, why not bring everything up a little": the column
    #    goes up 40 in Fused Glass (Selected item level with the page title)
    old = '<animation effect="slide" end="24,0" time="0" condition="$EXP[Aeon_FGlass] + !$EXP[FGS]">Conditional</animation>'
    add = ('<animation effect="slide" end="0,-40" time="0" condition="$EXP[Aeon_FGlass] + !$EXP[Aeon_MS]">Conditional</animation>'
           '<!-- 0.56.53 up 40: twelve buttons with Delete fit the panel -->')
    i = s.index('<left>1536</left><top>168</top>\n\t\t\t<visible>String.IsEqual(Window(Home).Property(aeon.skincat),homemenu)</visible>')
    j = s.index(old, i)
    if 'twelve buttons with Delete' not in s:
        s = s[:j + len(old)] + add + s[j + len(old):]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
    print('focus bars: %d buttons; rows: %d widths; %s' % (n, k, msg))
    t = io.open(FUSED, encoding='utf-8').read()
    if '<include name="FGS_BtnFocus">' not in t:
        i = t.index('\t<include name="FGS_RowTex">')
        t = t[:i] + ('\t<!-- 0.56.53 a button in Fused Glass style: the style\'s grey glass bar (white ink reads on it) -->\n'
                     '\t<include name="FGS_BtnFocus"><texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar.png</texturefocus></include>\n') + t[i:]
        io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(t)
    t = io.open(FUSED, encoding='utf-8').read()
    if '<include name="FGS_W319">' not in t:
        i = t.index('\t<include name="FGS_RowTex">')
        t = t[:i] + ('\t<!-- 0.56.53 Home menu / Context menu editors: widths flush with the frame lines in Fused Glass style -->\n'
                     '\t<include name="FGS_W319"><width>319</width></include><include name="FGS_W256_Else"><width>256</width></include>\n'
                     '\t<include name="FGS_W1019"><width>1019</width></include><include name="FGS_W995_Else"><width>995</width></include>\n') + t[i:]
        io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(t)
    for tag, a, b in (('height', 70, 54), ('top', 69, 53), ('height', 150, 134), ('top', 11, 3), ('height', 700, 702),
                      ('height', 70, 60), ('top', 70, 60), ('top', 140, 120), ('top', 7, 2), ('top', 37, 32), ('height', 770, 700)):
        cond(tag, a, b)                                # step 8's includes, also when SkinSettings is done already
    t = io.open(FUSED, encoding='utf-8').read()
    add = ''.join('<include name="%s">%s</include>' % (k, v) for k, v in sorted(HT.items()) if '<include name="%s">' % k not in t)
    if add:
        i = t.index('\t<include name="FGS_RowTex">')
        t = t[:i] + '\t<!-- 0.56.53 Home menu / Context menu editors: the 70 px grid in Fused Glass style -->\n\t' + add + '\n' + t[i:]
        io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(t)
    u = io.open(SUB, encoding='utf-8').read()
    if '<expression name="%s">' % ANY not in u:
        i = u.index('\t<expression name="Aeon_EditSlotOn">')
        u = u[:i] + '\t<expression name="%s">%s</expression>\n' % (ANY, ' | '.join('$EXP[Aeon_EditIsCustom%d]' % k for k in range(1, 11))) + u[i:]
        io.open(SUB, 'w', encoding='utf-8', newline='\n').write(u)


if __name__ == '__main__':
    main()
