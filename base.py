import pygame

class Base:
    def __init__(self, main, x, y, width, height, health, hitbox_margin=10):
        self.main = main
        self.x = x
        self.y = y
        self.width = width * self.main.scale
        self.height = height * self.main.scale
        self.max_health = health
        self.health = health
        self.hitbox_margin = hitbox_margin
        self.hitbox = pygame.Rect(self.x - hitbox_margin, self.y - hitbox_margin, self.width + 2 * hitbox_margin, self.height + 2 * hitbox_margin)

    def update_hitbox(self):
        self.hitbox.x = self.x - self.hitbox_margin
        self.hitbox.y = self.y - self.hitbox_margin
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

    def get_x(self):
        return self.x + self.width // 2

    def get_y(self):
        return self.y + self.height // 2