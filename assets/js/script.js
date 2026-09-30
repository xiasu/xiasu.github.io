'use strict';

const perspectives = {
  map: { title: 'From geometry to understanding.', text: 'Build spatial representations that connect what AI perceives with what people know.', project: 'FlyMeThrough', href: '#flymethrough' },
  relate: { title: 'The same space. Different possibilities.', text: 'Understand environments in relation to a person’s capabilities, needs, and intentions.', project: 'CapNav', href: '#capnav' },
  assist: { title: 'Understanding that helps people act.', text: 'Make accessibility barriers and potential safety risks visible in their spatial context.', project: 'RASSAR', href: '#rassar' }
};
const tabs = [...document.querySelectorAll('[data-lens]')];
const panel = document.querySelector('#lens-panel');
const lens = document.querySelector('.spatial-lens');
function selectPerspective(tab, moveFocus = false) {
  const key = tab.dataset.lens;
  const content = perspectives[key];
  tabs.forEach(item => {
    item.setAttribute('aria-selected', String(item === tab));
    item.tabIndex = item === tab ? 0 : -1;
  });
  lens.dataset.perspective = key;
  panel.setAttribute('aria-labelledby', tab.id);
  panel.querySelector('h2').textContent = content.title;
  panel.querySelector('p').textContent = content.text;
  const link = panel.querySelector('a');
  link.href = content.href;
  link.replaceChildren(document.createTextNode(`Explore ${content.project} `));
  const arrow = document.createElement('span');
  arrow.setAttribute('aria-hidden', 'true');
  arrow.textContent = '↗';
  link.append(arrow);
  if (moveFocus) tab.focus();
}
tabs.forEach((tab, index) => {
  tab.addEventListener('click', () => selectPerspective(tab));
  tab.addEventListener('keydown', event => {
    let next;
    if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
    if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = tabs.length - 1;
    if (next !== undefined) { event.preventDefault(); selectPerspective(tabs[next], true); }
  });
});
document.querySelector('#year').textContent = new Date().getFullYear();
