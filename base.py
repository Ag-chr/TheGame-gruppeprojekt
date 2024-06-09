import pygame

class Base:
    def __init__(self, main, x, y, width, height, health):
        self.main = main
        self.x = x
        self.y = y
        self.width = width * self.main.scale
        self.height = height * self.main.scale
        self.max_health = health
        self.health = health
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
    def draw(self, canvas):
        pygame.draw.rect(canvas, (255, 0, 0), self.hitbox, 2)
        healthbar_width = 100
        healthbar_height = 10
        health_width = (self.health / self.max_health) * healthbar_width
        pygame.draw.rect(canvas, (0, 128, 0), (self.x + (self.width // 2) - (healthbar_width // 2), self.y - 20, health_width, healthbar_height))
        pygame.draw.rect(canvas, (255, 0, 0), (self.x + (self.width // 2) - (healthbar_width // 2), self.y - 20, healthbar_width, healthbar_height), 2)

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
