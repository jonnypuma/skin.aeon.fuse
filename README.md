# Aeon Fuse

**Project page:** [jonnypuma.github.io/#/skin.aeon.fuse](https://jonnypuma.github.io/#/skin.aeon.fuse) · **All add-ons and apps by jonnypuma:** [jonnypuma.github.io](https://jonnypuma.github.io/)

This skin is an attempt to merge the design ideas and style of Aeon 2 concept skin with design elements and ideas from the Arctic Fuse 3 skin. Work in progress.

Aeon Fuse brings together the look of Aeon 2 and ideas from Arctic Fuse (hence the name). It was called Glass Aeon up to version 0.26.0; from 0.27.0 the skin is skin.aeon.fuse and its screensaver screensaver.aeon.fuse (the helper keeps its id script.aeon.helper, the waveform visualisation visualization.aeonwave).

A Kodi skin: Glass, restyled after the Aeon 2 concept. Three looks (the solid **Aeon** theme with 51 palettes, the
frosted **Glass** theme, and **Fused Glass**, its redesign with rounded frosted panels and white focus, in progress), library views built around the Aeon 2 list and walls, a Home screen with a spotlight and
widget rows, and its own screensaver.

## Add-ons

### Aeon Fuse

| Add-on | What it does |
| --- | --- |
| `skin.aeon.fuse` — Aeon Fuse | The skin. |
| `script.aeon.helper` — Aeon Fuse Helper | Required. Library counts, ratings, artwork colours, fonts, the context menu items, the Planner list, memory hand-back on small Linux boxes, the setup wizard's finishing step. |
| `screensaver.aeon.fuse` — Aeon Fuse Screensaver | Optional. The skin's screensaver (library slides with zoom and slide, now playing). |
| `visualization.aeonwave` — Aeon Fuse Waveform Visualizer | Optional. The thin waveform on the Now playing card. Builds for Linux ARM64 / ARM 32-bit / x86-64 and Windows x64 (`aeonwave/dist/` of the source tree). |

### Required from elsewhere

| Add-on | For | Where to get it |
| --- | --- | --- |
| `script.skinvariables` (Skin Variables, 2.1.21 or newer) | The Home menu items, widget rows and submenus | Kodi repository (built in). Newer builds: jamal2362, Bald. Brings `script.module.jurialmunkey` with it. |

### Optional: each adds its feature when installed

| Add-on | Adds | Where to get it |
| --- | --- | --- |
| `plugin.video.themoviedb.helper` (TMDb Helper) | The Planner (upcoming episodes and films), online rows, extra ratings | Kodi repository (5.x); newer 6.x: jamal2362 |
| `script.embuary.helper` (Embuary Helper) | The Next up row (next episodes; without it, shows in progress) | Kodi repository |
| `script.artistslideshow` (Artist Slideshow) | Artist pictures behind Now playing | Kodi repository |
| `script.cu.lrclyrics` (CU LRC Lyrics) | Lyrics on Now playing (Lines or Words) | Kodi repository |
| `script.karmamole.helper` (KarmaMole Skin Helper) | Box colours taken from the artwork | Kodi repository, KarmaMole |
| `service.skippy` (Skippy) | Skip intro / recap / credits buttons | Skippy Repo |
| `service.trickplay` (Trickplay) | Thumbnail previews on the seek bar | Skippy Repo |
| `script.tinyppi` (TinyPPI) | The playback info button in the video controls | jamal2362 |
| `resource.images.studios.white` | Studio and network logos | Kodi repository |
| `resource.images.recordlabels.white` | Record label logos | Kodi repository |
| `resource.images.languageflags.colour` | Language flags in the video info | Kodi repository |
| `resource.fonts.copacetic` | The "Inter (Copacetic)" font set | Kodi repository |
| `resource.font.robotocjksc` | The "Roboto CJKSC" font set (Chinese / Japanese / Korean) | jamal2362 (also Bald, jurialmunkey) |
| `script.mcfontface` (McFontFace) | The "McFontface Inter / Open Sans / Lato" font sets | Not in a repository: <https://github.com/pannal/script.mcfontface/releases> |
| `visualization.waveform` (Waveform) | Kodi's own waveform, if Aeon Fuse Waveform Visualizer is not used | Kodi repository |
| `service.coreelec.settings` / `service.libreelec.settings` | The CoreELEC / LibreELEC entry in the System menu | Part of CoreELEC / LibreELEC |

### Repositories

Add one as a file source (Settings > File manager > Add source) with the address of its zip below, then
Add-ons > Install from zip file (allow unknown sources first, Settings > System > Add-ons).

| Repository | Zip |
| --- | --- |
| jamal2362 (CE-Repo) | <https://raw.githubusercontent.com/CE-Repo/repository.jamal2362/main/addons/zips/repository.jamal2362/repository.jamal2362-4.0.zip> |
| Skippy Repo (jonnypuma) | <https://raw.githubusercontent.com/jonnypuma/repository.skippyrepo/main/zips/repository.skippyrepo/repository.skippyrepo-1.0.4.zip> |
| KarmaMole's Kodi Skins | <https://karmamole.github.io/kodi-skins/repository.karmamole/repository.karmamole-1.0.6.zip> |
| Kodinerds | <https://repo.kodinerds.net/addons/repository.kodinerds/repository.kodinerds-7.0.1.9.zip> |
| jurialmunkey | <https://raw.githubusercontent.com/jurialmunkey/repository.jurialmunkey/master/repo/zips/repository.jurialmunkey/repository.jurialmunkey-3.6.zip> |
| Bald | <https://dangerouslaser.github.io/skin.bald/kodi/repository.bald/repository.bald-1.2.0.zip> |

(Versions of 12 November 2026; a repository updates itself once installed.)

## Languages

English plus 22 translations: German, French, Spanish, Italian, Dutch, Portuguese (Portugal and Brazil), Swedish,
Norwegian Bokmål, Danish, Finnish, Polish, Czech, Hungarian, Russian, Ukrainian, Greek, Turkish, Japanese, Korean and
Chinese (Simplified and Traditional). They live in `language/resource.language.<code>/strings.po` (the helper,
screensaver and waveform visualiser have their own `resources/language`). Kodi picks them up from Settings >
Interface > Regional > Language; a text missing from a language shows in English.

- Ids 31000-31999 (Kodi's range for skins, full): `$LOCALIZE[id]` or a bare id. Kodi ignores a skin's ids from 32000
  for `$LOCALIZE`, so ids 32000 and up, in the same strings.po, are read as the skin's add-on strings:
  `$ADDON[skin.aeon.fuse id]`. Conditions and view ids (`<viewtype label="...">`) need 31xxx ids.
- Where Kodi has the word the skin uses Kodi's own string. Ids used inside `$INFO[...]` and in conditions must not
  contain `, ( ) [ ] | $`.
- Japanese, Korean and Chinese need a font with those characters: Settings > Interface > Skin > Fonts, Roboto CJKSC
  (needs `resource.font.robotocjksc`).
- Right-to-left languages are not included: the layouts only run left to right.

## First start

A setup wizard opens on Home the first time. It starts with the credits, then asks for the library backdrop (and, with
Neutral, a palette), the skin theme, the menu theme (the theme's own menus or Fuse), the Home menu items, the Home
menu position and spotlight, the corner boxes, watched indicators, titles or logos, media info, extra fanart, spoilers,
motion and (on Linux boxes) memory hand-back, each with a preview. Run it again any time from
Skin settings > Motion, memory, reset > Setup wizard.

## Credits

Huge thanks and credit go out to the following:

1. **djh_**, creator of the Aeon 2 concept this skin is styled after.
   GitHub: <https://github.com/deadendthrills> · Video: <https://www.youtube.com/@duncanharris9168>
2. **jurialmunkey**: <https://github.com/jurialmunkey>
3. **jamal2362**: <https://github.com/jamal2362>
4. **KarmaMole**: <https://github.com/KarmaMole>
5. **The Kodi development team** at [www.kodi.tv](https://www.kodi.tv)

The setup wizard opens with the same list.

## License

GPL-2.0-or-later, see `LICENSE.txt`. Aeon Fuse is a modified version of Glass (`skin.glass`), which is based on
Daylight (`skin.daylight`) by Omar Kamel. The bundled interface fonts are under the SIL Open Font License (`fonts/`).
The ten lyric fonts of the Words lyrics style (`fonts/lyrics/`) are the ones Estuary MOD V2 ships, unchanged: five under
the SIL Open Font License or Apache 2.0, five free fonts under their authors' own terms; each is listed with its author
and terms in `fonts/lyrics/README-lyrics-fonts.txt`.
The optional Home menu icons in `media/icons/af3/` (one of them, `arrows-left-right.png`, is also the File manager's
two-way arrow in the Aeon look) come unchanged from Arctic Fuse 3 by jurialmunkey and stay under its Creative Commons
BY-NC-SA 4.0 licence (see `media/icons/af3/LICENSE.txt`).
The four pictures behind the Skin settings preview cards (`media/previews/clear_*.jpg`) are smaller copies of pictures
from Skin Backgrounds - Clear Design by Orna Post and Benny Buchnik and stay under its Creative Commons BY-SA 3.0 US
licence (see `media/previews/LICENSE.txt`).
