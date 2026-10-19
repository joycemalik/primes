// The Book of the Quiet Waves: footnotes, contents, reading light, and the small figures you can play with.
(() => {
'use strict';
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const root = document.documentElement;
const store = { get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
const css = (v) => getComputedStyle(root).getPropertyValue(v).trim();

/* ---------- footnotes: number them, put a copy in the margin, open a popover on tap ---------- */
const pop = $('#pop'), popBody = $('.body', pop);
let popFor = null;
$$('.fn').forEach((fn, i) => {
  const n = i + 1, html = fn.innerHTML;
  const ref = document.createElement('button'); ref.type = 'button'; ref.className = 'fnref'; ref.textContent = n; ref.setAttribute('aria-label', `Note ${n}`);
  const sn = document.createElement('span'); sn.className = 'sn'; sn.innerHTML = `<span class="n">${n}</span>${html}`;
  ref.addEventListener('click', () => {
    if (getComputedStyle(sn).display !== 'none') return;
    if (popFor === ref && !pop.hidden) { pop.hidden = true; return; }
    popBody.innerHTML = `<span class="n">${n}</span>${html}`; pop.hidden = false; popFor = ref;
    if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([popBody]).catch(() => {});
  });
  ref.addEventListener('mouseenter', () => sn.classList.add('lit')); ref.addEventListener('mouseleave', () => sn.classList.remove('lit'));
  // the margin note floats from the start of the paragraph that holds it
  const host = fn.closest('p, li, dd, .aside, .def') || fn.parentNode;
  fn.replaceWith(ref); host.insertBefore(sn, host.firstChild);
});
$('.x', pop).addEventListener('click', () => { pop.hidden = true; });
addEventListener('keydown', (e) => { if (e.key === 'Escape') { pop.hidden = true; closeToc(); } });

/* ---------- contents ---------- */
const toc = $('#toc'), tocBtn = $('#tocbtn'), chapters = $$('.chapter');
$('#toclist').innerHTML = chapters.map(c => `<li><a href="#${c.id}">${c.dataset.title}</a></li>`).join('');
const tocLinks = $$('#toclist a');
function closeToc() { toc.classList.remove('open'); tocBtn.setAttribute('aria-expanded', 'false'); }
tocBtn.addEventListener('click', () => { const o = toc.classList.toggle('open'); tocBtn.setAttribute('aria-expanded', String(o)); });
tocLinks.forEach(a => a.addEventListener('click', closeToc));

/* ---------- reading light and size ---------- */
const THEMES = ['paper', 'sepia', 'night'], NAMES = { paper: 'Paper', sepia: 'Sepia', night: 'Night' };
const themeBtn = $('#theme');
function curTheme() { return root.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'night' : 'paper'); }
function showTheme() { themeBtn.textContent = NAMES[curTheme()]; }
themeBtn.addEventListener('click', () => { const t = THEMES[(THEMES.indexOf(curTheme()) + 1) % 3]; root.dataset.theme = t; store.set('book-theme', t); showTheme(); redrawAll(); });
showTheme();
let fs = parseFloat(store.get('book-size')) || parseFloat(getComputedStyle(document.body).fontSize);
const size = (d) => { fs = Math.max(15, Math.min(26, fs + d)); root.style.setProperty('--fs', fs + 'px'); store.set('book-size', fs); };
$('#smaller').addEventListener('click', () => size(-1)); $('#bigger').addEventListener('click', () => size(1));

/* ---------- progress, current chapter, reading time ---------- */
const words = $('#book').textContent.split(/\s+/).length;
$('#readtime').textContent = `About ${(Math.round(words / 1000) * 1000).toLocaleString('en-US')} words · around ${Math.round(words / 200)} minutes, at an easy pace`;
function onScroll() {
  const max = document.documentElement.scrollHeight - innerHeight;
  $('#progress').style.width = (max > 0 ? scrollY / max * 100 : 0) + '%';
  let cur = 0; chapters.forEach((c, i) => { if (c.getBoundingClientRect().top < innerHeight * .35) cur = i; });
  tocLinks.forEach((a, i) => a.classList.toggle('here', i === cur));
}
addEventListener('scroll', onScroll, { passive: true }); onScroll();

/* ---------- figures ---------- */
const isP = (() => { const N = 20001, s = new Uint8Array(N).fill(1); s[0] = s[1] = 0; for (let i = 2; i * i < N; i++) if (s[i]) for (let j = i * i; j < N; j += i) s[j] = 0; return s; })();
const PR = []; for (let i = 2; i < isP.length; i++) if (isP[i]) PR.push(i);
function fit(cv) {
  const dpr = Math.min(devicePixelRatio || 1, 2), w = cv.clientWidth, h = cv.clientHeight;
  if (cv.width !== Math.round(w * dpr) || cv.height !== Math.round(h * dpr)) { cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); }
  const ctx = cv.getContext('2d'); ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, w, h);
  return { ctx, w, h, C: { ink: css('--ink'), dim: css('--dim'), prime: css('--prime'), wave: css('--wave'), violet: css('--violet'), rule: css('--rule') } };
}
const MONO = (px) => `${px}px "Courier Prime", monospace`;
const FIG = {};

FIG.rect = (el) => {
  let n = 12; const val = $('.val', el);
  $$('button', el).forEach(b => b.addEventListener('click', () => { n = Math.max(2, Math.min(36, n + +b.dataset.n)); draw(); }));
  function draw() {
    const { ctx, w, h, C } = fit($('canvas', el)); val.textContent = n;
    const shapes = []; for (let r = 1; r <= n; r++) if (n % r === 0 && r <= n / r) shapes.push([r, n / r]);
    const prime = shapes.length === 1, cols = shapes.length, cw = w / cols;
    shapes.forEach(([r, c], k) => {
      const d = Math.min((cw - 24) / c, (h - 70) / r, 22), x0 = k * cw + (cw - d * c) / 2, y0 = (h - 30 - d * r) / 2;
      ctx.fillStyle = prime ? C.prime : C.wave;
      for (let i = 0; i < r; i++) for (let j = 0; j < c; j++) { ctx.beginPath(); ctx.arc(x0 + d * (j + .5), y0 + d * (i + .5), d * .38, 0, 7); ctx.fill(); }
      ctx.fillStyle = C.dim; ctx.font = MONO(13); ctx.textAlign = 'center'; ctx.fillText(`${r} × ${c}`, k * cw + cw / 2, h - 14);
    });
    if (prime) { ctx.fillStyle = C.prime; ctx.font = MONO(14); ctx.textAlign = 'center'; ctx.fillText(`${n} is prime: only one row works`, w / 2, 22); }
  }
  return draw;
};

FIG.sieve = (el) => {
  const ps = [2, 3, 5, 7]; let k = 0; const val = $('.val', el);
  $('[data-act=step]', el).addEventListener('click', () => { if (k < ps.length) k++; draw(); });
  $('[data-act=reset]', el).addEventListener('click', () => { k = 0; draw(); });
  function draw() {
    const { ctx, w, h, C } = fit($('canvas', el)), cols = w < 420 ? 10 : 20, rows = Math.ceil(99 / cols), cw = w / cols, ch = Math.min(h / rows, 46), y0 = (h - ch * rows) / 2;
    const by = (n) => { for (let i = 0; i < k; i++) if (n !== ps[i] && n % ps[i] === 0) return i; return -1; };
    const col = [C.wave, C.violet, '#C9A23A', '#3E9A6E'];
    for (let n = 2; n <= 100; n++) {
      const i = n - 2, x = (i % cols) * cw, y = y0 + Math.floor(i / cols) * ch, b = by(n), done = k === ps.length;
      ctx.font = MONO(Math.min(16, cw * .38)); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      if (b >= 0) { ctx.globalAlpha = .35; ctx.fillStyle = col[b]; ctx.fillText(n, x + cw / 2, y + ch / 2); ctx.globalAlpha = 1; ctx.strokeStyle = col[b]; ctx.beginPath(); ctx.moveTo(x + cw * .2, y + ch * .7); ctx.lineTo(x + cw * .8, y + ch * .3); ctx.stroke(); }
      else { const sure = ps.slice(0, k).includes(n) || (done); ctx.fillStyle = sure ? C.prime : C.ink; if (sure) { ctx.beginPath(); ctx.arc(x + cw / 2, y + ch / 2, Math.min(cw, ch) * .36, 0, 7); ctx.strokeStyle = C.prime; ctx.stroke(); } ctx.fillText(n, x + cw / 2, y + ch / 2); }
    }
    ctx.textBaseline = 'alphabetic';
    val.textContent = k === 0 ? 'Nothing crossed out yet.' : k < ps.length ? `Crossed out the multiples of ${ps.slice(0, k).join(', ')}.` : 'Done. The 25 circled numbers are every prime up to 100.';
  }
  return draw;
};

FIG.sacks = (el) => {
  return function draw() {
    const { ctx, w, h, C } = fit($('canvas', el)), R = Math.min(w, h) / 2 - 8, N = 20000, sc = R / Math.sqrt(N);
    for (let n = 1; n <= N; n++) { const r = Math.sqrt(n) * sc, th = 2 * Math.PI * Math.sqrt(n), x = w / 2 + r * Math.cos(th), y = h / 2 - r * Math.sin(th);
      if (isP[n]) { ctx.fillStyle = C.prime; ctx.fillRect(x - .9, y - .9, 1.8, 1.8); } else { ctx.globalAlpha = .12; ctx.fillStyle = C.dim; ctx.fillRect(x - .5, y - .5, 1, 1); ctx.globalAlpha = 1; } }
  };
};

FIG.euler = (el) => {
  let k = 0; const val = $('.val', el), target = Math.PI ** 2 / 6;
  $('[data-act=more]', el).addEventListener('click', () => { k = Math.min(k + 1, 40); draw(); });
  $('[data-act=reset]', el).addEventListener('click', () => { k = 0; draw(); });
  function draw() {
    const { ctx, w, h, C } = fit($('canvas', el)), L = 40, Rr = w - 20, T = 30, B = h - 40, lo = 1, hi = 1.7;
    const Y = (v) => B - (v - lo) / (hi - lo) * (B - T), X = (i) => L + i / 40 * (Rr - L);
    ctx.strokeStyle = C.prime; ctx.setLineDash([5, 5]); ctx.beginPath(); ctx.moveTo(L, Y(target)); ctx.lineTo(Rr, Y(target)); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = C.prime; ctx.font = MONO(12); ctx.textAlign = 'right'; ctx.fillText('π²/6 = 1.6449…', Rr, Y(target) - 8);
    let prod = 1; ctx.fillStyle = C.wave;
    for (let i = 0; i < k; i++) { const p = PR[i]; prod *= 1 / (1 - 1 / (p * p)); const x = X(i + 1); ctx.fillRect(x - 3, Y(prod), 6, B - Y(prod)); if (i < 8) { ctx.fillStyle = C.dim; ctx.textAlign = 'center'; ctx.fillText(p, x, B + 16); ctx.fillStyle = C.wave; } }
    ctx.strokeStyle = C.rule; ctx.beginPath(); ctx.moveTo(L, B); ctx.lineTo(Rr, B); ctx.stroke();
    val.textContent = k ? `${k} prime${k > 1 ? 's' : ''} multiplied in (up to ${PR[k - 1]}): product = ${prod.toFixed(5)}, still ${(target - prod).toFixed(5)} short` : 'Each bar multiplies in one more prime factor 1 / (1 − 1/p²).';
  }
  return draw;
};

FIG.spiral = (el) => {
  const st = { s: .5, t: 14.1347 }, val = $('.val', el);
  $$('input', el).forEach(i => i.addEventListener('input', () => { st[i.dataset.k] = +i.value; draw(); }));
  function draw() {
    const { ctx, w, h, C } = fit($('canvas', el)), { s, t } = st, N = 600;
    $('.vs', el).textContent = s.toFixed(2); $('.vt', el).textContent = t.toFixed(2);
    // raw partial sums, and the same sums with the drift N^(1-s)/(1-s) taken away
    const raw = [[0, 0]], cor = []; let a = 0, b = 0;
    const den = (1 - s) ** 2 + t * t;
    for (let n = 1; n <= N; n++) {
      const m = Math.pow(n, -s), ang = -t * Math.log(n); a += m * Math.cos(ang); b += m * Math.sin(ang); raw.push([a, b]);
      const q = Math.pow(n, 1 - s), qa = -t * Math.log(n); // N^(1-s) = N^(1-σ) e^{-it ln N}, then divided by (1-s)
      const ur = q * Math.cos(qa), ui = q * Math.sin(qa), cr = (ur * (1 - s) - ui * t) / den, ci = (ui * (1 - s) + ur * t) / den;
      cor.push([a - cr, b - ci]);
    }
    const [zr, zi] = (typeof zetaC === 'function') ? zetaC(s, t) : cor[cor.length - 1];
    const sc = Math.min(w, h) / 6.5, cx = w / 2 - zr * sc * .5, cy = h / 2 + zi * sc * .5;
    const P = ([x, y]) => [cx + x * sc, cy - y * sc];
    ctx.strokeStyle = C.rule; ctx.beginPath(); ctx.moveTo(0, cy); ctx.lineTo(w, cy); ctx.moveTo(cx, 0); ctx.lineTo(cx, h); ctx.stroke();
    ctx.globalAlpha = .3; ctx.strokeStyle = C.dim; ctx.lineWidth = 1; ctx.beginPath(); raw.slice(0, 200).forEach((p, i) => { const [x, y] = P(p); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }); ctx.stroke(); ctx.globalAlpha = 1;
    ctx.lineWidth = 1.6; for (let i = 1; i < 60; i++) { ctx.strokeStyle = i < 30 ? C.wave : C.violet; const [x0, y0] = P(raw[i - 1]), [x1, y1] = P(raw[i]); ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke(); }
    ctx.strokeStyle = C.prime; ctx.lineWidth = 1.2; ctx.beginPath(); cor.slice(20).forEach((p, i) => { const [x, y] = P(p); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }); ctx.stroke();
    const [ex, ey] = P([zr, zi]); ctx.fillStyle = C.prime; ctx.beginPath(); ctx.arc(ex, ey, 5, 0, 7); ctx.fill();
    ctx.fillStyle = C.ink; ctx.beginPath(); ctx.arc(cx, cy, 3, 0, 7); ctx.fill();
    const mag = Math.hypot(zr, zi);
    val.innerHTML = `ζ(s) ≈ ${zr.toFixed(3)} ${zi < 0 ? '−' : '+'} ${Math.abs(zi).toFixed(3)}i · size ${mag.toFixed(3)}${mag < .02 ? ' · <b style="color:var(--prime)">a zero!</b>' : ''}`;
  }
  return draw;
};

FIG.critical = (el) => {
  let s = .5;
  $('input', el).addEventListener('input', (e) => { s = +e.target.value; draw(); });
  function draw() {
    const { ctx, w, h, C } = fit($('canvas', el)); $('.vs', el).textContent = s.toFixed(2);
    const L = 30, R = w - 12, T = 16, B = h - 30, X = (t) => L + t / 50 * (R - L), Y = (v) => B - Math.min(v, 3.2) / 3.2 * (B - T);
    ctx.strokeStyle = C.rule; ctx.beginPath(); ctx.moveTo(L, B); ctx.lineTo(R, B); ctx.stroke();
    (window.ZEROS || []).filter(z => z < 50).forEach(z => { ctx.strokeStyle = C.rule; ctx.setLineDash([2, 4]); ctx.beginPath(); ctx.moveTo(X(z), T); ctx.lineTo(X(z), B); ctx.stroke(); ctx.setLineDash([]); });
    ctx.strokeStyle = Math.abs(s - .5) < .01 ? C.prime : C.wave; ctx.lineWidth = 2; ctx.beginPath();
    for (let i = 0; i <= 600; i++) { const t = .2 + i / 600 * 49.8, [a, b] = zetaC(s, t), v = Math.hypot(a, b); i ? ctx.lineTo(X(t), Y(v)) : ctx.moveTo(X(t), Y(v)); }
    ctx.stroke(); ctx.lineWidth = 1;
    ctx.fillStyle = C.dim; ctx.font = MONO(12); ctx.textAlign = 'center'; for (let t = 0; t <= 50; t += 10) ctx.fillText(t, X(t), B + 18);
  }
  return draw;
};

FIG.explicit = (el) => {
  let K = 10; const Z = window.ZEROS || [];
  $('input', el).addEventListener('input', (e) => { K = +e.target.value; draw(); });
  const psi = (x) => { let s = 0; for (const p of PR) { if (p > x) break; for (let q = p; q <= x; q *= p) s += Math.log(p); } return s; };
  function draw() {
    const { ctx, w, h, C } = fit($('canvas', el)); $('.vk', el).textContent = K;
    const x1 = 50, L = 34, R = w - 12, T = 14, B = h - 28, X = (x) => L + x / x1 * (R - L), Y = (v) => B - v / 56 * (B - T);
    ctx.strokeStyle = C.rule; ctx.beginPath(); ctx.moveTo(L, B); ctx.lineTo(R, B); ctx.moveTo(X(0), Y(0)); ctx.lineTo(X(x1), Y(x1)); ctx.stroke();
    ctx.strokeStyle = C.prime; ctx.lineWidth = 2.4; ctx.beginPath(); let prev = 0; ctx.moveTo(X(1), Y(0));
    for (let x = 1; x <= x1; x += .05) { const v = psi(x); ctx.lineTo(X(x), Y(prev)); ctx.lineTo(X(x), Y(v)); prev = v; } ctx.stroke();
    ctx.strokeStyle = C.wave; ctx.lineWidth = 1.6; ctx.beginPath();
    for (let i = 0; i <= 900; i++) {
      const x = 1.5 + i / 900 * (x1 - 1.5), lx = Math.log(x), sx = Math.sqrt(x); let v = x - Math.log(2 * Math.PI) - .5 * Math.log(1 - 1 / (x * x));
      for (let k = 0; k < K && k < Z.length; k++) { const g = Z[k]; v -= 2 * sx * (.5 * Math.cos(g * lx) + g * Math.sin(g * lx)) / (.25 + g * g); }
      i ? ctx.lineTo(X(x), Y(v)) : ctx.moveTo(X(x), Y(v));
    }
    ctx.stroke(); ctx.lineWidth = 1;
    ctx.fillStyle = C.dim; ctx.font = MONO(12); ctx.textAlign = 'center'; for (let x = 0; x <= x1; x += 10) ctx.fillText(x, X(x), B + 18);
  }
  return draw;
};

/* ---------- diagrams ---------- */
const txt = (ctx, s, x, y, c, px = 13, al = 'center') => { ctx.fillStyle = c; ctx.font = MONO(px); ctx.textAlign = al; ctx.fillText(s, x, y); };
const arrow = (ctx, x0, y0, x1, y1, c, lw = 2) => { ctx.strokeStyle = c; ctx.fillStyle = c; ctx.lineWidth = lw; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke(); const a = Math.atan2(y1 - y0, x1 - x0); ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x1 - 10 * Math.cos(a - .4), y1 - 10 * Math.sin(a - .4)); ctx.lineTo(x1 - 10 * Math.cos(a + .4), y1 - 10 * Math.sin(a + .4)); ctx.fill(); ctx.lineWidth = 1; };

FIG.tree = (el) => () => {
  const { ctx, w, h, C } = fit($('canvas', el)), sx = w / 520, sy = h / 250;
  const N = { a: [260, 30, '360'], b: [160, 95, '36'], c: [380, 95, '10'], d: [100, 160, '6'], e: [220, 160, '6'], f: [340, 160, '2'], g: [420, 160, '5'], h: [70, 225, '2'], i: [130, 225, '3'], j: [190, 225, '2'], k: [250, 225, '3'] };
  [['a', 'b'], ['a', 'c'], ['b', 'd'], ['b', 'e'], ['c', 'f'], ['c', 'g'], ['d', 'h'], ['d', 'i'], ['e', 'j'], ['e', 'k']].forEach(([p, q]) => { ctx.strokeStyle = C.rule; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(N[p][0] * sx, N[p][1] * sy + 10); ctx.lineTo(N[q][0] * sx, N[q][1] * sy - 14); ctx.stroke(); });
  Object.values(N).forEach(([x, y, s]) => { const pr = isP[+s]; if (pr) { ctx.strokeStyle = C.prime; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.arc(x * sx, y * sy - 4, 15, 0, 7); ctx.stroke(); } txt(ctx, s, x * sx, y * sy + 1, pr ? C.prime : C.ink, 16); });
  ctx.lineWidth = 1; txt(ctx, '360 = 2 × 2 × 2 × 3 × 3 × 5', w - 10, h - 8, C.dim, 12, 'right');
};

FIG.euclid = (el) => () => {
  const { ctx, w, h, C } = fit($('canvas', el)), y = h * .34, ps = [2, 3, 5, 7], bw = Math.min(40, w / 16), x0 = w * .04;
  ps.forEach((p, i) => { const x = x0 + i * (bw + 6); ctx.strokeStyle = C.prime; ctx.strokeRect(x, y - bw / 2, bw, bw); txt(ctx, p, x + bw / 2, y + 5, C.prime, 15); });
  const x1 = x0 + 4 * (bw + 6), seg = (w - x1) / 5;
  arrow(ctx, x1 + 4, y, x1 + seg, y, C.dim); txt(ctx, '×', x1 + seg / 2, y - 12, C.dim, 13);
  txt(ctx, '210', x1 + seg * 1.6, y + 6, C.ink, 18);
  arrow(ctx, x1 + seg * 2.2, y, x1 + seg * 3.1, y, C.dim); txt(ctx, '+ 1', x1 + seg * 2.65, y - 12, C.dim, 13);
  txt(ctx, '211', x1 + seg * 3.8, y + 7, C.prime, 22);
  ps.forEach((p, i) => txt(ctx, `211 ÷ ${p} leaves remainder 1`, w / 2, h * .6 + i * 17, C.dim, 12));
  txt(ctx, 'no prime on the list divides it, so a prime is missing', w / 2, h - 8, C.ink, 12);
};

FIG.logladder = (el) => () => {
  const { ctx, w, h, C } = fit($('canvas', el)), L = 30, R = w - 30, y = h * .4, n = 6;
  ctx.strokeStyle = C.ink; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(L, y); ctx.lineTo(R, y); ctx.stroke();
  for (let k = 0; k <= n; k++) {
    const x = L + k / n * (R - L); ctx.strokeStyle = C.ink; ctx.beginPath(); ctx.moveTo(x, y - 7); ctx.lineTo(x, y + 7); ctx.stroke();
    txt(ctx, k < 4 ? String(10 ** k) : '10' + '⁴⁵⁶'[k - 4], x, y - 16, C.ink, 13); txt(ctx, 'ln ' + (k * Math.LN10).toFixed(1), x, y + 26, C.prime, 11);
    if (k) { const m = L + (k - .5) / n * (R - L); ctx.strokeStyle = C.wave; ctx.beginPath(); ctx.arc(m, y + 36, (R - L) / n / 2.2, Math.PI * .2, Math.PI * .8); ctx.stroke(); txt(ctx, '+2.3', m, y + 68, C.wave, 11); }
  }
  ctx.lineWidth = 1; txt(ctx, 'each ×10 adds the same 2.3 to ln x: multiplying becomes adding', w / 2, h - 8, C.dim, 12);
};

FIG.gaps = (el) => () => {
  const { ctx, w, h, C } = fit($('canvas', el)), cnt = new Array(37).fill(0);
  for (let i = 2; i < PR.length; i++) { const g = PR[i] - PR[i - 1]; if (g <= 36) cnt[g]++; }
  const mx = Math.max(...cnt), L = 14, R = w - 10, B = h - 30, T = 34, bw = (R - L) / 18;
  for (let g = 2, i = 0; g <= 36; g += 2, i++) { const bh = cnt[g] / mx * (B - T), six = g % 6 === 0; ctx.fillStyle = six ? C.prime : C.wave; ctx.fillRect(L + i * bw + 2, B - bh, bw - 4, bh); txt(ctx, g, L + i * bw + bw / 2, B + 16, six ? C.prime : C.dim, 10); }
  txt(ctx, `gaps between the ${PR.length.toLocaleString('en-US')} primes below 20,000 · multiples of 6 in orange`, w / 2, 16, C.dim, 12);
};

FIG.harmonic = (el) => () => {
  const { ctx, w, h, C } = fit($('canvas', el)), B = h - 34, T = 30, U = (B - T) / .75;
  const groups = [[2], [3, 4], [5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15, 16], Array.from({ length: 16 }, (_, i) => 17 + i)], cw = (w - 40) / groups.length;
  ctx.strokeStyle = C.prime; ctx.setLineDash([5, 5]); ctx.beginPath(); ctx.moveTo(20, B - U * .5); ctx.lineTo(w - 20, B - U * .5); ctx.stroke(); ctx.setLineDash([]);
  txt(ctx, '½', w - 10, B - U * .5 + 5, C.prime, 15);
  groups.forEach((g, i) => { let y = B; g.forEach((n, j) => { const hh = U / n; ctx.fillStyle = j % 2 ? C.violet : C.wave; ctx.fillRect(20 + i * cw + 8, y - hh + .5, cw - 16, hh - 1); y -= hh; });
    txt(ctx, g.length === 1 ? `1/${g[0]}` : `1/${g[0]} … 1/${g[g.length - 1]}`, 20 + i * cw + cw / 2, B + 18, C.dim, 11); });
  txt(ctx, 'every group reaches ½, and there are endless groups', w / 2, 16, C.dim, 12);
};

FIG.plane = (el) => () => {
  const { ctx, w, h, C } = fit($('canvas', el)), u = Math.min(w / 12, h / 7), cx = w * .42, cy = h * .58;
  ctx.strokeStyle = C.rule; for (let k = -8; k <= 8; k++) { ctx.beginPath(); ctx.moveTo(cx + k * u, 0); ctx.lineTo(cx + k * u, h); ctx.stroke(); ctx.beginPath(); ctx.moveTo(0, cy + k * u); ctx.lineTo(w, cy + k * u); ctx.stroke(); }
  ctx.strokeStyle = C.ink; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(0, cy); ctx.lineTo(w, cy); ctx.moveTo(cx, 0); ctx.lineTo(cx, h); ctx.stroke(); ctx.lineWidth = 1;
  txt(ctx, 'real', w - 8, cy - 8, C.dim, 12, 'right'); txt(ctx, 'imaginary', cx + 8, 16, C.dim, 12, 'left');
  ctx.strokeStyle = C.violet; ctx.setLineDash([3, 4]); ctx.beginPath(); ctx.arc(cx, cy, u * 1.6, 0, 2 * Math.PI); ctx.stroke(); ctx.setLineDash([]);
  [[1, 0, '1'], [0, 1, 'i'], [-1, 0, '−1'], [0, -1, '−i']].forEach(([a, b, s]) => { arrow(ctx, cx, cy, cx + a * u * 1.6, cy - b * u * 1.6, C.wave, 1.8); txt(ctx, s, cx + a * u * 2.05, cy - b * u * 2.05 + 5, C.wave, 14); });
  arrow(ctx, cx, cy, cx + 3 * u, cy - 2 * u, C.prime, 2.4); txt(ctx, '3 + 2i', cx + 3 * u + 8, cy - 2 * u - 6, C.prime, 15, 'left');
  txt(ctx, '× i turns a quarter', cx - u * 1.4, cy + u * 2.4, C.violet, 12, 'right');
};

FIG.clock = (el) => {
  let th = 1; $('input', el).addEventListener('input', (e) => { th = +e.target.value; draw(); });
  function draw() {
    const { ctx, w, h, C } = fit($('canvas', el)), r = Math.min(h * .36, w * .2), cx = w * .26, cy = h / 2 - 8;
    $('.vth', el).textContent = th.toFixed(2);
    ctx.strokeStyle = C.rule; ctx.beginPath(); ctx.arc(cx, cy, r, 0, 7); ctx.moveTo(cx - r - 14, cy); ctx.lineTo(cx + r + 14, cy); ctx.moveTo(cx, cy - r - 14); ctx.lineTo(cx, cy + r + 14); ctx.stroke();
    const x = cx + r * Math.cos(th), y = cy - r * Math.sin(th);
    ctx.strokeStyle = C.violet; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(cx, cy, r * .25, 0, -th, true); ctx.stroke();
    ctx.strokeStyle = C.wave; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(x, cy); ctx.stroke(); ctx.strokeStyle = C.prime; ctx.beginPath(); ctx.moveTo(x, cy); ctx.lineTo(x, y); ctx.stroke(); ctx.lineWidth = 1;
    arrow(ctx, cx, cy, x, y, C.ink, 2.4);
    const L = w * .52, R = w - 14, X = (a) => L + a / (2 * Math.PI) * (R - L);
    [[Math.cos, C.wave, 'cos θ (east)'], [Math.sin, C.prime, 'sin θ (north)']].forEach(([f, c, s], k) => { ctx.strokeStyle = c; ctx.lineWidth = 1.6; ctx.beginPath(); for (let i = 0; i <= 200; i++) { const a = i / 200 * 2 * Math.PI; i ? ctx.lineTo(X(a), cy - f(a) * r) : ctx.moveTo(X(a), cy - f(a) * r); } ctx.stroke(); txt(ctx, s, R, 14 + k * 16, c, 12, 'right'); });
    ctx.lineWidth = 1; ctx.strokeStyle = C.ink; ctx.setLineDash([3, 4]); ctx.beginPath(); ctx.moveTo(X(th), 0); ctx.lineTo(X(th), h - 24); ctx.stroke(); ctx.setLineDash([]);
    txt(ctx, `e^(iθ) = ${Math.cos(th).toFixed(2)} ${Math.sin(th) < 0 ? '−' : '+'} ${Math.abs(Math.sin(th)).toFixed(2)} i`, cx, h - 8, C.ink, 13);
  }
  return draw;
};

FIG.mirror = (el) => () => {
  const { ctx, w, h, C } = fit($('canvas', el)), u = Math.min(w / 6, 110), cx = w / 2 - u * .5, cy = h / 2, X = (s) => cx + s * u, Y = (t) => cy - t * u * .5;
  ctx.fillStyle = C.rule; ctx.fillRect(X(0), 0, u, h);
  ctx.strokeStyle = C.prime; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(X(.5), 0); ctx.lineTo(X(.5), h); ctx.stroke(); ctx.lineWidth = 1;
  ctx.strokeStyle = C.ink; ctx.beginPath(); ctx.moveTo(0, cy); ctx.lineTo(w, cy); ctx.stroke();
  [0, 1].forEach(s => txt(ctx, s, X(s) + (s ? 8 : -8), cy + 18, C.dim, 12)); txt(ctx, '½', X(.5), cy + 18, C.prime, 13);
  const s = [1.6, 1.4], m = [1 - s[0], -s[1]];
  ctx.strokeStyle = C.dim; ctx.setLineDash([4, 5]); ctx.beginPath(); ctx.moveTo(X(s[0]), Y(s[1])); ctx.lineTo(X(m[0]), Y(m[1])); ctx.stroke(); ctx.setLineDash([]);
  ctx.fillStyle = C.wave; ctx.beginPath(); ctx.arc(X(s[0]), Y(s[1]), 6, 0, 7); ctx.fill(); txt(ctx, 's', X(s[0]) + 12, Y(s[1]) - 6, C.wave, 16, 'left');
  ctx.fillStyle = C.violet; ctx.beginPath(); ctx.arc(X(m[0]), Y(m[1]), 6, 0, 7); ctx.fill(); txt(ctx, '1 − s', X(m[0]) - 12, Y(m[1]) + 16, C.violet, 16, 'right');
  ctx.fillStyle = C.ink; ctx.beginPath(); ctx.arc(X(.5), cy, 4, 0, 7); ctx.fill();
  txt(ctx, 'the mirror: real part ½', X(.5) + 10, 18, C.prime, 12, 'left'); txt(ctx, 'critical strip', X(.5), h - 10, C.dim, 12);
};

FIG.strip = (el) => () => {
  const { ctx, w, h, C } = fit($('canvas', el)), u = Math.min(w / 18, 40), cx = w * .64, cy = h - 26, ty = (h - 44) / 50;
  ctx.fillStyle = C.rule; ctx.fillRect(cx, 0, u, cy);
  ctx.strokeStyle = C.ink; ctx.beginPath(); ctx.moveTo(0, cy); ctx.lineTo(w, cy); ctx.stroke();
  for (let k = -2; cx + k * u > 6; k -= 2) { ctx.fillStyle = C.wave; ctx.beginPath(); ctx.arc(cx + k * u, cy, 4, 0, 7); ctx.fill(); if (k >= -8) txt(ctx, k, cx + k * u, cy + 18, C.wave, 11); }
  txt(ctx, 'trivial zeros', cx - 5 * u, cy - 14, C.wave, 12);
  ctx.strokeStyle = C.prime; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(cx + u / 2, 0); ctx.lineTo(cx + u / 2, cy); ctx.stroke(); ctx.lineWidth = 1;
  (window.ZEROS || []).filter(z => z < 50).forEach(z => { ctx.fillStyle = C.prime; ctx.beginPath(); ctx.arc(cx + u / 2, cy - z * ty, 4, 0, 7); ctx.fill(); });
  txt(ctx, 'nontrivial zeros', cx + u + 10, cy - 26 * ty, C.prime, 12, 'left'); txt(ctx, 'on Re(s) = ½', cx + u + 10, cy - 26 * ty + 15, C.prime, 12, 'left');
  ctx.fillStyle = C.ink; ctx.beginPath(); ctx.arc(cx + u, cy, 4, 0, 7); ctx.fill(); txt(ctx, 'pole at 1', cx + u + 8, cy + 18, C.ink, 11, 'left');
  txt(ctx, '0 < Re(s) < 1', cx + u / 2, 14, C.dim, 12);
};

FIG.loud = (el) => () => {
  const { ctx, w, h, C } = fit($('canvas', el)), L = 20, R = w - 10, T = 50, B = h - 30, xm = 1e6, ym = Math.pow(xm, .6);
  const X = (x) => L + x / xm * (R - L), Y = (v) => B - v / ym * (B - T);
  [[.5, C.prime, 'grows like √x : every zero on the line'], [.6, C.violet, 'grows like x^0.6 : one zero off the line']].forEach(([e, c, s], k) => {
    ctx.strokeStyle = c; ctx.lineWidth = 2.2; ctx.beginPath(); for (let i = 0; i <= 300; i++) { const x = i / 300 * xm; i ? ctx.lineTo(X(x), Y(Math.pow(x, e))) : ctx.moveTo(X(x), Y(0)); } ctx.stroke();
    txt(ctx, s, L + 6, 16 + k * 18, c, 12, 'left'); });
  ctx.lineWidth = 1; ctx.strokeStyle = C.rule; ctx.beginPath(); ctx.moveTo(L, B); ctx.lineTo(R, B); ctx.stroke();
  txt(ctx, 'the largest a single wave can swing, up to x = 1,000,000', R, B + 20, C.dim, 12, 'right');
};

FIG.spacing = (el) => () => {
  const { ctx, w, h, C } = fit($('canvas', el)), Z = (window.ZEROS || []).slice(0, 60), L = 20, R = w - 20;
  if (!Z.length) return;
  const span = Z[Z.length - 1] - Z[0]; let seed = 11; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const rows = [['heights of the first 60 zeta zeros', Z.map(z => (z - Z[0]) / span), C.prime], ['60 random points', Array.from({ length: Z.length }, rnd).sort((a, b) => a - b), C.wave]];
  rows.forEach(([s, pts, c], k) => { const y = h * (.3 + k * .38); ctx.strokeStyle = C.rule; ctx.beginPath(); ctx.moveTo(L, y); ctx.lineTo(R, y); ctx.stroke();
    ctx.strokeStyle = c; ctx.lineWidth = 2; pts.forEach(p => { ctx.beginPath(); ctx.moveTo(L + p * (R - L), y - 12); ctx.lineTo(L + p * (R - L), y + 12); ctx.stroke(); });
    ctx.lineWidth = 1; txt(ctx, s, L, y - 20, c, 12, 'left'); });
  txt(ctx, 'the zeros keep their distance; random points clump and leave holes', w / 2, h - 8, C.dim, 12);
};

/* ---------- live scenes from the film, played from here ---------- */
function filmFig(el) {
  const frame = $('.frame', el), range = $('input', el), play = $('button', el); let ifr = null, playing = false, last = 0;
  const send = () => { if (ifr && ifr.contentWindow) ifr.contentWindow.postMessage({ p: +range.value }, location.origin); };
  const load = new IntersectionObserver((es) => { if (es[0].isIntersecting && !ifr) {
    ifr = document.createElement('iframe'); ifr.title = $('.cap', el).textContent; ifr.src = `index.html?solo=${el.dataset.scene}:${range.value}&embed`;
    ifr.addEventListener('load', send); frame.appendChild(ifr); load.disconnect(); } }, { rootMargin: '300px' });
  load.observe(el);
  range.addEventListener('input', () => { setPlay(false); send(); });
  function tick(ts) { if (!playing) return; const dt = last ? (ts - last) / 1000 : 0; last = ts; let v = +range.value + dt / 45; if (v >= 1) { v = 1; playing = false; play.textContent = 'Play'; } range.value = v; send(); if (playing) requestAnimationFrame(tick); }
  function setPlay(v) { if (playing === v) return; playing = v; play.textContent = v ? 'Pause' : 'Play'; last = 0; if (v) { if (+range.value >= 1) range.value = 0; requestAnimationFrame(tick); } }
  play.addEventListener('click', () => setPlay(!playing));
}
$$('.fig.film').forEach(filmFig);

const draws = [];
$$('.fig:not(.film)').forEach(el => { const f = FIG[el.dataset.fig]; if (f) draws.push(f(el)); });
function redrawAll() { draws.forEach(d => { try { d(); } catch (e) { console.error(e); } }); }
// draw each figure the first time it comes near the screen, and again whenever the column changes size
const seen = new IntersectionObserver((es) => es.forEach(e => { if (e.isIntersecting) { const i = $$('.fig:not(.film)').indexOf(e.target); if (draws[i]) draws[i](); seen.unobserve(e.target); } }), { rootMargin: '400px' });
$$('.fig:not(.film)').forEach(el => seen.observe(el));
let rz; addEventListener('resize', () => { clearTimeout(rz); rz = setTimeout(redrawAll, 150); });
document.fonts && document.fonts.ready.then(redrawAll);
})();
