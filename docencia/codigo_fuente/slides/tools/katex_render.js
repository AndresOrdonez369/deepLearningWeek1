// usage: node katex_render.js < in.json > out.json   (array of TeX strings -> array of HTML)
const katex = require(process.env.KATEX_PATH || 'katex');
let s = '';
process.stdin.on('data', d => s += d);
process.stdin.on('end', () => {
  const arr = JSON.parse(s);
  const out = arr.map(t => katex.renderToString(t, { throwOnError: true, displayMode: false, output: 'html' }));
  process.stdout.write(JSON.stringify(out));
});
