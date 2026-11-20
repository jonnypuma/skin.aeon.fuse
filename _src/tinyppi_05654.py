# -*- coding: utf-8 -*-
"""0.56.54 TinyPPI is a CoreELEC tool (user: "tiny ppi is not for windows, it's for coreelec yet it was listed as a
requirement when trying to install on windows"). addon.xml no longer imports it (optional imports show in Kodi's
dependency list); here the setup wizard's add-on row: off CoreELEC its second line says "CoreELEC only" (32820) and OK
does not tick it (shown, not hidden). CoreELEC = System.OSVersionInfo holds CoreELEC (as the helper's menufile.py).
Run after _src/wizard_05640.py. Repeatable."""
import io
import os

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
CE = 'String.Contains(System.OSVersionInfo,CoreELEC)'


def main():
    p = os.path.join(D, 'Custom_1173_SetupWizard.xml')
    s = io.open(p, encoding='utf-8').read()
    old = '<onclick condition="!System.HasAddon(script.tinyppi)">Skin.ToggleSetting(aeon.wiz.add.script.tinyppi)</onclick>'
    if old in s:
        s = s.replace(old, '<onclick condition="!System.HasAddon(script.tinyppi) + %s">Skin.ToggleSetting(aeon.wiz.add.script.tinyppi)</onclick>' % CE, 1)
        io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
    p = os.path.join(D, 'Includes_Aeon_Wizard.xml')
    s = io.open(p, encoding='utf-8').read()
    head = '<variable name="Wiz_Addon_script_tinyppi">'
    line = '<value condition="!System.HasAddon(script.tinyppi) + !%s">$ADDON[skin.aeon.fuse 32820]</value>' % CE
    if line not in s:
        i = s.index(head) + len(head)
        s = s[:i] + '\n\t\t' + line + s[i:]
        io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
    print('tinyppi: wizard row CoreELEC only elsewhere')


if __name__ == '__main__':
    main()
