# -*- coding: utf-8 -*-
"""0.56.3 Fused Glass: no Flat focus highlight any more (Pill, Frosted, Outline, Tight stay).

The user (2026-11-15): the flat bar must fill the small gap to the card's top / bottom with the card's round corners
where it meets them, "if you are unable then we remove flat as an option for Fused Glass but keep the others". The
library lists could do it (0.56.2), but Kodi's own settings pages and add-on settings keep their rows in a scrolling
grouplist and tell the skin nothing about where the focused row sits, so a flat bar there always ends 12 px from the
card's rounded corner and pokes out of it. So Flat goes:
  - Skin settings > Appearance > Focus highlight (row 9749): Pill, Frosted, Outline, Tight (OK: Pill > Frosted >
    Outline > Tight > Pill); Pill moves next to Frosted, the row's pill is one choice shorter.
  - a Flat already chosen counts as Pill everywhere (FG_FocusFlat is false, the button pictures fall back to the pill)
    and Home resets it to Pill when it opens.
  - _src/fg_lib_focus.py no longer draws the library views' flat bars (FLAT_SLOTS = False).
Run from the skin folder; safe to run again."""
import io
import os
import re

FL = 'String.IsEqual(Skin.String(aeon.fgfocus),flat)'


def rd(p):
    return io.open(p, encoding='utf-8').read()


def wr(p, t):
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)


def fused():
    p = os.path.join('1080i', 'Includes_Fused.xml')
    t = rd(p)
    t = t.replace('<expression name="FG_FocusFlat">%s</expression>' % FL, '<expression name="FG_FocusFlat">false</expression>')
    t = t.replace('<expression name="FG_FocusShadowOn">!%s</expression>' % FL, '<expression name="FG_FocusShadowOn">true</expression>')
    t = re.sub(r'\n\t\t<value condition="%s">fg/fx_flat\.png</value>' % re.escape(FL), '', t)
    t = re.sub(r'\n\t\t<include condition="%s">FG_BtnFocusTex_flat</include>' % re.escape(FL), '', t)
    t = t.replace('<include condition="!%s + ' % FL, '<include condition="')
    wr(p, t)
    print('Includes_Fused: flat left', t.count(FL))


def row():
    p = os.path.join('1080i', 'SkinSettings.xml')
    t = rd(p)
    i = t.find('<control type="button" id="9749">')
    g = t.rfind('<control type="group">', 0, i)
    depth = 0
    for m in re.finditer(r'<control[ >]|</control>', t[g:]):
        depth += -1 if m.group(0) == '</control>' else 1
        if depth == 0:
            e = g + m.end()
            break
    c = t[g:e]
    if '$ADDON[skin.aeon.fuse 32410]' not in c:
        print('row 9749 already without Flat')
        return
    # the Flat choice (left 430) goes; Pill (324) takes its place next to Frosted; the row's pill is 106 shorter
    c = re.sub(r'\t*<control type="(?:image|label)"><left>430</left><top>13</top><width>106</width>.*?</control>\n', '', c)
    c = c.replace('<left>324</left><top>13</top><width>106</width>', '<left>430</left><top>13</top><width>106</width>')
    c = c.replace('<left>320</left><top>13</top><width>540</width>', '<left>426</left><top>13</top><width>434</width>')
    c = c.replace('Skin.SetString(aeon.fgfocus,flat)</onclick>', 'Skin.SetString(aeon.fgfocus,frost)</onclick>')
    c = re.sub(r'\s*<onclick condition="%s">Skin\.SetString\(aeon\.fgfocus,frost\)</onclick>' % re.escape(FL), '', c)
    assert '32410' not in c and 'fgfocus,flat' not in c
    wr(p, t[:g] + c + t[e:])
    print('row 9749: Pill, Frosted, Outline, Tight')


def home():
    p = os.path.join('1080i', 'Home.xml')
    t = rd(p)
    line = '\t<onload condition="%s">Skin.Reset(aeon.fgfocus)</onload>\n' % FL
    if line in t:
        return
    a = t.find('\t<onload')
    wr(p, t[:a] + '\t<!-- 0.56.3: Flat is gone (_src/fg_noflat.py): a Flat chosen before is the pill now -->\n' + line + t[a:])
    print('Home: resets a stored Flat')


def lib_focus():
    p = os.path.join('_src', 'fg_lib_focus.py')
    t = rd(p)
    t = t.replace("STYLES = (('pill', '!%s + !%s + !%s + !%s' % (FLAT, S % 'frost', S % 'outline', S % 'tight')),",
                  "STYLES = (('pill', '!%s + !%s + !%s' % (S % 'frost', S % 'outline', S % 'tight')),")
    if 'FLAT_SLOTS = ' not in t:
        t = t.replace("MARK = '<!-- flat focus bar (_src/fg_lib_focus.py) -->'",
                      "MARK = '<!-- flat focus bar (_src/fg_lib_focus.py) -->'\nFLAT_SLOTS = False   # 0.56.3: Flat is gone from Fused Glass (_src/fg_noflat.py)")
        t = t.replace("        for lid in LISTS:\n            blk, done = flat_slots(blk, lid)\n            ns += done\n",
                      "        for lid in (LISTS if FLAT_SLOTS else ()):\n            blk, done = flat_slots(blk, lid)\n            ns += done\n")
        t = t.replace("        if MARK in blk:\n            continue\n", "        if 'fg/fx_frost.png' in blk:\n            continue\n")
    wr(p, t)
    print('fg_lib_focus.py: no flat bars')


if __name__ == '__main__':
    fused()
    row()
    home()
    lib_focus()
