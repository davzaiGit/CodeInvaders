import pygame
import random

pygame.init()
screen = pygame.display.set_mode((640, 530))

class Resources:
    def __init__(self):
        
        # image loading

        self.playerShip = pygame.image.load("player.png")
        self.background = pygame.image.load("bg.png")
        self.destroy = pygame.image.load("enemy_explosion.png")
        self.bolt = pygame.image.load("bullet.png")
        self.obstacle = pygame.image.load("wall.png")

        self.enemies = []
        self.enemies.append(pygame.image.load("5.png"))
        self.enemies.append(pygame.image.load("4.png"))
        self.enemies.append(pygame.image.load("3.png"))
        self.enemies.append(pygame.image.load("2.png"))
        self.enemies.append(pygame.image.load("1.png"))

        # sound loading

        self.explosion = pygame.mixer.Sound('explosion.wav')
        self.enemyHit = pygame.mixer.Sound('enemyhit.wav')
        self.bullet = pygame.mixer.Sound('bullet.wav')

        # font inits

        self.bitFont = pygame.font.Font('PressStart2p.ttf', 16)
        self.introFont = pygame.font.Font('PressStart2p.ttf', 36)
        self.lowerFont = pygame.font.Font('PressStart2p.ttf', 16)
        self.endText = self.introFont.render("Game Over", True, (255, 255, 255))
        self.restart = self.lowerFont.render("Press Spacebar to retry", True, (255, 255, 255))
        self.title = self.introFont.render("Code Invaders", True, (255, 255, 255))
        self.instruction = self.lowerFont.render("Press Spacebar to start", True, (255, 255, 255))


class Values:
    def __init__(self):
        self.enemiesSpawned = False
        self.wallsSpawned = False
        self.enemySpawn = [50, 60]
        self.wallSpawn = [40, 400]

        self.bullets = []
        self.walls = []
        self.enemies = []
        self.enemyBullets = []
        self.player = Ship(295, 470)
        self.gameOverPositionY = 0
        self.retryPositionY = 530
        self.score = 0
        self.gameOver = False
        self.menuMusic = True
        self.gameMusic = False
        self.gameOverMusic = False

        # frame-based animation counters
        self.playerRespawnCounter = 180
        self.respawnImmunityCounter = 240
        self.respawnCounter = 240
        self.gameOverLoop = 0
        self.deathCounter = 10

        # intro/mainloop values
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.mainloop = True
        self.gameScreen = 0

    def reset(self):
        self.enemies.clear()
        self.enemySpawn = [50, 60]
        self.bullets.clear()
        self.score = 0
        self.player.lives = 3
        self.player.x = 295
        self.player.dead = False
        self.enemiesSpawned = False
        self.wallsSpawned = False
        self.gameOver = False
        self.gameMusic = True

    def drawGameOver(self):
        if self.gameOverMusic:
            pygame.mixer.music.load('GameOver.wav')
            pygame.mixer.music.play(0)
            self.gameOverMusic = False
        if self.gameOverLoop < 120:
            screen.blit(resources.endText, (158, self.gameOverPositionY))
            screen.blit(resources.restart, (138, self.retryPositionY))
            self.retryPositionY -= 0.8
            self.gameOverPositionY += 1.1
            self.gameOverLoop += 1
        screen.blit(resources.endText, (158, self.gameOverPositionY))
        screen.blit(resources.restart, (138, self.retryPositionY))


class Ship:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.width = 28
        self.height = 27
        self.speed = 8
        self.immune = True
        self.lives = 3
        self.dead = False

    def draw(self):
        if values.player.dead:
            values.player.immune = True
            if values.playerRespawnCounter > 0:
                if values.playerRespawnCounter > 150:
                    screen.blit(resources.destroy, (self.pos[0], self.pos[1]))
                values.playerRespawnCounter -= 1
            else:
                values.player.dead = False
                values.playerRespawnCounter = 180
        else:
            screen.blit(resources.playerShip, (self.pos[0], self.pos[1]))

    def immunity(self):
        if self.immune:
            if values.respawnImmunityCounter > 0:
                values.respawnImmunityCounter -= 1
            else:
                self.immune = False
                values.respawnImmunityCounter = 240

    def death(self):
        resources.explosion.play()
        self.dead = True
        self.immune = True
        self.lives -= 1


class Bullets:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.height = 12
        self.speed = 20
        self.enemySpeed = 8

    def draw(self):
        screen.blit(resources.bolt, (self.pos[0], self.pos[1]))


class Enemy:
    def __init__(self, x, y, direction, sprite):
        self.pos = [x, y]
        self.height = 30
        self.width = 40
        self.speed = 0.1
        self.dir = direction
        self.dead = False
        self.sprite = sprite

    def movement(self):
        if not values.player.dead:
            if self.dir == 1:
                if self.pos[0] < 590:
                    self.pos[0] += self.speed
            elif self.dir == -1:
                if self.pos[0] > 10:
                    self.pos[0] -= self.speed

    def draw(self):
        if not self.dead:
            screen.blit(self.sprite, (self.pos[0], self.pos[1]))
        else:
            if values.deathCounter > 0:
                screen.blit(resources.destroy, (self.pos[0], self.pos[1]))
                values.deathCounter -= 1
            else:
                screen.blit(resources.destroy, (self.pos[0], self.pos[1]))
                values.enemies.pop(values.enemies.index(enemy))
                values.deathCounter = 10

    def directionChange(self):
        if self.pos[0] >= 590:
            for i in values.enemies:
                i.dir = -1
                i.pos[1] += 10
        elif self.pos[0] <= 10:
            for i in values.enemies:
                i.dir = 1
                i.pos[1] += 10

    def speedChange(self):
        if self.pos[1] + self.height >= values.player.pos[1]:
            values.gameOver = True
        if len(values.enemies) < 40:
            self.speed = 0.2
        if len(values.enemies) < 30:
            self.speed = 0.4
        if len(values.enemies) < 20:
            self.speed = 0.6
        if len(values.enemies) < 15:
            self.speed = 1
        if len(values.enemies) < 10:
            self.speed = 1.5
        if len(values.enemies) < 5:
            self.speed = 3

    def shoot(self):
        if values.player.pos[0] <= enemy.pos[0] <= values.player.pos[0] + values.player.width and not enemy.dead:
            rand = random.randint(1, 155)
            if rand == 5 and len(values.enemyBullets) < 1 and not values.player.immune:
                values.enemyBullets.append(Bullets((enemy.pos[0] + 17.5), (enemy.pos[1] + 18)))


class Wall:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.height = 50
        self.width = 80

    def draw(self):
        screen.blit(resources.obstacle, (self.pos[0], self.pos[1]))


# initial game values

resources = Resources()
values = Values()

while values.mainloop:
    scoreText = resources.bitFont.render("Score:" + str(values.score), True, (255, 255, 255))
    livesText = resources.bitFont.render("Lives:" + str(values.player.lives), True, (255, 255, 255))
    if values.gameScreen == 1:
        # music handling
        if values.gameMusic:
            pygame.mixer.music.load('bgMusic.wav')
            pygame.mixer.music.play(-1)
            values.gameMusic = False
        if not values.gameOver:
            if values.player.lives == 0:
                values.gameOverLoop = 0
                values.gameOverPositionY = 0
                values.retryPositionY = 530
                values.gameOver = True
                values.gameOverMusic = True
    if not values.enemiesSpawned:
        # spawning enemies
        for enemy in range(1, 56):
            if enemy % 11 != 0:
                values.enemies.append(
                    Enemy(values.enemySpawn[0], values.enemySpawn[1], 1, resources.enemies[enemy % 5]))
                values.enemySpawn[0] += 50
            else:
                values.enemies.append(
                    Enemy(values.enemySpawn[0], values.enemySpawn[1], 1, resources.enemies[enemy % 5]))
                values.enemySpawn[0] = 50
                values.enemySpawn[1] += 43
        values.enemiesSpawned = True
    # wall spawning
    if not values.wallsSpawned:
        for wall in range(1, 5):
            values.walls.append(Wall(values.wallSpawn[0], values.wallSpawn[1]))
            values.wallSpawn[0] += 160
        wallsSpawned = True
    # enemy respawning
    if len(values.enemies) == 0:
        if values.respawnCounter > 0:
            values.respawnCounter -= 1
        else:
            values.enemiesSpawned = False
            values.enemySpawn[1] = 60
            values.respawnCounter = 240
    # changing enemy speed
    for enemy in values.enemies:
        enemy.movement()
        enemy.speedChange()
        enemy.shoot()
        enemy.directionChange()
    # enemy bullet mechanics
    for enemyBullet in values.enemyBullets:
        if enemyBullet.pos[1] < 530:
            for wall in values.walls:
                if wall.pos[0] <= enemyBullet.pos[0] <= wall.pos[0] + wall.width:
                    if enemyBullet.pos[1] + enemyBullet.height >= wall.pos[1]:
                        values.enemyBullets.pop(values.enemyBullets.index(enemyBullet))
            if values.player.pos[0] <= enemyBullet.pos[0] <= values.player.pos[0] + values.player.width:
                if values.player.pos[1] <= enemyBullet.pos[1] + enemyBullet.height <= \
                        values.player.pos[1] + values.player.height and not values.player.immune:
                    values.player.death()
                    values.enemyBullets.pop(values.enemyBullets.index(enemyBullet))

                else:
                    enemyBullet.pos[1] += enemyBullet.enemySpeed
            else:
                enemyBullet.pos[1] += enemyBullet.enemySpeed
        else:
            values.enemyBullets.pop(values.enemyBullets.index(enemyBullet))

    # player bullet mechanics
    for bullet in values.bullets:
        if bullet.pos[1] > 90:
            bullet.pos[1] -= bullet.speed
        else:
            values.bullets.pop(values.bullets.index(bullet))
        for wall in values.walls:
            if wall.pos[0] <= bullet.pos[0] <= wall.pos[0] + wall.width:
                if bullet.pos[1] >= wall.pos[1]:
                    values.bullets.pop(values.bullets.index(bullet))
        for enemy in values.enemies:
            if enemy.pos[0] <= bullet.pos[0] <= enemy.pos[0] + enemy.width:
                if enemy.pos[1] <= bullet.pos[1] <= enemy.pos[1] + enemy.height:
                    enemy.dead = True
                    values.bullets.pop(values.bullets.index(bullet))
                    resources.enemyHit.play()
                    values.score += 100

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and values.player.pos[0]>10 and not values.player.dead:
        values.player.pos[0] -= values.player.speed
    elif keys[pygame.K_RIGHT] and values.player.pos[0] <602 and not values.player.dead:
        values.player.pos[0] += values.player.speed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            values.mainloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                values.mainloop = False
            elif event.key == pygame.K_SPACE:
                if not values.player.dead and len(values.bullets) < 1 and values.gameScreen == 1:
                    values.bullets.append(Bullets((values.player.pos[0] + 11.5), (values.player.pos[1] + 12)))
                    resources.bullet.play()
                elif values.gameScreen == 0:
                    values.gameScreen = 1
                    values.gameMusic = True
                    values.player.immune = False
                elif values.gameOver:
                    values.reset()

    # drawing
    screen.blit(resources.background, (0, 0))
    if values.gameScreen == 0:
        screen.blit(resources.title, (90, 150))
        screen.blit(resources.instruction, (137, 370))
    elif values.gameScreen == 1:
        if values.gameOver:
            values.drawGameOver()
        else:
            for wall in values.walls:
                wall.draw()
            for bullet in values.bullets:
                bullet.draw()
            for enemyBullet in values.enemyBullets:
                enemyBullet.draw()
            for enemy in values.enemies:
                enemy.draw()
            values.player.draw()
            values.player.immunity()
            screen.blit(scoreText, (50, 25))
            screen.blit(livesText, (590 - livesText.get_width(), 25))
    text = "Code Invaders"
    pygame.display.set_caption(text)
    pygame.display.flip()
pygame.quit()
