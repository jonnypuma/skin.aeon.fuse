# -*- coding: utf-8 -*-
"""0.56.48, the user's three notes of 2026-11-18:
- "Movie sets in List view, the movie posters overlap with clearlogo. Move posters down to under clearlogo ... Also
  missing a chevron to the left to go to the movie selection on the poster." Fused Glass List (510): the set's film
  strip (5105) slides 96 px down while a clearlogo shows over it (logo 750..834, posters 848..992); a set shows no
  studio logo / name there (the strip's place). A chevron on the big poster's right edge while the list has the focus
  and Left opens a pane (a set's films, a film's versions).
- "Movie sets banner list: movie sets do not have banners so we can remove this view from Movie sets." Banner list
  (522) leaves sets: the picker card (1165) and the view's own condition in both the Aeon and the Fused Glass view
  (Kodi then falls back to the first list view, List 510, for a set node that was on it).
- "there is no panel blur in library view settings." The row (0.56.45) hid with the Clear style, which draws no
  blurred copy. It now shows in every Fused Glass style: in Clear, Default is Off and Light / Medium / Strong turn the
  blur on for that view ($EXP[FG_PanelBlurMat]).
The generators carry the same changes (fg_lib.py, fg_lib_lists2.py, fg_panel_blur.py, viewset_05645.py); this script
patches the files in place because later versions patched them too. Run from the skin folder. Repeatable."""
import io
import os
import xml.etree.ElementTree as ET

D = '1080i'
IS_SET = 'String.IsEqual(Container(510).ListItem.DBType,set)'
LOGO_UP = '$EXP[FG_L_LogosOn] + !String.IsEmpty(Container(510).ListItem.Art(clearlogo))'
STRIP_SLIDE = '<animation effect="slide" end="0,96" time="0" condition="%s">Conditional</animation>' % LOGO_UP
CHEVRON = ('\t\t\t<!-- 0.56.48 sets_05648: Left opens the pane (a set\'s films, a film\'s versions) -->\n'
           '\t\t\t<control type="group"><visible>Control.HasFocus(510) + $EXP[Aeon_HasLeftPane]</visible><include>Anim_FadeVisible</include>'
           '<control type="image"><left>623</left><top>576</top><width>48</width><height>48</height><texture colordiffuse="b3080a0e">fg/circle.png</texture></control>'
           '<control type="image"><left>635</left><top>588</top><width>24</width><height>24</height><aspectratio>keep</aspectratio>'
           '<texture colordiffuse="ffffffff">aeon/icons/chevron_left.png</texture></control></control>\n')
BLUR_OLD = '$EXP[FG_PanelBlur] + !String.IsEqual(Skin.String(aeon.fgmat),clear)'
BLUR_NEW = '$EXP[FG_PanelBlur] + $EXP[FG_PanelBlurMat]'
BLUR_EXP = ('\t<!-- 0.56.48 sets_05648: the Clear style draws the blurred copy only for a view whose own Panel blur (View settings) is on -->\n'
            '\t<expression name="FG_PanelBlurMat">!String.IsEqual(Skin.String(aeon.fgmat),clear) | [!String.IsEmpty(Window(Home).Property(aeon.vo.pblur)) + '
            '!String.IsEqual(Window(Home).Property(aeon.vo.pblur),off)]</expression>\n')
SETS_522 = 'Container.Content(tvshows) | Container.Content(movies) | Container.Content(sets) | Container.Content(seasons)'
NOSETS_522 = 'Container.Content(tvshows) | Container.Content(movies) | Container.Content(seasons)'


def rd(name):
    return io.open(os.path.join(D, name), encoding='utf-8').read()


def wr(name, text):
    io.open(os.path.join(D, name), 'w', encoding='utf-8', newline='\n').write(text)
    ET.parse(os.path.join(D, name))


def fused(t):
    # --- the set's film strip under the clearlogo
    a = '<control type="list" id="5105"><left>1356</left><top>752</top><width>420</width><height>150</height><orientation>horizontal</orientation>'
    assert t.count(a) == 1, '5105'
    if a + STRIP_SLIDE not in t:
        t = t.replace(a, a + STRIP_SLIDE)
    # --- no studio logo / name for a set (the strip's place)
    for old in ('String.IsEqual(Window(Home).Property(aeon.studio.of),Container(510).ListItem.Studio)</visible></control><control type="label"><left>1528</left><top>954</top>',
                'String.IsEqual(Window(Home).Property(aeon.studio.of),Container(510).ListItem.Studio)</visible><wrapmultiline>true</wrapmultiline></control></control>\n\t\t\t<!-- the rail -->'):
        new = old.replace('Container(510).ListItem.Studio)</visible>', 'Container(510).ListItem.Studio) + !%s</visible>' % IS_SET, 1)
        if new not in t:
            assert t.count(old) == 1, old[:60]
            t = t.replace(old, new)
    # --- the chevron on the poster
    if 'sets_05648: Left opens the pane' not in t:
        a = '\t\t\t<!-- the list card: six rows; the item in focus under them -->\n'
        assert t.count(a) == 1, 'list card'
        t = t.replace(a, CHEVRON + a)
    # --- Banner list: not for sets
    a = '<viewtype label="31140">list</viewtype><visible>%s</visible>'
    if a % NOSETS_522 not in t:
        assert t.count(a % SETS_522) == 1, '522'
        t = t.replace(a % SETS_522, a % NOSETS_522)
    # --- Panel blur per view in the Clear style
    t = t.replace(BLUR_OLD, BLUR_NEW)
    if 'name="FG_PanelBlurMat"' not in t:
        a = '\t<expression name="FG_PanelBlur">'
        assert t.count(a) == 1, 'FG_PanelBlur'
        i = t.index('\n', t.index(a)) + 1
        t = t[:i] + BLUR_EXP + t[i:]
    return t


def views2(t):
    a = '<viewtype label="31140">list</viewtype>\n\t\t\t\t<visible>%s</visible>'
    if a % NOSETS_522 not in t:
        assert t.count(a % SETS_522) == 1, 'aeon 522'
        t = t.replace(a % SETS_522, a % NOSETS_522)
    return t.replace('$EXP[Aeon_FGlass] + $EXP[Aeon_GBgFan] + !String.IsEqual(Skin.String(aeon.fgmat),clear)</visible>',
                     '$EXP[Aeon_FGlass] + $EXP[Aeon_GBgFan] + $EXP[FG_PanelBlurMat]</visible>')


def picker(t):
    a = '<onclick>Container.SetViewMode(522)</onclick><visible>%s</visible>'
    if a % NOSETS_522 not in t:
        assert t.count(a % SETS_522) == 1, 'picker 522'
        t = t.replace(a % SETS_522, a % NOSETS_522)
    return t


def panel_row(t):
    return t.replace('<visible>Skin.HasSetting(aeon.fglass) + !String.IsEqual(Skin.String(aeon.fgmat),clear)</visible>',
                     '<visible>Skin.HasSetting(aeon.fglass)</visible>')


def blur_label(t):
    """Default (Off) in the Clear style"""
    new = '\t\t<value condition="String.IsEqual(Skin.String(aeon.fgmat),clear)">$LOCALIZE[31546] ($LOCALIZE[31548])</value>\n'
    if new in t:
        return t
    a = '\t\t<value condition="String.IsEqual(Skin.String(aeon.x.pblur),off)">$LOCALIZE[31546] ($LOCALIZE[31548])</value>\n'
    s = t.index('<variable name="Aeon_VOS_pblur">')
    i = t.index(a, s)
    assert i < t.index('</variable>', s)
    return t[:i] + new + t[i:]


def main():
    for name, fn in (('Includes_Fused.xml', fused), ('Includes_Aeon_Views2.xml', views2), ('Custom_1165_VideoViews.xml', picker),
                     ('Includes_LibraryPanel.xml', panel_row), ('Includes_Aeon_Sub.xml', blur_label)):
        old = rd(name)
        new = fn(old)
        if new != old:
            wr(name, new)
        print('%-30s %s' % (name, 'changed' if new != old else 'as it was'))
    f = rd('Includes_Fused.xml') + rd('Includes_Aeon_Views2.xml')
    print('blur layers on FG_PanelBlurMat:', f.count('$EXP[FG_PanelBlurMat]'))


if __name__ == '__main__':
    main()
