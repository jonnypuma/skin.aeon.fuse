"""0.56.33 Skin settings > Appearance (grouplist 9770), the user's notes of 2026-11-17:
- Library background (9745) above Fanart look (9767); Fanart look shows only when Library background is Fanart
  (Skin.String(aeon.vbg) fanart), its expert rows (9794-9796) with it;
- the expert rows sit under what they change: Panel opacity / blur / tint (9791-9793) right under Skin style (9748),
  Fanart opacity / blur / tint (9794-9796) right under Fanart look; the Expert settings switch (9790) and Reset (9797)
  stay at the end. Before, Expert on showed them at the bottom of the page, out of sight ("does nothing").
- every row's Up / Down is rebuilt from the page order: the next row whose visibility holds, wrapping at the ends.
Run from the skin folder after the generators that add rows to 9770 (expert_05628, fgs_dialogs_05632). Repeatable."""
import io
import os
import re

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'SkinSettings.xml')
VBG = 'String.IsEqual(Skin.String(aeon.vbg),fanart)'


def ctl_end(t, start):
    depth = 0
    for m in re.finditer(r'<control[ >]|</control>', t[start:]):
        depth += -1 if m.group(0) == '</control>' else 1
        if depth == 0:
            return start + m.end()
    raise ValueError(start)


def children(t, gstart):
    """(start, end) of each top-level control inside the grouplist starting at gstart, plus the comment lines that
    belong to the next one (kept with it)"""
    inner = t.index('>', gstart) + 1
    gend = ctl_end(t, gstart)
    out = []
    pos = inner
    while True:
        m = re.compile(r'<control[ >]').search(t, pos, gend)
        if not m:
            break
        s = m.start()
        # take the comment lines right above with the control
        line = t.rfind('\n', 0, s) + 1
        while True:
            prev = t.rfind('\n', 0, line - 1) + 1
            if t[prev:line].strip().startswith('<!--') and t[prev:line].strip().endswith('-->'):
                line = prev
            else:
                break
        s = max(line, pos)
        e = ctl_end(t, m.start())
        out.append((s, e))
        pos = e
    return out, gend


def row_id(block):
    for m in re.finditer(r'<control type="button" id="(\d+)">', block):
        if 'Dlg_SkinRowButton' in block[m.start():ctl_end(block, m.start())]:
            return int(m.group(1))
    return None


def head_end(block):
    """end of the group's own head: the first nested control after the group's own tag (comments above skipped)"""
    first = block.index('<control')
    nxt = block.find('<control', first + 8)
    return nxt if nxt != -1 else len(block)


def own_visible(block):
    m = re.search(r'<visible>([^<]*)</visible>', block[:head_end(block)])
    return m.group(1) if m else None


def set_visible(block, cond):
    he = head_end(block)
    head = block[:he]
    if '<visible>' in head:
        head = re.sub(r'<visible>[^<]*</visible>', '<visible>%s</visible>' % cond, head, count=1)
    else:
        head = head.replace('<height>70</height>', '<height>70</height>\n\t\t<visible>%s</visible>' % cond, 1)
    return head + block[he:]


def main():
    t = io.open(P, encoding='utf-8').read()
    g = t.index('<control type="grouplist" id="9770">')
    kids, gend = children(t, g)
    blocks = [t[s:e] for s, e in kids]
    ids = [row_id(b) for b in blocks]
    order = list(range(len(blocks)))

    def move(rid, after):
        i, j = ids.index(rid), ids.index(after)
        k = order.index(i)
        order.pop(k)
        order.insert(order.index(j) + 1, i)

    def move_before(rid, before):
        i, j = ids.index(rid), ids.index(before)
        k = order.index(i)
        order.pop(k)
        order.insert(order.index(j), i)

    # Library background above Fanart look
    if order.index(ids.index(9745)) > order.index(ids.index(9767)):
        move_before(9745, 9767)
    # expert rows under what they change
    for rid, after in ((9791, 9748), (9792, 9791), (9793, 9792), (9794, 9767), (9795, 9794), (9796, 9795)):
        move(rid, after)
    # 0.56.37 (home_names_05637): "only the focused item's name" is for every theme now: under ALL THEMES, after
    # Home menu position
    move(9546, 9746)
    # visibility: Fanart look and its expert rows only with a Fanart library background
    for rid in (9767, 9794, 9795, 9796):
        i = ids.index(rid)
        cur = own_visible(blocks[i])
        if cur and VBG in cur:
            continue
        blocks[i] = set_visible(blocks[i], (cur + ' + ' + VBG) if cur else VBG)
    # rebuild Up / Down from the final order
    seq = [(ids[i], own_visible(blocks[i])) for i in order if ids[i]]

    def chain(tag, items):
        out = ''
        for rid, vis in items:
            out += '<%s condition="%s">%d</%s>' % (tag, vis, rid, tag) if vis else '<%s>%d</%s>' % (tag, rid, tag)
            if not vis:
                break
        return out
    for n, (rid, vis) in enumerate(seq):
        ups = list(reversed(seq[:n])) + list(reversed(seq[n + 1:]))
        downs = seq[n + 1:] + seq[:n]
        i = ids.index(rid)
        b = blocks[i]
        bs = b.index('<control type="button" id="%d">' % rid)
        be = ctl_end(b, bs)
        btn = b[bs:be]
        btn = re.sub(r'<onup(?: condition="[^"]*")?>[^<]*</onup>', '', btn)
        btn = re.sub(r'<ondown(?: condition="[^"]*")?>[^<]*</ondown>', '', btn)
        btn = btn.replace('<control type="button" id="%d">' % rid,
                          '<control type="button" id="%d">\n\t\t\t\t\t%s%s' % (rid, chain('onup', ups), chain('ondown', downs)), 1)
        blocks[i] = b[:bs] + btn + b[be:]
    s0 = kids[0][0]
    e0 = kids[-1][1]
    for (s1, e1), (s2, _e2) in zip(kids, kids[1:]):
        assert not t[e1:s2].strip(), ('text between rows', t[e1:s2][:80])
    new = '\n'.join(blocks[i].strip('\n') for i in order)
    t = t[:s0] + new + t[e0:]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    print('Appearance:', [r for r, _v in seq])


if __name__ == '__main__':
    main()
