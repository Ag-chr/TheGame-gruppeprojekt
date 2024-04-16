from tiles import *
from spritesheet import Spritesheet
from spritesheetToJson import SpritesheetToJson
import pygame

pygame.init()
tile_size = 16


DISPLAY_W, DISPLAY_H = tile_size * 16 * 1.7777778, tile_size * 9 * 1.7777778

screenW, screenH = pygame.display.Info().current_w, pygame.display.Info().current_h
screenW, screenH = screenW / 2, screenH / 2 # til at teste
scale = screenW / DISPLAY_W

window = pygame.display.set_mode((screenW, screenH))
canvas = pygame.Surface((tile_size * 16 * 101, tile_size * 16 * 101))


running = True
clock = pygame.time.Clock()

SpritesheetToJson("Images/water.png", tile_size)
waterSpritesheet = Spritesheet('Images/water.png')

SpritesheetToJson("Images/grass.png", tile_size)
grassSpritesheet = Spritesheet('Images/grass.png')

SpritesheetToJson("Images/Wooden House.png", tile_size)
woodenHouseSpritesheet = Spritesheet('Images/Wooden House.png')


#player_img = spritesheet.parse_sprite(('Character.png'))
#player_rect = player_img.get_rect()

maps = [TileMap('Levels/MainLevel_Water.csv', waterSpritesheet, tile_size, scale),
        TileMap('Levels/MainLevel_Grass.csv', grassSpritesheet, tile_size, scale),
        TileMap('Levels/MainLevel_House floor.csv', woodenHouseSpritesheet, tile_size, scale),
        TileMap('Levels/MainLevel_House walls.csv', woodenHouseSpritesheet, tile_size, scale)]

#player_rect.x, player_rect.y = map.start_x, map.start_y

XOffset = tile_size * 101 /-2
YOffset = tile_size * 101 /-2
#XOffset = 0
#YOffset = 0

moveAmount = 100

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                YOffset += moveAmount
            if event.key == pygame.K_DOWN:
                YOffset -= moveAmount
            if event.key == pygame.K_LEFT:
                XOffset += moveAmount
            if event.key == pygame.K_RIGHT:
                XOffset -= moveAmount

    canvas.fill((0, 180, 240))
    for map in maps:
        map.draw_map(canvas)
    #canvas.blit(player_img, player_rect)
    window.blit(canvas, (XOffset, YOffset))
    pygame.display.update()

pygame.quit()