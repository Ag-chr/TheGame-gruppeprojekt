import csv, os


def read_csv(filename):
    map = []
    with open(os.path.join(filename)) as data:
        data = csv.reader(data, delimiter=',')
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