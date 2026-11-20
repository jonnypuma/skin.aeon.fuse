# -*- coding: utf-8 -*-
"""0.56.53 List rows, after option A on the box (user, 2026-11-20: "UNRATED DIRECTOR'S CUT ... is cut off. Is it possible
to move the year and genre above to after the title? and non HDR movies should get an SDR chip, so that column fills
out"; "it says DIRECTORS_CUT instead of DIRECTOR'S CUT").
Fused Glass List (510), films and music videos:
- line 1: the title, then the year and the genres dimmed;
- line 2: the version as an outline chip sized to its text (fixed 260, centred: a lone button in a row gets no item);
- the version's name through Aeon_VerPretty: names written with underscores (DIRECTORS_CUT) read as words;
- the HDR slot says SDR when a film is not HDR (List 510 and the wide Low list 527), so the chip column has no hole.
Run after rowchipsA_05653.py. Repeatable."""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import settings_sections as ss  # noqa: E402
import tagrows_05653 as tr  # noqa: E402

P = os.path.join(HERE, '..', '1080i', 'Includes_Fused.xml')
MARK = '<!-- 0.56.53 rowsver -->'
MV = '[String.IsEqual(ListItem.DBType,movie) | String.IsEqual(ListItem.DBType,musicvideo)]'
TAG = '[%s]' % tr.TAG
SDRVIS = ('[String.IsEqual(ListItem.DBType,episode) | String.IsEqual(ListItem.DBType,movie) | String.IsEqual(ListItem.DBType,musicvideo)] + '
          '!String.IsEmpty(ListItem.VideoResolution) + String.IsEmpty(ListItem.HdrType) + $EXP[Aeon_VOMedia] + $EXP[Aeon_Chip_lib]')
NAMES = [('DIRECTORS_CUT', "Director's Cut"), ('DIRECTOR_S_CUT', "Director's Cut"), ('UNRATED_DIRECTORS_CUT', "Unrated Director's Cut"),
         ('EXTENDED_CUT', 'Extended Cut'), ('EXTENDED_EDITION', 'Extended Edition'), ('EXTENDED', 'Extended'), ('THEATRICAL_CUT', 'Theatrical Cut'),
         ('THEATRICAL', 'Theatrical'), ('UNRATED', 'Unrated'), ('UNCUT', 'Uncut'), ('UNCUT_VERSION', 'Uncut Version'), ('SPECIAL_EDITION', 'Special Edition'),
         ('ULTIMATE_EDITION', 'Ultimate Edition'), ('ULTIMATE_CUT', 'Ultimate Cut'), ('FINAL_CUT', 'Final Cut'), ('IMAX', 'IMAX'),
         ('IMAX_EDITION', 'IMAX Edition'), ('REMASTERED', 'Remastered'), ('REMASTER', 'Remaster'), ('CRITERION', 'Criterion'),
         ('CRITERION_COLLECTION', 'Criterion Collection'), ('ANNIVERSARY_EDITION', 'Anniversary Edition'), ('COLLECTORS_EDITION', "Collector's Edition"),
         ('ROGUE_CUT', 'Rogue Cut'), ('OPEN_MATTE', 'Open Matte'), ('ALTERNATE_CUT', 'Alternate Cut'), ('ALTERNATE_ENDING', 'Alternate Ending'),
         ('REDUX', 'Redux'), ('LIMITED_EDITION', 'Limited Edition'), ('RESTORED', 'Restored'), ('RESTORED_EDITION', 'Restored Edition'),
         ('INTERNATIONAL_CUT', 'International Cut'), ('EUROPEAN_CUT', 'European Cut'), ('TELEVISION_CUT', 'Television Cut'), ('WORKPRINT', 'Workprint'),
         ('BLACK_AND_WHITE', 'Black and White'), ('CHROME', 'Chrome'), ('3D', '3D')]
VAR = ('\t<variable name="Aeon_VerPretty">%s<value>$VAR[Aeon_VerStat]</value></variable>\n'
       % ''.join('<value condition="String.IsEqual(ListItem.VideoVersionName,%s)">%s</value>' % (k, v) for k, v in NAMES))


def chip(ink):
    """fixed 260: a lone button in a row gets no item (its label stayed empty on the box), so a picture + a label"""
    return ('<control type="image"><left>22</left><top>49</top><width>260</width><height>26</height><texture border="8" colordiffuse="%s">fg/e8.png</texture>'
            '<visible>%s + %s</visible></control><control type="label"><left>30</left><top>49</top><width>244</width><height>26</height><align>center</align>'
            '<aligny>center</aligny><font>lb_cap_14</font><textcolor>%s</textcolor><selectedcolor>%s</selectedcolor>'
            '<label>[UPPERCASE]$VAR[Aeon_VerPretty][/UPPERCASE]</label><visible>%s + %s</visible></control>' % (ink, MV, TAG, ink, ink, MV, TAG))


def titles(font, ink, focused=False):
    # the focused row: the dark secondary ink on a light bar (FG_L_TitleLine), as FG_L_Ink2
    lab = '$VAR[FG_L_TitleLine]' if focused else '$INFO[ListItem.Label][COLOR 8cffffff]$INFO[ListItem.Year,   ·  ,]$INFO[ListItem.Genre,  ·  ,][/COLOR]'
    one = ('<control type="label"><left>22</left><top>%d</top><width>820</width><height>38</height><align>left</align><aligny>center</aligny>'
           '<font>%s</font><textcolor>%s</textcolor><selectedcolor>%s</selectedcolor><label>%s</label><visible>%s + %s</visible></control>')
    # one line for every film (centring the ones without a version put the genres over the chips)
    return one % (10, font, ink, ink, lab, MV, TAG) + one % (10, font, ink, ink, lab, MV, '!' + TAG)


def sdr(left, top, focused=False):
    return ('<control type="image"><left>%d</left><top>%d</top><width>100</width><height>26</height><texture border="8" colordiffuse="66ffffff">fg/e8.png</texture>'
            '<visible>%s</visible></control><control type="label"><left>%d</left><top>%d</top><width>100</width><height>26</height><align>center</align>'
            '<aligny>center</aligny><font>lb_cap_14</font><textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><label>SDR</label>'
            '<visible>%s</visible></control>' % (left, top, SDRVIS, left, top, SDRVIS)).replace(
        *(('colordiffuse="66ffffff">fg/e8.png', 'colordiffuse="$VAR[FG_L_ChipEdge]">fg/e8.png') if focused else ('', ''))).replace(
        *(('<textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><label>SDR', '<textcolor>$VAR[FG_L_Ink]</textcolor><selectedcolor>$VAR[FG_L_Ink]</selectedcolor><label>SDR') if focused else ('', '')))


def remove_controls(x, pred):
    out, pos = [], 0
    m = ss.masked(x)
    i = 0
    while True:
        i = x.find('<control type="', pos)
        if i < 0:
            break
        e = ss.ctl_end(m, i)
        c = x[i:e]
        if pred(c):
            out.append(x[pos:i])
            pos = e
        else:
            out.append(x[pos:e])
            pos = e
    out.append(x[pos:])
    return ''.join(out)


def layout510(x, focused):
    font = 'lb_ui_24_bold'
    ink = '$VAR[FG_L_Ink]' if focused else 'ffffffff'
    # line 2 of films (and the version chip pairs from rowchipsA) out
    x = x.replace('<!-- 0.56.53 version chip A -->', '')
    film2 = '[String.IsEqual(ListItem.DBType,movie) | String.IsEqual(ListItem.DBType,musicvideo)]'
    x = remove_controls(x, lambda c: (('<left>22</left><top>46</top>' in c or '<left>224</left><top>46</top>' in c) and 'FG_L_RowSub' in c
                                      and film2 in c and '![String.IsEqual(ListItem.DBType,movie)' not in c)
                        or ('<left>22</left><top>48</top><width>190</width>' in c and 'fg/e8.png' in c)
                        or ('<left>30</left><top>48</top><width>174</width>' in c and 'Aeon_VerStat' in c))
    # the title of films moves to the new labels
    old = '<label>$INFO[ListItem.Label]</label><visible>!String.IsEqual(ListItem.DBType,episode)</visible></control>'
    assert old in x, 'title label'
    x = x.replace(old, '<label>$INFO[ListItem.Label]</label><visible>!String.IsEqual(ListItem.DBType,episode) + !%s</visible></control>%s%s%s'
                  % (MV, MARK, titles(font, ink, focused), chip(ink)), 1)
    return x


def main():
    s = io.open(P, encoding='utf-8').read()
    if MARK in s:
        print('rowsver: already there')
        return
    j = s.index('<control type="fixedlist" id="510"')
    for tag in ('itemlayout', 'focusedlayout'):
        i = s.index('<%s' % tag, j)
        i = s.index('>', i) + 1
        e = s.index('</%s>' % tag, i)
        x = layout510(s[i:e], tag == 'focusedlayout')
        x = x + sdr(499, 48, tag == 'focusedlayout')          # at the row's own level (the first chip group is the episodes')
        s = s[:i] + x + s[e:]
    # the wide Low list (527, edge 866): the SDR slot at 506, in every layout of the list
    k = s.index('<control type="list" id="527"')
    end = ss.ctl_end(ss.masked(s), k)
    count = [0]

    def fix(m):
        x = m.group(2)
        if '<left>506</left><top>48</top>' in x and 'SDR</label>' not in x:
            x = x + sdr(506, 48, m.group(1).startswith('<focusedlayout'))
            count[0] += 1
        return m.group(1) + x + m.group(3)
    s = s[:k] + re.sub(r'(<(?:itemlayout|focusedlayout)[^>]*>)(.*?)(</(?:itemlayout|focusedlayout)>)', fix, s[k:end], flags=re.S) + s[end:]
    n = count[0]
    if '<variable name="FG_L_TitleLine">' not in s:
        s = s.replace('</includes>', '\t<variable name="FG_L_TitleLine"><value condition="Control.HasFocus(510) + !$EXP[FG_FocusLight]">$INFO[ListItem.Label][COLOR 9e0f1115]$INFO[ListItem.Year,   ·  ,]$INFO[ListItem.Genre,  ·  ,][/COLOR]</value><value>$INFO[ListItem.Label][COLOR 8cffffff]$INFO[ListItem.Year,   ·  ,]$INFO[ListItem.Genre,  ·  ,][/COLOR]</value></variable>\n' + '</includes>', 1)
    if '<variable name="Aeon_VerPretty">' not in s:
        s = s.replace('</includes>', VAR + '</includes>', 1)
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
    print('rowsver: List 510 rows rebuilt, SDR in %d Low list layouts' % n)


if __name__ == '__main__':
    main()
