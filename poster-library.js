'use strict';
(() => {
  const library = document.getElementById('poster-library');
  if (!library) return;
  const style = document.getElementById('pl-style');
  const topic = document.getElementById('pl-topic');
  const search = document.getElementById('pl-search');
  const gallery = document.getElementById('pl-gallery');
  const cards = [...gallery.querySelectorAll('[data-library-item]')];
  const groups = [...gallery.querySelectorAll('[data-work-group]')];
  const sections = [...gallery.querySelectorAll('[data-category-section]')];
  const categoryButtons = [...library.querySelectorAll('[data-category-filter]')];
  const ratioButtons = [...library.querySelectorAll('[data-ratio-filter]')];
  const count = document.getElementById('pl-count');
  const empty = document.getElementById('pl-empty');
  const normalize = value => value.normalize('NFKC').toLocaleLowerCase().trim();
  let category = 'all';
  let ratio = 'all';

  function filterImages() {
    const terms = normalize(search.value).split(/\s+/).filter(Boolean);
    let visible = 0;
    const themes = new Set();
    cards.forEach(card => {
      const matches = (category === 'all' || card.dataset.category === category)
        && (style.value === 'all' || card.dataset.style === style.value)
        && (topic.value === 'all' || card.dataset.topic === topic.value)
        && (ratio === 'all' || card.dataset.ratio === ratio)
        && terms.every(term => normalize(card.dataset.name).includes(term));
      card.hidden = !matches;
      if (matches) { visible++; themes.add(card.dataset.topic); }
    });
    let visibleGroups=0;
    groups.forEach(group=>{
      const groupCards=[...group.querySelectorAll('[data-library-item]')];
      const number=groupCards.filter(card=>!card.hidden).length;
      group.hidden=number===0; group.dataset.visible=String(number);
      group.querySelector('[data-group-count]').textContent=number===groupCards.length ? number+' 张' : number+' / '+groupCards.length+' 张';
      if(number) visibleGroups++;
    });
    sections.forEach(section=>{section.hidden=![...section.querySelectorAll('[data-work-group]')].some(group=>!group.hidden);});
    count.textContent = visibleGroups+' 组 · '+visible+' / '+cards.length+' 张';
    empty.hidden = visible !== 0;
  }
  categoryButtons.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.categoryFilter;
    categoryButtons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    [...topic.querySelectorAll('optgroup')].forEach(group => { group.disabled = category !== 'all' && group.label !== category; });
    if(topic.value !== 'all' && category !== 'all' && !topic.value.startsWith(category+' / ')) topic.value = 'all';
    filterImages();
  }));
  style.addEventListener('change', filterImages);
  topic.addEventListener('change', filterImages);
  search.addEventListener('input', filterImages);
  ratioButtons.forEach(button => button.addEventListener('click', () => {
    ratio = button.dataset.ratioFilter;
    ratioButtons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    filterImages();
  }));
  document.getElementById('pl-reset').addEventListener('click', () => {
    category = ratio = 'all'; style.value = topic.value = 'all'; search.value = '';
    topic.querySelectorAll('optgroup').forEach(group => { group.disabled = false; });
    categoryButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.categoryFilter === 'all')));
    ratioButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.ratioFilter === 'all')));
    filterImages(); categoryButtons[0].focus();
  });
  if (new URLSearchParams(location.search).get('collection') === 'tests') {
    const testsButton=categoryButtons.find(button=>button.dataset.categoryFilter==='命题练习');
    if(testsButton) testsButton.click();
  }
  filterImages();

  const dialog = document.getElementById('pl-viewer');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const image = document.getElementById('pl-viewer-image');
  const title = document.getElementById('pl-viewer-title');
  const original = document.getElementById('pl-original');
  const position = document.getElementById('pl-position');
  const status = document.getElementById('pl-viewer-status');
  let items = [], current = 0, opener = null, previousOverflow = '';
  function display(index) {
    current = (index + items.length) % items.length;
    const anchor = items[current];
    const caption = anchor.querySelector('img').alt;
    title.textContent = image.alt = caption;
    original.href = anchor.href;
    original.textContent = anchor.href.endsWith('.png') ? '打开原图 ↗' : '打开高清大图 ↗';
    const group=anchor.closest('[data-work-group]');
    position.textContent = (group ? group.dataset.groupTitle+' · ' : '')+`${current + 1} / ${items.length}`;
    status.textContent = '正在加载大图…'; status.hidden = false;
    image.src = anchor.href;
  }
  image.addEventListener('load', () => { status.hidden = true; });
  image.addEventListener('error', () => { status.textContent = '暂时无法加载，可点击上方链接重试。'; status.hidden = false; });
  document.querySelectorAll('[data-poster-view]').forEach(anchor => anchor.addEventListener('click', event => {
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault(); opener = anchor;
    const selected = anchor.closest('.pl-image').querySelector('.pl-image__open');
    const scope = selected.closest('[data-work-group]') || selected.closest('.pl-group--legacy') || selected.closest('#pl-gallery') || selected.closest('.pl-legacy');
    items = [...scope.querySelectorAll('.pl-image__open')].filter(item => !item.closest('[hidden]'));
    if(!items.length) return;
    display(Math.max(0, items.indexOf(selected)));
    previousOverflow = document.body.style.overflow;
    dialog.showModal(); document.body.style.overflow = 'hidden';
  }));
  document.getElementById('pl-close').addEventListener('click', () => dialog.close());
  document.getElementById('pl-previous').addEventListener('click', () => display(current-1));
  document.getElementById('pl-next').addEventListener('click', () => display(current+1));
  dialog.addEventListener('keydown', event => {
    if(event.key === 'ArrowLeft' || event.key === 'ArrowRight') { event.preventDefault(); display(current+(event.key === 'ArrowRight'?1:-1)); }
  });
  dialog.addEventListener('click', event => {
    if(event.target !== dialog) return;
    const rect=dialog.getBoundingClientRect();
    if(event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    document.body.style.overflow = previousOverflow; image.removeAttribute('src');
    if(opener?.isConnected) opener.focus();
  });
})();
