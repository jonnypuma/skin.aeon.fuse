# -*- coding: utf-8 -*-
"""0.56.14 the Aeon theme's Album list (532) and Song list (533) to the Album list board on canvas HJTtCDChVWkaZZAyt76wJA
and the user's notes ("no gap between highligh bar and cover column", "artist clearlogo under cover", the grey line
repeated the album's name, the biography showed boxes for phonetic letters):
  rows: 1450 wide, so the focus bar meets the cover column; albums: the grey line "artist · year · genre", on the right
  the release type pill (EP / SINGLE / LIVE), the track count with a note (helper aeon.tc532.<row>) and the length; no
  year column; songs: "artist · album";
  the column under the cover (Aeon_M_SideBio): the artist's clearlogo (else the name, Unicode twin font), the kicker
  (ALBUM · genre / ARTIST · genre / SONG · genre) in gold, the facts (year · tracks · length / formed ... / album · year),
  the album review or the artist's biography in the Unicode twin font (IPA and CJK draw).
Run from the skin folder after aeon_lib_walls.py; runs once (marker per file)."""
import io
import os
import re
import xml.etree.ElementTree as ET

V2 = os.path.join('1080i', 'Includes_Aeon_Views2.xml')
SUB = os.path.join('1080i', 'Includes_Aeon_Sub.xml')
MARK = '0.56.14 aeon_lib_music'
TYPES = (('LIVE', 72, 'String.Contains(ListItem.Property(Album_Type),live)'),
         ('EP', 56, '[String.IsEqual(ListItem.Property(Album_Type),ep) | String.StartsWith(ListItem.Property(Album_Type),ep /)] + !String.Contains(ListItem.Property(Album_Type),live)'),
         ('SINGLE', 100, 'String.StartsWith(ListItem.Property(Album_Type),single) + !String.Contains(ListItem.Property(Album_Type),live)'))
PILL_END = 1214
ROWS = 9


def sub_part(s):
    if MARK in s:
        return s, False
    # the grey line: no album name repeated
    old = '\t\t<value>$INFO[ListItem.Artist]$INFO[ListItem.Album,   |   ,]</value>\n\t</variable>'
    assert s.count(old) == 1
    s = s.replace(old, '\t\t<!-- %s: albums "artist · year · genre", songs "artist · album" -->\n'
                       '\t\t<value condition="Container.Content(albums)">$INFO[ListItem.Artist]$INFO[ListItem.Year,  ·  ,]$INFO[ListItem.Genre,  ·  ,]</value>\n'
                       '\t\t<value>$INFO[ListItem.Artist]$INFO[ListItem.Album,  ·  ,]</value>\n\t</variable>' % MARK)
    # the column under the cover
    a = s.index('<include name="Aeon_M_SideBio">')
    b = s.index('\n\t</include>', a)
    inc = s[a:b]
    lines = inc.split('\n')
    keep = [l for l in lines if '<label>$VAR[Aeon_M_Meta]</label>' not in l and '<label>$VAR[Aeon_M_Bio]</label>' not in l
            and '<left>16</left><top>118</top><width>248</width><height>1</height>' not in l]
    assert len(keep) == len(lines) - 3, (len(keep), len(lines))
    i = [n for n, l in enumerate(keep) if '\t\t</control>' == l.rstrip()][-1]
    new = ('\t\t\t<!-- %s: clearlogo (else the name), kicker, facts, the review or biography -->\n'
           '\t\t\t<control type="image"><left>16</left><top>14</top><width>248</width><height>90</height><aspectratio align="center" aligny="center">keep</aspectratio><fadetime>200</fadetime>'
           '<texture background="true">$VAR[FG_M_ArtistLogo]</texture><visible>$EXP[Aeon_M_HasLogo]</visible></control>\n'
           '\t\t\t<control type="label"><left>16</left><top>14</top><width>248</width><height>90</height><aligny>center</aligny><wrapmultiline>true</wrapmultiline><font>un_lb_ui_28_bold</font><textcolor>ffffffff</textcolor>'
           '<label>$VAR[FG_M_ArtistName]</label><visible>!$EXP[Aeon_M_HasLogo]</visible></control>\n'
           '\t\t\t<control type="label"><left>16</left><top>116</top><width>248</width><height>26</height><aligny>center</aligny><font>lb_cap_16</font><textcolor>fg_mark</textcolor>'
           '<label>[UPPERCASE]$VAR[Aeon_M_Kicker][/UPPERCASE]</label></control>\n'
           '\t\t\t<control type="textbox"><left>16</left><top>144</top><width>248</width><height>60</height><font>lb_small_20_bold</font><textcolor>ffffffff</textcolor>'
           '<label>$VAR[Aeon_M_Facts]</label></control>\n'
           '\t\t\t<control type="image"><left>16</left><top>212</top><width>248</width><height>1</height><texture colordiffuse="30ffffff">common/white.png</texture></control>\n'
           '\t\t\t<control type="textbox"><left>16</left><top>224</top><width>248</width><height>344</height><font>un_lb_small_20</font><textcolor>ccffffff</textcolor>'
           '<label>$VAR[Aeon_M_Bio]</label><autoscroll delay="8000" time="3000" repeat="10000">true</autoscroll></control>' % MARK)
    keep.insert(i, new)
    s = s[:a] + '\n'.join(keep) + s[b:]
    defs = ('\t<!-- %s: the column under the cover -->\n'
            '\t<expression name="Aeon_M_HasLogo">[!String.IsEmpty(ListItem.Art(clearlogo)) | !String.IsEmpty(ListItem.Art(artist.clearlogo)) | !String.IsEmpty(ListItem.Art(albumartist.clearlogo))]</expression>\n'
            '\t<variable name="Aeon_M_Kicker">\n'
            '\t\t<value condition="Container.Content(artists)">$LOCALIZE[557]$INFO[ListItem.Genre,  ·  ,]</value>\n'
            '\t\t<value condition="Container.Content(albums)">$LOCALIZE[558]$INFO[ListItem.Genre,  ·  ,]</value>\n'
            '\t\t<value>$LOCALIZE[179]$INFO[ListItem.Genre,  ·  ,]</value>\n'
            '\t</variable>\n'
            '\t<variable name="Aeon_M_Facts">\n'
            '\t\t<value condition="Container.Content(albums) + Integer.IsEqual(Window(Home).Property(aeon.tc.focus),1)">[UPPERCASE]$INFO[ListItem.Year,,  ·  ]1 $ADDON[skin.aeon.fuse 32308]$VAR[FG_M_Len][/UPPERCASE]</value>\n'
            '\t\t<value condition="Container.Content(albums)">[UPPERCASE]$INFO[ListItem.Year]$INFO[Window(Home).Property(aeon.tc.focus),  ·  , $ADDON[skin.aeon.fuse 32309]]$VAR[FG_M_Len][/UPPERCASE]</value>\n'
            '\t\t<value condition="Container.Content(artists) + [!String.IsEmpty(ListItem.Property(Artist_Formed)) | !String.IsEmpty(ListItem.Property(Artist_Born))]">[UPPERCASE]$VAR[Aeon_M_Dates][/UPPERCASE]</value>\n'
            '\t\t<value condition="Container.Content(artists)">[UPPERCASE]$INFO[ListItem.Property(Artist_YearsActive)][/UPPERCASE]</value>\n'
            '\t\t<value>[UPPERCASE]$INFO[ListItem.Artist]$INFO[ListItem.Album,  ·  ,]$INFO[ListItem.Year,  ·  ,][/UPPERCASE]</value>\n'
            '\t</variable>\n' % MARK)
    assert s.count('</includes>') == 1
    s = s.replace('</includes>', defs + '</includes>')
    return s, True


def pill(name, w, cond, focused):
    x = PILL_END - w
    line = '$PARAM[ink2]'
    ink = '$PARAM[ink]'
    return ('\t\t\t<control type="image"><left>%d</left><top>29</top><width>%d</width><height>34</height><texture border="8" colordiffuse="%s">$VAR[Aeon_TexOutline]</texture><visible>Container.Content(albums) + %s</visible></control>\n'
            '\t\t\t<control type="label"><left>%d</left><top>29</top><width>%d</width><height>34</height><align>center</align><aligny>center</aligny><font>lb_cap_16</font><textcolor>%s</textcolor><selectedcolor>%s</selectedcolor>'
            '<label>%s</label><visible>Container.Content(albums) + %s</visible></control>\n' % (x, w, line, cond, x, w, ink, ink, name, cond))


def v2_part(v):
    if MARK in v:
        return v, False
    # rows 1450 wide: the focus bar meets the cover column
    for cid in ('532', '533'):
        a = v.index('<control type="list" id="%s">' % cid)
        b = v.index('</control>', v.index('</focusedlayout>', a))
        blk = v[a:b]
        assert blk.count('<width>1440</width>') == 1 and blk.count('width="1440"') == 2, cid
        blk = blk.replace('<width>1440</width>', '<width>1450</width>').replace('width="1440"', 'width="1450"')
        v = v[:a] + blk + v[b:]
    a = v.index('<include name="Aeon_V_SongRow">')
    b = v.index('\n\t</include>', a)
    row = v[a:b]
    n = row.count('<left>0</left><top>0</top><width>1440</width>') + row.count('<left>0</left><top>91</top><width>1440</width>')
    assert n == 3, n
    row = row.replace('<left>0</left><top>0</top><width>1440</width>', '<left>0</left><top>0</top><width>1450</width>')
    row = row.replace('<left>0</left><top>91</top><width>1440</width>', '<left>0</left><top>91</top><width>1450</width>')
    # albums: no year column (the year is in the grey line)
    old = '<label>$INFO[ListItem.Year]</label></control>'
    assert row.count(old) == 1
    row = row.replace(old, '<label>$INFO[ListItem.Year]</label><visible>!Container.Content(albums)</visible></control>')
    pills = '\t\t\t<!-- %s: the release type of an album (EP / SINGLE / LIVE) -->\n' % MARK
    for name, w, cond in TYPES:
        pills += pill(name, w, cond, False)
    d = row.rindex('\t\t</definition>')
    row = row[:d] + pills + row[d:]
    v = v[:a] + row + v[b:]
    # the track count of each album row, from the helper (aeon.tc532.<row>), with a note
    a = v.index('<include name="Aeon_V532_ViewAeon">')
    b = v.index('\n\t</include>', a)
    view = v[a:b]
    over = ('\t\t\t<!-- %s: the track count of the album on each screen row (script.aeon.helper aeon.tc532.<row>), with a note -->\n'
            '\t\t\t<control type="group">\n\t\t\t\t<left>90</left><top>144</top>\n'
            '\t\t\t\t<visible>Container.Content(albums) + !Container(532).Scrolling</visible>\n' % MARK)
    for r in range(ROWS):
        for foc, ink, vis in (('n', 'ccffffff', '!Container(532).Position(%d)' % r),
                              ('u', 'ccffffff', 'Container(532).Position(%d) + !Control.HasFocus(532)' % r),
                              ('f', '$VAR[Aeon_VInkF]', 'Container(532).Position(%d) + Control.HasFocus(532)' % r)):
            has = '!String.IsEmpty(Window(Home).Property(aeon.tc532.%d))' % r
            over += ('\t\t\t\t<control type="label"><left>1192</left><top>%d</top><width>102</width><height>92</height><align>right</align><aligny>center</aligny><font>lb_small_20_bold</font>'
                     '<textcolor>%s</textcolor><label>$INFO[Window(Home).Property(aeon.tc532.%d)]</label><visible>%s</visible></control>\n'
                     '\t\t\t\t<control type="image"><left>1300</left><top>%d</top><width>24</width><height>28</height><aspectratio>keep</aspectratio><texture colordiffuse="%s">common/aeon_ic_note.png</texture>'
                     '<visible>%s + %s</visible></control>\n' % (92 * r, ink, r, vis, 92 * r + 32, ink, vis, has))
    over += '\t\t\t</control>\n'
    i = view.index('\t\t\t<include content="Aeon_M_Nav"><param name="cid" value="532"/>')
    view = view[:i] + over + view[i:]
    v = v[:a] + view + v[b:]
    return v, True


def main():
    s = io.open(SUB, encoding='utf-8').read()
    v = io.open(V2, encoding='utf-8').read()
    m = io.open(MLIB, encoding='utf-8').read()
    v3 = io.open(V3, encoding='utf-8').read()
    s, ds = sub_part(s)
    v, dv = v2_part(v)
    v, di = infom_part(v)
    m, dm = list513_part(m)
    v3, dc = circles_part(v3)
    for fn, txt, done in ((SUB, s, ds), (V2, v, dv or di), (MLIB, m, dm), (V3, v3, dc)):
        if done:
            io.open(fn, 'w', encoding='utf-8', newline='\n').write(txt)
            ET.parse(fn)
    print('ok' if (ds or dv or di or dm or dc) else 'already done', ds, dv, di, dm, dc)


MARK_I = '0.56.14 aeon_lib_music infom'
MLIB = os.path.join('1080i', 'Includes_Aeon_MusicLib.xml')
V3 = os.path.join('1080i', 'Includes_Aeon_Views3.xml')


def infom_part(v):
    """the info strip of the Album wall (530), Cover showcase (531) and Artist wall (534): kicker (gold) with the
    artist's clearlogo on the right, the name (Unicode twin), the facts, the review or biography (Unicode twin)"""
    if MARK_I in v:
        return v, False
    a = v.index('<include name="Aeon_V_InfoM">')
    b = v.index('\n\t</include>', a)
    inc = v[a:b]
    lines = inc.split('\n')
    gi = [n for n, l in enumerate(lines) if '<left>88</left><top>$PARAM[top]</top>' in l]
    assert len(gi) == 1
    rule = [n for n, l in enumerate(lines) if '<left>-88</left><top>0</top><width>1820</width><height>1</height>' in l]
    assert len(rule) == 1
    end = [n for n, l in enumerate(lines) if l.strip() == '</control>'][-1]
    body = ('\t\t\t\t<!-- %s: kicker and the artist\'s clearlogo, the name, the facts, the review or biography -->\n'
            '\t\t\t\t<control type="label"><left>0</left><top>10</top><width>1320</width><height>28</height><aligny>center</aligny><font>lb_cap_16</font><textcolor>fg_mark</textcolor>'
            '<label>[UPPERCASE]$VAR[Aeon_M_Kicker][/UPPERCASE]</label></control>\n'
            '\t\t\t\t<control type="image"><left>1380</left><top>12</top><width>300</width><height>96</height><aspectratio align="right" aligny="center">keep</aspectratio><fadetime>200</fadetime>'
            '<texture background="true">$VAR[FG_M_ArtistLogo]</texture><visible>$EXP[Aeon_M_HasLogo] + !Skin.HasSetting(aeon.nologos)</visible></control>\n'
            '\t\t\t\t<control type="label"><left>0</left><top>36</top><width>1340</width><height>52</height><font>un_lb_ui_28_bold</font><textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor>'
            '<label>[UPPERCASE]$INFO[ListItem.Label][/UPPERCASE]</label></control>\n'
            '\t\t\t\t<control type="label"><left>0</left><top>90</top><width>1340</width><height>34</height><aligny>center</aligny><font>lb_small_20_bold</font><textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor>'
            '<label>$VAR[Aeon_M_Facts]</label></control>\n'
            '\t\t\t\t<control type="textbox"><left>0</left><top>134</top><width>1700</width><height>120</height><font>un_lb_small_20</font><textcolor>ccffffff</textcolor>'
            '<label>$VAR[Aeon_M_Bio]</label><autoscroll delay="8000" time="3000" repeat="10000">true</autoscroll><visible>$EXP[Aeon_VOBio]</visible></control>' % MARK_I)
    new = lines[:rule[0] + 1] + [body] + lines[end:]
    v = v[:a] + '\n'.join(new) + v[b:]
    v = v.replace('<include name="Aeon_V_InfoM">', '<!-- %s -->\n\t<include name="Aeon_V_InfoM">' % MARK_I, 1)
    return v, True


def list513_part(m):
    """List (513), the Aeon branch: the artist's clearlogo (artist, album or song) instead of the name over the facts"""
    if MARK in m:
        return m, False
    old = ('\t\t\t<control type="group">\n\t\t\t\t<left>1224</left><top>744</top>\n'
           '\t\t\t\t<!-- 0.39.8: the facts (formed / born, disbanded / died, years active, genre) show whatever the Biography option -->\n'
           '\t\t\t\t<visible>!$EXP[Aeon_FGlass]</visible>\n')
    assert m.count(old) == 1
    i = m.index(old)
    j = m.index('\t\t\t</control>\n', i) + len('\t\t\t</control>\n')
    grp = m[i:j]
    LOGO = '$EXP[Aeon_M_HasLogo] + !Skin.HasSetting(aeon.nologos)'
    plain = grp.replace('<visible>!$EXP[Aeon_FGlass]</visible>', '<visible>!$EXP[Aeon_FGlass] + ![%s]</visible>' % LOGO, 1)
    logo = ('\t\t\t<!-- %s: the artist\'s clearlogo over the facts -->\n'
            '\t\t\t<control type="group">\n\t\t\t\t<left>1224</left><top>744</top>\n'
            '\t\t\t\t<visible>!$EXP[Aeon_FGlass] + %s</visible>\n'
            '\t\t\t\t<control type="image"><left>0</left><top>0</top><width>572</width><height>96</height><aspectratio align="left" aligny="center">keep</aspectratio><fadetime>200</fadetime>'
            '<texture background="true">$VAR[FG_M_ArtistLogo]</texture></control>\n'
            '\t\t\t\t<control type="textbox"><left>0</left><top>108</top><width>572</width><height>110</height><font>lb_cap_20</font><textcolor>ccffffff</textcolor><label>$VAR[Aeon_M_Meta]</label></control>\n'
            '\t\t\t</control>\n' % (MARK, LOGO))
    m = m[:i] + plain + logo + m[j:]
    # the biography under the list in the Unicode twin font (phonetic letters, CJK)
    old = '\t\t\t\t<font>lb_small_20</font><textcolor>ccffffff</textcolor>\n\t\t\t\t<label>$VAR[Aeon_M_Bio]</label>'
    assert m.count(old) == 1
    m = m.replace(old, old.replace('lb_small_20', 'un_lb_small_20'))
    return m, True


def circles_part(v3):
    """Circles (536): people as squares in the Aeon theme (Glass keeps the round portraits; 0.56.14 music video
    artists, 0.56.16 everyone); music artists' names in the Unicode twin font"""
    if MARK in v3:
        return v3, False
    a = v3.index('<include name="Aeon_V536_Tile">')
    b = v3.index('\n\t</include>', a)
    tile = v3[a:b]
    SQ = '!$EXP[Aeon_VGlass]'      # 0.56.16 (the user: "actors shall be squares in Aeon theme in all views and windows")
    out = []
    for l in tile.split('\n'):
        if 'aeon/ring_circle.png' in l or 'common/aeon_circle_mask.png' in l:
            out.append(re.sub(r'<visible>(.*?)</visible>', lambda mm: '<visible>[%s] + !%s</visible>' % (mm.group(1), SQ), l, count=1)
                       if '<visible>' in l else l.replace('</control>', '<visible>!%s</visible></control>' % SQ))
        elif '<label>$INFO[ListItem.Label]</label>' in l:
            out.append(re.sub(r'<visible>(.*?)</visible>', lambda mm: '<visible>[%s] + !Container.Content(artists)</visible>' % mm.group(1), l, count=1))
            out.append(re.sub(r'<visible>(.*?)</visible>', lambda mm: '<visible>[%s] + Container.Content(artists)</visible>' % mm.group(1), l, count=1)
                       .replace('<font>lb_small_20_bold</font>', '<font>un_lb_small_20_bold</font>'))
        else:
            out.append(l)
    d = [n for n, l in enumerate(out) if '</definition>' in l][-1]
    sq = ('\t\t\t<!-- %s: people as squares in the Aeon theme -->\n'
          '\t\t\t<control type="image"><left>22</left><top>9</top><width>172</width><height>172</height><texture colordiffuse="$VAR[Aeon_Accent_L]">common/white.png</texture><visible>$PARAM[focused] + Control.HasFocus(536) + %s</visible></control>\n'
          '\t\t\t<control type="image"><left>28</left><top>15</top><width>160</width><height>160</height><texture colordiffuse="33ffffff">common/white.png</texture><visible>%s</visible></control>\n'
          '\t\t\t<control type="image"><left>28</left><top>15</top><width>160</width><height>160</height><aspectratio align="center" aligny="top">scale</aspectratio><texture background="true">$INFO[ListItem.Icon]</texture><visible>%s</visible></control>'
          % (MARK, SQ, SQ, SQ))
    out.insert(d, sq)
    v3 = v3[:a] + '\n'.join(out).replace('!!$EXP', '$EXP') + v3[b:]
    return v3, True


if __name__ == '__main__':
    main()
