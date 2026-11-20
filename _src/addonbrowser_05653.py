# -*- coding: utf-8 -*-
"""0.56.53 the add-on browser (and Favourites, the same view) in Fused Glass style (user, 2026-11-20, PC: "screenshot
for addons: misalignment, not uniform height. scrolling up after settings button does not go to the bottom addon in
the list. Likewise scrolling down from the youtube addon does not go to the top of the list").

- one height: the add-on rows 70 (were 100), as the button strip above them and every Skin settings row; the icon
  54 (was 72), the name and the summary moved up to fit; ten rows in the list's 700;
- the strip is a row of cells: no gap between its buttons (was 10) and a line at each one's right edge
  (fg/fgs_sep_r.png), so the focus bar fills its cell from line to line instead of ending past the icon column's line;
- round trip: Up from the strip goes to the last add-on, Down from the last add-on to the first (both looks).
Repeatable."""
import io
import os
import re

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', '1080i')
SEP = os.path.join(HERE, '..', 'media', 'fg', 'fgs_sep_r.png')


def rd(n):
    return io.open(os.path.join(D, n), encoding='utf-8').read()


def wr(n, t):
    io.open(os.path.join(D, n), 'w', encoding='utf-8', newline='\n').write(t)


def main():
    if not os.path.isfile(SEP):                       # 4 x 4, the right column white: border keeps it 1 px
        im = Image.new('RGBA', (64, 8), (255, 255, 255, 0))   # wide: a 4 px one bled a shade when stretched
        for y in range(8):
            im.putpixel((63, y), (255, 255, 255, 255))
        im.save(SEP)
    c = rd('Includes_Common.xml')
    i = c.index('<include name="FGS_SubNavLook">')
    e = c.index('</include>', i)
    x = c[i:e]
    if 'fgs_sep_r.png' not in x:
        x = x.replace('<texturenofocus />', '<texturenofocus border="0,0,2,0" colordiffuse="1affffff">fg/fgs_sep_r.png</texturenofocus>', 1)
        c = c[:i] + x + c[e:]
        wr('Includes_Common.xml', c)
    v = rd('Includes_Views.xml')
    i = v.index('<include name="FGS_AddonRow">')
    e = v.index('<include name="View_50_List">', i)
    seg = v[i:e]
    if 'height="100"' in seg or '<height>100</height>' in seg:
        seg = seg.replace('height="100"', 'height="70"').replace('<top>99</top>', '<top>69</top>')
        seg = seg.replace('<width>1</width><height>100</height>', '<width>1</width><height>70</height>')
        seg = seg.replace('<width>5</width><height>100</height>', '<width>5</width><height>70</height>')
        seg = seg.replace('<left>322</left><top>14</top><width>72</width><height>72</height>', '<left>331</left><top>8</top><width>54</width><height>54</height>')
        seg = seg.replace('<left>286</left><top>14</top><width>128</width><height>72</height>', '<left>302</left><top>8</top><width>96</width><height>54</height>')
        seg = seg.replace('<top>16</top><width>560</width><height>38</height>', '<top>5</top><width>560</width><height>34</height>')
        seg = seg.replace('<top>54</top><width>660</width><height>30</height>', '<top>37</top><width>660</width><height>26</height>')
        seg = seg.replace('<top>0</top><width>660</width><height>100</height>', '<top>0</top><width>660</width><height>70</height>')
        seg = seg.replace('<left>1050</left><top>16</top><width>114</width><height>38</height>', '<left>1050</left><top>5</top><width>114</width><height>34</height>')
        print('add-on rows: 70')
    v = v[:i] + seg + v[e:]
    # round trip, both list views of window 50
    n = v.count('<ondown>noop</ondown>\n\t\t\t\t<onleft condition="Window.IsActive(addonbrowser)')
    v = v.replace('<ondown>noop</ondown>\n\t\t\t\t<onleft condition="Window.IsActive(addonbrowser)',
                  '<ondown>Action(FirstPage)</ondown>\n\t\t\t\t<onleft condition="Window.IsActive(addonbrowser)')
    wr('Includes_Views.xml', v)
    a = rd('AddonBrowser.xml')
    i = a.index('<control type="grouplist" id="9000">')
    e = a.index('<include content="AG_SubNavButton">', i)
    head = a[i:e]
    if 'Action(LastPage)' not in head:
        head = head.replace('<onup>noop</onup>', '<onup>SetFocus(50)</onup><onup>Action(LastPage)</onup>', 1)
        head = head.replace('<itemgap>10</itemgap>', '<include condition="$EXP[FGS]">FGS_Gap0</include><include condition="!$EXP[FGS]">FGS_Gap10_Else</include>', 1)
        a = a[:i] + head + a[e:]
        wr('AddonBrowser.xml', a)
    f = rd('Includes_Fused.xml')
    if '<include name="FGS_Gap0">' not in f:
        k = f.index('\t<include name="FGS_RowTex">')
        f = f[:k] + '\t<include name="FGS_Gap0"><itemgap>0</itemgap></include><include name="FGS_Gap10_Else"><itemgap>10</itemgap></include>\n' + f[k:]
        wr('Includes_Fused.xml', f)
    print('wrap: %d lists' % n)


def gutter():
    """the scroll bar gutter (user, 2026-11-20: "ADDONS: no scrollbar gutter"): the list 360-1540, a 20 px column
    with lines at 1540 and 1560 holding the square bar 60 (1541, 19 wide), as every Fused Glass style menu"""
    v = rd('Includes_Views.xml')
    i = v.index('<include name="FGS_AddonRow">')
    e = v.index('<include name="View_50_List">', i)
    seg = v[i:e]
    if '<!-- gutter -->' in seg:
        return
    seg = seg.replace('<width>1190</width>', '<width>1180</width>').replace('<left>1050</left>', '<left>1030</left>')
    seg = seg.replace('<left>360</left>\n\t\t\t\t<top>251</top>\n\t\t\t\t<width>1200</width>',
                      '<left>360</left>\n\t\t\t\t<top>251</top>\n\t\t\t\t<width>1180</width>')
    seg = seg.replace('<itemlayout width="1200"', '<itemlayout width="1180"').replace('<focusedlayout width="1200"', '<focusedlayout width="1180"')
    a = seg.index('<control type="scrollbar" id="60">')
    b = seg.index('</control>', a) + len('</control>')
    bar = ('<!-- gutter --><!-- left frame line --><control type="image"><left>360</left><top>180</top><width>1</width><height>771</height>'
           '<texture colordiffuse="1affffff">common/white.png</texture></control><control type="image"><left>1540</left><top>180</top><width>1</width><height>771</height>'
           '<texture colordiffuse="1affffff">common/white.png</texture></control>'
           '<control type="image"><left>1560</left><top>180</top><width>1</width><height>771</height>'
           '<texture colordiffuse="1affffff">common/white.png</texture></control>'
           '<control type="scrollbar" id="60"><left>1541</left><top>251</top><width>19</width><height>700</height>'
           '<include>FGS_SBTex</include><textureslidernib /><textureslidernibfocus /><orientation>vertical</orientation>'
           '<showonepage>false</showonepage><onleft>50</onleft><onright>noop</onright><onup>9000</onup></control>')
    seg = seg[:a] + bar + seg[b:]
    v = v[:i] + seg + v[e:]
    wr('Includes_Views.xml', v)
    print('add-on gutter')


if __name__ == '__main__':
    main()
    gutter()
