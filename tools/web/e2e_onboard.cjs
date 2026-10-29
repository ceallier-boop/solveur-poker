// Premier lancement en trois écrans et niveaux (programme de travail, étape 4).
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_onboard.cjs [dossier]
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
(async () => {
  const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true })).newPage();
  const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE); await p.waitForSelector('#screen-onboard:not([hidden])', { timeout: 15000 });
  const res = { step1: await p.innerText('#ob-1'), nextDisabled: await p.isDisabled('#ob-next') };
  await p.screenshot({ path: `${OUT}/ob_1.png` });
  await p.click('#ob-exp button[data-v="confirme"]'); await p.click('#ob-goal button[data-v="ranges"]'); await p.click('#ob-next');
  res.step2 = await p.innerText('#ob-2'); res.proposed = await p.textContent('#ob-levels [aria-pressed="true"]'); await p.screenshot({ path: `${OUT}/ob_2.png` });
  await p.click('#ob-next'); res.step3 = await p.innerText('#ob-3'); await p.screenshot({ path: `${OUT}/ob_3.png` });
  await p.click('#ob-next'); await p.waitForSelector('#screen-home:not([hidden])'); await p.waitForSelector('#today-level:not([hidden])', { timeout: 10000 });
  res.level = (await p.innerText('#today-level')).replace(/\n+/g, ' | '); res.theme = await p.textContent('#today-steps li:nth-child(2)');
  await p.screenshot({ path: `${OUT}/ob_home.png` });
  await p.click('#today-level'); await p.waitForSelector('#st-level:not([hidden])', { timeout: 10000 });
  res.myLevel = (await p.innerText('#st-level')).replace(/\n+/g, ' | ');
  await p.click('#st-level-pick button[data-v="1"]'); await p.waitForTimeout(800); res.picked = await p.textContent('#st-level-name');
  await p.click('#st-back'); await p.waitForTimeout(1500); res.themeAfter = await p.textContent('#today-steps li:nth-child(2)');
  await p.reload(); await p.waitForSelector('#screen-home:not([hidden])', { timeout: 15000 }); res.noOnboardAgain = await p.isHidden('#screen-onboard');
  res.errs = errs; console.log(JSON.stringify(res, null, 1)); await b.close();
})();
