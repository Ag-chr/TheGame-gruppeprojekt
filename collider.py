import pygame

class Collider:
    def __init__(self, tile_size, scale, x, y, width=0, height=0, tileID=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        if tileID is not None:
            if tileID == "0":
                self.x += 11 * scale  # flytter 11 pixel fremad fordi tile starter ikke oppe i venstre hjørne
                self.width = 5 * scale
            elif tileID == "1":
                pass
            elif tileID == "2":
                self.width = 5 * scale

        if self.width == 0:
            self.width = tile_size * scale
        if self.height == 0:
            self.height = tile_size * scale

    def __str__(self):
        return f"x: {self.x}, y: {self.y}\nwidth: {self.width}, height: {self.height}"

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0 ,0), pygame.Rect(self.x, self.y, self.width, self.height))
