# -*- coding: utf-8 -*-
"""0.56.42 new Skin settings rows (run after _src/regroup_05642.py and _src/strings_05642b.py):
- System: Export skin settings (9513) and Import skin settings (9514), before Reset all skin settings. OK runs
  script.aeon.helper settings,export / settings,import (settingsio.py). The user: "We need an export/import skin
  settings function as well under memory/reset etc."
- Home: Home gradient (9516) Off | Soft | Strong, Skin.String(aeon.homegrad) '' = Soft = the look so far (the lower
  gradient whose strength follows Home vignette, and Fused Glass's bottom scrim). The user: "Home bar - where is the
  setting for the fading gradient from bottom of screen up to the home bar??" and "yes" to Off / Soft / Strong.
- Home, Fused Glass: Now playing on Home (9517) Beside the clock | Left corner, Skin.HasSetting(aeon.fgnpleft) (its own
  switch, so Aeon's Slot / Corner / Line / Bar choice stays apart). The user: "it can at least get a left corner position".
Rows are cloned from rows of the same kind (9549 action, 9745 three segments, 9746 two segments), Up / Down of their
lists written again (settings_rows.renav). Repeatable: a row that is there is left alone."""
import io
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import settings_rows as sr  # noqa: E402

D = '1080i'
A = '$ADDON[skin.aeon.fuse %d]'
HG = 'Skin.String(aeon.homegrad)'


def rd(name):
    return io.open(os.path.join(D, name), encoding='utf-8').read()


def wr(name, text):
    io.open(os.path.join(D, name), 'w', encoding='utf-8', newline='\n').write(text)
    ET.parse(os.path.join(D, name))


def set_clicks(item, rid, clicks):
    b = item.index('<control type="button" id="%d">' % rid)
    be = item.index('</control>', b)
    btn = re.sub(r'\s*<onclick(?: condition="[^"]*")?>[^<]*</onclick>', '', item[b:be])
    btn = btn.rstrip() + ''.join('\n\t\t\t\t\t' + c for c in clicks) + '\n\t\t\t\t'
    return item[:b] + btn + item[be:]


def settings():
    t = rd('SkinSettings.xml')
    if '<!-- row 9513 -->' not in t:
        for new, label, icon, what, value in ((9513, 32725, 'export', 'export', 32727), (9514, 32726, 'import', 'import', 32728)):
            x = sr.clone(t, 9549, new, [('$ADDON[skin.aeon.fuse 32442]', A % label), ('aeon/icons/search.png', 'aeon/icons/%s.png' % icon)])
            x = x.replace('$ADDON[skin.aeon.fuse 32035]', A % value)
            x = set_clicks(x, new, ['<onclick>RunScript(script.aeon.helper,settings,%s)</onclick>' % what])
            t = sr.insert_after(t, 9545 if new == 9513 else 9513, x)
    if '<!-- row 9516 -->' not in t:
        x = sr.clone(t, 9745, 9516, [('$LOCALIZE[31767]', A % 32741), ('aeon/icons/grid.png', 'aeon/icons/contrast.png')])
        x = x.replace('[String.IsEmpty(Skin.String(aeon.vbg)) | String.IsEqual(Skin.String(aeon.vbg),neutral)]', 'String.IsEqual(%s,off)' % HG)
        x = x.replace('String.IsEqual(Skin.String(aeon.vbg),fanart)', '[String.IsEmpty(%s) | String.IsEqual(%s,soft)]' % (HG, HG))
        x = x.replace('String.IsEqual(Skin.String(aeon.vbg),color)', 'String.IsEqual(%s,strong)' % HG)
        x = x.replace('$LOCALIZE[31549]', '$LOCALIZE[31548]').replace('$LOCALIZE[31550]', A % 32740).replace('$LOCALIZE[31680]', '$LOCALIZE[31673]')
        x = set_clicks(x, 9516, ['<onclick condition="String.IsEqual(%s,off)">Skin.Reset(aeon.homegrad)</onclick>' % HG,
                                 '<onclick condition="[String.IsEmpty(%s) | String.IsEqual(%s,soft)]">Skin.SetString(aeon.homegrad,strong)</onclick>' % (HG, HG),
                                 '<onclick condition="String.IsEqual(%s,strong)">Skin.SetString(aeon.homegrad,off)</onclick>' % HG])
        assert 'aeon.vbg' not in x
        t = sr.insert_after(t, 9765, x)
    if '<!-- row 9517 -->' not in t:
        x = sr.clone(t, 9746, 9517, [('$LOCALIZE[31856]', '$LOCALIZE[31765]'), ('aeon/icons/home.png', 'aeon/icons/music.png')])
        x = x.replace('Skin.HasSetting(aeon.lowmenu)', 'Skin.HasSetting(aeon.fgnpleft)').replace('Skin.ToggleSetting(aeon.lowmenu)', 'Skin.ToggleSetting(aeon.fgnpleft)')
        x = x.replace('$LOCALIZE[31857]', A % 32742).replace('$LOCALIZE[31858]', A % 32743)
        assert 'aeon.lowmenu' not in x
        t = sr.insert_after(t, 9743, x)
        t = sr.set_item_visible(t, 9517, '$EXP[Aeon_FGlass]')
    for gid in (9772, 9769):
        t = sr.renav(t, gid)
    wr('SkinSettings.xml', t)
    h = rd('Includes_Settings.xml')
    for rid, sid in ((9513, 32729), (9514, 32730), (9516, 32744), (9517, 32745)):
        h = sr.add_help(h, rid, sid)
    wr('Includes_Settings.xml', h)


def home():
    """the gradient: Off hides the lower gradient (and Fused Glass's bottom scrim), Strong lays a second, taller one over it"""
    t = rd('Includes_Aeon_Home.xml')
    old = ('\t\t<!-- soft gradient over the lower part; the band under the hero is translucent, never black -->\n'
           '\t\t<control type="image">\n\t\t\t<include>Aeon_LowBand</include>\n\t\t\t<left>0</left>\n\t\t\t<top>540</top>\n'
           '\t\t\t<width>1920</width>\n\t\t\t<height>540</height>\n'
           '\t\t\t<texture colordiffuse="$VAR[Aeon_VignetteLow]">aeon/osd_scrim_bottom.png</texture>\n\t\t</control>\n')
    if old in t:
        new = old.replace('aeon/osd_scrim_bottom.png</texture>\n', 'aeon/osd_scrim_bottom.png</texture>\n'
                          '\t\t\t<visible>!String.IsEqual(%s,off)</visible>\n' % HG)
        new = new.replace('<!-- soft gradient over the lower part;', '<!-- soft gradient over the lower part (0.56.42: Skin settings > Home > Home gradient, Soft = this);')
        new += ('\t\t<!-- 0.56.42 Home gradient Strong: a second, taller fade from the bottom up past the Home menu -->\n'
                '\t\t<control type="image">\n\t\t\t<include>Aeon_LowBand</include>\n'
                '\t\t\t<left>0</left><top>360</top><width>1920</width><height>720</height>\n'
                '\t\t\t<texture colordiffuse="b3000000">aeon/osd_scrim_bottom.png</texture>\n'
                '\t\t\t<visible>String.IsEqual(%s,strong)</visible>\n\t\t</control>\n' % HG)
        t = t.replace(old, new)
    old2 = ('\t\t\t<texture colordiffuse="fg_scrim">fg/scrim_b.png</texture>\n\t\t\t<visible>$EXP[Aeon_FGlass]</visible>\n')
    if old2 in t:
        t = t.replace(old2, '\t\t\t<texture colordiffuse="fg_scrim">fg/scrim_b.png</texture>\n'
                            '\t\t\t<visible>$EXP[Aeon_FGlass] + !String.IsEqual(%s,off)</visible>\n' % HG)
    assert 'String.IsEqual(%s,strong)' % HG in t and '$EXP[Aeon_FGlass] + !String.IsEqual(%s,off)' % HG in t
    wr('Includes_Aeon_Home.xml', t)


def spot():
    """the spotlights draw their own bottom fade over their picture (the Home layers lie under the spotlights, 0.29.2), so
    Home gradient drives that one too: Off hides it, Strong lays a taller one over it (Aeon_H_Spot2Item); the other
    spotlight item (Aeon_H_SpotItem) has no bottom fade of its own and gets the Strong one only"""
    t = rd('Includes_Aeon_Home.xml')
    strong = ('\t\t<!-- 0.56.42 Home gradient Strong -->\n\t\t<control type="image">\n'
              '\t\t\t<left>0</left><top>300</top><width>1920</width><height>780</height>\n'
              '\t\t\t<texture colordiffuse="b3000000">aeon/osd_scrim_bottom.png</texture>\n'
              '\t\t\t<visible>String.IsEqual(%s,strong)</visible>\n\t\t</control>\n' % HG)
    i = t.index('<include name="Aeon_H_Spot2Item">')
    j = t.index('\n\t</include>', i)
    blk = t[i:j]
    old = ('\t\t\t<left>0</left><top>420</top><width>1920</width><height>660</height>\n'
           '\t\t\t<texture colordiffuse="e0000000">aeon/osd_scrim_bottom.png</texture>\n\t\t</control>\n')
    if 'Home gradient Strong' not in blk:
        assert old in blk, 'spot2 fade'
        new = old[:-len('\t\t</control>\n')] + '\t\t\t<visible>!String.IsEqual(%s,off)</visible>\n\t\t</control>\n' % HG
        blk = blk.replace(old, new + strong, 1)
        t = t[:i] + blk + t[j:]
    i = t.index('<include name="Aeon_H_SpotItem">')
    j = t.index('\n\t</include>', i)
    blk = t[i:j]
    if 'Home gradient Strong' not in blk:
        k = blk.index('\t\t<!-- title: clearlogo (skin setting), else text -->')
        blk = blk[:k] + strong + blk[k:]
        t = t[:i] + blk + t[j:]
    wr('Includes_Aeon_Home.xml', t)


def capsule():
    """Fused Glass Now playing on Home: Left corner = the same capsule in the lower left corner (60, 976), clear of the
    rows under the menu (they start at x 660)"""
    t = rd('Includes_Fused.xml')
    i = t.index('<include name="FG_NowPlayingCapsule">')
    j = t.index('\n\t</include>', i)              # its own end (the first </include> is Anim_FadeVisible's)
    blk = t[i:j]
    if 'aeon.fgnpleft' not in blk:
        old = '<animation effect="slide" end="92,0" time="0" condition="!$EXP[AG_HasWeather]">Conditional</animation>'
        assert old in blk
        blk = blk.replace(old, '<animation effect="slide" end="92,0" time="0" condition="!$EXP[AG_HasWeather] + !Skin.HasSetting(aeon.fgnpleft)">Conditional</animation>\n'
                               '\t\t\t<!-- 0.56.42 Skin settings > Home > Now playing on Home: Left corner -->\n'
                               '\t\t\t<animation effect="slide" end="-1052,936" time="0" condition="Skin.HasSetting(aeon.fgnpleft)">Conditional</animation>')
        t = t[:i] + blk + t[j:]
    wr('Includes_Fused.xml', t)


def preview():
    """Home gradient's card in the Home page's preview container (skin_previews.py has it in NEW for later runs)"""
    import skin_previews as sp
    t = rd('SkinSettings.xml')
    if '<!-- preview:9516 -->' in t:
        return
    end = t.index('<!-- /PREVIEW CARD home -->')
    tail = t.rindex('</control></control>', 0, end)
    inner = sp.new_inner('home', sp.p_homegrad_t)
    t = t[:tail] + '<!-- preview:9516 -->\n<control type="group"><visible>Control.HasFocus(9516)</visible>%s</control>\n' % inner + t[tail:]
    b = t.rindex('<!-- PREVIEW CARD home (_src/skin_previews.py) -->', 0, end)
    v = t.index('<visible>', b)
    ve = t.index('</visible>', v)
    t = t[:ve] + ' | Control.HasFocus(9516)' + t[ve:]
    wr('SkinSettings.xml', t)
    # the cards' pictures variables: p_homegrad_t uses only existing ones (pic())


def main():
    settings()
    home()
    spot()
    capsule()
    preview()
    print('ok')


if __name__ == '__main__':
    main()
