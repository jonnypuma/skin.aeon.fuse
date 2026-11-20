# -*- coding: utf-8 -*-
"""Helpers for rows in the Skin settings pages that are scrolling lists (0.56.42, _src/regroup_05642.py): find a row's
list item, clone it with new ids / texts, put it after another row, and write Up / Down of a whole list again from the
order and the visibility of its items (first true condition wins, hidden rows are skipped, the ends wrap)."""
import re

import settings_sections as ss

LISTS = {9770: 9600, 9772: 9551, 9777: 9567, 9774: 9566, 9782: 9601, 9784: 9552, 9786: 9568, 9788: 9569, 9769: 9553}


def item_start(t, rid):
    """where the list item of row rid starts (its marker: <!-- row N --> or <!-- row N (generator) -->)"""
    x = re.search(r'<control type="group"><!-- row %d(?: \([^)]*\))? -->' % rid, t)
    if not x:
        raise ValueError('row %d: no list item' % rid)
    return x.start()


def item_span(t, rid):
    """(start, end) of the list item (70 px group) that holds row rid"""
    m = ss.masked(t)
    i = item_start(t, rid)
    return i, ss.ctl_end(m, i)


def list_of(t, rid):
    """the id of the list that holds row rid"""
    i = item_start(t, rid)
    best = None
    for gid in LISTS:
        g = t.find('<control type="grouplist" id="%d">' % gid)
        if 0 <= g < i and (best is None or g > best[1]):
            best = (gid, g)
    return best[0]


def clone(t, rid, new_id, swaps=()):
    """the item of row rid as a new row new_id: every rid in it becomes new_id, then each (old, new) of swaps once"""
    s, e = item_span(t, rid)
    x = re.sub(r'(?<!\d)%d(?!\d)' % rid, str(new_id), t[s:e])
    for old, new in swaps:
        assert old in x, (rid, old)
        x = x.replace(old, new, 1)
    return x


def insert_after(t, after, item):
    s, e = item_span(t, after)
    return t[:e] + '\n\t' + item + t[e:]


def set_item_visible(t, rid, cond):
    s, e = item_span(t, rid)
    x = t[s:e]
    o, c = ss.props(x)
    p = re.sub(r'\s*<visible>.*?</visible>', '', x[o:c], count=1)
    if cond:
        p = p.rstrip() + '\n\t\t<visible>%s</visible>\n' % cond
    return t[:s] + x[:o] + p + x[c:] + t[e:]


def renav(t, gid):
    """Up / Down of every row in list gid written again"""
    m = ss.masked(t)
    s = t.index('<control type="grouplist" id="%d">' % gid)
    e = ss.ctl_end(m, s)
    rows = []
    for a, b in ss.children(m, s, e):
        btns = re.findall(r'<control type="button" id="(\d+)">', m[a:b])
        if btns:
            rows.append((int(btns[0]), a, b, ss.own_visible(t[a:b])))
    vis = dict((r, v) for r, _, _, v in rows)
    ids = [r for r, _, _, v in rows if v != 'false']

    def nav(r):
        i = ids.index(r)
        out = []
        for tag, step in (('onup', -1), ('ondown', 1)):
            k = i
            for _ in range(len(ids) - 1):
                k = (k + step) % len(ids)
                c = vis[ids[k]]
                if c:
                    out.append('<%s condition="%s">%d</%s>' % (tag, c, ids[k], tag))
                else:
                    out.append('<%s>%d</%s>' % (tag, ids[k], tag))
                    break
        return ''.join(out)

    for r, a, b, v in sorted(rows, key=lambda x: -x[1]):
        it = t[a:b]
        bi = it.index('<control type="button" id="%d">' % r)
        be = it.index('</control>', bi)
        btn = it[bi:be]
        btn = re.sub(r'\s*<onup[^>]*>\d+</onup>', '', btn)        # 0.56.45: builtin actions (pickmode) stay
        btn = re.sub(r'\s*<ondown[^>]*>\d+</ondown>', '', btn)
        if v != 'false':
            k = btn.index('>') + 1
            m = re.search(r'<!-- 0.56.45 pickmode -->\s*(?:<on(?:up|down|back)[^>]*>[^<]*</on(?:up|down|back)>\s*)*', btn)
            if m:       # 0.56.45: after a pick row's closing actions
                k = m.end()
            btn = btn[:k] + '\n\t\t\t\t\t' + nav(r) + btn[k:]
        t = t[:a] + it[:bi] + btn + it[be:] + t[b:]
    return t


def add_help(h, rid, string_id, before=None):
    """Dlg_SkinHelp: the help line of row rid (a skin string from 32000 up)"""
    line = '\t\t<value condition="Control.HasFocus(%d)">$ADDON[skin.aeon.fuse %d]</value>\n' % (rid, string_id)
    if 'Control.HasFocus(%d)">' % rid in h[h.index('<variable name="Dlg_SkinHelp">'):]:
        return h
    i = h.index('<variable name="Dlg_SkinHelp">')
    i = h.index('\n', i) + 1
    return h[:i] + line + h[i:]
