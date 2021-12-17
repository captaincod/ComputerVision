"""
Сравнивает две картинки и ищет отличия
В окне Original на первой картинке показывает контуры отличий и пишет их количество в левом верхнем углу
В окне Difference белым на черном показаны отличия
"""

import cv2

cat = cv2.imread("resources/cat.png")

cat1 = cv2.cvtColor(cat, cv2.COLOR_BGR2GRAY)
cat2 = cv2.imread("resources/cat2.png", 0)

diff = cv2.absdiff(cat1, cat2)

thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.dilate(thresh, None, iterations=2)
contours, hierarchy = cv2.findContours(thresh.copy(),
                                       cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    (x, y, w, h) = cv2.boundingRect(cnt)
    cv2.rectangle(cat, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.putText(cat, f"Differences = {len(contours)}",
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0))

cv2.namedWindow("Original", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("Difference", cv2.WINDOW_KEEPRATIO)

cv2.imshow("Original", cat)
cv2.imshow("Difference", diff)
cv2.waitKey(0)
cv2.destroyAllWindows()
