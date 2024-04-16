import pygame, csv, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self) #initiates pygame.sprite class
        self.image = spritesheet.parse_sprite(image) # stores images
        # Manual load in: self.image = pygame.image.load(image)
        self.rect = self.image.get_rect() # makes image into rectangle object
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self, filename, spritesheet, tile_size, rescale):
        self.rescale = rescale
        self.tile_size = tile_size * rescale # size of tiles in pixels
        self.start_x, self.start_y = 0,0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0, 0))

    def load_map(self):
        for tile in self.tiles:
            tile.image = pygame.transform.scale_by(tile.image, self.rescale)
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        spritesheetName = self.spritesheet.filename[self.spritesheet.filename.rfind("/") + 1:-4]
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                #if map[y][x] == "-1":
                    #continue
                try:
                    tiles.append(Tile(f'{spritesheetName}{map[y][x]}.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                except:
                    pass
                    # Move to next tile in current row
                x += 1
                # Move to next row
            y += 1
            # Store the size of the tile map
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles
