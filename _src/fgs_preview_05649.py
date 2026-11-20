"""0.56.49 Fused Glass style: the Skin settings preview sits in the grid (the user, 2026-11-18: "why does the mockup
preview have a background overlay underneath it there on those screenshots?").

In the Fused Glass style the settings screen is one connected grid with three columns (120 | 480 | 1500 | 1820, the
frame lines in SkinSettings.xml), the third one for the preview. Each PREVIEW CARD (_src/skin_previews.py) also drew
its own Fused Glass card (Aeon_Glass, with its shadow) whenever the theme is Fused Glass, so in the style a second
panel lay over the grid's column (1532-1804 over 1500-1820). Now the card's panel shows in Fused Glass outside the
style only, and in the style the preview's text moves 20 px left: 24 px inside the column, as in the other two. The
Home menu / Context menu pages' card (1552) likewise. Run from the skin folder after skin_previews.py. Repeatable."""
import io
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'SkinSettings.xml')
CARD = ('<control type="group"><left>12</left><top>-91</top><width>272</width><height>866</height>'
        '<visible>$EXP[Aeon_FGlass]</visible><include>Aeon_Glass</include></control>')
SLIDE = '<animation effect="slide" start="0,0" end="8,-80" time="0" condition="$EXP[Aeon_FGlass]">Conditional</animation>'
FGS_SLIDE = '<animation effect="slide" start="0,0" end="-20,0" time="0" condition="$EXP[FGS]">Conditional</animation>'
SIDE = ('<visible>$EXP[Aeon_FGlass] + [String.IsEqual(Window(Home).Property(aeon.skincat),ctxmenu) | '
        'String.IsEqual(Window(Home).Property(aeon.skincat),homemenu)]</visible>')


def main():
    t = io.open(P, encoding='utf-8').read()
    n = [0, 0, 0]
    if CARD in t:
        n[0] = t.count(CARD)
        t = t.replace(CARD, CARD.replace('<visible>$EXP[Aeon_FGlass]</visible>', '<visible>$EXP[Aeon_FGlass] + !$EXP[FGS]</visible>'))
    if SLIDE + FGS_SLIDE not in t:
        n[1] = t.count(SLIDE)
        t = t.replace(SLIDE, SLIDE + FGS_SLIDE)
    if SIDE in t:
        n[2] = t.count(SIDE)
        t = t.replace(SIDE, SIDE.replace('<visible>$EXP[Aeon_FGlass] + ', '<visible>$EXP[Aeon_FGlass] + !$EXP[FGS] + '))
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    print('fgs_preview: %d card panels, %d text moves, %d side cards' % tuple(n))


if __name__ == '__main__':
    main()
