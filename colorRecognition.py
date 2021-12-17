"""
Считывает изображение с камеры и показывает цвет выделенной точки в HSV и BGR
В окне Camera показано изображение с камеры
Кликните мышкой на любую точку в окне
В левом верхнем левом углу будут BGR и HSV цвета в данной точке
В консоли выводятся координаты предыдущего клика\
Нажмите q для завершения
"""

import cv2
import numpy as np


position = []

cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)


def on_mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global position
        print(position)
        position = [y, x]


cv2.setMouseCallback("Camera", on_mouse_click)

measures = []
bgr_color = []
hsv_color = []
while cam.isOpened():
    _, image = cam.read()
    if position:
        pxl = image[position[0], position[1]]
        measures.append(pxl)
        if len(measures) >= 10:
            bgr_color = np.uint8([[np.average(measures, 0)]])
            hsv_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)
            bgr_color = bgr_color[0, 0]
            hsv_color = hsv_color[0, 0]
            measures.clear()
        cv2.circle(image, (position[1], position[0]),
                   7, (255, 127, 255), 3)
    cv2.putText(image, f"Color BGR = {bgr_color}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
    cv2.putText(image, f"Color HSV = {hsv_color}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))

    cv2.imshow("Camera", image)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
