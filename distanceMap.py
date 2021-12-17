"""
Показывает на бинарном изображении расстояние от каждой точки объекта до ближайщего пикселя фона
Выводит исходное изображение и отредактированное, на котором чем дальше точка от границы - тем она более желтого цвета
Красной точкой отмечен пик изображения
В консоль выводится время, за которое вункция выполнялась до @numba.njit() и после его применения
"""

import time

import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label
from skimage.segmentation import watershed
from skimage import draw
import numba


def neighbors4(y, x):
    return (y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1)


def neighbors8(y, x):
    return (y - 1, x), (y - 1, x + 1), (y, x + 1), (y + 1, x + 1), (y + 1, x), (y + 1, x - 1), (y, x - 1), (
        y - 1, x - 1)


def get_ext_boundaries(image):
    pos = np.where(image)
    boundaries = set()
    for y, x in zip(*pos):
        for yn, xn in neighbors8(y, x):
            if image[yn, xn] == 0:
                boundaries.add((yn, xn))
    return boundaries


def cblock(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


@numba.njit()
def euclid(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


@numba.njit()
def dist_transform(image, zbounds):
    dmap = np.zeros_like(image)
    pos = np.where(image)
    for i, p1 in enumerate(zip(*pos)):
        # print(f"{i+1}/{len(pos[0])}")
        dists = [euclid(p1, p2) for p2 in zbounds]
        dmap[p1[0], p1[1]] = min(dists)
    return dmap


def find_peaks(dmap):
    peaks = []
    for i in range(1, dmap.shape[0] - 1):
        for j in range(1, dmap.shape[1] - 1):
            sub = dmap[i - 1:i + 2, j - 1:j + 2]
            if np.count_nonzero(sub < sub[1, 1]) == 8:
                peaks.append((i, j))
    return peaks


'''
Предыдущее изображение 

image = np.zeros((350, 350))
r, c = draw.rectangle((50, 50), (250, 250))
image[r, c] = 1

r, c = draw.disk((250, 250), 50)
image[r, c] = 1

r, c = draw.rectangle((200, 200), (100, 100))
image[r, c] = 1
'''
image = np.zeros((500, 500))

r, c = draw.rectangle((100, 150), (300, 200))
image[r, c] = 1

r, c = draw.rectangle((175, 200), (225, 300))
image[r, c] = 1

r, c = draw.rectangle((175, 300), (300, 400))
image[r, c] = 1

zbounds = get_ext_boundaries(image)
rr = [z[0] for z in zbounds]
cc = [z[1] for z in zbounds]
image[rr, cc] = 2

prev_time = time.time()
dmap = dist_transform(image, zbounds)
peaks = find_peaks(dmap)
y = [p[0] for p in peaks]
x = [p[1] for p in peaks]

markers = np.zeros_like(dmap)
markers[y, x] = 1
markers = label(markers)

segm = watershed(-dmap, markers=markers, mask=image)

curr_time = time.time()
print("ранее было 24.98870873451233")
print(f"а сейчас {curr_time - prev_time}")

plt.figure()
plt.imshow(dmap)
plt.scatter(x, y, c='red')
plt.figure()
plt.imshow(segm)
plt.show()
