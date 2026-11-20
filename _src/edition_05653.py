# -*- coding: utf-8 -*-
"""0.56.53 the film's version / edition goes with its title, not with the technical media info (user, 2026-11-19):
- the name is Kodi's version name (ListItem.VideoVersionName, the user's own library versions) unless that is the
  default "Standard Edition" (or NONE); else, for the film in focus, the sidecar's edition (aeon.mi.edition) when
  Skin settings > Information > Media info chips > Version is on;
- Fused Glass: every info panel's status line starts with it ("Director's Cut  ◯ 209 min left");
  the rows of the List (510) and Compact list (524) views have it after the title;
- Aeon / Aeon Glass: the heading lines that had $INFO[...VideoVersionName,  •  ,] for every film ("Standard Edition"
  included) take the same rule;
- the edition leaves the chip rows and the media text lines of the library views (sidechips / chipline2 / sidetext
  made it a chip / a text part); the information page keeps its chip.
Run after sidechips_05653.py, chipline2_05653.py, sidetext_05653.py, textgate_05653.py (and after the view
generators, since the kickers come from them). Repeatable."""
import glob
import io
import os
import re

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
FUSED = os.path.join(D, 'Includes_Fused.xml')
VIEWS2 = os.path.join(D, 'Includes_Aeon_Views2.xml')
MARK = '<!-- 0.56.53 edition with the title -->'
MI = 'Window(Home).Property(aeon.mi.%s)'


def kodi_cond(p):
    return ('!String.IsEmpty({p}VideoVersionName) + !String.StartsWith({p}VideoVersionName,Standard) + '
            '!String.IsEqual({p}VideoVersionName,NONE)').format(p=p)


def side_cond(p):
    return ('Skin.HasSetting(aeon.chip.edition) + Skin.HasSetting(aeon.mi.sidecar) + '
            'String.IsEqual(%s,%sFileNameAndPath) + !String.IsEmpty(%s)' % (MI % 'path', p, MI % 'edition'))


def values(p, before='', after=''):
    """two <value>s: Kodi's version name, else the sidecar edition, with before / after around the name"""
    return ('<value condition="%s">%s$INFO[%sVideoVersionName]%s</value>'
            '<value condition="String.IsEqual(%sDBType,movie) + %s">%s$INFO[%s]%s</value>'
            % (kodi_cond(p), before, p, after, p, side_cond(p), before, MI % 'edition', after))


def fused():
    s = io.open(FUSED, encoding='utf-8').read()
    if MARK in s:
        return 'fused: already there'
    # the row suffix
    var = ('\t%s\n\t<variable name="FG_VerRow">%s</variable>\n' % (MARK, values('ListItem.', '  ·  ')))
    i = s.index('\t<variable name="FG_L_Kicker">')
    s = s[:i] + var + s[i:]
    # the info panels' status line (ring / tick / dot and "Unwatched", "209 min left"): the version first (user: "the
    # progress circle sits on its own row, why not have the version label in front of it")
    marks = '<!-- 0.56.53 version on the status line -->'
    n = 0

    def ins(m):
        nonlocal n
        c = m.group(1)
        n += 1
        p = 'Container(%s).ListItem.' % c
        cond = '[%s] | [String.IsEqual(%sDBType,movie) + %s]' % (kodi_cond(p), p, side_cond(p))
        return ('%s<control type="label"><width min="10" max="520">auto</width><height>32</height><aligny>center</aligny>'
                '<font>lb_ui_22_bold</font><textcolor>ffffffff</textcolor><label>$VAR[FG_Ver_%s]</label><visible>%s</visible>'
                '</control>' % (marks, c, cond)) + m.group(0)
    s = re.sub(r'<control type="group"><width>28</width><height>32</height><visible>\[\$EXP\[FG_L(\d+)_Ring\]', ins, s)
    cs = sorted(set(re.findall(r'\$VAR\[FG_Ver_(\d+)\]', s)))
    i = s.index('\t<variable name="FG_VerRow">')
    defs = '\n'.join('\t<variable name="FG_Ver_%s">%s</variable>' % (c, values('Container(%s).ListItem.' % c)) for c in cs)
    s = s[:i] + '\t' + marks + '\n' + defs + '\n' + s[i:]
    # the rows of the List and Compact list views
    r = 0
    for view, cid in (('FG_V510_View', '510'), ('FG_V524_View', '524')):
        a = s.index('<include name="%s">' % view)
        b = s.find('<include name=', a + 10)
        b = len(s) if b < 0 else b
        seg = s[a:b]
        j = seg.index('id="%s"' % cid)
        k = seg.index('</focusedlayout>', j)
        part = seg[j:k]
        r += part.count('$INFO[ListItem.Title]</label>')
        part = part.replace('$INFO[ListItem.Title]</label>', '$INFO[ListItem.Title]$VAR[FG_VerRow]</label>')
        s = s[:a] + seg[:j] + part + seg[k:] + s[b:]
    io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(s)
    return 'fused: %d status lines, %d row titles' % (n, r)


def aeon():
    s = io.open(VIEWS2, encoding='utf-8').read()
    if MARK in s:
        return 'aeon: already there'
    pfxs = sorted(set(re.findall(r'\$INFO\[((?:Container\(\d+\)\.)?ListItem\.)VideoVersionName,  •  ,\]', s)))
    vars_ = []
    for p in pfxs:
        name = 'Aeon_VerB_' + (re.sub(r'\D', '', p) or 'li')
        vars_.append('\t<variable name="%s">%s</variable>' % (name, values(p, '  •  ')))
        s = s.replace('$INFO[%sVideoVersionName,  •  ,]' % p, '$VAR[%s]' % name)
    i = s.index('\t<variable name="Aeon_TxMedia">')
    s = s[:i] + '\t' + MARK + '\n' + '\n'.join(vars_) + '\n' + s[i:]
    # the media text line: no edition part
    s = s.replace('$VAR[Aeon_TxSide_edition]', '')
    io.open(VIEWS2, 'w', encoding='utf-8', newline='\n').write(s)
    return 'aeon: %d heading prefixes' % len(pfxs)


def chips():
    """the edition chips the sidecar scripts put in the library chip rows go (the information page keeps its own)"""
    n = 0
    pat = re.compile(r'<control type="button">(?:(?!<control).)*?Skin\.HasSetting\(aeon\.chip\.edition\)\](?:(?!<control).)*?</control>',
                     re.S)
    for p in glob.glob(os.path.join(D, '*.xml')):
        if os.path.basename(p) in ('Includes_VideoInfo.xml', 'SkinSettings.xml'):
            continue
        t = io.open(p, encoding='utf-8').read()
        u, k = pat.subn(lambda m: '' if 'aeon.mi.path' in m.group(0) else m.group(0), t)
        if u != t:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(u)
            n += t.count('aeon.chip.edition)]') - u.count('aeon.chip.edition)]')
    return 'chips: %d edition chips out of the library rows' % n


def main():
    print(fused())
    print(aeon())
    print(chips())


if __name__ == '__main__':
    main()
