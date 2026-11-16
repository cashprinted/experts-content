// Render one .dc.html artboard to PNG with the brand font and assets served locally.
// node graphics/render.js <in.dc.html> <out.png> <width> <height> [scale]
// Blob ids map to the files in brand/img (the Design canvas serves the same files by id).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [, , src, out, W, H, scale = '2'] = process.argv;
const ROOT = path.resolve(__dirname, '..');
const font = fs.readFileSync(path.join(ROOT, 'brand/fonts/archivo.woff2')).toString('base64');
const css = `@font-face{font-family:'Archivo';src:url(data:font/woff2;base64,${font}) format('woff2');font-weight:100 900;font-stretch:62% 125%;}`;
const BLOBS = JSON.parse(fs.readFileSync(path.join(ROOT, 'brand/canvas-assets.json')));
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +W, height: +H }, deviceScaleFactor: +scale });
  await p.route('**/*', (r) => {
    const u = r.request().url();
    for (const [id, f] of Object.entries(BLOBS)) if (u.includes(id)) return r.fulfill({ contentType: 'image/svg+xml', body: fs.readFileSync(path.join(ROOT, f)) });
    if (u.startsWith('file:')) return r.continue();
    return r.abort();
  });
  await p.goto('file://' + path.resolve(src));
  await p.addStyleTag({ content: css });
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.screenshot({ path: out, clip: { x: 0, y: 0, width: +W, height: +H } });
  await b.close();
})();
