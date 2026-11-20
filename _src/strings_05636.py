"""0.56.36 short format names everywhere (the user, 2026-11-17: "Yes, short everywhere"): the long names some places
used (spotlights, two library views, the info page) become the short ones the rest of the skin shows. Each string
below is used only for its codec (checked: every use is a test of that codec). Brand names: the same in all 23
languages. Upper case where the string was upper case. Repeatable."""
import io
import os
import re

L = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'language')
SHORT = {
    31421: 'DD+ ATMOS',        # was DOLBY DIGITAL PLUS ATMOS (spotlights)
    31422: 'DTS-HD MA',        # was DTS-HD MASTER AUDIO
    31423: 'DTS-HD HRA',       # was DTS-HD HIGH RES
    31425: 'DD+',              # was DOLBY DIGITAL PLUS
    31426: 'DD',               # was DOLBY DIGITAL
    31445: 'DD+ ATMOS',        # was DOLBY ATMOS (two views, for eac3_ddp_atmos)
    31448: 'DD+',              # was DOLBY DIGITAL+
    31631: 'DD',               # was Dolby Digital (information page)
}
for d in sorted(os.listdir(L)):
    p = os.path.join(L, d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    en = d == 'resource.language.en_gb'
    for sid, text in SHORT.items():
        pat = re.compile(r'(msgctxt "#%d"\nmsgid ")(.*)("\nmsgstr ")(.*)(")' % sid)
        m = pat.search(t)
        assert m, (d, sid)
        t = t[:m.start()] + m.group(1) + text + m.group(3) + ('' if en else text) + m.group(5) + t[m.end():]
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('done', len(os.listdir(L)), 'languages')
