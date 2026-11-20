# -*- coding: utf-8 -*-
"""0.56.53 the media info written as text in the Aeon / Aeon Glass library views follows Skin settings > Information >
Media info chips part by part, like the chips (user, 2026-11-19: views that show the media info as labels with a
separator "should still use the media info chip setting"):
- Aeon_TxMedia ("TRUEHD 7.1  •  1.78:1  •  DV P7 MEL  •  4K"): the aspect ratio follows Aspect ratio (it followed
  Resolution only), the channels follow Audio channels (Aeon_TxAudio = FG_EcAudio with the channels on their switch),
  the Dolby Vision profile follows DV profile (Aeon_TxHdr = FG_L_HdrChip, plain DV when the profile is off).
- Aeon_MediaLine (the right info pane, "4K  |  HEVC  |  HDR10  |  TRUEHD  7.1 CH"): the channels follow Audio channels,
  and the sidecar values come after it ($VAR[Aeon_TxSide]); its separator is the bullet of the other views.
Run after sidetext_05653.py. Repeatable."""
import io
import os
import re

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
VIEWS2 = os.path.join(D, 'Includes_Aeon_Views2.xml')
FUSED = os.path.join(D, 'Includes_Fused.xml')
SUB = os.path.join(D, 'Includes_Aeon_Sub.xml')
VIDEO = os.path.join(D, 'Includes_Aeon_Video.xml')
MARK = '<!-- 0.56.53 text gates -->'


def var_block(s, name):
    i = s.index('<variable name="%s">' % name)
    return i, s.index('</variable>', i) + len('</variable>')


def main():
    v2 = io.open(VIEWS2, encoding='utf-8').read()
    if MARK in v2:
        print('text gates: already there')
        return
    fu = io.open(FUSED, encoding='utf-8').read()
    # Aeon_TxAudio / Aeon_TxCh: FG_EcAudio with the channels on their own switch
    a, b = var_block(fu, 'FG_EcAudio')
    audio = fu[a:b].replace('name="FG_EcAudio"', 'name="Aeon_TxAudio"').replace('$VAR[VidInfo_AudioChannels]', '$VAR[Aeon_TxCh]')
    # Aeon_TxHdr: FG_L_HdrChip with the DV profile on its switch
    a, b = var_block(fu, 'FG_L_HdrChip')
    hdr = fu[a:b].replace('name="FG_L_HdrChip"', 'name="Aeon_TxHdr"')
    first = re.search(r'<value condition="([^"]*)">', hdr)
    hdr = hdr.replace(first.group(0), '<value condition="%s + !Skin.HasSetting(aeon.hide.dvp)">' % first.group(1), 1)
    add = ('\t' + MARK + '\n\t<variable name="Aeon_TxCh"><value condition="!Skin.HasSetting(aeon.hide.channels)">'
           '$VAR[VidInfo_AudioChannels]</value></variable>\n\t' + audio + '\n\t' + hdr + '\n')
    i = v2.index('\t<variable name="Aeon_TxAspB">')
    v2 = v2[:i] + add + v2[i:]
    v2 = v2.replace('<variable name="Aeon_TxAspB"><value condition="$EXP[Aeon_TxHasRes] + !String.IsEmpty(ListItem.VideoAspect)">',
                    '<variable name="Aeon_TxAspB"><value condition="$EXP[Aeon_TxHasRes] + !Skin.HasSetting(aeon.hide.aspect) + '
                    '!String.IsEmpty(ListItem.VideoAspect)">', 1)
    v2 = v2.replace('[UPPERCASE]$VAR[FG_L_HdrChip][/UPPERCASE]</value></variable>',
                    '[UPPERCASE]$VAR[Aeon_TxHdr][/UPPERCASE]</value></variable>', 1)
    a, b = var_block(v2, 'Aeon_TxMedia')
    v2 = v2[:a] + v2[a:b].replace('$VAR[FG_EcAudio]', '$VAR[Aeon_TxAudio]').replace(
        '<value condition="$EXP[Aeon_TxHasRes] + !String.IsEmpty(ListItem.VideoAspect)">$INFO[ListItem.VideoAspect,,:1]$VAR[Aeon_TxHdrB]',
        '<value condition="$EXP[Aeon_TxHasRes] + !String.IsEmpty(ListItem.VideoAspect) + !Skin.HasSetting(aeon.hide.aspect)">'
        '$INFO[ListItem.VideoAspect,,:1]$VAR[Aeon_TxHdrB]') + v2[b:]
    io.open(VIEWS2, 'w', encoding='utf-8', newline='\n').write(v2)
    sub = io.open(SUB, encoding='utf-8').read()
    old = '$INFO[ListItem.AudioChannels,  , $ADDON[skin.aeon.fuse 32210]]</value>'
    if old in sub:
        sub = sub.replace(old, '</value>', 1)
        a, b = var_block(sub, 'Aeon_ML_Aud')
        sub = sub[:b] + ('\n\t<variable name="Aeon_ML_Ch"><value condition="!Skin.HasSetting(aeon.hide.audio) + '
                         '!Skin.HasSetting(aeon.hide.channels)">$INFO[ListItem.AudioChannels,  , $ADDON[skin.aeon.fuse 32210]]'
                         '</value></variable>') + sub[b:]
        io.open(SUB, 'w', encoding='utf-8', newline='\n').write(sub)
    vid = io.open(VIDEO, encoding='utf-8').read()
    vid = vid.replace('$VAR[Aeon_ML_Aud][/UPPERCASE]', '$VAR[Aeon_ML_Aud]$VAR[Aeon_ML_Ch]$VAR[Aeon_TxSide][/UPPERCASE]', 1)
    io.open(VIDEO, 'w', encoding='utf-8', newline='\n').write(vid)
    print('text gates: aspect, channels, DV profile; the pane line has the sidecar values')


if __name__ == '__main__':
    main()
