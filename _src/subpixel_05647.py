"""0.56.47 ready for Kodi 23 (the user, 2026-11-18: "sure add those now, it'll futureproof our skin").
Kodi 22 rounds every corner of a skin picture to a whole pixel (GUITexture::Render, ROUND_TO_PIXEL), so a slow pan or zoom
moves in 1 px steps and a progress bar grows in 1 px steps; only the picture slideshow draws between pixels. Kodi 23 adds
two texture attributes: subpixel="true" (draw at the exact, fractional position) and mipmap="true" (smaller copies of the
picture, no shimmer when a big picture is drawn smaller). Kodi 22 skips attributes it does not know, so nothing changes
there; on 23 the moving fanart glides and the bars fill smoothly.

- the moving fanart (the screensaver's zoom and slide, the music Now playing drift, the Home spotlight / widget screens'
  zoom, the start-up splash's slide): subpixel="true" mipmap="true" on the picture
- every progress bar: subpixel="true" on the part that grows (<midtexture>) and the end cap that moves with it
  (<righttexture>)
Run from the skin folder. Repeatable: re-run after a generator that writes progress bars or these pictures."""
import glob
import io
import os
import re

SKIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
X = os.path.join(SKIN, '1080i')
BOTH = ' subpixel="true" mipmap="true"'
MOVING = [
    ('Custom_1156_Screensaver.xml', '<texture background="true" colordiffuse="55ffffff">$VAR[Aeon_SSFanOdd]</texture>'),
    ('Custom_1156_Screensaver.xml', '<texture background="true" colordiffuse="55ffffff">$VAR[Aeon_SSFanEven]</texture>'),
    ('Includes_Aeon_Music.xml', '<texture background="true" colordiffuse="ffb0b0b0">$VAR[Aeon_NP_FanartBase]</texture>'),
    ('Includes_Aeon_Music.xml', '<texture background="true" colordiffuse="ffb0b0b0">$VAR[Aeon_NP_Fanart]</texture>'),
    ('Includes_Aeon_Sub.xml', '<texture background="true" colordiffuse="ffffffff">$VAR[Aeon_Sp_Art]</texture>'),
    ('Includes_Fused.xml', '<texture background="true" colordiffuse="66ffffff">$INFO[Window(Home).Property(aeon.splash.fan)]</texture>'),
]
BAR = re.compile(r'<(midtexture|righttexture)(?![^>]*subpixel=)(\s[^>]*?)?(\s*/?)>')


def moving():
    n = 0
    for name, tag in MOVING:
        p = os.path.join(X, name)
        t = io.open(p, encoding='utf-8').read()
        done = tag.replace('<texture ', '<texture' + BOTH + ' ', 1)
        if done in t:
            continue
        assert t.count(tag) == 1, (name, tag)
        t = t.replace(tag, done)
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
        n += 1
    return n


def bars():
    n = 0
    for p in sorted(glob.glob(os.path.join(X, '*.xml'))):
        t = io.open(p, encoding='utf-8').read()
        new, k = BAR.subn(lambda m: '<%s subpixel="true"%s%s>' % (m.group(1), m.group(2) or '', m.group(3)), t)
        if k:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(new)
            n += k
    return n


def main():
    print('subpixel: %d moving pictures, %d progress textures' % (moving(), bars()))


if __name__ == '__main__':
    main()
