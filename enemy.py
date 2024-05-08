import pygame
#from getSpritesheets import enemySpritesheet
from getSpritesheets import playerSpritesheet
import math
import random
from collider import Collider
from hjælpeFunktioner import read_csv,rectCollisionChecker, checkNearbyTiles

class Enemy:
    def __init__(self, name, map_width, map_height, xOffset, yOffset, width, height, health, damage, scale, main, speed,collisionMap,scanArea):
        self.name = name
        self.health = health
        self.damage = damage
        self.scale = scale
        self.main = main
        self.xOffset = xOffset * self.main.scale
        self.yOffset = yOffset * self.main.scale
        self.width = width * self.main.scale
        self.speed = speed
        self.height = height * self.main.scale
        self.scanArea = scanArea


        self.xVel = 0
        self.yVel = 0

        # Random spawn
        self.x = random.randint(0, map_width - self.width)
        self.y = random.randint(0, map_height - self.width)

        self.collisionMap = read_csv(collisionMap)

        self.collider = Collider(tile_size=self.main.tile_size, scale=self.main.scale, x=self.x + self.xOffset,
                                 y=self.y + self.yOffset, width=self.width, height=self.height)


        self.Enemy_img = playerSpritesheet.parse_sprite("character0.png")  # giver udsnit af sprite0 fra json fil
        self.Enemy_img = pygame.transform.scale_by(self.Enemy_img, self.main.scale)
        self.Enemy_rect = self.Enemy_img.get_rect()  # giver bredde og højde af enemy

    def draw_enemy(self, canvas):
        self.Enemy_rect.x = self.x
        self.Enemy_rect.y = self.y
        canvas.blit(self.Enemy_img, self.Enemy_rect)
    #def draw_enemy(self, canvas):
      #  enemy_color = (255, 0, 0)
      #  enemy_rect = pygame.Rect(self.x + self.xOffset, self.y + self.yOffset, self.width, self.width)
       # pygame.draw.rect(canvas, enemy_color, enemy_rect)

    def update(self, player):
        # Beregner playerens retning
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        xObstructed, yObstructed = self.checkCollision()

        # fikser retningen
        if distance > 0:
            dx /= distance
            dy /= distance

        if not xObstructed:
            self.x += dx * self.speed
        if not yObstructed:
            self.y += dy * self.speed




    def checkCollision(self) -> (bool, bool):
        self.collider.x, self.collider.y = self.x + self.xOffset, self.y + self.yOffset
        xObstructed = False
        yObstructed = False

        nearbyColliders = checkNearbyTiles(self.main.tile_size, self.main.scale, self.collisionMap, self.x, self.y, scanArea=self.scanArea)
        for collider in nearbyColliders:
            xObstructed, yObstructed = rectCollisionChecker(self.collider, collider, self.xVel, self.yVel, xObstructed, yObstructed)

        return xObstructed, yObstructed


    """    def take_damage(self, amount):
    pygame.draw.rect(canvas, enemy_color, enemy_rect)        self.health -= amount
        if self.health <= 0:
            print("test")
        else:
            print("test")  """
