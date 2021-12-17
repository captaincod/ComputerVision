"""
Считывает balls.png и выводит график, на котором уровни показывают количество цветов на картинке
"""

import matplotlib.pyplot as plt
import numpy as np
from skimage import color


image = plt.imread('resources/balls.png')
image = color.rgb2hsv(image)

plt.figure()
plt.subplot(121)
plt.imshow(image)
plt.subplot(122)
plt.plot(np.unique(image[:, :, 0]), 'o')
plt.plot(np.diff(np.unique(image[:, :, 0])))

plt.show()
