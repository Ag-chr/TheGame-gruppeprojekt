class Collider:
    def __init__(self, main, tilenum, x, y):
        self.main = main
        self.x = x
        self.y = y
        self.width = main.tile_size * main.scale
        self.height = main.tile_size * main.scale
        if tilenum == "0":
            self.x += 11 * main.scale  # flytter 11 pixel fremad fordi tile starter ikke oppe i venstre hjørne
            self.width = 5 * main.scale
        elif tilenum == "1":
            pass
        elif tilenum == "2":
            self.width = 5 * main.scale

    def __str__(self):
        return f"x: {self.x}, y: {self.y}\nwidth: {self.width}, height: {self.height}"
