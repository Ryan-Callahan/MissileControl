"""
    #todo add text here (program v.0.0.0)
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

    def reticlemove(self,x,y):
        self.rect.x = (x-(self.rect.width/2))
        self.rect.y = (y-(self.rect.height/2))


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

    def update(self):

        self.rect.move_ip(self.x_change, self.y_change)
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
        self.xpath = math.sqrt(self.endx**2 + self.x**2)
        self.ypath = math.sqrt(self.endy**2 + self.y**2)
        self.hypotenuse = math.sqrt(((self.endx**2)+(self.endy**2)))
        self.angle = math.degrees(math.atan((self.ypath/self.xpath)))
        if self.endx < self.x:
            self.angle += 180
        print(self.angle)

    def update(self):
        vel_x = self.speed * math.cos(self.angle)
        vel_y = self.speed * math.sin(self.angle)

        self.x_pos += vel_x
        self.rect.move_ip(vel_x, vel_y)
        screen.blit(self.sprite, (self.rect.x, self.rect.y))

class Base(Entity):

    def __init__(self, x, y, height, width, base_sprite, rocket_sprite):
        super(Base, self).__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite = base_sprite
        self.rocketsprite = rocket_sprite

    def generate_rockets(self):
            rocket = Rocket(((self.rect.x + (self.rect.width/2)) - self.rocketsprite.get_width()/2), self.rect.y + 2, self.rocketsprite.get_height(), self.rocketsprite.get_width(), self.rocketsprite)
            all_sprites_list.add(rocket)
            for x in range(0,2):
                rocket = Rocket(((self.rect.x + (self.rect.width / 2)) - (x*self.rocketsprite.get_width())),
                                self.rect.y + 6, self.rocketsprite.get_height(), self.rocketsprite.get_width(),
                                self.rocketsprite)
                all_sprites_list.add(rocket)
            for x in range(0,3):
                rocket = Rocket(((self.rect.x + (self.rect.width / 2)) - self.rocketsprite.get_width()/2 - self.rocketsprite.get_width() + (x*self.rocketsprite.get_width())),
                                self.rect.y + 10, self.rocketsprite.get_height(), self.rocketsprite.get_width(),
                                self.rocketsprite)
                all_sprites_list.add(rocket)
            for x in range(0,4):
                rocket = Rocket(((self.rect.x + (self.rect.width / 2)) + self.rocketsprite.get_width() - (x*self.rocketsprite.get_width())),
                                self.rect.y + 14, self.rocketsprite.get_height(), self.rocketsprite.get_width(),
                                self.rocketsprite)
                all_sprites_list.add(rocket)

    def update(self):

        screen.blit(self.sprite, (self.rect.x, self.rect.y))


def reset():

    for rocket in all_sprites_list:
        all_sprites_list.remove(rocket)

    for enemy in all_sprites_list:
        all_sprites_list.remove(enemy)

    for base in all_sprites_list:
        all_sprites_list.remove(base)

    base1 = Base(0, (window_height - groundsprite.get_height() - basesprite.get_height()), basesprite.get_height(),
                 basesprite.get_width(), basesprite, rocketsprite)
    all_sprites_list.add(base1)
    base1.generate_rockets()

    base2 = Base(((window_width/2)-(basesprite.get_width()/2)),
                 (window_height - groundsprite.get_height() - basesprite.get_height()), basesprite.get_height(),
                 basesprite.get_width(), basesprite, rocketsprite)
    all_sprites_list.add(base2)
    base2.generate_rockets()

    base3 = Base((window_width-basesprite.get_width()), (window_height - groundsprite.get_height() - basesprite.get_height()), basesprite.get_height(),
                 basesprite.get_width(), basesprite, rocketsprite)
    all_sprites_list.add(base3)
    base3.generate_rockets()







pygame.init()

pygame.mouse.set_visible(False)

groundsprite = pygame.image.load("hill.png")
basesprite = pygame.image.load("base.png")
reticlesprite = pygame.image.load("reticle.png")
enemysprite = pygame.image.load("enemy.png")
rocketsprite = pygame.image.load("rocket.png")



window_width = 700
window_height = 800

reticle = Reticle(100,100, reticlesprite.get_height(),reticlesprite.get_width(),reticlesprite)

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Missile Control")

clock = pygame.time.Clock()

all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(reticle)

"""
for x in range(0,10):
    rocket = Rocket((100 + (20*x)), 200, rocketsprite.get_height(), rocketsprite.get_width(), rocketsprite)
    all_sprites_list.add(rocket)
"""

enemies = 10


enemy_spawn_rate = 4000

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
            pass
        elif event.type == pygame.USEREVENT + 1:
            if enemies != 0:
                if firstwave == True:
                    wave = random.randint(3, (enemies/2))
                    for x in range(0,wave):
                        enemyx = random.randint(0, (window_width - enemysprite.get_width()))
                        enemy = Enemy(enemyx, 10, enemysprite.get_height(), enemysprite.get_width(), enemysprite, (200,250))
                        all_sprites_list.add(enemy)
                    pygame.time.set_timer(pygame.USEREVENT + 1, 5000)
                    firstwave = False
                    enemies -= wave
                else:
                    enemyx = random.randint(0, window_width)
                    enemy = Enemy(enemyx, 10, enemysprite.get_height(), enemysprite.get_width(), enemysprite, (200,250))
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