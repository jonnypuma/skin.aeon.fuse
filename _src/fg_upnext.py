# -*- coding: utf-8 -*-
"""0.52.5 Fused Glass Up next card: Skippy's next episode prompt in the skin's look (Skippy's skin hook,
service.skippy skin_properties.py: Skippy.SkinNextEpisode on the Home window hands the prompt to the skin).

Like the skin's skip button (Custom_1167 with its watchers 1171 / 1172) the card is a focusable dialog (1174) opened by
an empty watcher (1175) while Skippy.NextEpisode.Visible is true, and closed by another (1176) when it no longer is (or
the player controls / another dialog come up). Skin settings > Skippy: the skin's skip button also hands the prompt
over, in Fused Glass only (the other themes keep Skippy's own popup). Play now / Continue and Close / Stop call
RunScript(service.skippy,next_episode_play|close); Back is Close. The bar under the picture is the countdown gone:
Skippy drives control 30 every video frame (Skippy.SkinNextEpisodeProgress.*), the <info> bar shows until it starts.

Run from the skin folder; safe to run again (rewrites the three windows, patches the rest once)."""
import io
import os
import re
import sys

from PIL import Image, ImageDraw

D = '1080i'
H = 'Window(Home).Property(Skippy.%s)'
ON = 'Skin.HasSetting(aeon.skippy.button) + Skin.HasSetting(aeon.fglass)'
DIALOGS = ('videoosd', 'osdvideosettings', 'osdaudiosettings', 'osdsubtitlesettings', 'videobookmarks', 'playerprocessinfo', 'subtitlesearch',
           'selectdialog', 'contextmenu', 'sliderdialog', 'pvrosdchannels', 'pvrchannelguide', 'fullscreeninfo', 'yesnodialog', 'okdialog')
WANTED = ('Window.IsActive(fullscreenvideo) + Player.HasVideo + %s + String.IsEqual(%s,true) + String.IsEqual(%s,true)'
          ' + !String.IsEqual(Window(Home).Property(aeon.un.hidden),Player.FilenameAndPath) + ![%s]'
          % (ON, H % 'SkinNextEpisode', H % 'NextEpisode.Visible', ' | '.join('Window.IsVisible(%s)' % d for d in DIALOGS)))


BAR_FRAMES = 421
CD = 'Addon.SettingBool(service.skippy,next_episode_popup_countdown)'


def bar_frames():
    """fg/unbarf/0..420 and fg/unbar/0..100: the card's 288 x 6 bar filled that far (rounded ends), and the same
    numbered the other way round (…r) for a countdown."""
    import shutil
    for name, n in (('unbarf', BAR_FRAMES), ('unbar', 101)):
        d = os.path.join('media', 'fg', name)
        os.makedirs(d, exist_ok=True)
        for k in range(n):
            fill = round(288 * k / (n - 1))
            im = Image.new('L', (288 * 4, 6 * 4), 0)
            if fill:
                ImageDraw.Draw(im).rounded_rectangle([0, 0, max(fill * 4, 6 * 4) - 1, 6 * 4 - 1], 3 * 4, fill=255)
            out = Image.new('RGBA', (288, 6), (255, 255, 255, 0))
            out.putalpha(im.resize((288, 6), Image.LANCZOS))
            out.save(os.path.join(d, '%d.png' % k), optimize=True)
        r = d + 'r'
        os.makedirs(r, exist_ok=True)
        for k in range(n):
            shutil.copyfile(os.path.join(d, '%d.png' % (n - 1 - k)), os.path.join(r, '%d.png' % k))


def mask(w, h, r):
    im = Image.new('L', (w * 4, h * 4), 0)
    ImageDraw.Draw(im).rounded_rectangle([0, 0, w * 4 - 1, h * 4 - 1], r * 4, fill=255)
    out = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    out.putalpha(im.resize((w, h), Image.LANCZOS))
    out.save(os.path.join('media', 'fg', 'm%dx%d.png' % (w, h)), optimize=True)


def img(x, y, w, h, tex, col=None, border=None, extra=''):
    return ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><texture%s%s>%s</texture>%s</control>'
            % (x, y, w, h, ' border="%d"' % border if border else '', ' colordiffuse="%s"' % col if col else '', tex, extra))


def lbl(x, y, w, h, label, font, col, extra=''):
    return ('<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><aligny>center</aligny><font>%s</font>'
            '<textcolor>%s</textcolor><label>%s</label>%s</control>' % (x, y, w, h, font, col, label, extra))


def button(cid, label, action):
    hide = 'SetProperty(aeon.un.hidden,$INFO[Player.FilenameAndPath],home)'
    return ('<control type="button" id="%d"><width min="120" max="270">auto</width><height>48</height><label>%s</label><font>pl_ui_22_semibold</font>'
            '<textoffsetx>22</textoffsetx><align>center</align><aligny>center</aligny><textcolor>ffffffff</textcolor><focusedcolor>fg_ink</focusedcolor>'
            '<texturefocus border="24" colordiffuse="ffffffff">fg/r24.png</texturefocus><texturenofocus border="24" colordiffuse="24ffffff">fg/r24.png</texturenofocus>'
            '<onclick>%s</onclick><onclick>RunScript(service.skippy,%s)</onclick><onclick>Dialog.Close(1174,true)</onclick>'
            '<onback>%s</onback><onback>RunScript(service.skippy,next_episode_close)</onback><onback>Dialog.Close(1174,true)</onback>'
            '<onup>noop</onup><ondown>noop</ondown></control>' % (cid, label, hide, action, hide))


def card():
    x, y, w, h = 1132, 754, 668, 254
    body = img(-40, -40, w + 80, h + 80, 'fg/sh28.png', '$VAR[FG_PanelSh_8c]', 68)
    body += img(0, 0, w, h, 'fg/r28.png', 'fg_frost', 28) + img(0, 0, w, h, 'fg/e28.png', 'fg_edge', 28)
    # the picture and the countdown gone under it
    body += ('<control type="image"><left>22</left><top>22</top><width>320</width><height>180</height><aspectratio scalediffuse="false">scale</aspectratio>'
             '<texture background="true" diffuse="fg/m320x180.png">$VAR[FG_UN_Thumb]</texture></control>')
    # 0.53.2: the bar is a picture sequence (fg/unbar*: played or, when Skippy's popup counts down, left), stepped by
    # Skippy's frame while it drives the card; control 30 is the progress control Skippy drives (it stays hidden)
    body += img(38, 184, 288, 6, 'fg/pillh.png', '59ffffff', extra='').replace('<texture colordiffuse', '<texture border="3,0,3,0" colordiffuse')
    body += img(38, 184, 288, 6, '$VAR[FG_UN_BarTex]', 'fg_mark')
    body += ('<control type="progress" id="30"><left>38</left><top>184</top><width>288</width><height>6</height>'
             '<texturebg colordiffuse="00ffffff">fg/pillh.png</texturebg><midtexture colordiffuse="00ffffff">fg/pillh.png</midtexture></control>')
    body += lbl(22, 210, 320, 30, '$INFO[%s]' % (H % 'NextEpisode.Countdown'), 'pl_small_20_semibold', 'b3ffffff')
    # heading, show and episode, title, the buttons
    body += lbl(366, 22, 280, 24, '[UPPERCASE]$INFO[%s][/UPPERCASE]' % (H % 'NextEpisode.Heading'), 'pl_cap_16', 'a3ffffff')
    body += lbl(366, 50, 280, 28, '$VAR[FG_UN_Show]', 'pl_small_20_semibold', 'ccffffff')
    body += ('<control type="label"><left>366</left><top>80</top><width>280</width><height>66</height><aligny>top</aligny><font>pl_ui_24_bold</font>'
             '<textcolor>ffffffff</textcolor><wrapmultiline>true</wrapmultiline><label>$VAR[FG_UN_Title]</label></control>')
    body += ('<control type="grouplist" id="10"><left>366</left><top>186</top><width>280</width><height>48</height><orientation>horizontal</orientation><itemgap>10</itemgap>'
             '<onup>noop</onup><ondown>noop</ondown>%s%s</control>'
             % (button(11, '$INFO[%s]' % (H % 'NextEpisode.PlayLabel'), 'next_episode_play'), button(12, '$INFO[%s]' % (H % 'NextEpisode.CloseLabel'), 'next_episode_close')))
    return ('''<?xml version="1.0" encoding="UTF-8"?>
<!-- GENERATED by _src/fg_upnext.py (0.52.5): Skippy's next episode prompt as the Fused Glass Up next card. Opened by
     Custom_1175 while Skippy.NextEpisode.Visible is true, closed by Custom_1176. -->
<window type="dialog" id="1174">
	<zorder>2</zorder>
	<defaultcontrol always="true">11</defaultcontrol>
	<onload>SetFocus(11)</onload>
	<controls>
		<control type="group">
			<left>%d</left><top>%d</top><width>%d</width><height>%d</height>
			<animation type="WindowOpen" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="slide" start="140,0" end="0,0" time="320" tween="cubic" easing="out"/><effect type="fade" start="0" end="100" time="220"/></animation>
			<animation type="WindowClose"><effect type="fade" start="100" end="0" time="200"/></animation>
			%s
		</control>
	</controls>
</window>
''' % (x, y, w, h, body))


VARS = '''	<!-- ===== Up next card (0.52.5, _src/fg_upnext.py) -->
	<variable name="FG_UN_Thumb">
		<value condition="!String.IsEmpty(Window(Home).Property(Skippy.NextEpisode.Thumb))">$INFO[Window(Home).Property(Skippy.NextEpisode.Thumb)]</value>
		<value condition="!String.IsEmpty(Player.Art(fanart))">$INFO[Player.Art(fanart)]</value>
		<value>$INFO[Player.Art(thumb)]</value>
	</variable>
	<variable name="FG_UN_BarTex">
		<value condition="String.IsEqual(Window(Home).Property(Skippy.NextEpisode.SmoothProgress),true) + Addon.SettingBool(service.skippy,next_episode_popup_countdown)">fg/unbarfr/$INFO[Window(Home).Property(Skippy.NextEpisode.Frame)].png</value>
		<value condition="String.IsEqual(Window(Home).Property(Skippy.NextEpisode.SmoothProgress),true)">fg/unbarf/$INFO[Window(Home).Property(Skippy.NextEpisode.Frame)].png</value>
		<value condition="Addon.SettingBool(service.skippy,next_episode_popup_countdown)">fg/unbarr/$INFO[Window(Home).Property(Skippy.NextEpisode.Progress)].png</value>
		<value>fg/unbar/$INFO[Window(Home).Property(Skippy.NextEpisode.Progress)].png</value>
	</variable>
	<variable name="FG_UN_Show">
		<value>$INFO[Window(Home).Property(Skippy.NextEpisode.ShowTitle)]</value>
	</variable>
	<variable name="FG_UN_Title">
		<value condition="!String.IsEmpty(Window(Home).Property(Skippy.NextEpisode.Title)) + !String.IsEmpty(Window(Home).Property(Skippy.NextEpisode.Episode))">S$INFO[Window(Home).Property(Skippy.NextEpisode.Season)] E$INFO[Window(Home).Property(Skippy.NextEpisode.Episode)]  ·  $INFO[Window(Home).Property(Skippy.NextEpisode.Title)]</value>
		<value condition="!String.IsEmpty(Window(Home).Property(Skippy.NextEpisode.Title))">$INFO[Window(Home).Property(Skippy.NextEpisode.Title)]</value>
		<value>$INFO[Window(Home).Property(Skippy.NextEpisode.Label)]</value>
	</variable>
'''

HAND = [('<onload condition="Skin.HasSetting(aeon.skippy.button)">SetProperty(Skippy.SkinSkipButton,true,home)</onload>',
         '<onload condition="%s">SetProperty(Skippy.SkinNextEpisode,true,home)</onload>\n'
         '\t<onload condition="!%s">ClearProperty(Skippy.SkinNextEpisode,home)</onload>\n'
         '\t<onload condition="%s">SetProperty(Skippy.SkinNextEpisodeProgress.Window,11174,home)</onload>\n'
         '\t<onload condition="%s">SetProperty(Skippy.SkinNextEpisodeProgress.Control,30,home)</onload>\n'
         '\t<onload condition="!%s">ClearProperty(Skippy.SkinNextEpisodeProgress.Window,home)</onload>\n'
         '\t<onload condition="!%s">ClearProperty(Skippy.SkinNextEpisodeProgress.Control,home)</onload>' % ((('[' + ON + ']'),) * 6))]


def main():
    mask(320, 180, 16)
    bar_frames()
    io.open(os.path.join(D, 'Custom_1174_UpNext.xml'), 'w', encoding='utf-8', newline='\n').write(card())
    # 0.53.2: ask Skippy for a frame number on the card too (its bar is a picture sequence)
    for f in ('Home.xml', 'VideoFullScreen.xml'):
        p = os.path.join(D, f)
        t = io.open(p, encoding='utf-8').read()
        if 'Skippy.SkinNextEpisodeProgress.Frames' not in t:
            on, off = ('<onload condition="[%s]">SetProperty(Skippy.SkinNextEpisodeProgress.Control,30,home)</onload>' % ON,
                       '<onload condition="![%s]">ClearProperty(Skippy.SkinNextEpisodeProgress.Control,home)</onload>' % ON)
            assert t.count(on) == 1 and t.count(off) == 1, f
            t = t.replace(on, on + '\n\t<onload condition="[%s]">SetProperty(Skippy.SkinNextEpisodeProgress.Frames,%d,home)</onload>' % (ON, BAR_FRAMES))
            t = t.replace(off, off + '\n\t<onload condition="![%s]">ClearProperty(Skippy.SkinNextEpisodeProgress.Frames,home)</onload>' % ON)
            io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    io.open(os.path.join(D, 'Custom_1175_UpNextOpen.xml'), 'w', encoding='utf-8', newline='\n').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<!-- GENERATED by _src/fg_upnext.py: the Up next card\'s opener (as Custom_1171 for the skip pill). -->\n'
        '<window type="dialog" id="1175">\n\t<visible>%s + !Window.IsVisible(1174)</visible>\n\t<onload>ActivateWindow(1174)</onload>\n\t<controls/>\n</window>\n' % WANTED)
    io.open(os.path.join(D, 'Custom_1176_UpNextClose.xml'), 'w', encoding='utf-8', newline='\n').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<!-- GENERATED by _src/fg_upnext.py: the Up next card\'s closer (as Custom_1172 for the skip pill). -->\n'
        '<window type="dialog" id="1176">\n\t<visible>Window.IsVisible(1174) + ![%s]</visible>\n\t<onload>Dialog.Close(1174,true)</onload>\n\t<controls/>\n</window>\n' % WANTED)
    # the card's variables in the Fused Glass includes (once)
    p = os.path.join(D, 'Includes_Fused.xml')
    t = io.open(p, encoding='utf-8').read()
    t = re.sub(r'\t<!-- ===== Up next card \(0\.52\.5.*?(?=\t<variable name="FG_UN_Title">)', '', t, flags=re.S)
    t = re.sub(r'\t<variable name="FG_UN_Title">.*?</variable>\n', '', t, flags=re.S)
    t = t.replace('</includes>', VARS + '</includes>')
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    # the skip pill gives way while the card is up
    edits = {'Custom_1171_SkippyOpen.xml': [(' + !Window.IsVisible(1167)</visible>', ' + !Window.IsVisible(1167) + !Window.IsVisible(1174)</visible>')],
             'Custom_1172_SkippyClose.xml': [('<visible>Window.IsVisible(1167) + ![', '<visible>Window.IsVisible(1167) + [Window.IsVisible(1174) | !['),
                                             (']]</visible>', ']]]</visible>')]}
    for f, pairs in edits.items():
        p = os.path.join(D, f)
        t = io.open(p, encoding='utf-8').read()
        if 'IsVisible(1174)' not in t:
            for old, new in pairs:
                assert t.count(old) == 1, (f, old)
                t = t.replace(old, new)
            io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    # Home and the full-screen video hand the prompt over (the skip pill's setting, Fused Glass only)
    for f in ('Home.xml', 'VideoFullScreen.xml'):
        p = os.path.join(D, f)
        t = io.open(p, encoding='utf-8').read()
        if 'Skippy.SkinNextEpisode' not in t:
            old, new = HAND[0]
            assert t.count(old) == 1, f
            t = t.replace(old, old + '\n\t' + new)
            io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    # the settings row turns both on and off at once
    p = os.path.join(D, 'SkinSettings.xml')
    t = io.open(p, encoding='utf-8').read()
    if 'Skippy.SkinNextEpisode' not in t:
        old = '<onclick condition="Skin.HasSetting(aeon.skippy.button)">ClearProperty(Skippy.SkinSkipButton,home)</onclick>'
        assert t.count(old) == 1
        t = t.replace(old, old + '<onclick condition="Skin.HasSetting(aeon.skippy.button)">ClearProperty(Skippy.SkinNextEpisode,home)</onclick>')
        old = '<onclick condition="![Skin.HasSetting(aeon.skippy.button)]">SetProperty(Skippy.SkinSkipButton,true,home)</onclick>'
        assert t.count(old) == 1
        t = t.replace(old, old + '<onclick condition="![Skin.HasSetting(aeon.skippy.button)] + Skin.HasSetting(aeon.fglass)">SetProperty(Skippy.SkinNextEpisode,true,home)</onclick>')
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print('up next card written')


if __name__ == '__main__':
    sys.exit(main())
