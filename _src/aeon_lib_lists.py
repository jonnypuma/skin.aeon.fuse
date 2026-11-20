# -*- coding: utf-8 -*-
"""0.56.14 the Aeon theme's Compact list (524) rows and the Banner / Compact list band (Aeon_V_Bar, 522 / 524) to the
list row and info panel rules (canvas HJTtCDChVWkaZZAyt76wJA; the user: "move watched status to before duration, they
shall all be on the same column and aligned vertically on every list", "resolution pill shall be on the far right
always", "then build the other ones").
Compact list rows (Aeon_V_Row, 760 x 62, one line): the eye in its column right before the run time (films and episodes
alike), the rating after the run time; in progress the ring and the time left (helper aeon.left.N.hm) in yellow. The row
has room for the resolution pill only, which it keeps; audio, aspect and HDR are in the band.
Band (Aeon_V_Bar): as the List view's band (_src/aeon_lib510.py): year and Ends in the facts line, the status line first
in the chips row, audio as one chip, HDR with the profile and no SDR, the resolution last, the studio's logo or name.
The status of the focused item: Aeon_LV_Dot / Tick / Ring / Status, made from Fused Glass's FG_L510_* with
Container(510).ListItem read as ListItem.
Run from the skin folder after aeon_lib510.py / aeon_lib511.py; runs once."""
import io
import os
import re
import xml.etree.ElementTree as ET

V2 = os.path.join('1080i', 'Includes_Aeon_Views2.xml')
FUSED = os.path.join('1080i', 'Includes_Fused.xml')
MARK = '0.56.14 aeon_lib_lists'
PROG = 'Integer.IsGreater(ListItem.PercentPlayed,0)'


def add_vis(xml, extra):
    return re.sub(r'<visible>(.*?)</visible>', lambda m: '<visible>[%s] + %s</visible>' % (m.group(1), extra), xml, count=1)


def status_defs():
    """Aeon_LV_*: Fused Glass's 510 status, for the focused item of whichever list has the focus"""
    f = io.open(FUSED, encoding='utf-8').read()
    out = ''
    for kind, name in (('expression', 'Dot'), ('expression', 'Tick'), ('expression', 'Ring')):
        m = re.search(r'\t<expression name="FG_L510_%s">.*?</expression>\n' % name, f)
        assert m, name
        out += m.group(0).replace('FG_L510_', 'Aeon_LV_').replace('Container(510).ListItem', 'ListItem')
    m = re.search(r'\t<variable name="FG_L510_Status">.*?</variable>\n', f, re.S)
    assert m
    out += m.group(0).replace('FG_L510_', 'Aeon_LV_').replace('Container(510).ListItem', 'ListItem')
    return out


def main():
    v = io.open(V2, encoding='utf-8').read()
    if MARK in v:
        print('already done')
        return
    # ---------------------------------------------------------------- Compact list rows
    a = v.index('<include name="Aeon_V_Row">')
    b = v.index('\t</include>', a)
    row = v[a:b]
    moves = (('<include content="Aeon_WatchMark"><param name="left">668</param>', '<include content="Aeon_WatchMark"><param name="left">544</param>', 2),
             ('<include content="Aeon_WatchMark"><param name="left">712</param>', '<include content="Aeon_WatchMark"><param name="left">556</param>', 2),
             ('<include content="Aeon_Dur"><param name="left">544</param>', '<include content="Aeon_Dur"><param name="left">584</param>', 1),
             ('<include content="Aeon_Dur"><param name="left">556</param>', '<include content="Aeon_Dur"><param name="left">596</param>', 1),
             ('<control type="label"><left>606</left><top>0</top><width>60</width><height>62</height>', '<control type="label"><left>646</left><top>0</top><width>60</width><height>62</height>', 1),
             ('<control type="label"><left>634</left><top>0</top><width>60</width><height>62</height>', '<control type="label"><left>674</left><top>0</top><width>60</width><height>62</height>', 1))
    for old, new, n in moves:
        assert row.count(old) == n, (old, row.count(old))
        row = row.replace(old, new)
    # TV shows and seasons have no run time: their eye stays behind their count columns (shows 606, between E and the
    # rating; seasons 712, the old column), and they get no ring
    def twin(m):
        g = m.group(0)
        left = re.search(r'<param name="left">(\d+)</param>', g).group(1)
        kind, x = ('tvshows', 606) if left == '544' else ('seasons', 712)
        return (add_vis(g, '!Container.Content(%s)' % kind) + '\n\t\t\t\t' +
                add_vis(g.replace('<param name="left">%s</param>' % left, '<param name="left">%d</param>' % x), 'Container.Content(%s)' % kind))
    row, n = re.subn(r'<control type="group"><visible>[^<]*</visible><include content="Aeon_WatchMark"><param name="left">(?:544|556)</param>.*?</control>', twin, row)
    assert n == 4, n
    # the eye and the run time give way to the ring and the time left while in progress (films and episodes)
    row = re.sub(r'<control type="group"><visible>[^<]*</visible><include content="Aeon_(?:WatchMark|Dur)"><param name="left">(?:544|556|584|596)</param>.*?</control>',
                 lambda m: add_vis(m.group(0), '!%s' % PROG), row)
    film = '![[Container.Content(episodes) | Container.Content(musicvideos)] | Container.Content(seasons)] + !Container.Content(tvshows)'
    ep = '[Container.Content(episodes) | Container.Content(musicvideos)]'
    foc = '[$PARAM[focused] + Control.HasFocus($PARAM[id]) + !$EXP[Aeon_VGlass]]'
    new = '\t\t\t<!-- %s: in progress, the ring in the mark column and the time left in the run-time column, yellow -->\n' % MARK
    for which, mx, dx in ((film, 544, 584), (ep, 556, 596)):
        for f, col in (('!' + foc, 'fg_mark'), (foc, '$VAR[Aeon_OnBarInk3_L]')):
            vis = '%s + %s + %s' % (PROG, which, f)
            new += ('\t\t\t<control type="image"><left>%d</left><top>17</top><width>28</width><height>28</height><texture colordiffuse="%s">fg/pring/$INFO[ListItem.PercentPlayed].png</texture><visible>%s</visible></control>\n'
                    '\t\t\t<control type="label"><left>%d</left><top>0</top><width>60</width><height>62</height><align>center</align><aligny>center</aligny><font>lb_small_20_bold</font>'
                    '<textcolor>%s</textcolor><selectedcolor>%s</selectedcolor><label>$VAR[Aeon_RowLeft]</label><visible>%s</visible></control>\n'
                    % (mx, col, vis, dx, col, col, vis))
    d = row.rindex('\t\t</definition>')
    row = row[:d] + new + row[d:]
    v = v[:a] + row + v[b:]

    # ---------------------------------------------------------------- the band
    a = v.index('<include name="Aeon_V_Bar">')
    b = v.index('\t</include>', a)
    bar = v[a:b]
    g1 = bar.index('<control type="grouplist"><left>96</left><top>984</top>')
    g1e = bar.index('\t\t\t</control>', g1)
    facts = bar[g1:g1e]
    plain = ('<control type="label"><width min="10" max="300">auto</width><height>34</height><aligny>center</aligny><font>lb_ui_24_bold</font>'
             '<textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><label>%s</label><visible>%s</visible></control>\n')
    fb = facts.index('<control type="button">')
    facts = facts[:fb] + plain % ('$INFO[ListItem.Year]', '!String.IsEmpty(ListItem.Year)') + facts[fb:]
    facts += plain % ('[UPPERCASE]$LOCALIZE[31030] $INFO[ListItem.EndTimeResume][/UPPERCASE]', '!String.IsEmpty(ListItem.EndTimeResume)')
    bar = bar[:g1] + facts + bar[g1e:]
    g2 = bar.index('<control type="grouplist"><left>96</left><top>1030</top>')
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
    status = ('<control type="image"><width>34</width><height>34</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">common/aeon_eye_off.png</texture><visible>$EXP[Aeon_LV_Dot]</visible></control>\n'
              '<control type="image"><width>34</width><height>34</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">common/aeon_eye.png</texture><visible>$EXP[Aeon_LV_Tick]</visible></control>\n'
              '<control type="image"><width>30</width><height>34</height><aspectratio>keep</aspectratio><texture colordiffuse="fg_mark">fg/pring/$INFO[ListItem.PercentPlayed].png</texture><visible>$EXP[Aeon_LV_Ring]</visible></control>\n'
              '<control type="label"><width min="10" max="400">auto</width><height>34</height><aligny>center</aligny><font>lb_small_20_bold</font><textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><label>[UPPERCASE]$VAR[Aeon_LV_Status][/UPPERCASE]</label><visible>!$EXP[Aeon_LV_Ring]</visible></control>\n'
              '<control type="label"><width min="10" max="400">auto</width><height>34</height><aligny>center</aligny><font>lb_small_20_bold</font><textcolor>fg_mark</textcolor><selectedcolor>fg_mark</selectedcolor><label>[UPPERCASE]$VAR[Aeon_LV_Status][/UPPERCASE]</label><visible>$EXP[Aeon_LV_Ring]</visible></control>\n'
              '<control type="label"><width>6</width><height>34</height><label></label></control>\n')
    bar = bar[:g2] + head + '\n' + status + '\n'.join(keep) + '\n' + bar[g2e:]
    SO = 'String.IsEqual(Window(Home).Property(aeon.studio.of),ListItem.Studio)'
    studio = ('\t\t\t<!-- %s: the studio: the pack\'s logo, else its name -->\n'
              '\t\t\t<control type="image"><left>1040</left><top>996</top><width>260</width><height>60</height><aspectratio align="right" aligny="center">keep</aspectratio>'
              '<texture background="true">resource://resource.images.studios.white/$INFO[Window(Home).Property(aeon.studio)].png</texture>'
              '<visible>!Skin.HasSetting(aeon.nostudio) + !String.IsEmpty(Window(Home).Property(aeon.studio)) + %s</visible></control>\n'
              '\t\t\t<control type="label"><left>700</left><top>984</top><width>600</width><height>84</height><align>right</align><aligny>center</aligny><font>lb_small_20_bold</font>'
              '<textcolor>d9ffffff</textcolor><label>[UPPERCASE]$INFO[Window(Home).Property(aeon.studio.text)][/UPPERCASE]</label>'
              '<visible>!Skin.HasSetting(aeon.nostudio) + String.IsEmpty(Window(Home).Property(aeon.studio)) + !String.IsEmpty(Window(Home).Property(aeon.studio.text)) + %s</visible></control>\n'
              % (MARK, SO, SO))
    d = bar.rindex('\t\t</definition>')
    bar = bar[:d] + studio + bar[d:]
    v = v[:a] + bar + v[b:]
    assert v.count('</includes>') == 1
    v = v.replace('</includes>', '\t<!-- %s: the status of the focused item of any list (from Fused Glass\'s FG_L510_*) -->\n' % MARK + status_defs() + '</includes>')
    io.open(V2, 'w', encoding='utf-8', newline='\n').write(v)
    ET.parse(V2)
    print('ok')


if __name__ == '__main__':
    main()
