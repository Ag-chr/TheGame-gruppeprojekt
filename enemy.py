import pygame
from getSpritesheets import enemySpritesheet

class Enemy:
    def __init__(self, name, x, y,xOffset, yOffset,width, health, damage, scale, main):
        self.name = name
        self.health = health
        self.damage = damage
        self.scale = scale
        self.main = main
        self.xOffset = xOffset * self.main.scale
        self.yOffset = yOffset * self.main.scale
        self.width = width * self.main.scale


        self.x = x
        self.y = y

        self.Enemy_img = enemySpritesheet.parse_sprite("goblinss0.png")  # giver udsnit af sprite0 fra json fil
        self.Enemy_img = pygame.transform.scale_by(self.Enemy_img, self.main.scale)
        self.Enemy_rect = self.Enemy_img.get_rect()  # giver bredde og højde af enemy

   ## def draw_enemy(self, canvas):
        ##self.Enemy_rect.x = self.x
        ##self.Enemy_rect.y = self.y
        ##canvas.blit(self.Enemy_img, self.Enemy_rect)
    def draw_enemy(self, canvas):
        enemy_color = (255, 0, 0)
        enemy_rect = pygame.Rect(self.x + self.xOffset, self.y + self.yOffset, self.width, self.width)
        pygame.draw.rect(canvas, enemy_color, enemy_rect)

    """    def take_damage(self, amount):
    pygame.draw.rect(canvas, enemy_color, enemy_rect)        self.health -= amount
        if self.health <= 0:
            print("test")
        else:
            print("test")  """
