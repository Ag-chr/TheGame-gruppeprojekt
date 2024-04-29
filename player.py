import pygame, csv, os
from getSpritesheets import playerSpritesheet
from collider import Collider
import math
from hjælpeFunktioner import read_csv, rectCollisionChecker, checkNearbyTiles

class Player:
    def __init__(self, main, xStart, yStart):
        self.main = main

        self.player_img = playerSpritesheet.parse_sprite("character0.png")  # giver udsnit af sprite0 fra json fil
        self.player_img = pygame.transform.scale_by(self.player_img, self.main.scale)
        self.player_rect = self.player_img.get_rect()  # giver bredde og højde af sprite/player

        self.x = xStart - self.player_rect.width / 2
        self.y = yStart - self.player_rect.height / 2

        self.width = 10 * self.main.scale
        self.height = 12 * self.main.scale
        self.xOffset, self.yOffset = 3 * self.main.scale, 2 * self.main.scale  # centrerer collider
        self.playerCollider = Collider(tile_size=self.main.tile_size, scale=self.main.scale, x=self.x + self.xOffset, y=self.y + self.yOffset, width=self.width, height=self.height)

        self.speed = 2 * self.main.scale
        self.moveX = 0  # retning af bevægelse på x akse
        self.moveY = 0  # retning af bevægelse på x akse
        self.collisionMap = read_csv('Levels/MainLevel_Collision player.csv')  # brugt til tjekning af colliders tæt på

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
        self.playerCollider.x, self.playerCollider.y = self.x + self.xOffset, self.y + self.yOffset
        xObstructed = False
        yObstructed = False

        # Tjekker om colliders er tæt på. Hvis de er puttes de ind i en liste/array
        colliders = checkNearbyTiles(self.main.tile_size, self.main.scale, self.collisionMap, self.x, self.y, scanArea=(2, 2))
        # Tjekker hver collider om de rammer player
        for collider in colliders:
            xObstructed, yObstructed = rectCollisionChecker(self.playerCollider, collider, self.moveX, self.moveY, xObstructed, yObstructed)

        # Tjekker hvis player bevæger sig mere end speed, som den gør når den går skråt. Derefter rettes det
        distanceMoved = math.sqrt(self.moveX ** 2 + self.moveY ** 2)
        amountToCorrect = 1
        if distanceMoved > self.speed:
            amountToCorrect = self.speed / distanceMoved

        # stopper player hvis collider er i vejen
        if not xObstructed:
            self.x += self.moveX * amountToCorrect
        if not yObstructed:
            self.y += self.moveY * amountToCorrect

    def draw_player(self, canvas):
        self.player_rect.x = self.x
        self.player_rect.y = self.y
        canvas.blit(self.player_img, self.player_rect)
