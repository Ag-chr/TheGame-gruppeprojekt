import csv, os
from collider import Collider
import pygame


def read_csv(filename, dialect="excel"):
    map = []
    with open(os.path.join(filename)) as data:
        data = csv.reader(data, delimiter=',', dialect=dialect)
        for row in data:
            map.append(list(row))
    return map


def rectCollisionChecker(entityCollider, wallCollider, speedX=0, speedY=0, xObstructed=False, yObstructed=False):
    xFuture = entityCollider.x + speedX
    yFuture = entityCollider.y + speedY

    if entityCollider.x + entityCollider.width > wallCollider.x and entityCollider.x < wallCollider.x + wallCollider.width and yFuture + entityCollider.height > wallCollider.y and yFuture < wallCollider.y + wallCollider.height:
        yObstructed = True
    if entityCollider.y + entityCollider.height > wallCollider.y and entityCollider.y < wallCollider.y + wallCollider.height and xFuture + entityCollider.width > wallCollider.x and xFuture < wallCollider.x + wallCollider.width:
        xObstructed = True
    return xObstructed, yObstructed


def checkNearbyTiles(tile_size, scale, collisionMap, x, y, scanArea=(2, 2), scanTiles=None):
    real_tile_size = tile_size * scale
    scanWidth, scanHeight = scanArea[0], scanArea[1]
    nearbyColliders = []

    yGrid = int(y // real_tile_size)
    xGrid = int(x // real_tile_size)
    try:
        if scanTiles is None:
            for y in range(yGrid, yGrid + scanHeight):
                for x in range(xGrid, xGrid + scanWidth):
                    tileID = collisionMap[y][x]
                    if tileID == "-1": continue
                    nearbyColliders.append(Collider(tile_size, scale, x * real_tile_size, y * real_tile_size, tileID=tileID))
        else:
            for tile in scanTiles:
                y = tile[1] + yGrid
                x = tile[0] + xGrid

                tileID = collisionMap[y][x]
                if tileID == "-1": continue
                nearbyColliders.append(Collider(tile_size, scale, x * real_tile_size, y * real_tile_size, tileID=tileID))
        return nearbyColliders
    except:
        return []


def make_text(surface, text: str, pos: tuple[int, int], color, size):
    font = pygame.font.Font('freesansbold.ttf', size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=pos)
    surface.blit(text_surface, text_rect)
