'use strict';
// Administration des signalements : consomme /admin/reports, /admin/reports/{id}/resolve, /admin/disabled, /admin/log.
const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const ses = {
  get(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
  set(k, v) { try { sessionStorage.setItem(k, v); } catch (e) { /* stockage indisponible */ } },
  del(k) { try { sessionStorage.removeItem(k); } catch (e) { /* idem */ } },
};
const state = { token: ses.get('admin_token'), actor: ses.get('admin_actor') || '', tab: 'open' };
const date = (iso) => iso ? new Date(iso).toLocaleString('fr-FR', { dateStyle: 'short', timeStyle: 'short' }) : '';

async function api(path, opts = {}) {
  const r = await fetch(path, { ...opts, headers: { 'content-type': 'application/json', 'X-Admin-Token': state.token || '' } });
  const body = await r.json().catch(() => ({}));
  if (r.status === 403) { logout(body.detail); throw new Error(body.detail || 'accès refusé'); }
  if (!r.ok) throw new Error(body.detail || `Erreur ${r.status}`);
  return body;
}

function logout(msg) {
  ses.del('admin_token'); state.token = null;
  $('panel').hidden = true; $('login').hidden = false;
  $('login-error').hidden = !msg; $('login-error').textContent = msg || '';
}

function reportCard(r) {
  const c = r.correction;
  const strat = c ? c.strategy.map((s) => `${esc(s.label_fr)} ${String(s.pct).replace('.', ',')} %`).join(' · ') : '';
  const many = r.reports_on_spot > 1;
  const resolved = r.status !== 'open'
    ? `<p><b>${r.status === 'accepted' ? 'Accepté' : 'Rejeté'}</b> le ${date(r.resolved_at)} : ${esc(r.resolution)}</p>` : '';
  const form = r.status === 'open' ? `
    <form class="resolve" data-id="${r.id}">
      <label class="sr-only" for="res-${r.id}">Décision motivée</label>
      <textarea id="res-${r.id}" rows="2" minlength="3" maxlength="1000" required placeholder="Décision motivée (visible dans le journal)"></textarea>
      <div class="row">
        <label><input type="checkbox" name="disable"> Retirer ce spot du tirage</label>
      </div>
      <div class="row">
        <button class="primary" type="submit" value="accepted">Accepter</button>
        <button class="secondary" type="submit" value="rejected">Rejeter</button>
      </div>
    </form>` : '';
  return `<article class="item">
    <div class="row"><span class="tag${many ? ' many' : ''}">${esc(r.reason_fr)}</span>${many ? `<span class="tag many">${r.reports_on_spot} signalements sur ce spot</span>` : ''}</div>
    <p>${esc(r.prompt_fr || '(spot introuvable dans le dataset)')}</p>
    ${c ? `<p>Réponse du joueur : <b>${esc(c.chosen_label)}</b> · verdict : ${esc(c.verdict)} · meilleure action : <b>${esc(c.best_label)}</b></p>
    <details><summary>Correction affichée au joueur</summary><p>${esc(c.explanation_fr)}</p><p class="meta">${strat}</p></details>` : ''}
    ${r.comment ? `<blockquote>${esc(r.comment)}</blockquote>` : ''}
    <p class="meta">${date(r.created_at)} · dataset ${esc(r.dataset_version)} · spot ${esc(r.spot_id)} · main ${esc(r.hand)}</p>
    ${resolved}${form}
  </article>`;
}

function disabledCard(d) {
  return `<article class="item">
    <p><b>${esc(d.spot_id)}</b></p>
    <p>${esc(d.reason)}</p>
    <p class="meta">Retiré le ${date(d.disabled_at)} par ${esc(d.actor)} · dataset ${esc(d.dataset_version)} · signalement n° ${d.report_id ?? '—'}</p>
    <form class="enable" data-spot="${esc(d.spot_id)}">
      <label class="sr-only" for="en-${esc(d.spot_id)}">Motif de la remise en service</label>
      <textarea id="en-${esc(d.spot_id)}" rows="2" minlength="3" required placeholder="Motif de la remise en service"></textarea>
      <div class="row"><button class="secondary" type="submit">Remettre dans le tirage</button></div>
    </form>
  </article>`;
}

function logCard(e) {
  const d = e.details || {};
  const what = e.action === 'resolve_report'
    ? `Signalement n° ${d.report_id} ${d.status === 'accepted' ? 'accepté' : 'rejeté'}${d.disabled_spot ? `, spot ${esc(d.disabled_spot)} retiré` : ''} : ${esc(d.resolution)}`
    : e.action === 'enable_spot' ? `Spot ${esc(d.spot_id)} remis dans le tirage : ${esc(d.reason)}` : esc(e.action);
  return `<article class="item"><p>${what}</p><p class="meta">${date(e.at)} · ${esc(e.actor)}</p></article>`;
}

async function render() {
  for (const b of document.querySelectorAll('.tabs button')) b.setAttribute('aria-pressed', String(b.dataset.tab === state.tab));
  const list = $('list'); list.innerHTML = '<p class="lead">Chargement…</p>';
  try {
    let rows, html;
    if (state.tab === 'disabled') { rows = await api('/admin/disabled'); html = rows.map(disabledCard); }
    else if (state.tab === 'log') { rows = (await api('/admin/log')).reverse(); html = rows.map(logCard); }
    else { rows = await api(`/admin/reports?status=${state.tab}`); html = rows.map(reportCard); }
    $('count').textContent = `${rows.length} élément${rows.length > 1 ? 's' : ''}`;
    list.innerHTML = html.join('') || '<p class="lead">Rien ici.</p>';
  } catch (e) { list.innerHTML = `<p class="error">${esc(e.message)}</p>`; }
}

$('list').addEventListener('submit', async (e) => {
  e.preventDefault();
  const f = e.target; const text = f.querySelector('textarea').value.trim();
  if (text.length < 3) { f.querySelector('textarea').focus(); return; }
  for (const b of f.querySelectorAll('button')) b.disabled = true;
  try {
    if (f.classList.contains('resolve')) {
      const status = e.submitter ? e.submitter.value : 'rejected';
      await api(`/admin/reports/${f.dataset.id}/resolve`, { method: 'POST', body: JSON.stringify({ status, resolution: text, disable_spot: f.querySelector('[name=disable]').checked, actor: state.actor }) });
    } else {
      await api(`/admin/disabled/${encodeURIComponent(f.dataset.spot)}?reason=${encodeURIComponent(text)}&actor=${encodeURIComponent(state.actor)}`, { method: 'DELETE' });
    }
    await render();
  } catch (err) { alert(err.message); for (const b of f.querySelectorAll('button')) b.disabled = false; }
});
document.querySelector('.tabs').addEventListener('click', (e) => {
  const b = e.target.closest('button'); if (!b) return; state.tab = b.dataset.tab; render();
});
$('login-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  state.token = $('token').value; state.actor = $('actor').value.trim();
  try {
    await api('/admin/reports?status=open');
    ses.set('admin_token', state.token); ses.set('admin_actor', state.actor);
    $('login').hidden = true; $('panel').hidden = false; render();
  } catch (err) { /* logout() affiche déjà le message */ }
});
$('actor').value = state.actor;
if (state.token) { $('login').hidden = true; $('panel').hidden = false; render(); }
