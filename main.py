from tiles import *
from spritesheet import Spritesheet
from spritesheetToJson import SpritesheetToJson
import pygame

pygame.init()
running = True
clock = pygame.time.Clock()
tile_size = 16
DISPLAY_W, DISPLAY_H = tile_size * 16 * 2, tile_size * 9 * 2

gameWindowWidth, gameWindowHeight = pygame.display.Info().current_w, pygame.display.Info().current_h
#gameWindowWidth, gameWindowHeight = gameWindowWidth / 2, gameWindowHeight / 2 # til at teste
scale = gameWindowWidth / DISPLAY_W
window = pygame.display.set_mode((gameWindowWidth, gameWindowHeight))

SpritesheetToJson("Images/water.png", tile_size)
waterSpritesheet = Spritesheet('Images/water.png')

SpritesheetToJson("Images/grass.png", tile_size)
grassSpritesheet = Spritesheet('Images/grass.png')

SpritesheetToJson("Images/Wooden House.png", tile_size)
woodenHouseSpritesheet = Spritesheet('Images/Wooden House.png')

maps = [TileMap('Levels/MainLevel_Water.csv', waterSpritesheet, tile_size, scale),
        TileMap('Levels/MainLevel_Grass.csv', grassSpritesheet, tile_size, scale),
        TileMap('Levels/MainLevel_House floor.csv', woodenHouseSpritesheet, tile_size, scale),
        TileMap('Levels/MainLevel_House walls.csv', woodenHouseSpritesheet, tile_size, scale)]

canvas = pygame.Surface((maps[0].map_w, maps[0].map_h))

# player_img = spritesheet.parse_sprite(('Character.png'))
# player_rect = player_img.get_rect()
# player_rect.x, player_rect.y = map.start_x, map.start_y


XOffset = maps[0].map_w / 2 - gameWindowWidth / 2
YOffset = maps[0].map_h / 2 - gameWindowHeight / 2
moveAmount = 2.5 * scale
MoveX = 0
MoveY = 0

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                MoveY = -moveAmount
            if event.key == pygame.K_DOWN:
                MoveY = moveAmount
            if event.key == pygame.K_LEFT:
                MoveX = -moveAmount
            if event.key == pygame.K_RIGHT:
                MoveX = moveAmount

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                MoveY = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                MoveX = 0
    XOffset += MoveX
    YOffset += MoveY

    canvas.fill((0, 180, 240))
    for map in maps:
        map.draw_map(canvas)
    #canvas.blit(player_img, player_rect)

    canvas.set_clip(pygame.Rect((XOffset, YOffset), pygame.display.get_window_size()))
    screen_region = ((XOffset, YOffset), pygame.display.get_window_size())

    window.blit(canvas, (0, 0), screen_region)
    pygame.display.update()

pygame.quit()