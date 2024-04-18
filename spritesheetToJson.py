import pygame
import shutil

class SpritesheetToJson:
    start = '{"frames": {'
    end = '\n}}'

    def __init__(self, image, tile_size, spacing=0, startPos=(0, 0), endPos=(0, 0)):
        self.name = image[image.rfind("/") + 1:-4]
        self.tile_size = tile_size
        self.spacing = spacing
        self.startPos = startPos
        self.endPos = endPos
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
        amount_of_rows = (self.imageH - self.startPos[0] - self.endPos[0]) // (self.tile_size + self.spacing)
        amount_of_columns = (self.imageW  - self.startPos[1] - self.endPos[1]) // (self.tile_size + self.spacing)

        iteration = 0
        with open(self.name + ".json", "w") as file:
            file.write(self.start)
            for y in range(amount_of_rows):
                for x in range(amount_of_columns):
                    needKomma = ",\n"
                    if iteration == amount_of_rows * amount_of_columns - 1:
                        needKomma = ""

                    file.write(self.jsonIteration(x * self.tile_size + x * self.spacing + self.startPos[0],
                                                  y * self.tile_size + y * self.spacing + self.startPos[1],
                                                  self.tile_size, iteration) + needKomma)
                    iteration += 1
            file.write(self.end)

        shutil.move(self.pathStart, self.pathEnd)





if __name__ == "__main__":
    jsonFile = SpritesheetToJson("Images/water.png", 16)
