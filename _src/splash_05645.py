"""0.56.45 start-up splash (the user, 2026-11-18: "it seems to only wait until Movies is done before splash screen
vanishes and it looks like tv shows or music are never loaded"): the Movies / TV shows / Music steps were also done
once the helper's preload had finished (aeon.pl.done), and the preload skipped a section the skin had armed itself
(Home opening on TV shows), so the splash could end with rows still loading. Now each row step is done when its row
has titles or the helper says that row is in (Window(Home).Property(aeon.pl.<sec>.in), helper 0.3.111); the 30 s cap
stays. Rewrites the expressions, the splash and its end timer through _src/splash_05642.py. Repeatable."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import splash_05642 as sp  # noqa: E402

ROW = 'Integer.IsGreater(Container(%d).NumItems,0) | !String.IsEmpty(Window(Home).Property(aeon.pl.%s.in))'
NEW = {'Aeon_SplMov': ROW % (9301, 'movies'), 'Aeon_SplTvs': ROW % (9302, 'tv'), 'Aeon_SplMus': ROW % (9303, 'music')}


def main():
    sp.STEPS[:] = [(n, vis, NEW.get(n, done), label) for n, vis, done, label in sp.STEPS]
    here = os.getcwd()
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    try:
        sp.main()
    finally:
        os.chdir(here)


if __name__ == '__main__':
    main()
