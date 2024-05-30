from tiles import TileMap
from getSpritesheets import updateJson, waterSpritesheet, grassSpritesheet, woodenHouseSpritesheet
from hjælpeFunktioner import checkNearbyTiles, read_csv
import pygame

from player import Player
from camera import Camera
from gun import Gun
from button import Button
from enemy import Tank, Sprinter, Boss
from farm import Farm
from wavespawner import WaveManager


class Main():
    pygame.init()
    running = True
    clock = pygame.time.Clock()
    tile_size = 16

    def __init__(self, gameWindowWidth=pygame.display.Info().current_w,
                 gameWindowHeight=pygame.display.Info().current_h, tile_columns=16 * 2, tile_rows=9 * 2):
        self.windowWidth, self.windowHeight = gameWindowWidth, gameWindowHeight
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight))  # sætter størrelse af vinduet
        pygame.display.toggle_fullscreen()

        self.DISPLAY_W, self.DISPLAY_H = tile_columns * self.tile_size, tile_rows * self.tile_size  # ønsket antal af viste tiles på begge led
        self.scale = round(self.windowWidth / self.DISPLAY_W)  # forholdet for en pixel når den forstørres på skærm
        self.real_tile_size = self.tile_size * self.scale

        updateJson(self.tile_size)  # Json filer er dem som giver lokationen og størrelse for alle sprites
        # forskellige niveauer af tilemaps, så græs bliver tegnet oven på vand, osv.
        self.maps = [TileMap('Levels/MainLevel_Water.csv', waterSpritesheet, self.tile_size, self.scale),
                     TileMap('Levels/MainLevel_Grass.csv', grassSpritesheet, self.tile_size, self.scale),
                     TileMap('Levels/MainLevel_House floor.csv', woodenHouseSpritesheet, self.tile_size, self.scale),
                     TileMap('Levels/MainLevel_House walls.csv', woodenHouseSpritesheet, self.tile_size, self.scale)]

        # Canvas/surface skal være samme størrelse som map for at tegne det hele i starten
        self.canvas = pygame.Surface((self.maps[0].map_w, self.maps[0].map_h))

        self.player = Player(self, self.maps[0].map_w / 2, self.maps[0].map_h / 2, 3, 2, 10, 12, 2,
                             "Levels/MainLevel_Collision player.csv", scanArea=(2, 2))
        self.camera = Camera(self, self.player, 0.075, 100)
        self.gun = Gun(self, self.player, self.camera, "Images/gun.png", 15)
        self.farm = Farm(self, self.player, "Farm/Farm_Area.csv", "Levels/MainLevel_Farm boundary.csv", "Farm/Plant_Area.csv")

        self.enemies = []
        self.bullets = []
        self.plants = []

        self.wave_start = False
        self.show_text = False
        self.wave_text_timer = 0
        self.wave_number = 1

        self.wave_manager = WaveManager(self, [
            {'type': Sprinter, 'interval': 2, 'base_count': 5},
            {'type': Tank, 'interval': 5, 'base_count': 3},
            {'type': Boss, 'interval': 10, 'base_count': 1}
        ])
        self.money = 0

    def run(self):
        self.running = True

        # tegner mappet og gemmer i billede/canvas, som kan derefter tegnes
        mapCanvas = pygame.Surface((self.maps[0].map_w, self.maps[0].map_h))
        for map in self.maps:
            map.draw_map(mapCanvas)


        while self.running:
            self.clock.tick(60)  # 60 fps

# ------------------------------------------------ TJEKKER FOR INPUT ---------------------------------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()

                self.player.checkInput(event)
                self.gun.checkInput(event)
                self.farm.checkInput(event)
                self.wave_manager.handle_event(event)
# ------------------------------------------------ OPDATERE TING OG SAGER ----------------------------------------------
            self.player.update()
            self.gun.update()
            self.camera.update()
            self.wave_manager.update()

            for bullet in self.bullets:
                bullet.update()
                for enemy in self.enemies:
                    if bullet.skud(enemy):
                        enemy.hit()
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)

            for enemy in self.enemies:
                enemy.update(self.player)

            self.enemies = [enemy for enemy in self.enemies if not enemy.dead]

            if not self.wave_start and (self.player.xVel != 0 or self.player.yVel != 0): #Hvis playeren bevæger sig kommer teksten frem
                self.wave_start = True
                self.wave_manager.start_waves()
                self.show_text = True
                self.wave_text_timer = pygame.time.get_ticks()

# ------------------------------------------------ TEGNER TING OG SAGER ------------------------------------------------
            self.canvas.blit(mapCanvas, (0, 0))
            self.farm.draw_farm(self.canvas)
            self.farm.draw_transparent_tile(self.canvas)

            for plant in self.plants:
                plant.update()
                plant.draw(self.canvas)

            for enemy in self.enemies:
                enemy.update(self.player)
                enemy.draw_enemy(self.canvas)

            for bullet in self.bullets:
                bullet.draw(self.canvas)

            self.player.draw_player(self.canvas)
            self.gun.draw_gun(self.canvas)

            # visualisere colliders
            # for collider in checkNearbyTiles(self.tile_size, self.scale, read_csv('Levels/MainLevel_Collision player.csv'), self.player.x + self.player.width, self.player.y + self.player.height, scanTiles=((0,-1), (-1, 0), (0, 1), (1, 0))):
            #    pygame.draw.rect(self.canvas, (255, 0, 0), pygame.Rect(collider.x, collider.y, collider.width, collider.height))
# ------------------------------------------------ FINDER SKÆRM OMRÅDE -------------------------------------------------
            self.screen_region = ((self.camera.getCameraPos()), pygame.display.get_window_size())  # området hvor skærmen er
            self.canvas.set_clip(pygame.Rect(self.screen_region))  # modificere pixels kun indenfor skærm området

            # ------------------------------------------------ PUTTER TEGNET TING OG SAGER PÅ SKÆRM --------------------------------
            self.window.blit(self.canvas, (0, 0), self.screen_region)  # tegner canvas på skærm og kun det område som kan ses
            # UI
            self.farm.drawUI(self.window)
            self.gun.drawUI(self.window)
            self.money_ui(self.window, f"Money: {self.money}", (0, 0, 0))

            if self.show_text:
                self.wave_text(self.window, f"Wave {self.wave_number}", (255, 0, 0))
                if pygame.time.get_ticks() - self.wave_text_timer > 1500:  # Viser hvor lang tid teksten skal være på skærmen
                    self.show_text = False

            pygame.display.update()  # updater skærm så disse ændringer kan ses

    def wave_text(self, surface, text, color):
        font = pygame.font.Font('freesansbold.ttf', 75)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.windowWidth // 2, self.windowHeight // 2))
        surface.blit(text_surface, text_rect)

    def money_ui(self, surface, text, color):
        font = pygame.font.Font('freesansbold.ttf', 45)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.windowWidth/2, 210 * self.scale))
        surface.blit(text_surface, text_rect)


    def start(self):
        self.running = True
        startCanvas = pygame.Surface((self.windowWidth, self.windowHeight))

        def start():  # Start funktion der starter spillet når der bliver trykket play.
            self.running = False
            self.run()
            self.gameover()
            quit()

        font = pygame.font.Font('freesansbold.ttf', 75)
        text = font.render("Storm the Farm", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (self.windowWidth // 2, self.windowHeight // 2 - 150)
        play_button = Button(self.windowWidth // 2 - 175, self.windowHeight // 2 - 25, 350, 75, "Play", False,(0, 200, 0), lambda: start())  # Play knap
        quit_button = Button(self.windowWidth // 2 - 175, self.windowHeight // 2 + 100, 350, 75, "Quit", False,(200, 0, 0), lambda: quit())  # Quit knap

        startCanvas.fill((255, 255, 255))
        while self.running:
            self.clock.tick(60)  # 60 fps

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
                play_button.update(event)
                quit_button.update(event)

            startCanvas.blit(text, textRect)
            play_button.draw(startCanvas)  # Tegner play
            quit_button.draw(startCanvas)  # Tegner quit

            self.window.blit(startCanvas, (0, 0))  # tegner canvas på skærm og kun område som kan ses
            pygame.display.update()  # updater skærm så disse ændringer kan ses

    def gameover(self):
        self.running = True
        startCanvas = pygame.Surface((self.windowWidth, self.windowHeight))


        def start():  # Start funktion der starter spillet når der bliver trykket play.
            self.running = False
            self.run()
            self.gameover()
            quit()

        font = pygame.font.Font('freesansbold.ttf', 75)
        text = font.render("The farm was stormed", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (self.windowWidth // 2, self.windowHeight // 2 - 150)
        try_again_button = Button(self.windowWidth // 2 - 175, self.windowHeight // 2 - 25, 350, 75, "Try Again", False,(0, 200, 0), lambda: start())  # Try again knap
        quit_button = Button(self.windowWidth // 2 - 175, self.windowHeight // 2 + 100, 350, 75, "Quit", False,(200, 0, 0), lambda: quit())  # Quit knap

        startCanvas.fill((255, 255, 255))
        while self.running:
            self.clock.tick(60)  # 60 fps

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
                try_again_button.update(event)
                quit_button.update(event)

            startCanvas.blit(text, textRect)
            try_again_button.draw(startCanvas)  # Tegner again
            quit_button.draw(startCanvas)  # Tegner quit

            self.window.blit(startCanvas, (0, 0))  # tegner canvas på skærm og kun område som kan ses
            pygame.display.update()  # updater skærm så disse ændringer kan ses


main = Main(pygame.display.Info().current_w, pygame.display.Info().current_h, 16 * 1.6, 9 * 1.6)
main.start()
pygame.quit()
