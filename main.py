from tiles import *
from getSpritesheets import updateJson, waterSpritesheet, grassSpritesheet, woodenHouseSpritesheet
import pygame


from player import Player
from camera import Camera

class Main():
    pygame.init()
    running = True
    clock = pygame.time.Clock()
    tile_size = 16

    def __init__(self, gameWindowWidth=pygame.display.Info().current_w, gameWindowHeight=pygame.display.Info().current_h, tile_columns=16 * 2, tile_rows=9 * 2):
        self.gameWindowWidth = gameWindowWidth
        self.gameWindowHeight = gameWindowHeight
        self.window = pygame.display.set_mode((self.gameWindowWidth, self.gameWindowHeight))
        self.DISPLAY_W = tile_columns * self.tile_size
        self.DISPLAY_H = tile_rows * self.tile_size
        self.scale = int(self.gameWindowWidth / self.DISPLAY_W)
        self.real_tile_size = self.tile_size * self.scale

        updateJson(self.tile_size)
        self.maps = [TileMap('Levels/MainLevel_Water.csv', waterSpritesheet, self.tile_size, self.scale),
                     TileMap('Levels/MainLevel_Grass.csv', grassSpritesheet, self.tile_size, self.scale),
                     TileMap('Levels/MainLevel_House floor.csv', woodenHouseSpritesheet, self.tile_size, self.scale),
                     TileMap('Levels/MainLevel_House walls.csv', woodenHouseSpritesheet, self.tile_size, self.scale)]
        self.canvas = pygame.Surface((self.maps[0].map_w, self.maps[0].map_h))

        self.player = Player(self.scale, self.tile_size, self.maps[0].map_w / 2, self.maps[0].map_h / 2)
        self.camera = Camera(self.scale, self.gameWindowWidth, self.gameWindowHeight, self.player, 0.04 * self.scale, 100 * self.scale)

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

main = Main(pygame.display.Info().current_w, pygame.display.Info().current_h, 16 * 2, 9 * 2)
main.run()
pygame.quit()
