import cv2
import cvzone
import numpy as np
import yaml

# Video feed
#cap = Image.open(r"carParkImg.png")
cap = cv2.VideoCapture('randomParkingLot.mov')

with open(r'parking_spots.yml') as file:
    # with open('CarParkPos', 'rb') as f:
    posList = yaml.load(file, Loader=yaml.FullLoader)
    print(posList)


def croppedImage(image, x1, y1, x2, y2, x3, y3, x4, y4):
    img = image.copy()
    mask = np.zeros(img.shape[0:2], dtype=np.uint8)
    points = np.array(
        [[[x1, y1], [x2, y2], [x3, y3], [x4, y4]]])
    # method 1 smooth region
    cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA)
    # method 2 not so smooth region
    # cv2.fillPoly(mask, points, (255))
    res = cv2.bitwise_and(img, img, mask=mask)
    rect = cv2.boundingRect(points)  # returns (x,y,w,h) of the rect
    cropped = res[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]
    return cropped


def checkParkingSpace(imgPro):
    spaceCounter = 0

    for pos in posList:
        x2 = pos['points'][0][0]
        x1 = pos['points'][2][0]
        y2 = pos['points'][0][1]
        y1 = pos['points'][2][1]
        pts = np.array(pos['points'], np.int32)
        # print(x1)
        # print(x2)
        # print(y1)
        # print(y2)
        # print('...')
        # print(pos['points'][0][0])
        #imgCrop = imgPro.crop((left, top, right, bottom))
        #imgCrop = imgPro[y1:y2, x1:x2]
        imgCrop = croppedImage(imgPro, pos['points'][0][0], pos['points'][0][1], pos['points'][1][0], pos['points'][1][1], pos['points']
                               [2][0], pos['points'][2][1], pos['points'][3][0], pos['points'][3][1])
        cv2.imshow("imgCrop", imgCrop)
        count = cv2.countNonZero(imgCrop)
        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2
        isClosed = True
        cv2.polylines(img, [pts], isClosed, color, thickness)
        #cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
        cvzone.putTextRect(img, str(count), (pos['points'][0][0], pos['points'][0][1] - 3), scale=1,
                           thickness=2, offset=0, colorR=color)
    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                       thickness=5, offset=20, colorR=(0, 200, 0))


while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img)
    # cv2.imshow("ImageBlur", imgBlur)
    # cv2.imshow("ImageThres", imgMedian)
    cv2.waitKey(10)
