import cv2
import numpy as np

coordinates = []
WIN_NAME = 'Perspective'


def get_coordinate(event, x, y, flags, params):
    # print(event)
    if event == cv2.EVENT_LBUTTONDOWN:
        coordinates.append([x, y])
        # if len(coordinates) == 4:
        #     cv2.destroyWindow('Select Cords')


def get_zero_cordinates(listOfPoints):
    newPoints = []
    # print(listOfPoints)
    x = listOfPoints[0][0]
    y = listOfPoints[0][1]
    newPoints.append([0, 0])
    newPoints.append([listOfPoints[1][0] - x, 0])
    newPoints.append([0, listOfPoints[2][1] - y])
    # for point in listOfPoints[0:3]:
    #     newPoints.append([max((point[0] - x), 0), max((point[1] - y), 0)])
    newPoints.append([newPoints[1][0], newPoints[2][1]])
    return newPoints


def get_new_size(points):
    x = max([point[0] for point in points])
    y = max([point[1] for point in points])
    return x, y


def main():
    originalPoints=''
    srcImg = cv2.imread(r"C:\Users\ankitaa\Desktop\ADP Sample.jpg")
    if srcImg is None:
        print('Image Not found.')
        exit(0)
    cv2.namedWindow('Select Cords')
    cv2.setMouseCallback('Select Cords', get_coordinate)
    cv2.imshow('Select Cords', srcImg)
    cv2.waitKey(0)
    if len(coordinates) == 4:
        # cv2.destroyWindow('Select Cords')
        originalPoints = coordinates.copy()
        coordinates.clear()
        # break
    newPoints = get_zero_cordinates(originalPoints)
    npOgPnts = np.float32(originalPoints)
    npNwPnts = np.float32(newPoints)
    # npNwPnts = np.float32([[0,0],[300,0],[0,300],[300,300]])
    print(npOgPnts, '\n', npNwPnts)
    w, h = get_new_size(npNwPnts)
    perspectiveTransformMatrix = cv2.getPerspectiveTransform(npOgPnts, npNwPnts)
    result = cv2.warpPerspective(srcImg, perspectiveTransformMatrix, (w, h))
    cv2.imshow('result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
