from PIL import Image, ImageDraw, ImageFilter
import numpy as np
W,H=1200,2040  # larger than frame for camera drift
img=Image.new('RGB',(W,H),(14,20,34))
d=ImageDraw.Draw(img,'RGBA')
for x in range(0,W,40): d.line([(x,0),(x,H)],fill=(255,255,255,10 if x%200 else 18),width=1)
for y in range(0,H,40): d.line([(0,y),(W,y)],fill=(255,255,255,10 if y%200 else 18),width=1)
# soft top-left key light and bottom vignette, baked in (no live glow)
a=np.array(img).astype(np.float32)
yy,xx=np.mgrid[0:H,0:W]
light=np.exp(-(((xx-150)/700)**2+((yy-150)/900)**2))*14
vign=np.clip(((yy-H*0.55)/(H*0.6)),0,1)**2*10
a[...,0]+=light-vign; a[...,1]+=light-vign; a[...,2]+=light*1.2-vign
img=Image.fromarray(np.clip(a,0,255).astype(np.uint8))
img.save('../reel/assets/img/desk.png')
# crop matching the frame at drift 0 (offset 60,60) then blur 28 px for glass cards
fr=img.crop((60,60,60+1080,60+1920)).filter(ImageFilter.GaussianBlur(28))
fr.save('../reel/assets/img/desk_blur.png')
rng=np.random.default_rng(3)
n=(rng.random((256,256))*255).astype(np.uint8)
Image.fromarray(np.stack([n,n,n,np.full_like(n,255)],-1),'RGBA').save('../reel/assets/img/noise.png')
print('ok')
