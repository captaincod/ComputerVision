"""
Выводит объект на изображении, для которого задали цвет (нижние и верхние его границы)
В данном примере выводит красный бутон розы
"""

import cv2
import numpy as np

rose = cv2.imread("resources/rose.jpg")

hsv = cv2.cvtColor(rose, cv2.COLOR_BGR2HSV)
lower = np.array([0, 200, 100])
upper = np.array([0, 255, 255])

mask = cv2.inRange(hsv, lower, upper)
res = cv2.bitwise_and(rose, rose, mask=mask)

cv2.namedWindow("Image", cv2.WINDOW_KEEPRATIO)
cv2.imshow("Image", res)
cv2.waitKey(0)
cv2.destroyAllWindows()
