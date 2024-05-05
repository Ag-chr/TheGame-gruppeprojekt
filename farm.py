import pygame
from hjælpeFunktioner import read_csv
from tiles import TileMap
from getSpritesheets import farmSpritesheet
import csv
import math

class Farm:
    def __init__(self, main, player, farm_csv, farm_boundary):
        self.main = main
        self.player = player
        self.real_tile_size = self.main.tile_size * self.main.scale

        self.farmland_tile = "12"
        self.empty_tile = "10"

        self.farmland_image = farmSpritesheet.parse_sprite(f"tilled dirt{self.farmland_tile}.png").convert()
        self.farmland_image = pygame.transform.scale_by(self.farmland_image, self.main.scale)
        self.farmland_image.set_alpha(200)
        self.farmland_rect = self.farmland_image.get_rect()

        self.farm_csv_file = farm_csv
        self.farm_boundary = read_csv(farm_boundary)
        self.find_boundary()
        self.write_csv_farm_area()
        self.farm_csv_array = read_csv(farm_csv, "unix")
        self.farm_zone = pygame.Rect(self.start[0] * self.real_tile_size,
                                     self.start[1] * self.real_tile_size,
                                     self.end[0] * self.real_tile_size - self.start[0] * self.real_tile_size,
                                     self.end[1] * self.real_tile_size - self.start[1] * self.real_tile_size)
        self.farm_map = TileMap("Levels/MainLevel_Farm.csv", farmSpritesheet, self.main.tile_size, self.main.scale, x=self.start[0] * self.real_tile_size, y=self.start[1] * self.real_tile_size)

    def getPlayerGrid(self):
        player_direction = self.player.getDirection()
        xOffset = 0
        yOffset = 0
        if player_direction == "DOWN":
            yOffset = 1
        elif player_direction == "UP":
            yOffset = -1
        elif player_direction == "RIGHT":
            xOffset = 1
        elif player_direction == "LEFT":
            xOffset = -1
        x_player_grid = int((self.player.x + self.real_tile_size / 2) // self.real_tile_size + xOffset)
        y_player_grid = int((self.player.y + self.real_tile_size / 2) // self.real_tile_size + yOffset)
        return x_player_grid, y_player_grid

    def draw_farm(self, canvas):
        self.farm_map.draw_map(canvas)

    def draw_transparent_farmland(self, canvas):
        x_player_grid, y_player_grid = self.getPlayerGrid()
        x_player_boundary, y_player_boundary = x_player_grid - self.start[0], y_player_grid - self.start[1]

        try:
            tile = self.farm_csv_array[x_player_boundary][y_player_boundary]
        except:
            return
        if tile == self.empty_tile:
            return
        if x_player_boundary < 0 or y_player_boundary < 0:
            return

        self.farmland_rect.x = x_player_grid * self.real_tile_size
        self.farmland_rect.y = y_player_grid * self.real_tile_size
        canvas.blit(self.farmland_image, self.farmland_rect)

    def place_farmland(self):
        x_player_grid, y_player_grid = self.getPlayerGrid()
        x_player_boundary, y_player_boundary = x_player_grid - self.start[0], y_player_grid - self.start[1]
        tile = None

        try:
            tile = self.farm_csv_array[y_player_boundary][x_player_boundary]
        except:
            "Out of Bounds"
        if tile != "-1":
            return
        if x_player_boundary < 0 or y_player_boundary < 0:
            return

        self.farm_csv_array[y_player_boundary][x_player_boundary] = 12

        with open(self.farm_csv_file, "w") as file:
            csvwriter = csv.writer(file, delimiter=",", dialect="unix")
            csvwriter.writerows(self.farm_csv_array)

        self.farm_map = TileMap("Levels/MainLevel_Farm.csv", farmSpritesheet, self.main.tile_size, self.main.scale,
                                x=self.start[0] * self.real_tile_size, y=self.start[1] * self.real_tile_size)

    def checkInput(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                self.place_farmland()


    def find_boundary(self):
        boundary = self.farm_boundary
        x = y = 0
        self.start = None
        self.end = None

        for row in boundary:
            x = 0
            for tile in row:
                if boundary[y][x] != "-1":
                    if not bool(self.start):
                        self.start = (x + 1, y + 1)
                    else:
                        self.end = (x, y)
                x += 1
            y += 1

    def write_csv_farm_area(self):
        with open(self.farm_csv_file, "w") as file:
            for y in range(self.start[1], self.end[1]):
                file.write(f'{self.empty_tile}') if self.farm_boundary[y][self.start[0]] != "-1" else file.write('"-1"')

                for x in range(self.start[0] + 1, self.end[0]):
                    file.write(f',{self.empty_tile}') if self.farm_boundary[y][x] != "-1" else file.write(',"-1"')
                file.write("\n")