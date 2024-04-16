import pygame
import shutil

class SpritesheetToJson:
    start = '{"frames": {'
    end = '\n}}'

    def __init__(self, image, tile_size):
        self.name = image[image.rfind("/") + 1:-4]
        self.tile_size = tile_size
        self.pathStart = __file__[:__file__.rfind("\\") + 1] + self.name + ".json"
        self.pathEnd = image.replace("png", "json")
        try:
            self.image = pygame.image.load(image).convert()
        except():
            print("could not convert")
            self.image = pygame.image.load(image)
        self.imageW = self.image.get_width()
        self.imageH = self.image.get_height()

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





if __name__ == "__main__":
    jsonFile = SpritesheetToJson("Images/water.png", 16)
