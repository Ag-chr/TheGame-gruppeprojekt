import pygame
from getSpritesheets import enemySpritesheet
import math
import random
from collider import Collider
from hjælpeFunktioner import read_csv,rectCollisionChecker, checkNearbyTiles
from gun import Bullet

class Enemy:
    def __init__(self, main, player, name, map_width, map_height, xOffset, yOffset, width, height, health, damage, speed,collisionMap,scanArea):
        self.name = name
        self.max_health = health
        self.health = health
        self.damage = damage
        self.main = main
        self.player = player
        self.xOffset = xOffset * self.main.scale
        self.yOffset = yOffset * self.main.scale
        self.width = width * self.main.scale
        self.speed = speed
        self.height = height * self.main.scale
        self.scanArea = scanArea
        self.hitbox = (self.xOffset + 17, self.yOffset + 2, 31, 57)
        self.visible = True
        self.dead = False

        self.xVel = 0
        self.yVel = 0

        # Random spawn
        self.x = random.randint(0, map_width - self.width)
        self.y = random.randint(0, map_height - self.width)

        self.collisionMap = read_csv(collisionMap)

        self.collider = Collider(tile_size=self.main.tile_size, scale=self.main.scale, x=self.x + self.xOffset,
                                 y=self.y + self.yOffset, width=self.width, height=self.height)

        self.Enemy_img = enemySpritesheet.parse_sprite("kylling0.png")  # giver udsnit af sprite0 fra json fil
        self.Enemy_img = pygame.transform.scale_by(self.Enemy_img, self.main.scale)
        self.Enemy_rect = self.Enemy_img.get_rect()  # giver bredde og højde af enemy


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


    def hit(self):
        if self.health > 0:
            self.health -= 1
            if self.health <= 0:
                self.dead = True
                self.visible = False

#    def test(self, event, Enemy1, Enemy2):
#        if event.type == pygame.KEYDOWN:
#            if event.key == pygame.K_g:
#                Enemy1.hit()
#                Enemy2.hit()


    def update(self, player):
        if not self.dead:
            xObstructed, yObstructed = self.checkCollision()

            distanceFromPlayer = math.sqrt((self.player.y - self.y) ** 2 + (self.player.x - self.x) ** 2)
            angleToPlayer = math.atan2(self.player.y - self.y, self.player.x - self.x)

            self.xVel = math.cos(angleToPlayer) * self.speed
            self.yVel = math.sin(angleToPlayer) * self.speed

            if not xObstructed:
                self.x += self.xVel
            if not yObstructed:
                self.y += self.yVel



    def checkCollision(self) -> (bool, bool):
        self.collider.x, self.collider.y = self.x + self.xOffset, self.y + self.yOffset
        xObstructed = False
        yObstructed = False

        nearbyColliders = checkNearbyTiles(self.main.tile_size, self.main.scale, self.collisionMap, self.x, self.y, scanArea=self.scanArea)
        for collider in nearbyColliders:
            xObstructed, yObstructed = rectCollisionChecker(self.collider, collider, self.xVel, self.yVel, xObstructed, yObstructed)

        return xObstructed, yObstructed


class Sprinter(Enemy):
    def __init__(self, main, player, map_width, map_height, collisionMap):
        super().__init__(main, player, "Sprinter", map_width, map_height, 3, 2, 10, 10, 10, 2, 1, collisionMap, scanArea=(3, 3))
        self.Enemy_img = enemySpritesheet.parse_sprite("kylling4.png")
        self.Enemy_img = pygame.transform.scale_by(self.Enemy_img, self.main.scale)
        self.Enemy_rect = self.Enemy_img.get_rect()

class Tank(Enemy):
    def __init__(self, main, player, map_width, map_height, collisionMap):
        super().__init__(main, player, "Tank", map_width, map_height, 3, 2, 10, 10, 30, 5, 0.3, collisionMap, scanArea=(3, 3))
        self.Enemy_img = enemySpritesheet.parse_sprite("kylling4.png")
        self.Enemy_img = pygame.transform.scale_by(self.Enemy_img, self.main.scale)
        self.Enemy_rect = self.Enemy_img.get_rect()

class Boss(Enemy):
    def __init__(self, main, player, map_width, map_height, collisionMap):
        super().__init__(main, player, "Boss", map_width, map_height, 3, 2, 10, 10, 100, 10, 0.4, collisionMap, scanArea=(3, 3))
        self.Enemy_img = enemySpritesheet.parse_sprite("kylling4.png")
        self.Enemy_img = pygame.transform.scale_by(self.Enemy_img, self.main.scale)
        self.Enemy_rect = self.Enemy_img.get_rect()