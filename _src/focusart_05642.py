# -*- coding: utf-8 -*-
"""0.56.42 the focused title's art at once in a big library (helper 0.3.108 focusart.py publishes the focused item's
poster / fanart / thumb / landscape / clearlogo from the library as Window(Home).Property(aeon.fart.<kind>), with
aeon.fart.type and aeon.fart.dbid naming the item).

In every skin variable, right after a value that shows an item's own picture
    <value condition="!String.IsEmpty(X.Art(K))">$INFO[X.Art(K)]</value>      X = ListItem or Container(n).ListItem
comes the helper's copy of that picture, used only while the item's own is still empty and the copy belongs to that item:
    <value condition="String.IsEqual(Window(Home).Property(aeon.fart.dbid),X.DBID) + String.IsEqual(Window(Home).Property(aeon.fart.type),X.DBType)
                      + !String.IsEmpty(Window(Home).Property(aeon.fart.K))">$INFO[Window(Home).Property(aeon.fart.K)]</value>
Repeatable (a value that has its copy is left alone). Prints how many it added per file."""
import io
import os
import re
import xml.etree.ElementTree as ET

D = '1080i'
KINDS = ('poster', 'fanart', 'thumb', 'landscape', 'clearlogo')
LINE = re.compile(r'([ \t]*)<value condition="!String\.IsEmpty\(((?:Container\(\d+\)\.)?ListItem)\.Art\((%s)\)\)">'
                  r'\$INFO\[\2\.Art\(\3\)\]</value>\n' % '|'.join(KINDS))


def copy(indent, x, kind):
    p = 'Window(Home).Property(aeon.fart.%s)'
    return ('%s<value condition="String.IsEqual(%s,%s.DBID) + String.IsEqual(%s,%s.DBType) + !String.IsEmpty(%s)">$INFO[%s]</value>\n'
            % (indent, p % 'dbid', x, p % 'type', x, p % kind, p % kind))


def patch(text):
    out, n, i = [], 0, 0
    for m in LINE.finditer(text):
        out.append(text[i:m.end()])
        i = m.end()
        line = copy(m.group(1), m.group(2), m.group(3))
        if not text.startswith(line, m.end()):
            out.append(line)
            n += 1
    out.append(text[i:])
    return ''.join(out), n


def main():
    total = 0
    for name in sorted(os.listdir(D)):
        if not name.endswith('.xml') or name == 'Font.xml':
            continue
        p = os.path.join(D, name)
        t = io.open(p, encoding='utf-8').read()
        new, n = patch(t)
        if n:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(new)
            ET.parse(p)
            print(name, n)
            total += n
    print('added', total)


if __name__ == '__main__':
    main()
