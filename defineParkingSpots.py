# press escape to finish doing real time boxing.
# Program marks the polygons in the figure when it gets 4 double clicks
import cv2
import yaml
import numpy as np

refPt = []
cropping = False
data = []
file_path = 'parking_spots.yml'
img = cv2.imread('randomParkingLot.png')


def yaml_loader(file_path):
    with open(file_path, "r") as file_descr:
        data = yaml.safe_load(file_descr)
        return data


def yaml_dump(file_path, data):
    with open(file_path, "a") as file_descr:
        yaml.safe_dump(data, file_descr)


def yaml_dump_write(file_path, data):
    with open(file_path, "w") as file_descr:
        yaml.safe_dump(data, file_descr)


def draw_existing_spots():

    data = yaml_loader(file_path)
    if data is not None:
        for x in range(len(data)):
            print("Drawing spot ID " + str(data[x]['id']))
            refPt = data[x]['points']
            cv2.line(image, refPt[0], refPt[1], (0, 255, 0), 1)
            cv2.line(image, refPt[1], refPt[2], (0, 255, 0), 1)
            cv2.line(image, refPt[2], refPt[3], (0, 255, 0), 1)
            cv2.line(image, refPt[3], refPt[0], (0, 255, 0), 1)


def click_and_crop(event, x, y, flags, param):
    current_pt = {'id': 0, 'points': []}
    # grab references to the global variables
    global refPt, cropping
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt.append((x, y))
        cropping = False
    if len(refPt) == 4:
        if data == []:
            if yaml_loader(file_path) != None:
                data_already = len(yaml_loader(file_path))
            else:
                data_already = 0
        else:
            if yaml_loader(file_path) != None:
                data_already = len(data) + len(yaml_loader(file_path))
            else:
                data_already = len(data)

        cv2.line(image, refPt[0], refPt[1], (0, 255, 0), 1)
        cv2.line(image, refPt[1], refPt[2], (0, 255, 0), 1)
        cv2.line(image, refPt[2], refPt[3], (0, 255, 0), 1)
        cv2.line(image, refPt[3], refPt[0], (0, 255, 0), 1)

        temp_lst1 = list(refPt[2])
        temp_lst2 = list(refPt[3])
        temp_lst3 = list(refPt[0])
        temp_lst4 = list(refPt[1])

        current_pt['points'] = [temp_lst1, temp_lst2, temp_lst3, temp_lst4]
        current_pt['id'] = data_already
        data.append(current_pt)
        # data_already+=1
        refPt = []


#image = cv2.resize(img, None, fx=0.6, fy=0.6)
image = img
clone = image.copy()
cv2.namedWindow("Double click to mark points")
cv2.imshow("Double click to mark points", image)
cv2.setMouseCallback("Double click to mark points", click_and_crop)

draw_existing_spots()
# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    cv2.imshow("Double click to mark points", image)
    key = cv2.waitKey(1) & 0xFF
    if cv2.waitKey(33) == 27:
        break

# data list into yaml file
if data != []:
    yaml_dump(file_path, data)
cv2.destroyAllWindows()  # important to prevent window from becoming inresponsive
