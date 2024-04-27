import pygame, csv, os
from spritesheetToJson import SpritesheetToJson
from spritesheet import Spritesheet
from collider import Collider
import math

class Player:
    def __init__(self, main):
        self.main = main

        SpritesheetToJson("Images/character.png", self.main.tile_size, 16, (16, 16), (16, 16))
        self.player_spritesheet = Spritesheet("Images/character.png")

        self.player_img = self.player_spritesheet.parse_sprite("character0.png")
        self.player_img = pygame.transform.scale_by(self.player_img, self.main.scale)
        self.player_rect = self.player_img.get_rect()

        self.x = self.main.maps[0].map_w / 2 - self.player_rect.width / 2
        self.y = self.main.maps[0].map_h / 2 - self.player_rect.height / 2
        self.XOffset, self.YOffset = 3 * self.main.scale, 2 * self.main.scale
        self.width = 10 * self.main.scale
        self.height = 12 * self.main.scale
        self.playerCollider = None

        self.speed = 2 * self.main.scale
        self.moveX = 0
        self.moveY = 0

    def checkInput(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.moveY -= self.speed
            if event.key == pygame.K_s:
                self.moveY += self.speed
            if event.key == pygame.K_a:
                self.moveX -= self.speed
            if event.key == pygame.K_d:
                self.moveX += self.speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.moveY += self.speed
            if event.key == pygame.K_s:
                self.moveY -= self.speed
            if event.key == pygame.K_a:
                self.moveX += self.speed
            if event.key == pygame.K_d:
                self.moveX -= self.speed

    def update(self):
        self.playerCollider = Collider(main=self.main, x=self.x + self.XOffset, y=self.y + self.YOffset, width=self.width, height=self.height)
        xObstructed = False
        yObstructed = False
        amountToCorrect = 1

        colliders = self.checkCollision('Levels/MainLevel_Collision_Player.csv')
        for collider in colliders:
            xObstructed, yObstructed = self.main.rectCollisionChecker(self.playerCollider, collider, self.moveX, self.moveY, xObstructed, yObstructed)
        
        distanceMoved = math.sqrt(self.moveX ** 2 + self.moveY ** 2)
        if distanceMoved > self.speed:
            amountToCorrect = self.speed / distanceMoved

        if not xObstructed:
            self.x += self.moveX * amountToCorrect
        if not yObstructed:
            self.y += self.moveY * amountToCorrect

    def checkCollision(self, csvFile):
        def read_csv(filename):
            map = []
            with open(os.path.join(filename)) as data:
                data = csv.reader(data, delimiter=',')
                for row in data:
                    map.append(list(row))
            return map

        map = read_csv(csvFile)
        scanHeight, scanWidth = 2, 2
        nearbyColliders = []

        yGrid = int(self.y // self.main.real_tile_size)
        xGrid = int(self.x // self.main.real_tile_size)

        for y in range(yGrid, yGrid + scanHeight):
            for x in range(xGrid, xGrid + scanWidth):
                tileID = map[y][x]
                if tileID == "-1": continue
                nearbyColliders.append(Collider(self.main, x * self.main.real_tile_size, y * self.main.real_tile_size, tileID=tileID))
        return nearbyColliders

    def draw_player(self, canvas):
        self.player_rect.x = self.x
        self.player_rect.y = self.y
        canvas.blit(self.player_img, self.player_rect)
