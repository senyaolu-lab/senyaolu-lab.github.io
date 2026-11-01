from PIL import Image, ImageDraw, ImageFont
import math, subprocess, pathlib, wave, numpy as np, json, sys

# Resolve beside this delivered source, independent of the launch directory.
# Regenerated assets stay separate from the portfolio's published originals.
ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'renders'
EV=OUT/'evidence'
TMP=OUT/'scratch'
W,H,FPS=1920,1080,24
FONTS={}
def font(size,bold=False):
    key=(size,bold)
    if key not in FONTS:FONTS[key]=ImageFont.truetype('C:/Windows/Fonts/'+('msyhbd.ttc' if bold else 'msyh.ttc'),round(size))
    return FONTS[key]
def clamp(x):return max(0,min(1,x))
def ease(x):x=clamp(x);return x*x*(3-2*x)
def out(x):return 1-(1-clamp(x))**3
def lerp(a,b,t):return a+(b-a)*t
def mix(a,b,t):return tuple(round(lerp(x,y,clamp(t))) for x,y in zip(a,b))
def text(d,xy,s,size=30,c='#141B2E',bold=False,anchor='lt'):
    d.text(tuple(round(x) for x in xy),s,font=font(size,bold),fill=c,anchor=anchor)
def rr(d,box,fill,r=20,outline=None,width=1):
    d.rounded_rectangle(tuple(round(x) for x in box),radius=round(r),fill=fill,outline=outline,width=width)
def line(d,pts,c,w=3):d.line([(round(x),round(y)) for x,y in pts],fill=c,width=round(w),joint='curve')
def disk(d,x,y,r,c):d.ellipse((x-r,y-r,x+r,y+r),fill=c)
def text_fit(d,xy,s,maxwidth,size=30,c='#141B2E',bold=False):
    while d.textlength(s,font=font(size,bold))>maxwidth:size-=1
    text(d,xy,s,size,c,bold)
def fade_frame(im,t,dur):
    # A short intentional fade at the final frame, not a transition between slides.
    if t>dur-.65:
        overlay=Image.new('RGB',im.size, '#F5F7FB' if dur==24 else '#081927')
        return Image.blend(im,overlay,ease((t-dur+.65)/.65)*.12)
    return im

BLUE=(48,96,239);INK=(21,31,53);MUTED=(110,122,145);BG=(245,247,251);ORANGE=(255,140,66)
def sync_brand(d,t):
    text(d,(94,55),'SYNC / 同频',28,INK,True)
    text(d,(1818,59),'PRODUCT MOTION · 24s',17,MUTED,anchor='rt')
    line(d,[(96,103),(1824,103)],(218,224,235),2)
    line(d,[(96,1016),(1824,1016)],(218,224,235),2)
    text(d,(96,1030),'原创协作产品概念 / 程序化动态图形',17,MUTED)
    text(d,(1824,1030),f'{t:05.1f} / 24.0',17,MUTED,anchor='rt')
    line(d,[(96,1016),(96+1728*t/24,1016)],BLUE,3)
def card(d,x,y,w,h,tag,title,subtitle,color=BLUE,alpha=1):
    bg=mix(BG,(255,255,255),alpha); edge=mix(BG,(222,228,240),alpha)
    rr(d,(x,y+9,x+w,y+h+9),mix(BG,(225,230,240),alpha),22)
    rr(d,(x,y,x+w,y+h),bg,22,edge,2)
    rr(d,(x+22,y+22,x+32,y+52),mix(bg,color,alpha),5)
    text(d,(x+47,y+24),tag,17,mix(bg,MUTED,alpha),True)
    text_fit(d,(x+24,y+67),title,w-48,30,mix(bg,INK,alpha),True)
    if subtitle:text_fit(d,(x+24,y+114),subtitle,w-48,18,mix(bg,MUTED,alpha))
def check(d,x,y,s=1,c=BLUE):
    disk(d,x,y,16*s,c)
    line(d,[(x-7*s,y),(x-1*s,y+6*s),(x+9*s,y-7*s)],'white',3*s)
def taskboard(d,progress=0):
    # Actual task state changes across columns; the three objects persist throughout.
    x,y=300,370;w=1320;h=540
    rr(d,(x,y+12,x+w,y+h+12),(226,232,243),24)
    rr(d,(x,y,x+w,y+h),'white',24,(218,226,241),2)
    text(d,(x+36,y+28),'秋季发布 / 设计协作',28,INK,True)
    text(d,(x+w-36,y+38),'共享任务板',18,MUTED,anchor='rt')
    line(d,[(x,y+91),(x+w,y+91)],(232,236,244),2)
    cols=[x+30,x+460,x+890]
    for i,label in enumerate(['待确认','进行中','已完成']):
        rr(d,(cols[i],y+116,cols[i]+400,y+496),(247,249,253),16)
        disk(d,cols[i]+22,y+143,5,[ORANGE,BLUE,(34,164,117)][i])
        text(d,(cols[i]+38,y+133),label,22,INK,True)
    titles=['发布主视觉','产品短片','渠道延展']
    for i,title in enumerate(titles):
        p=ease((progress-i*.23)/.4)
        xx=lerp(cols[0]+14,cols[2]+14,p)
        yy=y+182+i*92
        rr(d,(xx,yy+3,xx+372,yy+81),(229,234,244),14)
        rr(d,(xx,yy,xx+372,yy+78),'white',14,(221,229,240),1)
        text(d,(xx+18,yy+17),title,22,INK,True)
        text(d,(xx+18,yy+49),['林同学 · 今天 18:00','周同学 · 明天 12:00','陈同学 · 周五 18:00'][i],14,MUTED)
        if p>.95:check(d,xx+340,yy+36,.7,(34,164,117))

def sync_frame(t):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im);sync_brand(d,t)
    # Reuse a grid of three colored orbit points as anchors throughout the film.
    if t<4:
        u=t/4
        text(d,(96,162),'信息散落在各处。',72,INK,True)
        text(d,(100,265),'消息在跳，进度却停在原地。',28,MUTED)
        pts=[(280,410,370,176,'聊天','这个版本确认了吗？','12 条新消息',BLUE),
             (1120,365,420,176,'文档','最终版_v7_再改一次','同一个决定，三个版本',ORANGE),
             (710,625,410,176,'日历','周五之前，谁来推进？','责任和截止时间尚未对齐',(124,96,208)),
             (1320,700,360,150,'待办','再同步一下','上下文仍在切换',BLUE)]
        for i,(x,y,w,h,tag,title,sub,c) in enumerate(pts):
            a=out((t-i*.35)/.6);xx=x+(1-a)*((-1)**i)*90+math.sin(t*1.6+i)*14;yy=y+math.cos(t*1.25+i*2)*13
            card(d,xx,yy,w,h,tag,title,sub,c,a)
        for i in range(6):
            xx=680+math.sin(t*.8+i)*300;yy=460+i*38
            disk(d,xx,yy,3,(211,220,238))
    elif t<8:
        u=out((t-4)/1.6)
        text(d,(96,162),'把共识，放进同一个地方。',64,INK,True)
        text(d,(100,258),'把消息里的下一步，变成每个人都看得见的任务。',26,MUTED)
        rr(d,(300,370,1620,910),'white',24,(218,226,241),2)
        text(d,(336,402),'秋季发布 / 设计协作',28,INK,True)
        line(d,[(300,461),(1620,461)],(232,236,244),2)
        starts=[(280,410),(1120,365),(710,625)]
        targets=[(336,502),(766,502),(1196,502)]
        for i,(tag,title,sub,c) in enumerate([('决定','主视觉方向确认','银蓝空间 / 统一设计基准',BLUE),('责任人','林同学','负责主视觉最终交付',ORANGE),('截止时间','今天 18:00','所有人共享同一时间点',(124,96,208))]):
            x=lerp(starts[i][0],targets[i][0],u);y=lerp(starts[i][1],targets[i][1],u)
            card(d,x,y,lerp(400,388,u),176,tag,title,sub,c)
        a=out((t-6.3)/.6)
        rr(d,(336,744,1584,851),mix(BG,(234,240,255),a),16)
        text(d,(369,776),'从讨论到任务，只保留真正需要推进的事。',26,mix(BG,BLUE,a),True)
    elif t<15:
        q=t-8
        text(d,(96,162),'一句共识，三个确定。',68,INK,True)
        text(d,(100,260),'决定 · 责任人 · 截止时间',28,MUTED)
        rr(d,(320,370,1600,900),(255,255,255),26,(218,226,241),2)
        text(d,(366,410),'发布主视觉',38,INK,True)
        rr(d,(1340,404,1548,451),(233,241,255),18);text(d,(1367,414),'待推进',21,BLUE,True)
        line(d,[(365,488),(1555,488)],(229,235,244),2)
        rows=[('决定','银蓝空间 / 统一设计基准'),('责任人','林同学'),('截止时间','今天 18:00')]
        for i,(label,value) in enumerate(rows):
            yy=535+i*106;hi=ease((q-i*1.25)/.6)
            rr(d,(354,yy-18,1566,yy+66),mix((255,255,255),(239,244,255),hi),14)
            text(d,(381,yy),label,24,MUTED)
            text(d,(643,yy),value,27,INK,True)
            if hi>0:
                # Line draws from label to confirmed check, describing causality.
                line(d,[(1120,yy+23),(1120+hi*300,yy+23)],mix((239,244,255),BLUE,hi),2)
                if hi>.95:check(d,1509,yy+20,.8)
        rr(d,(1341,813,1546,865),BLUE,14)
        text(d,(1443,825),'创建任务',21,'white',True,'mt')
        # Authored pointer arrives on the button, presses, and the status responds.
        p=out((q-4.4)/.9);cx=lerp(1650,1455,p);cy=lerp(940,844,p)
        d.polygon([(cx,cy),(cx+4,cy+32),(cx+13,cy+23),(cx+27,cy+25)],fill=INK)
        if q>5.4:
            r=(q-5.4)*80
            if r<75:d.ellipse((1444-r,837-r,1444+r,837+r),outline=mix(BG,BLUE,1-r/75),width=3)
            rr(d,(1340,404,1548,451),(231,247,239),18);text(d,(1367,414),'已创建',21,(24,140,94),True)
    elif t<20:
        q=t-15
        text(d,(96,162),'每一步，都有回音。',68,INK,True)
        text(d,(100,260),'任务移动，进度同步；完成的消息回到共同上下文。',27,MUTED)
        taskboard(d,clamp(q/3.4))
        if q>3.4:
            a=out((q-3.4)/.5);rr(d,(710,925,1210,983),mix(BG,(224,244,234),a),29)
            text(d,(960,940),'3 项任务已完成 · 团队同步更新',20,mix(BG,(29,133,91),a),True,'mt')
    else:
        q=t-20;a=out(q/.8)
        # One shared identity assembled from three formerly separate cards.
        for i,c in enumerate([BLUE,ORANGE,(124,96,208)]):
            xx=lerp([300,1200,720][i],1310+i*96,a);yy=lerp([500,390,780][i],430+i*88,a)
            rr(d,(xx,yy,xx+190,yy+190),c,48)
        text(d,(98,300),'少一层切换，',88,INK,True)
        text(d,(98,420),'多一步向前。',88,BLUE,True)
        text(d,(105,596),'SYNC / 同频',34,INK,True)
        text(d,(105,655),'让协作，进入同一拍。',26,MUTED)
        line(d,[(105,741),(710,741)],(203,215,238),3)
        text(d,(105,773),'决定更清楚   责任更明确   推进有闭环',23,MUTED)
    return fade_frame(im,t,24)

NIGHT=(8,25,39);PANEL=(15,38,53);AMBER=(255,190,94);CREAM=(245,229,194);DIM=(120,147,159)
def light_brand(d,t):
    text(d,(92,58),'留一盏灯',26,CREAM,True)
    text(d,(1828,62),'A LIGHT FOR THE WAY HOME',17,DIM,anchor='rt')
    line(d,[(92,105),(1828,105)],(43,67,78),2)
    text(d,(94,1026),'原创公共沟通概念 / 图形叙事短片',17,DIM)
    text(d,(1828,1026),f'{t:05.1f} / 30.0',17,DIM,anchor='rt')
def glow(im,x,y,r,strength=.6):
    d=ImageDraw.Draw(im)
    for k in range(14,0,-1):
        rad=r*(k/14);a=(1-k/15)**2*strength
        disk(d,x,y,rad,mix(NIGHT,AMBER,a*.24))
def building(d,x,y,w,h,cols,rows,lit=None,opening=1):
    rr(d,(x,y,x+w,y+h),PANEL,6)
    margin=22;gx=(w-2*margin)/cols;gy=(h-2*margin)/rows
    for c in range(cols):
        for r in range(rows):
            idx=r*cols+c;a=lit(c,r) if lit else 0
            xx=x+margin+c*gx+gx*.1;yy=y+margin+r*gy
            col=mix((27,54,67),AMBER,a)
            rr(d,(xx,yy,xx+gx*.64,yy+gy*.54*opening),col,3)
def person(d,x,y,scale=1,step=0,c=CREAM):
    disk(d,x,y-57*scale,10*scale,c)
    line(d,[(x,y-43*scale),(x,y-13*scale)],c,9*scale)
    line(d,[(x,y-33*scale),(x-13*scale,y-15*scale)],c,6*scale)
    line(d,[(x,y-33*scale),(x+15*scale,y-24*scale)],c,6*scale)
    st=math.sin(step)*10*scale
    line(d,[(x,y-13*scale),(x-10*scale-st,y+12*scale)],c,6*scale)
    line(d,[(x,y-13*scale),(x+10*scale+st,y+12*scale)],c,6*scale)
def curvepts(a,b,bend,n=80):
    return [(lerp(a[0],b[0],i/(n-1)),lerp(a[1],b[1],i/(n-1))-math.sin(math.pi*i/(n-1))*bend) for i in range(n)]
def partial_line(d,points,p,c,w=4):
    count=max(2,round(len(points)*clamp(p)))
    if p>0:line(d,points[:count],c,w)
def light_frame(t):
    im=Image.new('RGB',(W,H),NIGHT);d=ImageDraw.Draw(im);light_brand(d,t)
    if t<6:
        q=t/6
        text(d,(98,172),'城市睡了。',76,CREAM,True)
        text(d,(102,276),'但夜晚，还没有走完。',27,DIM)
        buildings=[(180,470,250,400,4,6),(467,370,260,500,4,8),(765,505,235,365,3,5),(1040,410,310,460,5,7),(1390,515,340,355,5,5)]
        for i,(x,y,w,h,c,r) in enumerate(buildings):
            def lit(cc,rrr,i=i):
                phase=((cc*7+rrr*3+i*11)%19)/19
                return (1-ease((q-phase*.6)/.25))*.85
            building(d,x,y,w,h,c,r,lit)
        line(d,[(92,904),(1828,904)],(46,73,86),2)
        # The single window remains when the city switches off.
        rr(d,(1194,654,1232,688),AMBER,4)
        disk(d,1690,260,35,(34,58,72))
    elif t<12:
        q=(t-6)/6
        text(d,(98,172),'总有人，还在路上。',70,CREAM,True)
        text(d,(102,276),'一个清楚的方向，可以让归途安心一点。',26,DIM)
        for i in range(8):
            x=140+i*220;y=440+math.sin(i*1.2)*70
            building(d,x,y,170,420-(y-440),2,6,lambda c,r:.08)
        road=curvepts((180,885),(1530,750),-55)
        line(d,road,(55,82,94),4)
        p=out(q)*.85;pos=road[round((len(road)-1)*p)]
        # An individual actually walks along a curved path, rather than a pan over a still.
        person(d,pos[0],pos[1]-19,1.5,t*7)
        x,y=1530,560
        glow(im,x,y,120,.8);d=ImageDraw.Draw(im)
        rr(d,(x-34,y-43,x+34,y+43),AMBER,5)
        d.polygon([(x-34,y+43),(x+34,y+43),(1690,860),(1390,860)],fill=(40,48,45))
        rr(d,(x-34,y-43,x+34,y+43),AMBER,5)
        text(d,(1529,908),'有光的地方，有人在等。',21,CREAM,anchor='mt')
    elif t<20:
        q=(t-12)/8
        text(d,(98,172),'一盏灯，接住另一个人。',66,CREAM,True)
        text(d,(102,274),'从一个窗口，到一条彼此照应的路。',26,DIM)
        nodes=[(260,725),(530,510),(785,785),(1040,565),(1320,715),(1605,480)]
        for i,p in enumerate(nodes):
            x,y=p;rr(d,(x-85,y-100,x+85,y+105),PANEL,12)
            active=ease((q-i*.12)/.15)
            if i:
                points=curvepts(nodes[i-1],p,65)
                partial_line(d,points,(q-(i-1)*.12)/.16,mix((37,64,77),AMBER,.75),4)
            glow(im,x,y,95,active);d=ImageDraw.Draw(im)
            rr(d,(x-29,y-42,x+29,y+42),mix((27,54,67),AMBER,active),5)
            line(d,[(x,y-42),(x,y+42)],mix((27,54,67),NIGHT,active),4)
            line(d,[(x-29,y),(x+29,y)],mix((27,54,67),NIGHT,active),4)
        for j in range(5):
            p=clamp((q-j*.12)/.16)
            if p>0 and p<1:
                pts=curvepts(nodes[j],nodes[j+1],65);x,y=pts[round(p*(len(pts)-1))];disk(d,x,y,9,CREAM)
        text(d,(101,929),'看见 → 等候 → 连接',26,CREAM,True)
        text(d,(1828,939),'让善意成为可感知的信号。',21,DIM,anchor='rt')
    elif t<26:
        q=(t-20)/6
        text(d,(98,172),'把等候，变成看得见的温柔。',61,CREAM,True)
        text(d,(102,274),'门口的一盏灯，也是社区的一次回应。',26,DIM)
        # Existing six windows reconfigure into an illuminated doorway.
        prev=[(260,725),(530,510),(785,785),(1040,565),(1320,715),(1605,480)]
        nxt=[(790,760),(790,590),(790,420),(1130,420),(1130,590),(1130,760)]
        a=ease(q/.38)
        for i,(x,y) in enumerate(prev):
            xx=lerp(x,nxt[i][0],a);yy=lerp(y,nxt[i][1],a)
            rr(d,(xx-28,yy-42,xx+28,yy+42),AMBER,5)
        if a>.9:
            frame=ease((q-.25)/.25)
            rr(d,(758,374,1162,858),mix(NIGHT,(54,66,62),frame),18)
            rr(d,(784,400,1136,858),mix(NIGHT,(252,184,85),frame),8)
            # Door panel rotates open through width collapse, revealing warm interior.
            door=clamp((q-.45)/.35)
            poly=[(784,400),(1136-(1136-811)*door,400+40*door),(1136-(1136-811)*door,858-40*door),(784,858)]
            d.polygon(poly,fill=(28,49,59))
            disk(d,1100-(1100-801)*door,628,7,AMBER)
            d.polygon([(785,858),(1137,858),(1450,980),(475,980)],fill=(37,49,48))
            p=out((q-.45)/.5)
            person(d,lerp(420,995,p),897,1.45,t*6)
        line(d,[(92,982),(1828,982)],(50,70,77),2)
    else:
        q=t-26
        text(d,(100,300),'为晚归的人',88,CREAM,True)
        text(d,(100,423),'留一盏灯。',102,AMBER,True)
        text(d,(105,617),'一个小小的回应，让城市更有温度。',29,DIM)
        x,y=1485,540;glow(im,x,y,250,.9);d=ImageDraw.Draw(im)
        rr(d,(x-100,y-140,x+100,y+140),AMBER,14)
        line(d,[(x,y-140),(x,y+140)],NIGHT,10)
        line(d,[(x-100,y),(x+100,y)],NIGHT,10)
        text(d,(105,819),'A LIGHT FOR THE WAY HOME',20,CREAM,True)
        text(d,(105,867),'公共沟通概念短片 · 非真实公益活动或成效记录',19,DIM)
    return fade_frame(im,t,30)

def make_audio(name,duration):
    sr=48000;n=int(sr*duration);tm=np.arange(n)/sr;audio=np.zeros(n,dtype=np.float64)
    # Original, procedurally composed score. No sampled music or third-party recordings.
    chords=[[146.83,220,293.66,369.99],[130.81,196,261.63,329.63],[164.81,220,329.63,440],[146.83,220,293.66,440]]
    block=6 if name=='sync' else 7.5
    for i,chord in enumerate(chords):
        start=i*block;mask=(tm>=start)&(tm<start+block);tt=tm[mask]-start
        env=np.minimum(tt/.8,1)*np.minimum((block-tt)/1.2,1)
        for j,f in enumerate(chord):
            audio[mask]+=.018*env*(np.sin(2*np.pi*f*tt+j*.45)+.25*np.sin(2*np.pi*2*f*tt))
    notes=[440,554.37,659.25,880,739.99,659.25,554.37,440]
    interval=.75 if name=='sync' else 1.25
    for k,start in enumerate(np.arange(.5,duration-1,interval)):
        length=min(1.8,duration-start);idx=(tm>=start)&(tm<start+length);tt=tm[idx]-start
        env=(1-np.exp(-tt*70))*np.exp(-tt*3.2)
        f=notes[(k*3 if name=='sync' else k)%len(notes)]
        audio[idx]+=(.08 if name=='sync' else .055)*env*(np.sin(2*np.pi*f*tt)+.18*np.sin(2*np.pi*f*2.01*tt))
    # Clear, low-level interaction cues align to authored actions, not arbitrary sound peaks.
    cues=[4,6.2,8,9.5,10.7,13.4,15,17.8,20] if name=='sync' else [4.7,7.4,12,13.5,15,16.5,18,22.8,26]
    for start in cues:
        idx=(tm>=start)&(tm<start+.22);tt=tm[idx]-start
        audio[idx]+=.08*np.exp(-tt*25)*np.sin(2*np.pi*(720*tt-1500*tt*tt))
    audio*=np.minimum(tm/.3,1)*np.minimum((duration-tm)/.7,1)
    peak=np.max(np.abs(audio));audio*=.66/max(peak,.01)
    stereo=np.column_stack([audio,np.roll(audio,240)*.94]);pcm=(np.clip(stereo,-1,1)*32767).astype('<i2')
    dest=TMP/(name+'.wav')
    with wave.open(str(dest),'wb') as wf:wf.setnchannels(2);wf.setsampwidth(2);wf.setframerate(sr);wf.writeframes(pcm.tobytes())
    return dest

def render(name,duration,fn):
    OUT.mkdir(parents=True,exist_ok=True);EV.mkdir(parents=True,exist_ok=True)
    audio=make_audio(name,duration)
    dest=OUT/(name+'.mp4')
    args=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(audio),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','-t',str(duration),str(dest)]
    proc=subprocess.Popen(args,stdin=subprocess.PIPE)
    for k in range(FPS*duration):
        frame=fn(k/FPS);proc.stdin.write(frame.tobytes())
        if k%(FPS*4)==0:print(f'{name}: {k/FPS:.0f}/{duration}s',flush=True)
    proc.stdin.close();code=proc.wait()
    if code:raise RuntimeError('ffmpeg failed '+str(code))
    times=[1,3.7,5.5,7.5,9,11,13.5,16,18.5,20.8,22,23.5] if name=='sync' else [1,4.8,7,10,12.5,14.5,17,19,20.8,23.8,26.4,28.5]
    sheet=Image.new('RGB',(1440,1120),'#eeeeea');d=ImageDraw.Draw(sheet)
    for i,t in enumerate(times):
        thumb=fn(t).resize((480,270),Image.Resampling.LANCZOS);sheet.paste(thumb,((i%3)*480,(i//3)*280))
        text(d,((i%3)*480+8,(i//3)*280+250),f'{t:04.1f}s',14,'white',True)
    sheet.save(EV/(name+'-contact-sheet.jpg'),quality=93)
    cover_t=11 if name=='sync' else 28
    fn(cover_t).save(OUT/(name+'-cover.jpg'),quality=94)
    meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(dest)]))
    (EV/(name+'-ffprobe.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
    subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-'],check=True)
    print(json.dumps({'name':name,'seconds':meta['format']['duration'],'bytes':dest.stat().st_size,'streams':[(x['codec_type'],x.get('width'),x.get('height'),x.get('nb_frames')) for x in meta['streams']]}),flush=True)

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description='Render two original portfolio motion films. Requires Pillow, NumPy and ffmpeg/ffprobe on PATH.')
    parser.add_argument('film',choices=['sync','light','both'],nargs='?',default='both')
    parser.add_argument('--out',type=pathlib.Path,default=OUT,help='Video and cover directory; default: renders beside this script.')
    parser.add_argument('--evidence',type=pathlib.Path,default=EV,help='Contact sheets and probe JSON; default: renders/evidence beside this script.')
    parser.add_argument('--scratch',type=pathlib.Path,default=TMP,help='Intermediate WAV directory; default: renders/scratch beside this script.')
    args=parser.parse_args();OUT=args.out;EV=args.evidence;TMP=args.scratch;TMP.mkdir(parents=True,exist_ok=True)
    which=args.film
    if which in ['sync','both']:render('sync',24,sync_frame)
    if which in ['light','both']:render('light',30,light_frame)
