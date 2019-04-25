"""
    #MissileControl (program v.0.4.2)
    Copyright (C) 2018  Ryan I Callahan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import pygame, sys
import random
import math
from pygame.locals import *

firstwave = True

tick = 80

groundsprite = pygame.image.load("hill.png")
basesprite = pygame.image.load("base.png")
reticlesprite = pygame.image.load("reticle.png")
enemysprite = pygame.image.load("enemy.png")
rocketsprite = pygame.image.load("rocket.png")

window_width = 700
window_height = 800

all_sprites_list = pygame.sprite.Group()

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Missile Control")

clock = pygame.time.Clock()


enemy_spawn_rate = 4000

enemies = 10

class Entity(pygame.sprite.Sprite):
    """Inherited by any object in the game."""

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # This makes a rectangle around the entity, used for anything
        # from collision to moving around.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Rocket(Entity):

    def __init__(self, x, y, height, width, rocket_sprite):
        super(Rocket, self).__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.y_change = 0
        self.x_change = 0
        self.sprite = rocket_sprite
        self.speed = 0
        self.shot = False

    def shoot(self, endpoint):
        self.endx, self.endy = endpoint
        self.endx -= (self.sprite.get_width()/2)

        self.pos_x = self.rect.x
        self.pos_y = self.rect.y

        vectorx = self.endx - self.rect.x
        vectory = self.endy - self.rect.y
        self.path = math.sqrt(vectorx ** 2 + vectory ** 2)
        self.angle = math.degrees(math.atan((vectory / vectorx)))
        if self.endx < self.x:
            self.angle += 180
        self.recty = self.rect.y
        self.rectx = self.rect.x
        self.speed = 10
        self.shot = True

    def explode(self):
        pass
    #todo Add explosion either with a sprite or a circle object

    def update(self):
        if self.shot == True:
            if self.rect.y <= self.endy:
                screen.blit(self.sprite, (int(self.rectx), int(self.recty)))
                self.explode()
            else:
                vel_x = self.speed * math.cos(math.radians(self.angle))
                vel_y = self.speed * math.sin(math.radians(self.angle))

                self.rectx += float(vel_x)
                self.recty += float(vel_y)
                self.rect.x = self.rectx
                self.rect.y = self.recty
                screen.blit(self.sprite, (int(self.rectx), int(self.recty)))

        else:
            screen.blit(self.sprite, (self.rect.x, self.rect.y))


class Enemy(Entity):

    def __init__(self, x, y, height, width, enemy_sprite, endpoint):
        super(Enemy, self).__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.y_change = 1
        self.x_change = 1
        self.speed = 1
        self.sprite = enemy_sprite
        self.endx, self.endy = endpoint

        self.pos_x = self.rect.x
        self.pos_y = self.rect.y

        vectorx = self.endx - self.rect.x
        vectory = self.endy - self.rect.y
        self.path = math.sqrt(vectorx**2 + vectory**2)
        self.angle = math.degrees(math.atan((vectory/vectorx)))
        if self.endx < self.x:
            self.angle += 180
        self.recty = self.rect.y
        self.rectx = self.rect.x


    def update(self):
        if self.rect.y >= self.endy:
            all_sprites_list.remove(self)
        else:
            vel_x = self.speed * math.cos(math.radians(self.angle))
            vel_y = self.speed * math.sin(math.radians(self.angle))

            self.rectx += float(vel_x)
            self.recty += float(vel_y)
            self.rect.x = self.rectx
            self.rect.y = self.recty
            screen.blit(self.sprite, (int(self.rectx), int(self.recty)))

class Base(Entity):

    def __init__(self, x, y, height, width, base_sprite, rocket_sprite):
        super(Base, self).__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite = base_sprite
        self.rocketsprite = rocket_sprite
        self.rocket_list = []

    def generate_rockets(self):
            rocket = Rocket(((self.rect.x + (self.rect.width/2)) - self.rocketsprite.get_width()/2), self.rect.y + 2, self.rocketsprite.get_height(), self.rocketsprite.get_width(), self.rocketsprite)
            all_sprites_list.add(rocket)
            for x in range(0,2):
                rocket = Rocket(((self.rect.x + (self.rect.width / 2)) - (x*self.rocketsprite.get_width())),
                                self.rect.y + 6, self.rocketsprite.get_height(), self.rocketsprite.get_width(),
                                self.rocketsprite)
                self.rocket_list.append(rocket)
                all_sprites_list.add(rocket)
            for x in range(0,3):
                rocket = Rocket(((self.rect.x + (self.rect.width / 2)) - self.rocketsprite.get_width()/2 - self.rocketsprite.get_width() + (x*self.rocketsprite.get_width())),
                                self.rect.y + 10, self.rocketsprite.get_height(), self.rocketsprite.get_width(),
                                self.rocketsprite)
                self.rocket_list.append(rocket)
                all_sprites_list.add(rocket)
            for x in range(0,4):
                rocket = Rocket(((self.rect.x + (self.rect.width / 2)) + self.rocketsprite.get_width() - (x*self.rocketsprite.get_width())),
                                self.rect.y + 14, self.rocketsprite.get_height(), self.rocketsprite.get_width(),
                                self.rocketsprite)
                self.rocket_list.append(rocket)
                all_sprites_list.add(rocket)
            print(self.rocket_list)

    def fire_rocket(self, x, endpoint):
        global basesprite
        rocket = Rocket(((self.rect.x + (self.rect.width / 2)) - (x*self.rocketsprite.get_width())),
                            self.rect.y + 6, self.rocketsprite.get_height(), self.rocketsprite.get_width(),
                            self.rocketsprite)
        all_sprites_list.add(rocket)
        rocket.shoot(endpoint)
        print("fire rcket", x)

    def update(self):

        screen.blit(self.sprite, (self.rect.x, self.rect.y))


base1 = Base(0, (window_height - groundsprite.get_height() - basesprite.get_height()), basesprite.get_height(),
                 basesprite.get_width(), basesprite, rocketsprite)
all_sprites_list.add(base1)

base2 = Base(((window_width / 2) - (basesprite.get_width() / 2)),
             (window_height - groundsprite.get_height() - basesprite.get_height()), basesprite.get_height(),
             basesprite.get_width(), basesprite, rocketsprite)
all_sprites_list.add(base2)

base3 = Base((window_width - basesprite.get_width()),
             (window_height - groundsprite.get_height() - basesprite.get_height()), basesprite.get_height(),
             basesprite.get_width(), basesprite, rocketsprite)
all_sprites_list.add(base3)

class Reticle(Entity):

    def __init__(self, x, y, height, width, reticle_sprite):
        super(Reticle, self).__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite = reticle_sprite

    def update(self):
        """
        Moves the Reticle
        """
        # Moves it relative to its current location.
        screen.blit(self.sprite, (self.rect.x, self.rect.y))

        # If the paddle moves off the screen, put it back on.
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > window_height - self.height:
            self.rect.y = window_height - self.height

    def click(self, clickspot):
        global window_width
        mx, my = clickspot
        if mx <= (window_width/3):
            base1.fire_rocket(1, clickspot)
        if mx >= (window_width/3) and mx <= (2*window_width/3):
            base2.fire_rocket(2, clickspot)
        if mx >= (2*window_width/3):
            base3.fire_rocket(3, clickspot)


    def reticlemove(self,x,y):
        self.rect.x = (x-(self.rect.width/2))
        self.rect.y = (y-(self.rect.height/2))


def reset():

    for rocket in all_sprites_list:
        all_sprites_list.remove(rocket)

    for enemy in all_sprites_list:
        all_sprites_list.remove(enemy)

    for base in all_sprites_list:
        all_sprites_list.remove(base)

    all_sprites_list.add(base1)
    base1.generate_rockets()

    all_sprites_list.add(base2)
    base2.generate_rockets()

    all_sprites_list.add(base3)
    base3.generate_rockets()




pygame.init()

pygame.mouse.set_visible(False)


reticle = Reticle(100,100, reticlesprite.get_height(),reticlesprite.get_width(),reticlesprite)
all_sprites_list.add(reticle)


"""
for x in range(0,10):
    rocket = Rocket((100 + (20*x)), 200, rocketsprite.get_height(), rocketsprite.get_width(), rocketsprite)
    all_sprites_list.add(rocket)
"""



pygame.time.set_timer(pygame.USEREVENT +1, 1000)

reset()

while True:
    #Ensures reticle appears over everything else
    all_sprites_list.remove(reticle)

    screen.fill((0,0,0))
    screen.blit(groundsprite, (0,(window_height-groundsprite.get_height())))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
            reticle.reticlemove(mousex, mousey)
        elif event.type == MOUSEBUTTONDOWN:
            reticle.click(pygame.mouse.get_pos())
        elif event.type == pygame.USEREVENT + 1:
            if enemies != 0:
                if firstwave == True:
                    wave = random.randint(3, (enemies/2))
                    for x in range(0,wave):
                        enemyx = random.randint(0, (window_width - enemysprite.get_width()))
                        endx = random.randint(0, window_width)
                        enemy = Enemy(enemyx, 10, enemysprite.get_height(), enemysprite.get_width(), enemysprite, (endx
                                                                                                                   , 800))
                        all_sprites_list.add(enemy)
                    pygame.time.set_timer(pygame.USEREVENT + 1, 5000)
                    firstwave = False
                    enemies -= wave
                else:
                    enemyx = random.randint(0, window_width)
                    endx = random.randint(0, window_width)
                    enemy = Enemy(enemyx, 10, enemysprite.get_height(), enemysprite.get_width(), enemysprite, (endx, 800))
                    all_sprites_list.add(enemy)
                    enemies -= 1
                    pygame.time.set_timer(pygame.USEREVENT + 1, 5000)
            else:
                print("no more enemies")

    #Ensures reticle appears over everything else
    all_sprites_list.add(reticle)

    all_sprites_list.update()
    pygame.display.update()
    clock.tick(tick)