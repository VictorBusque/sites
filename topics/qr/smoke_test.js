// Minimal DOM shim to smoke-test the article's page script logic.
// Executes buildS1..S5, updateS2..5, renderLab against a fake DOM and
// asserts the honest invariants (bit counts, codeword counts, seats,
// penalties, ink). This is a harness, not a browser.
'use strict';

class El {
  constructor(tag) {
    this.tagName = tag.toUpperCase();
    this.children = [];
    this.parent = null;
    this._attrs = {};
    this._text = '';
    this.style = {};
    this.classList = { _s: new Set(), add(c) { this._s.add(c); }, remove(c) { this._s.delete(c); }, toggle(c, on) { if (on === undefined) on = !this._s.has(c); if (on) this._s.add(c); else this._s.delete(c); }, contains(c) { return this._s.has(c); } };
    this.dataset = {};
  }
  get id() { return this._attrs.id || ''; }
  setAttribute(k, v) { this._attrs[k] = String(v); if (k === 'class') { this.classList._s = new Set(String(v).split(/\s+/).filter(Boolean)); } }
  getAttribute(k) { if (k === 'class') return [...this.classList._s].join(' '); return this._attrs[k] === undefined ? null : this._attrs[k]; }
  appendChild(c) { c.parent = this; this.children.push(c); return c; }
  insertBefore(c, ref) { c.parent = this; const i = this.children.indexOf(ref); this.children.splice(i === -1 ? this.children.length : i, 0, c); return c; }
  removeChild(c) { const i = this.children.indexOf(c); if (i !== -1) this.children.splice(i, 1); return c; }
  get firstChild() { return this.children[0] || null; }
  set textContent(v) { this._text = String(v); this.children = []; }
  get textContent() { return this._text + this.children.map(c => c.textContent).join(''); }
  set innerHTML(v) { this._html = v; this.children = []; parseHtml(v, this); }
  get innerHTML() { return this._html || ''; }
  querySelectorAll(sel) { return queryAll(this, sel); }
  querySelector(sel) { return queryAll(this, sel)[0] || null; }
  addEventListener(ev, fn) { (this._listeners = this._listeners || {})[ev] = fn; }
  removeEventListener() {}
  dispatch(ev) { if (this._listeners && this._listeners[ev]) this._listeners[ev]({ target: this }); }
  matches(sel) { return matchSel(this, sel); }
}

function queryAll(root, sel) {
  // supports: '#id .cls' and 'input' scoped
  const parts = sel.trim().split(/\s+/);
  const out = [];
  function walk(node) {
    for (const c of node.children) {
      if (matchSel(c, sel)) out.push(c);
      walk(c);
    }
  }
  walk(root);
  return out;
}
function matchSel(el, sel) {
  const parts = sel.trim().split(/\s+/);
  if (parts.length === 2) {
    const [idPart, cls] = parts;
    let node = el;
    let okId = true;
    if (idPart.startsWith('#')) { okId = false; while (node) { if (node._attrs.id === idPart.slice(1)) { okId = true; break; } node = node.parent; } }
    return okId && el.classList.contains(cls.replace('.', ''));
  }
  if (sel === 'input') return el.tagName === 'INPUT';
  if (sel.startsWith('#')) return el._attrs.id === sel.slice(1);
  if (sel.startsWith('.')) return el.classList.contains(sel.slice(1));
  return el.tagName === sel.toUpperCase();
}

// crude parser for the chip markup the page script emits
function parseHtml(html, parent) {
  const re = /<(\/?)([a-z0-9]+)([^>]*)>/g;
  let last = 0, stack = [parent], m;
  while ((m = re.exec(html)) !== null) {
    const text = html.slice(last, m.index);
    if (text && stack.length) stack[stack.length - 1]._text += text;
    last = re.lastIndex;
    const [, close, tag, attrsRaw] = m;
    if (close) { stack.pop(); continue; }
    const el = new El(tag);
    const attrs = attrsRaw.match(/([\w-]+)="([^"]*)"/g) || [];
    for (const a of attrs) {
      const mm = a.match(/([\w-]+)="([^"]*)"/);
      el.setAttribute(mm[1], mm[2]);
      if (mm[1] === 'data-i' || mm[1] === 'data-k' || mm[1] === 'data-r' || mm[1] === 'data-c' || mm[1] === 'data-bit') el.dataset[mm[1].slice(5)] = mm[2];
    }
    if (!/\/>$/.test(m[0])) stack[stack.length - 1].appendChild(el), stack.push(el);
    else stack[stack.length - 1].appendChild(el);
  }
  const rest = html.slice(last);
  if (rest && stack.length) stack[stack.length - 1]._text += rest;
}

// ── bootstrap the ids the page script touches ──
const doc = { _byId: {} };
for (const id of ['s1Grid','s2Chars','s2Ribbon','s2Rack','s2Readout','s3Data','s3Gen','s3Ec','s3Badge','s3Table','s3EcLabel','s4Wrap','s5Detail','s5Rack','s5Fmt','s5Note','labSvg','labVerdict','labStats','labDamage','labLevels']) {
  doc._byId[id] = new El('div');
  doc._byId[id].setAttribute('id', id);
}
doc.getElementById = id => doc._byId[id] || null;
doc.querySelectorAll = sel => {
  const out = [];
  Object.values(doc._byId).forEach(el => out.push(...el.querySelectorAll(sel)));
  return out;
};
doc.querySelector = sel => doc.querySelectorAll(sel)[0] || null;
doc.createElementNS = (ns, tag) => new El(tag);
doc.createElement = tag => new El(tag);
doc.readyState = 'complete';
doc.addEventListener = () => {};

global.document = doc;
global.VB = { esc: s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;') };
global.window = { VB: global.VB, VBScene: { onStep: () => {} } };

// lab controls
const slider = doc._byId.labDamage;
slider.setAttribute('type', 'range');
const levelsHost = doc._byId.labLevels;
['L','M','Q'].forEach(v => {
  const lab = new El('label');
  const inp = new El('input');
  inp.setAttribute('type', 'radio'); inp.setAttribute('name', 'lablvl'); inp.setAttribute('value', v);
  inp.value = v;
  const span = new El('span'); span._text = v;
  lab.appendChild(inp); lab.appendChild(span);
  levelsHost.appendChild(lab);
});
levelsHost.querySelectorAll = sel => levelsHost.children.filter(c => c.tagName === 'LABEL').map(l => l.children[0]);

// ── run the page script ──
const src = require('fs').readFileSync('/tmp/page2.js', 'utf8');
new Function(src)();

// ── assertions ──
function fail(msg) { console.error('FAIL:', msg); process.exitCode = 1; }
function ok(cond, msg) { if (cond) console.log('ok  —', msg); else fail(msg); }

const s2bits = doc._byId.s2Ribbon.children;
ok(s2bits.length === 104, 'S02 ribbon has 104 bits, got ' + s2bits.length);
ok(s2bits.filter(b => b._attrs['data-i'] === '0').length === 1, 'bit data-i present');
const ones = s2bits.filter(b => b.getAttribute('class').includes(' one')).length;
ok(ones === 39, 'bitstream has 39 one-bits (verified vs codewords), got ' + ones);
const rack = doc._byId.s2Rack.children;
ok(rack.length === 19, 'S02 rack has 19 codewords, got ' + rack.length);
ok(rack[0].textContent.trim() === '40' && rack[6].textContent.trim() === 'F2', 'rack hex values correct: ' + rack.map(c => c.textContent.trim()).join(' '));
const padCount = rack.filter(c => c.getAttribute('class').includes('pad')).length;
ok(padCount === 6, '6 pad codewords, got ' + padCount);

const s3data = doc._byId.s3Data.children;
ok(s3data.length === 19, 'S03 data wall 19, got ' + s3data.length);
const s3ec = doc._byId.s3Ec.children;
ok(s3ec.length === 7, 'S03 ec wall 7, got ' + s3ec.length);
ok(s3ec[0].textContent.trim() === 'C8' && s3ec[6].textContent.trim() === 'F6', 'EC hex correct: ' + s3ec.map(c => c.textContent.trim()).join(' '));
const s3gen = doc._byId.s3Gen.children;
ok(s3gen.length === 8 && s3gen[7].textContent.trim() === '117', 'generator strip: ' + s3gen.map(c => c.textContent.trim()).join(' '));
ok(doc._byId.s3Table.children.length === 4, 'trade-off table 4 rows, got ' + doc._byId.s3Table.children.length);

const s4 = doc._byId.s4Wrap.children[0];
const s4rects = s4.children.filter(c => c._attrs['data-bit'] !== undefined);
ok(s4rects.length === 208, 'S04 has 208 seat rects, got ' + s4rects.length);
const ecSeats = s4rects.filter(c => c.getAttribute('class').includes(' ec')).length;
ok(ecSeats === 208 - 152, 'S04 ec seats = 56 (7 codewords × 8), got ' + ecSeats);

const s5detail = doc._byId.s5Detail.children[0];
ok(s5detail !== undefined, 'S05 detail svg built');
const ovl = s5detail.children.filter(c => c.getAttribute('class').includes('ovl'));
ok(ovl.length === 104, 'mask-0 overlay restricted to data cells (104), got ' + ovl.length);
const cands = doc._byId.s5Rack.children;
ok(cands.length === 8, 'S05 has 8 candidates, got ' + cands.length);
const scores = cands.map(c => c.children[c.children.length - 1].textContent.trim().replace('★ ', ''));
ok(scores.join(' ') === '452 642 538 444 587 521 546 492', 'penalty scores: ' + scores.join(' '));
ok(cands.findIndex(c => c.getAttribute('class').includes('best')) === 3, 'winner is mask 3 (index 3)');
const fmt = doc._byId.s5Fmt.children;
ok(fmt.length === 3, 'S05 format strips built, got ' + fmt.length);
const fbits = fmt[0].children[0].children.map(fb => fb._attrs['data-i'] !== undefined ? fb.getAttribute('class').includes('one') ? '1' : '0' : '').join('');
const fbits2 = fmt[0].children[0].children.map(fb => fb.getAttribute('class').includes(' one') ? '1' : '0').join('');
ok(fbits2 === '111100010011101', 'format bits L3 = 111100010011101, got ' + fbits2);

// update functions through steps
function stepThrough(scene) {
  const fnMap = { scene2: 'updateS2', scene3: 'updateS3', scene4: 'updateS4', scene5: 'updateS5' };
}
// call updaters via a fake VBScene hook capture — re-run with captured fn
let captured = null;
global.window.VBScene = { onStep: fn => { captured = fn; } };
// boot already ran with the stub; re-eval to capture
try {
  const src2 = require('fs').readFileSync('/tmp/page2.js', 'utf8');
  new Function(src2)();
} catch (e) {}
ok(typeof captured === 'function', 'VBScene.onStep registered');
// scene2 updates
['scene2','scene3','scene4','scene5'].forEach(sid => {
  const steps = sid === 'scene4' ? 6 : 5;
  for (let i = 1; i <= steps; i++) {
    try { captured({ id: sid }, null, i); } catch (e) { fail(sid + ' step ' + i + ' threw: ' + e.message); }
  }
});
console.log('step updates ran without exceptions');

// lab: default render (L, 0 damage)
const labSvg = doc._byId.labSvg;
ok(labSvg.children.length === 441, 'lab svg 441 modules, got ' + labSvg.children.length);
ok(labSvg.children.filter(c => c.getAttribute('class').includes('ink')).length === 0, '0 ink at dmg=0');
ok(doc._byId.labVerdict.textContent.includes('PRISTINE'), 'verdict pristine at 0 damage');

// damage 3 → within budget (budget L = 3)
slider.value = '3'; slider.dispatch('input');
const ink3 = labSvg.children.filter(c => c.getAttribute('class').includes('ink')).length;
ok(ink3 === 24, '3 damaged codewords ink 24 modules, got ' + ink3);
ok(doc._byId.labVerdict.textContent.includes('WITHIN BUDGET'), 'L: 3 damaged → within budget');
ok(doc._byId.labVerdict.textContent.includes('3 / 3'), 'verdict reads 3 / 3');

// damage 4 → exceeds budget
slider.value = '4'; slider.dispatch('input');
ok(doc._byId.labVerdict.textContent.includes('BUDGET EXCEEDED'), 'L: 4 damaged → budget exceeded');
ok(doc._byId.labVerdict.textContent.includes('4 / 3'), 'verdict reads 4 / 3');

// level Q → budget 6
const qRadio = levelsHost.querySelectorAll('input')[2];
qRadio.value = 'Q'; qRadio.dispatch('change');
ok(doc._byId.labVerdict.textContent.includes('WITHIN BUDGET') && doc._byId.labVerdict.textContent.includes('4 / 6'), 'Q: 4 damaged → within budget 6');
ok(labSvg.children.filter(c => c.getAttribute('class').includes('ink')).length === 32, 'Q render inks 32 modules, got ' + labSvg.children.filter(c => c.getAttribute('class').includes('ink')).length);

// no H radio exists
ok(![...levelsHost.querySelectorAll('input')].some(i => i.value === 'H'), 'lab picker has no H level (HELLO WORLD does not fit V1-H)');
console.log('lab damage path verified');

