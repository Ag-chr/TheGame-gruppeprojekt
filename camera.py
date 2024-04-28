import math
import pygame
from hjælpeFunktioner import rectCollisionChecker

class Camera:
    def __init__(self, scale, gameWindowWidth, gameWindowHeight, player, acceleration, lookingDistance):
        self.scale = scale
        self.gameWindowWidth, self.gameWindowHeight = gameWindowWidth, gameWindowHeight

        self.player = player

        self.x = self.player.x + (16 * self.scale) / 2
        self.y = self.player.y + (16 * self.scale) / 2
        self.acceleration = acceleration
        self.speed = 0.25 * self.scale

        self.lookingDistance = lookingDistance
        self.xLookingScale = self.lookingDistance / self.gameWindowWidth
        self.yLookingScale = self.lookingDistance / self.gameWindowHeight

        self.noLookZone = pygame.Rect(self.gameWindowWidth / 4, self.gameWindowHeight / 4, self.gameWindowWidth / 2, self.gameWindowHeight / 2)

    def update(self):
        xMouse, yMouse = pygame.mouse.get_pos()
        mouse = pygame.Rect(xMouse, yMouse, 0, 0)

        isXInNoLookZone, isYInNoLookZone = rectCollisionChecker(mouse, self.noLookZone)
        xOffset = 0
        yOffset = 0

        if not (isXInNoLookZone and isYInNoLookZone):
            xOffset = mouse.x * self.xLookingScale - self.lookingDistance / 2
            yOffset = mouse.y * self.yLookingScale - self.lookingDistance / 2

        xPlayer = self.player.x + 16 * self.scale / 2
        yPlayer = self.player.y + 16 * self.scale / 2

        distanceFromPlayer = math.sqrt((yPlayer - self.y + yOffset) ** 2 + (xPlayer - self.x + xOffset) ** 2)
        angleToPlayer = math.atan2(yPlayer - self.y + yOffset, xPlayer - self.x + xOffset)

        self.speed = self.acceleration * distanceFromPlayer / self.scale

        xVel = math.cos(angleToPlayer) * self.speed
        yVel = math.sin(angleToPlayer) * self.speed

        self.x = self.x + xVel
        self.y = self.y + yVel

        return self.x - self.gameWindowWidth / 2, self.y - self.gameWindowHeight / 2
