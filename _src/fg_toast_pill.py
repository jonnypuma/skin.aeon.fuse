# -*- coding: utf-8 -*-
"""0.56.6 Fused Glass toasts from the clock pill (Skin settings > Look > Toasts from the clock pill, aeon.toastpill): one
contiguous pill in every material.

The user (2026-11-16): "the expanding clock dock animation works under Glass but it shows the left rounded edge of the
clock dock so the illusion breaks that it is one contiguous pill, which is the whole point of it. i guess the darker
materials just hides it but it's still there too when they are used."
Why: the toast pill (DialogNotification) was a stretched band with a whole round cap (r32, 64 wide) sliding out over
its left end and another over its right end, drawn over the window's own clock capsule. With see-through glass the
overlaps showed: the caps darker where they lay on the band, and the window's capsule with its round left end and
edge line through the pill.
Now:
  - the pill is cut into pieces that never overlap: a left half cap (fg/pill64l.png, 32 x 64) that slides out, the
    band (zoomed from the clock end) and a right half cap (fg/pill64r.png); its edge the same way (fg/pill64le.png,
    fg/pill64me.png along the band, fg/pill64re.png), so the rim is one line all round while it grows. The half cap
    and the band end move together (same tween and time), as before.
  - the pill takes the clock capsule's material (FG_Frost / FG_Edge; it was the denser FG_Panel), and starts and ends
    as exactly the capsule (1588..1824 with weather, 1680..1824 without), so it can take the capsule's place at once:
  - the window's clock capsule (FG_ClockCapsule) is hidden while the toast pill shows; the pill appears without a
    fade (it is the capsule at first) and closes back to the capsule's size without fading, then the capsule is back.
Run from the skin folder; safe to run again."""
import io
import os
import re

from PIL import Image

NOTE = os.path.join('1080i', 'DialogNotification.xml')
FUSED = os.path.join('1080i', 'Includes_Fused.xml')
FG = os.path.join('media', 'fg')


def textures():
    """the halves of a 64 x 64 pill drawn from r32 / e32 (80 x 80, border 32: four 32 x 32 corners)"""
    for src, left, right, mid in (('r32.png', 'pill64l.png', 'pill64r.png', None), ('e32.png', 'pill64le.png', 'pill64re.png', 'pill64me.png')):
        im = Image.open(os.path.join(FG, src)).convert('RGBA')
        for name, x0 in ((left, 0), (right, 48)):
            out = Image.new('RGBA', (32, 64), (255, 255, 255, 0))
            out.paste(im.crop((x0, 0, x0 + 32, 32)), (0, 0))
            out.paste(im.crop((x0, 48, x0 + 32, 80)), (0, 32))
            out.save(os.path.join(FG, name), optimize=True)
        if mid:
            col = Image.new('RGBA', (4, 64), (255, 255, 255, 0))
            for x in range(4):
                col.paste(im.crop((40, 0, 41, 32)), (x, 0))
                col.paste(im.crop((40, 48, 41, 80)), (x, 32))
            col.save(os.path.join(FG, mid), optimize=True)
    print('pill halves and band edge')


def anim_zoom(start):
    return ('<animation type="WindowOpen" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="zoom" start="%s,100" '
            'end="100,100" center="1792,72" time="380" delay="100" tween="cubic" easing="out"/></animation>'
            '<animation type="WindowClose" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="zoom" start="100,100" '
            'end="%s,100" center="1792,72" time="300" delay="150" tween="cubic" easing="in"/></animation>' % (start, start))


ANIM_SLIDE = ('<animation type="WindowOpen" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="slide" start="588,0" '
              'end="0,0" time="380" delay="100" tween="cubic" easing="out"/></animation><animation type="WindowClose" '
              'condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="slide" start="0,0" end="588,0" time="300" delay="150" '
              'tween="cubic" easing="in"/></animation>')


def pill(x0, zoom):
    """the pill from x0 to 1824 at top 40: left half cap, band, right half cap, and their rim"""
    band_l, band_w = x0 + 32, 1792 - (x0 + 32)
    img = '\t\t\t\t<control type="image"><left>%d</left><top>40</top><width>%d</width><height>64</height><texture colordiffuse="%s">%s</texture>%s</control>\n'
    return ''.join((
        img % (band_l, band_w, '$VAR[FG_Frost]', 'common/white.png', anim_zoom(zoom)),
        img % (band_l, band_w, '$VAR[FG_Edge]', 'fg/pill64me.png', anim_zoom(zoom)),
        img % (x0, 32, '$VAR[FG_Frost]', 'fg/pill64l.png', ANIM_SLIDE),
        img % (x0, 32, '$VAR[FG_Edge]', 'fg/pill64le.png', ANIM_SLIDE),
        img % (1792, 32, '$VAR[FG_Frost]', 'fg/pill64r.png', ''),
        img % (1792, 32, '$VAR[FG_Edge]', 'fg/pill64re.png', '')))


def note():
    t = io.open(NOTE, encoding='utf-8').read()
    if 'fg/pill64l.png' in t:
        print('toast pill already in pieces')
        return
    for vis, x0, zoom in (('$EXP[AG_HasWeather]', 1000, '22.6'), ('!$EXP[AG_HasWeather]', 1092, '12.0')):
        a = t.find('<visible>%s</visible>' % vis, t.find('<visible>$EXP[FG_ToastPill]</visible>'))
        a = t.find('\n', a) + 1
        # the pill's pictures (fill and rim) up to the first label or group of the time / weather
        b = a
        while True:
            line_end = t.find('\n', b) + 1
            line = t[b:line_end]
            if not line.strip().startswith('<control type="image">'):
                break
            b = line_end
        old = t[a:b]
        assert old.count('<control type="image">') == 4, (vis, old.count('<control type="image">'))
        t = t[:a] + pill(x0, zoom) + t[b:]
    # the pill appears as the capsule (no fade in) and closes back to it (no fade out): the capsule takes over
    t = t.replace('<visible>$EXP[FG_ToastPill]</visible>\n\t\t\t<animation type="WindowOpen"><effect type="fade" start="0" end="100" time="100"/></animation>\n'
                  '\t\t\t<animation type="WindowClose"><effect type="fade" start="100" end="0" time="150" delay="450"/></animation>',
                  '<visible>$EXP[FG_ToastPill]</visible>\n'
                  '\t\t\t<animation type="WindowOpen" condition="Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" time="100"/></animation>\n'
                  '\t\t\t<animation type="WindowClose" condition="Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="100" end="0" time="150"/></animation>')
    assert 'time="150" delay="450"' not in t
    io.open(NOTE, 'w', encoding='utf-8', newline='\n').write(t)
    print('toast pill: half caps, band and rim in pieces, the capsule material')


def capsule():
    t = io.open(FUSED, encoding='utf-8').read()
    a = t.find('<include name="FG_ClockCapsule">')
    g = t.find('<control type="group">', a)
    head = t[g:g + 200]
    if 'Window.IsVisible(notification)' in head:
        print('capsule already hides under the toast pill')
        return
    t = t[:g] + ('<control type="group">\n\t\t\t<!-- 0.56.6: the toast pill takes its place while it shows (_src/fg_toast_pill.py) -->\n'
                 '\t\t\t<visible>![$EXP[FG_ToastPill] + Window.IsVisible(notification)]</visible>') + t[g + len('<control type="group">'):]
    io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(t)
    print('FG_ClockCapsule: hidden while the toast pill shows')


if __name__ == '__main__':
    textures()
    note()
    capsule()
