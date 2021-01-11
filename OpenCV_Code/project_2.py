import cv2
import numpy as np

# to use webcam, use 0 parameter
cap = cv2.VideoCapture(0)
cap.set(3, 540)  # sets width, id #3 640 pixels
cap.set(4, 640)  # sets height, id #4 480 pixels
cap.set(10, 100)  # seSts brightness, 100 is kinda dim
###########################
widthImg = 540
heightImg = 640
###########################


def preProcessing(img):  # apply various preprocessing techniques
    # convert to grayscale explicitly, since most cv2 functions use 1-channel (ie grayscale)
    # if not explicitly done, cv2 will do it underhood for u, there's no real performance boost
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # why blur? cuz eliminates noise while edge detection
    imgBlur = cv2.GaussianBlur(
        imgGray, (5, 5), 1
    )  # apply a blur, higher sigma more blur
    imgCanny = cv2.Canny(  # find edges?
        imgBlur, 100, 100
    )  # if shadows or reflections, need dialte and kernel
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=2)
    imgThres = cv2.erode(imgDial, kernel, iterations=1)

    return imgThres


def getContours(img):
    biggest = np.array([])
    maxArea = 0
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  # how much to use? what is this threshold
            # draw contour, -1 for on contour, thickness 1
            peri = cv2.arcLength(cnt, True)  # closed to True
            # approximation of corner points
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)  # resolution = 0.2*peri
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    cv2.drawContours(
        imgContour, biggest, -1, (255, 0, 0), 20
    )  # last param controls size of dots
    print("biggest", biggest)
    return biggest


def getWarp(img, biggest):
    """
    warping needs 2 points, then get matrix, then get output
    """
    biggest = reorder(biggest)
    # print(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    warped_img = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

    return warped_img


def reorder(my_points):
    """
    biggest.shape = (4,1,2), 4 for 4 points, 2 for x and y, so 1 is redundant
    """
    try:
        my_points = my_points.reshape((4, 2))

        my_points_new = np.zeros((4, 1, 2), np.int32)
        add = my_points.sum(1)

        my_points_new[0] = my_points[
            np.argmin(add)
        ]  # find index of smallest, then get actual y and x to store
        my_points_new[3] = my_points[np.argmax(add)]

        diff = np.diff(my_points, axis=1)
        my_points_new[1] = my_points[np.argmin(diff)]
        my_points_new[2] = my_points[np.argmax(diff)]
        print("new points", my_points_new)

        return my_points_new
    except:
        return my_points


while True:
    # success is just a boolean that lets you know working or not
    # img is the video feed in this case
    success, img = cap.read()
    # img = cv2.imread("test.jpg")
    img = cv2.resize(img, (widthImg, heightImg))
    # cv2.resize(img, (widthImg, heightImg))
    imgContour = img.copy()
    imgThres = preProcessing(img)
    biggest = getContours(imgThres)

    if biggest.size != 0:
        imgWarped = getWarp(img, biggest)
        cv2.imshow("video", imgWarped)
    else:
        cv2.imshow("video", imgContour)
    if cv2.waitKey(1) & 0xFF == ord("q"):  # press 'q' to stop
        break
