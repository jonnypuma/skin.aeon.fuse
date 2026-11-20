# -*- coding: utf-8 -*-
"""0.46.0 Fused Glass Live TV (mockups LiveTVChannels, LiveTVGuide, LiveTVGuideOverlay on the refinements canvas).
Fused Glass only; the other themes keep Misc_PVRFrame's tab card, Misc_PVRList and the old guide.

- FG_PVRTabs: the areas in one glass pill at the top left (TV / Radio, Channels, Groups, Guide, Recordings, Timers,
  Timer rules, Search). Groups (106, only where a channel group applies: Channels and Guide) shows the group in use and
  opens Kodi's group chooser (SendClick(28)). Left / Right still move straight between the areas.
- FG_PVRChannels: Live TV > Channels as a list card (number, logo tile, channel, what is on, time and progress; the
  playing channel has a red dot) and a spotlight card (logo, now, progress, minutes left, plot, next, Watch / Record /
  Guide).
- FG_PVRGuideBack + FG_EpgGrid_fg / Misc_EPGLayouts_fg: Live TV > Guide: the programme in focus at the top, the playing
  picture in a tile, the grid in a card with the group pill; cells with a yellow focus ring.
- Guide over the playing channel: the player controls' guide button sets Window(Home).Property(aeon.guide.osd) and
  opens the guide; while it is set and video plays, the guide is a sheet over the full-screen picture (no tabs), the
  picture keeps playing above it, Back goes back to the picture (a 1 px button 6057 that switches to the picture as it gets focus).
Writes the FG_LIVETV block of Includes_Fused.xml and patches Includes_Misc.xml, MyPVRChannels.xml and MyPVRGuide.xml
(once). Run from the skin folder, then _src/fg_material.py."""
import io
import os
import re
import xml.etree.ElementTree as ET

D = '1080i'
FUSED = os.path.join(D, 'Includes_Fused.xml')
MISC = os.path.join(D, 'Includes_Misc.xml')
CHAN = os.path.join(D, 'MyPVRChannels.xml')
GUIDE = os.path.join(D, 'MyPVRGuide.xml')

OSD = '!String.IsEmpty(Window(Home).Property(aeon.guide.osd)) + Player.HasVideo'
RADIO = '!String.IsEmpty(Window.Property(IsRadio))'
TV = 'String.IsEmpty(Window.Property(IsRadio))'
INK = '$VAR[Aeon_OnBarInk]'
FOCUS = '$VAR[FG_PillFocusCol]'
RED = 'ffe5484d'


def glass(x, y, w, h, r, shadow='$VAR[FG_PanelSh_80]', sh=32, vis=''):
    """A frosted card: drop shadow, frost, edge."""
    v = '<visible>%s</visible>' % vis if vis else ''
    pad = 40
    return ('\t\t<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><texture border="%d" colordiffuse="%s">fg/sh%d.png</texture>%s</control>\n'
            '\t\t<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><texture border="%d" colordiffuse="fg_frost">fg/r%d.png</texture>%s</control>\n'
            '\t\t<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><texture border="%d" colordiffuse="fg_edge">fg/e%d.png</texture>%s</control>\n'
            % (x - pad, y - pad + 10, w + 2 * pad, h + 2 * pad, sh + pad, shadow, sh, v, x, y, w, h, r, r, v, x, y, w, h, r, r, v))


# ---------------------------------------------------------------------------------------------------------- the tabs
TABS = [  # id, area, label, x, width
    (100, 'Channels', '$LOCALIZE[19019]', 132, 158),
    (101, 'Guide', '$LOCALIZE[19069]', 624, 134),
    (102, 'Recordings', '$LOCALIZE[19017]', 762, 178),
    (103, 'Timers', '$LOCALIZE[19040]', 944, 134),
    (104, 'TimerRules', '$LOCALIZE[19138]', 1082, 178),
    (105, 'Search', '$LOCALIZE[137]', 1264, 134),
]
GROUPS_X, GROUPS_W = 294, 326           # 106, between Channels and Guide
SHIFT = GROUPS_W + 4                    # the tabs after it move left by this where there is no group
ORDER = ['Channels', 'Guide', 'Recordings', 'Timers', 'TimerRules', 'Search']


def area_open(area):
    return 'Window.IsActive(TV%s) | Window.IsActive(Radio%s)' % (area, area)


def go(area):
    """Open an area (focus stays on the tabs there: aeon.pvrnav)."""
    return ['SetProperty(aeon.pvrnav,1,home)', ('ReplaceWindow(TV%s)' % area, TV), ('ReplaceWindow(Radio%s)' % area, RADIO)]


def actions(tag, items, extra=''):
    out = ''
    for it in items:
        if isinstance(it, tuple):
            act, cond = it
            c = '[%s]%s' % (cond, (' + ' + extra) if extra else '')
            out += '<%s condition="%s">%s</%s>' % (tag, c, act, tag)
        else:
            out += ('<%s condition="%s">%s</%s>' % (tag, extra, it, tag)) if extra else '<%s>%s</%s>' % (tag, it, tag)
    return out


def tab(ident, area, label, x, w):
    i = ORDER.index(area)
    after_groups = i >= 1
    slide = ('\t\t\t\t<animation effect="slide" end="-%d,0" time="0" condition="!$PARAM[show_group]">Conditional</animation>\n' % SHIFT) if after_groups else ''
    # Left / Right: Channels -> Groups -> Guide where Groups shows; else straight to the next area
    if area == 'Channels':
        left = '<onleft>noop</onleft>'
        right = actions('onright', ['SetFocus(106)'], '$PARAM[show_group]') + actions('onright', go('Guide'), '!$PARAM[show_group]')
    elif area == 'Guide':
        left = actions('onleft', ['SetFocus(106)'], '$PARAM[show_group]') + actions('onleft', go('Channels'), '!$PARAM[show_group]')
        right = actions('onright', go('Recordings'))
    else:
        left = actions('onleft', go(ORDER[i - 1]))
        right = actions('onright', go(ORDER[i + 1])) if i + 1 < len(ORDER) else '<onright>noop</onright>'
    click = ('<onclick condition="%s + !Window.IsActive(TV%s)">ActivateWindow(TV%s)</onclick>'
             '<onclick condition="%s + !Window.IsActive(Radio%s)">ActivateWindow(Radio%s)</onclick>'
             '<onclick condition="%s">SetFocus(9100)</onclick>' % (TV, area, area, RADIO, area, area, area_open(area)))
    lab = '<control type="label"><width>%d</width><height>48</height><align>center</align><aligny>center</aligny><font>%s</font><textcolor>%s</textcolor><label>%s</label><visible>%s</visible></control>'
    return ('\t\t\t<control type="group">\n\t\t\t\t<left>%d</left><top>8</top>\n%s'
            '\t\t\t\t<control type="button" id="%d"><width>%d</width><height>48</height><label></label><texturefocus border="24" colordiffuse="%s">fg/r24.png</texturefocus><texturenofocus />'
            '%s%s%s<onup>noop</onup><ondown condition="Control.IsVisible(9001)">9001</ondown><ondown condition="!Control.IsVisible(9001) + Control.IsVisible(6056)">6056</ondown>'
            '<ondown condition="!Control.IsVisible(9001) + !Control.IsVisible(6056)">$PARAM[content_id]</ondown><onback>$PARAM[content_id]</onback></control>\n'
            '\t\t\t\t%s\n\t\t\t\t%s\n\t\t\t\t%s\n'
            '\t\t\t\t<control type="image"><left>%d</left><top>40</top><width>28</width><height>4</height><texture border="2" colordiffuse="fg_mark">fg/pill4.png</texture><visible>[%s] + !Control.HasFocus(%d)</visible></control>\n'
            '\t\t\t</control>\n'
            % (x, slide, ident, w, FOCUS, click, left, right,
               lab % (w, 'small_20_semibold', '9effffff', label, '![%s] + !Control.HasFocus(%d)' % (area_open(area), ident)),
               lab % (w, 'small_20_bold', 'ffffffff', label, '[%s] + !Control.HasFocus(%d)' % (area_open(area), ident)),
               lab % (w, 'small_20_bold', INK, label, 'Control.HasFocus(%d)' % ident),
               w // 2 - 14, area_open(area), ident))


def groups_tab():
    left = actions('onleft', [('SetFocus(100)', area_open('Channels'))]) + actions('onleft', go('Channels'), '!Window.IsActive(TVChannels) + !Window.IsActive(RadioChannels)')
    right = actions('onright', [('SetFocus(101)', area_open('Guide'))]) + actions('onright', go('Guide'), '!Window.IsActive(TVGuide) + !Window.IsActive(RadioGuide)')
    f = 'Control.HasFocus(106)'
    return ('\t\t\t<control type="group">\n\t\t\t\t<left>%d</left><top>8</top>\n\t\t\t\t<visible>$PARAM[show_group]</visible>\n'
            '\t\t\t\t<control type="image"><width>%d</width><height>48</height><texture border="24" colordiffuse="1affffff">fg/r24.png</texture><visible>!%s</visible></control>\n'
            '\t\t\t\t<control type="image"><width>%d</width><height>48</height><texture border="24" colordiffuse="2effffff">fg/e24.png</texture><visible>!%s</visible></control>\n'
            '\t\t\t\t<control type="button" id="106"><width>%d</width><height>48</height><label></label><texturefocus border="24" colordiffuse="%s">fg/r24.png</texturefocus><texturenofocus />'
            '<onclick>SendClick(28)</onclick>%s%s<onup>noop</onup><ondown condition="Control.IsVisible(9001)">9001</ondown><ondown condition="!Control.IsVisible(9001) + Control.IsVisible(6056)">6056</ondown>'
            '<ondown condition="!Control.IsVisible(9001) + !Control.IsVisible(6056)">$PARAM[content_id]</ondown><onback>$PARAM[content_id]</onback></control>\n'
            '\t\t\t\t<control type="image"><left>16</left><top>13</top><width>22</width><height>22</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">aeon/icons/layers.png</texture><visible>!%s</visible></control>\n'
            '\t\t\t\t<control type="image"><left>16</left><top>13</top><width>22</width><height>22</height><aspectratio>keep</aspectratio><texture colordiffuse="%s">aeon/icons/layers.png</texture><visible>%s</visible></control>\n'
            '\t\t\t\t<control type="label"><left>48</left><width>%d</width><height>48</height><aligny>center</aligny><font>small_20_semibold</font><textcolor>ffffffff</textcolor>'
            '<label>$LOCALIZE[19146][COLOR 9effffff]  ·  $PARAM[group_label][/COLOR]</label><visible>!%s</visible></control>\n'
            '\t\t\t\t<control type="label"><left>48</left><width>%d</width><height>48</height><aligny>center</aligny><font>small_20_semibold</font><textcolor>%s</textcolor>'
            '<label>$LOCALIZE[19146]  ·  $PARAM[group_label]</label><visible>%s</visible></control>\n'
            '\t\t\t\t<control type="image"><left>%d</left><top>15</top><width>18</width><height>18</height><aspectratio>keep</aspectratio><texture colordiffuse="b3ffffff">aeon/icons/chevron_down.png</texture><visible>!%s</visible></control>\n'
            '\t\t\t\t<control type="image"><left>%d</left><top>15</top><width>18</width><height>18</height><aspectratio>keep</aspectratio><texture colordiffuse="%s">aeon/icons/chevron_down.png</texture><visible>%s</visible></control>\n'
            '\t\t\t</control>\n'
            % (GROUPS_X, GROUPS_W, f, GROUPS_W, f, GROUPS_W, FOCUS, left, right, f, INK, f, GROUPS_W - 82, f, GROUPS_W - 82, INK, f,
               GROUPS_W - 32, f, GROUPS_W - 32, INK, f))


W_GROUP = TABS[-1][3] + TABS[-1][4] + 8             # the pill with Groups
W_PLAIN = W_GROUP - SHIFT
pill = ''
for w, cond in ((W_GROUP, '$PARAM[show_group]'), (W_PLAIN, '!$PARAM[show_group]')):
    pill += ('\t\t\t<control type="image"><left>-32</left><top>-22</top><width>%d</width><height>118</height><texture border="56" colordiffuse="66000000">fg/sh16.png</texture><visible>%s</visible></control>\n'
             '\t\t\t<control type="image"><width>%d</width><height>64</height><texture border="32" colordiffuse="fg_frost">fg/r32.png</texture><visible>%s</visible></control>\n'
             '\t\t\t<control type="image"><width>%d</width><height>64</height><texture border="32" colordiffuse="fg_edge">fg/e32.png</texture><visible>%s</visible></control>\n'
             % (w + 64, cond, w, cond, w, cond))
TABS_XML = ('\t<include name="FG_PVRTabs">\n\t\t<param name="show_group">false</param>\n\t\t<param name="group_label"></param>\n\t\t<param name="content_id">9100</param>\n'
            '\t\t<definition>\n\t\t<control type="group" id="9000">\n\t\t\t<left>96</left><top>40</top><width>%d</width><height>64</height>\n'
            '\t\t\t<visible>![%s]</visible>\n%s'
            '\t\t\t<control type="label"><left>26</left><width>100</width><height>64</height><aligny>center</aligny><font>hm_cap_16</font><textcolor>a8ffffff</textcolor><label>[UPPERCASE]$VAR[Misc_PVRMedium][/UPPERCASE]</label></control>\n'
            % (W_GROUP, OSD, pill)
            + tab(*TABS[0]) + groups_tab() + ''.join(tab(*t) for t in TABS[1:]) +
            '\t\t</control>\n\t\t</definition>\n\t</include>\n')


# ---------------------------------------------------------------------------------------------------------- Channels
L = 'ListItem'
C = 'Container(50).ListItem'


def row(focused, lid=50, w=968):
    """One channel row of a channel list (w x 74; the pill 68 high): list 50 of Channels, 11 of the channels OSD."""
    if focused:
        back = ('<control type="image"><left>0</left><top>3</top><width>%d</width><height>68</height><texture border="32" colordiffuse="%s">fg/r32.png</texture><visible>Control.HasFocus(%d)</visible></control>'
                '<control type="image"><left>0</left><top>3</top><width>%d</width><height>68</height><texture border="32" colordiffuse="1fffffff">fg/r32.png</texture><visible>!Control.HasFocus(%d)</visible></control>'
                % (w, FOCUS, lid, w, lid))
        ink, sub, tile, bar, track = INK, INK, 'ff1c1f27', INK, '2e0f1115'
        cond = 'Control.HasFocus(%d)' % lid
    else:
        back, ink, sub, tile, bar, track, cond = '', 'ffffffff', 'a8ffffff', '12ffffff', 'ffffffff', '2effffff', ''

    def both(xml_focus, xml_plain):
        """in the focused layout: dark ink while the list has focus, white otherwise"""
        if not focused:
            return xml_plain
        return xml_focus.replace('@V@', '<visible>%s</visible>' % cond) + xml_plain.replace('@V@', '<visible>!%s</visible>' % cond)
    num = '<control type="label"><left>0</left><top>3</top><width>48</width><height>68</height><align>right</align><aligny>center</aligny><font>num_22</font><textcolor>%s</textcolor><label>$INFO[ListItem.ChannelNumberLabel]</label>@V@</control>'
    name = ('<control type="label"><left>172</left><top>13</top><width>' + str(w - 408) + '</width><height>28</height><aligny>center</aligny><font>small_20_semibold</font><textcolor>%s</textcolor>'
            '<label>$INFO[ListItem.ChannelName]</label>@V@</control>')
    now = ('<control type="label"><left>172</left><top>41</top><width>' + str(w - 408) + '</width><height>24</height><aligny>center</aligny><font>small_20</font><textcolor>%s</textcolor>'
           '<label>$INFO[ListItem.Title]</label>@V@</control>')
    time = ('<control type="label"><left>' + str(w - 220) + '</left><top>13</top><width>196</width><height>24</height><align>right</align><aligny>center</aligny><font>small_20_semibold</font><textcolor>%s</textcolor>'
            '<label>$INFO[ListItem.StartTime]$INFO[ListItem.EndTime,–,]</label>@V@</control>')
    tile_x = '<control type="image"><left>64</left><top>9</top><width>96</width><height>56</height><texture border="12" colordiffuse="%s">fg/r12.png</texture>@V@</control>'
    px = str(w - 194)
    prog = ('<control type="image"><left>' + px + '</left><top>45</top><width>170</width><height>5</height><texture border="2" colordiffuse="%s">fg/pill4.png</texture>@V2@</control>'
            '<control type="progress"><left>' + px + '</left><top>45</top><width>170</width><height>5</height><texturebg border="2" colordiffuse="00ffffff">fg/pill4.png</texturebg>'
            '<midtexture border="2" colordiffuse="%s">fg/pill4.png</midtexture><info>ListItem.Progress</info>@V2@</control>')
    hasepg = 'ListItem.HasEpg'

    def p(xml):
        return xml.replace('@V2@', '<visible>%s@C@</visible>' % hasepg)
    progs = ''
    if focused:
        progs = (p(prog % (track, bar)).replace('@C@', ' + ' + cond) + p(prog % ('2effffff', 'ffffffff')).replace('@C@', ' + !' + cond))
    else:
        progs = p(prog % (track, bar)).replace('@C@', '')
    out = back
    out += both(num % sub, num % 'a8ffffff') if focused else (num % 'a8ffffff').replace('@V@', '')
    out += both(tile_x % tile, tile_x % '12ffffff') if focused else (tile_x % tile).replace('@V@', '')
    out += ('<control type="image"><left>70</left><top>13</top><width>84</width><height>48</height><aspectratio>keep</aspectratio><texture background="true">$INFO[ListItem.Icon]</texture></control>'
            '<control type="image"><left>2</left><top>32</top><width>10</width><height>10</height><texture colordiffuse="%s">fg/circle.png</texture><visible>ListItem.IsPlaying</visible></control>' % RED)
    for t in (name, now, time):
        plain = t % ('ffffffff' if t is name else ('a8ffffff' if t is now else 'c8ffffff'))
        out += both(t % (ink if t is name else sub), plain) if focused else plain.replace('@V@', '')
    out += progs
    # the playing channel is a "selected" item: Kodi draws its labels in selectedcolor (white by default), which vanished
    # on the white focus pill (0.46.0): the same colour as the text
    return re.sub(r'<textcolor>([^<]*)</textcolor>', r'<textcolor>\1</textcolor><selectedcolor>\1</selectedcolor>', out)


CHANNELS_XML = ('\t<include name="FG_PVRChannels">\n\t\t<param name="empty_label">$ADDON[skin.aeon.fuse 32356]</param>\n\t\t<definition>\n'
                + glass(96, 136, 1000, 906, 32) +
                '\t\t<control type="label"><left>620</left><top>150</top><width>444</width><height>44</height><align>right</align><aligny>center</aligny><font>hm_cap_16</font><textcolor>a8ffffff</textcolor>'
                '<label>[UPPERCASE]$INFO[Control.GetLabel(29)]$INFO[Container(50).NumItems,  ·  , $LOCALIZE[19019]][/UPPERCASE]</label></control>\n'
                '\t\t<control type="group" id="9100">\n\t\t\t<defaultcontrol always="true">50</defaultcontrol>\n'
                '\t\t\t<control type="list" id="50">\n\t\t\t\t<left>112</left><top>206</top><width>968</width><height>814</height>\n'
                '\t\t\t\t<onup>9001</onup><ondown>50</ondown><onleft>noop</onleft><onright>60</onright>\n'
                '\t\t\t\t<pagecontrol>60</pagecontrol><scrolltime tween="cubic" easing="out">200</scrolltime>\n'
                '\t\t\t\t<viewtype label="535">list</viewtype>\n'
                '\t\t\t\t<itemlayout height="74" width="968">%s</itemlayout>\n'
                '\t\t\t\t<focusedlayout height="74" width="968">%s</focusedlayout>\n'
                '\t\t\t</control>\n'
                '\t\t\t<include content="Misc_EmptyStateButton"><param name="top" value="206"/><param name="label" value="$PARAM[empty_label]"/></include>\n'
                '\t\t</control>\n'
                '\t\t<include content="AG_Scrollbar"><param name="id" value="60"/><param name="left" value="1082"/><param name="top" value="206"/><param name="height" value="814"/>'
                '<param name="onleft" value="50"/><param name="onright" value="9201"/></include>\n'
                % (row(False), row(True)))
# the spotlight of the channel in focus
S = 1164
CHANNELS_XML += (glass(1124, 136, 700, 906, 32) +
                 '\t\t<control type="group">\n\t\t\t<visible>Integer.IsGreater(Container(50).NumItems,0)</visible>\n'
                 '\t\t\t<control type="image"><left>%d</left><top>170</top><width>260</width><height>150</height><aspectratio align="left">keep</aspectratio><fadetime>200</fadetime><texture background="true">$INFO[%s.Icon]</texture></control>\n'
                 '\t\t\t<control type="label"><left>%d</left><top>336</top><width>620</width><height>28</height><aligny>center</aligny><font>hm_cap_16</font><textcolor>a8ffffff</textcolor>'
                 '<label>[UPPERCASE]$INFO[%s.ChannelNumberLabel,,  ·  ]$LOCALIZE[19030]$INFO[%s.StartTime,  ·  ,]$INFO[%s.EndTime,–,][/UPPERCASE]</label><visible>%s.HasEpg</visible></control>\n'
                 '\t\t\t<control type="label"><left>%d</left><top>364</top><width>620</width><height>76</height><aligny>center</aligny><font>pl_display_52</font><textcolor>ffffffff</textcolor><scroll>true</scroll>'
                 '<label>$INFO[%s.Title]</label></control>\n'
                 '\t\t\t<control type="group"><left>%d</left><top>452</top><visible>%s.HasEpg</visible>\n'
                 '\t\t\t\t<control type="image"><width>620</width><height>12</height><texture border="6" colordiffuse="3dffffff">fg/pill12.png</texture></control>\n'
                 '\t\t\t\t<control type="progress"><width>620</width><height>12</height><texturebg border="6" colordiffuse="00ffffff">fg/pill12.png</texturebg><midtexture border="6" colordiffuse="ffffffff">fg/pill12.png</midtexture><info>%s.Progress</info></control>\n'
                 '\t\t\t\t<control type="label"><top>22</top><width>620</width><height>30</height><aligny>center</aligny><font>small_20_semibold</font><textcolor>dbffffff</textcolor>'
                 '<label>$LOCALIZE[31030] $INFO[%s.EndTime]$INFO[%s.Duration(mins),  ·  , $ADDON[skin.aeon.fuse 32220]]</label></control>\n'
                 '\t\t\t</control>\n'
                 '\t\t\t<control type="textbox"><left>%d</left><top>520</top><width>620</width><height>232</height><font>pl_body_24</font><textcolor>ccffffff</textcolor><label>$INFO[%s.Plot]</label>'
                 '<autoscroll delay="6000" time="3000" repeat="10000">true</autoscroll></control>\n'
                 '\t\t\t<control type="group"><left>%d</left><top>780</top><visible>!String.IsEmpty(%s.NextTitle)</visible>\n'
                 '\t\t\t\t<control type="label"><width>620</width><height>28</height><aligny>center</aligny><font>hm_cap_16</font><textcolor>a8ffffff</textcolor><label>[UPPERCASE]$LOCALIZE[19031][/UPPERCASE]</label></control>\n'
                 '\t\t\t\t<control type="label"><top>34</top><width>90</width><height>34</height><aligny>center</aligny><font>small_20_bold</font><textcolor>ffffffff</textcolor><label>$INFO[%s.NextStartTime]</label></control>\n'
                 '\t\t\t\t<control type="label"><left>90</left><top>34</top><width>530</width><height>34</height><aligny>center</aligny><font>small_20_semibold</font><textcolor>dbffffff</textcolor><label>$INFO[%s.NextTitle]</label></control>\n'
                 '\t\t\t</control>\n'
                 % (S, C, S, C, C, C, C, S, C, S, C, C, C, C, S, C, S, C, C, C))
BTN = ('\t\t\t<control type="button" id="%d"><left>%d</left><top>942</top><width>%d</width><height>64</height><label>%s</label><font>small_20_bold</font><align>center</align><aligny>center</aligny>'
       '<textoffsetx>%d</textoffsetx><textcolor>%s</textcolor><focusedcolor>%s</focusedcolor>'
       '<texturefocus border="32" colordiffuse="%s">fg/r32.png</texturefocus><texturenofocus border="32" colordiffuse="%s">fg/r32.png</texturenofocus>'
       '<onclick>%s</onclick><onleft>%s</onleft><onright>%s</onright><onup>noop</onup><ondown>noop</ondown><onback>50</onback></control>\n')
CHANNELS_XML += (BTN % (9201, S, 170, '$LOCALIZE[208]', 26, 'ffffffff', INK, FOCUS, '2effffff', 'SetFocus(50)</onclick><onclick>Action(Select)', 60, 9202)
                 + BTN % (9202, S + 182, 184, '$LOCALIZE[264]', 34, 'ffffffff', INK, FOCUS, '1fffffff', 'SetFocus(50)</onclick><onclick>Action(Record)', 9201, 9203)
                 + BTN % (9203, S + 378, 150, '$LOCALIZE[19069]', 0, 'ffffffff', INK, FOCUS, '1fffffff', 'ActivateWindow(TVGuide)', 9202, 'noop') +
                 '\t\t\t<control type="image"><left>%d</left><top>963</top><width>22</width><height>22</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">aeon/icons/play.png</texture><visible>!Control.HasFocus(9201)</visible></control>\n'
                 '\t\t\t<control type="image"><left>%d</left><top>963</top><width>22</width><height>22</height><aspectratio>keep</aspectratio><texture colordiffuse="%s">aeon/icons/play.png</texture><visible>Control.HasFocus(9201)</visible></control>\n'
                 '\t\t\t<control type="image"><left>%d</left><top>967</top><width>14</width><height>14</height><texture colordiffuse="%s">fg/circle.png</texture></control>\n'
                 '\t\t</control>\n\t\t</definition>\n\t</include>\n' % (S + 24, S + 24, INK, S + 182 + 24, RED))


# ---------------------------------------------------------------------------------------------------------- Guide
G = 'Container(50).ListItem'
NOWCHIP = ('<control type="button"><width min="44" max="300">auto</width><height>30</height><label>$LOCALIZE[31324]</label><font>hm_cap_14</font><textcolor>fg_mark</textcolor><focusedcolor>fg_mark</focusedcolor>'
           '<disabledcolor>fg_mark</disabledcolor><align>center</align><aligny>center</aligny><textoffsetx>14</textoffsetx><texturenofocus border="15" colordiffuse="38e8b04b">fg/r16.png</texturenofocus>'
           '<texturefocus border="15" colordiffuse="38e8b04b">fg/r16.png</texturefocus><visible>Integer.IsGreater(%s.Progress,0) + Integer.IsLess(%s.Progress,100)</visible></control>' % (G, G))
KICKER = '[UPPERCASE]$INFO[%s.ChannelNumberLabel,,  ·  ]$INFO[%s.ChannelName][/UPPERCASE]' % (G, G)
META = '$INFO[%s.StartTime]$INFO[%s.EndTime,–,]$INFO[%s.Duration(mins),  ·  , $ADDON[skin.aeon.fuse 32220]]' % (G, G, G)


def keycap(key, label):
    return ('\t\t\t\t<control type="group"><width>%d</width><height>30</height>'
            '<control type="image"><width>%d</width><height>30</height><texture border="8" colordiffuse="66ffffff">fg/e8.png</texture></control>'
            '<control type="label"><width>%d</width><height>30</height><align>center</align><aligny>center</aligny><font>hm_cap_14</font><textcolor>ffffffff</textcolor><label>%s</label></control></control>\n'
            '\t\t\t\t<control type="label"><width>auto</width><height>30</height><aligny>center</aligny><font>small_20_semibold</font><textcolor>c8ffffff</textcolor><label>%s</label></control>\n'
            % (len(key) * 12 + 22, len(key) * 12 + 22, len(key) * 12 + 22, key, label))


GUIDE_XML = ('\t<expression name="FG_GuideOSD">%s</expression>\n' % OSD +
             '\t<include name="FG_PVRGuideBack">\n'
             # --- over the playing channel: the picture, the channel pill, the clock, the sheet
             '\t\t<control type="group">\n\t\t\t<visible>$EXP[FG_GuideOSD]</visible>\n'
             '\t\t\t<control type="videowindow"><left>0</left><top>0</top><width>1920</width><height>1080</height></control>\n'
             '\t\t\t<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture colordiffuse="99000000">common/white.png</texture></control>\n'
             # 0.46.1: the sheet sits higher (36-738) so the player controls card shows under it, as it was when Guide was pressed
             + glass(96, 36, 1728, 702, 32).replace('\t\t<control', '\t\t\t<control') +
             '\t\t\t<control type="group">\n\t\t\t\t<visible>Integer.IsGreater(Container(50).NumItems,0)</visible>\n'
             '\t\t\t\t<control type="image"><left>128</left><top>58</top><width>112</width><height>68</height><texture border="12" colordiffuse="12ffffff">fg/r12.png</texture></control>\n'
             '\t\t\t\t<control type="image"><left>136</left><top>64</top><width>96</width><height>56</height><aspectratio>keep</aspectratio><texture background="true">$INFO[%s.Icon]</texture></control>\n'
             '\t\t\t\t<control type="grouplist"><left>260</left><top>52</top><width>1040</width><height>26</height><orientation>horizontal</orientation><itemgap>14</itemgap><usecontrolcoords>true</usecontrolcoords>\n'
             '\t\t\t\t\t<control type="label"><width>auto</width><height>26</height><aligny>center</aligny><font>hm_cap_16</font><textcolor>a8ffffff</textcolor><label>[UPPERCASE]$LOCALIZE[19069]  ·  [/UPPERCASE]%s</label></control>\n'
             '\t\t\t\t\t%s\n'
             '\t\t\t\t</control>\n'
             '\t\t\t\t<control type="label"><left>260</left><top>78</top><width>1040</width><height>46</height><aligny>center</aligny><font>pl_display_40</font><textcolor>ffffffff</textcolor><label>$VAR[FG_EpgHeadTitle]</label></control>\n'
             '\t\t\t\t<control type="label"><left>260</left><top>124</top><width>1040</width><height>28</height><aligny>center</aligny><font>small_20_semibold</font><textcolor>c8ffffff</textcolor><label>%s</label></control>\n'
             '\t\t\t</control>\n'
             '\t\t\t<control type="grouplist"><left>1300</left><top>58</top><width>492</width><height>30</height><orientation>horizontal</orientation><align>right</align><itemgap>10</itemgap><usecontrolcoords>true</usecontrolcoords>\n%s\t\t\t</control>\n'
             '\t\t\t<control type="grouplist"><left>1300</left><top>96</top><width>492</width><height>30</height><orientation>horizontal</orientation><align>right</align><itemgap>10</itemgap><usecontrolcoords>true</usecontrolcoords>\n%s\t\t\t</control>\n'
             '\t\t\t<include>FG_OSDGhost</include>\n'
             '\t\t</control>\n'
             % (G, KICKER, NOWCHIP, META, keycap('OK', '$LOCALIZE[19000]'), keycap('BACK', '$LOCALIZE[15067]')))
# --- the Guide page: the programme in focus, the playing picture, the grid card
GUIDE_XML += ('\t\t<control type="group">\n\t\t\t<visible>!$EXP[FG_GuideOSD]</visible>\n'
              '\t\t\t<control type="group">\n\t\t\t\t<visible>Integer.IsGreater(Container(50).NumItems,0)</visible>\n'
              '\t\t\t\t<control type="image"><left>96</left><top>140</top><width>96</width><height>56</height><texture border="12" colordiffuse="12ffffff">fg/r12.png</texture></control>\n'
              '\t\t\t\t<control type="image"><left>102</left><top>144</top><width>84</width><height>48</height><aspectratio>keep</aspectratio><texture background="true">$INFO[%s.Icon]</texture></control>\n'
              '\t\t\t\t<control type="grouplist"><left>210</left><top>153</top><width>1080</width><height>30</height><orientation>horizontal</orientation><itemgap>14</itemgap><usecontrolcoords>true</usecontrolcoords>\n'
              '\t\t\t\t\t<control type="label"><width>auto</width><height>30</height><aligny>center</aligny><font>hm_cap_16</font><textcolor>b3ffffff</textcolor><label>%s</label></control>\n'
              '\t\t\t\t\t%s\n'
              '\t\t\t\t</control>\n'
              '\t\t\t\t<control type="label"><left>96</left><top>204</top><width>1200</width><height>84</height><aligny>center</aligny><font>pl_display_60</font><textcolor>ffffffff</textcolor><scroll>true</scroll><label>$VAR[FG_EpgHeadTitle]</label></control>\n'
              '\t\t\t\t<control type="label"><left>96</left><top>292</top><width>1200</width><height>32</height><aligny>center</aligny><font>small_20_bold</font><textcolor>dbffffff</textcolor><label>%s</label></control>\n'
              '\t\t\t\t<control type="textbox"><left>96</left><top>334</top><width>1180</width><height>66</height><font>small_20</font><textcolor>c2ffffff</textcolor><label>$INFO[%s.Plot]</label>'
              '<autoscroll delay="6000" time="3000" repeat="10000">true</autoscroll></control>\n'
              '\t\t\t</control>\n'
              '\t\t\t<control type="group">\n\t\t\t\t<left>1344</left><top>136</top>\n\t\t\t\t<visible>Player.HasVideo</visible>\n'
              '\t\t\t\t<control type="image"><left>-40</left><top>-30</top><width>560</width><height>350</height><texture border="64" colordiffuse="$VAR[FG_PanelSh_80]">fg/sh24.png</texture></control>\n'
              '\t\t\t\t<control type="videowindow"><width>480</width><height>270</height></control>\n'
              '\t\t\t\t<control type="image"><top>206</top><width>480</width><height>64</height><texture colordiffuse="cc000000">aeon/osd_scrim_bottom.png</texture></control>\n'
              '\t\t\t\t<control type="image"><width>480</width><height>270</height><texture border="22" colordiffuse="3dffffff">fg/e22.png</texture></control>\n'
              '\t\t\t\t<control type="grouplist"><left>16</left><top>226</top><width>450</width><height>28</height><orientation>horizontal</orientation><itemgap>12</itemgap><usecontrolcoords>true</usecontrolcoords>\n'
              '\t\t\t\t\t<control type="group"><width>66</width><height>28</height><visible>Pvr.IsPlayingTv | Pvr.IsPlayingRadio</visible>'
              '<control type="image"><width>66</width><height>28</height><texture border="14" colordiffuse="%s">fg/r16.png</texture></control>'
              '<control type="label"><width>66</width><height>28</height><align>center</align><aligny>center</aligny><font>hm_cap_14</font><textcolor>ffffffff</textcolor><label>$ADDON[skin.aeon.fuse 32477]</label></control></control>\n'
              '\t\t\t\t\t<control type="label"><width>auto</width><height>28</height><aligny>center</aligny><font>small_20_semibold</font><textcolor>ffffffff</textcolor><label>$INFO[VideoPlayer.ChannelNumberLabel,,  ·  ]$INFO[VideoPlayer.ChannelName]$INFO[VideoPlayer.Title,,]</label><visible>Pvr.IsPlayingTv | Pvr.IsPlayingRadio</visible></control>\n'
              '\t\t\t\t\t<control type="label"><width>auto</width><height>28</height><aligny>center</aligny><font>small_20_semibold</font><textcolor>ffffffff</textcolor><label>$INFO[VideoPlayer.Title]</label><visible>!Pvr.IsPlayingTv + !Pvr.IsPlayingRadio</visible></control>\n'
              '\t\t\t\t</control>\n'
              '\t\t\t</control>\n'
              % (G, KICKER, NOWCHIP, META, G, RED)
              + glass(96, 436, 1728, 606, 32).replace('\t\t<control', '\t\t\t<control') +
              '\t\t</control>\n'
              # the group pill, in both
              '\t\t<control type="group"><animation effect="slide" end="0,-290" time="0" condition="$EXP[FG_GuideOSD]">Conditional</animation>\n'
              '\t\t<control type="button" id="6056"><left>128</left><top>456</top><width>290</width><height>40</height><label></label>'
              '<texturefocus border="20" colordiffuse="%s">fg/r22.png</texturefocus><texturenofocus border="20" colordiffuse="1affffff">fg/r22.png</texturenofocus>'
              '<onclick>SendClick(28)</onclick><onup condition="!$EXP[FG_GuideOSD]">SetFocus(101)</onup><onup condition="$EXP[FG_GuideOSD]">noop</onup><ondown>9100</ondown><onright>9100</onright><onleft>noop</onleft>'
              '<onback condition="$EXP[FG_GuideOSD]">6057</onback><onback condition="!$EXP[FG_GuideOSD]">9100</onback></control>\n'
              # over the playing channel, Back moves to this 1 px button, which switches to the picture as it gets focus: a Back
              # whose onback is a builtin is not taken as handled, and Kodi then sends Live TV windows Home (0.46.0)
              '\t\t<control type="button" id="6057"><left>0</left><top>0</top><width>1</width><height>1</height><label></label><texturefocus /><texturenofocus />'
              '<onfocus>SetProperty(aeon.guide.back,1,home)</onfocus><onfocus>SetFocus(9100)</onfocus><onfocus>Action(FullScreen)</onfocus><visible>$EXP[FG_GuideOSD]</visible></control>\n'
              '\t\t<control type="image"><left>142</left><top>465</top><width>22</width><height>22</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">aeon/icons/layers.png</texture><visible>!Control.HasFocus(6056)</visible></control>\n'
              '\t\t<control type="image"><left>142</left><top>465</top><width>22</width><height>22</height><aspectratio>keep</aspectratio><texture colordiffuse="%s">aeon/icons/layers.png</texture><visible>Control.HasFocus(6056)</visible></control>\n'
              '\t\t<control type="label"><left>174</left><top>456</top><width>210</width><height>40</height><aligny>center</aligny><font>small_20_semibold</font><textcolor>ffffffff</textcolor><label>$INFO[Control.GetLabel(30)]</label><visible>!Control.HasFocus(6056)</visible></control>\n'
              '\t\t<control type="label"><left>174</left><top>456</top><width>210</width><height>40</height><aligny>center</aligny><font>small_20_semibold</font><textcolor>%s</textcolor><label>$INFO[Control.GetLabel(30)]</label><visible>Control.HasFocus(6056)</visible></control>\n'
              '\t\t<control type="image"><left>392</left><top>467</top><width>18</width><height>18</height><aspectratio>keep</aspectratio><texture colordiffuse="b3ffffff">aeon/icons/chevron_down.png</texture><visible>!Control.HasFocus(6056)</visible></control>\n'
              '\t\t<control type="image"><left>392</left><top>467</top><width>18</width><height>18</height><aspectratio>keep</aspectratio><texture colordiffuse="%s">aeon/icons/chevron_down.png</texture><visible>Control.HasFocus(6056)</visible></control>\n'
              '\t\t<!-- 0.56.13 the channel number being typed (Kodi\'s channel entry in the guide): a pill in the accent colour over the group pill -->\n'
              '\t\t<control type="group"><visible>!String.IsEmpty(PVR.ChannelNumberInput)</visible><animation type="Visible"><effect type="fade" start="0" end="100" time="120"/></animation>\n'
              '\t\t<control type="image"><left>128</left><top>456</top><width>290</width><height>40</height><texture border="20" colordiffuse="$VAR[Aeon_Accent]">fg/r22.png</texture></control>\n'
              '\t\t<control type="label"><left>148</left><top>456</top><width>120</width><height>40</height><aligny>center</aligny><font>small_20_semibold</font><textcolor>$VAR[Aeon_AccentText]</textcolor><label>[UPPERCASE]$LOCALIZE[19029][/UPPERCASE]</label></control>\n'
              '\t\t<control type="label"><left>262</left><top>456</top><width>140</width><height>40</height><align>right</align><aligny>center</aligny><font>st_ui_24_bold</font><textcolor>$VAR[Aeon_AccentText]</textcolor><label>$INFO[PVR.ChannelNumberInput]</label></control>\n'
              '\t\t</control>\n'
              '\t\t</control>\n'
              '\t</include>\n' % (FOCUS, INK, INK, INK))

# --- the grid: place and layouts (rows 65: a 57 high cell, 8 apart; ruler 46; channel column 320)
GRID_XML = ('\t<include name="FG_EpgGrid_fg">\n'
            '\t\t<left>128</left><top>454</top><width>1664</width><height>566</height>\n'
            '\t\t<timeblocks>30</timeblocks><rulerunit>6</rulerunit>\n'
            '\t\t<progresstexture border="0,46,12,80" colordiffuse="fg_mark">fg/epgnow.png</progresstexture>\n'
            '\t\t<animation effect="slide" end="0,-290" time="0" condition="$EXP[FG_GuideOSD]">Conditional</animation>\n'
            '\t</include>\n'
            '\t<include name="Misc_EPGLayouts_fg">\n'
            '\t\t<rulerlayout height="46" width="269">\n'
            '\t\t\t<control type="image"><left>0</left><top>32</top><width>2</width><height>10</height><texture colordiffuse="4dffffff">common/white.png</texture><visible>String.Contains(ListItem.Label,:)</visible></control>\n'
            '\t\t\t<control type="label"><left>10</left><top>0</top><width>250</width><height>40</height><aligny>center</aligny><font>small_20_bold</font><textcolor>b3ffffff</textcolor><label>$INFO[ListItem.Label]</label><visible>String.Contains(ListItem.Label,:)</visible></control>\n'
            '\t\t</rulerlayout>\n')
CHROW = ('\t\t\t<control type="image"><left>0</left><top>26</top><width>10</width><height>10</height><texture colordiffuse="%s">fg/circle.png</texture><visible>ListItem.IsPlaying</visible></control>\n'
         '\t\t\t<control type="label"><left>0</left><top>0</top><width>44</width><height>65</height><align>right</align><aligny>center</aligny><font>num_22</font><textcolor>%s</textcolor><label>$INFO[ListItem.ChannelNumberLabel]</label></control>\n'
         '\t\t\t<control type="image"><left>56</left><top>5</top><width>104</width><height>55</height><texture border="12" colordiffuse="%s">fg/r12.png</texture></control>\n'
         '\t\t\t<control type="image"><left>64</left><top>10</top><width>88</width><height>45</height><aspectratio>keep</aspectratio><texture background="true">$INFO[ListItem.Icon]</texture></control>\n'
         '\t\t\t<control type="textbox"><left>172</left><top>6</top><width>136</width><height>54</height><font>hm_cap_14</font><textcolor>%s</textcolor><align>left</align><label>$INFO[ListItem.ChannelName]</label></control>\n')
GRID_XML += ('\t\t<channellayout height="65" width="320">\n' + CHROW % (RED, '9effffff', '12ffffff', 'c8ffffff') + '\t\t</channellayout>\n'
             '\t\t<focusedchannellayout height="65" width="320">\n'
             '\t\t\t<control type="image"><left>48</left><top>1</top><width>268</width><height>63</height><texture border="12" colordiffuse="17ffffff">fg/r12.png</texture><visible>Control.HasFocus(50)</visible></control>\n'
             + CHROW % (RED, 'ffffffff', '1fffffff', 'ffffffff') + '\t\t</focusedchannellayout>\n')
CELL = ('\t\t\t<control type="label" id="%d"><left>17</left><top>8</top><width>6</width><height>26</height><font>small_20_semibold</font><textcolor>%s</textcolor><label>$INFO[ListItem.Label]</label><visible>%s</visible></control>\n'
        '\t\t\t<control type="label" id="%d"><left>17</left><top>34</top><width>6</width><height>22</height><font>hm_cap_14</font><textcolor>%s</textcolor><label>$INFO[ListItem.StartTime]$INFO[ListItem.EndTime,–,]</label><visible>%s</visible></control>\n')
GRID_XML += ('\t\t<itemlayout height="65" width="40">\n'
             '\t\t\t<control type="image" id="2"><left>3</left><top>4</top><width>34</width><height>57</height><texture border="12" colordiffuse="14ffffff">fg/r12.png</texture><visible>!String.IsEmpty(ListItem.Label)</visible></control>\n'
             '\t\t\t<control type="image" id="3"><left>3</left><top>4</top><width>34</width><height>57</height><texture border="12" colordiffuse="0fffffff">fg/r12.png</texture><visible>Integer.IsGreater(ListItem.Progress,0) + Integer.IsLess(ListItem.Progress,100)</visible></control>\n'
             '\t\t\t<control type="image" id="7"><left>3</left><top>4</top><width>34</width><height>57</height><texture border="12" colordiffuse="08ffffff">fg/r12.png</texture><visible>String.IsEmpty(ListItem.Label)</visible></control>\n'
             + CELL % (1, 'ebffffff', '!Integer.IsEqual(ListItem.Progress,100)', 4, '99ffffff', '!Integer.IsEqual(ListItem.Progress,100) + !String.IsEmpty(ListItem.Label)')
             + CELL % (5, '66ffffff', 'Integer.IsEqual(ListItem.Progress,100)', 6, '47ffffff', 'Integer.IsEqual(ListItem.Progress,100) + !String.IsEmpty(ListItem.Label)') +
             '\t\t\t<control type="label" id="8"><left>17</left><top>4</top><width>6</width><height>57</height><aligny>center</aligny><font>small_20</font><textcolor>52ffffff</textcolor><label>$LOCALIZE[19055]</label><visible>String.IsEmpty(ListItem.Label)</visible></control>\n'
             '\t\t</itemlayout>\n'
             '\t\t<focusedlayout height="65" width="40">\n'
             '\t\t\t<control type="image" id="2"><left>3</left><top>4</top><width>34</width><height>57</height><texture border="12" colordiffuse="33ffffff">fg/r12.png</texture></control>\n'
             '\t\t\t<control type="image" id="3"><left>0</left><top>1</top><width>40</width><height>63</height><texture border="15" colordiffuse="fg_mark">fg/ring12.png</texture><visible>Control.HasFocus(50)</visible></control>\n'
             + CELL % (1, 'ffffffff', 'true', 4, 'ccffffff', 'true') +
             '\t\t</focusedlayout>\n'
             '\t</include>\n')

# ---------------------------------------------------------------------------------------------------------- channels OSD
# the channel list over the picture (DialogPVRChannelsOSD, Kodi ids: list 11, scrollbar 60): a glass card on the left
# (left edge at 96, in line with the Now playing pill and the player controls card, 0.46.2) with a group pill (button 30: Left / Right = previous / next channel group, Down = the list) and the channel rows of
# Live TV > Channels. The player controls' Groups button opens it with the group pill in focus (aeon.osdch.groups).
CHOSD_XML = ('\t<include name="FG_ChOSD">\n'
             '\t\t<control type="image"><left>0</left><top>0</top><width>1232</width><height>740</height><texture colordiffuse="b3000000">fg/scrim_l.png</texture></control>\n'
             + glass(96, 120, 940, 600, 32) +
             '\t\t<control type="label"><left>136</left><top>144</top><width>860</width><height>30</height><aligny>center</aligny><font>hm_cap_16</font><textcolor>a8ffffff</textcolor>'
             '<label>[UPPERCASE]$LOCALIZE[19019]$INFO[Container(11).NumItems,  ·  ,][/UPPERCASE]</label></control>\n'
             '\t\t<control type="button" id="30"><left>128</left><top>182</top><width>480</width><height>52</height><label></label>'
             '<texturefocus border="26" colordiffuse="%s">fg/r26.png</texturefocus><texturenofocus border="26" colordiffuse="1affffff">fg/r26.png</texturenofocus>'
             '<onleft>PreviousChannelGroup</onleft><onright>NextChannelGroup</onright><onclick>NextChannelGroup</onclick><onup>noop</onup><ondown>11</ondown></control>\n'
             '\t\t<control type="image"><left>144</left><top>199</top><width>18</width><height>18</height><aspectratio>keep</aspectratio><texture colordiffuse="b3ffffff" flipx="true">aeon/icons/chevron_right.png</texture><visible>!Control.HasFocus(30)</visible></control>\n'
             '\t\t<control type="image"><left>144</left><top>199</top><width>18</width><height>18</height><aspectratio>keep</aspectratio><texture colordiffuse="%s" flipx="true">aeon/icons/chevron_right.png</texture><visible>Control.HasFocus(30)</visible></control>\n'
             '\t\t<control type="image"><left>574</left><top>199</top><width>18</width><height>18</height><aspectratio>keep</aspectratio><texture colordiffuse="b3ffffff">aeon/icons/chevron_right.png</texture><visible>!Control.HasFocus(30)</visible></control>\n'
             '\t\t<control type="image"><left>574</left><top>199</top><width>18</width><height>18</height><aspectratio>keep</aspectratio><texture colordiffuse="%s">aeon/icons/chevron_right.png</texture><visible>Control.HasFocus(30)</visible></control>\n'
             '\t\t<control type="image"><left>178</left><top>197</top><width>22</width><height>22</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">aeon/icons/layers.png</texture><visible>!Control.HasFocus(30)</visible></control>\n'
             '\t\t<control type="image"><left>178</left><top>197</top><width>22</width><height>22</height><aspectratio>keep</aspectratio><texture colordiffuse="%s">aeon/icons/layers.png</texture><visible>Control.HasFocus(30)</visible></control>\n'
             '\t\t<control type="label"><left>212</left><top>182</top><width>350</width><height>52</height><aligny>center</aligny><font>small_20_semibold</font><textcolor>ffffffff</textcolor><label>$INFO[VideoPlayer.ChannelGroup]</label><visible>!Control.HasFocus(30)</visible></control>\n'
             '\t\t<control type="label"><left>212</left><top>182</top><width>350</width><height>52</height><aligny>center</aligny><font>small_20_semibold</font><textcolor>%s</textcolor><label>$INFO[VideoPlayer.ChannelGroup]</label><visible>Control.HasFocus(30)</visible></control>\n'
             '\t\t<control type="list" id="11">\n\t\t\t<left>112</left><top>252</top><width>892</width><height>444</height>\n'
             '\t\t\t<onup>30</onup><ondown>11</ondown><onleft>PreviousChannelGroup</onleft><onright>60</onright>\n'
             '\t\t\t<pagecontrol>60</pagecontrol><scrolltime tween="cubic" easing="out">200</scrolltime>\n'
             '\t\t\t<itemlayout height="74" width="892">%s</itemlayout>\n'
             '\t\t\t<focusedlayout height="74" width="892">%s</focusedlayout>\n'
             '\t\t</control>\n'
             '\t\t<include content="AG_Scrollbar"><param name="id" value="60"/><param name="left" value="1010"/><param name="top" value="252"/><param name="height" value="436"/>'
             '<param name="onleft" value="11"/><param name="onright" value="noop"/></include>\n'
             '\t</include>\n' % (FOCUS, INK, INK, INK, INK, row(False, 11, 892), row(True, 11, 892)))

# a slim rounded scroll bar for Fused Glass pages (0.46.0: the Planner's day list, before the flat Aeon strip)
SCROLL_XML = ('\t<include name="FG_ScrollPill">\n\t\t<param name="vis">true</param>\n\t\t<definition>\n'
              '\t\t\t<control type="scrollbar" id="$PARAM[sid]">\n'
              '\t\t\t\t<left>$PARAM[left]</left><top>$PARAM[top]</top><width>8</width><height>$PARAM[height]</height>\n'
              '\t\t\t\t<texturesliderbackground border="3" colordiffuse="1affffff">aeon/track_8.png</texturesliderbackground>\n'
              '\t\t\t\t<texturesliderbar border="3" colordiffuse="73ffffff">aeon/track_8.png</texturesliderbar>\n'
              '\t\t\t\t<texturesliderbarfocus border="3" colordiffuse="fg_mark">aeon/track_8.png</texturesliderbarfocus>\n'
              '\t\t\t\t<orientation>vertical</orientation><showonepage>false</showonepage>\n'
              '\t\t\t\t<onleft>$PARAM[list]</onleft><onright>noop</onright><onback>$PARAM[list]</onback>\n'
              '\t\t\t\t<visible>$PARAM[vis]</visible>\n'
              '\t\t\t</control>\n\t\t</definition>\n\t</include>\n')

# the player controls card as it was when Guide was pressed (0.46.1): drawn, not focusable, under the guide sheet
def ghost_btn(x, icon, lit=False, label=''):
    if lit:
        return ('\t\t\t<control type="image"><left>%d</left><top>932</top><width>64</width><height>64</height><texture colordiffuse="ffffffff">fg/circle.png</texture></control>\n'
                '\t\t\t<control type="image"><left>%d</left><top>947</top><width>34</width><height>34</height><aspectratio>keep</aspectratio><texture colordiffuse="aeon_onbar">%s</texture></control>\n'
                '\t\t\t<control type="label"><left>%d</left><top>1006</top><width>200</width><height>28</height><align>center</align><aligny>center</aligny><font>pl_small_20</font><textcolor>ffffffff</textcolor><label>[UPPERCASE]%s[/UPPERCASE]</label></control>\n'
                % (x + 8, x + 23, icon, x - 60, label))
    return ('\t\t\t<control type="image"><left>%d</left><top>932</top><width>64</width><height>64</height><texture colordiffuse="1fffffff">fg/circle.png</texture></control>\n'
            '\t\t\t<control type="image"><left>%d</left><top>947</top><width>34</width><height>34</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">%s</texture></control>\n'
            % (x + 8, x + 23, icon))


GHOST_XML = ('\t<include name="FG_OSDGhost">\n' + glass(96, 752, 1728, 290, 32).replace('\t\t<control', '\t\t\t<control') +
             '\t\t\t<control type="image"><left>164</left><top>780</top><width>156</width><height>234</height><texture border="18" colordiffuse="14ffffff">fg/r18.png</texture></control>\n'
             '\t\t\t<control type="image"><left>178</left><top>814</top><width>128</width><height>77</height><aspectratio>keep</aspectratio><texture background="true">$INFO[VideoPlayer.Cover]</texture></control>\n'
             '\t\t\t<control type="label"><left>164</left><top>910</top><width>156</width><height>44</height><align>center</align><aligny>center</aligny><font>pl_display_40</font><textcolor>ffffffff</textcolor><label>$INFO[VideoPlayer.ChannelNumberLabel]</label></control>\n'
             '\t\t\t<control type="label"><left>388</left><top>778</top><width>1000</width><height>26</height><aligny>center</aligny><font>pl_cap_16</font><textcolor>99ffffff</textcolor>'
             '<label>[UPPERCASE]$INFO[VideoPlayer.ChannelNumberLabel,,  ·  ]$INFO[VideoPlayer.ChannelName]$INFO[VideoPlayer.Genre,  ·  ,][/UPPERCASE]</label></control>\n'
             '\t\t\t<control type="label"><left>388</left><top>804</top><width>1000</width><height>48</height><aligny>center</aligny><font>pl_display_40</font><textcolor>ffffffff</textcolor><label>$INFO[VideoPlayer.Title]</label></control>\n'
             '\t\t\t<control type="label"><left>1400</left><top>778</top><width>392</width><height>26</height><align>right</align><aligny>center</aligny><font>pl_cap_16</font><textcolor>99ffffff</textcolor>'
             '<label>[UPPERCASE]$LOCALIZE[19031]$INFO[VideoPlayer.NextStartTime,  ·  ,][/UPPERCASE]</label><visible>!String.IsEmpty(VideoPlayer.NextTitle)</visible></control>\n'
             '\t\t\t<control type="label"><left>1400</left><top>806</top><width>392</width><height>32</height><align>right</align><aligny>center</aligny><font>pl_ui_22_bold</font><textcolor>ffffffff</textcolor><label>$INFO[VideoPlayer.NextTitle]</label></control>\n'
             '\t\t\t<control type="image"><left>388</left><top>864</top><width>1404</width><height>12</height><texture border="6" colordiffuse="3dffffff">fg/pill12.png</texture></control>\n'
             '\t\t\t<control type="progress"><left>388</left><top>864</top><width>1404</width><height>12</height><texturebg border="6" colordiffuse="00ffffff">fg/pill12.png</texturebg>'
             '<midtexture border="6" colordiffuse="ffffffff">fg/pill12.png</midtexture><info>PVR.EpgEventProgress</info></control>\n'
             '\t\t\t<control type="label"><left>388</left><top>882</top><width>300</width><height>28</height><aligny>center</aligny><font>pl_small_20</font><textcolor>ffffffff</textcolor><label>$INFO[VideoPlayer.StartTime]</label></control>\n'
             '\t\t\t<control type="label"><left>840</left><top>882</top><width>500</width><height>28</height><align>center</align><aligny>center</aligny><font>pl_small_20</font><textcolor>c8ffffff</textcolor><label>$INFO[PVR.EpgEventRemainingTime,, $LOCALIZE[31965]]</label></control>\n'
             '\t\t\t<control type="label"><left>1492</left><top>882</top><width>300</width><height>28</height><align>right</align><aligny>center</aligny><font>pl_small_20</font><textcolor>ffffffff</textcolor><label>$INFO[VideoPlayer.EndTime]</label></control>\n'
             + ghost_btn(380, 'aeon/icons/chevron_down.png') + ghost_btn(460, 'aeon/icons/chevron_up.png')
             + ('\t\t\t<control type="image"><left>468</left><top>932</top><width>64</width><height>64</height><texture colordiffuse="1fffffff">fg/circle.png</texture></control>\n'.replace('468', '548')
                + '\t\t\t<control type="image"><left>569</left><top>953</top><width>22</width><height>22</height><texture colordiffuse="ffe5484d">fg/circle.png</texture></control>\n')
             + ghost_btn(620, 'aeon/icons/stop.png')
             + ghost_btn(1240, 'aeon/icons/subtitles.png') + ghost_btn(1320, 'aeon/icons/audio.png')
             + ghost_btn(1400, 'aeon/icons/sidebar.png', True, '$LOCALIZE[19069]') + ghost_btn(1480, 'aeon/icons/lines.png')
             + ghost_btn(1560, 'aeon/icons/layers.png') + ghost_btn(1640, 'aeon/icons/info.png') + ghost_btn(1720, 'aeon/icons/ppi.png') +
             '\t</include>\n')

BLOCK = ('\t<!-- FG_LIVETV:begin (written by _src/fg_livetv.py) ======================== Live TV: tabs, Channels, Guide (0.46.0) -->\n'
         + TABS_XML + CHANNELS_XML + GUIDE_XML + GRID_XML + CHOSD_XML + SCROLL_XML + GHOST_XML + '\t<!-- FG_LIVETV:end -->\n')

# ---------------------------------------------------------------------------------------------------------- write
f = io.open(FUSED, encoding='utf-8').read()
f = re.sub(r'\t<!-- FG_LIVETV:begin.*?<!-- FG_LIVETV:end -->\n', '', f, flags=re.S)
f = f.replace('</includes>', BLOCK + '</includes>')
io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(f)

m = io.open(MISC, encoding='utf-8').read()
# the old Fused grid place and layouts give way to the ones above
for name in ('Misc_EPGLayouts_fg', 'FG_EpgGrid_fg'):
    m, n = re.subn(r'\t<include name="%s">.*?\n\t</include>\n' % name, '', m, count=1, flags=re.S)
    if n:
        print('moved', name, 'to Includes_Fused.xml')
if 'FG_PVRTabs' not in m:
    # Misc_PVRFrame: Fused Glass gets the tab pill (no page title: the pill says it); 9001 moves up under it, its Group
    # button gives way to the Groups tab, and the Guide (Fused Glass) has no 9001 row
    a = ('\t\t\t<include content="AG_TopBar">\n\t\t\t\t<param name="index" value="10"/>\n'
         '\t\t\t\t<param name="title" value="$VAR[Misc_PVRMedium]  ·  $PARAM[title]"/>\n\t\t\t\t<param name="sub" value="$PARAM[group_label]"/>\n\t\t\t</include>\n')
    assert m.count(a) == 1
    m = m.replace(a, a.replace('<include content="AG_TopBar">', '<include content="AG_TopBar" condition="!Skin.HasSetting(aeon.fglass)">')
                  + '\t\t\t<include condition="Skin.HasSetting(aeon.fglass)">Aeon_ClockBox</include>\n'
                  '\t\t\t<include content="FG_PVRTabs" condition="Skin.HasSetting(aeon.fglass)">\n\t\t\t\t<param name="show_group" value="$PARAM[show_group]"/>\n'
                  '\t\t\t\t<param name="group_label" value="$PARAM[group_label]"/>\n\t\t\t\t<param name="content_id" value="$PARAM[content_id]"/>\n\t\t\t</include>\n', 1)
    # the old tab card (group 9000, buttons 100-105) moves into Misc_PVRTabsClassic, loaded by the other themes only, so
    # the ids exist once
    a = '\t\t\t<control type="group" id="9000">\n\t\t\t\t<left>102</left><top>128</top>'
    assert m.count(a) == 1
    s = m.index(a)
    lines = m[s:].split('\n')
    depth, k = 0, 0
    while True:
        depth += lines[k].count('<control') - lines[k].count('</control>')
        k += 1
        if depth == 0:
            break
    old = '\n'.join(lines[:k]) + '\n'
    m = m.replace(old, '\t\t\t<include content="Misc_PVRTabsClassic" condition="!Skin.HasSetting(aeon.fglass)">\n'
                  '\t\t\t\t<param name="content_id" value="$PARAM[content_id]"/>\n\t\t\t</include>\n', 1)
    frame_end = m.index('\t<include name="Misc_PVROptions_Channels">')
    m = m[:frame_end] + ('\t<!-- the area tabs on a card: the themes other than Fused Glass (FG_PVRTabs in Includes_Fused.xml) -->\n'
                         '\t<include name="Misc_PVRTabsClassic">\n\t\t<param name="content_id">9100</param>\n\t\t<definition>\n'
                         + old + '\t\t</definition>\n\t</include>\n\n') + m[frame_end:]
    a = ('\t\t\t<control type="grouplist" id="9001">\n\t\t\t\t<left>subnav_left</left>\n\t\t\t\t<top>misc_nav2_top</top>\n')
    assert m.count(a) == 1
    m = m.replace(a, a + '\t\t\t\t<animation effect="slide" end="$PARAM[fg_subnav_slide]" time="0" condition="Skin.HasSetting(aeon.fglass)">Conditional</animation>\n'
                  '\t\t\t\t<visible>!Skin.HasSetting(aeon.fglass) | $PARAM[fg_subnav]</visible>\n', 1)
    a = '\t\t<param name="options">Misc_None</param>\n\t\t<param name="content_id">9100</param>\n'
    assert m.count(a) == 1
    m = m.replace(a, a + '\t\t<param name="fg_subnav_slide">0,-58</param>\n\t\t<param name="fg_subnav">true</param>\n', 1)
    a = '\t\t\t\t\t<param name="visible" value="$PARAM[show_group]"/>\n'
    assert m.count(a) == 1
    m = m.replace(a, '\t\t\t\t\t<param name="visible" value="$PARAM[show_group] + !Skin.HasSetting(aeon.fglass)"/>\n', 1)
    # the old tab card stays for the other themes: Fused Glass hides it (FG_Hidden9000 below sets an id-less copy away)
io.open(MISC, 'w', encoding='utf-8', newline='\n').write(m)

c = io.open(CHAN, encoding='utf-8').read()
if 'FG_PVRChannels' not in c:
    a = '\t\t<include content="Misc_PVRList">'
    assert c.count(a) == 1
    c = c.replace(a, '\t\t<include condition="Skin.HasSetting(aeon.fglass)">FG_PVRChannels</include>\n\t\t<include content="Misc_PVRList" condition="!Skin.HasSetting(aeon.fglass)">', 1)
    a = '\t\t\t<param name="options" value="Misc_PVROptions_Channels"/>\n'
    assert c.count(a) == 1
    c = c.replace(a, a + '\t\t\t<param name="group_label" value="$INFO[Control.GetLabel(29)]"/>\n\t\t\t<param name="fg_subnav_slide" value="2,-36"/>\n', 1)
    io.open(CHAN, 'w', encoding='utf-8', newline='\n').write(c)

g = io.open(GUIDE, encoding='utf-8').read()
if 'FG_PVRGuideBack' not in g:
    s = g.index('\t\t<!-- Fused Glass (0.39.7, mockup A)')
    e = g.index('\t\t<!-- ====== grid')
    g = g[:s] + '\t\t<!-- Fused Glass (0.46.0, mockups LiveTVGuide / LiveTVGuideOverlay): _src/fg_livetv.py -->\n\t\t<include condition="Skin.HasSetting(aeon.fglass)">FG_PVRGuideBack</include>\n' + g[e:]
    a = '\t\t\t<param name="show_group" value="true"/>\n\t\t</include>'
    assert g.count(a) == 1
    g = g.replace(a, '\t\t\t<param name="show_group" value="true"/>\n\t\t\t<param name="fg_subnav" value="false"/>\n\t\t</include>', 1)
    a = '\t\t\t\t<onback>ActivateWindow(pvrguidecontrols)</onback>\n'
    assert g.count(a) == 1
    g = g.replace(a, '\t\t\t\t<onback condition="!$EXP[FG_GuideOSD]">ActivateWindow(pvrguidecontrols)</onback>\n'
                  '\t\t\t\t<onback condition="$EXP[FG_GuideOSD]">6057</onback>\n', 1)
    a = '\t\t\t\t<onup>9001</onup>\n\t\t\t\t<pagecontrol>60</pagecontrol>'
    assert g.count(a) == 1
    g = g.replace(a, '\t\t\t\t<onup condition="!Skin.HasSetting(aeon.fglass)">9001</onup>\n\t\t\t\t<onup condition="Skin.HasSetting(aeon.fglass)">6056</onup>\n\t\t\t\t<pagecontrol>60</pagecontrol>', 1)
    a = '\t<onload>ClearProperty(aeon.pvrnav,home)</onload>\n'
    assert g.count(a) == 1
    g = g.replace(a, a + '\t<onunload>ClearProperty(aeon.guide.osd,home)</onunload>\n'
                  '\t<!-- over the playing channel: start on the playing channel (now, and again once the grid has loaded) -->\n'
                  '\t<onload condition="$EXP[FG_GuideOSD]">PVR.EpgGridControl(PlayingChannel)</onload>\n'
                  '\t<onload condition="$EXP[FG_GuideOSD]">AlarmClock(fgguideplaying,PVR.EpgGridControl(PlayingChannel),00:01,silent)</onload>\n', 1)
    io.open(GUIDE, 'w', encoding='utf-8', newline='\n').write(g)

# the Planner's day list: the slim scroll bar on Fused Glass
PLAN = os.path.join(D, 'Custom_1168_Planner.xml')
pl = io.open(PLAN, encoding='utf-8').read()
old = ('\t\t<include content="Aeon_E_Scroll"><param name="sid" value="9580"/><param name="list" value="9500"/>'
       '<param name="vis" value="String.IsEqual(Window(Home).Property(aeon.planner.mode),day)"/></include>\n')
if 'FG_ScrollPill' not in pl:
    assert pl.count(old) == 1
    pl = pl.replace(old, old.replace('<include content="Aeon_E_Scroll">', '<include content="Aeon_E_Scroll" condition="!Skin.HasSetting(aeon.fglass)">')
                    + '\t\t<include content="FG_ScrollPill" condition="Skin.HasSetting(aeon.fglass)"><param name="sid" value="9580"/><param name="list" value="9500"/>'
                    '<param name="left" value="1846"/><param name="top" value="298"/><param name="height" value="740"/>'
                    '<param name="vis" value="String.IsEqual(Window(Home).Property(aeon.planner.mode),day)"/></include>\n', 1)
    io.open(PLAN, 'w', encoding='utf-8', newline='\n').write(pl)
ET.parse(PLAN)

# the channel list over live TV: Fused Glass loads FG_ChOSD; the old panel (list 11, scrollbar 60, label 2) moves into
# ChOSD_Classic (Includes_Misc.xml) for the other themes, so the ids exist once
CHOSD = os.path.join(D, 'DialogPVRChannelsOSD.xml')
o = io.open(CHOSD, encoding='utf-8').read()
if 'FG_ChOSD' not in o:
    s = o.index('\t<controls>\n') + len('\t<controls>\n')
    e = o.index('\t</controls>')
    classic = o[s:e]
    o = (o[:s] + '\t\t<include condition="Skin.HasSetting(aeon.fglass)">FG_ChOSD</include>\n'
         '\t\t<include condition="!Skin.HasSetting(aeon.fglass)">ChOSD_Classic</include>\n' + o[e:])
    o = o.replace('\t<defaultcontrol always="true">11</defaultcontrol>\n',
                  '\t<defaultcontrol always="true">11</defaultcontrol>\n'
                  '\t<!-- 0.46.0: the player controls\' Groups button opens the list with the group pill in focus -->\n'
                  '\t<onload condition="!String.IsEmpty(Window(Home).Property(aeon.osdch.groups)) + Skin.HasSetting(aeon.fglass)">SetFocus(30)</onload>\n'
                  '\t<onload>ClearProperty(aeon.osdch.groups,home)</onload>\n', 1)
    io.open(CHOSD, 'w', encoding='utf-8', newline='\n').write(o)
    mm = io.open(MISC, encoding='utf-8').read()
    if 'name="ChOSD_Classic"' not in mm:
        mm = mm.replace('</includes>', '\t<!-- the channel list over live TV (DialogPVRChannelsOSD): the themes other than Fused Glass (FG_ChOSD) -->\n'
                        '\t<include name="ChOSD_Classic">\n' + classic + '\t</include>\n</includes>')
        io.open(MISC, 'w', encoding='utf-8', newline='\n').write(mm)
for name in (FUSED, MISC, CHAN, GUIDE, CHOSD):
    ET.parse(name)
print('ok', len(BLOCK) // 1024, 'KB')
