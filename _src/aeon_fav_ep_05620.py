# -*- coding: utf-8 -*-
"""0.56.20 the user (2026-11-17): "Aeon theme: Favorites submenu, shows an episode from Rings of Power but it shows tv
show landscape. In Fused Glass I believe it shows the episode thumb and progress status in the spotlight? We should
have parity with Fused Glass."

Aeon / Aeon Glass Home > Favourites (Aeon_H_Favourites_Classic, written by _src/fg_fav.py - run this after it): the
helper already gives each show / episode favourite aeon.fav.ep ("Continue S3 E2 - The Gift of Men"), aeon.fav.left,
aeon.fav.started, aeon.fav.next and aeon.fav.epthumb (plugin.py favourites), which Fused Glass shows. Now Aeon too:
- the card shows the episode's thumb when the favourite has one (else the landscape / fanart as before) and a
  progress line along its foot once the episode is started;
- the spotlight under the plot: the episode line, the time left on the right, a progress bar, the next episode.
Runs once (marker)."""
import io
import os
import xml.etree.ElementTree as ET

P = os.path.join('1080i', 'Includes_Fused.xml')
MARK = '0.56.20 aeon_fav_ep'
L = 'Container(9309).ListItem'


def swap(t, old, new, count=1):
    n = t.count(old)
    assert n == count, (old[:140], n, count)
    return t.replace(old, new)


def main():
    t = io.open(P, encoding='utf-8').read()
    if MARK in t:
        print('already')
        return
    t = swap(t, '\t<variable name="Aeon_FavArtL">\n\t\t<value condition="!String.IsEmpty(ListItem.Art(landscape))">',
             '\t<!-- %s: an episode favourite shows its episode (the helper\'s aeon.fav.epthumb), as in Fused Glass -->\n'
             '\t<variable name="Aeon_FavArtL">\n\t\t<value condition="!String.IsEmpty(ListItem.Property(aeon.fav.epthumb))">$INFO[ListItem.Property(aeon.fav.epthumb)]</value>\n'
             '\t\t<value condition="!String.IsEmpty(ListItem.Art(landscape))">' % MARK)
    a = t.index('<include name="Aeon_H_Favourites_Classic">')
    b = t.index('\n\t</include>', a)
    s = t[a:b]
    # the card: the episode thumb counts as wide art; a progress line once started
    old_vis = '<visible>!String.IsEmpty(ListItem.Art(fanart)) | !String.IsEmpty(ListItem.Art(landscape))</visible>'
    assert s.count(old_vis) == 2, s.count(old_vis)
    s = s.replace(old_vis, '<visible>!String.IsEmpty(ListItem.Art(fanart)) | !String.IsEmpty(ListItem.Art(landscape)) | !String.IsEmpty(ListItem.Property(aeon.fav.epthumb))</visible>')
    old_k = '<visible>String.IsEmpty(ListItem.Art(fanart)) + String.IsEmpty(ListItem.Art(landscape))</visible>'
    assert s.count(old_k) == 2, s.count(old_k)
    s = s.replace(old_k, '<visible>String.IsEmpty(ListItem.Art(fanart)) + String.IsEmpty(ListItem.Art(landscape)) + String.IsEmpty(ListItem.Property(aeon.fav.epthumb))</visible>')
    bar = ('<control type="progress"><left>16</left><top>166</top><width>280</width><height>6</height>'
           '<texturebg colordiffuse="66000000">common/white.png</texturebg><midtexture colordiffuse="$VAR[Aeon_Accent]">common/white.png</midtexture>'
           '<info>ListItem.PercentPlayed</info><visible>!String.IsEmpty(ListItem.Property(aeon.fav.started))</visible></control>')
    for lay in ('\t\t\t\t\t\t<control type="label"><left>16</left><top>182</top><width>280</width><height>24</height><font>hm_cap_16</font><textcolor>99ffffff</textcolor>',
                '\t\t\t\t\t\t<control type="label"><left>16</left><top>182</top><width>280</width><height>24</height><font>hm_cap_16</font><textcolor>b3ffffff</textcolor>'):
        s = swap(s, lay, '\t\t\t\t\t\t' + bar + '<!-- %s -->\n' % MARK + lay)
    # the spotlight: episode, time left, a bar, the next episode
    plot = '\t\t\t\t<control type="textbox"><left>120</left><top>336</top><width>820</width><height>150</height><font>hm_body_24</font><textcolor>ccffffff</textcolor><label>$INFO[Container(9309).ListItem.Plot]</label></control>\n'
    ep = ('\t\t\t\t\t<!-- %s: the episode of a show favourite, as in Fused Glass -->\n'
          '\t\t\t\t\t<control type="group"><left>120</left><top>500</top><visible>!String.IsEmpty(%s.Property(aeon.fav.ep))</visible>\n'
          '\t\t\t\t\t\t<control type="label"><left>0</left><top>0</top><width>820</width><height>40</height><aligny>center</aligny><font>hm_ui_24_bold</font><textcolor>ffffffff</textcolor><label>[UPPERCASE]$INFO[%s.Property(aeon.fav.ep)][/UPPERCASE]</label></control>\n'
          '\t\t\t\t\t\t<control type="label"><left>520</left><top>0</top><width>300</width><height>40</height><align>right</align><aligny>center</aligny><font>hm_ui_24_bold</font><textcolor>ffffffff</textcolor><label>[UPPERCASE]$INFO[%s.Property(aeon.fav.left)][/UPPERCASE]</label><visible>!String.IsEmpty(%s.Property(aeon.fav.started))</visible></control>\n'
          '\t\t\t\t\t\t<control type="progress"><left>0</left><top>48</top><width>820</width><height>6</height><texturebg colordiffuse="33ffffff">common/white.png</texturebg><midtexture colordiffuse="$VAR[Aeon_Accent]">common/white.png</midtexture><info>%s.PercentPlayed</info><visible>!String.IsEmpty(%s.Property(aeon.fav.started))</visible></control>\n'
          '\t\t\t\t\t\t<control type="label"><left>0</left><top>64</top><width>820</width><height>34</height><aligny>center</aligny><font>hm_ui_22</font><textcolor>b3ffffff</textcolor><label>$INFO[%s.Property(aeon.fav.next)]</label></control>\n'
          '\t\t\t\t\t</control>\n' % (MARK, L, L, L, L, L, L, L))
    s = swap(s, plot, plot + ep)
    t = t[:a] + s + t[b:]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(P)
    print('ok')


if __name__ == '__main__':
    main()
