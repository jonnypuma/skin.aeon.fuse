# -*- coding: utf-8 -*-
"""0.56.53 no random fanart behind a library item that has none (user, 2026-11-20, on a leftover "Aliens" whose file is
gone and which has no fanart: "why are we showing a random fanart for an item which is not in the library anymore
though. should show a neutral background"). The library ground (AG_Background_L) carried the general backdrop - the
helper's random pick from its pool (aeon.bgfan, the settings screens' picture); the Fused Glass views draw the item's own
fanart (or the neutral / colour look of Library background) over it, so it only showed where an item had no fanart.
In Fused Glass the library ground no longer carries it: an item without fanart stands on the neutral ground. Aeon
Glass unchanged. Repeatable."""
import io
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'Includes_Common.xml')


def main():
    t = io.open(P, encoding='utf-8').read()
    i = t.index('<include name="AG_Background_L">')
    e = t.index('\n\t</include>', i)
    old = '<control type="group"><visible>$EXP[Aeon_VGlass]</visible><include>Aeon_Backdrop</include></control>'
    new = ('<control type="group"><visible>$EXP[Aeon_VGlass] + !$EXP[Aeon_FGlass]</visible><include>Aeon_Backdrop</include></control>'
           '<!-- 0.56.53 libneutral: no random backdrop under the Fused Glass library -->')
    seg = t[i:e]
    if old in seg and 'libneutral' not in seg:
        t = t[:i] + seg.replace(old, new, 1) + t[e:]
        io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
        print('library ground: no random backdrop in Fused Glass')
    else:
        print('already')


if __name__ == '__main__':
    main()
