// zutot talk slides — minimal slide engine (no dependencies), LTR.
// Keys: →/Space/PageDown = next, ←/PageUp = previous, Home/End,
// F = fullscreen, Esc = back to the home page (also from fullscreen).
// No speaker-notes key: <aside> notes stay hidden. Arrow keys always change slides,
// even when a slider has focus (a deck may add its own non-arrow keys).
(function () {
  const stage = document.getElementById('stage');
  const slides = Array.from(stage.querySelectorAll('.slide'));
  const progress = document.createElement('div'); progress.id = 'progress';
  const counter = document.createElement('div'); counter.id = 'counter';
  document.body.append(progress, counter);

  let i = Math.max(0, Math.min(slides.length - 1, (parseInt(location.hash.slice(1), 10) || 1) - 1));

  function fit() {
    const s = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
    stage.style.transform = `translate(-50%, -50%) scale(${s})`;
  }

  function show(n) {
    i = Math.max(0, Math.min(slides.length - 1, n));
    slides.forEach((el, k) => el.classList.toggle('active', k === i));
    progress.style.width = `${((i + 1) / slides.length) * 100}%`;
    counter.textContent = `${i + 1} / ${slides.length}`;
    history.replaceState(null, '', `#${i + 1}`);
  }

  const home = () => { location.href = '../../'; };
  let fsByKey = false;
  // Esc in fullscreen is swallowed by the browser (it exits fullscreen): go home then too,
  // unless fullscreen was left with F.
  document.addEventListener('fullscreenchange', () => {
    if (!document.fullscreenElement && !fsByKey) home();
    fsByKey = false;
  });
  const interactive = (t) => t && t.closest && t.closest('input, select, textarea, .interactive');

  document.addEventListener('keydown', (e) => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    switch (e.key) {
      case 'ArrowRight': case 'ArrowDown': case ' ': case 'PageDown': case 'Enter':
        e.preventDefault(); show(i + 1); break;
      case 'ArrowLeft': case 'ArrowUp': case 'PageUp': case 'Backspace':
        e.preventDefault(); show(i - 1); break;
      case 'Home': show(0); break;
      case 'End': show(slides.length - 1); break;
      case 'f': case 'F':
        fsByKey = true;
        if (document.fullscreenElement) document.exitFullscreen();
        else document.documentElement.requestFullscreen();
        break;
      case 'Escape': home(); break;
    }
  });

  // click: right half = next, left half = previous
  document.addEventListener('click', (e) => {
    if (e.target.closest('a') || interactive(e.target)) return;
    show(e.clientX > window.innerWidth / 2 ? i + 1 : i - 1);
  });

  // swipe
  let x0 = null;
  document.addEventListener('touchstart', (e) => { x0 = interactive(e.target) ? null : e.touches[0].clientX; }, { passive: true });
  document.addEventListener('touchend', (e) => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 40) show(dx < 0 ? i + 1 : i - 1);
  });

  window.addEventListener('resize', fit);
  window.addEventListener('hashchange', () => show((parseInt(location.hash.slice(1), 10) || 1) - 1));
  fit(); show(i);
})();
