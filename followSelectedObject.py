"""
Считывает изображение с камеры и следит за выделенным объектом
В окне Camera показано изображение с камеры
Нажмите r (с английской раскладкой). В окне ROI selection будет зафиксированное изображение.
Выделите мышкой объект, который хотите отслеживать. Нажмите Enter.
Теперь в окне ROI показан отслеживаемый объект, а в Camera будут видны его контуры
Нажмите q для завершения
"""

import cv2

cam = cv2.VideoCapture(0)

cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("ROI", cv2.WINDOW_KEEPRATIO)

roi = None
while cam.isOpened():

    _, image = cam.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if roi is not None:
        # тут сидит фурье и смотрит, похоже ли изображение
        res = cv2.matchTemplate(gray, roi, cv2.TM_CCORR_NORMED)
        # cv2.imshow("Match template", res)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + roi.shape[1],
                        top_left[1] + roi.shape[0])
        cv2.rectangle(image, top_left, bottom_right, 255, 2)

    cv2.imshow("Camera", image)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('r'):
        r = cv2.selectROI("ROI selection", gray)
        roi = gray[int(r[1]): int(r[1] + r[3]),
                   int(r[0]): int(r[0] + r[2])]
        cv2.imshow("ROI", roi)
        cv2.destroyWindow("ROI selection")

cam.release()
cv2.destroyAllWindows()
