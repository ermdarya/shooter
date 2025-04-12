from time import time as timer
from pygame import *
from random import *

window = display.set_mode((700,500))
display.set_caption('SHOOTER')
background = transform.scale(image.load('galaxy.jpg'),(700,500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.2)
mixer.music.play()
font.init()
font1 = font.SysFont('Arial',15)
font2 = font.SysFont('Arial',30)
win = font2.render('YOU WIN',True,(0,255,0))
lose = font2.render('YOU LOSE',True,(255,0,0))
wait = font2.render('Wait, reload..',True,(150,0,0))
fire_sound = mixer.Sound('fire.ogg')


class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,w,h,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect))


class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x>5 :
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x <595:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15,20,15)
        bulls.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y<0:
            self.kill()
    
        
            

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80,700-80)
            lost +=1

bulls = sprite.Group()
monsters = sprite.Group()
aster = sprite.Group()
for i in range(7):
    monster = Enemy('ufo.png',randint(80,620),-50,80,80,randint(1,2))     
    monsters.add(monster) 
for i in range(3):
    asteroid = Enemy('asteroid.png',randint(80,620),-50,80,80,randint(1,2))
    aster.add(asteroid)


ship = Player('rocket.png',50,400,80,100,5)
lost=0
score =0
game = True
finish = False
score1 = 0
RESTART_DELAY = 3

num_fire =0
real_time = False

while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        if i.type == KEYDOWN:
            if i.key == K_SPACE:
                if num_fire < 5 and real_time==False:
                    fire_sound.play()
                    ship.fire()
                    num_fire+=1
                if num_fire>=5 and real_time == False:
                    last_time = timer()
                    real_time=True


            

    if not finish:
        window.blit(background,(0,0))
        if real_time == True:
            now_time = timer()
            if now_time- last_time<3:
                window.blit(wait,(250,400))
            else:
                num_fire=0
                real_time=False

        
        ship.reset()
        ship.update()
        monsters.draw(window)
        monsters.update()   
        bulls.draw(window)
        bulls.update()
        aster.draw(window)
        aster.update()
        textlost=font1.render('пропущено: '+str(lost),True,(250,250,250))
        window.blit(textlost,(600,30))
        textlost1=font1.render('очки:'+str(score),True,(250,250,250))
        window.blit(textlost1,(600,60))

        if sprite.groupcollide(monsters,bulls,True,True):
            score +=1
            monster = Enemy('ufo.png',randint(80,620),-50,80,80,randint(1,2))
            monsters.add(monster)
        if score >9:
            finish = True
            window.blit(win,(270,250))
        if sprite.spritecollide(ship,monsters,False) or sprite.spritecollide(ship,aster,False):
            finish=True
            window.blit(lose,(270,250))
        
    else: 

        time.delay(RESTART_DELAY*1000 )  
        num_fire=0
        real_time=False
        monsters.empty()
        aster.empty()
        for i in range(7):
            monster = Enemy('ufo.png', randint(80, 620), -50, 80, 80, randint(1, 3))
            monsters.add(monster)
        for i in range(3):
            asteroid = Enemy('asteroid.png',randint(80,620),-50,80,80,randint(1,2))
            aster.add(asteroid)

        ship = Player('rocket.png', 50, 400, 80, 100, 5)
        bulls = sprite.Group()
        lost = 0
        score = 0
        score1 = 0
        finish = False
    time.delay(10)
    display.update()
