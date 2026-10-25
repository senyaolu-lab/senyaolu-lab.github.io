'use strict';
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');

// Navigation is deliberately native: anchors remain usable without JavaScript.
const menu = $('.menu-toggle');
const mobileNav = $('#mobile-nav');
const closeMenu = () => { menu.setAttribute('aria-expanded', 'false'); mobileNav.hidden = true; };
menu.addEventListener('click', () => { const open = menu.getAttribute('aria-expanded') !== 'true'; menu.setAttribute('aria-expanded', String(open)); mobileNav.hidden = !open; });
$$('a', mobileNav).forEach(a => a.addEventListener('click', closeMenu));
document.addEventListener('keydown', e => { if (e.key === 'Escape') {closeMenu();} });
matchMedia('(min-width: 761px)').addEventListener('change', e => {if (e.matches) closeMenu();});

const cards = $$('.project-card');
const more = $('#show-more');
let category = 'all', expanded = false;
function updateProjects() {
  let shown = 0;
  cards.forEach(card => {
    const match = category === 'all' || card.dataset.category.split(' ').includes(category);
    const visible = match && (category !== 'all' || expanded || shown < 6);
    card.hidden = !visible;
    if (visible) shown++;
  });
  $('.result-count').textContent = `SHOWING ${String(shown).padStart(2, '0')} / ${cards.length}`;
  more.hidden = category !== 'all';
  more.style.display = category === 'all' ? '' : 'none';
  more.innerHTML = expanded ? '收起项目 <span>↑</span>' : `展开全部 ${cards.length} 个项目 <span>↓</span>`;
  more.setAttribute('aria-expanded', String(expanded));
}
$$('[data-filter]').forEach(button => button.addEventListener('click', () => {
  category = button.dataset.filter;
  $$('[data-filter]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
  updateProjects();
}));
more.addEventListener('click', () => {
  expanded = !expanded; updateProjects();
  if (!expanded) $('#work').scrollIntoView({behavior: reducedMotion.matches ? 'instant' : 'smooth'});
});
updateProjects();


// A locally rendered, dependency-free trefoil surface. Never captures pointer data.
const canvas = $('#sculpture');
const ctx = canvas.getContext('2d');
if (ctx) {
  let width = 600, height = 650, rotation = .4, pointerX = 0, pointerY = 0;
  let frame, last = 0, visible = true;
  const points = [], rings = 144, sides = 28;
  const center = t => [(2 + .55 * Math.cos(3*t))*Math.cos(2*t), (2 + .55 * Math.cos(3*t))*Math.sin(2*t), .85*Math.sin(3*t)];
  for (let i = 0; i < rings; i++) {
    const t = i / rings * Math.PI * 2, p = center(t), next = center(t + .001);
    let tangent = next.map((v,k) => v-p[k]);
    const len = Math.hypot(...tangent); tangent = tangent.map(v=>v/len);
    let normal = [-tangent[1], tangent[0], 0]; const nl = Math.hypot(...normal); normal = normal.map(v=>v/nl);
    const binormal = [tangent[1]*normal[2]-tangent[2]*normal[1], tangent[2]*normal[0]-tangent[0]*normal[2], tangent[0]*normal[1]-tangent[1]*normal[0]];
    const ring = [];
    for (let j = 0; j <= sides; j++) {
      const a = j/sides * Math.PI * 2;
      ring.push(p.map((v,k) => v + .49 * (normal[k]*Math.cos(a)+binormal[k]*Math.sin(a))));
    }
    points.push(ring);
  }
  const motionButton = document.createElement('button');
  motionButton.className = 'motion-toggle'; motionButton.type = 'button';
  motionButton.textContent = reducedMotion.matches ? '播放动效 ▷' : '暂停动效 Ⅱ';
  motionButton.setAttribute('aria-label','暂停或播放生成式图形动画');
  canvas.parentElement.append(motionButton);
  let paused = reducedMotion.matches;
  motionButton.setAttribute('aria-pressed', String(paused));
  const resize = () => {
    const rect = canvas.getBoundingClientRect(); width = rect.width; height = rect.height;
    const dpr = Math.min(devicePixelRatio || 1, 1.8);
    canvas.width = width*dpr; canvas.height = height*dpr; ctx.setTransform(dpr,0,0,dpr,0,0);
    draw();
  };
  function project(point) {
    let [x,y,z] = point;
    const ax = .75 + pointerY*.15, ay = rotation + pointerX*.15;
    const y1 = y*Math.cos(ax)-z*Math.sin(ax), z1 = y*Math.sin(ax)+z*Math.cos(ax);
    const x1 = x*Math.cos(ay)+z1*Math.sin(ay), z2 = -x*Math.sin(ay)+z1*Math.cos(ay);
    const az = -.35, x2 = x1*Math.cos(az)-y1*Math.sin(az), y2 = x1*Math.sin(az)+y1*Math.cos(az);
    const scale = Math.min(width*.143, height*.16), perspective = 9/(9-z2);
    return [width*.53+x2*scale*perspective, height*.48+y2*scale*perspective, z2];
  }
  function draw() {
    ctx.clearRect(0,0,width,height);
    const glow = ctx.createRadialGradient(width*.54,height*.5,0,width*.54,height*.5,width*.43);
    glow.addColorStop(0,'rgba(143,179,108,.085)'); glow.addColorStop(.6,'rgba(73,99,52,.025)');glow.addColorStop(1,'rgba(11,13,12,0)');
    ctx.fillStyle = glow;ctx.fillRect(0,0,width,height);
    const projected = points.map(r=>r.map(project));
    const ordered = projected.map((r,i)=>({r,i,z:r.reduce((s,p)=>s+p[2],0)/r.length})).sort((a,b)=>a.z-b.z);
    for (const {r,i,z} of ordered) {
      const depth = (z+3.5)/7, light = .22+.7*depth;
      ctx.strokeStyle = `rgba(${Math.round(170+70*depth)},${Math.round(183+58*depth)},${Math.round(158+74*depth)},${light*.8})`;
      ctx.lineWidth = .65 + depth*.22;
      ctx.beginPath();r.forEach((p,j)=>j?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.stroke();
      const next = projected[(i+1)%rings];
      ctx.strokeStyle = `rgba(193,222,163,${.035+depth*.15})`;ctx.lineWidth=.5;
      ctx.beginPath();for(let j=0;j<sides;j+=2){ctx.moveTo(r[j][0],r[j][1]);ctx.lineTo(next[j][0],next[j][1]);}ctx.stroke();
    }
    const p = projected[33][7];ctx.fillStyle='#d7ffa6';ctx.beginPath();ctx.arc(p[0],p[1],2,0,Math.PI*2);ctx.fill();
  }
  function tick(now) {
    if (!paused && visible && !document.hidden) { if (now-last>32) { rotation+=.0035;draw();last=now; } frame=requestAnimationFrame(tick); }
  }
  function schedule() { cancelAnimationFrame(frame);if(!paused&&visible&&!document.hidden)frame=requestAnimationFrame(tick); }
  motionButton.addEventListener('click',()=>{paused=!paused;motionButton.textContent=paused?'播放动效 ▷':'暂停动效 Ⅱ';motionButton.setAttribute('aria-pressed',String(paused));schedule();});
  canvas.parentElement.addEventListener('pointermove',e=>{const b=canvas.getBoundingClientRect();pointerX=(e.clientX-b.left)/b.width-.5;pointerY=(e.clientY-b.top)/b.height-.5;});
  canvas.parentElement.addEventListener('pointerleave',()=>{pointerX=pointerY=0;});
  reducedMotion.addEventListener('change',e=>{paused=e.matches;motionButton.textContent=paused?'播放动效 ▷':'暂停动效 Ⅱ';motionButton.setAttribute('aria-pressed',String(paused));schedule();});
  new ResizeObserver(resize).observe(canvas);
  new IntersectionObserver(([e])=>{visible=e.isIntersecting;schedule();}).observe(canvas);
  document.addEventListener('visibilitychange',schedule);
  resize();schedule();
}
