import pygame

class Collider:
    def __init__(self, main, x, y, tileID=None, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        if tileID is not None:
            if tileID == "0":
                self.x += 11 * main.scale  # flytter 11 pixel fremad fordi tile starter ikke oppe i venstre hjørne
                self.width = 5 * main.scale
            elif tileID == "1":
                pass
            elif tileID == "2":
                self.width = 5 * main.scale

        if self.width == 0:
            self.width = main.tile_size * main.scale
        if self.height == 0:
            self.height = main.tile_size * main.scale

    def __str__(self):
        return f"x: {self.x}, y: {self.y}\nwidth: {self.width}, height: {self.height}"

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0 ,0), pygame.Rect(self.x, self.y, self.width, self.height))
