# -*- coding: utf-8 -*-
"""0.56.15 three Skin settings rows (the user, 2026-11-16):
- Appearance, the Aeon / Glass theme's rows: Home menu underline Off | On (aeon.hm.underline; "in Aeon and Aeon Glass
  we can also use the little yellow underline underscore highlight under Home Menu items, like we have in Fused Glass");
- Appearance, All themes: Fanart look Dimmed | Frosted (aeon.fanartlook; empty = the theme's own: Aeon dimmed, Glass and
  Fused Glass frosted; "I'd like an option to choose a dimmed fanart, like we have in Aeon. Aeon should also be able to
  use the Fused Glass frosted fanart");
- Ratings: Ratings shown as Icons | Text (aeon.rating.text; "should be an option to use icons or text labels too").
Segmented rows as Now playing on Home (9743) draws them; the Up / Down chains and the help lines (Includes_Settings.xml)
follow. Runs once."""
import io
import os
import re
import xml.etree.ElementTree as ET

P = os.path.join('1080i', 'SkinSettings.xml')
HELP = os.path.join('1080i', 'Includes_Settings.xml')
MARK = '0.56.15 settings_05615'
UL, FL, RT = 9766, 9767, 9768
FROST = '[String.IsEqual(Skin.String(aeon.fanartlook),frosted) | [String.IsEmpty(Skin.String(aeon.fanartlook)) + Skin.HasSetting(aeon.vglass)]]'


def segments(rid, opts, right=860):
    """opts: [(selected condition, label, width)]: a pill track ending at `right`, one pill per option"""
    total = 8 + sum(w for _, _, w in opts)
    x0 = right - total
    o = ('<control type="image"><left>%d</left><top>13</top><width>%d</width><height>44</height><texture border="22,0,22,0" colordiffuse="22ffffff">$VAR[Aeon_MenuTexPill]</texture><visible>!Control.HasFocus(%d)</visible></control>\n'
         '\t\t\t\t<control type="image"><left>%d</left><top>13</top><width>%d</width><height>44</height><texture border="22,0,22,0" colordiffuse="26000000">$VAR[Aeon_MenuTexPill]</texture><visible>Control.HasFocus(%d)</visible></control>\n'
         % (x0, total, rid, x0, total, rid))
    x = x0 + 4
    for sel, label, w in opts:
        for fill, foc in (('$VAR[Aeon_Accent]', '!'), ('$VAR[Aeon_OnBarFill]', '')):
            o += ('\t\t\t\t<control type="image"><left>%d</left><top>13</top><width>%d</width><height>44</height><texture border="22,0,22,0" colordiffuse="%s">$VAR[Aeon_MenuTexPill]</texture>'
                  '<visible>[%s] + %sControl.HasFocus(%d)</visible></control>\n' % (x, w, fill, sel, foc, rid))
        for font, col, s, foc in (('st_ui_22_bold', '$VAR[Aeon_AccentText]', '', '!'), ('st_ui_22_bold', '$VAR[Aeon_SegSelTxt]', '', ''),
                                  ('st_ui_22', '99ffffff', '!', '!'), ('st_ui_22', '$VAR[Aeon_SegUnselF]', '!', '')):
            o += ('\t\t\t\t<control type="label"><left>%d</left><top>13</top><width>%d</width><height>44</height><align>center</align><font>%s</font>'
                  '<textcolor>%s</textcolor><label>%s</label><visible>%s[%s] + %sControl.HasFocus(%d)</visible></control>\n'
                  % (x, w, font, col, label, s, sel, foc, rid))
        x += w
    return o


def grouplist_row(tpl, rid, label, icon, vis, enable, nav, clicks, opts):
    """a copy of row 9743 (Appearance grouplist) for another setting"""
    r = tpl.replace('<!-- row 9743 -->', '<!-- row %d -->' % rid)
    r = r.replace('<visible>!$EXP[Aeon_FGlass]</visible>', '<visible>%s</visible>' % vis if vis else '', 1)
    r = r.replace('Control.HasFocus(9743)', 'Control.HasFocus(%d)' % rid).replace('id="9743"', 'id="%d"' % rid)
    r = r.replace('<param name="id" value="9743"/>', '<param name="id" value="%d"/>' % rid)
    r = re.sub(r'<param name="enable" value="[^"]*"/>', '<param name="enable" value="%s"/>' % enable if enable else '', r)
    r = r.replace('<param name="label" value="$LOCALIZE[31765]"/>', '<param name="label" value="%s"/>' % label)
    r = r.replace('<param name="icon" value="aeon/icons/music.png"/>', '<param name="icon" value="%s"/>' % icon)
    b = r.index('<control type="button" id="%d">' % rid)
    be = r.index('</control>', b) + len('</control>')
    button = ('<control type="button" id="%d">\n\t\t\t\t\t%s\n\t\t\t\t\t<include>Dlg_SkinRowButton</include>\n\t\t\t\t\t<onback>9600</onback>\n'
              '\t\t\t\t\t<onleft>SetFocus(9600)</onleft>\n%s\t\t\t\t</control>' % (rid, nav, ''.join('\t\t\t\t\t%s\n' % c for c in clicks)))
    # the segments replace 9743's (from its pill group to the chrome group's end)
    se = r.rindex('\n\t\t\t</control>')
    r = r[:b] + button + '\n\t\t\t\t' + segments(rid, opts).rstrip('\n') + r[se:]
    return r


def main():
    t = io.open(P, encoding='utf-8').read()
    if MARK in t:
        print('already done')
        return
    # ---------------------------------------------------------------- Appearance rows
    i = t.index('<!-- row 9743 -->')
    s = t.rindex('\n', 0, i) + 1
    e = t.index('\n\t</control>\n', i) + len('\n\t</control>\n')
    tpl = t[s:e]
    assert tpl.count('<control type="button" id="9743">') == 1
    off_on = [('!Skin.HasSetting(aeon.hm.underline)', '$LOCALIZE[31548]', 92), ('Skin.HasSetting(aeon.hm.underline)', '$LOCALIZE[31547]', 92)]
    ul = grouplist_row(tpl, UL, '$ADDON[skin.aeon.fuse 32607]', 'aeon/icons/home.png', '!$EXP[Aeon_FGlass]', '!$EXP[Aeon_FGlass]',
                       '<onup>9743</onup><ondown>9741</ondown>',
                       ['<onclick>Skin.ToggleSetting(aeon.hm.underline)</onclick>'], off_on)
    looks = [('!' + FROST, '$ADDON[skin.aeon.fuse 32609]', 132), (FROST, '$ADDON[skin.aeon.fuse 32411]', 132)]
    fl = grouplist_row(tpl, FL, '$ADDON[skin.aeon.fuse 32608]', 'common/aeon_ic_screen.png', None, None,
                       '<onup>9742</onup><ondown>9745</ondown>',
                       ['<onclick condition="%s">Skin.SetString(aeon.fanartlook,dimmed)</onclick>' % FROST,
                        '<onclick condition="!%s">Skin.SetString(aeon.fanartlook,frosted)</onclick>' % FROST], looks)
    t = t[:e] + '\t<!-- %s: Home menu underline (Aeon / Glass) -->\n' % MARK + ul + t[e:]
    i = t.index('<!-- row 9742 -->')
    e2 = t.index('\n\t</control>\n', i) + len('\n\t</control>\n')
    t = t[:e2] + '\t<!-- %s: Fanart look -->\n' % MARK + fl + t[e2:]
    # the neighbours' Up / Down
    for rid, old, new in ((9743, '<ondown>9741</ondown>', '<ondown>%d</ondown>' % UL),
                          (9741, '<onup condition="!$EXP[Aeon_FGlass]">9743</onup>', '<onup condition="!$EXP[Aeon_FGlass]">%d</onup>' % UL),
                          (9742, '<ondown>9745</ondown>', '<ondown>%d</ondown>' % FL),
                          (9745, '<onup>9742</onup>', '<onup>%d</onup>' % FL)):
        b = t.index('<control type="button" id="%d">' % rid)
        be = t.index('</control>', b)
        seg = t[b:be]
        assert seg.count(old) == 1, (rid, old)
        t = t[:b] + seg.replace(old, new) + t[be:]
    # ---------------------------------------------------------------- Ratings: Ratings shown as Icons | Text
    b = t.index('<control type="button" id="9714">')
    gs = t.rindex('\t\t\t<control type="group">\n\t\t\t\t<top>471</top>', 0, b)
    ge = t.index('\n\t\t\t</control>\n', b) + len('\n\t\t\t</control>\n')
    g = t[gs:ge]
    g = g.replace('<top>471</top>', '<top>541</top>', 1).replace('9714', str(RT))
    g = g.replace('<param name="label" value="$LOCALIZE[31780]"/>', '<param name="label" value="$ADDON[skin.aeon.fuse 32610]"/>')
    bb = g.index('<control type="button" id="%d">' % RT)
    bbe = g.index('</control>', bb) + len('</control>')
    button = ('<control type="button" id="%d">\n\t\t\t\t\t<include>Dlg_SkinRowButton</include>\n\t\t\t\t\t<onup>9714</onup>\n\t\t\t\t\t<ondown>9710</ondown>\n'
              '\t\t\t\t\t<onback>9567</onback>\n\t\t\t\t\t<onleft>SetFocus(9567)</onleft>\n\t\t\t\t\t<onclick>Skin.ToggleSetting(aeon.rating.text)</onclick>\n\t\t\t\t</control>' % RT)
    se = g.rindex('\n\t\t\t</control>')
    g = g[:bb] + button + '\n\t\t\t\t' + segments(RT, [('!Skin.HasSetting(aeon.rating.text)', '$LOCALIZE[536]', 112),
                                                        ('Skin.HasSetting(aeon.rating.text)', '$ADDON[skin.aeon.fuse 32611]', 112)]).rstrip('\n') + g[se:]
    t = t[:ge] + '\t\t\t<!-- %s: Ratings shown as Icons | Text -->\n' % MARK + g + t[ge:]
    # its focus bar (the page's focus bars are separate groups)
    m = re.search(r'\t\t\t<control type="group">\n\t\t\t\t<left>-119</left>\n\t\t\t\t<top>471</top>\n\t\t\t\t<visible>Control.HasFocus\(9714\)</visible>.*?\n\t\t\t</control>\n', t, re.S)
    assert m
    t = t[:m.end()] + m.group(0).replace('<top>471</top>', '<top>541</top>').replace('Control.HasFocus(9714)', 'Control.HasFocus(%d)' % RT) + t[m.end():]
    for rid, old, new in ((9714, '<ondown>9710</ondown>', '<ondown>%d</ondown>' % RT), (9710, '<onup>9714</onup>', '<onup>%d</onup>' % RT)):
        b = t.index('<control type="button" id="%d">' % rid)
        be = t.index('</control>', b)
        seg = t[b:be]
        assert seg.count(old) == 1, (rid, old)
        t = t[:b] + seg.replace(old, new) + t[be:]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(P)
    # ---------------------------------------------------------------- help lines
    h = io.open(HELP, encoding='utf-8').read()
    anchor = '\t\t<value condition="Control.HasFocus(9743)">$LOCALIZE[31580]</value>\n'
    assert h.count(anchor) == 1
    h = h.replace(anchor, anchor + '\t\t<value condition="Control.HasFocus(%d)">$ADDON[skin.aeon.fuse 32612]</value>\n'
                  '\t\t<value condition="Control.HasFocus(%d)">$ADDON[skin.aeon.fuse 32613]</value>\n'
                  '\t\t<value condition="Control.HasFocus(%d)">$ADDON[skin.aeon.fuse 32614]</value>\n' % (UL, FL, RT))
    io.open(HELP, 'w', encoding='utf-8', newline='\n').write(h)
    ET.parse(HELP)
    print('ok')


if __name__ == '__main__':
    main()
