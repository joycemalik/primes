// "Where the waves go quiet": the film engine.
// Each .scene is a tall section with a sticky full-screen stage. Scroll position inside the section is the
// playhead (p from 0 to 1). A pulse steps through the integers n = 2, 3, 4, ...; primes ring, composites tick,
// and every scene listens to that pulse. "Play" scrolls the film at the tempo of the current scene.
(() => {
'use strict';
const { ZEROS, DATA, FILES, GOLHEX } = window;
const $ = (s) => document.querySelector(s);
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const K = { bg: '#07080B', ink: '#EDE6D6', dim: '#A39C8C', prime: '#FF6A3D', wave: '#6FA8FF', violet: '#C58BFF', ochre: '#E0B44C', green: '#7FD1A8' };
const FONT = (px) => `${px}px "Courier Prime", "Courier New", monospace`;
const HAND = (px) => `${px}px "La Belle Aurore", "Segoe Script", cursive`;
const rgba = (hex, a) => { const n = parseInt(hex.slice(1), 16); return `rgba(${n >> 16 & 255},${n >> 8 & 255},${n & 255},${a})`; };
const mix = (h1, h2, t) => { const a = parseInt(h1.slice(1), 16), b = parseInt(h2.slice(1), 16); const c = [16, 8, 0].map(s => Math.round((a >> s & 255) + ((b >> s & 255) - (a >> s & 255)) * t)); return `rgb(${c.join(',')})`; };
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const smooth = (x) => { x = clamp(x); return x * x * (3 - 2 * x); };
const fmt = (n) => Math.round(n).toLocaleString('en-US');

/* ---------------- number theory ---------------- */
const LIM = 1000000;
const isP = new Uint8Array(LIM + 1).fill(1); isP[0] = isP[1] = 0;
for (let i = 2; i * i <= LIM; i++) if (isP[i]) for (let j = i * i; j <= LIM; j += i) isP[j] = 0;
const PI = new Int32Array(LIM + 1); { let c = 0; for (let i = 0; i <= LIM; i++) { if (isP[i]) c++; PI[i] = c; } }
const PR = []; for (let i = 2; i <= LIM; i++) if (isP[i]) PR.push(i);
const SMALL = PR.filter(p => p <= 47);
const distinct = (m) => { const f = []; let t = m; for (let p = 2; p * p <= t; p++) if (t % p === 0) { f.push(p); while (t % p === 0) t /= p; } if (t > 1) f.push(t); return f; };

/* ---------------- canvas helper ---------------- */
function fit(cv) {
  const dpr = Math.min(window.devicePixelRatio || 1, 1.75);
  const w = cv.clientWidth, h = cv.clientHeight;
  if (cv.width !== Math.round(w * dpr) || cv.height !== Math.round(h * dpr)) { cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); }
  const ctx = cv.getContext('2d'); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 1; ctx.shadowBlur = 0;
  ctx.fillStyle = K.bg; ctx.fillRect(0, 0, w, h);
  return { ctx, w, h };
}
const live = (id, text) => { const el = document.getElementById(id); if (el && el._t !== text) { el.innerHTML = text; el._t = text; } };

/* ---------------- the pulse ---------------- */
const pulse = { n: 1, flash: 0, lastPrime: 2 };
let prevPrime = 2, mel = 4;
const PENTA = [57, 60, 62, 64, 67, 69, 72, 74, 76, 79, 81];

/* ================= scenes ================= */
const SCENES = {};

/* Prologue: counting primes */
SCENES.count = {
  tempo: 80,
  draw(ctx, w, h, p) {
    const X = Math.round(100 * Math.pow(1000, smooth(p / .9)));
    const L = w * .08, R = w * .92, T = h * .24, B = h * .68;
    const li = (x) => { if (x < 2) return 0; const lx = Math.log(x); let s = 0.5772156649 + Math.log(lx), term = 1; for (let k = 1; k < 60; k++) { term *= lx / k; s += term / k; } return s; };
    const ymax = PI[X] * 1.12;
    const xs = (x) => L + (x / X) * (R - L), ys = (y) => B - (y / ymax) * (B - T);
    ctx.strokeStyle = rgba(K.ink, .18); ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(L, B); ctx.lineTo(R, B); ctx.moveTo(L, T - 10); ctx.lineTo(L, B); ctx.stroke();
    // Li(x) dashed, x/ln x blue, pi(x) bright staircase
    const steps = Math.round(R - L);
    ctx.setLineDash([5, 6]); ctx.strokeStyle = rgba(K.ink, .45); ctx.beginPath();
    for (let i = 1; i <= steps; i++) { const x = 2 + (X - 2) * i / steps; const y = ys(li(x) - li(2)); i === 1 ? ctx.moveTo(xs(x), y) : ctx.lineTo(xs(x), y); } ctx.stroke(); ctx.setLineDash([]);
    ctx.strokeStyle = K.wave; ctx.lineWidth = 2; ctx.beginPath();
    for (let i = 1; i <= steps; i++) { const x = 2 + (X - 2) * i / steps; const y = ys(x / Math.log(x)); i === 1 ? ctx.moveTo(xs(x), y) : ctx.lineTo(xs(x), y); } ctx.stroke();
    ctx.shadowColor = K.prime; ctx.shadowBlur = 14; ctx.strokeStyle = K.prime; ctx.lineWidth = 2.4; ctx.beginPath();
    let prev = 0; ctx.moveTo(xs(0), ys(0));
    for (let i = 1; i <= steps * 2; i++) { const x = X * i / (steps * 2), v = PI[Math.floor(x)]; ctx.lineTo(xs(x), ys(prev)); ctx.lineTo(xs(x), ys(v)); prev = v; }
    ctx.stroke(); ctx.shadowBlur = 0;
    ctx.font = FONT(12); ctx.fillStyle = K.dim; ctx.textAlign = 'center';
    for (let k = 0; k <= 4; k++) ctx.fillText(fmt(X * k / 4), xs(X * k / 4), B + 22);
    ctx.textAlign = 'left'; ctx.font = HAND(Math.max(18, w / 55));
    ctx.fillStyle = K.prime; ctx.fillText('π(x), the primes', xs(X * .72), ys(PI[Math.floor(X * .72)]) - 18);
    ctx.fillStyle = K.wave; ctx.fillText('x / ln x', xs(X * .82), ys(X * .82 / Math.log(X * .82)) + 34);
    const a = PI[X], g = X / Math.log(X), l = li(X) - li(2);
    live('live-count', `x       = ${fmt(X)}\nπ(x)    = <b>${fmt(a)}</b>\nx/ln x  = ${fmt(g)}   (${((g - a) / a * 100).toFixed(1)}%)\nLi(x)   = ${fmt(l)}   (+${((l - a) / a * 100).toFixed(1)}%)`);
  },
  audio() { Sound.setDrone([{ f: 55, g: .05 }, { f: 82.5, g: .03 }]); },
};

/* Act I: the prime wave (equation W(n)) */
SCENES.sieve = {
  tempo: 92,
  draw(ctx, w, h, p) {
    const idx = Math.round(smooth(p / .78) * 14), P = SMALL[idx], ctxP = SMALL.slice(0, idx + 1);
    const N = Math.round(150 + 250 * smooth(p / .9));
    const L = w * .05, R = w * .95, T = h * .26, B = h * .64, bw = (R - L) / N;
    const W = new Float64Array(N + 1); let mx = 1;
    for (let n = 2; n <= N; n++) { let s = 0; for (const q of ctxP) if (n % q === 0 && n !== q) s += 1 / Math.sqrt(q); W[n] = s; if (s > mx) mx = s; }
    const sy = (B - T) / mx;
    const cursor = 2 + (pulse.n % (N - 1));
    ctx.globalCompositeOperation = 'lighter';
    let nodes = 0, fp = 0, first = 0;
    for (let n = 2; n <= N; n++) {
      let y = B; const x = L + (n - 1) * bw;
      ctxP.forEach((q, i) => { if (n % q === 0 && n !== q) { const hh = sy / Math.sqrt(q); ctx.fillStyle = rgba(i < 4 ? K.wave : K.violet, .55 + .35 * (n === cursor)); ctx.fillRect(x + bw * .15, y - hh, Math.max(1, bw * .7), hh - .6); y -= hh; } });
      if (W[n] === 0) {
        nodes++; const r = Math.max(2.2, Math.min(5, bw * .45));
        if (isP[n]) { ctx.fillStyle = n === cursor ? '#FFFFFF' : K.prime; ctx.shadowColor = K.prime; ctx.shadowBlur = n === cursor ? 24 : 10; ctx.beginPath(); ctx.arc(x + bw / 2, B + 16, r, 0, 7); ctx.fill(); ctx.shadowBlur = 0; }
        else { fp++; if (!first) first = n; ctx.strokeStyle = K.ochre; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(x + bw / 2, B + 16, r + 2, 0, 7); ctx.stroke(); }
      }
    }
    ctx.globalCompositeOperation = 'source-over';
    // the travelling cursor of the pulse
    ctx.strokeStyle = rgba(K.ink, .35); ctx.beginPath(); ctx.moveTo(L + (cursor - .5) * bw, T - 10); ctx.lineTo(L + (cursor - .5) * bw, B + 30); ctx.stroke();
    ctx.font = FONT(12); ctx.fillStyle = K.dim; ctx.textAlign = 'center';
    const tk = N > 300 ? 50 : 25; for (let n = tk; n <= N; n += tk) ctx.fillText(n, L + (n - .5) * bw, B + 46);
    if (P * P <= N) {
      const x = L + P * P * bw; ctx.strokeStyle = K.ochre; ctx.setLineDash([4, 6]); ctx.beginPath(); ctx.moveTo(x, T - 30); ctx.lineTo(x, B + 30); ctx.stroke(); ctx.setLineDash([]);
      ctx.font = HAND(Math.max(18, w / 60)); ctx.fillStyle = K.ochre; ctx.textAlign = 'left'; ctx.fillText(`P² = ${P * P}`, Math.max(12, x - 110), B - 12);
    }
    const st = DATA.sieveStats.reduce((a, b) => Math.abs(b.ctx - P) < Math.abs(a.ctx - P) ? b : a);
    live('live-sieve', `waves from  {${ctxP.length > 6 ? ctxP.slice(0, 5).join(', ') + ', … ' + P : ctxP.join(', ')}}\nnodes       ${nodes}\nprimes      <b>${nodes - fp}</b>\nslipped     ${fp}${first ? '   first ' + first : ''}\n\nup to 100,000 with P ≈ ${st.ctx}:\n${fmt(st.fp)} composites slip through`);
    this._P = ctxP;
  },
  audio() { const ps = this._P || [2]; Sound.setDrone(ps.slice(0, 12).map((q, i) => ({ f: 55 * q / (q > 11 ? 4 : 1) * (q > 31 ? .5 : 1), g: .07 / Math.sqrt(i + 1) }))); },
};

/* Act I: continuous waves */
SCENES.smooth = {
  tempo: 96,
  draw(ctx, w, h, p, T) {
    const idx = Math.round(smooth(p / .5) * 8), ps = SMALL.slice(0, idx + 1), mode = smooth((p - .5) / .15);
    const M = 72, L = w * .05, R = w * .95, top = h * .26, base = h * .64;
    const prod = (x) => Math.pow(ps.reduce((a, q) => a * Math.abs(Math.sin(Math.PI * x / q)), 1), 1 / ps.length);
    const cos = (x) => ps.reduce((a, q) => a + (1 + Math.cos(2 * Math.PI * x / q)) / 2, 0) / ps.length;
    const f = (x) => (1 - mode) * prod(x) + mode * cos(x);
    const X = (x) => L + (x / M) * (R - L), Y = (v) => base - v * (base - top);
    const steps = Math.round((R - L) * 1.5);
    ctx.beginPath(); for (let i = 0; i <= steps; i++) { const x = i / steps * M; i ? ctx.lineTo(X(x), Y(f(x))) : ctx.moveTo(X(x), Y(f(x))); }
    ctx.lineTo(X(M), base); ctx.lineTo(X(0), base); ctx.closePath();
    const g = ctx.createLinearGradient(0, top, 0, base); g.addColorStop(0, rgba(K.wave, .35)); g.addColorStop(1, rgba(K.wave, 0)); ctx.fillStyle = g; ctx.fill();
    ctx.shadowColor = K.wave; ctx.shadowBlur = 16; ctx.strokeStyle = K.wave; ctx.lineWidth = 2.2; ctx.beginPath();
    for (let i = 0; i <= steps; i++) { const x = i / steps * M; i ? ctx.lineTo(X(x), Y(f(x))) : ctx.moveTo(X(x), Y(f(x))); } ctx.stroke(); ctx.shadowBlur = 0;
    let esc = 0, slip = 0;
    for (let n = 2; n <= M; n++) {
      const hit = ps.some(q => n % q === 0), x = X(n), y = Y(hit && mode < .5 ? 0 : f(n));
      if (isP[n] && !hit) { esc++; ctx.fillStyle = K.prime; ctx.shadowColor = K.prime; ctx.shadowBlur = 12; ctx.beginPath(); ctx.arc(x, y, 4.5, 0, 7); ctx.fill(); ctx.shadowBlur = 0; }
      else if (!isP[n] && !hit) { slip++; ctx.strokeStyle = K.ochre; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(x, y, 5, 0, 7); ctx.stroke(); }
      else { ctx.fillStyle = rgba(K.ink, .3); ctx.beginPath(); ctx.arc(x, y, 2, 0, 7); ctx.fill(); }
    }
    ctx.font = FONT(12); ctx.fillStyle = K.dim; ctx.textAlign = 'center'; for (let n = 0; n <= M; n += 12) ctx.fillText(n, X(n), base + 26);
    live('live-smooth', `waves from  {${ps.join(', ')}}\nshape       ${mode < .5 ? 'product of sines' : 'sum of cosines'}\nprimes escape   <b>${esc}</b>\ncomposites slip ${slip}\nrepeats every   ${fmt(ps.reduce((a, b) => a * b, 1))}`);
    this._ps = ps;
  },
  audio() { const ps = this._ps || [2]; Sound.setDrone(ps.map((q, i) => ({ f: 55 * q, g: .06 / Math.sqrt(i + 1) }))); },
};

/* Act II: Z(n) on the unit circle */
const ZN = (() => { const N = 3000, a = new Array(N + 1); for (let n = 2; n <= N; n++) { const f = distinct(n); let re = 0, im = 0; for (const q of f) { re += Math.cos(q * Math.log(n)); im += Math.sin(q * Math.log(n)); } a[n] = [re, im, f.length]; } return a; })();
SCENES.zn = {
  tempo: 104,
  draw(ctx, w, h, p, T) {
    const N = Math.round(30 + 2970 * smooth(p / .55)), reveal = smooth((p - .58) / .12);
    const cx = w * .5, cy = h * .44, sc = Math.min(w * .4, h * .38) / 3;
    ctx.strokeStyle = rgba(K.ink, .1); ctx.lineWidth = 1; for (const r of [2, 3]) { ctx.beginPath(); ctx.arc(cx, cy, r * sc, 0, 7); ctx.stroke(); }
    ctx.beginPath(); ctx.moveTo(cx - 3.3 * sc, cy); ctx.lineTo(cx + 3.3 * sc, cy); ctx.moveTo(cx, cy - 3.3 * sc); ctx.lineTo(cx, cy + 3.3 * sc); ctx.stroke();
    ctx.shadowColor = K.prime; ctx.shadowBlur = 18; ctx.strokeStyle = rgba(K.prime, .7); ctx.lineWidth = 1.6; ctx.beginPath(); ctx.arc(cx, cy, sc, 0, 7); ctx.stroke(); ctx.shadowBlur = 0;
    ctx.globalCompositeOperation = 'lighter';
    let np = 0, npp = 0;
    for (let n = 2; n <= N; n++) {
      const [a, b, k] = ZN[n], x = cx + a * sc, y = cy - b * sc;
      if (isP[n]) { np++; ctx.fillStyle = rgba(K.prime, .85); ctx.beginPath(); ctx.arc(x, y, 2.6, 0, 7); ctx.fill(); }
      else if (k === 1) { npp++; const pulseR = 4 + reveal * (3 + 2 * Math.sin(T * 4 + n)); ctx.strokeStyle = rgba(K.ochre, .35 + .65 * reveal); ctx.lineWidth = 1.2 + reveal; ctx.beginPath(); ctx.arc(x, y, pulseR, 0, 7); ctx.stroke(); }
      else { ctx.fillStyle = k === 2 ? rgba(K.wave, .55) : rgba(K.violet, .6); ctx.fillRect(x - 1.1, y - 1.1, 2.2, 2.2); }
    }
    ctx.globalCompositeOperation = 'source-over';
    const cur = pulse.n % N + 2; if (ZN[cur]) { const [a, b] = ZN[cur]; ctx.strokeStyle = rgba(K.ink, .6); ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + a * sc, cy - b * sc); ctx.stroke(); }
    if (reveal > 0) { ctx.globalAlpha = reveal; ctx.font = HAND(Math.max(20, w / 48)); ctx.fillStyle = K.ochre; ctx.textAlign = 'center'; ctx.fillText('4, 8, 9, 16, 25, 27, 32 … also on the circle', cx, cy - 3.05 * sc); ctx.globalAlpha = 1; }
    live('live-zn', `n ≤ ${fmt(N)}\nprimes on |z| = 1        <b>${fmt(np)}</b>\nprime powers on |z| = 1  ${npp}\ntwo distinct factors     ${fmt(ZN.slice(2, N + 1).filter(z => z[2] === 2).length)}\nthree or more            ${fmt(ZN.slice(2, N + 1).filter(z => z[2] >= 3).length)}`);
  },
  pitch(n) { const z = ZN[(n % 2999) + 2]; return PENTA[Math.floor(((Math.atan2(z[1], z[0]) / (2 * Math.PI)) + 1) % 1 * PENTA.length)]; },
  audio() { Sound.setDrone([{ f: 110, g: .03 }, { f: 165, g: .02 }]); },
};

/* Act II: spirals morphing Sacks -> golden -> Ulam */
const SP = (() => {
  const N = 30000, PHI = (1 + Math.sqrt(5)) / 2, GA = 2 * Math.PI / (PHI * PHI);
  const sacks = new Float32Array(2 * (N + 1)), gold = new Float32Array(2 * (N + 1)), ulam = new Float32Array(2 * (N + 1));
  const um = (n) => { if (n === 1) return [0, 0]; const k = Math.ceil((Math.sqrt(n) - 1) / 2); let t = 2 * k + 1, m = t * t; t -= 1; if (n >= m - t) return [k - (m - n), -k]; m -= t; if (n >= m - t) return [-k, -k + (m - n)]; m -= t; if (n >= m - t) return [-k + (m - n), k]; return [k, k - (m - n - t)]; };
  const half = Math.sqrt(N) / 2;
  for (let n = 1; n <= N; n++) {
    const r = Math.sqrt(n / N), th = 2 * Math.PI * Math.sqrt(n); sacks[2 * n] = r * Math.cos(th); sacks[2 * n + 1] = r * Math.sin(th);
    const r2 = n / N, th2 = n * GA; gold[2 * n] = r2 * Math.cos(th2); gold[2 * n + 1] = r2 * Math.sin(th2);
    const [a, b] = um(n); ulam[2 * n] = a / half; ulam[2 * n + 1] = b / half;
  }
  const euler = new Set(); for (let k = 0; k < 200; k++) euler.add(k * k + k + 41);
  return { N, sacks, gold, ulam, euler };
})();
SCENES.spiral = {
  tempo: 108,
  draw(ctx, w, h, p, T) {
    let A = SP.sacks, B = SP.sacks, m = 0, label = 'Sacks spiral · r = √n, θ = 2π√n';
    if (p < .38) { } else if (p < .54) { B = SP.gold; m = smooth((p - .38) / .16); label = 'Sacks → golden angle'; }
    else if (p < .68) { A = B = SP.gold; label = 'Golden angle · θ = n · 137.5°'; }
    else if (p < .84) { A = SP.gold; B = SP.ulam; m = smooth((p - .68) / .16); label = 'golden angle → Ulam square'; }
    else { A = B = SP.ulam; label = 'Ulam spiral, 1963'; }
    const spin = (A === SP.ulam && B === SP.ulam) ? 0 : T * .015 * (1 - (B === SP.ulam ? m : 0));
    const cx = w * .5, cy = h * .45, R = Math.min(w * .48, h * .44), cs = Math.cos(spin), sn = Math.sin(spin);
    const eul = p > .12 && p < .4 ? smooth((p - .12) / .08) * (1 - smooth((p - .34) / .06)) : 0;
    const dot = Math.max(1.3, R / Math.sqrt(SP.N) * 1.05);
    ctx.globalCompositeOperation = 'lighter';
    ctx.fillStyle = rgba(K.wave, .07);
    for (let n = 2; n <= SP.N; n++) { if (isP[n]) continue; const x = A[2 * n] + (B[2 * n] - A[2 * n]) * m, y = A[2 * n + 1] + (B[2 * n + 1] - A[2 * n + 1]) * m; ctx.fillRect(cx + (x * cs - y * sn) * R, cy - (x * sn + y * cs) * R, dot * .8, dot * .8); }
    const hit = pulse.lastPrime;
    for (let n = 2; n <= SP.N; n++) {
      if (!isP[n]) continue;
      const x = A[2 * n] + (B[2 * n] - A[2 * n]) * m, y = A[2 * n + 1] + (B[2 * n + 1] - A[2 * n + 1]) * m;
      const X = cx + (x * cs - y * sn) * R, Y = cy - (x * sn + y * cs) * R;
      if (eul && SP.euler.has(n)) { ctx.fillStyle = rgba(K.violet, eul); ctx.beginPath(); ctx.arc(X, Y, dot + 2.5, 0, 7); ctx.fill(); }
      else { ctx.fillStyle = rgba(K.prime, .78); ctx.fillRect(X - dot / 2, Y - dot / 2, dot, dot); }
      if (n === hit && hit <= SP.N) { ctx.strokeStyle = rgba('#FFFFFF', .9); ctx.lineWidth = 1.5; ctx.beginPath(); ctx.arc(X, Y, 9 + pulse.flash * 10, 0, 7); ctx.stroke(); }
    }
    ctx.globalCompositeOperation = 'source-over';
    if (eul > 0) { ctx.globalAlpha = eul; ctx.font = HAND(Math.max(20, w / 50)); ctx.fillStyle = K.violet; ctx.textAlign = 'left'; ctx.fillText('n² + n + 41', cx + R * .55, cy - R * .78); ctx.globalAlpha = 1; }
    const sl = document.getElementById('spiral-label'); if (sl && sl.textContent !== label) sl.textContent = label;
    live('live-spiral', `integers   1 … ${fmt(SP.N)}\nprimes     <b>${fmt(PI[SP.N])}</b>${eul > .5 ? '\nEuler n² + n + 41: prime for n = 0 … 39' : ''}`);
  },
  audio() { Sound.setDrone([{ f: 98, g: .03 }, { f: 147, g: .02 }, { f: 196, g: .015 }]); },
};

/* Act III: bits, machines, formulas */
const BITS = (() => {
  const truth = []; for (let k = 1; k <= 1000; k++) truth.push([isP[10 * k + 1], isP[10 * k + 3]]);
  const bm = (s) => { let C = [1], B = [1], L = 0, m = -1; for (let n = 0; n < s.length; n++) { let d = s[n]; for (let i = 1; i <= L; i++) if (i < C.length && C[i]) d ^= s[n - i]; if (!d) continue; const T = C.slice(), sh = new Array(n - m).fill(0).concat(B); while (C.length < sh.length) C.push(0); const len = Math.min(C.length, sh.length); C = C.slice(0, len).map((c, i) => c ^ sh[i]); if (2 * L <= n) { L = n + 1 - L; B = T; m = n; } } const taps = []; for (let i = 1; i < C.length; i++) if (C[i] === 1) taps.push(i); return taps; };
  const ext = (seq, taps, k) => { for (let j = 0; j < k; j++) { let x = 0; for (const i of taps) x ^= seq[seq.length - i]; seq.push(x); } return seq; };
  const A = truth.slice(0, 100).map(q => q[0]), Bc = truth.slice(0, 100).map(q => q[1]);
  const ga = ext(A.slice(), bm(A.slice()), 900), gb = ext(Bc.slice(), bm(Bc.slice()), 900);
  const gem = [[1, 1], [0, 1]]; const v2 = (k) => { let c = 0; while (k % 2 === 0) { k /= 2; c++; } return c; };
  for (let i = 2; i < 1000; i++) { const a = gem[i - 1], b = gem[i - 2]; let x = (a[0] + b[0]) % 2, y = (a[1] + b[1]) % 2; if (i >= 8) { const v = v2(i + 1); x = (x + v % 2) % 2; y = (y + (((v - 1) % 2) + 2) % 2) % 2; } gem.push([x, y]); }
  const score = (f, a, b) => { let s = 0; for (let i = a; i < b; i++) if (f(i)[0] === truth[i][0] && f(i)[1] === truth[i][1]) s++; return s / (b - a); };
  return [['GPT recurrence', score(i => [ga[i], gb[i]], 0, 100), score(i => [ga[i], gb[i]], 100, 1000)], ['Gemini rule', score(i => gem[i], 0, 100), score(i => gem[i], 100, 1000)], ['always guess zero', score(() => [0, 0], 0, 100), score(() => [0, 0], 100, 1000)]];
})();
SCENES.bits = {
  tempo: 116,
  draw(ctx, w, h, p) {
    const fill = smooth(p / .3), bars = smooth((p - .32) / .18) * (1 - smooth((p - .78) / .08)), nth = smooth((p - .82) / .08);
    // barcode
    const cols = 60, rows = 20, gw = Math.min(w * .9, h * 1.35), gh = gw / 3, x0 = (w - gw) / 2, y0 = h * .24, cw = gw / cols, rh = gh / rows;
    const shown = Math.round(1200 * fill), fade = 1 - .78 * smooth((p - .3) / .1);
    ctx.globalAlpha = fade;
    for (let k = 1; k <= shown; k++) {
      const a = isP[6 * k - 1], b = isP[6 * k + 1], c = (k - 1) % cols, r = Math.floor((k - 1) / cols), x = x0 + c * cw, y = y0 + r * rh, hh = (rh - 2) / 2;
      const col = a && b ? K.prime : K.wave;
      ctx.fillStyle = a ? col : rgba(K.ink, .06); ctx.fillRect(x + .6, y, cw - 1.2, hh);
      ctx.fillStyle = b ? col : rgba(K.ink, .06); ctx.fillRect(x + .6, y + hh + 1, cw - 1.2, hh);
    }
    ctx.globalAlpha = 1;
    if (bars > 0) {
      ctx.globalAlpha = bars; const bx = w * .1, bW = w * .62, by = h * .2;
      ctx.font = FONT(13); ctx.textAlign = 'left';
      ctx.fillStyle = K.dim; ctx.fillText('first 100 pairs, fitted', bx, by - 10); ctx.fillStyle = K.prime; ctx.fillText('next 900 pairs, unseen', bx + 260, by - 10);
      BITS.forEach((r, i) => {
        const y = by + 20 + i * h * .13; ctx.fillStyle = K.ink; ctx.font = HAND(Math.max(20, w / 50)); ctx.fillText(r[0], bx, y + 6);
        [[r[1], rgba(K.ink, .55)], [r[2], K.prime]].forEach(([v, c], j) => { const yy = y + 18 + j * 16; ctx.fillStyle = rgba(K.ink, .08); ctx.fillRect(bx, yy, bW, 11); ctx.fillStyle = c; ctx.fillRect(bx, yy, bW * v * smooth((p - .32) / .2 + .2), 11); ctx.fillStyle = K.ink; ctx.font = FONT(13); ctx.fillText(Math.round(v * 100) + '%', bx + bW + 12, yy + 10); });
      });
      ctx.globalAlpha = 1;
    }
    if (nth > 0) {
      ctx.globalAlpha = nth; const n = 1e5, act = 1299709, Ln = Math.log(n), LL = Math.log(Ln);
      const rows2 = [['my evolved formula', (1284917.04 - act) / act, K.prime], ['n (ln n + ln ln n − 1)', (n * (Ln + LL - 1) - act) / act, K.wave], ['Cipolla, 1902', (n * (Ln + LL - 1 + (LL - 2) / Ln) - act) / act, K.green]];
      const bx = w * .1, bW = w * .6, by = h * .26;
      ctx.font = FONT(13); ctx.fillStyle = K.dim; ctx.textAlign = 'left'; ctx.fillText('error in the 100,000th prime (1,299,709)', bx, by - 14);
      rows2.forEach((r, i) => { const y = by + 10 + i * h * .1; ctx.font = HAND(Math.max(20, w / 50)); ctx.fillStyle = K.ink; ctx.fillText(r[0], bx, y + 4); ctx.fillStyle = r[2]; ctx.fillRect(bx, y + 16, Math.max(3, bW * Math.abs(r[1]) / .012), 12); ctx.font = FONT(13); ctx.fillStyle = K.ink; ctx.fillText((r[1] * 100).toFixed(3) + '%', bx + Math.max(3, bW * Math.abs(r[1]) / .012) + 12, y + 27); });
      ctx.globalAlpha = 1;
    }
    let tw = 0; for (let k = 1; k <= shown; k++) if (isP[6 * k - 1] && isP[6 * k + 1]) tw++;
    live('live-bits', p < .32 ? `pairs drawn   ${fmt(shown)}\ntwin primes   <b>${tw}</b>` : p < .82 ? `fitted   GPT ${Math.round(BITS[0][1] * 100)}%  Gemini ${Math.round(BITS[1][1] * 100)}%\nunseen   GPT <b>${Math.round(BITS[0][2] * 100)}%</b>  Gemini <b>${Math.round(BITS[1][2] * 100)}%</b>\nguess zero  ${Math.round(BITS[2][2] * 100)}%` : `evolved formula   −1.14%\ntwo-term PNT      −0.31%\nCipolla 1902      <b>−0.017%</b>`);
  },
  audio() { Sound.setDrone([{ f: 73.4, g: .03 }]); },
};

/* Act III: Game of Life on the hex seed */
const LIFE = (() => {
  const S = 48; let bits = ''; for (const ch of GOLHEX) bits += parseInt(ch, 16).toString(2).padStart(4, '0');
  const gens = [Uint8Array.from(bits.slice(0, S * S), b => +b)];
  const step = (g) => { const n = new Uint8Array(S * S); for (let i = 0; i < S; i++) for (let j = 0; j < S; j++) { let c = 0; for (let di = -1; di <= 1; di++) for (let dj = -1; dj <= 1; dj++) if (di || dj) c += g[((i + di + S) % S) * S + (j + dj + S) % S]; const a = g[i * S + j]; n[i * S + j] = (a && (c === 2 || c === 3)) || (!a && c === 3) ? 1 : 0; } return n; };
  return { S, get(k) { while (gens.length <= k) gens.push(step(gens[gens.length - 1])); return gens[k]; } };
})();
SCENES.life = {
  tempo: 124,
  draw(ctx, w, h, p) {
    const gen = Math.round(p * 420), g = LIFE.get(gen), S = LIFE.S;
    const side = Math.min(w * .6, h * .64), cs = side / S, x0 = (w - side) / 2, y0 = h * .08;
    ctx.strokeStyle = rgba(K.ink, .08); ctx.strokeRect(x0 - 1, y0 - 1, side + 2, side + 2);
    ctx.shadowColor = K.prime; ctx.shadowBlur = 8; ctx.fillStyle = K.prime; let pop = 0;
    for (let i = 0; i < S; i++) for (let j = 0; j < S; j++) if (g[i * S + j]) { pop++; ctx.fillRect(x0 + j * cs + 1, y0 + i * cs + 1, cs - 2, cs - 2); }
    ctx.shadowBlur = 0;
    live('live-life', `generation  <b>${gen}</b>\nlive cells  ${pop} of ${S * S}\nseed        first 2,304 bits of FA57A5BA…`);
    this._pop = pop;
  },
  audio() { Sound.setDrone([{ f: 55, g: .02 + .00004 * (this._pop || 0) }]); },
};

/* Act IV: the 3-D rotation walk, with the gap melody */
const WALK = (() => {
  let pos = [0, 0, 0], dir = [1, 0, 0]; const P3 = [pos.slice()]; const ps = PR.filter(q => q >= 11 && q <= 20000);
  const rot = (v, ax, a) => { const c = Math.cos(a), s = Math.sin(a); return ax === 'y' ? [c * v[0] + s * v[2], v[1], -s * v[0] + c * v[2]] : [c * v[0] - s * v[1], s * v[0] + c * v[1], v[2]]; };
  for (let i = 0; i + 1 < ps.length; i++) { const gc = ps[i + 1] - ps[i] - 1; for (let k = 0; k < gc; k++) { pos = [pos[0] + dir[0], pos[1] + dir[1], pos[2] + dir[2]]; P3.push(pos); } const d = ps[i + 1] % 10; dir = rot(dir, (d === 1 || d === 7) ? 'y' : 'z', ((d === 1 || d === 3) ? 1 : -1) * gc); }
  let cx = 0, cy = 0, cz = 0; for (const q of P3) { cx += q[0]; cy += q[1]; cz += q[2]; } cx /= P3.length; cy /= P3.length; cz /= P3.length;
  const ds = P3.map(q => Math.hypot(q[0] - cx, q[1] - cy, q[2] - cz)).sort((a, b) => a - b);
  const melody = new Map(); let note = 60; for (let i = 0; i + 1 < PR.length && PR[i] < 200000; i++) { melody.set(PR[i], note); note += Math.min(PR[i + 1] - PR[i], 12); if (note > 84) note = 60 + ((note - 60) % 24); }
  return { P3, c: [cx, cy, cz], r: ds[Math.floor(ds.length * .9)] * 1.1, melody };
})();
SCENES.walk = {
  tempo: 100,
  draw(ctx, w, h, p, T) {
    const n = Math.max(2, Math.round(WALK.P3.length * smooth(p / .82)));
    const yaw = .5 + p * 4.2 + T * .03, pitch = .35 + .15 * Math.sin(p * 3);
    const cyw = Math.cos(yaw), syw = Math.sin(yaw), cp = Math.cos(pitch), sp = Math.sin(pitch), sc = Math.min(w * .7, h * .62) / WALK.r, [ox, oy, oz] = WALK.c;
    const proj = (q) => { const x = q[0] - ox, y = q[1] - oy, z = q[2] - oz; const x1 = cyw * x + syw * z, z1 = -syw * x + cyw * z; const y1 = cp * y - sp * z1, z2 = sp * y + cp * z1; const f = 1 / (1 + z2 / (WALK.r * 4)); return [w / 2 + x1 * sc * f, h * .44 - y1 * sc * f]; };
    ctx.globalCompositeOperation = 'lighter'; ctx.lineWidth = 1.2;
    const seg = 48, per = Math.ceil(n / seg);
    for (let s = 0; s < seg; s++) { const i0 = s * per, i1 = Math.min(n - 1, (s + 1) * per); if (i0 >= i1) break; ctx.strokeStyle = rgba(s / seg < .5 ? K.violet : K.prime, .5); ctx.strokeStyle = mix(K.violet, K.prime, s / seg); ctx.globalAlpha = .7; ctx.beginPath(); for (let i = i0; i <= i1; i++) { const [x, y] = proj(WALK.P3[i]); i === i0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y); } ctx.stroke(); }
    ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
    const [hx, hy] = proj(WALK.P3[n - 1]); ctx.fillStyle = '#FFFFFF'; ctx.shadowColor = K.prime; ctx.shadowBlur = 20 + 20 * pulse.flash; ctx.beginPath(); ctx.arc(hx, hy, 4, 0, 7); ctx.fill(); ctx.shadowBlur = 0;
    live('live-walk', `steps walked   ${fmt(n)}\nprimes passed  <b>${fmt(Math.max(0, PI[Math.min(20000, n + 10)] - 4))}</b>\nnote now       ${['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][(WALK.melody.get(pulse.lastPrime) || 60) % 12]}`);
  },
  pitch(n) { return WALK.melody.get(n) || 60; },
  restOnComposite: true,
  audio() { Sound.setDrone([{ f: 65.4, g: .035 }, { f: 98, g: .02 }]); },
};

/* Act V: the zeta spiral */
SCENES.zeta = {
  tempo: 84, scale: 1,
  draw(ctx, w, h, p) {
    const t = 10 + 25 * smooth(p / .92), s = .5;
    const NMAX = 1500, pts = [], raw = []; let re = 0, im = 0;
    const or = 1 - s, oi = -t, od = or * or + oi * oi;
    for (let n = 1; n <= NMAX; n++) {
      const ln = Math.log(n), m = Math.exp(-s * ln); re += m * Math.cos(-t * ln); im += m * Math.sin(-t * ln); raw.push([re, im]);
      const m1 = Math.exp(or * ln), ar = m1 * Math.cos(oi * ln), ai = m1 * Math.sin(oi * ln);
      pts.push([re - (ar * or + ai * oi) / od - .5 * m * Math.cos(-t * ln), im - (ai * or - ar * oi) / od - .5 * m * Math.sin(-t * ln)]);
    }
    const [zr, zi] = zetaC(s, t);
    let mx = Math.hypot(zr, zi) + .25; for (const q of raw.slice(0, 120)) mx = Math.max(mx, Math.hypot(q[0] - zr, q[1] - zi));
    const target = Math.min(w * .46, h * .4) / Math.min(mx, 4); this.scale += (target - this.scale) * .08; const sc = this.scale;
    const cx = w / 2 - zr * sc * .5, cy = h * .44 + zi * sc * .5;
    const X = (q) => cx + q[0] * sc, Y = (q) => cy - q[1] * sc;
    ctx.strokeStyle = rgba(K.ink, .08); ctx.beginPath(); ctx.moveTo(0, cy); ctx.lineTo(w, cy); ctx.moveTo(cx, 0); ctx.lineTo(cx, h); ctx.stroke();
    ctx.strokeStyle = rgba(K.ink, .22); ctx.lineWidth = 1; ctx.beginPath(); raw.slice(0, 160).forEach((q, i) => i ? ctx.lineTo(X(q), Y(q)) : ctx.moveTo(X(q), Y(q))); ctx.stroke();
    ctx.globalCompositeOperation = 'lighter'; ctx.lineWidth = 1.7;
    for (let i = 1; i < pts.length; i++) { ctx.strokeStyle = mix(K.wave, K.violet, Math.min(1, Math.log(i + 1) / Math.log(NMAX))); ctx.beginPath(); ctx.moveTo(X(pts[i - 1]), Y(pts[i - 1])); ctx.lineTo(X(pts[i]), Y(pts[i])); ctx.stroke(); }
    ctx.globalCompositeOperation = 'source-over';
    const mag = Math.hypot(zr, zi);
    ctx.strokeStyle = mag < .06 ? K.prime : rgba(K.ink, .7); ctx.lineWidth = 1.6; ctx.beginPath(); ctx.arc(cx, cy, 9 + (mag < .06 ? 6 * pulse.flash : 0), 0, 7); ctx.stroke();
    ctx.shadowColor = K.prime; ctx.shadowBlur = 24; ctx.fillStyle = K.prime; ctx.beginPath(); ctx.arc(cx + zr * sc, cy - zi * sc, 6, 0, 7); ctx.fill(); ctx.shadowBlur = 0;
    ctx.font = HAND(Math.max(22, w / 44)); ctx.fillStyle = K.prime; ctx.textAlign = 'left'; ctx.fillText('ζ(s)', cx + zr * sc + 14, cy - zi * sc - 12);
    ctx.fillStyle = K.ink; ctx.fillText('0', cx - 26, cy + 30);
    const passed = ZEROS.filter(z => z <= t);
    if (this._t !== undefined) for (const z of ZEROS) if (z > Math.min(this._t, t) && z <= Math.max(this._t, t)) Sound.bell(196 * z / ZEROS[0], 1);
    this._t = t; this._mag = mag;
    live('live-zeta', `s      = ½ + ${t.toFixed(4)} i\nζ(s)   = ${zr.toFixed(4)} ${zi < 0 ? '−' : '+'} ${Math.abs(zi).toFixed(4)} i\n|ζ(s)| = <b>${mag.toFixed(4)}</b>${passed.length ? `\nzeros passed: ${passed.map(z => z.toFixed(2)).join(', ')}` : ''}`);
  },
  audio() { const m = this._mag || 1; Sound.setDrone([{ f: 110, g: .07 * Math.min(1, m) }, { f: 164.8, g: .045 * Math.min(1, m) }, { f: 220 * (1 + Math.min(m, 3) * .05), g: .03 * Math.min(1, m) }], .15); },
};

/* Act V: domain colouring of zeta, panning up the critical strip */
const DOMAIN = (() => {
  const T0 = 0, T1 = 120, S0 = -2, S1 = 3, W = 2400, H = 150;
  const cv = document.createElement('canvas'); cv.width = W; cv.height = H; const g = cv.getContext('2d');
  const img = g.createImageData(W, H); let col = 0, done = false;
  const hsl = (h, s, l) => { const k = (n) => (n + h * 12) % 12, a = s * Math.min(l, 1 - l); const f = (n) => l - a * Math.max(-1, Math.min(k(n) - 3, 9 - k(n), 1)); return [f(0) * 255, f(8) * 255, f(4) * 255]; };
  function work(ms) {
    const t0 = performance.now();
    while (col < W && performance.now() - t0 < ms) {
      const t = T0 + (col + .5) / W * (T1 - T0);
      for (let r = 0; r < H; r++) {
        const sg = S1 - (r + .5) / H * (S1 - S0); let [zr, zi] = zetaC(sg, t); if (!isFinite(zr) || !isFinite(zi)) { zr = 1e9; zi = 0; }
        const arg = Math.atan2(zi, zr), lm = Math.log2(Math.hypot(zr, zi) + 1e-300), band = lm - Math.floor(lm);
        const [R, G, B] = hsl(((arg / (2 * Math.PI)) + 1) % 1, .62, lm < -12 ? .04 : .2 + .32 * (1 - Math.pow(band, .55)));
        const i = (r * W + col) * 4; img.data[i] = R; img.data[i + 1] = G; img.data[i + 2] = B; img.data[i + 3] = 255;
      }
      col++;
    }
    g.putImageData(img, 0, 0); if (col >= W) done = true;
  }
  return { T0, T1, S0, S1, W, H, cv, work, get done() { return done; }, get col() { return col; } };
})();
SCENES.domain = {
  tempo: 80,
  near() { if (!DOMAIN.done) DOMAIN.work(10); },
  draw(ctx, w, h, p) {
    if (!DOMAIN.done) DOMAIN.work(14);
    const band = h * .58, y0 = h * .1, unit = band / (DOMAIN.S1 - DOMAIN.S0), span = w / unit;
    const tStart = (DOMAIN.T1 - span) * smooth(p), sx = (tStart - DOMAIN.T0) / (DOMAIN.T1 - DOMAIN.T0) * DOMAIN.W, sw = span / (DOMAIN.T1 - DOMAIN.T0) * DOMAIN.W;
    ctx.imageSmoothingEnabled = true; ctx.drawImage(DOMAIN.cv, sx, 0, sw, DOMAIN.H, 0, y0, w, band);
    const Y = (sg) => y0 + (DOMAIN.S1 - sg) / (DOMAIN.S1 - DOMAIN.S0) * band, X = (t) => (t - tStart) * unit;
    ctx.strokeStyle = rgba('#FFFFFF', .85); ctx.setLineDash([7, 7]); ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(0, Y(.5)); ctx.lineTo(w, Y(.5)); ctx.stroke(); ctx.setLineDash([]);
    ctx.strokeStyle = rgba('#FFFFFF', .25); for (const sg of [0, 1]) { ctx.beginPath(); ctx.moveTo(0, Y(sg)); ctx.lineTo(w, Y(sg)); ctx.stroke(); }
    ctx.font = FONT(12); ctx.fillStyle = K.ink; ctx.textAlign = 'left'; ctx.fillText('σ = ½', 12, Y(.5) - 8); ctx.fillText('σ = 1', 12, Y(1) - 6); ctx.fillText('σ = 0', 12, Y(0) - 6);
    ctx.textAlign = 'center'; for (let t = Math.ceil(tStart / 5) * 5; t < tStart + span; t += 5) ctx.fillText(`${t}i`, X(t), y0 + band + 22);
    const vis = ZEROS.filter(z => z > tStart && z < tStart + span);
    ctx.font = HAND(Math.max(16, w / 70));
    vis.forEach((z, i) => { ctx.fillStyle = '#FFFFFF'; ctx.shadowColor = '#000'; ctx.shadowBlur = 6; ctx.beginPath(); ctx.arc(X(z), Y(.5), 3.5, 0, 7); ctx.fill(); ctx.fillText(z.toFixed(2), X(z), Y(.5) - 14 - (i % 2) * 22); ctx.shadowBlur = 0; });
    const mid = tStart + span / 2; if (this._mid !== undefined) for (const z of ZEROS) if (z > Math.min(this._mid, mid) && z <= Math.max(this._mid, mid)) Sound.bell(220 * Math.pow(2, ((z * 7) % 12) / 12), .7); this._mid = mid;
    live('live-domain', `t from ${tStart.toFixed(1)} to ${(tStart + span).toFixed(1)}\nzeros in view  <b>${vis.length}</b>, all on σ = ½\n${DOMAIN.done ? '' : `painting… ${Math.round(DOMAIN.col / DOMAIN.W * 100)}%`}`);
  },
  audio() { Sound.setDrone([{ f: 55, g: .04 }, { f: 82.4, g: .025 }, { f: 110, g: .02 }]); },
};

/* Act V: the explicit formula; each zero is a tone */
const psi = (() => { const a = new Float64Array(130); for (let x = 2; x < 130; x++) { let s = 0; for (const q of PR) { if (q > x) break; let r = q; while (r <= x) { s += Math.log(q); r *= q; } } a[x] = s; } return a; })();
SCENES.explicit = {
  tempo: 90, cache: {},
  draw(ctx, w, h, p) {
    const K0 = p < .08 ? 0 : Math.min(1000, Math.round(Math.pow(10, 3 * smooth((p - .08) / .78))));
    const XM = 60, L = w * .07, R = w * .95, T = h * .24, B = h * .66, x0 = 2, top = XM * 1.1;
    const X = (x) => L + (x - x0) / (XM - x0) * (R - L), Y = (v) => B - v / top * (B - T);
    ctx.strokeStyle = rgba(K.ink, .15); ctx.beginPath(); ctx.moveTo(L, B); ctx.lineTo(R, B); ctx.moveTo(L, T - 10); ctx.lineTo(L, B); ctx.stroke();
    ctx.setLineDash([4, 6]); ctx.strokeStyle = rgba(K.ink, .35); ctx.beginPath(); ctx.moveTo(X(x0), Y(x0)); ctx.lineTo(X(XM), Y(XM)); ctx.stroke(); ctx.setLineDash([]);
    ctx.shadowColor = K.prime; ctx.shadowBlur = 16; ctx.strokeStyle = K.prime; ctx.lineWidth = 2.6; ctx.beginPath(); let prev = psi[2]; ctx.moveTo(X(2), Y(prev));
    for (let n = 3; n <= XM; n++) { if (psi[n] !== prev) { ctx.lineTo(X(n), Y(prev)); ctx.lineTo(X(n), Y(psi[n])); prev = psi[n]; } } ctx.lineTo(X(XM), Y(prev)); ctx.stroke(); ctx.shadowBlur = 0;
    const key = K0 + '|' + Math.round(R - L);
    if (!this.cache[key]) {
      const steps = Math.round((R - L) * 1.2), arr = new Float32Array(steps + 1);
      for (let i = 0; i <= steps; i++) { const x = x0 + i / steps * (XM - x0) + 1e-6, Lx = Math.log(x), sx = Math.sqrt(x); let v = x - Math.log(2 * Math.PI) - .5 * Math.log(1 - 1 / (x * x)); for (let k = 0; k < K0; k++) { const g = ZEROS[k]; v -= 2 * sx * (.5 * Math.cos(g * Lx) + g * Math.sin(g * Lx)) / (.25 + g * g); } arr[i] = v; }
      this.cache = { [key]: arr };
    }
    const arr = this.cache[key], steps = arr.length - 1;
    ctx.shadowColor = K.wave; ctx.shadowBlur = 10; ctx.strokeStyle = K.wave; ctx.lineWidth = 1.8; ctx.beginPath();
    for (let i = 0; i <= steps; i++) { const x = x0 + i / steps * (XM - x0), y = clamp(Y(arr[i]), T - 40, B + 40); i ? ctx.lineTo(X(x), y) : ctx.moveTo(X(x), y); } ctx.stroke(); ctx.shadowBlur = 0;
    ctx.font = FONT(12); ctx.fillStyle = K.dim; ctx.textAlign = 'center'; for (let x = 10; x <= XM; x += 10) ctx.fillText(x, X(x), B + 24);
    ctx.font = HAND(Math.max(20, w / 50)); ctx.textAlign = 'left'; ctx.fillStyle = K.prime; ctx.fillText('the primes, ψ(x)', X(46), Y(psi[46]) - 22); ctx.fillStyle = K.wave; ctx.fillText(K0 ? `${K0} zero${K0 > 1 ? 's' : ''} of ζ` : 'x alone', X(6), Y(40));
    live('live-explicit', `zeros used   <b>${K0}</b>${K0 ? `\nhighest γ    ${ZEROS[K0 - 1].toFixed(2)}` : ''}\nψ(60)        ${psi[60].toFixed(2)}\nwaves give   ${arr[steps].toFixed(2)}`);
    this._K = K0;
  },
  audio() { const n = Math.min(this._K || 0, 16); const parts = [{ f: 55, g: .05 }]; for (let k = 0; k < n - 1; k++) parts.push({ f: 110 * ZEROS[k] / ZEROS[0], g: .07 / Math.sqrt(k + 1) }); Sound.setDrone(parts, .8); },
};

/* Act V: the critical line, then the spacing of the zeros */
const GUE = (() => { const sp = []; for (let i = 0; i + 1 < ZEROS.length; i++) sp.push((ZEROS[i + 1] - ZEROS[i]) * Math.log(ZEROS[i] / (2 * Math.PI)) / (2 * Math.PI)); const bins = 30, mx = 3, hst = new Array(bins).fill(0); for (const s of sp) { const b = Math.floor(s / mx * bins); if (b >= 0 && b < bins) hst[b]++; } return hst.map(c => c / (sp.length * mx / bins)); })();
SCENES.critical = {
  tempo: 72,
  draw(ctx, w, h, p, T) {
    const settle = smooth((p - .3) / .14), sig = .5 + .3 * Math.sin(p * Math.PI * 5) * (1 - settle);
    const SIG = [.2, .3, .4, .5, .6, .7, .8], i0 = clamp(Math.floor((sig - .2) / .1), 0, 5), fr = clamp((sig - SIG[i0]) / .1);
    const A = DATA.zetaCurves.curves[String(SIG[i0])], B = DATA.zetaCurves.curves[String(SIG[i0 + 1])];
    const gueOn = smooth((p - .45) / .12), half = w * (1 - .45 * gueOn);
    const cx = half * .42, cy = h * .42, sc = Math.min(half, h) * .17;
    ctx.strokeStyle = rgba(K.ink, .1); ctx.beginPath(); ctx.moveTo(0, cy); ctx.lineTo(half, cy); ctx.moveTo(cx, h * .1); ctx.lineTo(cx, h * .72); ctx.stroke();
    ctx.globalCompositeOperation = 'lighter'; ctx.lineWidth = 1.6; let mn = 1e9;
    for (let i = 1; i < A.length; i++) {
      const a0 = A[i - 1][0] + (B[i - 1][0] - A[i - 1][0]) * fr, b0 = A[i - 1][1] + (B[i - 1][1] - A[i - 1][1]) * fr, a1 = A[i][0] + (B[i][0] - A[i][0]) * fr, b1 = A[i][1] + (B[i][1] - A[i][1]) * fr;
      if (i > 50) mn = Math.min(mn, Math.hypot(a1, b1));
      if (Math.abs(a0) > 5 || Math.abs(b0) > 5) continue;
      ctx.strokeStyle = mix(K.wave, K.violet, i / A.length); ctx.beginPath(); ctx.moveTo(cx + a0 * sc, cy - b0 * sc); ctx.lineTo(cx + a1 * sc, cy - b1 * sc); ctx.stroke();
    }
    ctx.globalCompositeOperation = 'source-over';
    const atHalf = Math.abs(sig - .5) < .02;
    ctx.shadowColor = K.prime; ctx.shadowBlur = atHalf ? 26 : 0; ctx.fillStyle = atHalf ? K.prime : K.ink; ctx.beginPath(); ctx.arc(cx, cy, 5, 0, 7); ctx.fill(); ctx.shadowBlur = 0;
    ctx.font = HAND(Math.max(22, w / 44)); ctx.fillStyle = K.ink; ctx.textAlign = 'left'; ctx.fillText(`σ = ${sig.toFixed(2)}`, Math.max(16, cx - sc * 2.2), h * .12);
    if (gueOn > 0) {
      ctx.globalAlpha = gueOn; const gx = half + w * .03, gw = w - gx - w * .05, gy = h * .26, gh = h * .4, mxS = 3, my = 1.1;
      const X = (s) => gx + s / mxS * gw, Y = (v) => gy + gh - v / my * gh;
      GUE.forEach((d, i) => { ctx.fillStyle = rgba(K.wave, .55); ctx.fillRect(X(i * mxS / 30) + 1, Y(d * gueOn), gw / 30 - 2, Y(0) - Y(d * gueOn)); });
      const curve = (f, c, lw) => { ctx.strokeStyle = c; ctx.lineWidth = lw; ctx.beginPath(); for (let i = 0; i <= 200; i++) { const s = i / 200 * mxS; i ? ctx.lineTo(X(s), Y(f(s))) : ctx.moveTo(X(s), Y(f(s))); } ctx.stroke(); };
      curve(s => Math.exp(-s), rgba(K.ink, .4), 1.4); ctx.shadowColor = K.prime; ctx.shadowBlur = 10; curve(s => 32 / (Math.PI ** 2) * s * s * Math.exp(-4 * s * s / Math.PI), K.prime, 2.4); ctx.shadowBlur = 0;
      ctx.font = FONT(12); ctx.fillStyle = K.dim; ctx.textAlign = 'center'; for (let s = 0; s <= 3; s++) ctx.fillText(s, X(s), gy + gh + 22);
      ctx.font = HAND(Math.max(18, w / 60)); ctx.textAlign = 'left'; ctx.fillStyle = K.prime; ctx.fillText('random-matrix law', X(1.25), Y(1.0)); ctx.fillStyle = K.dim; ctx.fillText('independent points', X(.1), Y(1.02) - 6);
      ctx.globalAlpha = 1;
    }
    live('live-critical', `σ = ${sig.toFixed(2)}\nclosest approach to 0   <b>${mn.toFixed(4)}</b>\n${atHalf ? 'passes through zero at every zero' : 'never reaches zero'}${gueOn > .5 ? '\n\nspacings of the first 1,000 zeros' : ''}`);
    this._sig = sig;
  },
  audio() { const d = Math.abs((this._sig || .5) - .5); Sound.setDrone(ZEROS.slice(0, 6).map((z, k) => ({ f: 110 * z / ZEROS[0] * (1 + d * .06 * (k % 2 ? 1 : -1)), g: .05 / Math.sqrt(k + 1) })), .6); },
};

/* Act VI: Robin's inequality. For every range of n, the largest value of σ(n) / (n ln ln n). */
const ROBIN = (() => {
  const N = 1000000, EG = Math.exp(0.5772156649015329), NB = 360, LO = Math.log10(20), HI = 6; let bins = null;
  function build() {
    const sig = new Float64Array(N + 1); for (let d = 1; d <= N; d++) for (let m = d; m <= N; m += d) sig[m] += d;
    bins = []; for (let b = 0; b < NB; b++) bins.push({ n: 0, r: 0 });
    for (let n = 20; n <= N; n++) { const r = sig[n] / (n * Math.log(Math.log(n))), b = Math.min(NB - 1, Math.floor((Math.log10(n) - LO) / (HI - LO) * NB)); if (r > bins[b].r) { bins[b].r = r; bins[b].n = n; } }
  }
  return { EG, LO, HI, get bins() { if (!bins) build(); return bins; } };
})();
SCENES.robin = {
  tempo: 128,
  near() { if (!this._built) { this._built = true; setTimeout(() => ROBIN.bins, 50); } },
  draw(ctx, w, h, p) {
    const lim = Math.pow(10, ROBIN.LO + (ROBIN.HI - ROBIN.LO) * smooth(p / .85)), pts = ROBIN.bins.filter(b => b.n && b.n <= lim);
    const L = w * .08, R = w * .94, T = h * .22, B = h * .66, lo = 1.35, hi = 2.35;
    const X = (n) => L + (Math.log10(n) - ROBIN.LO) / (ROBIN.HI - ROBIN.LO) * (R - L), Y = (v) => B - (clamp(v, lo, hi) - lo) / (hi - lo) * (B - T);
    ctx.strokeStyle = rgba(K.ink, .14); ctx.beginPath(); ctx.moveTo(L, B); ctx.lineTo(R, B); ctx.stroke();
    ctx.fillStyle = rgba(K.prime, .07); ctx.fillRect(L, T - 10, R - L, Y(ROBIN.EG) - T + 10);
    ctx.shadowColor = K.prime; ctx.shadowBlur = 18; ctx.strokeStyle = K.prime; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(L, Y(ROBIN.EG)); ctx.lineTo(R, Y(ROBIN.EG)); ctx.stroke(); ctx.shadowBlur = 0;
    ctx.strokeStyle = rgba(K.ink, .3); ctx.setLineDash([3, 6]); ctx.beginPath(); ctx.moveTo(X(5040), T - 10); ctx.lineTo(X(5040), B); ctx.stroke(); ctx.setLineDash([]);
    ctx.globalCompositeOperation = 'lighter';
    pts.forEach((b, i) => { const above = b.r >= ROBIN.EG, last = i === pts.length - 1; ctx.fillStyle = above ? K.ochre : (b.n > 5040 ? K.ink : rgba(K.ink, .55)); if (last) { ctx.shadowColor = K.ink; ctx.shadowBlur = 18; } ctx.beginPath(); ctx.arc(X(b.n), Y(b.r), last ? 5 : 2.4, 0, 7); ctx.fill(); ctx.shadowBlur = 0; });
    ctx.globalCompositeOperation = 'source-over';
    ctx.font = FONT(12); ctx.fillStyle = K.dim; ctx.textAlign = 'center'; ['100', '1,000', '10,000', '100,000', '1,000,000'].forEach((t, i) => ctx.fillText(t, X(10 ** (i + 2)), B + 24));
    ctx.font = HAND(Math.max(20, w / 52)); ctx.textAlign = 'left'; ctx.fillStyle = K.prime; ctx.fillText('cross this line after 5040 and the hypothesis is false', L + 10, Y(ROBIN.EG) - 14);
    ctx.fillStyle = K.dim; ctx.fillText('5040', X(5040) + 8, B - 10);
    const after = pts.filter(b => b.n > 5040), best = after.reduce((a, b) => b.r > a.r ? b : a, { n: 0, r: 0 });
    live('live-robin', `checked up to       ${fmt(lim)}\nlargest above 5040  ${best.n ? 'n = ' + fmt(best.n) : '…'}\nits ratio           ${best.n ? best.r.toFixed(5) : ''}\nthe line e^γ        ${ROBIN.EG.toFixed(5)}${best.n ? `\nclosest gap         <b>${(ROBIN.EG - best.r).toFixed(5)}</b>` : ''}`);
    this._p = p;
  },
  audio() { const p = this._p || 0; Sound.setRiser(smooth(p / .85), 200 + 2600 * smooth(p / .85)); Sound.setDrone([{ f: 55, g: .05 }, { f: 55 * Math.pow(2, 11.5 / 12) * (1 - .02 * (1 - p)), g: .03 * p }]); },
};

/* ================= opening ================= */
const OPEN = (() => {
  const cv = $('#c-open'), N = 40000; let off = null, offW = 0; const ripples = [];
  function build(size) {
    const c = document.createElement('canvas'); c.width = c.height = size; const g = c.getContext('2d'); g.globalCompositeOperation = 'lighter';
    const R = size / 2, sc = R / Math.sqrt(N) * .98;
    for (let n = 2; n <= N; n++) { const r = Math.sqrt(n) * sc, th = 2 * Math.PI * Math.sqrt(n), x = R + r * Math.cos(th), y = R + r * Math.sin(th); if (isP[n]) { g.fillStyle = 'rgba(255,106,61,0.75)'; g.fillRect(x - 1, y - 1, 2, 2); } else { g.fillStyle = 'rgba(111,168,255,0.07)'; g.fillRect(x - .6, y - .6, 1.2, 1.2); } }
    return c;
  }
  return {
    cv,
    draw(T) {
      const { ctx, w, h } = fit(cv), S = Math.max(w, h) * 1.25, dpr = Math.min(window.devicePixelRatio || 1, 1.75);
      if (!off || offW !== Math.round(S * dpr)) { offW = Math.round(S * dpr); off = build(Math.min(offW, 2400)); }
      const cx = w * (w > 800 ? .66 : .5), cy = h * .42, rot = T * .01;
      ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.drawImage(off, -S / 2, -S / 2, S, S);
      const sc = S / 2 / Math.sqrt(N) * .98;
      for (const r of ripples) { const rr = Math.sqrt(r.n) * sc, th = 2 * Math.PI * Math.sqrt(r.n); ctx.strokeStyle = rgba(K.prime, Math.max(0, 1 - r.age)); ctx.lineWidth = 1.5; ctx.beginPath(); ctx.arc(rr * Math.cos(th), rr * Math.sin(th), 4 + r.age * 40, 0, 7); ctx.stroke(); }
      ctx.restore();
      const fade = ctx.createLinearGradient(0, h * .35, 0, h); fade.addColorStop(0, 'rgba(7,8,11,0)'); fade.addColorStop(1, 'rgba(7,8,11,0.95)'); ctx.fillStyle = fade; ctx.fillRect(0, 0, w, h);
      if (w > 800) { const side = ctx.createLinearGradient(0, 0, w * .6, 0); side.addColorStop(0, 'rgba(7,8,11,0.85)'); side.addColorStop(1, 'rgba(7,8,11,0)'); ctx.fillStyle = side; ctx.fillRect(0, 0, w, h); }
      for (let i = ripples.length - 1; i >= 0; i--) { ripples[i].age += .016; if (ripples[i].age > 1) ripples.splice(i, 1); }
    },
    ripple(n) { if (n <= N) ripples.push({ n, age: 0 }); },
  };
})();

/* ================= engine ================= */
const sceneEls = [...document.querySelectorAll('.scene')].map(el => ({ el, def: SCENES[el.dataset.scene], cv: el.querySelector('canvas'), words: [...el.querySelectorAll('.line')].reduce((a, l) => a + l.textContent.split(/\s+/).length, 0), lines: [...el.querySelectorAll('.line')].map((l, i, a) => ({ l, at: +l.dataset.at, to: i + 1 < a.length ? +a[i + 1].dataset.at : 1.01 })) }));
const whereEls = [...document.querySelectorAll('[data-where]')];
const actEls = [...document.querySelectorAll('.act')];
const SOLO = (() => { const q = new URLSearchParams(location.search); if (!q.get('solo')) return null; const [id, pp] = q.get('solo').split(':'); const s = document.getElementById(id); if (!s) return null; document.body.classList.add('solo'); s.classList.add('solo-on'); const o = { id, p: clamp(+pp || 0) };
  // embedded in the book: the page that holds us moves the playhead
  if (q.has('embed')) { document.body.classList.add('embed'); addEventListener('message', (e) => { if (e.origin === location.origin && e.data && typeof e.data.p === 'number') o.p = clamp(e.data.p); }); }
  return o; })();
let filmCarry = 0, film = false, tempo = 76, lastTs = performance.now(), nextBeat = 0, active = null, lastAct = null, T = 0;
const btnFilm = $('#film'), btnSound = $('#sound'), countEl = $('#count');

function setFilm(v) { film = v && !reduce; btnFilm.setAttribute('aria-pressed', String(film)); btnFilm.textContent = film ? 'Pause' : 'Play'; }
function setSound(v) { const ok = Sound.setOn(v); btnSound.setAttribute('aria-pressed', String(v && ok)); btnSound.textContent = v && ok ? 'Sound on' : 'Sound off'; if (!v) { Sound.setDrone([]); Sound.setRiser(0, 300); } }
btnFilm.addEventListener('click', () => setFilm(!film));
btnSound.addEventListener('click', () => setSound(!Sound.isOn()));
const goFull = () => { const el = document.documentElement; try { const p = (el.requestFullscreen || el.webkitRequestFullscreen || el.msRequestFullscreen); if (p && !document.fullscreenElement) { const r = p.call(el); if (r && r.catch) r.catch(() => {}); } } catch (e) {} };
$('#begin-sound').addEventListener('click', () => { goFull(); setSound(true); setFilm(true); if (scrollY < 10) window.scrollBy(0, 1); });
$('#begin-quiet').addEventListener('click', () => { goFull(); setFilm(true); if (scrollY < 10) window.scrollBy(0, 1); });
const stopFilm = () => { if (film) setFilm(false); };
addEventListener('wheel', stopFilm, { passive: true }); addEventListener('touchstart', stopFilm, { passive: true });
addEventListener('keydown', (e) => { if (e.target.closest('input, select, textarea')) return; if (e.code === 'Space') { e.preventDefault(); setFilm(!film); } else if (['ArrowDown', 'ArrowUp', 'PageDown', 'PageUp', 'Home', 'End'].includes(e.key)) stopFilm(); });

function beat() {
  pulse.n = pulse.n >= LIM - 1 ? 2 : pulse.n + 1;
  const n = pulse.n, prime = !!isP[n], def = active && active.def;
  countEl.textContent = `n = ${fmt(n)}`; countEl.classList.toggle('hit', prime);
  if (prime) {
    pulse.flash = 1; pulse.lastPrime = n; OPEN.ripple(n); dispatchEvent(new CustomEvent('prime', { detail: n }));
    const gap = n - prevPrime; prevPrime = n;
    if (!(def && def.pitch)) { const d = n % 10; mel += (d === 1 || d === 7 ? 1 : -1) * Math.max(1, Math.round(gap / 2)); if (mel > 9 || mel < 0) mel = mel > 9 ? 18 - mel : -mel; }
    const midi = def && def.pitch ? def.pitch(n) : PENTA[mel];
    Sound.mallet(midi, def && def.pitch ? .8 : .65, n % 10);
    if (gap === 2) Sound.mallet(midi + 4, .35, n % 10);
    // the harmony moves every eight primes, its root chosen by the next prime in line
    if (PI[n] % 8 === 0) Sound.setChord(PR[PI[n] >> 3] % 6);
  } else if (!(def && def.restOnComposite) && n % 6 === 0) Sound.tick(.5);
}

function frame(ts) {
  const dt = Math.min(.1, (ts - lastTs) / 1000); lastTs = ts; T += dt;
  const vh = innerHeight;
  // which scene owns the screen
  active = null; let best = 0;
  if (SOLO) { active = sceneEls.find(s => s.el.id === SOLO.id); best = vh; }
  else for (const s of sceneEls) { const r = s.el.getBoundingClientRect(); const vis = Math.min(vh, r.bottom) - Math.max(0, r.top); if (vis > best) { best = vis; active = s; } }
  if (active && best < vh * .5) active = null;
  // tempo and the pulse
  const target = active ? active.def.tempo : 72; tempo += (target - tempo) * Math.min(1, dt * 1.2);
  const interval = 60 / tempo / 2;
  if (ts / 1000 >= nextBeat) { nextBeat = ts / 1000 + interval; beat(); }
  pulse.flash = Math.max(0, pulse.flash - dt * 3);
  // the film plays itself
  if (film) {
    const max = document.documentElement.scrollHeight - vh;
    // pace by reading: each scene lasts as long as its narration takes at about 200 words a minute, plus a breath per line
    let speed = vh / 3.2;
    if (active) { const r = active.el.getBoundingClientRect(); speed = (r.height - vh) / (active.words / 3.3 + active.lines.length * 2.2 + 3); }
    if (scrollY >= max - 2) setFilm(false); else { filmCarry += speed * dt; const step = Math.floor(filmCarry); if (step) { window.scrollBy(0, step); filmCarry -= step; } }
  }
  // opening
  const or = OPEN.cv.getBoundingClientRect(); if (or.bottom > 0) OPEN.draw(T);
  // scenes
  for (const s of sceneEls) {
    const r = s.el.getBoundingClientRect();
    if (s.def.near && r.top < vh * 3 && r.bottom > -vh) s.def.near();
    if (s !== active) continue;
    const p = SOLO ? SOLO.p : clamp(-r.top / (r.height - vh));
    const { ctx, w, h } = fit(s.cv);
    try { s.def.draw(ctx, w, h, p, T); } catch (e) { console.error(e); }
    for (const L of s.lines) L.l.classList.toggle('on', p >= L.at && p < L.to);
    if (Sound.isOn()) s.def.audio && s.def.audio();
  }
  if (!active && Sound.isOn()) { Sound.setDrone([{ f: 55, g: .035 }, { f: 82.4, g: .02 }]); Sound.setRiser(0, 300); }
  if (active && active.def !== SCENES.robin && Sound.isOn()) Sound.setRiser(0, 300);
  // act titles: a boom as each one arrives
  for (const a of actEls) { const r = a.getBoundingClientRect(); if (r.top < vh * .45 && r.bottom > vh * .55 && lastAct !== a) { lastAct = a; Sound.boom(); } }
  // progress and where we are
  const max = document.documentElement.scrollHeight - vh; $('#progress').style.width = (max > 0 ? scrollY / max * 100 : 0) + '%';
  let where = whereEls[0]; for (const el of whereEls) if (el.getBoundingClientRect().top <= vh * .5) where = el;
  const wl = $('#where'); if (wl.textContent !== where.dataset.where) wl.textContent = where.dataset.where;
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);

/* ================= contact: copy the address ================= */
(() => {
  const b = document.getElementById('copy-mail'), out = document.getElementById('copied'); if (!b) return;
  b.addEventListener('click', () => {
    const mail = b.dataset.mail;
    const done = () => { out.textContent = 'Copied'; setTimeout(() => { out.textContent = ''; }, 2200); };
    const fallback = () => { const a = document.querySelector('.contact .mail'); const r = document.createRange(); r.selectNodeContents(a); const s = getSelection(); s.removeAllRanges(); s.addRange(r); out.textContent = 'Selected. Press Ctrl+C to copy'; };
    try { navigator.clipboard.writeText(mail).then(done, fallback); } catch (e) { fallback(); }
  });
})();

/* ================= epilogue: Robin tester ================= */
(() => {
  const EG = Math.exp(0.5772156649015329);
  function check() {
    const raw = $('#rn').value.replace(/[,_\s]/g, ''), n = Number(raw);
    if (!/^\d+$/.test(raw) || n < 3 || n > 1e14) { $('#rr').innerHTML = 'Enter a whole number from 3 to 10¹⁴.'; return; }
    let t = n, s = 1; for (let q = 2; q * q <= t; q++) { if (t % q === 0) { let pk = 1, sum = 1; while (t % q === 0) { t /= q; pk *= q; sum += pk; } s *= sum; } } if (t > 1) s *= (t + 1);
    const r = s / (n * Math.log(Math.log(n)));
    $('#rr').innerHTML = `σ(n) = <b>${fmt(s)}</b> · ratio <b>${r.toFixed(6)}</b> against e^γ = ${EG.toFixed(6)} · ${n <= 5040 ? (r >= EG ? 'above the line, which is allowed for n ≤ 5040' : 'below the line') : r >= EG ? '<b>above the line. Check the arithmetic in exact integers before you tell anyone.</b>' : `below the line by ${(EG - r).toFixed(6)}`}`;
  }
  $('#rb').addEventListener('click', check); $('#rn').addEventListener('keydown', (e) => { if (e.key === 'Enter') check(); }); check();
})();

/* ================= epilogue: the archive ================= */
(() => {
  const TH = { wave: '01 waves', physics: '02 physics models', complex: '03 complex plane', bits: '04 bit pairs', hex: '05 hex puzzle', music: '06 music', geometry: '07 gaps, walks, spirals', ml: '08 machine learning', matrix: '09 prime matrix', gamma: '10 factorials', docs: 'docs', archive: 'archive', other: 'other projects' };
  const on = new Set(Object.keys(TH)); let q = '', sort = 'p';
  const counts = {}; FILES.forEach(f => counts[f.t] = (counts[f.t] || 0) + 1);
  const box = $('#themes'); box.innerHTML = Object.entries(TH).filter(([k]) => counts[k]).map(([k, l]) => `<button type="button" data-t="${k}" aria-pressed="true">${l} · ${counts[k]}</button>`).join('');
  box.addEventListener('click', (e) => { const b = e.target.closest('button'); if (!b) return; const t = b.dataset.t; on.has(t) ? on.delete(t) : on.add(t); b.setAttribute('aria-pressed', String(on.has(t))); render(); });
  const size = (s) => s >= 1e6 ? (s / 1e6).toFixed(1) + ' MB' : s >= 1e3 ? Math.round(s / 1e3) + ' KB' : s + ' B';
  const esc = (s) => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  function render() {
    let rows = FILES.filter(f => on.has(f.t) && (!q || f.p.toLowerCase().includes(q) || (f.o || '').toLowerCase().includes(q)));
    if (sort === 'd') rows = rows.slice().sort((a, b) => (b.d || '').localeCompare(a.d || '')); else if (sort === 's') rows = rows.slice().sort((a, b) => b.s - a.s);
    $('#rq').textContent = `${rows.length} of ${FILES.length} entries`;
    $('#ftbody').innerHTML = rows.map(f => `<tr><td>${esc(f.p)}${f.k === 'folder' ? ` (${f.n} files)` : ''}</td><td class="was">${f.o && f.o !== f.p ? esc(f.o) : ''}</td><td class="n">${size(f.s)}</td><td class="n">${f.d}</td></tr>`).join('');
  }
  $('#q').addEventListener('input', (e) => { q = e.target.value.trim().toLowerCase(); render(); });
  $('#sort').addEventListener('change', (e) => { sort = e.target.value; render(); });
  render();
})();

/* ?at=scene-id:progress opens the film at that point (handy for sharing a moment) */
(() => { const at = new URLSearchParams(location.search).get('at'); if (!at) return; const [id, pp] = at.split(':'); const el = document.getElementById(id); if (!el) return;
  const go = () => scrollTo(0, el.getBoundingClientRect().top + scrollY + Math.max(0, el.offsetHeight - innerHeight) * clamp(+pp || 0)); go(); setTimeout(go, 300); })();
})();
