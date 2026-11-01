'use strict';
(() => {
  const dialog = document.querySelector('.image-dialog');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const picture = document.getElementById('viewer-image');
  const title = document.getElementById('viewer-title');
  const original = document.getElementById('viewer-original');
  const close = document.getElementById('viewer-close');
  const status = dialog.querySelector('.viewer-status');
  let invoker = null;

  document.querySelectorAll('[data-full-image]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      invoker = link;
      title.textContent = link.dataset.title || '作品大图';
      original.href = link.href;
      picture.alt = link.dataset.alt || link.dataset.title || '作品原图';
      picture.hidden = true;
      status.textContent = '正在载入原图…';
      picture.onload = () => { picture.hidden = false; status.textContent = ''; };
      picture.onerror = () => { status.textContent = '图片未能加载，请使用右上角“打开原图”。'; };
      picture.src = link.href;
      dialog.showModal();
      document.body.classList.add('lightbox-open');
      close.focus();
    });
  });

  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('lightbox-open');
    picture.onload = null;
    picture.onerror = null;
    picture.removeAttribute('src');
    picture.hidden = true;
    status.textContent = '';
    if (invoker && invoker.isConnected) invoker.focus();
  });
})();
