/* ============================================================
   Campus Plant Corner — interactions
   ============================================================ */
(function () {
  'use strict';

  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── sticky nav ─────────────────────────────────────────── */
  const nav = document.getElementById('nav');
  const onScroll = () => nav.classList.toggle('is-stuck', window.scrollY > 24);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ── mobile menu ────────────────────────────────────────── */
  const burger = document.getElementById('burger');
  const mobile = document.getElementById('mobileMenu');
  burger.addEventListener('click', () => {
    const open = burger.getAttribute('aria-expanded') === 'true';
    burger.setAttribute('aria-expanded', String(!open));
    mobile.classList.toggle('is-open', !open);
    mobile.hidden = false;
  });
  mobile.querySelectorAll('a').forEach((a) =>
    a.addEventListener('click', () => {
      burger.setAttribute('aria-expanded', 'false');
      mobile.classList.remove('is-open');
    })
  );

  /* ── reveal on scroll ───────────────────────────────────── */
  const items = document.querySelectorAll('[data-reveal]');
  if (!('IntersectionObserver' in window) || reduce) {
    items.forEach((el) => el.classList.add('in'));
  } else {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('in');
            io.unobserve(entry.target);
          }
        });
      },
      { rootMargin: '0px 0px -12% 0px', threshold: 0.12 }
    );
    items.forEach((el) => io.observe(el));
  }

  /* ── marquee: duplicate the row so -50% loops seamlessly ── */
  const marquee = document.getElementById('marquee');
  if (marquee) {
    marquee.innerHTML += marquee.innerHTML;
    marquee.setAttribute('aria-hidden', 'true');
  }

  /* ── count-up numbers ───────────────────────────────────── */
  const counters = document.querySelectorAll('[data-count]');
  if (counters.length) {
    const run = (el) => {
      const target = Number(el.dataset.count) || 0;
      if (reduce) { el.textContent = target.toLocaleString('en-US'); return; }
      const dur = 1400;
      const t0 = performance.now();
      const step = (now) => {
        const p = Math.min(1, (now - t0) / dur);
        const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(target * eased).toLocaleString('en-US');
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    if ('IntersectionObserver' in window) {
      const io2 = new IntersectionObserver(
        (entries) =>
          entries.forEach((e) => {
            if (e.isIntersecting) { run(e.target); io2.unobserve(e.target); }
          }),
        { threshold: 0.6 }
      );
      counters.forEach((c) => io2.observe(c));
    } else {
      counters.forEach(run);
    }
  }

  /* ── hero parallax ──────────────────────────────────────── */
  const frame = document.querySelector('[data-parallax]');
  if (frame && !reduce && window.matchMedia('(pointer: fine)').matches) {
    let raf = null, tx = 0, ty = 0;
    document.querySelector('.hero').addEventListener('mousemove', (e) => {
      const r = frame.getBoundingClientRect();
      tx = ((e.clientX - (r.left + r.width / 2)) / window.innerWidth) * 14;
      ty = ((e.clientY - (r.top + r.height / 2)) / window.innerHeight) * 10;
      if (raf) return;
      raf = requestAnimationFrame(() => {
        raf = null;
        frame.style.translate = `${tx.toFixed(2)}px ${ty.toFixed(2)}px`;
      });
    });
  }

  /* ── watercolour blob with ordered (Bayer) dithering ────────
     The illustration fades into the paper as grain instead of a
     gradient — the trick the Vestris hero uses on its artwork.  */
  const canvas = document.getElementById('blob');
  if (canvas && canvas.getContext) {
    const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];
    const WASHES = [
      { x: 0.34, y: 0.30, rx: 0.40, ry: 0.34, c: [143, 187, 168], a: 0.85 },
      { x: 0.62, y: 0.48, rx: 0.38, ry: 0.36, c: [201, 216, 189], a: 0.90 },
      { x: 0.46, y: 0.70, rx: 0.42, ry: 0.28, c: [190, 158, 122], a: 0.42 }
    ];

    let lastW = 0;

    function paint() {
      const rect = canvas.getBoundingClientRect();
      // supersample so the dither grain stays fine even on 1x displays
      const dpr = Math.min(Math.max(window.devicePixelRatio || 1, 1) * 2, 3);
      const w = Math.max(2, Math.round(rect.width * dpr));
      const h = Math.max(2, Math.round(rect.height * dpr));
      if (Math.abs(w - lastW) < 8 && canvas.width === w) return;
      lastW = w;

      canvas.width = w;
      canvas.height = h;

      const srcCv = document.createElement('canvas');
      srcCv.width = w;
      srcCv.height = h;
      const s = srcCv.getContext('2d');

      WASHES.forEach((b) => {
        const g = s.createRadialGradient(b.x * w, b.y * h, 0, b.x * w, b.y * h, Math.max(b.rx * w, b.ry * h));
        g.addColorStop(0, `rgba(${b.c.join(',')},${b.a})`);
        g.addColorStop(0.55, `rgba(${b.c.join(',')},${b.a * 0.72})`);
        g.addColorStop(1, `rgba(${b.c.join(',')},0)`);
        s.fillStyle = g;
        s.beginPath();
        s.ellipse(b.x * w, b.y * h, b.rx * w, b.ry * h, 0, 0, Math.PI * 2);
        s.fill();
      });

      const src = s.getImageData(0, 0, w, h).data;
      const ctx = canvas.getContext('2d');
      const out = ctx.createImageData(w, h);
      const px = out.data;

      for (let y = 0; y < h; y++) {
        const row = (y & 3) * 4;
        for (let x = 0; x < w; x++) {
          const i = (y * w + x) * 4;
          const a = src[i + 3];
          if (a === 0) continue;
          const t = ((BAYER[row + (x & 3)] + 0.5) / 16) * 255;
          if (a > t) {
            px[i] = src[i];
            px[i + 1] = src[i + 1];
            px[i + 2] = src[i + 2];
            px[i + 3] = 255;
          }
        }
      }
      ctx.putImageData(out, 0, 0);
    }

    paint();
    let rt = null;
    window.addEventListener('resize', () => {
      clearTimeout(rt);
      rt = setTimeout(paint, 220);
    });
  }

  /* ── background music ───────────────────────────────────────
     Browsers only start audio without a gesture in some cases, so we
     try on load, fall back to the first interaction, and always keep a
     visible toggle.                                                     */
  const audio = document.getElementById('bgm');
  const soundBtn = document.getElementById('sound');

  if (audio && soundBtn) {
    const LEVEL = 0.32;
    const FADE_MS = 1600;
    let fade = null;
    let started = false;

    const paintButton = (on) => {
      soundBtn.setAttribute('aria-pressed', String(on));
      soundBtn.classList.remove('is-idle');
      soundBtn.setAttribute(
        'aria-label',
        on ? '背景音乐：关 / Background music: off'
           : '背景音乐：开 / Background music: on'
      );
    };

    const fadeTo = (to, ms = FADE_MS) => new Promise((resolve) => {
      if (fade) clearInterval(fade);
      const from = Number.isFinite(audio.volume) ? audio.volume : 0;
      const t0 = performance.now();
      fade = setInterval(() => {
        const p = Math.min(1, (performance.now() - t0) / ms);
        audio.volume = Math.max(0, Math.min(1, from + (to - from) * p));
        if (p >= 1) {
          clearInterval(fade);
          fade = null;
          resolve();
        }
      }, 40);
    });

    /* first-gesture unlock: declared up front so giveUp() can always unbind */
    let unlock = null;
    const events = ['pointerdown', 'keydown', 'touchstart', 'wheel'];
    const detach = () => {
      if (unlock) events.forEach((e) => window.removeEventListener(e, unlock));
    };

    /* the audio file is broken or not decodable — don't leave a dead button */
    const giveUp = () => {
      soundBtn.hidden = true;
      detach();
    };

    const start = async () => {
      audio.volume = 0;
      try {
        await audio.play();
        started = true;
        paintButton(true);
        fadeTo(LEVEL);
        return true;
      } catch (err) {
        if (err && err.name === 'NotSupportedError') { giveUp(); return false; }
        paintButton(false);
        soundBtn.classList.add('is-idle');
        return false;
      }
    };

    const stop = async () => {
      await fadeTo(0, 500);
      audio.pause();
      paintButton(false);
    };

    /* autoplay on arrival, unless the visitor muted it last time */
    const saved = (() => {
      try { return localStorage.getItem('cpc:music'); } catch (e) { return null; }
    })();
    if (saved !== 'off') start();

    /* if autoplay was blocked, start at the first interaction instead */
    unlock = (ev) => {
      if (ev && ev.target && ev.target.closest && ev.target.closest('#sound')) return;
      if (!audio.paused) return;
      start().then((ok) => { if (ok) detach(); });
    };
    events.forEach((e) => window.addEventListener(e, unlock, { passive: true }));

    soundBtn.addEventListener('click', async (ev) => {
      ev.stopPropagation();
      if (audio.paused) {
        const ok = await start();
        if (ok) {
          detach();
          try { localStorage.setItem('cpc:music', 'on'); } catch (e) {}
        }
      } else {
        await stop();
        try { localStorage.setItem('cpc:music', 'off'); } catch (e) {}
      }
    });

    /* keep the icon honest if playback stops for another reason */
    audio.addEventListener('pause', () => { if (!started) paintButton(false); });
    audio.addEventListener('play', () => paint(true));
  }
})();
