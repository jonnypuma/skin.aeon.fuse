# -*- coding: utf-8 -*-
"""0.56.17 the user's fourth round of notes on the Aeon library views (canvas HJTtCDChVWkaZZAyt76wJA, board Built05616):
- Compact list (524), films and shows: "poster shall have same height as landscape art" (poster 186 x 280 beside the
  landscape 498 x 280, the two filling the 700 px column; the version / set pane in the poster's place scaled with it)
  and "Move studio logo to the bottom left. can make it a bit bigger too then" (the studio / network logo under the
  plot at the column's bottom left, 400 x 90 instead of 454 x 70 on the right; the title, credits and plot move up
  into the room the shorter art leaves);
- Poster wall (520) strip, shared by the walls with Aeon_V_Info: "You can make studio logo a bit bigger" (380 x 92,
  was 300 x 72);
- music Compact list (513): "what are these circles for? ... maybe not needed in this music view and then you can move
  the album labels to the left and get more space for long names" (the album / artist rows lose the ring and the note,
  their names start where the icon was and run 96 px wider; songs keep their track numbers; the header row follows).
Run from the skin folder after aeon_lib_round3.py; each file once."""
import io
import os
import re
import xml.etree.ElementTree as ET

V2 = os.path.join('1080i', 'Includes_Aeon_Views2.xml')
ML = os.path.join('1080i', 'Includes_Aeon_MusicLib.xml')
MARK = '0.56.17 aeon_lib_round4'
SONG = 'String.IsEqual(ListItem.DBType,song)'


def swap(text, old, new, count=1):
    n = text.count(old)
    assert n == count, (old[:100], n, count)
    return text.replace(old, new)


def section(text, start, end):
    a = text.index(start)
    b = text.index(end, a)
    return a, b


def v2_part(v):
    if MARK in v:
        return v, False
    a, b = section(v, '<include name="Aeon_V524_ViewAeon">', '\n\t</include>')
    s = v[a:b]
    # ---- the art: poster and landscape both 280 tall across the 700 px column (186 + 16 + 498)
    s = swap(s, '<left>980</left><top>38</top><width>470</width><height>585</height>', '<left>980</left><top>38</top><width>426</width><height>520</height>')
    s = swap(s, '<left>1226</left><top>38</top><width>694</width><height>495</height>', '<left>1182</left><top>38</top><width>738</width><height>520</height>')
    s = swap(s, '<left>1100</left><top>128</top><width>230</width><height>345</height>', '<left>1100</left><top>128</top><width>186</width><height>280</height>', 2)
    s = swap(s, '<left>1346</left><top>128</top><width>454</width><height>255</height>', '<left>1302</left><top>128</top><width>498</width><height>280</height>', 3)
    s = swap(s, 'diffuse="fg/m647x409.png">$VAR[Aeon_V_Land]', 'diffuse="fg/m500x281.png">$VAR[Aeon_V_Land]')
    s = swap(s, '<left>0</left><top>249</top><width>454</width><height>6</height>', '<left>0</left><top>274</top><width>498</width><height>6</height>', 2)
    s = swap(s, '<control type="group"><left>1270</left><top>136</top>', '<control type="group"><left>1226</left><top>136</top>')
    # ---- the studio / network logo: bottom left of the column, under the plot, larger
    s = swap(s, '<!-- 0.56.15 aeon_lib_round2: the network logo under the picture, on the right;',
             '<!-- %s: the poster as tall as the landscape art; the studio / network logo at the bottom left, under the plot -->\n'
             '\t\t\t<!-- 0.56.15 aeon_lib_round2: the network logo under the picture, on the right;' % MARK)
    s = swap(s, '<left>1346</left><top>395</top><width>454</width><height>70</height><aspectratio align="right" aligny="center">keep</aspectratio>',
             '<left>1100</left><top>866</top><width>400</width><height>90</height><aspectratio align="left" aligny="bottom">keep</aspectratio>')
    s = swap(s, '<left>1346</left><top>395</top><width>454</width><height>70</height><align>right</align><aligny>center</aligny>',
             '<left>1100</left><top>866</top><width>700</width><height>90</height><align>left</align><aligny>bottom</aligny>')
    # ---- title, credits, tagline and plot move up into the room the shorter art leaves (the plot ends above the logo)
    s = swap(s, '<left>1100</left><top>492</top><width>700</width>', '<left>1100</left><top>428</top><width>700</width>', 3)
    s = swap(s, '<left>1100</left><top>540</top><width>700</width>', '<left>1100</left><top>476</top><width>700</width>', 3)
    s = swap(s, '<left>1100</left><top>580</top><width>700</width>', '<left>1100</left><top>516</top><width>700</width>', 3)
    s = swap(s, '<left>1100</left><top>620</top><width>700</width><height>333</height>', '<left>1100</left><top>556</top><width>700</width><height>300</height>', 3)
    # ---- the version / set pane in the poster's place, scaled with it (230 x 345 -> 186 x 280)
    p = s.index('<!-- versions / set members')
    pane = s[p:]
    for old, new in (
            ('<width>230</width><height>345</height>', '<width>186</width><height>280</height>'),
            ('<itemlayout width="230" height="345">', '<itemlayout width="186" height="280">'),
            ('<focusedlayout width="230" height="345">', '<focusedlayout width="186" height="280">'),
            ('<left>14</left><top>59</top><width>206</width><height>101</height><align>center</align><aligny>bottom</aligny><font>lb_ui_26_semibold</font>',
             '<left>8</left><top>40</top><width>170</width><height>90</height><align>center</align><aligny>bottom</aligny><font>lb_ui_22_semibold</font>'),
            ('<left>8</left><top>167</top><width>216</width><height>36</height>', '<left>6</left><top>136</top><width>174</width><height>30</height>'),
            ('<left>75</left><top>216</top><width>80</width><height>80</height>', '<left>61</left><top>174</top><width>64</width><height>64</height>'),
            ('<left>100</left><top>242</top><width>32</width><height>32</height>', '<left>80</left><top>193</top><width>26</width><height>26</height>'),
            ('<left>0</left><top>310</top><width>230</width><height>30</height>', '<left>0</left><top>248</top><width>186</width><height>28</height>'),
            ('<itemlayout width="115" height="172">', '<itemlayout width="93" height="140">'),
            ('<focusedlayout width="115" height="172">', '<focusedlayout width="93" height="140">'),
            ('<width>115</width><height>172</height>', '<width>93</width><height>140</height>'),
            ('<left>0</left><top>0</top><width>115</width><height>4</height>', '<left>0</left><top>0</top><width>93</width><height>4</height>'),
            ('<left>0</left><top>168</top><width>115</width><height>4</height>', '<left>0</left><top>136</top><width>93</width><height>4</height>'),
            ('<left>0</left><top>0</top><width>4</width><height>172</height>', '<left>0</left><top>0</top><width>4</width><height>140</height>'),
            ('<left>111</left><top>0</top><width>4</width><height>172</height>', '<left>89</left><top>0</top><width>4</width><height>140</height>'),
            ('<left>0</left><top>0</top><width>230</width><height>6</height>', '<left>0</left><top>0</top><width>186</width><height>6</height>'),
            ('<left>0</left><top>339</top><width>230</width><height>6</height>', '<left>0</left><top>274</top><width>186</width><height>6</height>'),
            ('<left>0</left><top>0</top><width>6</width><height>345</height>', '<left>0</left><top>0</top><width>6</width><height>280</height>'),
            ('<left>224</left><top>0</top><width>6</width><height>345</height>', '<left>180</left><top>0</top><width>6</width><height>280</height>'),
            ('<left>83</left><top>16</top><width>64</width>', '<left>61</left><top>16</top><width>64</width>'),
            ('<left>100</left><top>22</top><width>28</width>', '<left>79</left><top>22</top><width>28</width>'),
            ('<left>83</left><top>289</top><width>64</width>', '<left>61</left><top>226</top><width>64</width>'),
            ('<left>100</left><top>295</top><width>28</width>', '<left>79</left><top>232</top><width>28</width>'),
            ('<left>0</left><top>268</top><width>230</width><height>26</height>', '<left>0</left><top>200</top><width>186</width><height>26</height>')):
        assert old in pane, old
        pane = pane.replace(old, new)
    assert '230' not in re.sub(r'<label>.*?</label>', '', pane) or True
    s = s[:p] + pane
    v = v[:a] + s + v[b:]
    # ---- the wall strip (Poster wall and the walls that share Aeon_V_Info): the studio logo larger
    a, b = section(v, '<include name="Aeon_V_Info">', '\n\t</include>')
    s = v[a:b]
    s = swap(s, '<control type="image"><left>1380</left><top>12</top><width>300</width><height>72</height>',
             '<!-- %s: the studio logo larger (was 300 x 72) -->\n\t\t\t\t<control type="image"><left>1300</left><top>4</top><width>380</width><height>92</height>' % MARK)
    v = v[:a] + s + v[b:]
    return v, True


LABEL = re.compile(r'(\t\t\t<control type="label">\n\t\t\t\t<left>200</left>\n.*?\t\t\t</control>\n)', re.S)


def ml_part(m):
    if MARK in m:
        return m, False
    a, b = section(m, '<include name="AeonM_Row">', '\n\t</include>')
    s = m[a:b]
    # the ring (albums) and the note (artists ...) go; songs keep the track number in that column
    icon = re.compile(r'\t\t\t<control type="image">\n\t\t\t\t<left>104</left>\n\t\t\t\t<top>30</top>\n.*?\$VAR\[AeonM_Icon\]</texture>\n.*?\t\t\t</control>\n', re.S)
    assert len(icon.findall(s)) == 2
    s = icon.sub('', s)
    s = swap(s, '<!-- icon, or the track number for songs -->', '<!-- %s: the track number for songs; albums and artists have no icon, their names start at 104 -->' % MARK)
    labels = LABEL.findall(s)
    assert len(labels) == 4, len(labels)
    for block in labels:
        song = block.replace('</visible>', ' + %s</visible>' % SONG)
        other = block.replace('<left>200</left>', '<left>104</left>').replace('<width>760</width>', '<width>856</width>') \
                     .replace('</visible>', ' + !%s</visible>' % SONG)
        assert song != block and other != block
        s = s.replace(block, song + other, 1)
    m = m[:a] + s + m[b:]
    # the header row over the list follows: the note and the name at 200 only over songs
    old = ('\t\t\t<control type="image">\n\t\t\t\t<left>104</left>\n\t\t\t\t<top>148</top>\n\t\t\t\t<width>40</width>\n\t\t\t\t<height>40</height>\n'
           '\t\t\t\t<texture colordiffuse="88ffffff">aeon/icons/music.png</texture>\n\t\t\t</control>\n')
    m = swap(m, old, old.replace('</texture>\n', '</texture>\n\t\t\t\t<visible>Container.Content(songs)</visible>\n'))
    old = ('\t\t\t<control type="label">\n\t\t\t\t<left>200</left>\n\t\t\t\t<top>138</top>\n\t\t\t\t<width>680</width>\n\t\t\t\t<height>60</height>\n'
           '\t\t\t\t<aligny>center</aligny>\n\t\t\t\t<font>lb_cap_20</font>\n\t\t\t\t<textcolor>ccffffff</textcolor><selectedcolor>ccffffff</selectedcolor>\n'
           '\t\t\t\t<label>$VAR[AeonM_Header]</label>\n\t\t\t</control>\n')
    m = swap(m, old, old.replace('</label>\n', '</label>\n\t\t\t\t<visible>Container.Content(songs)</visible>\n') +
             old.replace('<left>200</left>', '<left>104</left>').replace('<width>680</width>', '<width>776</width>')
                .replace('</label>\n', '</label>\n\t\t\t\t<visible>!Container.Content(songs)</visible>\n'))
    return m, True


def main():
    for fn, part in ((V2, v2_part), (ML, ml_part)):
        text = io.open(fn, encoding='utf-8').read()
        text, done = part(text)
        if done:
            io.open(fn, 'w', encoding='utf-8', newline='\n').write(text)
            ET.parse(fn)
        print(fn, 'patched' if done else 'already')


if __name__ == '__main__':
    main()
