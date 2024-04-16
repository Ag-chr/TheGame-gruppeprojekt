import pygame
import shutil

class SpritesheetToJson:
    start = '{"frames": {'
    end = '\n}}'

    def __init__(self, name, image, tile_size):
        self.name = name
        self.tile_size = tile_size
        self.pathStart = __file__[:__file__.rfind("\\") + 1] + name + ".json"
        self.pathEnd = image.replace("png", "json")
        self.image = pygame.image.load(image).convert()
        self.imageW = self.image.get_width()
        self.imageH = self.image.get_height()
        print(self.imageW // 16, self.imageH // 16)

        self.makeJsonFile()


    def jsonIteration(self, x, y, size, iteration):
        return """
"%s%i.png":
  {
    "frame": {"x": %i,"y": %i,"w": %i,"h": %i},
    "rotated": false,
    "trimmed": false,
    "spriteSourceSize": {"x": %i,"y": %i,"w": %i,"h": %i},
    "sourceSize": {"w": %i, "h": %i}
  }""" % (self.name, iteration, x, y, size, size, x, y, size, size, size, size)

    def makeJsonFile(self):
        iteration = 0
        with open(self.name + ".json", "w") as file:
            file.write(self.start)
            for y in range(self.imageH // self.tile_size):
                for x in range(self.imageW // self.tile_size):
                    needKomma = ",\n"
                    if iteration == self.imageH // self.tile_size * self.imageW // self.tile_size - 1:
                        needKomma = ""

                    file.write(self.jsonIteration(x * self.tile_size, y * self.tile_size, self.tile_size, iteration) + needKomma)
                    iteration += 1
            file.write(self.end)

        shutil.move(self.pathStart, self.pathEnd)






# jsonFile = SpritesheetToJson("grass", "Images/grass.png", 16)
