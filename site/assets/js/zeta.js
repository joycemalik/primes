// complex zeta: Borwein eta for Re(s) >= 0.5, reflection otherwise
const ZN = 64;
const ZD = (() => { const d = new Float64Array(ZN + 1); let s = 0, t = 1 / ZN; // d_k = n * sum_{i<=k} (n+i-1)! 4^i / ((n-i)! (2i)!)
  let term = 1 / ZN; // i=0 term: (n-1)!/(n! 0!) = 1/n
  for (let i = 0; i <= ZN; i++) { if (i > 0) term *= 4 * (ZN + i - 1) * (ZN - i + 1) / ((2 * i - 1) * (2 * i)); s += term; d[i] = ZN * s; } return d; })();
const LNK = Array.from({ length: ZN }, (_, k) => Math.log(k + 1));
function zetaC(re, im) {
  if (re < 0.5) {
    // zeta(s) = 2^s pi^(s-1) sin(pi s/2) Gamma(1-s) zeta(1-s)
    const [zr, zi] = zetaC(1 - re, -im);
    const [gr, gi] = gammaC(1 - re, -im);
    // 2^s pi^(s-1) = exp(s ln2 + (s-1) ln pi)
    const er = re * Math.LN2 + (re - 1) * Math.log(Math.PI), ei = im * Math.LN2 + im * Math.log(Math.PI);
    const ea = Math.exp(er), pr = ea * Math.cos(ei), pi = ea * Math.sin(ei);
    // sin(pi s/2), s=a+ib: sin(x)cosh(y) + i cos(x) sinh(y)
    const x = Math.PI * re / 2, y = Math.PI * im / 2;
    const sr = Math.sin(x) * Math.cosh(y), si = Math.cos(x) * Math.sinh(y);
    let ar = pr * sr - pi * si, ai = pr * si + pi * sr;
    let br = ar * gr - ai * gi, bi = ar * gi + ai * gr;
    return [br * zr - bi * zi, br * zi + bi * zr];
  }
  let sr = 0, si = 0;
  for (let k = 0; k < ZN; k++) {
    const c = ((k & 1) ? -1 : 1) * (ZD[k] - ZD[ZN]);
    const m = Math.exp(-re * LNK[k]), a = -im * LNK[k];
    sr += c * m * Math.cos(a); si += c * m * Math.sin(a);
  }
  sr /= -ZD[ZN]; si /= -ZD[ZN];
  // divide by (1 - 2^(1-s))
  const m = Math.exp((1 - re) * Math.LN2), a = -im * Math.LN2;
  const dr = 1 - m * Math.cos(a), di = -m * Math.sin(a), dd = dr * dr + di * di;
  return [(sr * dr + si * di) / dd, (si * dr - sr * di) / dd];
}
const LG = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];
function gammaC(re, im) {
  if (re < 0.5) { // reflection: Gamma(s) = pi / (sin(pi s) Gamma(1-s))
    const [gr, gi] = gammaC(1 - re, -im);
    const x = Math.PI * re, y = Math.PI * im;
    const sr = Math.sin(x) * Math.cosh(y), si = Math.cos(x) * Math.sinh(y);
    const dr = sr * gr - si * gi, di = sr * gi + si * gr, dd = dr * dr + di * di;
    return [Math.PI * dr / dd, -Math.PI * di / dd];
  }
  re -= 1;
  let xr = LG[0], xi = 0;
  for (let i = 1; i < 9; i++) { const dr = re + i, dd = dr * dr + im * im; xr += LG[i] * dr / dd; xi -= LG[i] * im / dd; }
  const tr = re + 7.5, ti = im;
  // t^(z+0.5) * e^-t * sqrt(2pi) * x
  const lt = 0.5 * Math.log(tr * tr + ti * ti), at = Math.atan2(ti, tr);
  const pr = (re + 0.5) * lt - im * at - tr, pa = (re + 0.5) * at + im * lt - ti;
  const m = Math.sqrt(2 * Math.PI) * Math.exp(pr);
  const cr = m * Math.cos(pa), ci = m * Math.sin(pa);
  return [cr * xr - ci * xi, cr * xi + ci * xr];
}
if (typeof module !== 'undefined') module.exports = { zetaC, gammaC };
