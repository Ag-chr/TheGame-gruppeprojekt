from tiles import *
from spritesheet import Spritesheet
import spritesheetToJson

pygame.init()
tile_size = 16
DISPLAY_W, DISPLAY_H = tile_size * 32, tile_size * 18

screenW, screenH = pygame.display.Info().current_w, pygame.display.Info().current_h
screenW, screenH = screenW / 2, screenH / 2 # til at teste
scale = screenW / DISPLAY_W

window = pygame.display.set_mode((screenW, screenH))
canvas = pygame.Surface((screenW, screenH))


running = True
clock = pygame.time.Clock()

grassSpritesheet = Spritesheet('Images/grass.png')
spritesheetToJson.SpritesheetToJson("grass", "Images/grass.png", tile_size)

#player_img = spritesheet.parse_sprite(('Character.png'))
#player_rect = player_img.get_rect()

map = TileMap('Levels/test_level_1_Grass.csv', grassSpritesheet, tile_size, scale)
#player_rect.x, player_rect.y = map.start_x, map.start_y

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False



    canvas.fill((0, 180, 240))
    map.draw_map(canvas)
    #canvas.blit(player_img, player_rect)
    window.blit(canvas, (0, 0))
    pygame.display.update()

pygame.quit()