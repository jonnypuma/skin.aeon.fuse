"""0.56.50 the skin's version on the start-up splash (the user, 2026-11-18: "we should have Skin version number on the
splash screen"): "v0.56.50" in the bottom right corner, on the hint's line (OK or Back skips), dimmer than the hint.
In Aeon_SplashFront, so Startup.xml (the first frame) and Home's splash both show it; System.AddonVersion is read from
the add-on list in memory (no library check, see startup_05649.py). Run from the skin folder. Repeatable."""
import io
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'Includes_Fused.xml')
MARK = '<!-- 0.56.50 splash version -->'
HINT = ('\t\t\t<control type="label"><left>0</left><top>1000</top><width>1920</width><height>34</height><align>center</align>'
        '<aligny>center</aligny><font>hm_ui_20</font><textcolor>66ffffff</textcolor><label>$ADDON[skin.aeon.fuse 32624]</label></control>\n')
VER = ('\t\t\t' + MARK + '<control type="label"><left>1260</left><top>1000</top><width>600</width><height>34</height><align>right</align>'
       '<aligny>center</aligny><font>hm_ui_20</font><textcolor>4dffffff</textcolor>'
       '<label>$INFO[System.AddonVersion(skin.aeon.fuse),v]</label></control>\n')


def main():
    t = io.open(P, encoding='utf-8').read()
    if MARK in t:
        print('splashver: already there')
        return
    s = t.index('\t<include name="Aeon_SplashFront">')
    e = t.index('\t</include>\n', s)
    i = t.index(HINT, s, e) + len(HINT)
    t = t[:i] + VER + t[i:]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    print('splashver: the version on the splash')


if __name__ == '__main__':
    main()
