"""0.56.52 Ratings shown in / Media info shown in (places_05652.py): every ratings control and every media info chip
gets the switch of its place, $EXP[Aeon_Rate_<place>] / $EXP[Aeon_Chip_<place>], as an extra <visible> (a control's
<visible> tags are ANDed, like a window's). The user, 2026-11-19: "a modal to choose where to use them: library,
information pages, widgets, spotlights etc."

What counts (leaf controls only: image / label / textbox / fadelabel, and buttons without an id or onclick = display
pills): a label by its text (variables by their values; a variable named like a chip - Res / Hdr / Aud / Asp / Chip ...
- also by its conditions), an image by its texture, or by its <visible> when it is a pill / outline / rating icon.
A separator label (· • |) that shows only with the ratings / chips goes with them. Titles, plots and meta lines are never touched (their text is not ratings or chips).

Places, by include: FG library views (FG_V5xx_View, Aeon_V538_View) and the Aeon / Aeon Glass views (Includes_Aeon_Views2/3,
Includes_Aeon_Video, Includes_Views_Video) = lib; Includes_VideoInfo = info; Aeon_Sp_Item (Widget & Spotlight screens)
= widgets; Aeon_Home (Home spotlights + the strip panels) = spot; the player's information screens and Aeon_InfoRating /
Aeon_InfoChip calls = player (not the OSD's audio / subtitle buttons, not process info); the screensaver's Ultra HD tag
= ss; the Live TV information line's rating = pvr (a variable that is empty when off).
Aeon_RatingIcons (library + information page) takes a place param (default lib; the information page passes info).

RUN AFTER the generators that write those files (fg_lib*.py, fg_epcomb.py, wx_screensaver.py, fg_ss.py, ms_menus.py ...):
they write the controls again without the switch. Repeatable (a control that has the switch is left alone).
Run from the skin folder."""
import io
import os
import re
import sys
import glob
from collections import Counter

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
RATE = re.compile(r'ListItem\.Rating|\.Rating\(|VideoPlayer\.Rating|aeon\.r\.|aeon\.rating\.|"rating/|>rating/|ratings/|'
                  r'Aeon_RH_|Aeon_VORat|aeon\.sp\.rating')
CHIP = re.compile(r'Aeon_TxMedia|VideoResolution|AudioCodec|AudioChannels|VideoAspect|HdrType|aeon\.mi\.|aeon\.chip\.|'
                  r'aeon\.hide\.(res|hdr|audio|aspect|channels|dvp|source)|OSD_Flag|Aeon_VOMedia|aeon\.sp\.mediainfo|VideoCodec|aeon\.dvp')
NAMECHIP = re.compile(r'Res(?![a-z])|Hdr|HDR|Aud|Audio|Ch(?![a-z])|Chan|Asp|Chip|Codec|Media|Flag|3D|Dvp|DV')
PILL = re.compile(r'fg/e\d|Aeon_TexOutline|FG_ChipTex|pill|outline|chip|flags/|ratings?/|rounded', re.I)
ART = re.compile(r'ListItem\.(Art|Icon|Thumb)|Player\.Art|fanart', re.I)
LEAF = re.compile(r'<control type="(image|label|textbox|fadelabel|button)"[^>]*>(?:(?!<control).)*?</control>', re.S)

# file -> list of (include-name regex, place, ratings?, chips?); '-' = outside any include
FILES = {
    'Includes_Fused.xml': [(r'FG_V5\d\d_View$|Aeon_V538_View$', 'lib')],
    'Includes_Aeon_Views2.xml': [(r'.', 'lib')],
    'Includes_Aeon_Views3.xml': [(r'.', 'lib')],
    'Includes_Aeon_Video.xml': [(r'.', 'lib')],
    'Includes_Views_Video.xml': [(r'^(?!VidView_EpisodeRow$)', 'lib')],
    'Includes_VideoInfo.xml': [(r'.', 'info')],
    'Includes_Aeon_Sub.xml': [(r'^Aeon_Sp_Item$', 'widgets'), (r'^Aeon_RatingIcons$', '$PARAM[place]')],
    'Includes_Aeon_Home.xml': [(r'^Aeon_Home$', 'spot')],
    'Includes_FusedPlayer.xml': [(r'^(FG_FullInfo|FullInfo_Classic|FG_OSD2)$', 'player')],
    'Includes_Aeon_OSD.xml': [(r'^Aeon_InfoRating$', 'player')],
}
VARS = {}
_memo = {}


def load_vars():
    for f in glob.glob(os.path.join(D, '*.xml')):
        t = io.open(f, encoding='utf-8').read()
        for m in re.finditer(r'<variable name="([^"]+)">(.*?)</variable>', t, re.S):
            VARS[m.group(1)] = m.group(2)


def var_kind(name, depth=0):
    if name in _memo:
        return _memo[name]
    _memo[name] = set()
    body = VARS.get(name, '')
    vals = ''.join(re.findall(r'<value[^>]*>(.*?)</value>', body, re.S))
    k = set()
    if RATE.search(vals):
        k.add('R')
    if CHIP.search(vals) or (NAMECHIP.search(name) and CHIP.search(body)):
        k.add('C')
    if depth < 6:
        for v in re.findall(r'\$VAR\[([^\]]+)\]', vals):
            k |= var_kind(v, depth + 1)
    _memo[name] = k
    return k


def text_kind(x):
    k = set()
    if RATE.search(x):
        k.add('R')
    if CHIP.search(x):
        k.add('C')
    for v in re.findall(r'\$VAR\[([^\]]+)\]', x):
        k |= var_kind(v)
    return k


def classify(x):
    typ = re.match(r'<control type="(\w+)"', x).group(1)
    if typ == 'image':
        tex = ' '.join(re.findall(r'<texture[^>]*>(.*?)</texture>', x))
        k = text_kind(tex)
        if k:
            return k
        if ART.search(tex) or not PILL.search(x):
            return set()
        return text_kind(' '.join(re.findall(r'<visible>(.*?)</visible>', x)))
    if typ == 'button' and ('<onclick' in x or re.match(r'<control type="button"[^>]* id=', x)):
        return set()
    lab = ' '.join(re.findall(r'<label>(.*?)</label>', x))
    if lab.strip() and len(lab.strip()) <= 3 and not re.search(r'\w', lab):
        # a separator (· • |) shown only with the ratings / chips: hidden with them
        vis = ' '.join(re.findall(r'<visible>(.*?)</visible>', x))
        return text_kind(vis.replace('HasRating', 'ListItem.Rating'))
    return text_kind(lab)


def gate(x, cond):
    if cond in x:
        return x
    return x[:x.rindex('</control>')] + '<visible>%s</visible>' % cond + '</control>'


def place_of(name, rules):
    for rx, place in rules:
        if re.search(rx, name):
            return place
    return None


def run_file(f, rules, stats):
    p = os.path.join(D, f)
    t = io.open(p, encoding='utf-8').read()
    incs = [(m.start(), m.group(1)) for m in re.finditer(r'<include name="([^"]+)"', t)]
    out, last = [], 0
    for m in LEAF.finditer(t):
        x = m.group(0)
        k = classify(x)
        if not k:
            continue
        before = [n for pos, n in incs if pos < m.start()]
        place = place_of(before[-1] if before else '-', rules)
        if not place:
            continue
        y = x
        if 'R' in k:
            y = gate(y, '$EXP[Aeon_Rate_%s]' % place)
        if 'C' in k:
            y = gate(y, '$EXP[Aeon_Chip_%s]' % place)
        if y != x:
            stats[(f, place, ''.join(sorted(k)))] += 1
            out.append(t[last:m.start()])
            out.append(y)
            last = m.end()
    out.append(t[last:])
    t = ''.join(out)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)


def specials(stats):
    # Aeon_RatingIcons: a place param, lib unless the caller says; the information page passes info
    p = os.path.join(D, 'Includes_Aeon_Sub.xml')
    t = io.open(p, encoding='utf-8').read()
    head = '\t<include name="Aeon_RatingIcons">\n\t\t<param name="li">ListItem</param>\n'
    if head in t and '<param name="place">' not in t[t.index(head):t.index(head) + 400]:
        t = t.replace(head, head + '\t\t<param name="place">lib</param>\n', 1)
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    p = os.path.join(D, 'Includes_VideoInfo.xml')
    t = io.open(p, encoding='utf-8').read()
    old = '<include content="Aeon_RatingIcons"><param name="h" value="30"/>'
    if old in t:
        t = t.replace(old, '<include content="Aeon_RatingIcons"><param name="place" value="info"/><param name="h" value="30"/>')
        stats[('Includes_VideoInfo.xml', 'info', 'RatingIcons call')] += 1
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    # Aeon_InfoChip calls (player): the chip ones get the switch in their visible param (language flags do not)
    p = os.path.join(D, 'Includes_FusedPlayer.xml')
    t = io.open(p, encoding='utf-8').read()

    def chip_call(m):
        x = m.group(0)
        lab = re.search(r'<param name="label"(?: value="([^"]*)"\s*/>|>(.*?)</param>)', x, re.S)
        if not lab or 'C' not in text_kind(lab.group(1) or lab.group(2) or '') or 'Aeon_Chip_player' in x:
            return x
        stats[('Includes_FusedPlayer.xml', 'player', 'InfoChip call')] += 1
        v = re.search(r'<param name="visible"(?: value="([^"]*)"\s*/>|>(.*?)</param>)', x, re.S)
        if v:
            cond = v.group(1) if v.group(1) is not None else v.group(2)
            new = '<param name="visible" value="[%s] + $EXP[Aeon_Chip_player]"/>' % cond.replace('"', '&quot;')
            return x[:v.start()] + new + x[v.end():]
        i = x.index('>') + 1
        return x[:i] + '<param name="visible" value="$EXP[Aeon_Chip_player]"/>' + x[i:]
    t = re.sub(r'<include content="Aeon_InfoChip">.*?</include>', chip_call, t, flags=re.S)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    # screensaver: the Ultra HD tag (label 31001 and its outline)
    p = os.path.join(D, 'Custom_1156_Screensaver.xml')
    t = io.open(p, encoding='utf-8').read()

    def ss(m):
        x = m.group(0)
        if ('$LOCALIZE[31001]' in x or 'Aeon_TexOutline' in x) and 'VideoResolution' in x:
            y = gate(x, '$EXP[Aeon_Chip_ss]')
            if y != x:
                stats[('Custom_1156_Screensaver.xml', 'ss', 'C')] += 1
            return y
        return x
    t = LEAF.sub(ss, t)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    # Live TV: the rating inside the information line
    p = os.path.join(D, 'DialogPVRInfo.xml')
    t = io.open(p, encoding='utf-8').read()
    old = '$INFO[ListItem.Rating,  ·  , / 10]'
    if old in t:
        t = t.replace(old, '$VAR[Aeon_PVRRating]')
        stats[('DialogPVRInfo.xml', 'pvr', 'R')] += 1
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    p = os.path.join(D, 'Includes_Settings.xml')
    t = io.open(p, encoding='utf-8').read()
    if 'name="Aeon_PVRRating"' not in t:
        i = t.index('\t<!-- 0.56.22 chips:')
        t = t[:i] + ('\t<variable name="Aeon_PVRRating">\n\t\t<value condition="$EXP[Aeon_Rate_pvr]">'
                     + old + '</value>\n\t</variable>\n') + t[i:]
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)


def main():
    load_vars()
    stats = Counter()
    for f, rules in FILES.items():
        run_file(f, rules, stats)
    specials(stats)
    for k in sorted(stats):
        print('placegate: %-30s %-8s %-18s %d' % (k + (stats[k],)))
    print('placegate: %d controls / calls' % sum(stats.values()))


if __name__ == '__main__':
    main()
