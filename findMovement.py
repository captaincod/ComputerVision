"""
Считывает изображение с камеры и ищет движение
В окне Camera изображение с камеры и контуры изменяющихся (двигающихся) объектов
В окнах Background и Thresh показаны движущиеся объекты
Если движения не замечено, в консоль будет выводится "Update background!"
Нажмите b (с английской раскладкой), чтобы зафиксировать изображение на Background и Thresh
Нажмите q для завершения
"""
import cv2
import numpy as np

cam = cv2.VideoCapture(0)

cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("Background", cv2.WINDOW_KEEPRATIO)

background = None
prev_gray = None
buffer = []
frames = 0
while cam.isOpened():

    _, image = cam.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    key = cv2.waitKey(1)
    if frames % 20 == 0:
        if prev_gray is not None:
            diff = prev_gray - gray
            buffer.append(diff.mean())
    if len(buffer) > 20:
        buffer.pop(0)
        std = np.std(buffer)
        if std < 50:
            print("Update background!")
            background = gray.copy()

    """
    if prev_gray is not None:
        diff = prev_gray - gray
        mx = np.max(diff)
        if mx < 27:
            background = gray.copy()
    """
    if key == ord('q'):
        break
    if key == ord('b'):
        background = gray.copy()
    if background is not None:
        delta = cv2.absdiff(background, gray)
        thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 300:  # изменяемое значение
                (x, y, w, h) = cv2.boundingRect(cnt)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Thresh", thresh)
        cv2.imshow("Background", delta)
    cv2.imshow("Camera", image)
    prev_gray = gray

cam.release()
cv2.destroyAllWindows()
