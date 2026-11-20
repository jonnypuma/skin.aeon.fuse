# -*- coding: utf-8 -*-
"""0.56.22 splash (the user: "the loading strip is a bit boring. a nice, sleek spinner would be nicer. also it's not good
that the coreelec update interrupts it every time ... has to override background modals until it's finished loading.
better show a toast on the splash screen then"). Runs once (marker).

- The progress strip of each look (Aeon, Aeon Glass, Fused Glass) becomes a thin spinning ring: a faint track and a
  tapered arc in the look's accent, turning once every 1.1 s (still with Reduce motion). The steps under it stay.
- A yes / no / OK / progress dialog that opens while the splash is up (CoreELEC's update question, ~15 s after Home)
  is moved off the screen, not hidden, so it keeps its buttons and focus and nothing is answered; a toast on the splash
  names it ("<heading> · waits until loading is done"). When the splash ends the dialog slides in as usual. Kodi's
  "Keep changes?" after a skin change (13123) is never held back: it closes by itself after 10 s."""
import io
import os
import re
import xml.etree.ElementTree as ET

MARK = '0.56.22 splash'
FUSED = os.path.join('1080i', 'Includes_Fused.xml')
CONFIRM = os.path.join('1080i', 'DialogConfirm.xml')
SID = 32644
S = {'en_gb': 'waits until loading is done', 'cs_cz': 'počká, až se vše načte', 'da_dk': 'venter, til indlæsningen er færdig',
     'de_de': 'wartet, bis alles geladen ist', 'el_gr': 'περιμένει να ολοκληρωθεί η φόρτωση', 'es_es': 'espera a que termine la carga',
     'fi_fi': 'odottaa, kunnes lataus on valmis', 'fr_fr': 'attend la fin du chargement', 'hu_hu': 'megvárja a betöltés végét',
     'it_it': 'attende la fine del caricamento', 'ja_jp': '読み込みが終わるまで待機中', 'ko_kr': '로딩이 끝날 때까지 대기',
     'nb_no': 'venter til innlastingen er ferdig', 'nl_nl': 'wacht tot het laden klaar is', 'pl_pl': 'czeka na koniec wczytywania',
     'pt_br': 'aguarda o fim do carregamento', 'pt_pt': 'aguarda o fim do carregamento', 'ru_ru': 'ждёт окончания загрузки',
     'sv_se': 'väntar tills inläsningen är klar', 'tr_tr': 'yükleme bitene kadar bekliyor', 'uk_ua': 'чекає завершення завантаження',
     'zh_cn': '等待加载完成', 'zh_tw': '等待載入完成'}


def textures():
    from PIL import Image, ImageDraw
    import math
    k, size, stroke = 4, 176, 12
    for name, sweep, taper in (('spin_track', 360, False), ('spin_arc', 290, True)):
        out = os.path.join('media', 'fg', name + '.png')
        big = Image.new('L', (size * k, size * k), 0)
        d = ImageDraw.Draw(big)
        r = (size * k - stroke * k) / 2.0
        c = size * k / 2.0
        steps = 720
        for i in range(steps):
            # clockwise from 12 o'clock; the arc brightens towards its head (the clockwise end)
            a0 = math.radians(-90 + sweep * i / steps)
            a = 255 if not taper else int(255 * (0.08 + 0.92 * (i / float(steps)) ** 1.6))
            x, y = c + r * math.cos(a0), c + r * math.sin(a0)
            d.ellipse((x - stroke * k / 2.0, y - stroke * k / 2.0, x + stroke * k / 2.0, y + stroke * k / 2.0), fill=a)
        im = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        im.putalpha(big.resize((size, size), Image.LANCZOS))
        im.save(out)


def spinner(x, y, track, arc):
    return ('<control type="group"><left>%d</left><top>%d</top><width>44</width><height>44</height><!-- %s: the spinner -->'
            '<control type="image"><left>0</left><top>0</top><width>44</width><height>44</height><texture colordiffuse="%s">fg/spin_track.png</texture></control>'
            '<control type="image"><left>0</left><top>0</top><width>44</width><height>44</height><texture colordiffuse="%s">fg/spin_arc.png</texture>'
            '<animation effect="rotate" end="-360" center="auto" time="1100" loop="true" reversible="false" condition="!Skin.HasSetting(aeon.reducemotion)">Conditional</animation></control>'
            '</control>' % (x, y, MARK, track, arc))


def strings():
    for folder in sorted(os.listdir('language')):
        lang = folder.replace('resource.language.', '')
        p = os.path.join('language', folder, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        if 'msgctxt "#%d"' % SID in t:
            continue
        t = t.rstrip('\n') + '\n\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (SID, S['en_gb'], '' if lang == 'en_gb' else S[lang])
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)


def main():
    f = io.open(FUSED, encoding='utf-8').read()
    if MARK in f:
        print('already')
        return
    textures()
    strings()
    a = f.index('<include name="Aeon_Splash">')
    b = f.index('\n\t</include>', a)
    seg = f[a:b]
    # (left, top of the strip) -> spinner centred on the strip: Aeon 640,540 h6; Aeon Glass 680,512 h8; Fused Glass 700,520 h10
    for left, top, h, track, arc in ((640, 540, 6, '1fffffff', '$VAR[Aeon_Accent]'), (680, 512, 8, '24ffffff', 'ffffffff'),
                                     (700, 520, 10, '24ffffff', 'fg_mark')):
        lines = re.findall(r'[ \t]*<control type="image"><left>%d</left><top>%d</top>[^\n]*\n' % (left, top), seg)
        assert len(lines) == 5, (left, len(lines))
        first = seg.index(lines[0])
        indent = lines[0][:len(lines[0]) - len(lines[0].lstrip())]
        for line in lines:
            seg = seg.replace(line, '', 1)
        seg = seg[:first] + indent + spinner(938, top + h // 2 - 22, track, arc) + '\n' + seg[first:]
    f = f[:a] + seg + f[b:]
    # the dialog held back while the splash is up
    old = '\t<expression name="Aeon_SplTv">'
    f = f.replace(old, '\t<!-- %s: a dialog that opens while the splash is up waits off the screen (not Kodi\'s "Keep changes?" after a skin change) -->\n'
                       '\t<expression name="Aeon_SplHold">!String.IsEmpty(Window(Home).Property(aeon.splash)) + !String.IsEqual(Control.GetLabel(1),$LOCALIZE[13123])</expression>\n' % MARK + old, 1)
    io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(f)
    ET.parse(FUSED)

    c = io.open(CONFIRM, encoding='utf-8').read()
    old = '''	<controls>
		<include condition="!$EXP[Aeon_MS]">Confirm_Classic</include>
		<include condition="$EXP[Aeon_MS_mosaic]">MS_Confirm_mosaic</include>
		<include condition="$EXP[Aeon_MS_ledger]">MS_Confirm_ledger</include>
		<include condition="$EXP[Aeon_MS_bridge]">MS_Confirm_bridge</include>
		<include condition="$EXP[Aeon_MS_tabslab]">MS_Confirm_tabslab</include>
	</controls>'''
    assert c.count(old) == 1
    c = c.replace(old, '''	<controls>
		<control type="group">
			<!-- %(m)s: while the start-up splash is up the dialog waits below the screen (it keeps its buttons and focus) -->
			<animation effect="slide" end="0,1400" time="0" condition="$EXP[Aeon_SplHold]">Conditional</animation>
			<include condition="!$EXP[Aeon_MS]">Confirm_Classic</include>
			<include condition="$EXP[Aeon_MS_mosaic]">MS_Confirm_mosaic</include>
			<include condition="$EXP[Aeon_MS_ledger]">MS_Confirm_ledger</include>
			<include condition="$EXP[Aeon_MS_bridge]">MS_Confirm_bridge</include>
			<include condition="$EXP[Aeon_MS_tabslab]">MS_Confirm_tabslab</include>
		</control>
		<!-- %(m)s: the toast on the splash: the dialog's heading, "waits until loading is done" -->
		<control type="group">
			<visible>$EXP[Aeon_SplHold]</visible>
			<animation type="Visible" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" time="300"/><effect type="slide" start="0,24" end="0,0" time="300" tween="cubic" easing="out"/></animation>
			<control type="grouplist">
				<left>0</left><top>880</top><width>1920</width><height>64</height><orientation>horizontal</orientation><align>center</align><itemgap>0</itemgap><usecontrolcoords>true</usecontrolcoords>
				<control type="button"><width min="200" max="1500">auto</width><height>64</height><label>$INFO[Control.GetLabel(1),[B],[/B]  ·  ]$ADDON[skin.aeon.fuse %(sid)d]</label><font>hm_ui_22</font><textcolor>f2ffffff</textcolor><disabledcolor>f2ffffff</disabledcolor><align>center</align><aligny>center</aligny><textoffsetx>32</textoffsetx><enable>false</enable><texturenofocus border="32" colordiffuse="e61a1b20">fg/r32.png</texturenofocus><texturefocus border="32" colordiffuse="e61a1b20">fg/r32.png</texturefocus></control>
			</control>
		</control>
	</controls>''' % {'m': MARK, 'sid': SID})
    io.open(CONFIRM, 'w', encoding='utf-8', newline='\n').write(c)
    ET.parse(CONFIRM)
    print('ok')


if __name__ == '__main__':
    main()
