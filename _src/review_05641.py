# -*- coding: utf-8 -*-
"""0.56.41 the user's Skin settings review of 2026-11-18 (the parts built in this version). Run from the skin folder after
the generators that write these rows / views (fg_osd.py writes the player's disc test). Repeatable.

1. Plotline (aeon.plotline): Plot | Tagline | Both (the user: "There should be one more option here: Both ... in many
   views I see both plotline and tagline so the option does not seem to work"). Every separate tagline line now
   follows it: shown with Tagline or Both (expression Aeon_TagOn). Fused Glass views: the plot under the tagline shows
   only with Both, the full-height plot also when the tagline is off; with Tagline only the tagline shows. Aeon views:
   the tagline line only with Both (with Tagline the plot place already shows the tagline); the third version list
   (5224 / 5244) takes the plot through a Plotline variable too. Row 9703 becomes a three-way picker.
2. Spinning disc art (row 9725): Off | Videos | Music | Both (aeon.osd.discart, string; the old switch aeon.osd.disc
   becomes Both once, at Home's first load). The player's disc tests use expression Aeon_OSDDisc.
3. Row 9781 ("Combine multi-episode files into a single row in library"): the name gets the room up to its On / Off.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from appearance_order_05633 import ctl_end  # noqa: E402

D = os.path.join(HERE, '..', '1080i')
PL = 'Skin.String(aeon.plotline)'
TAG_ON = 'String.IsEqual(%s,tagline) | String.IsEqual(%s,both)' % (PL, PL)
BOTH = 'String.IsEqual(%s,both)' % PL
DISC = ('[String.IsEqual(Skin.String(aeon.osd.discart),both) | [String.IsEqual(Skin.String(aeon.osd.discart),video) + Player.HasVideo] | '
        '[String.IsEqual(Skin.String(aeon.osd.discart),music) + Player.HasAudio]]')


def rd(name):
    return io.open(os.path.join(D, name), encoding='utf-8').read()


def wr(name, text):
    io.open(os.path.join(D, name), 'w', encoding='utf-8', newline='\n').write(text)


def add_expression(t, name, value, after):
    """put <expression name> in after the expression `after` (replaced on a re-run)"""
    t = re.sub(r'\n\t<expression name="%s">[^<]*</expression>' % name, '', t)
    i = t.index('<expression name="%s">' % after)
    e = t.index('</expression>', i) + len('</expression>')
    return t[:e] + '\n\t<expression name="%s">%s</expression>' % (name, value.replace('&', '&amp;')) + t[e:]


# ------------------------------------------------------------------------------------------------- 1. plotline
def fused_taglines(t):
    out, pos, n = [], 0, [0, 0, 0]
    for m in re.finditer(r'<control type="(label|textbox)">(?:(?!<control).)*?</control>', t, re.S):
        c = m.group(0)
        lab = re.search(r'<label>(.*?)</label>', c, re.S)
        vis = re.search(r'<visible>(.*?)</visible>', c, re.S)
        if not lab or not vis:
            continue
        v = vis.group(1)
        new = v
        if m.group(1) == 'label' and re.search(r'ListItem\.Tagline\]$', lab.group(1)) and 'Aeon_TagOn' not in v:
            new = v + ' + $EXP[Aeon_TagOn]'
            n[0] += 1
        elif m.group(1) == 'textbox' and '.Plot]' in lab.group(1) and 'Tagline)' in v and 'plotline' not in v and 'Aeon_TagOn' not in v:
            def fix(mm):
                bangs, atom = mm.group(1), mm.group(2)
                if bangs == '!':                 # the plot under the tagline: only with Both
                    n[1] += 1
                    return '!%s + %s' % (atom, BOTH)
                n[2] += 1                        # '' or '!!': the full-height plot, also when the tagline is off
                return '[%s | !$EXP[Aeon_TagOn]]' % atom
            new = re.sub(r'(!{0,2})(String\.IsEmpty\((?:Container\(\d+\)\.)?ListItem\.Tagline\))', fix, v, count=1)
        if new != v:
            c2 = c[:vis.start(1)] + new + c[vis.end(1):]          # vis is a match on the control's own text
            out.append(t[pos:m.start()] + c2)
            pos = m.end()
    out.append(t[pos:])
    print('fused: tagline lines %d, plots under a tagline %d, full plots %d' % tuple(n))
    return ''.join(out)


def aeon_taglines(t):
    n = 0

    def vis(m):
        nonlocal n
        n += 1
        return m.group(1) + '<visible>%s</visible></control>' % BOTH
    t = re.sub(r'(<control type="label">[^\n]*?<label>\$INFO\[(?:Container\(\d+\)\.)?ListItem\.Tagline\]</label>)</control>', vis, t)
    # the version lists' plots through a Plotline variable like their neighbours
    for cid in ('5224', '5244'):
        t = t.replace('<label>$INFO[Container(%s).ListItem.Plot]</label><autoscroll' % cid, '<label>$VAR[Aeon_Plotline_%s]</label><autoscroll' % cid)
        if '<variable name="Aeon_Plotline_%s">' % cid not in t:
            base = '5221' if cid == '5224' else '5241'
            s = t.index('\t<variable name="Aeon_Plotline_%s">' % base)
            e = t.index('</variable>', s) + len('</variable>')
            t = t[:e] + '\n' + t[s:e].replace(base, cid) + t[e:]
    print('aeon: tagline lines', n)
    return t


# ------------------------------------------------------------------------------------------------- rows from templates
def row_group(t, rid):
    i = t.index('<control type="button" id="%d">' % rid)
    j = t.rfind('<include content="Dlg_SkinRowChrome"', 0, i)
    g = t.rfind('<control type="group">', 0, j)
    return g, ctl_end(t, g)


def value_area(t, rid):
    """(start, end) of what follows the row's button inside its content group"""
    _g, e = row_group(t, rid)                                  # the group that holds the chrome, the button, the values
    b = t.index('<control type="button" id="%d">' % rid)
    return ctl_end(t, b), e - len('</control>')


def picker_from(t, template, target, swaps, clicks):
    """the target row's value area = the template's, with its setting, values, labels and id swapped"""
    ts, te = value_area(t, template)
    area = t[ts:te].replace('Control.HasFocus(%d)' % template, 'Control.HasFocus(%d)' % target)
    for a, b in swaps:
        assert a in area, (template, a)
        area = area.replace(a, b)
    s, e = value_area(t, target)
    t = t[:s] + area + t[e:]
    b = t.index('<control type="button" id="%d">' % target)
    be = ctl_end(t, b)
    btn = re.sub(r'\s*<onclick(?: condition="[^"]*")?>[^<]*</onclick>', '', t[b:be])
    btn = btn[:-len('</control>')] + ''.join('\n\t\t\t\t\t' + c for c in clicks) + '\n\t\t\t\t</control>'
    return t[:b] + btn + t[be:]


def settings():
    t = rd('SkinSettings.xml')
    # 1. Plotline: Plot | Tagline | Both from Library background's three segments (Neutral | Fanart | Color)
    t = picker_from(t, 9745, 9703, [
        ('Skin.String(aeon.vbg)', PL), (',neutral)', ',plot)'), (',fanart)', ',tagline)'), (',color)', ',both)'),
        ('$LOCALIZE[31549]', '$LOCALIZE[31690]'), ('$LOCALIZE[31550]', '$LOCALIZE[31691]'), ('$LOCALIZE[31680]', '$LOCALIZE[21475]')],
        ['<onclick condition="[String.IsEmpty(%s) | String.IsEqual(%s,plot)]">Skin.SetString(aeon.plotline,tagline)</onclick>' % (PL, PL),
         '<onclick condition="String.IsEqual(%s,tagline)">Skin.SetString(aeon.plotline,both)</onclick>' % PL,
         '<onclick condition="String.IsEqual(%s,both)">Skin.Reset(aeon.plotline)</onclick>' % PL])
    # 2. Spinning disc art: Off | Videos | Music | Both from Focus highlight's four segments (Pill | Frosted | Outline | Tight)
    da = 'Skin.String(aeon.osd.discart)'
    t = picker_from(t, 9749, 9725, [
        ('Skin.String(aeon.fgfocus)', da), (',pill)', ',off)'), (',frost)', ',video)'), (',outline)', ',music)'), (',tight)', ',both)'),
        ('$ADDON[skin.aeon.fuse 32409]', '$LOCALIZE[31548]'), ('$ADDON[skin.aeon.fuse 32411]', '$LOCALIZE[3]'),
        ('$ADDON[skin.aeon.fuse 32412]', '$LOCALIZE[2]'), ('$ADDON[skin.aeon.fuse 32413]', '$LOCALIZE[21475]')],
        ['<onclick condition="[String.IsEmpty(%s) | String.IsEqual(%s,off)]">Skin.SetString(aeon.osd.discart,video)</onclick>' % (da, da),
         '<onclick condition="String.IsEqual(%s,video)">Skin.SetString(aeon.osd.discart,music)</onclick>' % da,
         '<onclick condition="String.IsEqual(%s,music)">Skin.SetString(aeon.osd.discart,both)</onclick>' % da,
         '<onclick condition="String.IsEqual(%s,both)">Skin.Reset(aeon.osd.discart)</onclick>' % da])
    # 3. the long name of row 9781
    g, e = row_group(t, 9781)
    row = t[g:e]
    row2 = re.sub(r'<param name="namefgs" value="\d+"/>', '<param name="namefgs" value="760"/>', row, count=1)
    row2 = re.sub(r'(<param name="id" value="9781"/>)(?:<param name="namew" value="\d+"/>)?', r'\1<param name="namew" value="680"/>', row2, count=1)
    t = t[:g] + row2 + t[e:]
    wr('SkinSettings.xml', t)
    # help: Plotline and disc art
    s = rd('Includes_Settings.xml')
    s = s.replace('<value condition="Control.HasFocus(9703)">$LOCALIZE[31586]</value>', '<value condition="Control.HasFocus(9703)">$ADDON[skin.aeon.fuse 32721]</value>')
    if 'Control.HasFocus(9725)">' not in s:
        s = s.replace('<value condition="Control.HasFocus(9703)">', '<value condition="Control.HasFocus(9725)">$ADDON[skin.aeon.fuse 32720]</value>\n\t\t<value condition="Control.HasFocus(9703)">', 1)
    wr('Includes_Settings.xml', s)


def player():
    for name in ('Includes_Aeon_OSD.xml', 'Includes_FusedPlayer.xml'):
        t = rd(name)
        t = t.replace('Skin.HasSetting(aeon.osd.disc)', '$EXP[Aeon_OSDDisc]')
        wr(name, t)
    t = rd('Includes_FusedPlayer.xml')
    if '<expression name="Aeon_OSDDisc">' not in t:
        t = t.replace('\t<expression name="FG_OSDHasDisc">', '\t<expression name="Aeon_OSDDisc">%s</expression>\n\t<expression name="FG_OSDHasDisc">' % DISC, 1)
    wr('Includes_FusedPlayer.xml', t)
    # the old switch becomes Both once (Home's first load after the update)
    h = rd('Home.xml')
    line = ('\t<onload condition="Skin.HasSetting(aeon.osd.disc) + String.IsEmpty(Skin.String(aeon.osd.discart))">Skin.SetString(aeon.osd.discart,both)</onload>\n'
            '\t<onload condition="Skin.HasSetting(aeon.osd.disc)">Skin.Reset(aeon.osd.disc)</onload>\n')
    if 'aeon.osd.discart' not in h:
        i = h.index('\t<onload')
        h = h[:i] + line + h[i:]
        wr('Home.xml', h)


ART_MARK = '<!-- 0.56.41 art trigger -->'


def art_trigger(t):
    """4. the Fused Glass List view showed no poster and no fanart on the box (Kodi 22): the focused item's art was never
    loaded, because nothing in the list's own rows draws art for a film. A 2 x 2 near-clear poster in the focused row
    makes Kodi load that item's art (poster, fanart, logo for the view around it); only the focused row, so no other
    row's fanart is loaded."""
    # Tested on the box: it did not help, and the cause is elsewhere. Kodi loads the art of a library list in the
    # background from the top: in 6127 films, Lawrence of Arabia gets its poster ~30-40 s after the view opens. The
    # trigger is taken out again (a later version may have the helper fetch the focused item's art first).
    trigger = (ART_MARK + '<control type="image"><left>0</left><top>0</top><width>2</width><height>2</height>'
               '<texture colordiffuse="01ffffff" background="true">$INFO[ListItem.Art(poster)]</texture></control>')
    if trigger in t:
        t = t.replace(trigger, '')
        print('List view: art trigger taken out')
    return t


def stack_preview():
    """5. the Stacked row's preview card (row 9755) redrawn from skin_previews.p_stack, in place, so the generator chain
    after skin_previews need not run again"""
    import skin_previews as sp
    t = rd('SkinSettings.xml')
    tag = '<!-- preview:9755 -->'
    s = t.index('<control type="group">', t.index(tag))
    e = ctl_end(t, s)
    cwd = os.getcwd()
    os.chdir(os.path.join(HERE, '..'))
    try:
        inner = sp.new_inner('home', sp.p_stack)
    finally:
        os.chdir(cwd)
    t = t[:s] + '<control type="group"><visible>Control.HasFocus(9755)</visible>%s</control>' % inner + t[e:]
    wr('SkinSettings.xml', t)


FONT_MARK = '<!-- 0.56.41 heading sample -->'


def font_mock():
    """6. the font picker's preview (Aeon_FontMock): the user saw Figtree, Fraunces + Figtree and Bebas Neue + Figtree
    "IDENTICAL": only the top line used the heading face, everything else the text face (Figtree in all three). A film
    title in the heading face now stands over the text, which moves down under it."""
    t = rd('Includes_Aeon_Menu.xml')
    if FONT_MARK in t:
        return
    old_body = '<control type="textbox"><left>40</left><top>444</top><width>920</width><height>140</height><font>pv$PARAM[n]_b</font>'
    assert old_body in t
    t = t.replace(old_body, '<control type="textbox"><left>40</left><top>506</top><width>920</width><height>84</height><font>pv$PARAM[n]_b</font>', 1)
    head = ('<control type="label"><left>40</left><top>58</top><width>920</width><height>76</height><font>pv$PARAM[n]_h</font>'
            '<textcolor>$VAR[AG_Ink]</textcolor><label>$INFO[Container(100).ListItem.Label]</label></control>')
    assert head in t
    t = t.replace(head, head + FONT_MARK + '<control type="label"><left>40</left><top>438</top><width>920</width><height>64</height>'
                  '<font>pv$PARAM[n]_h</font><textcolor>ffffffff</textcolor><label>Lawrence of Arabia</label></control>', 1)
    wr('Includes_Aeon_Menu.xml', t)


def band():
    """7. Band under the Home menu (aeon.homeband) in Fused Glass too (the user: "Fused Glass shall have it too, default is
    off"): Home draws it in every theme; Skin settings > Backgrounds shows the row in every theme, in Fused Glass one row
    lower (the Home bar row has its place there), Up / Down through both."""
    h = rd('Includes_Aeon_Home.xml')
    h = h.replace('<visible>Skin.HasSetting(aeon.homeband) + !$EXP[Aeon_FGlass]</visible>', '<visible>Skin.HasSetting(aeon.homeband)</visible>')
    h = h.replace('(aeon.homeband, Aeon / Glass, off by default)', '(aeon.homeband, every theme since 0.56.41, off by default)')
    wr('Includes_Aeon_Home.xml', h)
    t = rd('SkinSettings.xml')
    slide = '<animation effect="slide" start="0,0" end="0,70" time="0" condition="$EXP[Aeon_FGlass]">Conditional</animation>'
    if slide + '<!-- 9737 -->' not in t:
        # the row's own group: its visibility becomes the slide
        b = t.index('<control type="button" id="9737">')
        g = t.rfind('<control type="group">', 0, t.rfind('<include content="Dlg_SkinRowChrome"', 0, b))
        head_end = t.index('<include content="Dlg_SkinRowChrome"', g)
        head = t[g:head_end]
        assert '<visible>!$EXP[Aeon_FGlass]</visible>' in head, head[:200]
        head = head.replace('<visible>!$EXP[Aeon_FGlass]</visible>', slide + '<!-- 9737 -->', 1)
        t = t[:g] + head + t[head_end:]
        # its focus bar
        f = t.index('<visible>Control.HasFocus(9737)</visible>')
        t = t[:f] + '<visible>Control.HasFocus(9737)</visible>' + slide + t[f + len('<visible>Control.HasFocus(9737)</visible>'):]
    # Up / Down: Aeon ... 9736 > 9737 > 9730; Fused Glass ... 9736 > 9764 > 9737 > 9730
    def nav(rid, ups, downs):
        nonlocal t
        b = t.index('<control type="button" id="%d">' % rid)
        e = ctl_end(t, b)
        btn = re.sub(r'\s*<on(?:up|down)(?: condition="[^"]*")?>[^<]*</on(?:up|down)>', '', t[b:e])
        btn = btn.replace('<control type="button" id="%d">' % rid, '<control type="button" id="%d">\n\t\t\t\t\t%s%s' % (rid, ups, downs), 1)
        t = t[:b] + btn + t[e:]
    fg, ae = '$EXP[Aeon_FGlass]', '!$EXP[Aeon_FGlass]'
    nav(9737, '<onup condition="%s">9764</onup><onup condition="%s">9736</onup>' % (fg, ae), '<ondown>9730</ondown>')
    nav(9764, '<onup>9736</onup>', '<ondown>9737</ondown>')
    nav(9730, '<onup>9737</onup>', '<ondown>9731</ondown>')
    wr('SkinSettings.xml', t)


def main():
    band()
    font_mock()
    stack_preview()
    t = rd('Includes_Aeon_Sub.xml')
    t = add_expression(t, 'Aeon_TagOn', TAG_ON, 'Aeon_VOPlot')
    wr('Includes_Aeon_Sub.xml', t)
    wr('Includes_Fused.xml', art_trigger(fused_taglines(rd('Includes_Fused.xml'))))
    wr('Includes_Aeon_Views2.xml', aeon_taglines(rd('Includes_Aeon_Views2.xml')))
    settings()
    player()
    print('done')


if __name__ == '__main__':
    main()
