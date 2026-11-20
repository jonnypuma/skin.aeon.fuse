# -*- coding: utf-8 -*-
"""0.56.20 small fixes from the user's notes of 2026-11-17 (each step once, by its own marker):
a) "When i navigate up to a TV Show's spotlight and then go to the autoscroll cycler, when on any of the autoscroll
   items, OK does not work. It does not take me to that tv show in the library." - the Home spotlight lists of the TV
   shows (9422) and of the music (9423) list folders (shows, albums) but their <content> had no target, so Kodi had no
   window to open a folder in and OK did nothing. target="videos" / "music" opens it in the library.
b) "Language flags OSD information - use rounded language icons addon for fused glass - optional dependency": the
   Fused Glass player's audio / subtitle flags come from resource.images.languageflags.rounded when it is installed
   (34 x 34 circles), else from the colour pack as before, else the code as text; addon.xml imports it as optional."""
import io
import os
import sys
import xml.etree.ElementTree as ET

HOME = os.path.join('1080i', 'Includes_Aeon_Home.xml')


def swap(t, old, new, count=1):
    n = t.count(old)
    assert n == count, (old[:140], n, count)
    return t.replace(old, new)


def step_a():
    t = io.open(HOME, encoding='utf-8').read()
    mark = '0.56.20 misc a'
    if mark in t:
        return 'a already'
    t = swap(t, '<content sortby="$VAR[Aeon_SP2Sort_tv]"', '<content target="videos" sortby="$VAR[Aeon_SP2Sort_tv]"')
    t = swap(t, '<content sortby="$VAR[Aeon_SP2Sort_music]"', '<content target="music" sortby="$VAR[Aeon_SP2Sort_music]"')
    t = swap(t, '\t\t<control type="wraplist" id="9422">', '\t\t<!-- %s: OK on a show / album of the spotlight opens it in the library (the lists had no target) -->\n\t\t<control type="wraplist" id="9422">' % mark)
    io.open(HOME, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(HOME)
    return 'a ok'


def step_b():
    p = os.path.join('1080i', 'Includes_FusedPlayer.xml')
    t = io.open(p, encoding='utf-8').read()
    mark = '0.56.20 misc b'
    if mark in t:
        return 'b already'
    ROUND = 'System.AddonIsEnabled(resource.images.languageflags.rounded)'
    COLOUR = 'System.AddonIsEnabled(resource.images.languageflags.colour)'
    for info in ('VideoPlayer.AudioLanguage', 'VideoPlayer.SubtitlesLanguage'):
        old_img = '<control type="image"><width>44</width><height>34</height><aspectratio>keep</aspectratio><texture>$INFO[%s,resource://resource.images.languageflags.colour/,.png]</texture>' % info
        assert t.count(old_img) == 1, (info, t.count(old_img))
        a = t.index(old_img)
        b = t.index('</control>', a) + len('</control>')
        line = t[a:b]
        vis = line[line.index('<visible>') + 9:line.index('</visible>')]
        colour_only = line.replace('<visible>' + vis + '</visible>', '<visible>%s + !%s</visible>' % (vis, ROUND))
        rounded = (line.replace('<width>44</width>', '<width>34</width>')
                   .replace('resource://resource.images.languageflags.colour/', 'resource://resource.images.languageflags.rounded/')
                   .replace('<visible>' + vis + '</visible>', '<visible>%s</visible>' % vis.replace(COLOUR, ROUND)))
        t = t[:a] + '<!-- %s: the rounded pack first -->' % mark + rounded + colour_only + t[b:]
    # the text chip shows when no pack is there (or flags are off)
    t = t.replace('+ ![!Skin.HasSetting(aeon.osd.noflags) + %s]"/>' % COLOUR,
                  '+ ![!Skin.HasSetting(aeon.osd.noflags) + [%s | %s]]"/>' % (COLOUR, ROUND))
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(p)
    a = io.open('addon.xml', encoding='utf-8').read()
    if 'resource.images.languageflags.rounded' not in a:
        a = a.replace('\t\t<import addon="resource.images.languageflags.colour" optional="true"/>\n',
                      '\t\t<import addon="resource.images.languageflags.colour" optional="true"/>\n'
                      '\t\t<import addon="resource.images.languageflags.rounded" optional="true"/>\n', 1)
        io.open('addon.xml', 'w', encoding='utf-8', newline='\n').write(a)
    return 'b ok'


def step_c():
    """c) Spotlight window (Custom_1157_Spotlight.xml, Up from a Home spotlight): OK on an item of the cycling list did
    nothing for a show. Its first action closed the window and the next ones read $INFO[ListItem.FolderPath] after
    that, from the window underneath (Home's menu item). Now the item's folder and file go into Home properties
    first, then the window closes, then the library / player opens from those properties. (Kodi checks every
    condition when OK is pressed, while the window is still open, so ListItem.IsFolder stays the condition; only the
    $INFO values of an action are filled in when that action runs.)"""
    p = os.path.join('1080i', 'Custom_1157_Spotlight.xml')
    t = io.open(p, encoding='utf-8').read()
    mark = '0.56.20 misc c'
    if mark in t:
        return 'c already'
    old = ('\t\t\t<onclick>Dialog.Close(1157,true)</onclick>\n'
           '\t\t\t<onclick condition="$EXP[Aeon_SpMusic] + ListItem.IsFolder">ActivateWindow(Music,$INFO[ListItem.FolderPath],return)</onclick>\n'
           '\t\t\t<onclick condition="$EXP[Aeon_SpMusic] + !ListItem.IsFolder">PlayMedia($INFO[ListItem.FileNameAndPath])</onclick>\n'
           '\t\t\t<onclick condition="!$EXP[Aeon_SpMusic] + ListItem.IsFolder">ActivateWindow(Videos,$INFO[ListItem.FolderPath],return)</onclick>\n'
           '\t\t\t<onclick condition="!$EXP[Aeon_SpMusic] + !ListItem.IsFolder">PlayMedia($INFO[ListItem.FileNameAndPath])</onclick>\n')
    n = t.count(old)
    assert n >= 1, n
    G = 'Window(Home).Property(aeon.sp.go)'
    F = 'Window(Home).Property(aeon.sp.file)'
    new = ('\t\t\t<!-- %s: what to open is read before the window closes (afterwards ListItem is Home\'s) -->\n'
           '\t\t\t<onclick>SetProperty(aeon.sp.go,$ESCINFO[ListItem.FolderPath],home)</onclick>\n'
           '\t\t\t<onclick>SetProperty(aeon.sp.file,$ESCINFO[ListItem.FileNameAndPath],home)</onclick>\n'
           '\t\t\t<onclick>Dialog.Close(1157,true)</onclick>\n'
           '\t\t\t<onclick condition="$EXP[Aeon_SpMusic] + ListItem.IsFolder">ActivateWindow(Music,$ESCINFO[%s],return)</onclick>\n'
           '\t\t\t<onclick condition="$EXP[Aeon_SpMusic] + !ListItem.IsFolder">PlayMedia($ESCINFO[%s])</onclick>\n'
           '\t\t\t<onclick condition="!$EXP[Aeon_SpMusic] + ListItem.IsFolder">ActivateWindow(Videos,$ESCINFO[%s],return)</onclick>\n'
           '\t\t\t<onclick condition="!$EXP[Aeon_SpMusic] + !ListItem.IsFolder">PlayMedia($ESCINFO[%s])</onclick>\n' % (mark, G, F, G, F))
    t = t.replace(old, new)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(p)
    return 'c ok (%d lists)' % n


def step_d():
    """d) Fuse survey (finding 5, number pad): the keys of the keyboard and the number pad focused a square block
    (Dlg_Tex_Key_Plain: common/white.png) in Aeon Glass and with the Fuse menu theme, so Done showed as a big white
    square in a rounded card. There the focused key is a 12 px rounded box; Aeon's menu styles keep the square."""
    p = os.path.join('1080i', 'Includes_Dialogs.xml')
    t = io.open(p, encoding='utf-8').read()
    mark = '0.56.20 misc d'
    if mark in t:
        return 'd already'
    old = ('\t<include name="Dlg_Tex_Key_Round">\n\t\t<include condition="Skin.HasSetting(aeon.fglass)">Dlg_Tex_Key_FG</include>\n'
           '\t\t<include condition="!Skin.HasSetting(aeon.fglass)">Dlg_Tex_Key_Plain</include>\n\t</include>')
    assert t.count(old) == 1, t.count(old)
    rnd = '!Skin.HasSetting(aeon.fglass) + [Skin.HasSetting(aeon.vglass) | $EXP[Aeon_Fused]]'
    new = ('\t<!-- %s: Aeon Glass and the Fuse menu theme focus a rounded key -->\n'
           '\t<include name="Dlg_Tex_Key_Fu">\n\t\t<texturefocus border="12" colordiffuse="$VAR[AG_Accent]">fg/r12.png</texturefocus>\n'
           '\t\t<texturenofocus colordiffuse="00ffffff">common/white.png</texturenofocus>\n\t</include>\n'
           '\t<include name="Dlg_Tex_Key_Round">\n\t\t<include condition="Skin.HasSetting(aeon.fglass)">Dlg_Tex_Key_FG</include>\n'
           '\t\t<include condition="%s">Dlg_Tex_Key_Fu</include>\n'
           '\t\t<include condition="!Skin.HasSetting(aeon.fglass) + ![%s]">Dlg_Tex_Key_Plain</include>\n\t</include>' % (mark, rnd, rnd))
    t = t.replace(old, new, 1)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(p)
    return 'd ok'


def step_e():
    """e) (after c, from the box test) the TV spotlight's window lists recent EPISODES; the user: "It does not take me to
    that tv show in the library". OK on an episode opens its show (videodb://tvshows/titles/<TvShowDBID>/); films and
    other files still play, folders still open; nothing happens while the list is empty (still loading)."""
    p = os.path.join('1080i', 'Custom_1157_Spotlight.xml')
    t = io.open(p, encoding='utf-8').read()
    mark = '0.56.20 misc e'
    if mark in t:
        return 'e already'
    G = 'Window(Home).Property(aeon.sp.go)'
    F = 'Window(Home).Property(aeon.sp.file)'
    S = 'Window(Home).Property(aeon.sp.show)'
    old_play = '\t\t\t<onclick condition="!$EXP[Aeon_SpMusic] + !ListItem.IsFolder">PlayMedia($ESCINFO[%s])</onclick>\n' % F
    n = t.count(old_play)
    assert n >= 1, n
    new_play = ('\t\t\t<onclick condition="!$EXP[Aeon_SpMusic] + !ListItem.IsFolder + !String.IsEmpty(ListItem.Label) + !String.IsEqual(ListItem.DBType,episode)">PlayMedia($ESCINFO[%s])</onclick>\n'
                '\t\t\t<onclick condition="!$EXP[Aeon_SpMusic] + String.IsEqual(ListItem.DBType,episode) + !String.IsEmpty(ListItem.TvShowDBID)">ActivateWindow(Videos,videodb://tvshows/titles/$INFO[%s]/,return)</onclick><!-- %s: an episode opens its show -->\n'
                % (F, S, mark))
    t = t.replace(old_play, new_play)
    old_set = '\t\t\t<onclick>SetProperty(aeon.sp.file,$ESCINFO[ListItem.FileNameAndPath],home)</onclick>\n'
    assert t.count(old_set) == n, (t.count(old_set), n)
    t = t.replace(old_set, old_set + '\t\t\t<onclick>SetProperty(aeon.sp.show,$INFO[ListItem.TvShowDBID],home)</onclick>\n')
    for kind in ('Music', 'Videos'):
        o = 'ListItem.IsFolder">ActivateWindow(%s,$ESCINFO[%s],return)</onclick>' % (kind, G)
        t = t.replace(o, 'ListItem.IsFolder + !String.IsEmpty(ListItem.Label)">ActivateWindow(%s,$ESCINFO[%s],return)</onclick>' % (kind, G))
    o = '$EXP[Aeon_SpMusic] + !ListItem.IsFolder">PlayMedia($ESCINFO[%s])' % F
    t = t.replace(o, '$EXP[Aeon_SpMusic] + !ListItem.IsFolder + !String.IsEmpty(ListItem.Label)">PlayMedia($ESCINFO[%s])' % F)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(p)
    return 'e ok (%d lists)' % n


STEPS = {'a': step_a, 'b': step_b, 'c': step_c, 'd': step_d, 'e': step_e}

if __name__ == '__main__':
    for k in (sys.argv[1:] or sorted(STEPS)):
        print(STEPS[k]())
