import pygame
from getSpritesheets import enemySpritesheet, goblinSpritesheet
import math
import random
from collider import Collider
from hjælpeFunktioner import read_csv,rectCollisionChecker, checkNearbyTiles
from farm import Farm, Plant
from player import Player
import time
from entityCollider import EntityCollider

class Enemy(EntityCollider):
    def __init__(self, main, player, name, map_width, map_height, xOffset, yOffset, width, height, health, damage, speed,collisionMap,scanArea):
        super().__init__(main=main, speed=speed, collisionMap=collisionMap, x=random.randint(0, map_width), y=random.randint(0, map_height), xOffset=xOffset, yOffset=yOffset, width=width, height=height, scanArea=scanArea)
        self.name = name
        self.max_health = health
        self.health = health
        self.damage = damage
        self.player = player
        self.hitbox = (self.xOffset + 17, self.yOffset + 2, 31, 57)
        self.visible = True
        self.dead = False

        self.Enemy_img = enemySpritesheet.parse_sprite("kylling0.png")  # giver udsnit af sprite0 fra json fil
        self.Enemy_img = pygame.transform.scale_by(self.Enemy_img, self.main.scale)
        self.Enemy_rect = self.Enemy_img.get_rect()  # giver bredde og højde af enemy

        self.attack_range = 50
        self.attack_cooldown = 1.0
        self.last_attack_time = 0



    def draw_enemy(self, canvas):
        if not self.dead:
            self.Enemy_rect.x = self.x + self.xOffset
            self.Enemy_rect.y = self.y + self.yOffset
            canvas.blit(self.Enemy_img, self.Enemy_rect)

            healthbar_width = 50
            healthbar_height = 10

            enemy_center_x = self.x + self.xOffset + self.width / 2

            healthbar_x = enemy_center_x - healthbar_width / 2

            #Beregner healthbaren
            health_width = (self.health / self.max_health) * healthbar_width

            # Tegner den grønne
            pygame.draw.rect(canvas, (0, 128, 0), (healthbar_x, self.y - 20, health_width, healthbar_height))

            self.hitbox = (self.x + 17, self.y + 4, self.width, self.height)

    def hit(self, damage):
        if self.health > 0:
            self.health -= damage
            if self.health <= 0:
                self.main.money += 10
                self.dead = True
                self.visible = False
                self.main.enemies.remove(self)

    def update(self):
        if self.player.respawning:
            return
        if self.dead:
            return

        distancefromplayer = math.sqrt((self.player.y - self.y) ** 2 + (self.player.x - self.x) ** 2)
        nearest_target = self.player
        min_distance = distancefromplayer

        # Tjek afstanden til hver plante
        for plant in self.main.plants:
            distance = math.sqrt((plant.y - self.y) ** 2 + (plant.x - self.x) ** 2)
            if distance < min_distance:
                min_distance = distance
                nearest_target = plant

        # Hvis fjenden er inden for angrebsafstand, angreb målet
        if min_distance <= self.attack_range:
            current_time = time.time()
            if current_time - self.last_attack_time >= self.attack_cooldown:
                self.attack(nearest_target)
                self.last_attack_time = current_time
            return

        # Beregn retningen til målet (player eller farm)
        angletotarget = math.atan2(nearest_target.y - self.y, nearest_target.x - self.x)

        xObstructed, yObstructed = self.checkCollision()
        self.xVel = math.cos(angletotarget) * self.speed
        self.yVel = math.sin(angletotarget) * self.speed

        if not xObstructed:
            self.x += self.xVel
        if not yObstructed:
            self.y += self.yVel

    def sværhed(self, wave_number):
        if self.main.wave_number > 1:
            self.max_health += wave_number * 1.5
            self.health = self.max_health

    def attack(self, target):
        if self.player.respawning:
            return
        if isinstance(target, Player):
            target.hit(self.damage)
        elif isinstance(target, Plant):
            target.hit(self.damage)


class Sprinter(Enemy):
    def __init__(self, main, player, map_width, map_height, collisionMap):
        super().__init__(main, player, "Sprinter", map_width, map_height, 3, 2, 10, 10, 20, 5, 1, collisionMap, scanArea=(3, 3))
        self.Enemy_img = goblinSpritesheet.parse_sprite("goblin4.png")
        self.Enemy_img = pygame.transform.scale_by(self.Enemy_img, self.main.scale)
        self.Enemy_rect = self.Enemy_img.get_rect()

class Tank(Enemy):
    def __init__(self, main, player, map_width, map_height, collisionMap):
        super().__init__(main, player, "Tank", map_width, map_height, 3, 2, 10, 10, 40, 10, 0.30, collisionMap, scanArea=(3, 3))
        self.Enemy_img = enemySpritesheet.parse_sprite("kylling4.png")
        self.Enemy_img = pygame.transform.scale_by(self.Enemy_img, self.main.scale)
        self.Enemy_rect = self.Enemy_img.get_rect()

class Boss(Enemy):
    def __init__(self, main, player, map_width, map_height, collisionMap):
        super().__init__(main, player, "Boss", map_width, map_height, 3, 2, 10, 10, 50, 20, 0.5, collisionMap, scanArea=(3, 3))
        self.Enemy_img = enemySpritesheet.parse_sprite("kylling4.png")
        self.Enemy_img = pygame.transform.scale_by(self.Enemy_img, self.main.scale)
        self.Enemy_rect = self.Enemy_img.get_rect()




