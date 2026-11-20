# -*- coding: utf-8 -*-
"""0.56.14 the Aeon theme's wall views' info strip (Aeon_V_Info: Poster wall 520, Landscape 521, Square 525, Cards 526,
Showcase 523) to the info panel rule, as the Poster wall board on canvas HJTtCDChVWkaZZAyt76wJA draws it:
  kicker (FILM · genres / TV SHOW · genres / SEASON · show / MOVIE SET / Season 3 · Episode 1) with the studio's logo
  (else its name) on the right, no taller than the clock dock;
  the title;
  facts: ratings, year, certificate, run time, ENDS, then the status (eye, or the yellow ring and the time left);
  chips: one audio chip, aspect, HDR with the profile (no SDR), the resolution last;
  the plot.
The genres move from a chip to the kicker; the date chip becomes the year.
Run from the skin folder after aeon_lib522.py; runs once."""
import io
import os
import re
import xml.etree.ElementTree as ET

V2 = os.path.join('1080i', 'Includes_Aeon_Views2.xml')
MARK = '0.56.14 aeon_lib_walls'


def add_vis(xml, extra):
    return re.sub(r'<visible>(.*?)</visible>', lambda m: '<visible>[%s] + %s</visible>' % (m.group(1), extra), xml, count=1)


PLAIN = ('<control type="label"><width min="10" max="300">auto</width><height>34</height><aligny>center</aligny><font>lb_ui_24_bold</font>'
         '<textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><label>%s</label><visible>%s</visible></control>')
STATUS = ('<control type="label"><width>6</width><height>34</height><label></label></control>\n'
          '<control type="image"><width>34</width><height>34</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">common/aeon_eye_off.png</texture><visible>$EXP[Aeon_LV_Dot]</visible></control>\n'
          '<control type="image"><width>34</width><height>34</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">common/aeon_eye.png</texture><visible>$EXP[Aeon_LV_Tick]</visible></control>\n'
          '<control type="image"><width>30</width><height>34</height><aspectratio>keep</aspectratio><texture colordiffuse="fg_mark">fg/pring/$INFO[ListItem.PercentPlayed].png</texture><visible>$EXP[Aeon_LV_Ring]</visible></control>\n'
          '<control type="label"><width min="10" max="500">auto</width><height>34</height><aligny>center</aligny><font>lb_small_20_bold</font><textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><label>[UPPERCASE]$VAR[Aeon_LV_Status][/UPPERCASE]</label><visible>!$EXP[Aeon_LV_Ring]</visible></control>\n'
          '<control type="label"><width min="10" max="500">auto</width><height>34</height><aligny>center</aligny><font>lb_small_20_bold</font><textcolor>fg_mark</textcolor><selectedcolor>fg_mark</selectedcolor><label>[UPPERCASE]$VAR[Aeon_LV_Status][/UPPERCASE]</label><visible>$EXP[Aeon_LV_Ring]</visible></control>')
SO = 'String.IsEqual(Window(Home).Property(aeon.studio.of),ListItem.Studio)'
KICKER = ('\t<!-- %s: the kicker over a wall\'s title -->\n'
          '\t<variable name="Aeon_LV_Kicker">\n'
          '\t\t<value condition="String.IsEqual(ListItem.DBType,episode)">$INFO[ListItem.Season,$LOCALIZE[20373] ,]$INFO[ListItem.Episode,  ·  $LOCALIZE[20359] ,]</value>\n'
          '\t\t<value condition="String.IsEqual(ListItem.DBType,tvshow)">$LOCALIZE[20364]$INFO[ListItem.Genre,  ·  ,]</value>\n'
          '\t\t<value condition="String.IsEqual(ListItem.DBType,season)">$LOCALIZE[20373]$INFO[ListItem.TVShowTitle,  ·  ,]</value>\n'
          '\t\t<value condition="String.IsEqual(ListItem.DBType,set)">$LOCALIZE[20457]</value>\n'
          '\t\t<value condition="String.IsEqual(ListItem.DBType,musicvideo)">$LOCALIZE[20391]$INFO[ListItem.Genre,  ·  ,]</value>\n'
          '\t\t<value>$LOCALIZE[20338]$INFO[ListItem.Genre,  ·  ,]</value>\n'
          '\t</variable>\n' % MARK)


def main():
    v = io.open(V2, encoding='utf-8').read()
    if MARK in v:
        print('already done')
        return
    a = v.index('<include name="Aeon_V_Info">')
    b = v.index('\n\t</include>', a)
    inc = v[a:b]
    lines = inc.split('\n')
    # the title: below the kicker, clear of the studio's logo
    ti = [i for i, l in enumerate(lines) if '<label>[UPPERCASE]$INFO[ListItem.Title]$VAR[Aeon_Ver][/UPPERCASE]</label>' in l]
    assert len(ti) == 1
    t = lines[ti[0]]
    t = t.replace('<left>0</left><top>16</top><width>1680</width><height>56</height>', '<left>0</left><top>36</top><width>1340</width><height>52</height>', 1)
    assert '<top>36</top>' in t
    head = ('\t\t\t\t<control type="label"><left>0</left><top>10</top><width>1320</width><height>28</height><aligny>center</aligny><font>lb_cap_16</font>'
            '<textcolor>a3ffffff</textcolor><selectedcolor>a3ffffff</selectedcolor><label>[UPPERCASE]$VAR[Aeon_LV_Kicker][/UPPERCASE]</label></control>\n'
            '\t\t\t\t<control type="image"><left>1380</left><top>12</top><width>300</width><height>72</height><aspectratio align="right" aligny="center">keep</aspectratio>'
            '<texture background="true">resource://resource.images.studios.white/$INFO[Window(Home).Property(aeon.studio)].png</texture>'
            '<visible>!Skin.HasSetting(aeon.nostudio) + !String.IsEmpty(Window(Home).Property(aeon.studio)) + %s</visible></control>\n'
            '\t\t\t\t<control type="label"><left>1080</left><top>10</top><width>600</width><height>28</height><align>right</align><aligny>center</aligny><font>lb_small_20_bold</font>'
            '<textcolor>d9ffffff</textcolor><selectedcolor>d9ffffff</selectedcolor><label>[UPPERCASE]$INFO[Window(Home).Property(aeon.studio.text)][/UPPERCASE]</label>'
            '<visible>!Skin.HasSetting(aeon.nostudio) + String.IsEmpty(Window(Home).Property(aeon.studio)) + !String.IsEmpty(Window(Home).Property(aeon.studio.text)) + %s</visible></control>\n'
            % (SO, SO))
    lines[ti[0]] = '\t\t\t\t<!-- %s: kicker and studio, title, facts with Ends and the status, chips with the resolution last, plot -->\n' % MARK + head + t
    out = '\n'.join(lines)
    # the facts row
    g1 = out.index('<control type="grouplist"><left>0</left><top>72</top>')
    g1e = out.index('\n</control>', g1)
    items = out[g1:g1e].split('\n')
    gh, items = items[0].replace('<top>72</top>', '<top>90</top>', 1), items[1:]
    rat = [l for l in items if 'ratings/' in l or 'Aeon_R_' in l or 'star.png' in l or 'ListItem.Rating' in l]
    rated = [l for l in items if '$VAR[Aeon_LVRated]' in l]
    dur = [l for l in items if '$VAR[Aeon_LVDur]' in l]
    assert len(rat) == 10 and len(rated) == 2 and len(dur) == 2, (len(rat), len(rated), len(dur))
    facts = rat + [PLAIN % ('$INFO[ListItem.Year]', '!String.IsEmpty(ListItem.Year)')] + rated + dur + \
        [PLAIN % ('[UPPERCASE]$LOCALIZE[31030] $INFO[ListItem.EndTimeResume][/UPPERCASE]', '!String.IsEmpty(ListItem.EndTimeResume)'), STATUS]
    out = out[:g1] + gh + '\n' + '\n'.join(facts) + out[g1e:]
    # the chips row
    g2 = out.index('<control type="grouplist"><left>0</left><top>116</top>')
    g2e = out.index('\n</control>', g2)
    items = out[g2:g2e].split('\n')
    gh, items = items[0].replace('<top>116</top>', '<top>132</top>', 1), items[1:]
    keep = []
    for l in items:
        if '$VAR[Aeon_LVCh]' in l or 'Property(aeon.dvp)' in l:
            continue
        l = l.replace('$VAR[Aeon_LVAud]', '[UPPERCASE]$VAR[FG_EcAudio][/UPPERCASE]').replace('$VAR[Aeon_LVHdr]', '$VAR[FG_L_HdrChip]')
        if '$VAR[FG_L_HdrChip]' in l:
            l = add_vis(l, '!String.IsEmpty(ListItem.HdrType)')
        keep.append(l)

    def key(l):
        for i, k in enumerate(('FG_EcAudio', 'Aeon_LVAsp', 'FG_L_HdrChip', 'Aeon_LVRes')):
            if k in l:
                return i
        return 9
    keep.sort(key=key)
    assert len(keep) == 8, len(keep)
    out = out[:g2] + gh + '\n' + '\n'.join(keep) + out[g2e:]
    # the plot
    for old, new in (('<left>0</left><top>162</top><width>1680</width><height>72</height>', '<left>0</left><top>176</top><width>1680</width><height>70</height>'),
                     ('<left>0</left><top>116</top><width>1680</width><height>110</height>', '<left>0</left><top>132</top><width>1680</width><height>110</height>')):
        assert out.count(old) == 1, old
        out = out.replace(old, new)
    v = v[:a] + out + v[b:]
    # Cards: the strip 10 px higher, so the plot's second line clears the screen's edge
    old = '<include content="Aeon_V_Info"><param name="top">840</param></include>'
    assert v.count(old) == 1
    v = v.replace(old, old.replace('840', '830'))
    assert v.count('</includes>') == 1
    v = v.replace('</includes>', KICKER + '</includes>')
    io.open(V2, 'w', encoding='utf-8', newline='\n').write(v)
    ET.parse(V2)
    print('ok')


if __name__ == '__main__':
    main()
