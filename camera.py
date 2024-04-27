import math
import pygame

class Camera:
    def __init__(self, main, player, acceleration, maxSpeed):
        self.main = main
        self.player = player
        self.x = self.player.x + (16 * self.main.scale) / 2
        self.y = self.player.y + (16 * self.main.scale) / 2
        self.acceleration = acceleration
        self.speed = 0.25 * self.main.scale
        self.maxSpeed = maxSpeed

    def update(self):
        xPlayer = self.player.x + (16 * self.main.scale) / 2
        yPlayer = self.player.y + (16 * self.main.scale) / 2

        distanceFromPlayer = math.sqrt((yPlayer - self.y) ** 2 + (xPlayer - self.x) ** 2)
        angleToPlayer = math.atan2(yPlayer - self.y, xPlayer - self.x)

        self.speed = self.acceleration * distanceFromPlayer / self.main.scale

        self.speed = self.constrain(self.speed, 0, self.player.speed / 2)

        xVel = math.cos(angleToPlayer) * self.speed
        yVel = math.sin(angleToPlayer) * self.speed

        self.x = self.x + xVel
        self.y = self.y + yVel

        return self.x - self.main.gameWindowWidth / 2, self.y - self.main.gameWindowHeight / 2

    def constrain(self, num, min=None, max=None):
        if num < min and min is not None:
            num = min
        if num > max and max is not None:
            num = max
        return num
