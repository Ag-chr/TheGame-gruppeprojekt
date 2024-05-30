import keyword

import pygame
from hjælpeFunktioner import read_csv
from tiles import TileMap
from getSpritesheets import farmSpritesheet
import csv
import math
from gun import Bullet
import time

class Farm:
    def __init__(self, main, player, farm_csv, farm_boundary, plant_csv):
        self.main = main
        self.player = player
        self.real_tile_size = self.main.tile_size * self.main.scale

        self.farmland_tile = "12"
        self.boundary_tile = "10"

        self.farmland_image = farmSpritesheet.parse_sprite(f"tilled dirt{self.farmland_tile}.png").convert()
        self.farmland_image = pygame.transform.scale_by(self.farmland_image, self.main.scale)

        self.real_tile_size = int(self.main.real_tile_size)
        self.plant1_image = pygame.Surface((self.real_tile_size, self.real_tile_size))
        pygame.draw.rect(self.plant1_image, (56, 153, 0), (0, 0, self.real_tile_size, self.real_tile_size))

        self.plant2_image = pygame.Surface((self.real_tile_size, self.real_tile_size))
        pygame.draw.rect(self.plant2_image, (66, 184, 0), (0, 0, self.real_tile_size, self.real_tile_size))

        self.plant3_image = pygame.Surface((self.real_tile_size, self.real_tile_size))
        pygame.draw.rect(self.plant3_image, (76, 214, 0), (0, 0, self.real_tile_size, self.real_tile_size))

        self.start_of_bounds = None
        self.end_of_bounds = None
        self.farm_boundary = read_csv(farm_boundary)
        self.find_boundary()

        self.farm_csv = farm_csv
        self.write_csv_area(self.farm_csv, self.boundary_tile, "-1")
        self.farm_csv_array = read_csv(self.farm_csv, "unix")
        self.farm_map = TileMap("Farm/Farm_Area.csv", farmSpritesheet, self.main.tile_size, self.main.scale, x=self.start_of_bounds[0] * self.real_tile_size, y=self.start_of_bounds[1] * self.real_tile_size)

        self.plant_csv = plant_csv
        self.write_csv_area(self.plant_csv, self.boundary_tile, "12")
        self.plant_csv_array = read_csv(self.plant_csv, "unix")

        self.image_key = "image"
        self.placeable_tile_key = "placeable_tile"
        self.class_key = "class"
        self.firing_distance_key = "firing_distance"
        self.price_key = "price"

        self.selection = [{self.image_key: self.farmland_image, self.placeable_tile_key: "-1", self.price_key: 50},
                          {self.image_key: self.plant1_image, self.placeable_tile_key: "12", self.firing_distance_key: 100 * self.main.scale, "class": Plant1, self.price_key: 100},
                          {self.image_key: self.plant2_image, self.placeable_tile_key: "12", self.firing_distance_key: 150 * self.main.scale, "class": Plant2, self.price_key: 200},
                          {self.image_key: self.plant3_image, self.placeable_tile_key: "12", self.firing_distance_key: 200 * self.main.scale, "class": Plant3, self.price_key: 300}]
        self.currentSelection = 0

    def checkInput(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                if self.currentSelection == 0:
                    self.place_farmland()
                else:
                    self.place_plant()
            if event.key == pygame.K_q:
                self.switchItem("LEFT")
            if event.key == pygame.K_e:
                self.switchItem("RIGHT")

    def getPlayerGridPos(self):
        player_direction = self.player.getDirection()
        x_player_grid = int((self.player.x + self.real_tile_size / 2) // self.real_tile_size + player_direction[0])
        y_player_grid = int((self.player.y + self.real_tile_size / 2) // self.real_tile_size + player_direction[1])

        x_player_boundary, y_player_boundary = x_player_grid - self.start_of_bounds[0], y_player_grid - self.start_of_bounds[1]
        return x_player_grid, y_player_grid, x_player_boundary, y_player_boundary

    def is_placeable(self, x, y, csv_array, placeable_tile):
        if x >= len(csv_array[0]) or y >= len(csv_array):
            return False
        if x < 0 or y < 0:
            return False
        if csv_array[y][x] != placeable_tile:
            return False
        return True

    def draw_farm(self, canvas):
        self.farm_map.draw_map(canvas)

    def drawUI(self, canvas):
        scale = self.main.scale
        width, height = 35 * scale, 35 * scale

        background = pygame.Surface((width, height))
        background.set_alpha(150)

        tile = self.selection[self.currentSelection][self.image_key]
        canvas.blit(background, (self.main.windowWidth - width - 10 * scale, self.main.windowHeight - height - 10 * scale))
        canvas.blit(tile, (self.main.windowWidth - width/2 - 10 * scale - tile.get_width() /2, self.main.windowHeight - height / 2 - 10 * scale - tile.get_height() / 2))

    def switchItem(self, direction: str):
        if direction == "LEFT":
            self.currentSelection += -1
        elif direction == "RIGHT":
            self.currentSelection += 1

        if self.currentSelection >= len(self.selection):
            self.currentSelection = 0
        elif self.currentSelection < 0:
            self.currentSelection = len(self.selection) - 1

    def draw_transparent_tile(self, canvas):
        x_player_grid, y_player_grid, x_player_boundary, y_player_boundary = self.getPlayerGridPos()
        selected = self.selection[self.currentSelection]

        if not self.is_placeable(x_player_boundary, y_player_boundary, self.farm_csv_array, selected[self.placeable_tile_key]):
            return

        tile_image_trans = selected[self.image_key].copy()
        tile_image_trans.set_alpha(150)
        canvas.blit(tile_image_trans, (x_player_grid * self.real_tile_size, y_player_grid * self.real_tile_size))

    def change_num_in_csv(self, csv_file, x, y, num):
        csv_array = read_csv(csv_file, dialect="unix")
        csv_array[y][x] = num

        with open(csv_file, "w") as file:
            csvwriter = csv.writer(file, delimiter=",", dialect="unix")
            csvwriter.writerows(csv_array)

        return csv_array

    def place_farmland(self):
        x_player_grid, y_player_grid, x_player_boundary, y_player_boundary = self.getPlayerGridPos()
        selected_farmland = self.selection[self.currentSelection]

        if not self.is_placeable(x_player_boundary, y_player_boundary, self.farm_csv_array, "-1"):
            return

        if self.main.money < selected_farmland[self.price_key]:
            return
        self.main.money -= selected_farmland[self.price_key]

        self.farm_csv_array = self.change_num_in_csv(self.farm_csv, x_player_boundary, y_player_boundary, "12")

        self.farm_map = TileMap("Farm/Farm_Area.csv", farmSpritesheet, self.main.tile_size, self.main.scale,
                                x=self.start_of_bounds[0] * self.real_tile_size, y=self.start_of_bounds[1] * self.real_tile_size)

    def place_plant(self):
        x_player_grid, y_player_grid, x_player_boundary, y_player_boundary = self.getPlayerGridPos()
        selected_plant = self.selection[self.currentSelection]

        if not self.is_placeable(x_player_boundary, y_player_boundary, self.farm_csv_array, selected_plant[self.placeable_tile_key]):
            return
        if not self.is_placeable(x_player_boundary, y_player_boundary, self.plant_csv_array, selected_plant[self.placeable_tile_key]):
            return

        if self.main.money < selected_plant[self.price_key]:
            return
        self.main.money -= selected_plant[self.price_key]

        self.plant_csv_array = self.change_num_in_csv(self.plant_csv, x_player_boundary, y_player_boundary, "-1")
        print(x_player_boundary, y_player_boundary)

        self.main.plants.append(selected_plant[self.class_key](self.main, self, selected_plant[self.image_key], x_player_grid * self.real_tile_size, y_player_grid * self.real_tile_size, self.main.enemies, selected_plant[self.firing_distance_key]))

    def find_boundary(self):
        boundary = self.farm_boundary
        x = y = 0

        for row in boundary:
            x = 0
            for tile in row:
                if boundary[y][x] != "-1":
                    if not bool(self.start_of_bounds):
                        self.start_of_bounds = (x + 1, y + 1)
                    else:
                        self.end_of_bounds = (x, y)
                x += 1
            y += 1

    def write_csv_area(self, file, boundary_tile, empty_tile):
        with open(file, "w") as file:
            for y in range(self.start_of_bounds[1], self.end_of_bounds[1]):
                file.write(f'"{boundary_tile}"') if self.farm_boundary[y][self.start_of_bounds[0]] != "-1" else file.write(f'"{empty_tile}"')

                for x in range(self.start_of_bounds[0] + 1, self.end_of_bounds[0]):
                    file.write(f',"{boundary_tile}"') if self.farm_boundary[y][x] != "-1" else file.write(f',"{empty_tile}"')
                file.write("\n")

class Plant:
    def __init__(self, main, farm, image, x, y, targets: list, health, damage, firingspeed, firing_distance):
        self.main = main
        self.farm = farm
        self.image = image
        self.x, self.y = x, y
        self.width = self.height = 16 * self.main.scale
        self.targets = targets

        self.health = health
        self.damage = damage
        self.firingspeed = firingspeed
        self.firing_distance = firing_distance

        self.xPoint = self.x + self.width / 2
        self.yPoint = self.y + self.height / 2

        self.startTime = time.time()
        self.dead = False

    def draw(self, canvas):
        canvas.blit(self.image, (self.x, self.y))
        width = height = self.main.scale
        pygame.draw.rect(canvas, (0, 0, 0), (self.xPoint - width / 2, self.yPoint - height / 2, width, height))

    def update(self):
        self.targets = self.main.enemies
        target = self.nearest_target()

        if target is None:
            return
        xCenter, yCenter = self.x + self.width / 2, self.y + self.height / 2
        angle_to_target = math.atan2(target.y + target.height / 2 - yCenter, target.x + target.width / 2 - xCenter)

        self.xPoint = math.cos(angle_to_target) * 6 * self.main.scale + xCenter
        self.yPoint = math.sin(angle_to_target) * 6 * self.main.scale + yCenter

        if time.time() > self.startTime + self.firingspeed:
            self.startTime = time.time()
            self.main.bullets.append(Bullet(self.main, angle_to_target, 3, 1, 2, 2, "Levels/MainLevel_Collision enemy.csv", (2, 2), xCenter, yCenter, 0, 0))

    def nearest_target(self):
        min_distance = math.inf
        nearest_target = None
        for target in self.targets:
            distance = math.sqrt((target.x - (self.x - self.width / 2))**2 + (target.y - (self.y + self.height / 2))**2)
            if distance < min_distance and distance < self.firing_distance:
                min_distance = distance
                nearest_target = target
        return nearest_target

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.main.plants.remove(self)
            xboundary = (self.x // (self.main.tile_size * self.main.scale)) - self.farm.start_of_bounds[0]
            yboundary = (self.y // (self.main.tile_size * self.main.scale)) - self.farm.start_of_bounds[1]
            self.farm.plant_csv_array = self.farm.change_num_in_csv(self.farm.plant_csv, xboundary, yboundary, "12")


class Plant1(Plant):
    def __init__(self, main, farm, image, x, y, targets, firing_distance):
        super().__init__(main, farm, image, x, y, targets, 5, 1, 2, firing_distance)


class Plant2(Plant):
    def __init__(self, main, farm, image, x, y, targets, firing_distance):
        super().__init__(main, farm, image, x, y, targets, 10, 2, 1.5, firing_distance)


class Plant3(Plant):
    def __init__(self, main, farm, image, x, y, targets, firing_distance):
        super().__init__(main, farm, image, x, y, targets, 15, 3, 1, firing_distance)
