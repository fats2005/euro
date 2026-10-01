import math, random, sys, pygame
pygame.init(); pygame.display.set_caption('EuroRoad Racer')
W,H=1280,720; screen=pygame.display.set_mode((W,H),pygame.RESIZABLE); clock=pygame.time.Clock()
ROAD_W=760; MAX_SPEED=250; ACCEL=95; BRAKE=150; DRAG=24
WHITE=(245,245,245); GRASS=(55,132,66); ROAD=(52,55,61); EDGE=(235,235,220); YELLOW=(245,190,55)
font=pygame.font.SysFont('arial',22,bold=True); big=pygame.font.SysFont('arial',38,bold=True); small=pygame.font.SysFont('arial',16)
def clamp(v,a,b): return max(a,min(b,v))
def car_surface(color,scale=1):
 s=pygame.Surface((220,120),pygame.SRCALPHA); pygame.draw.ellipse(s,(0,0,0,90),(20,83,180,25)); pygame.draw.polygon(s,color,[(25,78),(40,55),(68,48),(83,20),(150,20),(174,49),(198,59),(205,82),(187,92),(35,92)]); pygame.draw.polygon(s,(35,52,67),[(88,26),(145,26),(164,49),(79,49)]); pygame.draw.rect(s,(255,235,180),(194,65,10,10),border_radius=3); pygame.draw.rect(s,(255,235,180),(22,65,10,10),border_radius=3)
 for x in (47,163): pygame.draw.circle(s,(15,15,17),(x,88),17); pygame.draw.circle(s,(95,95,100),(x,88),7)
 return pygame.transform.smoothscale(s,(int(220*scale),int(120*scale)))
player_img=car_surface((36,113,230)); traffic=[]
colors=[(220,50,50),(235,180,40),(35,160,100),(145,65,190),(235,235,235),(40,40,45)]
for i in range(8): traffic.append({'lane':random.choice([-1,0,1]),'z':random.uniform(.12,.95),'speed':random.uniform(75,170),'color':random.choice(colors)})
speed=distance=player_x=0.; paused=game_over=False
def reset():
 global speed,distance,player_x,game_over
 speed=distance=player_x=0.; game_over=False
 for t in traffic: t.update(lane=random.choice([-1,0,1]),z=random.uniform(.15,.95),speed=random.uniform(70,175))
def draw_world(offset):
 for y in range(H//2): pygame.draw.line(screen,(int(70+55*y/(H/2)),int(155+45*y/(H/2)),int(225+20*y/(H/2))),(0,y),(W,y))
 horizon=int(H*.46); cx=W//2+int(math.sin(offset*.0008)*120)
 pygame.draw.polygon(screen,(91,119,137),[(0,horizon+40),(150,horizon-20),(280,horizon+25),(430,horizon-35),(590,horizon+25),(750,horizon-25),(900,horizon+20),(1050,horizon-40),(W,horizon+35)])
 pygame.draw.rect(screen,GRASS,(0,horizon,W,H-horizon)); top=70; bot=ROAD_W
 pygame.draw.polygon(screen,ROAD,[(cx-top,horizon),(cx+top,horizon),(cx+bot,H),(cx-bot,H)])
 pygame.draw.line(screen,EDGE,(cx-top,horizon),(cx-bot,H),8); pygame.draw.line(screen,EDGE,(cx+top,horizon),(cx+bot,H),8)
 for lane in (-1,0,1):
  for i in range(18):
   z=((i*90+offset*1.5)%1600)/1600
   if .05<z<.97:
    y=horizon+(H-horizon)*z*z; x=cx+lane*(38+(ROAD_W/3-38)*z); pygame.draw.rect(screen,WHITE,(int(x-2.5*z),int(y),max(2,int(5*z)),max(8,int(48*z))))
 random.seed(12)
 for i in range(28):
  side=-1 if i%2==0 else 1; z=((i*177+offset*.45)%1800)/1800; y=horizon+(H-horizon)*z*z; x=cx+side*(190+430*z)
  if 0<x<W:
   s=max(.18,.9*z); pygame.draw.rect(screen,(91,60,35),(int(x-4*s),int(y),max(2,int(8*s)),max(3,int(35*s)))); pygame.draw.circle(screen,(35,112,52),(int(x),int(y-10*s)),max(3,int(24*s)))
def hud():
 p=pygame.Surface((300,120),pygame.SRCALPHA); p.fill((5,10,18,185)); screen.blit(p,(25,25)); screen.blit(big.render(f'{int(speed):03d} km/h',True,WHITE),(45,38)); screen.blit(small.render(f'DISTANCE  {distance/1000:06.1f} km',True,(190,210,230)),(47,84)); pygame.draw.rect(screen,(55,65,75),(47,103,245,8),border_radius=4); pygame.draw.rect(screen,YELLOW,(47,103,int(245*speed/MAX_SPEED),8),border_radius=4)
clock=pygame.time.Clock(); running=True
while running:
 dt=min(clock.tick(60)/1000,.035)
 for e in pygame.event.get():
  if e.type==pygame.QUIT: running=False
  elif e.type==pygame.VIDEORESIZE: W,H=e.w,e.h; screen=pygame.display.set_mode((W,H),pygame.RESIZABLE)
  elif e.type==pygame.KEYDOWN:
   if e.key==pygame.K_ESCAPE: running=False
   elif e.key==pygame.K_p: paused=not paused
   elif e.key==pygame.K_r: reset()
 keys=pygame.key.get_pressed()
 if not paused and not game_over:
  if keys[pygame.K_w] or keys[pygame.K_UP]: speed+=ACCEL*dt
  elif keys[pygame.K_s] or keys[pygame.K_DOWN]: speed-=BRAKE*dt
  else: speed-=DRAG*dt
  speed=clamp(speed,0,MAX_SPEED); steer=int(keys[pygame.K_d] or keys[pygame.K_RIGHT])-int(keys[pygame.K_a] or keys[pygame.K_LEFT]); player_x=clamp(player_x+steer*(.95+speed/MAX_SPEED)*dt,-1,1); distance+=speed*dt
  for t in traffic:
   t['z']+=(speed-t['speed'])*dt/180
   if t['z']>1.05: t.update(z=-.08,lane=random.choice([-1,0,1]),speed=random.uniform(70,175))
   if t['z']<-.15: t['z']=.95
   if .84<t['z']<.98 and abs(t['lane']-player_x)<.22: game_over=True
 draw_world(distance); horizon=int(H*.46); cx=W//2+int(math.sin(distance*.0008)*120)
 for t in sorted(traffic,key=lambda a:a['z']):
  z=clamp(t['z'],.05,1); y=horizon+(H-horizon)*z*z; x=cx+t['lane']*(70+(ROAD_W-70)*z); img=car_surface(t['color'],.22+.78*z); screen.blit(img,(int(x-img.get_width()/2),int(y-img.get_height()*.72)))
 px=cx+player_x*(ROAD_W*.32); screen.blit(player_img,(int(px-player_img.get_width()/2),H-150)); hud(); screen.blit(small.render('W/UP Accelerate   S/DOWN Brake   A/D Steer   P Pause   R Restart   ESC Exit',True,WHITE),(25,H-30))
 if paused or game_over:
  ov=pygame.Surface((W,H),pygame.SRCALPHA); ov.fill((0,0,0,150)); screen.blit(ov,(0,0)); title='PAUSED' if paused else 'CRASH!'; sub='Press P to continue' if paused else 'Press R to restart'; a=big.render(title,True,WHITE); b=font.render(sub,True,WHITE); screen.blit(a,(W//2-a.get_width()//2,H//2-40)); screen.blit(b,(W//2-b.get_width()//2,H//2+10))
 pygame.display.flip()
pygame.quit(); sys.exit()
