'use strict';
(() => {
  const projects = [['hisense-c3.html','Hisense · C3 系列'],['hisense.html','Hisense · IFA Berlin 2026'],['hisense-store.html','Hisense · 门店大屏'],['shanhai.html','山海志 · 东方奇幻品牌'],['silent-altitude.html','静默海拔 · 数字体验'],['prism.html','AI 点亮创意棱镜'],['worry.html','烦恼收容所 · 潮玩 IP'],['ui-design.html','AI 创新 UI 设计'],['subtext.html','话里有话 · AI 产品'],['chisuanbian.html','吃随便 · 微信小程序'],['ad.html','心力价签 · 广告战役'],['bkb.html','BLACK KING BAR'],['motion.html','山海志 · 动态演绎'],['personal.html','个人短片三则'],['music.html','AI 音乐'],['imagegen.html','AI 视觉实验']];
  const index = projects.findIndex(p => p[0] === location.pathname.split('/').pop());
  const next = projects[(index+1)%projects.length];
  const link=document.createElement('a');link.className='case-next';link.href=next[0];
  const text=document.createElement('div');const label=document.createElement('small');label.textContent='CONTINUE EXPLORING / NEXT PROJECT';const title=document.createElement('strong');title.textContent=next[1];text.append(label,title);const arrow=document.createElement('span');arrow.textContent='↗';link.append(text,arrow);
  const footer=document.querySelector('footer');if(footer)footer.before(link);else document.body.append(link);
  const progress=document.createElement('div');progress.className='case-progress';progress.setAttribute('aria-hidden','true');document.body.append(progress);
  let ticking=false;const onScroll=()=>{if(!ticking){requestAnimationFrame(()=>{const length=document.documentElement.scrollHeight-innerHeight;progress.style.transform=`scaleX(${length>0?scrollY/length:0})`;ticking=false;});ticking=true;}};
  addEventListener('scroll',onScroll,{passive:true});onScroll();
  const dialog=document.createElement('dialog');dialog.className='lightbox';dialog.setAttribute('aria-label','查看作品大图');
  dialog.innerHTML='<header><span id="lightbox-title"></span><button type="button" autofocus>关闭 ×</button></header><img alt="">';document.body.append(dialog);
  const image=dialog.querySelector('img'),caption=dialog.querySelector('span');let opener;
  const close=()=>dialog.close();dialog.querySelector('button').addEventListener('click',close);
  dialog.addEventListener('click',e=>{if(e.target===dialog)close();});
  dialog.addEventListener('close',()=>{document.body.style.overflow='';if(opener)opener.focus();});
  document.querySelectorAll('main img, section img').forEach(img=>{
    if(img.closest('a,button,.lb,.lightbox'))return;
    // Existing gallery scripts keep their own interactions.
    if(img.hasAttribute('onclick')||img.closest('[onclick]'))return;
    const button=document.createElement('button');button.className='media-open';button.type='button';button.setAttribute('aria-label','放大查看：'+(img.alt||'项目图片'));img.before(button);button.append(img);
    button.addEventListener('click',()=>{opener=button;image.src=img.currentSrc||img.src;image.alt=img.alt||'项目作品';caption.textContent=img.alt||'PROJECT DETAIL';dialog.showModal();document.body.style.overflow='hidden';});
  });
})();
