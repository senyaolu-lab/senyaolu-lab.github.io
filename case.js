'use strict';
(() => {
  const projects = [["hisense-c3.html", "Hisense · C3 系列"], ["hisense.html", "Hisense · IFA Berlin 2026"], ["hisense-store.html", "Hisense · 种草店大屏"], ["https://deadlock-cursed-apple-atlas.rockyheron12.chatgpt.site/#city", "Deadlock · The Cursed Apple"], ["personal.html", "个人短片三则"], ["imagegen.html", "图片类"], ["skip-launch/", "跳格 SKIP"], ["sound-between/", "声隙 SOUND BETWEEN"], ["shanhai.html", "山海志"], ["silent-altitude.html", "静默海拔 SILENT ALTITUDE"], ["prism.html", "AI 点亮创意棱镜"], ["worry.html", "烦恼收容所"], ["ui-design.html", "为智能时代设计界面"], ["subtext.html", "话里有话"], ["chisuanbian.html", "吃随便"], ["ad.html", "心力价签"], ["bkb.html", "BLACK KING BAR"], ["motion.html", "山海志 · 动态演绎"], ["music.html", "声音，也是一种想象"]];
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
