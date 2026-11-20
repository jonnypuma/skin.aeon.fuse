# -*- coding: utf-8 -*-
"""0.56.29 the Fused Glass style, the connected grid (the user: "the new menu sections are not connected, it's missing the
vertical line between settings groups and you have huge gaps, see how it should look like in your own mockup
screenshots"; the boards KodiSkin / SkinDetails: one frame, a divider between the columns, the columns touching).
Idempotent; run after fgs_05629.py.

- Skin settings: under the Fused Glass style the Fused Glass offsets (the category column 24 px left, the pages 20 px
  right, the preview) are off, so the columns sit as in Aeon, flush; the frame (top, bottom, sides) and the dividers at
  480 and 1500 show, with the rules under the title band and the rows.
- Kodi settings pages and add-on settings: the Fused Glass style uses the classic page (SetCat_Classic /
  AddonSet_Classic: one frame 100-1820 x 180-864, the divider at 480, the categories flush with the settings), its frame
  lines on, and the System screen's focus in its templates (params fgs / pre: the white bar + rules, a rule under each
  row, white ink); the open category's grey overlay off (Kodi's faded bar marks it); the level button the bar too.
"""
import io
import os
import re

D = '1080i'
MARK = '0.56.29 fgs_flush'


def rd(p):
    return io.open(os.path.join(D, p), encoding='utf-8').read()


def wr(p, t):
    io.open(os.path.join(D, p), 'w', encoding='utf-8', newline='\n').write(t)


def skin_settings():
    t = rd('SkinSettings.xml')
    # every step is safe to repeat (skin_previews.py rewrites its cards between runs)
    a = 'condition="$EXP[Aeon_FGlass]">Conditional</animation>'
    n = t.count(a)
    t = t.replace(a, 'condition="$EXP[Aeon_FGlass] + !$EXP[FGS]">Conditional</animation>')
    # the frame and the dividers (Aeon / Aeon Glass) under the Fused Glass style too
    frame = 0
    for m in list(re.finditer(r'<control type="image"><left>(120|480|1500|1820)</left><top>(108|960)</top><width>(1700|1)</width><height>(1|852)</height>'
                              r'<texture colordiffuse="30ffffff">common/white\.png</texture><visible>([^<]*)</visible></control>', t)):
        pass
    def fr(mm):
        nonlocal frame
        if mm.group(2).endswith('| $EXP[FGS]'):
            return mm.group(0)
        frame += 1
        return mm.group(1) + '<visible>[%s] | $EXP[FGS]</visible>' % mm.group(2)
    t = re.sub(r'(<control type="image"><left>(?:120|480|1500|1820)</left><top>(?:108|960)</top><width>(?:1700|1)</width><height>(?:1|852)</height>'
               r'<texture colordiffuse="30ffffff">common/white\.png</texture>)<visible>([^<]*)</visible>', fr, t)
    # the title band's rule
    old = '<visible>[[!String.IsEqual(Window(Home).Property(aeon.skincat),homemenu)] + !$EXP[Aeon_Fused]] + !$EXP[Aeon_FGlass]</visible>'
    k = t.count(old)
    t = t.replace(old, '<visible>[[!String.IsEqual(Window(Home).Property(aeon.skincat),homemenu)] + !$EXP[Aeon_Fused]] + [!$EXP[Aeon_FGlass] | $EXP[FGS]]</visible>')
    if MARK not in t:
        t = t.replace('<control type="group"><left>120</left><top>108</top><width>360</width>', '<!-- %s --><control type="group"><left>120</left><top>108</top><width>360</width>' % MARK, 1)
    wr('SkinSettings.xml', t)
    print('skin settings: offsets %d, frame lines %d, title rule %d' % (n, frame, k))


def windows():
    for name, classic, fg in (('SettingsCategory.xml', 'SetCat_Classic', 'FG_SettingsPage'), ('DialogAddonSettings.xml', 'AddonSet_Classic', 'FG_AddonSettingsPage')):
        t = rd(name)
        a = '<include condition="!Skin.HasSetting(aeon.fglass) + !$EXP[Aeon_MS]">%s</include>' % classic
        b = '<include condition="[!Skin.HasSetting(aeon.fglass) + !$EXP[Aeon_MS]] | $EXP[FGS]">%s</include><!-- %s -->' % (classic, MARK)
        if b not in t:
            assert t.count(a) == 1, (name, a)
            t = t.replace(a, b)
        a = '<include condition="Skin.HasSetting(aeon.fglass)">%s</include>' % fg
        b = '<include condition="Skin.HasSetting(aeon.fglass) + !$EXP[FGS]">%s</include>' % fg
        if b not in t:
            assert t.count(a) == 1, (name, a)
            t = t.replace(a, b)
        wr(name, t)
    print('windows: classic page under the Fused Glass style')


def classic():
    t = rd('Includes_Aeon_Menu.xml')
    if MARK in t:
        print('classic: already')
        return
    # the frame lines of the two classic pages
    for inc in ('SetCat_Classic', 'AddonSet_Classic'):
        i = t.index('<include name="%s">' % inc)
        j = t.index('\n\t</include>', i)
        blk = t[i:j]
        n = blk.count('<visible>!$EXP[Aeon_Fused] + !$EXP[Aeon_VGlass]</visible>')
        assert n >= 6, (inc, n)
        blk = blk.replace('<visible>!$EXP[Aeon_Fused] + !$EXP[Aeon_VGlass]</visible>', '<visible>[!$EXP[Aeon_Fused] + !$EXP[Aeon_VGlass]] | $EXP[FGS]</visible>')
        # the templates and the level button: the Fused Glass style's look
        old = '''<include content="Aeon_SettingCategoryTemplate">
				<param name="width" value="380"/>
				<param name="roundfirst" value="true"/>'''
        assert blk.count(old) == 1, inc
        blk = blk.replace(old, old + '\n\t\t\t\t<param name="fgs" value="true"/>')
        m = re.search(r'<include content="Aeon_SettingTemplates">\s*<param name="width" value="(\d+)"/>', blk)
        assert m, inc
        blk = blk[:m.end()] + '\n\t\t\t\t<param name="fgs" value="true"/><param name="pre" value="FGS_"/>' + blk[m.end():]
        t = t[:i] + blk + t[j:]
    # the category template
    i = t.index('<include name="Aeon_SettingCategoryTemplate">')
    j = t.index('\n\t</include>', i)
    blk = t[i:j]
    blk = blk.replace('<param name="roundfirst">false</param>', '<param name="roundfirst">false</param>\n\t\t<param name="fgs">false</param>', 1)
    blk = blk.replace('<focusedcolor>$VAR[Aeon_CatFocInk]</focusedcolor>', '<focusedcolor>$VAR[FGS_Aeon_CatFocInk]</focusedcolor>')
    blk = blk.replace('<selectedcolor>$VAR[Aeon_CatSelInk]</selectedcolor>', '<selectedcolor>$VAR[FGS_Aeon_CatSelInk]</selectedcolor>')
    old = ('<include condition="$PARAM[roundfirst]">Aeon_TexCatFocus</include>\n\t\t\t\t<include condition="!$PARAM[roundfirst]">Aeon_TexRowFocus</include>\n'
           '\t\t\t\t<include>Aeon_TexCatNoFocus</include>')
    assert blk.count(old) == 1
    blk = blk.replace(old, '<include condition="$PARAM[fgs] + $EXP[FGS]">FGS_RowTex</include>\n'
                      '\t\t\t\t<include condition="$PARAM[roundfirst] + ![$PARAM[fgs] + $EXP[FGS]]">Aeon_TexCatFocus</include>\n'
                      '\t\t\t\t<include condition="!$PARAM[roundfirst] + ![$PARAM[fgs] + $EXP[FGS]]">Aeon_TexRowFocus</include>\n'
                      '\t\t\t\t<include condition="![$PARAM[fgs] + $EXP[FGS]]">Aeon_TexCatNoFocus</include>')
    t = t[:i] + blk + t[j:]
    # the setting row and the templates
    i = t.index('<include name="Aeon_SettingRow">')
    j = t.index('\n\t</include>', i)
    blk = t[i:j]
    blk = blk.replace('<param name="font">st_ui_24_semibold</param>', '<param name="font">st_ui_24_semibold</param>\n\t\t<param name="fgs">false</param>\n\t\t<param name="pre"></param>', 1)
    blk = blk.replace('<focusedcolor>$VAR[Aeon_OnBarInk]</focusedcolor>', '<focusedcolor>$VAR[$PARAM[pre]Aeon_OnBarInk]</focusedcolor>')
    old = '<include>Aeon_TexRowFocus</include>\n\t\t\t<include>Aeon_TexRowNoFocus</include>'
    assert blk.count(old) == 1
    blk = blk.replace(old, '<include condition="$PARAM[fgs] + $EXP[FGS]">FGS_RowTex</include>\n'
                      '\t\t\t<include condition="![$PARAM[fgs] + $EXP[FGS]]">Aeon_TexRowFocus</include>\n'
                      '\t\t\t<include condition="![$PARAM[fgs] + $EXP[FGS]]">Aeon_TexRowNoFocus</include>')
    t = t[:i] + blk + t[j:]
    i = t.index('<include name="Aeon_SettingTemplates">')
    j = t.index('\n\t</include>', i)
    blk = t[i:j]
    blk = blk.replace('<param name="width">1058</param>', '<param name="width">1058</param>\n\t\t<param name="fgs">false</param>\n\t\t<param name="pre"></param>', 1)
    blk = blk.replace('<include content="Aeon_SettingRow"><param name="width" value="$PARAM[width]"/></include>',
                      '<include content="Aeon_SettingRow"><param name="width" value="$PARAM[width]"/><param name="fgs" value="$PARAM[fgs]"/><param name="pre" value="$PARAM[pre]"/></include>')
    for v in ('Aeon_OnBarInk', 'Aeon_OnBarInk2', 'Aeon_OnBarInk3', 'Aeon_OnBarIcon', 'Aeon_OnBarFill', 'Aeon_OnBarTrack', 'Aeon_OnBarLine', 'Aeon_SegSelTxt', 'Aeon_SegUnselF'):
        blk = blk.replace('$VAR[%s]' % v, '$VAR[$PARAM[pre]%s]' % v)
    # a template's own focus texture (the slider row): the bar too
    blk = blk.replace('\t\t\t\t<include>Aeon_TexRowFocus</include>', '\t\t\t\t<include condition="$PARAM[fgs] + $EXP[FGS]">FGS_RowTex</include>\n'
                      '\t\t\t\t<include condition="![$PARAM[fgs] + $EXP[FGS]]">Aeon_TexRowFocus</include>')
    t = t[:i] + blk + t[j:]
    # the open category's grey overlay: off under the Fused Glass style (Kodi's faded bar marks it)
    i = t.index('<include name="Aeon_CatParentBars">')
    j = t.index('\n\t</include>', i)
    blk = t[i:j]
    k = blk.count('+ !Container(3).HasPrevious</visible>')
    blk = blk.replace('+ !Container(3).HasPrevious</visible>', '+ !Container(3).HasPrevious + !$EXP[FGS]</visible>')
    t = t[:i] + blk + t[j:]
    t = t.replace('\t<include name="Aeon_SettingCategoryTemplate">', '\t<!-- %s: the classic pages take params fgs / pre under the Fused Glass style -->\n'
                  '\t<include name="Aeon_SettingCategoryTemplate">' % MARK, 1)
    wr('Includes_Aeon_Menu.xml', t)
    print('classic: templates, parent bars %d' % k)
    # the level button
    s = rd('Includes_Settings.xml')
    if 'FGS_RowTex' not in s:
        VG = 'Skin.HasSetting(aeon.vglass) + !Skin.HasSetting(aeon.fglass) + !String.IsEqual(Skin.String(aeon.menutheme),fused)'
        old = ('<include condition="![$PARAM[round] + %s]">AG_LevelTexPlain</include>' % VG)
        assert s.count(old) == 1
        s = s.replace(old, '<include condition="![$PARAM[round] + %s] + ![$PARAM[round] + $EXP[FGS]]">AG_LevelTexPlain</include>\n'
                      '\t\t\t\t<include condition="$PARAM[round] + $EXP[FGS]">FGS_RowTex</include>' % VG)
        i = s.index('<include name="AG_SettingLevelButton">')
        j = s.index('\n\t</include>', i)
        blk = s[i:j].replace('<focusedcolor>$VAR[Aeon_OnBarInk]</focusedcolor>', '<focusedcolor>$VAR[FGS_Aeon_OnBarInk]</focusedcolor>')
        s = s[:i] + blk + s[j:]
        wr('Includes_Settings.xml', s)
    # the category inks' twins
    f = rd('Includes_Fused.xml')
    if 'name="FGS_Aeon_CatFocInk"' not in f:
        f = f.replace('</includes>', ''.join('\t<variable name="FGS_%s">\n\t\t<value condition="$EXP[FGS]">ffffffff</value>\n\t\t<value>$VAR[%s]</value>\n\t</variable>\n' % (v, v)
                                             for v in ('Aeon_CatFocInk', 'Aeon_CatSelInk')) + '</includes>')
        wr('Includes_Fused.xml', f)


if __name__ == '__main__':
    skin_settings()
    windows()
    classic()
