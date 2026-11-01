(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.CreatorCore=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){
  'use strict';
  const chars=s=>Array.from(String(s||'').trim()).length;
  const normalizeCopy=(s,max,lines=1)=>Array.from(String(s||'').replace(/\r/g,'').split('\n').slice(0,lines).join(lines>1?'\n':' ')).slice(0,max).join('');
  const escapeXML=s=>String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
  function validateImage(file){if(!file)return {ok:false,message:'请选择一张图片。'};if(!['image/jpeg','image/png','image/webp'].includes(file.type))return {ok:false,message:'仅支持 JPG、PNG 和 WebP 图片。'};if(file.size>12*1024*1024)return {ok:false,message:'图片超过 12 MB，请换一张较小的图片。'};return {ok:true,message:'文件格式与大小通过。'};}
  const briefs={commute:{name:'通勤中的小宇宙',prompt:'把日常通勤中一个容易忽略的细节折成纸城。',keywords:'车窗 / 路口 / 天桥',hook:'这条每天走的路，藏着另一座城。'},afterhours:{name:'夜色重新开场',prompt:'选取一处夜间城市生活，将灯光与人物关系转换为纸艺层次。',keywords:'灯牌 / 夜摊 / 窗灯',hook:'白天没说完的故事，夜里继续。'},edges:{name:'城市的边角料',prompt:'发现墙角、楼梯或建筑接缝，以纸面折叠突出它的独特结构。',keywords:'转角 / 楼梯 / 缝隙',hook:'城市最小的角落，也值得一张大作品。'}};
  const levels={starter:{name:'第一次创作',pace:'单图 + 两步拆解',goal:'完成一个明确观察点，使用一种可控纸艺语言。'},growing:{name:'持续创作者',pace:'三图故事 + 过程',goal:'保持同一城市视觉设定，串联发现、转化和结果。'},advanced:{name:'进阶创作者',pace:'短片 + 可复用模板',goal:'建立输入约束与跨镜头一致性，交付他人可接手的模板。'}};
  function buildPlan(briefKey,levelKey){const b=briefs[briefKey]||briefs.commute,l=levels[levelKey]||levels.starter;const titles=['发现一个细节','做一次视觉翻译','公开制作过程','邀请共同发现','换一个观察角度','修好关键问题','整理成可复用资产'];return titles.map((title,i)=>({day:i+1,title,brief:b.name,level:l.name,format:i===5?'修改前 / 修改后':i===6?'模板 / 参数说明':l.pace,prompt:[b.prompt,'以同一观察点试作两种折叠结构，只保留最清楚的一种。','记录原始观察、提示词选择与后期调整，注明 AI 参与。','请读者用一个具体城市细节回应，避免空泛求赞。','保留材质与配色，改变视角检验系列一致性。','根据自检与人工反馈修正文字、形体、版权或隐私问题。','附输入限制、复现步骤和失败示例，方便他人继续创作。'][i],signal:['观察点清晰度','主题对应性','过程可追溯性','有效回应内容','系列一致性','问题关闭情况','模板可复现性'][i]}));}
  function evaluateDraft(d){d=d||{};const m=d.media||{},mime=String(m.type||''),video=mime==='video/mp4',hasMedia=Boolean(m.present);const ratio=Number(m.width)/Number(m.height);const entries=[
    ['R01','素材来源与使用权',Boolean(d.rights),'block','确认照片、字体、音乐及引用素材的来源与许可；需要人工查验记录。'],
    ['R02','AI 参与说明',!d.usedAI||Boolean(d.aiDisclosure),'block','使用 AI 时，说明生成与人工修改的边界，不冒充实拍或真实事件。'],
    ['R03','真实文件与格式',hasMedia&&['image/jpeg','image/png','image/webp','video/mp4'].includes(mime),'block','需读取实际本地文件；接受 JPG / PNG / WebP / MP4。'],
    ['R04','画幅与分辨率',hasMedia&&Number(m.width)>=1080&&Number(m.height)>=1920&&Math.abs(ratio-9/16)<=.02,'revise','此概念挑战采用竖版 9:16，最低 1080 × 1920；不是平台通用规范。'],
    ['R05','文件大小与时长',hasMedia&&Number(m.size)>0&&Number(m.size)<=50*1024*1024&&(!video||(Number(m.duration)>=6&&Number(m.duration)<=30)),'revise','单文件不超过 50 MB；视频 6–30 秒；图片不检查时长。'],
    ['R06','标题可读长度',chars(d.title)>=6&&chars(d.title)<=40,'revise','标题 6–40 个字符；长度通过不代表内容质量通过。'],
    ['R07','过程说明完整度',chars(d.caption)>=20&&chars(d.caption)<=400,'revise','说明 20–400 个字符，建议包含观察、转译与人工修改。'],
    ['R08','主题证据',Boolean(briefs[d.brief])&&chars(d.observation)>=12,'revise','提供至少 12 字的具体观察；是否对应主题仍由人工判断。'],
    ['R09','隐私与敏感内容自查',Boolean(d.privacyReviewed),'block','确认去除可识别的无授权个人信息，完成内容安全自查；不能代替人工审核。'],
    ['R10','画面质量自查',Boolean(d.safeAreaReviewed&&d.textLegible&&d.noArtifacts),'revise','确认主体安全区、文字可辨及明显生成瑕疵；人工复核后才能决定发布。']
  ].map(([id,label,pass,severity,note])=>({id,label,pass,severity,note}));const blockers=entries.filter(r=>!r.pass&&r.severity==='block').length,changes=entries.filter(r=>!r.pass&&r.severity==='revise').length;return {version:'1.0',status:blockers?'hold':changes?'revise':'human-review',label:blockers?'暂缓流转 · 补齐必要条件':changes?'需要修改 · 完成自检项目':'自检完成 · 待人工复核',blockers,changes,passed:entries.filter(r=>r.pass).length,rules:entries};}
  function csvCell(v){let s=String(v??'');if(/^[=+@\-\t\r]/.test(s))s="'"+s;return '"'+s.replace(/"/g,'""')+'"';}
  function toCSV(rows,columns){return '\uFEFF'+[columns.map(c=>csvCell(c.label)).join(','),...rows.map(r=>columns.map(c=>csvCell(r[c.key])).join(','))].join('\r\n');}
  return {chars,normalizeCopy,escapeXML,validateImage,briefs,levels,buildPlan,evaluateDraft,toCSV};
});
