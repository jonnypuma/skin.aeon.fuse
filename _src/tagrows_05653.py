# -*- coding: utf-8 -*-
"""0.56.53 the film's version as a small outline tag right after the title in the list rows (user, 2026-11-19, "Use
B"): Fused Glass List (510) and the Aeon / Aeon Glass List row (Includes_Aeon_Video, $VAR[Aeon_Title]); not the Compact
lists (no room beside the title, user). Only rows whose film has a real version name (Kodi's
version name, not "Standard Edition" $LOCALIZE[40400] or NONE) change: their title label is hidden and a horizontal
grouplist in its place holds the title (a disabled button: Kodi sizes buttons to their text in a list row, labels
not) and the tag (a disabled button with an outline, the title's colour).
Every other row keeps its label as it was. Repeatable."""
import io
import os
import re

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
MARK = '<!-- 0.56.53 version tag -->'
TAG = ('[String.IsEqual(ListItem.DBType,movie) + !String.IsEmpty(ListItem.VideoVersionName) + '
       '!String.IsEqual(ListItem.VideoVersionName,$LOCALIZE[40400]) + !String.IsEqual(ListItem.VideoVersionName,NONE)] | '
       # the sidecar's edition for the film in focus (Lawrence of Arabia: Kodi says Standard Edition, Curator says
       # Anniversary Edition), as in the info panels (user, 2026-11-19)
       '[String.IsEqual(ListItem.DBType,movie) + Skin.HasSetting(aeon.chip.edition) + Skin.HasSetting(aeon.mi.sidecar) + '
       'String.IsEqual(Window(Home).Property(aeon.mi.path),ListItem.FileNameAndPath) + '
       '!String.IsEmpty(Window(Home).Property(aeon.mi.edition))]')
RESERVE = 210            # room the title leaves for the tag


def tag_button(h, colour, reserve=None):
    reserve = reserve or RESERVE
    top = max(0, (int(h) - 26) // 2)
    return ('<control type="button"><top>%d</top><width min="30" max="%d">auto</width><height>26</height>'
            '<label>[UPPERCASE]$VAR[Aeon_VerStat][/UPPERCASE]</label><font>lb_cap_14</font>'
            '<textcolor>{c}</textcolor><focusedcolor>{c}</focusedcolor><disabledcolor>{c}</disabledcolor>'
            '<align>center</align><aligny>center</aligny><textoffsetx>9</textoffsetx><enable>false</enable>'
            '<texturenofocus border="8" colordiffuse="{c}">fg/e8.png</texturenofocus>'
            '<texturefocus border="8" colordiffuse="{c}">fg/e8.png</texturefocus></control>'
            % (top, reserve - 12)).replace('{c}', colour)


def wrap(x, bare, reserve=None):
    reserve = reserve or RESERVE
    """the label x as it was (hidden for films with a version) + the grouplist with title and tag"""
    g = re.search(r'<left>(-?\d+)</left>\s*<top>(-?\d+)</top>\s*<width>(\d+)</width>\s*<height>(\d+)</height>', x)
    if not g:
        return None
    left, top, w, h = g.groups()
    colour = re.search(r'<textcolor>([^<]*)</textcolor>', x).group(1)
    vis = ''.join('<visible>%s</visible>' % v for v in re.findall(r'<visible>(.*?)</visible>', x, re.S))
    # the title as a button: in a list row Kodi sizes a button to its text, not a label (tried on the box)
    font = re.search(r'<font>([^<]*)</font>', x).group(1)
    inner = ('<control type="button"><width min="10" max="%d">auto</width><height>%s</height><label>%s</label>'
             '<font>%s</font><textcolor>{c}</textcolor><focusedcolor>{c}</focusedcolor><disabledcolor>{c}</disabledcolor>'
             '<align>left</align><aligny>center</aligny><textoffsetx>0</textoffsetx><enable>false</enable>'
             '<texturenofocus /><texturefocus /></control>' % (int(w) - reserve, h, bare, font)).replace('{c}', colour)
    old = x.replace('</control>', '<visible>![%s]</visible></control>' % TAG, 1) if x.rstrip().endswith('</control>') else x
    group = ('%s<control type="grouplist"><left>%s</left><top>%s</top><width>%s</width><height>%s</height>'
             '<orientation>horizontal</orientation><itemgap>12</itemgap><usecontrolcoords>true</usecontrolcoords>%s'
             '<visible>%s</visible>%s%s</control>' % (MARK, left, top, w, h, vis, TAG, inner, tag_button(h, colour, reserve)))
    return old + group


def apply(path, region, label_pat, bare, reserve=None):
    s = io.open(path, encoding='utf-8').read()
    a, b = region(s)
    seg = s[a:b]
    if MARK in seg:
        return 0
    n = 0

    def one(m):
        nonlocal n
        x = m.group(0)
        if not re.search(label_pat, x):
            return x
        y = wrap(x, bare, reserve)
        if y is None:
            return x
        n += 1
        return y
    seg = re.sub(r'<control type="label">(?:(?!<control).)*?</control>', one, seg, flags=re.S)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(s[:a] + seg + s[b:])
    return n


def include(name, list_id=None):
    def region(s):
        a = s.index('<include name="%s">' % name)
        b = s.find('<include name=', a + 10)
        b = len(s) if b < 0 else b
        if list_id:
            j = s.index('id="%s"' % list_id, a)
            k = s.index('</focusedlayout>', j)
            return j, k
        return a, b
    return region


def main():
    fused = os.path.join(D, 'Includes_Fused.xml')
    n1 = apply(fused, include('FG_V510_View', '510'),
               r'<left>22</left><top>10</top><width>820</width>[^\n]*?<label>\$INFO\[ListItem\.Label\]</label>', '$INFO[ListItem.Label]')
    n2 = 0                  # Compact list: no room for a tag beside its narrow title (user, 2026-11-19)
    video = os.path.join(D, 'Includes_Aeon_Video.xml')

    def whole(s):
        return 0, len(s)
    n3 = apply(video, whole, r'<left>140</left>\s*<top>20</top>[\s\S]*?<label>\$VAR\[Aeon_Title\]</label>',
               '[UPPERCASE]$INFO[ListItem.Label][/UPPERCASE]')
    views2 = os.path.join(D, 'Includes_Aeon_Views2.xml')
    n4 = 0                  # the Aeon compact row: no room either
    print('version tags: Fused List %d, Fused Compact list %d, Aeon List %d, Aeon single-line rows %d' % (n1, n2, n3, n4))


if __name__ == '__main__':
    main()
