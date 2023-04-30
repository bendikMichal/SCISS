import pygame, time, sys
from random import *
from math import *
pygame.init()

clock = pygame.time.Clock()
fps = 60

width, height = 960, 640
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sciss")

size = 32 
images = {
    "scissors" : pygame.transform.scale(pygame.image.load("images/scissors.png").convert_alpha(), (size, size)),
    "paper" : pygame.transform.scale(pygame.image.load("images/paper.png").convert_alpha(), (size, size)),
    "rock" : pygame.transform.scale(pygame.image.load("images/rock.png").convert_alpha(), (size, size))
}

types = [
    "scissors",
    "paper",
    "rock"
]

wanted = {
    "scissors": "paper",
    "paper": "rock",
    "rock": "scissors"
} 

entities_num = 50
slowness = 1#5
things = [[[randint(0, width), randint(0, height)], choice(types), i] for i in range (entities_num)]

def dist (a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def ct(a, b, r):
    return dist(a, b) < r

main = True

while main:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main = False

    key = pygame.key.get_pressed()

    if key[pygame.K_r]:
        things = [[[randint(0, width), randint(0, height)], choice(types), i] for i in range (entities_num)]

    win.fill((0, 0, 0))

    for t in things:
        hitb_col = (255, 0, 0)

        target = None
        found = False
        for tt in things: 
            if ct(t[0], tt[0], size) and t[2] != tt[2] and t[1] != tt[1]:
                hitb_col = (0, 255, 0)
                if t[1] == wanted[tt[1]]:
                    t[1] = tt[1]
                    # things.remove(t)
                else:
                    tt[1] = t[1]
                    # things.remove(tt)

            if tt[1] == wanted[t[1]]:
                target = [0, 0]
                if dist(t[0], target) > dist(t[0], tt[0]) or not found:
                    target = tt[0].copy()
                    found = True


        if target is None:
            target = [width / 2, height / 2]

        mx = (target[0] - t[0][0])
        my = (target[1] - t[0][1])
        
        if mx != 0 and my != 0:
            # suspect a problem with not matching angles
            angle = atan2(my, mx)
            amx = cos(angle) / slowness
            amy = sin(angle) / slowness

            for ttt in things: 
                if ct([t[0][0] + amx, t[0][1] + amy], ttt[0], size) and t[2] != ttt[2]:
                    if t[0][0] < ttt[0][0]:
                        t[0][0] = ttt[0][0] - size / 2
                    if t[0][0] > ttt[0][0]:
                        t[0][0] = ttt[0][0] + size / 2

                    if t[0][1] < ttt[0][1]:
                        t[0][1] = ttt[0][1] - size / 2
                    if t[0][1] > ttt[0][1]:
                        t[0][1] = ttt[0][1] + size / 2

            t[0][0] += amx
            t[0][1] += amy

            if t[0][0] < 0:
                t[0][0] = 0
            if t[0][0] > width:
                t[0][0] = width

            if t[0][1] < 0:
                t[0][1] = 0
            if t[0][1] > height:
                t[0][1] = height


        win.blit(images[t[1]], [t[0][0] - size / 2, t[0][1] - size / 2])
        # pygame.draw.circle(win, hitb_col, t[0], size / 2, 1)
        # pygame.draw.line(win, hitb_col, t[0], [t[0][0] + amx * 40, t[0][1] + amy * 40], 2)

    pygame.display.update()


pygame.quit()
sys.exit()
