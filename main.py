from tiles import *
from spritesheet import Spritesheet
from spritesheetToJson import SpritesheetToJson
import pygame
import os
import math

from player import Player
from camera import Camera

class Main():
    pygame.init()
    running = True
    clock = pygame.time.Clock()
    tile_size = 16

    def __init__(self, gameWindowWidth=pygame.display.Info().current_w, gameWindowHeight=pygame.display.Info().current_h, tile_columns=tile_size * 16 * 2, tile_rows=tile_size * 9 * 2):
        self.gameWindowWidth = gameWindowWidth
        self.gameWindowHeight = gameWindowHeight
        self.window = pygame.display.set_mode((self.gameWindowWidth, self.gameWindowHeight))
        self.DISPLAY_W = tile_columns
        self.DISPLAY_H = tile_rows
        self.scale = int(self.gameWindowWidth / self.DISPLAY_W)
        self.real_tile_size = self.tile_size * self.scale

        SpritesheetToJson("Images/water.png", self.tile_size)
        self.waterSpritesheet = Spritesheet('Images/water.png')

        SpritesheetToJson("Images/grass.png", self.tile_size)
        self.grassSpritesheet = Spritesheet('Images/grass.png')

        SpritesheetToJson("Images/Wooden House.png", self.tile_size)
        self.woodenHouseSpritesheet = Spritesheet('Images/Wooden House.png')

        SpritesheetToJson("Images/collision.png", self.tile_size)
        self.collisionSpritesheet = Spritesheet("Images/collision.png")

        self.maps = [TileMap('Levels/MainLevel_Water.csv', self.waterSpritesheet, self.tile_size, self.scale),
                     TileMap('Levels/MainLevel_Grass.csv', self.grassSpritesheet, self.tile_size, self.scale),
                     TileMap('Levels/MainLevel_House floor.csv', self.woodenHouseSpritesheet, self.tile_size, self.scale),
                     TileMap('Levels/MainLevel_House walls.csv', self.woodenHouseSpritesheet, self.tile_size, self.scale)]
        self.canvas = pygame.Surface((self.maps[0].map_w, self.maps[0].map_h))

        self.player = Player(self)
        self.camera = Camera(self, self.player, 0.04 * self.scale, 3 * self.scale)

    def rectCollisionChecker(self, entityCollider, wallCollider, speedX, speedY, xObstructed, yObstructed):
        xFuture = entityCollider.x + speedX
        yFuture = entityCollider.y + speedY

        if entityCollider.x + entityCollider.width > wallCollider.x and entityCollider.x < wallCollider.x + wallCollider.width and yFuture + entityCollider.height > wallCollider.y and yFuture < wallCollider.y + wallCollider.height:
            yObstructed = True
        if entityCollider.y + entityCollider.height > wallCollider.y and entityCollider.y < wallCollider.y + wallCollider.height and xFuture + entityCollider.width > wallCollider.x and xFuture < wallCollider.x + wallCollider.width:
            xObstructed = True

        return xObstructed, yObstructed

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

                self.player.checkInput(event)
            self.player.update()
            self.camera.update()


            self.canvas.fill((0, 180, 240))
            for map in self.maps:
                map.draw_map(self.canvas)

            # visualisere colliders
            #for collider in self.player.checkCollision('Levels/MainLevel_Collision_Player.csv'):
            #    pygame.draw.rect(self.canvas, (255, 0, 0), pygame.Rect(collider.x, collider.y, collider.width, collider.height))

            self.player.draw_player(self.canvas)


            screen_region = (self.camera.update(), pygame.display.get_window_size())
            self.canvas.set_clip(pygame.Rect(screen_region))
            self.window.blit(self.canvas, (0, 0), screen_region)
            pygame.display.update()

tile_size = 16

main = Main(pygame.display.Info().current_w, pygame.display.Info().current_h, tile_size * 16 * 2, tile_size * 9 * 2)
main.run()
pygame.quit()
