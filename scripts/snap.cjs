// node snap.js <index.html> <outdir> t1 t2 ...   quick stills: seeks the timeline and shows clips active at t
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const [file, out, ...ts] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 0.5 });
  await p.goto('file://' + path.resolve(file));
  await p.evaluate(() => document.fonts.ready);
  for (const t of ts.map(Number)) {
    await p.evaluate((t) => {
      document.querySelectorAll('.clip').forEach(c => {
        const a = +c.dataset.start, d = +c.dataset.duration;
        c.style.display = (t >= a && t < a + d) ? '' : 'none';
      });
      window.__timelines.main.seek(t);
    }, t);
    await p.screenshot({ path: `${out}/t${t.toFixed(2).padStart(5, '0')}.png` });
  }
  await b.close();
})();
