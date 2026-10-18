# Where the Waves Go Quiet (web app)

A scroll film about three months of chasing the prime numbers and the Riemann hypothesis. Every frame is drawn live in the browser, and the soundtrack is synthesised from the mathematics while you watch. There is no build step and no server code.

## View it locally

* Double-click `index.html`, or
* serve the folder: `python -m http.server 8000` inside `site/`, then open <http://localhost:8000>.

Press **Play** (or the space bar) to let the film run at the tempo of each scene, or scroll yourself. **Sound** turns the score on; browsers only allow audio after a click.

## Host it

The repository root has a `vercel.json` that publishes this folder, so importing the repo in Vercel needs no settings. To deploy only this folder instead, run `npx vercel --prod` inside `site/`; the local `vercel.json` adds clean URLs and asset caching.

## Layout

| Path | What it is |
|---|---|
| `index.html` | The film: opening, six acts of scenes with narration and working notes, and the epilogue. |
| `assets/css/film.css` | The look: dark screening room, film grain, handwritten subtitles, typed notes. |
| `assets/js/film.js` | The engine and every scene. Scroll position inside a scene is its playhead. |
| `assets/js/sound.js` | The score, all Web Audio: mallets on primes, ticks on composites, drones, bells, booms, a riser. |
| `assets/js/zeta.js` | Complex ζ(s) and Γ(s) (Borwein series and functional equation), checked against mpmath to 8 digits. |
| `assets/js/data.js` | Precomputed data: the first 1,000 zeta zeros, ζ(σ + it) curves, sieve statistics, the archive listing and the hex seed. |
| `vercel.json` | Settings for deploying this folder on its own. |

## Stills and links into the film

* `?at=s-zeta:0.4` opens the film at 40% of the zeta-spiral scene.
* `?solo=s-domain:0.5` renders one scene as a still, without scrolling.

Scene ids: `s-count`, `s-sieve`, `s-smooth`, `s-zn`, `s-spiral`, `s-bits`, `s-life`, `s-walk`, `s-zeta`, `s-domain`, `s-explicit`, `s-critical`, `s-robin`.

## External resources

Fonts come from Google Fonts (Big Shoulders Display, La Belle Aurore, Courier Prime), and the equations come from MathJax 3.2.2 on cdnjs.
