
import time as timer
from pygame import *
from random import *
window = display.set_mode (( 700, 500 ))
display.set_caption ( 'Шутер' )
win_height = 500
win_width = 700
background = transform.scale ( image.load ( 'galaxy.jpg' ), ( win_width, win_height ) )
clock = time.Clock()
FPS = 60
won = 0
lost =  0
game = True
finish = False


mixer.init()
mixer.music.load ( 'space.ogg' )
mixer.music.set_volume(0.5)
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

class GameSprite( sprite.Sprite ):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 25, 40, -5)
        bullets.add(bullet)
    
        
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


time_fire = 0
rel_time = False
num_fire = 0
img_bullet = 'bullet.png'
img_enemy = 'ufo.png'
img_asteroid = 'asteroid.png'
num_monster = 5
num_asteroid = 2
num_bullet = 3
asteroids = sprite.Group()
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(1, num_monster):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, num_monster))
    monsters.add(monster)


for i in range(1, num_asteroid):
    asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, num_asteroid))
    asteroids.add(asteroid)

font.init()
font1 = font.SysFont('Arial', 36)
font = font.SysFont('Arial', 70)
reloading = font1.render('reloading...', 1, (0, 250, 200))

player = Player('rocket.png', 5, win_height -100, 80, 100, 10)


while game:
    window.blit ( background, ( 0, 0 ) )
    player.reset()
    player.update()
    text_lose = font1.render('Пропущено'+ str(lost), 1, (0, 250, 200))
    text_won = font1.render('Сбито'+ str(won), 1, (0, 250, 200))
    window.blit(text_lose, (20, 20))
    window.blit(text_won, (20, 60))
    monsters.update()
    monsters.draw(window)
    bullets.update()
    bullets.draw(window)
    asteroids.update()
    asteroids.draw(window)

    collides = sprite.groupcollide(monsters, bullets, True, True )
    collides1 = sprite.groupcollide(asteroids, bullets, False, True )
    for c in collides:
        won += 1
        monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, num_monster))
        monsters.add(monster)
        asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, num_asteroid))
        asteroids.add(asteroid)
    


    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
    
                if num_fire < 5 and rel_time == False:
                    player.fire()
                    fire_sound.play()
                    num_fire += 1
                elif num_fire >= 5 and rel_time == False:
                    rel_time = True
                    time_fire = timer.time()

    if rel_time == True:
        now_time = timer.time()    
        if now_time - time_fire < 3:
            pass
        else:
            num_fire = 0
            rel_time = False
            

 

                
            
    if lost >= 10 or sprite.spritecollide(player, asteroids, False) or sprite.spritecollide(player, monsters, False):
        LOSE = font1.render('You lose!', True, (255, 200, 200))
        window.blit(LOSE,(200, 200))
        game = False
    elif won >= 8:
        WON  = font.render('You won!' , True, (250, 205, 250))
        window.blit(WON, (200, 200))
        game = False
    
    display.update()
    clock.tick( FPS )

timer.sleep(2)