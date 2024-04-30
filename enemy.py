import pygame

class Enemy:

    width = 16
    height = 16
    color = (255, 0, 128)


    def __init__(self, x, screen, y, width, height, end):
        self.x = x
        self.y = y
        self.path = [x, end] #Enemy start sted
        self.theScreen = screen


    def draw(self):
        pygame.draw.rect(self.theScreen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

