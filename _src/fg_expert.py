# -*- coding: utf-8 -*-
"""0.56.28 Expert settings: the panel fills and the fanart alpha at five steps of opacity (and the fills at five steps
of tint). Used by fg_material.py (panel fills, FG_MATERIAL block) and expert_05628.py (fanart alpha).

A variable keeps its own values; a first value hands over to its twin <name>X while an expert step is set, and the
twin holds every step for every original value (Kodi takes the first value whose condition is true), so with the
defaults nothing extra is evaluated past that first line."""
import re

STEPS = ('m2', 'm1', '', 'p1', 'p2')
OPACITY = {'m2': 0.6, 'm1': 0.8, '': 1.0, 'p1': 1.2, 'p2': 1.4}
FROSTED = (214, 220, 232)            # the light frost the tint moves toward


def sval(setting, v):
    return 'String.IsEmpty(Skin.String(%s))' % setting if not v else 'String.IsEqual(Skin.String(%s),%s)' % (setting, v)


def adjust(hexcol, op='', tint=''):
    a, r, g, b = (int(hexcol[i:i + 2], 16) for i in (0, 2, 4, 6))
    a = min(255, int(round(a * OPACITY[op])))
    if tint in ('m2', 'm1'):
        f = 0.45 if tint == 'm2' else 0.7
        r, g, b = (int(round(c * f)) for c in (r, g, b))
    elif tint in ('p1', 'p2'):
        f = 0.18 if tint == 'p1' else 0.36
        r, g, b = (int(round(c + (t - c) * f)) for c, t in zip((r, g, b), FROSTED))
    return '%02x%02x%02x%02x' % (a, r, g, b)


def values(var_text):
    """[(condition or None, value)] of a <variable> block"""
    return [(m.group(1), m.group(2)) for m in re.finditer(r'<value(?: condition="([^"]*)")?>([^<]*)</value>', var_text)]


def expressions(prefix, op_setting, tint_setting=None):
    """the step expressions <prefix>_<op><tint> and <prefix>_On"""
    out = []
    combos = []
    for op in STEPS:
        for tint in (STEPS if tint_setting else ('',)):
            if not op and not tint:
                continue
            name = '%s_%s%s' % (prefix, op or 'd', ('_' + (tint or 'd')) if tint_setting else '')
            cond = sval(op_setting, op) + ((' + ' + sval(tint_setting, tint)) if tint_setting else '')
            out.append('\t<expression name="%s">%s</expression>\n' % (name, cond))
            combos.append((name, op, tint))
    on = '!String.IsEmpty(Skin.String(%s))' % op_setting + ((' | !String.IsEmpty(Skin.String(%s))' % tint_setting) if tint_setting else '')
    out.append('\t<expression name="%s_On">%s</expression>\n' % (prefix, on))
    return ''.join(out), combos


def expand(text, names, prefix, combos):
    """each named variable in text gets a first value that hands over to its twin <name>X, and the twin"""
    twins = []
    for name in names:
        m = re.search(r'\t<variable name="%s">\n(.*?)\t</variable>\n' % re.escape(name), text, re.S)
        assert m, name
        body = m.group(1)
        if '$VAR[%sX]' % name in body:
            continue
        vals = values(body)
        lines = []
        for exp, op, tint in combos:
            for cond, val in vals:
                if not re.fullmatch(r'[0-9a-fA-F]{8}', val):
                    continue
                c = '$EXP[%s]' % exp + (' + [%s]' % cond if cond else '')
                lines.append('\t\t<value condition="%s">%s</value>\n' % (c, adjust(val.lower(), op, tint)))
        default = [v for c, v in vals if not c]
        lines.append('\t\t<value>%s</value>\n' % (default[-1] if default else vals[-1][1]))   # not reached: a step is set
        twins.append('\t<variable name="%sX">\n%s\t</variable>\n' % (name, ''.join(lines)))
        new_body = '\t\t<value condition="$EXP[%s_On]">$VAR[%sX]</value>\n' % (prefix, name) + body
        text = text[:m.start(1)] + new_body + text[m.end(1):]
    return text, ''.join(twins)
