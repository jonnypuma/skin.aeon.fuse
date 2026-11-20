# -*- coding: utf-8 -*-
"""0.56.14 the Aeon theme's Low list (527) and the shared info chips (Aeon_V_Chips2: Low list, Flix) to the list row and
info panel rules (canvas HJTtCDChVWkaZZAyt76wJA). The user's notes: the watched status right before the run time in one
column on every list; "resolution pill shall be on the far right always"; "watched status next to certification";
Low list: "move episode thumb next to clearlogo", "align network logo on the right" (the network logo at the panel's
bottom right, as tall as the clock / count box at most, as in the Episode list).
Low list rows (Aeon_LowRow, 1093 x 108, as the List view's): episodes and films get the List's chips (audio, aspect,
HDR, the resolution pill on the far right), the eye in the List's mark column (955) right before the run time, the ring
and the time left in yellow while in progress; the title ends before the chips.
Aeon_V_Chips2: the status (eye / ring and the words) after the certificate and run time; one audio chip; HDR with the
profile, no SDR; the resolution last.
Low list panel (Aeon_V527_ViewAeon, Aeon / Glass only): episodes get the facts line "SEASON 1 | EPISODE 1 | date |
minutes | ENDS"; the episode picture beside the clearlogo; the network logo at the bottom right; the separate WATCHED
line goes for episodes (the status is beside the certificate now).
Run from the skin folder after aeon_lib_lists.py; runs once."""
import io
import os
import re
import xml.etree.ElementTree as ET

VID = os.path.join('1080i', 'Includes_Aeon_Video.xml')
V2 = os.path.join('1080i', 'Includes_Aeon_Views2.xml')
MARK = '0.56.14 aeon_lib_lists2'
PROG = 'Integer.IsGreater(ListItem.PercentPlayed,0)'
HDR = '!String.IsEmpty(ListItem.HdrType)'
RES = '!String.IsEmpty(ListItem.VideoResolution)'
MARK_X, CHIPS_END, GAP = 955, 941, 8
W_RES, W_AUD, W_ASP, W_HDR = 144, 150, 80, 96


def add_vis(xml, extra):
    return re.sub(r'<visible>(.*?)</visible>', lambda m: '<visible>[%s] + %s</visible>' % (m.group(1), extra), xml, count=1)


def chip(x, w, label, vis, focused):
    line = '$VAR[Aeon_OnBarLine]' if focused else '88ffffff'
    ink = '$VAR[Aeon_OnBarInk2_L]' if focused else 'ccffffff'
    return ('<control type="image"><left>%d</left><top>34</top><width>%d</width><height>40</height><texture border="8" colordiffuse="%s">$VAR[Aeon_TexOutline]</texture><visible>%s</visible></control>'
            '<control type="label"><left>%d</left><top>34</top><width>%d</width><height>40</height><align>center</align><aligny>center</aligny><font>lb_cap_16</font>'
            '<textcolor>%s</textcolor><selectedcolor>%s</selectedcolor><label>%s</label><visible>%s</visible></control>\n'
            % (x, w, line, vis, x + 6, w - 12, ink, ink, label, vis))


def low_row_parts():
    out = '\t\t\t<!-- %s: the List view\'s chips (resolution pill on the far right), ring and time left -->\n' % MARK
    for focused in (False, True):
        f = '[$PARAM[focused] + Control.HasFocus(527)]' if focused else '![$PARAM[focused] + Control.HasFocus(527)]'
        base = '%s + %s' % (RES, f)
        for has_hdr in (True, False):
            hv = HDR if has_hdr else '!' + HDR
            x = CHIPS_END - W_RES - GAP
            if has_hdr:
                x -= W_HDR
                out += '\t\t\t' + chip(x, W_HDR, '$VAR[FG_L_HdrChip]', '%s + %s' % (base, HDR), focused)
                x -= GAP
            x -= W_ASP
            out += '\t\t\t' + chip(x, W_ASP, '$INFO[ListItem.VideoAspect]:1', '%s + %s + !String.IsEmpty(ListItem.VideoAspect)' % (base, hv), focused)
            x -= GAP + W_AUD
            out += '\t\t\t' + chip(x, W_AUD, '[UPPERCASE]$VAR[FG_EcAudio][/UPPERCASE]', '%s + %s + !String.IsEmpty(ListItem.AudioCodec)' % (base, hv), focused)
        # Aeon's two-part resolution pill, rightmost
        x = CHIPS_END - W_RES
        line = '$VAR[Aeon_OnBarLine]' if focused else '88ffffff'
        fill = '$VAR[Aeon_OnBarFill_L]' if focused else 'lib_aeon_white'
        ink = '$VAR[Aeon_OnBarInk2_L]' if focused else 'ccffffff'
        inv = '$VAR[Aeon_OnBarInv]' if focused else 'lib_aeon_onbar'
        out += ('\t\t\t<control type="image"><left>%d</left><top>34</top><width>%d</width><height>40</height><texture colordiffuse="%s">common/aeon_badge_fill.png</texture><visible>%s + $EXP[Aeon_HasResL] + %s</visible></control>\n'
                '\t\t\t<control type="image"><left>%d</left><top>34</top><width>%d</width><height>40</height><texture colordiffuse="%s">common/aeon_badge_out.png</texture><visible>%s + $EXP[Aeon_HasResL] + %s</visible></control>\n'
                '\t\t\t<control type="label"><left>%d</left><top>34</top><width>86</width><height>40</height><align>center</align><aligny>center</aligny><font>lb_cap_20</font><textcolor>%s</textcolor><selectedcolor>%s</selectedcolor><label>$VAR[Aeon_ResL]</label><visible>%s + $EXP[Aeon_HasResL] + %s</visible></control>\n'
                '\t\t\t<control type="label"><left>%d</left><top>34</top><width>58</width><height>40</height><align>center</align><aligny>center</aligny><font>lb_cap_20</font><textcolor>%s</textcolor><selectedcolor>%s</selectedcolor><label>$VAR[Aeon_ResR]</label><visible>%s + $EXP[Aeon_HasResL] + %s</visible></control>\n'
                '\t\t\t<control type="image"><left>%d</left><top>34</top><width>62</width><height>40</height><texture colordiffuse="%s">common/aeon_badge_solo_fill.png</texture><visible>%s + !$EXP[Aeon_HasResL] + %s</visible></control>\n'
                '\t\t\t<control type="label"><left>%d</left><top>34</top><width>62</width><height>40</height><align>center</align><aligny>center</aligny><font>lb_cap_20</font><textcolor>%s</textcolor><selectedcolor>%s</selectedcolor><label>$VAR[Aeon_ResR]</label><visible>%s + !$EXP[Aeon_HasResL] + %s</visible></control>\n'
                % (x, W_RES, fill, RES, f, x, W_RES, line, RES, f, x, ink, ink, RES, f, x + 86, inv, inv, RES, f,
                   CHIPS_END - 62, fill, RES, f, CHIPS_END - 62, inv, inv, RES, f))
        ring = '$VAR[Aeon_OnBarInk_L]' if focused else 'fg_mark'
        out += ('\t\t\t<control type="image"><left>%d</left><top>40</top><width>28</width><height>28</height><texture colordiffuse="%s">fg/pring/$INFO[ListItem.PercentPlayed].png</texture><visible>%s + %s</visible></control>\n'
                '\t\t\t<control type="label"><left>996</left><top>0</top><width>94</width><height>108</height><align>center</align><aligny>center</aligny><font>lb_ui_24_bold</font><textcolor>%s</textcolor><selectedcolor>%s</selectedcolor><label>$VAR[Aeon_RowLeft]</label><visible>%s + %s</visible></control>\n'
                % (MARK_X, ring, PROG, f, ring, ring, PROG, f))
    return out


def chips2(bar):
    """Aeon_V_Chips2: status after the certificate / run time; audio as one chip, HDR with the profile and no SDR,
    the resolution last"""
    # params: dur (the run-time chip; the Low list has it in the facts line), stat (the status; the Low list's shows
    # have their own watched count line)
    bar = bar.replace('<param name="width">540</param>', '<param name="width">540</param>\n\t\t<param name="dur">true</param>\n\t\t<param name="stat">true</param>', 1)
    g1 = bar.index('<control type="grouplist"><left>$PARAM[left]</left><top>$PARAM[top1]</top>')
    g1e = bar.index('\t\t\t</control>', g1)
    grp = bar[g1:g1e]
    n = grp.count('<label>$VAR[Aeon_LVDur]</label>')
    assert n == 2, n
    grp = '\n'.join(add_vis(l, '$PARAM[dur]') if '<label>$VAR[Aeon_LVDur]</label>' in l else l for l in grp.split('\n'))
    bar = bar[:g1] + grp + bar[g1e:]
    g1e = bar.index('\t\t\t</control>', g1)
    status = ('<control type="label"><width>4</width><height>34</height><label></label><visible>$PARAM[stat]</visible></control>\n'
              '<control type="image"><width>34</width><height>34</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">common/aeon_eye_off.png</texture><visible>$EXP[Aeon_LV_Dot] + $PARAM[stat]</visible></control>\n'
              '<control type="image"><width>34</width><height>34</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">common/aeon_eye.png</texture><visible>$EXP[Aeon_LV_Tick] + $PARAM[stat]</visible></control>\n'
              '<control type="image"><width>30</width><height>34</height><aspectratio>keep</aspectratio><texture colordiffuse="fg_mark">fg/pring/$INFO[ListItem.PercentPlayed].png</texture><visible>$EXP[Aeon_LV_Ring] + $PARAM[stat]</visible></control>\n'
              '<control type="label"><width min="10" max="400">auto</width><height>34</height><aligny>center</aligny><font>lb_small_20_bold</font><textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><label>[UPPERCASE]$VAR[Aeon_LV_Status][/UPPERCASE]</label><visible>!$EXP[Aeon_LV_Ring] + $PARAM[stat]</visible></control>\n'
              '<control type="label"><width min="10" max="400">auto</width><height>34</height><aligny>center</aligny><font>lb_small_20_bold</font><textcolor>fg_mark</textcolor><selectedcolor>fg_mark</selectedcolor><label>[UPPERCASE]$VAR[Aeon_LV_Status][/UPPERCASE]</label><visible>$EXP[Aeon_LV_Ring] + $PARAM[stat]</visible></control>\n')
    bar = bar[:g1e] + status + bar[g1e:]
    g2 = bar.index('<control type="grouplist"><left>$PARAM[left]</left><top>$PARAM[top2]</top>')
    g2e = bar.index('\t\t\t</control>', g2)
    lines = bar[g2:g2e].split('\n')
    head, items = lines[0], [l for l in lines[1:] if l.strip()]
    keep = []
    for l in items:
        if '$VAR[Aeon_LVCh]' in l or 'Property(aeon.dvp)' in l:
            continue
        l = l.replace('$VAR[Aeon_LVAud]', '[UPPERCASE]$VAR[FG_EcAudio][/UPPERCASE]').replace('$VAR[Aeon_LVHdr]', '$VAR[FG_L_HdrChip]')
        if '$VAR[FG_L_HdrChip]' in l:
            l = add_vis(l, '!String.IsEmpty(ListItem.HdrType)') if '<visible>' in l else l.replace('</control>', '<visible>!String.IsEmpty(ListItem.HdrType)</visible></control>', 1)
        keep.append(l)

    def key(l):
        for i, k in enumerate(('FG_EcAudio', 'Aeon_LVAsp', 'FG_L_HdrChip', 'Aeon_LVRes')):
            if k in l:
                return i
        return 9
    keep.sort(key=key)
    return bar[:g2] + head + '\n' + '\n'.join(keep) + '\n' + bar[g2e:]


def main():
    t = io.open(VID, encoding='utf-8').read()
    v = io.open(V2, encoding='utf-8').read()
    if MARK in t:
        print('already done')
        return
    # ---------------------------------------------------------------- Low list rows
    a = t.index('<include name="Aeon_LowRow">')
    b = t.index('\t</include>', a)
    row = t[a:b]
    n = row.count('<include content="Aeon_WatchMark"><param name="left">922</param>')
    assert n == 2, n
    row = row.replace('<include content="Aeon_WatchMark"><param name="left">922</param>', '<include content="Aeon_WatchMark"><param name="left">%d</param>' % MARK_X)
    row = re.sub(r'<control type="group"><visible>[^<]*</visible>(?:<control type="group">)?<include content="Aeon_(?:WatchMark|Dur)">.*?</control>(?:</control>)?',
                 lambda m: add_vis(m.group(0), '!%s' % PROG), row)
    # the run time (a vis param) gives way to the time left too
    row, n = re.subn(r'(<include content="Aeon_Dur"><param name="left">1014</param>.*?<param name="vis" value=")([^"]*)("/>)',
                     lambda m: '%s[%s] + !%s%s' % (m.group(1), m.group(2), PROG, m.group(3)), row)
    assert n == 2, n
    # the title / grey line end before the chips (items with a resolution)
    def narrow(m):
        lab = m.group(0)
        out = add_vis(lab, 'String.IsEmpty(ListItem.VideoResolution)')
        for has_hdr in (False, True):
            start = CHIPS_END - W_RES - GAP - (W_HDR + GAP if has_hdr else 0) - W_ASP - GAP - W_AUD
            twin = lab.replace('<width>740</width>', '<width>%d</width>' % (start - 16 - 150), 1)
            out += '\n\t\t\t' + add_vis(twin, '%s + %s' % (RES, HDR if has_hdr else '!' + HDR))
        return out
    row, n = re.subn(r'<control type="label"><left>150</left><top>(?:18|56)</top><width>740</width>.*?</control>', narrow, row)
    assert n == 4, n
    d = row.rindex('\t\t</definition>')
    row = row[:d] + low_row_parts() + row[d:]
    t = t[:a] + row + t[b:]

    # ---------------------------------------------------------------- Low list panel (Aeon / Glass only)
    a = t.index('<include name="Aeon_V527_ViewAeon">')
    b = t.index('\t</include>', a)
    p = t[a:b]
    EPT = 'Container.Content(episodes) + !String.IsEmpty(ListItem.Art(thumb)) + $EXP[Aeon_VOArt]'
    # the clearlogo / show title: 340 wide when the episode picture stands beside it
    p = re.sub(r'<control type="image"><left>100</left><top>432</top><width>600</width><height>140</height>.*?</control>',
               lambda m: add_vis(m.group(0), '![%s]' % EPT) + '\n\t\t\t' + add_vis(m.group(0).replace('<width>600</width>', '<width>340</width>', 1), EPT), p, count=1)
    p = re.sub(r'<control type="label"><left>100</left><top>422</top><width>600</width><height>150</height>.*?</control>',
               lambda m: add_vis(m.group(0), '![%s]' % EPT) + '\n\t\t\t' + add_vis(m.group(0).replace('<width>600</width>', '<width>340</width>', 1), EPT), p, count=1)
    # the episode picture beside the logo (it stood at the bottom)
    n = p.count('<control type="image"><left>100</left><top>906</top><width>240</width><height>135</height>')
    assert n == 2, n
    p = p.replace('<control type="image"><left>100</left><top>906</top><width>240</width><height>135</height>',
                  '<control type="image"><left>460</left><top>432</top><width>240</width><height>135</height>')
    # the network / studio logo at the bottom right, as tall as the count box at most (no slide beside the picture)
    m = re.search(r'<control type="image"><left>100</left><top>940</top><width>600</width><height>80</height>.*?</control>', p)
    assert m
    logo = m.group(0)
    logo = re.sub(r'<animation effect="slide"[^>]*>Conditional</animation>', '', logo)
    logo = logo.replace('<left>100</left><top>940</top><width>600</width><height>80</height>', '<left>100</left><top>972</top><width>600</width><height>108</height>', 1)
    logo = logo.replace('<aspectratio align="left" aligny="center">keep</aspectratio>', '<aspectratio align="right" aligny="center">keep</aspectratio>', 1)
    p = p.replace(m.group(0), logo)
    # facts line: episodes as the Episode list's
    old = '<label>$VAR[Aeon_LowMeta]</label>'
    assert p.count(old) == 1
    p = p.replace(old, '<label>$VAR[Aeon_LowFacts]</label>')
    # the chips: no run-time chip (it is in the facts line), so the status stands next to the certificate; shows and
    # seasons keep their watched count line instead
    old = '<include content="Aeon_V_Chips2"><param name="left">100</param><param name="top1">634</param><param name="top2">678</param><param name="width">600</param></include>'
    assert p.count(old) == 1
    p = p.replace(old, old.replace('</include>', '<param name="dur">false</param><param name="stat">![Container.Content(tvshows) | Container.Content(seasons)]</param></include>'))
    # the WATCHED line: not for episodes (the status is beside the certificate)
    old = '<label>[UPPERCASE]$VAR[Aeon_LowWatched][/UPPERCASE]</label><visible>'
    assert p.count(old) == 1
    p = p.replace(old, '<label>[UPPERCASE]$VAR[Aeon_LowWatched][/UPPERCASE]</label><visible>!Container.Content(episodes) + ')
    t = t[:a] + p + t[b:]
    t = t.replace('</includes>', '\t<!-- %s: the Low list\'s facts line -->\n'
                  '\t<variable name="Aeon_LowFacts">\n'
                  '\t\t<value condition="String.IsEqual(ListItem.DBType,episode)">[UPPERCASE]$INFO[ListItem.Season,$LOCALIZE[20373] ,]$INFO[ListItem.Episode, | $LOCALIZE[20359] ,]$INFO[ListItem.Premiered, | ,]'
                  '$INFO[ListItem.Duration(mins), | , $ADDON[skin.aeon.fuse 32220]]$INFO[ListItem.EndTimeResume, | $LOCALIZE[31030] ,][/UPPERCASE]</value>\n'
                  '\t\t<value condition="String.IsEqual(ListItem.DBType,movie) | String.IsEqual(ListItem.DBType,musicvideo)">[UPPERCASE]$INFO[ListItem.Year]$INFO[ListItem.Duration(mins), | , $ADDON[skin.aeon.fuse 32220]]'
                  '$INFO[ListItem.EndTimeResume, | $LOCALIZE[31030] ,]$INFO[ListItem.Genre, | ,][/UPPERCASE]</value>\n'
                  '\t\t<value>$VAR[Aeon_LowMeta]</value>\n'
                  '\t</variable>\n</includes>' % MARK)
    io.open(VID, 'w', encoding='utf-8', newline='\n').write(t)

    # ---------------------------------------------------------------- Aeon_V_Chips2
    a = v.index('<include name="Aeon_V_Chips2">')
    b = v.index('\t</include>', a)
    v = v[:a] + chips2(v[a:b]) + v[b:]
    v = v.replace('<include name="Aeon_V_Chips2">', '<!-- %s: status after the certificate, one audio chip, no SDR, the resolution last -->\n\t<include name="Aeon_V_Chips2">' % MARK, 1)
    io.open(V2, 'w', encoding='utf-8', newline='\n').write(v)
    ET.parse(VID)
    ET.parse(V2)
    print('ok')


if __name__ == '__main__':
    main()
