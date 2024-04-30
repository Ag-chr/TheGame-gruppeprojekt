from tiles import *
from getSpritesheets import updateJson, waterSpritesheet, grassSpritesheet, woodenHouseSpritesheet
from hjælpeFunktioner import checkNearbyTiles, read_csv
import pygame


from player import Player
from camera import Camera

class Main():
    pygame.init()
    running = True
    clock = pygame.time.Clock()
    tile_size = 16

    def __init__(self, gameWindowWidth=pygame.display.Info().current_w, gameWindowHeight=pygame.display.Info().current_h, tile_columns=16 * 2, tile_rows=9 * 2):
        self.windowWidth, self.windowHeight = gameWindowWidth, gameWindowHeight
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight))  # sætter størrelse af vinduet
        pygame.display.toggle_fullscreen()

        self.DISPLAY_W, self.DISPLAY_H = tile_columns * self.tile_size, tile_rows * self.tile_size  # ønsket antal af viste tiles på begge led
        self.scale = round(self.windowWidth / self.DISPLAY_W)  # forholdet for en pixel når den forstørres til at fylde hele skærmen

        updateJson(self.tile_size)  # Json filer er dem som giver lokationen og størrelse for alle sprites
        # forskellige niveauer af tilemaps, så græs bliver tegnet oven på vand, osv.
        self.maps = [TileMap('Levels/MainLevel_Water.csv', waterSpritesheet, self.tile_size, self.scale),
                     TileMap('Levels/MainLevel_Grass.csv', grassSpritesheet, self.tile_size, self.scale),
                     TileMap('Levels/MainLevel_House floor.csv', woodenHouseSpritesheet, self.tile_size, self.scale),
                     TileMap('Levels/MainLevel_House walls.csv', woodenHouseSpritesheet, self.tile_size, self.scale)]

        # tegnefladen skal være samme størrelse som map for at tegne det hele i starten
        self.canvas = pygame.Surface((self.maps[0].map_w, self.maps[0].map_h))

        self.player = Player(self, self.maps[0].map_w / 2, self.maps[0].map_h / 2)
        self.camera = Camera(self, self.player, 0.075, 100)

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(60)  # 60 fps

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()

                self.player.checkInput(event)
            self.player.update()

            self.canvas.fill((0, 180, 240))
            for map in self.maps:
                map.draw_map(self.canvas)

            # visualisere colliders
            #for collider in checkNearbyTiles(self.tile_size, self.scale, read_csv('Levels/MainLevel_Collision player.csv'), self.player.x + self.player.width, self.player.y + self.player.height, scanTiles=((0,-1), (-1, 0), (0, 1), (1, 0))):
            #    pygame.draw.rect(self.canvas, (255, 0, 0), pygame.Rect(collider.x, collider.y, collider.width, collider.height))

            self.player.draw_player(self.canvas)

            screen_region = (self.camera.update(), pygame.display.get_window_size())  # området hvor skærmen er
            self.canvas.set_clip(pygame.Rect(screen_region))  # modificere pixels kun indenfor skærm området
            self.window.blit(self.canvas, (0, 0), screen_region)  # tegner canvas på skærm og kun område som kan ses
            pygame.display.update()  # updater skærm så disse ændringer kan ses

    def start(self):
        self.running = True
        startCanvas = pygame.Surface((self.windowWidth, self.windowHeight))

        font = pygame.font.Font('freesansbold.ttf', 50)
        text = font.render("Storm the Farm", False, (255, 0, 0))
        textRect = text.get_rect()
        textRect.center = (self.windowWidth // 2, self.windowHeight // 2)

        while self.running:
            self.clock.tick(60)  # 60 fps

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()


            startCanvas.fill((0, 180, 240))
            startCanvas.blit(text, textRect)

            self.window.blit(startCanvas, (0, 0))  # tegner canvas på skærm og kun område som kan ses
            pygame.display.update()  # updater skærm så disse ændringer kan ses


main = Main(pygame.display.Info().current_w, pygame.display.Info().current_h, 16 * 1.6, 9 * 1.6)
main.start()
main.run()
pygame.quit()
