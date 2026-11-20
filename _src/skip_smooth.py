# -*- coding: utf-8 -*-
"""0.52.6 Smooth skip progress through Skippy's progress hook (service.skippy 7.15.0, skin_properties.py): while the
skin's skip pill (window 1167) is up, Skippy drives a progress control in it (31, no <info>) every video frame and
publishes Skippy.Segment.Frame (0 .. FRAMES - 1) while Skippy.Segment.SmoothProgress is true. The ring and the bar
are image sequences, so they get FRAMES pictures each (media/fg/pringf, media/aeon/skipbarf: a 420 px bar moves a
pixel at a time); without the driver (an older Skippy) everything shows the whole-per-cent pictures as before.

Declared on the Home window by Home.xml / VideoFullScreen.xml with the skin's skip button setting. Run from the skin
folder; safe to run again."""
import io
import os
import re

from PIL import Image, ImageDraw

FRAMES = 421
SS = 4
D = '1080i'
OLD_RING = 'fg/pring/$INFO[Window(Home).Property(Skippy.Segment.Progress)].png'
OLD_BAR = 'aeon/skipbar/$INFO[Window(Home).Property(Skippy.Segment.Progress)].png'
SMOOTH = 'String.IsEqual(Window(Home).Property(Skippy.Segment.SmoothProgress),true)'
# 0.53.2: Skippy > Progress bar counts down (its setting progress_bar_countdown): the pill shows what is left, as
# Skippy's own dialog does. Skippy.Segment.Progress / .Frame stay "played", so the reversed sequences (…r) are the same
# pictures numbered the other way round.
CD = 'Addon.SettingBool(service.skippy,progress_bar_countdown)'
FRAME = '$INFO[Window(Home).Property(Skippy.Segment.Frame)]'
PCT = '$INFO[Window(Home).Property(Skippy.Segment.Progress)]'
VARS = '''	<!-- ===== smooth skip progress (0.52.6, _src/skip_smooth.py): Skippy's frame while it drives the pill, else the per cent;
	     counting down when Skippy's progress bar counts down (0.53.2) -->
	<variable name="Aeon_SkipRingTex">
		<value condition="%(s)s + %(cd)s">fg/pringfr/%(f)s.png</value>
		<value condition="%(s)s">fg/pringf/%(f)s.png</value>
		<value condition="%(cd)s">fg/pringr/%(p)s.png</value>
		<value>%(r)s</value>
	</variable>
	<variable name="Aeon_SkipBarTex">
		<value condition="%(s)s + %(cd)s">aeon/skipbarfr/%(f)s.png</value>
		<value condition="%(s)s">aeon/skipbarf/%(f)s.png</value>
		<value condition="%(cd)s">aeon/skipbarr/%(p)s.png</value>
		<value>%(b)s</value>
	</variable>
	<!-- smooth skip progress: end -->
''' % {'s': SMOOTH, 'cd': CD, 'f': FRAME, 'p': PCT, 'r': OLD_RING, 'b': OLD_BAR}


def reversed_copy(src, dst, n):
    """dst/k.png = src/(n - 1 - k).png: the same pictures numbered the other way round."""
    import shutil
    os.makedirs(dst, exist_ok=True)
    for k in range(n):
        shutil.copyfile(os.path.join(src, '%d.png' % (n - 1 - k)), os.path.join(dst, '%d.png' % k))
ON = 'Skin.HasSetting(aeon.skippy.button)'
DECLARE = ('<onload condition="%(on)s">SetProperty(Skippy.SkinSkipProgress.Window,11167,home)</onload>\n'
           '\t<onload condition="%(on)s">SetProperty(Skippy.SkinSkipProgress.Control,31,home)</onload>\n'
           '\t<onload condition="%(on)s">SetProperty(Skippy.SkinSkipProgress.Frames,%(n)d,home)</onload>\n'
           '\t<onload condition="!%(on)s">ClearProperty(Skippy.SkinSkipProgress.Window,home)</onload>\n'
           '\t<onload condition="!%(on)s">ClearProperty(Skippy.SkinSkipProgress.Control,home)</onload>\n'
           '\t<onload condition="!%(on)s">ClearProperty(Skippy.SkinSkipProgress.Frames,home)</onload>' % {'on': ON, 'n': FRAMES})


def frames():
    rd, bd = os.path.join('media', 'fg', 'pringf'), os.path.join('media', 'aeon', 'skipbarf')
    os.makedirs(rd, exist_ok=True)
    os.makedirs(bd, exist_ok=True)
    S = 80 * SS
    for k in range(FRAMES):
        im = Image.new('L', (S, S), 0)
        if k:
            ImageDraw.Draw(im).arc([9 * SS, 9 * SS, S - 9 * SS - 1, S - 9 * SS - 1], -90, -90 + 360.0 * k / (FRAMES - 1), fill=255, width=7 * SS)
        out = Image.new('RGBA', (80, 80), (255, 255, 255, 0))
        out.putalpha(im.resize((80, 80), Image.LANCZOS))
        out.save(os.path.join(rd, '%d.png' % k), optimize=True)
        bar = Image.new('RGBA', (420, 6), (255, 255, 255, 0))
        if k:
            bar.paste((255, 255, 255, 255), (0, 0, round(420 * k / (FRAMES - 1)), 6))
        bar.save(os.path.join(bd, '%d.png' % k), optimize=True)
    reversed_copy(rd, os.path.join('media', 'fg', 'pringfr'), FRAMES)
    reversed_copy(bd, os.path.join('media', 'aeon', 'skipbarfr'), FRAMES)
    reversed_copy(os.path.join('media', 'fg', 'pring'), os.path.join('media', 'fg', 'pringr'), 101)
    reversed_copy(os.path.join('media', 'aeon', 'skipbar'), os.path.join('media', 'aeon', 'skipbarr'), 101)


def patch():
    n = 0
    for f in ('Custom_1167_SkippySkip.xml', 'Includes_Fused.xml'):
        p = os.path.join(D, f)
        t = io.open(p, encoding='utf-8').read()
        k = t.count(OLD_RING) + t.count(OLD_BAR)
        t = t.replace('>' + OLD_RING + '<', '>$VAR[Aeon_SkipRingTex]<').replace('>' + OLD_BAR + '<', '>$VAR[Aeon_SkipBarTex]<')
        if f == 'Includes_Fused.xml':
            t = re.sub(r'\t<!-- ===== smooth skip progress \(0\.52\.6.*?<!-- smooth skip progress: end -->\n', '', t, flags=re.S)
            t = re.sub(r'\t<!-- ===== smooth skip progress \(0\.52\.6.*?</variable>\n\t<variable name="Aeon_SkipBarTex">.*?</variable>\n', '', t, flags=re.S)
            t = t.replace('</includes>', VARS + '</includes>')
        if f == 'Custom_1167_SkippySkip.xml' and 'Aeon_SkipBarTex]</texture><visible>Skin.HasSetting(aeon.vglass)' not in t:
            # 0.53.2 the Glass pill's bar counting down: its pictures (track + bar), the progress controls step aside
            t = t.replace('<visible>Skin.HasSetting(aeon.vglass) + !$EXP[Aeon_FGlass] + !%s</visible>' % SMOOTH,
                          '<visible>Skin.HasSetting(aeon.vglass) + !$EXP[Aeon_FGlass] + !%s + !%s</visible>' % (SMOOTH, CD))
            t = t.replace('<visible>Skin.HasSetting(aeon.vglass) + !$EXP[Aeon_FGlass] + %s</visible>\n\t\t\t</control>' % SMOOTH,
                          '<visible>Skin.HasSetting(aeon.vglass) + !$EXP[Aeon_FGlass] + %s + !%s</visible>\n\t\t\t</control>\n'
                          '\t\t\t<control type="image"><left>0</left><top>90</top><width>420</width><height>6</height><texture colordiffuse="22000000">common/white.png</texture>'
                          '<visible>Skin.HasSetting(aeon.vglass) + !$EXP[Aeon_FGlass] + %s</visible></control>\n'
                          '\t\t\t<control type="image"><left>0</left><top>90</top><width>420</width><height>6</height><texture colordiffuse="aeon_onbar_99">$VAR[Aeon_SkipBarTex]</texture>'
                          '<visible>Skin.HasSetting(aeon.vglass) + !$EXP[Aeon_FGlass] + %s</visible></control>' % (SMOOTH, CD, CD, CD))
        if f == 'Custom_1167_SkippySkip.xml' and 'id="31"' not in t:
            # the Glass pill's bar: the <info> one until Skippy drives control 31
            old = '''				<info>Window(Home).Property(Skippy.Segment.Progress)</info>
				<visible>Skin.HasSetting(aeon.vglass) + !$EXP[Aeon_FGlass]</visible>
			</control>'''
            assert t.count(old) == 1, 'glass bar'
            new = '''				<info>Window(Home).Property(Skippy.Segment.Progress)</info>
				<visible>Skin.HasSetting(aeon.vglass) + !$EXP[Aeon_FGlass] + !%s</visible>
			</control>
			<!-- 0.52.6: the same bar, driven by Skippy every video frame (Skippy.SkinSkipProgress.Control); in the other looks it
			     stays hidden, their ring and bar follow Skippy.Segment.Frame -->
			<control type="progress" id="31">
				<left>0</left><top>90</top><width>420</width><height>6</height>
				<texturebg colordiffuse="22000000">common/aeon_line_6.png</texturebg>
				<midtexture colordiffuse="aeon_onbar_99">common/aeon_line_6.png</midtexture>
				<visible>Skin.HasSetting(aeon.vglass) + !$EXP[Aeon_FGlass] + %s</visible>
			</control>''' % (SMOOTH, SMOOTH)
            t = t.replace(old, new)
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
        n += k
    for f in ('Home.xml', 'VideoFullScreen.xml'):
        p = os.path.join(D, f)
        t = io.open(p, encoding='utf-8').read()
        if 'Skippy.SkinSkipProgress' not in t:
            anchor = '<onload condition="!Skin.HasSetting(aeon.skippy.button)">ClearProperty(Skippy.SkinSkipButton,home)</onload>'
            assert t.count(anchor) == 1, f
            t = t.replace(anchor, anchor + '\n\t' + DECLARE)
            io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    # (ms_skip_bar.py is a run-once script: if it is ever run again, run this one after it)
    return n


if __name__ == '__main__':
    frames()
    print('textures replaced:', patch())
