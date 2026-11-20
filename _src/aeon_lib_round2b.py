# -*- coding: utf-8 -*-
"""0.56.15 what the three new Skin settings rows (_src/settings_05615.py) switch:
- Ratings shown as Icons | Text (aeon.rating.text): every rating provider icon in a row of ratings (IMDb, TMDb, Rotten
  Tomatoes, Trakt; all of them grouplist items) gets its name beside it as a label, shown instead of the icon in Text
  mode, in the number's font and colour (so with Colour on the whole "IMDb 7.8" takes the colour; with icons only the
  number does);
- Fanart look Dimmed | Frosted (aeon.fanartlook) in the library backdrop (Aeon_V_Bg): Frosted = the Glass themes' light
  fanart with its colour tint and vignette, Dimmed = Aeon's stronger fanart under a dark veil; empty = the theme's own;
- Home menu underline (aeon.hm.underline, Aeon and Glass): the accent mark under the focused Home menu item's icon, as
  Fused Glass draws it (a square line in Aeon, the pill in Glass).
Each file is changed once (by what it already has), so the Aeon view chain (scratchpad rebuild_aeon.py) can restore its
files and run this again."""
import io
import os
import re
import xml.etree.ElementTree as ET

D = '1080i'
MARK = '0.56.15 aeon_lib_round2b'
NAMES = {'imdb': 'IMDb', 'tmdb': 'TMDb', 'rtfresh': 'RT', 'trakt': 'Trakt'}
RATE_FILES = ('Includes_Aeon_Home.xml', 'Includes_Aeon_Sub.xml', 'Includes_Aeon_Views2.xml', 'Includes_Aeon_Views3.xml', 'Includes_Fused.xml')


def rate_text(t):
    if '$EXP[Aeon_RateText]' in t:
        return t, 0
    out, pos, n = [], 0, 0
    for m in re.finditer(r'<control type="image">(?:(?!</control>).)*?<texture[^>]*>ratings/(imdb|tmdb|rtfresh|trakt)\.png</texture>(?:(?!</control>).)*?</control>', t, re.S):
        img = m.group(0)
        assert '<left>' not in img, img[:120]
        h = re.search(r'<height>([^<]*)</height>', img).group(1)
        v = re.search(r'<visible>(.*?)</visible>', img, re.S)
        cond = v.group(1) if v else ''
        nxt = t[m.end():m.end() + 1500]
        lm = re.search(r'<control type="label">(?:(?!</control>).)*?</control>', nxt, re.S)
        font = re.search(r'<font>([^<]*)</font>', lm.group(0)).group(1) if lm and '<font>' in lm.group(0) else 'lb_ui_24_bold'
        col = re.search(r'<textcolor>([^<]*)</textcolor>', lm.group(0)).group(1) if lm and '<textcolor>' in lm.group(0) else 'ffffffff'
        if v:
            new_img = img.replace(v.group(0), '<visible>[%s] + !$EXP[Aeon_RateText]</visible>' % cond, 1)
            lab_vis = '[%s] + $EXP[Aeon_RateText]' % cond
        else:
            new_img = img[:-len('</control>')] + '<visible>!$EXP[Aeon_RateText]</visible></control>'
            lab_vis = '$EXP[Aeon_RateText]'
        label = ('<control type="label"><width min="10" max="160">auto</width><height>%s</height><aligny>center</aligny><font>%s</font>'
                 '<textcolor>%s</textcolor><selectedcolor>%s</selectedcolor><label>%s</label><visible>%s</visible></control>'
                 % (h, font, col, col, NAMES[m.group(1)], lab_vis))
        out.append(t[pos:m.start()])
        out.append(new_img + label)
        pos = m.end()
        n += 1
    out.append(t[pos:])
    return ''.join(out), n


def fanart_look(v2):
    if 'Aeon_FanFrosted' in v2:
        return v2, False
    a = v2.index('<include name="Aeon_V_Bg">')
    b = v2.index('\n\t</include>', a)
    bg = v2[a:b]
    for old, new, n in (('<visible>$EXP[Aeon_VGlass] + $EXP[Aeon_GBgFan]</visible>', '<visible>$EXP[Aeon_FanShown] + $EXP[Aeon_FanFrosted]</visible>', 2),
                        ('<texture>common/aeon_vignette.png</texture><visible>$EXP[Aeon_VGlass]</visible>',
                         '<texture>common/aeon_vignette.png</texture><visible>$EXP[Aeon_VGlass] | [$EXP[Aeon_FanShown] + $EXP[Aeon_FanFrosted]]</visible>', 1),
                        ('<visible>!$EXP[Aeon_VGlass] + $EXP[Aeon_VBgFan]</visible>', '<visible>$EXP[Aeon_FanShown] + !$EXP[Aeon_FanFrosted]</visible>', 2)):
        assert bg.count(old) == n, (old, bg.count(old))
        bg = bg.replace(old, new)
    bg = bg.replace('<definition>', '<definition>\n\t\t\t<!-- %s: Fanart look (aeon.fanartlook): Frosted = the Glass themes\' light fanart, colour tint and '
                    'vignette; Dimmed = Aeon\'s fanart under a dark veil; the theme picks while nothing is chosen -->' % MARK, 1)
    return v2[:a] + bg + v2[b:], True


def home_underline(h):
    if 'aeon.hm.underline' in h:
        return h, False
    old = ('\t\t\t<!-- the accent mark centred under the item\'s icon (0.36.0) -->\n'
           '\t\t\t<control type="image">\n'
           '\t\t\t\t<left>42</left><top>92</top><width>36</width><height>4</height>\n'
           '\t\t\t\t<texture border="2,0,2,0" colordiffuse="fg_mark">fg/pill4.png</texture>\n'
           '\t\t\t\t<visible>$PARAM[focused] + $EXP[Aeon_FGlass]</visible>\n'
           '\t\t\t</control>\n')
    assert h.count(old) == 1
    new = old + ('\t\t\t<!-- %s: Aeon and Glass too, with Home menu underline on (a square line in Aeon) -->\n'
                 '\t\t\t<control type="image"><left>42</left><top>92</top><width>36</width><height>4</height><texture border="2,0,2,0" colordiffuse="fg_mark">fg/pill4.png</texture>'
                 '<visible>$PARAM[focused] + !$EXP[Aeon_FGlass] + Skin.HasSetting(aeon.hm.underline) + $EXP[Aeon_VGlass]</visible></control>\n'
                 '\t\t\t<control type="image"><left>42</left><top>92</top><width>36</width><height>4</height><texture colordiffuse="fg_mark">common/white.png</texture>'
                 '<visible>$PARAM[focused] + Skin.HasSetting(aeon.hm.underline) + !$EXP[Aeon_VGlass]</visible></control>\n' % MARK)
    return h.replace(old, new), True


def defs(g):
    if 'Aeon_RateText' in g:
        return g, False
    anchor = '\t<variable name="Aeon_PrevRating">'
    assert g.count(anchor) == 1
    return g.replace(anchor, '\t<!-- %s -->\n'
                     '\t<expression name="Aeon_RateText">Skin.HasSetting(aeon.rating.text)</expression>\n'
                     '\t<expression name="Aeon_FanFrosted">[String.IsEqual(Skin.String(aeon.fanartlook),frosted) | [String.IsEmpty(Skin.String(aeon.fanartlook)) + $EXP[Aeon_VGlass]]]</expression>\n'
                     '\t<expression name="Aeon_FanShown">[$EXP[Aeon_VGlass] + $EXP[Aeon_GBgFan]] | [!$EXP[Aeon_VGlass] + $EXP[Aeon_VBgFan]]</expression>\n' % MARK + anchor, 1), True


def main():
    done = []
    for fn in RATE_FILES:
        p = os.path.join(D, fn)
        t = io.open(p, encoding='utf-8').read()
        t, n = rate_text(t)
        if fn == 'Includes_Aeon_Views2.xml':
            t, d = fanart_look(t)
            n += d
        if fn == 'Includes_Aeon_Home.xml':
            t, d = home_underline(t)
            n += d
        if n:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
            ET.parse(p)
            done.append((fn, n))
    p = os.path.join(D, 'Includes_Aeon_Glass.xml')
    g, d = defs(io.open(p, encoding='utf-8').read())
    if d:
        io.open(p, 'w', encoding='utf-8', newline='\n').write(g)
        ET.parse(p)
        done.append(('Includes_Aeon_Glass.xml', 1))
    print('ok' if done else 'already done', done)


if __name__ == '__main__':
    main()
