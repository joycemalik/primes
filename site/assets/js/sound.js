// Sound for "Where the waves go quiet". Everything is synthesised live with the Web Audio API.
// Primes ring as mallet notes, composites tick, the waves of small primes and the zeros of zeta
// are held as drones, and each act opens with a low boom and a sweep of air.
window.Sound = (() => {
  let ctx = null, master, bus, lp, noiseBuf, on = false;
  const voices = [];            // drone pool: sine oscillators with their own gain
  let riser = null;
  const pad = [];

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
    const verb = ctx.createConvolver(); verb.buffer = impulse(5.5, 3.2);
    const wet = ctx.createGain(); wet.gain.value = .45; verb.connect(wet); wet.connect(master);
    bus = ctx.createGain(); bus.gain.value = .9; bus.connect(master); bus.connect(verb);
    // a dotted echo, darkened each time round, so single primes bloom into phrases
    const dl = ctx.createDelay(2), fb = ctx.createGain(), dlp = ctx.createBiquadFilter(), dw = ctx.createGain();
    dl.delayTime.value = .54; fb.gain.value = .38; dlp.type = 'lowpass'; dlp.frequency.value = 1800; dw.gain.value = .3;
    bus.connect(dl); dl.connect(dlp); dlp.connect(fb); fb.connect(dl); dlp.connect(dw); dw.connect(verb); dw.connect(master);
    // the pad: two detuned voices per chord tone through a slowly breathing filter
    const plp = ctx.createBiquadFilter(); plp.type = 'lowpass'; plp.frequency.value = 900; plp.Q.value = .7;
    const lfo = ctx.createOscillator(), lg = ctx.createGain(); lfo.frequency.value = .05; lg.gain.value = 380; lfo.connect(lg); lg.connect(plp.frequency); lfo.start();
    const pg = ctx.createGain(); pg.gain.value = .5; plp.connect(pg); pg.connect(master); pg.connect(verb);
    for (let i = 0; i < 8; i++) { const o = ctx.createOscillator(), g = ctx.createGain(); o.type = i % 2 ? 'sawtooth' : 'triangle'; o.detune.value = (i % 2 ? 7 : -7); g.gain.value = 0; o.connect(g); g.connect(plp); o.start(); pad.push({ o, g }); }
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
    if (ctx) { if (v) ctx.resume(); if (v) setChord(0); else pad.forEach(p => p.g.gain.setTargetAtTime(0, ctx.currentTime, .3)); master.gain.setTargetAtTime(v ? .85 : 0, ctx.currentTime, .25); }
    return true;
  }
  const mtof = (m) => 440 * Math.pow(2, (m - 69) / 12);
  function env(g, t, peak, attack, decay) { g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(peak, t + attack); g.gain.exponentialRampToValueAtTime(.0001, t + attack + decay); }

  const PAN = { 1: -.6, 3: -.2, 7: .2, 9: .6 };
  function mallet(midi, vel = 1, digit = 0) {
    if (!on) return; const t = ctx.currentTime, f = mtof(midi);
    const g = ctx.createGain(); env(g, t, .16 * vel, .012, 2.6);
    const pn = ctx.createStereoPanner ? ctx.createStereoPanner() : null;
    if (pn) { pn.pan.value = PAN[digit] || 0; g.connect(pn); pn.connect(bus); } else g.connect(bus);
    const soft = ctx.createBiquadFilter(); soft.type = 'lowpass'; soft.frequency.setValueAtTime(f * 6, t); soft.frequency.exponentialRampToValueAtTime(f * 1.5, t + 1.2); soft.connect(g);
    const a = ctx.createOscillator(); a.type = 'sine'; a.frequency.value = f;
    const b = ctx.createOscillator(); b.type = 'triangle'; b.frequency.value = f * 2.001;
    const c = ctx.createOscillator(); c.type = 'sine'; c.frequency.value = f * 3;
    const bg = ctx.createGain(); bg.gain.value = .18; const cg = ctx.createGain(); env(cg, t, .08, .005, .4);
    a.connect(soft); b.connect(bg); bg.connect(soft); c.connect(cg); cg.connect(soft);
    [a, b, c].forEach(o => { o.start(t); o.stop(t + 3); });
  }
  // chords in C, all inside the pentatonic the primes sing in: Cmaj9, Am9, Fmaj7#11, G6sus, Em7, Dm9
  const CHORDS = [[48, 55, 64, 71, 74], [45, 52, 60, 67, 71], [41, 53, 57, 64, 71], [43, 50, 57, 64, 72], [40, 52, 55, 62, 71], [38, 50, 57, 60, 64]];
  function setChord(k) {
    if (!ctx) return; const t = ctx.currentTime, ch = CHORDS[k % CHORDS.length];
    pad.forEach((v, i) => { const m = ch[Math.floor(i / 2) + (i % 2 ? 1 : 0)] ?? ch[0]; v.o.frequency.setTargetAtTime(mtof(m), t, .8); v.g.gain.setTargetAtTime(on ? .022 : 0, t, 2.5); });
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
    const hp = ctx.createBiquadFilter(); hp.type = 'highpass'; hp.frequency.value = 5200;
    const g = ctx.createGain(); env(g, t, .012 * vel, .001, .03);
    s.connect(hp); hp.connect(g); g.connect(master); s.start(t, Math.random()); s.stop(t + .08);
  }
  function boom() {
    if (!on) return; const t = ctx.currentTime;
    const o = ctx.createOscillator(), g = ctx.createGain(); o.type = 'sine';
    o.frequency.setValueAtTime(65.4, t); o.frequency.exponentialRampToValueAtTime(64.8, t + 4);
    env(g, t, .3, .08, 5); bell(130.8, .6); o.connect(g); g.connect(master); o.start(t); o.stop(t + 5.2);
    const s = ctx.createBufferSource(); s.buffer = noiseBuf;
    const bp = ctx.createBiquadFilter(); bp.type = 'bandpass'; bp.Q.value = 1.2;
    bp.frequency.setValueAtTime(400, t); bp.frequency.exponentialRampToValueAtTime(3200, t + 1.4);
    const ng = ctx.createGain(); env(ng, t, .05, .9, 1.6); s.connect(bp); bp.connect(ng); ng.connect(bus); s.start(t); s.stop(t + 1.9);
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
  return { setOn, isOn: () => on, mallet, setChord, bell, tick, boom, setDrone, setRiser, mtof };
})();
