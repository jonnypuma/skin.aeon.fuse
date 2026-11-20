"""0.56.45 Skin settings: choose an option, then set it (the user, 2026-11-18: "Is it possible to press OK on an option
and then it will let you cycle each option and when you have decided which option to set you press OK again and
then the option activates?").

Rows with three or more options (pills): OK opens the row (Window(Home).Property(aeon.pickrow) = the row, aeon.pick
= the option in use, counted from 0); Left / Right move the pick (the filled pill follows it, a ring round the pills
shows the row is open, the help line says how); OK sets the picked option and closes the row; Up / Down / Back close
it unchanged (Back goes to the category list as before). Two-option rows and switches keep one OK press.
Kodi checks all of a click's conditions against the state before the click, then runs the actions in order
(CGUIAction::ExecuteActions), so one OK can test "open?" and change it.

Also "after pressing OK on a setting, the highlight focus bar is set back to the category list": rows that reload the
skin (Focus highlight, Skin style, theme, palette, fonts) note themselves (aeon.skinback / aeon.skinbackcat, Home
window properties survive a skin reload) and the window's onload puts the page and the focus back.

Run from the skin folder after the settings generators (settings_05644.py ...), after renav, then ok_only.py (it keeps
the pick moves). Repeatable: rows already done are skipped."""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import settings_rows as sr      # noqa: E402
import settings_sections as ss  # noqa: E402

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
SKIN = os.path.join(D, 'SkinSettings.xml')
INC = os.path.join(D, 'Includes_Settings.xml')
GLASS = os.path.join(D, 'Includes_Aeon_Glass.xml')
P = 'Window(Home).Property(aeon.pick)'
HELP = 32748
RELOAD = re.compile(r'ReloadSkin|RunScript\(script\.aeon\.helper,(theme|menutheme|skinstyle|palette|fonts)\b')
MARK = '<!-- 0.56.45 pickmode -->'


def E(rid):
    return 'String.IsEqual(Window(Home).Property(aeon.pickrow),%d)' % rid


def norm(c):
    return re.sub(r'[\[\]\s]', '', c)


def options(x, rid):
    pat = (r'<control type="label"><left>(\d+)</left><top>13</top><width>\d+</width><height>44</height><align>center</align>'
           r'<font>st_ui_22_bold</font><textcolor>\$VAR\[Aeon_AccentText\]</textcolor><label>([^<]*)</label>'
           r'<visible>(.*?) \+ !Control.HasFocus\(%d\)</visible>' % rid)
    return [(int(a), b, c) for a, b, c in re.findall(pat, x)]


def token(cond, key):
    m = re.search(r'(?<!!)String\.IsEqual\(Skin\.String\(%s\),(\w+)\)' % re.escape(key), cond)
    return m.group(1) if m else ''


AEON = '!Skin.HasSetting(aeon.vglass)'
AGL = 'Skin.HasSetting(aeon.vglass) + !Skin.HasSetting(aeon.fglass)'
FGL = 'Skin.HasSetting(aeon.fglass)'
MT = 'String.IsEqual(Skin.String(aeon.menutheme),%s)'
FM = 'String.IsEqual(Skin.String(aeon.fgmenu),%s)'
# 9748 Skin style, its options per theme: (group, the condition as its pills read it, the helper call that sets it)
STYLE = [('aeon', '[%s]' % (MT % 'mosaic'), 'menutheme,mosaic'),
         ('aeon', '[%s]' % (MT % 'ledger'), 'menutheme,ledger'),
         ('aeon', '[![%s | %s | %s | %s]]' % (MT % 'mosaic', MT % 'ledger', MT % 'tabslab', MT % 'fused'), 'menutheme,aeon'),
         ('aeon', '[%s]' % (MT % 'tabslab'), 'menutheme,tabslab'),
         ('aeon', '[%s]' % (MT % 'fused'), 'menutheme,fused'),
         ('glass', '[[String.IsEmpty(Skin.String(aeon.menutheme)) | !%s]]' % (MT % 'fused'), 'menutheme,aeon'),
         ('glass', '[%s]' % (MT % 'fused'), 'menutheme,fused'),
         ('fg', '[String.IsEmpty(Skin.String(aeon.fgmenu))]', 'skinstyle,dark'),
         ('fg', '[%s]' % (FM % 'glass'), 'skinstyle,glass'),
         ('fg', '[%s]' % (FM % 'frost'), 'skinstyle,frost'),
         ('fg', '[%s]' % (FM % 'system'), 'skinstyle,system')]
PREFIX = {'aeon': AEON, 'glass': AGL, 'fg': FGL}
STYLE_FG_LEFT = 0       # the Fused Glass pills' group has no offset of its own


def plan_style(opts):
    """9748 Skin style: three groups (the Aeon menu styles, Aeon Glass, Fused Glass), each set by the helper; the click
    logic gets the theme in front, the pills keep their own text (style_visuals)"""
    return [(g, j, '', '%s + %s' % (PREFIX[g], core), ['RunScript(script.aeon.helper,%s)' % call])
            for j, (g, core, call) in enumerate(STYLE)]


def style_visuals(seg, e):
    """the pills of 9748 block by block (Aeon Glass first, then the Aeon theme, then Fused Glass): the same text means
    different options in different blocks (Fuse)"""
    out, group = [], 'glass'
    for line in seg.split('\n'):
        if '<!-- Aeon theme' in line:
            group = 'aeon'
        elif '<!-- Fused Glass' in line:
            group = 'fg'
        if '<visible>' in line:
            for j in sorted((j for j, s in enumerate(STYLE) if s[0] == group), key=lambda j: -len(STYLE[j][1])):
                line = line.replace(STYLE[j][1], '@@%d@@' % j)
            for j, s in enumerate(STYLE):
                line = line.replace('@@%d@@' % j, '[[!%s + %s] | [%s + String.IsEqual(%s,%d)]]' % (e, s[1], e, P, j))
        out.append(line)
    return '\n'.join(out)


def theme_key(cond):
    """the theme an option of row 9744 stands for, from its condition (0.56.51: the old guess looked for "glass" in the
    text, and aeon.vglass / aeon.fglass both contain it, so every pill set Aeon Glass)"""
    c = norm(cond)
    if 'Skin.HasSetting(aeon.fglass)' in c and '!Skin.HasSetting(aeon.fglass)' not in c:
        return 'fused'
    if '!Skin.HasSetting(aeon.vglass)' in c:
        return 'aeon'
    assert 'Skin.HasSetting(aeon.vglass)' in c, cond
    return 'glass'


def plan_theme(opts):
    out = []
    for left, label, cond in sorted(opts):
        out.append(('all', left, label, cond, ['RunScript(script.aeon.helper,theme,%s)' % theme_key(cond)]))
    assert [a[4][0].rsplit(',', 1)[1][:-1] for a in out] == ['aeon', 'glass', 'fused'], out
    return out


def plan_chain(rid, opts, clicks):
    """the set actions of each option from the old chain (the actions under option i's condition set option i+1)"""
    opts = sorted(opts)
    conds = []
    for c, a in clicks:
        if c and (not conds or conds[-1][0] != c):
            conds.append((c, [a]))
        elif c:
            conds[-1][1].append(a)
    sets = {}
    for c, acts in conds:
        hit = [j for j, (_l, _b, oc) in enumerate(opts) if norm(c) == norm(oc) or norm(c).startswith(norm(oc) + '+')
               or norm(oc).endswith('+' + norm(c))]      # the pills may add the theme in front (Home bar 9764)
        if len(hit) != 1:
            return None, 'condition %r matches %s' % (c[:80], hit)
        sets[(hit[0] + 1) % len(opts)] = acts
    if len(sets) != len(opts):
        return None, 'only %d of %d options have a set action' % (len(sets), len(opts))
    return [('all', l, b, oc, sets[j]) for j, (l, b, oc) in enumerate(opts)], ''


def rewrite(x, rid, plan, after):
    n = len(plan)
    e = E(rid)
    b0 = x.index('<control type="button" id="%d">' % rid)
    b1 = x.index('</control>', b0)
    btn = x[b0:b1]
    btn = re.sub(r'\s*<onclick[^>]*>[^<]*</onclick>', '', btn)
    # Left / Right / Back of the closed row keep what they did; Up / Down close an open row
    btn = re.sub(r'<onleft>', '<onleft condition="!%s">' % e, btn)
    btn = re.sub(r'<onleft condition="(?!!String.IsEqual\(Window\(Home\).Property\(aeon.pickrow\))', '<onleft condition="!%s + ' % e, btn)
    btn = re.sub(r'<onright>', '<onright condition="!%s">' % e, btn)
    reload_row = any(RELOAD.search(a) for _g, _l, _b, _c, acts in plan for a in acts) or any(RELOAD.search(a) for a in after)
    clicks = []
    for j, (_g, _l, _b, cond, _acts) in enumerate(plan):
        clicks.append('<onclick condition="!%s + %s">SetProperty(aeon.pick,%d,home)</onclick>' % (e, cond, j))
    clicks.append('<onclick condition="!%s">SetProperty(aeon.pickrow,%d,home)</onclick>' % (e, rid))
    for j, (_g, _l, _b, cond, acts) in enumerate(plan):
        ch = '%s + String.IsEqual(%s,%d) + ![%s]' % (e, P, j, cond)
        if reload_row:
            clicks.append('<onclick condition="%s">SetProperty(aeon.skinback,%d,home)</onclick>' % (ch, rid))
            clicks.append('<onclick condition="%s">CancelAlarm(aeonskinback,true)</onclick>' % ch)
            clicks.append('<onclick condition="%s">SetProperty(aeon.skinbackcat,$INFO[Window(Home).Property(aeon.skincat)],home)</onclick>' % ch)
        for a in acts:
            clicks.append('<onclick condition="%s">%s</onclick>' % (ch, a))
        for a in after:
            clicks.append('<onclick condition="%s">%s</onclick>' % (ch, a))
    clicks.append('<onclick condition="%s">ClearProperty(aeon.pickrow,home)</onclick>' % e)
    moves = []
    for j, (g, _l, _b, _c, _a) in enumerate(plan):
        prev = j - 1 if j > 0 and plan[j - 1][0] == g else None
        nxt = j + 1 if j + 1 < n and plan[j + 1][0] == g else None
        c = '%s + String.IsEqual(%s,%d)' % (e, P, j)
        moves.append('<onleft condition="%s">%s</onleft>' % (c, 'SetProperty(aeon.pick,%d,home)' % prev if prev is not None else 'noop'))
        moves.append('<onright condition="%s">%s</onright>' % (c, 'SetProperty(aeon.pick,%d,home)' % nxt if nxt is not None else 'noop'))
    close = ['<onup condition="%s">ClearProperty(aeon.pickrow,home)</onup>' % e,
             '<ondown condition="%s">ClearProperty(aeon.pickrow,home)</ondown>' % e,
             '<onback condition="%s">ClearProperty(aeon.pickrow,home)</onback>' % e]
    k = btn.index('>') + 1
    btn = btn[:k] + '\n\t\t\t\t\t' + MARK + '\n\t\t\t\t\t' + '\n\t\t\t\t\t'.join(close + moves + clicks) + btn[k:]
    x = x[:b0] + btn + x[b1:]
    # the pills: in an open row the pick is filled, not the option in use
    seg0 = x.index('</control>', x.index('<control type="button" id="%d">' % rid)) + len('</control>')
    seg = x[seg0:]
    if rid == 9748:
        seg = style_visuals(seg, e)
    else:
        for j, (_g, _l, _b, cond, _a) in enumerate(plan):
            seg = seg.replace(cond, '[[!%s + %s] | [%s + String.IsEqual(%s,%d)]]' % (e, cond, e, P, j))
    # the ring round the pills while the row is open (9748: one per theme, its pills are three tracks)
    tracks = re.findall(r'<control type="image"><left>(\d+)</left><top>13</top><width>(\d+)</width><height>44</height>'
                        r'<texture border="22,0,22,0" colordiffuse="22ffffff">[^<]*</texture><visible>([^<]*)</visible>', seg)
    rings = []
    for l, w, vis in tracks:
        cond = e
        if rid == 9748:
            theme = vis.replace('!Control.HasFocus(%d)' % rid, '').replace('[]', '').strip(' +')
            cond = '%s + %s' % (e, theme or FGL)
            l = int(l) + (STYLE_FG_LEFT if not theme else 0)
        rings.append('<control type="image"><left>%d</left><top>9</top><width>%d</width><height>52</height><texture border="26,0,26,0" '
                     'colordiffuse="$VAR[FGS_Aeon_OnBarInk]">$VAR[Aeon_MenuTexRing]</texture><visible>%s</visible></control>'
                     % (int(l) - 4, int(w) + 8, cond))
        if rid != 9748:
            break
    if rings:
        tail = '\n\t\t\t</control>\n\t</control>'
        assert seg.endswith(tail)
        seg = seg[:-len(tail)] + '\n\t\t\t\t' + '\n\t\t\t\t'.join(rings) + tail
    return x[:seg0] + seg, reload_row


def main():
    t = io.open(SKIN, encoding='utf-8').read()
    report, done = [], 0
    m = ss.masked(t)
    rows = []
    for gid in sr.LISTS:
        s = t.index('<control type="grouplist" id="%d">' % gid)
        e = ss.ctl_end(m, s)
        for a, b in ss.children(m, s, e):
            bt = re.search(r'<control type="button" id="(\d+)">', m[a:b])
            if bt:
                rows.append(int(bt.group(1)))
    for rid in rows:
        s, e = sr.item_span(t, rid)
        x = t[s:e]
        if MARK in x:
            continue
        opts = options(x, rid)
        btn = re.search(r'<control type="button" id="%d">(.*?)</control>' % rid, x, re.S).group(1)
        clicks = re.findall(r'<onclick(?: condition="([^"]*)")?>([^<]*)</onclick>', btn)
        after = [a for c, a in clicks if not c]
        if rid == 9748:
            plan = plan_style(opts)
            after = []
        elif rid == 9744:
            plan = plan_theme(opts)
            after = []
        elif len(opts) >= 3:
            plan, why = plan_chain(rid, opts, clicks)
            if not plan:
                report.append('%d: skipped (%s)' % (rid, why))
                continue
        else:
            # two options / switches: one OK as before; a reloading one notes itself for the focus to come back
            if any(RELOAD.search(a) for _c, a in clicks) and 'aeon.skinback' not in x:
                b0 = x.index('<control type="button" id="%d">' % rid)
                k = x.index('>', b0) + 1
                x = x[:k] + ('\n\t\t\t\t\t<onclick>SetProperty(aeon.skinback,%d,home)</onclick>'
                             '<onclick>SetProperty(aeon.skinbackcat,$INFO[Window(Home).Property(aeon.skincat)],home)</onclick>' % rid) + x[k:]
                t = t[:s] + x + t[e:]
                report.append('%d: notes itself before its reload' % rid)
            continue
        x, rl = rewrite(x, rid, plan, after)
        t = t[:s] + x + t[e:]
        done += 1
        report.append('%d: %d options%s' % (rid, len(plan), ', reloads' if rl else ''))
    # the window: no row open when it opens or closes; after a reload, the page and the row again
    if 'aeon.skinback' not in t[:t.index('<controls>')]:
        old = '\t<onload>SetProperty(aeon.skincat,appearance,home)</onload>\n'
        assert old in t
        t = t.replace(old, old +
                      '\t<onload>ClearProperty(aeon.pickrow,home)</onload>\n'
                      '\t<onload condition="!String.IsEmpty(Window(Home).Property(aeon.skinback))">SetProperty(aeon.skincat,$INFO[Window(Home).Property(aeon.skinbackcat)],home)</onload>\n'
                      '\t<onload condition="!String.IsEmpty(Window(Home).Property(aeon.skinback))">SetFocus($INFO[Window(Home).Property(aeon.skinback)])</onload>\n'
                      '\t<onload>CancelAlarm(aeonskinback,true)</onload>\n'
                      '\t<onload>AlarmClock(aeonskinback,ClearProperty(aeon.skinback,home),00:08,silent)</onload>\n'
                      '\t<onunload>ClearProperty(aeon.pickrow,home)</onunload>\n', 1)
    io.open(SKIN, 'w', encoding='utf-8', newline='\n').write(t)
    h = io.open(INC, encoding='utf-8').read()
    line = '\t\t<value condition="!String.IsEmpty(Window(Home).Property(aeon.pickrow))">$ADDON[skin.aeon.fuse %d]</value>\n' % HELP
    if line not in h:
        i = h.index('<variable name="Dlg_SkinHelp">')
        i = h.index('\n', i) + 1
        h = h[:i] + line + h[i:]
        io.open(INC, 'w', encoding='utf-8', newline='\n').write(h)
    g = io.open(GLASS, encoding='utf-8').read()
    if 'name="Aeon_MenuTexRing"' not in g:
        i = g.index('\t<variable name="Aeon_MenuTexOutline">')
        g = g[:i] + ('\t<!-- 0.56.45 pickmode: the ring round an open row\'s pills -->\n'
                     '\t<variable name="Aeon_MenuTexRing">\n'
                     '\t\t<value condition="$EXP[Aeon_Fused] | Skin.HasSetting(aeon.vglass)">aeon/pill_52_ring.png</value>\n'
                     '\t\t<value>common/aeon_flat_pill_52_ring.png</value>\n'
                     '\t</variable>\n') + g[i:]
        io.open(GLASS, 'w', encoding='utf-8', newline='\n').write(g)
    print('\n'.join(report))
    print('pickmode: %d rows' % done)


if __name__ == '__main__':
    main()
