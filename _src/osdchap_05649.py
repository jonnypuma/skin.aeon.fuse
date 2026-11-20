"""0.56.49 Skippy's segments as chapters on the player's bar (the user, 2026-11-18: "if the file itself does not have
chapters, it should still show chapters and timeline gaps on the OSD progress bar if Skippy has identified them").

The helper (0.3.112, resources/lib/skchapters.py) turns Skippy's segment list into chapters: every segment start and
end inside the file is a cut. It publishes Window(Home).Property(aeon.sk.ranges) in Kodi's Player.Chapters form, and
aeon.sk.part / aeon.sk.count. Each bar that draws Player.Chapters as gaps (ranges controls: Aeon, Aeon Glass, Fused
Glass seek bar, Fused Glass player card, its small poster bar and its pause card) gets a twin fed by aeon.sk.ranges,
shown when the file has no chapters of its own (OSD_HasSkChapters); the "Chapter n / m" lines follow. Run from the
skin folder. Repeatable."""
import io
import os
import re

X = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
SK = 'Window(Home).Property(aeon.sk.%s)'
EXP = ('\t<expression name="OSD_HasSkChapters">!$EXP[OSD_HasChapters] + !String.IsEmpty(%s)</expression>'
       '<!-- 0.56.49 Skippy\'s segments as chapters -->\n' % (SK % 'ranges'))
RANGES = re.compile(r'<control type="ranges">.*?</control>', re.S)


def rd(name):
    return io.open(os.path.join(X, name), encoding='utf-8').read()


def wr(name, t):
    io.open(os.path.join(X, name), 'w', encoding='utf-8', newline='\n').write(t)


def expression():
    t = rd('Includes_OSD.xml')
    if 'name="OSD_HasSkChapters"' in t:
        return 0
    a = t.index('\t<expression name="OSD_HasChapters">')
    b = t.index('\n', a) + 1
    wr('Includes_OSD.xml', t[:b] + EXP + t[b:])
    return 1


def bars():
    n = 0
    for name in ('Includes_Aeon_OSD.xml', 'Includes_FusedPlayer.xml', 'Includes_OSD_Aeon.xml'):
        t = rd(name)
        out, last = [], 0
        for m in RANGES.finditer(t):
            blk = m.group(0)
            if '<info>Player.Chapters</info>' not in blk or '$EXP[OSD_HasChapters]' not in blk:
                continue
            twin = blk.replace('<info>Player.Chapters</info>', '<info>%s</info>' % (SK % 'ranges')).replace(
                '$EXP[OSD_HasChapters]', '$EXP[OSD_HasSkChapters]')
            if twin in t:
                continue
            line0 = t.rfind('\n', 0, m.start()) + 1
            indent = t[line0:m.start()]
            out.append(t[last:m.end()])
            out.append('\n' + indent + twin)
            last = m.end()
            n += 1
        if last:
            out.append(t[last:])
            wr(name, ''.join(out))
    return n


def labels():
    n = 0
    part = '$INFO[%s] / $INFO[%s]' % (SK % 'part', SK % 'count')
    for name, old in (('Includes_Aeon_OSD.xml', '<value condition="Integer.IsGreater(Player.ChapterCount,0)">[COLOR a6ffffff]$LOCALIZE[21396]:[/COLOR]  [B]$INFO[Player.Chapter] / $INFO[Player.ChapterCount][/B]</value>'),
                      ('Includes_FusedPlayer.xml', '<value condition="$EXP[OSD_HasChapters]">$LOCALIZE[21396] $INFO[Player.Chapter] / $INFO[Player.ChapterCount]</value>')):
        t = rd(name)
        if (SK % 'part') in t:
            continue
        assert t.count(old) == 1, name
        new = re.sub(r'condition="[^"]*"', 'condition="!Integer.IsGreater(Player.ChapterCount,1) + $EXP[OSD_HasSkChapters]"', old, 1)
        new = new.replace('$INFO[Player.Chapter] / $INFO[Player.ChapterCount]', part)
        line0 = t.rfind('\n', 0, t.index(old)) + 1
        indent = t[line0:t.index(old)]
        t = t.replace(old, old + '\n' + indent + new)
        wr(name, t)
        n += 1
    return n


def main():
    print('osdchap: expression %d, bars %d, labels %d' % (expression(), bars(), labels()))


if __name__ == '__main__':
    main()
