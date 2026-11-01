'use strict';
(() => {
  const library = document.getElementById('poster-library');
  if (!library) return;
  const industry = document.getElementById('pl-industry');
  const style = document.getElementById('pl-style');
  const search = document.getElementById('pl-search');
  const gallery = document.getElementById('pl-gallery');
  const groups = [...gallery.querySelectorAll('.pl-group')];
  const ratioButtons = [...library.querySelectorAll('[data-ratio-filter]')];
  const count = document.getElementById('pl-count');
  const empty = document.getElementById('pl-empty');
  const normalize = value => value.normalize('NFKC').toLocaleLowerCase().trim();
  let ratio = 'all';

  function filterImages() {
    const terms = normalize(search.value).split(/\s+/).filter(Boolean);
    let visible = 0;
    groups.forEach(group => {
      const groupMatches = (industry.value === 'all' || group.dataset.industry === industry.value)
        && (style.value === 'all' || group.dataset.style === style.value);
      let groupVisible = 0;
      group.querySelectorAll('[data-library-item]').forEach(item => {
        const name = normalize(`${group.dataset.name} ${item.dataset.name}`);
        const matches = groupMatches && (ratio === 'all' || item.dataset.ratio === ratio)
          && terms.every(term => name.includes(term));
        item.hidden = !matches;
        if (matches) groupVisible++;
      });
      group.hidden = groupVisible === 0;
      group.querySelector('.pl-pair').dataset.visible = String(groupVisible);
      visible += groupVisible;
    });
    // Single-format results form a compact image grid; paired images stay together.
    gallery.dataset.filtered = String(ratio !== 'all');
    count.textContent = visible === 32 ? '32 幅' : `${visible} / 32 幅`;
    empty.hidden = visible !== 0;
  }

  industry.addEventListener('change', filterImages);
  style.addEventListener('change', filterImages);
  search.addEventListener('input', filterImages);
  ratioButtons.forEach(button => button.addEventListener('click', () => {
    ratio = button.dataset.ratioFilter;
    ratioButtons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    filterImages();
  }));
  document.getElementById('pl-reset').addEventListener('click', () => {
    industry.value = 'all';
    style.value = 'all';
    search.value = '';
    ratio = 'all';
    ratioButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.ratioFilter === 'all')));
    filterImages();
    industry.focus();
  });
  filterImages();

  const dialog = document.getElementById('pl-viewer');
  // PNG links remain usable in browsers without native dialog support.
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const image = document.getElementById('pl-viewer-image');
  const title = document.getElementById('pl-viewer-title');
  const original = document.getElementById('pl-original');
  const position = document.getElementById('pl-position');
  const status = document.getElementById('pl-viewer-status');
  let items = [];
  let current = 0;
  let opener = null;
  let previousOverflow = '';

  function display(index) {
    current = (index + items.length) % items.length;
    const anchor = items[current];
    const caption = anchor.querySelector('img').alt;
    title.textContent = caption;
    image.alt = caption;
    original.href = anchor.href;
    position.textContent = `${current + 1} / ${items.length}`;
    status.textContent = '正在加载原图…';
    status.hidden = false;
    image.src = anchor.href;
  }
  image.addEventListener('load', () => { status.hidden = true; });
  image.addEventListener('error', () => {
    status.textContent = '暂时无法加载，可点击“打开原图”重试。';
    status.hidden = false;
  });
  document.querySelectorAll('[data-poster-view]').forEach(anchor => anchor.addEventListener('click', event => {
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    opener = anchor;
    const selected = anchor.closest('.pl-image').querySelector('.pl-image__open');
    const scope = selected.closest('#pl-gallery') || selected.closest('.pl-legacy') || document;
    items = [...scope.querySelectorAll('.pl-image__open')].filter(item => !item.closest('.pl-image').hidden && !item.closest('.pl-group').hidden);
    if (!items.length) return;
    display(Math.max(0, items.indexOf(selected)));
    previousOverflow = document.body.style.overflow;
    dialog.showModal();
    document.body.style.overflow = 'hidden';
  }));
  document.getElementById('pl-close').addEventListener('click', () => dialog.close());
  document.getElementById('pl-previous').addEventListener('click', () => display(current - 1));
  document.getElementById('pl-next').addEventListener('click', () => display(current + 1));
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      display(current + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    document.body.style.overflow = previousOverflow;
    image.removeAttribute('src');
    if (opener && opener.isConnected) opener.focus();
  });
})();
