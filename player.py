import pygame, csv, os
from getSpritesheets import playerSpritesheet
from collider import Collider
import math
from hjælpeFunktioner import read_csv, rectCollisionChecker, checkNearbyTiles
from entityCollider import EntityCollider


class Player(EntityCollider):
    def __init__(self, main, x, y, xOffset, yOffset, width, height, speed, collisionMap, scanArea):
        EntityCollider.__init__(self, main, x, y, xOffset, yOffset, width, height, speed, collisionMap, scanArea)

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

    def draw_player(self, canvas):
        self.player_rect.x = self.x
        self.player_rect.y = self.y
        canvas.blit(self.player_img, self.player_rect)
