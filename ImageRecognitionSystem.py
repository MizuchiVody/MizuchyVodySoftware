from cv2 import *
from numpy import *
from imutils import *


def ProcessImage(img):
    # Preparing the image to be processed
    image = img  # copying the image to
    resized = resize(image, width=300)  # Resizing the image
    ratio = img.shape[0] / float(resized.shape[0])  # Getting the ratio of the original image versus the new image
    blurred = GaussianBlur(resized, (5, 5), 0)  # Adding Guassian Blur to the image to eliminate noise

    HSV = cvtColor(blurred, COLOR_BGR2HSV)  # Converting the image to HSV (Hue, Saturation, Intensity)color space

    # Determining the upper and lower boundaries for the colors
    # Blue
    lower_blue = array([90, 50, 50])
    upper_blue = array([170, 255, 255])
    # Yellow
    lower_yellow = array([13, 90, 90])
    upper_yellow = array([50, 255, 255])
    # Red
    lower_red = array([0, 80, 75])
    upper_red = array([10, 255, 255])

    # Threshing the image using upper and lower boundaries for the three colors
    hsvbluethresh = inRange(HSV, lower_blue, upper_blue)
    hsvyellowthresh = inRange(HSV, lower_yellow, upper_yellow)
    hsvredthresh = inRange(HSV, lower_red, upper_red)

    # Initializing a list containing the three threshed
    ThreshColors = [hsvbluethresh, hsvredthresh, hsvyellowthresh]

    color = {0: "Blue", 1: "Red", 2: "Yellow"}
    tailTri = {0: "C", 1: "A", 2: "B"}
    tailRect = {0: "F", 1: "D", 3: "E"}
    maxArea = 0
    shape = "Unknown"
    for i in range(0, 3):
        #  Finding the contours for each threshed image
        countours = findContours(ThreshColors[i].copy(), RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)
        countours = countours[0] if is_cv2() else countours[1]
        for cnt in countours:
            #  Approximating the contours to eliminate unnecessary points to make counting the number of sides for each
            #  shape more accurate
            approx = approxPolyDP(cnt, 0.02 * arcLength(cnt, True), True)
            #  Computing the area of the contours found
            area = contourArea(cnt)
            #  Getting the contour with the maximum area
            if (area > maxArea):
                #  Getting the number of sides for the contour with the maximum area
                l = len(approx)
                global cntA
                cntA = cnt
                #  determining which shape, color, tail section is detected
                if l == 3:
                    shape = "Triangle"

                elif l == 4:
                    shape = "Rectangle"

                tail = "Unknown"
                if shape == "Triangle":
                    tail = tailTri[i]
                elif shape == "Rectangle":
                    if i == 0:
                        tail = "F"
                    elif i == 1:
                        tail = "D"
                    else:
                        tail = "E"

        if shape != "Unknown" and tail != "Unknown":
            #  Computing the moment of the contour and the center to be able to draw the contour and write at its center
            M = moments(cntA)
            X = int((M["m10"] / M["m00"]) * ratio) if (M["m00"] != 0) else 0
            Y = int((M["m01"] / M["m00"]) * ratio) if (M["m00"] != 0) else 0
            cntA = cntA.astype("float")
            cntA *= ratio
            cntA = cntA.astype("int")
            #  Draw the contour around the shape detected and writing at its center the shape, color, and corresponding
            #  tail section
            drawContours(img, [cntA], 0, (0, 255, 0), 2)
            ans = color[i] + ' ' + shape + ' ' + tail
            putText(img=image, text=ans, org=(X, Y), fontFace=FONT_HERSHEY_DUPLEX, fontScale=1, color=(255, 255, 255),
                    thickness=2)
