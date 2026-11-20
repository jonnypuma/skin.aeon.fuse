# -*- coding: utf-8 -*-
"""0.56.20 the Fuse menu theme survey (board https://claude.ai/artifact/VYbR9x9VrGpYHHQTowqYi4), the user: "fix all of
them and in accordance with my comments in the survey". This pass:

a) Aeon + Fuse kept Aeon's square parts inside its rounded cards (dialog buttons, outlined rows and chips, pills, the
   primary / outline buttons, the information page's flags). Every skin-load switch that picks a rounded texture for
   Aeon Glass (Skin.HasSetting(aeon.vglass)) and a square one for Aeon gets a third branch for Aeon + Fuse: Aeon Glass's
   texture and border (the shape) with Aeon's colours (<name>_fu). Fuse needs Kodi to start again, so a skin-load
   condition is right;
b) context menu: Aeon + Fuse focuses a 12 px rounded bar (the card is r28 and the rows sit 16 px in: concentric);
   Aeon Glass + Fuse insets its rows like Fused Glass (6 px in, 12 px narrower, the rounded row pill) on Aeon Glass's
   r22 panel; in Aeon Glass the focused row's text is dark (it was white on the solid white bar);
c) Aeon Glass: the media chips on the information page are rounded (8 px) like its other parts;
d) Aeon + Fuse: the information page's poster takes the rounded mask (VidView_ArtImage gets a "round" parameter; the
   library views keep Aeon's plain rectangle);
e) Aeon + Fuse: the settings level button (Basic / Expert) is a rounded box.
Runs once (marker)."""
import io
import os
import re
import xml.etree.ElementTree as ET

D = '1080i'
MARK = '0.56.20 fuse_survey'
FUSED = '$EXP[Aeon_Fused]'


def rd(f):
    return io.open(os.path.join(D, f), encoding='utf-8').read()


def wr(f, t):
    io.open(os.path.join(D, f), 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(os.path.join(D, f))


def swap(t, old, new, count=1):
    n = t.count(old)
    assert n == count, (old[:140], n, count)
    return t.replace(old, new)


def fuse_variants(files):
    """a) the rounded-shape branch for Aeon + Fuse in every vglass / !vglass texture switch whose shapes differ"""
    defs = {}
    for f, t in files.items():
        for m in re.finditer(r'<include name="([^"]+)">(.*?)</include>', t, re.S):
            defs.setdefault(m.group(1), (f, m.group(2)))
    done = []
    for f in list(files):
        t = files[f]
        for m in list(re.finditer(r'(\t*)<include name="([^"]+)">(\s*(?:<include condition="[^"]*">[^<]+</include>\s*)+)</include>', t)):
            indent, name, body = m.group(1), m.group(2), m.group(3)
            conds = re.findall(r'<include condition="([^"]*)">([^<]+)</include>', body)
            g = [n for c, n in conds if c.strip() == 'Skin.HasSetting(aeon.vglass)' or c.strip().startswith('Skin.HasSetting(aeon.vglass) + !')]
            fl = [(c, n) for c, n in conds if c.strip() == '!Skin.HasSetting(aeon.vglass)']
            if not g or not fl or g[0] not in defs or fl[0][1] not in defs:
                continue
            gbody, fbody = defs[g[0]][1], defs[fl[0][1]][1]
            tg = re.findall(r'>([^<>\s]+\.png)<', gbody)
            tf = re.findall(r'>([^<>\s]+\.png)<', fbody)
            if tg == tf:
                continue
            # Aeon Glass's texture elements, each with the colour of the same element in Aeon's variant
            fcol = dict(re.findall(r'<(texture\w*)[^>]*colordiffuse="([^"]*)"', fbody))
            fu = re.sub(r'<(texture\w*)([^>]*?)colordiffuse="[^"]*"',
                        lambda mm: '<%s%scolordiffuse="%s"' % (mm.group(1), mm.group(2), fcol.get(mm.group(1), 'ffffffff')), gbody)
            fu_name = fl[0][1].rsplit('_', 1)[0] + '_fu' if fl[0][1].endswith('_f') else fl[0][1] + '_fu'
            new_body = body.replace('<include condition="!Skin.HasSetting(aeon.vglass)">%s</include>' % fl[0][1],
                                    '<include condition="!Skin.HasSetting(aeon.vglass) + !%s">%s</include>%s\t<include condition="!Skin.HasSetting(aeon.vglass) + %s">%s</include>'
                                    % (FUSED, fl[0][1], '\n' + indent, FUSED, fu_name), 1)
            block = '%s<include name="%s">%s</include>' % (indent, name, new_body)
            fu_def = '%s<!-- %s: Aeon + Fuse: %s\'s shape, %s\'s colours -->\n%s<include name="%s">%s</include>\n' % (indent, MARK, g[0], fl[0][1], indent, fu_name, fu)
            t = t.replace(m.group(0), fu_def + block, 1)
            done.append(name)
        files[f] = t
    return done


def ctx(dlg, fused):
    """b) the context menu rows"""
    dlg = swap(dlg, '\t\t\t\t\t<animation effect="slide" end="6,0" time="0" condition="$EXP[Aeon_FGlass]">Conditional</animation>\n\t\t\t\t\t<description>grouplist for context buttons</description>',
               '\t\t\t\t\t<animation effect="slide" end="6,0" time="0" condition="$EXP[Ctx_PillRows]">Conditional</animation><!-- %s: also Aeon Glass + Fuse -->\n\t\t\t\t\t<description>grouplist for context buttons</description>' % MARK)
    dlg = swap(dlg, '<include condition="$EXP[Aeon_FGlass]">Ctx_RowW_fg</include><include condition="!$EXP[Aeon_FGlass]">Ctx_RowW</include>',
               '<include condition="$EXP[Ctx_PillRows]">Ctx_RowW_fg</include><include condition="!$EXP[Ctx_PillRows]">Ctx_RowW</include><include condition="Skin.HasSetting(aeon.vglass) + !Skin.HasSetting(aeon.fglass)">Ctx_InkGlass</include>', 2)
    dlg = swap(dlg, '\t<include name="Ctx_RowW"><width>560</width></include>',
               '\t<!-- %s: the rows of Fused Glass (inset pill) for Aeon Glass + Fuse too; Aeon Glass\'s focused text dark on its white bar -->\n'
               '\t<expression name="Ctx_PillRows">$EXP[Aeon_FGlass] | [Skin.HasSetting(aeon.vglass) + %s]</expression>\n'
               '\t<include name="Ctx_InkGlass"><focusedcolor>aeon_onbar</focusedcolor></include>\n'
               '\t<include name="Ctx_RowW"><width>560</width></include>' % (MARK, FUSED))
    fused = swap(fused, '\t<include name="FG_CtxRowTex">\n\t\t<include condition="Skin.HasSetting(aeon.fglass)">FG_CtxRowTex_fg</include>\n\t\t<include condition="!Skin.HasSetting(aeon.fglass)">FG_CtxRowTex_old</include>\n\t</include>',
                 '\t<!-- %s: Aeon + Fuse: a 12 px rounded bar, concentric with the r28 card (rows 16 px in); Aeon Glass + Fuse: the inset pill -->\n'
                 '\t<include name="FG_CtxRowTex_fu"><texturefocus border="12" colordiffuse="aeon_white">fg/r12.png</texturefocus></include>\n'
                 '\t<include name="FG_CtxRowTex">\n'
                 '\t\t<include condition="Skin.HasSetting(aeon.fglass) | [Skin.HasSetting(aeon.vglass) + %s]">FG_CtxRowTex_fg</include>\n'
                 '\t\t<include condition="!Skin.HasSetting(aeon.vglass) + %s">FG_CtxRowTex_fu</include>\n'
                 '\t\t<include condition="!Skin.HasSetting(aeon.fglass) + !%s">FG_CtxRowTex_old</include>\n\t</include>' % (MARK, FUSED, FUSED, FUSED))
    return dlg, fused


def main():
    names = sorted(f for f in os.listdir(D) if f.endswith('.xml'))
    files = {f: rd(f) for f in names}
    if any(MARK in t for t in files.values()):
        print('already')
        return
    done = fuse_variants(files)
    print('a) Fuse variants for', len(done), done)
    files['Includes_Dialogs.xml'], files['Includes_Fused.xml'] = ctx(files['Includes_Dialogs.xml'], files['Includes_Fused.xml'])
    # c) Aeon Glass's media chips rounded
    files['Includes_Fused.xml'] = swap(files['Includes_Fused.xml'], '<include name="FG_ChipTex_old"><texturenofocus border="10" colordiffuse="44ffffff">common/rect_square.png</texturenofocus></include>',
                                       '<include name="FG_ChipTex_old"><texturenofocus border="8" colordiffuse="44ffffff">fg/r8.png</texturenofocus></include><!-- %s: rounded in Aeon Glass -->' % MARK)
    vi = files['Includes_VideoInfo.xml']
    n = vi.count('<texturefocus border="10" colordiffuse="55ffffff">common/rect_square.png</texturefocus><include>FG_ChipTex</include>')
    vi = vi.replace('<texturefocus border="10" colordiffuse="55ffffff">common/rect_square.png</texturefocus><include>FG_ChipTex</include>',
                    '<texturefocus border="8" colordiffuse="55ffffff">fg/r8.png</texturefocus><include>FG_ChipTex</include>')
    print('c) chips', n)
    # d) the information page's poster rounded in Aeon + Fuse
    vv = files['Includes_Views_Video.xml']
    vv = swap(vv, '\t\t<param name="fade">0</param>\n\t\t<definition>\n\t\t\t<control type="image">\n\t\t\t\t<left>0</left>',
              '\t\t<param name="fade">0</param>\n\t\t<param name="round">Skin.HasSetting(aeon.vglass)</param><!-- %s: the information page passes Aeon + Fuse too -->\n\t\t<definition>\n\t\t\t<control type="image">\n\t\t\t\t<left>0</left>' % MARK)
    vv = swap(vv, '<visible>$PARAM[visible] + !ListItem.IsParentFolder + Skin.HasSetting(aeon.vglass)</visible>\n\t\t\t</control>\n\t\t\t<!-- masked in Glass (above), a plain rectangle in Aeon -->',
              '<visible>$PARAM[visible] + !ListItem.IsParentFolder + [$PARAM[round]]</visible>\n\t\t\t</control>\n\t\t\t<!-- masked in Glass (above), a plain rectangle in Aeon -->')
    vv = swap(vv, '<visible>$PARAM[visible] + !ListItem.IsParentFolder + !Skin.HasSetting(aeon.vglass)</visible>\n\t\t\t</control>\n\t\t</definition>\n\t</include>',
              '<visible>$PARAM[visible] + !ListItem.IsParentFolder + ![$PARAM[round]]</visible>\n\t\t\t</control>\n\t\t</definition>\n\t</include>')
    files['Includes_Views_Video.xml'] = vv
    vi = swap(vi, '\t\t\t\t\t<param name="art" value="$VAR[VidInfo_Poster]"/>\n\t\t\t\t\t<param name="mask" value="aeon/mask_poster_info.png"/>',
              '\t\t\t\t\t<param name="art" value="$VAR[VidInfo_Poster]"/>\n\t\t\t\t\t<param name="round" value="Skin.HasSetting(aeon.vglass) | %s"/>\n\t\t\t\t\t<param name="mask" value="aeon/mask_poster_info.png"/>' % FUSED)
    files['Includes_VideoInfo.xml'] = vi
    # e) the level button (Basic / Expert) rounded in Aeon + Fuse
    f = [k for k, t in files.items() if '<include name="AG_SettingLevelButton">' in t][0]
    t = files[f]
    a = t.index('<include name="AG_SettingLevelButton">')
    b = t.index('</definition>', a)
    s = swap(t[a:b], '<texturenofocus colordiffuse="$VAR[Aeon_LevelCol]">common/white.png</texturenofocus>',
             '<texturenofocus border="12" colordiffuse="$VAR[Aeon_LevelCol]">$VAR[Aeon_FuseBox12]</texturenofocus>')
    files[f] = t[:a] + s + t[b:]
    g = files['Includes_Aeon_Glass.xml']
    g = swap(g, '\t<variable name="Aeon_MenuTexPill">',
             '\t<!-- %s: a plain box, rounded (12 px) with the Fuse menu theme -->\n\t<variable name="Aeon_FuseBox12">\n\t\t<value condition="$EXP[Aeon_Fused]">fg/r12.png</value>\n\t\t<value>common/white.png</value>\n\t</variable>\n\t<variable name="Aeon_MenuTexPill">' % MARK)
    files['Includes_Aeon_Glass.xml'] = g
    changed = 0
    for k, t in files.items():
        if t != rd(k):
            wr(k, t)
            changed += 1
    print('files changed', changed)


if __name__ == '__main__':
    main()
