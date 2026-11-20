"""0.39.7: Kodi froze (black screen, JSON-RPC dead, SSH alive) on the box right after a song was stopped (2026-11-13).
gdb: the GUI thread sat in CDirectoryProvider::IsUpdating() for a label whose skin variable tests
Container(9881).IsUpdating (CustomRow_Count1), while a JobWorker held that provider's lock in
CDirectoryProvider::OnJobComplete -> StartDirectoryJob, evaluating the list's path variable, which needed the GUI
lock (a Container / ListItem / Window info label). Lock-order deadlock inside Kodi.
Rule: never test Container(<id>).IsUpdating from a label, visibility or path the GUI thread evaluates when that list's
path is built from info labels. (Container.IsUpdating without an id asks the media window and is safe.)
- CustomRow_Count1-3: the "Loading..." step is gone (an empty row shows no count).
- Aeon_StripPath_movies / tv / music: no "!Container(9391).IsUpdating" guard (a strip may load once more).
- Classic Home empty states (9101 / 9130) and the Planner's "nothing on this day" label (9500): shown on an empty
  list after a short fade-in delay instead of the IsUpdating test.
Run in 1080i."""
import io
import re


def rw(path, fn):
    s = io.open(path, encoding='utf-8').read()
    t = fn(s)
    assert t != s, path
    io.open(path, 'w', encoding='utf-8', newline='').write(t)


def custom_rows(s):
    for n in (1, 2, 3):
        old = '<value condition="Container(988%d).IsUpdating + !Integer.IsGreater(Container(988%d).NumItems,0)">$LOCALIZE[31952]</value>' % (n, n)
        assert s.count(old) == 1, n
        s = s.replace(old, '<value condition="!Integer.IsGreater(Container(988%d).NumItems,0)"></value>' % n)
    return s


def strips(s):
    n = s.count('!Container(9391).IsUpdating + ')
    assert n >= 30, n
    return s.replace('!Container(9391).IsUpdating + ', '')


DELAY = '<animation type="Visible"><effect type="fade" start="0" end="100" delay="1200" time="200"/></animation>'


def classic_home(s):
    for cid in ('9101', '9130'):
        old = ' + !Container(%s).IsUpdating</visible>' % cid
        assert s.count(old) == 1, cid
        s = s.replace(old, '</visible>\n\t\t\t\t' + DELAY)
    return s


def planner(s):
    old = ' + !Container(9500).IsUpdating</visible>'
    assert s.count(old) == 1
    return s.replace(old, '</visible>' + DELAY)


rw('Includes_CustomRows.xml', custom_rows)
rw('Includes_Aeon_Sub.xml', strips)
rw('Includes_Home.xml', classic_home)
rw('Custom_1168_Planner.xml', planner)
left = []
import glob
for f in glob.glob('*.xml'):
    left += ['%s: %s' % (f, m) for m in re.findall(r'Container\(\d+\)\.IsUpdating', io.open(f, encoding='utf-8').read())]
print('ok; Container(<id>).IsUpdating left:', left)
