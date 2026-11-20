# -*- coding: utf-8 -*-
"""0.56.22 splash, after the box check of splash_05622.py. Runs once (marker).

- The held dialog slides 4000 px down (1400 left the Mosaic dialog's tall dim layer over the lower splash).
- While a dialog is held the splash's "OK or Back skips" must not answer it: the dialog's own buttons are below the
  screen but still focused, so OK would press the caller's default (CoreELEC's update question could be Yes). The dialog
  now opens on an invisible guard button (9990) while it is held; OK or Back on it ends the splash only and focuses No
  (10). When the splash ends by itself, the splash's timer moves the focus from the guard to No as well."""
import io
import os
import xml.etree.ElementTree as ET

MARK = '0.56.22 splash_b'
CONFIRM = os.path.join('1080i', 'DialogConfirm.xml')
TIMERS = os.path.join('1080i', 'Timers.xml')


def main():
    c = io.open(CONFIRM, encoding='utf-8').read()
    if MARK in c:
        print('already')
        return
    old = '<animation effect="slide" end="0,1400" time="0" condition="$EXP[Aeon_SplHold]">Conditional</animation>'
    assert c.count(old) == 1
    c = c.replace(old, '<animation effect="slide" end="0,4000" time="0" condition="$EXP[Aeon_SplHold]">Conditional</animation>')
    old = '\t<include>Anim_DialogOpenClose</include>\n'
    assert c.count(old) == 1
    c = c.replace(old, old + '\t<!-- %s: a dialog held back by the splash opens on the guard button -->\n'
                             '\t<onload condition="$EXP[Aeon_SplHold]">SetFocus(9990)</onload>\n' % MARK)
    old = '\t\t<!-- 0.56.22 splash: the toast on the splash'
    assert c.count(old) == 1
    guard = ('\t\t<!-- %s: the guard while the dialog is held: OK or Back ends the splash, then No has the focus -->\n'
             '\t\t<control type="button" id="9990"><left>0</left><top>0</top><width>1</width><height>1</height><label></label>'
             '<texturefocus></texturefocus><texturenofocus></texturenofocus><onup>noop</onup><ondown>noop</ondown><onleft>noop</onleft><onright>noop</onright>'
             '<onclick>ClearProperty(aeon.splash,home)</onclick><onclick>SetFocus(10)</onclick>'
             '<onback>ClearProperty(aeon.splash,home)</onback><onback>SetFocus(10)</onback></control>\n') % MARK
    c = c.replace(old, guard + old)
    io.open(CONFIRM, 'w', encoding='utf-8', newline='\n').write(c)
    ET.parse(CONFIRM)
    t = io.open(TIMERS, encoding='utf-8').read()
    old = '\t\t<onstart condition="Window.IsActive(home) + Control.HasFocus(9999)">SetFocus(9000)</onstart>\n'
    assert t.count(old) == 1
    t = t.replace(old, old + '\t\t<onstart condition="Control.HasFocus(9990)">SetFocus(10)</onstart><!-- %s: a held dialog gets No -->\n' % MARK)
    io.open(TIMERS, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(TIMERS)
    print('ok')


if __name__ == '__main__':
    main()
