"""Round 11: the workshop smoke clears under the hand and shows the suit behind it."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, '..', '..', 'src', 'app.src.js')
s = open(p, encoding='utf-8').read()
start = s.index("    if (kind === 'smoke') {")
end = s.index("    } else if (kind === 'desk') {")
s = s[:start] + r'''    if (kind === 'smoke') {
      /* a thick, slow cloud of the brand squares, softened, rising. The hand
         parts it; behind it a square that turns into a spade the clearer the
         middle gets. Left alone, it closes again. With no hand for a while, a
         slow ghost hand passes through, so phones see it too. */
      var defs = document.createElementNS(NS, 'defs');
      defs.innerHTML = '<filter id="smokeblur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.6"/></filter>';
      svg.appendChild(defs);
      var symG = document.createElementNS(NS, 'g'), symP = document.createElementNS(NS, 'path');
      symP.setAttribute('fill', '#C9A227'); symP.setAttribute('d', PATHS.square);
      symG.setAttribute('transform', 'translate(160 110) scale(1.15) translate(-50 -50)');
      symG.setAttribute('opacity', '0'); symG.appendChild(symP); svg.appendChild(symG);
      var cloud = document.createElementNS(NS, 'g');
      cloud.setAttribute('filter', 'url(#smokeblur)'); svg.appendChild(cloud);
      var puffs = [];
      for (var i = 0; i < 58; i++) {
        var g = document.createElementNS(NS, 'g'), p = document.createElementNS(NS, 'path');
        p.setAttribute('fill', 'currentColor'); p.setAttribute('d', PATHS.square);
        g.appendChild(p); cloud.appendChild(g);
        var a = Math.random() * Math.PI * 2, rr = Math.pow(Math.random(), .7);
        puffs.push({ g: g, hx: 160 + Math.cos(a) * rr * 120, hy: 30 + Math.random() * 170, s: rnd(22, 58),
          o: rnd(.16, .34), rot: rnd(0, 90), vr: rnd(-9, 9), rise: rnd(5, 12), ph: rnd(0, 6.3), ox: 0, oy: 0 });
      }
      var hand = { x: -1e3, y: -1e3, at: -1e4 }, clear = 0, smokeOn = false, last = 0;
      function toLocal(e) {
        var b = svg.getBoundingClientRect(), k = 320 / b.width;
        hand.x = (e.clientX - b.left) * k; hand.y = (e.clientY - b.top) * k; hand.at = performance.now();
      }
      svg.addEventListener('pointermove', toLocal, { passive: true });
      svg.addEventListener('pointerdown', toLocal, { passive: true });
      svg.addEventListener('pointerleave', function () { hand.x = hand.y = -1e3; }, { passive: true });
      function draw(now) {
        var dt = last ? Math.min(.05, (now - last) / 1000) : 0; last = now;
        var hx = hand.x, hy = hand.y;
        if (now - hand.at > 3200) {                 /* the ghost hand */
          var u = now / 1000;
          hx = 160 + Math.sin(u * .55) * 70; hy = 110 + Math.sin(u * 1.1) * 38;
        }
        var near = 0;
        for (var i = 0; i < puffs.length; i++) {
          var q = puffs[i];
          q.hy -= q.rise * dt;
          if (q.hy < 18) { q.hy = 205; q.hx = 160 + rnd(-120, 120); }
          q.rot += q.vr * dt;
          var x = q.hx + Math.sin(now / 1900 + q.ph) * 9 + q.ox, y = q.hy + q.oy;
          var dx = x - hx, dy = y - hy, d = Math.hypot(dx, dy) || 1;
          if (d < 78) { var f = (1 - d / 78) * 520 * dt; q.ox += dx / d * f; q.oy += dy / d * f; }
          q.ox -= q.ox * Math.min(1, .9 * dt); q.oy -= q.oy * Math.min(1, .9 * dt);   /* closes back, slowly */
          x = q.hx + Math.sin(now / 1900 + q.ph) * 9 + q.ox; y = q.hy + q.oy;
          if (Math.hypot(x - 160, y - 110) < 62) near += q.s / 40;
          var edge = Math.min(1, (q.hy - 18) / 40, (205 - q.hy) / 30);
          q.g.setAttribute('opacity', (q.o * Math.max(0, edge)).toFixed(3));
          q.g.setAttribute('transform', 'translate(' + x.toFixed(1) + ' ' + y.toFixed(1) + ') rotate(' + q.rot.toFixed(1) +
            ') scale(' + (q.s / 100).toFixed(3) + ') translate(-50 -50)');
        }
        /* the fewer (and smaller) puffs over the middle, the clearer it is */
        var want = Math.max(0, Math.min(1, 1 - (near - 2) / 7));
        clear += (want - clear) * Math.min(1, 2.4 * dt);
        symG.setAttribute('opacity', (.12 + clear * .88).toFixed(3));
        symP.setAttribute('d', mix('smooth-spade', easeOut(clear)));
        if (clear > .85) symG.classList.add('glow'); else symG.classList.remove('glow');
      }
      if (reduce) { draw(0); symG.setAttribute('opacity', '1'); symP.setAttribute('d', mix('smooth-spade', 1)); }
      else {
        new IntersectionObserver(function (es) {
          smokeOn = es[0].isIntersecting;
          if (smokeOn) { last = 0; requestAnimationFrame(function step(now) { if (!smokeOn) return; draw(now); requestAnimationFrame(step); }); }
        }).observe(svg);
      }
''' + s[end:]
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
