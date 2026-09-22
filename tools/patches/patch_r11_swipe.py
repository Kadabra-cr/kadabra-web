"""Round 11: phone piles, the finish veil, cables to the task line, hover without flicker."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, '..', '..', 'src', 'app.src.js')
s = open(p, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


# ---- phones: the two answer buttons are the piles --------------------------
rep('''  var idx = 0, els = [], minis = [], drag = null, done = false, touched = false, nudgeTimer = 0, nudgeBack = 0, nudgeSide = 1;''',
'''  var idx = 0, els = [], minis = [], drag = null, done = false, touched = false, nudgeTimer = 0, nudgeBack = 0, nudgeSide = 1;
  /* phones get their own table: no piles beside the deck, the two answer
     buttons are the piles. A sent card flies into its button and leaves a
     small card in it. */
  var phone = matchMedia('(max-width:900px)');
  var bL = document.getElementById('bLeft'), bR = document.getElementById('bRight');
  [bL, bR].forEach(function (b) { b.insertAdjacentHTML('beforeend', '<span class="tally" aria-hidden="true"></span>'); });
  function pileOf(dir) { return phone.matches ? (dir > 0 ? bR : bL) : (dir > 0 ? pileR : pileL); }''')
rep('''      (right ? pileR : pileL).classList.add('nudge');''', '''      pileOf(right ? 1 : -1).classList.add('nudge');''')
rep('''        pileR.classList.remove('nudge');
        pileL.classList.remove('nudge');
        if (el.classList.contains('piled')) return;''', '''        [pileR, pileL, bL, bR].forEach(function (p) { p.classList.remove('nudge'); });
        if (el.classList.contains('piled')) return;''')
rep('''    pileR.classList.remove('nudge');
    pileL.classList.remove('nudge');
    els.forEach(function (el) { el.classList.remove('nudging', 'nudging-l'); });''', '''    [pileR, pileL, bL, bR].forEach(function (p) { p.classList.remove('nudge'); });
    els.forEach(function (el) { el.classList.remove('nudging', 'nudging-l'); });''')
rep('''  function pileSpot(dir, k) {
    var pile = (dir > 0 ? pileR : pileL).getBoundingClientRect();''', '''  function pileSpot(dir, k) {
    if (phone.matches) {
      /* into the button: small, turned, gone */
      var bt = pileOf(dir).getBoundingClientRect(), dk = deck.getBoundingClientRect();
      return 'translate(' + (bt.left + bt.width / 2 - dk.left - dk.width / 2).toFixed(1) + 'px,' +
        (bt.top + bt.height / 2 - dk.top - dk.height / 2).toFixed(1) + 'px) rotate(' + (dir * 24) + 'deg) scale(.14)';
    }
    var pile = (dir > 0 ? pileR : pileL).getBoundingClientRect();''')
rep('''    (dir > 0 ? pileR : pileL).classList.add('hot');
    el.style.zIndex = 40 + idx;
    el.style.pointerEvents = 'none';
    el.style.transition = reduce ? 'none' : 'transform .68s cubic-bezier(.16,1,.3,1)';
    el.style.transform = pileSpot(dir, k);
    el.classList.add('piled');''', '''    pileOf(dir).classList.add('hot');
    el.style.zIndex = 40 + idx;
    el.style.pointerEvents = 'none';
    if (phone.matches) {
      var b = pileOf(dir);
      el.style.transition = reduce ? 'none' : 'transform .5s cubic-bezier(.5,0,.75,0), opacity .22s linear .3s';
      el.style.opacity = '0';
      setTimeout(function () {
        b.querySelector('.tally').insertAdjacentHTML('beforeend', '<i></i>');
        b.classList.remove('landed'); void b.offsetWidth; b.classList.add('landed');
      }, reduce ? 0 : 460);
    } else el.style.transition = reduce ? 'none' : 'transform .68s cubic-bezier(.16,1,.3,1)';
    el.style.transform = pileSpot(dir, k);
    el.classList.add('piled');''')
rep('''    (dx > 0 ? pileR : pileL).classList.toggle('hot', Math.abs(dx) > 30);''', '''    pileOf(dx > 0 ? 1 : -1).classList.toggle('hot', Math.abs(dx) > 30);
    pileOf(dx > 0 ? -1 : 1).classList.remove('hot');''')

# ---- the finish: fade the table, hold the mark, lay the desk out unseen -----
start = s.index('  /* The hand is played. The table clears to the mark')
end = s.index('  /* Each card hangs a cable to its note.')
s = s[:start] + '''  /* The hand is played. The table fades, the mark holds the screen for a
     moment (with a small turning ring, so the wait reads as work), and the
     desk is laid out behind it, unseen. Then the mark lets go and the rows
     are dealt one after another. */
  var swipeSec = document.getElementById('swipe');
  function finish() {
    if (done) return;
    done = true;
    stopNudge();
    var narrow = phone.matches;
    minis = [];

    function lay() {
      var wrapW = desk.getBoundingClientRect().width;
      SLOT.w = Math.round(narrow ? Math.min(wrapW, 420) : Math.min(420, wrapW * .42)); SLOT.h = Math.round(SLOT.w * .6);
      btns.hidden = true; hint.hidden = true;
      heads.classList.add('flip'); stage.classList.add('flip');
      rows.innerHTML = '';
      els.forEach(function (el) {
        var cd = CARDS[els.indexOf(el)], right = el.dataset.dir === 'r';
        /* the card and its note swap sides row by row, whatever was answered */
        var flip = !narrow && +el.dataset.fn % 2 === 0;
        var row = document.createElement('div');
        row.className = 'row' + (flip ? ' flip' : '') + (reduce ? '' : ' dealt');
        row.dataset.fn = el.dataset.fn;
        var slot = document.createElement('div');
        slot.className = 'slot'; slot.dataset.fn = el.dataset.fn;
        slot.style.width = SLOT.w + 'px'; slot.style.height = SLOT.h + 'px';
        var note = document.createElement('div');
        note.className = 'note'; note.dataset.fn = el.dataset.fn; note.tabIndex = 0;
        note.innerHTML = '<p class="said">@@t.swipe.said@@ <b>' + (right ? '@@t.swipe.pileR@@' : '@@t.swipe.pileL@@') + '</b></p>' +
          '<p class="q">' + cd.q + '</p><p class="a">' + (right ? cd.r : cd.l) + '</p>';
        if (flip) { row.appendChild(note); row.appendChild(slot); } else { row.appendChild(slot); row.appendChild(note); }
        rows.appendChild(row);
        slot.appendChild(el);
        el.classList.remove('piled'); el.classList.add('desk');
        el.style.zIndex = ''; el.style.pointerEvents = ''; el.style.transition = 'none'; el.style.transform = 'none';
        el.style.opacity = '';
        el.style.width = SLOT.w + 'px'; el.style.height = SLOT.h + 'px';
        minis.push(slot);
      });
      reveal.hidden = false;
    }
    function dealRows() {
      var list = [].slice.call(rows.querySelectorAll('.row'));
      list.forEach(function (r, i) { setTimeout(function () { r.classList.remove('dealt'); }, 120 + i * 190); });
      if (!narrow) setTimeout(drawCables, 120 + list.length * 190 + 600);
    }

    if (reduce) { lay(); rows.querySelectorAll('.row').forEach(function (r) { r.classList.remove('dealt'); }); if (!narrow) drawCables(); return; }
    swipeSec.classList.add('clearing');                  /* the table fades first */
    var veil = document.createElement('div');
    veil.className = 'veil';
    veil.innerHTML = '<svg class="mark" viewBox="0 0 1703.11 435.6" aria-hidden="true"><use href="#logo-full" width="1703.11" height="435.6"/></svg>' +
      '<svg class="ring" viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="16"/></svg>';
    document.body.appendChild(veil);
    setTimeout(function () { veil.classList.add('on'); }, 380);
    /* opaque from ~1s: only now is the page rebuilt, so the work is never seen */
    setTimeout(function () {
      lay();
      swipeSec.classList.remove('clearing');
      var hdr = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--hdr')) || 72;
      window.scrollTo(0, heads.getBoundingClientRect().top + scrollY - hdr - 24);
    }, 1150);
    setTimeout(function () { veil.classList.add('out'); dealRows(); }, 3300);
    setTimeout(function () { if (veil.parentNode) veil.parentNode.removeChild(veil); }, 4300);
  }

''' + s[end:]

# ---- cables: to the task line, a little tighter; hover without flicker -------
rep('''      var band = m.querySelector('.cband') || m, said = note.querySelector('.said') || note;''',
    '''      var band = m.querySelector('.cband') || m, said = note.querySelector('.q') || note;''')
rep('''      var len = span * 1.16 + 24, seg = len / (N - 1), pts = [];''', '''      var len = span * 1.07 + 10, seg = len / (N - 1), pts = [];''')
rep('''  var hotRope = null;
  desk.addEventListener('pointermove', function (e) {
    if (!ropes.length) return;
    var l = ropeLocal(e); ptrR.x = l.x; ptrR.y = l.y; ptrR.on = true;
    if (grabbed) { grabbed.rope.pts[grabbed.i].x = l.x; grabbed.rope.pts[grabbed.i].y = l.y; return; }
    var nb = nearest(l.x, l.y, 30);
    var fn = nb ? nb.rope.fn : null;
    if (fn !== hotRope) { if (hotRope) hot(hotRope, false); if (fn) hot(fn, true); hotRope = fn; }
    desk.style.cursor = nb ? 'grab' : '';
  }, { passive: true });
  desk.addEventListener('pointerleave', function () {
    ptrR.on = false; ptrR.x = ptrR.y = -1e4;
    if (hotRope) { hot(hotRope, false); hotRope = null; }
    desk.style.cursor = '';
  }, { passive: true });''', '''  /* one owner for the highlight: whatever the pointer is over (a card, a
     note) or close to (a cable). A cable once lit stays lit until the pointer
     is well clear of it, and letting go waits a beat: no flicker. */
  var hotFn = null, coolT = 0;
  function setHot(fn) {
    if (fn) { clearTimeout(coolT); coolT = 0; }
    if (fn === hotFn) return;
    if (!fn) { if (!coolT) coolT = setTimeout(function () { coolT = 0; if (hotFn) hot(hotFn, false); hotFn = null; }, 220); return; }
    if (hotFn) hot(hotFn, false);
    hot(fn, true); hotFn = fn;
  }
  desk.addEventListener('pointermove', function (e) {
    var l = ropeLocal(e); ptrR.x = l.x; ptrR.y = l.y; ptrR.on = true;
    if (grabbed) { grabbed.rope.pts[grabbed.i].x = l.x; grabbed.rope.pts[grabbed.i].y = l.y; return; }
    var el = e.target.closest ? e.target.closest('[data-fn]') : null;
    var nb = ropes.length ? nearest(l.x, l.y, 34) : null;
    if (!nb && hotFn && ropes.length) { var keep = nearest(l.x, l.y, 80); if (keep && keep.rope.fn === hotFn) nb = keep; }
    setHot(el ? el.dataset.fn : nb ? nb.rope.fn : null);
    desk.style.cursor = nb && !el ? 'grab' : '';
  }, { passive: true });
  desk.addEventListener('pointerleave', function () {
    ptrR.on = false; ptrR.x = ptrR.y = -1e4;
    setHot(null);
    desk.style.cursor = '';
  }, { passive: true });''')
rep('''  function link() {
    function fnOf(e) { var el = e.target.closest ? e.target.closest('[data-fn]') : null; return el && el.dataset.fn; }
    desk.addEventListener('pointerover', function (e) { var fn = fnOf(e); if (fn) hot(fn, true); }, { passive: true });
    desk.addEventListener('pointerout', function (e) { var fn = fnOf(e); if (fn) hot(fn, false); }, { passive: true });
    desk.addEventListener('focusin', function (e) { var fn = fnOf(e); if (fn) hot(fn, true); });
    desk.addEventListener('focusout', function (e) { var fn = fnOf(e); if (fn) hot(fn, false); });
  }''', '''  function link() {
    function fnOf(e) { var el = e.target.closest ? e.target.closest('[data-fn]') : null; return el && el.dataset.fn; }
    desk.addEventListener('focusin', function (e) { setHot(fnOf(e)); });
    desk.addEventListener('focusout', function () { setHot(null); });
  }''')
# the brush is gentler than the pick-up radius, so a lit cable is not pushed out from under the hand
rep('''            if (d < 44 && d > 0) { var f = (1 - d / 44) * 2.2; p.x += dx / d * f; p.y += dy / d * f; }''',
    '''            if (d < 40 && d > 0) { var f = (1 - d / 40) * 1.1; p.x += dx / d * f; p.y += dy / d * f; }''')
# resize: no cables on phones
rep('''    rz = setTimeout(drawCables, 180);''', '''    rz = setTimeout(function () { if (phone.matches) { cables.innerHTML = ''; ropes = []; } else drawCables(); }, 180);''')
# reset: tallies emptied
rep('''    pileL.classList.remove('hot'); pileR.classList.remove('hot');''', '''    [pileL, pileR, bL, bR].forEach(function (p) { p.classList.remove('hot', 'landed'); });
    [bL, bR].forEach(function (b) { b.querySelector('.tally').innerHTML = ''; });''')
rep('''      el.style.transition = 'none'; el.style.transform = reduce ? rest : 'none';''', '''      el.style.transition = 'none'; el.style.transform = reduce ? rest : 'none'; el.style.opacity = '';''')
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
