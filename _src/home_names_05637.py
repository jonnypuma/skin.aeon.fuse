"""0.56.37 "Home menu: only the focused item's name" (aeon.hm.icons) in every theme (the user, 2026-11-17: "should apply
to all themes"). Fused Glass drew it with its own row (the neighbours' icons, the focused icon with its mark and its
name rolling out); Aeon and Aeon Glass draw their Home row the same way (icon + name in hm_display_60, the others
dimmed), so the row serves them too:
- FG_HmIcons no longer needs Fused Glass (the list's empty layouts and the icon row follow it);
- the focused icon's mark follows the theme like Aeon_H_Title: Fused Glass the pill always, Aeon Glass the pill and Aeon
  a square line with Home menu underline on;
- Skin settings: row 9546 shows in every theme, under ALL THEMES after Home menu position (appearance_order_05633
  rebuilds the page's Up / Down); its help loses "Fused Glass only." in all 23 languages.
Run from the skin folder before appearance_order_05633 (it moves the row). Repeatable."""
import io
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
D = os.path.join(ROOT, '1080i')
L = os.path.join(ROOT, 'language')


def rd(name):
    return io.open(os.path.join(D, name), encoding='utf-8').read()


def wr(name, text):
    io.open(os.path.join(D, name), 'w', encoding='utf-8', newline='\n').write(text)


def main():
    t = rd('Includes_Fused.xml')
    t = t.replace('<expression name="FG_HmIcons">Skin.HasSetting(aeon.hm.icons) + $EXP[Aeon_FGlass]</expression>',
                  '<expression name="FG_HmIcons">Skin.HasSetting(aeon.hm.icons)</expression>')
    wr('Includes_Fused.xml', t)

    t = rd('Includes_Aeon_Home.xml')
    old = '<control type="image"><left>57</left><top>92</top><width>36</width><height>4</height><texture border="2,0,2,0" colordiffuse="fg_mark">fg/pill4.png</texture></control>'
    if old in t:
        assert t.count(old) == 1
        new = ('<control type="image"><left>57</left><top>92</top><width>36</width><height>4</height><texture border="2,0,2,0" colordiffuse="fg_mark">fg/pill4.png</texture>'
               '<visible>$EXP[Aeon_FGlass] | [Skin.HasSetting(aeon.hm.underline) + $EXP[Aeon_VGlass]]</visible></control>'
               '<control type="image"><left>57</left><top>92</top><width>36</width><height>4</height><texture colordiffuse="fg_mark">common/white.png</texture>'
               '<visible>Skin.HasSetting(aeon.hm.underline) + !$EXP[Aeon_VGlass] + !$EXP[Aeon_FGlass]</visible></control>')
        t = t.replace(old, new)
    wr('Includes_Aeon_Home.xml', t)

    t = rd('SkinSettings.xml')
    s = t.index('<!-- row 9546')
    e = t.index('\n\t<control type="group">', s + 10)
    b = t[s:e]
    b = b.replace('\t\t<visible>$EXP[Aeon_FGlass]</visible>\n', '', 1)
    b = b.replace('<visible>Control.HasFocus(9546) + $EXP[Aeon_FGlass]</visible>', '<visible>Control.HasFocus(9546)</visible>')
    t = t[:s] + b + t[e:]
    wr('SkinSettings.xml', t)

    for d in sorted(os.listdir(L)):
        p = os.path.join(L, d, 'strings.po')
        po = io.open(p, encoding='utf-8').read()
        m = re.search(r'(msgctxt "#32426"\nmsgid ")(.*)("\nmsgstr ")(.*)(")', po)
        cut = lambda s: re.sub(r'\s*[^.。]*Fused Glass[^.。]*[.。]\s*$', '', s)      # noqa: E731
        po = po[:m.start()] + m.group(1) + cut(m.group(2)) + m.group(3) + cut(m.group(4)) + m.group(5) + po[m.end():]
        io.open(p, 'w', encoding='utf-8', newline='\n').write(po)
    print('done')


if __name__ == '__main__':
    main()
