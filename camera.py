import math
import pygame
from hjælpeFunktioner import rectCollisionChecker

class Camera:
    def __init__(self, main, player, acceleration, lookingDistance):
        self.main = main

        self.player = player

        self.x = self.player.x + 16 * self.main.scale / 2
        self.y = self.player.y + 16 * self.main.scale / 2
        self.acceleration = acceleration * self.main.scale  # hvor hurtigt kamera accelererer efter player
        self.speed = 0  # nu værende hastighed mod player

        self.lookingDistance = lookingDistance * self.main.scale  # afstand for hvor langt man kan kigge væk
        self.xLookingScale = self.lookingDistance / self.main.windowWidth
        self.yLookingScale = self.lookingDistance / self.main.windowHeight

        # område hvor man ikke kigger længere
        self.noLookZone = pygame.Rect(self.main.windowWidth / 4, self.main.windowHeight / 4, self.main.windowWidth / 2, self.main.windowHeight / 2)

    def update(self):
        xMouse, yMouse = pygame.mouse.get_pos()
        mouse = pygame.Rect(xMouse, yMouse, 0, 0)  # bruges til når man skal tjekke om hvis mus er inde i noLookZone

        xOffset = mouse.x * self.xLookingScale - self.lookingDistance / 2
        yOffset = mouse.y * self.yLookingScale - self.lookingDistance / 2

        # tjekker om mus er indenfor noLookZone
        isXInNoLookZone, isYInNoLookZone = rectCollisionChecker(mouse, self.noLookZone)
        if isXInNoLookZone and isYInNoLookZone:
            xOffset = yOffset = 0

        # players x og y koords og oppe i venstre side af sprite så det centreres
        xPlayer = self.player.x + 16 * self.main.scale / 2
        yPlayer = self.player.y + 16 * self.main.scale / 2

        distanceFromPlayer = math.sqrt((yPlayer - self.y + yOffset) ** 2 + (xPlayer - self.x + xOffset) ** 2)
        angleToPlayer = math.atan2(yPlayer - self.y + yOffset, xPlayer - self.x + xOffset)

        self.speed = self.acceleration * distanceFromPlayer / self.main.scale

        xVel = math.cos(angleToPlayer) * self.speed
        yVel = math.sin(angleToPlayer) * self.speed

        self.x = self.x + xVel
        self.y = self.y + yVel

        # x og y er i midten af skærm. De flyttes oppe til venstre så hele skærm bliver brugt
        return self.x - self.main.windowWidth / 2, self.y - self.main.windowHeight / 2
