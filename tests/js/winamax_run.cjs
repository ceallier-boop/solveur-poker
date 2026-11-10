// Lance spinsacademy/web/winamax.js sous Node comme dans le navigateur (objet window) sur les fichiers d'un dossier, dans
// l'ordre de winamax_counts.py (noms triés), et écrit sur la sortie standard {result, csv}. Usage : node winamax_run.cjs <dossier>
const fs = require('fs'), path = require('path'), vm = require('vm');
const ctx = { window: {}, setTimeout, Promise, console };
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(__dirname, '..', '..', 'spinsacademy', 'web', 'winamax.js'), 'utf8'), ctx);
const W = ctx.window.Winamax, dir = process.argv[2];
const files = fs.readdirSync(dir).sort().filter((n) => fs.statSync(path.join(dir, n)).isFile())
  .map((n) => ({ name: n, text: fs.readFileSync(path.join(dir, n), 'utf8') }));
let progress = 0;
W.analyze(files, () => { progress += 1; }).then((r) => {
  process.stdout.write(JSON.stringify({ result: r, csv: W.toCsv(r), progress, version: W.VERSION }));
}).catch((e) => { process.stderr.write(String(e && e.message || e)); process.exit(2); });
