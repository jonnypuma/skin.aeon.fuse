# -*- coding: utf-8 -*-
"""0.56.20 the Fuse menu theme survey, part 2 (after fuse_survey_05620.py), with the user's comments on the board:
- 11 file manager (Aeon + Fuse): "the black strip is not rounded" - the strip between the panes is a pill (r20 = w / 2)
  with the Fuse menu theme; the Aeon menu styles keep the square strip;
- 12 Browse for folder / Choose art's image picker: the list was 640 high for 68 px rows (9.4 rows, the last cut in half)
  and an empty band followed: 9 whole rows (612), the rule and the path under them, the card 40 shorter;
- 13 select dialogs: the card follows the number of rows (4 to 9 rows; a longer list scrolls in 9) and stays centred;
- 14 Kodi's Settings hub: Aeon Glass with the Fuse menu theme takes the Fuse hub like Aeon (it kept Aeon Glass's column);
- 15 Interface (settings categories) and add-on settings: "we don't need the empty strip here unless we have mockup
  previews" - the settings list reaches the card's right edge (the empty third column is gone); "for Aeon Glass an ugly
  line between Skin, regional etc box and the Look and feel box" - the two cards are one card, the square frame lines
  are gone from these rounded pages;
- 9 / 10 Aeon Glass legibility: the event log and system info get one card under the side menu and the content (no
  panel behind the menu before, and no seam between cards); the file manager panes, favourites, profiles, the review
  viewer (text viewer) and those two pages use a denser glass (AG_CardDense: a dark r28 layer in Aeon Glass only);
- 8 colour picker: rounded swatches (12 px) with the Fuse menu theme and in Aeon Glass.
Runs once (marker)."""
import io
import os
import re
import xml.etree.ElementTree as ET

D = '1080i'
MARK = '0.56.20 fuse_survey2'
FUSED = '$EXP[Aeon_Fused]'
VG = '$EXP[Aeon_VGlass] + !$EXP[Aeon_FGlass]'


def rd(f):
    return io.open(os.path.join(D, f), encoding='utf-8').read()


def swap(t, old, new, count=1):
    n = t.count(old)
    assert n == count, (old[:160], n, count)
    return t.replace(old, new)


def block(t, start, end='\n\t</include>'):
    a = t.index(start)
    return a, t.index(end, a)


def main():
    F = {f: rd(f) for f in os.listdir(D) if f.endswith('.xml')}
    if any(MARK in t for t in F.values()):
        print('already')
        return
    # ---- dense card (Aeon Glass): AG_CardDense, and AG_GenericDialog's "dense" / "card_visible" params
    c = F['Includes_Common.xml']
    c = swap(c, '\t<!-- AG_Card_L: the library windows\' copy of AG_Card',
             '\t<!-- %s: AG_Card with a dark layer in Aeon Glass, for pages of lists and long text over fanart -->\n'
             '\t<include name="AG_CardDense">\n\t\t<definition>\n\t\t\t<include>Aeon_Glass</include>\n'
             '\t\t\t<control type="image"><left>0</left><top>0</top><right>0</right><bottom>0</bottom><texture border="28" colordiffuse="a60c0c10">fg/r28.png</texture><visible>%s</visible></control>\n'
             '\t\t</definition>\n\t</include>\n\t<!-- AG_Card_L: the library windows\' copy of AG_Card' % (MARK, VG))
    F['Includes_Common.xml'] = c
    d = F['Includes_Dialogs.xml']
    a, b = block(d, '<include name="AG_GenericDialog">', '</definition>')
    s = d[a:b]
    s = swap(s, '\t\t<param name="kicker"></param>\n', '\t\t<param name="kicker"></param>\n\t\t<param name="dense">false</param>\n\t\t<param name="card_visible">true</param>\n')
    s = swap(s, '\t\t\t\t<include>AG_Card</include>\n\t\t\t</control>',
             '\t\t\t\t<include>AG_Card</include>\n'
             '\t\t\t\t<control type="image"><left>0</left><top>0</top><right>0</right><bottom>0</bottom><texture border="28" colordiffuse="a60c0c10">fg/r28.png</texture><visible>$PARAM[dense] + %s</visible></control><!-- %s -->\n'
             '\t\t\t\t<visible>$PARAM[card_visible]</visible>\n\t\t\t</control>' % (VG, MARK))
    d = d[:a] + s + d[b:]
    # ---- 13 select: the card follows the rows (list 3); the dialog stays centred
    a, b = block(d, '<include name="Dlg_SelectCentred">')
    s = d[a:b]
    s = swap(s, '\t\t\t\t<param name="kicker" value="$VAR[Dlg_SelectPosition]"/>\n\t\t\t</include>',
             '\t\t\t\t<param name="kicker" value="$VAR[Dlg_SelectPosition]"/>\n\t\t\t\t<param name="card_visible" value="!Control.IsVisible(3) | Integer.IsGreater(Container(3).NumItems,8)"/>\n\t\t\t</include>\n' + cards())
    s = swap(s, '\t\t\t<width>1120</width>\n\t\t\t<height>800</height>\n', '\t\t\t<width>1120</width>\n\t\t\t<height>800</height>\n' + slides(), 1)
    d = d[:a] + s + d[b:]
    F['Includes_Dialogs.xml'] = d
    # ---- 12 Browse / Choose art's image picker: 9 whole rows
    fb = F['FileBrowser.xml']
    fb = swap(fb, '\t\t\t<height>860</height>\n\t\t\t<include content="AG_GenericDialog">\n\t\t\t\t<param name="width" value="1400"/>\n\t\t\t\t<param name="height" value="860"/>',
              '\t\t\t<height>820</height><!-- %s: 9 whole rows of 68 (612), the rule and path under them -->\n\t\t\t<include content="AG_GenericDialog">\n\t\t\t\t<param name="width" value="1400"/>\n\t\t\t\t<param name="height" value="820"/>' % MARK)
    fb = swap(fb, '\t\t\t\t<width>1000</width>\n\t\t\t\t<height>640</height>', '\t\t\t\t<width>1000</width>\n\t\t\t\t<height>612</height>')
    fb = swap(fb, '<param name="height" value="640"/>', '<param name="height" value="612"/>')
    fb = swap(fb, '<param name="top" value="784"/>', '<param name="top" value="744"/>')
    fb = swap(fb, '\t\t\t\t<top>796</top>', '\t\t\t\t<top>756</top>')
    F['FileBrowser.xml'] = fb
    # ---- 11 the file manager's strip: a pill with Fuse
    m = F['Includes_Misc.xml']
    m = swap(m, '\t\t\t\t<texture colordiffuse="ff000000">common/white.png</texture>\n\t\t\t</control>\n\t\t\t<control type="image">\n\t\t\t\t<left>930</left>',
             '\t\t\t\t<texture colordiffuse="ff000000">common/white.png</texture>\n\t\t\t\t<visible>!%s</visible>\n\t\t\t</control>\n'
             '\t\t\t<!-- %s: "the black strip is not rounded": a pill with the Fuse menu theme -->\n'
             '\t\t\t<control type="image"><left>940</left><top>108</top><width>40</width><height>908</height><texture border="20" colordiffuse="ff000000">fg/r20.png</texture><visible>%s</visible></control>\n'
             '\t\t\t<control type="image">\n\t\t\t\t<left>930</left>' % (FUSED, MARK, FUSED))
    # ---- 10 dense cards: file manager panes, favourites (Misc_MediaWindow)
    for name in ('<include name="FM_Side">', '<include name="Misc_MediaWindow">'):
        a, b = block(m, name, '</definition>')
        s = m[a:b]
        n = s.count('<include>AG_Card</include>')
        assert n >= 1, (name, n)
        m = m[:a] + s.replace('<include>AG_Card</include>', '<include>AG_CardDense</include>') + m[b:]
    F['Includes_Misc.xml'] = m
    F['SettingsProfile.xml'] = F['SettingsProfile.xml'].replace('<include>AG_Card</include>', '<include>AG_CardDense</include>')
    tv = F['DialogTextViewer.xml']
    tv = re.sub(r'(<include content="AG_GenericDialog">)', r'\1\n\t\t\t\t<param name="dense" value="true"/><!-- %s -->' % MARK, tv, count=1)
    F['DialogTextViewer.xml'] = tv
    # ---- 9 event log / system info in Aeon Glass: one dense card under the menu and the content
    ev = F['EventLog.xml']
    ev = swap(ev, '\t\t\t<include>AG_Card</include>\n\t\t\t<visible>[$EXP[Aeon_VGlass] | $EXP[Aeon_Fused]] + !$EXP[Aeon_FGlass]</visible>\n\t\t</control>',
              '\t\t\t<include>AG_Card</include>\n\t\t\t<visible>$EXP[Aeon_Fused] + !$EXP[Aeon_VGlass]</visible>\n\t\t</control>\n'
              '\t\t<!-- %s: Aeon Glass: one dense card under the menu and the events (the menu had no panel over the fanart) -->\n'
              '\t\t<control type="group"><left>100</left><top>content_top</top><width>1700</width><height>848</height><include>AG_CardDense</include><visible>%s</visible></control>' % (MARK, VG))
    F['EventLog.xml'] = ev
    si = F['SettingsSystemInfo.xml']
    si = swap(si, '\t\t<!-- ====== cards -->\n\t\t<control type="group">\n\t\t\t<left>540</left>',
              '\t\t<!-- ====== cards -->\n'
              '\t\t<!-- %s: Aeon Glass: one dense card under the sections, the facts and the meters (no seams, the menu on a panel) -->\n'
              '\t\t<control type="group"><left>100</left><top>content_top</top><width>1700</width><height>848</height><include>AG_CardDense</include><visible>%s</visible></control>\n'
              '\t\t<control type="group">\n\t\t\t<visible>!$EXP[Aeon_VGlass] | $EXP[Aeon_FGlass]</visible>\n\t\t\t<left>540</left>' % (MARK, VG))
    si = swap(si, '\t\t<control type="group">\n\t\t\t<left>1380</left>', '\t\t<control type="group">\n\t\t\t<visible>!$EXP[Aeon_VGlass] | $EXP[Aeon_FGlass]</visible>\n\t\t\t<left>1380</left>')
    F['SettingsSystemInfo.xml'] = si
    # ---- 14 Settings hub: Aeon Glass + Fuse takes the Fuse hub
    st = F['Settings.xml']
    st = swap(st, '<onload condition="Skin.HasSetting(aeon.vglass)">SetFocus(9001)</onload>', '<onload condition="Skin.HasSetting(aeon.vglass) + !%s">SetFocus(9001)</onload>' % FUSED)
    st = swap(st, '\t\t\t<visible>Skin.HasSetting(aeon.vglass)</visible>\n\t\t\t<include content="Aeon_MenuHeader2">',
              '\t\t\t<visible>Skin.HasSetting(aeon.vglass) + !%s</visible><!-- %s: Aeon Glass + Fuse takes the Fuse hub -->\n\t\t\t<include content="Aeon_MenuHeader2">' % (FUSED, MARK))
    F['Settings.xml'] = st
    am = F['Includes_Aeon_Menu.xml']
    a, b = block(am, '<include name="Hub_Classic">')
    s = swap(am[a:b], '\t\t<visible>!Skin.HasSetting(aeon.vglass)</visible>', '\t\t<visible>!Skin.HasSetting(aeon.vglass) | %s</visible>' % FUSED)
    am = am[:a] + s + am[b:]
    # ---- 15 settings categories + add-on settings: one card, no square frame lines on rounded pages, no empty strip
    for name in ('<include name="SetCat_Classic">', '<include name="AddonSet_Classic">'):
        a, b = block(am, name)
        s = am[a:b]
        s = s.replace('<visible>!$EXP[Aeon_Fused]</visible>', '<visible>!$EXP[Aeon_Fused] + !$EXP[Aeon_VGlass]</visible>')
        if 'SetCat' in name:
            s = swap(s, '\t\t\t\t<left>481</left>\n\t\t\t\t<top>181</top>\n\t\t\t\t<width>1058</width>', '\t\t\t\t<left>481</left>\n\t\t\t\t<top>181</top>\n\t\t\t\t<width>1296</width><!-- %s: to the card\'s edge (the empty third column is gone) -->' % MARK)
            s = swap(s, '<param name="width" value="1058"/>', '<param name="width" value="1296"/>')
            s = swap(s, '<param name="left" value="1540"/>', '<param name="left" value="1790"/>')
        am = am[:a] + s + am[b:]
    F['Includes_Aeon_Menu.xml'] = am
    for f in ('SettingsCategory.xml', 'DialogAddonSettings.xml'):
        t = F[f]
        old = ('<control type="group"><left>100</left><top>180</top><width>380</width><height>684</height><visible>!$EXP[Aeon_FGlass] + !$EXP[Aeon_MS]</visible><include>Aeon_Glass</include></control>\n'
               '\t\t<control type="group"><left>480</left><top>180</top><width>1340</width><height>684</height><visible>!$EXP[Aeon_FGlass] + !$EXP[Aeon_MS]</visible><include>Aeon_Glass</include></control>')
        t = swap(t, old, '<!-- %s: one card for the categories and the settings (two cards met in a line) -->\n'
                         '\t\t<control type="group"><left>100</left><top>180</top><width>1720</width><height>684</height><visible>!$EXP[Aeon_FGlass] + !$EXP[Aeon_MS]</visible><include>Aeon_Glass</include></control>' % MARK)
        F[f] = t
    # ---- 8 colour picker: rounded swatches with Fuse and in Aeon Glass
    cp = F['DialogColorPicker.xml']
    rnd = '[%s | Skin.HasSetting(aeon.vglass)] + !Skin.HasSetting(aeon.fglass)' % FUSED
    for w, h in (('126', '64'),):
        cp = cp.replace('<texture colordiffuse="0dffffff">common/white.png</texture>',
                        '<texture colordiffuse="0dffffff">common/white.png</texture><visible>![%s]</visible>' % rnd)
        cp = cp.replace('<texture>common/white.png</texture>\n',
                        '<texture>common/white.png</texture><visible>![%s]</visible>\n' % rnd)
    # the rounded copies: after each square swatch pair
    cp = re.sub(r'(\t*)(<control type="image">\s*<left>(\d+)</left>\s*<top>(\d+)</top>\s*<width>126</width>\s*<height>64</height>\s*<texture>common/white.png</texture><visible>[^<]*</visible>\s*<colordiffuse>\$INFO\[ListItem.Label2\]</colordiffuse>\s*</control>)',
                lambda mm: mm.group(1) + mm.group(2) + '\n' + mm.group(1) +
                '<control type="image"><left>%s</left><top>%s</top><width>126</width><height>64</height><texture border="12" colordiffuse="0dffffff">fg/r12.png</texture><visible>%s</visible></control>\n' % (mm.group(3), mm.group(4), rnd) + mm.group(1) +
                '<control type="image"><left>%s</left><top>%s</top><width>126</width><height>64</height><texture border="12">fg/r12.png</texture><colordiffuse>$INFO[ListItem.Label2]</colordiffuse><visible>%s</visible></control><!-- %s -->' % (mm.group(3), mm.group(4), rnd, MARK), cp)
    assert cp.count(MARK) == 2, cp.count(MARK)
    F['DialogColorPicker.xml'] = cp
    changed = 0
    for k, t in F.items():
        if t != rd(k):
            io.open(os.path.join(D, k), 'w', encoding='utf-8', newline='\n').write(t)
            ET.parse(os.path.join(D, k))
            changed += 1
    print('files changed', changed)


def cards():
    out = '\t\t\t<!-- %s: the card follows the rows (4 to 8; 9 and more: the 800 card) -->\n' % MARK
    for n in range(4, 9):
        h = 112 + n * 68 + 76
        cond = '!Integer.IsGreater(Container(3).NumItems,4)' if n == 4 else 'Integer.IsEqual(Container(3).NumItems,%d)' % n
        out += ('\t\t\t<control type="group"><left>0</left><top>0</top><width>1120</width><height>%d</height>'
                '<animation effect="fade" start="0" end="100" time="200">WindowOpen</animation><animation effect="fade" start="100" end="0" time="150">WindowClose</animation>'
                '<include>AG_Card</include><visible>Control.IsVisible(3) + %s</visible></control>\n' % (h, cond))
    return out


def slides():
    out = ''
    for n in range(4, 9):
        h = 112 + n * 68 + 76
        cond = '!Integer.IsGreater(Container(3).NumItems,4)' if n == 4 else 'Integer.IsEqual(Container(3).NumItems,%d)' % n
        out += '\t\t\t<animation effect="slide" end="0,%d" time="0" condition="Control.IsVisible(3) + %s">Conditional</animation>\n' % ((800 - h) // 2, cond)
    return out


if __name__ == '__main__':
    main()
