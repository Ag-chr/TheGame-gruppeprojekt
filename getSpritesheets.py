from spritesheetToJson import SpritesheetToJson
from spritesheet import Spritesheet
import pygame

pygame.display.set_mode()

waterSpritesheet = Spritesheet('Images/water.png')
grassSpritesheet = Spritesheet('Images/grass.png')
woodenHouseSpritesheet = Spritesheet('Images/Wooden House.png')
collisionSpritesheet = Spritesheet("Images/collision.png")
playerSpritesheet = Spritesheet("Images/character.png")
farmSpritesheet = Spritesheet("Images/tilled dirt.png")
enemySpritesheet = Spritesheet("Images/kylling.png")
goblinSpritesheet = Spritesheet("Images/goblin.png")


pygame.quit()

def updateJson(tile_size):
    SpritesheetToJson("Images/kylling.png", tile_size)
    SpritesheetToJson("Images/tilled dirt.png", tile_size)
    SpritesheetToJson("Images/water.png", tile_size)
    SpritesheetToJson("Images/grass.png", tile_size)
    SpritesheetToJson("Images/Wooden House.png", tile_size)
    SpritesheetToJson("Images/collision.png", tile_size)
    SpritesheetToJson("Images/character.png", tile_size, 16, (16, 16), (16, 16))
    SpritesheetToJson("Images/goblin.png", tile_size)



