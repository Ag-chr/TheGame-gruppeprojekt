import pygame, csv, os
from spritesheetToJson import SpritesheetToJson
from spritesheet import Spritesheet
from collider import Collider


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
        self.width = 13 * self.main.scale
        self.height = 15 * self.main.scale

        self.moveAmount = 2 * self.main.scale
        self.moveX = 0
        self.moveY = 0

    def checkInput(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.moveY -= self.moveAmount
            if event.key == pygame.K_s:
                self.moveY += self.moveAmount
            if event.key == pygame.K_a:
                self.moveX -= self.moveAmount
            if event.key == pygame.K_d:
                self.moveX += self.moveAmount

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.moveY += self.moveAmount
            if event.key == pygame.K_s:
                self.moveY -= self.moveAmount
            if event.key == pygame.K_a:
                self.moveX += self.moveAmount
            if event.key == pygame.K_d:
                self.moveX -= self.moveAmount


    def update(self):
        xFuture = self.x + self.moveX
        yFuture = self.y + self.moveY
        xObstructed = False
        yObstructed = False

        colliders = self.checkCollision('Levels/MainLevel_Collision_Player.csv')
        for collider in colliders:
            if self.x + self.width > collider.x and self.x < collider.x + collider.width and yFuture + self.height > collider.y and yFuture < collider.y + collider.height:
                yObstructed = True

            if self.y + self.height > collider.y and self.y < collider.y + collider.height and xFuture + self.width > collider.x and xFuture < collider.x + collider.width:
                xObstructed = True

        if not xObstructed:
            self.x += self.moveX
        if not yObstructed:
            self.y += self.moveY

    def checkCollision(self, csvFile):
        def read_csv(filename):
            map = []
            with open(os.path.join(filename)) as data:
                data = csv.reader(data, delimiter=',')
                for row in data:
                    map.append(list(row))
            return map

        map = read_csv(csvFile)
        scanHeight, scanWidth = 3, 3
        nearbyColliders = []

        yGrid = int(self.y // self.main.real_tile_size - 1)
        xGrid = int(self.x // self.main.real_tile_size - 1)

        for y in range(yGrid, yGrid + scanHeight + 1):
            for x in range(xGrid, xGrid + scanWidth + 1):
                tilenum = map[y][x]
                if tilenum == "-1": continue
                nearbyColliders.append(Collider(self.main, tilenum, x * self.main.real_tile_size, y * self.main.real_tile_size))
        return nearbyColliders

    def draw_player(self, canvas):
        self.player_rect.x = self.x
        self.player_rect.y = self.y
        canvas.blit(self.player_img, self.player_rect)



