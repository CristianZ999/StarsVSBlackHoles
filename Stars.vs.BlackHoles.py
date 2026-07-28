import pygame
import math, random

pygame.init()

WIDTH, HEIGHT = (728, 400)
sight = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Stars vs Black Holes")

bg = pygame.image.load('Fabulous.jpg')
char = pygame.image.load('ChampionNeo.jpg')
clock = pygame.time.Clock()
bulletSound = pygame.mixer.Sound("Pew.mp3")
hitSound = pygame.mixer.Sound("ExplosiveHit.mp3")
# music = pygame.mixer.music.load('funnyfight.mp3')
# pygame.mixer.music.play(-1)

score = 0


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.image = char
        self.hitbox = self.image.get_rect(topleft=(x, y))

    def draw(self, win):
        win.blit(char, (self.x, self.y))
        self.hitbox = self.image.get_rect(topleft=(self.x, self.y))


class projectile(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('Rainbow.jpg')
        self.vel = 10
        self.hitbox = self.image.get_rect(topleft=(x, y))
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - self.x, my - self.y
        len = math.hypot(dx, dy)
        self.dx = dx / len
        self.dy = dy / len

    def move(self):
        self.x += self.dx * self.vel
        self.y += self.dy * self.vel

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
        self.hitbox = self.image.get_rect(topleft=(self.x, self.y))


class Enemy(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.done = False
        self.vel = 3
        self.image = pygame.image.load('EnemySmal.jpg')
        self.hitbox = self.image.get_rect(topleft=(x, y))

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
        self.hitbox = self.image.get_rect(topleft=(self.x, self.y))

    def move(self):
        self.x -= 1


def redrawGameWindow():
    sight.blit(bg, (0, 0))
    man.draw(sight)
    for bullet in bullets:
        bullet.draw(sight)
    for enemy in enemies:
        enemy.draw(sight)
    text = font.render('Score: ' + str(score), 5, (255, 0, 0))
    sight.blit(text, (390, 10))
    pygame.display.update()


man = player(100, 200, 64, 64)
bullets = []
enemies = []
run = True
rate_of_fire = 0
font = pygame.font.SysFont('georgia', 30, True)

while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if rate_of_fire > 0:
        rate_of_fire += 0.1
    if rate_of_fire > 2:
        rate_of_fire = 0

    for bullet in bullets:
        if 0 < bullet.x < WIDTH and 0 < bullet.y < HEIGHT:
            bullet.move()
        else:
            bullets.pop(bullets.index(bullet))

    for enemy in enemies:
        if 0 < enemy.x < WIDTH and 0 < enemy.y < HEIGHT and enemy.done == False:
            enemy.move()
        else:
            enemies.pop(enemies.index(enemy))

    for enemy in enemies:
        if man.hitbox.colliderect(enemy.hitbox):
            score += 1
            hitSound.play()
            enemies.pop(enemies.index(enemy))
        else:
            for bullet in bullets:
                if bullet.hitbox.colliderect(enemy.hitbox):
                    hitSound.play()
                    score += 1
                    enemies.pop(enemies.index(enemy))
                    # bullets.pop(bullets.index(bullet))

    if len(enemies) <= 5:
        enemies.append(Enemy(WIDTH - 1, random.randint(1, HEIGHT - 1)))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel

    elif keys[pygame.K_RIGHT] and man.x < WIDTH - man.width - man.vel:
        man.x += man.vel

    elif keys[pygame.K_UP] and man.y > man.vel:
        man.y -= man.vel

    elif keys[pygame.K_DOWN] and man.y < HEIGHT - man.height - man.vel:
        man.y += man.vel

    elif event.type == pygame.MOUSEBUTTONDOWN and rate_of_fire == 0:

        if len(bullets) <= 500:
            bullets.append(projectile(man.x, man.y))
            bulletSound.play()

        rate_of_fire = 1

    redrawGameWindow()

pygame.quit()
