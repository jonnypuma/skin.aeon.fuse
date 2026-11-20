# -*- coding: utf-8 -*-
"""Home menu: 24 positions (was 13) and 10 custom items (was 3), with Add item in the menu editor (skin 0.54.0).

Every piece of the skin that exists once per Home menu position is cloned from position 13 to 14-24, and every piece
that exists once per custom item is cloned from custom item 3 to 4-10 (in that order, so the new custom items get
positions 14-24 too). The rules, from the largest unit to the smallest:
  - a definition named after the item (Aeon_MenuSlotLabel13, Aeon_SP2Path_custom3, Aeon_H_Spot3 ...): cloned whole;
  - a one-line <expression>: its OR terms that name the item (and no other one) are cloned in place, descending into
    [ ] groups where a term names several;
  - a line that names the item and no other one: cloned below itself;
  - a line of several tags (the panel's <onback> / <ondown> lists): the tags that name the item are cloned in place;
  - known blocks (the Home menu items, the spotlight wraplist and its page dots, the spotlight timer, the panel's
    Custom item settings button) are cloned as blocks.
Then the Skin settings > Home menu rows become a scrolling grouplist of 24 rows plus the Add item row, the type cycle
of the Home lists window (Aeon_EditNext*) is written again with all ten custom items, and the four System fallback
items of Home (one per position 10-13, which could show System twice) become one.

usage (from the skin folder):  python _src/menu24.py [outdir]
  outdir given: the changed files are written there (dry run); without it the skin's files are rewritten.
It refuses to run on files that already have aeon.menu.24."""
import os
import re
import sys

SKIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XML = os.path.join(SKIN, '1080i')

POS_OLD, POS_NEW = 13, 24
CUS_OLD, CUS_NEW = 3, 10
NEW_POS = range(POS_OLD + 1, POS_NEW + 1)
NEW_CUS = range(CUS_OLD + 1, CUS_NEW + 1)
CUS_LIST = {1: 9411, 2: 9412, 3: 9413, 4: 9415, 5: 9416, 6: 9417, 7: 9418, 8: 9419, 9: 9420, 10: 9424}
CUS_BTN = {1: 9668, 2: 9669, 3: 9670, 4: 9680, 5: 9681, 6: 9682, 7: 9683, 8: 9684, 9: 9685, 10: 9686}
ROW_ID = {n: 9589 + n for n in range(1, 11)}
ROW_ID.update({11: 9613, 12: 9614, 13: 9615})
ROW_ID.update(zip(NEW_POS, [9627, 9628, 9629, 9631, 9632, 9633, 9634, 9635, 9636, 9637, 9638]))
ADD_ROW, ROW_LIST, ROW_BAR = 9639, 9641, 9642
CYCLE = ['movies', 'tv', 'livetv', 'music', 'search', 'system', 'power', 'favourites', 'pictures', 'addons', 'weather',
         'files'] + ['custom%d' % k for k in range(1, CUS_NEW + 1)] + ['off']
ADD_LABEL = '$ADDON[skin.aeon.fuse 32591]'
SEP = '<control type="image"><left>41</left><top>53</top><width>1019</width><height>1</height><texture colordiffuse="30ffffff">common/white.png</texture><visible>[!$EXP[Aeon_Fused]] + !$EXP[Aeon_FGlass] + !$EXP[Aeon_MS]</visible></control>'
SLIDE = '<animation effect="slide" end="-10,0" time="0" condition="!$EXP[Aeon_FGlass]">Conditional</animation>'
ADD_HELP = '$ADDON[skin.aeon.fuse 32592]'

WARN = []


def guid(k):
    return 'guid-aeon%04d' % (11 + k)


# ---------------------------------------------------------------- tokens of one custom item / one position
CUS_SPOT = {1: 9851, 2: 9852, 3: 9853, 4: 9854, 5: 9855, 6: 9856, 7: 9857, 8: 9858, 9: 9859, 10: 9860}


def cus_rx(k, ids=None):
    """ids: a window's own control per custom item (the panel buttons of Skin settings, the path buttons of the
    spotlight editor), {k: id}"""
    parts = [r'(?<![A-Za-z0-9])custom%d(?!\d)' % k, r'aeonsp2custom%d(?!\d)' % k, r'CustomMenu\.%d\.' % k,
             r'CustomMenu%dOn\b' % k, r'CustomMenu_(?:Label|Value)%d\b' % k, r'\b%d\b' % CUS_LIST[k],
             r'Aeon_H_Spot(?:Path)?%d\b' % k, r'Aeon_EditIsCustom%d\b' % k, re.escape(guid(k)),
             r'CustomMenu_(?:OnClick|SettingsClick)"><param name="item" value="%d"' % k]
    if ids:
        parts.append(r'\b%d\b' % ids[k])
    return re.compile('|'.join(parts))


def cus_sub(s, k, ids=None):
    s = re.sub(r'(?<![A-Za-z0-9])custom3(?!\d)', 'custom%d' % k, s)
    s = re.sub(r'aeonsp2custom3(?!\d)', 'aeonsp2custom%d' % k, s)
    s = s.replace('CustomMenu.3.', 'CustomMenu.%d.' % k)
    s = re.sub(r'CustomMenu3On\b', 'CustomMenu%dOn' % k, s)
    s = re.sub(r'CustomMenu_(Label|Value)3\b', lambda m: 'CustomMenu_%s%d' % (m.group(1), k), s)
    s = re.sub(r'\b9413\b', str(CUS_LIST[k]), s)
    s = re.sub(r'Aeon_H_Spot(Path)?3\b', lambda m: 'Aeon_H_Spot%s%d' % (m.group(1) or '', k), s)
    s = re.sub(r'Aeon_EditIsCustom3\b', 'Aeon_EditIsCustom%d' % k, s)
    s = s.replace(guid(3), guid(k))
    s = re.sub(r'(CustomMenu_(?:OnClick|SettingsClick)"><param name="item" value=")3"', lambda m: '%s%d"' % (m.group(1), k), s)
    s = s.replace('$LOCALIZE[31983]', '$LOCALIZE[31909] %d' % k)       # "Menu item 3" -> "Custom item 4"
    s = s.replace('(custom 3)', '(custom %d)' % k)
    if ids:
        s = re.sub(r'\b%d\b' % ids[CUS_OLD], str(ids[k]), s)
    return s


def pos_rx(p, skinsettings=False):
    parts = [r'aeon\.menu\.(?:hide\.)?%d\b' % p, r'aeon\.editslot\),%d\)' % p,
             r'Aeon_(?:MenuSlotLabel|SlotHint|HideAct|EditNext)%d\b' % p]
    if skinsettings:
        parts.append(r'\b%d\b' % ROW_ID[p])
    return re.compile('|'.join(parts))


def pos_sub(s, p, skinsettings=False, old=POS_OLD):
    s = re.sub(r'aeon\.menu\.(hide\.)?%d\b' % old, lambda m: 'aeon.menu.%s%d' % (m.group(1) or '', p), s)
    s = re.sub(r'aeon\.editslot\),%d\)' % old, 'aeon.editslot),%d)' % p, s)
    s = re.sub(r'Aeon_(MenuSlotLabel|SlotHint|HideAct|EditNext)%d\b' % old, lambda m: 'Aeon_%s%d' % (m.group(1), p), s)
    if skinsettings:
        s = re.sub(r'\b%d\b' % ROW_ID[old], str(ROW_ID[p]), s)
    return s


class Kind:
    """what one cloning stage looks for: the item to copy, the others of its kind, and the copies to make"""
    def __init__(self, name, target, others, subs):
        self.name, self.target_rx, self.other_rxs, self.subs = name, target, others, subs

    def target(self, s):
        return bool(self.target_rx.search(s))

    def other(self, s):
        return any(rx.search(s) for rx in self.other_rxs)


def custom_kind(ids=None):
    return Kind('custom', cus_rx(CUS_OLD, ids), [cus_rx(k, ids) for k in range(1, CUS_OLD)],
                [lambda s, k=k: cus_sub(s, k, ids) for k in NEW_CUS])


def position_kind(skinsettings=False):
    return Kind('position', pos_rx(POS_OLD, skinsettings), [pos_rx(p, skinsettings) for p in range(1, POS_OLD)],
                [lambda s, p=p: pos_sub(s, p, skinsettings) for p in NEW_POS])


# ---------------------------------------------------------------- expression terms
def split_top(s):
    parts, depth, cur = [], 0, []
    for ch in s:
        if ch == '[':
            depth += 1
        elif ch == ']':
            depth -= 1
        if ch == '|' and depth == 0:
            parts.append(''.join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append(''.join(cur))
    return parts


def matching(s, i):
    depth = 0
    for j in range(i, len(s)):
        if s[j] == '[':
            depth += 1
        elif s[j] == ']':
            depth -= 1
            if depth == 0:
                return j
    raise ValueError('unbalanced [ ] in ' + s[:120])


def clone_terms(s, kind, where):
    parts = split_top(s)
    if len(parts) == 1:
        return descend(s, kind, where)
    out, changed = [], False
    for part in parts:
        core = part.strip()
        if kind.target(core) and not kind.other(core):
            out.append(core)
            out += [sub(core) for sub in kind.subs]
            changed = True
        elif kind.target(core):
            new = descend(core, kind, where)
            out.append(new)
            changed = changed or new != core
        else:
            out.append(core)
    return ' | '.join(out) if changed else s


def descend(s, kind, where):
    """look for the OR group that holds the item, inside the [ ] groups of s"""
    out, i, found = [], 0, False
    while i < len(s):
        if s[i] == '[':
            j = matching(s, i)
            inner = s[i + 1:j]
            if kind.target(inner):
                new = clone_terms(inner, kind, where)
                found = found or new != inner
                inner = new
            out.append('[' + inner + ']')
            i = j + 1
        else:
            out.append(s[i])
            i += 1
    result = ''.join(out)
    if not found and kind.target(s):
        WARN.append('%s: %s term without an OR group to clone in: %s' % (where, kind.name, s[:160]))
    return result


# ---------------------------------------------------------------- lines and definitions
DEF_RX = re.compile(r'^\s*<(variable|expression|include)\s+name="([^"]+)"')
ONE_EXPR = re.compile(r'^(\s*<expression name="[^"]+">)(.*)(</expression>\s*)$')
TAG_RX = re.compile(r'<(\w+)((?:\s+[\w:]+="[^"]*")*)\s*>([^<]*)</\1>')


def def_end(lines, i, kind):
    if kind == 'expression' and '</expression>' in lines[i]:
        return i
    if kind == 'variable':
        for j in range(i, len(lines)):
            if '</variable>' in lines[j]:
                return j
    depth = 0
    for j in range(i, len(lines)):
        depth += len(re.findall(r'<include[\s>]', lines[j])) - len(re.findall(r'<include[^>]*/>', lines[j]))
        depth -= lines[j].count('</include>')
        if depth <= 0:
            return j
    raise ValueError('no end of definition at line %d' % (i + 1))


def block_end(lines, i, tag='control'):
    depth = 0
    for j in range(i, len(lines)):
        depth += len(re.findall(r'<%s[\s>]' % tag, lines[j])) - len(re.findall(r'<%s[^>]*/>' % tag, lines[j]))
        depth -= lines[j].count('</%s>' % tag)
        if depth <= 0:
            return j
    raise ValueError('no end of <%s> at line %d' % (tag, i + 1))


def clone_line(line, kind, where):
    if not kind.target(line):
        return [line]
    m = ONE_EXPR.match(line)
    if m:
        return [m.group(1) + clone_terms(m.group(2), kind, where) + m.group(3)]
    if not kind.other(line):
        return [line] + [sub(line) for sub in kind.subs]
    tags = TAG_RX.findall(line)
    if len(tags) > 1:
        def one(mt):
            t = mt.group(0)
            if kind.target(t) and not kind.other(t):
                return t + ''.join(sub(t) for sub in kind.subs)
            if kind.target(t):
                body = mt.group(3)
                cond = re.search(r'condition="([^"]*)"', mt.group(2))
                if mt.group(1) in ('visible', 'enable') and not cond:
                    return t.replace('>%s<' % body, '>%s<' % clone_terms(body, kind, where), 1)
                if cond and not kind.target(body):
                    return t.replace(cond.group(0), 'condition="%s"' % clone_terms(cond.group(1), kind, where), 1)
                WARN.append('%s: %s tag names several: %s' % (where, kind.name, t[:160]))
            return t
        return [TAG_RX.sub(one, line)]
    # one tag whose condition attribute (or <visible> / <enable> body) ORs the items: clone the terms in it
    if len(tags) == 1:
        mt = TAG_RX.search(line)
        attrs, body = mt.group(2), mt.group(3)
        cond = re.search(r'condition="([^"]*)"', attrs)
        if cond and kind.target(cond.group(1)) and not kind.target(body):
            new = clone_terms(cond.group(1), kind, where)
            if new != cond.group(1):
                return [line.replace('condition="%s"' % cond.group(1), 'condition="%s"' % new, 1)]
        if mt.group(1) in ('visible', 'enable') and kind.target(body) and not cond:
            new = clone_terms(body, kind, where)
            if new != body:
                return [line.replace('>%s<' % body, '>%s<' % new, 1)]
    WARN.append('%s: %s line names several, left alone: %s' % (where, kind.name, line.strip()[:160]))
    return [line]


def clone_pass(lines, kind, where, skip_defs=(), protect=None, region=None):
    """the generic stage over a file. protect: set of line numbers left alone; region: (first, last) line numbers
    outside of which nothing is touched"""
    protect = protect or set()
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        inside = region is None or region[0] <= i <= region[1]
        if i in protect or not inside:
            out.append(line)
            i += 1
            continue
        m = DEF_RX.match(line)
        if m:
            end = def_end(lines, i, m.group(1))
            block = lines[i:end + 1]
            name = m.group(2)
            if any(re.fullmatch(rx, name) for rx in skip_defs):
                out += block
            elif kind.target('name="%s"' % name):
                out += block
                for sub in kind.subs:
                    out += [sub(l) for l in block]
            else:
                for n, l in enumerate(block, i):
                    out += [l] if n in protect else clone_line(l, kind, '%s %s' % (where, name))
            i = end + 1
            continue
        out += clone_line(line, kind, '%s line %d' % (where, i + 1))
        i += 1
    return out


# ---------------------------------------------------------------- files
def read(name):
    with open(os.path.join(XML, name), 'r', encoding='utf-8', newline='') as handle:
        text = handle.read()
    nl = '\r\n' if '\r\n' in text else '\n'
    return text.split(nl), nl


def includes_custommenu():
    lines, nl = read('Includes_CustomMenu.xml')
    lines = clone_pass(lines, custom_kind(), 'CustomMenu', skip_defs=[r'CustomMenuCount\d+'])
    return {'Includes_CustomMenu.xml': (lines, nl)}


def editnext_defs(indent):
    out = []
    for p in range(1, POS_NEW + 1):
        out.append('%s<variable name="Aeon_EditNext%d">' % (indent, p))
        for a, b in zip(CYCLE, CYCLE[1:] + ['movies']):
            out.append('%s\t<value condition="String.IsEqual(Skin.String(aeon.menu.%d),%s)">%s</value>' % (indent, p, a, b))
        out.append('%s\t<value>movies</value>' % indent)
        out.append('%s</variable>' % indent)
    return out


def includes_sub():
    lines, nl = read('Includes_Aeon_Sub.xml')
    skip = [r'Aeon_EditNext\d+']
    lines = clone_pass(lines, custom_kind(), 'Sub', skip_defs=skip)
    lines = clone_pass(lines, position_kind(), 'Sub', skip_defs=skip)
    # the type cycle again, all positions, all custom items
    first = next(i for i, l in enumerate(lines) if '<variable name="Aeon_EditNext1">' in l)
    out, i, placed = [], 0, False
    while i < len(lines):
        m = re.match(r'^(\s*)<variable name="Aeon_EditNext\d+">', lines[i])
        if m:
            end = def_end(lines, i, 'variable')
            if not placed:
                out += editnext_defs(m.group(1))
                placed = True
            i = end + 1
            continue
        out.append(lines[i])
        i += 1
    assert placed and first
    # the editor's row list: a row shows while it or a later position holds an item; the Add row follows the last
    exprs = ['\t<!-- Home menu editor (0.54.0): position n is used / a later one is (rows after the last item hide) -->']
    for p in range(1, POS_NEW + 1):
        exprs.append('\t<expression name="Aeon_MenuUsed%d">!String.IsEmpty(Skin.String(aeon.menu.%d)) + '
                     '!String.IsEqual(Skin.String(aeon.menu.%d),off)</expression>' % (p, p, p))
    for p in range(1, POS_NEW + 1):
        exprs.append('\t<expression name="Aeon_MenuTail%d">%s</expression>' % (
            p, ' | '.join('[$EXP[Aeon_MenuUsed%d]]' % q for q in range(p, POS_NEW + 1))))
    exprs.append('\t<expression name="Aeon_MenuFull">%s</expression>' % ' + '.join(
        '$EXP[Aeon_MenuUsed%d]' % q for q in range(1, POS_NEW + 1)))
    close = max(i for i, l in enumerate(out) if '</includes>' in l)
    out[close:close] = exprs
    return {'Includes_Aeon_Sub.xml': (out, nl)}


def includes_home():
    lines, nl = read('Includes_Aeon_Home.xml')
    if any('aeon.menu.%d)' % POS_NEW in l for l in lines):
        raise SystemExit('Includes_Aeon_Home.xml already has position %d' % POS_NEW)
    protect = set()
    # 1. the Home menu items (wraplist 9000): 24 positions x every key, one System fallback
    head = next(i for i, l in enumerate(lines) if '<include content="Aeon_H_Title"><param name="focused" value="true"/></include>' in l)
    start = next(i for i in range(head, len(lines)) if lines[i].strip() == '<content>')
    end = next(i for i in range(start, len(lines)) if lines[i].strip() == '</content>')
    items, i = [], start + 1
    while i < end:
        assert lines[i].strip() == '<item>', lines[i]
        j = next(k for k in range(i, end) if lines[k].strip() == '</item>')
        items.append(lines[i:j + 1])
        i = j + 1
    by_pos, fallback = {}, None
    for item in items:
        text = '\n'.join(item)
        key = re.search(r'<label2>(\w+)</label2>', text).group(1)
        m = re.search(r'<visible>String\.IsEqual\(Skin\.String\(aeon\.menu\.(\d+)\),', text)
        if not m:
            fallback = fallback or item
            continue
        by_pos.setdefault(int(m.group(1)), []).append((key, item))
    new_items = []
    for p in range(1, POS_OLD + 1):
        for key, item in by_pos[p]:
            new_items.append(item)
            if key == 'custom%d' % CUS_OLD:
                for k in NEW_CUS:
                    new_items.append([cus_sub(l, k) for l in item])
    template = [it for it in new_items if any('aeon.menu.%d)' % POS_OLD in l for l in it)]
    for p in NEW_POS:
        for item in template:
            new_items.append([pos_sub(l, p) for l in item])
    vis = ' + '.join('!String.IsEqual(Skin.String(aeon.menu.%d),system)' % p for p in range(1, POS_NEW + 1))
    fb = [re.sub(r'<visible>.*</visible>', '<visible>%s</visible>' % vis, l) for l in fallback]
    indent = re.match(r'\s*', fallback[0]).group(0)
    fb.insert(0, indent + '<!-- System when no position holds it (one item for all positions since 0.54.0) -->')
    new_items.append(fb)
    flat = [l for it in new_items for l in it]
    lines = lines[:start + 1] + flat + lines[end:]
    protect.update(range(start, start + 1 + len(flat) + 1))
    # 2. the spotlight wraplist of custom item 3 and its page dots
    for marker in ('<control type="wraplist" id="9413">', '<visible>$EXP[Aeon_SP2Show_custom3]</visible>'):
        s = next(i for i, l in enumerate(lines) if marker in l)
        e = block_end(lines, s)
        block = lines[s:e + 1]
        clones = [cus_sub(l, k) for k in NEW_CUS for l in block]
        lines[e + 1:e + 1] = clones
        protect = {x + len(clones) if x > e else x for x in protect}
        protect.update(range(s, e + 1 + len(clones)))
    lines = clone_pass(lines, custom_kind(), 'Home', protect=protect)
    return {'Includes_Aeon_Home.xml': (lines, nl)}


def timers():
    lines, nl = read('Timers.xml')
    s = next(i for i, l in enumerate(lines) if '<name>aeonsp2custom3</name>' in l)
    s = max(i for i in range(s) if '<timer>' in lines[i])
    e = next(i for i in range(s, len(lines)) if '</timer>' in lines[i])
    block = lines[s:e + 1]
    lines[e + 1:e + 1] = [cus_sub(l, k) for k in NEW_CUS for l in block]
    return {'Timers.xml': (lines, nl)}


def spotlight_editor():
    """Custom_1163 (Spotlight editor): the path button per custom item (9851-9853 -> 9854-9860)"""
    lines, nl = read('Custom_1163_Spotlight.xml')
    s = next(i for i, l in enumerate(lines) if '<control type="button" id="9853">' in l)
    e = block_end(lines, s)
    block = lines[s:e + 1]
    clones = [cus_sub(l, k, CUS_SPOT) for k in NEW_CUS for l in block]
    lines[e + 1:e + 1] = clones
    protect = set(range(s, e + 1 + len(clones)))
    lines = clone_pass(lines, custom_kind(CUS_SPOT), 'Custom_1163', protect=protect)
    return {'Custom_1163_Spotlight.xml': (lines, nl)}


def simple(name, kinds):
    lines, nl = read(name)
    for kind in kinds:
        lines = clone_pass(lines, kind, name)
    return {name: (lines, nl)}


# ---------------------------------------------------------------- Skin settings > Home menu
def skin_settings():
    lines, nl = read('SkinSettings.xml')
    # the category's Right goes to the row list (it focuses the row that had the focus last, else the first)
    cat = next(i for i, l in enumerate(lines) if '<param name="id" value="9558"/>' in l)
    nav = cat + 2
    assert '<param name="onright" value="9590"/>' in lines[nav], lines[nav]
    lines[nav] = lines[nav].replace('<param name="onright" value="9590"/>', '<param name="onright" value="%d"/>' % ROW_LIST)

    # --- the rows
    vis = next(i for i, l in enumerate(lines) if '<visible>String.IsEqual(Window(Home).Property(aeon.skincat),homemenu)</visible>' in l)
    first = next(i for i in range(vis, len(lines)) if lines[i].strip() == '<top>191</top>') - 1
    assert lines[first].strip() == '<control type="group">'
    last_btn = next(i for i in range(first, len(lines)) if '<control type="button" id="9615">' in lines[i])
    last_grp = max(i for i in range(first, last_btn) if lines[i].strip() == '<control type="group">')
    last = block_end(lines, last_grp)
    row1 = lines[first:block_end(lines, first) + 1]
    indent = re.match(r'\s*', row1[0]).group(0)
    new = rows_list(row1, indent)
    lines[first:last + 1] = new

    # --- the action panel: Add item focused shows what Add does instead of the item's buttons
    pstart = next(i for i, l in enumerate(lines) if '<visible>String.IsEqual(Window(Home).Property(aeon.skincat),homemenu)</visible>' in l
                  and i > first + len(new) and '<left>1536</left>' in lines[i - 1])
    assert lines[pstart - 2].strip() == '<control type="group">', lines[pstart - 2]
    pend = block_end(lines, pstart - 2)
    for i in range(pstart, pend):
        l = lines[i]
        if '<label>$LOCALIZE[31719]</label>' in l or '<label>$VAR[Aeon_EditTitle]</label>' in l:
            lines[i] = l.replace('</control>', '<visible>!Control.HasFocus(%d)</visible></control>' % ADD_ROW, 1) \
                if l.rstrip().endswith('</control>') and '<visible>' not in l else l
    buttons = next(i for i in range(pstart, pend) if lines[i].strip() == '<control type="group"><top>96</top>')
    lines[buttons] = lines[buttons].replace('<top>96</top>', '<top>96</top><visible>!Control.HasFocus(%d)</visible>' % ADD_ROW)
    pin = re.match(r'\s*', lines[pstart]).group(0)
    add_panel = [
        pin + '<!-- Add item focused (0.54.0): what it does; the item buttons hide -->',
        pin + '<control type="group">',
        pin + '\t<visible>Control.HasFocus(%d)</visible>' % ADD_ROW,
        pin + '\t<control type="label"><left>24</left><top>34</top><width>240</width><height>44</height><font>st_ui_24_bold</font>'
              '<textcolor>ffffffff</textcolor><label>%s</label></control>' % ADD_LABEL,
        pin + '\t<control type="textbox"><left>24</left><top>110</top><width>212</width><height>520</height><font>st_small_20</font>'
              '<textcolor>99ffffff</textcolor><label>%s</label></control>' % ADD_HELP,
        pin + '</control>',
    ]
    lines[buttons:buttons] = add_panel
    pend += len(add_panel)

    # --- panel: the custom item settings buttons 4-10 and the nav / back lists
    s = next(i for i in range(pstart, pend) if '<control type="button" id="9670">' in lines[i])
    s = max(i for i in range(pstart, s) if lines[i].strip().startswith('<control type="group">'))
    e = block_end(lines, s)
    block = lines[s:e + 1]
    clones = [cus_sub(l, k, CUS_BTN) for k in NEW_CUS for l in block]
    lines[e + 1:e + 1] = clones
    pend += len(clones)
    protect = set(range(s, e + 1 + len(clones)))
    region = (pstart, pend)
    lines = clone_pass(lines, custom_kind(CUS_BTN), 'SkinSettings', protect=protect, region=region)
    pend = block_end(lines, pstart - 2)
    lines = clone_pass(lines, position_kind(True), 'SkinSettings', region=(pstart, pend))
    return {'SkinSettings.xml': (lines, nl)}


def rows_list(row1, indent):
    """24 rows and the Add row in a grouplist that scrolls (it scrolls to a button inside a row group). The row
    groups have no id: a group with its button's id is what Kodi takes as the focused control, and a group drops Up /
    Down (tested on the box)."""
    shift = 160
    body = row1[1:-1]                                 # without the group's own open / close lines
    body = [l for l in body if l.strip() != '<top>191</top>']

    def row(p):
        rid = ROW_ID[p]
        out = [indent + '\t<control type="group">',
               indent + '\t\t<width>1100</width><height>54</height>',
               indent + '\t\t<visible>$EXP[Aeon_MenuTail%d]</visible>' % p]
        nxt = ROW_ID.get(p + 1)
        for l in body:
            l = re.sub(r'<left>(-?\d+)</left>', lambda m: '<left>%d</left>' % (int(m.group(1)) + shift), l)
            l = re.sub(r'\b9590\b', str(rid), l)
            l = l.replace('aeon.editslot,1,home', 'aeon.editslot,%d,home' % p)
            l = l.replace('1    $VAR[Aeon_MenuSlotLabel1]', '%d    $VAR[Aeon_MenuSlotLabel%d]' % (p, p))
            l = l.replace('$VAR[Aeon_SlotHint1]', '$VAR[Aeon_SlotHint%d]' % p)
            if l.strip() == '<onup>9615</onup>':
                l = re.sub(r'<onup>.*', '<onup>%d</onup>' % ADD_ROW if p == 1 else '<onup>%d</onup>' % ROW_ID[p - 1], l)
            elif l.strip() == '<ondown>9591</ondown>':
                pre = re.match(r'\s*', l).group(0)
                if nxt:
                    l = pre + '<ondown condition="$EXP[Aeon_MenuTail%d]">%d</ondown><ondown>%d</ondown>' % (p + 1, nxt, ADD_ROW)
                else:
                    l = pre + '<ondown>%d</ondown>' % ADD_ROW
            out.append('\t' + l)
        out.append(indent + '\t</control>')
        return out

    up = ''.join('<onup condition="$EXP[Aeon_MenuUsed%d]">%d</onup>' % (p, ROW_ID[p]) for p in range(POS_NEW, 0, -1))
    ink_dim = '[$EXP[Aeon_MenuFull]]'
    add = [
        indent + '\t<!-- Add item (0.54.0): the next free position at the end of the menu, through the type picker -->',
        indent + '\t<control type="group">',
        indent + '\t\t<width>1100</width><height>54</height>',
        indent + '\t\t%s' % SEP,
        indent + '\t\t<control type="image"><left>1</left><top>-34</top><width>1099</width><height>134</height><texture border="56" colordiffuse="$VAR[FG_ShadowCol]">fg/sh16.png</texture>'
                 '<visible>[Control.HasFocus(%d)] + $EXP[Aeon_FGlass] + $EXP[FG_FocusShadowOn]</visible><include>FG_LandShadowVisible</include></control>' % ADD_ROW,
        indent + '\t\t<control type="image"><left>41</left><top>0</top><width>1019</width><height>54</height><texture border="20" colordiffuse="$VAR[Aeon_MenuFocusColR]">$VAR[Aeon_MenuFocusTex]</texture>'
                 '<visible>Control.HasFocus(%d)</visible><animation effect="zoom" start="100,100" end="102.355,100.000" center="auto" time="0" condition="$EXP[Aeon_FGlass] + $EXP[FG_FocusFlat]">Conditional</animation></control>' % ADD_ROW,
        indent + '\t\t<control type="button" id="%d">' % ADD_ROW,
        indent + '\t\t\t<left>41</left><top>0</top><width>1019</width><height>54</height>',
        indent + '\t\t\t<label></label><texturefocus /><texturenofocus />',
        indent + '\t\t\t%s<onup>noop</onup>' % up,
        indent + '\t\t\t<ondown condition="$EXP[Aeon_MenuTail1]">%d</ondown><ondown>noop</ondown>' % ROW_ID[1],
        indent + '\t\t\t<onback>9558</onback><onleft>SetFocus(9558)</onleft><onright>noop</onright>',
        indent + '\t\t\t<onfocus>SetProperty(aeon.editrow,%d,home)</onfocus>' % ADD_ROW,
        indent + '\t\t\t<onclick>RunScript(special://home/addons/script.aeon.helper/swap.py,add)</onclick>',
        indent + '\t\t</control>',
        indent + '\t\t<control type="image"><left>163</left><top>3</top><width>48</width><height>48</height><texture colordiffuse="99ffffff">icons/af3/plus.png</texture>'
                 '<visible>!Control.HasFocus(%d) + !%s</visible></control>' % (ADD_ROW, ink_dim),
        indent + '\t\t<control type="image"><left>163</left><top>3</top><width>48</width><height>48</height><texture colordiffuse="44ffffff">icons/af3/plus.png</texture>'
                 '<visible>!Control.HasFocus(%d) + %s</visible></control>' % (ADD_ROW, ink_dim),
        indent + '\t\t<control type="image"><left>163</left><top>3</top><width>48</width><height>48</height><texture colordiffuse="$VAR[Aeon_OnBarInk]">icons/af3/plus.png</texture>'
                 '<visible>Control.HasFocus(%d)</visible></control>' % ADD_ROW,
        indent + '\t\t<control type="label"><left>210</left><top>0</top><width>400</width><height>54</height><aligny>center</aligny><font>st_ui_24_semibold</font>'
                 '<textcolor>99ffffff</textcolor><label>%s</label><visible>!Control.HasFocus(%d) + !%s</visible></control>' % (ADD_LABEL, ADD_ROW, ink_dim),
        indent + '\t\t<control type="label"><left>210</left><top>0</top><width>400</width><height>54</height><aligny>center</aligny><font>st_ui_24_semibold</font>'
                 '<textcolor>44ffffff</textcolor><label>%s</label><visible>!Control.HasFocus(%d) + %s</visible></control>' % (ADD_LABEL, ADD_ROW, ink_dim),
        indent + '\t\t<control type="label"><left>210</left><top>0</top><width>400</width><height>54</height><aligny>center</aligny><font>st_ui_24_bold</font>'
                 '<textcolor>$VAR[Aeon_OnBarInk]</textcolor><label>%s</label><visible>Control.HasFocus(%d)</visible></control>' % (ADD_LABEL, ADD_ROW),
        indent + '\t\t<control type="label"><left>560</left><top>0</top><width>440</width><height>54</height><align>right</align><aligny>center</aligny><font>st_small_20_semibold</font>'
                 '<textcolor>ccffffff</textcolor><label>$INFO[Window(Home).Property(aeon.menucount),, / %d]</label><visible>!Control.HasFocus(%d)</visible></control>' % (POS_NEW, ADD_ROW),
        indent + '\t\t<control type="label"><left>560</left><top>0</top><width>440</width><height>54</height><align>right</align><aligny>center</aligny><font>st_small_20_semibold</font>'
                 '<textcolor>$VAR[Aeon_OnBarInk]</textcolor><label>$INFO[Window(Home).Property(aeon.menucount),, / %d]</label><visible>Control.HasFocus(%d)</visible></control>' % (POS_NEW, ADD_ROW),
        indent + '\t</control>',
    ]
    out = [indent + '<!-- Home menu rows (0.54.0): 24 positions in a list that scrolls; rows after the last item hide, Add item follows -->',
           indent + '<control type="grouplist" id="%d">' % ROW_LIST,
           indent + '\t<left>-160</left><top>191</top><width>1100</width><height>%d</height>' % (13 * 54),
           indent + '\t<orientation>vertical</orientation><itemgap>0</itemgap><usecontrolcoords>true</usecontrolcoords>',
           indent + '\t<scrolltime tween="cubic" easing="out">200</scrolltime><pagecontrol>%d</pagecontrol>' % ROW_BAR]
    for p in range(1, POS_NEW + 1):
        out += row(p)
    out += add
    out.append(indent + '</control>')
    out += [indent + '<control type="scrollbar" id="%d">' % ROW_BAR,
            indent + '\t<left>904</left><top>197</top><width>4</width><height>%d</height>' % (13 * 54 - 12),
            indent + '\t<texturesliderbackground border="2" colordiffuse="22ffffff">aeon/track_8.png</texturesliderbackground>',
            indent + '\t<texturesliderbar border="2" colordiffuse="99ffffff">aeon/track_8.png</texturesliderbar>',
            indent + '\t<texturesliderbarfocus border="2" colordiffuse="99ffffff">aeon/track_8.png</texturesliderbarfocus>',
            indent + '\t<textureslidernib /><textureslidernibfocus />',
            indent + '\t<orientation>vertical</orientation><showonepage>false</showonepage>',
            indent + '\t%s' % SLIDE,      # Aeon / Glass: the rows meet the box edge, the bar goes inside it
            indent + '</control>']
    return out


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else None
    files = {}
    files.update(includes_home())
    files.update(includes_sub())
    files.update(includes_custommenu())
    files.update(timers())
    files.update(spotlight_editor())
    files.update(simple('Includes_Aeon_Wizard.xml', [position_kind()]))
    files.update(simple('Home.xml', [position_kind()]))
    files.update(simple('Custom_1158_HomeLists.xml', [position_kind()]))
    files.update(simple('Custom_1159_HomeSubmenu.xml', [position_kind()]))
    files.update(skin_settings())
    for name, (lines, nl) in files.items():
        path = os.path.join(outdir or XML, name)
        with open(path, 'w', encoding='utf-8', newline='') as handle:
            handle.write(nl.join(lines))
        print('%-32s %6d lines' % (name, len(lines)))
    for w in WARN:
        print('WARN', w)


if __name__ == '__main__':
    main()
