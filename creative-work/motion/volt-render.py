"""VOLT: original 22-second photographic motion concept.

AI-generated photographic assets use camera moves, light and focus compositing.
This script does not create continuous live action or claim a
video-model run. Requires Python, Pillow, NumPy, ffmpeg, ffprobe and Windows fonts.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
import argparse, json, math, subprocess, wave
import numpy as np

HERE=Path(__file__).resolve().parent
ASSETS=HERE.parent/'assets'
W,H,FPS,DURATION=1920,1080,24,22
CUTS=(0,4.25,8.75,14.5,22)
LIME=(219,255,0)
FONTS={}

def clamp(x):return max(0.0,min(1.0,x))
def smooth(x):x=clamp(x);return x*x*(3-2*x)
def cubic(x):return 1-(1-clamp(x))**3
def mix(a,b,x):return a+(b-a)*x
def font(size,kind='cn'):
    key=(size,kind)
    if key not in FONTS:
        name={'cn':'msyhbd.ttc','small':'msyh.ttc','latin':'ARIALNB.TTF'}[kind]
        FONTS[key]=ImageFont.truetype('C:/Windows/Fonts/'+name,round(size))
    return FONTS[key]

def image(name,mode='RGB'):
    p=ASSETS/name
    if not p.exists():raise FileNotFoundError(f'Required photographic asset is missing: {p}')
    return Image.open(p).convert(mode)

def frame_crop(src,zoom=1,dx=0,dy=0,anchor=(.5,.5),transparent=False):
    """Camera transform, in pixels of the final frame; avoids geometry morphs."""
    sw,sh=src.size
    ratio=min(sw/W,sh/H)/zoom
    cw,ch=W*ratio,H*ratio
    cx=sw*anchor[0]+dx*ratio;cy=sh*anchor[1]+dy*ratio
    box=(cx-cw/2,cy-ch/2,cx+cw/2,cy+ch/2)
    return src.transform((W,H),Image.Transform.EXTENT,box,Image.Resampling.BICUBIC,
                         fillcolor=(0,0,0,0) if transparent else (8,12,15))

def show_text(canvas,words,x,y,size,color,alpha=1,kind='cn',tracking=0):
    if alpha<=0:return
    layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer);f=font(size,kind)
    xx=x
    for c in words:
        d.text((round(xx),round(y)),c,font=f,fill=(*color,round(255*clamp(alpha))),stroke_width=0)
        xx+=d.textlength(c,font=f)+tracking
    canvas.alpha_composite(layer)

def make_audio(dest):
    """All waveforms/noise are synthesized here; no external musical samples."""
    sr=48000;n=DURATION*sr;tm=np.arange(n,dtype=np.float64)/sr
    sound=np.zeros((n,2),dtype=np.float64);rng=np.random.default_rng(221104)
    def add(start,signal,vol=1,pan=0):
        a=round(start*sr);b=min(n,a+len(signal))
        if b<=a:return
        sig=signal[:b-a]*vol
        sound[a:b,0]+=sig*math.sqrt((1-pan)/2)
        sound[a:b,1]+=sig*math.sqrt((1+pan)/2)
    def tone(freq,dur,attack=.01,decay=1.8):
        t=np.arange(round(dur*sr))/sr
        return (1-np.exp(-t/max(.001,attack)))*np.exp(-decay*t)*np.sin(2*np.pi*freq*t)
    def colored_noise(dur,low,high):
        m=round(dur*sr);noise=rng.normal(size=m)
        f=np.fft.rfftfreq(m,1/sr);spec=np.fft.rfft(noise)
        filt=np.exp(-(f/max(high,1))**3)*(1-np.exp(-(f/max(low,1))**3))
        z=np.fft.irfft(spec*filt,n=m);return z/max(np.std(z),1e-5)
    # A train passes; stereo position and motor pitch are independently animated.
    t=tm[:round(4.25*sr)];env=np.minimum(t/.4,1)*(1-smooth_array((t-3.96)/.29))
    rail=colored_noise(4.25,80,3500)*(.08+.025*np.sin(t*2*np.pi*21))
    motor=.07*np.sin(2*np.pi*(82*t+5*t*t))+.025*np.sin(2*np.pi*(220*t+17*t*t))
    # Metallic wheel texture is lower than the rumble and intentionally retreats at the cut.
    rail+=(.018*np.sin(2*np.pi*(710*t+36*t*t))+.01*np.sin(2*np.pi*(1340*t+14*t*t)))
    a=(rail+motor)*env
    pan=np.sin((t/4.25-.5)*np.pi)*.55
    sound[:len(t),0]+=a*np.sqrt((1-pan)/2);sound[:len(t),1]+=a*np.sqrt((1+pan)/2)
    # Very brief vacuum at the product cut, followed by a tactile low-frequency seal.
    add(4.34,tone(52,1.5,.015,3.4),.24)
    add(4.35,tone(138,1.1,.008,5),.035,.12)
    for k,start in enumerate([5.15,6.35,7.55]):
        add(start,tone([146.832,164.814,130.813][k],1.2,.012,3.2),.055,[-.2,.2,0][k])
    # A small airy light sweep moves around the macro, not a stock whoosh.
    for start,pan in [(4.25,-.7),(8.46,.7),(14.28,-.35)]:
        dur=.52;u=np.arange(round(dur*sr))/sr;env=np.sin(np.pi*u/dur)**2
        add(start,colored_noise(dur,1100,8000)*env,.045,pan)
    # The open waterfront is intentionally sparse: soft air and three separated tones.
    breeze=colored_noise(5.75,160,2800);u=np.arange(len(breeze))/sr
    env=np.sin(np.pi*u/5.75)**2*(.75+.25*np.sin(u*1.4))
    add(8.75,breeze*env,.018,-.3)
    add(8.9,tone(146.832,4.8,.32,.65),.055,0)
    for start,freq,pan in [(9.35,293.665,-.35),(11.1,440,.35),(12.95,349.228,-.1)]:
        z=tone(freq,2.8,.025,1.05)+.12*tone(freq*2.001,2.8,.02,1.6)
        add(start,z,.06,pan)
    add(14.55,tone(73.416,2.2,.008,1.8),.16)
    add(14.55,tone(293.665,1.8,.006,2.6),.06,.1)
    # Three-note original sonic signature resolves the final visual lock-up.
    for start,freq,pan in [(17.05,293.665,-.22),(17.48,440,.22),(18.08,587.33,0)]:
        z=tone(freq,3.5,.012,.95)+.16*tone(freq*2.002,3.5,.008,1.5)
        add(start,z,.1,pan)
    # High airy space at the ending; no reverb plug-in or external recording.
    end=colored_noise(7.5,3500,9000)
    u=np.arange(len(end))/sr;add(14.5,end*np.sin(np.pi*u/7.5)**2,.004,.4)
    dry=sound.copy()
    for delay,gain in [(.071,.09),(.139,.05),(.251,.025)]:
        shift=int(delay*sr);sound[shift:]+=dry[:-shift,::-1]*gain
    fade=np.minimum(tm/.07,1)*np.minimum((DURATION-tm)/.9,1)
    sound*=fade[:,None]
    peak=np.abs(sound).max();sound*=.82/max(peak,1e-9)
    pcm=(np.clip(sound,-1,1)*32767).astype('<i2')
    with wave.open(str(dest),'wb')as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes(pcm.tobytes())
    return {'sample_rate':sr,'channels':2,'seconds':DURATION,'peak_dbfs':float(20*np.log10(np.abs(pcm).max()/32767)),'source':'All sounds procedurally synthesized; no external samples.'}

def smooth_array(x):x=np.clip(x,0,1);return x*x*(3-2*x)

class Film:
    def __init__(self,hero_only=False,macro_only=False):
        self.subway=image('volt-subway.png')
        if not hero_only and not macro_only:
            self.lifestyle=image('volt-lifestyle.png')
        if not hero_only:
            self.macro=image('volt-macro.png')
            self.macro_blur=self.macro.filter(ImageFilter.GaussianBlur(5))
        self.product=image('volt-cutout.png','RGBA')
        # Fixed photographic buffers support a pull-focus without fabricating new geometry.
        y,x=np.mgrid[0:H,0:W];self.x=x/W;self.y=y/H
        self.vignette=np.uint8(np.clip((np.sqrt(((self.x-.5)/.73)**2+((self.y-.5)/.8)**2)-.45)*84,0,65))
        rad=np.exp(-(((self.x-.70)/.40)**2+((self.y-.40)/.55)**2)*2.2)
        floor=np.exp(-(((self.x-.70)/.46)**2+((self.y-.93)/.12)**2)*2.6)
        base=np.zeros((H,W,3),dtype=np.float32)
        for ch,value in enumerate([6,10,12]):base[:,:,ch]=value+rad*[20,27,31][ch]+floor*[7,9,8][ch]
        self.hero_bg=Image.fromarray(np.uint8(np.clip(base,0,255)),'RGB')
        rng=np.random.default_rng(763)
        self.reflections=[(rng.uniform(.02,.49),rng.uniform(.465,.555),rng.uniform(2,8),rng.uniform(0,6.28)) for _ in range(36)]
        self.grain=[]
        for i in range(8):
            g=rng.integers(0,255,(270,480),dtype=np.uint8)
            self.grain.append(Image.fromarray(g,'L').resize((W,H),Image.Resampling.BILINEAR).convert('RGB'))
        self.column=self.subway.crop((0,0,int(self.subway.width*.13),self.subway.height)).resize((270,H)).filter(ImageFilter.GaussianBlur(3))

    def station(self,t):
        u=t/4.25
        # Camera move plus independent foreground light and column layers.
        im=frame_crop(self.subway,mix(1.025,1.075,smooth(u)),dx=mix(-7,9,u)).convert('RGBA')
        # Passing near-field reflections add actual independent motion across the train.
        lights=Image.new('RGBA',(W,H));d=ImageDraw.Draw(lights)
        for k in range(5):
            xx=((t*940+k*530)%(W+1150))-700
            yy=260+k*146
            d.polygon([(xx,yy),(xx+330,yy-44),(xx+680,yy-46),(xx+260,yy+20)],fill=(166,218,239,12))
        lights=lights.filter(ImageFilter.GaussianBlur(18));im.alpha_composite(lights)
        # A real photographed column crosses the lens to motivate the abrupt focal change.
        if t>3.67:
            q=clamp((t-3.67)/.58);x=round(mix(-600,W+180,cubic(q)))
            im.alpha_composite(self.column.convert('RGBA'),(x,0))
        if t<.24:im=Image.blend(Image.new('RGBA',(W,H),(0,0,0,255)),im,smooth(t/.24))
        if t>4.13:im=Image.blend(im,Image.new('RGBA',(W,H),(3,7,9,255)),smooth((t-4.13)/.12))
        return im

    def detail(self,t):
        u=(t-4.25)/4.5
        focus=smooth((t-4.25)/.75)
        source=Image.blend(self.macro_blur,self.macro,focus)
        im=frame_crop(source,mix(1.08,1.015,cubic(u)),dx=mix(16,-14,u),dy=mix(10,-4,u)).convert('RGBA')
        # Wide specular strip is deliberately weak; it reads as a studio lamp, not an effect.
        pos=mix(-.4,1.4,smooth(u));band=np.exp(-((self.x-pos-self.y*.12)/.16)**2)
        luma=np.asarray(im.convert('L'),dtype=np.float32)/255
        alpha=np.uint8(band*(.25+.75*luma)*20)
        sweep=Image.new('RGBA',(W,H),(180,222,236,0));sweep.putalpha(Image.fromarray(alpha,'L'));im.alpha_composite(sweep)
        if t<4.43:im=Image.blend(Image.new('RGBA',(W,H),(3,7,9,255)),im,smooth((t-4.25)/.18))
        return im

    def quiet_life(self,t):
        u=(t-8.75)/5.75
        # A different listener in a bright everyday setting. No body animation is implied.
        im=frame_crop(self.lifestyle,mix(1.015,1.028,smooth(u)),dx=mix(-8,8,u)).convert('RGBA')
        layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
        # Small water reflections form a separate, quiet environmental layer.
        for x,y,length,phase in self.reflections:
            xx=x*W+math.sin(t*.7+phase)*4;yy=y*H
            alpha=round(6+11*(.5+.5*math.sin(t*1.8+phase)))
            d.line((xx,yy,xx+length,yy),fill=(223,241,246,alpha),width=1)
        im.alpha_composite(layer)
        # A short dark dissolve prepares the final product studio without a visual effect.
        if t>14.23:
            q=smooth((t-14.23)/.27)
            im=Image.blend(im,Image.new('RGBA',(W,H),(7,11,13,255)),q)
        return im

    def hero(self,t):
        u=t-14.5
        im=self.hero_bg.copy().convert('RGBA')
        settle=cubic(u/3.5)
        scale=mix(1.03,.86,settle)
        ph=round(1080*scale);pw=round(self.product.width/self.product.height*ph)
        prod=self.product.resize((pw,ph),Image.Resampling.LANCZOS)
        x=round(mix(845,860,settle));y=round(mix(-36,66,settle))
        # Light/grounding is a separate physical layer; product orientation stays locked.
        sh=Image.new('RGBA',(W,H));sd=ImageDraw.Draw(sh)
        sd.ellipse((1010,957,1750,1018),fill=(0,0,0,170));sh=sh.filter(ImageFilter.GaussianBlur(24));im.alpha_composite(sh)
        im.alpha_composite(prod,(x,y))
        # The headline arrives only after the product camera has mostly settled.
        a=smooth((u-.65)/.75);dy=mix(20,0,cubic((u-.65)/.85))
        show_text(im,'VOLT',104,113+dy,220,LIME,a,'latin',-5)
        show_text(im,'把噪声，',110,422,91,(237,242,243),smooth((u-2.25)/.7))
        show_text(im,'留在身后。',110,539,91,(237,242,243),smooth((u-2.65)/.7))
        show_text(im,'伏特 / VOLT ONE',114,746,23,(149,164,170),smooth((u-3.2)/.7),'small',2)
        show_text(im,'独立品牌概念',114,933,17,(98,114,122),smooth((u-3.5)/.7),'small',2)
        if u<.2:im=Image.blend(Image.new('RGBA',(W,H),(7,11,13,255)),im,smooth(u/.2))
        return im

    def frame(self,t):
        if t<4.25:im=self.station(t)
        elif t<8.75:im=self.detail(t)
        elif t<14.5:im=self.quiet_life(t)
        else:im=self.hero(t)
        shade=Image.new('RGBA',(W,H),(0,0,0,0));shade.putalpha(Image.fromarray(self.vignette,'L'));im.alpha_composite(shade)
        out=Image.blend(im.convert('RGB'),self.grain[int(t*FPS)%len(self.grain)],.012)
        return out

def write_storyboard(film):
    times=[2.1,6.35,11.45,20.1]
    names=['01 / CITY','02 / DETAIL','03 / QUIET LIFE','04 / VOLT']
    timing=['00.00—04.25','04.25—08.75','08.75—14.50','14.50—22.00']
    sheet=Image.new('RGB',(2160,1500),'#101619');d=ImageDraw.Draw(sheet)
    d.text((72,56),'VOLT / 把噪声，留在身后。',font=font(50),fill='#e9eeee')
    d.text((76,128),'PHOTOGRAPHIC MOTION  /  22 SECONDS',font=font(21,'latin'),fill='#a5bdc4')
    for i,t in enumerate(times):
        x=72+(i%2)*1038;y=210+(i//2)*612
        thumb=film.frame(t).resize((978,550),Image.Resampling.LANCZOS);sheet.paste(thumb,(x,y))
        d.text((x,y+567),names[i],font=font(20,'latin'),fill=LIME)
        d.text((x+727,y+567),timing[i],font=font(18,'small'),fill='#9cadb2')
    sheet.save(HERE/'volt-storyboard.jpg',quality=95)
    for i,t in enumerate(times):film.frame(t).save(HERE/f'volt-shot-{i+1}.jpg',quality=95)
    film.frame(20.1).save(HERE/'volt-poster.jpg',quality=95)

def render(film,duration=DURATION,dest=None):
    audio=HERE/'volt-original-audio.wav';make_audio(audio)
    dest=dest or HERE/'volt-film.mp4'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','-','-i',str(audio),'-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p','-af','loudnorm=I=-16:TP=-1.5:LRA=8','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart','-t',str(duration),str(dest)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for k in range(round(duration*FPS)):
        p.stdin.write(film.frame(k/FPS).tobytes())
        if k%(FPS*2)==0:print(f'VOLT {k/FPS:.0f} / {duration}s',flush=True)
    p.stdin.close()
    if p.wait():raise RuntimeError('FFmpeg encoding failed')
    meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(dest)]))
    dest.with_suffix('.ffprobe.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
    subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-'],check=True)
    return meta

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['audio','hero','macro','opening','preview','render'],default='preview',nargs='?');a=p.parse_args()
    HERE.mkdir(parents=True,exist_ok=True)
    if a.mode=='audio':print(json.dumps(make_audio(HERE/'volt-original-audio.wav')))
    elif a.mode=='hero':Film(hero_only=True).frame(20.1).save(HERE/'volt-poster.jpg',quality=95)
    elif a.mode=='macro':Film(macro_only=True).frame(6.35).save(HERE/'volt-shot-2.jpg',quality=95)
    elif a.mode=='opening':
        film=Film(macro_only=True);film.frame(2.1).save(HERE/'volt-shot-1.jpg',quality=95)
        print(json.dumps(render(film,8.75,HERE/'volt-opening.mp4')['format']))
    else:
        film=Film();write_storyboard(film)
        if a.mode=='render':print(json.dumps(render(film)['format']))
