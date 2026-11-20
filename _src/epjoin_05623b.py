# -*- coding: utf-8 -*-
"""0.56.23 Episodes in one file as one row, part 2: the episode numbers that views compose inside variables
(<value> texts: "S6 E1", "Season 6 | Episode 1", the Fused Glass panels) and labels the first pass missed (a prefix
holding $LOCALIZE[n]) go through the same range variables as epjoin_05623.py, so a joined row shows "S6 E1-2" /
"Episodes 1-2". Not the episode-code variables (they show aeon.ep.code first) nor the range variables themselves.
Safe to run again: what is done holds no bare episode number any more."""
import hashlib
import io
import os
import re
import xml.etree.ElementTree as ET

MARK = '0.56.23 epjoin_b'
D = '1080i'
SUB = os.path.join(D, 'Includes_Aeon_Sub.xml')
SKIP = {'Includes_FusedPlayer.xml', 'MyPVRGuide.xml', 'Includes_Misc.xml', 'SkinSettings.xml', 'DialogPVRInfo.xml',
        'DialogPVRChannelGuide.xml'}
ARG = r'((?:[^,\[\]]|\$LOCALIZE\[\d+\])*)'          # a prefix / postfix may hold $LOCALIZE[n]
EP = re.compile(r'\$INFO\[((?:Container\(\d+\)\.)?ListItem)\.Episode(?:,' + ARG + ',' + ARG + r')?\]')
WORD = re.compile(r'\$LOCALIZE\[20359\] \$INFO\[((?:Container\(\d+\)\.)?ListItem)\.Episode\]')
made = {}


def var_for(prefix, pre, post, word):
    key = '%s|%s|%s|%s' % (prefix, pre, post, word)
    name = 'Aeon_EpN_' + hashlib.md5(key.encode('utf-8')).hexdigest()[:8]
    if name not in made:
        rng = '$INFO[%s.Property(aeon.ep.range)]' % prefix
        if word:
            plain, many = '$LOCALIZE[20359] $INFO[%s.Episode]' % prefix, '$LOCALIZE[20360] ' + rng
        elif pre is None:
            plain, many = '$INFO[%s.Episode]' % prefix, rng
        else:
            plain = '$INFO[%s.Episode,%s,%s]' % (prefix, pre, post)
            many = pre.replace('$LOCALIZE[20359]', '$LOCALIZE[20360]') + rng + post
        made[name] = ('\t<variable name="%s">\n\t\t<value condition="!String.IsEmpty(%s.Property(aeon.ep.range))">%s</value>\n'
                      '\t\t<value>%s</value>\n\t</variable>' % (name, prefix, many, plain))
    return '$VAR[%s]' % name


def fix(text):
    if 'ChannelName' in text or 'aeon.ep.range' in text:
        return text
    text = WORD.sub(lambda m: var_for(m.group(1), None, None, True), text)
    return EP.sub(lambda m: var_for(m.group(1), m.group(2), m.group(3), False), text)


def main():
    count = 0
    for name in sorted(os.listdir(D)):
        if not name.endswith('.xml') or name in SKIP:
            continue
        p = os.path.join(D, name)
        t = io.open(p, encoding='utf-8').read()
        if 'ListItem.Episode' not in t:
            continue
        before = t
        t = re.sub(r'(<label2?>)(.*?)(</label2?>)', lambda m: m.group(1) + fix(m.group(2)) + m.group(3), t)
        out, pos = [], 0
        for m in re.finditer(r'<variable name="([^"]+)">(.*?)</variable>', t, re.S):
            if m.group(1).startswith(('Aeon_EpCode', 'Aeon_EpN_')):
                continue
            body = re.sub(r'(<value(?: condition="[^"]*")?>)(.*?)(</value>)', lambda v: v.group(1) + fix(v.group(2)) + v.group(3), m.group(2))
            if body != m.group(2):
                count += 1
                out.append(t[pos:m.start(2)] + body)
                pos = m.end(2)
        if out:
            t = ''.join(out) + t[pos:]
        if t != before:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
            ET.parse(p)
    sub = io.open(SUB, encoding='utf-8').read()
    have = set(re.findall(r'<variable name="(Aeon_EpN_\w+)">', sub))
    new = [made[k] for k in sorted(made) if k not in have]
    tag = '\t<!-- %s: the numbers inside variables and labels -->\n' % MARK
    if tag not in sub:
        old_tag = '\t<!-- %s: the numbers inside variables -->\n' % MARK
        if old_tag in sub:
            sub = sub.replace(old_tag, tag)
        else:
            anchor = "\t<!-- 0.56.23 epjoin: an episode number that may be a joined row's range (helper ?info=episodes) -->\n"
            assert sub.count(anchor) == 1
            sub = sub.replace(anchor, anchor + tag)
    sub = sub.replace(tag, tag + ''.join(v + '\n' for v in new))
    io.open(SUB, 'w', encoding='utf-8', newline='\n').write(sub)
    ET.parse(SUB)
    print('variables changed', count, 'range variables added', len(new))


if __name__ == '__main__':
    main()
