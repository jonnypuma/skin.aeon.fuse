"""0.45.1 Fused Glass player card: the button row (FG_OSDRow in 1080i/Includes_FusedPlayer.xml), generated.
Run from the skin folder.

The buttons sit in groups inside the grouplists 201 / 202, and a grouplist cannot move focus between buttons nested in
groups, so every button gets its own Left / Right that skip the buttons hidden for what is playing (Live TV had no way
off Stop). Live TV (mockup LiveTVOSD): channel down, play / pause, channel up, record on the left; subtitles, audio,
guide (the Live TV guide as a sheet over the picture, 0.46.0), channels, groups (the channel list with its group
pill in focus), info, PPI / stats on the right. Films and
episodes keep previous, rewind, play, forward, next, stop and subtitles, audio, video, chapters, info, stats / PPI.
Also: the spinning disc stops on pause instead of turning back (reversible="false"), fg chevron_up icon."""
import io
import os
import re

from PIL import Image

PLAYER = '1080i/Includes_FusedPlayer.xml'
LIVE = '$EXP[FG_OSDLive]'
PPI = 'System.AddonIsEnabled(script.tinyppi)'
L = lambda n: '$LOCALIZE[%d]' % n
B = lambda s: '[B]%s[/B]' % s

# id, label, icon, onclick (list), visible, extra (icon size / colour)
LEFT = [
    (610, B('$LOCALIZE[19029] -'), 'aeon/icons/chevron_down.png', ['Action(ChannelDown)'], LIVE, {}),
    (600, B(L(31121)), 'aeon/icons/prev.png', ['PlayerControl(Previous)'], '$EXP[OSD_HasPrevNext] + !' + LIVE, {}),
    (601, B(L(31122)), 'aeon/icons/rewind.png', ['PlayerControl(Rewind)'], 'Player.SeekEnabled + !' + LIVE, {}),
    (602, '$VAR[Aeon_OSD_LblPlay]', '$VAR[Aeon_OSD_Play]', ['PlayerControl(Play)'], '[!' + LIVE + '] | Player.PauseEnabled | Player.Paused | PVR.IsTimeShift', {}),  # 0.46.1: Live TV when Kodi can pause it (time-shift)
    (606, B(L(31125)), 'aeon/icons/forward.png', ['PlayerControl(Forward)'], 'Player.SeekEnabled + !' + LIVE, {}),
    (611, B('$LOCALIZE[19029] +'), 'aeon/icons/chevron_up.png', ['Action(ChannelUp)'], LIVE, {}),
    (607, B(L(31126)), 'aeon/icons/next.png', ['PlayerControl(Next)'], '$EXP[OSD_HasPrevNext] + !' + LIVE, {}),
    (612, B(L(264)), 'fg/circle.png', ['PlayerControl(Record)'], LIVE, {'isz': 22, 'il': 29, 'it': 27, 'col': 'ffe5484d', 'fcol': 'ffe5484d'}),
    (603, B(L(31124)), 'aeon/icons/stop.png', ['PlayerControl(Stop)'], '', {}),                                # 0.46.0: Live TV too
]
RIGHT = [
    (70046, '$VAR[Aeon_OSD_LblSubs]', 'aeon/icons/subtitles.png', ['ActivateWindow(osdsubtitlesettings)'], '', {}),
    (70049, '$VAR[Aeon_OSD_LblAudio]', 'aeon/icons/audio.png', ['ActivateWindow(osdaudiosettings)'], '', {}),
    (70048, '$VAR[Aeon_OSD_LblVideo]', 'common/aeon_ic_screen.png', ['ActivateWindow(osdvideosettings)'], '!' + LIVE, {}),
    (70053, B(L(19069)), 'aeon/icons/sidebar.png', ['SetProperty(aeon.guide.osd,1,home)', 'Dialog.Close(all,true)', 'ActivateWindow(TVGuide)'], LIVE, {}),
    (70054, B(L(19019)), 'aeon/icons/lines.png', ['ActivateWindow(pvrosdchannels)'], LIVE, {}),
    (70055, B(L(19146)), 'aeon/icons/layers.png', ['SetProperty(aeon.osdch.groups,1,home)', 'ActivateWindow(pvrosdchannels)'], LIVE, {}),  # 0.46.0
    (70044, '$VAR[Aeon_OSD_LblChapter]', 'aeon/icons/chapters.png', ['ActivateWindow(videobookmarks)'], '$EXP[OSD_HasChapters] + !' + LIVE, {}),
    (70043, B(L(31351)), 'aeon/icons/info.png', ['Action(Info,fullscreenvideo)'], '', {}),
    (70051, B(L(31352)), 'common/aeon_ic_stats.png', ['Action(PlayerProcessInfo)'], '!' + PPI, {}),
    (70052, B(L(31352)), 'aeon/icons/ppi.png', ['CancelAlarm(osd_timeout,true)', 'RunScript(script.tinyppi,dialog)'], PPI,
     {'isz': 56, 'il': 12, 'it': 10}),
]
ALL = LEFT + RIGHT


def nav(tag, start, step):
    """Conditional moves to the next visible button in the cycle (step +1 right, -1 left)."""
    out, seen = '', []
    k = start
    for _ in range(len(ALL) - 1):
        k = (k + step) % len(ALL)
        ident, vis = ALL[k][0], ALL[k][4]
        cond = ' + '.join(['!%s' % ('[%s]' % s) for s in seen] + (['[%s]' % vis] if vis else []))
        out += ('<%s condition="%s">%d</%s>' % (tag, cond, ident, tag)) if cond else '<%s>%d</%s>' % (tag, ident, tag)
        if not vis:
            break
        seen.append(vis)
    return out


def button(k):
    ident, label, icon, clicks, vis, extra = ALL[k]
    isz, il, it = extra.get('isz', 34), extra.get('il', 23), extra.get('it', 21)
    col, fcol = extra.get('col', 'ffffffff'), extra.get('fcol', 'aeon_onbar')
    return '''				<control type="group">
					<width>80</width><height>110</height>
					<visible>%(vis)s</visible>
					<control type="image"><left>8</left><top>6</top><width>64</width><height>64</height><texture colordiffuse="1fffffff">fg/circle.png</texture><visible>!Control.HasFocus(%(id)d)</visible></control>
					<control type="button" id="%(id)d">
						<left>2</left><top>0</top><width>76</width><height>76</height><label></label>
						<texturefocus colordiffuse="ffffffff">fg/circle.png</texturefocus><texturenofocus />
						%(clicks)s
						%(right)s
						%(left)s
						<onup condition="Player.SeekEnabled">87</onup>
						<ondown condition="$EXP[OSD_HasChapters]">ActivateWindow(videobookmarks)</ondown>
						<ondown condition="!$EXP[OSD_HasChapters]">noop</ondown>
					</control>
					<control type="image"><left>%(il)d</left><top>%(it)d</top><width>%(isz)d</width><height>%(isz)d</height><aspectratio>keep</aspectratio><texture colordiffuse="%(col)s">%(icon)s</texture><visible>!Control.HasFocus(%(id)d)</visible></control>
					<control type="image"><left>%(il)d</left><top>%(it)d</top><width>%(isz)d</width><height>%(isz)d</height><aspectratio>keep</aspectratio><texture colordiffuse="%(fcol)s">%(icon)s</texture><visible>Control.HasFocus(%(id)d)</visible></control>
					<control type="label">
						<left>-260</left><top>80</top><width>600</width><height>28</height><align>center</align><aligny>center</aligny>
						<font>pl_small_20</font><textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><scroll>true</scroll>
						<label>[UPPERCASE]%(label)s[/UPPERCASE]</label>
						<visible>Control.HasFocus(%(id)d)</visible>
					</control>
				</control>
''' % {'vis': vis or 'true', 'id': ident, 'clicks': ''.join('<onclick>%s</onclick>' % c for c in clicks),
       'right': nav('onright', k, 1), 'left': nav('onleft', k, -1), 'il': il, 'it': it, 'isz': isz, 'col': col, 'fcol': fcol,
       'icon': icon, 'label': label}


ROW = '''	<include name="FG_OSDRow">
		<!-- written by _src/fg_osdrow.py (0.45.1): every button moves Left / Right itself, past the hidden ones -->
		<control type="group" id="200">
			<left>0</left><top>926</top><width>1920</width><height>110</height>
			<control type="grouplist" id="201">
				<left>0</left><top>0</top><width>1150</width><height>110</height>
				<orientation>horizontal</orientation><itemgap>0</itemgap><usecontrolcoords>true</usecontrolcoords>
				<control type="group"><width>380</width><height>110</height></control>
%s			</control>
			<control type="grouplist" id="202">
				<left>770</left><top>0</top><width>1150</width><height>110</height>
				<orientation>horizontal</orientation><align>right</align><itemgap>0</itemgap><usecontrolcoords>true</usecontrolcoords>
%s				<control type="group"><width>120</width><height>110</height></control>
			</control>
		</control>
	</include>
''' % (''.join(button(k) for k in range(len(LEFT))), ''.join(button(k) for k in range(len(LEFT), len(ALL))))

t = io.open(PLAYER, encoding='utf-8').read()
start = t.index('\t<include name="FG_OSDRow">')
end = t.index('\n\t</include>\n', start) + len('\n\t</include>\n')     # its own closing tag: the only one at one tab
t = t[:start] + ROW + t[end:]
# the disc stops on pause instead of turning back
t = t.replace('<animation type="Conditional" condition="Player.Playing + !Player.Paused + !Skin.HasSetting(aeon.reducemotion)" loop="true"><effect type="rotate"',
              '<animation type="Conditional" reversible="false" condition="Player.Playing + !Player.Paused + !Skin.HasSetting(aeon.reducemotion)" loop="true"><effect type="rotate"')
io.open(PLAYER, 'w', encoding='utf-8', newline='\n').write(t)

up = os.path.join('media', 'aeon', 'icons', 'chevron_up.png')
if not os.path.exists(up):
    Image.open(os.path.join('media', 'aeon', 'icons', 'chevron_down.png')).transpose(Image.FLIP_TOP_BOTTOM).save(up)
import xml.etree.ElementTree as ET
ET.parse(PLAYER)
print('ok')
