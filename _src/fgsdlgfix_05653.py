# -*- coding: utf-8 -*-
"""0.56.53 Fused Glass style dialogs (user, 2026-11-20, box):
1. "the context menu you have forgotten to add the focus highlight shadow and dark background too, same for the
   Manage... submenu": Kodi clones those rows from one button (FGS_DlgRow), which cannot carry the shadow image; its
   focus texture becomes the bar with the dark fill baked in (fg/fgs_bar_dk.png), as Kodi's settings rows. Every
   dialog row on FGS_DlgRow (context menu, Manage..., Select's buttons, ...) follows.
2. "the 'Select movie to add as a version' window is missing the movie title which you want to add a version to": the
   version manager (DialogVideoManager) keeps its film's title in Window(Home).Property(aeon.vm.title) while it is
   open; Select shows it in front of its heading (the lead of the style's header), as the context menu shows its item.
3. "the browse files and browse library buttons on the bottom are disconnected from the list box": Select's extra
   buttons (5, 8 in 9001) are the frame's last row (882-951, cells from the frame's left line, 361-1539), the frame's
   lines carried down to them; only while one of them shows.
Repeatable."""
import io
import os

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
FUSED = os.path.join(D, 'Includes_Fused.xml')
VM = os.path.join(D, 'DialogVideoManager.xml')


def block(t, name):
    i = t.index('<include name="%s">' % name)
    return i, t.index('\n\t</include>', i)


def main():
    t = io.open(FUSED, encoding='utf-8').read()
    i, e = block(t, 'FGS_DlgRow')
    t = t[:i] + t[i:e].replace('colordiffuse="ffffffff">fg/fgs_bar.png</texturefocus>', 'colordiffuse="ffffffff">fg/fgs_bar_dk.png</texturefocus>') + t[e:]
    i, e = block(t, 'FGS_Select')
    seg = t[i:e]
    if '<!-- dlgfix -->' not in seg:
        seg = seg.replace('<include content="FGS_DlgHeader"><param name="label" value="$INFO[Control.GetLabel(1)]"/></include>',
                          '<!-- dlgfix --><include content="FGS_DlgHeader"><param name="lead" value="$INFO[Window(Home).Property(aeon.vm.title)]"/>'
                          '<param name="leadvis" value="!String.IsEmpty(Window(Home).Property(aeon.vm.title))"/>'
                          '<param name="label" value="$INFO[Control.GetLabel(1)]"/></include>', 1)
        joined = ('<control type="group"><visible>Control.IsVisible(5) | Control.IsVisible(8)</visible>'
                  '<control type="image"><left>360</left><top>881</top><width>1</width><height>71</height><texture colordiffuse="1affffff">common/white.png</texture></control>'
                  '<control type="image"><left>1560</left><top>881</top><width>1</width><height>71</height><texture colordiffuse="1affffff">common/white.png</texture></control>'
                  '<control type="image"><left>360</left><top>951</top><width>1201</width><height>1</height><texture colordiffuse="1affffff">common/white.png</texture></control>'
                  '</control>')
        seg = seg.replace('<control type="grouplist" id="9001">\n\t\t\t\t<left>810</left><top>900</top><width>750</width><height>70</height>',
                          joined + '<control type="grouplist" id="9001">\n\t\t\t\t<left>361</left><top>882</top><width>1199</width><height>69</height>', 1)
        t = t[:i] + seg + t[e:]
    # 2b. the same film in the yes/no Kodi shows instead of the list when no similar film is in the library
    i, e = block(t, 'FGS_Confirm')
    seg = t[i:e]
    if 'aeon.vm.title' not in seg:
        seg = seg.replace('<include content="FGS_DlgHeader"><param name="label" value="$INFO[Control.GetLabel(1)]"/></include>',
                          '<include content="FGS_DlgHeader"><param name="lead" value="$INFO[Window(Home).Property(aeon.vm.title)]"/>'
                          '<param name="leadvis" value="!String.IsEmpty(Window(Home).Property(aeon.vm.title))"/>'
                          '<param name="label" value="$INFO[Control.GetLabel(1)]"/></include>', 1)
        t = t[:i] + seg + t[e:]
    # 4. "the path on the movies in the list shall scroll so you can see full path": the second line (label2: the
    #    path) of the focused row scrolls; the others stay cut
    i, e = block(t, 'FGS_SelRow')
    seg = t[i:e]
    old = ('<control type="label"><left>486</left><top>40</top><width>658</width><height>24</height><aligny>center</aligny>'
           '<font>st_small_20</font><textcolor>80ffffff</textcolor><label>$INFO[ListItem.Label2]</label><visible>$PARAM[pic]</visible></control>')
    if old in seg:
        new = (old.replace('<visible>$PARAM[pic]</visible>', '<visible>$PARAM[pic] + ![$PARAM[focus] + Control.HasFocus($PARAM[id])]</visible>')
               + old.replace('<visible>$PARAM[pic]</visible>', '<scroll>true</scroll><visible>$PARAM[pic] + $PARAM[focus] + Control.HasFocus($PARAM[id])</visible>')
               + '<!-- path scrolls -->')
        t = t[:i] + seg.replace(old, new, 1) + t[e:]
    io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(t)
    v = io.open(VM, encoding='utf-8').read()
    if 'aeon.vm.title' not in v:
        v = v.replace('<include>Anim_DialogOpenClose</include>',
                      '<onload>SetProperty(aeon.vm.title,$INFO[ListItem.Title],home)</onload>\n'
                      '\t<onunload>ClearProperty(aeon.vm.title,home)</onunload><!-- 0.56.53 Select shows which film -->\n'
                      '\t<include>Anim_DialogOpenClose</include>', 1)
        io.open(VM, 'w', encoding='utf-8', newline='\n').write(v)
    print('dialog rows dark fill; Select: the film, joined buttons')


if __name__ == '__main__':
    main()
