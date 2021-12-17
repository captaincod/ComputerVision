"""
Изображение с камеры вставляется на картинку с выпуском новостей. Нажмите q для завершения программы
"""

import cv2
import numpy as np

news = cv2.imread("resources/news.jpg")

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cam.isOpened():
    raise RuntimeError("Camera not working")
ret, camera_image = cam.read()
rows, cols, _ = camera_image.shape
pts1 = np.float32([[0,0], [0, rows], [cols, 0], [cols, rows]])
pts2 = np.float32([[18, 24], [39, 297], [435, 51], [435, 270]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
print(matrix)
cv2.namedWindow("Image")
while True:
    ret, camera_image = cam.read()
    camera_image = cv2.flip(camera_image,1)
    aff_img = cv2.warpPerspective(camera_image, matrix, (cols, rows))
    aff_img = aff_img[:-150, :-150]
    gray = cv2.cvtColor(aff_img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

    roi = news[:aff_img.shape[0], :aff_img.shape[1]]
    mask_inv = cv2.bitwise_not(mask)

    bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    image = cv2.add(aff_img, bg)
    news[:image.shape[0], :image.shape[1]] = image
    cv2.imshow("Image", news)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cv2.destroyAllWindows()
cam.release()
