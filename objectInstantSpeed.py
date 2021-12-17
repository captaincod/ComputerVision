"""
Считывает изображение с камеры и выводит мгновенную скорость объекта с заданным уветом
В lower и upper необходимо задать нижние и верхние границы HSV-цвета отслеживаемого объекта
в формате lower = (H_low, S_low, V_low); upper = (H_up, 255, 255)
В окне Camera будет виден контур отслеживаемого объекта и значение его мгновенной скорости
В окне Mask можете отслеживать маску заданного цвета на изображении,
чтобы откорректировать границы и не считывать слишком много точек
"""

import cv2
import time

cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)

# for yellow ball
lower = (0, 200, 150)
upper = (5, 255, 255)

prev_time = time.time()
curr_time = time.time()
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0
d = 5.6 * 10 ** -2  # m
radius = 1

while cam.isOpened():
    _, image = cam.read()
    curr_time = time.time()
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 0:
        # контур с максимальной площадью
        c = max(cnts, key=cv2.contourArea)
        (curr_x, curr_y), radius = cv2.minEnclosingCircle(c)
        if radius > 10:
            cv2.circle(image, (int(curr_x), int(curr_y)), 5,
                       (0, 255, 255), 2)
            cv2.circle(image, (int(curr_x), int(curr_y)), int(radius),
                       (0, 255, 255), 2)

    time_diff = curr_time - prev_time
    pxl_per_m = d / radius
    dist = ((prev_x - curr_x) ** 2 + (prev_y - curr_y) ** 2) ** 0.5
    # print(dist)
    speed = dist / time_diff * pxl_per_m
    cv2.putText(image, "Speed = {0:.5f}m/s".format(speed),
                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0, 255, 255), 2)
    cv2.imshow("Camera", image)
    cv2.imshow("Mask", mask)
    prev_time = curr_time
    prev_x = curr_x
    prev_y = curr_y

    key = cv2.waitKey(1)
    if key == ord('q'):
        break


cam.release()
cv2.destroyAllWindows()
