// Navigation à cinq onglets (I9) : utilitaire commun des parcours dans le navigateur. Un élément de la feuille du profil (chrono, exercices
// adaptatifs, données) : la feuille s'ouvre le temps du clic, puis se referme.
// Avant de cliquer ou d'attendre un élément rangé dans un onglet qui n'est pas affiché, ouvre cet onglet ; un clic sur l'ancien
// choix de mode (.mode-switch [data-value="gto"|"exploit"]) devient un clic sur l'onglet GTO ou Exploitant.
// Usage : const page = await ctx.newPage().then(require('./nav_helper.cjs').wire);  puis, au besoin, await page.openTab('prog')
const MODE_TAB = { gto: 'gto', exploit: 'expl' };
const cssOf = (sel) => (typeof sel === 'string' ? sel.split(' >> ')[0].trim() : null);

async function openTab(page, tab) {
  await page.evaluate((t) => { const b = document.querySelector(`.tab[data-tab="${t}"]`); if (b) b.click(); }, tab);
  await page.waitForTimeout(400);
}

async function inSheet(page, sel) {                                  // l'élément est-il dans la feuille du profil, fermée ?
  const css = cssOf(sel); if (!css) return false;
  return page.evaluate((s) => { let el = null; try { el = document.querySelector(s); } catch (e) { return false; }
    const sh = el && el.closest('#profile'); return !!(sh && sh.hidden); }, css).catch(() => false);
}
const setSheet = (page, open) => page.evaluate((o) => { const sh = document.getElementById('profile'); if (sh) sh.hidden = !o; }, open);

async function reveal(page, sel) {                                   // ouvre l'onglet de l'élément s'il est dans une page cachée
  const css = cssOf(sel); if (!css) return false;
  const tab = await page.evaluate((s) => {
    let el = null; try { el = document.querySelector(s.replace(/:not\(\[hidden\]\)/g, '')); } catch (e) { return null; }   // un bloc encore caché : son onglet quand même
    const pg = el && el.closest('.tab-page'), bar = document.getElementById('tabs');
    return pg && pg.hidden && bar && !bar.hidden ? pg.dataset.tab : null;
  }, css).catch(() => null);
  if (!tab) return false;
  await openTab(page, tab); return true;
}

function wire(page) {
  const click = page.click.bind(page), tap = page.tap.bind(page), wait = page.waitForSelector.bind(page);
  page.click = async (sel, opts) => {
    const m = /^\.mode-switch \[data-value="(gto|exploit)"\]$/.exec(cssOf(sel) || '');
    if (m) { await page.evaluate((t) => { const b = document.querySelector(`.tab[data-tab="${t}"]`); if (b) b.click(); }, MODE_TAB[m[1]]); return; }
    if (await inSheet(page, sel)) { await setSheet(page, true); try { return await click(sel, opts); } finally { await setSheet(page, false); } }   // réglages et données : feuille du profil
    await reveal(page, sel); return click(sel, opts);
  };
  page.tap = async (sel, opts) => {
    if (await inSheet(page, sel)) { await setSheet(page, true); try { return await tap(sel, opts); } finally { await setSheet(page, false); } }
    await reveal(page, sel); return tap(sel, opts);
  };
  page.waitForSelector = async (sel, opts) => {
    if (!opts || !opts.state || opts.state === 'visible') await reveal(page, sel);
    return wait(sel, opts);
  };
  page.openTab = (tab) => openTab(page, tab);
  return page;
}

module.exports = { wire, openTab };
