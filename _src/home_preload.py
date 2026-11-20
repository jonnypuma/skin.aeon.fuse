# -*- coding: utf-8 -*-
"""0.56.4 Home: the strips under Movies, TV shows and Music stay loaded, load ahead, and show that they are loading.

The user (2026-11-15): "it's also annoying pressing down on a home menu item and nothing's happening because stuff is
loading, so it would be nice with a loading toast and spinner in the submenu while things load like we do for the
planner, i also think stuff should try to load on progressively on startup as long as no video is playing".

Before: each strip (9301 / 9302 / 9303) took its path from the shared submenu list 9391, which holds the submenu of
the focused Home item, and only while its own item had the focus. Every visit loaded the strip again from nothing
(box: films 1.3 s, TV shows 3.6-4.7 s, music 1.7-2.0 s), and Down did nothing until it had.
Now:
  - three hidden submenu lists of their own, 93911 / 93912 / 93913 (guid-aeon0001 / 0002 / 0003), give the strips
    their paths (Aeon_StripPath_*), whichever Home item has the focus, so a strip loads once and keeps its titles.
    9391 stays the list the submenu is drawn from.
  - a section loads once it is armed: Window(Home).Property(aeon.pl.<sec>). The skin timer aeonhomearm arms the
    focused one at once; the helper's service arms all three one after another after Kodi starts, while Home is open
    and no video plays (script.aeon.helper service.py HomePreload).
  - while the focused item's strip loads, the Planner's capsule (spinner + Loading..., Fused Glass panel or a dark
    box) sits where the submenu opens, under the menu on the left (Aeon_H_StripLoading).
  - Down waits for the strip up to 45 s while it loads or refreshes, the menu keeping the focus (swap.py focusstrip).
Run from the skin folder; safe to run again."""
import io
import os
import re

SECS = (('movies', 1, 9301), ('tv', 2, 9302), ('music', 3, 9303))
NODE = ('plugin://script.skinvariables/?info=get_shortcuts_node&amp;menu=aeonmenu&amp;skin=skin.aeon.fuse&amp;mode=submenu'
        '&amp;guid=guid-aeon000%d$INFO[Window(Home).Property(SkinVariables.ShortcutsNode.Reload),&amp;reload=,]')
ARMED = '!String.IsEmpty(Window(Home).Property(aeon.pl.%s))'


def rd(p):
    return io.open(p, encoding='utf-8').read()


def wr(p, t):
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)


def sub_vars():
    p = os.path.join('1080i', 'Includes_Aeon_Sub.xml')
    t = rd(p)
    if 'name="Aeon_H_NodeFix_movies"' not in t:
        add = ['\t<!-- 0.56.4: the submenu of Movies / TV shows / Music for its strip, once the section is armed '
               '(_src/home_preload.py) -->\n']
        for sec, n, _ in SECS:
            add.append('\t<variable name="Aeon_H_NodeFix_%s">\n\t\t<value condition="%s">%s</value>\n\t</variable>\n'
                       % (sec, ARMED % sec, NODE % n))
        a = t.find('\t<variable name="Aeon_StripPath_movies">')
        t = t[:a] + ''.join(add) + t[a:]
    for sec, n, _ in SECS:
        a = t.find('\t<variable name="Aeon_StripPath_%s">' % sec)
        b = t.find('</variable>', a)
        v = t[a:b]
        v2 = v.replace('String.IsEqual(Container(9000).ListItem.Label2,%s) + ' % sec, '')
        v2 = v2.replace('Container(9391)', 'Container(9391%d)' % n)
        t = t[:a] + v2 + t[b:]
        print('Aeon_StripPath_%s: %s' % (sec, 'from 9391%d' % n if v2 != v else 'already'))
    wr(p, t)


def home():
    p = os.path.join('1080i', 'Includes_Aeon_Home.xml')
    t = rd(p)
    # the three lists, next to 9391
    if 'id="93911"' not in t:
        a = t.find('<control type="list" id="9391">')
        b = t.find('</control>', a) + len('</control>\n')
        lists = ['\t\t<!-- 0.56.4: each strip\'s own submenu list, loaded once its section is armed (_src/home_preload.py) -->\n']
        for sec, n, _ in SECS:
            lists.append('\t\t<control type="list" id="9391%d">\n'
                         '\t\t\t<left>2000</left><top>%d</top><width>10</width><height>10</height>\n'
                         '\t\t\t<itemlayout width="10" height="10"/><focusedlayout width="10" height="10"/>\n'
                         '\t\t\t<content>$VAR[Aeon_H_NodeFix_%s]</content>\n'
                         '\t\t</control>\n' % (n, 20 * n, sec))
        t = t[:b] + ''.join(lists) + t[b:]
        print('lists 93911-93913')
    # a strip slides out of sight unless it has the focus itself: it went only while no strip had the focus, when the
    # other two were empty anyway (their paths waited for their own item); now all three keep their titles
    old = ('<animation effect="slide" end="0,420" time="0" condition="[![Control.HasFocus(9301) | Control.HasFocus(9302) | '
           'Control.HasFocus(9303)] | Container($PARAM[id]).IsUpdating | ![$PARAM[visible]]]">Conditional</animation>')
    if old in t:
        t = t.replace(old, '<animation effect="slide" end="0,420" time="0" condition="[!Control.HasFocus($PARAM[id]) | '
                           'Container($PARAM[id]).IsUpdating | ![$PARAM[visible]]]">Conditional</animation>')
        print('strips: only the focused one in sight')
    # Down from the menu: straight into a strip that is in; one still loading (or refreshing after a library change:
    # it is out of sight meanwhile) keeps the menu and its Loading... capsule, and the helper lands when it is in
    for sec, n, cid in SECS:
        exp = {'movies': 'Movies', 'tv': 'TV', 'music': 'Music'}[sec]
        old = ('<ondown condition="$EXP[Aeon_H_%s] + !Integer.IsGreater(Container(%d).NumItems,0)">RunScript(script.aeon.helper,focusstrip,%d)</ondown>'
               '<ondown condition="$EXP[Aeon_H_%s]">SetFocus(%d)</ondown>' % (exp, cid, cid, exp, cid))
        new = ('<ondown condition="$EXP[Aeon_H_%s] + [!Integer.IsGreater(Container(%d).NumItems,0) | Container(%d).IsUpdating]">RunScript(script.aeon.helper,focusstrip,%d)</ondown>'
               '<ondown condition="$EXP[Aeon_H_%s] + Integer.IsGreater(Container(%d).NumItems,0) + !Container(%d).IsUpdating">SetFocus(%d)</ondown>'
               % (exp, cid, cid, cid, exp, cid, cid, cid))
        if old in t:
            t = t.replace(old, new)
            print('Down to %d waits while it loads' % cid)
    # the capsule, over the strips (same Low position groups)
    if '<include>Aeon_H_StripLoading</include>' not in t:
        a = t.find('\t\t<!-- category of the strip (Up on a title lists the others) -->')
        t = t[:a] + '\t\t<include>Aeon_H_StripLoading</include>\n' + t[a:]
        print('capsule placed')
    t = t.replace('<!-- strips (also the hero source). Always loaded: a hidden list drops its items and has to load them again, so Down\n'
                  '\t\t     from the menu did nothing until it had; they slide out of sight while they have no focus (Aeon_H_Strip) -->',
                  '<!-- strips (also the hero source). Always loaded: a hidden list drops its items and has to load them again, so Down\n'
                  '\t\t     from the menu did nothing until it had; they slide out of sight while they have no focus (Aeon_H_Strip).\n'
                  '\t\t     0.56.4: their paths come from their own submenu lists (93911-93913), so they keep their titles when\n'
                  '\t\t     the menu moves on; a section loads once armed (aeon.pl.<sec>: Timers.xml aeonhomearm, the helper\'s\n'
                  '\t\t     HomePreload); Aeon_H_StripLoading while the focused one loads -->')
    if '<include name="Aeon_H_StripLoading">' not in t:
        load = ' | '.join('[$EXP[Aeon_H_%s] + [String.IsEmpty(Window(Home).Property(aeon.pl.%s)) | Container(9391%d).IsUpdating | Container(%d).IsUpdating]]'
                          % ({'movies': 'Movies', 'tv': 'TV', 'music': 'Music'}[sec], sec, n, cid) for sec, n, cid in SECS)
        inc = ('\t<!-- 0.56.4: Loading... while the strip of the focused Movies / TV shows / Music loads (_src/home_preload.py),\n'
               '\t     where the submenu opens (level with its first row, 764, under the menu band that ends at 759); the Planner\'s capsule -->\n'
               '\t<expression name="Aeon_H_StripLoad">%s</expression>\n'
               '\t<include name="Aeon_H_StripLoading">\n'
               '\t\t<control type="group">\n'
               '\t\t\t<left>352</left><top>764</top>\n'
               '\t\t\t<visible>Control.HasFocus(9000) + $EXP[Aeon_H_StripLoad]</visible>\n'
               '\t\t\t<animation type="Visible"><effect type="fade" start="0" end="100" delay="250" time="200"/></animation>\n'
               '\t\t\t<animation type="Hidden"><effect type="fade" start="100" end="0" time="150"/></animation>\n'
               '\t\t\t<control type="image"><width>288</width><height>64</height><texture border="32" colordiffuse="$VAR[FG_Panel]">fg/r32.png</texture><visible>$EXP[Aeon_FGlass]</visible></control>\n'
               '\t\t\t<control type="image"><width>288</width><height>64</height><texture border="32" colordiffuse="$VAR[FG_Edge]">fg/e32.png</texture><visible>$EXP[Aeon_FGlass]</visible></control>\n'
               '\t\t\t<control type="image"><left>12</left><top>12</top><width>40</width><height>40</height><texture colordiffuse="1fffffff">fg/circle.png</texture><visible>$EXP[Aeon_FGlass]</visible></control>\n'
               '\t\t\t<control type="image"><width>288</width><height>64</height><texture colordiffuse="80000000">common/white.png</texture><visible>!$EXP[Aeon_FGlass]</visible></control>\n'
               '\t\t\t<control type="image"><left>18</left><top>18</top><width>28</width><height>28</height><texture colordiffuse="ffffffff">common/aeon_spinner.gif</texture><visible>!Skin.HasSetting(aeon.reducemotion)</visible></control>\n'
               '\t\t\t<control type="image"><left>18</left><top>18</top><width>28</width><height>28</height><texture colordiffuse="ffffffff">common/aeon_spinner_still.png</texture><visible>Skin.HasSetting(aeon.reducemotion)</visible></control>\n'
               '\t\t\t<control type="label"><left>64</left><top>0</top><width>200</width><height>64</height><aligny>center</aligny><font>ui_22</font><textcolor>ffffffff</textcolor><label>$LOCALIZE[31952]</label></control>\n'
               '\t\t</control>\n'
               '\t</include>\n' % load)
        a = t.find('\t<include name="Aeon_H_Strip">')
        t = t[:a] + inc + t[a:]
        print('capsule include')
    wr(p, t)


def timer():
    p = os.path.join('1080i', 'Timers.xml')
    t = rd(p)
    if '<name>aeonhomearm</name>' in t:
        return
    start = ' | '.join('[String.IsEqual(Container(9000).ListItem.Label2,%s) + String.IsEmpty(Window(Home).Property(aeon.pl.%s))]'
                       % (sec, sec) for sec, _, _ in SECS)
    ons = ''.join('\t\t<onstop condition="String.IsEqual(Container(9000).ListItem.Label2,%s)">SetProperty(aeon.pl.%s,1,home)</onstop>\n'
                  % (sec, sec) for sec, _, _ in SECS)
    block = ('\t<timer>\n'
             '\t\t<name>aeonhomearm</name>\n'
             '\t\t<description>0.56.4: Home strip of the focused Movies / TV shows / Music loads and stays loaded (_src/home_preload.py)</description>\n'
             '\t\t<start>Window.IsActive(home) + [%s]</start>\n'
             '\t\t<stop>true</stop>\n%s'
             '\t</timer>\n' % (start, ons))
    a = t.rfind('</timers>')
    wr(p, t[:a] + block + t[a:])
    print('timer aeonhomearm')


if __name__ == '__main__':
    sub_vars()
    home()
    timer()
