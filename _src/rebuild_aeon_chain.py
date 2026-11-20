"""Restore Includes_Aeon_Video.xml / Includes_Aeon_Views2.xml (and Views3 / MusicLib when backed up) from
backups/pre05613 and run the 0.56.13+ Aeon view generators in order. Prints a diff summary against the files before."""
import difflib
import io
import os
import shutil
import subprocess
import sys

SKIN = r'C:\Users\gideo\AppData\Roaming\Kodi\addons\skin.aeon.fuse'
BK = r'C:\Users\gideo\AppData\Roaming\Kodi\backups\pre05613'
SP = os.path.dirname(os.path.abspath(__file__))
FILES = [f for f in ('Includes_Aeon_Video.xml', 'Includes_Aeon_Views2.xml', 'Includes_Aeon_Views3.xml', 'Includes_Aeon_MusicLib.xml', 'Includes_Aeon_Sub.xml')
         if os.path.exists(os.path.join(BK, f))]
GENS = ['aeon_lib510', 'aeon_lib511', 'aeon_lib_lists', 'aeon_lib_lists2', 'aeon_lib522', 'aeon_lib_walls'] + \
       [g for g in ('aeon_lib_music', 'aeon_lib_other', 'aeon_lib_round2', 'views_05615', 'aeon_lib_round2b', 'aeon_lib_round3', 'aeon_lib_round4', 'aeon_lib_round5', 'aeon_lib_round6', 'aeon_lib_round7', 'aeon_lib_round8', 'rename_aeonglass_05618', 'sets_05648') if os.path.exists(os.path.join(SKIN, '_src', g + '.py'))]
before = {f: io.open(os.path.join(SKIN, '1080i', f), encoding='utf-8').read() for f in FILES}
for f in FILES:
    shutil.copy(os.path.join(BK, f), os.path.join(SKIN, '1080i', f))
for g in GENS:
    r = subprocess.run([sys.executable, os.path.join('_src', g + '.py')], cwd=SKIN, capture_output=True, text=True)
    print(g, (r.stdout + r.stderr).strip().splitlines()[-1:] if (r.stdout + r.stderr).strip() else '')
    if r.returncode:
        print(r.stderr)
        sys.exit(1)
for f in FILES:
    after = io.open(os.path.join(SKIN, '1080i', f), encoding='utf-8').read()
    d = [l for l in difflib.unified_diff(before[f].split('\n'), after.split('\n'), lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++', '---')]
    print(f, 'changed lines:', len(d))
    for l in d[:int(sys.argv[1]) if len(sys.argv) > 1 else 6]:
        print('   ', l[:220])
