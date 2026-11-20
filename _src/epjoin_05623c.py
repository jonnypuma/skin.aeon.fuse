# -*- coding: utf-8 -*-
"""0.56.23 Episodes in one file as one row, part 3 (after the box check in Fused Glass):
- the panels' kickers that write episode 1 out ("S6 E1 · Season premiere") show the range ("S6 E1-2 · Season
  premiere") through the range variable of their list;
- the Fused Glass header of a joined season (the helper's list) reads like the season's own: "TV shows › Lost" over
  "Season 6" (Kodi gives a plugin list the add-on's name as its folder name).
Safe to run again."""
import hashlib
import io
import os
import re
import xml.etree.ElementTree as ET

D = '1080i'
FUSED = os.path.join(D, 'Includes_Fused.xml')
SUB = os.path.join(D, 'Includes_Aeon_Sub.xml')
MARK = '0.56.23 epjoin_c'
JOINED = 'String.StartsWith(Container.FolderPath,plugin://script.aeon.helper/?info=episodes)'


def range_var(prefix):
    key = '%s|%s|%s|%s' % (prefix, None, None, False)
    name = 'Aeon_EpN_' + hashlib.md5(key.encode('utf-8')).hexdigest()[:8]
    body = ('\t<variable name="%s">\n\t\t<value condition="!String.IsEmpty(%s.Property(aeon.ep.range))">$INFO[%s.Property(aeon.ep.range)]</value>\n'
            '\t\t<value>$INFO[%s.Episode]</value>\n\t</variable>' % (name, prefix, prefix, prefix))
    return name, body


def main():
    need = {}
    count = 0
    for fname in sorted(os.listdir(D)):
        if not fname.endswith('.xml') or fname in ('Includes_FusedPlayer.xml', 'SkinSettings.xml'):
            continue
        p = os.path.join(D, fname)
        t = io.open(p, encoding='utf-8').read()

        def fix(m):
            nonlocal count
            cond, text = m.group(1), m.group(2)
            em = re.search(r'Integer\.IsEqual\(((?:Container\(\d+\)\.)?ListItem)\.Episode,1\)', cond)
            if not em or ' E1' not in text:
                return m.group(0)
            name, body = range_var(em.group(1))
            need[name] = body
            count += 1
            return '<value condition="%s">%s</value>' % (cond, re.sub(r' E1(?!\d)', ' E$VAR[%s]' % name, text, count=1))
        new = re.sub(r'<value condition="([^"]*)">([^<]*)</value>', fix, t)
        if new != t:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(new)
            ET.parse(p)
    sub = io.open(SUB, encoding='utf-8').read()
    have = set(re.findall(r'<variable name="(Aeon_EpN_\w+)">', sub))
    add = [need[k] for k in sorted(need) if k not in have]
    if add:
        tag = '\t<!-- 0.56.23 epjoin_b: the numbers inside variables and labels -->\n'
        assert sub.count(tag) == 1
        sub = sub.replace(tag, tag + ''.join(v + '\n' for v in add))
        io.open(SUB, 'w', encoding='utf-8', newline='\n').write(sub)
        ET.parse(SUB)
    f = io.open(FUSED, encoding='utf-8').read()
    if MARK not in f:
        old = '\t<variable name="FG_L_Kicker">\n'
        assert f.count(old) == 1
        f = f.replace(old, old + '\t\t<value condition="%s">$LOCALIZE[20343]$INFO[ListItem.TVShowTitle,  ›  ,]</value><!-- %s: a joined season -->\n' % (JOINED, MARK))
        old = '\t<variable name="FG_L_Title">\n'
        assert f.count(old) == 1
        f = f.replace(old, old + '\t\t<value condition="%s + !String.IsEmpty(ListItem.Season)">$LOCALIZE[20373] $INFO[ListItem.Season]</value><!-- %s -->\n' % (JOINED, MARK))
        io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(f)
        ET.parse(FUSED)
    print('kickers', count, 'range variables added', len(add))


if __name__ == '__main__':
    main()
