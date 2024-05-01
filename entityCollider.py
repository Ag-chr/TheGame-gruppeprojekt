from hjælpeFunktioner import read_csv, checkNearbyTiles, rectCollisionChecker
from collider import Collider


class EntityCollider:
    def __init__(self, main, x, y, xOffset, yOffset, width, height, speed, collisionMap, scanArea=(2,2)):
        self.main = main
        self.xOffset = xOffset * self.main.scale
        self.yOffset = yOffset * self.main.scale
        self.width = width * self.main.scale
        self.height = height * self.main.scale
        self.speed = speed * self.main.scale

        self.x = x - (self.xOffset + self.width) / 2
        self.y = y - (self.xOffset + self.width) / 2

        self.xVel = 0
        self.yVel = 0
        self.collisionMap = read_csv(collisionMap)
        self.scanArea = scanArea

        self.collider = Collider(tile_size=self.main.tile_size, scale=self.main.scale, x=self.x + self.xOffset, y=self.y + self.yOffset, width=self.width, height=self.height)

    def checkCollision(self) -> (bool, bool):
        self.collider.x, self.collider.y = self.x + self.xOffset, self.y + self.yOffset
        xObstructed = False
        yObstructed = False

        nearbyColliders = checkNearbyTiles(self.main.tile_size, self.main.scale, self.collisionMap, self.x, self.y, scanArea=self.scanArea)
        for collider in nearbyColliders:
            xObstructed, yObstructed = rectCollisionChecker(self.collider, collider, self.xVel, self.yVel, xObstructed, yObstructed)

        return xObstructed, yObstructed

