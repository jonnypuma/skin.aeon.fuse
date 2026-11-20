# -*- coding: utf-8 -*-
"""0.40.5 Fused Glass: Skin settings > Look > Toasts from the clock pill (Skin.HasSetting(aeon.toastpill), off).
The clock pill grows to the left and holds the toast (skin.glass/mockups/clock-pill, look A). Run once from the skin folder."""
import io
import xml.etree.ElementTree as ET

# 1. the expression
F = '1080i/Includes_Fused.xml'
f = io.open(F, encoding='utf-8').read()
assert 'FG_ToastPill' not in f
a = '\t<expression name="FG_RailClock">'
assert f.count(a) == 1
f = f.replace(a, '\t<!-- 0.40.5: Skin settings > Look > Toasts from the clock pill (aeon.toastpill): wherever the clock is the pill at the top\n'
                 '\t     right (not the library rail, not full-screen video without the player controls) -->\n'
                 '\t<expression name="FG_ToastPill">Skin.HasSetting(aeon.toastpill) + $EXP[Aeon_FGlass] + !$EXP[FG_NoClock] + '
                 '![!$EXP[Aeon_HomeAny] + $EXP[FG_RailClock]]</expression>\n' + a, 1)
io.open(F, 'w', encoding='utf-8', newline='\n').write(f)
ET.parse(F)

D = '1080i/DialogNotification.xml'
d = io.open(D, encoding='utf-8').read()
# 2. today's capsule (look B) gives way: its fill and edge hide; its text and icon stay where they are (the same place in A)
for old in ('<control type="image"><left>-180</left><top>40</top><width>576</width><height>64</height><texture border="32" colordiffuse="fg_panel">fg/r32.png</texture></control>',
            '<control type="image"><left>-180</left><top>40</top><width>576</width><height>64</height><texture border="32" colordiffuse="fg_edge">fg/e32.png</texture></control>'):
    assert d.count(old) == 1
    d = d.replace(old, old.replace('</control>', '<visible>!$EXP[FG_ToastPill]</visible></control>'), 1)
# 3. the text group: in look A the text fades in after the grow and goes first on close
old_open = '<animation type="WindowOpen" condition="!Skin.HasSetting(aeon.reducemotion) + $EXP[Aeon_FGlass]">'
old_close = '<animation type="WindowClose" condition="!Skin.HasSetting(aeon.reducemotion) + $EXP[Aeon_FGlass]">'
assert d.count(old_open) == 1 and d.count(old_close) == 1
new_open = '<animation type="WindowOpen" condition="!Skin.HasSetting(aeon.reducemotion) + $EXP[Aeon_FGlass] + !$EXP[FG_ToastPill]">'
d = d.replace(old_open, new_open, 1)
d = d.replace(old_close, '<animation type="WindowClose" condition="!Skin.HasSetting(aeon.reducemotion) + $EXP[Aeon_FGlass] + !$EXP[FG_ToastPill]">', 1)
i = d.index(new_open)
d = d[:i] + ('<animation type="WindowOpen" condition="$EXP[FG_ToastPill] + !Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" time="220" delay="480"/></animation>\n'
             '\t\t\t<animation type="WindowOpen" condition="$EXP[FG_ToastPill] + Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" time="150"/></animation>\n'
             '\t\t\t<animation type="WindowClose" condition="$EXP[FG_ToastPill]"><effect type="fade" start="100" end="0" time="150"/></animation>\n\t\t\t') + d[i:]

GROW = '!Skin.HasSetting(aeon.reducemotion)'
CLOCK_WX = ('<control type="group"><left>1588</left><top>40</top>'
            '<control type="label"><left>24</left><width>96</width><height>64</height><aligny>center</aligny><align>center</align><font>hm_ui_30_semibold</font><textcolor>ffffffff</textcolor><label>$INFO[System.Time(HH:mm)]</label></control>'
            '<control type="image"><left>126</left><top>18</top><width>1</width><height>28</height><texture colordiffuse="33ffffff">common/white.png</texture></control>'
            '<control type="image"><left>140</left><top>16</top><width>32</width><height>32</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">$VAR[AG_WeatherIcon]</texture></control>'
            '<control type="label"><left>174</left><width>54</width><height>64</height><aligny>center</aligny><align>center</align><font>hm_ui_24</font><textcolor>dbffffff</textcolor><label>$INFO[Weather.Temperature]</label></control></control>')
CLOCK_NARROW = ('<control type="label"><left>1680</left><top>40</top><width>144</width><height>64</height><aligny>center</aligny><align>center</align>'
                '<font>hm_ui_30_semibold</font><textcolor>ffffffff</textcolor><label>$INFO[System.Time(HH:mm)]</label></control>')


def pill(L, clock_x, wx):
    """the wide pill from L to 1824 (top 40, 64 tall), grown from the clock pill that starts at clock_x"""
    band_x = L + 32
    band_w = 1792 - band_x
    start = round(100.0 * (1792 - (clock_x + 32)) / band_w, 1)
    slide = clock_x - L
    o = ['\t\t\t<control type="group">', '\t\t\t\t<visible>%s$EXP[AG_HasWeather]</visible>' % ('' if wx else '!')]
    o.append('\t\t\t\t<control type="image"><left>%d</left><top>40</top><width>%d</width><height>64</height><texture colordiffuse="fg_panel">common/white.png</texture>'
             '<animation type="WindowOpen" condition="%s"><effect type="zoom" start="%s,100" end="100,100" center="1792,72" time="380" delay="100" tween="cubic" easing="out"/></animation>'
             '<animation type="WindowClose" condition="%s"><effect type="zoom" start="100,100" end="%s,100" center="1792,72" time="300" delay="150" tween="cubic" easing="in"/></animation></control>'
             % (band_x, band_w, GROW, start, GROW, start))
    o.append('\t\t\t\t<control type="image"><left>%d</left><top>40</top><width>64</width><height>64</height><texture border="32" colordiffuse="fg_panel">fg/r32.png</texture>'
             '<animation type="WindowOpen" condition="%s"><effect type="slide" start="%d,0" end="0,0" time="380" delay="100" tween="cubic" easing="out"/></animation>'
             '<animation type="WindowClose" condition="%s"><effect type="slide" start="0,0" end="%d,0" time="300" delay="150" tween="cubic" easing="in"/></animation></control>'
             % (L, GROW, slide, GROW, slide))
    o.append('\t\t\t\t<control type="image"><left>1760</left><top>40</top><width>64</width><height>64</height><texture border="32" colordiffuse="fg_panel">fg/r32.png</texture></control>')
    o.append('\t\t\t\t<control type="image"><left>%d</left><top>40</top><width>%d</width><height>64</height><texture border="32" colordiffuse="fg_edge">fg/e32.png</texture>'
             '<animation type="WindowOpen" condition="%s"><effect type="fade" start="0" end="100" time="150" delay="480"/></animation>'
             '<animation type="WindowClose"><effect type="fade" start="100" end="0" time="100"/></animation></control>' % (L, 1824 - L, GROW))
    o.append('\t\t\t\t' + (CLOCK_WX if wx else CLOCK_NARROW))
    o.append('\t\t\t</control>')
    return '\n'.join(o)


look_a = ('\t\t<!-- 0.40.5 Fused Glass, Skin settings > Look > Toasts from the clock pill (aeon.toastpill, off): the clock pill grows to\n'
          '\t\t     the left and holds the toast (skin.glass/mockups/clock-pill, look A). Drawn whole here, near solid, over the\n'
          '\t\t     frosted clock pill of the window, the time and weather again at its right end. Kodi cannot animate a width:\n'
          '\t\t     the round left end slides out while a flat band behind it stretches from the clock; the text (the group after\n'
          '\t\t     this one) fades in once it is wide. Closing: text out, pill back, then the pill fades and the frosted clock\n'
          '\t\t     pill shows again. Reduce motion: the wide pill only fades in and out. -->\n'
          '\t\t<control type="group">\n'
          '\t\t\t<visible>$EXP[FG_ToastPill]</visible>\n'
          '\t\t\t<animation type="WindowOpen"><effect type="fade" start="0" end="100" time="100"/></animation>\n'
          '\t\t\t<animation type="WindowClose"><effect type="fade" start="100" end="0" time="150" delay="450"/></animation>\n'
          + pill(1000, 1588, True) + '\n' + pill(1092, 1680, False) + '\n\t\t</control>\n')
anchor = '\t<controls>\n'
assert d.count(anchor) == 1
d = d.replace(anchor, anchor + look_a, 1)
io.open(D, 'w', encoding='utf-8', newline='\n').write(d)
ET.parse(D)
print('look A in place')
