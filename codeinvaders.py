import pygame
import random
pygame.init()
screen = pygame.display.set_mode((640,530))
#game imports
playership=pygame.image.load("player.png")
background=pygame.image.load("bg.png")
destroy=pygame.image.load("enemy_explosion.png")
bolt=pygame.image.load("bullet.png")
obstacle=pygame.image.load("wall.png")
enemies=[]
enemies.append(pygame.image.load("5.png"))
enemies.append(pygame.image.load("4.png"))
enemies.append(pygame.image.load("3.png"))
enemies.append(pygame.image.load("2.png"))
enemies.append(pygame.image.load("1.png"))
explosion=pygame.mixer.Sound('explosion.wav')
enemyHit=pygame.mixer.Sound('enemyhit.wav')
bullet=pygame.mixer.Sound('bullet.wav')
bitfont=pygame.font.Font('PressStart2p.ttf',16)
introfont=pygame.font.Font('PressStart2p.ttf',36)
lowerfont=pygame.font.Font('PressStart2p.ttf',16)
endText=introfont.render("Game Over", 1, (255, 255, 255))
restart=lowerfont.render("Press Spacebar to retry", 1, (255, 255, 255))


#intro import

title = introfont.render("Code Invaders", 1, (255, 255, 255))
instruction = lowerfont.render("Press Spacebar to start", 1, (255, 255, 255))

class ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width=28
        self.height=27
        self.speed = 8
        self.immune = False
        self.lives=3
        self.dead=False
    def draw(self):
        if self.dead==0:
            screen.blit(playership, (self.x,self.y))
        else:
            screen.blit(destroy, (self.x,self.y))
class bullets:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.height=12
        self.speed=20
    def draw(self):
        screen.blit(bolt, (self.x,self.y))

class enemy:
    def __init__(self,x,y,dir,sprite):
        self.x=x
        self.y=y
        self.height=30
        self.width=40
        self.speed=0.1
        self.dir=dir
        self.dead=0
        self.sprite=sprite
    def movement(self):
        if self.dir == 1:
            if self.x < 590:
                self.x += self.speed
        elif self.dir == -1:
            if self.x > 10:
                self.x -= self.speed

    def draw(self):
        if self.dead==0:
            screen.blit(self.sprite, (self.x,self.y))
        else:
            screen.blit(destroy, (self.x,self.y))

class wall:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.height=50
        self.width=80
    def draw(self):
        screen.blit(obstacle, (self.x,self.y))

#initial game values
enemiesSpawned=False
wallsSpawned=False
enemyspawnX=50
enemyspawnY=60
wallspawnX=40
wallspawnY=400
respawnCounter=240
PlayerRespawn=180
respawnImmunity=240
bulletCount=[]
wallCount=[]
enemyCount=[]
enemyShots=[]
player=ship(295,470)
score=0
gameOver=False
MenuMusic=True
GameMusic=False
GameOverMusic=False

#frame-based animation counters
GameOverPositionY=0
RetryPositionY=530
introLoop=0
GameOverLoop=0
deathCounter=10

#intro/mainloop values
clock=pygame.time.Clock()
FPS=60
playtime=0.0
mainloop=True
game=0
introShown=False
introShip=ship(295,530)

while mainloop:
    scoretext = bitfont.render("Score:" + str(score), 1, (255, 255, 255))
    livestext = bitfont.render("Lives:" + str(player.lives), 1, (255, 255, 255))
    if game==0:
        if MenuMusic:
            pygame.mixer.music.load('introMusic.mp3')
            pygame.mixer.music.play(-1)
            MenuMusic=False
    elif game==1:
        #music handling
        if GameMusic:
            pygame.mixer.music.load('bgMusic.mp3')
            pygame.mixer.music.play(-1)
            GameMusic=False
        miliseconds = clock.tick(FPS)
        spriteSelector =0
        if not gameOver:
            if player.lives == 0:
                GameOverLoop=0
                GameOverPositionY = 0
                RetryPositionY = 530
                gameOver = True
                GameOverMusic=True
            if introShown:
                if not enemiesSpawned:
                    # spawning enemies
                    for i in range(1, 56):
                        if i % 11 != 0:
                            enemyCount.append(enemy((enemyspawnX), (enemyspawnY), 1, enemies[spriteSelector]))
                            enemyspawnX += 50
                        else:
                            enemyCount.append(enemy((enemyspawnX), (enemyspawnY), 1, enemies[spriteSelector]))
                            enemyspawnY += 43
                            enemyspawnX = 50
                            spriteSelector += 1
                    enemiesSpawned = True
                # wall spawning
                if not wallsSpawned:
                    for l in range(1, 5):
                        wallCount.append(wall((wallspawnX), (wallspawnY)))
                        wallspawnX += 160
                    wallsSpawned = True
                # enemy respawning
                if len(enemyCount) == 0:
                    if respawnCounter > 0:
                        respawnCounter -= 1
                    else:
                        enemiesSpawned = False
                        enemyspawnY = 60
                        respawnCounter = 240
                #changing enemy speed
                for i in enemyCount:
                    if i.y + i.height >= player.y:
                        gameOver=True
                    if len(enemyCount) < 40:
                        i.speed = 0.2
                    if len(enemyCount) < 30:
                        i.speed = 0.4
                    if len(enemyCount) < 20:
                        i.speed = 0.6
                    if len(enemyCount) < 15:
                        i.speed = 1
                    if len(enemyCount) < 10:
                        i.speed = 1.5
                    if len(enemyCount) < 5:
                        i.speed = 3
                    for round in bulletCount:
                        # collisions between bullets and enemies
                        if round.x >= i.x and round.x <= i.x + i.width:
                            if round.y >= i.y and round.y <= i.y + i.height:
                                i.dead = 1
                                bulletCount.pop(bulletCount.index(round))
                                enemyHit.play()
                                score += 100
                    # enemy shooting mechanics
                    if i.x >= player.x and i.x <= player.x + player.width and i.dead != 1:
                        rand = random.randint(1, 155)
                        if rand == 5 and len(enemyShots) < 1 and not player.immune:
                            enemyShots.append(bullets((i.x + 17.5), (i.y + 18)))
                    if not player.dead:
                        i.movement()
                    # changing enemy directions
                    if i.x >= 590:
                        for i in enemyCount:
                            i.dir = -1
                            i.y += 10
                    elif i.x <= 10:
                        for i in enemyCount:
                            i.dir = 1
                            i.y += 10
                # enemy bullet mechanics
                for i in enemyShots:
                    for l in wallCount:
                        if i.x >= l.x and i.x <= l.x + l.width:
                            if i.y + i.height >= l.y:
                                enemyShots.pop(enemyShots.index(i))
                for i in enemyShots:
                    i.speed = 8
                    if i.y < 530:
                        if i.x >= player.x and i.x <= player.x + player.width:
                            if i.y + i.height >= player.y and i.y + i.height <= player.y + player.height and not player.immune:
                                explosion.play()
                                player.dead = True
                                player.immune = True
                                enemyShots.pop(enemyShots.index(i))
                                player.lives -= 1
                            else:
                                i.y += i.speed
                        else:
                            i.y += i.speed
                    else:
                        enemyShots.pop(enemyShots.index(i))

                # player bullet mechanics
                for round in bulletCount:
                    for l in wallCount:
                        if round.x >= l.x and round.x <= l.x + l.width:
                            if round.y >= l.y:
                                bulletCount.pop(bulletCount.index(round))
                    if round.y > 90:
                        round.y -= round.speed
                    else:
                        bulletCount.pop(bulletCount.index(round))
    #player movement input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x>10 and not player.dead and introShown:
        player.x -= player.speed
    elif keys[pygame.K_RIGHT] and player.x<602 and not player.dead and introShown:
        player.x += player.speed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
            elif event.key == pygame.K_SPACE:
                if not player.dead and len(bulletCount)<1 and game==1 and introShown:
                    bulletCount.append(bullets((player.x+11.5), (player.y+12)))
                    bullet.play()
                elif game==0:
                    game=1
                    GameMusic=True
                elif gameOver:
                    enemyCount.clear()
                    enemyspawnX = 50
                    enemyspawnY = 60
                    bulletCount.clear()
                    score=0
                    player.lives=3
                    player.x=295
                    player.dead=False
                    introShown=False
                    enemiesSpawned=False
                    wallsSpawned=False
                    gameOver=False
                    GameMusic=True
    text = "Code Invaders"
    #drawing
    screen.blit(background,(0,0))
    if game==0:
        screen.blit(title, (90,150))
        screen.blit(instruction, (137,370))
    elif game==1:
        if gameOver:
            if GameOverMusic:
                pygame.mixer.music.load('GameOver.wav')
                pygame.mixer.music.play(0)
                GameOverMusic=False
            if GameOverLoop<120:
                screen.blit(endText, (158, GameOverPositionY))
                screen.blit(restart, (138, RetryPositionY))
                RetryPositionY-=0.8
                GameOverPositionY+=1.1
                GameOverLoop+=1
            screen.blit(endText, (158,GameOverPositionY))
            screen.blit(restart, (138,RetryPositionY))
        else:
            if introShown == False:
                player.immune = True
                if introLoop < 180:
                    introShip.draw()
                    introShip.y -= 0.3
                    introLoop += 1
                else:
                    introShip.draw()
                    introShip.y=530
                    introShown = True
                    introLoop=0
            else:
                for l in wallCount:
                    l.draw()
                for round in bulletCount:
                    round.draw()
                for i in enemyShots:
                    i.draw()
                for i in enemyCount:
                    if i.dead == 1:
                        if deathCounter > 0:
                            i.draw()
                            deathCounter -= 1
                        else:
                            i.draw()
                            enemyCount.pop(enemyCount.index(i))
                            deathCounter = 10
                    else:
                        i.draw()
                if player.dead:
                    player.immune = True
                    if PlayerRespawn > 0:
                        if PlayerRespawn > 150:
                            player.draw()
                        PlayerRespawn -= 1
                    else:
                        player.dead = False
                        PlayerRespawn = 180
                else:
                    player.draw()
                if player.immune:
                    if respawnImmunity > 0:
                        respawnImmunity -= 1
                    else:
                        player.immune = False
                        respawnImmunity = 240
                screen.blit(scoretext, (50, 25))
                screen.blit(livestext, (590 - livestext.get_width(), 25))
    pygame.display.set_caption(text)
    pygame.display.flip()
pygame.quit()