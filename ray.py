import pygame
import math

pygame.init()


Map = [
    "##########",
    "#   r    #",
    "#        #",
    "#   #    #",
    "#    #   #",
    "#        #",
    "#        #",
    "##########"
]

colors = {
    '#': (100, 100, 100),
    'r': (200, 100, 100)
}

spawn = [3, 3]

root = pygame.display.set_mode((800, 600))

bsize = 50

x, y = spawn[0] * bsize, spawn[1] * bsize

angle = 90

maxs = 10000

mxbiss = maxs * math.cos(math.radians(45))

def draw_map(rot):
    for i in range(0, len(Map)):
        for j in range(0, len(Map[0])):
            if Map[i][j] == '#':
                pygame.draw.rect(rot, (100, 100, 100), (j * bsize, i * bsize, bsize, bsize))
            if Map[i][j] == 'r':
                pygame.draw.rect(rot, (200, 100, 100), (j * bsize, i * bsize, bsize, bsize))

def draw_player(rot, x, y):
    pygame.draw.circle(rot, (255, 0, 255), (x, y), bsize // 4)

def collide(x, y):
    if x < 0 or x // bsize >= len(Map[0]):
        return [True, 0]
    if y < 0 or y // bsize >= len(Map):
        return [True, 0]

    if (x % bsize <= 5 and y % bsize <= 5) and Map[y // bsize][x // bsize] in ['#', 'r']:
        return [-10,  Map[y // bsize][x // bsize]]
    if (bsize - (x % bsize) <= 5 and bsize - (y % bsize) <= 5) and Map[y // bsize][x // bsize] in ['#', 'r']:
        return [-10,  Map[y // bsize][x // bsize]]


    return [Map[y // bsize][x // bsize] in ['#', 'r'], Map[y // bsize][x // bsize]]


def check_rays(x, y, angle, fov=90 ,n=50, rot=None):
    rays = []

    i = angle

    while i <= angle + fov:

        x1, y1 = x, y
        step = 5
        newcollide = collide(x + int(step * math.cos(math.radians(i))), y + int(step * math.sin(math.radians(i))))

        while newcollide[0] == 0 and step < maxs and abs(step * math.cos(math.radians(abs(i - angle - 45)))) <= mxbiss:
            step += 5
            newcollide = collide(x + int(step * math.cos(math.radians(i))), y + int(step * math.sin(math.radians(i))))


        x1 = x + int(step * math.cos(math.radians(i)))
        y1 = y + int(step * math.sin(math.radians(i)))

        newcollide = collide(x + int(step * math.cos(math.radians(i))), y + int(step * math.sin(math.radians(i))))

        if newcollide[0] == -10:
            step = -step
            newcollide = collide(x + int(step * math.cos(math.radians(i))), y + int(step * math.sin(math.radians(i))))


        rays.append([step, newcollide[1]])

        #pygame.draw.line(rot, (10, 100, 10), (x, y), (x1, y1))
        i += fov / n


    draw_view(rays, 800, 600, 2)
    #return rays

    #quit()

def draw_view(rays, sx, sy, size, horizonty=None):
    root.fill((150, 100, 200))
    if horizonty == None:
        horizonty = sy // 2 - 100
    
    bx = sx / len(rays)
    by = sy / (maxs * 4)
    bufx = 4
    

    for i in range(0, len(rays)):   # sy - maxs        sy / maxs
        if rays[i][0] < 0:

            sz = int(maxs / rays[i][0])
            if -rays[i][0] < 255:
                color = (50, 50, 50)
            else:
                color = (0, 0, 0)

            pygame.draw.rect(root, color, (i * bx, horizonty + sz, bx + bufx, 2 * -sz))
            pygame.draw.rect(root, (50, 200, 50), (i * bx, horizonty + sz + 2 * -sz, bx + bufx, (sy - (horizonty + sz))))

        else:

            sz = int(maxs / rays[i][0])

            if rays[i][0] > 255:
                color = (0, 0, 0)
            else:
                color = [255 - rays[i][0], 255 - rays[i][0], 255 - rays[i][0]]
                if rays[i][1] == 'r' and color[0] + 100 < 256:
                    color[0] = (color[0] + 100) % 256
            if rays[i][0] > 0:



                pygame.draw.rect(root, color, (i * bx,  horizonty - sz, bx + bufx, sz * 2))
                pygame.draw.rect(root, (50, 200, 50), (i * bx + bufx, horizonty - sz + 2 * sz, bx + bufx, (sy - (horizonty - sz))))


            

    
    


clock = pygame.time.Clock()

while 1:
    root.fill((50, 50, 100))
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            quit()

    k = pygame.key.get_pressed()
    if k[pygame.K_UP]:
        if collide(x + int(5 * math.cos(math.radians((angle + 45)))), y + int(5 * math.sin(math.radians((angle + 45)))))[0] == 0:
            x += int(5 * math.cos(math.radians((angle + 45))))
            y += int(5 * math.sin(math.radians((angle + 45))))

    if k[pygame.K_DOWN]:
        if collide(x - int(5 * math.cos(math.radians((angle + 45)))), y - int(5 * math.sin(math.radians((angle + 45)))))[0] == 0:
            x -= int(5 * math.cos(math.radians((angle + 45))))
            y -= int(5 * math.sin(math.radians((angle + 45))))
    if k[pygame.K_LEFT]:
        angle = (angle - 5) % 360
    if k [pygame.K_RIGHT]:
        angle = (angle + 5) % 360
    
    
    check_rays(x, y, angle, 90, 90, root)
    if k[pygame.K_m]:
        draw_player(root, x, y)
        draw_map(root)
    pygame.display.update()
    #angle = (angle + 5) % 360
    clock.tick(30)