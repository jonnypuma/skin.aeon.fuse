"""0.56.53 (helper 0.3.114):
- Skin settings > Libraries: Update and clean on another Kodi (row 9502, switch aeon.libremote), Address (9503),
  User name (9504), Password (9505), Test connection (9506). The four setting rows show only while the switch is on.
- Skin settings > System: Recommended add-ons (row 9507, after Import): the helper's list of optional add-ons, OK
  installs one (its repository first when needed).
- Every UpdateLibrary / CleanLibrary of the skin goes through RunScript(script.aeon.helper,lib,update|clean,video|music),
  which runs it here or sends it to the other Kodi.
Run from the skin folder, then ok_only.py. Repeatable."""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import settings_rows as sr  # noqa: E402

X = os.path.join(HERE, '..', '1080i')
P = os.path.join(X, 'SkinSettings.xml')
SET = os.path.join(X, 'Includes_Settings.xml')
A = '$ADDON[skin.aeon.fuse %d]'
ON = 'Skin.HasSetting(aeon.libremote)'

# row, after, label, icon, onclick, value variable, help, dimmed with the switch, list (onback)
VALUE_ROWS = [
    (9503, 9502, 32772, 'cloud.png', 'libremote,address', 'Aeon_LibRemoteHost', 32777, True, 9567),
    (9504, 9503, 32773, 'artist.png', 'libremote,user', 'Aeon_LibRemoteUser', 32778, True, 9567),
    (9505, 9504, 32774, 'lock.png', 'libremote,password', 'Aeon_LibRemotePass', 32778, True, 9567),
    (9506, 9505, 32775, 'check.png', 'libremote,test', 'Aeon_LibRemoteTest', 32779, True, 9567),
    (9507, 9514, 32762, 'stack.png', 'addonrec', 'Aeon_RecCount', 32719, False, 9553),
]

VARS = '''\t<!-- 0.56.53 libremote / recommended add-ons rows (helper remotelib.py, addonrec.py) -->
\t<variable name="Aeon_LibRemoteHost">
\t\t<value condition="!String.IsEmpty(Skin.String(aeon.libremote.host))">$INFO[Skin.String(aeon.libremote.host)]</value>
\t\t<value>$ADDON[skin.aeon.fuse 32780]</value>
\t</variable>
\t<variable name="Aeon_LibRemoteUser">
\t\t<value condition="!String.IsEmpty(Skin.String(aeon.libremote.user))">$INFO[Skin.String(aeon.libremote.user)]</value>
\t\t<value>$ADDON[skin.aeon.fuse 32780]</value>
\t</variable>
\t<variable name="Aeon_LibRemotePass">
\t\t<value condition="Skin.HasSetting(aeon.libremote.pwset)">&#8226;&#8226;&#8226;&#8226;&#8226;&#8226;</value>
\t\t<value>$ADDON[skin.aeon.fuse 32780]</value>
\t</variable>
\t<variable name="Aeon_LibRemoteTest">
\t\t<value>$INFO[Skin.String(aeon.libremote.status)]</value>
\t</variable>
\t<variable name="Aeon_RecCount">
\t\t<value>$INFO[Skin.String(aeon.rec.count)]</value>
\t</variable>
'''

BUILTIN = re.compile(r'\b(UpdateLibrary|CleanLibrary)\((video|music)\)')


def route(text):
    return BUILTIN.sub(lambda m: 'RunScript(script.aeon.helper,lib,%s,%s)'
                       % ('update' if m.group(1) == 'UpdateLibrary' else 'clean', m.group(2)), text)


def main():
    t = io.open(P, encoding='utf-8').read()
    if 'id="9502"' not in t:
        item = sr.clone(t, 9726, 9502, [
            ('$LOCALIZE[31880]', A % 32771), ('aeon/icons/lock.png', 'aeon/icons/cloud.png'),
            ('row 9502 -->', 'row 9502 (0.56.53 libremote) -->')])
        item = item.replace('aeon.kiosk', 'aeon.libremote')
        t = sr.insert_after(t, 9726, item)
    for rid, after, label, icon, click, var, _h, dim, back in VALUE_ROWS:
        if 'id="%d"' % rid in t:
            continue
        item = sr.clone(t, 9780, rid, [
            ('$ADDON[skin.aeon.fuse 32645]', A % label), ('aeon/icons/layers.png', 'aeon/icons/' + icon),
            ('RunScript(script.aeon.helper,chippick)', 'RunScript(script.aeon.helper,%s)' % click),
            ('$VAR[Aeon_ChipsShown]', '$VAR[%s]' % var), ('$VAR[Aeon_ChipsShown]', '$VAR[%s]' % var),
            ('<onback>9566</onback>', '<onback>%d</onback>' % back), ('SetFocus(9566)', 'SetFocus(%d)' % back),
            ('0.56.22 chips', '0.56.53 %s' % click.split(',')[-1])])
        t = sr.insert_after(t, after, item)
        if dim:     # hidden while the switch is off (user, 2026-11-19)
            t = sr.set_item_visible(t, rid, ON)
    if 'RunScript(script.aeon.helper,addonrec,count)' not in t:
        t = t.replace('\t<onload>SetProperty(aeon.skincat,appearance,home)</onload>',
                      '\t<onload>SetProperty(aeon.skincat,appearance,home)</onload>\n'
                      '\t<onload>RunScript(script.aeon.helper,addonrec,count)</onload>', 1)
    t = sr.renav(t, 9777)
    t = sr.renav(t, 9769)
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)

    s = io.open(SET, encoding='utf-8').read()
    if '<variable name="Aeon_LibRemoteHost">' not in s:
        i = s.index('\t<!-- 0.56.52 places:')
        s = s[:i] + VARS + s[i:]
    for rid, help_id in [(9502, 32776)] + [(r[0], r[6]) for r in VALUE_ROWS]:
        s = sr.add_help(s, rid, help_id)
    io.open(SET, 'w', encoding='utf-8', newline='\n').write(s)

    n = 0
    for f in sorted(os.listdir(X)):
        if not f.endswith('.xml'):
            continue
        p = os.path.join(X, f)
        a = io.open(p, encoding='utf-8').read()
        b = route(a)
        if a != b:
            n += len(BUILTIN.findall(a))
            io.open(p, 'w', encoding='utf-8', newline='\n').write(b)
    print('libremote: rows 9502-9507, %d library calls routed through the helper' % n)


if __name__ == '__main__':
    main()
