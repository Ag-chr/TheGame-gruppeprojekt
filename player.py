import pygame, csv, os
from getSpritesheets import playerSpritesheet
from collider import Collider
import math
from hjælpeFunktioner import read_csv, rectCollisionChecker, checkNearbyTiles


class Player:
    def __init__(self, main, x, y, xOffset, yOffset, width, height, speed, collisionMap, scanArea):
        self.main = main
        self.xOffset = xOffset * self.main.scale
        self.yOffset = yOffset * self.main.scale
        self.width = width * self.main.scale
        self.height = height * self.main.scale
        self.speed = speed * self.main.scale

        self.x = x - (self.xOffset + self.width) / 2
        self.y = y - (self.xOffset + self.width) / 2

        self.xVel = 0
        self.yVel = 0
        self.collisionMap = read_csv(collisionMap)
        self.scanArea = scanArea

        self.collider = Collider(tile_size=self.main.tile_size, scale=self.main.scale, x=self.x + self.xOffset,
                                 y=self.y + self.yOffset, width=self.width, height=self.height)

        self.player_img = playerSpritesheet.parse_sprite("character0.png")  # giver udsnit af sprite0 fra json fil
        self.player_img = pygame.transform.scale_by(self.player_img, self.main.scale)
        self.player_rect = self.player_img.get_rect()  # giver bredde og højde af sprite/player

    def checkInput(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.yVel -= self.speed
            if event.key == pygame.K_s:
                self.yVel += self.speed
            if event.key == pygame.K_a:
                self.xVel -= self.speed
            if event.key == pygame.K_d:
                self.xVel += self.speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.yVel += self.speed
            if event.key == pygame.K_s:
                self.yVel -= self.speed
            if event.key == pygame.K_a:
                self.xVel += self.speed
            if event.key == pygame.K_d:
                self.xVel -= self.speed

    def update(self):
        # bruger checkCollision fra fil entitycollider.py, som tjekker hvis
        xObstructed, yObstructed = self.checkCollision()

        # Tjekker hvis player bevæger sig mere end speed, som den gør når den går skråt. Derefter rettes det
        distanceMoved = math.sqrt(self.xVel ** 2 + self.yVel ** 2)
        amountToCorrect = 1
        if distanceMoved > self.speed:
            amountToCorrect = self.speed / distanceMoved

        # stopper player hvis collider er i vejen
        if not xObstructed:
            self.x += self.xVel * amountToCorrect
        if not yObstructed:
            self.y += self.yVel * amountToCorrect

    def checkCollision(self) -> (bool, bool):
        self.collider.x, self.collider.y = self.x + self.xOffset, self.y + self.yOffset
        xObstructed = False
        yObstructed = False

        nearbyColliders = checkNearbyTiles(self.main.tile_size, self.main.scale, self.collisionMap, self.x, self.y, scanArea=self.scanArea)
        for collider in nearbyColliders:
            xObstructed, yObstructed = rectCollisionChecker(self.collider, collider, self.xVel, self.yVel, xObstructed, yObstructed)

        return xObstructed, yObstructed

    def draw_player(self, canvas):
        self.player_rect.x = self.x
        self.player_rect.y = self.y
        canvas.blit(self.player_img, self.player_rect)
