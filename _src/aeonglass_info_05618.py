# -*- coding: utf-8 -*-
"""0.56.18 the user's notes on the information pages (2026-11-16):
- Aeon Glass: "some menus have perpendicular edges but the highlight outline is rounded" - the Aeon Glass card
  (Aeon_Glass, used by AG_Card: the information page's cards, the text viewer, dialogs) is rounded: the frosted fills
  and the hairline edge as r28 shapes (fg/r28, fg/e28) with the rounded shadow, like the focus ring around them;
- Aeon Glass: "there is no dark gradient fade over the landscape picture in the information page" - the hero picture
  takes Fused Glass's mask (fg/mhero1160: fades in from the left, rounded on the right) instead of aeon/mask_hero_tall
  (a full mask, no fade);
- "The frosted background when selected (plot panel) isn't very nice" - not the Material: the focus glow
  (aeon/ring_glow_<r>, AG_Halo) was opaque in its middle and filled the focused card; AG_FocusRing uses
  aeon/ring_glow_out_<r> (_src/ring_glow_out.py), the glow outside the card only;
- Aeon Glass and the Fuse menu theme (Aeon / Aeon Glass): "Information pages: Recommended titles, Similar titles and
  Review are not rounded" - the posters, their focus frame and the review cards take Fused Glass's rounded parts
  (Aeon_RoundInfo = Fused Glass | Aeon Glass | Fuse menu theme). The full-screen review (Kodi's text viewer) sits on
  AG_Card, rounded with the card above.
Runs once (marker)."""
import io
import os
import re
import xml.etree.ElementTree as ET

GL = os.path.join('1080i', 'Includes_Aeon_Glass.xml')
VI = os.path.join('1080i', 'Includes_VideoInfo.xml')
MARK = '0.56.18 aeonglass_info'
VG = '<visible>$EXP[Aeon_VGlass] + !$EXP[Aeon_FGlass]</visible>'


def swap(t, old, new, count=1):
    n = t.count(old)
    assert n == count, (old[:100], n, count)
    return t.replace(old, new)


def glass(t):
    a = t.index('<include name="Aeon_Glass">')
    b = t.index('\n\t</include>', a)
    s = t[a:b]
    lines = s.split('\n')
    old = [l for l in lines if VG in l]
    assert len(old) == 7, len(old)
    new = ('\t\t\t<!-- %s: Aeon Glass rounded (r28) like its focus ring: shadow, the two frosted fills, the hairline edge -->\n'
           '\t\t\t<control type="image"><left>-40</left><top>-40</top><right>-40</right><bottom>-40</bottom><texture border="68" colordiffuse="55000000">fg/sho28.png</texture>%s</control>\n'
           '\t\t\t<control type="image"><left>0</left><top>0</top><right>0</right><bottom>0</bottom><texture border="28" colordiffuse="3a101010">fg/r28.png</texture>%s</control>\n'
           '\t\t\t<control type="image"><left>0</left><top>0</top><right>0</right><bottom>0</bottom><texture border="28" colordiffuse="0fffffff">fg/r28.png</texture>%s</control>\n'
           '\t\t\t<control type="image"><left>0</left><top>0</top><right>0</right><bottom>0</bottom><texture border="28" colordiffuse="38ffffff">fg/e28.png</texture>%s</control>'
           % (MARK, VG, VG, VG, VG))
    first = s.index(old[0])
    last = s.index(old[-1]) + len(old[-1])
    s = s[:first] + new.lstrip('\t') + s[last:]
    return t[:a] + s + t[b:]


def hero_strip():
    """step b (after the box shots): the dark fade strip (aeon/hero_fade, AG_Surface) began fully dark where the picture
    begins and drew a hard edge against the translucent Aeon Glass card; Aeon Glass, like Fused Glass, lets the picture
    fade into the glass instead (the mask above) and takes Fused Glass's soft shade over the picture's foot."""
    v = io.open(VI, encoding='utf-8').read()
    if MARK + 'b' in v:
        return False
    old = '<texture colordiffuse="$VAR[AG_Surface]">aeon/hero_fade.png</texture>\n\t\t\t\t<visible>!$EXP[Aeon_FGlass]</visible>'
    v = swap(v, old, old.replace('<visible>!$EXP[Aeon_FGlass]</visible>', '<visible>!$EXP[Aeon_VGlass]</visible><!-- %sb: Aeon Glass fades through the mask -->' % MARK))
    old = '<texture diffuse="fg/mhero1160.png" colordiffuse="c0000000">fg/scrim_b.png</texture>\n\t\t\t\t<visible>Skin.HasSetting(aeon.vglass) + $EXP[Aeon_FGlass]</visible>'
    v = swap(v, old, old.replace('<visible>Skin.HasSetting(aeon.vglass) + $EXP[Aeon_FGlass]</visible>', '<visible>Skin.HasSetting(aeon.vglass)</visible>'))
    io.open(VI, 'w', encoding='utf-8', newline='\n').write(v)
    ET.parse(VI)
    return True


def main():
    g = io.open(GL, encoding='utf-8').read()
    v = io.open(VI, encoding='utf-8').read()
    if MARK in g:
        print('already', 'strip' if hero_strip() else '')
        return
    g = glass(g)
    g = g.replace('\t<expression name="Aeon_Fused">',
                  '\t<!-- %s: the information page\'s rows rounded: Fused Glass, Aeon Glass, the Fuse menu theme -->\n'
                  '\t<expression name="Aeon_RoundInfo">[$EXP[Aeon_FGlass] | $EXP[Aeon_VGlass] | String.IsEqual(Skin.String(aeon.menutheme),fused)]</expression>\n'
                  '\t<expression name="Aeon_Fused">' % MARK, 1)
    # the focus glow, outside the card only (every AG_FocusRing)
    files = {}
    for fn in sorted(os.listdir('1080i')):
        if not fn.endswith('.xml'):
            continue
        p = os.path.join('1080i', fn)
        t = g if p == GL else v if p == VI else io.open(p, encoding='utf-8').read()
        if 'aeon/ring_glow_$PARAM[r].png' in t:
            t = t.replace('aeon/ring_glow_$PARAM[r].png', 'aeon/ring_glow_out_$PARAM[r].png')
            files[p] = t
    assert files, 'AG_FocusRing not found'
    if GL in files:
        g = files.pop(GL)
    if VI in files:
        v = files.pop(VI)
    # hero: the left fade in Aeon Glass too
    v = swap(v, '<texture background="true" diffuse="aeon/mask_hero_tall.png" colordiffuse="$VAR[AG_ArtDim]">$VAR[VidInfo_Fanart]</texture>',
             '<texture background="true" diffuse="fg/mhero1160.png" colordiffuse="$VAR[AG_ArtDim]">$VAR[VidInfo_Fanart]</texture><!-- %s: fades in from the left -->' % MARK)
    # Recommended / Similar posters and the review cards: rounded where the cards are
    for name in ('VidInfo_OnlineItem', 'VidInfo_ReviewRow'):
        a = v.index('<include name="%s">' % name)
        b = v.index('\n\t</include>', a)
        s = v[a:b]
        n = s.count('$EXP[Aeon_FGlass]')
        assert n >= 4, (name, n)
        s = s.replace('!$EXP[Aeon_FGlass]', '!$EXP[Aeon_RoundInfo]').replace('$EXP[Aeon_FGlass]', '$EXP[Aeon_RoundInfo]')
        v = v[:a] + s + v[b:]
    v = v.replace('<include name="VidInfo_OnlineItem">', '<!-- %s: rounded in Fused Glass, Aeon Glass and the Fuse menu theme (Aeon_RoundInfo) -->\n\t<include name="VidInfo_OnlineItem">' % MARK, 1)
    for p, t in ((GL, g), (VI, v)) + tuple(files.items()):
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
        ET.parse(p)
    print('ok', sorted([GL, VI] + list(files)))


if __name__ == '__main__':
    main()
