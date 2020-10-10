# -*- coding: utf-8 -*-
import numpy as np
import time

WIDTH = 5
HEIGHT = 5
LOGO = '★'

PLAYGROUND = np.array(
    np.random.randint(1, 5, WIDTH*HEIGHT)
).reshape((HEIGHT, WIDTH))


def printPlayground():
    # print('\x1b[2J\x1b[u', end='')
    for line_index, line in enumerate(PLAYGROUND):
        for element in line:
            if element != -1:
                print('\x1b[{}m{}'.format(30+element, LOGO), end='')
            else:
                print('\x1b[{}m{}'.format(30, ' '), end='')
        print('\x1b[0m'+str(line_index))
    for i in range(WIDTH):
        print(i, end='')


def findSameColor(point, color=None, last_direction=(0, 0)):
    PLAYGROUND_FLAG = np.zeros_like(PLAYGROUND)
    direction = set([(0, 1), (0, -1), (1, 0), (-1, 0)])

    res = []
    next_points = set([point])
    color = PLAYGROUND[point[0], point[1]]
    while next_points:
        next_point = next_points.pop()
        PLAYGROUND_FLAG[next_point[0], next_point[1]] = 1
        if PLAYGROUND[next_point[0], next_point[1]] == color:
            res.append(next_point)
        for d in direction:
            next_point_ = tuple(map(lambda x, y: x+y, next_point, d))
            if next_point_[0] < 0 or next_point_[0] >= HEIGHT or next_point_[1] < 0 or next_point_[1] >= WIDTH:
                continue
            if PLAYGROUND_FLAG[next_point_[0], next_point_[1]] == 0 and PLAYGROUND[next_point_[0], next_point_[1]] == color:
                next_points.add(next_point_)
    return res


print('\x1b[2J\x1b[s', end='')
while True:
    printPlayground()
    point = input(" x,y=")
    point = tuple(map(lambda x: int(x), point.split(',')))
    wait_kill_point = findSameColor(point)
    if len(wait_kill_point) >= 2:
        for kill_point in wait_kill_point:
            PLAYGROUND[kill_point[0], kill_point[1]] = -1

        for time in range(HEIGHT-2, -1, -1):
            for h in range(time, -1, -1):
                for w in range(WIDTH):
                    if PLAYGROUND[h+1, w] == -1 and PLAYGROUND[h, w] != -1:
                        PLAYGROUND[h+1, w] = PLAYGROUND[h, w]
                        PLAYGROUND[h, w] = -1

        for w in range(WIDTH-1):
            if PLAYGROUND[HEIGHT-1, w] == -1:
                for h in range(HEIGHT):
                    PLAYGROUND[h, w] = PLAYGROUND[h, w+1]
                    PLAYGROUND[h, w+1] = -1
