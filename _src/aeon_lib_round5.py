# -*- coding: utf-8 -*-
"""0.56.18 the user's notes on the version / set panes (2026-11-16): "the arrow up/down pointers need to be made
smaller, especially the frosted background for them. However, changing version does not change the mediainfo,
duration etc".

- In a library window ListItem.* is always the main list's item (CGUIMediaWindow::GetCurrentListItem), also while the
  version / set pane has the focus. The panes' bands (Aeon_V_Bar5101 / 5104 / 5221 / 5224 / 5241 / 5244), the title,
  credits and plot over them (Banner list, Compact list) and the List view's head pane read ListItem.* through the
  0.56.15 / 0.56.16 text variables, so they kept the main film's media info and run time. Every variable / expression
  they reach that reads a bare ListItem.* gets a copy per pane with Container(<pane>).ListItem.* (name_<pane>), and those
  places use the copies. The List view's head pane splits into one per pane (5101, 5104).
- The up / down pointers in the panes: pill 64 x 40 -> 36 x 24 (the light / dark pill under the chevron), chevron
  28 -> 18, centres kept; the List pane takes the Compact list's style too (light pill, dark chevron, 44 x 28 / 20).
- Compact list pane (186 x 280 since 0.56.17): the title, version name, play ring, counter and pointers no longer sit
  on each other; the year / run time line goes (the title line under the art has it, now for the version).
Run from the skin folder after aeon_lib_round4.py; each file once."""
import io
import os
import re
import xml.etree.ElementTree as ET

V2 = os.path.join('1080i', 'Includes_Aeon_Views2.xml')
VID = os.path.join('1080i', 'Includes_Aeon_Video.xml')
MARK = '0.56.18 aeon_lib_round5'
BARE = re.compile(r'(?<![\w).])ListItem\.')        # not Container(n).ListItem.
REF = re.compile(r'\$(VAR|EXP|ESCVAR)\[([A-Za-z0-9_]+)\]')


def swap(text, old, new, count=1):
    n = text.count(old)
    assert n == count, (old[:100], n, count)
    return text.replace(old, new)


def definitions():
    """every <variable> / <expression> of the skin: name -> (kind, element text)"""
    out = {}
    folder = '1080i'
    for fn in sorted(os.listdir(folder)):
        if not fn.endswith('.xml') or fn == 'Font.xml':
            continue
        text = io.open(os.path.join(folder, fn), encoding='utf-8').read()
        for kind in ('variable', 'expression'):
            for m in re.finditer(r'<%s\s+name="([^"]+)"[^>]*>.*?</%s>' % (kind, kind), text, re.S):
                out.setdefault(m.group(1), (kind, m.group(0)))
    return out


def needs(name, defs, memo, stack=()):
    """does this variable / expression read a bare ListItem.*, itself or through what it uses"""
    if name in memo:
        return memo[name]
    if name not in defs or name in stack:
        return False
    body = defs[name][1]
    hit = bool(BARE.search(body)) or any(needs(r, defs, memo, stack + (name,)) for _, r in REF.findall(body))
    memo[name] = hit
    return hit


def closure(text, defs, memo):
    names, todo = set(), [r for _, r in REF.findall(text)]
    while todo:
        n = todo.pop()
        if n in names or not needs(n, defs, memo):
            continue
        names.add(n)
        todo.extend(r for _, r in REF.findall(defs[n][1]))
    return names


def clone_text(text, pane, names):
    text = BARE.sub('Container(%d).ListItem.' % pane, text)
    return REF.sub(lambda m: '$%s[%s_%d]' % (m.group(1), m.group(2), pane) if m.group(2) in names else m.group(0), text)


def element_at(text, start):
    """the <control ...> ... </control> that starts at `start`"""
    depth, i = 0, start
    pat = re.compile(r'<control\b|</control>')
    for m in pat.finditer(text, start):
        depth += 1 if m.group(0) != '</control>' else -1
        if depth == 0:
            return start, m.end()
    raise AssertionError('unclosed control')


def include_body(text, name):
    a = text.index('<include name="%s">' % name)
    b = text.index('\n\t</include>', a)
    return a, b


def shrink_pointers(s):
    """pills 64 x 40 -> 36 x 24, chevrons 28 -> 18, centres kept"""
    def pill(m):
        return '<left>%d</left><top>%d</top><width>36</width><height>24</height><texture border="12,0,12,0"' % (int(m.group(1)) + 14, int(m.group(2)) + 8)
    s, n1 = re.subn(r'<left>(\d+)</left><top>(\d+)</top><width>64</width><height>40</height><texture border="20,0,20,0"', pill, s)

    def chev(m):
        return '<left>%d</left><top>%d</top><width>18</width><height>18</height><aspectratio>keep</aspectratio><texture%s' % (int(m.group(1)) + 5, int(m.group(2)) + 5, m.group(3))
    s, n2 = re.subn(r'<left>(\d+)</left><top>(\d+)</top><width>28</width><height>28</height><aspectratio>keep</aspectratio><texture([^>]*>aeon/icons/chevron_down\.png)', chev, s)
    return s, n1, n2


def list_pointers(s):
    """List (510) pane: the Compact list's pointer style (light pill, dark chevron), 44 x 28 / 20 (was 64 x 40 / 28 with
    a line pill and an accent chevron), centres kept"""
    n1 = n2 = 0
    for top in (34, 1004):
        for colour, tex in (('66000000', '$VAR[Aeon_TexPill40]'), ('ccffffff', 'aeon/pill_44_line.png')):
            old = '<left>331</left><top>%d</top><width>64</width><height>40</height><texture border="20,0,20,0" colordiffuse="%s">%s</texture>' % (top, colour, tex)
            assert s.count(old) == 1, old
            s = s.replace(old, '<left>341</left><top>%d</top><width>44</width><height>28</height><texture border="14,0,14,0" colordiffuse="%s">$VAR[Aeon_TexPill40]</texture>' % (top + 6, colour))
            n1 += 1
        old = '<left>349</left><top>%d</top><width>28</width><height>28</height><aspectratio>keep</aspectratio><texture colordiffuse="$VAR[Aeon_Accent_L]">aeon/icons/chevron_down.png' % (top + 6)
        assert s.count(old) == 1, old
        s = s.replace(old, '<left>353</left><top>%d</top><width>20</width><height>20</height><aspectratio>keep</aspectratio><texture colordiffuse="lib_aeon_onbar">aeon/icons/chevron_down.png' % (top + 10))
        n2 += 1
    return s, n1, n2


def run():
    defs = definitions()
    memo = {}
    v2 = io.open(V2, encoding='utf-8').read()
    vid = io.open(VID, encoding='utf-8').read()
    if MARK in v2:
        print('already')
        return
    clones = {}                                   # pane -> names to copy

    # ---- the bands of the panes (all in Views2)
    for pane in (5101, 5104, 5221, 5224, 5241, 5244):
        a, b = include_body(v2, 'Aeon_V_Bar%d' % pane)
        body = v2[a:b]
        names = closure(body, defs, memo)
        clones.setdefault(pane, set()).update(names)
        v2 = v2[:a] + clone_text(body, pane, names) + v2[b:]
    # ---- title / credits / plot over the bands while a pane has the focus (Banner list 522, Compact list 524)
    for pane in (5221, 5224, 5241, 5244):
        start = v2.index('<control type="group"><visible>Control.HasFocus(%d)</visible>' % pane)
        a, b = element_at(v2, start)
        body = v2[a:b]
        names = closure(body, defs, memo)
        clones[pane].update(names)
        v2 = v2[:a] + clone_text(body, pane, names) + v2[b:]
    # ---- List (510): the head pane over the rows, one per pane
    marker = '<!-- 0.56.16 aeon_lib_round3: the same for the version / set film in focus -->'
    i = vid.index(marker)
    a, b = element_at(vid, vid.index('<control type="group">', i))
    group = vid[a:b]
    old_vis = '<visible>!$EXP[Aeon_FGlass] + [Control.HasFocus(5101) | Control.HasFocus(5104)]</visible>'
    assert old_vis in group
    parts = []
    for pane in (5101, 5104):
        g = group.replace(old_vis, '<visible>!$EXP[Aeon_FGlass] + Control.HasFocus(%d)</visible>' % pane)
        names = closure(g, defs, memo)
        clones.setdefault(pane, set()).update(names)
        parts.append(clone_text(g, pane, names))
    vid = vid[:a] + ('\n\t\t\t<!-- %s: one per pane, reading that pane\'s item (ListItem.* is the main list\'s) -->\n\t\t\t' % MARK).join([''] + parts).lstrip('\n\t') + vid[b:]

    # ---- the copies, after the definitions (Views2)
    out = ['\t<!-- %s: the variables / expressions the version / set panes read, per pane with Container(<pane>).ListItem.*\n'
           '\t     (in a library window ListItem.* is the main list\'s item even while a pane has the focus) -->' % MARK]
    for pane in sorted(clones):
        for name in sorted(clones[pane]):
            kind, element = defs[name]
            element = element.replace('name="%s"' % name, 'name="%s_%d"' % (name, pane), 1)
            out.append('\t' + clone_text(element, pane, clones[pane]))
    v2 = v2.replace('</includes>', '\n'.join(out) + '\n</includes>', 1) if v2.count('</includes>') == 1 else None
    assert v2 is not None

    # ---- smaller pointers (List pane in Video, Banner / Compact list panes in Views2)
    vid, a1, b1 = list_pointers(vid)
    a2 = b2 = 0
    for view in ('Aeon_V522_ViewAeon', 'Aeon_V524_ViewAeon'):
        a, b = include_body(v2, view)
        s, n1, n2 = shrink_pointers(v2[a:b])
        v2 = v2[:a] + s + v2[b:]
        a2, b2 = a2 + n1, b2 + n2
    assert (a1, b1) == (4, 2) and (a2, b2) == (8, 4), (a1, b1, a2, b2)

    # ---- Compact list pane (186 x 280): the parts apart
    a, b = include_body(v2, 'Aeon_V524_ViewAeon')
    s = v2[a:b]
    for old, new in (
            ('<left>8</left><top>40</top><width>170</width><height>90</height><align>center</align><aligny>bottom</aligny><font>lb_ui_22_semibold</font>',
             '<left>8</left><top>34</top><width>170</width><height>84</height><align>center</align><aligny>bottom</aligny><font>lb_ui_22_semibold</font>'),
            ('<left>6</left><top>136</top><width>174</width><height>30</height>', '<left>6</left><top>120</top><width>174</width><height>28</height>'),
            ('<left>61</left><top>174</top><width>64</width><height>64</height>', '<left>67</left><top>154</top><width>52</width><height>52</height>'),
            ('<left>80</left><top>193</top><width>26</width><height>26</height>', '<left>83</left><top>170</top><width>20</width><height>20</height>'),
            ('<left>0</left><top>200</top><width>186</width><height>26</height>', '<left>0</left><top>214</top><width>186</width><height>26</height>')):
        s = swap(s, old, new)
    meta = re.search(r'\n\t*<control type="label"><left>0</left><top>248</top><width>186</width><height>28</height>.*?\$VAR\[Aeon_TileMeta\]</label></control>', s)
    assert meta
    s = s[:meta.start()] + s[meta.end():]
    # the pointers: up at the top edge, down at the bottom edge
    s = swap(s, '<left>75</left><top>24</top><width>36</width><height>24</height>', '<left>75</left><top>6</top><width>36</width><height>24</height>', 2)
    s = swap(s, '<left>84</left><top>27</top><width>18</width><height>18</height>', '<left>84</left><top>9</top><width>18</width><height>18</height>')
    s = swap(s, '<left>75</left><top>234</top><width>36</width><height>24</height>', '<left>75</left><top>250</top><width>36</width><height>24</height>', 2)
    s = swap(s, '<left>84</left><top>237</top><width>18</width><height>18</height>', '<left>84</left><top>253</top><width>18</width><height>18</height>')
    v2 = v2[:a] + s + v2[b:]

    for fn, text in ((V2, v2), (VID, vid)):
        io.open(fn, 'w', encoding='utf-8', newline='\n').write(text)
        ET.parse(fn)
    print('ok', dict((p, len(n)) for p, n in sorted(clones.items())))


if __name__ == '__main__':
    run()
