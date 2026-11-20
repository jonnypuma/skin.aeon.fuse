# -*- coding: utf-8 -*-
"""0.56.45 music player controls (MusicOSD.xml): the album track list on the right (the user, 2026-11-18: "there is
space left on the right side for an overlay where we could put the tracklisting for the album playing ... navigate to
this tracklisting and choose which track to play ... a left arrow icon and a right arrow icon to cycle through albums
by the same artist. when on the left arrow it would then show the name of the album it would open").

With the controls open Now playing shrinks to 84 % from (140,190) (Includes_Aeon_Music.xml), ending at x 1484: the
panel takes 1516-1780 (the progress line's right end), y 190-778, as a card of the theme (Aeon_Glass). Top: the
arrows (702 / 703, RunScript(script.aeon.helper,osdalbum,prev|next)) with the artist between them; the album's name
and year under them (on an arrow: the album it opens); then list 701, musicdb://albums/<aeon.osd.alb.id>/ (target
music, a plain text: Kodi reads targets off the main thread), OK = RunScript(script.aeon.helper,osdplay,<songid>):
the album from that song. The playing song is marked. Up from the seek bar goes to the list; Down from the list to the
seek bar, Left to the controls. Library songs only. Helper 0.3.111 (resources/lib/osdalbums.py). Repeatable."""
import io
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'MusicOSD.xml')
MARK = '<!-- 0.56.45 osdtracks -->'
HP = 'Window(Home).Property(aeon.osd.alb.%s)'
SHOW = 'Integer.IsGreater(MusicPlayer.DBID,0) + !String.IsEmpty(%s)' % (HP % 'id')
PLAYING = 'ListItem.IsPlaying'       # (String.IsEqual(ListItem.DBID,MusicPlayer.DBID) marked every row on the box)


W = 324          # 0.56.46: wider (1516-1840; the user: "you have space on the right side")


def arrow(cid, left, icon, direction, other):
    """0.56.46: a white circle under the focused arrow (a button cannot draw a $VAR focus texture)"""
    on = '!String.IsEmpty(%s)' % (HP % direction)
    return """
			<control type="image"><left>%(left)d</left><top>12</top><width>44</width><height>44</height><texture colordiffuse="ffffffff">fg/circle.png</texture><visible>Control.HasFocus(%(cid)d)</visible></control>
			<control type="button" id="%(cid)d">
				<left>%(left)d</left><top>12</top><width>44</width><height>44</height>
				<label></label><texturefocus /><texturenofocus />
				<onleft>%(other_l)s</onleft><onright>%(other_r)s</onright><onup>noop</onup><ondown>701</ondown>
				<onclick condition="%(on)s">RunScript(script.aeon.helper,osdalbum,%(direction)s)</onclick>
			</control>
			<control type="image"><left>%(il)d</left><top>22</top><width>24</width><height>24</height><aspectratio>keep</aspectratio><texture colordiffuse="ccffffff">%(icon)s</texture><visible>!Control.HasFocus(%(cid)d) + %(on)s</visible></control>
			<control type="image"><left>%(il)d</left><top>22</top><width>24</width><height>24</height><aspectratio>keep</aspectratio><texture colordiffuse="33ffffff">%(icon)s</texture><visible>!Control.HasFocus(%(cid)d) + !%(on)s</visible></control>
			<control type="image"><left>%(il)d</left><top>22</top><width>24</width><height>24</height><aspectratio>keep</aspectratio><texture colordiffuse="ff0f1115">%(icon)s</texture><visible>Control.HasFocus(%(cid)d)</visible></control>""" % {
        'cid': cid, 'left': left, 'il': left + 10, 'icon': icon, 'direction': direction, 'on': on,
        'other_l': 'noop' if direction == 'prev' else str(other), 'other_r': str(other) if direction == 'prev' else 'noop'}


def row(focused):
    w = W - 24
    bar = ('<control type="image"><left>0</left><top>0</top><width>%d</width><height>44</height><texture border="20" colordiffuse="$VAR[Aeon_MenuFocusColR]">$VAR[Aeon_MenuFocusTex]</texture><visible>Control.HasFocus(701)</visible></control>' % w
           if focused else '')
    ink = '$VAR[Aeon_OnBarInk]' if focused else 'ffffffff'
    dim = '$VAR[Aeon_OnBarInk3]' if focused else '80ffffff'
    return """%(bar)s
					<control type="label"><left>12</left><top>0</top><width>36</width><height>44</height><aligny>center</aligny><font>pl_small_20</font><textcolor>%(dim)s</textcolor><label>$INFO[ListItem.TrackNumber]</label><visible>!%(playing)s</visible></control>
					<control type="image"><left>14</left><top>12</top><width>20</width><height>20</height><texture colordiffuse="%(mark)s">common/aeon_eq_anim.gif</texture><visible>%(playing)s</visible></control>
					<control type="label"><left>48</left><top>0</top><width>%(tw)d</width><height>44</height><aligny>center</aligny><font>pl_small_20</font><textcolor>%(ink)s</textcolor><scroll>%(scroll)s</scroll><label>$INFO[ListItem.Title]</label></control>""" % {
        'bar': bar, 'ink': ink, 'dim': dim, 'playing': PLAYING, 'scroll': 'true' if focused else 'false', 'tw': w - 60,
        'mark': '$VAR[Aeon_OnBarInk]' if focused else '$VAR[Aeon_Accent]'}


def panel():
    """0.56.46: the album shown keeps its title over the list; an arrow's album shows between the arrows (where the
    artist is) while it has the focus"""
    inner = W - 28
    between = ('<control type="label"><left>60</left><top>12</top><width>%d</width><height>44</height><align>center</align><aligny>center</aligny>'
               '<font>%%s</font><textcolor>%%s</textcolor><scroll>true</scroll><label>%%s</label><visible>%%s</visible></control>' % (W - 120))
    return """
		%(mark)s
		<control type="group" id="700">
			<left>1516</left><top>190</top><width>%(w)d</width><height>588</height>
			<visible>%(show)s</visible>
			<animation effect="fade" start="0" end="100" time="200" delay="150">Visible</animation>
			<animation effect="fade" start="100" end="0" time="150">Hidden</animation>
			<control type="group"><include>Aeon_Glass</include></control>%(left)s%(right)s
			%(artist)s
			%(prev)s
			%(next)s
			<control type="label"><left>14</left><top>62</top><width>%(inner)d</width><height>60</height><font>pl_small_20_bold</font><textcolor>ffffffff</textcolor><wrapmultiline>true</wrapmultiline><label>$INFO[%(name)s]</label></control>
			<control type="label"><left>14</left><top>120</top><width>%(inner)d</width><height>24</height><font>pl_small_20</font><textcolor>80ffffff</textcolor><label>$INFO[%(year)s]</label></control>
			<control type="image"><left>14</left><top>152</top><width>%(inner)d</width><height>1</height><texture colordiffuse="26ffffff">common/white.png</texture></control>
			<control type="list" id="701">
				<left>12</left><top>162</top><width>%(lw)d</width><height>414</height>
				<onup>702</onup><ondown>87</ondown><onleft>602</onleft><onright>noop</onright>
				<scrolltime tween="cubic" easing="out">200</scrolltime>
				<orientation>vertical</orientation>
				<itemlayout width="%(lw)d" height="46">%(item)s
				</itemlayout>
				<focusedlayout width="%(lw)d" height="46">%(focus)s
				</focusedlayout>
				<content target="music" sortby="track" sortorder="ascending">$VAR[Aeon_OsdAlbumPath]</content>
				<onclick>RunScript(script.aeon.helper,osdplay,$INFO[ListItem.DBID])</onclick>
			</control>
		</control>""" % {
        'mark': MARK, 'show': SHOW, 'w': W, 'inner': inner, 'lw': W - 24, 'name': HP % 'name', 'year': HP % 'year',
        'left': arrow(702, 12, 'aeon/icons/chevron_left.png', 'prev', 703),
        'right': arrow(703, W - 56, 'aeon/icons/chevron_right.png', 'next', 702),
        'artist': between % ('pl_cap_16', '99ffffff', '[UPPERCASE]$INFO[MusicPlayer.AlbumArtist][/UPPERCASE]',
                             '!Control.HasFocus(702) + !Control.HasFocus(703)'),
        'prev': between % ('pl_small_20', 'ffffffff', '$INFO[%s]' % (HP % 'prev.name'), 'Control.HasFocus(702)'),
        'next': between % ('pl_small_20', 'ffffffff', '$INFO[%s]' % (HP % 'next.name'), 'Control.HasFocus(703)'),
        'item': row(False), 'focus': row(True)}


def main():
    t = io.open(P, encoding='utf-8').read()
    if MARK in t:
        print('osdtracks: already there')
        return
    anchor = '\t\t<!-- elapsed / total and the seek bar, above the controls, same width -->'
    assert anchor in t
    t = t.replace(anchor, panel().lstrip('\n') + '\n' + anchor, 1)
    old = '\t\t\t<onup>noop</onup>\n\t\t\t<ondown>602</ondown>\n\t\t\t<visible>Player.SeekEnabled</visible>'
    assert old in t
    t = t.replace(old, '\t\t\t<onup condition="Control.IsVisible(700)">701</onup><onup>noop</onup>\n\t\t\t<ondown>602</ondown>\n\t\t\t<visible>Player.SeekEnabled</visible>')
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    var_path()
    print('osdtracks: the album panel in MusicOSD.xml')


def var_path():
    """the list's path: never musicdb://albums// (every album: the controls load before the helper names an album, and
    that long job kept the list busy after the album was set), the always-empty playlist until then"""
    sub = os.path.join(os.path.dirname(P), 'Includes_Aeon_Sub.xml')
    x = io.open(sub, encoding='utf-8').read()
    if 'name="Aeon_OsdAlbumPath"' in x:
        return
    i = x.index('\t<variable name="Aeon_VOS_ratings">')
    x = x[:i] + ('\t<!-- 0.56.45 osdtracks: the album track list in the music player controls -->\n'
                 '\t<variable name="Aeon_OsdAlbumPath">\n'
                 '\t\t<value condition="String.IsEmpty(Window(Home).Property(aeon.osd.alb.id))">special://skin/shortcuts/customrows-none.xsp</value>\n'
                 '\t\t<value>musicdb://albums/$INFO[Window(Home).Property(aeon.osd.alb.id)]/</value>\n'
                 '\t</variable>\n') + x[i:]
    io.open(sub, 'w', encoding='utf-8', newline='\n').write(x)


if __name__ == '__main__':
    main()
