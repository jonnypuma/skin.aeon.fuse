# Aeon 2 reference notes (from "Aeon 2 WIP November 2021", 640x360 source)

Observed by stepping through the video frame by frame. Fonts/colours are estimates
because the source is low-res.

## Global look
- Near-black UI (#101010-#1a1a1a panels), light-grey/white focus bar, white uppercase
  geometric sans (Montserrat-like), bold titles, small light-grey uppercase sub-lines.
- Focus bar = solid off-white (#e8e8e8) with dark text and an arrow-shaped notch on its left edge.
- Heavy use of fade/slide transitions; screens fade through black between sections.

## Movie/TV library list view (2:01-2:36)
- Layout: left ~48% poster pane, right ~52% dark list.
- List row: round/triangle certificate badge | TITLE (bold uppercase) | "1998 | COMEDY / CRIME" (small).
  Boxed sets show a "stack" icon and "BOXED SET" sub-line.
- Focus: white bar with notch; poster pane crossfades to focused item's poster.
- Poster pane bottom: "year | runtime", artwork credit caption box.

## Left arrow on a movie with versions (Blade Runner, 2:01)
- Focus moves into the left poster pane. The pane is a VERTICAL list of posters/versions
  that scrolls up/down (one per version: Final Cut, International Cut, Workprint Cut...).
- Each tile shows the version title + subtitle centred over a dimmed poster, a circular
  play button, and "year | runtime" at the bottom. Crossfade between tiles.
- Right arrow returns to the list.

## Left arrow on a Set (2:36)
- Left pane becomes a 2-column poster grid, scrolling vertically, one tile per movie in the set.
- Focused tile dims and shows title, play-circle, "year | runtime".

## Right arrow on movie/show/season/episode (4:02)
- Right info pane slides out from the right with metadata (plot, cast, details).
- TV episode view: fanart full-screen darkened, show clearlogo bottom-left, wide episode
  list (white focus bar, "1|1" season/episode badge, title, "WRITTEN BY x | DIRECTED BY y",
  watched eye icon on the right), plot peeking on the far right.

## Left options rail (6:50)
- Narrow vertical icon rail on far left of a view: view/artwork/sort/filter/refresh/edit.
- Focused icon expands into a white label tab: "ARTWORK / KEYART".
- Text edit dialog: large bold input text, spaced dim on-screen keyboard.

## Music Now Playing (6:49)
- Dark centre card: artist, TRACK 02 FROM THE ALBUM / album / RELEASED IN / ON label.
- Thin line audio waveform across the card (subtle, animated).
- A lighter grey translucent vertical block fills the card from the left as song progress;
  elapsed 01:34 left, total 05:21 right; "FLAC 924KBPS" tag.
- Large album art right of the card; blurred fanart background.

## Other screens seen
- Music library: left list with artist icons and genre sub-line, big artist fanart right.
- Home: left "MUSIC"/"MOVIES" big labels over wide fanart with widget thumbnails.
- Video OSD "NOW PLAYING MOVIES": circular "ENDS 1:20" ring, title + rating, RESUME, dot pager.
- Settings: left category list (VIDEOS/MUSIC/DISCS...), setting name + dim description.
- Power menu: vertical icons, "SHUTDOWN SYSTEM / OR PUSH DOWN TO CONFIGURE KODI".

---
# Full-video sweep (every ~8 s of the 10:24 video) - additional findings

## Home
- Hero fanart top ~57 %, band below with three titles: previous (dim) | CURRENT (large, thin geometric caps,
  small section icon at its left) | next (dim). Focused item sits at ~34 % from the left; list wraps.
- Clock = two stacked numbers (hh over mm) in a grey square, top-right corner.
- Under the titles: thumbnail of recently played / latest + now playing line (equaliser icon, title / artist)
  and a thin progress line.
- Main-menu items can have a vertical SUB-menu (e.g. TV SHOWS -> MATURE / KIDS) shown as a dim stacked list
  with a "<<" chevron marker next to the focused one, over dimmed fanart.
- Each section change crossfades the fanart; moving between sections fades through black.

## Movie / TV list
- TV show rows: left icon is a star (unwatched / favourite) or an eye (watched); movie rows: certificate badge;
  sets: stack icon. Sub-line "YEAR | GENRE / GENRE".
- Focus bar white, whole row; text turns dark grey.
- Right on a TV show: full fanart + show logo bottom-left and an info block bottom-right: outlined chips
  "2 SEASONS" "42 EPISODES", then "2018 | CHILDREN", then plot.
- Seasons: logo centred left, list right: year badge, "* ALL SEASONS 218 EPISODES", "SEASON 1 24 EPISODES".
- Episode list: badge "1|2", title, "WRITTEN BY | DIRECTED BY", eye icon; plot peeks on the right.

## Genres (video)
- Left column (about 45 %): clock stacked top-left, three-dot "options" icon at left edge, list of genres:
  "ACTION AND ADVENTURE" with sub-line "LATEST: VENOM: LET THERE BE CARNAGE | 2021", focused row white.
- Right 55 %: poster mosaic (two columns, offset) of the latest titles in the focused genre.

## Logo wall (TV shows)
- 4-column wall of clearlogos on a dark ground; focused logo sits in a slightly lighter box and enlarges.

## Music library
- Header row "MUSIC LIBRARY" with a wave icon, then artist rows (person icon, ARTIST bold, genre dim);
  list sits in a grey translucent band (top ~ 20-77 % of height) over a dimmed, artwork-tinted background;
  big artist fanart on the right; small album cover + disc count under the list.
- Album: header row (disc icon, ARTIST / ALBUM), track rows: number, TITLE bold, "ARTIST | ALBUM" dim,
  duration right, EXPLICIT chip; focused row white. Album cover large (red example) at the bottom left.
- The WHOLE background is a colour wash taken from the cover art (brown for a red cover, gold for the next
  artist image) - Kodi: $INFO[Fanart.Color1].

## Now playing (details)
- Progress block grows from the card's left edge as the track plays, ~30 px wide at 0:10 -> ~65 px at 0:58
  (rate is slow; it is the "moving grey background").
- Thin wave across the card at ~65 % height; "FLAC 924KBPS" tag; times 00:10 | 04:41 under a hairline.

## Pictures / art
- Pictures library shows full-screen framed CARDS (white border, centred title in large light caps, dim sub-line
  "Moebius . Frazetta . Dean . Berkey . others", year at bottom) in a carousel with neighbours cropped at the
  edges.
- Picture viewer: left icon rail with two-line labels (ASPECT RATIO / KEEP, SORT / NAME, REFRESH / LIBRARY,
  MUSIC / PLAYER, ARTIST / CANALETTO, SUBJECT, LOCATION, DATE), large picture, caption overlay bottom,
  thumbnail strip at the right edge.

## Motion (from still pairs; true frame timing not recoverable from this source)
- Poster / fanart crossfade ~300-400 ms when focus changes (double exposures seen mid-change).
- Left-pane tiles crossfade title overlay over the dimmed poster.
- Screen-to-screen: fade through black.
- Lists scroll smoothly, focused row stays at a fixed position (fixed focus row ~ 40 % from the top).
