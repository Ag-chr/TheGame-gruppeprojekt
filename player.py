import pygame, csv, os
from getSpritesheets import playerSpritesheet
from collider import Collider
import math
from hjælpeFunktioner import read_csv, rectCollisionChecker, checkCollision

class Player:
    def __init__(self, scale, tile_size, xStart, yStart):
        self.scale = scale
        self.tile_size = tile_size

        self.player_img = playerSpritesheet.parse_sprite("character0.png")
        self.player_img = pygame.transform.scale_by(self.player_img, self.scale)
        self.player_rect = self.player_img.get_rect()

        self.x = xStart - self.player_rect.width / 2
        self.y = yStart - self.player_rect.height / 2

        self.XOffset, self.YOffset = 3 * self.scale, 2 * self.scale
        self.width = 10 * self.scale
        self.height = 12 * self.scale
        self.playerCollider = Collider(tile_size=self.tile_size, scale=self.scale, x=self.x + self.XOffset, y=self.y + self.YOffset, width=self.width, height=self.height)

        self.speed = 2 * self.scale
        self.moveX = 0
        self.moveY = 0
        self.collisionMap = read_csv('Levels/MainLevel_Collision player.csv')

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
        self.playerCollider.x, self.playerCollider.y = self.x + self.XOffset, self.y + self.YOffset
        xObstructed = False
        yObstructed = False
        amountToCorrect = 1

        colliders = checkCollision(self.collisionMap, self.x, self.y, self.tile_size, self.scale)
        for collider in colliders:
            xObstructed, yObstructed = rectCollisionChecker(self.playerCollider, collider, self.moveX, self.moveY, xObstructed, yObstructed)
        
        distanceMoved = math.sqrt(self.moveX ** 2 + self.moveY ** 2)
        if distanceMoved > self.speed:
            amountToCorrect = self.speed / distanceMoved

        if not xObstructed:
            self.x += self.moveX * amountToCorrect
        if not yObstructed:
            self.y += self.moveY * amountToCorrect

    def draw_player(self, canvas):
        self.player_rect.x = self.x
        self.player_rect.y = self.y
        canvas.blit(self.player_img, self.player_rect)
