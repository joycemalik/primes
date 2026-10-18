# The Prime Wave Notebook (web app)

An interactive, static website that tours the prime-number and Riemann-hypothesis research in this folder. There's no build step and no server code: every chart is computed in the browser.

## View it locally

* Double-click `index.html`, or
* serve the folder (better for video and fonts): `python -m http.server 8000` inside `site/`, then open <http://localhost:8000>.

## Host it

The `site/` folder is the whole website. Upload it as-is to any static host:

| Host | How |
|---|---|
| GitHub Pages | Push the repo, then Settings → Pages → deploy from branch, folder `/site` (or copy `site/` to a `docs/` folder). `.nojekyll` is included. |
| Netlify / Cloudflare Pages | Drag the `site` folder onto the dashboard, or set the publish directory to `site`. |
| Vercel | From inside `site/`: `npx vercel` then `npx vercel --prod`. Or import a Git repo that contains only this folder and set **Root Directory = site**, **Framework = Other**, no build command. `vercel.json` adds clean URLs and asset caching. Don't import the whole research repo: it has files over GitHub's 100 MB limit. |
| Any web server | Copy the folder into the web root. |

## Layout

| Path | What it is |
|---|---|
| `index.html` | The page, typeset as a 1920s journal: eight sheets (title page, six parts, appendix) with numbered equations, plates, margin notes and references. |
| `vercel.json` | Vercel settings: clean URLs, caching for `assets/`. |
| `assets/css/styles.css` | All styles. Paper and ink colours are tokens at the top. The page deliberately keeps one look (paper on a desk) instead of switching to a dark theme. |
| `assets/js/app.js` | Every interactive figure, one block per chapter, in page order. |
| `assets/js/zeta.js` | Complex ζ(s) and Γ(s) (Borwein series and functional equation), checked against mpmath to 8 digits. |
| `assets/js/data.js` | Precomputed data: the first 1,000 zeta zeros, ζ(σ+it) curves, sieve statistics, prime-matrix eigenvalues, the folder explorer and the hex seed. |
| `assets/img/` | Figures and the radial animation copied from the research folders. |

## External resources

Fonts come from Google Fonts (Old Standard TT, UnifrakturMaguntia, La Belle Aurore, Courier Prime, Special Elite) and the equations from MathJax 3.2.2 on cdnjs. Offline, the page still works with system fonts, but the equations then show as raw TeX.

## Updating the data

`data.js` was generated from the folder in October 2026. The first 1,000 zeros came from `mpmath.zetazero`. If you add research files, regenerate the explorer rows (`window.FILES`) so the folder explorer stays complete.
