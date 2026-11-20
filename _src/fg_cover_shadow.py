"""0.52.0 Screensaver: the album cover's dropped shadow is one pre-blurred soft texture (media/fg/shc.png, 9-slice)
instead of six black copies of the cover at 12 % each (which showed as steps: the user's note). Draws the texture and
patches 1080i/Custom_1156_Screensaver.xml (both cover groups, Aeon and Fused Glass). Safe to run again. Run from the
skin folder."""
import io
import os
import re

from PIL import Image, ImageDraw, ImageFilter

SS = 4
R, M, BLUR = 12, 96, 30          # corner radius of the cover, blur margin, gaussian radius (px at 1:1)
B = M + 94                       # 9-slice border: the falloff and a solid inside fit in the corners
N = 2 * B + 16


def texture():
    n = N
    big = Image.new('L', (n * SS, n * SS), 0)
    ImageDraw.Draw(big).rounded_rectangle([M * SS, M * SS, (n - M) * SS - 1, (n - M) * SS - 1], R * SS, fill=255)
    a = big.resize((n, n), Image.LANCZOS).filter(ImageFilter.GaussianBlur(BLUR))
    out = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    out.putalpha(a)
    out.save(os.path.join('media', 'fg', 'shc.png'), optimize=True)


def shadow(x, y, w, h, drop=22, col='99000000'):
    """The soft shadow of a w x h picture at (x, y), dropped a little."""
    return ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><fadetime>700</fadetime>'
            '<texture border="%d" colordiffuse="%s">fg/shc.png</texture></control>' % (x - M, y - M + drop, w + 2 * M, h + 2 * M, B, col))


def patch():
    p = os.path.join('1080i', 'Custom_1156_Screensaver.xml')
    t = io.open(p, encoding='utf-8').read()
    # the six stacked copies (821 ... 761 wide) of either group, up to the cover itself
    t = re.sub(r'<texture border="\d+" colordiffuse="([0-9a-f]{8})">fg/shc\.png</texture>', lambda m: '<texture border="%d" colordiffuse="%s">fg/shc.png</texture>' % (B, m.group(1)), t)
    stack = re.compile(r'(\t\t\t)<control type="image"><left>140</left><top>144</top><width>821</width>.*?<width>761</width><height>761</height>[^\n]*</control>\n', re.S)
    found = len(stack.findall(t))
    t = stack.sub(lambda m: m.group(1) + shadow(174, 164, 753, 753) + '\n', t)
    t = t.replace('a few sizes larger and a little lower, so it always has the cover\'s own shape and fades out softly.',
                  'a few sizes larger and a little lower. 0.52.0: one pre-blurred soft texture (fg/shc.png, _src/fg_cover_shadow.py):\n'
                  '\t\t     the stacked copies showed as steps.')
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    return found


if __name__ == '__main__':
    texture()
    print('stacks replaced:', patch())
