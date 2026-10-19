// Depth: a fractal space behind the film.
// One fixed WebGL canvas draws Julia sets as layers at different depths. Scrolling flies through them (an
// endless log-periodic zoom), the pointer shifts near layers more than far ones, and every prime the pulse
// rings sends a ripple that bends the space. The same pointer tilts each stage in 3D so the figures sit in
// front of the fractal rather than on top of it.
(() => {
'use strict';
if (new URLSearchParams(location.search).has('embed')) return;
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const root = document.documentElement;
const cv = document.createElement('canvas'); cv.className = 'depth'; cv.setAttribute('aria-hidden', 'true');
document.body.prepend(cv);
const gl = cv.getContext('webgl', { antialias: false, alpha: false, premultipliedAlpha: false });

// every scene and act tints the fractal with its own colour
const TINT = { count: [1, .42, .24], sieve: [.44, .66, 1], smooth: [.44, .66, 1], zn: [.77, .55, 1], spiral: [1, .42, .24], bits: [.88, .7, .3], life: [.5, .82, .66], walk: [.44, .66, 1], zeta: [.77, .55, 1], domain: [1, .42, .24], explicit: [1, .42, .24], critical: [.77, .55, 1], robin: [.88, .7, .3] };
const tint = [1, .42, .24], tintTo = [1, .42, .24];

const pointer = { x: 0, y: 0, tx: 0, ty: 0 };
addEventListener('pointermove', (e) => { pointer.tx = e.clientX / innerWidth * 2 - 1; pointer.ty = e.clientY / innerHeight * 2 - 1; }, { passive: true });
addEventListener('deviceorientation', (e) => { if (e.gamma == null) return; pointer.tx = Math.max(-1, Math.min(1, e.gamma / 30)); pointer.ty = Math.max(-1, Math.min(1, (e.beta - 45) / 30)); }, { passive: true });

const ripples = []; // [age, strength]
addEventListener('prime', (e) => { ripples.unshift([0, Math.min(1, .35 + Math.log10(e.detail) / 8)]); ripples.length = Math.min(ripples.length, 4); });

let prog = null;
if (gl) {
  const vs = 'attribute vec2 p; void main(){ gl_Position = vec4(p, 0., 1.); }';
  const fs = `precision mediump float;
uniform vec2 R; uniform float T, Z, V; uniform vec2 M; uniform vec3 C; uniform vec4 W; uniform vec4 WS;
// one Julia layer: smooth escape count, returned as brightness
float julia(vec2 z, vec2 c){
  float n = 0.; float m = 0.;
  for (int i = 0; i < 56; i++){ z = vec2(z.x*z.x - z.y*z.y, 2.*z.x*z.y) + c; m = dot(z,z); if (m > 64.) break; n += 1.; }
  if (m <= 64.) return 0.;
  return (n - log2(log2(m)) + 4.) / 56.;
}
void main(){
  vec2 uv = (gl_FragCoord.xy - .5*R) / min(R.x, R.y);
  // distortion: a lens around the pointer, ripples from each prime, and a swirl that follows scroll speed
  vec2 mp = M * vec2(.9, -.6); vec2 d = uv - mp; float dl = length(d);
  uv += d * .18 * exp(-dl*dl*5.);
  float rl = length(uv);
  for (int k = 0; k < 4; k++){ float a = k==0?W.x:k==1?W.y:k==2?W.z:W.w; float s = k==0?WS.x:k==1?WS.y:k==2?WS.z:WS.w;
    float ring = rl - a*1.6; uv += normalize(uv+1e-4) * s * .05 * (1.-a) * exp(-ring*ring*60.) * sin(ring*60.); }
  float sw = V * .6 * exp(-rl*1.5); uv = mat2(cos(sw), -sin(sw), sin(sw), cos(sw)) * uv;
  // depth: four layers, each a step further in; the zoom wraps so the flight never ends
  vec3 col = vec3(0.);
  for (int i = 0; i < 4; i++){
    float f = fract(Z + float(i) / 4.);
    float sc = exp2(mix(1.6, -2.4, f));          // far layers are small, near layers huge
    float fade = smoothstep(0., .25, f) * smoothstep(1., .7, f);
    vec2 par = M * (.04 + .22 * f);               // nearer layers drift more with the pointer
    float ang = T * .02 + float(i) * 1.7;
    vec2 q = mat2(cos(ang), -sin(ang), sin(ang), cos(ang)) * (uv - par) * sc;
    float ph = T * .05 + float(i) * 2.1 + Z * 1.3;
    vec2 c = vec2(-.745, .113) + .045 * vec2(cos(ph), sin(ph*1.3));
    float b = julia(q, c);
    vec3 lc = mix(C * .9, vec3(.93, .9, .84), pow(b, 3.)) * pow(b, 1.6);
    col += lc * fade * (.25 + .75 * f);
  }
  col *= .55;
  col = 1. - exp(-col * 1.6);
  col *= smoothstep(1.35, .2, length((gl_FragCoord.xy / R - .5) * vec2(1.2, 1.)));
  gl_FragColor = vec4(vec3(.027, .031, .043) + col, 1.);
}`;
  const sh = (t, s) => { const o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); if (!gl.getShaderParameter(o, gl.COMPILE_STATUS)) { console.warn(gl.getShaderInfoLog(o)); return null; } return o; };
  const v = sh(gl.VERTEX_SHADER, vs), f = sh(gl.FRAGMENT_SHADER, fs);
  if (v && f) {
    prog = gl.createProgram(); gl.attachShader(prog, v); gl.attachShader(prog, f); gl.linkProgram(prog); gl.useProgram(prog);
    gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer()); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    const loc = gl.getAttribLocation(prog, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    prog.u = {}; ['R', 'T', 'Z', 'V', 'M', 'C', 'W', 'WS'].forEach(k => prog.u[k] = gl.getUniformLocation(prog, k));
  }
}
if (!prog) cv.style.display = 'none';

const stages = [...document.querySelectorAll('.scene')].map((el, i) => ({ i, el, st: el.querySelector('.stage'), key: el.dataset.scene }));
const acts = [...document.querySelectorAll('.act')];
let fade = 1, T = 0, last = performance.now(), lastY = scrollY, vel = 0, zoom = 0, scale = 1;

function frame(ts) {
  const dt = Math.min(.1, (ts - last) / 1000); last = ts; T += reduce ? 0 : dt;
  const vh = innerHeight, k = Math.min(1, dt * 4);
  pointer.x += (pointer.tx - pointer.x) * k; pointer.y += (pointer.ty - pointer.y) * k;
  const dy = scrollY - lastY; lastY = scrollY;
  vel += (Math.max(-1, Math.min(1, dy / vh * 6)) - vel) * Math.min(1, dt * 5);
  // scroll depth: one full fractal cycle every ~3 screens, plus a slow drift of its own
  const target = scrollY / vh / 3 + T * .006; zoom += (target - zoom) * Math.min(1, dt * 3);

  // the stage that owns the screen sets the tint; each stage tilts and rises out of the depth
  let key = null, focus = 0;
  for (const s of stages) {
    const r = s.el.getBoundingClientRect();
    if (r.bottom < -vh || r.top > vh * 2) continue;
    if (r.top <= vh * .5 && r.bottom >= vh * .5) key = s.key;
    const enter = Math.max(0, Math.min(1, (vh - r.top) / vh)), leave = Math.max(0, Math.min(1, r.bottom / vh));
    const e = Math.min(enter, leave), ee = e * e * (3 - 2 * e);
    s.st.style.setProperty('--depth', (1 - ee).toFixed(3));
    // the camera: each scene opens close in and off to one side, settles on the whole figure, then drifts on
    const p = Math.max(0, Math.min(1, -r.top / (r.height - vh))), a = s.i * 2.4, q = .5 - p;
    s.st.style.setProperty('--cs', (1 + .1 * q * q * 4).toFixed(4));
    s.st.style.setProperty('--cx', (Math.cos(a) * q * 5).toFixed(3) + '%');
    s.st.style.setProperty('--cy', (Math.sin(a) * q * 3.5).toFixed(3) + '%');
    s.st.style.setProperty('--cr', (Math.sin(a * 1.7) * q * 1.6).toFixed(3) + 'deg');
    focus = Math.max(focus, ee);
  }
  // the fractal is for the passages between figures; once a figure owns the screen it steps out of the way
  fade += ((1 - focus) - fade) * Math.min(1, dt * 3); cv.style.opacity = fade.toFixed(3);
  if (key && TINT[key]) TINT[key].forEach((c, i) => tintTo[i] = c);
  for (let i = 0; i < 3; i++) tint[i] += (tintTo[i] - tint[i]) * Math.min(1, dt * 1.5);
  for (const a of acts) { const r = a.getBoundingClientRect(); if (r.bottom < 0 || r.top > vh) continue; a.style.setProperty('--ap', ((vh - r.top) / (vh + r.height) * 2 - 1).toFixed(3)); }
  root.style.setProperty('--px', pointer.x.toFixed(4)); root.style.setProperty('--py', pointer.y.toFixed(4)); root.style.setProperty('--vel', vel.toFixed(3));

  for (const r of ripples) r[0] += dt * .7;
  while (ripples.length && ripples[ripples.length - 1][0] > 1) ripples.pop();

  if (prog && fade > .01) {
    const q = innerWidth < 700 ? .45 : .6, w = Math.round(innerWidth * q), h = Math.round(vh * q);
    if (cv.width !== w || cv.height !== h) { cv.width = w; cv.height = h; gl.viewport(0, 0, w, h); }
    const W = [0, 1, 2, 3].map(i => ripples[i] ? ripples[i][0] : 1), WS = [0, 1, 2, 3].map(i => ripples[i] ? ripples[i][1] : 0);
    const u = prog.u;
    gl.uniform2f(u.R, w, h); gl.uniform1f(u.T, T); gl.uniform1f(u.Z, zoom); gl.uniform1f(u.V, vel);
    gl.uniform2f(u.M, pointer.x, pointer.y); gl.uniform3fv(u.C, tint); gl.uniform4fv(u.W, W); gl.uniform4fv(u.WS, WS);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  }
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
})();
