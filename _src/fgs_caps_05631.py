"""0.56.31 Fused Glass style: capitals in the settings lists, like the mockup (categories, row names, Kodi's values).

Kodi's own setting rows (Kodi settings, add-on settings) get their text from Kodi, so an [UPPERCASE] tag in the skin
cannot reach them. The style therefore switches the list fonts to uppercase twins uc_st_<font>: the settings face with
<style>uppercase</style> added. The HELPER writes them (script.aeon.helper 0.3.106 fonts.CAPS) inside its generated
section block of Font.xml, in every font set, so they follow the settings font choice; a twin written by hand into
that block is wiped at the next start (the helper rebuilds the block). Skin settings use the same twins.

Scope (all only under the style, $EXP[FGS]; the other styles and themes keep their fonts):
  Kodi / add-on settings: category list, rows (label and value), group headings, level button, add-on OK buttons;
  Skin settings: category list, row names (Dlg_SkinRowChrome), the inline sub-section rows (66 px, 20 labels).

Run from the skin folder after fgs_round2_05630: python _src/fgs_caps_05631.py (XML only; Font.xml is the helper's)."""
import io
import os
import re

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
TWINS = ['st_ui_24', 'st_ui_24_semibold', 'st_ui_24_bold', 'st_small_20_semibold']


def rd(name):
    return io.open(os.path.join(D, name), encoding='utf-8').read()


def wr(name, text):
    io.open(os.path.join(D, name), 'w', encoding='utf-8', newline='\n').write(text)


def pair(cond, plain, caps):
    """Two load-time includes: caps under the condition, the old font otherwise."""
    return ('<include content="Param_F" condition="%s"><param name="f" value="%s"/></include>'
            '<include content="Param_F" condition="![%s]"><param name="f" value="%s"/></include>' % (cond, caps, cond, plain))


def sub_in(text, start_pat, end_pat, old, new, count):
    """Replace old by new count times inside the first block from start_pat to end_pat."""
    s = text.index(start_pat)
    e = text.index(end_pat, s)
    block = text[s:e]
    assert block.count(old) == count, (start_pat, old, block.count(old))
    return text[:s] + block.replace(old, new) + text[e:]


def xml():
    # Includes_Aeon_Menu.xml: Param_F + Kodi / add-on settings templates
    t = rd('Includes_Aeon_Menu.xml')
    if 'name="Param_F"' not in t:
        a = '<include name="Param_H">'
        t = t.replace(a, '<include name="Param_F"><param name="f">st_ui_24</param><definition><font>$PARAM[f]</font></definition></include>\n\t' + a, 1)
        fg = '$PARAM[fgs] + $EXP[FGS]'
        t = sub_in(t, '<include name="Aeon_SettingRow">', '</include>\n\t<include name="Aeon_SettingTemplates">',
                   '<font>$PARAM[font]</font>', pair(fg, '$PARAM[font]', 'uc_st_ui_24_semibold'), 1)
        t = sub_in(t, '<include name="Aeon_SettingTemplates">', '<include name="Aeon_AddonSetButton">',
                   '<font>st_ui_24_bold</font>', pair(fg, 'st_ui_24_bold', 'uc_st_ui_24_bold'), 1)
        t = sub_in(t, '<include name="Aeon_AddonSetButton">', '</include>',
                   '<font>st_ui_24_semibold</font>', pair('$EXP[FGS]', 'st_ui_24_semibold', 'uc_st_ui_24_semibold'), 1)
        t = sub_in(t, '<include name="Aeon_SettingCategoryTemplate">', '<!-- Left settings strip',
                   '<font>st_ui_24_bold</font>', pair(fg, 'st_ui_24_bold', 'uc_st_ui_24_bold'), 1)
        wr('Includes_Aeon_Menu.xml', t)
        print('Includes_Aeon_Menu.xml done')

    # Includes_Settings.xml: level button, Skin settings categories and row names
    t = rd('Includes_Settings.xml')
    if 'uc_st_' not in t:
        t = sub_in(t, '<include name="AG_SettingLevelButton">', '</definition>',
                   '<font>st_small_20_semibold</font>', pair('$EXP[FGS]', 'st_small_20_semibold', 'uc_st_small_20_semibold'), 1)
        for name, n_b, n_s in (('Dlg_SkinCategory', 2, 1), ('Dlg_SkinRowChrome', 1, 3)):
            start = '<include name="%s">' % name
            t = sub_in(t, start, '</definition>', '<font>st_ui_24_bold</font>',
                       pair('$EXP[FGS]', 'st_ui_24_bold', 'uc_st_ui_24_bold'), n_b)
            t = sub_in(t, start, '</definition>', '<font>st_ui_24_semibold</font>',
                       pair('$EXP[FGS]', 'st_ui_24_semibold', 'uc_st_ui_24_semibold'), n_s)
        wr('Includes_Settings.xml', t)
        print('Includes_Settings.xml done')

    # SkinSettings.xml: the inline 66 px sub-section rows (Home menu items etc.)
    t = rd('SkinSettings.xml')
    if 'uc_st_' not in t:
        lead = '<left>16</left><top>0</top><width>360</width><height>66</height><aligny>center</aligny>'
        n = 0
        for f in ('st_ui_24_semibold', 'st_ui_24_bold'):
            old = lead + '<font>%s</font>' % f
            n += t.count(old)
            t = t.replace(old, lead + pair('$EXP[FGS]', f, 'uc_' + f))
        assert n == 20, n
        wr('SkinSettings.xml', t)
        print('SkinSettings.xml done (%d labels)' % n)


if __name__ == '__main__':
    xml()
