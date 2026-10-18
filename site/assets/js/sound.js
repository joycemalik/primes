// Sound for "Where the waves go quiet". Everything is synthesised live with the Web Audio API.
// Primes ring as mallet notes, composites tick, the waves of small primes and the zeros of zeta
// are held as drones, and each act opens with a low boom and a sweep of air.
window.Sound = (() => {
  let ctx = null, master, bus, lp, noiseBuf, on = false;
  const voices = [];            // drone pool: sine oscillators with their own gain
  let riser = null;

  function impulse(seconds, decay) {
    const len = Math.floor(ctx.sampleRate * seconds), buf = ctx.createBuffer(2, len, ctx.sampleRate);
    for (let c = 0; c < 2; c++) { const d = buf.getChannelData(c); for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, decay); }
    return buf;
  }
  function init() {
    if (ctx) return true;
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return false;
    ctx = new AC();
    const comp = ctx.createDynamicsCompressor(); comp.threshold.value = -18; comp.ratio.value = 3;
    master = ctx.createGain(); master.gain.value = 0; master.connect(comp); comp.connect(ctx.destination);
    const verb = ctx.createConvolver(); verb.buffer = impulse(3.4, 2.4);
    const wet = ctx.createGain(); wet.gain.value = .32; verb.connect(wet); wet.connect(master);
    bus = ctx.createGain(); bus.gain.value = .9; bus.connect(master); bus.connect(verb);
    noiseBuf = ctx.createBuffer(1, ctx.sampleRate * 2, ctx.sampleRate);
    const nd = noiseBuf.getChannelData(0); for (let i = 0; i < nd.length; i++) nd[i] = Math.random() * 2 - 1;
    lp = ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 1400; lp.Q.value = .4; lp.connect(bus);
    for (let i = 0; i < 16; i++) {
      const o = ctx.createOscillator(), g = ctx.createGain();
      o.type = i % 3 === 2 ? 'triangle' : 'sine'; o.frequency.value = 110; g.gain.value = 0;
      o.connect(g); g.connect(lp); o.start(); voices.push({ o, g });
    }
    // riser: looping noise through a moving band-pass
    const src = ctx.createBufferSource(); src.buffer = noiseBuf; src.loop = true;
    const bp = ctx.createBiquadFilter(); bp.type = 'bandpass'; bp.Q.value = 6; bp.frequency.value = 300;
    const rg = ctx.createGain(); rg.gain.value = 0;
    src.connect(bp); bp.connect(rg); rg.connect(bus); src.start();
    riser = { bp, rg };
    return true;
  }
  function setOn(v) {
    if (v && !init()) return false;
    on = v;
    if (ctx) { if (v) ctx.resume(); master.gain.setTargetAtTime(v ? .85 : 0, ctx.currentTime, .25); }
    return true;
  }
  const mtof = (m) => 440 * Math.pow(2, (m - 69) / 12);
  function env(g, t, peak, attack, decay) { g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(peak, t + attack); g.gain.exponentialRampToValueAtTime(.0001, t + attack + decay); }

  function mallet(midi, vel = 1) {
    if (!on) return; const t = ctx.currentTime, f = mtof(midi);
    const g = ctx.createGain(); env(g, t, .2 * vel, .004, 1.1); g.connect(bus);
    const a = ctx.createOscillator(); a.type = 'sine'; a.frequency.value = f;
    const b = ctx.createOscillator(); b.type = 'triangle'; b.frequency.value = f * 2;
    const bg = ctx.createGain(); bg.gain.value = .25; b.connect(bg); bg.connect(g); a.connect(g);
    a.start(t); b.start(t); a.stop(t + 1.3); b.stop(t + 1.3);
  }
  function bell(f, vel = 1) {
    if (!on) return; const t = ctx.currentTime;
    [[1, .22], [2.76, .09], [5.4, .04]].forEach(([r, amp]) => {
      const o = ctx.createOscillator(), g = ctx.createGain(); o.type = 'sine'; o.frequency.value = f * r;
      env(g, t, amp * vel, .003, 3.2 / r); o.connect(g); g.connect(bus); o.start(t); o.stop(t + 3.5);
    });
  }
  function tick(vel = 1) {
    if (!on) return; const t = ctx.currentTime;
    const s = ctx.createBufferSource(); s.buffer = noiseBuf;
    const hp = ctx.createBiquadFilter(); hp.type = 'highpass'; hp.frequency.value = 7000;
    const g = ctx.createGain(); env(g, t, .045 * vel, .001, .045);
    s.connect(hp); hp.connect(g); g.connect(master); s.start(t, Math.random()); s.stop(t + .08);
  }
  function boom() {
    if (!on) return; const t = ctx.currentTime;
    const o = ctx.createOscillator(), g = ctx.createGain(); o.type = 'sine';
    o.frequency.setValueAtTime(70, t); o.frequency.exponentialRampToValueAtTime(32, t + 1.6);
    env(g, t, .55, .01, 2.2); o.connect(g); g.connect(master); o.start(t); o.stop(t + 2.4);
    const s = ctx.createBufferSource(); s.buffer = noiseBuf;
    const bp = ctx.createBiquadFilter(); bp.type = 'bandpass'; bp.Q.value = 1.2;
    bp.frequency.setValueAtTime(400, t); bp.frequency.exponentialRampToValueAtTime(3200, t + 1.4);
    const ng = ctx.createGain(); env(ng, t, .12, .5, 1.2); s.connect(bp); bp.connect(ng); ng.connect(bus); s.start(t); s.stop(t + 1.9);
  }
  // parts: [{ f, g }] up to 16; glides to the new chord
  function setDrone(parts, glide = .5) {
    if (!ctx) return; const t = ctx.currentTime;
    voices.forEach((v, i) => {
      const p = parts[i];
      if (p) v.o.frequency.setTargetAtTime(p.f, t, glide * .4);
      v.g.gain.setTargetAtTime(on && p ? p.g : 0, t, glide);
    });
  }
  function setRiser(level, freq) {
    if (!ctx) return; const t = ctx.currentTime;
    riser.rg.gain.setTargetAtTime(on ? level * .16 : 0, t, .2);
    riser.bp.frequency.setTargetAtTime(freq, t, .2);
  }
  return { setOn, isOn: () => on, mallet, bell, tick, boom, setDrone, setRiser, mtof };
})();
